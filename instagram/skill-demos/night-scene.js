// night.js: "The star that came home", 10 s, no character. Same painted night world as the demo
// (sky, moon, hills, grass, the star pal), told by the camera alone.
//   0–2 s   slow drift over the hills, stars twinkling, grass swaying.
//   2–3 s   a star falls behind the far hill; a glow and sparkles where it lands.
//   3–6 s   the camera pushes toward the glow; the star rises out of the grass, dim, then brightening.
//   6–7.5 s it flies home along an arc, sparkle trail behind it.
//   7.5–10  it flares in the sky, a twinkle ripples across all the stars, the camera eases back; iris closes on it.
(() => {
  function sky(t, ripple = null) {
    boilSeed('sky');
    paint(rectPts(-600, -400, W + 1200, H + 800), { wash: PAL.night, ink: null });
    paint(ellPts(W / 2, H * .95, W * .75, H * .45 * 1.2, 30, 10), { fill: PAL.violet, fillOp: 110, bleed: .3, tex: .6, ink: null });
    paint(ellPts(W * .3, H * .15, W * .35, H * .25, 24, 10), { fill: PAL.indigo, fillOp: 90, bleed: .3, tex: .5, ink: null });
    for (let i = 0; i < 46; i++) {
      boilSeed('star' + i);
      const x = hash(i) * (W + 200) - 100, y = hash(i + 100) * H * .6 - 40;
      let tw = .55 + .45 * Math.sin(t * (2 + 2 * hash(i + 300)) + i);
      let rp = 0;
      if (ripple && t > ripple.t0) { const a = t - ripple.t0 - Math.hypot(x - ripple.x, y - ripple.y) / 1100; if (a > 0) rp = Math.exp(-a * 5) * Math.min(1, a * 25); }
      paint(starPts(x, y, (3 + 5 * hash(i + 200)) * tw, .35, 4), { wash: PAL.cream, washOp: Math.min(255, 150 + 100 * tw + 120 * rp), ink: null });
      if (rp > .08) { const L = 6 + 16 * rp; inkLine([[x - L, y], [x + L, y]], .6, PAL.cream, 'inkfine', 0); inkLine([[x, y - L], [x, y + L]], .6, PAL.cream, 'inkfine', 0); }   // the ripple: a quick cross-glint as the wave passes
    }
    boilSeed('moon');
    paint(ellPts(260, 170, 70, 70, 24, 1.5), { wash: PAL.cream, fill: PAL.ochre, fillOp: 40, ink: PAL.ink, sw: .8 });
    paint(ellPts(245, 150, 16, 12, 10), { fill: mixCol(PAL.cream, PAL.ochre, .5), fillOp: 120, ink: null });
  }
  function hill(cx, cy, rx, ry, col, t, tufts = 0) {
    boilSeed('hill' + cx);
    paint(ellPts(cx, cy, rx, ry, 40, 2), { wash: col, fill: mixCol(col, PAL.night, .35), fillOp: 90, bleed: .08, tex: .6, ink: PAL.ink, sw: 1 });
    for (let i = 0; i < tufts; i++) {
      const a = -Math.PI / 2 + (hash(i + cx) - .5) * 1.6, x = cx + Math.cos(a) * rx, y = cy + Math.sin(a) * ry + 4, sw = wob(t, .5, hash(i) * 3) * 5;
      for (const k of [-1, 0, 1]) inkLine([[x + k * 7, y], [x + k * 11 + sw, y - 22 - 8 * hash(i + k)]], .7, mixCol(col, PAL.cream, .35), 'inkfine', .4);
    }
  }
  function starling(x, y, r, o = {}) {
    const g = clamp(o.glow ?? .6), tw = 1 + .06 * Math.sin(T * 9);
    glow(x, y, r * (1.6 + 1.4 * g) * tw, '#FFD96A', .25 + .75 * g);
    push(); translate(x, y); rotate(o.rot || 0);
    paint(starPts(0, 0, r, .52, 5), { wash: mixCol('#B9A98A', '#FFE27A', g), fill: PAL.cream, fillOp: 30 + 80 * g, ink: PAL.ink, sw: clamp(r / 40, .5, 1.2) });
    pop();
  }
  const sparkle = (x, y, r, k) => { if (k > 0 && k < 1) paint(starPts(x, y, r * backOut(k) * (1 - k * .6), .25, 4, k * 2), { wash: PAL.cream, washOp: 255 * (1 - k * k), ink: null }); };

  const tFall0 = 1.9, tLand = 2.75, tRise = 3.6, tLaunch = 6.0, tHome = 7.4;
  const land = [1545, 700], home = [1380, 170];
  const fallAt = t => { const k = easeIn(seg(t, tFall0, tLand)); return [lerp(1700, land[0], k), lerp(30, land[1], k)]; };

  function shotNight(t, lt, dur) {
    const shake = t > tLand ? shakeXY(t, 6 * Math.exp(-(t - tLand) * 7)) : [0, 0];
    camBegin(kf(t, [[0, 820], [2.4, 960], [5.8, 1240], [8.2, 1100], [10, 1050]]) + shake[0],
             kf(t, [[0, 560], [5.8, 600], [7.6, 470], [10, 500]]) + shake[1],
             kf(t, [[0, 1], [2.8, 1.04], [5.8, 1.12], [8.2, 1.0], [10, 1.03]]));
    sky(t, window.NORIPPLE ? null : { x: home[0], y: home[1], t0: tHome });

    if (t > tFall0 && t < tLand + .05) {   // the fall and its trail
      boilSeed('fall');
      const P = []; for (let k = 6; k >= 0; k--) P.push(fallAt(Math.max(tFall0, t - k * .045)));
      if (Math.hypot(P[6][0] - P[0][0], P[6][1] - P[0][1]) > 8) paint(ribbon(P, 2, 26), { wash: PAL.cream, fill: PAL.ochre, fillOp: 90, ink: null });
      const [sx, sy] = fallAt(t); starling(sx, sy, 22, { glow: 1, rot: t * 9 });
    }
    if (t > tLand && t < tLaunch + .4) {   // the landing glow, fading while it waits
      const a = t - tLand, k = Math.exp(-a * 1.2);
      glow(land[0], land[1] - 10, 60 + 240 * (1 - Math.exp(-a * 5)), '#FFD96A', .25 + .9 * k);
      for (let i = 0; i < 7; i++) { const q = seg(a, i * .03, .5 + i * .03), ang = -Math.PI / 2 + (i - 3) * .35; sparkle(land[0] + Math.cos(ang) * 190 * q, land[1] - 40 + Math.sin(ang) * 170 * q, 18, q); }
    }
    hill(1560, 900, 820, 260, mixCol(PAL.teal, PAL.night, .45), t, 10);

    boilSeed('star');
    if (t > tRise && t < tLaunch) {   // it climbs out of the grass, dim at first, then brightening
      const k = easeOut(seg(t, tRise, tRise + 1.2)), b = seg(t, tRise + .8, tLaunch - .2);
      starling(land[0], land[1] - 30 - 70 * k + 6 * Math.sin(t * 3), 34, { glow: .15 + .85 * b, rot: .15 * Math.sin(t * 2.5) });
      sparkle(land[0], land[1] - 100, 60, seg(t, tLaunch - .45, tLaunch));
    } else if (t >= tLaunch && t < tHome) {   // the flight home
      const k = easeOut(seg(t, tLaunch, tHome)), from = [land[0], land[1] - 100];
      for (let i = 1; i < 9; i++) { const q = arcPt(from, home, 260, Math.max(0, k - i * .045)); sparkle(q[0] + jit(4), q[1], 16 - i, .3 + i * .08); }
      const p = arcPt(from, home, 260, k);
      starling(p[0], p[1], lerp(34, 22, k), { glow: 1, rot: t * 10 * (1 - k) });
    } else if (t >= tHome) {   // home: a flare, then a steady twinkle
      const a = t - tHome, flare = Math.exp(-a * 4);
      glow(...home, 90 + 120 * flare, '#FFE9A8', .6 * clamp(flare));
      sparkle(...home, 120, seg(a, 0, .55));
      starling(...home, 22 * (1 + .3 * clamp(flare)), { glow: .85 + .15 * Math.sin(a * 6), rot: .1 * Math.sin(a * 3) });
    }

    hill(700, 1010, 900, 220, mixCol(PAL.sap, PAL.night, .35), t, 16);
    const eye = toScreen(...home);
    camEnd();
    boilSeed('transition');
    if (lt < .5) iris(W / 2, H / 2, lerp(0, 1500, easeIn(lt / .5)));
    if (lt > 9.0) {   // close on the star that came home
      const r = lt < 9.45 ? lerp(1500, 200, ease(seg(lt, 9.0, 9.45))) : lt < dur - .25 ? 200 : lerp(200, 0, easeIn(seg(lt, dur - .25, dur - .03)));
      iris(...eye, r);
    }
  }

  shots([[0, shotNight]]);
})();
