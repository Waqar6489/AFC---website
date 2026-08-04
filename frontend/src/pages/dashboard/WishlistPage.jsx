import { Link } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';
import toast from 'react-hot-toast';
import { FiHeart, FiTrash2 } from 'react-icons/fi';
import { useWishlist } from '@/hooks/useWishlist';
import EmptyState from '@/components/ui/EmptyState';
import PageLoader from '@/components/ui/PageLoader';
import Button from '@/components/ui/Button';
import { extractApiError } from '@/services/apiClient';

export default function WishlistPage() {
  const { items, isLoading, removeItem } = useWishlist();

  async function handleRemove(id) {
    try {
      await removeItem(id);
    } catch (error) {
      toast.error(extractApiError(error).message);
    }
  }

  if (isLoading && items.length === 0) return <PageLoader />;

  return (
    <>
      <Helmet><title>Wishlist | AFC - Ahmad Foods</title></Helmet>
      <h1 className="text-2xl font-bold text-ink-900">Wishlist</h1>

      {items.length === 0 ? (
        <EmptyState
          icon={FiHeart}
          title="Your wishlist is empty"
          description="Save products you love to find them here later."
          action={<Button to="/shop" className="mt-2">Browse Shop</Button>}
          className="mt-6"
        />
      ) : (
        <ul className="mt-6 grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {items.map((item) => (
            <li key={item.id} className="flex gap-3 rounded-[var(--radius-card)] border border-ink-100 bg-white p-3">
              <div className="h-16 w-16 shrink-0 overflow-hidden rounded-[var(--radius-card)] bg-ink-50">
                {item.product_image && <img src={item.product_image} alt={item.product_name} className="h-full w-full object-cover" />}
              </div>
              <div className="flex flex-1 flex-col justify-between">
                <Link to={`/product/${item.product_slug}`} className="text-sm font-semibold text-ink-800 hover:text-marigold-600">
                  {item.product_name}
                </Link>
                <div className="flex items-center justify-between">
                  <span className="font-price text-sm text-ink-700">Rs {item.product_price}</span>
                  <button onClick={() => handleRemove(item.id)} aria-label="Remove from wishlist" className="text-ink-300 hover:text-danger">
                    <FiTrash2 className="h-4 w-4" />
                  </button>
                </div>
              </div>
            </li>
          ))}
        </ul>
      )}
    </>
  );
}
