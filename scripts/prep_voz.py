"""Voz do cantor para a intro: o trecho da voz separada + reverb de sala de concerto, sem plugin.

O reverb é uma réplica de um ValhallaVintageVerb no preset Concert Hall, feita com uma resposta ao
impulso sintética (ruído estéreo com decaimento por faixa) e um chorus leve só na cauda:
  Decay 4 s no médio · graves 1,5× mais longos abaixo de 700 Hz · agudos curtos acima de 6 kHz
  Predelay 20 ms · ataque lento (Concert Hall) · cauda escura (5,5 kHz) · modulação 2,53 Hz
  Mix 40,7% (seco 0,593 + molhado 0,407, o molhado na mesma energia do seco)
Mais −1,5 dB em 3,8 kHz na voz seca, para ficar menos áspera.

O que os testes mostraram: 50% com catedral = eco demais; 10 a 20% = "a capela demais".
Com ~40%, o eco fica uns 5 dB abaixo da voz.

Uso: python prep_voz.py voz.wav saida.wav --ini 1.0 --fim 31.0 [--mix 0.407]
     --ini/--fim: segundos da música (a voz separada fica alinhada com ela) do trecho que vai na intro
"""
import sys
for _s in (sys.stdout, sys.stderr):   # acentos no terminal do Windows
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8")
import argparse
import numpy as np, soundfile as sf, scipy.signal as ss
from pedalboard import Pedalboard, Chorus, PeakFilter

DECAY = 4.0                   # RT60 do médio (s)
BASS_FREQ, BASS_MULT = 700, 1.5
HIGH_FREQ = 6000              # acima disso o decaimento é bem mais curto
HIGH_DECAY = 1.2
PREDELAY = 0.020
ATTACK = 0.06                 # Concert Hall: ataque lento, pouca densidade no começo
HIGH_CUT = 5500               # cauda escura


def ir_concert_hall(sr, seed=7):
    rng = np.random.default_rng(seed)
    n = int((DECAY * BASS_MULT + 0.5) * sr)
    t = np.arange(n) / sr
    canais = []
    for _ in range(2):                                   # estéreo descorrelacionado
        ruido = rng.standard_normal(n)
        b, a = ss.butter(4, BASS_FREQ, "lowpass", fs=sr); graves = ss.lfilter(b, a, ruido)
        b, a = ss.butter(4, [BASS_FREQ, HIGH_FREQ], "bandpass", fs=sr); medios = ss.lfilter(b, a, ruido)
        b, a = ss.butter(4, HIGH_FREQ, "highpass", fs=sr); agudos = ss.lfilter(b, a, ruido)
        dec = lambda rt: 10 ** (-3 * t / rt)             # −60 dB em rt segundos
        x = graves * dec(DECAY * BASS_MULT) + medios * dec(DECAY) + agudos * dec(HIGH_DECAY) * 0.35
        x *= 1 - np.exp(-t / ATTACK)                     # ataque lento
        b, a = ss.butter(4, HIGH_CUT, "lowpass", fs=sr)  # cor escura
        canais.append(ss.lfilter(b, a, x))
    ir = np.stack(canais, 1)
    ir = np.concatenate([np.zeros((int(PREDELAY * sr), 2)), ir])
    return ir / np.sqrt((ir ** 2).sum())


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("voz"); ap.add_argument("saida")
    ap.add_argument("--ini", type=float, default=0.0)
    ap.add_argument("--fim", type=float, default=None)
    ap.add_argument("--mix", type=float, default=0.407)
    a = ap.parse_args()
    y, sr = sf.read(a.voz, always_2d=True)
    if y.shape[1] == 1:
        y = np.repeat(y, 2, 1)
    y = y[int(a.ini * sr): int(a.fim * sr) if a.fim else None]
    y = Pedalboard([PeakFilter(cutoff_frequency_hz=3800, gain_db=-1.5, q=1.0)])(
        y.T.astype(np.float32), sr).T.astype(np.float64)
    ir = ir_concert_hall(sr)
    wet = np.stack([ss.fftconvolve(y[:, c], ir[:, c])[: len(y)] for c in range(2)], 1)
    wet = Pedalboard([Chorus(rate_hz=2.53, depth=0.15, centre_delay_ms=7.0, feedback=0.0, mix=0.5)])(
        wet.T.astype(np.float32), sr).T                  # modulação leve só na cauda
    wet *= np.sqrt((y ** 2).mean() / ((wet ** 2).mean() + 1e-12))   # molhado na mesma energia do seco
    out = (1 - a.mix) * y + a.mix * wet
    out /= max(1.0, np.abs(out).max() / 0.98)
    sf.write(a.saida, out, sr, subtype="PCM_24")
    print("ok", a.saida, f"{len(out) / sr:.1f} s, mix {a.mix:.0%}")


if __name__ == "__main__":
    main()
