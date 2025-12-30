import { test, expect } from '@playwright/test';

test('fingerprint consistency check', async ({ page }) => {
  // 1. Fetch truth from backend
  const backendResponse = await fetch('http://localhost:8010/health');
  const backendData = await backendResponse.json();
  const backendFingerprint = backendData.build_version;
  
  console.log(`Backend Fingerprint: ${backendFingerprint}`);
  
  // 2. Visit the dashboard
  await page.goto('http://localhost:3000/royal');
  
  // 3. Wait for the footer to load data
  const footerFingerprint = page.locator('span:has-text("BUILD_FINGERPRINT:") + span');
  
  // Wait for the text to reach a non-loading state
  await expect(footerFingerprint).not.toHaveText('---', { timeout: 15000 });
  
  const displayedFingerprint = await footerFingerprint.innerText();
  console.log(`Footer Fingerprint: ${displayedFingerprint}`);
  
  // 4. Assert equality
  expect(displayedFingerprint).toBe(backendFingerprint);
});
