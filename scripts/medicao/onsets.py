"""Ataques (onsets) num intervalo: onde cada golpe, acorde ou palavra começa.

Uso: python onsets.py audio.wav ini fim [sensibilidade, padrão 0.3; menor = mais ataques]
"""
import sys
for _s in (sys.stdout, sys.stderr):   # acentos no terminal do Windows
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8")
import librosa

if len(sys.argv) < 4:
    sys.exit(__doc__)
ini, fim = float(sys.argv[2]), float(sys.argv[3])
y, sr = librosa.load(sys.argv[1], sr=22050, offset=ini, duration=fim - ini)
o = librosa.onset.onset_detect(y=y, sr=sr, units="time", backtrack=True,
                               delta=float(sys.argv[4]) if len(sys.argv) > 4 else 0.3)
print(" ".join(f"{ini + t:.2f}" for t in o))
