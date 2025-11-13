/** Hint panel component for displaying unlocked hints */

import { motion, AnimatePresence } from 'framer-motion';
import { hintReveal, scaleOnHover } from '../../lib/animations';
import type { Hint, GameState } from '../../types/game';
import { GAME_CONSTANTS } from '../../types/game';

interface HintPanelProps {
  gameState: GameState;
  unlockedHints: { [key: string]: string | number };
  isVisible?: boolean;
}

export const HintPanel: React.FC<HintPanelProps> = ({
  gameState,
  unlockedHints,
  isVisible = true,
}) => {
  // Check if a hint type is unlocked
  const isHintUnlocked = (hintType: string): boolean => {
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
        return hintType in unlockedHints;
    }
  };

  // Get hint display information
  const getHintInfo = (type: string) => {
    switch (type) {
      case 'length':
        return {
          title: 'Word Length',
          icon: '📏',
          description: `The secret word has ${unlockedHints.length || '?'} letters`,
          unlockThreshold: gameState.hint_unlock_rules.first_hint,
        };
      case 'first_letter':
        return {
          title: 'First Letter',
          icon: '🔤',
          description: `The secret word starts with '${unlockedHints.first_letter || '?'}'`,
          unlockThreshold: gameState.hint_unlock_rules.second_hint,
        };
      case 'pattern':
        return {
          title: 'Letter Pattern',
          icon: '🔍',
          description: unlockedHints.pattern || 'Pattern analysis unavailable',
          unlockThreshold: GAME_CONSTANTS.HINT_UNLOCK_THRESHOLDS.PATTERN,
        };
      case 'educational':
        return {
          title: 'Cipher Information',
          icon: '📚',
          description: gameState.cipher_info.weakness_explanation || 'No information available',
          unlockThreshold: 0,
        };
      default:
        return {
          title: 'Unknown Hint',
          icon: '❓',
          description: 'Hint information not available',
          unlockThreshold: 0,
        };
    }
  };

  const attemptsUsed = gameState.attempts_allowed - gameState.attempts_remaining;
  const hintsToShow = ['length', 'first_letter', 'pattern', 'educational'].filter(isHintUnlocked);

  if (!isVisible || hintsToShow.length === 0) {
    return null;
  }

  return (
    <motion.div
      className="fixed top-4 right-4 w-80 max-w-sm bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 z-40"
      initial={{ x: 400, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      transition={{ type: 'spring', stiffness: 100 }}
    >
      <div className="p-4">
        {/* Header */}
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-lg font-semibold text-gray-800 dark:text-white flex items-center gap-2">
            <span>💡</span>
            Hints
          </h3>
          <button
            className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
            onClick={() => {} /* Could be passed as prop to close */}
            aria-label="Close hints"
          >
            ×
          </button>
        </div>

        {/* Hint progress */}
        <div className="mb-4">
          <div className="flex justify-between text-sm text-gray-600 dark:text-gray-300 mb-1">
            <span>Progress</span>
            <span>{attemptsUsed} attempts used</span>
          </div>
          <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
            <motion.div
              className="bg-blue-500 h-2 rounded-full"
              initial={{ width: 0 }}
              animate={{ width: `${(attemptsUsed / gameState.attempts_allowed) * 100}%` }}
              transition={{ duration: 0.5 }}
            />
          </div>
        </div>

        {/* Hints list */}
        <div className="space-y-3 max-h-96 overflow-y-auto">
          <AnimatePresence>
            {hintsToShow.map((hintType, index) => {
              const hintInfo = getHintInfo(hintType);
              const isAvailable = isHintUnlocked(hintType);

              return (
                <motion.div
                  key={hintType}
                  className={`
                    border rounded-lg p-3
                    ${isAvailable
                      ? 'bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-700'
                      : 'bg-gray-50 dark:bg-gray-700/20 border-gray-200 dark:border-gray-600'
                    }
                  `}
                  variants={hintReveal}
                  initial="initial"
                  animate="animate"
                  exit="exit"
                  transition={{ delay: index * 0.1 }}
                  whileHover={isAvailable ? "hover" : ""}
                >
                  <div className="flex items-start gap-3">
                    <span className="text-2xl" role="img" aria-label={hintInfo.title}>
                      {hintInfo.icon}
                    </span>
                    <div className="flex-1 min-w-0">
                      <h4 className="font-semibold text-gray-800 dark:text-white text-sm">
                        {hintInfo.title}
                      </h4>
                      {isAvailable ? (
                        <p className="text-gray-600 dark:text-gray-300 text-xs mt-1">
                          {hintInfo.description}
                        </p>
                      ) : (
                        <div className="text-xs mt-1">
                          <p className="text-gray-500 dark:text-gray-400">
                            Unlocks after {hintInfo.unlockThreshold} attempts
                          </p>
                          <div className="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-1 mt-1">
                            <div
                              className="bg-gray-400 dark:bg-gray-500 h-1 rounded-full transition-all duration-300"
                              style={{
                                width: `${Math.min(100, (attemptsUsed / hintInfo.unlockThreshold) * 100)}%`
                              }}
                            />
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                </motion.div>
              );
            })}
          </AnimatePresence>
        </div>

        {/* Educational note */}
        {gameState.level >= 4 && (
          <motion.div
            className="mt-4 p-3 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-700 rounded-lg"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
          >
            <p className="text-xs text-yellow-800 dark:text-yellow-200">
              💡 <strong>Tip:</strong> Study the cipher information to understand how the encryption works.
              This might reveal patterns in the ciphertext!
            </p>
          </motion.div>
        )}
      </div>
    </motion.div>
  );
};

export default HintPanel;