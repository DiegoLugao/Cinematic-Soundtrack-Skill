"""Golpe tonal de piano ("ping") na tônica da música, feito a partir de notas soltas de piano.

Toca a tônica em duas oitavas (e a de baixo bem de leve), passa por uma catedral de 8 s
(mix 55%) e fica só no médio: passa-altas em 150 Hz e passa-baixas em 2,2 kHz. Na medição da
referência, o ping era um piano no médio, sem sub e sem brilho; um golpe com sub demais
embola com o piano dos acordes.

A catedral é sintética (ruído com decaimento de 8 s). Se você tiver uma resposta ao impulso
de que goste, passe com --ir.

Uso: python prep_ping.py saida.wav nota_media.wav nota_aguda.wav [nota_grave.wav] [--ir catedral.wav]
     ex.: para Lá menor, Lá4 + Lá5 (+ Lá3). Qualquer piano sampleado em WAV ou FLAC serve.
"""
import sys
for _s in (sys.stdout, sys.stderr):   # acentos no terminal do Windows
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8")
import argparse
import numpy as np, soundfile as sf, scipy.signal as ss

SR = 48000
GANHOS = [1.0, 0.6, 0.2]        # média, aguda, grave
MIX_CATEDRAL = 0.55


def carrega(arq):
    y, sr = sf.read(arq, always_2d=True)
    if sr != SR:
        y = ss.resample_poly(y, SR, sr, axis=0)
    if y.shape[1] == 1:
        y = np.repeat(y, 2, 1)
    return y


def ir_catedral(rt60=8.0, seed=3):
    rng = np.random.default_rng(seed)
    t = np.arange(int(rt60 * 1.1 * SR)) / SR
    canais = []
    for _ in range(2):
        x = rng.standard_normal(len(t)) * 10 ** (-3 * t / rt60)
        x *= 1 - np.exp(-t / 0.04)
        b, a = ss.butter(2, 4000, "lowpass", fs=SR)
        canais.append(ss.lfilter(b, a, x))
    ir = np.stack(canais, 1)
    ir = np.concatenate([np.zeros((int(0.03 * SR), 2)), ir])
    return ir / np.sqrt((ir ** 2).sum())


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("saida"); ap.add_argument("notas", nargs="+")
    ap.add_argument("--ir", default=None)
    a = ap.parse_args()
    camadas = [carrega(f) * g for f, g in zip(a.notas, GANHOS)]
    n = max(len(c) for c in camadas)
    seco = sum(np.pad(c, ((0, n - len(c)), (0, 0))) for c in camadas)[: int(9 * SR)]
    ir = carrega(a.ir) if a.ir else ir_catedral()
    tot = len(seco) + len(ir)
    seco = np.pad(seco, ((0, tot - len(seco)), (0, 0)))
    mol = np.stack([ss.fftconvolve(seco[:, c], ir[:, c])[:tot] for c in range(2)], 1)
    mol *= np.sqrt((seco ** 2).mean() / ((mol ** 2).mean() + 1e-12))
    out = (1 - MIX_CATEDRAL) * seco + MIX_CATEDRAL * mol
    b, c = ss.butter(2, 150, "highpass", fs=SR); out = ss.lfilter(b, c, out, axis=0)   # sem sub
    b, c = ss.butter(4, 2200, "lowpass", fs=SR); out = ss.lfilter(b, c, out, axis=0)   # sem brilho
    out = out[: int(10 * SR)]
    f = np.linspace(1, 0, int(1.5 * SR))[:, None]; out[-len(f):] *= f
    out /= np.abs(out).max() / 0.9
    sf.write(a.saida, out, SR, subtype="PCM_24")
    print("ok", a.saida)


if __name__ == "__main__":
    main()
