/** Virtual keyboard component for touch devices and visual feedback */

import { motion } from 'framer-motion';
import { keyPress, scaleOnHover } from '../../lib/animations';
import type { KeyboardState } from '../../types/game';

interface VirtualKeyboardProps {
  onKeyPress: (key: string) => void;
  keyboardState: KeyboardState;
  disabled?: boolean;
}

// QWERTY keyboard layout
const KEYBOARD_ROWS = [
  ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
  ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
  ['ENTER', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', 'BACK'],
];

const VirtualKeyboard: React.FC<VirtualKeyboardProps> = ({
  onKeyPress,
  keyboardState,
  disabled = false,
}) => {
  const getKeyColor = (key: string, state: string) => {
    if (disabled) return 'bg-gray-200 dark:bg-gray-700 text-gray-400';

    switch (state) {
      case 'correct':
        return 'bg-green-500 text-white border-green-600';
      case 'present':
        return 'bg-yellow-500 text-white border-yellow-600';
      case 'absent':
        return 'bg-gray-500 text-white border-gray-600';
      default:
        return 'bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-200 border-gray-300 dark:border-gray-600';
    }
  };

  const getKeySize = (key: string) => {
    if (key === 'ENTER' || key === 'BACK') {
      return 'px-3 md:px-4 text-xs md:text-sm min-w-[60px] md:min-w-[80px]';
    }
    return 'px-3 md:px-4 text-sm md:text-base min-w-[32px] md:min-w-[40px]';
  };

  const handleKeyClick = (key: string) => {
    if (!disabled) {
      onKeyPress(key);
    }
  };

  return (
    <motion.div
      className="fixed bottom-0 left-0 right-0 bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-700 p-2 md:p-4 lg:relative lg:bg-transparent lg:border-t-0"
      initial={{ y: 100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ type: 'spring', stiffness: 100 }}
    >
      <div className="max-w-lg mx-auto">
        {/* Mobile-only header */}
        <div className="lg:hidden text-center mb-2">
          <p className="text-xs text-gray-500 dark:text-gray-400">Virtual Keyboard</p>
        </div>

        {KEYBOARD_ROWS.map((row, rowIndex) => (
          <motion.div
            key={rowIndex}
            className="flex justify-center gap-1 md:gap-2 mb-1 md:mb-2"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: rowIndex * 0.1 }}
          >
            {row.map((key) => (
              <motion.button
                key={key}
                className={`
                  ${getKeySize(key)}
                  ${getKeyColor(key, keyboardState[key] || 'unused')}
                  h-10 md:h-12 border-2 rounded font-semibold
                  transition-all duration-200
                  focus:outline-none focus:ring-2 focus:ring-blue-500
                  disabled:cursor-not-allowed
                  select-none
                `}
                onClick={() => handleKeyClick(key)}
                variants={keyPress}
                whileTap="tap"
                whileHover={!disabled ? "hover" : ""}
                layout
                disabled={disabled}
                aria-label={key}
                role="button"
                tabIndex={0}
              >
                {key}
              </motion.button>
            ))}
          </motion.div>
        ))}

        {/* Keyboard instructions for accessibility */}
        <div className="sr-only">
          <p>Virtual keyboard for entering guesses. Press ENTER to submit your guess or BACK to delete the last letter.</p>
        </div>

        {/* Touch device indicator */}
        <motion.div
          className="text-center text-xs text-gray-500 dark:text-gray-400 mt-2 lg:hidden"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
        >
          <p>You can also use your device's physical keyboard</p>
        </motion.div>
      </div>
    </motion.div>
  );
};

export default VirtualKeyboard;