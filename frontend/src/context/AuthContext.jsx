import { createContext, useCallback, useEffect, useMemo, useState } from 'react';
import { authService } from '@/services/authService';
import { tokenStorage } from '@/utils/tokenStorage';

export const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  const loadCurrentUser = useCallback(async () => {
    if (!tokenStorage.hasTokens()) {
      setUser(null);
      setIsLoading(false);
      return;
    }
    try {
      const { data } = await authService.me();
      setUser(data);
    } catch {
      tokenStorage.clear();
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadCurrentUser();

    // Fired by the Axios interceptor when a refresh attempt fails (e.g.
    // the refresh token itself expired) — keeps context state in sync
    // with a logout that happened outside of an explicit user action.
    const handleForcedLogout = () => setUser(null);
    window.addEventListener('afc:unauthorized', handleForcedLogout);
    return () => window.removeEventListener('afc:unauthorized', handleForcedLogout);
  }, [loadCurrentUser]);

  const login = useCallback(async (credentials) => {
    const { data } = await authService.login(credentials);
    tokenStorage.setTokens({ access: data.access, refresh: data.refresh });
    setUser(data.user);
    return data.user;
  }, []);

  const register = useCallback(async (payload) => {
    const { data } = await authService.register(payload);
    return data;
  }, []);

  const logout = useCallback(async () => {
    const refresh = tokenStorage.getRefreshToken();
    try {
      if (refresh) await authService.logout(refresh);
    } catch {
      // Even if the server call fails (e.g. token already expired),
      // proceed with clearing local session state.
    } finally {
      tokenStorage.clear();
      setUser(null);
    }
  }, []);

  const refreshUser = useCallback(async () => {
    const { data } = await authService.me();
    setUser(data);
    return data;
  }, []);

  const value = useMemo(
    () => ({
      user,
      setUser,
      isAuthenticated: Boolean(user),
      isAdmin: user?.role === 'admin' || user?.role === 'staff',
      isLoading,
      login,
      register,
      logout,
      refreshUser,
    }),
    [user, isLoading, login, register, logout, refreshUser],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
