/** Animation presets and utilities for KeyCrypt using Framer Motion */

import { Variants, Transition } from 'framer-motion';

// Tile flip animation for Wordle-style feedback
export const tileFlip: Variants = {
  initial: {
    rotateX: 0,
    scale: 1,
    opacity: 1,
  },
  animate: {
    rotateX: 360,
    scale: [1, 1.1, 1],
    opacity: 1,
    transition: {
      duration: 0.6,
      ease: 'easeInOut',
      times: [0, 0.5, 1],
    },
  },
  exit: {
    rotateX: 0,
    scale: 1,
    opacity: 0,
    transition: {
      duration: 0.3,
    },
  },
};

// Shake animation for invalid words
export const shakeAnimation: Variants = {
  initial: { x: 0 },
  animate: {
    x: [0, -10, 10, -10, 10, -5, 5, 0],
    transition: {
      duration: 0.5,
      ease: 'easeInOut',
    },
  },
};

// Bounce animation for victory
export const bounceIn: Variants = {
  initial: {
    scale: 0,
    opacity: 0,
  },
  animate: {
    scale: [0, 1.2, 0.9, 1],
    opacity: 1,
    transition: {
      type: 'spring',
      stiffness: 260,
      damping: 20,
      duration: 0.6,
    },
  },
};

// Slide and fade for hint reveal
export const hintReveal: Variants = {
  initial: {
    y: 20,
    opacity: 0,
    scale: 0.8,
  },
  animate: {
    y: 0,
    opacity: 1,
    scale: 1,
    transition: {
      duration: 0.8,
      ease: 'easeOut',
      type: 'spring',
      stiffness: 100,
    },
  },
  exit: {
    y: -20,
    opacity: 0,
    scale: 0.8,
    transition: {
      duration: 0.3,
    },
  },
};

// Staggered container for list animations
export const staggerContainer: Variants = {
  initial: { opacity: 0 },
  animate: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
    },
  },
  exit: {
    opacity: 0,
    transition: {
      staggerChildren: 0.05,
      staggerDirection: -1,
    },
  },
};

// Fade in for containers
export const fadeIn: Variants = {
  initial: { opacity: 0 },
  animate: { opacity: 1 },
  exit: { opacity: 0 },
};

// Slide up for modals
export const slideUp: Variants = {
  initial: { y: 100, opacity: 0 },
  animate: { y: 0, opacity: 1 },
  exit: { y: 100, opacity: 0 },
};

// Slide down for dropdowns
export const slideDown: Variants = {
  initial: { y: -100, opacity: 0 },
  animate: { y: 0, opacity: 1 },
  exit: { y: -100, opacity: 0 },
};

// Scale for buttons on hover
export const scaleOnHover: Variants = {
  initial: { scale: 1 },
  hover: { scale: 1.05 },
  tap: { scale: 0.95 },
};

// Pulse for highlighting
export const pulse: Variants = {
  initial: { scale: 1 },
  animate: {
    scale: [1, 1.1, 1],
    transition: {
      duration: 1,
      repeat: Infinity,
      ease: 'easeInOut',
    },
  },
};

// Glow effect for new unlocks
export const glow: Variants = {
  initial: { boxShadow: '0 0 0 rgba(78, 205, 196, 0.4)' },
  animate: {
    boxShadow: [
      '0 0 0 rgba(78, 205, 196, 0.4)',
      '0 0 20px rgba(78, 205, 196, 0.8)',
      '0 0 0 rgba(78, 205, 196, 0.4)',
    ],
    transition: {
      duration: 2,
      repeat: Infinity,
      ease: 'easeInOut',
    },
  },
};

// Typewriter effect for text
export const typewriter = (text: string): Variants => ({
  initial: { width: 0 },
  animate: {
    width: '100%',
    transition: {
      duration: text.length * 0.05,
      ease: 'easeOut',
    },
  },
});

