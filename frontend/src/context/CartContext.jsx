import { createContext, useCallback, useEffect, useMemo, useState } from 'react';
import { orderService } from '@/services/orderService';
import { useAuth } from '@/hooks/useAuth';

export const CartContext = createContext(null);

const EMPTY_CART = { items: [], subtotal: '0.00', item_count: 0 };

export function CartProvider({ children }) {
  const { isAuthenticated } = useAuth();
  const [cart, setCart] = useState(EMPTY_CART);
  const [isLoading, setIsLoading] = useState(false);

  const refreshCart = useCallback(async () => {
    if (!isAuthenticated) {
      setCart(EMPTY_CART);
      return;
    }
    setIsLoading(true);
    try {
      const data = await orderService.getCart();
      setCart(data);
    } finally {
      setIsLoading(false);
    }
  }, [isAuthenticated]);

  useEffect(() => {
    refreshCart();
  }, [refreshCart]);

  const addItem = useCallback(
    async (payload) => {
      await orderService.cartItems.create(payload);
      await refreshCart();
    },
    [refreshCart],
  );

  const updateItem = useCallback(
    async (id, payload) => {
      await orderService.cartItems.update(id, payload);
      await refreshCart();
    },
    [refreshCart],
  );

  const removeItem = useCallback(
    async (id) => {
      await orderService.cartItems.remove(id);
      await refreshCart();
    },
    [refreshCart],
  );

  const value = useMemo(
    () => ({ cart, isLoading, refreshCart, addItem, updateItem, removeItem }),
    [cart, isLoading, refreshCart, addItem, updateItem, removeItem],
  );

  return <CartContext.Provider value={value}>{children}</CartContext.Provider>;
}
