"""Sequência de notas de uma melodia (pyin): para conferir a melodia de cello, a voz ou um riser.

Uso: python notes.py audio.wav [segundos, padrão 60]
"""
import sys
for _s in (sys.stdout, sys.stderr):   # acentos no terminal do Windows
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8")
import librosa, numpy as np

if len(sys.argv) < 2:
    sys.exit(__doc__)
dmax = float(sys.argv[2]) if len(sys.argv) > 2 else 60
y, sr = librosa.load(sys.argv[1], sr=22050, duration=dmax)
f0, v, _ = librosa.pyin(y, fmin=55, fmax=900, sr=sr, frame_length=2048, hop_length=512)
t = librosa.times_like(f0, sr=sr, hop_length=512)
out, cur, st = [], None, 0
for i in range(len(f0)):
    n = librosa.hz_to_note(f0[i], unicode=False) if v[i] and not np.isnan(f0[i]) else None
    if n != cur:
        if cur and t[i] - st > 0.18:
            out.append(f"{st:.1f}:{cur}")
        cur, st = n, t[i]
print(" ".join(out))
