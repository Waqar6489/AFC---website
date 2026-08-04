import { Link } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';
import toast from 'react-hot-toast';
import { FiMinus, FiPlus, FiShoppingBag, FiTrash2 } from 'react-icons/fi';
import { useCart } from '@/hooks/useCart';
import { useAuth } from '@/hooks/useAuth';
import Button from '@/components/ui/Button';
import EmptyState from '@/components/ui/EmptyState';
import PageLoader from '@/components/ui/PageLoader';
import { extractApiError } from '@/services/apiClient';

export default function CartPage() {
  
  const { isAuthenticated } = useAuth();
  const { cart, isLoading, updateItem, removeItem } = useCart();

  async function handleQuantityChange(item, delta) {
    const nextQuantity = item.quantity + delta;
    if (nextQuantity < 1) return;
    try {
      await updateItem(item.id, { quantity: nextQuantity });
    } catch (error) {
      toast.error(extractApiError(error).message);
    }
  }

  async function handleRemove(item) {
    try {
      await removeItem(item.id);
      toast.success('Removed from cart.');
    } catch (error) {
      toast.error(extractApiError(error).message);
    }
  }

  return (
    <>
      <Helmet><title>Your Cart | AFC - Ahmad Foods</title></Helmet>
      <div className="mx-auto max-w-5xl px-4 py-10 sm:px-6 lg:px-8">
        <div className="mt-4 rounded-lg border border-amber-200 bg-amber-50 p-4">
              <h3 className="font-semibold text-amber-800">Delivery Information</h3>

              <ul className="mt-2 space-y-1 text-sm text-amber-700">
                <li>🚚 Free delivery on orders of <strong>Rs. 2,000 or above</strong>.</li>
                <li>📍 Orders below <strong>Rs. 2,000</strong> will be delivery charged <strong>Rs. 30 per KM</strong>.</li>
                <li>🛵 We currently deliver within a <strong>10 KM radius</strong> of our restaurant.</li>
                <li>⏰ Orders are accepted daily from <strong>8:00 AM to 11:00 PM</strong>.</li>
              </ul>
            </div>
        <h1 className="text-2xl font-bold text-ink-900">Your Cart</h1>

        {!isAuthenticated ? (
          <EmptyState
            icon={FiShoppingBag}
            title="Log in to view your cart"
            description="Create an account or log in to add items to your cart and check out."
            action={<Button to="/login" className="mt-2">Log In</Button>}
          />
        ) : isLoading ? (
          <PageLoader />
        ) : cart.items.length === 0 ? (
          <EmptyState
            icon={FiShoppingBag}
            title="Your cart is empty"
            description="Browse our menu and add something delicious."
            action={<Button to="/shop" className="mt-2">Go to Shop</Button>}
          />
        ) : (
          <div className="mt-8 grid grid-cols-1 gap-8 lg:grid-cols-[1fr_320px]">
            <ul className="flex flex-col divide-y divide-ink-100 rounded-[var(--radius-card)] border border-ink-100 bg-white">
              {cart.items.map((item) => (
                <li key={item.id} className="flex gap-4 p-4">
                  <div className="h-20 w-20 shrink-0 overflow-hidden rounded-[var(--radius-card)] bg-ink-50">
                    {item.product_image && (
                      <img src={item.product_image} alt={item.product_name} className="h-full w-full object-cover" />
                    )}
                  </div>
                  <div className="flex flex-1 flex-col gap-1">
                    <Link to={`/product/${item.product_slug}`} className="font-semibold text-ink-800 hover:text-marigold-600">
                      {item.product_name}
                    </Link>
                    {item.variant_size && <p className="text-xs capitalize text-ink-400">{item.variant_size}</p>}
                    {item.addon_details?.length > 0 && (
                      <p className="text-xs text-ink-400">+ {item.addon_details.map((a) => a.name).join(', ')}</p>
                    )}
                    <div className="mt-1 flex items-center gap-3">
                      <div className="flex items-center rounded-full border border-ink-200">
                        <button
                          onClick={() => handleQuantityChange(item, -1)}
                          className="flex h-7 w-7 items-center justify-center text-ink-500 hover:text-ink-900"
                          aria-label="Decrease quantity"
                        >
                          <FiMinus className="h-3 w-3" />
                        </button>
                        <span className="w-6 text-center text-sm font-medium">{item.quantity}</span>
                        <button
                          onClick={() => handleQuantityChange(item, 1)}
                          className="flex h-7 w-7 items-center justify-center text-ink-500 hover:text-ink-900"
                          aria-label="Increase quantity"
                        >
                          <FiPlus className="h-3 w-3" />
                        </button>
                      </div>
                      <button
                        onClick={() => handleRemove(item)}
                        className="flex items-center gap-1 text-xs font-medium text-danger hover:underline"
                      >
                        <FiTrash2 className="h-3.5 w-3.5" /> Remove
                      </button>
                    </div>
                  </div>
                  <p className="font-price text-sm font-semibold text-ink-800">Rs {item.line_total}</p>
                </li>
              ))}
            </ul>

            <div className="h-fit rounded-[var(--radius-card)] border border-ink-100 bg-white p-5">
              <h2 className="font-semibold text-ink-800">Order Summary</h2>
              <div className="mt-4 flex justify-between text-sm text-ink-500">
                <span>Subtotal</span>
                <span className="font-price">Rs {cart.subtotal}</span>
              </div>
              <p className="mt-1 text-xs text-ink-400">Delivery fee and any coupon discount are calculated at checkout.</p>
              <Button to="/checkout" className="mt-5 w-full">Proceed to Checkout</Button>
            </div>
          </div>
        )}
      </div>
    </>
  );
}
