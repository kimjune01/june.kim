import fs from 'node:fs';
import path from 'node:path';
import yaml from 'js-yaml';

fs.writeFileSync(
  'public/assets/parts-bin.json',
  JSON.stringify(yaml.load(fs.readFileSync('src/data/parts-bin.yml', 'utf8'))),
);

// Google Scholar requires citation_pdf_url to remain in the abstract page's
// URL directory. Preserve /assets links and create root-level aliases beside
// the existing /<slug> article pages.
for (const filename of fs.readdirSync('src/content/blog')) {
  if (!filename.endsWith('.md') && !filename.endsWith('.mdx')) continue;
  const source = fs.readFileSync(path.join('src/content/blog', filename), 'utf8');
  if (!/^variant: post-paper$/m.test(source)) continue;

  const slug = filename.replace(/^\d{4}-\d{2}-\d{2}-/, '').replace(/\.mdx?$/, '');
  const pdf = path.join('public/assets', `${slug}.pdf`);
  if (fs.existsSync(pdf)) fs.copyFileSync(pdf, path.join('public', `${slug}.pdf`));
}
