#!/usr/bin/env python3
"""Code-synthesised 'knowledge vibe' BGM: 100 BPM, 25 bars = 60 s, Fmaj7–Em7–Dm7–Cmaj7.
Layers: pluck arpeggio, bell hook, pad, bass, kick / snap / hat. Same grid as index.html:
bar = 2.4 s, node i starts at 4.8·i, drums 4.8–52.8, clink accent at 55.2, last chord from 57.6.
usage: music.py out.wav"""
import sys, wave
import numpy as np

SR, BPM, DUR = 48000, 100, 60.0
BEAT = 60 / BPM; BAR = 4 * BEAT
n_total = int(SR * DUR)
L = np.zeros(n_total); R = np.zeros(n_total)
rng = np.random.default_rng(7)
mid = lambda m: 440 * 2 ** ((m - 69) / 12)

CHORDS = [[53, 57, 60, 64], [52, 55, 59, 62], [50, 53, 57, 60], [48, 52, 55, 59]]  # Fmaj7 Em7 Dm7 Cmaj7
ROOTS = [41, 40, 38, 36]


def add(sig, t, gain=1.0, pan=0.0):
    i = int(t * SR)
    if i >= n_total: return
    sig = sig[: n_total - i] * gain
    L[i:i + len(sig)] += sig * np.sqrt(0.5 * (1 - pan)) * 1.414
    R[i:i + len(sig)] += sig * np.sqrt(0.5 * (1 + pan)) * 1.414


def tt(sec): return np.arange(int(sec * SR)) / SR


def pluck(f, sec=0.9):  # marimba-ish: fundamental + 4th partial, fast decay
    x = tt(sec); e = np.exp(-x * 7) * np.minimum(1, x / 0.002)
    return (np.sin(2 * np.pi * f * x) + 0.35 * np.sin(2 * np.pi * f * 4.0 * x) * np.exp(-x * 25)) * e


def bell(f, sec=1.6):
    x = tt(sec); e = np.exp(-x * 2.8) * np.minimum(1, x / 0.003)
    return (np.sin(2 * np.pi * f * x) + 0.4 * np.sin(2 * np.pi * f * 2.76 * x) * np.exp(-x * 6) + 0.2 * np.sin(2 * np.pi * f * 5.4 * x) * np.exp(-x * 12)) * e


def pad(freqs, sec):
    x = tt(sec); e = np.minimum(1, x / 0.35) * np.minimum(1, (sec - x) / 0.4)
    s = np.zeros_like(x)
    for f in freqs:
        for det in (-0.12, 0.12):
            ff = f * 2 ** (det / 12)
            for h in range(1, 6):
                s += np.sin(2 * np.pi * ff * h * x + h) / h ** 1.6
    return s * e / (len(freqs) * 4)


def bass(f, sec):
    x = tt(sec); e = np.minimum(1, x / 0.01) * np.exp(-x * 1.6)
    return (np.sin(2 * np.pi * f * x) + 0.25 * np.sin(2 * np.pi * f * 2 * x)) * e


def kick():
    x = tt(0.45); f = 50 + 110 * np.exp(-x * 28)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x * 9)


def snap():
    x = tt(0.25); n = rng.standard_normal(len(x)); n = np.diff(n, prepend=0)
    return (n * 0.5 * np.exp(-x * 30) + np.sin(2 * np.pi * 1800 * x) * np.exp(-x * 60) * 0.4)


def hat():
    x = tt(0.08); n = np.diff(rng.standard_normal(len(x)), prepend=0)
    return n * np.exp(-x * 70) * 0.35


HOOK = [(0, 72), (1.5, 76), (2, 74), (3, 79), (4, 77), (5.5, 76), (6, 74), (7, 72)]  # beats within 2 bars

bars = int(DUR / BAR) + 1
for b in range(bars):
    t0 = b * BAR
    if t0 >= DUR: break
    ch, root = CHORDS[b % 4], ROOTS[b % 4]
    final = b >= 24
    if final:  # last chord rings out (Cmaj9)
        add(pad([mid(m) for m in [48, 52, 55, 59, 62]], DUR - t0), t0, 0.5)
        add(bell(mid(84), 2.4), t0, 0.25, 0.2)
        add(bass(mid(36), 2.4), t0, 0.5)
        continue
    add(pad([mid(m) for m in ch], BAR + 0.1), t0, 0.32 if b < 2 else 0.4)
    # arpeggio in 8ths, an octave up, alternating pan
    pat = [0, 1, 2, 3, 2, 1, 2, 3]
    for k, p in enumerate(pat):
        add(pluck(mid(ch[p] + 12)), t0 + k * BEAT / 2, 0.18 if b < 2 else 0.22, -0.35 if k % 2 else 0.35)
    if b >= 2:
        add(bass(mid(root), BEAT * 1.5), t0, 0.55)
        add(bass(mid(root), BEAT * 1.0), t0 + 2.5 * BEAT, 0.4)
    drums = 2 <= b < 22
    if drums:
        for k in range(4):
            if k in (0, 2): add(kick(), t0 + k * BEAT, 0.8)
            if k in (1, 3): add(snap(), t0 + k * BEAT, 0.35, 0.1)
        add(kick(), t0 + 3.5 * BEAT, 0.45)
        for k in range(8): add(hat(), t0 + k * BEAT / 2, 0.5 if k % 2 else 0.25, 0.3)
    if 4 <= b < 22 and b % 2 == 0:  # bell hook every 2 bars
        for beat, m in HOOK: add(bell(mid(m)), t0 + beat * BEAT, 0.16, -0.15)
    if b in (22, 23):  # outro: soft kick only on the clink downbeat
        if b == 23: add(kick(), t0, 0.6)

# ducking on every kick beat (vibe pump), only while drums run
x = np.arange(n_total) / SR
phase = (x % (2 * BEAT)) / (2 * BEAT)
duck = 1 - 0.25 * np.exp(-phase * 2 * BEAT * 9) * ((x >= 2 * BAR) & (x < 22 * BAR))
L *= duck; R *= duck

# small room reverb via FFT convolution with decaying noise
ir_len = int(0.9 * SR); irx = np.arange(ir_len) / SR
for ch, seed in ((L, 1), (R, 2)):
    ir = np.random.default_rng(seed).standard_normal(ir_len) * np.exp(-irx * 5.5); ir[0] = 0
    nfft = 1 << (n_total + ir_len).bit_length()
    wet = np.fft.irfft(np.fft.rfft(ch, nfft) * np.fft.rfft(ir, nfft), nfft)[:n_total]
    ch += wet * 0.035

# fade out tail
fade = np.minimum(1, (DUR - x) / 1.5); L *= fade; R *= fade
st = np.stack([L, R], 1); st /= np.max(np.abs(st)) / 0.89
with wave.open(sys.argv[1], "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype(np.int16).tobytes())
print(sys.argv[1])
