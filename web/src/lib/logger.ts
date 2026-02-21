// BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.

export type LogLevel = 'debug' | 'info' | 'warn' | 'error';

type LogMeta = Record<string, unknown>;

const REDACT_KEYS = ['phone', 'pin', 'token', 'authorization', 'password', 'tckn'];

function redact(meta?: LogMeta): LogMeta | undefined {
  if (!meta) return undefined;
  const result: LogMeta = {};
  for (const [key, value] of Object.entries(meta)) {
    if (REDACT_KEYS.includes(key.toLowerCase())) {
      result[key] = '[REDACTED]';
      continue;
    }
    result[key] = value;
  }
  return result;
}

function canLogDebug() {
  return process.env.NODE_ENV !== 'production';
}

function log(level: LogLevel, message: string, meta?: LogMeta) {
  const payload = { level, message, ...redact(meta) };
  if (level === 'debug' && !canLogDebug()) return;
  if (level === 'error') console.error(payload);
  else if (level === 'warn') console.warn(payload);
  else console.log(payload);
}

export const logger = {
  debug: (message: string, meta?: LogMeta) => log('debug', message, meta),
  info: (message: string, meta?: LogMeta) => log('info', message, meta),
  warn: (message: string, meta?: LogMeta) => log('warn', message, meta),
  error: (message: string, meta?: LogMeta) => log('error', message, meta)
};
