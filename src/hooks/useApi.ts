/** React Query hooks for KeyCrypt API operations */

import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { gameApi, userApi, handleApiError } from '../lib/api';
import type {
  NewGameRequest,
  NewGameResponse,
  GuessRequest,
  GuessResponse,
  HintsResponse,
  GameStatusResponse,
  UserProgress,
  UserStatistics,
  LeaderboardEntry,
} from '../types/game';

// Game-related hooks
export const useNewGame = () => {
  const queryClient = useQueryClient();

  return useMutation<NewGameResponse, Error, NewGameRequest>({
    mutationFn: async (data) => {
      try {
        const response = await gameApi.newGame(data);
        return response;
      } catch (error) {
        const message = handleApiError(error, 'Failed to start new game');
        throw new Error(message);
      }
    },
    onSuccess: (data) => {
      // Invalidate related queries
      queryClient.invalidateQueries({ queryKey: ['user-stats'] });
      queryClient.invalidateQueries({ queryKey: ['user-progress'] });
    },
    onError: (error) => {
      console.error('New game error:', error);
    },
  });
};

export const useSubmitGuess = () => {
  const queryClient = useQueryClient();

  return useMutation<GuessResponse, Error, GuessRequest>({
    mutationFn: async (data) => {
      try {
        const response = await gameApi.submitGuess(data);
        return response;
      } catch (error) {
        const message = handleApiError(error, 'Failed to submit guess');
        throw new Error(message);
      }
    },
    onSuccess: (data, variables) => {
      // Update game state cache
      queryClient.setQueryData(['game-status', variables.game_id], (old: any) => {
        if (old) {
          return {
            ...old,
            attempts_remaining: data.attempts_remaining,
            game_status: data.game_status,
            attempts: [
              ...old.attempts,
              {
                guess: variables.guess,
                feedback: data.feedback,
                attempt_number: old.attempts.length + 1,
              },
            ],
          };
        }
        return old;
      });

      // Invalidate hints for this game
      queryClient.invalidateQueries({ queryKey: ['hints', variables.game_id] });
      queryClient.invalidateQueries({ queryKey: ['user-stats'] });
    },
    onError: (error) => {
      console.error('Submit guess error:', error);
    },
  });
};

export const useGetHints = (gameId: string, enabled: boolean = true) => {
  return useQuery<HintsResponse, Error>({
    queryKey: ['hints', gameId],
    queryFn: async () => {
      try {
        const response = await gameApi.getHints(gameId);
        return response;
      } catch (error) {
        const message = handleApiError(error, 'Failed to get hints');
        throw new Error(message);
      }
    },
    enabled: enabled && !!gameId,
    staleTime: 10000, // 10 seconds
    refetchInterval: 5000, // Check for new hints every 5 seconds
  });
};

export const useGetGameStatus = (gameId: string, enabled: boolean = true) => {
  return useQuery<GameStatusResponse, Error>({
    queryKey: ['game-status', gameId],
    queryFn: async () => {
      try {
        const response = await gameApi.getGameStatus(gameId);
        return response;
      } catch (error) {
        const message = handleApiError(error, 'Failed to get game status');
        throw new Error(message);
      }
    },
    enabled: enabled && !!gameId,
    staleTime: 30000, // 30 seconds
  });
};

// User-related hooks
export const useCreateUser = () => {
  const queryClient = useQueryClient();

  return useMutation<any, Error, { email?: string; username: string; password: string; display_name?: string }>({
    mutationFn: async (data) => {
      try {
        const response = await userApi.createUser(data);
        return response;
      } catch (error) {
        const message = handleApiError(error, 'Failed to create user');
        throw new Error(message);
      }
    },
    onSuccess: (data) => {
      // Cache user data
      if (data.user?.user_id) {
        queryClient.setQueryData(['user', data.user.user_id], data.user);
      }
    },
    onError: (error) => {
      console.error('Create user error:', error);
    },
  });
};

export const useLogin = () => {
  const queryClient = useQueryClient();

  return useMutation<any, Error, { username: string; password: string }>({
    mutationFn: async (data) => {
      try {
        const response = await userApi.login(data);
        return response;
      } catch (error) {
        const message = handleApiError(error, 'Failed to login');
        throw new Error(message);
      }
    },
    onSuccess: (data) => {
      // Cache user data
      if (data.user?.user_id) {
        queryClient.setQueryData(['user', data.user.user_id], data.user);
        queryClient.invalidateQueries({ queryKey: ['user-stats', data.user.user_id] });
        queryClient.invalidateQueries({ queryKey: ['user-progress', data.user.user_id] });
      }
    },
    onError: (error) => {
      console.error('Login error:', error);
    },
  });
};

