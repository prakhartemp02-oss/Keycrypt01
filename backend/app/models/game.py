"""Game-related database models"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, JSON, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from .. import db

class Game(db.Model):
    """Game session model"""

    __tablename__ = 'games'

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Foreign key to optional user
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)

    # Game configuration
    level = Column(Integer, nullable=False)
    dictionary_category = Column(String(50), default='common')
    attempts_allowed = Column(Integer, default=6)
    attempts_remaining = Column(Integer, nullable=False)

    # Encrypted game data
    secret_word_ciphertext = Column(Text, nullable=False)
    hint_ciphertexts = Column(JSON, nullable=False)
    cipher_metadata = Column(JSON, nullable=False)

    # Game state
    game_status = Column(String(20), default='ongoing')  # ongoing, won, lost, abandoned

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="games")
    attempts = relationship("GameAttempt", back_populates="game", cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Game {self.id} level={self.level} status={self.game_status}>'

    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'game_id': str(self.id),
            'level': self.level,
            'attempts_allowed': self.attempts_allowed,
            'attempts_remaining': self.attempts_remaining,
            'encrypted_meta': {
                'cipher': self.cipher_metadata.get('cipher', 'Unknown'),
                'ciphertext': self.secret_word_ciphertext,
                'hint_ciphertexts': self.hint_ciphertexts,
                'encryption_metadata': self.cipher_metadata
            },
            'hint_unlock_rules': {
                'first_hint': 3,
                'second_hint': 5
            },
            'game_status': self.game_status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class GameAttempt(db.Model):
    """Individual game attempt model"""

    __tablename__ = 'game_attempts'

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Foreign key to game
    game_id = Column(UUID(as_uuid=True), ForeignKey('games.id'), nullable=False)

    # Attempt data
    guess_text = Column(String(255), nullable=False)
    feedback = Column(JSON, nullable=False)  # Wordle-style feedback
    attempt_number = Column(Integer, nullable=False)

    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    game = relationship("Game", back_populates="attempts")

    def __repr__(self):
        return f'<GameAttempt {self.id} game={self.game_id} guess={self.guess_text}>'

    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'attempt_id': str(self.id),
            'game_id': str(self.game_id),
            'guess': self.guess_text,
            'feedback': self.feedback,
            'attempt_number': self.attempt_number,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class UserProgress(db.Model):
    """User progress tracking model"""

    __tablename__ = 'user_progress'

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Foreign key to user
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)

    # Level-specific progress
    level = Column(Integer, nullable=False)

    # Statistics
    games_won = Column(Integer, default=0)
    games_played = Column(Integer, default=0)
    best_score = Column(Integer)  # Fewest attempts to win
    total_time_seconds = Column(Integer, default=0)
    average_hints_used = Column(Float, default=0.0)

    # Timestamps
    last_played = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="progress")

    # Unique constraint
    __table_args__ = (
        db.UniqueConstraint('user_id', 'level', name='unique_user_level_progress'),
    )

    def __repr__(self):
        return f'<UserProgress user={self.user_id} level={self.level} wins={self.games_won}>'

    def to_dict(self):
        """Convert to dictionary for API responses"""
        win_rate = (self.games_won / self.games_played * 100) if self.games_played > 0 else 0

        return {
            'user_id': str(self.user_id),
            'level': self.level,
            'games_won': self.games_won,
            'games_played': self.games_played,
            'win_rate': round(win_rate, 2),
            'best_score': self.best_score,
            'total_time_seconds': self.total_time_seconds,
            'average_hints_used': round(self.average_hints_used, 2),
            'last_played': self.last_played.isoformat() if self.last_played else None
        }

    def update_statistics(self, won: bool, attempts_used: int, hints_used: int, time_seconds: int):
        """Update progress statistics after a game"""
        self.games_played += 1
        if won:
            self.games_won += 1
            if self.best_score is None or attempts_used < self.best_score:
                self.best_score = attempts_used

        # Update time and hints averages
        if self.games_played > 0:
            total_time = self.total_time_seconds + time_seconds
            total_hints = self.average_hints_used * (self.games_played - 1) + hints_used
            self.total_time_seconds = total_time
            self.average_hints_used = total_hints / self.games_played

        self.updated_at = datetime.utcnow()
        self.last_played = datetime.utcnow()

class WordDictionary(db.Model):
    """Word dictionary for game secrets"""

    __tablename__ = 'word_dictionary'

    # Primary key
    id = Column(Integer, primary_key=True)

    # Word data
    word = Column(String(50), nullable=False, unique=True)
    length = Column(Integer, nullable=False)
    category = Column(String(50), default='common')
    difficulty_score = Column(Integer, default=0)  # 0-10, higher = more difficult

    # Metadata
    is_active = Column(Boolean, default=True)
    frequency_rank = Column(Integer)  # Optional: English frequency ranking
    definition = Column(Text)  # Optional: Word definition for hints

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<WordDictionary {self.word} length={self.length} category={self.category}>'

    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'word': self.word,
            'length': self.length,
            'category': self.category,
            'difficulty_score': self.difficulty_score,
            'is_active': self.is_active,
            'frequency_rank': self.frequency_rank
        }

    @classmethod
    def get_random_word(cls, level: int, category: str = None, max_length: int = None):
        """
        Get a random word appropriate for the level

        Args:
            level: Game level (affects word selection)
            category: Optional category filter
            max_length: Optional maximum word length

        Returns:
            Random WordDictionary entry or None
        """
        query = cls.query.filter(cls.is_active == True)

        if category:
            query = query.filter(cls.category == category)

        # Adjust word selection based on level
        if level <= 3:
            # Simple levels: shorter words
            query = query.filter(cls.length <= 6)
        elif level <= 6:
            # Intermediate levels: medium words
            query = query.filter(cls.length <= 8)
        else:
            # Advanced levels: longer words acceptable
            pass

        if max_length:
            query = query.filter(cls.length <= max_length)

        # Order by random and get first
        return query.order_by(db.func.random()).first()