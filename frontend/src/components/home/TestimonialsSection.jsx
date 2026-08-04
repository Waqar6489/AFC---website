import { useEffect, useState } from 'react';
import { reviewService } from '@/services/reviewService';
import StarRating from '@/components/common/StarRating';

export default function TestimonialsSection() {
  const [reviews, setReviews] = useState([]);

  useEffect(() => {
    // Unauthenticated requests only ever receive approved reviews (the
    // backend filters this), so no extra params are needed here.
    reviewService.list({ page_size: 6 }).then((data) => setReviews((data.results ?? data).filter((r) => r.is_approved)));
  }, []);

  if (reviews.length === 0) return null;

  return (
    <section className="bg-ink-800 py-14">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <p className="text-xs font-semibold uppercase tracking-[0.16em] text-marigold-300">Testimonials</p>
          <h2 className="mt-1 text-2xl font-bold text-cream">What Our Customers Say</h2>
        </div>
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {reviews.map((review) => (
            <div key={review.id} className="rounded-[var(--radius-card)] border border-ink-600 bg-ink-700 p-5">
              <StarRating value={review.rating} />
              <p className="mt-3 text-sm text-ink-200">&ldquo;{review.comment}&rdquo;</p>
              <p className="mt-3 text-sm font-semibold text-marigold-300">{review.user_name || 'Verified Customer'}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
