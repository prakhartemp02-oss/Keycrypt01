/** Game-related TypeScript interfaces for KeyCrypt */

export interface GameState {
  game_id: string;
  level: number;
  attempts_remaining: number;
  attempts_allowed: number;
  current_guess: string;
  submitted_guesses: GuessResult[];
  unlocked_hints: Hint[];
  game_status: 'ongoing' | 'won' | 'lost' | 'abandoned';
  cipher_info: CipherInfo;
  encrypted_meta: EncryptedMeta;
  hint_unlock_rules: HintUnlockRules;
  created_at?: string;
}

export interface GuessResult {
  attempt_id?: string;
  game_id?: string;
  guess: string;
  feedback: LetterFeedback[];
  attempt_number: number;
  created_at?: string;
}

export interface LetterFeedback {
  letter: string;
  status: 'correct' | 'present' | 'absent';
}

export interface Hint {
  type: 'length' | 'first_letter' | 'pattern' | 'educational';
  content: string | number;
  unlocked_at_attempt?: number;
}

export interface CipherInfo {
  name: string;
  level: number;
  description?: string;
  historical_context?: string;
  weakness_explanation?: string;
  modern_relevance?: string;
}

export interface EncryptedMeta {
  cipher: string;
  ciphertext: string;
  hint_ciphertexts: {
    length?: string;
    first_letter?: string;
    pattern?: string;
    educational?: string;
  };
  encryption_metadata: {
    [key: string]: any;
  };
}

export interface HintUnlockRules {
  first_hint: number;
  second_hint: number;
}

export interface NewGameRequest {
  level: number;
  dictionary_category?: string;
  user_id?: string;
}

export interface NewGameResponse {
  game_id: string;
  level: number;
  attempts_allowed: number;
  attempts_remaining: number;
  encrypted_meta: EncryptedMeta;
  hint_unlock_rules: HintUnlockRules;
  cipher_info: CipherInfo;
  game_status: string;
  created_at?: string;
}

export interface GuessRequest {
  game_id: string;
  guess: string;
}

export interface GuessResponse {
  game_id: string;
  feedback: LetterFeedback[];
  attempts_remaining: number;
  unlocked_hints: string[] | Hint[];
  game_status: string;
}

export interface HintsResponse {
  game_id: string;
  unlocked: {
    [key: string]: string | number;
  };
}

export interface GameStatusResponse {
  game_id: string;
  level: number;
  attempts_allowed: number;
  attempts_remaining: number;
  encrypted_meta: EncryptedMeta;
  hint_unlock_rules: HintUnlockRules;
  cipher_info?: CipherInfo;
  game_status: string;
  attempts: GuessResult[];
}

// Level information for UI
export interface LevelInfo {
  level: number;
  name: string;
  description: string;
  historical_context: string;
  difficulty: 'Easy' | 'Medium' | 'Hard' | 'Expert';
  unlocked: boolean;
  completed: boolean;
  best_score?: number;
  games_played?: number;
  games_won?: number;
}

// User progress
export interface UserProgress {
  user_id: string;
  level: number;
  games_won: number;
  games_played: number;
  win_rate: number;
  best_score?: number;
  total_time_seconds: number;
  average_hints_used: number;
  last_played?: string;
}

// Keyboard state
export interface KeyboardState {
  [key: string]: 'correct' | 'present' | 'absent' | 'unused';
}

// Animation states
export interface AnimationState {
  isFlipping: boolean;
  isShaking: boolean;
  isBouncing: boolean;
}

// Error handling
export interface GameError {
  code: string;
  message: string;
  details?: any;
}

// API response wrapper
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: GameError;
}

// Virtual keyboard layout
export interface KeyboardLayout {
  rows: string[][];
}

// Game settings
export interface GameSettings {
  enableSoundEffects: boolean;
  enableAnimations: boolean;
  darkMode: boolean;
  showEducationalHints: boolean;
  hardMode: boolean;
}

// Leaderboard entry
export interface LeaderboardEntry {
  rank: number;
  user_id: string;
  display_name: string;
  level: number;
  games_won: number;
  best_score?: number;
  win_rate: number;
}

// Tutorial step
export interface TutorialStep {
  id: string;
  title: string;
  content: string;
  highlight?: string[];
  next_step?: string;
}

// Achievement
export interface Achievement {
  id: string;
  name: string;
  description: string;
  icon: string;
  unlocked_at?: string;
  progress?: number;
  max_progress?: number;
}

// Statistics
export interface UserStatistics {
  user_id: string;
  total_games_played: number;
  total_games_won: number;
  overall_win_rate: number;
  levels_completed: number;
  levels_unlocked: number;
  best_overall_score?: number;
  total_time_seconds: number;
  average_time_per_game: number;
  best_scores_by_level: { [level: number]: number };
}

// Game constants
export const GAME_CONSTANTS = {
  MAX_ATTEMPTS: 6,
  WORD_LENGTHS: {
    MIN: 4,
    MAX: 10
  },
  LEVELS: {
    MIN: 1,
    MAX: 9
  },
  ANIMATION_DURATIONS: {
    TILE_FLIP: 600,
    SHAKE: 500,
    BOUNCE: 300,
    HINT_REVEAL: 800
  },
  HINT_UNLOCK_THRESHOLDS: {
    LENGTH: 3,
    FIRST_LETTER: 5,
    PATTERN: 4
  }
} as const;