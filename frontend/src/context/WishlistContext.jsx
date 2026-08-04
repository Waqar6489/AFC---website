import { createContext, useCallback, useEffect, useMemo, useState } from 'react';
import { wishlistService } from '@/services/wishlistService';
import { useAuth } from '@/hooks/useAuth';

export const WishlistContext = createContext(null);

export function WishlistProvider({ children }) {
  const { isAuthenticated } = useAuth();
  const [items, setItems] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const refreshWishlist = useCallback(async () => {
    if (!isAuthenticated) {
      setItems([]);
      return;
    }
    setIsLoading(true);
    try {
      const data = await wishlistService.list();
      setItems(data.results ?? data);
    } finally {
      setIsLoading(false);
    }
  }, [isAuthenticated]);

  useEffect(() => {
    refreshWishlist();
  }, [refreshWishlist]);

  const addItem = useCallback(
    async (productId) => {
      await wishlistService.create({ product: productId });
      await refreshWishlist();
    },
    [refreshWishlist],
  );

  const removeItem = useCallback(
    async (wishlistItemId) => {
      await wishlistService.remove(wishlistItemId);
      await refreshWishlist();
    },
    [refreshWishlist],
  );

  const isWishlisted = useCallback((productId) => items.some((item) => item.product === productId), [items]);

  const value = useMemo(
    () => ({ items, isLoading, refreshWishlist, addItem, removeItem, isWishlisted, count: items.length }),
    [items, isLoading, refreshWishlist, addItem, removeItem, isWishlisted],
  );

  return <WishlistContext.Provider value={value}>{children}</WishlistContext.Provider>;
}
