import { FiStar } from 'react-icons/fi';

export default function StarRating({ value = 0, size = 'sm' }) {
  const sizeClass = size === 'sm' ? 'h-3.5 w-3.5' : 'h-4 w-4';
  return (
    <div className="flex items-center gap-0.5 text-marigold-400" aria-label={`${value} out of 5 stars`}>
      {Array.from({ length: 5 }).map((_, index) => (
        <FiStar key={index} className={`${sizeClass} ${index < Math.round(value) ? 'fill-current' : 'text-ink-200'}`} />
      ))}
    </div>
  );
}
