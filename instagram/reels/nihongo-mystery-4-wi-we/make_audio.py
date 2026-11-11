#!/usr/bin/env python3
"""Original soft lo-fi bed + paper/pen sound effects for NIHONGO MYSTERY #4 (ゐ/ゑ)."""
import numpy as np, wave, os
SR = 44100
TOTAL = 56.5
N = int(TOTAL * SR); rng = np.random.default_rng(3)

def env(n, a=0.005, d=0.2):
    t = np.arange(n) / SR
    return np.minimum(t / max(a, 1e-4), 1) * np.exp(-t / d)
def add(buf, start, sig, g=1.0):
    i = int(start * SR); j = min(len(buf), i + len(sig))
    if 0 <= i < len(buf): buf[i:j] += sig[:j - i] * g
def lp(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); y = np.empty_like(x); acc = 0.0
    for i in range(len(x)): acc = (1 - a) * x[i] + a * acc; y[i] = acc
    return y
def tone(f, dur, a=0.01, d=0.5, harm=(1, .5, .25)):
    n = int(dur * SR); t = np.arange(n) / SR
    return sum(h * np.sin(2 * np.pi * f * (k + 1) * t) for k, h in enumerate(harm)) * env(n, a, d)

music = np.zeros(N); sfx = np.zeros(N)
# gentle pentatonic pluck + warm pad (Japanese-feeling, calm)
bpm = 84; beat = 60 / bpm
scale = [293.66, 329.63, 392.0, 440.0, 493.88, 587.33]   # D E G A B D (yo-like)
pat = [0, 2, 4, 3, 5, 3, 2, 1, 0, 2, 3, 4, 2, 1, 0, 1]
pads = [[146.83, 220.0, 293.66], [130.81, 196.0, 261.63], [164.81, 246.94, 329.63], [146.83, 220.0, 293.66]]
b = 0
while b * beat < TOTAL:
    t0 = b * beat
    if b % 4 == 0:
        pad = sum(lp(tone(f, 4 * beat, .3, 2.2, (1, .3, .1)), 1500) for f in pads[(b // 4) % 4])
        add(music, t0, pad, .07)
    add(music, t0, tone(scale[pat[b % 16]], beat * 1.5, .003, .45, (1, .5, .2, .1)), .10)
    if b % 2 == 1: add(music, t0 + beat / 2, tone(scale[pat[(b + 5) % 16]] * 2, beat, .002, .25, (1, .3)), .04)
    b += 1
def swoosh(d=.45, fc=2500):
    n = int(d * SR); return lp(rng.normal(0, 1, n), fc) * np.sin(np.linspace(0, np.pi, n)) ** 2
def page_turn():
    n = int(.55 * SR); x = rng.normal(0, 1, n); x = x - lp(x, 900)
    return x * np.sin(np.linspace(0, np.pi, n)) ** 1.5 * .5
def pen(d=.45):
    n = int(d * SR); x = rng.normal(0, 1, n); x = lp(x, 5000) - lp(x, 1500)
    wob = .55 + .45 * np.abs(np.sin(np.linspace(0, d * 38, n)))
    return x * wob * np.minimum(np.linspace(0, 8, n), 1) * np.minimum(np.linspace(8, 0, n), 1)
def tick():
    n = int(.03 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * 2200 * t) * env(n, .0005, .006)
def pop():
    n = int(.08 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * (500 + 700 * t / .08) * t) * env(n, .001, .025)
def thud():
    n = int(.6 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * (55 + 90 * np.exp(-t * 18)) * t) * env(n, .001, .18) + lp(rng.normal(0, 1, n), 900) * env(n, .001, .05) * .8)
def ding():
    n = int(1.0 * SR); t = np.arange(n) / SR
    return (np.sin(2*np.pi*1318.5*t) + .6*np.sin(2*np.pi*1975.5*t)) * env(n, .002, .35)
# cues (timeline before the CTA pause)
for c in (0.05, 1.0, 4.5, 5.6, 6.4, 7.1, 7.88, 8.68, 11.1, 12.82, 13.94, 16.34, 17.28, 17.9, 19.76, 21.58, 22.9,
          24.0, 25.08, 27.36, 28.6, 32.46, 33.2, 35.38, 36.12, 37.0, 42.6, 45.88, 47.9, 48.18): add(sfx, c, pop(), .3)
for c in (18.0, 18.3, 18.6, 41.2, 43.5): add(sfx, c, page_turn(), .5)   # snapshots dropped on the table
for c in (19.05, 19.3, 41.75, 44.1): add(sfx, c, pen(.45), .5)          # red pen circling the letter
add(sfx, 3.72, thud(), .8); add(sfx, 10.2, ding(), .28); add(sfx, 31.22, thud(), 1.0)
add(sfx, 34.22, pen(.3), .45); add(sfx, 35.7, pen(.3), .45)
for d in (46.25, 46.85, 47.3): add(sfx, d, tick(), 1.0); add(sfx, d + .05, pop(), .45)
add(sfx, 45.83, ding(), .3)
# 3.65 s pause before the CTA (same as the video): the noren beat, then the wipe
B=45.82; G=3.65; i=int(B*SR); sfx=np.concatenate([sfx[:i], np.zeros(int(G*SR)), sfx[i:]])[:N]
for c in (0.0,): add(sfx, B + c, pop(), .3)
for c in (0.15, 1.25): add(sfx, B + c, page_turn(), .5)   # noren snapshots
for c in (0.65, 1.75): add(sfx, B + c, pen(.45), .5)      # red-pen circles
add(sfx, B + G - 0.45, swoosh(.45, 2600), .45)            # the only wipe, into the CTA
t_all = np.arange(N) / SR
mix = music * 0.0 + sfx * 0.8  # bed sits under the voiceover
mix *= np.minimum(1, t_all / .05) * np.minimum(1, (TOTAL - t_all) / 1.2)
mix /= np.max(np.abs(mix)) * 1.15
st = np.stack([mix, mix], 1)
for name, data in (("sfx.wav", st), ("music_only.wav", np.stack([music, music], 1) / (np.max(np.abs(music)) * 1.15))):
    with wave.open(name, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((data * 32767).astype(np.int16).tobytes())
print("audio ok")
