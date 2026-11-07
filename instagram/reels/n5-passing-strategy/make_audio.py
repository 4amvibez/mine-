#!/usr/bin/env python3
"""Original soft lo-fi bed + paper/pen sound effects for the N5 passing-strategy reel."""
import numpy as np, wave, os
SR = 44100
TOTAL = 47.4
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

# scene starts, matched to the voiceover (take A)
T = dict(s2=5.01, s3=9.07, s4=16.65, s5=25.33, s6=31.31, s7=39.89)
# hook
add(sfx, 0.12, thud(), .55)
for k in range(15): add(sfx, 0.2 + k * 0.053, tick(), .35)       # 80 counting up
add(sfx, 3.85, pen(.45), .55)                                      # underline "There's a catch"
# date (page turn into paper)
add(sfx, T["s2"] - 0.3, page_turn(), .8)
for d in (0.85, 1.0): add(sfx, T["s2"] + d, pop(), .35)
add(sfx, T["s2"] + 1.4, pen(.55), .6)                              # circle the 6
add(sfx, T["s2"] + 2.2, pen(.5), .4)                               # "30 days" note
# sections
for d in (2.1, 4.1, 5.95): add(sfx, T["s3"] + d, swoosh(.35, 3000), .35)
add(sfx, T["s3"] + 6.8, pen(.5), .4)
# scoring
add(sfx, T["s4"] - 0.05, page_turn(), .5)
for d, ln in ((0.5, 1.2), (5.6, 0.8), (7.6, 0.6)): add(sfx, T["s4"] + d, rise(ln), .18)
# the catch
add(sfx, T["s5"] - 0.05, page_turn(), .5)
for d in (0.25, 0.6, 1.0): add(sfx, T["s5"] + d, pop(), .3)
add(sfx, T["s5"] + 1.75, thud(), 1.0)                              # FAIL stamp
# strategy
add(sfx, T["s6"] - 0.05, page_turn(), .5)
for d in (0.15, 2.9, 5.25, 6.6): add(sfx, T["s6"] + d, pop(), .3); add(sfx, T["s6"] + d + .4, pen(.3), .55)
# CTA
add(sfx, T["s7"] - 0.05, page_turn(), .5)
for d in (3.0, 3.5, 4.0): add(sfx, T["s7"] + d, pop(), .35)

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
