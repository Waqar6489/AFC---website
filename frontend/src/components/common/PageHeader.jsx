/** Consistent page-title band used across static/simple pages. */
export default function PageHeader({ eyebrow, title, description }) {
  return (
    <div className="border-b border-ink-100 bg-ink-50">
      <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        {eyebrow && (
          <p className="mb-2 text-xs font-semibold uppercase tracking-[0.16em] text-marigold-600">{eyebrow}</p>
        )}
        <h1 className="text-3xl font-bold tracking-tight text-ink-900 sm:text-4xl">{title}</h1>
        {description && <p className="mt-3 max-w-2xl text-ink-500">{description}</p>}
      </div>
    </div>
  );
}
