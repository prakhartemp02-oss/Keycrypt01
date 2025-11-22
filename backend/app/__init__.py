"""KeyCrypt Backend Application"""

import os

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from .config import config

# Initialize extensions
db = SQLAlchemy()

def create_app(config_name=None):
    """Application factory"""
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'default')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    CORS(app, origins=app.config['CORS_ORIGINS'])

    # Register blueprints
    from .routes.game import game_bp
    from .routes.auth import auth_bp

    app.register_blueprint(game_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api')

    # Create database tables
    with app.app_context():
        db.create_all()

    # Health check endpoint
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'service': 'keycrypt-backend'}

    return app