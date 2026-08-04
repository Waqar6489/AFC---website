import { forwardRef } from 'react';
import { Link } from 'react-router-dom';
import { FiLoader } from 'react-icons/fi';

const VARIANTS = {
  primary: 'bg-marigold-400 text-ink-900 hover:bg-marigold-300 active:bg-marigold-500 disabled:bg-marigold-200',
  dark: 'bg-ink-800 text-cream hover:bg-ink-700 active:bg-ink-900 disabled:bg-ink-300',
  outline: 'border border-ink-300 text-ink-800 hover:border-ink-800 hover:bg-ink-50 disabled:opacity-50',
  ghost: 'text-ink-700 hover:bg-ink-100 disabled:opacity-50',
  danger: 'bg-danger text-cream hover:opacity-90 disabled:opacity-50',
};

const SIZES = {
  sm: 'h-9 px-3.5 text-sm',
  md: 'h-11 px-5 text-sm',
  lg: 'h-[3.25rem] px-7 text-base',
};

/** The single Button primitive for the whole app. Pass `to="/path"` to
 * render as a React Router <Link> (so it stays a single focusable
 * element, unlike wrapping a <button> in an <a>) instead of a <button>. */
const Button = forwardRef(function Button(
  { variant = 'primary', size = 'md', isLoading = false, disabled, className = '', children, to, ...props },
  ref,
) {
  const classes = `inline-flex items-center justify-center gap-2 rounded-[var(--radius-card)] font-medium
        transition-colors duration-150 disabled:cursor-not-allowed
        ${VARIANTS[variant]} ${SIZES[size]} ${className}`;

  const content = (
    <>
      {isLoading && <FiLoader className="h-4 w-4 animate-spin" aria-hidden="true" />}
      {children}
    </>
  );

  if (to) {
    return (
      <Link ref={ref} to={to} className={classes} {...props}>
        {content}
      </Link>
    );
  }

  return (
    <button ref={ref} disabled={disabled || isLoading} className={classes} {...props}>
      {content}
    </button>
  );
});

export default Button;
