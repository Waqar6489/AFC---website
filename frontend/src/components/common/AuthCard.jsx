import { Link } from 'react-router-dom';
import Logo from '@/components/common/Logo';

/** Shared shell for the auth pages (Login/Register/Forgot/Reset/Verify)
 * — centers a card on the cream background with the logo above it. */
export default function AuthCard({ title, subtitle, children, footer }) {
  return (
    <div className="flex min-h-[calc(100vh-4rem)] items-center justify-center bg-ink-50 px-4 py-12">
      <div className="w-full max-w-md">
        <div className="mb-6 flex justify-center">
          <Link to="/"><Logo /></Link>
        </div>
        <div className="rounded-[var(--radius-card)] border border-ink-100 bg-white p-8 shadow-[var(--shadow-card)]">
          <h1 className="text-xl font-bold text-ink-900">{title}</h1>
          {subtitle && <p className="mt-1.5 text-sm text-ink-400">{subtitle}</p>}
          <div className="mt-6">{children}</div>
        </div>
        {footer && <p className="mt-5 text-center text-sm text-ink-500">{footer}</p>}
      </div>
    </div>
  );
}
