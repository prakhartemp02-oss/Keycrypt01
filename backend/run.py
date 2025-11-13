"""Flask application entry point for KeyCrypt backend"""

import os
import sys

# Add the app directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db

def create_tables():
    """Create database tables"""
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")

def seed_dictionary():
    """Seed the word dictionary"""
    from app.models.game import WordDictionary

    # Basic word list for demonstration
    words = [
        # Level 1-3 words (shorter, common)
        "APPLE", "BRAVO", "CIPHER", "DIGIT", "EARTH", "FLAME", "GHOST", "HOUSE",
        "JUICE", "KNIFE", "LEMON", "MOUSE", "NIGHT", "OCEAN", "PAPER", "QUEEN",
        "RADIO", "STONE", "TABLE", "UNCLE", "VOICE", "WATER", "YOUTH", "ZEBRA",

        # Level 4-6 words (medium length)
        "CASTLE", "DRAGON", "FOREST", "GARDEN", "HARBOR", "ISLAND", "JUNGLE",
        "KITCHEN", "LIBRARY", "MONSTER", "NATURE", "OFFICER", "PALACE", "QUARTER",
        "RAINBOW", "SCHOOL", "TEMPLE", "UNIFORM", "VILLAGE", "WARRIOR", "XYLOPHONE",

        # Level 7-9 words (longer, more complex)
        "ADVENTURE", "BUTTERFLY", "CHOCOLATE", "DIAMOND", "ELEPHANT", "FORTRESS",
        "GALAXY", "HELICOPTER", "ILLUMINATE", "JAVASCRIPT", "KEYBOARD", "LIGHTHOUSE",
        "MOUNTAIN", "NOSTALGIA", "OCCUPATION", "PARADISE", "QUANTUM", "RAINFOREST",
        "SYMPHONY", "TECHNOLOGY", "UNIVERSE", "VOLCANO", "WILDERNESS", "XENOPHOBIA"
    ]

    # Categorize words by difficulty
    for i, word in enumerate(words):
        level = (i % 3) + 1  # Rotate through levels 1-3 for base difficulty
        if len(word) >= 7:
            level = min(level + 3, 6)  # Medium words get higher levels
        if len(word) >= 9:
            level = min(level + 3, 9)  # Long words get highest levels

        difficulty = (len(word) - 4) // 2  # 0-10 scale
        difficulty = min(max(difficulty, 0), 10)

        word_entry = WordDictionary(
            word=word,
            length=len(word),
            category='common',
            difficulty_score=difficulty,
            frequency_rank=i + 1,
            definition=f"A {len(word)}-letter word"
        )

        db.session.add(word_entry)

    try:
        db.session.commit()
        print(f"Successfully seeded {len(words)} words into the dictionary!")
    except Exception as e:
        db.session.rollback()
        print(f"Error seeding dictionary: {e}")

if __name__ == '__main__':
    app = create_app()

    # Create tables if they don't exist
    create_tables()

    # Seed dictionary if it's empty
    from app.models.game import WordDictionary
    if WordDictionary.query.count() == 0:
        print("Dictionary is empty, seeding with sample words...")
        seed_dictionary()

    # Run the application
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'

    print(f"Starting KeyCrypt backend server on port {port}")
    print(f"Debug mode: {debug}")
    print(f"Database URL: {app.config['SQLALCHEMY_DATABASE_URI']}")

    app.run(host='0.0.0.0', port=port, debug=debug)