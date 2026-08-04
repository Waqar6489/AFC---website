import { useEffect, useState,useRef } from 'react';
import { Link, useParams } from 'react-router-dom';
import { toast } from 'react-toastify';
import { Helmet } from 'react-helmet-async';
import { FiCheck } from 'react-icons/fi';
import { orderService } from '@/services/orderService';
import PageLoader from '@/components/ui/PageLoader';
import Badge from '@/components/ui/Badge';

const TIMELINE_STEPS = [
  'pending', 'confirmed', 'preparing', 'cooking', 'packing',
  'ready_for_pickup', 'out_for_delivery', 'nearby', 'delivered',
];

export default function OrderDetailPage() {
  const { orderNumber } = useParams();
  const [order, setOrder] = useState(null);
  const previousStatus = useRef(null);

  useEffect(() => {
  let interval;

  const loadOrder = async () => {
  try {
    const data = await orderService.history.retrieve(orderNumber);

    if (!order) {
      previousStatus.current = data.status;
      setOrder(data);
      return;
    }

    if (previousStatus.current !== data.status) {
      toast.success(
        `Your order is now ${data.status.replaceAll("_", " ")}`
      );

      previousStatus.current = data.status;
      setOrder(data);
    }
  } catch (error) {
    console.error(error);
  }
};
  loadOrder();

  interval = setInterval(loadOrder, 3000); // every 5 sec

  return () => clearInterval(interval);
}, [orderNumber]);

  if (!order) return <PageLoader />;

  const isTerminatedEarly = ['cancelled', 'refunded'].includes(order.status);
  const currentStepIndex = TIMELINE_STEPS.indexOf(order.status);

  

  return (
    <>
      <Helmet><title>Order {order.order_number} | AFC - Ahmad Foods</title></Helmet>

      <Link to="/dashboard/orders" className="text-sm text-marigold-600 hover:underline">&larr; Back to orders</Link>

      <div className="mt-3 flex flex-wrap items-center justify-between gap-3">
        <h1 className="font-price text-xl font-bold text-ink-900">{order.order_number}</h1>
        <Badge variant={isTerminatedEarly ? 'danger' : 'marigold'} className="capitalize">
          {order.status.replaceAll('_', ' ')}
        </Badge>
      </div>

      {!isTerminatedEarly && (
        <ol className="mt-8 flex flex-wrap gap-y-6">
          {TIMELINE_STEPS.map((step, index) => {
            const isComplete = index <= currentStepIndex;
            return (
              <li key={step} className="flex min-w-[110px] flex-1 flex-col items-center gap-2 text-center">
                <span
                  className={`flex h-8 w-8 items-center justify-center rounded-full text-xs font-bold
                    ${isComplete ? 'bg-marigold-400 text-ink-900' : 'bg-ink-100 text-ink-400'}`}
                >
                  {isComplete ? <FiCheck className="h-4 w-4" /> : index + 1}
                </span>
                <span className={`text-xs capitalize ${isComplete ? 'font-semibold text-ink-800' : 'text-ink-400'}`}>
                  {step.replaceAll('_', ' ')}
                </span>
              </li>
            );
          })}
        </ol>
      )}

      <div className="mt-10 grid grid-cols-1 gap-6 lg:grid-cols-2">
        <div className="rounded-[var(--radius-card)] border border-ink-100 bg-white p-5">
          <h2 className="font-semibold text-ink-800">Items</h2>
          <ul className="mt-3 divide-y divide-ink-100">
            {order.items.map((item) => (
              <li key={item.id} className="flex justify-between py-2.5 text-sm">
                <span className="text-ink-600">{item.quantity} &times; {item.product_name}{item.variant_size ? ` (${item.variant_size})` : ''}</span>
                <span className="font-price text-ink-800">Rs {item.line_total}</span>
              </li>
            ))}
          </ul>
          <div className="mt-3 space-y-1 border-t border-ink-100 pt-3 text-sm">
            <div className="flex justify-between text-ink-500"><span>Subtotal</span><span className="font-price">Rs {order.subtotal}</span></div>
            {Number(order.discount_amount) > 0 && (
              <div className="flex justify-between text-success"><span>Discount ({order.coupon_code})</span><span className="font-price">-Rs {order.discount_amount}</span></div>
            )}
            <div className="flex justify-between font-semibold text-ink-900"><span>Total</span><span className="font-price">Rs {order.total_amount}</span></div>
          </div>
        </div>

        <div className="flex flex-col gap-6">
          <div className="rounded-[var(--radius-card)] border border-ink-100 bg-white p-5">
            <h2 className="font-semibold text-ink-800">Delivery Details</h2>
            <p className="mt-2 text-sm text-ink-600">{order.delivery_full_name}</p>
            <p className="text-sm text-ink-500">{order.delivery_phone}</p>
            <p className="text-sm text-ink-500">{order.delivery_address_line}, {order.delivery_city}</p>
            {order.notes && <p className="mt-2 text-xs text-ink-400">Note: {order.notes}</p>}
          </div>

          <div className="rounded-[var(--radius-card)] border border-ink-100 bg-white p-5">
            <h2 className="font-semibold text-ink-800">Status History</h2>
            <ul className="mt-3 flex flex-col gap-3">
              {order.status_history.map((entry, index) => (
                <li key={index} className="text-sm">
                  <span className="font-medium capitalize text-ink-700">{entry.status.replaceAll('_', ' ')}</span>
                  <span className="ml-2 text-xs text-ink-400">{new Date(entry.changed_at).toLocaleString()}</span>
                  {entry.note && <p className="text-xs text-ink-400">{entry.note}</p>}
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </>
  );
}
