"""Confere uma versão da trilha: nível, pico, espectrograma ao lado da referência e um vídeo
de tela preta para ouvir (ou mandar a um modelo que ouve, como o Gemini) as duas em sequência.

Faz três coisas:
  1. mede LUFS integrado e pico (alvo: −14 LUFS, pico abaixo de −1 dBFS);
  2. salva um PNG com o espectrograma da referência em cima e o da sua versão embaixo, no mesmo
     eixo de tempo (dá para ver golpe sem grave, piano sem baixo, riser que não chega no drop);
  3. com --video, gera um MP4 de tela preta: referência → 2 s de silêncio → sua versão.

Uso: python conferir.py sua.wav [--ref referencia.wav] [--desloc-ref 5.95] [--png saida.png] [--video ab.mp4]
     --desloc-ref: em que segundo da referência começa o trecho que corresponde ao 0 da sua versão
"""
import sys
for _s in (sys.stdout, sys.stderr):   # acentos no terminal do Windows
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8")
import argparse, os, re, subprocess
import numpy as np, librosa


def lufs(arq):
    e = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", arq, "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True, errors="ignore").stderr
    t = e[e.rfind("Summary:"):]
    return float(re.search(r"I:\s+(-?[\d.]+) LUFS", t).group(1)), float(re.search(r"Peak:\s+(-?[\d.]+) dBFS", t).group(1))


def espectro(ax, arq, offset, dur, titulo):
    import librosa.display
    y, sr = librosa.load(arq, sr=22050, offset=offset, duration=dur)
    S = librosa.amplitude_to_db(np.abs(librosa.stft(y, n_fft=2048, hop_length=512)), ref=np.max)
    librosa.display.specshow(S, sr=sr, hop_length=512, x_axis="time", y_axis="log", ax=ax, vmin=-80, vmax=0)
    ax.set_title(titulo)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sua")
    ap.add_argument("--ref")
    ap.add_argument("--desloc-ref", type=float, default=0.0)
    ap.add_argument("--png")
    ap.add_argument("--video")
    a = ap.parse_args()
    i, p = lufs(a.sua)
    print(f"{a.sua}: {i:.1f} LUFS, pico {p:.1f} dBFS" + ("  <- ajuste para −14" if abs(i + 14) > 0.5 else ""))
    dur = librosa.get_duration(path=a.sua)
    if a.ref and a.png:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, axs = plt.subplots(2, 1, figsize=(16, 8), sharex=True)
        espectro(axs[0], a.ref, a.desloc_ref, dur, "referência")
        espectro(axs[1], a.sua, 0.0, dur, "sua versão")
        fig.tight_layout(); fig.savefig(a.png, dpi=110)
        print("espectrograma em", a.png)
    if a.ref and a.video:
        subprocess.run(["ffmpeg", "-y", "-v", "error",
                        "-ss", str(a.desloc_ref), "-t", str(dur), "-i", a.ref, "-i", a.sua,
                        "-f", "lavfi", "-i", "color=c=black:s=640x360:r=10",
                        "-filter_complex",
                        "[0:a]aformat=sample_rates=48000:channel_layouts=stereo[r];"
                        "[1:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay=2000|2000[s];"
                        "[r][s]concat=n=2:v=0:a=1[out]",
                        "-map", "2:v", "-map", "[out]", "-t", f"{2 * dur + 2:.2f}", "-c:v", "libx264", "-tune", "stillimage",
                        "-c:a", "aac", "-b:a", "192k", a.video], check=True)
        print("comparativo em", a.video, "(referência, 2 s de silêncio, sua versão)")


if __name__ == "__main__":
    main()
