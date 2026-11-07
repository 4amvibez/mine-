#!/usr/bin/env python3
"""Original soft lo-fi bed + paper/pen sound effects for the N5 passing-strategy reel."""
import numpy as np, wave, os
SR = 44100
TOTAL = 67.3
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
# --- soft lo-fi bed: 80 BPM, Fmaj7 - Em7 - Dm7 - Cmaj7, warm keys + light kick/hat ---
bpm = 80; beat = 60 / bpm
chords = [[174.61, 220.0, 261.63, 329.63], [164.81, 196.0, 246.94, 293.66],
          [146.83, 174.61, 220.0, 261.63], [130.81, 164.81, 196.0, 246.94]]
kick_n = int(.3 * SR); kt = np.arange(kick_n) / SR
kick = np.sin(2 * np.pi * (45 + 70 * np.exp(-kt * 25)) * kt) * env(kick_n, .002, .14)
hat = np.diff(rng.normal(0, 1, int(.05 * SR) + 1)) * env(int(.05 * SR), .001, .012)
b = 0
while b * beat < TOTAL:
    t0 = b * beat; bar = (b // 4) % 4
    if b % 4 == 0:
        keys = sum(lp(tone(f, 4 * beat, .04, 1.8, (1, .35, .12)), 2200) for f in chords[bar])
        add(music, t0, keys, .09)
        add(music, t0, lp(tone(chords[bar][0] / 2, 4 * beat, .02, 1.2, (1, .2)), 600), .22)
    if b % 2 == 0: add(music, t0, kick, .45)
    add(music, t0 + beat / 2, hat, .12)
    b += 1

# --- sound effects ---
def swoosh(d=.45, fc=2500):
    n = int(d * SR); return lp(rng.normal(0, 1, n), fc) * np.sin(np.linspace(0, np.pi, n)) ** 2
def page_turn():
    n = int(.55 * SR); x = rng.normal(0, 1, n)
    x = x - lp(x, 900)  # keep the crisp paper highs
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
    return (np.sin(2 * np.pi * (55 + 90 * np.exp(-t * 18)) * t) * env(n, .001, .18)
            + lp(rng.normal(0, 1, n), 900) * env(n, .001, .05) * .8)
def rise(d=1.0):
    n = int(d * SR); t = np.arange(n) / SR
    f = 300 + 500 * (t / d) ** 1.5
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.minimum(t / .05, 1) * np.exp(-((t - d) ** 2) / .02) * .0 + \
           np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.linspace(0, np.pi, n)) * .5

# scene starts for the 67s version (reel2.html)
T = dict(s2=8.55, s3=12.75, sQ=20.15, s4=29.25, s5=38.10, s6=51.65, s7=60.20)
def ding():
    n = int(1.0 * SR); t = np.arange(n) / SR
    return (np.sin(2*np.pi*1318.5*t) + .6*np.sin(2*np.pi*1975.5*t)) * env(n, .002, .35)
# hook
add(sfx, 0.12, thud(), .55)
for k in range(15): add(sfx, 0.2 + k * 0.053, tick(), .35)
add(sfx, 3.85, pen(.45), .55)
add(sfx, 5.0, swoosh(.4, 3000), .4); add(sfx, 5.2, pop(), .35)       # banner
# date
add(sfx, T["s2"] - 0.3, page_turn(), .8)
for d in (0.85, 1.0): add(sfx, T["s2"] + d, pop(), .35)
add(sfx, T["s2"] + 1.4, pen(.55), .6)
add(sfx, T["s2"] + 2.2, pen(.5), .4)
# sections + paper pages
for d in (2.1, 4.1, 5.95): add(sfx, T["s3"] + d, swoosh(.35, 3000), .35); add(sfx, T["s3"] + d + .1, page_turn(), .25)
add(sfx, T["s3"] + 6.6, pen(.5), .4)
# quiz
add(sfx, T["sQ"] - 0.05, page_turn(), .5)
add(sfx, T["sQ"] + 1.9, pop(), .3)
for k in range(3): add(sfx, T["sQ"] + 3.7 + k, tick(), 1.2)        # 3-2-1
add(sfx, T["sQ"] + 7.45, ding(), .45); add(sfx, T["sQ"] + 7.5, pen(.45), .5)
# scoring
add(sfx, T["s4"] - 0.05, page_turn(), .5)
for d, ln in ((0.5, 1.2), (5.6, 0.8), (7.6, 0.6)): add(sfx, T["s4"] + d, rise(ln), .18)
# catch + stat
add(sfx, T["s5"] - 0.05, page_turn(), .5)
for d in (0.25, 0.6, 1.0): add(sfx, T["s5"] + d, pop(), .3)
add(sfx, T["s5"] + 1.75, thud(), 1.0)
add(sfx, T["s5"] + 6.0, swoosh(.5, 2000), .45)
for k in range(22): add(sfx, T["s5"] + 7.7 + k * 0.063, tick(), .3)  # counter
add(sfx, T["s5"] + 12.4, thud(), .45)
# strategy
add(sfx, T["s6"] - 0.05, page_turn(), .5)
for d in (0.15, 2.9, 5.25, 6.6): add(sfx, T["s6"] + d, pop(), .3); add(sfx, T["s6"] + d + .4, pen(.3), .55)
# CTA
add(sfx, T["s7"] - 0.05, page_turn(), .5)
for d in (0.5, 0.7, 0.9): add(sfx, T["s7"] + d, page_turn(), .2)
add(sfx, T["s7"] + 2.5, pop(), .45); add(sfx, T["s7"] + 2.6, ding(), .3)

t_all = np.arange(N) / SR
mix = music * 0.22 + sfx * 0.8  # bed sits under the voiceover
mix *= np.minimum(1, t_all / .05) * np.minimum(1, (TOTAL - t_all) / 1.2)
mix /= np.max(np.abs(mix)) * 1.15
st = np.stack([mix, mix], 1)
for name, data in (("audio.wav", st), ("music_only.wav", np.stack([music, music], 1) / (np.max(np.abs(music)) * 1.15))):
    with wave.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), name), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((data * 32767).astype(np.int16).tobytes())
print("audio ok")
