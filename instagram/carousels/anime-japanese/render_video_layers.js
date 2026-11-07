// Render the video-mode slides: a base PNG per slide, a caption PNG per clip box,
// and geometry.json with where each clip and caption sit on the 1080x1350 frame.
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
(async () => {
  const dir = __dirname;
  const out = path.join(dir, 'layers');
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.join(dir, 'slides_video.html'));
  await page.evaluate(() => document.fonts.ready);
  const slides = page.locator('section.slide');
  const n = await slides.count();
  const geo = {};
  for (let i = 0; i < n; i++) {
    const s = slides.nth(i);
    const num = i + 1;
    await s.screenshot({ path: path.join(out, `base-${String(num).padStart(2, '0')}.png`) });
    const g = await s.evaluate((el) => {
      const box = el.querySelector('.vbox');
      if (!box) return null;
      const sr = el.getBoundingClientRect();
      const r = box.getBoundingClientRect();
      const cap = box.querySelector('.vcap').getBoundingClientRect();
      return {
        x: Math.round(r.left - sr.left + box.clientLeft),
        y: Math.round(r.top - sr.top + box.clientTop),
        w: box.clientWidth, h: box.clientHeight,
        cx: Math.round(cap.left - sr.left), cy: Math.round(cap.top - sr.top),
        cw: Math.round(cap.width), ch: Math.round(cap.height),
      };
    });
    if (g) {
      geo[num] = g;
      await s.locator('.vcap').screenshot({ path: path.join(out, `cap-${String(num).padStart(2, '0')}.png`) });
    }
  }
  fs.writeFileSync(path.join(out, 'geometry.json'), JSON.stringify(geo, null, 2));
  await browser.close();
  console.log('layers', n, 'video slides', Object.keys(geo).join(','));
})();
