"""Ranking de candidatos pelo perfil espectral de um trecho da referência.

Para cada camada da referência (o golpe, o drone, o riser), pegue o trecho em que ela toca
quase sozinha e compare com os seus arquivos. O mais parecido no perfil de frequências sai no
topo. O ouvido decide entre os três primeiros.

Uso: python match.py referencia.wav ini fim "sons/drones/*.wav" ["outra/pasta/**/*.wav" ...]
"""
import sys
for _s in (sys.stdout, sys.stderr):   # acentos no terminal do Windows
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8")
import glob
import librosa, numpy as np


def perfil(y, sr):
    M = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=48, fmax=10000)
    p = librosa.power_to_db(M.mean(1))
    return (p - p.mean()) / p.std()


if len(sys.argv) < 5:
    sys.exit(__doc__)
a, b = float(sys.argv[2]), float(sys.argv[3])
yr, sr = librosa.load(sys.argv[1], sr=22050, offset=a, duration=b - a)
pr = perfil(yr, sr)
res = []
for padrao in sys.argv[4:]:
    for f in glob.glob(padrao, recursive=True):
        y, _ = librosa.load(f, sr=22050, duration=b - a)
        if len(y) >= sr * 0.5:
            res.append((np.corrcoef(pr, perfil(y, sr))[0, 1], f))
for r, f in sorted(res, reverse=True)[:12]:
    print(f"{r:.3f}  {f}")
