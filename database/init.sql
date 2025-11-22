-- KeyCrypt Database Initialization Script
-- This script sets up the database schema for the KeyCrypt educational cryptography game

-- Enable UUID extension for PostgreSQL
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create users table (optional authentication)
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    display_name VARCHAR(100),
    is_guest BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create word dictionary table
CREATE TABLE IF NOT EXISTS word_dictionary (
    id SERIAL PRIMARY KEY,
    word VARCHAR(50) NOT NULL UNIQUE,
    length INTEGER NOT NULL,
    category VARCHAR(50) DEFAULT 'common',
    difficulty_score INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create games table
CREATE TABLE IF NOT EXISTS games (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    level INTEGER NOT NULL CHECK (level BETWEEN 1 AND 9),
    secret_word_ciphertext TEXT NOT NULL,
    hint_ciphertexts JSONB NOT NULL DEFAULT '{}',
    cipher_metadata JSONB NOT NULL DEFAULT '{}',
    attempts_allowed INTEGER DEFAULT 6,
    attempts_remaining INTEGER NOT NULL DEFAULT 6,
    game_status VARCHAR(20) DEFAULT 'ongoing' CHECK (game_status IN ('ongoing', 'won', 'lost', 'abandoned')),
    dictionary_category VARCHAR(50) DEFAULT 'common',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create game attempts table
CREATE TABLE IF NOT EXISTS game_attempts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    game_id UUID NOT NULL REFERENCES games(id) ON DELETE CASCADE,
    guess_text VARCHAR(255) NOT NULL,
    feedback JSONB NOT NULL DEFAULT '[]',
    attempt_number INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create user progress table
CREATE TABLE IF NOT EXISTS user_progress (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    level INTEGER NOT NULL CHECK (level BETWEEN 1 AND 9),
    games_won INTEGER DEFAULT 0,
    games_played INTEGER DEFAULT 0,
    best_score INTEGER, -- Fewest attempts to win
    total_time_seconds INTEGER DEFAULT 0,
    average_hints_used DECIMAL(3,2) DEFAULT 0.0,
    last_played TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, level)
);

-- Create user statistics table
CREATE TABLE IF NOT EXISTS user_statistics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    total_games_played INTEGER DEFAULT 0,
    total_games_won INTEGER DEFAULT 0,
    overall_win_rate DECIMAL(5,2) DEFAULT 0.0,
    levels_completed INTEGER DEFAULT 0,
    levels_unlocked INTEGER DEFAULT 1,
    best_overall_score INTEGER,
    total_time_seconds INTEGER DEFAULT 0,
    average_time_per_game INTEGER DEFAULT 0,
    total_hints_used INTEGER DEFAULT 0,
    average_hints_per_game DECIMAL(3,2) DEFAULT 0.0,
    current_streak INTEGER DEFAULT 0,
    best_streak INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id)
);

