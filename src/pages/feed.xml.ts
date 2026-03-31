import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';

export async function GET(context: any) {
  const posts = await getCollection('blog');
  const sorted = posts.sort((a, b) => {
    const dateA = a.id.match(/^(\d{4}-\d{2}-\d{2})/)?.[1] || '';
    const dateB = b.id.match(/^(\d{4}-\d{2}-\d{2})/)?.[1] || '';
    return dateB.localeCompare(dateA);
  });

  return rss({
    title: 'june.kim',
    description: 'Blog posts by June Kim',
    site: context.site,
    items: sorted.map(post => {
      const slug = post.id.replace(/^\d{4}-\d{2}-\d{2}-/, '');
      const dateMatch = post.id.match(/^(\d{4}-\d{2}-\d{2})/);
      const pubDate = dateMatch ? new Date(dateMatch[1]) : new Date();
      return {
        title: post.data.title,
        pubDate,
        link: `/${slug}/`,
        categories: typeof post.data.tags === 'string'
          ? post.data.tags.split(/[,\s]+/).map(t => t.trim()).filter(Boolean)
          : (post.data.tags || []),
      };
    }),
  });
}
