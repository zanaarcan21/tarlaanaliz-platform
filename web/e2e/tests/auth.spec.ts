// BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
import { expect, test } from '@playwright/test';

test.describe('auth flow (stub)', () => {
  test('phone + pin login with deterministic selectors', async ({ page }) => {
    await page.route('**/api/auth/login', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          access_token: 'stub-token',
          user: { id: 'u-farmer-1', role: 'farmer' },
          request_id: 'req-auth-1',
          corr_id: 'corr-auth-1'
        })
      });
    });

    await page.goto('/login');
    await page.getByTestId('phone-input').fill('5551234567');
    await page.getByTestId('pin-input').fill('1234');
    await page.getByTestId('login-submit').click();

    await expect(page.getByTestId('auth-status')).toHaveText(/success/i);
  });
});
