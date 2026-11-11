// Renders one 1080x1920 PNG per cue (black bg, vertical JP, italic EN, optional handle).
// Usage: node render_frames.js <cues.json> <outDir> <fontsourcePackageDir>
//   fontsourcePackageDir = extracted `npm pack @fontsource/noto-serif-jp` (contains 400.css)
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const [cuesPath, outDir, fontDir] = process.argv.slice(2);
const htmlPath = path.join(path.resolve(fontDir), '_cue.html');
const { handle, cues } = JSON.parse(fs.readFileSync(cuesPath, 'utf8'));
fs.mkdirSync(outDir, { recursive: true });

const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');

const page = (jp, en) => `<!doctype html><html><head><meta charset="utf-8">
<link href="400.css" rel="stylesheet">
<style>
  html,body{margin:0;width:1080px;height:1920px;background:#000;overflow:hidden}
  /* Instagram Reels safe zone: keep clear of top ~250px, bottom ~420px (caption/audio bar)
     and the right ~150px (like/comment/share buttons). */
  .jp{position:absolute;left:50%;top:40%;transform:translate(-50%,-50%);
      writing-mode:vertical-rl;text-orientation:mixed;font-family:'Noto Serif JP',serif;font-size:56px;
      line-height:1;letter-spacing:2px;color:#f2f2f2;white-space:nowrap;
      font-feature-settings:'vert' 1,'vpal' 0}
  .en{position:absolute;left:150px;right:150px;top:66%;transform:translateY(-50%);text-align:center;
      font-family:'Inter',sans-serif;font-style:italic;font-weight:500;font-size:36px;line-height:1.35;
      color:#f2f2f2;text-wrap:balance}
  .h{position:absolute;left:0;right:0;top:71.5%;transform:translateY(-50%);text-align:center;
     font-family:'Inter',sans-serif;font-size:24px;color:#8a8a8a}
</style></head><body>
<div class="jp">${esc(jp)}</div><div class="en">${esc(en)}</div>
${handle ? `<div class="h">${esc(handle)}</div>` : ''}
</body></html>`;

(async () => {
  const browser = await chromium.launch();
  const p = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  for (let i = 0; i < cues.length; i++) {
    const [, jp, en] = cues[i];
    fs.writeFileSync(htmlPath, page(jp, en));
    await p.goto('file://' + htmlPath, { waitUntil: 'load' });
    const ok = await p.evaluate(async (t) => {
      await document.fonts.load("56px 'Noto Serif JP'", t);
      await document.fonts.ready;
      return document.fonts.check("56px 'Noto Serif JP'", t);
    }, jp);
    if (!ok) throw new Error('Noto Serif JP failed to load');
    await p.screenshot({ path: path.join(outDir, `cue_${String(i).padStart(3, '0')}.png`) });
  }
  await browser.close();
  console.log(`rendered ${cues.length} frames`);
})();
