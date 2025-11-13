/** Level selection page for KeyCrypt */

'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { useNewGame } from '../../hooks/useApi';
import { fadeIn, staggerContainer, levelUnlock } from '../../lib/animations';
import { useRouter } from 'next/navigation';
import type { LevelInfo } from '../../types/game';

// Level information
const LEVELS: LevelInfo[] = [
  {
    level: 1,
    name: 'Caesar Cipher',
    description: 'Simple shift cipher used by Julius Caesar',
    historical_context: 'Used for military messages in ancient Rome',
    difficulty: 'Easy',
    unlocked: true,
    completed: false,
  },
  {
    level: 2,
    name: 'Monoalphabetic Substitution',
    description: 'Random letter mapping throughout the alphabet',
    historical_context: 'Used throughout history for simple codes',
    difficulty: 'Easy',
    unlocked: true,
    completed: false,
  },
  {
    level: 3,
    name: 'Playfair Cipher',
    description: 'Digraph substitution using a 5x5 matrix',
    historical_context: 'Used by British forces in World War I',
    difficulty: 'Medium',
    unlocked: true,
    completed: false,
  },
  {
    level: 4,
    name: 'Hill Cipher',
    description: 'Matrix-based encryption using linear algebra',
    historical_context: 'First cipher using mathematical principles',
    difficulty: 'Medium',
    unlocked: true,
    completed: false,
  },
  {
    level: 5,
    name: 'Rail Fence',
    description: 'Transposition cipher writing in zig-zag pattern',
    historical_context: 'Used in American Civil War',
    difficulty: 'Medium',
    unlocked: true,
    completed: false,
  },
  {
    level: 6,
    name: 'Vigenère Cipher',
    description: 'Polyalphabetic substitution using keyword',
    historical_context: 'Considered unbreakable for 300 years',
    difficulty: 'Medium',
    unlocked: true,
    completed: false,
  },
  {
    level: 7,
    name: 'One-Time Pad',
    description: 'Theoretical perfect secrecy cipher',
    historical_context: 'Used during the Cold War for secure communications',
    difficulty: 'Hard',
    unlocked: true,
    completed: false,
  },
  {
    level: 8,
    name: 'DES/3DES',
    description: 'Modern symmetric block cipher',
    historical_context: 'FIPS standard from 1977, now deprecated',
    difficulty: 'Hard',
    unlocked: true,
    completed: false,
  },
  {
    level: 9,
    name: 'RSA',
    description: 'Asymmetric encryption with public/private keys',
    historical_context: 'Foundation of modern secure communications',
    difficulty: 'Expert',
    unlocked: true,
    completed: false,
  },
];

const getDifficultyColor = (difficulty: string) => {
  switch (difficulty) {
    case 'Easy':
      return 'bg-green-100 text-green-800 border-green-200';
    case 'Medium':
      return 'bg-yellow-100 text-yellow-800 border-yellow-200';
    case 'Hard':
      return 'bg-orange-100 text-orange-800 border-orange-200';
    case 'Expert':
      return 'bg-red-100 text-red-800 border-red-200';
    default:
      return 'bg-gray-100 text-gray-800 border-gray-200';
  }
};

const getDifficultyIcon = (difficulty: string) => {
  switch (difficulty) {
    case 'Easy':
      return '🌟';
    case 'Medium':
      return '🔥';
    case 'Hard':
      return '⚡';
    case 'Expert':
      return '🏆';
    default:
      return '❓';
  }
};

