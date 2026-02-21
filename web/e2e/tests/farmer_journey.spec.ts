// BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
import { expect, test } from '@playwright/test';

test.describe('farmer journey (stub)', () => {
  test('login -> field -> subscription -> payment -> results', async ({ page }) => {
    await page.route('**/api/**', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ ok: true, request_id: 'req-farmer-1', corr_id: 'corr-farmer-1' })
      });
    });

    await page.goto('/farmer');
    await page.getByTestId('login-phone-input').fill('5551234567');
    await page.getByTestId('login-pin-input').fill('1234');
    await page.getByTestId('login-submit').click();

    await page.getByTestId('add-field-button').click();
    await page.getByTestId('field-name-input').fill('Tarla A');
    await page.getByTestId('field-area-input').fill('12.5');
    await page.getByTestId('field-save-button').click();

    await page.getByTestId('subscription-create-button').click();
    await page.getByTestId('plan-radio-basic').check();
    await page.getByTestId('subscription-continue-button').click();

    await page.getByTestId('payment-file-input').setInputFiles({
      name: 'dekont.pdf',
      mimeType: 'application/pdf',
      buffer: Buffer.from('stub dekont')
    });
    await page.getByTestId('payment-upload-button').click();

    await expect(page.getByTestId('result-layer-list')).toBeVisible();
  });
});
