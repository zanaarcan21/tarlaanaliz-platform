/* BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated. */

const DEFAULT_CURRENCY = "TRY";
const DEFAULT_LOCALE = "tr-TR";

export interface MoneyInput {
  readonly amount: number;
  readonly currency?: string;
  readonly locale?: string;
}

export function formatMoney({ amount, currency = DEFAULT_CURRENCY, locale = DEFAULT_LOCALE }: MoneyInput): string {
  if (!Number.isFinite(amount)) {
    return "";
  }

  return new Intl.NumberFormat(locale, {
    style: "currency",
    currency,
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(amount);
}

export function toMinorUnits(amount: number): number {
  if (!Number.isFinite(amount)) {
    return 0;
  }
  return Math.round(amount * 100);
}

export function fromMinorUnits(minorAmount: number): number {
  if (!Number.isFinite(minorAmount)) {
    return 0;
  }
  return minorAmount / 100;
}
