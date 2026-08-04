import { createResourceService } from './createResourceService';
import {apiClient} from './apiClient';

const base = createResourceService('/notifications/');

export const notificationService = {
  ...base,
  markRead: (id) => base.detailAction(id, 'mark-read'),
  markAllRead: () => apiClient.post('/notifications/mark-all-read/'),
  unreadCount: () => base.listAction('unread-count'),
};
