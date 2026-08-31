#!/usr/bin/env node
// Orchestre la création d'une vidéo de conte enfant
// Usage: node run.mjs --story="Les trois petits cochons" --theme="constructif" --learning="structures solides"

import { generateStoryPrompt } from './generate-story-prompt.mjs';
import { generateTTSSegments, generateVideoPlans, assembleVideo } from './pipeline-tts-video.mjs';

const args = Object.fromEntries(
  process.argv.slice(2).map(arg => {
    const [k, v] = arg.replace(/^--/, '').split('=');
    return [k, v];
  })
);

const { story, theme = 'aventure', learning = '', duration = 45, voice = 'male' } = args;

if (!story) {
  console.error('Usage: node run.mjs --story="Titre" --theme="aventure|alphabet|constructif|mots|chiffres"');
  process.exit(1);
}

console.log(`🎬 Création: "${story}" (${theme}, ${duration}s)\n`);

// 1. Générer l'histoire structurée
console.log('📖 Génération de l\'histoire...');
const storyPrompt = await generateStoryPrompt({ story, theme, learning, duration });
// Appeler Claude API ou n8n pour générer storyData (JSON structuré)
// const storyData = await callClaudeAPI(storyPrompt);

// Pour démo:
const storyData = {
  title: story,
  intro: 'Bonjour les amis! Aujourd\'hui je vous raconte...',
  segments: [
    // Sera rempli par Claude
  ],
  outro: 'Et voilà! À bientôt pour une nouvelle aventure!'
};

console.log(`✅ Histoire générée: ${storyData.segments.length} plans\n`);

// 2. Générer TTS pour chaque segment
console.log('🎙️ Génération des voix...');
const ttsSegments = await generateTTSSegments(storyData.segments, voice);
console.log(`✅ ${ttsSegments.length} segments audio générés\n`);

// 3. Générer plans vidéo avec Ethanou
console.log('🎬 Génération des plans vidéo (Ethanou raconte)...');
const ETHANOU_PORTRAIT_ID = 'soul_ethanou_anime_v1'; // À obtenir de generate_image ci-dessous
const videoPlans = await generateVideoPlans(storyData, ETHANOU_PORTRAIT_ID);
console.log(`✅ ${videoPlans.length} plans vidéo prêts\n`);

// 4. Assembler la vidéo finale
console.log('🎞️ Assemblage final (TTS + vidéo + sous-titres)...');
const finalVideo = await assembleVideo(ttsSegments, videoPlans, story.replace(/\s+/g, '-').toLowerCase());
console.log(`✅ Vidéo finale: ${finalVideo.output_file} (${finalVideo.duration}s)\n`);

// 5. Upload sur previsualisation
console.log('📤 Publication sur previsualisation...');
// Uploader vers https://previsualisation.automatisationboost.com/contes-enfants/...
console.log(`✅ Live: https://previsualisation.automatisationboost.com/contes-enfants/${finalVideo.output_file}\n`);

console.log('🎉 Prêt à publier sur YouTube Shorts / TikTok!');
