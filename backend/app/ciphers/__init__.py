"""Base cipher interface and factory"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import string

class CipherBase(ABC):
    """Abstract base class for all cipher implementations"""

    def __init__(self, **kwargs):
        """Initialize cipher with given parameters"""
        pass

    @abstractmethod
    def encrypt(self, plaintext: str) -> str:
        """
        Encrypt plaintext to ciphertext

        Args:
            plaintext: Text to encrypt (uppercase letters only)

        Returns:
            Ciphertext
        """
        pass

    @abstractmethod
    def decrypt(self, ciphertext: str) -> str:
        """
        Decrypt ciphertext to plaintext

        Args:
            ciphertext: Text to decrypt

        Returns:
            Plaintext
        """
        pass

    @abstractmethod
    def generate_keys(self) -> Dict[str, Any]:
        """
        Generate encryption keys/parameters

        Returns:
            Dictionary containing key material
        """
        pass

    @abstractmethod
    def get_metadata(self) -> Dict[str, Any]:
        """
        Get cipher metadata for storage

        Returns:
            Dictionary with cipher information
        """
        pass

    @abstractmethod
    def get_name(self) -> str:
        """
        Get cipher name

        Returns:
            Cipher name
        """
        pass

    @abstractmethod
    def get_level(self) -> int:
        """
        Get cipher difficulty level

        Returns:
            Level number (1-9)
        """
        pass

    def preprocess_text(self, text: str) -> str:
        """
        Preprocess text for encryption/decryption

        Args:
            text: Raw text

        Returns:
            Processed text (uppercase letters only)
        """
        # Remove non-alphabetic characters and convert to uppercase
        return ''.join(c for c in text.upper() if c.isalpha())

    def postprocess_text(self, text: str) -> str:
        """
        Postprocess text after encryption/decryption

        Args:
            text: Processed text

        Returns:
            Final text
        """
        return text

# Cipher registry
_CIPHER_REGISTRY = {}

def register_cipher(cipher_class, level: int):
    """Register a cipher implementation"""
    _CIPHER_REGISTRY[level] = cipher_class

def get_cipher(level: int, **kwargs) -> Optional[CipherBase]:
    """
    Get cipher instance for a level

    Args:
        level: Cipher level (1-9)
        **kwargs: Cipher-specific parameters

    Returns:
        Cipher instance or None if level not found
    """
    if level in _CIPHER_REGISTRY:
        return _CIPHER_REGISTRY[level](**kwargs)
    return None

def get_all_ciphers() -> Dict[int, type]:
    """
    Get all registered ciphers

    Returns:
        Dictionary mapping levels to cipher classes
    """
    return _CIPHER_REGISTRY.copy()

# Import all cipher implementations to register them
from .caesar import CaesarCipher
from .substitution import SubstitutionCipher
from .playfair import PlayfairCipher
from .hill import HillCipher
from .railfence import RailFenceCipher
from .vigenere import VigenereCipher
from .otp import OTPCipher
from .des import DESCipher
from .rsa import RSACipher

# Auto-register ciphers
register_cipher(CaesarCipher, 1)
register_cipher(SubstitutionCipher, 2)
register_cipher(PlayfairCipher, 3)
register_cipher(HillCipher, 4)
register_cipher(RailFenceCipher, 5)
register_cipher(VigenereCipher, 6)
register_cipher(OTPCipher, 7)
register_cipher(DESCipher, 8)
register_cipher(RSACipher, 9)