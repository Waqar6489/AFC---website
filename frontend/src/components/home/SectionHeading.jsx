import { Link } from 'react-router-dom';

export default function SectionHeading({ eyebrow, title, viewAllTo }) {
  return (
    <div className="mb-6 flex items-end justify-between">
      <div>
        {eyebrow && <p className="text-xs font-semibold uppercase tracking-[0.16em] text-marigold-600">{eyebrow}</p>}
        <h2 className="mt-1 text-2xl font-bold text-ink-900">{title}</h2>
      </div>
      {viewAllTo && (
        <Link to={viewAllTo} className="text-sm font-semibold text-marigold-600 hover:underline">
          View All &rarr;
        </Link>
      )}
    </div>
  );
}
