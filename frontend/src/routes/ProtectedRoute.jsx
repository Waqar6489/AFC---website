import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { useAuth } from '@/hooks/useAuth';
import PageLoader from '@/components/ui/PageLoader';

/** Gates any nested route behind authentication — used for the customer
 * dashboard, checkout, and anywhere else the spec requires a logged-in
 * user (e.g. "guest clicks Add To Cart -> redirect to Login"). */
export default function ProtectedRoute() {
  const { isAuthenticated, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) return <PageLoader />;

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return <Outlet />;
}
