# Measuring the reference and validating each version

Timing, key, BPM, and levels come from measurement. When a reference exists—a remix or demo the user likes—it becomes the standard: both versions use the same song at the drop, so the drop provides a calibration point.

## Measure the reference

1. **Separate the reference vocal** with `separar_voz.py`; use the "(other)" file to isolate the tonal layers. Compare your version without its vocal as well.
2. **Align it with the song** using `medicao/align.py referencia.wav musica.wav ini fim`: it reports, for each second, which point in the song the reference uses. A constant offset from beginning to end means the complete vocal enters without edits (14.83 s in the example).
3. **Set time zero at the first hit** using `medicao/env.py referencia.wav ini fim 0.005`: find the instant when the energy jumps. In the example, the ping rises from −60 to −17 dB at 5.950 s in the reference. Count every time in your intro from that point.
4. **Chords:** determine harmony with `medicao/chromat.py`; derive each chord's exact time from energy jumps below 80 Hz. In the example, every chord lands on beat 1 of the bar, aligned with the words.
5. **Drop:** locate the song's kick using 10 ms RMS with `medir_musica.py --bumbo`.
6. **Song:** determine the key from chroma and confirm it externally; measure BPM through beat tracking and tuning in cents.

## Validate each version

### Spectrogram

`conferir.py sua.wav --ref referencia.wav --desloc-ref <s> --png espectro.png` places both tracks on the same time axis. Look for:

- sub content in the ping, visible as an active band below 100 Hz in the first frame;
- chords without bass—the reference has energy below 70 Hz, while yours does not;
- risers that fail to reach the drop or continue past it;
- drones that enter too early or too late.

### Frequency-band balance

`medicao/bands.py ref_sem_voz.wav sua_sem_voz.wav --trechos trechos.json` measures 20–70, 70–250, 250–2 k, 2–8 k, and 8–16 kHz in each segment, normalized against the drop. The drop must match within about 1 dB. A difference within one segment identifies which layer to filter.

### Listening

- The user's ears make the final decision. Ask for the exact timestamp of anything that sounds wrong.
- For a second opinion, `conferir.py --video ab.mp4` creates a black-screen MP4 containing the reference, 2 s of silence, then your version. Send it to Gemini with this prompt: "Compare the two soundtracks. Rate their similarity from 0 to 10, list each problem in the second track with its timestamp measured from the beginning of that track, and state what to fix using numerical values."
- To compare vocal separations, run a blind test: use the same phrase, randomize the order, and do not reveal which is which.
- Gemini can misidentify instruments. It is reliable for structure, level, echo, and artifacts.

### Measure before assigning blame

When something sounds wrong, measure before changing it. In the example, "the vocal disappears at 17 s" seemed to implicate the limiter. Measurement showed that the limiter was inactive (0.0 dB gain reduction) and that the A minor chord plus the ping were 2–5 dB above the vocal. Dynamic vocal priority fixed the problem; the limiter remained unchanged.

## Delivery targets

| Item | Target |
|---|---|
| Integrated loudness | −14 LUFS |
| Peak | Below −1 dBFS |
| Vocal echo | About 5 dB below the dry vocal |
| Tonal-layer midrange while the singer is active | At least 5 dB below the vocal |
| Build → drop contrast | About 4–5 dB (example: 5.1; reference: 4.3) |
| Drop versus the reference, by frequency-band balance | Within about 1 dB |