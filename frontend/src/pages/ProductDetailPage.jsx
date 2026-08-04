import { useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';
import toast from 'react-hot-toast';
import { FiHeart, FiMinus, FiPlus } from 'react-icons/fi';
import { productService } from '@/services/productService';
import { reviewService } from '@/services/reviewService';
import { useCart } from '@/hooks/useCart';
import { useWishlist } from '@/hooks/useWishlist';
import { useAuth } from '@/hooks/useAuth';
import Button from '@/components/ui/Button';
import Badge from '@/components/ui/Badge';
import PageLoader from '@/components/ui/PageLoader';
import StarRating from '@/components/common/StarRating';
import ProductGrid from '@/components/product/ProductGrid';
import ReviewForm from '@/components/product/ReviewForm';
import ReviewList from '@/components/product/ReviewList';
import { extractApiError } from '@/services/apiClient';

const TABS = ['Description', 'Ingredients', 'Nutrition', 'Reviews'];

export default function ProductDetailPage() {
  const { slug } = useParams();
  const [product, setProduct] = useState(null);
  const [notFound, setNotFound] = useState(false);
  const [activeImage, setActiveImage] = useState(0);
  const [selectedVariant, setSelectedVariant] = useState(null);
  const [selectedAddons, setSelectedAddons] = useState([]);
  const [quantity, setQuantity] = useState(1);
  const [activeTab, setActiveTab] = useState('Description');
  const [reviews, setReviews] = useState([]);

  const { addItem } = useCart();
  const { isWishlisted, addItem: addWish, items: wishItems, removeItem: removeWish } = useWishlist();
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    productService
      .retrieve(slug)
      .then((data) => {
        setProduct(data);
        if (data.variants?.length > 0) setSelectedVariant(data.variants[0].id);
      })
      .catch(() => setNotFound(true));
  }, [slug]);

  function refreshReviews(productId) {
    reviewService.list({ product: productId }).then((data) => setReviews((data.results ?? data).filter((r) => r.is_approved)));
  }

  useEffect(() => {
    if (product) refreshReviews(product.id);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [product?.id]);

  if (notFound) return <ProductNotFound />;
  if (!product) return <PageLoader />;

  const variant = product.variants.find((v) => v.id === selectedVariant);
  const basePrice = variant ? Number(variant.price) : Number(product.effective_price);
  const addonsTotal = selectedAddons.reduce((sum, id) => {
    const addon = product.available_addons.find((a) => a.id === id);
    return sum + (addon ? Number(addon.price) : 0);
  }, 0);
  const unitPrice = basePrice + addonsTotal;
  const wishlisted = isWishlisted(product.id);

  function toggleAddon(id) {
    setSelectedAddons((prev) => (prev.includes(id) ? prev.filter((a) => a !== id) : [...prev, id]));
  }

  async function handleAddToCart() {
    if (!isAuthenticated) {
      navigate('/login', { state: { from: { pathname: `/product/${slug}` } } });
      return;
    }
    try {
      await addItem({
        product: product.id,
        variant: selectedVariant || undefined,
        addons: selectedAddons,
        quantity,
      });
      toast.success('Added to cart!');
    } catch (error) {
      toast.error(extractApiError(error).message);
    }
  }

  async function handleToggleWishlist() {
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
    <>
      <Helmet><title>{product.name} | AFC - Ahmad Foods</title></Helmet>
      <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 gap-10 md:grid-cols-2">
          <div>
            <div className="aspect-square overflow-hidden rounded-[var(--radius-card)] bg-ink-50">
              {product.images?.[activeImage] && (
                <img src={product.images[activeImage]} alt={product.name} className="h-full w-full object-cover" />
              )}
            </div>
            {product.images?.length > 1 && (
              <div className="mt-3 flex gap-2">
                {product.images.map((image, index) => (
                  <button
                    key={image.id}
                    onClick={() => setActiveImage(index)}
                    className={`h-16 w-16 cursor-pointer overflow-hidden rounded-[var(--radius-card)] border-2 ${index === activeImage ? 'border-marigold-400' : 'border-transparent'}`}
                  >
                    <img src={image} alt="" className="h-full w-full object-cover" />
                  </button>
                ))}
              </div>
            )}
          </div>

          <div>
            <p className="text-xs font-semibold uppercase tracking-wider text-marigold-600">{product.category?.name}</p>
            <h1 className="mt-1 text-2xl font-bold text-ink-900">{product.name}</h1>

            <div className="mt-2 flex items-center gap-3">
              <StarRating value={product.average_rating} />
              <span className="text-xs text-ink-400">({product.review_count} reviews)</span>
              {product.discount_percentage > 0 && <Badge>-{product.discount_percentage}%</Badge>}
            </div>

            <p className="font-price mt-4 text-2xl font-semibold text-ink-800">Rs {unitPrice.toFixed(2)}</p>
            <p className="mt-2 text-ink-600">{product.short_description}</p>

            {product.variants.length > 0 && (
              <div className="mt-5">
                <p className="mb-2 text-sm font-medium text-ink-700">Size</p>
                <div className="flex flex-wrap gap-2">
                  {product.variants.map((v) => (
                    <button
                      key={v.id}
                      onClick={() => setSelectedVariant(v.id)}
                      className={`rounded-full border px-4 py-1.5 text-sm capitalize cursor-pointer
                        ${selectedVariant === v.id ? 'border-ink-800 bg-ink-800 text-cream' : 'border-ink-200 text-ink-600 hover:border-ink-400'}`}
                    >
                      {v.size.replace('_', ' ')} &middot; Rs {v.price}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {product.available_addons.length > 0 && (
              <div className="mt-5">
                <p className="mb-2 text-sm font-medium text-ink-700">Add-ons</p>
                <div className="flex flex-col gap-2">
                  {product.available_addons.map((addon) => (
                    <label key={addon.id} className="flex items-center justify-between rounded-md border border-ink-100 px-3 py-2 text-sm">
                      <span className="flex items-center gap-2 cursor-pointer">
                        <input type="checkbox"  className='cursor-pointer' checked={selectedAddons.includes(addon.id)} onChange={() => toggleAddon(addon.id)} />
                        {addon.name}
                      </span>
                      <span className="font-price text-ink-500">+Rs {addon.price}</span>
                    </label>
                  ))}
                </div>
              </div>
            )}

            <div className="mt-6 flex items-center gap-3">
              <div className="flex items-center rounded-full border border-ink-200">
                <button onClick={() => setQuantity((q) => Math.max(1, q - 1))} className="flex h-10 w-10 items-center justify-center text-ink-500 cursor-pointer" aria-label="Decrease quantity">
                  <FiMinus className="h-4 w-4"  />
                </button>
                <span className="w-8 text-center font-medium">{quantity}</span>
                <button onClick={() => setQuantity((q) => q + 1)} className="flex h-10 w-10 items-center justify-center text-ink-500 cursor-pointer" aria-label="Increase quantity">
                  <FiPlus className="h-4 w-4" />
                </button>
              </div>
              <Button onClick={handleAddToCart} disabled={!product.in_stock} className="flex-1 cursor-pointer">
                {product.in_stock ? 'Add to Cart' : 'Out of Stock'}
              </Button>
              <button
                onClick={handleToggleWishlist}
                aria-label="Toggle wishlist"
                className="flex h-11 w-11 cursor-pointer items-center justify-center rounded-full border border-ink-200 text-ink-500 hover:text-danger"
              >
                <FiHeart className={wishlisted ? 'h-5 w-5 fill-danger text-danger' : 'h-5 w-5'} />
              </button>
            </div>
          </div>
        </div>

        <div className="mt-14">
          <div className="flex gap-6 border-b border-ink-100">
            {TABS.map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`border-b-2 pb-3 text-sm font-medium cursor-pointer ${activeTab === tab ? 'border-marigold-400 text-ink-900' : 'border-transparent text-ink-400'}`}
              >
                {tab}
              </button>
            ))}
          </div>

          <div className="py-6 ">
            {activeTab === 'Description' && <p className="max-w-2xl text-sm leading-relaxed text-ink-600 ">{product.description}</p>}
            {activeTab === 'Ingredients' && (
              <p className="max-w-2xl text-sm leading-relaxed text-ink-600">{product.ingredients || 'Ingredient information not available.'}</p>
            )}
            {activeTab === 'Nutrition' && <NutritionTable nutrition={product.nutrition} />}
            {activeTab === 'Reviews' && (
              <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
                <ReviewList reviews={reviews} />
                {isAuthenticated && <ReviewForm productId={product.id} onSubmitted={() => refreshReviews(product.id)} />}
              </div>
            )}
          </div>
        </div>

        {product.frequently_bought_with?.length > 0 && (
          <div className="mt-14">
            <h2 className="mb-5 text-xl font-bold text-ink-900">Frequently Bought Together</h2>
            <ProductGrid products={product.frequently_bought_with} />
          </div>
        )}

        {product.related_products?.length > 0 && (
          <div className="mt-14">
            <h2 className="mb-5 text-xl font-bold text-ink-900">Related Products</h2>
            <ProductGrid products={product.related_products} />
          </div>
        )}
      </div>
    </>
  );
}

function NutritionTable({ nutrition }) {
  const rows = [
    ['Calories', nutrition?.calories, ''],
    ['Protein', nutrition?.protein_g, 'g'],
    ['Carbohydrates', nutrition?.carbs_g, 'g'],
    ['Fat', nutrition?.fat_g, 'g'],
    ['Sugar', nutrition?.sugar_g, 'g'],
  ].filter(([, value]) => value !== null && value !== undefined);

  if (rows.length === 0) return <p className="text-sm text-ink-400">Nutrition information not available.</p>;

  return (
    <table className="w-full max-w-sm text-sm">
      <tbody className="divide-y divide-ink-100">
        {rows.map(([label, value, unit]) => (
          <tr key={label}>
            <td className="py-2 text-ink-500">{label}</td>
            <td className="font-price py-2 text-right font-semibold text-ink-800">{value}{unit}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

function ProductNotFound() {
  return (
    <div className="mx-auto max-w-xl px-4 py-24 text-center">
      <h1 className="text-xl font-bold text-ink-900">Product not found</h1>
      <p className="mt-2 text-ink-500">This product may have been removed or is no longer available.</p>
      <Link to="/shop" className="mt-4 inline-block text-marigold-600 hover:underline">Back to Shop</Link>
    </div>
  );
}
