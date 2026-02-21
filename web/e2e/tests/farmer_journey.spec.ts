// BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
import { expect, test } from "@playwright/test";

test.describe("farmer journey smoke", () => {
  test("home page links to login page", async ({ page }) => {
    await page.goto("/");
    await expect(
      page.getByRole("heading", { name: "TarlaAnaliz Platform" }),
    ).toBeVisible();
    await page.getByRole("link", { name: "Girişe Git" }).click();
    await expect(page).toHaveURL(/\/login$/);
  });
});
