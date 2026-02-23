import { test, expect } from '@playwright/test';

test.describe('USD/CNY Quant POC Frontend', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to the homepage (Next.js default port)
    await page.goto('/');
  });

  test('has correct title', async ({ page }) => {
    // Expect the page to have the project title
    // The h1 text is "FX Quant POC (USD/CNY)"
    await expect(page.getByRole('heading', { name: 'FX Quant POC (USD/CNY)' })).toBeVisible();
  });

  test('displays status cards', async ({ page }) => {
    // Check for "Current Price" status card
    await expect(page.getByText('Current Price')).toBeVisible();

    // Check for "Total Equity (CNY)" status card
    await expect(page.getByText('Total Equity (CNY)')).toBeVisible();

    // Check for USD Balance
    await expect(page.getByText('USD Balance')).toBeVisible();

    // Check for CNY Balance
    await expect(page.getByText('CNY Balance')).toBeVisible();
  });

  test('displays control buttons', async ({ page }) => {
    // Check for Start button
    const startButton = page.getByRole('button', { name: 'Start' });
    await expect(startButton).toBeVisible();

    // Check for Stop button
    const stopButton = page.getByRole('button', { name: 'Stop' });
    await expect(stopButton).toBeVisible();
  });

  test('displays configuration section', async ({ page }) => {
      // Check for Strategy Parameters heading
      await expect(page.getByText('Strategy Parameters')).toBeVisible();

      // Check for inputs (using labels since they are visually associated)
      // Since htmlFor is missing, we use layout selectors or verify the presence of the labels and inputs generally
      await expect(page.getByText('Short Window')).toBeVisible();
      await expect(page.getByText('Long Window')).toBeVisible();

      // Verify inputs exist (type number)
      const inputs = page.locator('input[type="number"]');
      await expect(inputs).toHaveCount(2);
  });
});
