import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';
import { FiPackage } from 'react-icons/fi';
import { orderService } from '@/services/orderService';
import PageLoader from '@/components/ui/PageLoader';
import EmptyState from '@/components/ui/EmptyState';
import Badge from '@/components/ui/Badge';

const STATUS_VARIANT = {
  delivered: 'success',
  cancelled: 'danger',
  refunded: 'danger',
};

export default function OrdersPage() {
  const [orders, setOrders] = useState(null);

  useEffect(() => {
    orderService.history.list().then((data) => setOrders(data.results ?? data));
  }, []);

  if (orders === null) return <PageLoader />;

  return (
    <>
      <Helmet><title>My Orders | AFC - Ahmad Foods</title></Helmet>
      <h1 className="text-2xl font-bold text-ink-900">My Orders</h1>

      {orders.length === 0 ? (
        <EmptyState
          icon={FiPackage}
          title="No orders yet"
          description="Once you place an order, it will show up here."
          className="mt-6"
        />
      ) : (
        <ul className="mt-6 flex flex-col gap-3">
          {orders.map((order) => (
            <li key={order.order_number}>
              <Link
                to={`/dashboard/orders/${order.order_number}`}
                className="flex flex-wrap items-center justify-between gap-3 rounded-[var(--radius-card)] border border-ink-100 bg-white p-4 transition-shadow hover:shadow-[var(--shadow-card)]"
              >
                <div>
                  <p className="font-price text-sm font-semibold text-ink-800">{order.order_number}</p>
                  <p className="text-xs text-ink-400">{new Date(order.created_at).toLocaleDateString()}</p>
                </div>
                <p className="font-price text-sm text-ink-600">Rs {order.total_amount}</p>
                <Badge variant={STATUS_VARIANT[order.status] || 'outline'} className="capitalize">
                  {order.status.replaceAll('_', ' ')}
                </Badge>
              </Link>
            </li>
          ))}
        </ul>
      )}
    </>
  );
}
