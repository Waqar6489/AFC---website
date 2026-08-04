import ProductCard from '@/components/product/ProductCard';

export default function ProductGrid({ products, columns = 4 }) {
  const colsClass = {
    3: 'sm:grid-cols-2 lg:grid-cols-3',
    4: 'sm:grid-cols-2 lg:grid-cols-4',
  }[columns];

  return (
    <div className={`grid grid-cols-2 gap-4 ${colsClass}`}>
      {products.map((product) => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  );
}
