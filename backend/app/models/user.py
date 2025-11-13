"""User model for KeyCrypt"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db

class User(db.Model):
    """User model for optional authentication"""

    __tablename__ = 'users'

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # User information
    email = Column(String(255), unique=True, nullable=True)  # Optional email
    username = Column(String(100), unique=True, nullable=True)  # Optional username
    password_hash = Column(String(255), nullable=True)  # Optional password

    # User preferences
    display_name = Column(String(100), nullable=True)
    is_guest = Column(Boolean, default=True)  # True for anonymous users

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

    # Relationships
    games = relationship("Game", back_populates="user")
    progress = relationship("UserProgress", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f'<User {self.email or self.id}>'

    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)
        self.is_guest = False

    def check_password(self, password):
        """Check password against hash"""
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    def to_dict(self, include_sensitive=False):
        """Convert to dictionary for API responses"""
        data = {
            'user_id': str(self.id),
            'username': self.username,
            'display_name': self.display_name or f'Player {str(self.id)[:8]}',
            'is_guest': self.is_guest,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

        if include_sensitive:
            data['email'] = self.email

        return data

    @classmethod
    def create_guest_user(cls):
        """Create a guest user (anonymous)"""
        guest = cls(
            is_guest=True,
            display_name=f'Guest {uuid.uuid4().hex[:8]}'
        )
        return guest

    @classmethod
    def get_or_create_guest(cls, user_id: str = None):
        """
        Get existing user or create guest user

        Args:
            user_id: Optional existing user ID

        Returns:
            User instance
        """
        if user_id:
            user = cls.query.filter_by(id=user_id).first()
            if user:
                return user

        return cls.create_guest_user()

    def update_last_login(self):
        """Update last login timestamp"""
        self.last_login = datetime.utcnow()
        self.updated_at = datetime.utcnow()