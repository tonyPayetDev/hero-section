# BGM partagées

## flowers_horror.mp3
Musique de fond par défaut des vidéos Autoboost (« horror » est le NOM du morceau,
pas une ambiance visuelle à reproduire).

- Mesurée à **-12,4 LUFS** → utiliser `data-volume="0.05"`.
  À comparer avec `bgm-ascension.mp3` (-19,1 LUFS → `0.09`) : 7 dB d'écart, ne pas
  réutiliser le même volume d'une piste à l'autre sinon la musique passe devant la voix.
- Boucler avec `ffmpeg -stream_loop -1 -t <durée comp>` si le morceau est plus court
  que la composition.

Référence d'usage : `autoboost-40-seedance/public/index.html` (`<audio id="bgm">`).
