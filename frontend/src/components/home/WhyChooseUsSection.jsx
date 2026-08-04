import { FiClock, FiDollarSign, FiFeather, FiShield } from 'react-icons/fi';

const REASONS = [
  { icon: FiFeather, title: 'Fresh Ingredients', description: 'Sourced daily and baked fresh — never frozen, never rushed.' },
  { icon: FiClock, title: 'Fast Delivery', description: 'Freshly packed and delivered quickly within our delivery zone.' },
  { icon: FiShield, title: 'Best Quality', description: 'Every recipe is tested and perfected before it reaches your table.' },
  { icon: FiDollarSign, title: 'Affordable Price', description: 'Premium taste at prices that make celebrating easy.' },
];

export default function WhyChooseUsSection() {
  return (
    <section className="mx-auto max-w-7xl px-4 py-14 sm:px-6 lg:px-8">
      <div className="mb-8 text-center">
        <p className="text-xs font-semibold uppercase tracking-[0.16em] text-marigold-600">Why AFC</p>
        <h2 className="mt-1 text-2xl font-bold text-ink-900">Why Choose Us</h2>
      </div>
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {REASONS.map(({ icon: Icon, title, description }) => (
          <div key={title} className="flex flex-col items-center gap-3 text-center  border border-ink-50 rounded-[var(--radius-card)] p-6 shadow-sm hover:shadow-md transition-shadow">
            <span className="flex h-14 w-14 items-center justify-center rounded-full bg-marigold-50 text-marigold-600">
              <Icon className="h-6 w-6" />
            </span>
            <h3 className="font-semibold text-ink-900">{title}</h3>
            <p className="text-sm text-ink-500">{description}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
