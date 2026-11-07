// Render each <section class="slide"> in slides.html to a 1080x1350 PNG.
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
(async () => {
  const dir = __dirname;
  const out = path.join(dir, 'out');
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.join(dir, 'slides.html'));
  await page.evaluate(() => document.fonts.ready);
  const n = await page.locator('section.slide').count();
  for (let i = 0; i < n; i++) {
    const file = path.join(out, `anime-japanese-${String(i + 1).padStart(2, '0')}.png`);
    await page.locator('section.slide').nth(i).screenshot({ path: file });
  }
  await browser.close();
  console.log('rendered', n);
})();
