import { useEffect, useState } from 'react';
import SectionHeading from '@/components/home/SectionHeading';
import ProductGrid from '@/components/product/ProductGrid';

/** Generic "row of products" section — reused for Trending, Best
 * Selling, and Featured, each just passing a different fetcher. */
export default function ProductsSection({ eyebrow, title, fetcher }) {
  const [products, setProducts] = useState(null);

  useEffect(() => {
    fetcher({ page_size: 8 }).then((data) => setProducts(data.results ?? data));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  if (products !== null && products.length === 0) return null;

  return (
    <section className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
      <SectionHeading eyebrow={eyebrow} title={title} viewAllTo="/shop" />
      {products === null ? (
        <div className="grid grid-cols-2 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {Array.from({ length: 4 }).map((_, i) => <div key={i} className="aspect-[3/4] animate-pulse rounded-[var(--radius-card)] bg-ink-100" />)}
        </div>
      ) : (
        <ProductGrid products={products} />
      )}
    </section>
  );
}
