import { apiClient } from './apiClient';

export const coreService = {
  getSiteConfig: () => apiClient.get('/core/site-config/').then((res) => res.data),
  getAdminAnalytics: () => apiClient.get('/core/admin/analytics/').then((res) => res.data),
};
