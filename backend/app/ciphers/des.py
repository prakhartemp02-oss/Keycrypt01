"""DES/3DES Cipher Implementation - Level 8"""

from . import CipherBase
from ..utils.crypto import generate_des_key, hash_key_material
from typing import Dict, Any, Union
import secrets
import os
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import base64

class DESCipher(CipherBase):
    """
    DES/3DES Cipher - Symmetric block cipher using pycryptodome

    Educational Level: 8
    Historical Context: DES adopted as FIPS standard in 1977. 3DES developed
    in 1990s to address DES security concerns.
    Weakness: 56-bit key too small for modern security, vulnerable to brute force
    """

    def __init__(self, key: bytes = None, mode: str = 'DES', **kwargs):
        """
        Initialize DES/3DES cipher

        Args:
            key: 8-byte key for DES, 16/24 bytes for 3DES
            mode: 'DES', '2DES', or '3DES'
        """
        self.mode = mode.upper()
        if self.mode not in ['DES', '2DES', '3DES']:
            raise ValueError("Mode must be 'DES', '2DES', or '3DES'")

        if key is None:
            if self.mode == 'DES':
                self.key = generate_des_key()  # 8 bytes
            elif self.mode == '2DES':
                self.key = generate_des_key() + generate_des_key()  # 16 bytes
            else:  # 3DES
                self.key = generate_des_key() + generate_des_key() + generate_des_key()  # 24 bytes
        else:
            self.key = key
            self.validate_key()

    def validate_key(self):
        """Validate key length for chosen mode"""
        expected_lengths = {
            'DES': 8,
            '2DES': 16,
            '3DES': 24
        }

        expected = expected_lengths.get(self.mode)
        if len(self.key) != expected:
            raise ValueError(f"Key must be {expected} bytes for {self.mode} mode")

    def text_to_bytes(self, text: str) -> bytes:
        """Convert text to bytes using ASCII encoding"""
        return text.encode('ascii')

    def bytes_to_text(self, data: bytes) -> str:
        """Convert bytes to text using ASCII encoding"""
        return data.decode('ascii')

    def encrypt_des(self, plaintext: str, key: bytes) -> str:
        """Encrypt using single DES"""
        cipher = DES.new(key, DES.MODE_ECB)
        padded_text = pad(self.text_to_bytes(plaintext), DES.block_size)
        encrypted = cipher.encrypt(padded_text)
        return base64.b64encode(encrypted).decode('ascii')

    def decrypt_des(self, ciphertext: str, key: bytes) -> str:
        """Decrypt using single DES"""
        try:
            cipher = DES.new(key, DES.MODE_ECB)
            encrypted_bytes = base64.b64decode(ciphertext)
            decrypted = cipher.decrypt(encrypted_bytes)
            unpadded = unpad(decrypted, DES.block_size)
            return self.bytes_to_text(unpadded)
        except (ValueError, KeyError) as e:
            raise ValueError(f"Decryption failed: {str(e)}")

    def encrypt_2des(self, plaintext: str) -> str:
        """Encrypt using double DES (actually triple DES with encrypt-decrypt-encrypt)"""
        key1 = self.key[:8]
        key2 = self.key[8:16]

        # Encrypt with key1, decrypt with key2, encrypt with key1 again
        step1 = self.encrypt_des(plaintext, key1)
        step2 = self.decrypt_des(step1, key2)
        result = self.encrypt_des(step2, key1)
        return result

    def decrypt_2des(self, ciphertext: str) -> str:
        """Decrypt using double DES"""
        key1 = self.key[:8]
        key2 = self.key[8:16]

        # Reverse the process
        step1 = self.decrypt_des(ciphertext, key1)
        step2 = self.encrypt_des(step1, key2)
        result = self.decrypt_des(step2, key1)
        return result

    def encrypt_3des(self, plaintext: str) -> str:
        """Encrypt using triple DES (EDE mode)"""
        key1 = self.key[:8]
        key2 = self.key[8:16]
        key3 = self.key[16:24]

        # Encrypt with key1, decrypt with key2, encrypt with key3
        step1 = self.encrypt_des(plaintext, key1)
        step2 = self.decrypt_des(step1, key2)
        result = self.encrypt_des(step2, key3)
        return result

    def decrypt_3des(self, ciphertext: str) -> str:
        """Decrypt using triple DES"""
        key1 = self.key[:8]
        key2 = self.key[8:16]
        key3 = self.key[16:24]

        # Reverse the process
        step1 = self.decrypt_des(ciphertext, key3)
        step2 = self.encrypt_des(step1, key2)
        result = self.decrypt_des(step2, key1)
        return result

    def encrypt(self, plaintext: str) -> str:
        """
        Encrypt plaintext using DES/3DES

        Args:
            plaintext: Text to encrypt (will be padded to 8-byte blocks)

        Returns:
            Base64-encoded ciphertext
        """
        plaintext = self.preprocess_text(plaintext)

        if self.mode == 'DES':
            return self.encrypt_des(plaintext, self.key)
        elif self.mode == '2DES':
            return self.encrypt_2des(plaintext)
        else:  # 3DES
            return self.encrypt_3des(plaintext)

    def decrypt(self, ciphertext: str) -> str:
        """
        Decrypt ciphertext using DES/3DES

        Args:
            ciphertext: Base64-encoded ciphertext

        Returns:
            Plaintext
        """
        if self.mode == 'DES':
            return self.decrypt_des(ciphertext, self.key)
        elif self.mode == '2DES':
            return self.decrypt_2des(ciphertext)
        else:  # 3DES
            return self.decrypt_3des(ciphertext)

    def generate_keys(self) -> Dict[str, Any]:
        """
        Generate cipher key material

        Returns:
            Dictionary containing encryption key(s)
        """
        return {
            'key': base64.b64encode(self.key).decode('ascii'),
            'mode': self.mode,
            'algorithm': 'des'
        }

    def get_metadata(self) -> Dict[str, Any]:
        """
        Get cipher metadata for storage

        Returns:
            Cipher metadata
        """
        return {
            'cipher': f'{self.mode}',
            'level': 8,
            'mode': self.mode,
            'key_size': len(self.key) * 8,  # in bits
            'block_size': 64,  # 8 bytes
            'key_hash': hash_key_material({'key': base64.b64encode(self.key).decode('ascii')}),
            'algorithm_params': {
                'type': 'block_cipher',
                'operation_mode': 'ECB',  # Using ECB for simplicity
                'padding': 'PKCS7'
            }
        }

    def get_name(self) -> str:
        """Get cipher name"""
        return f"{self.mode}"

    def get_level(self) -> int:
        """Get difficulty level"""
        return 8

    def get_educational_content(self) -> Dict[str, str]:
        """
        Get educational content about this cipher

        Returns:
            Educational information
        """
        content = {
            'historical_context': (
                "DES (Data Encryption Standard) was adopted as FIPS standard in 1977. "
                "Developed by IBM, based on Lucifer cipher. 3DES (Triple DES) developed in 1990s "
                "to address DES's growing vulnerability to brute force attacks."
            ),
            'how_it_works': (
                "DES is a Feistel network cipher with 16 rounds, 64-bit blocks, and 56-bit effective key. "
                "It uses substitution (S-boxes) and permutation (P-boxes) for confusion and diffusion. "
                "3DES applies DES three times with different keys to increase security."
            ),
            'weakness_explanation': (
                f"DES's 56-bit key is vulnerable to exhaustive key search (possible in hours). "
                "3DES improves this to 112-bit security but is much slower. Both use ECB mode which "
                "has vulnerabilities with repeated blocks (demonstrational choice for simplicity)."
            ),
            'modern_relevance': (
                "Foundation for modern symmetric cryptography. Introduced key concepts like "
                "Feistel networks, S-boxes, and avalanche effect. Replaced by AES in most applications "
                "but still used in some legacy systems (ATM networks, payment systems)."
            )
        }

        if self.mode == '3DES':
            content['how_it_works'] += (
                " 3DES uses EDE (Encrypt-Decrypt-Encrypt) with three 56-bit keys: "
                "C = E3(D2(E1(P))). This maintains backward compatibility with single DES "
                "when K1=K2=K3."
            )

        return content

    def demonstrate_feistel_structure(self, plaintext: str) -> Dict[str, Any]:
        """
        Demonstrate Feistel network structure (simplified)

        Args:
            plaintext: Text to demonstrate on

        Returns:
            Feistel structure demonstration
        """
        # Simplified demonstration of Feistel properties
        # Real DES has complex S-boxes and permutations

        plaintext = self.preprocess_text(plaintext)
        if len(plaintext) % 8 != 0:
            plaintext = plaintext.ljust(((len(plaintext) // 8) + 1) * 8, 'X')

        return {
            'plaintext': plaintext,
            'block_size': 64,  # bits
            'key_size': 56,    # effective bits for DES
            'rounds': 16,
            'structure': 'Feistel network',
            'operations': [
                'Initial permutation',
                '16 rounds of Feistel functions',
                'Final permutation',
                'PKCS7 padding'
            ],
            'note': 'This is a high-level demonstration - actual DES uses complex mathematical operations'
        }

    def analyze_security_level(self) -> Dict[str, Any]:
        """
        Analyze security level of chosen DES mode

        Returns:
            Security analysis
        """
        security_info = {
            'DES': {
                'key_space': '2^56 ≈ 7.2 × 10^16',
                'security_level': 'Broken by modern standards',
                'brute_force_time': 'Hours with modern hardware',
                'year_broken': '1998 (EFF DES cracker)'
            },
            '2DES': {
                'key_space': '2^112 ≈ 5.2 × 10^33',
                'security_level': 'Weak (meet-in-the-middle attack)',
                'effective_security': '2^57 operations',
                'vulnerability': 'Meet-in-the-middle attack'
            },
            '3DES': {
                'key_space': '2^112 ≈ 5.2 × 10^33',
                'security_level': 'Moderate (deprecated)',
                'effective_security': '112 bits',
                'status': 'Being phased out in favor of AES'
            }
        }

        mode_info = security_info[self.mode]
        mode_info['recommended_alternative'] = 'AES-128/256'
        mode_info['performance_impact'] = f'{3 if self.mode == "3DES" else 1}x slower than modern alternatives'

        return mode_info