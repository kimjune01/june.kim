import { getCollection, type CollectionEntry } from 'astro:content';

export type FolkloreStory = CollectionEntry<'folklore'>['data'];

export async function loadFolkloreStories(): Promise<FolkloreStory[]> {
  const entries = await getCollection('folklore');
  const stories = entries.map(entry => entry.data);
  const ids = new Set<string>();
  for (const story of stories) {
    if (ids.has(story.id)) throw new Error(`Duplicate folklore story id: ${story.id}`);
    ids.add(story.id);
  }
  return stories.sort((a, b) => a.order - b.order || a.title.localeCompare(b.title));
}
