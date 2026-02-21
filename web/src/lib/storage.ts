// BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.

export interface StorageAdapter {
  get: (key: string) => string | null;
  set: (key: string, value: string) => void;
  remove: (key: string) => void;
}

export function createLocalStorageAdapter(): StorageAdapter {
  return {
    get: (key) => (typeof window === 'undefined' ? null : window.localStorage.getItem(key)),
    set: (key, value) => {
      if (typeof window !== 'undefined') window.localStorage.setItem(key, value);
    },
    remove: (key) => {
      if (typeof window !== 'undefined') window.localStorage.removeItem(key);
    }
  };
}

export const tokenStorageKey = 'ta_auth_token';
