# june.kim

The source for [june.kim](https://june.kim): June Kim's essays, research notes,
experiments, and project pages. The site is statically generated with Astro and
deployed to S3 behind CloudFront.

## Human Signal

[Human Signal](https://june.kim/human-signal/) is an experiment in measuring how
engineers supervise coding agents. Instead of asking candidates how they would
respond to an agent failure, it introduces controlled perturbations into a work
sample, observes the response in-frame, and keeps the trace behind every hiring
claim.

The current page and synthetic assessment report live in
[`src/pages/human-signal/index.astro`](src/pages/human-signal/index.astro).

## Development

Requires Node.js 22.12 or newer and pnpm.

```bash
pnpm install
pnpm run dev       # main site at http://localhost:12345
pnpm run build     # build the main site and reading site
pnpm run test
```

The main Astro application uses `src/`; the separate reading application uses
`reading-src/`. Production output is assembled in `dist/`.

## Folklore

The illustrated reading room at `/folk/` keeps tales in
`src/content/folklore/` and art in `public/folk/art/`. Editorial rules and the
illustration workflow are documented in
[`src/content/folklore/README.md`](src/content/folklore/README.md).

`folklore/desepia.sh <src_dir> <dst_dir>` corrects sepia-cast art using ffmpeg
signal analysis and produces web-ready images. It requires `ffmpeg` and `cwebp`.

## License

This repository is copyleft. Site code and templates are licensed under
[AGPL-3.0-or-later](LICENSE). Human Signal materials and other written content
are licensed under [CC BY-SA-NS](https://june.kim/cc-by-sa-ns), the CC BY-SA
4.0 terms plus the Network Services source-availability condition reproduced
in [LICENSE](LICENSE). Third-party components retain their stated licenses.
