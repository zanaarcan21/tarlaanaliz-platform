// BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.

export interface PublicEnv {
  NEXT_PUBLIC_API_BASE_URL: string;
  NEXT_PUBLIC_APP_ENV: 'development' | 'staging' | 'production' | 'test';
  NEXT_PUBLIC_ENABLE_RUM: 'true' | 'false';
}

function read(name: keyof PublicEnv): string {
  const value = process.env[name];
  if (!value) throw new Error(`Missing env: ${name}`);
  return value;
}

export function getPublicEnv(): PublicEnv {
  const env = read('NEXT_PUBLIC_APP_ENV');
  if (!['development', 'staging', 'production', 'test'].includes(env)) {
    throw new Error('NEXT_PUBLIC_APP_ENV is invalid');
  }

  const rum = read('NEXT_PUBLIC_ENABLE_RUM');
  if (!['true', 'false'].includes(rum)) {
    throw new Error('NEXT_PUBLIC_ENABLE_RUM must be true|false');
  }

  return {
    NEXT_PUBLIC_API_BASE_URL: read('NEXT_PUBLIC_API_BASE_URL'),
    NEXT_PUBLIC_APP_ENV: env as PublicEnv['NEXT_PUBLIC_APP_ENV'],
    NEXT_PUBLIC_ENABLE_RUM: rum as PublicEnv['NEXT_PUBLIC_ENABLE_RUM']
  };
}
