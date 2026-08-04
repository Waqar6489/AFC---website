import { NavLink, Outlet } from 'react-router-dom';
import {
  FiBell,
  FiHeart,
  FiHome,
  FiMapPin,
  FiPackage,
  FiStar,
  FiUser,
} from 'react-icons/fi';
// import { notificationService } from "@/services/notificationService";
import { notificationService } from '@/services/notificationService';
import { useEffect, useState } from 'react';

const NAV_ITEMS = [
  { to: '/dashboard', label: 'Overview', icon: FiHome, end: true },
  { to: '/dashboard/orders', label: 'Orders', icon: FiPackage },
  { to: '/dashboard/profile', label: 'Profile', icon: FiUser },
  { to: '/dashboard/addresses', label: 'Addresses', icon: FiMapPin },
  { to: '/dashboard/wishlist', label: 'Wishlist', icon: FiHeart },
  { to: '/dashboard/notifications', label: 'Notifications', icon: FiBell },
  { to: '/dashboard/reviews', label: 'My Reviews', icon: FiStar },
];

/** Nested inside MainLayout (navbar/footer stay), adds a left sidebar for
 * the customer account area — Orders/Profile/Addresses/Wishlist/
 * Notifications/Reviews, per spec. */
export default function DashboardLayout() {
  const [unreadCount, setUnreadCount] = useState(0);


  useEffect(() => {
    loadUnreadCount();

    const interval = setInterval(loadUnreadCount, 3000);

    return () => clearInterval(interval);
  }, []);

  async function loadUnreadCount() {
    try {
      const data = await notificationService.list();
      const notifications = data.results ?? data;

      setUnreadCount(
        notifications.filter((n) => !n.is_read).length
      );
    } catch (error) {
      console.error(error);
    }
  }
  return (
    <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
      <div className="grid grid-cols-1 gap-8 lg:grid-cols-[240px_1fr]">
        <aside>
          <nav className="flex gap-1 overflow-x-auto pb-2 lg:flex-col lg:overflow-visible lg:pb-0" aria-label="Dashboard">
            {NAV_ITEMS.map(({ to, label, icon: Icon, end }) => (
              <NavLink
                key={to}
                to={to}
                end={end}
                className={({ isActive }) =>
                  `flex shrink-0 items-center gap-2.5 whitespace-nowrap rounded-[var(--radius-card)] px-3.5 py-2.5 text-sm font-medium transition-colors
    ${isActive ? 'bg-ink-800 text-cream' : 'text-ink-600 hover:bg-ink-50'}`
                }
              >
                <div className="relative">
                  <Icon className="h-4 w-4" />

                  {label === "Notifications" && unreadCount > 0 && (
                    <span className="absolute -top-2 -right-2 flex h-4 min-w-4 items-center justify-center rounded-full bg-[#E7A618] px-1 text-[10px] font-bold text-ink-900">
                      {unreadCount > 99 ? "99+" : unreadCount}
                    </span>
                  )}
                </div>

                <span>{label}</span>
              </NavLink>
            ))}
          </nav>
        </aside>
        <div className="min-w-0">
          <Outlet />
        </div>
      </div>
    </div>
  );
}
