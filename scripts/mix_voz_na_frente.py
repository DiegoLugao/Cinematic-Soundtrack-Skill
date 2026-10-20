"""Mixagem final com a voz do cantor como prioridade e os tonais como complemento.

Por que existe: com um desvio fixo de volume, o acorde de piano mais o golpe ainda passavam a voz
em 2 a 5 dB em alguns trechos, e a voz "se perdia". Aqui a prioridade é dinâmica:
- os tonais (tudo que não é voz nem música) viram um bus;
- o bus é dividido em grave (< 250 Hz) e médio/agudo (>= 250 Hz, onde a voz mora);
- enquanto a voz canta, o médio/agudo do bus fica pelo menos FOLGA_DB abaixo da voz
  (até MAX_DB de redução), e o grave desce no máximo MAX_GRAVE_DB, para o piano manter o peso;
- envelopes de 50 ms, ataque de 15 ms e soltura de 300 ms;
- a música do drop não mexe.
Depois a soma volta a −14 LUFS e passa pelo limitador.

Uso: python mix_voz_na_frente.py <pasta do stems.py> <saida.wav> [pasta das camadas finais]
     opções no topo: VOZ (nome do grupo da voz) e SEM_MEXER (grupos fora do bus)
"""
import sys
for _s in (sys.stdout, sys.stderr):   # acentos no terminal do Windows
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8")
import glob, os, subprocess
import numpy as np, soundfile as sf, scipy.signal as ss

VOZ = "voz"                  # grupo da voz do cantor no plano
SEM_MEXER = ("voz", "musica")  # grupos que não entram no bus dos tonais
FOLGA_DB = 5.0               # médio/agudo dos tonais fica pelo menos isto abaixo da voz
MAX_DB = 7.0                 # redução máxima no médio/agudo
MAX_GRAVE_DB = 2.0           # redução máxima no grave
CORTE_HZ = 250
SAIDA_LUFS = -14.0
ATRASO_LIMITADOR = 239       # look-ahead do alimiter, em amostras


def env_db(x, sr, janela=0.05):
    w = int(janela * sr)
    pot = np.convolve((x ** 2).mean(1), np.ones(w) / w, "same")
    return 10 * np.log10(pot + 1e-12)


def suavizar(gr, sr, ataque=0.015, soltura=0.30):
    """gr em dB (<= 0): desce rápido (ataque), volta devagar (soltura)."""
    a, r = np.exp(-1 / (ataque * sr)), np.exp(-1 / (soltura * sr))
    out = np.empty_like(gr); v = 0.0
    for i, g in enumerate(gr):
        c = a if g < v else r
        v = c * v + (1 - c) * g
        out[i] = v
    return out


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    pasta, saida = sys.argv[1], sys.argv[2]
    final = sys.argv[3] if len(sys.argv) > 3 else None
    cam = {os.path.splitext(os.path.basename(f))[0]: sf.read(f, always_2d=True)[0]
           for f in glob.glob(os.path.join(pasta, "*.wav"))}
    if VOZ not in cam:
        sys.exit(f"não achei {VOZ}.wav em {pasta}: confira o campo \"grupo\" da voz no plano")
    sr = sf.info(os.path.join(pasta, VOZ + ".wav")).samplerate
    voz = cam[VOZ]
    n = len(voz)
    tonais = [k for k in cam if k not in SEM_MEXER]
    print("tonais no bus:", ", ".join(sorted(tonais)))
    bus = sum(cam[k][:n] for k in tonais)
    b, a = ss.butter(4, CORTE_HZ, "lowpass", fs=sr)
    grave_bus = ss.filtfilt(b, a, bus, axis=0)
    medio_bus = bus - grave_bus
    ev, em = env_db(voz, sr), env_db(medio_bus, sr)
    cantando = ev > np.percentile(ev[ev > -60], 25)
    excesso = np.where(cantando, em - (ev - FOLGA_DB), 0.0)       # quanto o médio passa da folga
    gr_med = suavizar(-np.clip(excesso, 0, MAX_DB), sr)
    gr_grv = suavizar(-np.clip(excesso * MAX_GRAVE_DB / MAX_DB, 0, MAX_GRAVE_DB), sr)
    g_med, g_grv = (10 ** (gr_med / 20))[:, None], (10 ** (gr_grv / 20))[:, None]
    saidas, soma = {}, np.zeros_like(voz)
    for nome, y in cam.items():
        y = y[:n]
        if nome in tonais:                       # mesma divisão por camada, para as camadas somarem a mix
            grv = ss.filtfilt(b, a, y, axis=0)
            y = grv * g_grv + (y - grv) * g_med
        saidas[nome] = y
        soma += y
    import pyloudnorm as pyln                     # repõe o volume que a prioridade tirou
    comp = 10 ** ((SAIDA_LUFS - pyln.Meter(sr).integrated_loudness(soma)) / 20)
    soma *= comp
    saidas = {k: v * comp for k, v in saidas.items()}
    os.makedirs(os.path.dirname(os.path.abspath(saida)), exist_ok=True)
    tmp = saida + ".bruto.wav"
    sf.write(tmp, soma, sr, subtype="FLOAT")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", tmp, "-af", "alimiter=limit=0.84:level=false",
                    "-ar", "48000", saida], check=True)
    os.remove(tmp)
    ativo = cantando & (gr_med < -0.1)
    print("redução no médio dos tonais com a voz: média %.1f dB, máx %.1f dB, em %.0f%% do canto"
          % (gr_med[ativo].mean() if ativo.any() else 0, gr_med.min(), 100 * ativo.sum() / max(1, cantando.sum())))
    print("saída", saida)
    if final:                                     # camadas finais, já com a prioridade aplicada
        os.makedirs(final, exist_ok=True)
        for nome, y in saidas.items():
            y = np.concatenate([np.zeros((ATRASO_LIMITADOR, y.shape[1])), y])[: len(y)]
            sf.write(os.path.join(final, nome + ".wav"), y, sr, subtype="PCM_24")


if __name__ == "__main__":
    main()
