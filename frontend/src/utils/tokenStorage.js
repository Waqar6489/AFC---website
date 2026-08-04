/**
 * Centralizes JWT persistence. Kept as a single module so the storage
 * mechanism (currently localStorage) can be swapped later without
 * touching every call site.
 */
const ACCESS_TOKEN_KEY = 'afc_access_token';
const REFRESH_TOKEN_KEY = 'afc_refresh_token';

export const tokenStorage = {
  getAccessToken: () => localStorage.getItem(ACCESS_TOKEN_KEY),
  getRefreshToken: () => localStorage.getItem(REFRESH_TOKEN_KEY),

  setTokens: ({ access, refresh }) => {
    if (access) localStorage.setItem(ACCESS_TOKEN_KEY, access);
    if (refresh) localStorage.setItem(REFRESH_TOKEN_KEY, refresh);
  },

  setAccessToken: (access) => {
    localStorage.setItem(ACCESS_TOKEN_KEY, access);
  },
  setRefreshToken: (refresh) => {
  localStorage.setItem(REFRESH_TOKEN_KEY, refresh);
},

  clear: () => {
    localStorage.removeItem(ACCESS_TOKEN_KEY);
    localStorage.removeItem(REFRESH_TOKEN_KEY);
  },

  hasTokens: () => Boolean(localStorage.getItem(REFRESH_TOKEN_KEY)),
};
