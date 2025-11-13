/** API client configuration and utilities for KeyCrypt */

import axios, { AxiosInstance, AxiosError } from 'axios';

// API base URL - change for production
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api';

// Create axios instance
export const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000, // 15 seconds timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for debugging
apiClient.interceptors.request.use(
  (config) => {
    if (process.env.NODE_ENV === 'development') {
      console.log(`📡 API Request: ${config.method?.toUpperCase()} ${config.url}`);
    }
    return config;
  },
  (error) => {
    console.error('❌ API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for debugging and error handling
apiClient.interceptors.response.use(
  (response) => {
    if (process.env.NODE_ENV === 'development') {
      console.log(`✅ API Response: ${response.config.method?.toUpperCase()} ${response.config.url}`);
    }
    return response;
  },
  (error: AxiosError) => {
    console.error('❌ API Response Error:', {
      url: error.config?.url,
      method: error.config?.method,
      status: error.response?.status,
      data: error.response?.data,
      message: error.message,
    });

    // Handle specific error cases
    if (error.response?.status === 401) {
      // Unauthorized - handle authentication
      console.warn('Authentication required');
    } else if (error.response?.status >= 500) {
      // Server error
      console.error('Server error occurred');
    }

    return Promise.reject(error);
  }
);

// API endpoint functions
export const gameApi = {
  /**
   * Start a new game
   */
  newGame: async (data: { level: number; dictionary_category?: string; user_id?: string }) => {
    const response = await apiClient.post('/new-game', data);
    return response.data;
  },

  /**
   * Submit a guess
   */
  submitGuess: async (data: { game_id: string; guess: string }) => {
    const response = await apiClient.post('/guess', data);
    return response.data;
  },

  /**
   * Get hints for a game
   */
  getHints: async (gameId: string) => {
    const response = await apiClient.get(`/hints?game_id=${gameId}`);
    return response.data;
  },

  /**
   * Get game status
   */
  getGameStatus: async (gameId: string) => {
    const response = await apiClient.get(`/game/${gameId}`);
    return response.data;
  },
};

export const userApi = {
  /**
   * Create a new user account
   */
  createUser: async (data: { email?: string; username: string; password: string; display_name?: string }) => {
    const response = await apiClient.post('/user/create', data);
    return response.data;
  },

  /**
   * Login user
   */
  login: async (data: { username: string; password: string }) => {
    const response = await apiClient.post('/user/login', data);
    return response.data;
  },

  /**
   * Create guest user
   */
  createGuest: async () => {
    const response = await apiClient.post('/user/guest');
    return response.data;
  },

  /**
   * Get user progress
   */
  getProgress: async (userId: string) => {
    const response = await apiClient.get(`/user/progress/${userId}`);
    return response.data;
  },

  /**
   * Get user statistics
   */
  getStats: async (userId: string) => {
    const response = await apiClient.get(`/user/stats/${userId}`);
    return response.data;
  },

  /**
   * Get leaderboard
   */
  getLeaderboard: async (level?: number, limit: number = 10) => {
    const params = new URLSearchParams();
    if (level) params.append('level', level.toString());
    params.append('limit', limit.toString());

    const response = await apiClient.get(`/leaderboard?${params}`);
    return response.data;
  },
};

// Utility functions
export const isApiError = (error: any): error is AxiosError => {
  return error && error.isAxiosError;
};

export const getErrorMessage = (error: unknown): string => {
  if (isApiError(error)) {
    return error.response?.data?.error || error.message || 'Unknown API error';
  }
  if (error instanceof Error) {
    return error.message;
  }
  return 'An unknown error occurred';
};

export const handleApiError = (error: unknown, fallbackMessage: string = 'An error occurred') => {
  const message = getErrorMessage(error);
  console.error('API Error:', error);

  // You could also show a toast notification here
  // toast.error(message || fallbackMessage);

  return message || fallbackMessage;
};

// Health check
export const healthCheck = async (): Promise<boolean> => {
  try {
    await apiClient.get('/health');
    return true;
  } catch (error) {
    console.error('Health check failed:', error);
    return false;
  }
};

// Test connection
export const testConnection = async (): Promise<{ success: boolean; message: string }> => {
  try {
    const response = await apiClient.get('/health');
    return {
      success: true,
      message: 'Connection successful',
    };
  } catch (error) {
    return {
      success: false,
      message: handleApiError(error, 'Connection failed'),
    };
  }
};

export default apiClient;