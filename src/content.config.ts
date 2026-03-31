import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/blog' }),
  schema: z.object({
    layout: z.string().optional(),
    title: z.string(),
    tags: z.union([z.string(), z.array(z.string())]).optional(),
    image: z.string().optional(),
    monospace_title: z.boolean().optional(),
    date: z.union([z.string(), z.date()]).optional(),
    permalink: z.string().optional(),
  }),
});

export const collections = { blog };
