// @ts-check
import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';

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
    shikiConfig: {
      theme: 'github-light',
    },
  },
  vite: {
    plugins: [tailwindcss()],
    server: {
      headers: { 'Cache-Control': 'no-store' },
      hmr: { overlay: true },
    },
  },
});
