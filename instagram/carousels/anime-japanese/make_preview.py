#!/usr/bin/env python3
"""Stitch all slides into one preview video with swipe transitions."""
import subprocess, os
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
os.makedirs("seg", exist_ok=True)
segs = []
for n in range(1, 12):
    v = f"out_video/anime-japanese-{n:02d}.mp4"; o = f"seg/{n:02d}.mp4"
    if os.path.exists(v):
        subprocess.run(["ffmpeg","-v","error","-y","-i",v,"-c","copy",o], check=True); d = 4.0
    else:
        d = 3.0
        subprocess.run(["ffmpeg","-v","error","-y","-loop","1","-framerate","30","-t",str(d),"-i",f"out/anime-japanese-{n:02d}.png",
            "-f","lavfi","-t",str(d),"-i","anullsrc=r=44100:cl=stereo","-c:v","libx264","-crf","18","-pix_fmt","yuv420p",
            "-r","30","-c:a","aac","-ar","44100","-shortest",o], check=True)
    segs.append((o, d))
T = 0.35; ins = []; fc = []; pv, pa, off = "[0:v]", "[0:a]", 0
for o, _ in segs: ins += ["-i", o]
for i in range(1, len(segs)):
    off += segs[i-1][1] - T
    fc.append(f"{pv}[{i}:v]xfade=transition=slideleft:duration={T}:offset={off:.3f}[v{i}]")
    fc.append(f"{pa}[{i}:a]acrossfade=d={T}[a{i}]")
    pv, pa = f"[v{i}]", f"[a{i}]"
subprocess.run(["ffmpeg","-v","error","-y",*ins,"-filter_complex",";".join(fc),"-map",pv,"-map",pa,"-c:v","libx264",
    "-crf","20","-pix_fmt","yuv420p","-c:a","aac","-movflags","+faststart","preview-carousel.mp4"], check=True)
print("preview ok")
