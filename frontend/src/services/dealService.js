import { apiClient } from './apiClient';
import { createResourceService } from './createResourceService';

const base = createResourceService('/deals/');

export const dealService = {
  ...base,
  active: (params) => base.listAction('active', params),
  validateCoupon: (payload) => apiClient.post('/deals/validate-coupon/', payload).then((res) => res.data),
};
