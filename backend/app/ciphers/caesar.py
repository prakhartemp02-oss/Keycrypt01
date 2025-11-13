"""Caesar Cipher Implementation - Level 1"""

from . import CipherBase
from ..utils.crypto import generate_caesar_shift, hash_key_material
from typing import Dict, Any

class CaesarCipher(CipherBase):
    """
    Caesar Cipher - Simple shift cipher used by Julius Caesar

    Educational Level: 1
    Historical Context: Used by Julius Caesar for military messages around 58 BC
    Weakness: Only 25 possible keys, vulnerable to brute force attacks
    """

    def __init__(self, shift: int = None, **kwargs):
        """
        Initialize Caesar cipher

        Args:
            shift: Number of positions to shift (1-25)
        """
        if shift is None:
            self.shift = generate_caesar_shift()
        else:
            if not 1 <= shift <= 25:
                raise ValueError("Shift must be between 1 and 25")
            self.shift = shift

    def encrypt(self, plaintext: str) -> str:
        """
        Encrypt plaintext using Caesar shift

        Args:
            plaintext: Text to encrypt

        Returns:
            Ciphertext with each letter shifted by self.shift positions
        """
        plaintext = self.preprocess_text(plaintext)
        ciphertext = []

        for char in plaintext:
            if char.isalpha():
                # Shift character with wrap-around
                shifted = ord(char) - ord('A') + self.shift
                shifted = shifted % 26 + ord('A')
                ciphertext.append(chr(shifted))
            else:
                ciphertext.append(char)

        return ''.join(ciphertext)

    def decrypt(self, ciphertext: str) -> str:
        """
        Decrypt ciphertext by reversing the shift

        Args:
            ciphertext: Text to decrypt

        Returns:
            Plaintext
        """
        ciphertext = self.preprocess_text(ciphertext)
        plaintext = []

        for char in ciphertext:
            if char.isalpha():
                # Reverse shift with wrap-around
                shifted = ord(char) - ord('A') - self.shift
                shifted = shifted % 26 + ord('A')
                plaintext.append(chr(shifted))
            else:
                plaintext.append(char)

        return ''.join(plaintext)

    def generate_keys(self) -> Dict[str, Any]:
        """
        Generate cipher key material

        Returns:
            Dictionary containing shift value
        """
        return {
            'shift': self.shift,
            'algorithm': 'caesar'
        }

    def get_metadata(self) -> Dict[str, Any]:
        """
        Get cipher metadata for storage

        Returns:
            Cipher metadata
        """
        return {
            'cipher': 'Caesar',
            'level': 1,
            'shift': self.shift,
            'key_hash': hash_key_material({'shift': self.shift}),
            'algorithm_params': {
                'alphabet_size': 26,
                'shift_range': '1-25'
            }
        }

    def get_name(self) -> str:
        """Get cipher name"""
        return "Caesar Cipher"

    def get_level(self) -> int:
        """Get difficulty level"""
        return 1

    def get_educational_content(self) -> Dict[str, str]:
        """
        Get educational content about this cipher

        Returns:
            Educational information
        """
        return {
            'historical_context': (
                "Used by Julius Caesar for military messages around 58 BC. "
                "He used it to communicate with his generals during the Gallic Wars."
            ),
            'how_it_works': (
                "Each letter in the plaintext is shifted by a fixed number of positions "
                "down the alphabet. For example, with a shift of 3, A becomes D, B becomes E, etc."
            ),
            'weakness_explanation': (
                "Only 25 possible keys (shifts 1-25), making it vulnerable to brute force attacks. "
                "An attacker can simply try all possible shifts until the message becomes readable."
            ),
            'modern_relevance': (
                "Foundation for understanding substitution ciphers and modular arithmetic in cryptography. "
                "Introduces the concept of algorithmic encryption."
            )
        }

    def brute_force_decrypt(self, ciphertext: str) -> list:
        """
        Demonstrate brute force attack (for educational purposes)

        Args:
            ciphertext: Text to decrypt

        Returns:
            List of all possible plaintexts with their shift values
        """
        results = []
        for shift in range(1, 26):
            temp_cipher = CaesarCipher(shift=shift)
            plaintext = temp_cipher.decrypt(ciphertext)
            results.append({
                'shift': shift,
                'plaintext': plaintext
            })
        return results