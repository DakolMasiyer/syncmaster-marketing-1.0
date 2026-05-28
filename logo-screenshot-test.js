/**
 * Playwright screenshot verification script for SyncMaster Design System
 * Captures full-page screenshots of all HTML files containing logo references
 * and checks for broken images (img elements with naturalWidth === 0).
 *
 * Usage: node logo-screenshot-test.js
 * Requires: npm install playwright --save-dev
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

// Design system root
const DS_ROOT = '/Users/dakolmasiyer/Projects/syncmaster-marketing-1.0/SyncMaster Design System';

// Output directory for screenshots
const OUT_DIR = '/Users/dakolmasiyer/Projects/syncmaster-marketing-1.0/logo-screenshots';

// Files to screenshot (relative to DS_ROOT)
const FILES = [
  'design_system.html',
  'brand_guidelines.html',
  'ui_kits/marketing/index.html',
  'ui_kits/dashboard/index.html',
  'preview/brand-logo-dark.html',
  'preview/brand-logo-light.html',
  'Behind the Scenes Carousel.html',
];

// Derive a safe screenshot filename from the relative path
function screenshotName(relPath) {
  // Replace path separators and spaces with dashes, keep .png extension
  return relPath.replace(/[\\/\s]+/g, '-').replace(/\.html$/, '') + '.png';
}

async function run() {
  // Ensure output directory exists
  fs.mkdirSync(OUT_DIR, { recursive: true });

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();

  const results = [];

  for (const relPath of FILES) {
    const absPath = path.join(DS_ROOT, relPath);
    const fileUrl = 'file://' + absPath;
    const outFile = path.join(OUT_DIR, screenshotName(relPath));

    let status = 'PASS';
    let brokenCount = 0;
    let errorMsg = null;

    try {
      const page = await context.newPage();

      // Navigate to the local HTML file
      await page.goto(fileUrl, { waitUntil: 'load', timeout: 15000 });

      // Wait an additional 1500ms for fonts/images to finish loading
      await page.waitForTimeout(1500);

      // Check for broken images: any <img> with naturalWidth === 0
      brokenCount = await page.evaluate(() => {
        const imgs = Array.from(document.querySelectorAll('img'));
        return imgs.filter(img => img.naturalWidth === 0).length;
      });

      if (brokenCount > 0) {
        status = 'FAIL';
      }

      // Take full-page screenshot
      await page.screenshot({ path: outFile, fullPage: true });

      await page.close();
    } catch (err) {
      status = 'FAIL';
      errorMsg = err.message;
    }

    results.push({ relPath, status, brokenCount, outFile, errorMsg });

    const detail = brokenCount > 0
      ? ` (${brokenCount} broken image${brokenCount > 1 ? 's' : ''})`
      : errorMsg
        ? ` (error: ${errorMsg})`
        : '';
    console.log(`[${status}] ${relPath}${detail}`);
    if (status === 'PASS') {
      console.log(`       -> ${outFile}`);
    }
  }

  await browser.close();

  // Summary
  console.log('\n--- Summary ---');
  const passed = results.filter(r => r.status === 'PASS');
  const failed = results.filter(r => r.status === 'FAIL');
  console.log(`PASSED: ${passed.length}/${results.length}`);
  console.log(`FAILED: ${failed.length}/${results.length}`);

  if (failed.length > 0) {
    console.log('\nFailed files:');
    failed.forEach(r => {
      const detail = r.errorMsg
        ? `error: ${r.errorMsg}`
        : `${r.brokenCount} broken image(s)`;
      console.log(`  - ${r.relPath} (${detail})`);
    });
  }

  if (passed.length > 0) {
    console.log('\nScreenshots saved:');
    passed.forEach(r => console.log(`  ${r.outFile}`));
  }

  // Exit with non-zero code if any failures
  process.exit(failed.length > 0 ? 1 : 0);
}

run().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
