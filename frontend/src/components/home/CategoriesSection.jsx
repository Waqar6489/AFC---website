import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { categoryService } from '@/services/categoryService';
import SectionHeading from '@/components/home/SectionHeading';

export default function CategoriesSection() {
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    categoryService.list({ ordering: 'order' }).then((data) => setCategories(data.results ?? data));
  }, []);

  if (categories.length === 0) return null;

  return (
    <section className="mx-auto max-w-7xl px-4 py-14 sm:px-6 lg:px-8">
      <SectionHeading eyebrow="Browse" title="Shop by Category" />
      <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-6">
        {categories.map((category) => (
          <Link
            key={category.id}
            to={`/shop?category=${category.slug}`}
            className="group flex flex-col items-center gap-2.5 rounded-[var(--radius-card)] border border-ink-100 bg-white p-4 text-center transition-shadow hover:shadow-[var(--shadow-card)]"
          >
            <div className="h-30 w-30 overflow-hidden rounded-full bg-ink-50">
              {category.image && (
                <img src={category.image} alt={category.name} className="h-full w-full object-cover transition-transform group-hover:scale-110" />
              )}
            </div>
            <span className="text-sm font-medium text-ink-700">{category.name}</span>
          </Link>
        ))}
      </div>
    </section>
  );
}
