import { getCollection } from 'astro:content';
import type { APIRoute, GetStaticPaths } from 'astro';

export const getStaticPaths: GetStaticPaths = async () => {
  const posts = await getCollection('blog');
  return posts.map((post) => {
    const slug = post.id.replace(/^\d{4}-\d{2}-\d{2}-/, '');
    return {
      params: { slug },
      props: { post },
    };
  });
};

export const GET: APIRoute = async ({ props }) => {
  const { post } = props as any;
  // Strip front matter from the raw body
  const raw = post.body || '';
  return new Response(raw, {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' },
  });
};
