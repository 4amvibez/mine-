#!/usr/bin/env bash
# Build the vertical-quote reel: black bg, vertical JP + italic EN cues timed to the voice,
# voice on top, music quietly underneath (vocal band scooped, ducked under speech).
#
# Usage: ./build.sh <voice_video> <music_video> <frames_dir> <out.mp4>
#   frames_dir = output of: node render_frames.js cues.json <frames_dir> <fontsource_dir>
set -euo pipefail
VOICE="$1"; MUSIC="$2"; FRAMES="$3"; OUT="$4"
HERE="$(cd "$(dirname "$0")" && pwd)"

LEAD=0.5        # black before the first line (reference style)
TAIL=2.5        # time after the voice ends (last line fades, music fades)
MUSIC_LUFS=-30  # background level; voice is normalised to -14, so music sits ~16 dB under

VDUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$VOICE")
TOTAL=$(python3 -c "print(round($LEAD+$VDUR+$TAIL,3))")
TMP=$(mktemp -d)

# 1) Image sequence with per-cue durations (concat demuxer)
python3 - "$HERE/cues.json" "$FRAMES" "$LEAD" "$TOTAL" > "$TMP/list.txt" <<'PY'
import json, sys, os
cues = json.load(open(sys.argv[1]))["cues"]; d = os.path.abspath(sys.argv[2])
lead, total = float(sys.argv[3]), float(sys.argv[4])
starts = [lead + c[0] for c in cues] + [total]
print(f"file '{d}/blank.png'\nduration {lead}")
for i in range(len(cues)):
    print(f"file '{d}/cue_{i:03d}.png'\nduration {starts[i+1]-starts[i]:.3f}")
print(f"file '{d}/cue_{len(cues)-1:03d}.png'")
PY
[ -f "$FRAMES/blank.png" ] || ffmpeg -v error -f lavfi -i color=black:s=1080x1920 -frames:v 1 "$FRAMES/blank.png"

FADE_OUT_ST=$(python3 -c "print($TOTAL-1.8)")
MFADE_ST=$(python3 -c "print($TOTAL-3)")
DELAY_MS=$(python3 -c "print(int($LEAD*1000))")

# 2) Video + audio mix
ffmpeg -v error -y \
  -f concat -safe 0 -i "$TMP/list.txt" \
  -i "$VOICE" -i "$MUSIC" -i "$MUSIC" \
  -filter_complex "
    [0:v]fps=30,format=yuv420p,fade=t=out:st=$FADE_OUT_ST:d=1.5[v];
    [1:a]highpass=f=80,loudnorm=I=-14:TP=-1.5:LRA=11,adelay=${DELAY_MS}|${DELAY_MS},apad,atrim=0:$TOTAL,asplit=2[voice][sc];
    [2:a]atrim=0:58[m1];[3:a]asetpts=PTS-STARTPTS[m2];
    [m1][m2]acrossfade=d=3[mloop];
    [mloop]equalizer=f=1000:t=q:w=1.2:g=-6,equalizer=f=2500:t=q:w=1.0:g=-7,equalizer=f=400:t=q:w=1.5:g=-2,
      highpass=f=60,lowpass=f=9000,loudnorm=I=$MUSIC_LUFS:TP=-9:LRA=11,
      atrim=0:$TOTAL,afade=t=in:d=1.5,afade=t=out:st=$MFADE_ST:d=3[bgm];
    [bgm][sc]sidechaincompress=threshold=0.05:ratio=4:attack=20:release=400[duck];
    [voice][duck]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.89[a]" \
  -map "[v]" -map "[a]" -t "$TOTAL" \
  -c:v libx264 -preset medium -crf 18 -r 30 -c:a aac -b:a 192k -ar 44100 -movflags +faststart "$OUT"

rm -rf "$TMP"
echo "wrote $OUT ($TOTAL s)"
