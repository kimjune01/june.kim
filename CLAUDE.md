# june.kim

Astro site hosted on S3 + CloudFront. Unified build: blog + reading + apps.

## Local dev

`pnpm run dev` — runs on port 12345 with hot reload.

## Deploy

`bash deploy.sh` — builds, creates .html aliases, syncs to S3, invalidates CloudFront.

## Adding a post

Create `src/content/blog/YYYY-MM-DD-slug.md` with front matter:
```yaml
---
layout: post
title: "Post Title"
tags: tag1, tag2
image: "/assets/slug-name.png"
---
```

`image:` sets the social preview (`og:image`, `twitter:card`, JSON-LD). It's independent of images in the post body — an inline diagram is not an og:image. Set it when the post has a meaningful preview image. Not all posts need one.

Tags are comma-separated. Available tags: coding, cognition, methodology, reflecting, envelopay, pageleft, vector-space, poetry, crafting, improving, projects, reading.

Posts that need component imports use `.mdx` extension. **Omit `layout` from `.mdx` frontmatter** — MDX treats it as an import. The default (`post`) is applied by `[slug].astro`. Content collection glob accepts both `**/*.{md,mdx}`.

## Structure

- **Blog posts**: `src/content/blog/*.md`
- **Blog layouts**: `src/layouts/BlogPost.astro`, `src/layouts/TagPage.astro`
- **Reading site**: `src/pages/reading/` (Astro + React islands, Scheme/Python REPLs)
- **Apps** (pre-built, in `public/`): jamdojo, pinyin-chart, advertising-journey, croupier, vectorspace-ads
- **Styling**: Tailwind — `src/styles/blog.css` for blog, reading pages use their own

## Editing style

When the user makes one-liner edits to prose, always give brief feedback — praise what works, push back if something weakens the writing. Don't just silently apply edits. The user wants a writing partner, not a text editor.

## Codex review

When sending posts to codex for review, don't roleplay. No "You are a senior editor." Just ask directly: what works, what doesn't, what to cut, what to strengthen.
