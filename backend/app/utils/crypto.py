"""Common cryptographic utilities"""

import os
import secrets
import string
from typing import Dict, Any

def generate_random_string(length: int, charset: str = None) -> str:
    """
    Generate a cryptographically secure random string

    Args:
        length: Length of the string to generate
        charset: Character set to use (defaults to uppercase letters)

    Returns:
        Random string
    """
    if charset is None:
        charset = string.ascii_uppercase

    return ''.join(secrets.choice(charset) for _ in range(length))

def generate_caesar_shift() -> int:
    """
    Generate a random Caesar cipher shift (1-25)

    Returns:
        Random shift value
    """
    return secrets.randbelow(25) + 1  # 1-25, never 0

def generate_substitution_alphabet() -> str:
    """
    Generate a random substitution alphabet

    Returns:
        Random permutation of the alphabet
    """
    alphabet = string.ascii_uppercase
    shuffled = list(alphabet)
    secrets.SystemRandom().shuffle(shuffled)
    return ''.join(shuffled)

def generate_vigenere_keyword(min_length: int = 3, max_length: int = 7) -> str:
    """
    Generate a random Vigenère cipher keyword

    Args:
        min_length: Minimum keyword length
        max_length: Maximum keyword length

    Returns:
        Random keyword
    """
    length = secrets.randbelow(max_length - min_length + 1) + min_length
    return generate_random_string(length)

def generate_playfair_keyword() -> str:
    """
    Generate a random Playfair cipher keyword

    Returns:
        Random keyword (letters only, no duplicates)
    """
    # Generate a keyword with unique letters
    alphabet = string.ascii_uppercase.replace('J', '')  # Playfair typically combines I/J
    keyword_length = secrets.randbelow(7) + 5  # 5-11 letters

    keyword = ''
    available_letters = list(alphabet)

    while len(keyword) < keyword_length and available_letters:
        letter = secrets.choice(available_letters)
        keyword += letter
        available_letters.remove(letter)

    return keyword

def generate_rail_fence_rails() -> int:
    """
    Generate a random number of rails for Rail Fence cipher

    Returns:
        Number of rails (2-4)
    """
    return secrets.randbelow(3) + 2  # 2-4 rails

def generate_otp_key(message_length: int) -> str:
    """
    Generate a one-time pad key

    Args:
        message_length: Length of the message

    Returns:
        Random key of the same length as the message
    """
    return generate_random_string(message_length)

def generate_des_key() -> bytes:
    """
    Generate a DES-compatible key

    Returns:
        8-byte key suitable for DES encryption
    """
    # DES requires 8 bytes (64 bits)
    return secrets.token_bytes(8)

def hash_key_material(key_material: Any) -> str:
    """
    Create a hash of key material for storage

    Args:
        key_material: Any key material to hash

    Returns:
        Hexadecimal hash
    """
    import hashlib
    import json

    # Convert key material to JSON string
    key_str = json.dumps(key_material, sort_keys=True)

    # Create SHA-256 hash
    return hashlib.sha256(key_str.encode()).hexdigest()

def secure_compare(a: str, b: str) -> bool:
    """
    Constant-time string comparison to prevent timing attacks

    Args:
        a: First string
        b: Second string

    Returns:
        True if strings are equal, False otherwise
    """
    import hmac

    # Use HMAC to prevent timing attacks
    return hmac.compare_digest(a.encode(), b.encode())