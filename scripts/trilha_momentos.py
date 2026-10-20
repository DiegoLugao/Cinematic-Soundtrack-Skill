"""Trilha montada por momentos: golpe tonal, drones, melodia, acordes, risers e a música real
entrando no drop, tudo no mesmo tom. Lê um plano JSON e mixa tudo com ffmpeg.

Plano (exemplo completo em ../plano-exemplo.json):
{
  "duracao": 58,
  "saida_lufs": -14,
  "tom": "A",                       # troca o {tom} nos nomes de arquivo
  "camadas": [
    {"arquivo": "sons/impacto-{tom}.wav", "papel": "golpe", "em": 39.37, "golpe": true},
    {"arquivo": "sons/riser-{tom}.wav", "papel": "riser", "pico_em": 39.37, "subida": 5},
    {"arquivo": "sons/drone-{tom}.wav", "papel": "drone", "em": 2.5, "ate": 39.37, "fade_in": 4},
    {"arquivo": "sons/cello-{nota}.wav", "nota": "C", "papel": "melodia", "em": 4.2, "ate": 10.6},
    {"arquivo": "musica/musica.wav", "papel": "musica", "corte": 30.42, "ataque": 0.065, "em": 39.37}
  ]
}

Campos de cada camada:
  "arquivo"     caminho relativo à pasta do plano (ou absoluto). {tom} vira o "tom" do plano;
                {nota} vira a "nota" da camada (ex.: o relativo maior) ou, sem ela, o "tom".
  "papel"       golpe | drone | melodia | acordes | riser | voz | musica (define o nível padrão)
  "grupo"       nome do grupo para o stems.py (ping, drones, cello, voz, acordes, risers, musica)
  "em"          segundo em que a camada começa na trilha
  "corte"       segundo do arquivo em que a camada começa ("metade" = meio do arquivo)
  "ate"         segundo da trilha em que a camada termina
  "golpe": true o pico do arquivo cai exatamente em "em" (pula a subida em reverso)
  "pico_em" + "subida"  riser: só os últimos "subida" segundos antes do pico, com o pico em "pico_em"
  "sync_s"      segundo do pico dentro do arquivo; sem ele, o script mede (maior RMS em 50 ms)
  "ataque"      segundos entre o "corte" e o bumbo (o bumbo cai em "em"); serve para a música do drop
  "a_partir_de" começa a camada nesse ponto da trilha (o resto do cálculo igual)
  "tempo": 1.25 acelera o trecho sem mudar o tom
  "passa_altas": 60   tira o sub de um golpe que cai junto do bumbo da música
  "filtro"      filtro livre do ffmpeg, ex.: "lowpass=f=2500,equalizer=f=180:t=q:w=1:g=1.5"
  "lufs_alvo"   nível da camada antes do master; o padrão vem de ALVO pelo papel
  "ganho_db"    ajuste fino por cima do lufs_alvo
  "fade_in", "fade_out", "mudo"
  Chaves que começam com "_" são comentários e o script ignora.

Uso: python trilha_momentos.py plano.json saida.wav
"""
import sys
for _s in (sys.stdout, sys.stderr):   # acentos no terminal do Windows
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8")
import json, os, re, subprocess

import numpy as np
import soundfile as sf

# LUFS de cada papel antes do master, relativos à música real em −14
ALVO = {"golpe": -16, "drone": -25, "loop-ritmico": -21, "melodia": -22, "acordes": -22,
        "riser": -19, "voz": -16, "musica": -14}
_cache = {}


def lufs(arquivo, inicio=0.0, dur=None):
    cmd = ["ffmpeg", "-hide_banner", "-nostats", "-ss", str(inicio)]
    if dur:
        cmd += ["-t", str(dur)]
    cmd += ["-i", arquivo, "-af", "ebur128=peak=true", "-f", "null", "-"]
    e = subprocess.run(cmd, capture_output=True, text=True, errors="ignore").stderr
    t = e[e.rfind("Summary:"):]
    return float(re.search(r"I:\s+(-?[\d.]+) LUFS", t).group(1)), float(re.search(r"Peak:\s+(-?[\d.]+) dBFS", t).group(1))


def info(arq):
    """Duração, nível do arquivo inteiro e segundo do pico (maior RMS em janelas de 50 ms)."""
    if arq not in _cache:
        y, sr = sf.read(arq, always_2d=True)
        m = (y ** 2).mean(1)
        w = max(1, int(0.05 * sr))
        rms = np.convolve(m, np.ones(w) / w, "same")
        _cache[arq] = {"dur": len(y) / sr, "lufs": lufs(arq)[0], "sync_s": float(np.argmax(rms) / sr)}
    return _cache[arq]


def resolve(plano, c, base):
    nome = c["arquivo"].replace("{tom}", plano.get("tom", "")).replace("{nota}", c.get("nota", plano.get("tom", "")))
    return nome if os.path.isabs(nome) else os.path.normpath(os.path.join(base, nome))


