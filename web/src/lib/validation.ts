/* BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated. */
/* KR-081: Contract-first doğrulama yardımcıları. */

export interface ValidationResult<TValue> {
  readonly valid: boolean;
  readonly value: TValue | null;
  readonly issues: readonly string[];
}

export function requiredString(value: unknown, fieldName: string): ValidationResult<string> {
  if (typeof value !== "string") {
    return { valid: false, value: null, issues: [`${fieldName} must be string`] };
  }

  const trimmed = value.trim();
  if (!trimmed) {
    return { valid: false, value: null, issues: [`${fieldName} is required`] };
  }

  return { valid: true, value: trimmed, issues: [] };
}

export function optionalString(value: unknown, fieldName: string): ValidationResult<string | undefined> {
  if (value == null || value === "") {
    return { valid: true, value: undefined, issues: [] };
  }

  const validated = requiredString(value, fieldName);
  return {
    valid: validated.valid,
    value: validated.valid ? validated.value ?? undefined : null,
    issues: validated.issues,
  };
}

export function mergeValidationResults(
  ...results: readonly ValidationResult<unknown>[]
): ValidationResult<Record<string, never>> {
  const issues = results.flatMap((result) => result.issues);
  return {
    valid: issues.length === 0,
    value: issues.length === 0 ? {} : null,
    issues,
  };
}
