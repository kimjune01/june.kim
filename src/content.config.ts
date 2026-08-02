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

const folklore = defineCollection({
  loader: glob({ pattern: '**/*.json', base: './src/content/folklore' }),
  schema: z.object({
    id: z.string(),
    order: z.number().int(),
    featured: z.boolean(),
    title: z.string(),
    originalTitle: z.string(),
    tradition: z.string(),
    region: z.string(),
    culture: z.string(),
    place: z.string(),
    ages: z.string(),
    minutes: z.number().int(),
    language: z.string(),
    themes: z.array(z.string()),
    color: z.string(),
    colorSoft: z.string(),
    sourceTitle: z.string(),
    sourceAuthor: z.string(),
    sourceYear: z.string(),
    sourceUrl: z.string().url(),
    note: z.string(),
    artLabel: z.string(),
    art: z.string(),
    image: z.string().optional(),
    pageArt: z.array(z.object({
      page: z.number().int().nonnegative(),
      image: z.string(),
      alt: z.string(),
    })).optional(),
    scenes: z.array(z.array(z.string()).nonempty()).nonempty(),
    rights: z.object({
      status: z.enum(['verified', 'review']),
      basis: z.string(),
      jurisdiction: z.string(),
      checked: z.string(),
    }),
    review: z.object({
      adaptation: z.enum(['draft', 'reviewed']),
      cultural: z.enum(['pending', 'reviewed']),
      reviewer: z.string().optional(),
    }),
  }),
});

export const collections = { blog, folklore };
