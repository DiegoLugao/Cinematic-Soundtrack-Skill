---
name: trilha-cinematografica
author: "@iamjeff.ia"
source: "https://www.instagram.com/iamjeff.ia/"
description: "Creates a cinematic version of a real song with Claude Code: measures key, BPM, tuning, and the drop kick; separates the vocal from the song itself (MelBand RoFormer Big Beta 4 via audio-separator); surrounds it with in-key tonal effects (hit, drones, call-and-response cello, piano chords sliced onto stressed words, and two risers peaking at the drop); gives the vocal concert-hall reverb (~40%); keeps the vocal above the tonal layers; and mixes to −14 LUFS using Python scripts and ffmpeg. Use when asked for a cinematic soundtrack, trailer-style remix, cinematic intro built around a song, 'make this song more cinematic,' tonal effects in the song's key, a build-up to the drop, or a 'normal sound vs. cinematic sound' comparison."
---

# Cinematic soundtrack built around a real song

The intro opens with the singer's vocal almost alone, carrying concert-hall ambience. In-key tonal effects surround and complement the vocal without competing with it. Everything builds to the drop, where the intro cuts cleanly and the full song enters on the kick. Nothing is played by hand: measure the song, write a JSON plan, and use the scripts in `scripts/` to build the mix with ffmpeg. The approved example is the intro to "Laugh Now Cry Later," using `examples/example-plan.json`.

## Before you begin

1. **Define what "done" means.** Confirm the use case (Reel, long-form video opener, film), intro duration, whether narration follows the drop, and the deliverables (final WAV, separate stems, and a "normal sound" version for comparison).
2. **Tools.** `ffmpeg` on PATH; Python with `numpy scipy soundfile librosa pyloudnorm pedalboard matplotlib`; and `audio-separator` in its own Python 3.11 environment (one dependency does not compile on 3.14). Check with `ffmpeg -version`, then run a script without arguments to display its usage.
3. **Sounds.** Ask where the user's sounds are stored and list the available options for each role (see the table below) in the song's key. Tonal sounds are often supplied in all 12 keys; use the file in the correct key. If a role is missing, identify it and propose the closest substitute.

## Process

1. **Song and moment.** Choose a strong vocal phrase before a beat entrance. For short-form video: about 13 s before the vocal, with the drop around 22 s. In the example, the vocal begins at 9.9 s and the drop lands at 39.37 s.
2. **Measure.** `scripts/medir_musica.py musica.wav --bumbo INI FIM` → key, relative key, BPM, meter, tuning, and the kick timestamp. Automatic key detection can be wrong, especially when choosing between a key and its relative key: confirm with Hooktheory, TuneBat, or the melody notes (`medicao/notes.py`). Tuning offsets beyond ±20 cents will make any tonal layer sound out of tune. Google's BPM can also be wrong (example: Google reports 134; measurement gives 136).
3. **Separate the vocal from the song itself.** `scripts/separar_voz.py musica.wav prep/voz.wav --dur 50`. Never use an acapella downloaded from the internet: in a blind test, Big Beta 4 scored 8.5, while the YouTube acapella scored 4 ("hollow, underwater").
4. **Choose sounds by role and key** (`references/en/roles-sounds-and-key.md`). When a reference exists, rank candidates with `medicao/match.py`, then choose by ear from the top three.
5. **Timing.** Find words and breaths with `medicao/tr.py`; harmony with `medicao/chromat.py`; and each chord's exact onset from low-frequency jumps (`medicao/env.py` with a 5–10 ms step). Build the layer table (time, layer, role, level) and show it before mixing.
6. **Plan.** Copy `examples/example-plan.json`, then replace the times and files. Field definitions are in `references/en/approved-recipe-v11.md` and at the top of `scripts/trilha_momentos.py`. Draft render: `trilha_momentos.py plano.json saida/rascunho.wav`.
7. **Vocal.** `prep_voz.py voz.wav prep/voz-reverb.wav --ini --fim` (4 s Concert Hall, 0.407 mix).
8. **Mix with the vocal in front.** Run `stems.py plano.json saida/stems`, then `mix_voz_na_frente.py saida/stems saida/final.wav saida/camadas`. Output is −14 LUFS with peaks below −1 dBFS.
9. **Validate** (`references/en/measurement-and-validation.md`). Use `conferir.py` to compare the spectrogram against the reference and generate an A/B listening video; use `medicao/bands.py` to inspect the balance by frequency band. Measure before blaming an effect.
10. **Deliver.** Provide the final WAV, stems, the plan used, and one line stating the song, key, BPM, and what changed relative to the example.

