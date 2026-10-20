"""Envelope de energia (RMS) e brilho (centroide) passo a passo, com uma barrinha de nível.

Serve para achar o 1º golpe da referência (na do exemplo, o ping sai de −60 para −17 dB em
5,950 s), os saltos de grave dos acordes e o bumbo do drop.

Uso: python env.py audio.wav ini fim [passo em s, padrão 0.25; use 0.005 para achar um ataque]
"""
import sys
for _s in (sys.stdout, sys.stderr):   # acentos no terminal do Windows
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8")
import librosa, numpy as np

if len(sys.argv) < 4:
    sys.exit(__doc__)
a, b = float(sys.argv[2]), float(sys.argv[3])
passo = float(sys.argv[4]) if len(sys.argv) > 4 else 0.25
y, sr = librosa.load(sys.argv[1], sr=22050, offset=a, duration=b - a)
n = max(1, int(passo * sr))
for i in range(0, len(y) - n, n):
    seg = y[i:i + n]
    db = 20 * np.log10(np.sqrt((seg ** 2).mean()) + 1e-9)
    cent = f"centroide {librosa.feature.spectral_centroid(y=seg, sr=sr).mean():5.0f} Hz " if n >= 2048 else ""
    print(f"{a + i / sr:7.3f} {db:6.1f} dB  {cent}" + "#" * max(0, int((db + 60) / 1.5)))
