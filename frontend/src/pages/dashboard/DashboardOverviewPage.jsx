import { useEffect, useState } from "react";
import { notificationService } from "@/services/notificationService";
import { Helmet } from 'react-helmet-async';
import { Link } from 'react-router-dom';
import { FiBell, FiHeart, FiMapPin, FiPackage, FiStar, FiUser } from 'react-icons/fi';
import { useAuth } from '@/hooks/useAuth';



const SHORTCUTS = [
  { to: '/dashboard/orders', label: 'My Orders', icon: FiPackage, description: 'Track and review past orders' },
  { to: '/dashboard/profile', label: 'Profile', icon: FiUser, description: 'Update your personal details' },
  { to: '/dashboard/addresses', label: 'Addresses', icon: FiMapPin, description: 'Manage delivery addresses' },
  { to: '/dashboard/wishlist', label: 'Wishlist', icon: FiHeart, description: 'Products you have saved' },
  { to: '/dashboard/notifications', label: 'Notifications', icon: FiBell, description: 'Order updates and alerts' },
  { to: '/dashboard/reviews', label: 'My Reviews', icon: FiStar, description: 'Reviews you have submitted' },
];

function DashboardOverviewPage() {
   const { user } = useAuth();
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
    <>
      <Helmet><title>Dashboard | AFC - Ahmad Foods</title></Helmet>
      <h1 className="text-2xl font-bold text-ink-900">
        Welcome back{user?.full_name ? `, ${user.full_name}` : ''}
      </h1>
      <p className="mt-1 text-sm text-ink-500">Here’s a quick look at your account.</p>

      <div className="mt-8 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {SHORTCUTS.map(({ to, label, icon: Icon, description }) => (
          <Link
            key={to}
            to={to}
            className="flex items-start gap-3 rounded-[var(--radius-card)] border border-ink-100 bg-white p-5 transition-shadow hover:shadow-[var(--shadow-card)]"
          >
            <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-marigold-50 text-marigold-600">
              {label === "Notifications" ? (
                <div className="relative">
                  <FiBell className="h-5 w-5" />

                  {unreadCount > 0 && (
                    <span className="absolute -top-2 -right-2 flex h-5 w-5 items-center justify-center rounded-full bg-[#E7A618] text-[10px] font-bold text-ink-900">
                      {unreadCount}
                    </span>
                  )}
                </div>
              ) : (
                <Icon className="h-5 w-5" />
              )}
            </span>
            <span>
              <span className="block font-semibold text-ink-800">{label}</span>
              <span className="block text-sm text-ink-400">{description}</span>
            </span>
          </Link>
        ))}
      </div>
    </>
  );
}
export default DashboardOverviewPage