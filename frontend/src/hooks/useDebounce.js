import { useEffect, useState } from 'react';

/** Debounces a fast-changing value (e.g. a search input) so dependent
 * effects (API calls) don't fire on every keystroke. */
export function useDebounce(value, delayMs = 350) {
  const [debounced, setDebounced] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebounced(value), delayMs);
    return () => clearTimeout(timer);
  }, [value, delayMs]);

  return debounced;
}
