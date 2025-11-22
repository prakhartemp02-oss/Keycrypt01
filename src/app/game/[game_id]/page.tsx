/** Dynamic game page for active KeyCrypt gameplay */

'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { GameBoard } from '../../../components/GameBoard/GameBoard';
import { VirtualKeyboard } from '../../../components/Keyboard/VirtualKeyboard';
import { HintPanel } from '../../../components/Hints/HintPanel';
import { useGetGameStatus, useSubmitGuess, useGetHints } from '../../../hooks/useApi';
import { useGameState } from '../../../hooks/useGameState';
import { fadeIn } from '../../../lib/animations';
import type { GameStatusResponse, GuessResponse, LetterFeedback } from '../../../types/game';

export default function GamePage() {
  const params = useParams();
  const router = useRouter();
  const gameId = params.game_id as string;

  const [showError, setShowError] = useState<string | null>(null);

  // API hooks
  const {
    data: gameData,
    isLoading: isLoadingGame,
    error: gameError,
    refetch: refetchGame,
  } = useGetGameStatus(gameId);

  const submitGuessMutation = useSubmitGuess();
  const {
    data: hintsData,
    isLoading: isLoadingHints,
    refetch: refetchHints,
  } = useGetHints(gameId);

  // Game state management
  const {
    gameState,
    handleLetterInput,
    handleBackspace,
    handleSubmit,
    processGuessResult,
    updateUnlockedHints,
    keyboardState,
    isSubmitting,
    error: gameStateError,
    validateGuess,
  } = useGameState(gameData ? convertApiDataToGameState(gameData) : {}, {
    onGameEnd: (status) => {
      console.log(`Game ${status}!`);
      // Could show a modal or navigate to results
    },
    onHintUnlock: (hints) => {
      console.log('Hints unlocked:', hints);
      refetchHints(); // Refetch hints when new ones are unlocked
    },
  });

  // Convert API data to game state format
  function convertApiDataToGameState(data: GameStatusResponse) {
    return {
      game_id: data.game_id,
      level: data.level,
      attempts_remaining: data.attempts_remaining,
      attempts_allowed: data.attempts_allowed,
      current_guess: '',
      submitted_guesses: data.attempts || [],
      unlocked_hints: hintsData?.unlocked ? Object.entries(hintsData.unlocked).map(([type, content]) => ({
        type: type as any,
        content,
      })) : [],
      game_status: data.game_status as 'ongoing' | 'won' | 'lost',
      cipher_info: data.cipher_info || {
        name: data.encrypted_meta.cipher,
        level: data.level,
        description: 'Decrypt the secret word',
      },
      encrypted_meta: data.encrypted_meta,
      hint_unlock_rules: data.hint_unlock_rules,
    };
  }

  // Handle guess submission
  const handleGuessSubmit = async (guess: string) => {
    if (!validateGuess()) {
      setShowError(gameStateError || 'Invalid guess');
      setTimeout(() => setShowError(null), 3000);
      return;
    }

    try {
      const result: GuessResponse = await submitGuessMutation.mutateAsync({
        game_id: gameId,
        guess: guess.toUpperCase(),
      });

      // Process the result
      processGuessResult(
        guess,
        result.feedback,
        result.attempts_remaining,
        Array.isArray(result.unlocked_hints)
          ? result.unlocked_hints
          : Object.keys(result.unlocked_hints || {}),
        result.game_status
      );

      // Update unlocked hints if they were returned
      if (result.unlocked_hints && !Array.isArray(result.unlocked_hints)) {
        updateUnlockedHints(
          Object.entries(result.unlocked_hints).map(([type, content]) => ({
            type: type as any,
            content,
          }))
        );
      }

      // Refetch game status to ensure we're in sync
      refetchGame();
    } catch (error) {
      setShowError(error instanceof Error ? error.message : 'Failed to submit guess');
      setTimeout(() => setShowError(null), 3000);
    }
  };

  // Handle virtual keyboard input
  const handleKeyPress = (key: string) => {
    if (gameState.game_status !== 'ongoing') return;

    if (key === 'ENTER') {
      if (gameState.current_guess.length > 0) {
        handleGuessSubmit(gameState.current_guess);
      }
    } else if (key === 'BACK') {
      handleBackspace();
    } else if (/^[A-Z]$/.test(key)) {
      handleLetterInput(key);
    }
  };

  // Handle physical keyboard input
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (gameState.game_status !== 'ongoing') return;

      const key = event.key.toUpperCase();

      // Prevent default for game keys
      if (/^[A-Z]$/.test(key) || key === 'ENTER' || key === 'BACKSPACE') {
        event.preventDefault();
      }

      if (key === 'ENTER') {
        if (gameState.current_guess.length > 0) {
          handleGuessSubmit(gameState.current_guess);
        }
      } else if (key === 'BACKSPACE') {
        handleBackspace();
      } else if (/^[A-Z]$/.test(key)) {
        handleLetterInput(key);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [gameState.current_guess, gameState.game_status, handleLetterInput, handleBackspace]);

  // Handle loading and error states
  if (isLoadingGame) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center">
        <motion.div
          className="text-center"
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5 }}
        >
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-xl text-gray-600 dark:text-gray-300">Loading game...</p>
        </motion.div>
      </div>
    );
  }

  if (gameError || !gameData) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center p-4">
        <motion.div
          className="bg-white dark:bg-gray-800 rounded-lg shadow-xl p-8 max-w-md w-full text-center"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <div className="text-red-500 text-6xl mb-4">🎮</div>
          <h2 className="text-2xl font-bold text-gray-800 dark:text-white mb-4">
            Game Not Found
          </h2>
          <p className="text-gray-600 dark:text-gray-300 mb-6">
            {gameError instanceof Error ? gameError.message : 'Unable to load the game. Please try again.'}
          </p>
          <div className="space-y-3">
            <button
              onClick={() => refetchGame()}
              className="w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold transition-colors duration-200"
            >
              Try Again
            </button>
            <button
              onClick={() => router.push('/levels')}
              className="w-full px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg font-semibold transition-colors duration-200"
            >
              Back to Levels
            </button>
          </div>
        </motion.div>
      </div>
    );
  }

  return (
    <motion.div
      className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 dark:from-gray-900 dark:to-gray-800 pb-20 lg:pb-0"
      variants={fadeIn}
      initial="initial"
      animate="animate"
    >
      {/* Error Display */}
      {showError && (
        <motion.div
          className="fixed top-4 left-1/2 transform -translate-x-1/2 z-50 bg-red-500 text-white px-6 py-3 rounded-lg shadow-lg"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
        >
          <p className="font-semibold">{showError}</p>
        </motion.div>
      )}

      {/* Return to Levels Button */}
      <motion.div
        className="fixed top-4 left-4 z-40"
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: 0.5 }}
      >
        <button
          onClick={() => router.push('/levels')}
          className="px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg font-semibold transition-colors duration-200 shadow-lg"
        >
          ← Back to Levels
        </button>
      </motion.div>

      {/* Game Status Indicator */}
      {gameState.game_status !== 'ongoing' && (
        <motion.div
          className="fixed top-4 right-4 z-40"
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.5 }}
        >
          <div className={`px-6 py-3 rounded-lg shadow-lg font-bold text-white ${
            gameState.game_status === 'won'
              ? 'bg-green-500'
              : 'bg-red-500'
          }`}>
            {gameState.game_status === 'won' ? '🎉 Victory!' : '😔 Game Over'}
          </div>
        </motion.div>
      )}

      {/* Main Game Content */}
      <div className="flex flex-col lg:flex-row min-h-screen">
        {/* Game Board - Takes most of the space on desktop */}
        <div className="flex-1 flex items-center justify-center p-4">
          <GameBoard
            gameState={gameState}
            onGuessSubmit={handleGuessSubmit}
            isSubmitting={isSubmitting || submitGuessMutation.isPending}
            lastGuessResult={gameState.submitted_guesses[gameState.submitted_guesses.length - 1]}
          />
        </div>

        {/* Side Panel - Hints */}
        <div className="lg:w-80 lg:bg-white lg:dark:bg-gray-800 lg:border-l lg:border-gray-200 lg:dark:border-gray-700 p-4 lg:p-6">
          {/* Hint Panel */}
          <div className="lg:sticky lg:top-4">
            <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-4 flex items-center gap-2">
              <span>💡</span>
              Hints & Clues
            </h3>

            <HintPanel
              gameState={gameState}
              unlockedHints={hintsData?.unlocked || {}}
              isVisible={true}
            />
          </div>
        </div>
      </div>

      {/* Virtual Keyboard - Shows on mobile, hidden on desktop */}
      <div className="lg:hidden">
        <VirtualKeyboard
          onKeyPress={handleKeyPress}
          keyboardState={keyboardState}
          disabled={isSubmitting || submitGuessMutation.isPending || gameState.game_status !== 'ongoing'}
        />
      </div>
    </motion.div>
  );
}