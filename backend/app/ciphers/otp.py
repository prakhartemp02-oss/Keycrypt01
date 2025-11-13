"""One-Time Pad Cipher Implementation - Level 7 (Demo)"""

from . import CipherBase
from ..utils.crypto import generate_otp_key, hash_key_material
from typing import Dict, Any
import secrets
import string

class OTPCipher(CipherBase):
    """
    One-Time Pad (OTP) Cipher - Theoretical perfect secrecy (demonstration)

    Educational Level: 7
    Historical Context: Patented by Gilbert Vernam in 1917. Proven unbreakable by
    Claude Shannon in 1949 when used correctly.
    Weakness: Key management challenges in practice
    """

    def __init__(self, key: str = None, **kwargs):
        """
        Initialize One-Time Pad cipher

        Args:
            key: Random key (must be same length as message, never reused)
        """
        if key is None:
            # For demonstration, generate a random key
            # In practice, this would come from a secure key source
            self.key = generate_otp_key(10)  # Default length for demo
        else:
            # Validate key
            if not key.isalpha() or not key.isupper():
                raise ValueError("OTP key must contain only uppercase letters")
            self.key = key

    def encrypt(self, plaintext: str) -> str:
        """
        Encrypt using One-Time Pad (XOR operation on letters)

        Args:
            plaintext: Text to encrypt

        Returns:
            Ciphertext
        """
        plaintext = self.preprocess_text(plaintext)

        # Pad key to match plaintext length
        if len(self.key) < len(plaintext):
            raise ValueError("Key must be at least as long as plaintext for OTP")

        ciphertext = []
        for i, char in enumerate(plaintext):
            if char.isalpha():
                # Convert to numbers (A=0, B=1, etc.)
                plain_num = ord(char) - ord('A')
                key_num = ord(self.key[i]) - ord('A')

                # XOR operation (addition modulo 26 for letters)
                cipher_num = (plain_num + key_num) % 26
                ciphertext.append(chr(cipher_num + ord('A')))
            else:
                ciphertext.append(char)

        # Store the key portion used for decryption
        self.used_key = self.key[:len(plaintext)]

        return ''.join(ciphertext)

    def decrypt(self, ciphertext: str) -> str:
        """
        Decrypt One-Time Pad (reverse XOR operation)

        Args:
            ciphertext: Text to decrypt

        Returns:
            Plaintext
        """
        ciphertext = self.preprocess_text(ciphertext)

        # Use the key that was used for encryption
        key_to_use = getattr(self, 'used_key', self.key)
        if len(key_to_use) < len(ciphertext):
            raise ValueError("Insufficient key material for decryption")

        plaintext = []
        for i, char in enumerate(ciphertext):
            if char.isalpha():
                # Convert to numbers
                cipher_num = ord(char) - ord('A')
                key_num = ord(key_to_use[i]) - ord('A')

                # Reverse XOR operation
                plain_num = (cipher_num - key_num) + 26  # Add 26 to handle negative
                plain_num = plain_num % 26
                plaintext.append(chr(plain_num + ord('A')))
            else:
                plaintext.append(char)

        return ''.join(plaintext)

    def generate_keys(self) -> Dict[str, Any]:
        """
        Generate cipher key material

        Returns:
            Dictionary containing OTP key
        """
        return {
            'key': self.key,
            'algorithm': 'otp'
        }

    def get_metadata(self) -> Dict[str, Any]:
        """
        Get cipher metadata for storage

        Returns:
            Cipher metadata
        """
        return {
            'cipher': 'One-Time Pad',
            'level': 7,
            'key_length': len(self.key),
            'key_hash': hash_key_material({'key': self.key}),
            'algorithm_params': {
                'type': 'perfect_secrecy',
                'key_requirement': 'key_length >= message_length',
                'usage_limit': 'never_reuse'
            }
        }

    def get_name(self) -> str:
        """Get cipher name"""
        return "One-Time Pad (Demo)"

    def get_level(self) -> int:
        """Get difficulty level"""
        return 7

    def get_educational_content(self) -> Dict[str, str]:
        """
        Get educational content about this cipher

        Returns:
            Educational information
        """
        return {
            'historical_context': (
                "Patented by Gilbert Vernam in 1917 for telegraph encryption. "
                "Claude Shannon mathematically proved its perfect secrecy in 1949. "
                "Used for Soviet-US communications during the Cold War and red phone hotlines."
            ),
            'how_it_works': (
                "Each message is combined with a random key of equal length using XOR operation. "
                "If the key is truly random, never reused, and kept secret, the cipher provides "
                "perfect secrecy - the ciphertext reveals no information about the plaintext."
            ),
            'weakness_explanation': (
                "Theoretical perfection but practical challenges: 1) Key distribution problem, "
                "2) Key must never be reused (vulnerable to two-time pad attacks), 3) Key generation "
                "requires true randomness, 4) Key storage and management complexities."
            ),
            'modern_relevance': (
                "Foundation for modern stream ciphers and one-time authentication. "
                "Principles used in quantum key distribution. Demonstrates the fundamental limits "
                "of classical cryptography and importance of key management."
            )
        }

    def demonstrate_perfect_secrecy(self, plaintext: str) -> Dict[str, Any]:
        """
        Demonstrate perfect secrecy property

        Args:
            plaintext: Text to demonstrate on

        Returns:
            Demonstration showing uniform ciphertext distribution
        """
        plaintext = self.preprocess_text(plaintext)
        possible_ciphertexts = set()

        # Generate multiple random keys and show different ciphertexts
        sample_keys = []
        sample_ciphertexts = []

        for _ in range(10):
            random_key = generate_otp_key(len(plaintext))
            temp_otp = OTPCipher(key=random_key)
            ciphertext = temp_otp.encrypt(plaintext)
            sample_keys.append(random_key)
            sample_ciphertexts.append(ciphertext)
            possible_ciphertexts.add(ciphertext)

        return {
            'plaintext': plaintext,
            'sample_keys': sample_keys[:3],  # Show first 3
            'sample_ciphertexts': sample_ciphertexts[:3],
            'unique_ciphertexts_found': len(possible_ciphertexts),
            'theoretical_maximum': 26 ** len(plaintext),  # All possible ciphertexts
            'explanation': "Each key produces a different ciphertext, all equally likely"
        }

    def demonstrate_two_time_pad_vulnerability(self) -> Dict[str, Any]:
        """
        Demonstrate why key reuse breaks OTP security

        Returns:
            Security demonstration
        """
        # Two different plaintexts encrypted with same key (SECURITY VIOLATION)
        key = "RANDOMKEY"
        plaintext1 = "SECRET"
        plaintext2 = "MESSAGE"

        otp = OTPCipher(key=key)

        # Encrypt both with same key (insecure!)
        cipher1 = otp.encrypt(plaintext1)
        cipher2 = otp.encrypt(plaintext2)

        # Show how XOR of ciphertexts reveals XOR of plaintexts
        # C1 ⊕ C2 = (P1 ⊕ K) ⊕ (P2 ⊕ K) = P1 ⊕ P2
        xor_result = self.xor_strings(cipher1, cipher2)
        plaintext_xor = self.xor_strings(plaintext1, plaintext2)

        return {
            'key': key,
            'plaintext1': plaintext1,
            'plaintext2': plaintext2,
            'ciphertext1': cipher1,
            'ciphertext2': cipher2,
            'ciphertext_xor': xor_result,
            'plaintext_xor': plaintext_xor,
            'vulnerability_explanation': "XOR of ciphertexts equals XOR of plaintexts when same key is reused"
        }

    def xor_strings(self, text1: str, text2: str) -> str:
        """
        XOR two strings letter by letter

        Args:
            text1: First string
            text2: Second string

        Returns:
            XOR result as string of numbers
        """
        result = []
        min_len = min(len(text1), len(text2))

        for i in range(min_len):
            num1 = ord(text1[i]) - ord('A')
            num2 = ord(text2[i]) - ord('A')
            xor_num = num1 ^ num2
            result.append(str(xor_num).zfill(2))

        return ' '.join(result)

    def analyze_key_randomness(self, key: str) -> Dict[str, Any]:
        """
        Analyze randomness of a key (educational)

        Args:
            key: Key to analyze

        Returns:
            Randomness analysis
        """
        # Simple frequency analysis
        frequency = {}
        for char in key:
            frequency[char] = frequency.get(char, 0) + 1

        # Calculate expected frequency for truly random
        expected_freq = len(key) / 26

        # Chi-squared test for randomness
        chi_squared = 0
        for char in string.ascii_uppercase:
            observed = frequency.get(char, 0)
            chi_squared += ((observed - expected_freq) ** 2) / expected_freq

        return {
            'key_length': len(key),
            'letter_frequency': frequency,
            'expected_frequency': expected_freq,
            'chi_squared': chi_squared,
            'randomness_score': "Good" if chi_squared < 40 else "Poor",  # Rough threshold
            'warning': "This is a simple analysis - true randomness requires more sophisticated tests"
        }