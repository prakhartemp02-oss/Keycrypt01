"""Monoalphabetic Substitution Cipher Implementation - Level 2"""

from . import CipherBase
from ..utils.crypto import generate_substitution_alphabet, hash_key_material
from typing import Dict, Any
import string

class SubstitutionCipher(CipherBase):
    """
    Monoalphabetic Substitution Cipher - Random letter mapping

    Educational Level: 2
    Historical Context: Used in various forms throughout history, from simple codes to
    the Alberti cipher disk (1467)
    Weakness: Vulnerable to frequency analysis attacks
    """

    def __init__(self, alphabet: str = None, **kwargs):
        """
        Initialize substitution cipher

        Args:
            alphabet: Substitution alphabet (26 unique uppercase letters)
        """
        self.plain_alphabet = string.ascii_uppercase

        if alphabet is None:
            self.cipher_alphabet = generate_substitution_alphabet()
        else:
            # Validate alphabet
            if len(alphabet) != 26:
                raise ValueError("Substitution alphabet must have exactly 26 letters")
            if len(set(alphabet)) != 26:
                raise ValueError("Substitution alphabet must contain unique letters")
            if not alphabet.isalpha() or not alphabet.isupper():
                raise ValueError("Substitution alphabet must contain only uppercase letters")

            self.cipher_alphabet = alphabet

        # Create mapping dictionaries for faster encryption/decryption
        self.encrypt_map = dict(zip(self.plain_alphabet, self.cipher_alphabet))
        self.decrypt_map = dict(zip(self.cipher_alphabet, self.plain_alphabet))

    def encrypt(self, plaintext: str) -> str:
        """
        Encrypt plaintext using substitution mapping

        Args:
            plaintext: Text to encrypt

        Returns:
            Ciphertext
        """
        plaintext = self.preprocess_text(plaintext)
        ciphertext = []

        for char in plaintext:
            if char.isalpha():
                ciphertext.append(self.encrypt_map[char])
            else:
                ciphertext.append(char)

        return ''.join(ciphertext)

    def decrypt(self, ciphertext: str) -> str:
        """
        Decrypt ciphertext using reverse substitution mapping

        Args:
            ciphertext: Text to decrypt

        Returns:
            Plaintext
        """
        ciphertext = self.preprocess_text(ciphertext)
        plaintext = []

        for char in ciphertext:
            if char.isalpha():
                plaintext.append(self.decrypt_map[char])
            else:
                plaintext.append(char)

        return ''.join(plaintext)

    def generate_keys(self) -> Dict[str, Any]:
        """
        Generate cipher key material

        Returns:
            Dictionary containing substitution alphabet
        """
        return {
            'substitution_alphabet': self.cipher_alphabet,
            'algorithm': 'substitution'
        }

    def get_metadata(self) -> Dict[str, Any]:
        """
        Get cipher metadata for storage

        Returns:
            Cipher metadata
        """
        return {
            'cipher': 'Monoalphabetic Substitution',
            'level': 2,
            'substitution_alphabet': self.cipher_alphabet,
            'key_hash': hash_key_material({'alphabet': self.cipher_alphabet}),
            'algorithm_params': {
                'alphabet_size': 26,
                'possible_keys': '26! (4x10^26 possible combinations)'
            }
        }

    def get_name(self) -> str:
        """Get cipher name"""
        return "Monoalphabetic Substitution"

    def get_level(self) -> int:
        """Get difficulty level"""
        return 2

    def get_educational_content(self) -> Dict[str, str]:
        """
        Get educational content about this cipher

        Returns:
            Educational information
        """
        return {
            'historical_context': (
                "Used throughout history in various forms. Leon Battista Alberti created "
                "the first polyalphabetic cipher in 1467, but simple substitution ciphers "
                "have been used for centuries in military codes and treasure maps."
            ),
            'how_it_works': (
                "Each letter in the plaintext is replaced by a different letter according to "
                "a fixed mapping. Unlike Caesar cipher, the mapping is random rather than "
                "a simple shift. For example: A→Q, B→X, C→M, etc."
            ),
            'weakness_explanation': (
                "Vulnerable to frequency analysis attacks. In English, 'E' is the most common "
                "letter, followed by 'T', 'A', 'O', 'I', 'N', 'S', 'H', 'R'. Attackers can analyze "
                "letter frequencies in the ciphertext to deduce the substitution mapping."
            ),
            'modern_relevance': (
                "Demonstrates the importance of frequency analysis in cryptanalysis. "
                "Foundation for understanding why simple substitution is insufficient for "
                "secure communication."
            )
        }

    def get_letter_frequency_analysis(self, ciphertext: str) -> Dict[str, Any]:
        """
        Perform frequency analysis on ciphertext (for educational purposes)

        Args:
            ciphertext: Ciphertext to analyze

        Returns:
            Frequency analysis results
        """
        ciphertext = self.preprocess_text(ciphertext)
        frequency = {}

        for char in ciphertext:
            frequency[char] = frequency.get(char, 0) + 1

        # Sort by frequency
        sorted_frequency = sorted(frequency.items(), key=lambda x: x[1], reverse=True)

        # English letter frequencies for comparison
        english_freq = [
            'E', 'T', 'A', 'O', 'I', 'N', 'S', 'H', 'R', 'D', 'L', 'U', 'C',
            'M', 'W', 'F', 'G', 'Y', 'P', 'B', 'V', 'K', 'J', 'X', 'Q', 'Z'
        ]

        return {
            'cipher_frequencies': sorted_frequency,
            'english_frequencies': english_freq,
            'total_letters': len(ciphertext),
            'unique_letters': len(frequency)
        }