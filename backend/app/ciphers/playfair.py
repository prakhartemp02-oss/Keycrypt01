"""Playfair Cipher Implementation - Level 3"""

from . import CipherBase
from ..utils.crypto import generate_playfair_keyword, hash_key_material
from typing import Dict, Any, Tuple, List
import string

class PlayfairCipher(CipherBase):
    """
    Playfair Cipher - Digraph substitution using 5x5 matrix

    Educational Level: 3
    Historical Context: Invented by Charles Wheatstone in 1854, popularized by
    Lord Playfair. Used by British forces in WWI and WWII.
    Weakness: Vulnerable to digraph frequency analysis
    """

    def __init__(self, keyword: str = None, **kwargs):
        """
        Initialize Playfair cipher

        Args:
            keyword: Keyword for matrix generation (combines I/J)
        """
        if keyword is None:
            self.keyword = generate_playfair_keyword()
        else:
            # Clean keyword - remove spaces and duplicates
            keyword = keyword.upper().replace(' ', '').replace('J', 'I')
            if not keyword.isalpha():
                raise ValueError("Keyword must contain only letters")
            self.keyword = keyword

        self.create_matrix()

    def create_matrix(self):
        """Create 5x5 Playfair matrix from keyword"""
        # Create matrix without duplicates, combining I/J
        alphabet = string.ascii_uppercase.replace('J', '')  # 25 letters
        matrix_chars = []

        # Add unique keyword letters
        for char in self.keyword:
            if char not in matrix_chars:
                matrix_chars.append(char)

        # Add remaining alphabet letters
        for char in alphabet:
            if char not in matrix_chars:
                matrix_chars.append(char)

        # Create 5x5 matrix
        self.matrix = []
        for i in range(5):
            row = matrix_chars[i * 5:(i + 1) * 5]
            self.matrix.append(row)

        # Create position lookup for quick access
        self.positions = {}
        for row in range(5):
            for col in range(5):
                self.positions[self.matrix[row][col]] = (row, col)

    def preprocess_digraphs(self, text: str) -> List[str]:
        """
        Preprocess text into digraphs (pairs)

        Args:
            text: Text to preprocess

        Returns:
            List of digraphs
        """
        text = self.preprocess_text(text).replace('J', 'I')  # Combine I/J
        digraphs = []

        i = 0
        while i < len(text):
            if i + 1 < len(text):
                a, b = text[i], text[i + 1]
                if a == b:
                    # Insert X between identical letters
                    digraphs.append(a + 'X')
                    i += 1
                else:
                    digraphs.append(a + b)
                    i += 2
            else:
                # Single letter at end, add X
                digraphs.append(text[i] + 'X')
                i += 1

        return digraphs

    def encrypt_digraph(self, digraph: str) -> str:
        """
        Encrypt a single digraph

        Args:
            digraph: Two-letter digraph to encrypt

        Returns:
            Encrypted digraph
        """
        if len(digraph) != 2:
            raise ValueError("Digraph must have exactly 2 letters")

        a, b = digraph[0], digraph[1]
        row_a, col_a = self.positions[a]
        row_b, col_b = self.positions[b]

        if row_a == row_b:
            # Same row - shift right
            new_a = self.matrix[row_a][(col_a + 1) % 5]
            new_b = self.matrix[row_b][(col_b + 1) % 5]
        elif col_a == col_b:
            # Same column - shift down
            new_a = self.matrix[(row_a + 1) % 5][col_a]
            new_b = self.matrix[(row_b + 1) % 5][col_b]
        else:
            # Different row and column - swap columns
            new_a = self.matrix[row_a][col_b]
            new_b = self.matrix[row_b][col_a]

        return new_a + new_b

    def decrypt_digraph(self, digraph: str) -> str:
        """
        Decrypt a single digraph

        Args:
            digraph: Two-letter digraph to decrypt

        Returns:
            Decrypted digraph
        """
        if len(digraph) != 2:
            raise ValueError("Digraph must have exactly 2 letters")

        a, b = digraph[0], digraph[1]
        row_a, col_a = self.positions[a]
        row_b, col_b = self.positions[b]

        if row_a == row_b:
            # Same row - shift left
            new_a = self.matrix[row_a][(col_a - 1) % 5]
            new_b = self.matrix[row_b][(col_b - 1) % 5]
        elif col_a == col_b:
            # Same column - shift up
            new_a = self.matrix[(row_a - 1) % 5][col_a]
            new_b = self.matrix[(row_b - 1) % 5][col_b]
        else:
            # Different row and column - swap columns
            new_a = self.matrix[row_a][col_b]
            new_b = self.matrix[row_b][col_a]

        return new_a + new_b

    def encrypt(self, plaintext: str) -> str:
        """
        Encrypt plaintext using Playfair cipher

        Args:
            plaintext: Text to encrypt

        Returns:
            Ciphertext
        """
        digraphs = self.preprocess_digraphs(plaintext)
        encrypted_digraphs = [self.encrypt_digraph(digraph) for digraph in digraphs]
        return ''.join(encrypted_digraphs)

    def decrypt(self, ciphertext: str) -> str:
        """
        Decrypt ciphertext using Playfair cipher

        Args:
            ciphertext: Text to decrypt

        Returns:
            Plaintext
        """
        ciphertext = self.preprocess_text(ciphertext)

        if len(ciphertext) % 2 != 0:
            raise ValueError("Ciphertext length must be even")

        digraphs = [ciphertext[i:i + 2] for i in range(0, len(ciphertext), 2)]
        decrypted_digraphs = [self.decrypt_digraph(digraph) for digraph in digraphs]
        result = ''.join(decrypted_digraphs)

        # Remove inserted X's (heuristic - remove X's that don't belong)
        # This is not perfect due to ambiguity, but works for most cases
        cleaned = []
        i = 0
        while i < len(result):
            if result[i] == 'X':
                # Check if X was inserted to separate identical letters
                if (i > 0 and i < len(result) - 1 and
                    result[i - 1] == result[i + 1]):
                    # Skip the X
                    i += 1
                    continue
                elif i == len(result) - 1:
                    # X at end was added to make even length
                    break
            cleaned.append(result[i])
            i += 1

        return ''.join(cleaned)

    def generate_keys(self) -> Dict[str, Any]:
        """
        Generate cipher key material

        Returns:
            Dictionary containing keyword and matrix
        """
        return {
            'keyword': self.keyword,
            'matrix': self.matrix,
            'algorithm': 'playfair'
        }

    def get_metadata(self) -> Dict[str, Any]:
        """
        Get cipher metadata for storage

        Returns:
            Cipher metadata
        """
        return {
            'cipher': 'Playfair',
            'level': 3,
            'keyword': self.keyword,
            'matrix': self.matrix,
            'key_hash': hash_key_material({'keyword': self.keyword, 'matrix': self.matrix}),
            'algorithm_params': {
                'matrix_size': '5x5',
                'alphabet_combination': 'I/J combined',
                'digraph_processing': True
            }
        }

    def get_name(self) -> str:
        """Get cipher name"""
        return "Playfair Cipher"

    def get_level(self) -> int:
        """Get difficulty level"""
        return 3

    def get_educational_content(self) -> Dict[str, str]:
        """
        Get educational content about this cipher

        Returns:
            Educational information
        """
        return {
            'historical_context': (
                "Invented by Charles Wheatstone in 1854 and promoted by Lord Playfair. "
                "Used by British forces in World War I and World War II. One of the first "
                "practical digraph substitution ciphers."
            ),
            'how_it_works': (
                "Uses a 5x5 matrix created from a keyword. Text is broken into digraphs (pairs). "
                "Each digraph is encrypted based on letter positions in the matrix: "
                "Same row = shift right, Same column = shift down, Different = form rectangle and swap corners."
            ),
            'weakness_explanation': (
                "Vulnerable to digraph frequency analysis. Since letter pairs are encrypted consistently, "
                "common digraphs like 'TH', 'HE', 'IN' can be identified. The 5x5 structure also reduces "
                "the effective key space."
            ),
            'modern_relevance': (
                "Foundation for understanding block ciphers and digraph analysis. "
                "Introduced matrix-based encryption principles used in modern algorithms."
            )
        }

    def get_matrix_display(self) -> List[str]:
        """
        Get formatted matrix for display

        Returns:
            List of strings representing matrix rows
        """
        return [' '.join(row) for row in self.matrix]

    def analyze_digraph_patterns(self, text: str) -> Dict[str, Any]:
        """
        Analyze digraph patterns in text (educational)

        Args:
            text: Text to analyze

        Returns:
            Digraph frequency analysis
        """
        text = self.preprocess_text(text).replace('J', 'I')
        digraphs = []

        # Create digraphs
        i = 0
        while i < len(text):
            if i + 1 < len(text):
                if text[i] == text[i + 1]:
                    digraphs.append(text[i] + 'X')
                    i += 1
                else:
                    digraphs.append(text[i:i + 2])
                    i += 2
            else:
                digraphs.append(text[i] + 'X')
                i += 1

        # Count frequencies
        frequencies = {}
        for digraph in digraphs:
            frequencies[digraph] = frequencies.get(digraph, 0) + 1

        # Sort by frequency
        sorted_digraphs = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)

        return {
            'total_digraphs': len(digraphs),
            'unique_digraphs': len(frequencies),
            'most_common': sorted_digraphs[:10],
            'processed_text': ''.join(digraphs)
        }