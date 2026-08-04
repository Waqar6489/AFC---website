import StarRating from '@/components/common/StarRating';

export default function ReviewList({ reviews }) {
  if (reviews.length === 0) {
    return <p className="text-sm text-ink-400">No reviews yet — be the first to review this product.</p>;
  }
  return (
    <ul className="flex flex-col gap-4">
      {reviews.map((review) => (
        <li key={review.id} className="rounded-[var(--radius-card)] border border-ink-100 bg-white p-4">
          <div className="flex items-center justify-between">
            <StarRating value={review.rating} />
            <span className="text-xs text-ink-400">{new Date(review.created_at).toLocaleDateString()}</span>
          </div>
          <p className="mt-2 text-sm text-ink-600">{review.comment}</p>
          <p className="mt-2 text-xs font-semibold text-ink-700">{review.user_name || 'Verified Customer'}</p>
        </li>
      ))}
    </ul>
  );
}
