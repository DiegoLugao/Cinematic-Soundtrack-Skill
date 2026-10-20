# Roles, sounds, and key

Each intro layer has a role. Choose a sound by asking three questions in this order: does it serve the role, does it fit the song's key, and, when a reference exists, does its frequency profile resemble the corresponding reference layer?

## Roles

| Role | Sound | Function | Caution |
|---|---|---|---|
| Tonal hit ("ping") | Piano or bell note on the tonic, with a long tail | Opens the intro in the first frame and marks accents | Keep it in the midrange only (150 Hz to 2.2 kHz); sub content muddies the chords |
| Drone | Low, continuous sound with almost no attack | Forms the bed that sustains the intro through the drop | High-pass around 90 Hz; two layered drones add body |
| Texture | Pad or airy sound with slow movement | Adds motion to the drone | Keep it lower than the drone (−2 dB) |
| Cello melody | Short phrases with clearly defined beginnings and endings | "Call" before the vocal and "response" in the breath | Choose a real cello (G2 to G3); substituting a violin phrase sounds too high |
| Chord progression | Piano playing one sustained chord at a time | Accents stressed words and establishes the harmony | Must include bass; slice one chord per bar |
| Air riser | Rising noise or breath | Creates the first arc toward the drop | Low-pass around 5 kHz |
| Aggressive riser | Rising tonal synthesizer | Creates the second, shorter, stronger arc | Low-pass around 4 kHz |
| Impact | Low hit with a tail | Reinforces the drop kick | High-pass at 60 Hz to avoid competing with the kick |

Tonal sounds are often recorded in all 12 keys. When assembling the directory, name each file with its note (`drone-1-A.wav`, `cello-C.wav`): in the plan, `{tom}` and `{nota}` select the correct file.

## The key rule

Every layer must fit the song's notes.

- A minor key and the major key 3 semitones above it use the same seven notes: A minor and C major, E minor and G major, D minor and F major. The major key is the minor key's **relative major**.
- For a minor-key song, use minor sounds in the song's key, major sounds in its relative major, and sounds that work in both modes (marked major/minor or lacking a third). In A minor, the example uses cello and chords in C major.
- For a major-key song, use the inverse: major sounds in the song's key, minor sounds in its relative minor 3 semitones below, and sounds compatible with both modes.
- Never place a major sound over a minor song on the same tonic (A major over A minor), or vice versa. The thirds clash and the result sounds out of tune.
- Notation: A♭ = G#, E♭ = D#, B♭ = A#, D♭ = C#, G♭ = F#.

## Before choosing: tuning

Measure with `medir_musica.py`. If the song is more than about 20 cents away from A 440, every tonal sound layered over it will sound out of tune. Some well-known songs have this issue: one measures around +45 cents, and key-reference sources disagree between two adjacent keys. Prefer another song, or retune the sounds first with `rubberband` in ffmpeg.

## Choose by measurement

When a reference exists:

1. Find a segment where the layer plays almost alone: the opening ping, the drone before the vocal, or the risers before the drop.
2. Run `medicao/match.py referencia.wav ini fim "sons/**/*.wav"`: it ranks files by the frequency profile of that segment.
3. Audition the top three in context inside the plan, then keep the one that sounds right with the vocal.
4. Next, compare each segment's frequency-band balance with `medicao/bands.py`. If one segment has too much low end, filter the sound occupying that segment; do not replace everything.

Without a reference, choose by role and key. Then inspect the spectrogram to confirm that the ping stays in the midrange, the chords contain bass, and the risers reach the drop.

## Slicing the chord progression

1. `medicao/chords.py sons/acordes-C.wav` identifies the start of each chord in the file (in the example: F at 0 s, G at 8 s, Am at 16 s, C at 24 s, Dm at 32 s, C at 40 s).
2. `medicao/chromat.py musica.wav ini dur` reports the song's harmony second by second across the intro segment.
3. For each bar containing a stressed word, take the chord the song plays there from the file (`"corte"` = that chord's start time in the file) and place it on beat 1 of the bar (`"em"`). Derive the exact time from the song's low-frequency jumps with `medicao/env.py` using a 5 ms step.
4. End each slice 0.06 s after the next slice begins, using a 0.15 s fade; cut the final slice at the drop.

When the song's harmony changes every bar and no progression file follows it, use the song's own harmonic instrument—the "(other)" separation—under the vocal at the same speed as the vocal. A static bed will sound out of tune over changing chords.

## Building the ping from piano notes

`prep_ping.py saida.wav nota_media.wav nota_aguda.wav [nota_grave.wav]`: use the tonic in two octaves at gains of 1.0 and 0.6, plus a very quiet lower octave at 0.2; apply 8 s cathedral reverb at 55% mix and filters at 150 Hz and 2.2 kHz. Any sampled piano in WAV or FLAC format will work. For A minor, use A4 + A5 + A3.