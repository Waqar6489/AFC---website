import { useEffect, useState } from 'react';
import { Helmet } from 'react-helmet-async';
import { FiBell } from 'react-icons/fi';
import { notificationService } from '@/services/notificationService';
import EmptyState from '@/components/ui/EmptyState';
import PageLoader from '@/components/ui/PageLoader';
import Button from '@/components/ui/Button';

export default function NotificationsPage() {
  const [notifications, setNotifications] = useState(null);
  

  function loadNotifications() {
    notificationService.list().then((data) => setNotifications(data.results ?? data));
  }

  useEffect(loadNotifications, []);

  async function handleMarkRead(id) {
    await notificationService.markRead(id);
    loadNotifications();
  }

  async function handleMarkAllRead() {
    await notificationService.markAllRead();
    loadNotifications();
  }

  if (notifications === null) return <PageLoader />;

  const hasUnread = notifications.some((n) => !n.is_read);

  return (
    <>
      <Helmet><title>Notifications | AFC - Ahmad Foods</title></Helmet>
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-ink-900">Notifications</h1>
        {hasUnread && <Button variant="ghost" size="sm" onClick={handleMarkAllRead}>Mark all as read</Button>}
      </div>

      {notifications.length === 0 ? (
        <EmptyState icon={FiBell} title="No notifications yet" description="Order updates will appear here." className="mt-6" />
      ) : (
        <ul className="mt-6 flex flex-col gap-2">
          {notifications.map((notification) => (
            <li
              key={notification.id}
              onClick={() => !notification.is_read && handleMarkRead(notification.id)}
              className={`cursor-pointer rounded-[var(--radius-card)] border p-4 transition-colors
                ${notification.is_read ? 'border-ink-100 bg-white' : 'border-marigold-200 bg-marigold-50'}`}
            >
              <div className="flex items-center justify-between">
                <p className="text-sm font-semibold text-ink-800">{notification.title}</p>
                <span className="text-xs text-ink-400">{new Date(notification.created_at).toLocaleDateString()}</span>
              </div>
              <p className="mt-1 text-sm text-ink-500">{notification.message}</p>
            </li>
          ))}
        </ul>
      )}
    </>
  );
}
