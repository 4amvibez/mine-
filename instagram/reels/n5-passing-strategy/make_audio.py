#!/usr/bin/env python3
"""Original soft lo-fi bed + paper/pen sound effects for the N5 passing-strategy reel."""
import numpy as np, wave, os
SR = 44100
TOTAL = 55.0
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

# hook
add(sfx, 0.12, thud(), .55)
for k in range(16): add(sfx, 0.2 + k * 0.055, tick(), .35)       # 80 counting up
add(sfx, 0.9, pop(), .4)
add(sfx, 2.35, pen(.45), .55)                                      # underline
# date (page turn into paper)
add(sfx, 4.15, page_turn(), .8)
for d in (4.85, 5.0): add(sfx, d, pop(), .35)
add(sfx, 5.7, pen(.55), .6)                                        # circle the 6
add(sfx, 6.8, pen(.5), .4)                                         # "30 days" note
# sections
for d in (9.9, 12.6, 15.3): add(sfx, d, swoosh(.35, 3000), .35)
add(sfx, 17.6, pen(.5), .4)
# scoring
add(sfx, 19.45, page_turn(), .5)
for d in (20.5, 23.9, 27.2): add(sfx, d, rise(1.1), .18)
# the catch
add(sfx, 30.95, page_turn(), .5)
for d in (31.5, 32.1, 32.8): add(sfx, d, pop(), .3)
add(sfx, 33.6, thud(), 1.0)                                        # FAIL stamp
# strategy
add(sfx, 38.95, page_turn(), .5)
for d in (39.6, 42.0, 44.5, 47.0): add(sfx, d, pop(), .3); add(sfx, d + .4, pen(.3), .55)
# CTA
add(sfx, 49.95, page_turn(), .5)
for i, d in enumerate((51.5, 51.65, 51.8)): add(sfx, d, pop(), .35)

t_all = np.arange(N) / SR
mix = music * 0.35 + sfx
mix *= np.minimum(1, t_all / .05) * np.minimum(1, (TOTAL - t_all) / 1.2)
mix /= np.max(np.abs(mix)) * 1.15
st = np.stack([mix, mix], 1)
for name, data in (("audio.wav", st), ("music_only.wav", np.stack([music, music], 1) / (np.max(np.abs(music)) * 1.15))):
    with wave.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), name), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((data * 32767).astype(np.int16).tobytes())
print("audio ok")
