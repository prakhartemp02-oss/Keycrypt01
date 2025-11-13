"""Rail Fence Cipher Implementation - Level 5"""

from . import CipherBase
from ..utils.crypto import generate_rail_fence_rails, hash_key_material
from typing import Dict, Any, List
import string

class RailFenceCipher(CipherBase):
    """
    Rail Fence Cipher - Transposition cipher writing in zig-zag pattern

    Educational Level: 5
    Historical Context: Used in the American Civil War and by ancient Greeks
    Weakness: Pattern is visible in the ciphertext, vulnerable to known-plaintext attacks
    """

    def __init__(self, rails: int = None, **kwargs):
        """
        Initialize Rail Fence cipher

        Args:
            rails: Number of rails to use (2-4)
        """
        if rails is None:
            self.rails = generate_rail_fence_rails()
        else:
            if not 2 <= rails <= 4:
                raise ValueError("Number of rails must be between 2 and 4")
            self.rails = rails

    def encrypt(self, plaintext: str) -> str:
        """
        Encrypt plaintext using Rail Fence pattern

        Args:
            plaintext: Text to encrypt

        Returns:
            Ciphertext
        """
        plaintext = self.preprocess_text(plaintext)
        if not plaintext:
            return ""

        # Create rails
        rail_patterns = [''] * self.rails
        rail = 0
        direction = 1  # 1 for down, -1 for up

        for char in plaintext:
            rail_patterns[rail] += char

            # Move to next rail
            rail += direction

            # Change direction at top or bottom rail
            if rail == 0:
                direction = 1
            elif rail == self.rails - 1:
                direction = -1

        # Combine all rails
        ciphertext = ''.join(rail_patterns)
        return ciphertext

    def decrypt(self, ciphertext: str) -> str:
        """
        Decrypt ciphertext by reconstructing the rail pattern

        Args:
            ciphertext: Text to decrypt

        Returns:
            Plaintext
        """
        ciphertext = self.preprocess_text(ciphertext)
        if not ciphertext:
            return ""

        length = len(ciphertext)

        # Calculate how many characters go in each rail
        rail_lengths = [0] * self.rails
        rail = 0
        direction = 1

        # First pass: determine rail lengths
        for i in range(length):
            rail_lengths[rail] += 1
            rail += direction

            if rail == 0:
                direction = 1
            elif rail == self.rails - 1:
                direction = -1

        # Split ciphertext into rails
        rails = []
        start = 0
        for rail_length in rail_lengths:
            rails.append(list(ciphertext[start:start + rail_length]))
            start += rail_length

        # Second pass: reconstruct plaintext
        plaintext = []
        rail = 0
        direction = 1
        rail_indices = [0] * self.rails

        for i in range(length):
            # Get character from current rail
            char = rails[rail][rail_indices[rail]]
            plaintext.append(char)
            rail_indices[rail] += 1

            # Move to next rail
            rail += direction

            if rail == 0:
                direction = 1
            elif rail == self.rails - 1:
                direction = -1

        return ''.join(plaintext)

    def generate_keys(self) -> Dict[str, Any]:
        """
        Generate cipher key material

        Returns:
            Dictionary containing number of rails
        """
        return {
            'rails': self.rails,
            'algorithm': 'railfence'
        }

    def get_metadata(self) -> Dict[str, Any]:
        """
        Get cipher metadata for storage

        Returns:
            Cipher metadata
        """
        return {
            'cipher': 'Rail Fence',
            'level': 5,
            'rails': self.rails,
            'key_hash': hash_key_material({'rails': self.rails}),
            'algorithm_params': {
                'rails_range': '2-4',
                'type': 'transposition'
            }
        }

    def get_name(self) -> str:
        """Get cipher name"""
        return "Rail Fence"

    def get_level(self) -> int:
        """Get difficulty level"""
        return 5

    def get_educational_content(self) -> Dict[str, str]:
        """
        Get educational content about this cipher

        Returns:
            Educational information
        """
        return {
            'historical_context': (
                "Used during the American Civil War and by ancient Greeks. "
                "The pattern resembles a fence, hence the name. It's a transposition cipher "
                "that doesn't change the letters themselves, only their positions."
            ),
            'how_it_works': (
                "Write the plaintext in a zig-zag pattern across multiple 'rails', then read "
                "horizontally to get the ciphertext. For example with 3 rails: 'HELLO WORLD' "
                "becomes: H O L\nE L W R D\nL O   (read as HOL ELWRD LO)"
            ),
            'weakness_explanation': (
                "The rail pattern is often visible in the ciphertext. Known-plaintext attacks "
                "can easily determine the number of rails. With enough ciphertext, statistical "
                "analysis of character positions can break the cipher."
            ),
            'modern_relevance': (
                "Introduces transposition ciphers where letters are rearranged rather than "
                "substituted. Foundation for understanding more complex transposition methods "
                "used in modern cryptography."
            )
        }

    def get_visual_pattern(self, plaintext: str) -> List[str]:
        """
        Create visual representation of the rail pattern

        Args:
            plaintext: Text to visualize

        Returns:
            List of strings representing each rail
        """
        plaintext = self.preprocess_text(plaintext)
        if not plaintext:
            return [""] * self.rails

        # Initialize rails with spaces
        rails = [[' '] * len(plaintext) for _ in range(self.rails)]

        rail = 0
        direction = 1

        for i, char in enumerate(plaintext):
            rails[rail][i] = char
            rail += direction

            if rail == 0:
                direction = 1
            elif rail == self.rails - 1:
                direction = -1

        # Convert to strings
        return [''.join(rail).rstrip() for rail in rails]