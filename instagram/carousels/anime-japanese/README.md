# Anime Japanese that gets you fired (11-slide carousel)

`slides/` has the 11 finished 1080x1350 PNGs, ready to upload in order.

## Add your own anime images (optional)

Every kanji has furigana. Save images in `images/` with these exact names, then
rebuild. Any slide without an image still works as it is.

| File | Slide | Shape |
|---|---|---|
| `cover.png` | 1, cover character (transparent background) | portrait |
| `stake.png` | 2, the boss scene | landscape |
| `s03.png` to `s08.png` | 3 to 8, one character per word | portrait 3:4 |
| `s10.png` | 10, quiz scene | wide |
| `s11.png` | 11, CTA character | square |

## Rebuild

The fonts (Dela Gothic One, Yuji Syuku, Archivo Black, Noto Sans JP 500/700/900)
come from Google Fonts. They are not committed because they're large. Put the
`.ttf` files in `fonts/` using the file names from `build.py`, then run:

```bash
python3 build.py && node render.js   # writes PNGs to out/
```
