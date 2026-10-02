# Master sheet prompt — template

The `histoire-du-jour` agent copies this file to `episodes/<X>/docs/SHEET_PROMPT.md` and replaces every
`{{…}}`. Tony pastes the prompt into ChatGPT (image) or Higgsfield **together with the M sheet
(`episodes/M/assets/source/assets_master_sheet.png`) attached as layout + character reference**, then saves the
result as `episodes/<X>/assets/source/assets_master_sheet.png`.

Why the layout matters: `tools/slice_sheet.py` cuts the sheet with `sheet_map.json` (copied from M). The closer
the new sheet is to the M grid, the fewer boxes need adjusting. Milo's base poses are NOT taken from the new
sheet (the `heroes/milo/` library keeps him identical across letters), only the pose holding the quest object.

---

## Prompt (paste as is)

```
Use the attached image as an EXACT layout, style and character reference. Create a NEW asset master sheet
with the SAME grid, the SAME panel sizes and positions, the SAME dark navy background with rounded panels,
the SAME yellow panel titles and the SAME small white file-name labels under every item.
Only the content changes, for the letter {{UPPER}}. Portrait sheet, about 1214 x 1295 px (or exactly 2x).
Style: premium children's picture book, warm 3D cartoon / CGI, soft lighting, tropical jungle, bright and
friendly, no text other than the labels listed below. Every non-background item sits on a light grey
checkerboard (as in the reference), fully visible, not touching its neighbours, with clear space around it.

ROW 1 - five tall background panels, titles "SCÈNE 1 - FOND" … "SCÈNE 5 - FOND", labels
"background_01.png" … "background_05.png". Empty scenery, no characters, keep the bottom third simple
(a character will stand there):
 1. {{BG1}}
 2. {{BG2}} with a wooden direction sign reading "{{QUEST_LABEL_UPPER}}" with a yellow arrow
 3. {{BG3}}
 4. {{BG4}} with a wide empty wooden stage / platform in the lower third
 5. {{BG5}} golden sunset, sparkles, magical reward mood

ROW 2 - panel "PERSONNAGE PRINCIPAL - MILO (PNG TRANSPARENT)": the SAME Milo as the reference (small brown
monkey, big brown eyes, light muzzle, blue backpack), sitting, labels "milo_closed.png" (mouth closed smile)
and "milo_open.png" (mouth open). Panel "AUTRES POSES (PNG TRANSPARENT)", left to right:
"milo_wave_open.png" (waving), "milo_{{QUEST_SLUG}}_open.png" (sitting, holding the {{QUEST_WORD}} with both
hands, happy open mouth), "milo_walk_1.png", "milo_walk_2.png" (walking to the right), "milo_point_open.png"
(pointing up).

ROW 3 - panel "LETTRE {{UPPER}}": glossy 3D balloon letters, "{{UPPER}}" in red (label
"letter_{{UPPER}}_upper.png") and "{{LOWER}}" in blue (label "letter_{{LOWER}}_lower.png").
Panel "PANNEAU": the wooden sign alone, reading "{{QUEST_LABEL_UPPER}}", label "sign_{{QUEST_SLUG}}.png".
Panel "ÉLÉMENTS TEXTE (PNG TRANSPARENT)": leave it with 3 to 5 simple cream speech bubbles (optional, unused).

ROW 4 - panel "OBJETS (PNG TRANSPARENT)", eight objects left to right, each a single clear, front-facing,
child-readable illustration, labels in this order:
"{{QUEST_SLUG}}.png" ({{QUEST_WORD}}), "{{W1_SLUG}}.png" ({{W1}}), "{{W2_SLUG}}.png" ({{W2}}),
"{{W3_SLUG}}.png" ({{W3}}), "{{D1_SLUG}}.png" ({{D1}}), "{{D2_SLUG}}.png" ({{D2}}),
"rocher_plantes.png" (rock with flowers), "fleurs.png" (tropical flower).

ROW 5 - panel "EFFETS (PNG TRANSPARENT)": "etoiles.png" (golden sparkles), "magie.png" (golden magic swirl),
"rayons.png" (three yellow emphasis rays), "pop.png" (magenta starburst with white centre),
"feuilles.png" (four green leaves). Panel "LOGO / SIGNATURE": the SAME "Histoire du jour" logo with the open
book, label "histoire_du_jour.png". Panel "CADRE VIDÉO (OPTIONNEL)": same frame as the reference,
label "frame_overlay.png".
```

## Placeholders

| placeholder | meaning | M example |
|---|---|---|
| `{{UPPER}}` / `{{LOWER}}` | the letter | M / m |
| `{{QUEST_WORD}}`, `{{QUEST_SLUG}}` | quest object, file slug (lowercase, no accents, `_`) | mangue / mangue |
| `{{QUEST_LABEL_UPPER}}` | sign text | MANGUE MAGIQUE |
| `{{W1..3}}`, `{{W1..3_SLUG}}` | the three example words | maison, moto, montagne |
| `{{D1}}`, `{{D2}}` (+ slugs) | the two mini-game distractors (do NOT start with the sound) | lune, chat |
| `{{BG1..5}}` | short scene descriptions matching the story | jungle clearing with lagoon and mountains … |
