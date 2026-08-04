import { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';
import { FiGrid, FiList, FiSearch } from 'react-icons/fi';
import { productService } from '@/services/productService';
import PageHeader from '@/components/common/PageHeader';
import FilterSidebar from '@/components/product/FilterSidebar';
import ProductGrid from '@/components/product/ProductGrid';
import ProductCard from '@/components/product/ProductCard';
import Pagination from '@/components/ui/Pagination';
import PageLoader from '@/components/ui/PageLoader';
import EmptyState from '@/components/ui/EmptyState';

const SORT_OPTIONS = [
  { value: '', label: 'Newest' },
  { value: 'price', label: 'Price: Low to High' },
  { value: '-price', label: 'Price: High to Low' },
  { value: '-average_rating', label: 'Top Rated' },
  { value: 'name', label: 'Name: A-Z' },
];

export default function ShopPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [products, setProducts] = useState(null);
  const [pageInfo, setPageInfo] = useState({ count: 0, totalPages: 1 });
  const [viewMode, setViewMode] = useState('grid');

  const currentPage = Number(searchParams.get('page') || 1);
  const filters = Object.fromEntries(searchParams.entries());

  useEffect(() => {
    setProducts(null);
    const params = { ...filters, page: currentPage };
    productService.list(params).then((data) => {
      setProducts(data.results ?? data);
      setPageInfo({ count: data.count ?? data.length, totalPages: data.total_pages ?? 1 });
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [searchParams]);

  function updateFilters(patch) {
    const next = new URLSearchParams(searchParams);
    Object.entries(patch).forEach(([key, value]) => {
      if (value === undefined || value === '') next.delete(key);
      else next.set(key, value);
    });
    next.delete('page');
    setSearchParams(next);
  }

  function goToPage(page) {
    const next = new URLSearchParams(searchParams);
    next.set('page', page);
    setSearchParams(next);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  return (
    <>
      <Helmet><title>Shop | AFC - Ahmad Foods</title></Helmet>
      <PageHeader eyebrow="Menu" title="Shop" description="Browse our full range of cakes, pastries, and sweets." />

      <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
        {filters.search && (
          <div className="mb-6 flex items-center gap-2 text-sm text-ink-500">
            <FiSearch className="h-4 w-4" /> Showing results for <span className="font-semibold text-ink-800">&ldquo;{filters.search}&rdquo;</span>
          </div>
        )}

        <div className="grid grid-cols-1 gap-8 lg:grid-cols-[240px_1fr]">
          <FilterSidebar filters={filters} onChange={updateFilters} />

          <div>
            <div className="mb-5 flex flex-wrap items-center justify-between gap-3">
              <p className="text-sm text-ink-400">{pageInfo.count} products</p>
              <div className="flex items-center gap-3">
                <select
                  value={filters.ordering || ''}
                  onChange={(e) => updateFilters({ ordering: e.target.value || undefined })}
                  className="h-9 rounded-md border border-ink-200 px-2.5 text-sm cursor-pointer"
                >
                  {SORT_OPTIONS.map((opt) => <option key={opt.value} value={opt.value}>{opt.label}</option>)}
                </select>
                <div className="flex overflow-hidden rounded-md border border-ink-200">
                  <button
                    onClick={() => setViewMode('grid')}
                    className={`flex h-9 w-9 cursor-pointer items-center justify-center ${viewMode === 'grid' ? 'bg-ink-800 text-cream' : 'text-ink-500'}`}
                    aria-label="Grid view"
                  >
                    <FiGrid className="h-4 w-4 " />
                  </button>
                  <button
                    onClick={() => setViewMode('list')}
                    className={`flex h-9 w-9 cursor-pointer items-center justify-center ${viewMode === 'list' ? 'bg-ink-800 text-cream' : 'text-ink-500'}`}
                    aria-label="List view"
                  >
                    <FiList className="h-4 w-4" />
                  </button>
                </div>
              </div>
            </div>

            {products === null ? (
              <PageLoader />
            ) : products.length === 0 ? (
              <EmptyState title="No products found" description="Try adjusting your filters or search term." />
            ) : viewMode === 'grid' ? (
              <ProductGrid products={products} />
            ) : (
              <div className="flex flex-col gap-3">
                {products.map((product) => (
                  <div key={product.id} className="max-w-xs">
                    <ProductCard product={product} />
                  </div>
                ))}
              </div>
            )}

            <Pagination currentPage={currentPage} totalPages={pageInfo.totalPages} onPageChange={goToPage} />
          </div>
        </div>
      </div>
    </>
  );
}
