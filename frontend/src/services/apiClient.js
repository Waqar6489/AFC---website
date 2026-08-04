import axios from 'axios';
import { tokenStorage } from '@/utils/tokenStorage';

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api/v1';

export const apiClient = axios.create({
  baseURL: API_URL,
  headers: { 'Content-Type': 'application/json' },
});

// Separate, interceptor-free instance for the token refresh call itself —
// using the main `apiClient` there would recurse into the 401 handler.
const refreshClient = axios.create({ baseURL: API_URL });

apiClient.interceptors.request.use((config) => {
  const publicEndpoints = [
    '/auth/register/',
    '/auth/login/',
    '/auth/verify-email/',
    '/auth/resend-verification/',
    '/auth/forgot-password/',
    '/auth/reset-password/',
    '/auth/refresh/',
  ];

  const isPublicEndpoint = publicEndpoints.some((endpoint) =>
    config.url?.includes(endpoint)
  );

  if (!isPublicEndpoint) {
    const token = tokenStorage.getAccessToken();

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }

  return config;
});

let isRefreshing = false;
let pendingQueue = [];

function resolveQueue(error, newAccessToken) {
  pendingQueue.forEach(({ resolve, reject }) => {
    if (error) reject(error);
    else resolve(newAccessToken);
  });
  pendingQueue = [];
}

function broadcastLogout() {
  tokenStorage.clear();
  window.dispatchEvent(new CustomEvent('afc:unauthorized'));
}

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    const status = error.response?.status;

    // Never try to refresh on the auth endpoints themselves — a failed
    // login/refresh should surface as-is, not trigger another refresh.
    const isAuthEndpoint =
  originalRequest?.url?.includes('/auth/login') ||
  originalRequest?.url?.includes('/auth/register') ||
  originalRequest?.url?.includes('/auth/verify-email') ||
  originalRequest?.url?.includes('/auth/resend-verification') ||
  originalRequest?.url?.includes('/auth/forgot-password') ||
  originalRequest?.url?.includes('/auth/reset-password') ||
  originalRequest?.url?.includes('/auth/refresh');

    if (status === 401 && !originalRequest._retry && !isAuthEndpoint) {
      const refreshToken = tokenStorage.getRefreshToken();
      if (!refreshToken) {
        broadcastLogout();
        return Promise.reject(error);
      }

      if (isRefreshing) {
        // A refresh is already in flight — queue this request and replay
        // it once the new access token is available, rather than firing
        // a second, redundant refresh call.
        return new Promise((resolve, reject) => {
          pendingQueue.push({ resolve, reject });
        }).then((newAccessToken) => {
          originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
          return apiClient(originalRequest);
        });
      }

      originalRequest._retry = true;
      isRefreshing = true;

      try {
        const { data } = await refreshClient.post('/auth/refresh/', { refresh: refreshToken });
        tokenStorage.setAccessToken(data.access);
        resolveQueue(null, data.access);
        originalRequest.headers.Authorization = `Bearer ${data.access}`;
        return apiClient(originalRequest);
      } catch (refreshError) {
        resolveQueue(refreshError, null);
        broadcastLogout();
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }

    return Promise.reject(error);
  },
);

/**
 * Normalizes the backend's error envelope ({ success, message, errors })
 * into a plain, consistent shape for UI code:
 *   { message: string, fieldErrors: Record<string, string[]> }
 */
export function extractApiError(error) {
  const data = error?.response?.data;

  if (!data) {
    return {
      message: 'Network error. Please check your connection and try again.',
      fieldErrors: {},
    };
  }

  const fieldErrors = data.errors || {};

  // First validation error nikaalo
  let message = data.message || 'Something went wrong. Please try again.';

  if (Object.keys(fieldErrors).length > 0) {
    const firstKey = Object.keys(fieldErrors)[0];
    const firstError = fieldErrors[firstKey];

    if (Array.isArray(firstError)) {
      message = firstError[0];
    } else if (typeof firstError === 'string') {
      message = firstError;
    }
  }

  return {
    message,
    fieldErrors,
  };
}
