"""Nota dominante por janela (croma): a harmonia de um trecho segundo a segundo.

Na referência do exemplo, foi assim que saiu a sequência de acordes Lám-Sol-Fá-Sol-Lám-Sol.

Uso: python chromat.py audio.wav ini dur [passo em s, padrão 1]
"""
import sys
for _s in (sys.stdout, sys.stderr):   # acentos no terminal do Windows
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8")
import librosa, numpy as np

if len(sys.argv) < 4:
    sys.exit(__doc__)
ini, dur = float(sys.argv[2]), float(sys.argv[3])
passo = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
y, sr = librosa.load(sys.argv[1], sr=22050, offset=ini, duration=dur)
C = librosa.feature.chroma_cqt(y=y, sr=sr, hop_length=1024)
t = librosa.times_like(C, sr=sr, hop_length=1024)
rms = librosa.feature.rms(y=y, hop_length=1024)[0]
N = "C C# D D# E F F# G G# A A# B".split()
s = []
for a in np.arange(0, dur, passo):
    i = (t >= a) & (t < a + passo)
    v = C[:, i].mean(1)
    segunda = "/" + N[np.argsort(v)[-2]] if np.sort(v)[-2] > 0.7 else ""
    s.append(f"{ini + a:.0f}:{N[v.argmax()]}{segunda}({20 * np.log10(rms[i].mean() + 1e-9):.0f})")
print(" ".join(s))
