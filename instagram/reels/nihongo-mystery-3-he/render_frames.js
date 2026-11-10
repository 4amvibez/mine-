// Render reel.html frame by frame (deterministic time), or a few stills with --stills.
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
(async () => {
  const dir = __dirname;
  const stills = process.argv.includes('--stills');
  const FPS = 30;
  const out = path.join(dir, stills ? 'stills' : 'frames');
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.join(dir, process.env.PAGE || 'reel.html'));
  await page.evaluate(() => document.fonts.ready);
  const total = await page.evaluate(() => window.TOTAL);
  const times = stills ? process.argv.slice(3).map(Number) : [...Array(Math.round(total * FPS)).keys()].map(i => i / FPS);
  for (let i = 0; i < times.length; i++) {
    await page.evaluate((t) => window.render(t), times[i]);
    const name = stills ? `t${times[i].toFixed(2)}.png` : `${String(i).padStart(4, '0')}.jpg`;
    await page.screenshot({ path: path.join(out, name), type: stills ? 'png' : 'jpeg', quality: stills ? undefined : 92 });
  }
  await browser.close();
  console.log('total', total, 'frames', times.length);
})();
