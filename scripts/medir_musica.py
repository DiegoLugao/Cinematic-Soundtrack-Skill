"""Tom, BPM e afinação de uma música, e o segundo exato do bumbo do drop.

- Tom: se o Essentia estiver instalado (pip install essentia; funciona no Mac e no Linux, no
  Windows pelo WSL), vota entre 5 perfis de tonalidade; com 2 votos ou menos, sai "conferir".
  Sem o Essentia, usa o librosa (perfis de Krumhansl), que erra mais: confira sempre no
  Hooktheory, no tunebat ou no songbpm. Detector de tom erra entre o tom e o relativo
  (Lá menor × Dó maior); o ouvido e as notas da melodia desempatam.
- BPM: beat tracking. Desconfie do número do Google: na música de exemplo ele dizia 134 e
  a medida deu 136.
- Afinação: desvio em cents do Lá 440. Passou de ~±20 cents, as camadas tonais vão soar
  desafinadas sobre a música (dá para corrigir o tom das camadas ou escolher outra música).
- Bumbo (--bumbo ini fim): procura, no intervalo, o maior salto de energia abaixo de 120 Hz
  em janelas de 10 ms. É ali que a música inteira entra no remix.

Uso: python medir_musica.py musica.wav [--bumbo 28 32]
"""
import sys
for _s in (sys.stdout, sys.stderr):   # acentos no terminal do Windows
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8")
import argparse
import numpy as np, librosa, scipy.signal as ss

NOTAS = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
PT = {"C": "Dó", "C#": "Dó#", "D": "Ré", "D#": "Mi♭", "E": "Mi", "F": "Fá", "F#": "Fá#", "G": "Sol",
      "G#": "Lá♭", "A": "Lá", "A#": "Si♭", "B": "Si"}
PERFIS = {  # (maior, menor): Krumhansl, Temperley e EDMA
    "krumhansl": ([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88],
                  [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]),
    "temperley": ([5, 2, 3.5, 2, 4.5, 4, 2, 4.5, 2, 3.5, 1.5, 4], [5, 2, 3.5, 4.5, 2, 4, 2, 4.5, 3.5, 2, 1.5, 4]),
    "edma": ([7.16, 3.5, 3.83, 3.81, 4.17, 5.5, 3.69, 6.44, 3.7, 4.04, 3.62, 3.9],
             [7, 3.14, 4.36, 5.4, 3.07, 4.36, 3.27, 6.31, 4.8, 3.25, 4.43, 3.5]),
}


def tom_essentia(arq):
    import essentia, essentia.standard as es
    from collections import Counter
    essentia.log.infoActive = essentia.log.warningActive = False
    audio = es.MonoLoader(filename=arq, sampleRate=44100)()
    votos = []
    for perfil in ["shaath", "edma", "bgate", "krumhansl", "noland"]:
        k, escala, _ = es.KeyExtractor(profileType=perfil, sampleRate=44100)(audio)
        k = {"Db": "C#", "Eb": "D#", "Gb": "F#", "Ab": "G#", "Bb": "A#"}.get(k, k)
        votos.append(f"{k} {'maior' if escala == 'major' else 'menor'}")
    t, n = Counter(votos).most_common(1)[0]
    bpm = float(es.RhythmExtractor2013(method="multifeature")(audio)[0])
    return t, f"{n}/5 votos" + ("  <- conferir no Hooktheory/tunebat" if n < 3 else ""), bpm


def tom_librosa(y, sr):
    """Voto entre 2 cromas (STFT e CQT) × 3 perfis de tonalidade."""
    from collections import Counter
    votos = []
    for croma in (librosa.feature.chroma_stft(y=y, sr=sr), librosa.feature.chroma_cqt(y=y, sr=sr)):
        c = croma.mean(1)
        for maior, menor in PERFIS.values():
            res = [(np.corrcoef(c, np.roll(p, i))[0, 1], f"{NOTAS[i]} {nome}")
                   for i in range(12) for nome, p in (("maior", maior), ("menor", menor))]
            votos.append(max(res)[1])
    t, n = Counter(votos).most_common(1)[0]
    outros = sorted(set(votos) - {t})
    return t, f"librosa, {n}/6 votos{'; outros: ' + ', '.join(outros) if outros else ''}  <- conferir no Hooktheory/tunebat"


def cents(y, sr):
    """Afinação: média circular do desvio dos picos espectrais em relação ao Lá 440."""
    f, _, Z = ss.stft(y, sr, nperseg=8192, noverlap=6144)
    M = np.abs(Z)
    desvios, pesos = [], []
    for col in M.T[::2]:
        if col.max() < 1e-4:
            continue
        pk, _ = ss.find_peaks(col, height=col.max() * 0.15, distance=3)
        for i in pk:
            if not (80 < f[i] < 2000) or i == 0 or i >= len(col) - 1:
                continue
            a, b, c = np.log(col[i - 1] + 1e-12), np.log(col[i] + 1e-12), np.log(col[i + 1] + 1e-12)
            fr = f[i] + 0.5 * (a - c) / (a - 2 * b + c) * (f[1] - f[0])   # interpolação parabólica
            m = 12 * np.log2(fr / 440.0)
            desvios.append(m - np.round(m)); pesos.append(col[i])
    ang = np.array(desvios) * 2 * np.pi
    return np.angle(np.sum(np.array(pesos) * np.exp(1j * ang))) / (2 * np.pi) * 100


def bumbo(arq, ini, fim):
    y, sr = librosa.load(arq, sr=22050, offset=ini, duration=fim - ini)
    b, a = ss.butter(4, 120, "lowpass", fs=sr)
    g = ss.lfilter(b, a, y)
    w = int(0.01 * sr)
    db = 20 * np.log10(np.sqrt(np.convolve(g ** 2, np.ones(w) / w, "same")) + 1e-9)
    salto = db[w:] - db[:-w]
    i = int(np.argmax(salto)) + w
    antes = db[max(0, i - 2 * w):i - w].mean()            # nível logo antes do salto
    j = i - w + int(np.argmax(db[i - w:i + 1] > antes + 6))   # primeiro instante 6 dB acima
    return ini + j / sr, float(salto.max())


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("musica")
    ap.add_argument("--bumbo", nargs=2, type=float, metavar=("INI", "FIM"))
    a = ap.parse_args()
    y, sr = librosa.load(a.musica, sr=22050, mono=True, duration=180)
    try:
        t, obs, bpm = tom_essentia(a.musica)
    except ImportError:
        t, obs = tom_librosa(y, sr)
        bpm = float(np.atleast_1d(librosa.beat.beat_track(y=y, sr=sr)[0])[0])
    nota, modo = t.split()
    i = NOTAS.index(nota)
    rel = f"{PT[NOTAS[(i + 3) % 12]]} maior" if modo == "menor" else f"{PT[NOTAS[(i - 3) % 12]]} menor"
    print(f"tom       {PT[nota]} {modo} ({nota})   relativo: {rel}   [{obs}]")
    print(f"BPM       {bpm:.1f}   (1 tempo = {60 / bpm:.3f} s, 1 compasso 4/4 = {240 / bpm:.3f} s)")
    c = cents(y, sr)
    aviso = "  <- acima de ±20: as camadas vão soar desafinadas" if abs(c) > 20 else ""
    print(f"afinação  {c:+.0f} cents em relação ao Lá 440{aviso}")
    if a.bumbo:
        s, d = bumbo(a.musica, *a.bumbo)
        print(f"bumbo     {s:.3f} s (salto de {d:.0f} dB abaixo de 120 Hz)")


if __name__ == "__main__":
    main()
