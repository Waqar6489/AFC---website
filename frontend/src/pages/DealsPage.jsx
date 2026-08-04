import { useEffect, useState } from 'react';
import { Helmet } from 'react-helmet-async';
import { dealService } from '@/services/dealService';
import PageHeader from '@/components/common/PageHeader';
import DealCard from '@/components/common/DealCard';
import PageLoader from '@/components/ui/PageLoader';
import EmptyState from '@/components/ui/EmptyState';
import { FiTag } from 'react-icons/fi';

export default function DealsPage() {
  const [deals, setDeals] = useState(null);

  useEffect(() => {
    dealService.active().then(setDeals);
  }, []);

  return (
    <>
      <Helmet><title>Deals | AFC - Ahmad Foods</title></Helmet>
      <PageHeader eyebrow="Offers" title="Deals & Discounts" description="Countdown timers, coupon codes, and seasonal offers." />
      <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        {deals === null ? (
          <PageLoader />
        ) : deals.length === 0 ? (
          <EmptyState icon={FiTag} title="No active deals right now" description="Check back soon for new offers." />
        ) : (
          <div className="grid grid-cols-1 gap-6 ">
            {deals.map((deal) => <DealCard key={deal.id} deal={deal} />)}
          </div>
        )}
      </div>
    </>
  );
}
