"""Paint the Chinese ink-wash assets for the は reel with the user's poly_ink library:
background (paper + misty mountains), は written stroke by stroke, and a dry-brush sweep transition."""
import os, sys
import numpy as np
from PIL import Image

REPO = sys.argv[1]
OUT = sys.argv[2]
sys.path.insert(0, REPO)
from poly_ink import InkScene, brush_stroke, sweep, splatter  # noqa: E402
from poly_ink.brush import HOOK, PRESS_DOWN  # noqa: E402

W, H = 1080, 1920
os.makedirs(OUT, exist_ok=True)


def rgba(scene, at, color=(20, 18, 16)):
    scene.render(at=at)
    D = np.clip(scene.p.D, 0, 1)
    R = np.clip(scene.p.R, 0, 1)
    a = np.maximum(D, R)
    img = np.zeros((H, W, 4), np.uint8)
    rgb = np.array(color, np.float32)[None, None, :] * (1 - R[..., None]) + np.array((179, 36, 29), np.float32) * R[..., None]
    img[..., :3] = rgb.astype(np.uint8)
    img[..., 3] = (a * 255).astype(np.uint8)
    return Image.fromarray(img, 'RGBA')


# 1. background: paper + faint distant mountains sinking into mist
bg = InkScene(W, H, seed=77)
p = bg.p
far = p.ridge(1480, peaks=[(160, 150, 260), (520, 110, 230), (900, 170, 300)], rough=16, seed=3)
p.wash(far, dens=0.10, decay=110, tex=120, edge=0.25, mist_y=1600, mist_h=120, seed=4)
near = p.ridge(1720, peaks=[(300, 180, 320), (820, 140, 280)], rough=18, seed=5)
p.wash(near, dens=0.16, decay=90, tex=120, edge=0.25, mist_y=1820, mist_h=90, seed=6)
bg.add_background(0, 1)
bg.render().convert('RGB').save(os.path.join(OUT, 'bg.jpg'), quality=92)

# 2. は written by the bristle brush, stroke by stroke (≈2.1 s)
B = lambda pts, width, **k: brush_stroke(W, H, pts, width, **k)
ha = InkScene(W, H, seed=11)
t = ha.add(B([(330, 590), (316, 800), (314, 1000), (330, 1130), (378, 1078)], 66, dry=0.4, profile=HOOK, seed=1), 0, 560)
t = ha.add(B([(470, 765), (620, 752), (790, 738)], 54, dry=0.45, profile=PRESS_DOWN, seed=2), t + 140, 330)
LOOP = ((0, 0.6), (0.05, 1.0), (0.55, 0.9), (0.8, 0.75), (1, 0.15))
t = ha.add(B([(640, 590), (643, 770), (646, 930), (648, 1040), (612, 1092), (540, 1094), (508, 1052),
              (560, 1012), (668, 1034), (770, 1100), (830, 1135)], 54, dry=0.5, profile=LOOP, seed=3), t + 150, 850)
ha.add(splatter(W, H, 840, 1140, (30, 14), n=7, size=(1.2, 3.2), seed=5, direction=0.5), t - 120, 120)
total = int(ha.length) + 100
os.makedirs(os.path.join(OUT, 'ha'), exist_ok=True)
for i, ms in enumerate(range(0, total + 1, 33)):
    rgba(ha, ms).save(os.path.join(OUT, 'ha', f'{i + 1:04d}.png'))
rgba(ha, None).save(os.path.join(OUT, 'ha_final.png'))
print('ha frames', i + 1, 'ms', total)

# 3. dry-brush sweep for scene transitions (≈0.5 s)
sw = InkScene(W, H, seed=21)
tt = 0
for k, (pts, width, ink, dry) in enumerate([
        ([(-120, 1250), (300, 1050), (700, 800), (1200, 560)], 230, 0.9, 0.62),
        ([(-80, 1420), (380, 1180), (800, 960), (1220, 760)], 120, 0.7, 0.66)]):
    sw.add(sweep(W, H, pts, width, ink=ink, dry=dry, seed=60 + 7 * k, wash=0.3), 60 * k, 380)
sw.add(splatter(W, H, 1000, 640, (160, 90), n=30, seed=9, direction=-0.5), 300, 160)
os.makedirs(os.path.join(OUT, 'sw'), exist_ok=True)
for i, ms in enumerate(range(0, 501, 33)):
    rgba(sw, ms).save(os.path.join(OUT, 'sw', f'{i + 1:04d}.png'))
print('sweep frames', i + 1)
