// Pipeline: TTS des segments → Générer plans vidéo avec Ethanou

import { execSync } from 'child_process';

export async function generateTTSSegments(segments, voiceUrl = '') {
  // Chaque segment text → audio TTS via WaveSpeed
  const results = [];

  for (const seg of segments) {
    const payload = {
      text: seg.narration,
      model: 'wavespeed-ai/qwen3-tts/voice-clone',
      duration_seconds: seg.duration_sec,
      language: 'fr',
      ...(voiceUrl && { voice_url: voiceUrl }) // Si voix clonée
    };

    // Appel WaveSpeed via n8n webhook ou API directe
    // POST https://api.wavespeed.ai/api/v3/generate
    // Retourne: { audio_url, duration_actual }

    results.push({
      segment_id: seg.id,
      narration: seg.narration,
      audio_url: 'WAVESPEED_RESULT_URL',
      duration_actual: seg.duration_sec
    });
  }

  return results;
}

export async function generateVideoPlans(storyData, ethanouPortraitId) {
  // Pour chaque segment TTS:
  // Générer un plan vidéo de Ethanou qui raconte, avec visual_cue (background/éléments)

  const plans = [];

  for (const seg of storyData.segments) {
    const videoPrompt = \`
      Ethanou (avatar anime jeune garçon, cheveux bruns, sourire bienveillant) raconte:
      "\${seg.narration}"

      Contexte visuel: \${seg.visual_cue}
      Durée: \${seg.duration_sec}s

      Style: animation légère, expressions faciales engageantes, gestes naturels.
      Environnement: simple, coloré, amical (style chaîne enfants type Bluey).
    \`;

    // Seedance t2v OU utiliser un generate_video avec Ethanou comme référence
    // Output: video.mp4 (~\${seg.duration_sec}s)

    plans.push({
      segment: seg,
      video_prompt: videoPrompt,
      ethanou_reference_id: ethanouPortraitId
    });
  }

  return plans;
}

export async function assembleVideo(ttsSegments, videoPlans, storyTitle) {
  // FFmpeg: concat TTS audio + plans vidéo, sync lèvres si besoin
  // Ajouter sous-titres (segments[].narration)
  // Ajouter musique de fond (royalty-free enfants)
  // Output: story_final.mp4

  const cmd = \`
    ffmpeg \\
      -i video_plan_1.mp4 \\
      -i audio_segment_1.mp3 \\
      -i video_plan_2.mp4 \\
      -i audio_segment_2.mp3 \\
      ... \\
      -c:v libx264 -c:a aac \\
      -vf "subtitles=subs.srt" \\
      \${storyTitle}_final.mp4
  \`;

  // Exécuter assemblage
  // Retourner chemin final

  return {
    title: storyTitle,
    output_file: \`\${storyTitle}_final.mp4\`,
    duration: ttsSegments.reduce((sum, s) => sum + s.duration_actual, 0),
    ready_for_youtube: true
  };
}
