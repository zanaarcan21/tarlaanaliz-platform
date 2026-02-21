// BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
import { expect, test } from "@playwright/test";

test.describe("expert journey smoke", () => {
  test("expert queue page renders static shell", async ({ page }) => {
    await page.goto("/queue");
    await expect(
      page.getByRole("heading", { name: "İnceleme Kuyruğu" }),
    ).toBeVisible();
  });
});
