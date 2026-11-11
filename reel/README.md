# Vertical quote reel

Black 1080×1920 reel: vertical Japanese (Noto Serif JP) on top, italic English (Inter) below,
each phrase cut on the voice, with quiet background music ducked under the speech.

1. Edit `cues.json`: `[start_seconds, "日本語", "English"]` per phrase; `handle` is an optional watermark.
2. `npm pack @fontsource/noto-serif-jp && tar xzf noto-serif-jp-*.tgz` (font dir = `package/`)
3. `node render_frames.js cues.json frames package`
4. `./build.sh <voice.mp4> <music.mp4> frames reel_final.mp4`

Background level is `MUSIC_LUFS` in `build.sh` (−30 by default; lower = quieter).
