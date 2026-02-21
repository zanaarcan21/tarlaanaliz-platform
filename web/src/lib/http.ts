// BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.

import { getPublicEnv } from './env';

export interface HttpRequestOptions extends Omit<RequestInit, 'headers'> {
  headers?: HeadersInit;
  requestId?: string;
  corrId?: string;
  token?: string | null;
}

function id(prefix: string) {
  return `${prefix}-${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

export async function http<T>(path: string, options?: HttpRequestOptions): Promise<T> {
  const env = getPublicEnv();
  const url = `${env.NEXT_PUBLIC_API_BASE_URL}${path}`;
  const requestId = options?.requestId ?? id('req');
  const corrId = options?.corrId ?? id('corr');

  let headers: HeadersInit = {
    'content-type': 'application/json',
    'x-request-id': requestId,
    'x-corr-id': corrId,
    ...(options?.headers ?? {})
  };

  if (options?.token) {
    headers = { ...headers, authorization: `Bearer ${options.token}` };
  }

  const response = await fetch(url, {
    ...options,
    headers
  });

  if (response.status === 401) throw new Error('Unauthorized');
  if (response.status === 403) throw new Error('Forbidden');
  if (!response.ok) throw new Error('Request failed');

  return (await response.json()) as T;
}
