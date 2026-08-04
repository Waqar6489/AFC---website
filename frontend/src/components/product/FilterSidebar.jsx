import { useEffect, useState } from 'react';
import { categoryService } from '@/services/categoryService';

export default function FilterSidebar({ filters, onChange }) {
  const [categories, setCategories] = useState([]);
  const [priceRange, setPriceRange] = useState({ min: filters.min_price || '', max: filters.max_price || '' });

  useEffect(() => {
    categoryService.list({ ordering: 'order' }).then((data) => setCategories(data.results ?? data));
  }, []);

  function applyPriceRange() {
    onChange({ min_price: priceRange.min || undefined, max_price: priceRange.max || undefined });
  }

  return (
    <aside className="flex flex-col gap-6">
      <FilterGroup title="Category">
        <label className="flex items-center gap-2 text-sm text-ink-600 cursor-pointer">
          <input
            type="radio"
            name="category"
            checked={!filters.category}
            onChange={() => onChange({ category: undefined })}
          />
          All Categories
        </label>
        {categories.map((category) => (
          <label key={category.id} className="flex items-center gap-2 text-sm text-ink-600 cursor-pointer">
            <input
              type="radio"
              name="category"
              className='cursor-pointer'
              checked={filters.category === category.slug}
              onChange={() => onChange({ category: category.slug })}
            />
            {category.name}
          </label>
        ))}
      </FilterGroup>

      <FilterGroup title="Price Range">
        <div className="flex items-center gap-2 cursor-pointer">
          <input
            type="number"
            placeholder="Min"
            value={priceRange.min}
            onChange={(e) => setPriceRange((p) => ({ ...p, min: e.target.value }))}
            className="h-9 w-full rounded-md border border-ink-200 px-2 text-sm"
          />
          <span className="text-ink-300">–</span>
          <input
            type="number"
            placeholder="Max"
            value={priceRange.max}
            onChange={(e) => setPriceRange((p) => ({ ...p, max: e.target.value }))}
            className="h-9 w-full rounded-md border border-ink-200 px-2 text-sm"
          />
        </div>
        <button onClick={applyPriceRange} className="mt-2 self-start cursor-pointer text-xs font-semibold text-marigold-600 hover:underline">
          Apply
        </button>
      </FilterGroup>

      <FilterGroup title="Discount">
        <label className="flex items-center gap-2 text-sm text-ink-600 cursor-pointer">
          <input
            type="checkbox"
            className="cursor-pointer"
            checked={filters.on_deal === 'true'}
            onChange={(e) => onChange({ on_deal: e.target.checked ? 'true' : undefined })}
          />
          On Discount Only
        </label>
      </FilterGroup>

      <FilterGroup title="Availability">
        <label className="flex items-center gap-2 text-sm text-ink-600 cursor-pointer">
          <input
            type="checkbox"
            className="cursor-pointer"
            checked={filters.in_stock === 'true'}
            onChange={(e) => onChange({ in_stock: e.target.checked ? 'true' : undefined })}
          />
          In Stock Only
        </label>
      </FilterGroup>
    </aside>
  );
}

function FilterGroup({ title, children }) {
  return (
    <div className="border-b border-ink-100 pb-5">
      <h3 className="mb-2.5 text-sm font-semibold text-ink-900">{title}</h3>
      <div className="flex flex-col gap-2">{children}</div>
    </div>
  );
}
