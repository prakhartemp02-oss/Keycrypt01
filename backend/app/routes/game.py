"""Game API endpoints"""

import uuid
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from sqlalchemy.exc import SQLAlchemyError

from .. import db
from ..models.game import Game, GameAttempt, WordDictionary, UserProgress
from ..models.user import User
from ..ciphers import get_cipher
from ..utils.validation import (
    sanitize_guess, validate_level, validate_game_id,
    sanitize_dictionary_category, validate_user_id
)
from ..utils.crypto import hash_key_material

game_bp = Blueprint('game', __name__)

@game_bp.route('/new-game', methods=['POST'])
def new_game():
    """
    Start a new game session

    Request:
    {
        "level": 3,
        "dictionary_category": "animals",
        "user_id": "optional-player-id"
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON request'}), 400

        # Validate and parse request
        level = data.get('level')
        validate_level(level)

        dictionary_category = sanitize_dictionary_category(data.get('dictionary_category'))
        user_id = validate_user_id(data.get('user_id'))

        # Get or create user
        if user_id:
            user = User.get_or_create_guest(user_id)
        else:
            user = User.create_guest_user()
            db.session.add(user)

        # Select a random word
        word_entry = WordDictionary.get_random_word(level, dictionary_category)
        if not word_entry:
            # Fallback: create a simple word
            word_entry = _create_fallback_word(level)

        secret_word = word_entry.word

        # Initialize cipher for this level
        cipher = get_cipher(level)
        if not cipher:
            return jsonify({'error': f'Cipher not found for level {level}'}), 400

        # Generate keys and encrypt the secret word
        cipher_keys = cipher.generate_keys()
        ciphertext = cipher.encrypt(secret_word)

        # Generate encrypted hints
        hints = {
            'length': cipher.encrypt(str(len(secret_word))),
            'first_letter': cipher.encrypt(secret_word[0] if secret_word else ''),
            'pattern': _generate_pattern_hint(cipher, secret_word),
            'educational': _get_educational_hint(cipher, level)
        }

        # Create game record
        game = Game(
            user_id=user.id,
            level=level,
            dictionary_category=dictionary_category,
            attempts_allowed=current_app.config['MAX_ATTEMPTS_PER_GAME'],
            attempts_remaining=current_app.config['MAX_ATTEMPTS_PER_GAME'],
            secret_word_ciphertext=ciphertext,
            hint_ciphertexts=hints,
            cipher_metadata=cipher.get_metadata()
        )

        db.session.add(game)
        db.session.commit()

        # Return game data (never include plaintext secret)
        response = game.to_dict()
        response['cipher_info'] = {
            'name': cipher.get_name(),
            'level': cipher.get_level(),
            'description': cipher.get_educational_content()['how_it_works']
        }

        return jsonify(response), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Database error in new_game: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    except Exception as e:
        current_app.logger.error(f"Unexpected error in new_game: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@game_bp.route('/guess', methods=['POST'])
def submit_guess():
    """
    Submit a guess and receive feedback

    Request:
    {
        "game_id": "uuid",
        "guess": "apple"
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON request'}), 400

        game_id = data.get('game_id')
        guess = data.get('guess')

        validate_game_id(game_id)
        guess = sanitize_guess(guess)

        # Get game
        game = Game.query.filter_by(id=game_id).first()
        if not game:
            return jsonify({'error': 'Game not found'}), 404

        if game.game_status != 'ongoing':
            return jsonify({'error': f'Game is {game.game_status}'}), 400

        if game.attempts_remaining <= 0:
            return jsonify({'error': 'No attempts remaining'}), 400

        # Get cipher and decrypt secret
        cipher = get_cipher(game.level, **game.cipher_metadata.get('algorithm_params', {}))
        if not cipher:
            return jsonify({'error': f'Cannot load cipher for level {game.level}'}), 500

        secret_word = cipher.decrypt(game.secret_word_ciphertext)

        # Generate feedback
        feedback = _generate_wordle_feedback(guess, secret_word)

        # Record attempt
        attempt = GameAttempt(
            game_id=game.id,
            guess_text=guess,
            feedback=feedback,
            attempt_number=current_app.config['MAX_ATTEMPTS_PER_GAME'] - game.attempts_remaining + 1
        )
        db.session.add(attempt)

        # Update game state
        game.attempts_remaining -= 1

        # Check win condition
        if guess == secret_word:
            game.game_status = 'won'
            _update_user_progress(game, True, attempt.attempt_number)
        elif game.attempts_remaining == 0:
            game.game_status = 'lost'
            _update_user_progress(game, False, attempt.attempt_number)

        game.updated_at = datetime.utcnow()

        # Check for hint unlocks
        unlocked_hints = _check_hint_unlocks(game, cipher)

        db.session.commit()

        # Clear secret from memory
        del secret_word

        return jsonify({
            'game_id': str(game.id),
            'feedback': feedback,
            'attempts_remaining': game.attempts_remaining,
            'unlocked_hints': unlocked_hints,
            'game_status': game.game_status
        }), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Database error in submit_guess: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    except Exception as e:
        current_app.logger.error(f"Unexpected error in submit_guess: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@game_bp.route('/hints', methods=['GET'])
def get_hints():
    """
    Get currently unlocked hints

    Query parameters:
    - game_id: UUID of the game
    """
    try:
        game_id = request.args.get('game_id')
        validate_game_id(game_id)

        game = Game.query.filter_by(id=game_id).first()
        if not game:
            return jsonify({'error': 'Game not found'}), 404

        # Get cipher for decryption
        cipher = get_cipher(game.level, **game.cipher_metadata.get('algorithm_params', {}))
        if not cipher:
            return jsonify({'error': f'Cannot load cipher for level {game.level}'}), 500

        # Check which hints should be unlocked
        unlocked_hints = _check_hint_unlocks(game, cipher, decrypt=True)

        return jsonify({
            'game_id': str(game.id),
            'unlocked': unlocked_hints
        }), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"Error in get_hints: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@game_bp.route('/game/<game_id>', methods=['GET'])
def get_game_status(game_id):
    """
    Get current game status

    Path parameters:
    - game_id: UUID of the game
    """
    try:
        validate_game_id(game_id)

        game = Game.query.filter_by(id=game_id).first()
        if not game:
            return jsonify({'error': 'Game not found'}), 404

        # Get attempts history
        attempts = [attempt.to_dict() for attempt in game.attempts]

        response = game.to_dict()
        response['attempts'] = attempts
        # Never include the secret word in plaintext
        response.pop('secret_word', None)

        return jsonify(response), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"Error in get_game_status: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

def _generate_wordle_feedback(guess: str, secret: str) -> list:
    """
    Generate Wordle-style feedback for a guess

    Args:
        guess: The guessed word
        secret: The secret word

    Returns:
        List of feedback strings: 'correct_position', 'wrong_position', 'absent'
    """
    if len(guess) != len(secret):
        raise ValueError("Guess length must match secret length")

    feedback = ['absent'] * len(guess)
    secret_chars = list(secret)

    # First pass: mark correct positions
    for i in range(len(guess)):
        if guess[i] == secret_chars[i]:
            feedback[i] = 'correct_position'
            secret_chars[i] = None  # Mark as used

    # Second pass: mark wrong positions
    for i in range(len(guess)):
        if feedback[i] == 'absent' and guess[i] in secret_chars:
            feedback[i] = 'wrong_position'
            secret_chars[secret_chars.index(guess[i])] = None  # Mark as used

    return feedback

def _check_hint_unlocks(game: Game, cipher, decrypt: bool = False) -> dict:
    """
    Check which hints should be unlocked based on attempts

    Args:
        game: Game object
        cipher: Cipher instance
        decrypt: Whether to decrypt hints for returning

    Returns:
        Dictionary of unlocked hints
    """
    attempts_used = current_app.config['MAX_ATTEMPTS_PER_GAME'] - game.attempts_remaining
    unlocked = {}

    # Length hint unlocked at 3 attempts
    if attempts_used >= 3:
        if decrypt:
            try:
                unlocked['length'] = int(cipher.decrypt(game.hint_ciphertexts['length']))
            except:
                unlocked['length'] = len(game.secret_word_ciphertext)  # Fallback
        else:
            unlocked['length'] = 'unlocked'

    # First letter hint unlocked at 5 attempts
    if attempts_used >= 5:
        if decrypt:
            try:
                unlocked['first_letter'] = cipher.decrypt(game.hint_ciphertexts['first_letter'])
            except:
                unlocked['first_letter'] = '?'
        else:
            unlocked['first_letter'] = 'unlocked'

    # Pattern hint for advanced levels (levels 4-9)
    if game.level >= 4 and attempts_used >= 4:
        if decrypt:
            try:
                unlocked['pattern'] = cipher.decrypt(game.hint_ciphertexts['pattern'])
            except:
                unlocked['pattern'] = 'Pattern analysis unavailable'
        else:
            unlocked['pattern'] = 'unlocked'

    # Educational hint always available
    if decrypt:
        unlocked['educational'] = game.hint_ciphertexts.get('educational', 'No hint available')
    else:
        unlocked['educational'] = 'available'

    return unlocked

def _generate_pattern_hint(cipher, secret_word: str) -> str:
    """
    Generate a pattern hint for the secret word

    Args:
        cipher: Cipher instance
        secret_word: The secret word

    Returns:
        Encrypted pattern hint
    """
    # Create a simple pattern (double letters, etc.)
    pattern = []
    for i, char in enumerate(secret_word):
        if i > 0 and char == secret_word[i-1]:
            pattern.append('double')
        elif char in 'AEIOU':
            pattern.append('vowel')
        else:
            pattern.append('consonant')

    pattern_text = ' '.join(pattern)
    return cipher.encrypt(pattern_text)

def _get_educational_hint(cipher, level: int) -> str:
    """Get educational hint for the cipher"""
    educational_content = cipher.get_educational_content()
    return educational_content.get('weakness_explanation', 'No educational hint available')

def _update_user_progress(game: Game, won: bool, attempts_used: int):
    """Update user progress statistics"""
    if not game.user_id:
        return  # No user to track for guest sessions

    # Get or create progress record
    progress = UserProgress.query.filter_by(
        user_id=game.user_id,
        level=game.level
    ).first()

    if not progress:
        progress = UserProgress(
            user_id=game.user_id,
            level=game.level
        )
        db.session.add(progress)

    # Update statistics
    progress.update_statistics(won, attempts_used, 0, 0)  # hints and time tracking not implemented yet

def _create_fallback_word(level: int):
    """Create a fallback word when database is empty"""
    fallback_words = {
        1: "APPLE",
        2: "BRAVO",
        3: "CIPHER",
        4: "MATRIX",
        5: "FENCES",
        6: "RANDOM",
        7: "PADDED",
        8: "ENCRYPT",
        9: "DIGITAL"
    }

    word = fallback_words.get(level, "GAME")
    return WordDictionary(
        word=word,
        length=len(word),
        category='fallback',
        difficulty_score=level
    )