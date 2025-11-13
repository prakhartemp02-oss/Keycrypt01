/** Letter tile component for the game board */

import { motion } from 'framer-motion';
import { tileFlip, shakeAnimation } from '../../lib/animations';
import type { LetterFeedback } from '../../types/game';

interface LetterTileProps {
  letter: string;
  status?: 'correct' | 'present' | 'absent' | 'empty';
  index: number;
  isRevealing?: boolean;
  isShaking?: boolean;
  delay?: number;
}

export const LetterTile: React.FC<LetterTileProps> = ({
  letter,
  status = 'empty',
  index,
  isRevealing = false,
  isShaking = false,
  delay = 0,
}) => {
  const getTileColor = () => {
    switch (status) {
      case 'correct':
        return 'bg-green-500 border-green-600 text-white';
      case 'present':
        return 'bg-yellow-500 border-yellow-600 text-white';
      case 'absent':
        return 'bg-gray-500 border-gray-600 text-white';
      default:
        return 'bg-white border-gray-300 text-gray-900';
    }
  };

  const getAnimationVariants = () => {
    if (isShaking) {
      return shakeAnimation;
    }
    if (isRevealing) {
      return {
        initial: { rotateX: 0, scale: 1 },
        animate: {
          rotateX: 360,
          scale: [1, 1.1, 1],
          transition: {
            delay,
            duration: 0.6,
            ease: 'easeInOut',
            times: [0, 0.5, 1],
          },
        },
      };
    }
    return {};
  };

  const variants = getAnimationVariants();

  return (
    <motion.div
      key={`${letter}-${index}`}
      className={`
        relative inline-flex items-center justify-center
        w-14 h-14 md:w-16 md:h-16
        border-2 rounded-md font-bold text-xl md:text-2xl
        transition-all duration-200
        ${getTileColor()}
      `}
      variants={variants}
      initial={variants.initial}
      animate={variants.animate}
      style={{
        transformStyle: 'preserve-3d',
        backfaceVisibility: 'hidden',
      }}
      role="gridcell"
      aria-label={`Position ${index + 1}: ${letter || 'empty'}`}
      aria-selected={letter.length > 0}
    >
      {letter && (
        <motion.span
          className="select-none"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: delay + 0.2 }}
        >
          {letter}
        </motion.span>
      )}
    </motion.div>
  );
};

export default LetterTile;