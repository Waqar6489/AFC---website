import { useEffect, useState } from 'react';
import { dealService } from '@/services/dealService';
import SectionHeading from '@/components/home/SectionHeading';
import DealCard from '@/components/common/DealCard';

export default function DealsSection() {
  const [deals, setDeals] = useState(null);

  useEffect(() => {
    dealService.active().then(setDeals).catch(() => setDeals([]));
  }, []);

  if (deals !== null && deals.length === 0) return null;

  return (
    <section className="bg-ink-50 py-14">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <SectionHeading eyebrow="Limited Time" title="Current Deals" viewAllTo="/deals" />
        {deals === null ? (
          <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
            {Array.from({ length: 3 }).map((_, i) => <div key={i} className="aspect-[4/3] animate-pulse rounded-[var(--radius-card)] bg-ink-200" />)}
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
            {deals.slice(0, 3).map((deal) => <DealCard key={deal.id} deal={deal} />)}
          </div>
        )}
      </div>
    </section>
  );
}