export const useCreateGuest = () => {
  const queryClient = useQueryClient();

  return useMutation<any, Error, void>({
    mutationFn: async () => {
      try {
        const response = await userApi.createGuest();
        return response;
      } catch (error) {
        const message = handleApiError(error, 'Failed to create guest session');
        throw new Error(message);
      }
    },
    onSuccess: (data) => {
      // Cache user data
      if (data.user?.user_id) {
        queryClient.setQueryData(['user', data.user.user_id], data.user);
      }
    },
    onError: (error) => {
      console.error('Create guest error:', error);
    },
  });
};

export const useUserProgress = (userId: string, enabled: boolean = true) => {
  return useQuery<{ user_id: string; progress: { [level: number]: UserProgress } }, Error>({
    queryKey: ['user-progress', userId],
    queryFn: async () => {
      try {
        const response = await userApi.getProgress(userId);
        return response;
      } catch (error) {
        const message = handleApiError(error, 'Failed to get user progress');
        throw new Error(message);
      }
    },
    enabled: enabled && !!userId,
    staleTime: 60000, // 1 minute
  });
};

export const useUserStats = (userId: string, enabled: boolean = true) => {
  return useQuery<UserStatistics, Error>({
    queryKey: ['user-stats', userId],
    queryFn: async () => {
      try {
        const response = await userApi.getStats(userId);
        return response.statistics;
      } catch (error) {
        const message = handleApiError(error, 'Failed to get user statistics');
        throw new Error(message);
      }
    },
    enabled: enabled && !!userId,
    staleTime: 300000, // 5 minutes
  });
};

export const useLeaderboard = (level?: number, limit: number = 10, enabled: boolean = true) => {
  return useQuery<{ leaderboard: LeaderboardEntry[] }, Error>({
    queryKey: ['leaderboard', level, limit],
    queryFn: async () => {
      try {
        const response = await userApi.getLeaderboard(level, limit);
        return response;
      } catch (error) {
        const message = handleApiError(error, 'Failed to get leaderboard');
        throw new Error(message);
      }
    },
    enabled,
    staleTime: 120000, // 2 minutes
  });
};

// Utility hooks
export const useApiHealth = () => {
  return useQuery<boolean, Error>({
    queryKey: ['api-health'],
    queryFn: async () => {
      try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000'}/health`);
        return response.ok;
      } catch (error) {
        console.error('Health check failed:', error);
        return false;
      }
    },
    staleTime: 60000, // 1 minute
    refetchInterval: 30000, // Check every 30 seconds
  });
};

// Hook to invalidate all game-related queries
export const useInvalidateGameQueries = () => {
  const queryClient = useQueryClient();

  return (gameId?: string) => {
    if (gameId) {
      queryClient.invalidateQueries({ queryKey: ['game-status', gameId] });
      queryClient.invalidateQueries({ queryKey: ['hints', gameId] });
    }
    queryClient.invalidateQueries({ queryKey: ['user-stats'] });
    queryClient.invalidateQueries({ queryKey: ['user-progress'] });
  };
};

// Hook to prefetch game data
export const usePrefetchGameData = () => {
  const queryClient = useQueryClient();

  return (gameId: string) => {
    queryClient.prefetchQuery({
      queryKey: ['game-status', gameId],
      queryFn: () => gameApi.getGameStatus(gameId),
      staleTime: 30000,
    });

    queryClient.prefetchQuery({
      queryKey: ['hints', gameId],
      queryFn: () => gameApi.getHints(gameId),
      staleTime: 10000,
    });
  };
};

// Hook for optimistic updates
export const useOptimisticUpdate = () => {
  const queryClient = useQueryClient();

  return <T>(
    queryKey: string[],
    updateFn: (oldData: T | undefined) => T,
    rollbackFn?: (oldData: T | undefined) => void
  ) => {
    // Cancel any outgoing refetches
    queryClient.cancelQueries({ queryKey });

    // Snapshot the previous value
    const previousData = queryClient.getQueryData(queryKey);

    // Optimistically update
    queryClient.setQueryData(queryKey, updateFn);

    // Return rollback function
    return () => {
      queryClient.setQueryData(queryKey, previousData);
      rollbackFn?.(previousData);
    };
  };
};

export default {
  // Game hooks
  useNewGame,
  useSubmitGuess,
  useGetHints,
  useGetGameStatus,

  // User hooks
  useCreateUser,
  useLogin,
  useCreateGuest,
  useUserProgress,
  useUserStats,
  useLeaderboard,

  // Utility hooks
  useApiHealth,
  useInvalidateGameQueries,
  usePrefetchGameData,
  useOptimisticUpdate,
};