"""Authentication and user management API endpoints"""

import uuid
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, current_app
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import check_password_hash

from .. import db
from ..models.user import User
from ..models.game import UserProgress
from ..utils.validation import sanitize_dictionary_category

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/user/create', methods=['POST'])
def create_user():
    """
    Create a new user account

    Request:
    {
        "email": "user@example.com",
        "username": "player123",
        "password": "securepassword",
        "display_name": "Player Name"
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON request'}), 400

        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        display_name = data.get('display_name')

        # Basic validation
        if not username or len(username) < 3:
            return jsonify({'error': 'Username must be at least 3 characters'}), 400

        if not password or len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400

        # Check if username already exists
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 409

        # Check if email already exists (optional)
        if email and User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already exists'}), 409

        # Create user
        user = User(
            email=email,
            username=username,
            display_name=display_name or username
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return jsonify({
            'user': user.to_dict(),
            'message': 'User created successfully'
        }), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Database error in create_user: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    except Exception as e:
        current_app.logger.error(f"Unexpected error in create_user: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/user/login', methods=['POST'])
def login_user():
    """
    Authenticate a user

    Request:
    {
        "username": "player123",
        "password": "securepassword"
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON request'}), 400

        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400

        # Find user by username or email
        user = User.query.filter(
            (User.username == username) | (User.email == username)
        ).first()

        if not user or not user.check_password(password):
            return jsonify({'error': 'Invalid credentials'}), 401

        # Update last login
        user.update_last_login()
        db.session.commit()

        return jsonify({
            'user': user.to_dict(),
            'message': 'Login successful'
        }), 200

    except Exception as e:
        current_app.logger.error(f"Error in login_user: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/user/guest', methods=['POST'])
def create_guest():
    """
    Create a guest user (anonymous play)

    Request: {}
    """
    try:
        user = User.create_guest_user()
        db.session.add(user)
        db.session.commit()

        return jsonify({
            'user': user.to_dict(),
            'message': 'Guest session created'
        }), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Database error in create_guest: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    except Exception as e:
        current_app.logger.error(f"Unexpected error in create_guest: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/user/progress/<user_id>', methods=['GET'])
def get_user_progress(user_id):
    """
    Get user's progress across all levels

    Path parameters:
    - user_id: UUID of the user
    """
    try:
        # Verify user exists
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Get progress for all levels
        progress_records = UserProgress.query.filter_by(user_id=user_id).all()
        progress_dict = {record.level: record.to_dict() for record in progress_records}

        # Ensure all levels 1-9 are represented
        for level in range(1, 10):
            if level not in progress_dict:
                progress_dict[level] = {
                    'user_id': user_id,
                    'level': level,
                    'games_won': 0,
                    'games_played': 0,
                    'win_rate': 0.0,
                    'best_score': None,
                    'total_time_seconds': 0,
                    'average_hints_used': 0.0
                }

        return jsonify({
            'user_id': user_id,
            'progress': progress_dict,
            'total_levels_completed': len([p for p in progress_dict.values() if p['games_won'] > 0])
        }), 200

    except Exception as e:
        current_app.logger.error(f"Error in get_user_progress: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/user/stats/<user_id>', methods=['GET'])
def get_user_stats(user_id):
    """
    Get comprehensive user statistics

    Path parameters:
    - user_id: UUID of the user
    """
    try:
        # Verify user exists
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Get all progress records
        progress_records = UserProgress.query.filter_by(user_id=user_id).all()

        # Calculate overall statistics
        total_games = sum(p.games_played for p in progress_records)
        total_wins = sum(p.games_won for p in progress_records)
        overall_win_rate = (total_wins / total_games * 100) if total_games > 0 else 0

        # Find best performance
        best_scores = {p.level: p.best_score for p in progress_records if p.best_score}
        best_overall_score = min(best_scores.values()) if best_scores else None

        # Time statistics
        total_time = sum(p.total_time_seconds for p in progress_records)

        # Level completion statistics
        completed_levels = len([p for p in progress_records if p.games_won > 0])

        return jsonify({
            'user_id': user_id,
            'user': user.to_dict(),
            'statistics': {
                'total_games_played': total_games,
                'total_games_won': total_wins,
                'overall_win_rate': round(overall_win_rate, 2),
                'levels_completed': completed_levels,
                'levels_unlocked': min(completed_levels + 1, 9),  # Next level is unlocked
                'best_overall_score': best_overall_score,
                'total_time_seconds': total_time,
                'average_time_per_game': total_time / total_games if total_games > 0 else 0,
                'best_scores_by_level': best_scores
            }
        }), 200

    except Exception as e:
        current_app.logger.error(f"Error in get_user_stats: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    """
    Get public leaderboard statistics

    Query parameters:
    - level: Optional level filter (1-9)
    - limit: Maximum number of entries (default: 10)
    """
    try:
        level = request.args.get('level', type=int)
        limit = min(request.args.get('limit', 10, type=int), 50)  # Cap at 50

        # Build query
        query = db.session.query(
            UserProgress.user_id,
            UserProgress.level,
            UserProgress.games_won,
            UserProgress.best_score,
            User.display_name,
            User.username
        ).join(User, UserProgress.user_id == User.id)

        if level:
            query = query.filter(UserProgress.level == level)

        # Order by wins, then by best score (lower is better)
        query = query.filter(UserProgress.games_won > 0).order_by(
            UserProgress.games_won.desc(),
            UserProgress.best_score.asc().nullslast()
        ).limit(limit)

        results = query.all()

        # Format results
        leaderboard = []
        for rank, (user_id, level_num, games_won, best_score, display_name, username) in enumerate(results, 1):
            leaderboard.append({
                'rank': rank,
                'user_id': str(user_id),
                'display_name': display_name or f'Player {str(user_id)[:8]}',
                'level': level_num,
                'games_won': games_won,
                'best_score': best_score,
                'win_rate': 0  # Would need additional calculation
            })

        return jsonify({
            'leaderboard': leaderboard,
            'level_filter': level,
            'entries_returned': len(leaderboard)
        }), 200

    except Exception as e:
        current_app.logger.error(f"Error in get_leaderboard: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500