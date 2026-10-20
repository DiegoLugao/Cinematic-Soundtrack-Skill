"""Camadas separadas (stems) de um plano do trilha_momentos.py, agrupadas pelo campo "grupo" de
cada camada, com o MESMO ganho de master da mixagem completa: somadas, dão a mixagem (sem o
limitador). O mix_voz_na_frente.py usa estas camadas. Também servem para mostrar no vídeo
"camada por camada" ou montar num editor de áudio.

Uso: python stems.py ../plano-exemplo.json ../saida/stems
Sai um WAV por grupo: ping.wav, drones.wav, cello.wav, voz.wav, acordes.wav, risers.wav, musica.wav…
"""
import sys
for _s in (sys.stdout, sys.stderr):   # acentos no terminal do Windows
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8")
import json, os, subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import trilha_momentos as TM

ATRASO_LIMITADOR = 239   # o alimiter do master atrasa a mixagem em 239 amostras (5 ms de look-ahead)


def render(plano, cams, saida, ganho_master):
    total = plano["duracao"]
    cmd, filtros = ["ffmpeg", "-y", "-v", "error"], []
    for k, c in enumerate(cams):
        filtros.append(TM.filtro_camada(k, c))
        cmd += ["-i", c["arq"]]
    n = len(cams)
    filtros.append("anullsrc=r=48000:cl=stereo,atrim=duration=%s[z]" % total)
    filtros.append("[z]" + "".join(f"[c{k}]" for k in range(n)) +
                   f"amix=inputs={n + 1}:normalize=0:duration=first,volume={ganho_master:.2f}dB,"
                   f"afade=t=out:st={total - 3}:d=3[out]")
    cmd += ["-filter_complex", ";".join(filtros), "-map", "[out]", "-ar", "48000", "-c:a", "pcm_s24le", saida]
    subprocess.run(cmd, check=True)


def alinhar(arq, atraso=ATRASO_LIMITADOR):
    """A camada leva o mesmo atraso do limitador, para somar certinho com a mixagem."""
    import numpy as np, soundfile as sf
    y, sr = sf.read(arq, always_2d=True)
    y = np.concatenate([np.zeros((atraso, y.shape[1])), y])[: len(y)]
    sf.write(arq, y, sr, subtype="PCM_24")


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    plano_arq, pasta = sys.argv[1], sys.argv[2]
    plano = json.load(open(plano_arq, encoding="utf-8"))
    base = os.path.dirname(os.path.abspath(plano_arq))
    os.makedirs(pasta, exist_ok=True)
    cams = [c for c in TM.camadas(plano, base) if not c["mudo"]]
    bruto = os.path.join(pasta, "_bruto.wav")
    render(plano, cams, bruto, 0.0)
    i, _ = TM.lufs(bruto)
    g = plano.get("saida_lufs", -14) - i            # o mesmo ganho de master da mixagem completa
    os.remove(bruto)
    grupos = []
    for c in cams:
        if c["grupo"] not in grupos:
            grupos.append(c["grupo"])
    for nome in grupos:
        sel = [c for c in cams if c["grupo"] == nome]
        arq = os.path.join(pasta, nome + ".wav")
        render(plano, sel, arq, g)
        alinhar(arq)
        print(f"{nome:10s} {len(sel)} camada(s) -> {arq}")


if __name__ == "__main__":
    main()
