import { useEffect, useState } from 'react';
import { useForm } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';
import toast from 'react-hot-toast';
import { FiAlertTriangle, FiCheckCircle, FiMapPin, FiTruck } from 'react-icons/fi';
import { useCart } from '@/hooks/useCart';
import Input from '@/components/ui/Input';
import Button from '@/components/ui/Button';
import PageLoader from '@/components/ui/PageLoader';
import { orderService } from '@/services/orderService';
import { extractApiError } from '@/services/apiClient';

const GEO_STATE = { IDLE: 'idle', LOCATING: 'locating', DENIED: 'denied', CHECKING: 'checking', ELIGIBLE: 'eligible', INELIGIBLE: 'ineligible' };

export default function CheckoutPage() {
  const { cart, isLoading: isCartLoading, refreshCart } = useCart();
  const navigate = useNavigate();
  const [geoState, setGeoState] = useState(GEO_STATE.IDLE);
  const [coords, setCoords] = useState(null);
  const [eligibilityMessage, setEligibilityMessage] = useState('');
  const [deliveryFee, setDeliveryFee] = useState(0);
  const [distanceKm, setDistanceKm] = useState(0);

  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm();

  function requestLocation() {
    if (!navigator.geolocation) {
      setGeoState(GEO_STATE.DENIED);
      setEligibilityMessage('Your browser does not support location detection.');
      return;
    }
    setGeoState(GEO_STATE.LOCATING);
    navigator.geolocation.getCurrentPosition(
      async ({ coords: position }) => {
        const point = { latitude: position.latitude.toFixed(6), longitude: position.longitude.toFixed(6) };
        setCoords(point);
        setGeoState(GEO_STATE.CHECKING);
        try {
          const result = await orderService.checkDelivery(point);
          setGeoState(result.data.is_within_radius ? GEO_STATE.ELIGIBLE : GEO_STATE.INELIGIBLE);
          setEligibilityMessage(
            result.data.is_within_radius
              ? `You're within our ${result.data.delivery_radius_km} KM delivery area (${result.data.distance_km} KM away).`
              : result.message,
          );
          const distance = Number(result.data.distance_km);
          setDistanceKm(distance);

          const subtotal = Number(cart.subtotal);

          if (subtotal >= 2000) {
            setDeliveryFee(0);
          } else {
            setDeliveryFee(distance * 30);
          }
        } catch {
          setGeoState(GEO_STATE.DENIED);
          setEligibilityMessage('Could not verify delivery eligibility. Please try again.');

        }
      },
      () => {
        setGeoState(GEO_STATE.DENIED);
        setEligibilityMessage('Location access was denied. We need your location to confirm we deliver to you.');
      },
    );
  }

  useEffect(() => {
    requestLocation();
  }, []);

  async function onSubmit(values) {
    if (geoState !== GEO_STATE.ELIGIBLE || !coords) {
      toast.error('We need to confirm your delivery location before you can check out.');
      return;
    }
    try {
      const response = await orderService.checkout({
        ...values,
        latitude: coords.latitude,
        longitude: coords.longitude,
      });
      toast.success('Order placed successfully!');
      await refreshCart();
      navigate(`/dashboard/orders/${response.data.order_number}`);
    } catch (error) {
      toast.error(extractApiError(error).message);
    }
  }

  if (isCartLoading) return <PageLoader />;

  return (
    <>
      <Helmet><title>Checkout | AFC - Ahmad Foods</title></Helmet>
      <div className="mx-auto max-w-4xl px-4 py-10 sm:px-6 lg:px-8">
        <h1 className="text-2xl font-bold text-ink-900">Checkout</h1>

        <DeliveryStatusBanner state={geoState} message={eligibilityMessage} onRetry={requestLocation} />

        {cart.items.length === 0 ? (
          <p className="mt-6 text-ink-500">Your cart is empty. Add something delicious before checking out.</p>
        ) : (
          <form onSubmit={handleSubmit(onSubmit)} className="mt-8 grid grid-cols-1 gap-8 lg:grid-cols-[1fr_320px]" noValidate>
            <div className="flex flex-col gap-4 rounded-[var(--radius-card)] border border-ink-100 bg-white p-6">
              <h2 className="font-semibold text-ink-800">Delivery Details</h2>
              <div className="grid grid-cols-2 gap-3">
                <Input label="Full name" error={errors.full_name?.message} {...register('full_name', { required: 'Required' })} />
                <Input label="Phone" type="tel" placeholder="+923001234567" error={errors.phone?.message} {...register('phone', { required: 'Required' })} />
              </div>
              <Input label="Address line" error={errors.address_line?.message} {...register('address_line', { required: 'Required' })} />
              <Input label="City" error={errors.city?.message} {...register('city', { required: 'Required' })} />
              <Input label="Coupon code (optional)" {...register('coupon_code')} />
              <div className="flex flex-col gap-1.5">
                <label htmlFor="notes" className="text-sm font-medium text-ink-700">Order notes (optional)</label>
                <textarea
                  id="notes"
                  rows={3}
                  className="rounded-[var(--radius-card)] border border-ink-200 bg-cream px-3.5 py-2.5 text-sm focus:border-marigold-400"
                  {...register('notes')}
                />
              </div>
              <div>
                <p className="mb-1.5 text-sm font-medium text-ink-700">Payment Method</p>
                <label className="flex items-center gap-2 text-sm text-ink-600">
                  <input type="radio" value="cod" defaultChecked {...register('payment_method')} /> Cash on Delivery
                </label>
              </div>
            </div>

            <div className="h-fit rounded-[var(--radius-card)] border border-ink-100 bg-white p-5">
              <h2 className="font-semibold text-ink-800">Order Summary</h2>
              <ul className="mt-3 flex flex-col gap-2 text-sm text-ink-600">
                {cart.items.map((item) => (
                  <li key={item.id} className="flex justify-between">
                    <span>{item.quantity} &times; {item.product_name}</span>
                    <span className="font-price">Rs {item.line_total}</span>
                  </li>
                ))}
              </ul>
              <div className="mt-2 flex justify-between text-sm text-ink-700">
                <span>Distance</span>
                <span>{distanceKm.toFixed(2)} KM</span>
              </div>

              <div className="mt-2 flex justify-between text-sm text-ink-700">
                <span>Delivery</span>
                <span className="font-price">
                  {deliveryFee === 0 ? (
                    <span className="text-green-600 font-semibold">FREE</span>
                  ) : (
                    `Rs ${deliveryFee.toFixed(0)}`
                  )}
                </span>
              </div>

              <div className="mt-3 flex justify-between border-t pt-3 text-base font-bold">
                <span>Total</span>
                <span className="font-price">
                  Rs {(Number(cart.subtotal) + deliveryFee).toFixed(0)}
                </span>
              </div>
              <Button
                type="submit"
                isLoading={isSubmitting}
                disabled={geoState !== GEO_STATE.ELIGIBLE}
                className="mt-5 w-full"
              >
                Place Order
              </Button>
            </div>
            
          </form>
        )}
      </div>
    </>
  );
}

