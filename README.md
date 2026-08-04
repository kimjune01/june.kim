# june.kim

Personal site. Astro, S3 + CloudFront.

```bash
pnpm run dev    # localhost:12345
bash deploy.sh  # build → S3 → CloudFront invalidation
```

## Folklore

Illustrated reading room at `/folk/` — tales in `src/content/folklore/`, art in `public/folk/art/`.

`folklore/desepia.sh <src_dir> <dst_dir>` fixes sepia-cast art: it measures each image's warmth (ffprobe signalstats) and applies ffmpeg white balance, cooling, and yellow/red desaturation scaled to that warmth, so neutral images pass through untouched. Needs `ffmpeg` and `cwebp`. Run it on a batch of new art before committing.
