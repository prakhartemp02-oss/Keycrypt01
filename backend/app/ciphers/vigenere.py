"""Vigenère Cipher Implementation - Level 6"""

from . import CipherBase
from ..utils.crypto import generate_vigenere_keyword, hash_key_material
from typing import Dict, Any
import string

class VigenereCipher(CipherBase):
    """
    Vigenère Cipher - Polyalphabetic substitution using keyword

    Educational Level: 6
    Historical Context: Invented by Giovan Battista Bellaso in 1553, misattributed to
    Blaise de Vigenère in the 19th century. Used extensively in the 17th-19th centuries.
    Weakness: Vulnerable to Kasiski examination and frequency analysis of repeated key portions
    """

    def __init__(self, keyword: str = None, **kwargs):
        """
        Initialize Vigenère cipher

        Args:
            keyword: Keyword for encryption (uppercase letters only)
        """
        self.plain_alphabet = string.ascii_uppercase

        if keyword is None:
            self.keyword = generate_vigenere_keyword()
        else:
            keyword = keyword.upper().replace(' ', '')
            if not keyword.isalpha():
                raise ValueError("Keyword must contain only letters")
            if len(keyword) < 2:
                raise ValueError("Keyword must be at least 2 characters long")
            self.keyword = keyword

        # Create Vigenère table (tabula recta)
        self.create_tabula_recta()

    def create_tabula_recta(self):
        """Create the Vigenère table for quick lookup"""
        self.tabula_recta = {}
        for i, row_char in enumerate(self.plain_alphabet):
            row = {}
            for j, col_char in enumerate(self.plain_alphabet):
                # Shift by i positions and wrap around
                shifted_index = (j + i) % 26
                row[col_char] = self.plain_alphabet[shifted_index]
            self.tabula_recta[row_char] = row

    def encrypt(self, plaintext: str) -> str:
        """
        Encrypt plaintext using Vigenère cipher

        Args:
            plaintext: Text to encrypt

        Returns:
            Ciphertext
        """
        plaintext = self.preprocess_text(plaintext)
        if not plaintext:
            return ""

        ciphertext = []
        keyword_index = 0

        for char in plaintext:
            if char.isalpha():
                # Get current keyword character
                key_char = self.keyword[keyword_index % len(self.keyword)]

                # Encrypt using Vigenère table
                encrypted_char = self.tabula_recta[key_char][char]
                ciphertext.append(encrypted_char)

                keyword_index += 1
            else:
                ciphertext.append(char)

        return ''.join(ciphertext)

    def decrypt(self, ciphertext: str) -> str:
        """
        Decrypt ciphertext by finding the key character that produced the encryption

        Args:
            ciphertext: Text to decrypt

        Returns:
            Plaintext
        """
        ciphertext = self.preprocess_text(ciphertext)
        if not ciphertext:
            return ""

        plaintext = []
        keyword_index = 0

        for char in ciphertext:
            if char.isalpha():
                # Get current keyword character
                key_char = self.keyword[keyword_index % len(self.keyword)]

                # Find the plaintext character that encrypts to this ciphertext
                # with this key character
                for plain_char, encrypted_char in self.tabula_recta[key_char].items():
                    if encrypted_char == char:
                        plaintext.append(plain_char)
                        break

                keyword_index += 1
            else:
                plaintext.append(char)

        return ''.join(plaintext)

    def generate_keys(self) -> Dict[str, Any]:
        """
        Generate cipher key material

        Returns:
            Dictionary containing keyword
        """
        return {
            'keyword': self.keyword,
            'algorithm': 'vigenere'
        }

    def get_metadata(self) -> Dict[str, Any]:
        """
        Get cipher metadata for storage

        Returns:
            Cipher metadata
        """
        return {
            'cipher': 'Vigenère',
            'level': 6,
            'keyword_length': len(self.keyword),
            'keyword_hash': hash_key_material({'keyword': self.keyword}),
            'algorithm_params': {
                'keyword_length_range': '3-7',
                'type': 'polyalphabetic',
                'table_size': '26x26'
            }
        }

    def get_name(self) -> str:
        """Get cipher name"""
        return "Vigenère Cipher"

    def get_level(self) -> int:
        """Get difficulty level"""
        return 6

    def get_educational_content(self) -> Dict[str, str]:
        """
        Get educational content about this cipher

        Returns:
            Educational information
        """
        return {
            'historical_context': (
                "Invented by Giovan Battista Bellaso in 1553 but misattributed to Blaise de Vigenère. "
                "Considered 'le chiffré indéchiffrable' (the indecipherable cipher) for 300 years. "
                "Used extensively for military and diplomatic communications in the 17th-19th centuries."
            ),
            'how_it_works': (
                "Uses a keyword to shift letters by different amounts. Each letter of the keyword "
                "determines the shift for the corresponding plaintext letter. For example, with "
                "keyword 'KEY', the first letter is shifted by K (10), second by E (4), third by Y (24), "
                "then repeats. This creates a polyalphabetic substitution."
            ),
            'weakness_explanation': (
                "Vulnerable to Kasiski examination (finding repeated sequences) and frequency analysis. "
                "Since the keyword repeats, patterns emerge in the ciphertext. The Index of Coincidence "
                "can also identify Vigenère-encrypted text."
            ),
            'modern_relevance': (
                "Foundation for modern stream ciphers. Introduces the concept of using a key sequence "
                "to vary encryption. The principle of polyalphabetic substitution appears in modern "
                "cryptographic protocols."
            )
        }

    def get_kasiski_analysis(self, ciphertext: str, min_length: int = 3) -> Dict[str, Any]:
        """
        Perform Kasiski examination to find repeated sequences (educational)

        Args:
            ciphertext: Ciphertext to analyze
            min_length: Minimum sequence length to consider

        Returns:
            Analysis results
        """
        ciphertext = self.preprocess_text(ciphertext)
        sequences = {}

        # Find all repeated sequences
        for length in range(min_length, len(ciphertext) // 2):
            for i in range(len(ciphertext) - length + 1):
                sequence = ciphertext[i:i + length]
                if sequence in sequences:
                    sequences[sequence].append(i)
                else:
                    sequences[sequence] = [i]

        # Filter to only repeated sequences
        repeated_sequences = {seq: positions for seq, positions in sequences.items() if len(positions) > 1}

        # Calculate distances between repetitions
        distances = []
        for positions in repeated_sequences.values():
            for i in range(len(positions) - 1):
                distances.append(positions[i + 1] - positions[i])

        # Find GCDs to suggest key length
        def gcd(a, b):
            while b:
                a, b = b, a % b
            return a

        def find_gcds(numbers):
            if not numbers:
                return []
            result = numbers[0]
            for num in numbers[1:]:
                result = gcd(result, num)
                if result == 1:
                    break
            return result

        suggested_key_lengths = []
        if distances:
            # Find factors of common distances
            common_distances = list(set([d for d in distances if distances.count(d) > 1]))
            for distance in common_distances[:5]:  # Top 5 common distances
                for factor in range(2, min(distance, 13)):  # Reasonable key lengths
                    if distance % factor == 0:
                        suggested_key_lengths.append(factor)

        return {
            'repeated_sequences': repeated_sequences,
            'distances': distances,
            'suggested_key_lengths': list(set(suggested_key_lengths)),
            'actual_keyword_length': len(self.keyword)
        }

    def get_tabula_recta_row(self, key_char: str) -> str:
        """
        Get a specific row of the Vigenère table

        Args:
            key_char: Key character for the row

        Returns:
            The corresponding row of the tabula recta
        """
        if key_char.upper() not in self.tabula_recta:
            raise ValueError(f"Invalid key character: {key_char}")

        return ''.join(self.tabula_recta[key_char.upper()].values())