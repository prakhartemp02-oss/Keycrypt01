"""Input validation utilities"""

import re
from typing import Optional

class ValidationError(Exception):
    """Custom validation error"""
    pass

def sanitize_guess(guess: str, max_length: int = 20) -> str:
    """
    Sanitize and validate a user guess

    Args:
        guess: Raw user input
        max_length: Maximum allowed word length

    Returns:
        Uppercase, sanitized guess

    Raises:
        ValidationError: If guess is invalid
    """
    if not guess:
        raise ValidationError("Guess cannot be empty")

    # Remove whitespace and convert to uppercase
    sanitized = re.sub(r'\s+', '', guess.strip()).upper()

    # Validate length
    if len(sanitized) < 1:
        raise ValidationError("Guess must contain at least one letter")

    if len(sanitized) > max_length:
        raise ValidationError(f"Guess cannot exceed {max_length} letters")

    # Validate characters (alphabetic only)
    if not re.match(r'^[A-Z]+$', sanitized):
        raise ValidationError("Guess must contain only letters")

    return sanitized

def validate_level(level: int) -> None:
    """
    Validate game level

    Args:
        level: Level number to validate

    Raises:
        ValidationError: If level is invalid
    """
    if not isinstance(level, int):
        raise ValidationError("Level must be an integer")

    if not 1 <= level <= 9:
        raise ValidationError("Level must be between 1 and 9")

def validate_game_id(game_id: str) -> None:
    """
    Validate game ID format

    Args:
        game_id: Game ID to validate

    Raises:
        ValidationError: If game ID is invalid
    """
    if not game_id:
        raise ValidationError("Game ID cannot be empty")

    if not isinstance(game_id, str):
        raise ValidationError("Game ID must be a string")

    # Basic UUID format validation (simplified)
    uuid_pattern = r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
    if not re.match(uuid_pattern, game_id):
        raise ValidationError("Invalid game ID format")

def sanitize_dictionary_category(category: Optional[str]) -> str:
    """
    Sanitize dictionary category

    Args:
        category: Raw category input

    Returns:
        Sanitized category name
    """
    if not category:
        return "common"

    # Remove special characters, keep alphanumeric and underscores
    sanitized = re.sub(r'[^a-zA-Z0-9_]', '', category.strip().lower())

    if not sanitized:
        return "common"

    return sanitized

def validate_user_id(user_id: Optional[str]) -> Optional[str]:
    """
    Validate user ID

    Args:
        user_id: User ID to validate

    Returns:
        Sanitized user ID or None
    """
    if not user_id:
        return None

    if not isinstance(user_id, str):
        return None

    # Basic sanitization - remove potentially dangerous characters
    sanitized = re.sub(r'[<>"\'/\\]', '', user_id.strip())

    return sanitized if sanitized else None