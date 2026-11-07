#!/usr/bin/env python3
"""Composite each anime clip into its slide and export looping 1080x1350 MP4s.

Needs layers/ from render_video_layers.js. Every video slide is the same length
(DUR seconds); short clips loop to fill it.
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "clips")
OUT = os.path.join(HERE, "out_video")
LAY = os.path.join(HERE, "layers")
DUR = 4.0
FPS = 30
RADIUS = 22

# slide: (file, start, end, crop "w:h:x:y" of the useful picture area or None)
CLIPS = {
    3: ("119fae12-video_20261107_153958.mp4", 0.0, 2.6, "810:1080:640:0"),               # Kenshiro
    4: ("97db2996-video_20261107_155232.mp4", 0.0, 1.50, "810:1080:1000:0"),              # Bakugo
    5: ("b873e0d3-Very-rude-way-SnapYT.App.mp4", 2.15, 4.10, "202:206:0:78"),  # Pain, 貴様
    6: ("8a296746-_______________________-_4____shorts-anime-SnapYT.App.mp4", 54.95, 57.4, None),  # ボク様
    7: ("df161ae0-______-SnapYT.App.mp4", 2.6, 4.9, None),                   # Jotaro
    8: ("e098e325-video_20261107_162809.mp4", 0.0, 2.0, "1210:720:181:0"),  # samurai, 拙者
}

geo = json.load(open(os.path.join(LAY, "geometry.json")))
os.makedirs(OUT, exist_ok=True)

for n, (fname, a, b, crop) in CLIPS.items():
    g = geo[str(n)]
    w, h = g["w"], g["h"]
    src = os.path.join(SRC, fname)
    base = os.path.join(LAY, f"base-{n:02d}.png")
    cap = os.path.join(LAY, f"cap-{n:02d}.png")
    out = os.path.join(OUT, f"anime-japanese-{n:02d}.mp4")
    pre = f"crop={crop}," if crop else ""
    # fill the box (cover), rounded corners via an alpha mask, loop to DUR
    vf = (
        f"[1:v]trim={a}:{b},setpts=PTS-STARTPTS,{pre}"
        f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},fps={FPS},format=yuva420p,"
        f"geq=lum='lum(X,Y)':cb='cb(X,Y)':cr='cr(X,Y)':"
        f"a='if(gt(abs(X-{w}/2),{w}/2-{RADIUS})*gt(abs(Y-{h}/2),{h}/2-{RADIUS}),"
        f"if(lte(hypot(abs(X-{w}/2)-({w}/2-{RADIUS}),abs(Y-{h}/2)-({h}/2-{RADIUS})),{RADIUS}),255,0),255)',"
        f"loop=loop=-1:size=32767,trim=0:{DUR},setpts=PTS-STARTPTS[clip];"
        f"[0:v][clip]overlay={g['x']}:{g['y']}:shortest=0[v1];"
        f"[v1][2:v]overlay={g['cx']}:{g['cy']},format=yuv420p,trim=0:{DUR}[v];"
        f"[1:a]atrim={a}:{b},asetpts=PTS-STARTPTS,aloop=loop=-1:size=2e9,atrim=0:{DUR},afade=t=out:st={DUR-0.25}:d=0.25[aout]"
    )
    cmd = ["ffmpeg", "-v", "error", "-y",
           "-loop", "1", "-framerate", str(FPS), "-t", str(DUR), "-i", base,
           "-i", src,
           "-loop", "1", "-framerate", str(FPS), "-t", str(DUR), "-i", cap,
           "-filter_complex", vf, "-map", "[v]", "-map", "[aout]",
           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS),
           "-c:a", "aac", "-b:a", "128k", "-ar", "44100", "-t", str(DUR), "-movflags", "+faststart", out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    print(n, "OK" if r.returncode == 0 else "FAIL\n" + r.stderr[-1500:])
