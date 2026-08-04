import { apiClient } from './apiClient';

export const authService = {
  register: (payload) => apiClient.post('/auth/register/', payload).then((res) => res.data),

  login: (payload) => apiClient.post('/auth/login/', payload).then((res) => res.data),

  logout: (refresh) => apiClient.post('/auth/logout/', { refresh }).then((res) => res.data),

  me: () => apiClient.get('/auth/me/').then((res) => res.data),

  verifyEmail: (payload) => apiClient.post('/auth/verify-email/', payload).then((res) => res.data),

  resendVerification: (email) =>
    apiClient.post('/auth/resend-verification/', { email }).then((res) => res.data),

  forgotPassword: (email) => apiClient.post('/auth/forgot-password/', { email }).then((res) => res.data),

  resetPassword: (payload) => apiClient.post('/auth/reset-password/', payload).then((res) => res.data),

  changePassword: (payload) => apiClient.post('/auth/change-password/', payload).then((res) => res.data),
};
