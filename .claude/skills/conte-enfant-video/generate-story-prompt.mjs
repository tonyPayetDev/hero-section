// Génère un prompt structuré pour créer l'histoire
export async function generateStoryPrompt({ story, theme, learning, duration }) {
  const learningLine = learning ? `\nObjectif pédagogique: ${learning}` : '';
  const durationSegments = Math.ceil(duration / 10); // Chaque segment ~10s = 1 plan vidéo

  return `Tu es scénariste pour chaîne YouTube enfants (Ethanou, 8 ans, narrateur amical).

Crée une histoire courte EN FRANÇAIS: "${story}"
Thème: ${theme}
${learningLine}

CONTRAINTES:
- Durée TOTALE environ ${duration}s (${durationSegments} plans de ~10s chacun)
- Langage simple (vocabulaire enfants 6-9 ans)
- Rythme rapide, engagement constant (pas de passages mous)
- Morale ou apprentissage INTÉGRÉ (pas moralisateur, naturel)
- Zéro violence, peurs excessives, contenu sombre

FORMAT RÉPONSE (JSON):
{
  "title": "Titre court",
  "intro": "1-2 phrases pour accrocher (Ethanou parle directement)",
  "segments": [
    {
      "duration_sec": 10,
      "narration": "Texte TTS (~150 caractères = ~10s)",
      "visual_cue": "Ce qu'on voit (avatar + background/éléments)",
      "learning_moment": "Si applicable"
    },
    ...
  ],
  "outro": "Conclusion chaleur (1 phrase)",
  "teaching_point": "Résumé de ce qu'on a appris"
}

Produis UNIQUEMENT le JSON, pas d'explications.`;
}
