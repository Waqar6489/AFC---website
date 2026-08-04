import { useEffect, useRef, useState } from 'react';
import { Link, NavLink, useNavigate } from 'react-router-dom';
import {
  FiHeart,
  FiLogOut,
  FiMenu,
  FiPackage,
  FiSearch,
  FiShoppingCart,
  FiUser,
  FiX,
} from 'react-icons/fi';
import { useAuth } from '@/hooks/useAuth';
import { useCart } from '@/hooks/useCart';
import { useWishlist } from '@/hooks/useWishlist';
import Logo from '@/components/common/Logo';
import Button from '@/components/ui/Button';

const NAV_LINKS = [
  { to: '/', label: 'Home', end: true },
  { to: '/shop', label: 'Shop' },
  { to: '/deals', label: 'Deals' },
  { to: '/about', label: 'About Us' },
  { to: '/contact', label: 'Contact Us' },
];

export default function Navbar() {
  const { isAuthenticated, user, logout } = useAuth();
  const { cart } = useCart();
  const { count: wishlistCount } = useWishlist();
  const navigate = useNavigate();

  const [searchTerm, setSearchTerm] = useState('');
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isAccountMenuOpen, setIsAccountMenuOpen] = useState(false);
  const accountMenuRef = useRef(null);

  useEffect(() => {
    function handleClickOutside(event) {
      if (accountMenuRef.current && !accountMenuRef.current.contains(event.target)) {
        setIsAccountMenuOpen(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  function handleSearchSubmit(event) {
    event.preventDefault();
    const trimmed = searchTerm.trim();
    navigate(trimmed ? `/shop?search=${encodeURIComponent(trimmed)}` : '/shop');
    setIsMobileMenuOpen(false);
  }

  async function handleLogout() {
    await logout();
    setIsAccountMenuOpen(false);
    navigate('/');
  }

  const navLinkClass = ({ isActive }) =>
    `text-sm font-medium transition-colors ${isActive ? 'text-marigold-500' : 'text-ink-600 hover:text-ink-900'}`;

  return (
    <header className="sticky top-0 z-50 bg-cream/95 backdrop-blur supports-[backdrop-filter]:bg-cream/80">
      {/* Thin marigold top strip — a small "packaging ribbon" touch */}
      <div className="h-1 w-full bg-marigold-400" />

      <div className="border-b border-ink-100">
        <div className="mx-auto flex h-28 max-w-7xl items-center gap-4 px-4 sm:px-6 lg:px-5">
          <Link to="/" aria-label="AFC - Ahmad Foods home" className='h-22 w-35'>
            <Logo />
          </Link>

          <nav className="hidden items-center gap-7 lg:flex  pl-9.5" aria-label="Primary">
            {NAV_LINKS.map((link) => (
              <NavLink key={link.to} to={link.to} end={link.end} className={navLinkClass}>
                {link.label}
              </NavLink>
            ))}
          </nav>

          <form onSubmit={handleSearchSubmit} className="ml-auto hidden max-w-sm flex-1 md:flex">
            <div className="relative w-full">
              <FiSearch className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-ink-300" />
              <input
                type="search"
                value={searchTerm}
                onChange={(event) => setSearchTerm(event.target.value)}
                placeholder="Search cakes, pastries, sweets..."
                aria-label="Search products"
                className="h-10 w-full rounded-[var(--radius-pill)] border border-ink-200 bg-white pl-9 pr-4
                  text-sm placeholder:text-ink-300 focus:border-marigold-400"
              />
            </div>
          </form>

          <div className="ml-auto flex items-center gap-1 md:ml-0">
            <IconLink to={isAuthenticated ? '/dashboard/wishlist' : '/login'} label="Wishlist" count={wishlistCount}>
              <FiHeart className="h-5 w-5" />
            </IconLink>

            <IconLink to="/cart" label="Cart" count={cart.item_count}>
              <FiShoppingCart className="h-5 w-5" />
            </IconLink>

            {isAuthenticated ? (
              <div className="relative ml-1" ref={accountMenuRef}>
                <button
                  onClick={() => setIsAccountMenuOpen((open) => !open)}
                  className="flex h-10 w-10 items-center justify-center rounded-full bg-ink-800 text-sm font-semibold text-cream"
                  aria-haspopup="menu"
                  aria-expanded={isAccountMenuOpen}
                  aria-label="Account menu"
                >
                  {user?.full_name?.[0]?.toUpperCase() || <FiUser className="h-4 w-4" />}
                </button>
                {isAccountMenuOpen && (
                  <div
                    role="menu"
                    className="absolute right-0 mt-2 w-52 rounded-[var(--radius-card)] border border-ink-100 bg-white py-1.5 shadow-[var(--shadow-lifted)]"
                  >
                    <div className="border-b border-ink-100 px-4 py-2.5">
                      <p className="truncate text-sm font-semibold text-ink-800">{user?.full_name || 'My Account'}</p>
                      <p className="truncate text-xs text-ink-400">{user?.email}</p>
                    </div>
                    <MenuLink to="/dashboard" icon={FiUser} onClick={() => setIsAccountMenuOpen(false)}>
                      Dashboard
                    </MenuLink>
                    <MenuLink to="/dashboard/orders" icon={FiPackage} onClick={() => setIsAccountMenuOpen(false)}>
                      My Orders
                    </MenuLink>
                    <button
                      role="menuitem"
                      onClick={handleLogout}
                      className="flex w-full items-center gap-2.5 px-4 py-2.5 text-left text-sm text-danger hover:bg-ink-50"
                    >
                      <FiLogOut className="h-4 w-4" /> Logout
                    </button>
                  </div>
                )}
              </div>
            ) : (
              <div className="ml-1 hidden items-center gap-2 sm:flex">
                <Button to="/login" variant="ghost" size="sm">Login</Button>
                <Button to="/register" variant="dark" size="sm">Register</Button>
              </div>
            )}

            <button
              className="ml-1 flex h-10 w-10 items-center justify-center rounded-full hover:bg-ink-50 lg:hidden"
              onClick={() => setIsMobileMenuOpen((open) => !open)}
              aria-label="Toggle menu"
              aria-expanded={isMobileMenuOpen}
            >
              {isMobileMenuOpen ? <FiX className="h-5 w-5" /> : <FiMenu className="h-5 w-5" />}
            </button>
          </div>
        </div>
      </div>

      {isMobileMenuOpen && (
        <div className="border-b border-ink-100 bg-cream px-4 py-4 lg:hidden">
          <form onSubmit={handleSearchSubmit} className="mb-4 flex">
            <div className="relative w-full">
              <FiSearch className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-ink-300" />
              <input
                type="search"
                value={searchTerm}
                onChange={(event) => setSearchTerm(event.target.value)}
                placeholder="Search..."
                aria-label="Search products"
                className="h-10 w-full rounded-[var(--radius-pill)] border border-ink-200 bg-white pl-9 pr-4 text-sm"
              />
            </div>
          </form>
          <nav className="flex flex-col gap-1" aria-label="Mobile">
            {NAV_LINKS.map((link) => (
              <NavLink
                key={link.to}
                to={link.to}
                end={link.end}
                onClick={() => setIsMobileMenuOpen(false)}
                className={({ isActive }) =>
                  `rounded-md px-3 py-2.5 text-sm font-medium ${isActive ? 'bg-marigold-50 text-marigold-600' : 'text-ink-700 hover:bg-ink-50'}`
                }
              >
                {link.label}
              </NavLink>
            ))}
            {!isAuthenticated && (
              <div className="mt-2 flex gap-2 border-t border-ink-100 pt-3">
                <Button to="/login" variant="ghost" size="sm" className="flex-1" onClick={() => setIsMobileMenuOpen(false)}>
                  Login
                </Button>
                <Button to="/register" variant="dark" size="sm" className="flex-1" onClick={() => setIsMobileMenuOpen(false)}>
                  Register
                </Button>
              </div>
            )}
          </nav>
        </div>
      )}
    </header>
  );
}

function IconLink({ to, label, count, children }) {
  return (
    <Link
      to={to}
      aria-label={label}
      className="relative flex h-10 w-10 items-center justify-center rounded-full text-ink-700 hover:bg-ink-50"
    >
      {children}
      {count > 0 && (
        <span className="absolute -right-0.5 -top-0.5 flex h-4 min-w-4 items-center justify-center rounded-full bg-marigold-400 px-1 text-[10px] font-bold text-ink-900">
          {count > 99 ? '99+' : count}
        </span>
      )}
    </Link>
  );
}

function MenuLink({ to, icon: Icon, onClick, children }) {
  return (
    <Link
      to={to}
      role="menuitem"
      onClick={onClick}
      className="flex items-center gap-2.5 px-4 py-2.5 text-sm text-ink-700 hover:bg-ink-50"
    >
      <Icon className="h-4 w-4" /> {children}
    </Link>
  );
}
