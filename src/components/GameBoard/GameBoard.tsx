/** Main game board component */

import { useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { GameGrid } from './GameGrid';
import { useGameState } from '../../hooks/useGameState';
import { fadeIn } from '../../lib/animations';
import type { GameState } from '../../types/game';

interface GameBoardProps {
  gameState: GameState;
  onGuessSubmit: (guess: string) => void;
  isSubmitting?: boolean;
  lastGuessResult?: {
    guess: string;
    feedback: ('correct' | 'present' | 'absent')[];
  };
}

export const GameBoard: React.FC<GameBoardProps> = ({
  gameState,
  onGuessSubmit,
  isSubmitting = false,
  lastGuessResult,
}) => {
  const boardRef = useRef<HTMLDivElement>(null);

  // Local state for animation control
  const [isRevealing, setIsRevealing] = useState(false);
  const [isShaking, setIsShaking] = useState(false);

  // Handle keyboard input
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (isSubmitting || gameState.game_status !== 'ongoing') return;

      const key = event.key.toUpperCase();

      // Handle letter input
      if (/^[A-Z]$/.test(key)) {
        event.preventDefault();
        // This would be handled by the gameState hook
        return;
      }

      // Handle backspace
      if (key === 'BACKSPACE') {
        event.preventDefault();
        // This would be handled by the gameState hook
        return;
      }

      // Handle enter
      if (key === 'ENTER') {
        event.preventDefault();
        // Submit current guess
        if (gameState.current_guess.length > 0) {
          onGuessSubmit(gameState.current_guess);
        }
        return;
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [gameState.current_guess, gameState.game_status, isSubmitting, onGuessSubmit]);

  // Handle guess result animation
  useEffect(() => {
    if (lastGuessResult) {
      setIsRevealing(true);
      setTimeout(() => setIsRevealing(false), 2000);
    }
  }, [lastGuessResult]);

  // Handle invalid word shake animation
  const triggerShake = () => {
    setIsShaking(true);
    setTimeout(() => setIsShaking(false), 600);
  };

  // Get game status message
  const getGameStatusMessage = () => {
    switch (gameState.game_status) {
      case 'won':
        return '🎉 Congratulations! You solved it!';
      case 'lost':
        return '😔 Game Over. Try again!';
      case 'ongoing':
        return gameState.attempts_remaining === 1
          ? 'Last attempt!'
          : `${gameState.attempts_remaining} attempts remaining`;
      default:
        return '';
    }
  };

  return (
    <motion.div
      ref={boardRef}
      className="flex flex-col items-center justify-center min-h-screen p-4"
      variants={fadeIn}
      initial="initial"
      animate="animate"
    >
      {/* Game Header */}
      <motion.div
        className="text-center mb-6"
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.2 }}
      >
        <h1 className="text-3xl md:text-4xl font-bold text-gray-800 dark:text-white mb-2">
          Level {gameState.level}: {gameState.cipher_info.name}
        </h1>
        <p className="text-gray-600 dark:text-gray-300 text-sm md:text-base">
          {gameState.cipher_info.description}
        </p>
      </motion.div>

      {/* Game Status */}
      {gameState.game_status !== 'ongoing' && (
        <motion.div
          className="text-center mb-4 p-4 bg-blue-100 dark:bg-blue-900 rounded-lg"
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ type: 'spring', stiffness: 200 }}
        >
          <p className="text-lg font-semibold text-blue-800 dark:text-blue-200">
            {getGameStatusMessage()}
          </p>
        </motion.div>
      )}

      {/* Attempts Counter */}
      <motion.div
        className="mb-6 text-center"
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.3 }}
      >
        <div className="flex items-center justify-center gap-2">
          <span className="text-gray-600 dark:text-gray-300">
            Attempts:
          </span>
          <div className="flex gap-1">
            {Array.from({ length: gameState.attempts_allowed }, (_, i) => (
              <div
                key={i}
                className={`w-3 h-3 rounded-full ${
                  i < gameState.submitted_guesses.length
                    ? 'bg-gray-400'
                    : 'bg-gray-200 dark:bg-gray-600'
                }`}
              />
            ))}
          </div>
          <span className="text-sm text-gray-500 dark:text-gray-400">
            {gameState.attempts_remaining}/{gameState.attempts_allowed}
          </span>
        </div>
      </motion.div>

      {/* Game Grid */}
      <GameGrid
        gameState={gameState}
        isRevealing={isRevealing}
        isShaking={isShaking}
      />

      {/* Loading Overlay */}
      {isSubmitting && (
        <motion.div
          className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
            <p className="text-gray-700 dark:text-gray-300">Checking your guess...</p>
          </div>
        </motion.div>
      )}

      {/* Keyboard Instructions */}
      <motion.div
        className="mt-8 text-center text-sm text-gray-500 dark:text-gray-400"
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.5 }}
      >
        <p>Type letters to guess • Press Enter to submit • Backspace to delete</p>
      </motion.div>
    </motion.div>
  );
};

export default GameBoard;