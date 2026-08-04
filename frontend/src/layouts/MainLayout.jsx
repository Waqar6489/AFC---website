import { Outlet } from 'react-router-dom';
import Navbar from '@/components/layout/Navbar';
import Footer from '@/components/layout/Footer';

/** The standard public-site shell: sticky navbar, routed page content,
 * footer. Used for Home/Shop/Product/Cart/Checkout/static pages. */
export default function MainLayout() {
  return (
    <div className="flex min-h-screen flex-col bg-cream">
      <Navbar />
      <main className="flex-1">
        <Outlet />
      </main>
      <Footer />
    </div>
  );
}
