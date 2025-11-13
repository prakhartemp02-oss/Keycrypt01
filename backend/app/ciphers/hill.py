"""Hill Cipher Implementation - Level 4"""

from . import CipherBase
from ..utils.crypto import hash_key_material
from typing import Dict, Any, List
import string
import random
import math

class HillCipher(CipherBase):
    """
    Hill Cipher - Matrix-based substitution using linear algebra

    Educational Level: 4
    Historical Context: Invented by Lester S. Hill in 1929. First polygraphic
    substitution cipher based on linear algebra.
    Weakness: Vulnerable to known-plaintext attacks, requires solving linear equations
    """

    def __init__(self, key_matrix: List[List[int]] = None, matrix_size: int = None, **kwargs):
        """
        Initialize Hill cipher

        Args:
            key_matrix: NxN matrix with integer elements
            matrix_size: Size of square matrix (2 or 3)
        """
        if key_matrix is None:
            if matrix_size is None:
                matrix_size = random.choice([2, 3])
            self.matrix_size = matrix_size
            self.key_matrix = self.generate_invertible_matrix(matrix_size)
        else:
            self.matrix_size = len(key_matrix)
            self.key_matrix = key_matrix

        # Validate matrix
        if not self.is_valid_matrix(self.key_matrix):
            raise ValueError("Invalid key matrix")

        # Calculate modular inverse for decryption
        self.inverse_matrix = self.matrix_inverse_mod(self.key_matrix, 26)

    def generate_invertible_matrix(self, size: int) -> List[List[int]]:
        """
        Generate a random invertible matrix modulo 26

        Args:
            size: Matrix size (2 or 3)

        Returns:
            Invertible matrix
        """
        max_attempts = 1000
        for _ in range(max_attempts):
            # Generate random matrix
            matrix = [[random.randint(0, 25) for _ in range(size)] for _ in range(size)]

            # Check if invertible
            if self.determinant_mod(matrix, 26) != 0:
                if self.matrix_inverse_mod(matrix, 26) is not None:
                    return matrix

        # Fallback to known good matrices
        if size == 2:
            return [[6, 24], [1, 13]]  # Known invertible matrix
        else:
            return [[2, 3, 1], [5, 4, 2], [1, 6, 3]]  # Known invertible 3x3 matrix

    def is_valid_matrix(self, matrix: List[List[int]]) -> bool:
        """Check if matrix is square and has proper values"""
        if not matrix or not all(len(row) == len(matrix) for row in matrix):
            return False

        # Check if all values are valid
        for row in matrix:
            for val in row:
                if not isinstance(val, int) or val < 0 or val > 25:
                    return False

        # Check if invertible
        return self.determinant_mod(matrix, 26) != 0

    def determinant_mod(self, matrix: List[List[int]], mod: int) -> int:
        """Calculate determinant of matrix modulo mod"""
        n = len(matrix)

        if n == 1:
            return matrix[0][0] % mod
        elif n == 2:
            det = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
            return det % mod
        elif n == 3:
            det = (
                matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1]) -
                matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0]) +
                matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
            )
            return det % mod
        else:
            raise ValueError("Matrix size not supported")

    def matrix_inverse_mod(self, matrix: List[List[int]], mod: int) -> List[List[int]]:
        """Calculate matrix inverse modulo mod"""
        n = len(matrix)
        det = self.determinant_mod(matrix, mod)

        if det == 0:
            return None  # Matrix not invertible

        # Find modular inverse of determinant
        det_inv = self.modular_inverse(det, mod)
        if det_inv is None:
            return None

        # Calculate adjugate matrix
        adj = self.adjugate_matrix(matrix)

        # Calculate inverse: det_inv * adj (mod 26)
        inverse = []
        for i in range(n):
            row = []
            for j in range(n):
                val = (det_inv * adj[i][j]) % mod
                row.append(val)
            inverse.append(row)

        return inverse

    def modular_inverse(self, a: int, mod: int) -> int:
        """Find modular inverse using extended Euclidean algorithm"""
        a = a % mod

        if math.gcd(a, mod) != 1:
            return None  # No inverse exists

        # Extended Euclidean algorithm
        def extended_gcd(a, b):
            if a == 0:
                return b, 0, 1
            gcd, x1, y1 = extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y

        gcd, x, _ = extended_gcd(a, mod)
        return x % mod

    def adjugate_matrix(self, matrix: List[List[int]]) -> List[List[int]]:
        """Calculate adjugate (cofactor transpose) matrix"""
        n = len(matrix)
        adj = [[0] * n for _ in range(n)]

        for i in range(n):
            for j in range(n):
                # Calculate cofactor C(i,j)
                minor = self.get_minor(matrix, i, j)
                cofactor = ((-1) ** (i + j)) * self.determinant_mod(minor, 26)
                # Transpose: C(j,i) = cofactor
                adj[j][i] = cofactor % 26

        return adj

    def get_minor(self, matrix: List[List[int]], row: int, col: int) -> List[List[int]]:
        """Get minor matrix by removing specified row and column"""
        return [matrix[i][:col] + matrix[i][col + 1:] for i in range(len(matrix)) if i != row]

    def matrix_multiply_mod(self, matrix: List[List[int]], vector: List[int], mod: int) -> List[int]:
        """Multiply matrix by vector modulo mod"""
        n = len(matrix)
        result = []

        for i in range(n):
            sum_val = 0
            for j in range(n):
                sum_val += matrix[i][j] * vector[j]
            result.append(sum_val % mod)

        return result

    def text_to_numbers(self, text: str) -> List[int]:
        """Convert text to numbers (A=0, B=1, ..., Z=25)"""
        text = self.preprocess_text(text)
        return [ord(char) - ord('A') for char in text]

    def numbers_to_text(self, numbers: List[int]) -> str:
        """Convert numbers to text"""
        return ''.join(chr(num + ord('A')) for num in numbers)

    def encrypt(self, plaintext: str) -> str:
        """
        Encrypt plaintext using Hill cipher

        Args:
            plaintext: Text to encrypt

        Returns:
            Ciphertext
        """
        plaintext = self.preprocess_text(plaintext)
        if not plaintext:
            return ""

        # Convert to numbers
        numbers = self.text_to_numbers(plaintext)

        # Pad if necessary to make length divisible by matrix size
        if len(numbers) % self.matrix_size != 0:
            padding_length = self.matrix_size - (len(numbers) % self.matrix_size)
            numbers.extend([23] * padding_length)  # X = 23

        # Encrypt in blocks
        encrypted_numbers = []
        for i in range(0, len(numbers), self.matrix_size):
            block = numbers[i:i + self.matrix_size]
            encrypted_block = self.matrix_multiply_mod(self.key_matrix, block, 26)
            encrypted_numbers.extend(encrypted_block)

        return self.numbers_to_text(encrypted_numbers)

    def decrypt(self, ciphertext: str) -> str:
        """
        Decrypt ciphertext using Hill cipher

        Args:
            ciphertext: Text to decrypt

        Returns:
            Plaintext
        """
        ciphertext = self.preprocess_text(ciphertext)
        if not ciphertext:
            return ""

        # Convert to numbers
        numbers = self.text_to_numbers(ciphertext)

        # Decrypt in blocks
        decrypted_numbers = []
        for i in range(0, len(numbers), self.matrix_size):
            block = numbers[i:i + self.matrix_size]
            decrypted_block = self.matrix_multiply_mod(self.inverse_matrix, block, 26)
            decrypted_numbers.extend(decrypted_block)

        # Convert back to text and remove padding
        result = self.numbers_to_text(decrypted_numbers)
        # Remove trailing X's used for padding
        result = result.rstrip('X')

        return result

    def generate_keys(self) -> Dict[str, Any]:
        """
        Generate cipher key material

        Returns:
            Dictionary containing key matrix
        """
        return {
            'key_matrix': self.key_matrix,
            'matrix_size': self.matrix_size,
            'algorithm': 'hill'
        }

    def get_metadata(self) -> Dict[str, Any]:
        """
        Get cipher metadata for storage

        Returns:
            Cipher metadata
        """
        return {
            'cipher': 'Hill',
            'level': 4,
            'matrix_size': self.matrix_size,
            'determinant': self.determinant_mod(self.key_matrix, 26),
            'key_hash': hash_key_material({'matrix': self.key_matrix}),
            'algorithm_params': {
                'type': 'matrix_substitution',
                'modulus': 26,
                'supported_sizes': [2, 3]
            }
        }

    def get_name(self) -> str:
        """Get cipher name"""
        return "Hill Cipher"

    def get_level(self) -> int:
        """Get difficulty level"""
        return 4

    def get_educational_content(self) -> Dict[str, str]:
        """
        Get educational content about this cipher

        Returns:
            Educational information
        """
        return {
            'historical_context': (
                "Invented by Lester S. Hill in 1929 and published in 'Cryptography in an "
                "Algebraic Alphabet'. First cipher to systematically use linear algebra for encryption. "
                "Breakthrough in polygraphic substitution."
            ),
            'how_it_works': (
                "Represents letters as numbers (A=0, B=1, etc.) and encrypts them using "
                "matrix multiplication. For a 2x2 matrix, each pair of letters becomes a 2-element vector "
                "that is multiplied by the key matrix modulo 26. Decryption uses the modular inverse."
            ),
            'weakness_explanation': (
                "Vulnerable to known-plaintext attacks. If an attacker knows even one plaintext-ciphertext "
                "pair, they can solve linear equations to recover the key matrix. The linear nature also "
                "creates patterns that can be exploited."
            ),
            'modern_relevance': (
                "Foundation for understanding modern block ciphers and linear cryptanalysis. "
                "Demonstrates mathematical principles used in algorithms like AES. Matrix multiplication "
                "and modular arithmetic are fundamental to cryptography."
            )
        }

    def matrix_to_string(self, matrix: List[List[int]]) -> str:
        """
        Convert matrix to string representation

        Args:
            matrix: Matrix to convert

        Returns:
            String representation
        """
        return '\\n'.join([' '.join(f'{val:2d}' for val in row) for row in matrix])

    def demonstrate_encryption(self, plaintext: str) -> Dict[str, Any]:
        """
        Demonstrate step-by-step encryption process

        Args:
            plaintext: Text to demonstrate encryption on

        Returns:
            Step-by-step demonstration
        """
        plaintext = self.preprocess_text(plaintext)
        if len(plaintext) < self.matrix_size:
            plaintext += 'X' * (self.matrix_size - len(plaintext))

        numbers = self.text_to_numbers(plaintext)
        blocks = [numbers[i:i + self.matrix_size] for i in range(0, len(numbers), self.matrix_size)]

        demonstration = {
            'plaintext': plaintext,
            'numbers': numbers,
            'blocks': blocks,
            'key_matrix': self.key_matrix,
            'encrypted_blocks': []
        }

        for block in blocks:
            encrypted = self.matrix_multiply_mod(self.key_matrix, block, 26)
            demonstration['encrypted_blocks'].append(encrypted)

        return demonstration