function DeliveryStatusBanner({ state, message, onRetry }) {
  if (state === GEO_STATE.IDLE || state === GEO_STATE.LOCATING || state === GEO_STATE.CHECKING) {
    return (
      <div className="mt-6 flex items-center gap-2.5 rounded-[var(--radius-card)] border border-ink-200 bg-ink-50 px-4 py-3 text-sm text-ink-600">
        <FiMapPin className="h-4 w-4 shrink-0 animate-pulse" /> Checking your delivery eligibility...
      </div>
    );
  }
  if (state === GEO_STATE.ELIGIBLE) {
    return (
      <div className="mt-6 flex items-center gap-2.5 rounded-[var(--radius-card)] border border-success/30 bg-success/10 px-4 py-3 text-sm text-success">
        <FiCheckCircle className="h-4 w-4 shrink-0" /> {message}
      </div>
    );
  }
  return (
    <div className="mt-6 flex flex-wrap items-center gap-2.5 rounded-[var(--radius-card)] border border-danger/30 bg-danger/10 px-4 py-3 text-sm text-danger">
      <FiAlertTriangle className="h-4 w-4 shrink-0" />
      <span className="flex-1">{message}</span>
      <button onClick={onRetry} className="font-semibold underline">Try again</button>
    </div>
  );
}
