# autoboost-80 — « Claude monte comme un pro » (Tony vs Tony IA)

9:16 · 1080×1920 · 30 fps · **53,5 s** (1606 images) · −16,2 LUFS · CTA **BOOST** (porte Blotato existante)

Remake of [@pauloshimas' reel](https://www.instagram.com/reel/Dd4S4nYysi1/) (« Claude can finally edit like a pro »:
computer vision, transcription, segmentation, everything becomes code, blue pill / red pill). It is rewritten in
Tony's style as a duo with his IA avatar, who heckles him. The script is in `session/script.json`.

- **Voices**: every line is in Tony's cloned voice (the n8n `tts-gen` webhook, WaveSpeed clone, F0 checked).
  The IA lines get a light « machine » colour (+1 semitone, short slapback) so the two voices read apart.
- **Tony**: the real take (`video_25`), muted and re-cut to the voice track by `resync.py` (lip sync v2).
  Every run of his lines is filled by the take window whose own loudness envelope best matches the cloned
  voice. A run may split at the voice's pauses, so the mouth is closed on both sides of a cut. A DTW warp
  (hold at most 2 frames, step, or skip a frame) then lands each syllable. Mouth/voice on-off mismatch per line
  went from 27–49 % (v1, take passages read in order) to 0–6 %. Silent windows, played forward then backward,
  sit under the IA's lines. The take is matted once with `hyperframes remove-background`, and both the cutout and
  the unmatted take (segmentation reveal) are written from the same frame map.
- **Music**: Valse des fleurs, house recording (`bed_valse.py`). The hollow version runs under the voices,
  laid out so that the full orchestra lands its bar 5 cadence right after the last word.
- **Tony IA**: the BUREAU avatar in a violet neon circle on his shoulder. Its lips move only on its lines.
  Tony dims and steps aside while it talks.
- **Gags**:
  - vision boxes on his real room, then « HUMAIN ? » and the « COIFFURE EN OPTION » sticker;
  - his words with their real timestamps, then « euh » ×3 in red;
  - the room peels away pixel by pixel, then the white sticker outline;
  - beach / moon / Teams meeting behind him, then the « PAS TEAMS. » stamp;
  - the code window;
  - « J'ai les idées », then « PARFOIS. » and the bulb goes out;
  - violet (« bleue ») vs red pill, then « commente BOOST ».

```bash
python3 build.py video_25.mp4 take_transcript.json VO_DIR build/      # voice.wav, vo.json, avatar.mp4 (+ v1 Tony track)
ffmpeg -i video_25.mp4 -vf fps=30 -c:v libx264 -crf 14 -c:a pcm_s16le take30.mkv && ffmpeg -i take30.mkv -an -c:v copy take30.mp4
npx hyperframes remove-background take30.mp4 -o take_alpha.webm      # the whole take, once
python3 resync.py take30.mp4 take30.mkv take_alpha.webm build/       # tony_src.mp4, tony.webm, tony_cuts.json (lip sync)
python3 bed_valse.py build/                                           # bed.wav, Valse des fleurs
BUILD=build python3 motion/gen.py && npx hyperframes render motion/public -o silent.mp4 --fps 30 --quality delivery
python3 .claude/skills/face-cam-boost/scripts/facecam_audio.py --voice build/voice.wav --events motion/events.json \
        --frames 1606 --out mix.wav --bed-file build/bed.wav --bed-gain -6
```

Known limit: a thin light rim around the cutout, left by the automatic matte against the white wall.
