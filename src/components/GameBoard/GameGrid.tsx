/** Game grid component displaying all guess attempts */

import { motion } from 'framer-motion';
import { GuessRow } from './GuessRow';
import { staggerContainer } from '../../lib/animations';
import type { GameState } from '../../types/game';
import { GAME_CONSTANTS } from '../../types/game';

interface GameGridProps {
  gameState: GameState;
  isRevealing?: boolean;
  isShaking?: boolean;
}

export const GameGrid: React.FC<GameGridProps> = ({
  gameState,
  isRevealing = false,
  isShaking = false,
}) => {
  const { submitted_guesses, current_guess, attempts_allowed } = gameState;
  const currentAttempt = submitted_guesses.length;

  // Create all rows (submitted guesses + current guess + empty rows)
  const rows = [];

  // Add submitted guesses
  submitted_guesses.forEach((guess, index) => {
    rows.push({
      key: `submitted-${index}`,
      guess: guess.guess,
      feedback: guess.feedback.map(f => f.status),
      isSubmitted: true,
      isCurrent: false,
      attemptNumber: index + 1,
      isRevealing: false, // Already revealed
      isShaking: false,
    });
  });

  // Add current guess row if game is ongoing
  if (gameState.game_status === 'ongoing' && currentAttempt < attempts_allowed) {
    rows.push({
      key: 'current',
      guess: current_guess,
      feedback: undefined,
      isSubmitted: false,
      isCurrent: true,
      attemptNumber: currentAttempt + 1,
      isRevealing: false,
      isShaking: isShaking,
    });
  }

  // Fill remaining rows with empty guesses
  const remainingRows = attempts_allowed - rows.length;
  for (let i = 0; i < remainingRows; i++) {
    rows.push({
      key: `empty-${i}`,
      guess: '',
      feedback: undefined,
      isSubmitted: false,
      isCurrent: false,
      attemptNumber: currentAttempt + 2 + i,
      isRevealing: false,
      isShaking: false,
    });
  }

  return (
    <motion.div
      className="flex flex-col items-center justify-center p-4"
      variants={staggerContainer}
      initial="initial"
      animate="animate"
    >
      <div className="bg-gray-100 dark:bg-gray-800 rounded-lg p-4 shadow-lg">
        {rows.map((row) => (
          <GuessRow
            key={row.key}
            guess={row.guess}
            feedback={row.feedback}
            isSubmitted={row.isSubmitted}
            isCurrent={row.isCurrent}
            attemptNumber={row.attemptNumber}
            isRevealing={row.isRevealing}
            isShaking={row.isShaking}
          />
        ))}
      </div>
    </motion.div>
  );
};

export default GameGrid;