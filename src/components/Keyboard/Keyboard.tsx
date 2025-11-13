/** Keyboard management component combining virtual and physical keyboard input */

import { useEffect, useCallback } from 'react';
import { motion } from 'framer-motion';
import VirtualKeyboard from './VirtualKeyboard';
import { fadeIn } from '../../lib/animations';
import type { KeyboardState } from '../../types/game';

interface KeyboardProps {
  onKeyPress: (key: string) => void;
  keyboardState: KeyboardState;
  disabled?: boolean;
  showVirtualKeyboard?: boolean;
}

export const Keyboard: React.FC<KeyboardProps> = ({
  onKeyPress,
  keyboardState,
  disabled = false,
  showVirtualKeyboard = true,
}) => {
  // Handle physical keyboard input
  const handlePhysicalKeyDown = useCallback(
    (event: KeyboardEvent) => {
      if (disabled) return;

      const key = event.key.toUpperCase();

      // Handle letter keys
      if (/^[A-Z]$/.test(key)) {
        event.preventDefault();
        onKeyPress(key);
        return;
      }

      // Handle special keys
      switch (key) {
        case 'ENTER':
          event.preventDefault();
          onKeyPress('ENTER');
          break;
        case 'BACKSPACE':
          event.preventDefault();
          onKeyPress('BACK');
          break;
        case 'DELETE':
          event.preventDefault();
          onKeyPress('BACK');
          break;
      }
    },
    [onKeyPress, disabled]
  );

  // Set up physical keyboard event listeners
  useEffect(() => {
    window.addEventListener('keydown', handlePhysicalKeyDown);
    return () => {
      window.removeEventListener('keydown', handlePhysicalKeyDown);
    };
  }, [handlePhysicalKeyDown]);

  // Auto-show virtual keyboard on touch devices
  useEffect(() => {
    const isTouchDevice = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
    // Virtual keyboard is always shown for simplicity, but could be conditional
  }, []);

  return (
    <motion.div
      className="keyboard-container"
      variants={fadeIn}
      initial="initial"
      animate="animate"
    >
      {/* Virtual Keyboard */}
      {showVirtualKeyboard && (
        <VirtualKeyboard
          onKeyPress={onKeyPress}
          keyboardState={keyboardState}
          disabled={disabled}
        />
      )}

      {/* Keyboard status indicator (for accessibility) */}
      <div className="sr-only" role="status" aria-live="polite">
        <p>Keyboard is {disabled ? 'disabled' : 'enabled'}</p>
      </div>
    </motion.div>
  );
};

export default Keyboard;