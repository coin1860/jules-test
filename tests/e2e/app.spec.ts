import { test, expect } from '@playwright/test';

test.describe('USD/CNY Quant POC Frontend', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to the homepage (Next.js default port)
    await page.goto('/');
  });

  test('has correct title', async ({ page }) => {
    // Expect the page to have the project title
    // Assumption: The title will be "USD/CNY Quant POC" or similar
    await expect(page).toHaveTitle(/USD\/CNY Quant POC/i);
  });

  test('displays market data section', async ({ page }) => {
    // Check for a market data display
    // Assumption: There is a heading or section labeled "Market Data"
    const marketDataHeader = page.getByRole('heading', { name: /Market Data/i });
    await expect(marketDataHeader).toBeVisible();

    // Check for USD/CNY rate display
    const rateDisplay = page.getByText(/USD\/CNY/i);
    await expect(rateDisplay).toBeVisible();
  });

  test('displays portfolio balance', async ({ page }) => {
    // Check for portfolio section
    // Assumption: Displays "Balance" or "Equity"
    const balanceText = page.getByText(/Balance/i);
    await expect(balanceText).toBeVisible();
  });

  test('allows navigating to trade execution', async ({ page }) => {
    // Check for trade buttons
    // Assumption: Buttons explicitly labeled "Buy USD" and "Sell USD"
    const buyButton = page.getByRole('button', { name: /Buy USD/i });
    const sellButton = page.getByRole('button', { name: /Sell USD/i });

    await expect(buyButton).toBeVisible();
    await expect(sellButton).toBeVisible();

    // Verify button interactivity (mock check)
    await expect(buyButton).toBeEnabled();
  });
});
