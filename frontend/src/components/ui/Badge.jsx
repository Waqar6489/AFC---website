const VARIANTS = {
  marigold: 'bg-marigold-400 text-ink-900',
  ink: 'bg-ink-800 text-cream',
  outline: 'border border-ink-300 text-ink-600',
  success: 'bg-success/10 text-success',
  danger: 'bg-danger/10 text-danger',
};

/** Small pill label — used for stock/trending/deal/order-status tags. */
export default function Badge({ variant = 'marigold', className = '', children }) {
  return (
    <span
      className={`inline-flex  cursor-pointer items-center rounded-[var(--radius-pill)] px-2.5 py-1 text-xs font-semibold
        tracking-wide ${VARIANTS[variant]} ${className}`}
    >
      {children}
    </span>
  );
}
