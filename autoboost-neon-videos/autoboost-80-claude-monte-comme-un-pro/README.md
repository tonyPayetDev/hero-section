# autoboost-80 — « Claude monte comme un pro » (Tony vs Tony IA)

9:16 · 1080×1920 · 30 fps · **53,5 s** (1606 images) · −16,2 LUFS · CTA **BOOST** (porte Blotato existante)

Remake of [@pauloshimas' reel](https://www.instagram.com/reel/Dd4S4nYysi1/) (« Claude can finally edit like a pro »:
computer vision, transcription, segmentation, everything becomes code, blue pill / red pill). It is rewritten in
Tony's style as a duo with his IA avatar, who heckles him. The script is in `session/script.json`.

- **Voices**: every line is in Tony's cloned voice (the n8n `tts-gen` webhook, WaveSpeed clone, F0 checked).
  The IA lines get a light « machine » colour (+1 semitone, short slapback) so the two voices read apart.
- **Tony**: the real take (`video_25`), muted and re-cut to the voice track. Talking passages sit under
  his lines, silent ones (he listens) under the IA's lines. Matted with `hyperframes remove-background`;
  the unmatted take sits underneath for the segmentation reveal.
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
python3 build.py video_25.mp4 take_transcript.json VO_DIR build/      # voice.wav, vo.json, tony_src.mp4, avatar.mp4, bed.wav
npx hyperframes remove-background build/tony_src.mp4 -o build/tony.webm
BUILD=build python3 motion/gen.py && npx hyperframes render motion/public -o silent.mp4 --fps 30 --quality delivery
python3 .claude/skills/face-cam-boost/scripts/facecam_audio.py --voice build/voice.wav --events motion/events.json \
        --frames 1606 --out mix.wav --bed-file build/bed.wav --bed-gain -22.4
```

Known limit: a thin light rim around the cutout, left by the automatic matte against the white wall.
