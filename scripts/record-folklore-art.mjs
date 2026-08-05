import fs from 'node:fs';

const [queueId, image, alt] = process.argv.slice(2);
if (!queueId || !image || !alt) throw new Error('usage: record-folklore-art.mjs <story:page> <web-image-path> <alt>');

const [storyId, rawPage] = queueId.split(':');
const page = Number(rawPage);
const storyPath = `src/content/folklore/${storyId}.json`;
const story = JSON.parse(fs.readFileSync(storyPath, 'utf8'));
if (!story.pageArt.some(item => item.page === page)) story.pageArt.push({ page, image, alt });
story.pageArt.sort((a, b) => a.page - b.page);
fs.writeFileSync(storyPath, `${JSON.stringify(story, null, 2)}\n`);

const queuePath = 'drafts/folklore-art-expansion.json';
const manifest = JSON.parse(fs.readFileSync(queuePath, 'utf8'));
const entry = manifest.queue.find(item => item.id === queueId);
if (!entry) throw new Error(`queue entry not found: ${queueId}`);
entry.status = 'complete';
entry.image = image;
manifest.completed = manifest.queue.filter(item => item.status === 'complete').length;
manifest.remaining = manifest.total - manifest.completed;
fs.writeFileSync(queuePath, `${JSON.stringify(manifest, null, 2)}\n`);
console.log(`${queueId}: complete (${manifest.remaining} remaining)`);
