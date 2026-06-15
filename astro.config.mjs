// @ts-check
import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';
// Auto-numbers section headings on posts with `autonumber: true`. See the
// plugin file for the authoring syntax. Runs during `astro dev` and `astro build`.
import remarkSectionNumbers from './src/plugins/remark-section-numbers.mjs';
// Wraps lone-image paragraphs in <figure><figcaption> (caption from alt) so
// clean-markdown figures render with captions. See the plugin header.
import rehypeFigures from './src/plugins/rehype-figures.mjs';

export default defineConfig({
  integrations: [react(), mdx(), sitemap()],
  site: 'https://june.kim',
  base: '/',
  server: { port: 12345 },
  devToolbar: { enabled: false },
  image: {
    service: { entrypoint: 'astro/assets/services/noop' },
  },
  markdown: {
    remarkPlugins: [remarkSectionNumbers],
    rehypePlugins: [rehypeFigures],
    shikiConfig: {
      theme: 'github-light',
    },
  },
  vite: {
    plugins: [tailwindcss()],
    server: {
      headers: { 'Cache-Control': 'no-store' },
      hmr: { overlay: true },
      watch: {
        ignored: [
          '**/.claude/worktrees/**',
          '**/.claude/projects/**',
          '**/torch_compile_debug/**',
          '**/test/**',
          '**/check/**',
          '**/.petricode/**',
          '**/worklog/**',
          '**/data/**',
          '**/dump.rdb',
          '**/_site/**',
        ],
      },
    },
  },
});
