# Vertical quote reels

Black 1080×1920 reels: vertical Japanese (Noto Serif JP) on top, italic English (Inter) below,
each phrase cut on the voice, quiet background music ducked under the speech, text kept inside
the Instagram Reels safe zone.

| Reel | Files |
|---|---|
| 01 大切な人 (66 s) | `01-taisetsu.*` |
| 02 偶然じゃない (27 s, Fish Audio voice) | `02-guuzen.*` |

Each reel has `NN-name.cues.json` (`[start_seconds, "日本語", "English"]` per phrase, optional
`handle` watermark and `cover` `[jp, en]`), the final `.mp4`, a `_cover.png` and a `.caption.txt`.

## Build

1. `npm pack @fontsource/noto-serif-jp && tar xzf noto-serif-jp-*.tgz` (font dir = `package/`)
2. `node render_frames.js NN-name.cues.json frames package`
3. `./build.sh NN-name.cues.json <voice.mp3|mp4> <music.mp4> frames NN-name.mp4`

Background level is `MUSIC_LUFS` in `build.sh` (−30 by default; lower = quieter).
