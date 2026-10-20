"""Separa a voz da música com o MelBand RoFormer Big Beta 4 (audio-separator).

No teste cego (mesma frase, notas de 0 a 10), ele venceu as outras opções:
  MelBand RoFormer Big Beta 4 ......... 8,5
  média Big Beta 4 + MelBand Kim ...... 6,5 (oca e metálica)
  MelBand RoFormer Kim ................ 6
  htdemucs_ft (demucs) ................ 5 (abafada)
  acapella baixada do YouTube ......... 4 ("oca, subaquática")
Por isso a voz sai da própria música, e não de uma acapella da internet.

O audio-separator precisa de um ambiente Python 3.11 próprio (no 3.14 uma dependência não compila).
Este script procura o executável nesta ordem:
  1. a variável de ambiente AUDIO_SEPARATOR (caminho completo do executável);
  2. o ambiente ../.venv-separador ao lado da pasta scripts (como o README ensina a criar);
  3. o comando "audio-separator" no PATH.
O modelo (~1,5 GB) baixa sozinho na primeira vez, para a pasta MODELOS abaixo.

Uso: python separar_voz.py musica.wav voz.wav [--ini 0] [--dur 50]
     --ini/--dur: trecho da música a separar (o resto é ignorado; separar só o que vai usar é mais rápido)
Saída: voz.wav alinhada com a música a partir de --ini (o segundo 0 da voz = o segundo --ini da música).
"""
import sys
for _s in (sys.stdout, sys.stderr):   # acentos no terminal do Windows
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8")
import argparse, glob, os, shutil, subprocess, tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
MODELO = "melband_roformer_big_beta4.ckpt"
MODELOS = os.path.join(AQUI, "..", "modelos")     # ajuste se quiser guardar os modelos em outro lugar


def executavel():
    if os.environ.get("AUDIO_SEPARATOR"):
        return os.environ["AUDIO_SEPARATOR"]
    venv = os.path.join(AQUI, "..", ".venv-separador")
    for c in (os.path.join(venv, "Scripts", "audio-separator.exe"), os.path.join(venv, "bin", "audio-separator")):
        if os.path.exists(c):
            return c
    achado = shutil.which("audio-separator")
    if achado:
        return achado
    sys.exit("audio-separator não encontrado. Veja o passo 3 do README da pasta 2-projeto.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("musica"); ap.add_argument("saida")
    ap.add_argument("--ini", type=float, default=0.0)
    ap.add_argument("--dur", type=float, default=50.0)
    a = ap.parse_args()
    os.makedirs(MODELOS, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        trecho = os.path.join(tmp, "trecho.wav")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(a.ini), "-t", str(a.dur), "-i", a.musica, trecho],
                       check=True)
        subprocess.run([executavel(), trecho, "-m", MODELO, "--model_file_dir", os.path.abspath(MODELOS),
                        "--output_dir", tmp, "--output_format", "WAV"], check=True)
        vozes = glob.glob(os.path.join(tmp, "*(vocals)*.wav")) or glob.glob(os.path.join(tmp, "*(Vocals)*.wav"))
        if not vozes:
            sys.exit("o separador não gerou o arquivo (vocals). Veja a saída acima.")
        shutil.copy(vozes[0], a.saida)
    print("voz em", a.saida)


if __name__ == "__main__":
    main()
