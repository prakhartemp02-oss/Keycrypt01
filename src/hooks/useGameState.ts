/** Custom hook for managing game state in KeyCrypt */

import { useState, useCallback, useEffect } from 'react';
import type { GameState, GuessResult, LetterFeedback, Hint, KeyboardState } from '../types/game';
import { GAME_CONSTANTS } from '../types/game';

interface UseGameStateOptions {
  maxAttempts?: number;
  onGameEnd?: (status: 'won' | 'lost') => void;
  onHintUnlock?: (hints: string[]) => void;
}

export const useGameState = (initialGame: Partial<GameState> = {}, options: UseGameStateOptions = {}) => {
  const [gameState, setGameState] = useState<GameState>(() => ({
    game_id: initialGame.game_id || '',
    level: initialGame.level || 1,
    attempts_remaining: initialGame.attempts_remaining || GAME_CONSTANTS.MAX_ATTEMPTS,
    attempts_allowed: initialGame.attempts_allowed || GAME_CONSTANTS.MAX_ATTEMPTS,
    current_guess: '',
    submitted_guesses: initialGame.submitted_guesses || [],
    unlocked_hints: initialGame.unlocked_hints || [],
    game_status: initialGame.game_status || 'ongoing',
    cipher_info: initialGame.cipher_info || { name: 'Unknown', level: 1 },
    encrypted_meta: initialGame.encrypted_meta || {
      cipher: 'unknown',
      ciphertext: '',
      hint_ciphertexts: {},
      encryption_metadata: {},
    },
    hint_unlock_rules: initialGame.hint_unlock_rules || {
      first_hint: GAME_CONSTANTS.HINT_UNLOCK_THRESHOLDS.LENGTH,
      second_hint: GAME_CONSTANTS.HINT_UNLOCK_THRESHOLDS.FIRST_LETTER,
    },
    ...initialGame,
  }));

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Derived state
  const currentAttempt = gameState.submitted_guesses.length + 1;
  const isGameOver = gameState.game_status !== 'ongoing';
  const canSubmit = gameState.current_guess.length > 0 && !isSubmitting && !isGameOver;

  // Keyboard state derived from submitted guesses
  const keyboardState: KeyboardState = useCallback(() => {
    const state: KeyboardState = {};

    gameState.submitted_guesses.forEach(guess => {
      guess.feedback.forEach((feedback, index) => {
        const letter = guess.guess[index].toUpperCase();
        const currentStatus = state[letter];

        // Update with highest priority status
        if (
          feedback.status === 'correct' ||
          (feedback.status === 'present' && currentStatus !== 'correct') ||
          (feedback.status === 'absent' && !currentStatus)
        ) {
          state[letter] = feedback.status;
        }
      });
    });

    return state;
  }, [gameState.submitted_guesses])();

  // Handle letter input
  const handleLetterInput = useCallback((letter: string) => {
    if (isGameOver || isSubmitting) return;

    setGameState(prev => {
      const maxLength = Math.min(10, prev.current_guess.length + 1);
      if (prev.current_guess.length >= maxLength) return prev;

      return {
        ...prev,
        current_guess: prev.current_guess + letter.toUpperCase(),
      };
    });

    // Clear any previous errors
    setError(null);
  }, [isGameOver, isSubmitting]);

  // Handle backspace
  const handleBackspace = useCallback(() => {
    if (isGameOver || isSubmitting) return;

    setGameState(prev => ({
      ...prev,
      current_guess: prev.current_guess.slice(0, -1),
    }));

    setError(null);
  }, [isGameOver, isSubmitting]);

  // Handle word submission
  const handleSubmit = useCallback(async () => {
    if (!canSubmit || isSubmitting) return;

    setIsSubmitting(true);
    setError(null);

    try {
      // This will be handled by the parent component with API call
      // Return the current guess for external processing
      return gameState.current_guess.toUpperCase();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to submit guess');
      setIsSubmitting(false);
      return null;
    }
  }, [canSubmit, isSubmitting, gameState.current_guess]);

  // Process guess result (called after API response)
  const processGuessResult = useCallback((
    guess: string,
    feedback: LetterFeedback[],
    attempts_remaining: number,
    unlocked_hints: string[],
    game_status: string
  ) => {
    const newGuess: GuessResult = {
      guess: guess.toUpperCase(),
      feedback,
      attempt_number: currentAttempt,
      created_at: new Date().toISOString(),
    };

    const hintsToUnlock: string[] = [];

    // Check hint unlock rules
    const attemptsUsed = gameState.attempts_allowed - attempts_remaining;
    if (attemptsUsed >= gameState.hint_unlock_rules.first_hint) {
      hintsToUnlock.push('length');
    }
    if (attemptsUsed >= gameState.hint_unlock_rules.second_hint) {
      hintsToUnlock.push('first_letter');
    }
    if (gameState.level >= 4 && attemptsUsed >= GAME_CONSTANTS.HINT_UNLOCK_THRESHOLDS.PATTERN) {
      hintsToUnlock.push('pattern');
    }

    setGameState(prev => ({
      ...prev,
      submitted_guesses: [...prev.submitted_guesses, newGuess],
      attempts_remaining,
      game_status: game_status as 'ongoing' | 'won' | 'lost',
      current_guess: '',
    }));

    // Handle hint unlock callback
    if (hintsToUnlock.length > 0) {
      options.onHintUnlock?.(hintsToUnlock);
    }

    // Handle game end callback
    if (game_status !== 'ongoing') {
      options.onGameEnd?.(game_status as 'won' | 'lost');
    }

    setIsSubmitting(false);
  }, [currentAttempt, gameState, options]);

  // Reset game state
  const resetGame = useCallback((newGame: Partial<GameState>) => {
    setGameState({
      game_id: newGame.game_id || '',
      level: newGame.level || 1,
      attempts_remaining: newGame.attempts_remaining || GAME_CONSTANTS.MAX_ATTEMPTS,
      attempts_allowed: newGame.attempts_allowed || GAME_CONSTANTS.MAX_ATTEMPTS,
      current_guess: '',
      submitted_guesses: [],
      unlocked_hints: newGame.unlocked_hints || [],
      game_status: 'ongoing',
      cipher_info: newGame.cipher_info || { name: 'Unknown', level: 1 },
      encrypted_meta: newGame.encrypted_meta || {
        cipher: 'unknown',
        ciphertext: '',
        hint_ciphertexts: {},
        encryption_metadata: {},
      },
      hint_unlock_rules: newGame.hint_unlock_rules || {
        first_hint: GAME_CONSTANTS.HINT_UNLOCK_THRESHOLDS.LENGTH,
        second_hint: GAME_CONSTANTS.HINT_UNLOCK_THRESHOLDS.FIRST_LETTER,
      },
      ...newGame,
    });

    setError(null);
    setIsSubmitting(false);
  }, []);

  // Update unlocked hints
  const updateUnlockedHints = useCallback((hints: Hint[]) => {
    setGameState(prev => ({
      ...prev,
      unlocked_hints: hints,
    }));
  }, []);

  // Clear error
  const clearError = useCallback(() => {
    setError(null);
  }, []);

  // Validate current guess
  const validateGuess = useCallback(() => {
    const guess = gameState.current_guess.toUpperCase();

    if (guess.length < 4) {
      setError('Word must be at least 4 letters long');
      return false;
    }

    if (guess.length > 10) {
      setError('Word must be no more than 10 letters long');
      return false;
    }

    if (!/^[A-Z]+$/.test(guess)) {
      setError('Word must contain only letters');
      return false;
    }

    return true;
  }, [gameState.current_guess]);

  // Get guess grid for current attempt
  const getCurrentGuessRow = useCallback(() => {
    const row = Array(GAME_CONSTANTS.MAX_ATTEMPTS).fill('');
    for (let i = 0; i < gameState.current_guess.length; i++) {
      row[i] = gameState.current_guess[i].toUpperCase();
    }
    return row;
  }, [gameState.current_guess]);

  // Check if a specific hint is unlocked
  const isHintUnlocked = useCallback((hintType: string) => {
    const attemptsUsed = gameState.attempts_allowed - gameState.attempts_remaining;

    switch (hintType) {
      case 'length':
        return attemptsUsed >= gameState.hint_unlock_rules.first_hint;
      case 'first_letter':
        return attemptsUsed >= gameState.hint_unlock_rules.second_hint;
      case 'pattern':
        return gameState.level >= 4 && attemptsUsed >= GAME_CONSTANTS.HINT_UNLOCK_THRESHOLDS.PATTERN;
      case 'educational':
        return true; // Educational hints are always available
      default:
        return false;
    }
  }, [gameState]);

  // Get formatted time remaining (for future time-based features)
  const getTimeRemaining = useCallback(() => {
    // Placeholder for future time-based game features
    return null;
  }, []);

  // Effects
  useEffect(() => {
    // Validate guess when it changes
    if (gameState.current_guess.length > 0) {
      validateGuess();
    }
  }, [gameState.current_guess, validateGuess]);

  // Clear error when game state changes significantly
  useEffect(() => {
    if (error && !isSubmitting) {
      const timer = setTimeout(clearError, 3000);
      return () => clearTimeout(timer);
    }
  }, [error, isSubmitting, clearError]);

  return {
    // Core state
    gameState,
    setGameState,

    // Derived state
    currentAttempt,
    isGameOver,
    canSubmit,
    keyboardState,

    // Actions
    handleLetterInput,
    handleBackspace,
    handleSubmit,
    processGuessResult,
    resetGame,
    updateUnlockedHints,
    clearError,

    // Utilities
    validateGuess,
    getCurrentGuessRow,
    isHintUnlocked,
    getTimeRemaining,

    // State
    isSubmitting,
    error,
  };
};

export default useGameState;