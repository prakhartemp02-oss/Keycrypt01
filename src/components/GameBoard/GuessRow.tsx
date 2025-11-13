/** Guess row component for the game board */

import { motion } from 'framer-motion';
import { LetterTile } from './LetterTile';
import { staggerContainer } from '../../lib/animations';
import type { GuessResult } from '../../types/game';

interface GuessRowProps {
  guess: string;
  feedback?: ('correct' | 'present' | 'absent')[];
  isSubmitted?: boolean;
  isCurrent?: boolean;
  attemptNumber: number;
  isRevealing?: boolean;
  isShaking?: boolean;
}

export const GuessRow: React.FC<GuessRowProps> = ({
  guess,
  feedback,
  isSubmitted = false,
  isCurrent = false,
  attemptNumber,
  isRevealing = false,
  isShaking = false,
}) => {
  // Create an array of letters with empty spaces for remaining tiles
  const letters = guess.split('');
  while (letters.length < 5) {
    letters.push('');
  }

  // Determine status for each tile
  const getTileStatus = (index: number) => {
    if (!isSubmitted || !feedback) {
      return letters[index] ? 'empty' : 'empty';
    }
    return feedback[index] || 'absent';
  };

  return (
    <motion.div
      className="flex justify-center gap-1 md:gap-2 mb-2"
      role="row"
      aria-label={`Guess ${attemptNumber}: ${guess || 'empty'}`}
      variants={staggerContainer}
      initial="initial"
      animate="animate"
    >
      {letters.map((letter, index) => (
        <LetterTile
          key={`${attemptNumber}-${index}`}
          letter={letter}
          status={getTileStatus(index)}
          index={index}
          isRevealing={isRevealing && isSubmitted}
          isShaking={isShaking && isCurrent}
          delay={index * 0.1}
        />
      ))}
    </motion.div>
  );
};

export default GuessRow;