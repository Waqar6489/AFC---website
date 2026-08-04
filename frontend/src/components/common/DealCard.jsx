import { useState } from 'react';
import toast from 'react-hot-toast';
import { FiCopy } from 'react-icons/fi';
import DealCountdown from '@/components/common/DealCountdown';

export default function DealCard({ deal }) {
  const [copied, setCopied] = useState(false);

  function handleCopyCode() {
    if (!deal.coupon_code) return;
    navigator.clipboard.writeText(deal.coupon_code);
    setCopied(true);
    toast.success('Coupon code copied!');
    setTimeout(() => setCopied(false), 2000);
  }

  return (
    <div className="overflow-hidden rounded-[var(--radius-card)] border border-ink-100 bg-white">
      <div className="relative aspect-[16/9] bg-ink-100">
        {deal.banner_image ? (
          <img src={deal.banner_image} alt={deal.title} className="h-full w-full object-cover" />
        ) : (
          <div className="flex h-full w-full items-center justify-center bg-ink-800 text-marigold-300">
            <span className="font-price text-2xl font-bold">
              {deal.discount_type === 'percentage' ? `${deal.discount_value}% OFF` : `Rs ${deal.discount_value} OFF`}
            </span>
          </div>
        )}
      </div>
      <div className="p-4">
        <h3 className="font-semibold text-ink-900">{deal.title}</h3>
        {deal.description && <p className="mt-1 line-clamp-2 text-sm text-ink-500">{deal.description}</p>}

        <div className="mt-3 flex items-center justify-between">
          <DealCountdown secondsRemaining={deal.seconds_remaining} />
          {deal.coupon_code && (
            <button
              onClick={handleCopyCode}
              className="flex items-center gap-1.5 rounded-full border border-dashed border-marigold-400 bg-marigold-50 px-3 py-1.5 text-xs font-bold text-marigold-700"
            >
              {deal.coupon_code} <FiCopy className="h-3 w-3" />
            </button>
          )}
        </div>
        {copied && <p className="mt-1 text-xs text-success">Copied to clipboard!</p>}
      </div>
    </div>
  );
}
