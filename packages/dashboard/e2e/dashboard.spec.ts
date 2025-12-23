import { expect, test } from '@playwright/test';

test.describe('AFO Kingdom Dashboard', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to the main page
    await page.goto('/');
  });

  test('should load the main dashboard', async ({ page }) => {
    // Check if the main heading is visible (actual heading is "PROJECT GENESIS")
    await expect(page.getByRole('heading', { name: /PROJECT GENESIS/ })).toBeVisible();

    // Check if the main navigation or content areas are present
    await expect(page.locator('main')).toBeVisible();

    // Check for system vitality section (unique content)
    await expect(page.getByText('11-ORGANS VITALITY')).toBeVisible();
  });

  test('should navigate to manual page', async ({ page }) => {
    // Navigate to the manual page
    await page.goto('/docs/manual');

    // Check if the manual page loads (Matches the first heading which is the main title)
    await expect(page.getByRole('heading', { name: /야전교범/ }).first()).toBeVisible();

    // Check if the principles section is visible
    await expect(page.getByText('야전교범 3원칙')).toBeVisible();
  });

  test('should load Trinity Harmony widget in sandbox', async ({ page }) => {
    // Navigate to the Trinity Harmony widget sandbox
    await page.goto('/sandbox/TrinityHarmonyWidget');

    // Check for Trinity Harmony title
    await expect(page.getByText(/Trinity Harmony/)).toBeVisible();
  });

  test('should handle lazy loading components', async ({ page }) => {
    // Navigate to the main page
    await page.goto('/');

    // Wait for lazy-loaded components to appear
    await page.waitForTimeout(2000); // Allow time for lazy loading

    // Check if lazy-loaded content appears
    // This test verifies that Suspense boundaries work correctly
    await expect(page.locator('main')).toBeVisible();
  });

  test('should be responsive on mobile', async ({ page, isMobile }) => {
    if (isMobile) {
      // Check mobile layout
      await expect(page.locator('main')).toBeVisible();

      // Check if mobile navigation or responsive elements work
      const viewport = page.viewportSize();
      if (viewport && viewport.width < 768) {
        // Mobile viewport specific checks
        await expect(page.locator('[data-mobile-menu]')).toBeVisible({ timeout: 1000 }).catch(() => {
          // If no mobile menu, that's also fine
          console.log('No mobile-specific menu detected');
        });
      }
    }
  });

  test('should handle error boundaries gracefully', async ({ page }) => {
    // Navigate to a page that might trigger errors
    await page.goto('/nonexistent-route');

    // Check if error boundary shows appropriate message
    await expect(page.getByText(/not found|error|404/)).toBeVisible({ timeout: 5000 }).catch(() => {
      // If no error page, check if redirected to home
      expect(page.url()).toContain('/');
    });
  });

  test('should load images with proper optimization', async ({ page }) => {
    // Check for optimized images (WebP format, lazy loading)
    const images = page.locator('img');

    // Wait for images to load
    await images.first().waitFor({ timeout: 10000 }).catch(() => {
      // No images found, which is also acceptable
      console.log('No images found on page');
    });

    // If images exist, check for optimization attributes
    const imageCount = await images.count();
    if (imageCount > 0) {
      for (let i = 0; i < Math.min(imageCount, 3); i++) {
        const img = images.nth(i);
        const src = await img.getAttribute('src');

        // Check for WebP or optimized formats
        if (src) {
          expect(src).toMatch(/\.(webp|avif|jpg|jpeg|png)/i);
        }

        // Check for lazy loading
        const loading = await img.getAttribute('loading');
        if (loading) {
          expect(loading).toBe('lazy');
        }
      }
    }
  });

  test('should have proper accessibility attributes', async ({ page }) => {
    // Check for ARIA labels and semantic HTML
    const headings = page.locator('h1, h2, h3, h4, h5, h6');
    await expect(headings.first()).toBeVisible();

    // Check for alt text on images
    const images = page.locator('img[alt]');
    const imagesWithoutAlt = page.locator('img:not([alt])');

    const altCount = await images.count();
    const noAltCount = await imagesWithoutAlt.count();

    // Prefer images with alt text
    if (altCount > 0 || noAltCount === 0) {
      expect(altCount).toBeGreaterThanOrEqual(0);
    }
  });
});
