import { existsSync, readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';

const root = new URL('../', import.meta.url);
const read = (path: string) => readFileSync(new URL(path, root), 'utf8');

describe('Google Scholar paper discovery', () => {
  const layout = read('src/layouts/BlogPost.astro');

  it('publishes the PDF beside the article URL', () => {
    expect(layout).toContain('`https://june.kim/${slug}.pdf`');
  });

  it('shows the author and publication date next to each paper title', () => {
    expect(layout).toContain('class="citation_author"');
    expect(layout).toContain('class="citation_publication_date"');
  });

  it('provides a repository-style papers index', () => {
    expect(existsSync(new URL('src/pages/papers/index.astro', root))).toBe(true);
  });
});
