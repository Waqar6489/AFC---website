/** Consistent "nothing here yet" state — empty cart, no orders, no
 * search results, etc. */
export default function EmptyState({ icon: Icon, title, description, action, className = '' }) {
  return (
    <div className={`flex flex-col items-center justify-center gap-3 rounded-[var(--radius-card)] border border-dashed border-ink-200 px-6 py-16 text-center ${className}`}>
      {Icon && <Icon className="h-10 w-10 text-ink-300" aria-hidden="true" />}
      <p className="text-base font-semibold text-ink-800">{title}</p>
      {description && <p className="max-w-sm text-sm text-ink-400">{description}</p>}
      {action}
    </div>
  );
}
