# Intro variations and continuity rules

The v11 recipe—early vocal, call-and-response cello, chords sliced onto words, and two risers—is only one option. Each song calls for its own treatment: speed, whether to open with the vocal or instrumental, and the choice of elements depend on the mood, beat, key, and BPM.

## Soundtrack brief (complete before each song)

| Field | Example |
|---|---|
| Use | 20–30 s Reel, long-form video opener, film |
| Emotion and arc | Intimate → tension → explosion; or melancholy from beginning to end |
| Song, key, BPM, tuning | Measured and verified |
| Chords in the segment | `medicao/chromat.py` |
| Base recipe | One of the options below |
| Palette | What this song adds and what it leaves out |
| Speed | Whether it slows down, by how much, and where it returns |

## Recipes

**Early vocal (the example recipe).** Ping in the first frame; drones from about 2.5 s; solo cello; vocal with about 40% reverb; cello response in the breath; relative-major chords sliced one per stressed word; accent ping on the first chord; two risers during the final 5 s; clean drop on the kick.

**Build toward the vocal.** Melodic hit in the first frame; drone from 0 with a gentle fade-in; violin or cello melody from about 4.5 s; a tonal swell peaking at the vocal entrance; vocal only during the final ~10 s; a high riser lasting about 10 s and a low riser lasting about 8 s, both ending at the drop; and a tonal impact whose tail spills into the song. For short-form video, shorten only the instrumental section before the vocal; keep the vocal at about 9 s and leave the risers unchanged.

**Open with the song's own instrument.** Use the track's synthesizer or piano—the "(other)" separation—at 85% speed with pitch preserved, together with the ping and cello excerpts. When the vocal enters, the instrument fades into a reverb tail of about 30%; the vocal also enters at 85% speed with about 40% reverb. Use block piano chords on strong beats, with a ping on each attack. Add an aggressive riser in the final seconds, and return the **last phrase to 100% speed**. End the phrase cleanly, leave a fraction of silence, then enter the full song.

**Open with the muffled instrumental.** Start the song's instruments without the vocal, with a closed low-pass filter around 400 Hz, then open it through the end of the first chord cycle. Bring in the vocal at its original time after several bars. Use a break already present in the song before the chorus as the breath, about 1 s long, with one riser crossing it alone.

**Ballad without a drop.** Lower the drone by about 11 dB when the piano enters; add sub-bass under the pre-chorus and cut it cleanly at the chorus.

## Speed

- The phrase at 100% speed must **continue the lyrics** from the 85% section. Jumping to another verse at the same time as the speed change exposes the edit. Leave a breath of about 0.25 s before it.
- Ramp the speed instead of switching abruptly: update rubberband's `tempo` every 50 ms with `asendcmd`, identically for the vocal and instrument.
- Test each voice first: one singer sounded robotic at 85% and natural at 90%. Slowed vocals require rubberband's smooth mode (`transients=smooth:detector=soft:window=long:channels=together`). Long vowels are the weak point.

## Continuity

- No edit should be perceptible. Do not let any layer exit with an audible volume drop.
- Keep one continuous layer running from the beginning to the end of the intro, such as a soft drone.
- Do not stop the opening stem abruptly: fade it into a long tail beneath the vocal entrance. An instrument leaving before the drop needs about a 2.5 s fade; 0.4 s sounds like a cut.
- Thin the arrangement before the drop: stop the piano and pings, leaving the vocal and a riser growing for about 3 s. The riser crosses the breath as the only effect and peaks at the drop. The breath lasts half a bar.
- The final word can dissolve into the breath with a fade of about 1.2 s instead of cutting cleanly.
- At the speed change, the drone and riser may restart with a 1.5 s fade-in, creating a slight pullback before the build resumes.
- Everything ends at the same point, where the full song enters.

## Transition between two sections

1. End the outgoing section at the end of a phrase. During the final ~0.23 s, raise cathedral reverb from 0 to 50% and let the tail continue.
2. Add tonal elements in key: a vocal effect peaking at the cut, a low piano rising into the cut, and, during the quiet moment, a drone and sub in key.
3. Bring the incoming section back muffled, with a low-pass around 650–700 Hz and a high-pass around 400 Hz, always aligned to a bar on the grid. Open the filters over the final ~4 s so they reach maximum openness on beat 1 of the chorus, with the riser and ping landing at the same point.
4. Start the incoming vocal at the beginning of a phrase after a natural silence; locate it from the words reported by `medicao/tr.py`.
5. Give segments from the same stem the same gain, calculated from the unprocessed audio.

**Two hype arcs.** The transition effect cannot arrive at the last moment. Start a tonal effect and a riser at the opening and build them to the vocal cut (arc 1); at the cut, restart with another riser and build it to the beat (arc 2).

## Fixed pulse

Piano and any repeated hit must follow a fixed pulse from beginning to end—for example, every 2 beats on the kick grid. The listener learns the tempo and expects the next hit at the same interval. For variation, add another note from the same chord—the third or fifth in another octave—on the same pulse without changing the interval.

## General rules

- The hype begins about 10 s before the beat and only adds layers until the impact.
- A tonal riser with glissando clashes with a fixed guitar riff; use a noise riser instead.
- A swell that ends abruptly needs a reverb tail.
- Every new layer needs a function. When in doubt, use less.
- In a narrated video, the remix opens the video and narration begins at least 0.5 s after the drop, dry, with the music well below it. Narration over the remix does not work.