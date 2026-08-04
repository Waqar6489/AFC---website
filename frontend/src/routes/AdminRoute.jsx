import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '@/hooks/useAuth';
import PageLoader from '@/components/ui/PageLoader';

/** Gates a route behind admin/staff role — a lightweight UX convenience
 * only. The backend independently enforces this on every admin
 * endpoint, so this is not a security boundary by itself. */
export default function AdminRoute() {
  const { isAuthenticated, isAdmin, isLoading } = useAuth();

  if (isLoading) return <PageLoader />;
  if (!isAuthenticated || !isAdmin) return <Navigate to="/" replace />;

  return <Outlet />;
}
