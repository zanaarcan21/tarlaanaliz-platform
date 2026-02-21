// BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
import { expect, test } from "@playwright/test";

test.describe("auth flow smoke", () => {
  test("renders login form fields", async ({ page }) => {
    await page.goto("/login");

    await expect(
      page.getByRole("heading", { name: "Giriş Yap" }),
    ).toBeVisible();
    await expect(page.getByLabel("Telefon")).toBeVisible();
    await expect(page.getByLabel("PIN")).toBeVisible();
    await expect(page.getByRole("button", { name: "Giriş" })).toBeVisible();
  });
});
