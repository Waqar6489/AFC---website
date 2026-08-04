import { apiClient } from './apiClient';
import { createResourceService } from './createResourceService';

const cartItems = createResourceService('/orders/cart-items/');
const orderHistory = createResourceService('/orders/history/');

export const orderService = {
  getCart: () => apiClient.get('/orders/cart/').then((res) => res.data),
  cartItems,

  checkDelivery: ({ latitude, longitude }) =>
    apiClient.post('/orders/check-delivery/', { latitude, longitude }).then((res) => res.data),

  checkout: (payload) => apiClient.post('/orders/checkout/', payload).then((res) => res.data),

  history: orderHistory,
  updateStatus: (orderNumber, payload) =>
    orderHistory.detailAction(orderNumber, 'update-status', payload),
};