## Layer roles

| Role | Placement | Pre-master level (example) |
|---|---|---|
| Tonal hit (piano ping on the tonic, midrange only) | First frame; accent on the first and last chords; drop | −21 / −25 / −26 / −21 LUFS |
| Two drones or textures in key | 2.5 s through the drop, with 4–4.5 s fade-ins | −26 and −28 |
| Cello in the relative major | Call alone before the vocal; response in the breath | −22 and −26 |
| Singer's vocal with reverb | First phrase through the drop | −16 |
| Piano chords in the relative major, sliced | First beat of each bar, on a stressed word, following the harmony | −17 |
| Two risers | Start about 5.1 and 3.7 s before; peak exactly at the drop | −16 and −17.5 |
| Tonal impact without sub (60 Hz high-pass) | At the drop | −20 |
| Full song | Dry, on the drop kick | −11.5 |

## Non-negotiable rules

- **The vocal is the priority; tonal layers are complementary.** While the singer is active, keep the tonal layers' midrange (≥ 250 Hz) at least 5 dB below the vocal, with up to 7 dB of reduction, while reducing the low end by no more than 2 dB. A fixed offset is not enough.
- **Sung-vocal reverb:** Concert Hall, 4 s, 20 ms predelay, ~40% mix, with the echo about 5 dB below the vocal. A 50% cathedral treatment produces too much echo; 10–20% sounds "too a cappella." Narration over the video remains dry.
- **Key:** every layer must fit the song's notes. A minor-key song can use minor sounds in its key, major sounds in its relative major, and sounds compatible with both modes. Never place major over minor on the same tonic, or vice versa.
- **Cello only in the gaps.** Never place it over a sung phrase.
- **Chords on the bar.** Place each slice on beat 1, aligned with a word, using the chord the song plays there. End each slice with a 0.15 s fade; cut the final slice at the drop.
- **Clean drop.** Cut every intro layer on the kick with a 20–60 ms fade and no pause before it. The impact comes from the contrast between the build and the entrance (5.1 dB in the example).
- **Keep the ping in the midrange.** High-pass at 150 Hz and low-pass at 2.2 kHz; with sub content, it muddies the chords.
- **Measure the reference; do not estimate.** Timing, key, BPM, and levels come from measurement; the drop from the same song is the calibration standard.
- **Less is more.** Every new layer needs a function; when in doubt, remove it.

## Pitfalls

- The `"arquivo"` path in the plan is relative to the JSON file's directory; `{tom}` and `{nota}` are replaced with the plan's `"tom"` and the layer's `"nota"`.
- For a riser with `"pico_em"`, the script finds the file's peak using the highest RMS over 50 ms. If the file reaches its climax before the end, provide `"sync_s"`.
- If a layer is shorter than its assigned segment, it ends too soon; replace the sound or split the layer with `"a_partir_de"`.
- `trilha_momentos.py` alone does not protect the vocal. The final deliverable must pass through `mix_voz_na_frente.py`.
- Key detectors, Google's BPM, and instrument names supplied by Gemini can be wrong. Use measurement and your ears to decide.

## Skill references

| File | When to open it |
|---|---|
| `references/en/approved-recipe-v11.md` | The approved recipe, including all values, plan fields, and all 11 versions |
| `references/en/roles-sounds-and-key.md` | Choosing each sound, the relative-key rule, tuning, and slicing the progression |
| `references/en/measurement-and-validation.md` | Measuring a reference, spectrograms, frequency-band balance, and A/B comparison with Gemini |
| `references/en/intro-variations.md` | Other intro formats, transitions between sections, speed changes, and a fixed pulse |
| `scripts/` | Included analysis, preparation, rendering, stem, and validation scripts |

## Installation

Copy this directory to `~/.claude/skills/trilha-cinematografica/` for all projects, or `.claude/skills/trilha-cinematografica/` for one project only. To invoke it directly, ask Claude Code to "use the trilha-cinematografica skill."