"""RSA Cipher Implementation - Level 9"""

from . import CipherBase
from ..utils.crypto import hash_key_material
from typing import Dict, Any, Tuple
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import secrets

class RSACipher(CipherBase):
    """
    RSA Cipher - Asymmetric encryption using public/private key pairs

    Educational Level: 9
    Historical Context: Invented by Ron Rivest, Adi Shamir, and Leonard Adleman in 1977.
    One of the first practical public-key cryptosystems.
    Weakness: Requires large key sizes, vulnerable to quantum attacks
    """

    def __init__(self, public_key: bytes = None, private_key: bytes = None, **kwargs):
        """
        Initialize RSA cipher

        Args:
            public_key: PEM-encoded public key
            private_key: PEM-encoded private key
        """
        self.key_size = 2048  # Use 2048-bit keys for demonstration

        if public_key is None or private_key is None:
            # Generate new key pair
            self.key = RSA.generate(self.key_size)
            self.public_key = self.key.publickey()
        else:
            # Load existing keys
            self.public_key = RSA.import_key(public_key)
            self.private_key = RSA.import_key(private_key)

        # Create cipher objects
        self.encrypt_cipher = PKCS1_OAEP.new(self.public_key)
        self.decrypt_cipher = PKCS1_OAEP.new(self.private_key if hasattr(self, 'private_key') else self.public_key)

    def generate_keys(self) -> Dict[str, Any]:
        """
        Generate RSA key pair

        Returns:
            Dictionary containing public and private keys
        """
        return {
            'public_key': self.public_key.export_key().decode('ascii'),
            'private_key': self.private_key.export_key().decode('ascii'),
            'key_size': self.key_size,
            'algorithm': 'rsa'
        }

    def get_metadata(self) -> Dict[str, Any]:
        """
        Get cipher metadata for storage

        Returns:
            Cipher metadata
        """
        return {
            'cipher': 'RSA',
            'level': 9,
            'key_size': self.key_size,
            'public_key_modulus': self.public_key.n,
            'public_key_exponent': self.public_key.e,
            'key_hash': hash_key_material({
                'modulus': str(self.public_key.n),
                'exponent': str(self.public_key.e)
            }),
            'algorithm_params': {
                'type': 'asymmetric',
                'padding': 'OAEP',
                'key_pair': True
            }
        }

    def text_to_bytes(self, text: str) -> bytes:
        """Convert text to bytes"""
        return text.encode('utf-8')

    def bytes_to_text(self, data: bytes) -> str:
        """Convert bytes to text"""
        return data.decode('utf-8')

    def encrypt(self, plaintext: str) -> str:
        """
        Encrypt using RSA public key

        Args:
            plaintext: Text to encrypt

        Returns:
            Base64-encoded ciphertext
        """
        plaintext = self.preprocess_text(plaintext)
        plaintext_bytes = self.text_to_bytes(plaintext)

        # RSA has size limitations, encrypt in chunks if necessary
        max_chunk_size = (self.key_size // 8) - 42  # OAEP padding overhead

        if len(plaintext_bytes) <= max_chunk_size:
            # Single block encryption
            encrypted = self.encrypt_cipher.encrypt(plaintext_bytes)
            return base64.b64encode(encrypted).decode('ascii')
        else:
            # For educational purposes, split into smaller chunks
            # (In practice, you'd use hybrid encryption with AES for data)
            encrypted_chunks = []
            for i in range(0, len(plaintext_bytes), max_chunk_size):
                chunk = plaintext_bytes[i:i + max_chunk_size]
                encrypted_chunk = self.encrypt_cipher.encrypt(chunk)
                encrypted_chunks.append(base64.b64encode(encrypted_chunk).decode('ascii'))

            return '|'.join(encrypted_chunks)

    def decrypt(self, ciphertext: str) -> str:
        """
        Decrypt using RSA private key

        Args:
            ciphertext: Base64-encoded ciphertext

        Returns:
            Plaintext
        """
        if '|' in ciphertext:
            # Multiple chunks
            encrypted_chunks = ciphertext.split('|')
            plaintext_bytes = b''

            for chunk in encrypted_chunks:
                encrypted_bytes = base64.b64decode(chunk)
                decrypted_chunk = self.decrypt_cipher.decrypt(encrypted_bytes)
                plaintext_bytes += decrypted_chunk
        else:
            # Single chunk
            encrypted_bytes = base64.b64decode(ciphertext)
            plaintext_bytes = self.decrypt_cipher.decrypt(encrypted_bytes)

        return self.bytes_to_text(plaintext_bytes)

    def get_name(self) -> str:
        """Get cipher name"""
        return "RSA"

    def get_level(self) -> int:
        """Get difficulty level"""
        return 9

    def get_educational_content(self) -> Dict[str, str]:
        """
        Get educational content about this cipher

        Returns:
            Educational information
        """
        return {
            'historical_context': (
                "Invented in 1977 by Ron Rivest, Adi Shamir, and Leonard Adleman at MIT. "
                "One of the first practical public-key cryptosystems. Named after their initials. "
                "Revolutionized cryptography by enabling secure communication without shared secrets."
            ),
            'how_it_works': (
                "Based on the mathematical difficulty of factoring large prime numbers. "
                "Uses a public key (n, e) for encryption and private key (n, d) for decryption. "
                "Encryption: C = M^e mod n. Decryption: M = C^d mod n. Security relies on d being "
                "computationally infeasible to derive from e and n without knowing the prime factors."
            ),
            'weakness_explanation': (
                "Requires large key sizes (2048+ bits) for security. Vulnerable to quantum computers "
                "(Shor's algorithm). Computationally expensive for large data. Key distribution and "
                "certificate validation are complex. Side-channel attacks possible."
            ),
            'modern_relevance': (
                "Foundation of modern secure communication. Used in TLS/SSL, digital signatures, "
                "email encryption (PGP), cryptocurrency, and secure key exchange. Core technology "
                "for internet security infrastructure."
            )
        }

    def demonstrate_key_generation(self) -> Dict[str, Any]:
        """
        Demonstrate RSA key generation process

        Returns:
            Key generation demonstration
        """
        # Generate a smaller key for demonstration purposes
        demo_key = RSA.generate(512)  # Smaller key for speed

        return {
            'prime_p': demo_key.p,
            'prime_q': demo_key.q,
            'modulus_n': demo_key.n,  # p * q
            'phi_n': demo_key.n - demo_key.p - demo_key.q + 1,  # (p-1)(q-1)
            'public_exponent_e': demo_key.e,
            'private_exponent_d': demo_key.d,
            'explanation': {
                'modulus': 'n = p * q (product of two large primes)',
                'phi': 'φ(n) = (p-1)(q-1) (Euler\'s totient function)',
                'public_key': '(n, e) where e is chosen to be coprime with φ(n)',
                'private_key': 'd is the modular inverse of e mod φ(n)',
                'security': 'Relies on difficulty of factoring n to find p and q'
            }
        }

    def demonstrate_asymmetric_property(self, message: str) -> Dict[str, Any]:
        """
        Demonstrate asymmetric encryption property

        Args:
            message: Message to demonstrate with

        Returns:
            Asymmetric property demonstration
        """
        # Encrypt with public key
        encrypted_with_pub = self.encrypt(message)

        # Try to decrypt with public key (should fail)
        try:
            decrypted_with_pub = self.decrypt(encrypted_with_pub)
            pub_decrypt_success = True
        except Exception:
            decrypted_with_pub = "Decryption failed (as expected)"
            pub_decrypt_success = False

        # Decrypt with private key (should succeed)
        decrypted_with_priv = self.decrypt(encrypted_with_pub)

        return {
            'original_message': message,
            'encrypted_with_public_key': encrypted_with_pub[:50] + '...' if len(encrypted_with_pub) > 50 else encrypted_with_pub,
            'decrypted_with_public_key': decrypted_with_pub,
            'decrypted_with_private_key': decrypted_with_priv,
            'public_key_decryption_successful': pub_decrypt_success,
            'asymmetric_property': 'Only the holder of the private key can decrypt messages encrypted with the public key'
        }

    def analyze_key_security(self) -> Dict[str, Any]:
        """
        Analyze RSA key security parameters

        Returns:
            Security analysis
        """
        key_sizes = {
            512: {
                'security_bits': 64,
                'factorization_time': 'Hours on modern computers',
                'status': 'Broken'
            },
            1024: {
                'security_bits': 80,
                'factorization_time': 'Days to weeks with modern hardware',
                'status': 'Weak'
            },
            2048: {
                'security_bits': 112,
                'factorization_time': 'Years with current technology',
                'status': 'Secure (2024)'
            },
            3072: {
                'security_bits': 128,
                'factorization_time': 'Decades with current technology',
                'status': 'Very Secure'
            },
            4096: {
                'security_bits': 152,
                'factorization_time': 'Centuries with current technology',
                'status': 'Very Secure'
            }
        }

        current_security = key_sizes.get(self.key_size, {'status': 'Unknown'})

        return {
            'current_key_size': self.key_size,
            'current_security': current_security,
            'modulus_size_bits': self.key_size,
            'modulus_size_bytes': self.key_size // 8,
            'key_comparison': key_sizes,
            'quantum_vulnerability': 'Vulnerable to quantum computers (Shor\'s algorithm)',
            'recommended_minimum': '2048 bits for current applications'
        }

    def get_public_key_info(self) -> Dict[str, Any]:
        """
        Get information about the public key

        Returns:
            Public key information
        """
        return {
            'modulus_n_hex': hex(self.public_key.n),
            'modulus_n_decimal': str(self.public_key.n),
            'modulus_size_bits': self.public_key.size_in_bits(),
            'public_exponent_e': self.public_key.e,
            'public_key_pem': self.public_key.export_key().decode('ascii'),
            'usage': 'This key can be freely shared for others to encrypt messages to you'
        }