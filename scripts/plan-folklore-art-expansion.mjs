import fs from 'node:fs';
import path from 'node:path';

const contentDir = 'src/content/folklore';
const records = fs.readdirSync(contentDir)
  .filter(name => name.endsWith('.json'))
  .map(name => JSON.parse(fs.readFileSync(path.join(contentDir, name), 'utf8')))
  .sort((a, b) => a.order - b.order);

const desiredCount = sceneCount => sceneCount <= 6
  ? Math.floor(sceneCount / 2)
  : sceneCount <= 12 ? 4 : 6;

const queue = [];
for (const story of records) {
  const needed = Math.max(0, desiredCount(story.scenes.length) - story.pageArt.length);
  if (!needed) continue;

  const occupied = new Set(story.pageArt.map(item => item.page));
  const available = Array.from({ length: story.scenes.length - 1 }, (_, i) => i + 1)
    .filter(page => !occupied.has(page));

  for (let slot = 0; slot < needed; slot += 1) {
    const ideal = Math.round(((slot + 1) * (story.scenes.length - 1)) / (needed + 1));
    const page = available.toSorted((a, b) => Math.abs(a - ideal) - Math.abs(b - ideal) || a - b)[0];
    available.splice(available.indexOf(page), 1);
    occupied.add(page);
    const number = String(page + 1).padStart(2, '0');
    const scene = story.scenes[page].join(' ').replace(/\s+/g, ' ').slice(0, 1100);
    queue.push({
      id: `${story.id}:${page}`,
      storyId: story.id,
      title: story.title,
      culture: story.culture,
      page,
      output: `public/folk/art/${story.id}/${number}-scene.webp`,
      status: 'pending',
      prompt: `Use case: illustration-story\nAsset type: landscape interior story illustration for a children's folklore reading app\nPrimary request: Illustrate this scene from “${story.title}”: ${scene}\nStyle/medium: warm hand-painted gouache and colored pencil, classic children’s storybook, tactile paper grain\nComposition/framing: landscape 4:3, one clear narrative moment, readable on a tablet\nCultural setting: ${story.culture}; use respectful, story-appropriate landscape, architecture, and clothing cues without caricature\nLighting/mood: expressive, inviting, suitable for ages 6–8 reading with an adult\nConstraints: preserve the named characters and action; no text, letters, captions, borders, watermark, photorealism, graphic violence, or frightening imagery`,
    });
  }
}

fs.writeFileSync('drafts/folklore-art-expansion.json', `${JSON.stringify({ policy: { short: 'every other scene', medium: 'up to four interior illustrations', long: 'up to six major-beat illustrations' }, total: queue.length, queue }, null, 2)}\n`);
console.log(`Planned ${queue.length} additional illustrations.`);
