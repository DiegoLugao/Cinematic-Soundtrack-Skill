# Approved recipe (v11): "Laugh Now Cry Later"

The intro runs about 39 s. The singer enters nearly a cappella with concert-hall reverb, while the tonal layers surround the vocal as complementary elements. The full song enters dry on the verse kick and continues for about 18 s (58 s total). In Gemini's listening comparison against the reference, v11 scored 9.7 out of 10. The complete plan is in `examples/example-plan.json`.

## The song

- A minor, **136 BPM** (Google reports 134), tuning +0.02 semitone (standard).
- Drop kick: 30.485 s into the song, measured with 10 ms RMS. In the intro, it lands at 39.37 s.
- Vocal: separated from the song itself with MelBand RoFormer Big Beta 4; the 1.0–31.0 s segment of the song is placed at 9.88 s in the intro.

## Timeline and layers

| Time (s) | Layer | Processing |
|---|---|---|
| 0.00 | Piano ping in A (A4 + A5, with a touch of A3), 8 s cathedral reverb at 55% mix | 150 Hz high-pass, 2.2 kHz low-pass (4th order); −21 LUFS |
| 2.5 → 39.37 | Drone 1 in A | 4 s fade-in; 90 Hz high-pass, +1.5 dB at 180 Hz, +2 dB at 280 Hz, 2.5 kHz low-pass; −26 |
| 2.5 → 39.37 | Drone 2 (texture) in A | 4.5 s fade-in; 90 Hz high-pass, +1.5 dB at 180 Hz, +2.5 dB at 280 Hz; −28 |
| 4.2–10.6 | Cello in C major (relative major), A→E phrase, the "call" | 0.8 s fade-in, 1 s fade-out; 3.2 kHz low-pass; −22 |
| 9.88 → 39.37 | Vocal with reverb | −16 |
| 13.4–18.0 | Cello, phrase in E, the "response" | 0.6 s fade-in, 1.5 s fade-out; 3.2 kHz low-pass; −26 |
| 16.09 / 21.50 / 25.00 / 28.70 / 32.23 / 35.85 | Sliced Am, G, F, G, Am, G chords (progression in C major: F G Am C Dm C, 8 s each) | +5 dB at 70 Hz, 2.5 kHz low-pass; 0.15 s fade-out; −17 |
| 16.09 and 35.85 | Accent ping | −25 and −26 (the second cuts at the drop) |
| 34.25 → 39.37 | Riser 2, more aggressive | Peak at the drop; 4 kHz low-pass; 60 ms fade at the end; −16 |
| 35.69 → 39.37 | Riser 1, rising air | Peak at the drop; 5 kHz low-pass; 60 ms fade; −17.5 |
| 39.37 | Drop: song from 30.42 s (kick at 30.485) + ping + tonal impact | Song −11.5; ping −21; impact with 60 Hz high-pass, −20; every intro layer cuts cleanly |

Without filtering, the aggressive riser was 10 dB brighter than the reference. The progression was chosen because it includes bass: the reference measures +6 dB below 70 Hz during the chords.

## Vocal reverb (Concert Hall replica, no plugin)

| Preset parameter | Replica in `prep_voz.py` |
|---|---|
| Concert Hall, '70s color | Slow attack (60 ms envelope), dark tail |
| Decay 4.00 s | 4 s midrange RT60 (700 Hz to 6 kHz) |
| BassFreq 700 Hz × 1.5 | 6 s RT60 below 700 Hz |
| Damping 6 kHz / −24 dB | 1.2 s RT60 above 6 kHz, at −9 dB |
| Predelay 20 ms | 20 ms |
| HighCut 8 kHz | 5.5 kHz (at 8 kHz, the tail sounded brighter than the reference) |
| Mod 2.53 Hz / 38% | 2.53 Hz chorus, depth 0.15, mix 0.5, applied only to the tail |
| Mix 40.7% | Wet signal at the same energy as the dry signal; output = 0.593 × dry + 0.407 × wet |

Also apply −1.5 dB at 3.8 kHz (Q 1) to the dry vocal. Result: echo at −4.9 dB relative to the vocal.

## Mixing with the vocal on top

1. `trilha_momentos.py` resolves the layers, timing, and levels.
2. `stems.py` exports the groups using the mix's master gain.
3. `mix_voz_na_frente.py`: the tonal layers become a bus split at 250 Hz. While the singer is active, keep the bus midrange at least 5 dB below the vocal, with up to 7 dB of reduction, while reducing the low end by no more than 2 dB. Use 50 ms envelopes, 15 ms attack, and 300 ms release. Return to −14 LUFS and pass through the limiter (`alimiter` 0.84).
4. This step outputs the final layers with the limiter's 239-sample delay; together they sum to the mix.

Output: −14.0 LUFS, −1.2 dBFS peak.

## Plan fields

`arquivo`, `papel` (golpe, drone, melodia, acordes, riser, voz, musica), `grupo`, `em`, `corte` (or `"metade"`), `ate`, `golpe: true` (the file's peak lands at `em`), `pico_em` + `subida` (riser), `sync_s` (the file's peak if automatic measurement is wrong), `ataque` (seconds between the cut and the kick), `a_partir_de`, `tempo`, `passa_altas`, `filtro` (free-form ffmpeg expression), `lufs_alvo`, `ganho_db`, `fade_in`, `fade_out`, `mudo`. Top-level fields: `duracao`, `saida_lufs`, `tom`. Keys beginning with `_` are comments.

## The 11 versions

| Version | Change | Result |
|---|---|---|
| v1 | Measured timing; a hit with sub instead of the ping; progression without bass; vocal with 40% hall | Spectrogram: piano without bass, ping with too much sub |
| v2–v3 | Actual piano ping; filters based on frequency-band balance; progression with bass | Bands close to the reference; matching drop |
| v4 | Chords placed at the exact times based on low-frequency jumps | 9.2 |
| v5 | 50% reverb + cathedral, fuller drones, dip in the risers | 9.3 |
| v6 | More drop contrast, more open risers | 9.6; "it sounds REALLY good," but "too much echo on the vocal" |
| v7 | 20% reverb, hall only | — |
| v8 | 10% reverb + fixed −2.5 dB reduction on tonal layers while the singer is active | "too a cappella" |
| v9 | Concert Hall replica, 40.7% mix | Vocal rated 9/10 for matching the reference |
| v10 | Darker tail, −1.5 dB at 3.8 kHz | Better, but the vocal "gets lost" at 17 s and the separation is weak |
| **v11** | Vocal from Big Beta 4 + dynamic vocal priority | **9.7**; "the closest to perfection so far" |

## Further refinement

Two Gemini suggestions were not tested: widen the stereo image and add light saturation to the sub on the first beat of the drop. Test these by ear in an audio editor.