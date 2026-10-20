"""Acordes de um arquivo de progressão (moldes maior e menor sobre o croma, um por ataque).

Serve para saber a ordem dos acordes de um arquivo de progressão de piano e onde começa cada
um, antes de fatiar. Também funciona num trecho da música (melhor sem a voz).

Uso: python chords.py progressao.wav
"""
import sys
for _s in (sys.stdout, sys.stderr):   # acentos no terminal do Windows
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8")
import librosa, numpy as np

if len(sys.argv) < 2:
    sys.exit(__doc__)
N = "C C# D D# E F F# G G# A A# B".split()
T = {}
for r in range(12):
    for q, iv in (("", (0, 4, 7)), ("m", (0, 3, 7))):
        v = np.zeros(12); v[[(r + i) % 12 for i in iv]] = 1
        T[N[r] + q] = v / np.linalg.norm(v)
y, sr = librosa.load(sys.argv[1], sr=22050)
on = list(librosa.onset.onset_detect(y=y, sr=sr, units="time", backtrack=True, delta=0.25)) + [len(y) / sr]
C = librosa.feature.chroma_cqt(y=y, sr=sr, hop_length=512, bins_per_octave=36)
t = librosa.times_like(C, sr=sr, hop_length=512)
rms = librosa.feature.rms(y=y, hop_length=512)[0]
for a, b in zip(on[:-1], on[1:]):
    if b - a < 0.4:
        continue
    i = (t >= a) & (t < min(b, a + 1.5))
    v = C[:, i].mean(1); v = v / np.linalg.norm(v)
    melhor = sorted(((float(v @ T[k]), k) for k in T), reverse=True)[:2]
    print(f"{a:6.2f}-{b:6.2f} s  {melhor[0][1]:4s}({melhor[0][0]:.2f})  2º {melhor[1][1]}({melhor[1][0]:.2f})"
          f"  rms {20 * np.log10(rms[i].mean() + 1e-9):.0f} dB")
