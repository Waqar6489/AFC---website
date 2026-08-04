import { FiChevronLeft, FiChevronRight } from 'react-icons/fi';

export default function Pagination({ currentPage, totalPages, onPageChange }) {
  if (totalPages <= 1) return null;

  const pages = Array.from({ length: totalPages }, (_, i) => i + 1).filter(
    (page) => page === 1 || page === totalPages || Math.abs(page - currentPage) <= 1,
  );

  return (
    <nav className="mt-10 flex items-center justify-center gap-1.5" aria-label="Pagination">
      <button
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage === 1}
        className="flex h-9 w-9 items-center justify-center rounded-full text-ink-500 hover:bg-ink-100 disabled:opacity-30"
        aria-label="Previous page"
      >
        <FiChevronLeft className="h-4 w-4" />
      </button>

      {pages.map((page, index) => (
        <span key={page} className="flex items-center">
          {index > 0 && pages[index - 1] !== page - 1 && <span className="px-1 text-ink-300">&hellip;</span>}
          <button
            onClick={() => onPageChange(page)}
            className={`flex h-9 w-9 items-center justify-center rounded-full text-sm font-medium
              ${page === currentPage ? 'bg-ink-800 text-cream' : 'text-ink-600 hover:bg-ink-100'}`}
          >
            {page}
          </button>
        </span>
      ))}

      <button
        onClick={() => onPageChange(currentPage + 1)}
        disabled={currentPage === totalPages}
        className="flex h-9 w-9 items-center justify-center rounded-full text-ink-500 hover:bg-ink-100 disabled:opacity-30"
        aria-label="Next page"
      >
        <FiChevronRight className="h-4 w-4" />
      </button>
    </nav>
  );
}
