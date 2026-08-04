import { apiClient } from './apiClient';
import { createResourceService } from './createResourceService';

const addressResource = createResourceService('/accounts/addresses/');

export const accountService = {
  getProfile: () => apiClient.get('/accounts/profile/').then((res) => res.data),
  updateProfile: (payload) => apiClient.patch('/accounts/profile/', payload).then((res) => res.data),

  addresses: addressResource,
};
