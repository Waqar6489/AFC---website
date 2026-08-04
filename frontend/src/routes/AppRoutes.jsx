import { lazy, Suspense } from 'react';
import { Route, Routes } from 'react-router-dom';
import PageLoader from '@/components/ui/PageLoader';
import ProtectedRoute from '@/routes/ProtectedRoute';
import GuestOnlyRoute from '@/routes/GuestOnlyRoute';

// Layouts are small and used on nearly every route, so they're loaded
// eagerly. Every page is code-split via React.lazy per the spec's
// lazy-loading / code-splitting requirement.
import MainLayout from '@/layouts/MainLayout';
import DashboardLayout from '@/layouts/DashboardLayout';

const HomePage = lazy(() => import('@/pages/HomePage'));
const ShopPage = lazy(() => import('@/pages/ShopPage'));
const ProductDetailPage = lazy(() => import('@/pages/ProductDetailPage'));
const DealsPage = lazy(() => import('@/pages/DealsPage'));
const AboutPage = lazy(() => import('@/pages/AboutPage'));
const ContactPage = lazy(() => import('@/pages/ContactPage'));
const CartPage = lazy(() => import('@/pages/CartPage'));
const CheckoutPage = lazy(() => import('@/pages/CheckoutPage'));
const NotFoundPage = lazy(() => import('@/pages/NotFoundPage'));

const PrivacyPolicyPage = lazy(() => import('@/pages/static/PrivacyPolicyPage'));
const TermsAndConditionsPage = lazy(() => import('@/pages/static/TermsAndConditionsPage'));
const RefundPolicyPage = lazy(() => import('@/pages/static/RefundPolicyPage'));
const ShippingPolicyPage = lazy(() => import('@/pages/static/ShippingPolicyPage'));

const LoginPage = lazy(() => import('@/pages/auth/LoginPage'));
const RegisterPage = lazy(() => import('@/pages/auth/RegisterPage'));
const ForgotPasswordPage = lazy(() => import('@/pages/auth/ForgotPasswordPage'));
const ResetPasswordPage = lazy(() => import('@/pages/auth/ResetPasswordPage'));
const VerifyEmailPage = lazy(() => import('@/pages/auth/VerifyEmailPage'));
const CheckEmailPage = lazy(() => import('@/pages/auth/CheckEmailPage'));

const DashboardOverviewPage = lazy(() => import('@/pages/dashboard/DashboardOverviewPage'));
const OrdersPage = lazy(() => import('@/pages/dashboard/OrdersPage'));
const OrderDetailPage = lazy(() => import('@/pages/dashboard/OrderDetailPage'));
const ProfilePage = lazy(() => import('@/pages/dashboard/ProfilePage'));
const AddressesPage = lazy(() => import('@/pages/dashboard/AddressesPage'));
const WishlistPage = lazy(() => import('@/pages/dashboard/WishlistPage'));
const NotificationsPage = lazy(() => import('@/pages/dashboard/NotificationsPage'));
const MyReviewsPage = lazy(() => import('@/pages/dashboard/MyReviewsPage'));

export default function AppRoutes() {
  return (
    <Suspense fallback={<PageLoader />}>
      <Routes>
        <Route element={<MainLayout />}>
          {/* Public pages */}
          <Route path="/" element={<HomePage />} />
          <Route path="/shop" element={<ShopPage />} />
          <Route path="/product/:slug" element={<ProductDetailPage />} />
          <Route path="/deals" element={<DealsPage />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/contact" element={<ContactPage />} />
          <Route path="/cart" element={<CartPage />} />
          <Route path="/privacy-policy" element={<PrivacyPolicyPage />} />
          <Route path="/terms-and-conditions" element={<TermsAndConditionsPage />} />
          <Route path="/refund-policy" element={<RefundPolicyPage />} />
          <Route path="/shipping-policy" element={<ShippingPolicyPage />} />

          {/* Guest-only auth pages */}
          <Route element={<GuestOnlyRoute />}>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
          </Route>
          <Route path="/forgot-password" element={<ForgotPasswordPage />} />
          <Route path="/check-email" element={<CheckEmailPage />} />
          <Route path="/reset-password" element={<ResetPasswordPage />} />
          <Route path="/verify-email" element={<VerifyEmailPage />} />

          {/* Authenticated-only */}
          <Route element={<ProtectedRoute />}>
            <Route path="/checkout" element={<CheckoutPage />} />
            <Route path="/dashboard" element={<DashboardLayout />}>
              <Route index element={<DashboardOverviewPage />} />
              <Route path="orders" element={<OrdersPage />} />
              <Route path="orders/:orderNumber" element={<OrderDetailPage />} />
              <Route path="profile" element={<ProfilePage />} />
              <Route path="addresses" element={<AddressesPage />} />
              <Route path="wishlist" element={<WishlistPage />} />
              <Route path="notifications" element={<NotificationsPage />} />
              <Route path="reviews" element={<MyReviewsPage />} />
            </Route>
          </Route>

          <Route path="*" element={<NotFoundPage />} />
        </Route>
      </Routes>
    </Suspense>
  );
}
