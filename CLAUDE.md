# june.kim blog

Jekyll blog hosted on S3 + CloudFront.

## Local dev

`bundle exec jekyll serve --livereload` — runs on port 4000 with auto-reload.

## Deploy

`bash deploy.sh` — builds the site and syncs to S3, then invalidates CloudFront.

## Editing style

When the user makes one-liner edits to prose, always give brief feedback — praise what works, push back if something weakens the writing. Don't just silently apply edits. The user wants a writing partner, not a text editor.
