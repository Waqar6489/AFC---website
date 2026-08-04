import { Helmet } from 'react-helmet-async';
import Button from '@/components/ui/Button';

export default function NotFoundPage() {
  return (
    <>
      <Helmet><title>Page Not Found | AFC - Ahmad Foods</title></Helmet>
      <div className="flex min-h-[60vh] flex-col items-center justify-center px-4 text-center">
        <p className="font-price text-6xl font-bold text-marigold-400">404</p>
        <h1 className="mt-3 text-2xl font-bold text-ink-900">Page not found</h1>
        <p className="mt-2 max-w-sm text-ink-500">
          The page you’re looking for doesn’t exist or may have moved.
        </p>
        <Button to="/" className="mt-6">Back to Home</Button>
      </div>
    </>
  );
}
