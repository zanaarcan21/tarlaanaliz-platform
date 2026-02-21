// BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
'use client';

import { useCallback, useMemo, useState } from 'react';

export type AuthRole = 'farmer' | 'expert' | 'pilot' | 'admin';

export interface AuthUser {
  id: string;
  role: AuthRole;
  phoneMasked?: string;
}

export interface LoginInput {
  phone: string;
  pin: string;
}

export interface AuthState {
  token: string | null;
  user: AuthUser | null;
}

export interface TokenStorage {
  getToken: () => string | null;
  setToken: (token: string) => void;
  clearToken: () => void;
}

const TOKEN_KEY = 'ta_auth_token';

function createBrowserTokenStorage(): TokenStorage {
  return {
    getToken: () => (typeof window === 'undefined' ? null : window.localStorage.getItem(TOKEN_KEY)),
    setToken: (token) => {
      if (typeof window !== 'undefined') window.localStorage.setItem(TOKEN_KEY, token);
    },
    clearToken: () => {
      if (typeof window !== 'undefined') window.localStorage.removeItem(TOKEN_KEY);
    }
  };
}

interface UseAuthOptions {
  tokenStorage?: TokenStorage;
}

export function useAuth(options?: UseAuthOptions) {
  const tokenStorage = useMemo(() => options?.tokenStorage ?? createBrowserTokenStorage(), [options?.tokenStorage]);

  const [state, setState] = useState<AuthState>({
    token: tokenStorage.getToken(),
    user: null
  });

  const login = useCallback(
    async (input: LoginInput) => {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ phone: input.phone, pin: input.pin })
      });

      if (!response.ok) {
        throw new Error('Login failed');
      }

      const data = (await response.json()) as { access_token: string; user: AuthUser };
      tokenStorage.setToken(data.access_token);
      setState({ token: data.access_token, user: data.user });
      return data;
    },
    [tokenStorage]
  );

  const logout = useCallback(() => {
    tokenStorage.clearToken();
    setState({ token: null, user: null });
  }, [tokenStorage]);

  const isAuthenticated = Boolean(state.token);

  return {
    ...state,
    isAuthenticated,
    login,
    logout
  };
}
