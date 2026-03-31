# june.kim

Astro site hosted on S3 + CloudFront. Unified build: blog + reading + apps.

## Architecture

- **Blog posts**: `~/Documents/junekim-migrates/src/content/blog/*.md`
- **Reading site**: `~/Documents/junekim-migrates/src/pages/reading/`
- **Apps** (static, in `public/`): jamdojo, pinyin-chart, advertising-journey, croupier, vectorspace-ads
- **Styling**: Tailwind (one `blog.css` for blog pages, reading pages use their own Tailwind)

## Local dev

`cd ~/Documents/junekim-migrates && pnpm run dev` — runs on port 12345 with hot reload.

## Deploy

`cd ~/Documents/junekim-migrates && bash deploy.sh` — builds, creates .html aliases, syncs to S3, invalidates CloudFront.

## Adding a post

Create `src/content/blog/YYYY-MM-DD-slug.md` with front matter:
```yaml
---
layout: post
title: "Post Title"
tags: tag1, tag2
---
```

Tags are comma-separated. Available tags: coding, cognition, methodology, reflecting, envelopay, pageleft, vector-space, poetry, crafting, improving, projects, reading.

## Legacy

This repo (`june.kim`) contains the original Jekyll source. It's kept for git history but no longer used for builds. The canonical source is `~/Documents/junekim-migrates/`.

## Editing style

When the user makes one-liner edits to prose, always give brief feedback — praise what works, push back if something weakens the writing. Don't just silently apply edits. The user wants a writing partner, not a text editor.

## Codex review

When sending posts to codex for review, don't roleplay. No "You are a senior editor." Just ask directly: what works, what doesn't, what to cut, what to strengthen.
