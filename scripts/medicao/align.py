"""Acha em que ponto da música cada trecho da referência está (croma + mel, janelas de 2 s).

Serve para descobrir que parte da música a referência usa e se ela corta a voz ou usa o trecho
inteiro. Na referência do exemplo, o deslocamento ficou fixo em 14,83 s do começo ao fim:
a voz inteira, sem cortes.

Uso: python align.py referencia.wav musica.wav ini fim
     ini/fim: trecho da referência a analisar, em segundos
"""
import sys
for _s in (sys.stdout, sys.stderr):   # acentos no terminal do Windows
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8")
import librosa, numpy as np

SR, HOP = 22050, 512


def feat(p):
    y, _ = librosa.load(p, sr=SR, mono=True)
    C = librosa.feature.chroma_cqt(y=y, sr=SR, hop_length=HOP)
    M = librosa.power_to_db(librosa.feature.melspectrogram(y=y, sr=SR, hop_length=HOP, n_mels=64))
    return np.vstack([C * 3, (M - M.mean()) / M.std()])


if len(sys.argv) < 5:
    sys.exit(__doc__)
R, S = feat(sys.argv[1]), feat(sys.argv[2])
fps = SR / HOP
W = int(2 * fps)
for t0 in np.arange(float(sys.argv[3]), float(sys.argv[4]), 1.0):
    a = R[:, int(t0 * fps):int(t0 * fps) + W]
    if a.shape[1] < W:
        break
    a = (a - a.mean()) / (a.std() + 1e-9)
    melhor = (-9, 0)
    for j in range(0, S.shape[1] - W):
        b = S[:, j:j + W]
        c = (a * (b - b.mean()) / (b.std() + 1e-9)).mean()
        if c > melhor[0]:
            melhor = (c, j)
    print(f"ref {t0:5.1f} s -> música {melhor[1] / fps:6.2f} s  corr {melhor[0]:.2f}  desloc. {melhor[1] / fps - t0:+.2f} s")
