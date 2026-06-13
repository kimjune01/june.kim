import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/blog' }),
  schema: z.object({
    variant: z.string().optional(),
    autonumber: z.boolean().optional(),
    title: z.string(),
    subtitle: z.string().optional(),
    tags: z.union([z.string(), z.array(z.string())]).optional(),
    image: z.string().optional(),
    keywords: z.union([z.string(), z.array(z.string())]).optional(),
    monospace_title: z.boolean().optional(),
    date: z.union([z.string(), z.date()]).optional(),
    permalink: z.string().optional(),
  }),
});

export const collections = { blog };
