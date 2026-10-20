"""Balanço por faixa de frequência em cada trecho: referência × a sua versão.

As duas entram sem voz (separe com o separar_voz.py e use o arquivo "(other)", ou com o demucs
--two-stems vocals). Os valores saem normalizados pelo trecho do drop: o drop é a mesma música
nas duas e serve de régua. Ele tem de bater em até ~1 dB; os outros trechos mostram onde a sua
versão tem grave, médio ou brilho a mais ou a menos.

Uso: python bands.py ref_sem_voz.wav sua_sem_voz.wav --trechos trechos.json [--desloc-ref 5.95]
     trechos.json: [[0, 4, "ping"], [4, 10, "drone+cello"], [10, 16, "voz entra"],
                    [16, 34, "piano"], [34, 39.3, "risers"], [39.5, 54, "drop"]]
     (tempos da SUA versão; o último trecho precisa se chamar "drop")
     --desloc-ref: quantos segundos a referência está atrasada em relação à sua versão
"""
import sys
for _s in (sys.stdout, sys.stderr):   # acentos no terminal do Windows
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8")
import argparse, json
import librosa, numpy as np

FAIXAS = [(20, 70), (70, 250), (250, 2000), (2000, 8000), (8000, 16000)]


def analisa(arq, trechos, desloc):
    y, sr = librosa.load(arq, sr=44100, offset=desloc, duration=max(t[1] for t in trechos) + 1)
    S = np.abs(librosa.stft(y, n_fft=4096, hop_length=1024)) ** 2
    fr = librosa.fft_frequencies(sr=sr, n_fft=4096)
    t = librosa.frames_to_time(np.arange(S.shape[1]), sr=sr, hop_length=1024)
    out = {}
    for a, b, nome in trechos:
        i = (t >= a) & (t < b)
        out[nome] = [10 * np.log10(S[(fr >= lo) & (fr < hi)][:, i].sum(0).mean() + 1e-12) for lo, hi in FAIXAS]
    ref = np.mean(out["drop"])
    return {k: [x - ref for x in v] for k, v in out.items()}


ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("referencia"); ap.add_argument("sua")
ap.add_argument("--trechos", required=True)
ap.add_argument("--desloc-ref", type=float, default=0.0)
a = ap.parse_args()
trechos = json.load(open(a.trechos, encoding="utf-8"))
r, o = analisa(a.referencia, trechos, a.desloc_ref), analisa(a.sua, trechos, 0.0)
print("trecho           " + "  ".join(f"{lo}-{hi} Hz".rjust(12) for lo, hi in FAIXAS))
for k in r:
    print(f"{k:12s} REF " + " ".join(f"{x:12.1f}" for x in r[k]))
    print(f"{'':12s} SUA " + " ".join(f"{x:12.1f}" for x in o[k]))
