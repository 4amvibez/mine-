#!/usr/bin/env python3
"""Synthesize an original 120 BPM game-show track plus timer ticks, reveal dings
and whooshes for the kanji twins reel. Writes audio.wav (44.1 kHz stereo)."""
import numpy as np, wave, os

SR = 44100
HOOK, RD, BOSS, END = 2.0, 4.2, 5.0, 2.6
ROUND_STARTS = [HOOK + i * RD for i in range(4)] + [HOOK + 4 * RD]
END_T = ROUND_STARTS[-1] + BOSS
TOTAL = END_T + END
N = int(TOTAL * SR)
t_all = np.arange(N) / SR
rng = np.random.default_rng(7)

def env(n, a=0.005, d=0.2):
    t = np.arange(n) / SR
    return np.minimum(t / a, 1) * np.exp(-t / d)

def add(buf, start, sig, gain=1.0):
    i = int(start * SR)
    j = min(len(buf), i + len(sig))
    if i < len(buf):
        buf[i:j] += sig[: j - i] * gain

def note(f, dur, kind="saw", a=0.01, d=0.3):
    n = int(dur * SR); t = np.arange(n) / SR
    if kind == "saw":
        s = sum(((-1) ** (k + 1)) * np.sin(2 * np.pi * f * k * t) / k for k in range(1, 8))
    elif kind == "square":
        s = sum(np.sin(2 * np.pi * f * k * t) / k for k in range(1, 12, 2))
    else:
        s = np.sin(2 * np.pi * f * t)
    return s * env(n, a, d)

def lowpass(x, cutoff):
    a = np.exp(-2 * np.pi * cutoff / SR); y = np.zeros_like(x); acc = 0.0
    for i in range(len(x)):
        acc = (1 - a) * x[i] + a * acc; y[i] = acc
    return y

music = np.zeros(N); sfx = np.zeros(N)
BPM = 120; beat = 60 / BPM
# Am - F - C - G, one bar (4 beats) each
chords = [(220.0, [220.0, 261.63, 329.63]), (174.61, [174.61, 220.0, 261.63]),
          (130.81, [261.63, 329.63, 392.0]), (196.0, [196.0, 246.94, 293.66])]
kick = (np.sin(2 * np.pi * (50 + 120 * np.exp(-np.arange(int(.25 * SR)) / SR * 30)) * np.arange(int(.25 * SR)) / SR)
        * env(int(.25 * SR), 0.001, 0.12))
snare = rng.normal(0, 1, int(.2 * SR)) * env(int(.2 * SR), 0.001, 0.06) * 0.6 + note(190, .2, "sine", .001, .05) * 0.4
hat = np.diff(rng.normal(0, 1, int(.06 * SR) + 1)) * env(int(.06 * SR), 0.001, 0.015) * 0.5
lead = [659.25, 587.33, 523.25, 587.33, 659.25, 783.99, 659.25, 523.25]

b = 0
while b * beat < TOTAL:
    t0 = b * beat; bar = (b // 4) % 4; root, chord = chords[bar]
    add(music, t0, kick, 0.9)
    if b % 4 in (1, 3): add(music, t0, snare, 0.55)
    add(music, t0, hat, 0.35); add(music, t0 + beat / 2, hat, 0.25)
    for half in (0, 1):  # bass 8ths
        add(music, t0 + half * beat / 2, lowpass(note(root / 2, beat / 2, "saw", .005, .18), 900), 0.35)
    if b % 4 == 0:  # pad chord per bar
        pad = sum(lowpass(note(f, 4 * beat, "saw", .08, 1.6), 1400) for f in chord)
        add(music, t0, pad, 0.10)
    if b % 2 == 0:  # light pluck melody
        add(music, t0, note(lead[(b // 2) % 8], beat, "square", .002, .12), 0.06)
    b += 1

# sound effects
def tick():
    n = int(.08 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 1800 * t) + 0.5 * np.sin(2 * np.pi * 2700 * t)) * env(n, .001, .015)
def ding():
    n = int(1.0 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 1318.5 * t) + 0.6 * np.sin(2 * np.pi * 1975.5 * t) + 0.3 * np.sin(2 * np.pi * 2637 * t)) * env(n, .002, .35)
def whoosh():
    n = int(.4 * SR); x = rng.normal(0, 1, n)
    sweep = np.sin(np.linspace(0, np.pi, n)) ** 2
    return lowpass(x, 2500) * sweep
def pop():
    n = int(.09 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * (400 + 900 * t / .09) * t) * env(n, .001, .03)
def boom():
    n = int(.8 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * (40 + 60 * np.exp(-t * 8)) * t) * env(n, .002, .35) + lowpass(rng.normal(0, 1, n), 600) * env(n, .001, .1) * .5

add(sfx, 0.0, boom(), 0.9)
for d in (0, .15, .3, .6, .9): add(sfx, d, pop(), 0.35)
for i, s in enumerate(ROUND_STARTS):
    add(sfx, s, whoosh(), 0.35)
    for k in range(3): add(sfx, s + 0.3 + k * 0.8, tick(), 0.55)
    add(sfx, s + 0.3 + 2.4, ding(), 0.5)
add(sfx, END_T, whoosh(), 0.35)
for d in (0, .1, .3, .6, .9): add(sfx, END_T + d, pop(), 0.3)
add(sfx, END_T + 0.3, ding(), 0.4)

# duck music slightly under the ticks/dings, fade the ends
mix = music * 0.8 + sfx
mix *= np.minimum(1, t_all / 0.05) * np.minimum(1, (TOTAL - t_all) / 0.6)
mix /= np.max(np.abs(mix)) * 1.12
stereo = np.stack([mix, mix], axis=1)
with wave.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio.wav"), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((stereo * 32767).astype(np.int16).tobytes())
print("audio", round(TOTAL, 2), "s")
