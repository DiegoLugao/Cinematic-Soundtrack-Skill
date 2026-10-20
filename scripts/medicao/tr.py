"""Transcrição com o tempo de cada palavra (faster-whisper large-v3). Serve para achar as
palavras fortes da voz, onde entram os acordes, e os respiros, onde entra o cello.

Usa a GPU NVIDIA se houver; sem ela, roda na CPU (mais devagar).

Uso: python tr.py voz.wav [outra.wav ...] [--idioma en]
"""
import sys
for _s in (sys.stdout, sys.stderr):   # acentos no terminal do Windows
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8")
from faster_whisper import WhisperModel

args = sys.argv[1:]
idioma = None
if "--idioma" in args:
    i = args.index("--idioma")
    idioma = args[i + 1]
    del args[i:i + 2]
if not args:
    sys.exit(__doc__)
try:
    m = WhisperModel("large-v3", device="cuda", compute_type="float16")
except Exception:
    m = WhisperModel("large-v3", device="cpu", compute_type="int8")
for p in args:
    print("=====", p)
    segs, _ = m.transcribe(p, language=idioma, word_timestamps=True, vad_filter=False, beam_size=5)
    for s in segs:
        print(f"[{s.start:6.2f}-{s.end:6.2f}] " + " ".join(f"{w.word.strip()}@{w.start:.2f}" for w in s.words))