// Loading skeleton
export const skeleton: Variants = {
  initial: { opacity: 0.3 },
  animate: {
    opacity: [0.3, 0.7, 0.3],
    transition: {
      duration: 1.5,
      repeat: Infinity,
      ease: 'easeInOut',
    },
  },
};

// Page transitions
export const pageTransition: Variants = {
  initial: { x: 300, opacity: 0 },
  animate: { x: 0, opacity: 1 },
  exit: { x: -300, opacity: 0 },
};

// Custom transition types
export const smoothTransition: Transition = {
  type: 'spring',
  stiffness: 100,
  damping: 15,
};

export const bouncyTransition: Transition = {
  type: 'spring',
  stiffness: 260,
  damping: 20,
};

export const gentleTransition: Transition = {
  type: 'tween',
  duration: 0.3,
  ease: 'easeInOut',
};

// Staggered tile animations for game board
export const tileRevealStagger = (index: number): Variants => ({
  initial: { rotateY: -90, opacity: 0 },
  animate: {
    rotateY: 0,
    opacity: 1,
    transition: {
      delay: index * 0.05,
      duration: 0.4,
      ease: 'easeOut',
    },
  },
});

// Keyboard key press animation
export const keyPress: Variants = {
  initial: { scale: 1, backgroundColor: '#374151' },
  tap: {
    scale: 0.9,
    backgroundColor: '#4B5563',
    transition: { duration: 0.1 },
  },
};

// Success animation
export const successAnimation: Variants = {
  initial: { scale: 0, rotate: -180 },
  animate: {
    scale: 1,
    rotate: 0,
    transition: {
      type: 'spring',
      stiffness: 200,
      damping: 15,
    },
  },
};

// Error animation
export const errorAnimation: Variants = {
  initial: { x: 0, backgroundColor: 'transparent' },
  animate: {
    x: [-5, 5, -5, 5, 0],
    backgroundColor: '#EF4444',
    transition: {
      x: { duration: 0.5 },
      backgroundColor: { duration: 0.2 },
    },
  },
};

// Level unlock animation
export const levelUnlock: Variants = {
  initial: { scale: 0.8, opacity: 0, rotate: -10 },
  animate: {
    scale: [0.8, 1.1, 1],
    opacity: 1,
    rotate: 0,
    transition: {
      duration: 0.8,
      ease: 'easeOut',
      times: [0, 0.6, 1],
    },
  },
};

// Progress bar animation
export const progressFill: Variants = {
  initial: { width: '0%' },
  animate: { width: '100%' },
  exit: { width: '0%' },
};

// Floating animation for decorative elements
export const floating: Variants = {
  initial: { y: 0 },
  animate: {
    y: [-10, 10, -10],
    transition: {
      duration: 3,
      repeat: Infinity,
      ease: 'easeInOut',
    },
  },
};

// Responsive animation that respects user preferences
export const getResponsiveAnimation = (prefersReducedMotion: boolean) => {
  if (prefersReducedMotion) {
    return {
      initial: { opacity: 0 },
      animate: { opacity: 1 },
      exit: { opacity: 0 },
      transition: { duration: 0 },
    };
  }

  return {
    initial: { opacity: 0, scale: 0.9 },
    animate: { opacity: 1, scale: 1 },
    exit: { opacity: 0, scale: 0.9 },
    transition: gentleTransition,
  };
};

// Utility to create staggered delays
export const createStaggerDelay = (baseDelay: number = 0.1) => (index: number) => index * baseDelay;

// Utility for conditional animations
export const conditionalVariants = (condition: boolean, trueVariant: any, falseVariant: any) =>
  condition ? trueVariant : falseVariant;

// Preset animation groups
export const gameAnimations = {
  tileFlip,
  shake: shakeAnimation,
  bounce: bounceIn,
  hintReveal,
};

export const uiAnimations = {
  fadeIn,
  slideUp,
  scale: scaleOnHover,
  pulse,
  glow,
  skeleton,
};

export const pageAnimations = {
  transition: pageTransition,
  stagger: staggerContainer,
};