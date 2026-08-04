import { Link, useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { FiHeart } from 'react-icons/fi';
import Badge from '@/components/ui/Badge';
import { useCart } from '@/hooks/useCart';
import { useWishlist } from '@/hooks/useWishlist';
import { useAuth } from '@/hooks/useAuth';
import { extractApiError } from '@/services/apiClient';

/** The single product card used across Home sections, Shop grid, and
 * related-products lists. */
export default function ProductCard({ product }) {
  const { addItem } = useCart();
  const { isWishlisted, addItem: addWish, items: wishItems, removeItem: removeWish } = useWishlist();
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const wishlisted = isWishlisted(product.id);

  

  async function handleToggleWishlist(event) {
    event.preventDefault();
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }
    try {
      if (wishlisted) {
        const existing = wishItems.find((item) => item.product === product.id);
        if (existing) await removeWish(existing.id);
      } else {
        await addWish(product.id);
      }
    } catch (error) {
      toast.error(extractApiError(error).message);
    }
  }

  return (
    <Link
      to={`/product/${product.slug}`}
      className="group flex flex-col overflow-hidden rounded-[var(--radius-card)] border border-ink-100 bg-white transition-shadow hover:shadow-[var(--shadow-card)]"
    >
      <div className="relative aspect-square overflow-hidden bg-ink-50">
        {product.primary_image ? (
          <img
            src={product.primary_image}
            alt={product.name}
            className="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"
            loading="lazy"
          />
        ) : (
          <div className="flex h-full w-full items-center justify-center text-ink-200">No image</div>
        )}

        <div className="absolute left-2 top-2 flex flex-col gap-1">
          {product.discount_percentage > 0 && <Badge variant="marigold">-{product.discount_percentage}%</Badge>}
          {product.is_trending && <Badge variant="ink">Trending</Badge>}
        </div>

        <button
          onClick={handleToggleWishlist}
          aria-label={wishlisted ? 'Remove from wishlist' : 'Add to wishlist'}
          className="absolute right-2 top-2 flex h-8 w-8 items-center justify-center rounded-full bg-white/90 text-ink-600 shadow-sm hover:text-danger"
        >
          <FiHeart className={wishlisted ? 'h-4 w-4 fill-danger text-danger' : 'h-4 w-4'} />
        </button>

        {!product.in_stock && (
          <div className="absolute inset-x-0 bottom-0 bg-ink-800/90 py-1.5 text-center text-xs font-semibold text-cream">
            Out of Stock
          </div>
        )}
      </div>

      <div className="flex flex-1 flex-col gap-1 p-3.5">
        <p className="text-xs font-medium uppercase tracking-wide text-marigold-600">{product.category}</p>
        <h3 className="line-clamp-2 text-sm font-semibold text-ink-800">{product.name}</h3>
        <div className="mt-auto flex items-center justify-between pt-2">
          <div className="flex items-baseline gap-1.5">
            <span className="font-price text-sm font-semibold text-ink-900">Rs {product.effective_price}</span>
            {product.discount_price && (
              <span className="font-price text-xs text-ink-300 line-through">Rs {product.price}</span>
            )}
          </div>
          
        </div>
      </div>
    </Link>
  );
}
