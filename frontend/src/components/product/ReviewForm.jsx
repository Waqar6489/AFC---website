import { useState } from 'react';
import { useForm } from 'react-hook-form';
import toast from 'react-hot-toast';
import { FiStar } from 'react-icons/fi';
import Button from '@/components/ui/Button';
import { reviewService } from '@/services/reviewService';
import { extractApiError } from '@/services/apiClient';

export default function ReviewForm({ productId, onSubmitted }) {
  const [rating, setRating] = useState(0);
  const [hoverRating, setHoverRating] = useState(0);
  const { register, handleSubmit, reset, formState: { errors, isSubmitting } } = useForm();

  async function onSubmit(values) {
    if (rating === 0) {
      toast.error('Please select a star rating.');
      return;
    }
    try {
      await reviewService.create({ product: productId, rating, comment: values.comment });
      toast.success('Thanks! Your review has been submitted for approval.');
      reset();
      setRating(0);
      onSubmitted?.();
    } catch (error) {
      toast.error(extractApiError(error).message);
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="rounded-[var(--radius-card)] border border-ink-100 bg-white p-5" noValidate>
      <h3 className="font-semibold text-ink-800">Write a Review</h3>
      <p className="mt-1 text-xs text-ink-400">Only customers with a delivered order for this product can review it.</p>

      <div className="mt-3 flex items-center gap-1">
        {Array.from({ length: 5 }).map((_, index) => {
          const starValue = index + 1;
          return (
            <button
              key={starValue}
              type="button"
              onClick={() => setRating(starValue)}
              onMouseEnter={() => setHoverRating(starValue)}
              onMouseLeave={() => setHoverRating(0)}
              aria-label={`Rate ${starValue} stars`}
            >
              <FiStar
                className={`h-6 w-6 ${(hoverRating || rating) >= starValue ? 'fill-marigold-400 text-marigold-400' : 'text-ink-200'}`}
              />
            </button>
          );
        })}
      </div>

      <textarea
        rows={3}
        placeholder="Share your experience..."
        className="mt-3 w-full rounded-[var(--radius-card)] border border-ink-200 bg-cream px-3.5 py-2.5 text-sm focus:border-marigold-400"
        {...register('comment', { required: 'Please write a short review.' })}
      />
      {errors.comment && <p className="mt-1 text-xs text-danger">{errors.comment.message}</p>}

      <Button type="submit" isLoading={isSubmitting} size="sm" className="mt-3">Submit Review</Button>
    </form>
  );
}
