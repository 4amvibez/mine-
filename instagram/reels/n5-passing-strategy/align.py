#!/usr/bin/env python3
"""Find where each scene's first spoken line starts in the voiceover (word timestamps),
then print scene start times for reel.html's window.T."""
import sys, json, subprocess, numpy as np, re
from faster_whisper import WhisperModel

wav = sys.argv[1]
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", wav, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True).stdout
audio = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
m = WhisperModel("small", device="cpu", compute_type="int8")
segs, _ = m.transcribe(audio, language="en", word_timestamps=True)
words = [(w.word.strip().lower(), w.start, w.end) for s in segs for w in s.words]
print(" ".join(f"{w}@{a:.2f}" for w, a, _ in words))
# cue words that start each scene, in order
cues = [("s2", ["exam"]), ("s3", ["n5", "has", "three"]), ("s4", ["need", "eighty"]),
        ("s5", ["miss"]), ("s6", ["scores", "scaled"]), ("s7", ["save"])]
def norm(w): return re.sub(r"[^a-z0-9]", "", w)
T = {"s1": 0.0}; i = 0
for scene, keys in cues:
    while i < len(words) and norm(words[i][0]) not in [norm(k) for k in keys]:
        i += 1
    if i < len(words):
        T[scene] = round(max(words[i][1] - 0.25, 0), 2)
end = words[-1][2] + 2.2 if words else 55
T["end"] = round(end, 2)
print(json.dumps(T))
