// BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
import { expect, test } from '@playwright/test';

test.describe('expert journey (stub)', () => {
  test('login -> queue -> review -> verdict', async ({ page }) => {
    await page.route('**/api/**', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ ok: true, request_id: 'req-expert-1', corr_id: 'corr-expert-1' })
      });
    });

    await page.goto('/expert');
    await page.getByTestId('login-phone-input').fill('5551234567');
    await page.getByTestId('login-pin-input').fill('1234');
    await page.getByTestId('login-submit').click();

    await page.getByTestId('expert-queue-item-0').click();
    await expect(page.getByTestId('annotation-canvas')).toBeVisible();

    await page.getByTestId('verdict-select').selectOption('approve');
    await page.getByTestId('verdict-submit').click();

    await expect(page.getByTestId('review-status')).toHaveText(/submitted/i);
  });
});
