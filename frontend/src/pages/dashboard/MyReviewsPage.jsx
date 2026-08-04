import { useEffect, useState } from 'react';
import { Helmet } from 'react-helmet-async';
import { FiStar } from 'react-icons/fi';
import { reviewService } from '@/services/reviewService';
import { useAuth } from '@/hooks/useAuth';
import EmptyState from '@/components/ui/EmptyState';
import PageLoader from '@/components/ui/PageLoader';
import Badge from '@/components/ui/Badge';

export default function MyReviewsPage() {
  const { user } = useAuth();
  const [reviews, setReviews] = useState(null);

  useEffect(() => {
    // The reviews endpoint returns the requesting user's own reviews
    // (approved or pending) plus publicly-approved ones when
    // unfiltered; scope client-side to just this user's submissions.
    reviewService.list().then((data) => {
      const all = data.results ?? data;
      setReviews(all.filter((r) => r.user_name === user?.full_name));
    });
  }, [user]);

  if (reviews === null) return <PageLoader />;

  return (
    <>
      <Helmet><title>My Reviews | AFC - Ahmad Foods</title></Helmet>
      <h1 className="text-2xl font-bold text-ink-900">My Reviews</h1>

      {reviews.length === 0 ? (
        <EmptyState icon={FiStar} title="No reviews yet" description="Reviews you submit for delivered orders will show up here." className="mt-6" />
      ) : (
        <ul className="mt-6 flex flex-col gap-3">
          {reviews.map((review) => (
            <li key={review.id} className="rounded-[var(--radius-card)] border border-ink-100 bg-white p-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-1 text-marigold-400">
                  {Array.from({ length: 5 }).map((_, index) => (
                    <FiStar key={index} className={index < review.rating ? 'fill-current' : 'text-ink-200'} />
                  ))}
                </div>
                <Badge variant={review.is_approved ? 'success' : 'outline'}>
                  {review.is_approved ? 'Published' : 'Pending Approval'}
                </Badge>
              </div>
              <p className="mt-2 text-sm text-ink-600">{review.comment}</p>
              <p className="mt-1 text-xs text-ink-400">{new Date(review.created_at).toLocaleDateString()}</p>
            </li>
          ))}
        </ul>
      )}
    </>
  );
}
