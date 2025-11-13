import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""

    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///keycrypt.db')
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')

    # RSA Keys (per-server)
    RSA_PRIVATE_KEY_PATH = os.getenv('RSA_PRIVATE_KEY_PATH', 'keys/private.pem')
    RSA_PUBLIC_KEY_PATH = os.getenv('RSA_PUBLIC_KEY_PATH', 'keys/public.pem')

    # Encryption key for sensitive data
    MASTER_KEY = os.getenv('MASTER_KEY')
    if not MASTER_KEY:
        # Generate a key for development
        MASTER_KEY = Fernet.generate_key().decode()

    # Security settings
    RATE_LIMIT_REQUESTS = int(os.getenv('RATE_LIMIT_REQUESTS', '60'))
    RATE_LIMIT_WINDOW = int(os.getenv('RATE_LIMIT_WINDOW', '60'))  # seconds
    MAX_ATTEMPTS_PER_GAME = int(os.getenv('MAX_ATTEMPTS_PER_GAME', '6'))
    GAMES_PER_IP_PER_MINUTE = int(os.getenv('GAMES_PER_IP_PER_MINUTE', '5'))

    # Game settings
    WORD_DICTIONARY_PATH = os.getenv('WORD_DICTIONARY_PATH', 'database/words.txt')

    # CORS settings
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SQLALCHEMY_ECHO = False

    # Production security settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DATABASE_URL = 'sqlite:///:memory:'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}