def camadas(plano, base="."):
    """Resolve cada camada do plano: arquivo, trecho, posição, ganho, processamento e fades."""
    total = plano["duracao"]
    res = []
    for k, c in enumerate(plano["camadas"]):
        arq = resolve(plano, c, base)
        if not os.path.exists(arq):
            sys.exit(f"arquivo não encontrado: {arq}")
        papel = c.get("papel", "musica")
        m = info(arq)
        sync = c.get("sync_s", m["sync_s"])
        corte = c.get("corte", 0.0)
        if corte == "metade":
            corte = m["dur"] / 2
        em = c.get("em", 0.0) - c.get("ataque", 0.0)
        if c.get("golpe"):                          # o pico cai em "em": pula a subida em reverso
            corte, em = max(0.0, sync - 0.02), c["em"]
        if c.get("golpe_com_subida"):               # o pico cai em "em", com a subida em reverso antes
            corte, em = 0.0, c["em"] - sync
        if "pico_em" in c:                          # riser: só os últimos "subida" s antes do pico
            corte = max(0.0, sync - c.get("subida", 3.0))
            em = c["pico_em"] - (sync - corte)
        ate = c.get("ate", min(total, em + m["dur"] - corte))
        if "pico_em" in c and "ate" not in c:
            ate = c["pico_em"] + 0.25
        if "a_partir_de" in c:                      # corta o começo da camada (ex.: recomeçar com fade-in)
            d = c["a_partir_de"] - em
            corte, em = corte + d * c.get("tempo", 1.0), c["a_partir_de"]
        dur = max(0.05, ate - em)
        if papel in ("musica", "voz"):              # música e voz: mede o trecho que toca
            nivel, _ = lufs(arq, corte, min(20, dur))
        else:                                        # tonais: mede o arquivo inteiro
            nivel = m["lufs"]
        ganho = c.get("lufs_alvo", ALVO.get(papel, -20)) - nivel + c.get("ganho_db", 0.0)
        fator = c.get("tempo", 1.0)
        proc = []
        if fator != 1.0:
            proc.append(f"atempo={fator}")
        if c.get("passa_altas"):
            proc.append(f"highpass=f={c['passa_altas']}:poles=2")
        if c.get("filtro"):
            proc.append(c["filtro"])
        res.append({"k": k, "arq": arq, "papel": papel, "grupo": c.get("grupo", papel),
                    "nome": os.path.splitext(os.path.basename(arq))[0], "corte": corte, "em": em, "ate": ate,
                    "dur": dur, "ganho": ganho, "fator": fator, "proc": proc,
                    "fi": c.get("fade_in", 0.02), "fo": c.get("fade_out", 0.0 if papel == "golpe" else 0.12),
                    "mudo": c.get("mudo", False)})
    return res


def filtro_camada(k, c):
    f = (f"[{k}:a]atrim=start={c['corte']:.3f}:duration={c['dur'] * c['fator']:.3f},asetpts=PTS-STARTPTS,"
         f"aformat=sample_rates=48000:channel_layouts=stereo,volume={c['ganho']:.1f}dB")
    for pr in c["proc"]:
        f += "," + pr
    if c["fi"]:
        f += f",afade=t=in:d={c['fi']}"
    if c["fo"]:
        f += f",afade=t=out:st={max(0.0, c['dur'] - c['fo']):.3f}:d={c['fo']}"
    ms = int(round(max(0.0, c["em"]) * 1000))
    return f + f",adelay={ms}|{ms}[c{k}]"


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    plano_arq, saida = sys.argv[1], sys.argv[2]
    plano = json.load(open(plano_arq, encoding="utf-8"))
    base = os.path.dirname(os.path.abspath(plano_arq))
    total = plano["duracao"]
    os.makedirs(os.path.dirname(os.path.abspath(saida)), exist_ok=True)
    entradas, filtros = [], []
    for k, c in enumerate([c for c in camadas(plano, base) if not c["mudo"]]):
        entradas.append(c["arq"])
        filtros.append(filtro_camada(k, c))
        print(f"{c['papel']:9s} {c['nome'][:36]:36s} {c['em']:6.2f}–{c['ate']:6.2f}s  ganho {c['ganho']:+.1f} dB")
    n = len(entradas)
    # base de silêncio com a duração exata da trilha: o amix termina junto com ela
    filtros.append(f"anullsrc=r=48000:cl=stereo,atrim=duration={total}[z]")
    filtros.append("[z]" + "".join(f"[c{k}]" for k in range(n)) +
                   f"amix=inputs={n + 1}:normalize=0:duration=first[out]")
    tmp = saida + ".bruto.wav"
    cmd = ["ffmpeg", "-y", "-v", "error"]
    for a in entradas:
        cmd += ["-i", a]
    cmd += ["-filter_complex", ";".join(filtros), "-map", "[out]", "-ar", "48000", "-c:a", "pcm_f32le", tmp]
    subprocess.run(cmd, check=True)
    # master: ganho fixo até o alvo (preserva a dinâmica entre os momentos) + limitador
    i, _ = lufs(tmp)
    g = plano.get("saida_lufs", -14) - i
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", tmp, "-af",
                    f"volume={g:.2f}dB,alimiter=limit=0.84:level=false,afade=t=out:st={total - 3}:d=3",
                    "-ar", "48000", saida], check=True)
    os.remove(tmp)
    print("saída", saida, "LUFS/pico", lufs(saida))


if __name__ == "__main__":
    main()
