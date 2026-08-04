import { apiClient } from './apiClient';

export const contactService = {
  submit: (payload) => apiClient.post('/contact/submit/', payload).then((res) => res.data),
  subscribeNewsletter: (email) =>
    apiClient.post('/contact/newsletter/subscribe/', { email }).then((res) => res.data),
};