export default function LevelsPage() {
  const [selectedLevel, setSelectedLevel] = useState<number | null>(null);
  const newGameMutation = useNewGame();
  const router = useRouter();

  const handleLevelSelect = async (level: number) => {
    setSelectedLevel(level);

    try {
      // Start a new game
      const result = await newGameMutation.mutateAsync({
        level,
        dictionary_category: 'common',
      });

      // Navigate to game page with game ID
      router.push(`/game/${result.game_id}`);
    } catch (error) {
      console.error('Failed to start game:', error);
      // Handle error - show toast or alert
      alert('Failed to start game. Please try again.');
    }
  };

  const completedLevels = 0; // This would come from user progress
  const unlockedLevels = Math.min(completedLevels + 1, 9);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 dark:from-gray-900 dark:to-gray-800 p-4">
      {/* Header */}
      <motion.div
        className="text-center mb-8"
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-4xl md:text-6xl font-bold text-gray-800 dark:text-white mb-4">
          🔐 KeyCrypt
        </h1>
        <p className="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
          Learn cryptography through interactive puzzles. Master 9 levels from ancient ciphers to modern encryption.
        </p>
      </motion.div>

      {/* Progress Overview */}
      <motion.div
        className="max-w-4xl mx-auto mb-8"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
      >
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
          <h2 className="text-2xl font-semibold text-gray-800 dark:text-white mb-4">
            Your Progress
          </h2>
          <div className="flex items-center justify-between mb-2">
            <span className="text-gray-600 dark:text-gray-300">Overall Progress</span>
            <span className="text-sm text-gray-500 dark:text-gray-400">
              {completedLevels}/9 levels completed
            </span>
          </div>
          <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3">
            <motion.div
              className="bg-gradient-to-r from-blue-500 to-purple-500 h-3 rounded-full"
              initial={{ width: 0 }}
              animate={{ width: `${(completedLevels / 9) * 100}%` }}
              transition={{ duration: 1, delay: 0.5 }}
            />
          </div>
        </div>
      </motion.div>

      {/* Level Grid */}
      <motion.div
        className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
        variants={staggerContainer}
        initial="initial"
        animate="animate"
      >
        {LEVELS.map((level, index) => {
          const isUnlocked = level.level <= unlockedLevels;
          const isCompleted = level.level <= completedLevels;
          const isLoading = selectedLevel === level.level && newGameMutation.isPending;

          return (
            <motion.div
              key={level.level}
              variants={levelUnlock}
              custom={index}
              whileHover={isUnlocked ? { scale: 1.02 } : {}}
              className={`
                relative bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden
                ${isUnlocked ? 'cursor-pointer hover:shadow-xl' : 'opacity-75 cursor-not-allowed'}
                transition-all duration-300
              `}
              onClick={() => isUnlocked && handleLevelSelect(level.level)}
            >
              {/* Level Badge */}
              <div className="absolute top-4 right-4 z-10">
                <div className={`
                  px-3 py-1 rounded-full text-xs font-semibold border
                  ${getDifficultyColor(level.difficulty)}
                `}>
                  {getDifficultyIcon(level.difficulty)} {level.difficulty}
                </div>
              </div>

              {/* Lock Overlay */}
              {!isUnlocked && (
                <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center z-20">
                  <div className="text-center">
                    <div className="text-4xl mb-2">🔒</div>
                    <p className="text-white font-semibold">Complete Level {level.level - 1}</p>
                  </div>
                </div>
              )}

              {/* Completion Badge */}
              {isCompleted && (
                <div className="absolute top-4 left-4 z-10">
                  <div className="bg-green-500 text-white rounded-full p-2">
                    <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  </div>
                </div>
              )}

              {/* Content */}
              <div className="p-6">
                <div className="text-center mb-4">
                  <div className="text-3xl font-bold text-blue-600 dark:text-blue-400 mb-2">
                    Level {level.level}
                  </div>
                  <h3 className="text-xl font-semibold text-gray-800 dark:text-white">
                    {level.name}
                  </h3>
                </div>

                <p className="text-gray-600 dark:text-gray-300 text-sm mb-4">
                  {level.description}
                </p>

                <div className="text-xs text-gray-500 dark:text-gray-400">
                  <p className="mb-1">📜 {level.historical_context}</p>
                </div>

                {/* Action Button */}
                {isUnlocked && (
                  <motion.button
                    className={`
                      w-full mt-4 px-4 py-2 rounded-lg font-semibold
                      ${isLoading
                        ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                        : 'bg-blue-600 hover:bg-blue-700 text-white'
                      }
                      transition-colors duration-200
                    `}
                    whileHover={isUnlocked && !isLoading ? { scale: 1.05 } : {}}
                    whileTap={isUnlocked && !isLoading ? { scale: 0.95 } : {}}
                    disabled={isLoading}
                  >
                    {isLoading ? (
                      <div className="flex items-center justify-center gap-2">
                        <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                        Starting...
                      </div>
                    ) : isCompleted ? (
                      'Play Again'
                    ) : (
                      'Start Level'
                    )}
                  </motion.button>
                )}
              </div>
            </motion.div>
          );
        })}
      </motion.div>

      {/* Back to Home */}
      <motion.div
        className="text-center mt-8"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1 }}
      >
        <button
          onClick={() => router.push('/')}
          className="px-6 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg font-semibold transition-colors duration-200"
        >
          ← Back to Home
        </button>
      </motion.div>
    </div>
  );
}