-- Create achievements table
CREATE TABLE IF NOT EXISTS achievements (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT NOT NULL,
    icon VARCHAR(50) DEFAULT '🏆',
    category VARCHAR(50) DEFAULT 'general',
    requirement_type VARCHAR(50) NOT NULL, -- 'wins', 'streak', 'perfect_game', etc.
    requirement_value INTEGER NOT NULL,
    points INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create user achievements table
CREATE TABLE IF NOT EXISTS user_achievements (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    achievement_id UUID NOT NULL REFERENCES achievements(id) ON DELETE CASCADE,
    unlocked_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    progress INTEGER DEFAULT 0,
    UNIQUE(user_id, achievement_id)
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_games_user_status ON games(user_id, game_status);
CREATE INDEX IF NOT EXISTS idx_games_level_created ON games(level, created_at);
CREATE INDEX IF NOT EXISTS idx_game_attempts_game_id ON game_attempts(game_id);
CREATE INDEX IF NOT EXISTS idx_game_attempts_game_number ON game_attempts(game_id, attempt_number);
CREATE INDEX IF NOT EXISTS idx_words_length_category ON word_dictionary(length, category) WHERE is_active = TRUE;
CREATE INDEX IF NOT EXISTS idx_words_category_active ON word_dictionary(category, is_active);
CREATE INDEX IF NOT EXISTS idx_user_progress_user_level ON user_progress(user_id, level);
CREATE INDEX IF NOT EXISTS idx_user_progress_level_wins ON user_progress(level, games_won);
CREATE INDEX IF NOT EXISTS idx_user_stats_user ON user_statistics(user_id);
CREATE INDEX IF NOT EXISTS idx_user_achievements_user ON user_achievements(user_id);

-- Create function to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_games_updated_at BEFORE UPDATE ON games
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_progress_updated_at BEFORE UPDATE ON user_progress
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_statistics_updated_at BEFORE UPDATE ON user_statistics
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert initial word dictionary data
-- Common 4-8 letter words suitable for the game
INSERT INTO word_dictionary (word, length, category, difficulty_score) VALUES
-- 4-letter words
    ('WORD', 4, 'common', 1),
    ('GAME', 4, 'common', 1),
    ('PLAY', 4, 'common', 1),
    ('CODE', 4, 'common', 1),
    ('KEYS', 4, 'common', 1),
    ('LOCK', 4, 'common', 1),
    ('CARD', 4, 'common', 1),
    ('CHIP', 4, 'common', 1),
    ('DATA', 4, 'common', 1),
    ('FILE', 4, 'common', 1),
    ('LINK', 4, 'common', 1),
    ('MAIL', 4, 'common', 1),
    ('NODE', 4, 'common', 1),
    ('PAGE', 4, 'common', 1),
    ('PING', 4, 'common', 1),
    ('PORT', 4, 'common', 1),
    ('SEND', 4, 'common', 1),
    ('SYNC', 4, 'common', 1),
    ('TASK', 4, 'common', 1),
    ('USER', 4, 'common', 1),

-- 5-letter words
    ('CYPHER', 6, 'crypto', 1),
    ('SECRET', 6, 'crypto', 1),
    ('CODING', 6, 'tech', 1),
    ('BINARY', 6, 'tech', 1),
    ('BYTES', 5, 'tech', 1),
    ('CLOUD', 5, 'tech', 1),
    ('DEBUG', 5, 'tech', 1),
    ('EMAIL', 5, 'tech', 1),
    ('ERROR', 5, 'tech', 1),
    ('FLASH', 5, 'tech', 1),
    ('FORKS', 5, 'tech', 1),
    ('FRAME', 5, 'tech', 1),
    ('GHOST', 5, 'tech', 1),
    ('GUARD', 5, 'crypto', 1),
    ('HASHS', 5, 'crypto', 1),
    ('HELLO', 5, 'common', 1),
    ('HOUSE', 5, 'common', 1),
    ('INPUT', 5, 'tech', 1),
    ('IPV4', 4, 'tech', 1),
    ('IPV6', 4, 'tech', 1),
    ('LOGIC', 5, 'tech', 1),
    ('LOGIN', 5, 'tech', 1),
    ('LOGS', 4, 'tech', 1),
    ('LOOPS', 5, 'tech', 1),
    ('MERGE', 5, 'tech', 1),
    ('MOUSE', 5, 'tech', 1),
    ('NETS', 4, 'tech', 1),
    ('NODES', 5, 'tech', 1),
    ('PANEL', 5, 'tech', 1),
    ('PARKS', 5, 'common', 1),
    ('PATCH', 5, 'tech', 1),
    ('PHONE', 5, 'tech', 1),
    ('PHOTO', 5, 'tech', 1),
    ('PIXEL', 5, 'tech', 1),
    ('PLANS', 5, 'common', 1),
    ('PLUGIN', 6, 'tech', 1),
    ('PRINT', 5, 'tech', 1),
    ('PROXY', 5, 'tech', 1),
    ('QUERY', 5, 'tech', 1),
    ('QUEUE', 5, 'tech', 1),
    ('QUICK', 5, 'common', 1),
    ('RANGE', 5, 'tech', 1),
    ('RESET', 5, 'tech', 1),
    ('RETRY', 5, 'tech', 1),
    ('ROBOT', 5, 'tech', 1),
    ('ROCKS', 5, 'common', 1),
    ('ROUTE', 5, 'tech', 1),
    ('SCALE', 5, 'tech', 1),
    ('SCREEN', 6, 'tech', 1),
    ('SCRIPT', 6, 'tech', 1),
    ('SCROLL', 6, 'tech', 1),
    ('SEARCH', 6, 'tech', 1),
    ('SEEDS', 5, 'crypto', 1),
    ('SHELL', 5, 'tech', 1),
    ('SHIPS', 5, 'common', 1),
    ('SHORT', 5, 'common', 1),
    ('SIGHT', 5, 'common', 1),
    ('SIGNAL', 6, 'tech', 1),
    ('SKETCH', 6, 'tech', 1),
    ('SLICES', 6, 'tech', 1),
    ('SLOTS', 5, 'tech', 1),
    ('SMALL', 5, 'common', 1),
    ('SNAIL', 5, 'common', 1),
    ('SOCIAL', 6, 'tech', 1),
    ('SOUND', 5, 'tech', 1),
    ('SPACE', 5, 'tech', 1),
    ('SPAN', 4, 'common', 1),
    ('SPEED', 5, 'tech', 1),
    ('SPLIT', 5, 'tech', 1),
    ('SPONS', 5, 'common', 1),
    ('STAMP', 5, 'common', 1),
    ('STATE', 5, 'tech', 1),
    ('STEPS', 5, 'common', 1),
    ('STORE', 5, 'tech', 1),
    ('STORM', 5, 'common', 1),
    ('STRIP', 5, 'tech', 1),
    ('STUDY', 5, 'common', 1),
    ('STYLE', 5, 'tech', 1),
    ('SUGAR', 5, 'common', 1),
    ('SWAPS', 5, 'tech', 1),
    ('SWIFT', 5, 'tech', 1),
    ('SWITCH', 6, 'tech', 1),
    ('SYNTAX', 6, 'tech', 1),
    ('TABLE', 5, 'tech', 1),
    ('TAPES', 5, 'tech', 1),
    ('TAXIS', 5, 'common', 1),
    ('TEAMS', 5, 'common', 1),
    ('TECHS', 5, 'tech', 1),
    ('TERMS', 5, 'common', 1),
    ('TESTS', 5, 'tech', 1),
    ('TEXTS', 5, 'tech', 1),
    ('THEME', 5, 'tech', 1),
    ('TILES', 5, 'tech', 1),
    ('TIMER', 5, 'tech', 1),
    ('TITLE', 5, 'common', 1),
    ('TODAY', 5, 'common', 1),
    ('TOOLS', 5, 'tech', 1),
    ('TOWER', 5, 'common', 1),
    ('TRACK', 5, 'tech', 1),
    ('TRADE', 5, 'common', 1),
    ('TRAIN', 5, 'common', 1),
    ('TRASH', 5, 'tech', 1),
    ('TREES', 5, 'common', 1),
    ('TRIAL', 5, 'common', 1),
    ('TRIES', 5, 'common', 1),
    ('TROOP', 5, 'common', 1),
    ('TRUCK', 5, 'common', 1),
    ('TRUST', 5, 'crypto', 1),
    ('TUTOR', 5, 'common', 1),
    ('TWEET', 5, 'tech', 1),
    ('TWICE', 5, 'common', 1),
    ('TYPES', 5, 'tech', 1),
    ('UNDER', 5, 'common', 1),
    ('UNIFY', 5, 'tech', 1),
    ('UNITS', 5, 'tech', 1),
    ('UPPER', 5, 'common', 1),
    ('USAGE', 5, 'tech', 1),
    ('USERS', 5, 'tech', 1),
    ('VALID', 5, 'tech', 1),
    ('VALUE', 5, 'common', 1),
    ('VIDEO', 5, 'tech', 1),
    ('VIEWS', 5, 'tech', 1),
    ('VIRUS', 5, 'tech', 1),
    ('VISIT', 5, 'common', 1),
    ('VOICE', 5, 'tech', 1),
    ('WASTE', 5, 'common', 1),
    ('WATCH', 5, 'common', 1),
    ('WAVES', 5, 'common', 1),
    ('WEAVE', 5, 'common', 1),
    ('WHEEL', 5, 'common', 1),
    ('WHERE', 5, 'common', 1),
    ('WHILE', 5, 'common', 1),
    ('WHITE', 5, 'common', 1),
    ('WHOLE', 5, 'common', 1),
    ('WHOSE', 5, 'common', 1),
    ('WIDTH', 5, 'tech', 1),
    ('WINDOW', 6, 'tech', 1),
    ('WIPES', 5, 'common', 1),
    ('WIRE', 4, 'tech', 1),
    ('WOKEN', 5, 'common', 1),
    ('WOMAN', 5, 'common', 1),
    ('WOMEN', 5, 'common', 1),
    ('WORLD', 5, 'common', 1),
    ('WORRY', 5, 'common', 1),
    ('WORSE', 5, 'common', 1),
    ('WORST', 5, 'common', 1),
    ('WORTH', 5, 'common', 1),
    ('WOULD', 5, 'common', 1),
    ('WOUND', 5, 'common', 1),
    ('WRITE', 5, 'common', 1),
    ('WRONG', 5, 'common', 1),
    ('WROTE', 5, 'common', 1),
    ('YIELD', 5, 'tech', 1),
    ('YOUNG', 5, 'common', 1),
    ('YOURS', 5, 'common', 1),
    ('YOUTH', 5, 'common', 1),
    ('ZONES', 5, 'tech', 1),

-- 6-letter words
    ('BINARY', 6, 'tech', 2),
    ('CIPHER', 6, 'crypto', 2),
    ('CODING', 6, 'tech', 2),
    ('DECODE', 6, 'crypto', 2),
    ('ENCRYPT', 7, 'crypto', 3),
    ('HASHES', 6, 'crypto', 2),
    ('LOCKED', 6, 'crypto', 2),
    ('PUZZLE', 6, 'common', 2),
    ('SECRET', 6, 'crypto', 2),
    ('SECURE', 6, 'crypto', 2),
    ('SYSTEM', 6, 'tech', 2),
    ('TOKENS', 6, 'crypto', 2),
    ('UNLOCK', 6, 'crypto', 2),
    ('VALUES', 6, 'tech', 2),

-- 7-letter words
    ('CIPHERS', 7, 'crypto', 3),
    ('DECODED', 7, 'crypto', 3),
    ('ENCRYPT', 7, 'crypto', 3),
    ('KEYCARD', 7, 'crypto', 3),
    ('NETWORK', 7, 'tech', 3),
    ('PASSWORD', 8, 'crypto', 4),
    ('PRIVACY', 7, 'crypto', 3),
    ('PROGRAM', 7, 'tech', 3),
    ('SECURITY', 8, 'crypto', 4),
    ('VIRTUAL', 7, 'tech', 3),

-- 8-letter words
    ('ALGORITHM', 9, 'tech', 4),
    ('BACKUP', 6, 'tech', 2),
    ('COMPUTER', 8, 'tech', 4),
    ('DATABASE', 8, 'tech', 4),
    ('ENCRYPTION', 10, 'crypto', 5),
    ('FIREWALL', 8, 'crypto', 4),
    ('SOFTWARE', 8, 'tech', 4),
    ('TECHNOLOGY', 10, 'tech', 5),

-- Longer words (9-10 letters) for advanced levels
    ('AUTHENTICATE', 11, 'crypto', 6),
    ('CRYPTOCURRENCY', 14, 'crypto', 8),
    ('JULIUS', 6, 'history', 2),
    ('CAESAR', 6, 'history', 2),
    ('PLAYFAIR', 8, 'crypto', 4),
    ('VIGENERE', 8, 'crypto', 4);

-- Insert default achievements
INSERT INTO achievements (name, description, icon, category, requirement_type, requirement_value, points) VALUES
    ('First Win', 'Win your first game at any level', '🏆', 'general', 'wins', 1, 10),
    ('Caesar Master', 'Complete Level 1 (Caesar Cipher)', '👑', 'levels', 'level_complete', 1, 25),
    ('Substitution Expert', 'Complete Level 2 (Monoalphabetic Substitution)', '🎓', 'levels', 'level_complete', 2, 30),
    ('Playfair Pioneer', 'Complete Level 3 (Playfair Cipher)', '🗝️', 'levels', 'level_complete', 3, 35),
    ('Hill Climber', 'Complete Level 4 (Hill Cipher)', '⛰️', 'levels', 'level_complete', 4, 40),
    ('Rail Rider', 'Complete Level 5 (Rail Fence)', '🚂', 'levels', 'level_complete', 5, 45),
    ('Vigenère Victor', 'Complete Level 6 (Vigenère Cipher)', '✌️', 'levels', 'level_complete', 6, 50),
    ('One-Time Wonder', 'Complete Level 7 (One-Time Pad)', '🔐', 'levels', 'level_complete', 7, 55),
    ('DES Defender', 'Complete Level 8 (DES/3DES)', '🛡️', 'levels', 'level_complete', 8, 60),
    ('RSA Champion', 'Complete Level 9 (RSA)', '🏅', 'levels', 'level_complete', 9, 100),
    ('Perfect Game', 'Win a game with only 1 attempt', '⚡', 'performance', 'perfect_game', 1, 50),
    ('Speed Demon', 'Win a game in under 2 minutes', '⚡', 'performance', 'speed_run', 1, 40),
    ('No Hints Needed', 'Win a game without using any hints', '🧠', 'performance', 'no_hints', 1, 30),
    ('Winning Streak', 'Win 3 games in a row', '🔥', 'streak', 'streak', 3, 75),
    ('Cipher Expert', 'Complete all 9 levels', '🎖️', 'mastery', 'all_levels', 9, 200),
    ('Dedicated Player', 'Play 50 games total', '📊', 'volume', 'games_played', 50, 100),
    ('Consistent Winner', 'Achieve 80% win rate over 20 games', '📈', 'performance', 'high_win_rate', 20, 150);

-- Create a default guest user for anonymous play
INSERT INTO users (username, display_name, is_guest) VALUES
('guest', 'Guest Player', TRUE)
ON CONFLICT (username) DO NOTHING;

-- Print completion message
DO $$
BEGIN
    RAISE NOTICE 'KeyCrypt database initialized successfully!';
    RAISE NOTICE 'Added % words to dictionary', (SELECT COUNT(*) FROM word_dictionary);
    RAISE NOTICE 'Added % achievements', (SELECT COUNT(*) FROM achievements);
END $$;