/* BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated. */
/* KR-033: Auth artefact lifecycle (TTL + temizleme) kontrollü tutulur. */

const TOKEN_KEY = "ta_auth_token";
const PIN_KEY = "ta_auth_pin";

type StorageKind = "token" | "pin";

interface StoredSecret {
  readonly value: string;
  readonly expiresAt: number;
}

const memoryStore = new Map<string, string>();

function getStorage(): Pick<Storage, "getItem" | "setItem" | "removeItem"> {
  if (typeof window !== "undefined" && window.localStorage) {
    return window.localStorage;
  }

  return {
    getItem: (key) => memoryStore.get(key) ?? null,
    setItem: (key, value) => {
      memoryStore.set(key, value);
    },
    removeItem: (key) => {
      memoryStore.delete(key);
    },
  };
}

function storageKey(kind: StorageKind): string {
  return kind === "token" ? TOKEN_KEY : PIN_KEY;
}

function save(kind: StorageKind, value: string, ttlMs: number): void {
  const expiresAt = Date.now() + Math.max(0, ttlMs);
  const payload: StoredSecret = { value, expiresAt };
  getStorage().setItem(storageKey(kind), JSON.stringify(payload));
}

function load(kind: StorageKind): string | null {
  const key = storageKey(kind);
  const raw = getStorage().getItem(key);
  if (!raw) {
    return null;
  }

  try {
    const payload = JSON.parse(raw) as StoredSecret;
    if (payload.expiresAt <= Date.now()) {
      getStorage().removeItem(key);
      return null;
    }
    return payload.value;
  } catch {
    getStorage().removeItem(key);
    return null;
  }
}

export function setAuthToken(token: string, ttlMs: number): void {
  save("token", token, ttlMs);
}

export function getAuthToken(): string | null {
  return load("token");
}

export function setPinArtifact(pinArtifact: string, ttlMs: number): void {
  save("pin", pinArtifact, ttlMs);
}

export function getPinArtifact(): string | null {
  return load("pin");
}

export function clearAuthStorage(): void {
  const storage = getStorage();
  storage.removeItem(TOKEN_KEY);
  storage.removeItem(PIN_KEY);
}
