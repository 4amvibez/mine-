# Anime Japanese that gets you fired (10-slide carousel)

`slides/` has the 10 finished 1080x1350 PNGs, ready to upload in order.

## Add your own anime images (optional)

Save them in `images/` with these exact names, then rebuild:

- `cover.png`: replaces the お前！ speech bubble on slide 1
- `stake.png`: replaces the two boss cards on slide 2

## Rebuild

The fonts (Dela Gothic One, Yuji Syuku, Archivo Black, Noto Sans JP 500/700/900)
come from Google Fonts. They are not committed because they're large. Put the
`.ttf` files in `fonts/` using the file names from `build.py`, then run:

```bash
python3 build.py && node render.js   # writes PNGs to out/
```
