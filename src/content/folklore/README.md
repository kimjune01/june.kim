# Folklore collection

This is a small, illustrated reading room for familiar folk tales and fables. Each
story should be pleasant to read on a tablet and should point interested readers to
a reasonable public-domain edition or interpretation.

It is not a critical edition or archival transcription project. The aim is simpler:
keep a readable copy of each tale, identify where that version came from, and make it
easy to explore related traditions.

Each JSON file is one story and acts as the source of truth for its shelves, card,
reader pages, citation, and illustrations. Astro validates the records during builds.

## Editorial approach

For each story:

1. Choose a recognizable version from a credible public-domain collection.
2. Confirm that the linked edition contains the story and is reusable in the intended
   publication jurisdiction.
3. Make a comfortable reading copy. It is fine to remove book furniture, repair
   obvious transcription errors, normalize awkward line breaks, and divide the story
   into screen-sized pages.
4. Keep the tale recognizably faithful to the chosen version. If it is substantially
   shortened, simplified, combined with another version, or newly written, describe
   it as a retelling rather than implying that it is the source text.
5. Give the reader a useful pointer: collection title, author, editor or translator,
   year, and a working link to the edition.

This project does not need to settle which variant is definitive. Older collections
may use dated wording or framing; use reasonable judgment about audience and context.
Legal availability does not automatically make every presentation considerate, but
formal scholarly review is not a prerequisite for adding a story.

Set `published` to `false` when the source pointer is wrong, missing, or still being
worked out. The record will continue to validate without appearing in the library.

## Record anatomy

- `id` is the permanent URL and local-storage key. Avoid changing it after release.
- `order` controls shelf order; `featured` selects the opening shelf.
- `published: false` withholds an incomplete record. It may be omitted otherwise.
- `title` is the English reading title. `originalTitle` records a documented
  source-language or traditional title when one is reasonably available; avoid
  presenting a newly back-translated title as historical fact.
- `tradition`, `region`, and `culture` organize the shelves. Use the most useful
  attribution supported by the chosen collection.
- `place`, `ages`, `minutes`, and `themes` help readers browse. `language` describes
  the text displayed by the site.
- `sourceTitle`, `sourceAuthor`, `sourceYear`, and `sourceUrl` form the pointer shown
  at the end of the story. `note` briefly explains how the reading copy relates to it.
- `rights` records the edition-level rights check. `review` is lightweight editorial
  bookkeeping for text and cultural checks, not a claim of scholarly certification.
- `scenes` contains the reading pages; each page is an array of paragraphs. Page
  divisions are part of the screen layout, not the underlying tale.
- `image` is the cover. `pageArt` places interior illustrations on distinct,
  zero-based, non-cover pages. Every image needs useful alt text.
- `art`, `artLabel`, `color`, and `colorSoft` supply visual metadata and palette.

## Reading and illustration rhythm

Story length follows the story. Five pages is neither a target nor a maximum. Break
at natural paragraph or scene boundaries and favor comfortable tablet-sized pages.

Each finished story has a cover plus interior illustrations scaled to its length:
roughly every other scene for stories up to six scenes, up to four interior images for
stories up to twelve scenes, and up to six major-beat images for longer stories. They
should keep a consistent cast and visual language, suit the tale’s setting where
practical, and appear near the passage they depict. All artwork is shown at its natural
aspect ratio; the reader scrolls rather than cropping an illustration.

If page divisions change, recheck `pageArt.page`. The schema rejects cover placements,
out-of-range indexes, duplicate interior pages, and records with too few or too many
interior images for their length.

## Expanding interior artwork

`scripts/plan-folklore-art-expansion.mjs` derives missing illustration beats from the
current story records and writes `drafts/folklore-art-expansion.json`. The checked-in
manifest is also the completion ledger; its current 118-item expansion is fully drained.
Regenerating it starts a fresh plan based on whatever artwork is then present.

For each pending entry:

1. Generate a landscape 4:3 scene from its prompt, adjusting frightening or harmful
   passages to a faithful, child-safe beat when needed.
2. Visually review the result for narrative accuracy, cultural cues, unwanted text,
   character consistency, and suitability for ages 6–8.
3. Optimize the approved image as WebP at the entry's `output` path. For a batch with
   a strong sepia cast, run `folklore/desepia.sh <src_dir> <dst_dir>` first.
4. Register the image and alt text in both the story and manifest:

   ```sh
   node scripts/record-folklore-art.mjs <story:page> <web-image-path> "<alt text>"
   ```

   `web-image-path` is the public URL form, such as
   `/folk/art/snow-white/24-scene.webp`, not the `public/` filesystem path.
5. Before committing, run `pnpm validate:folklore` and `git diff --check`. Confirm the
   manifest counters agree with its entries and that every recorded image exists.

## Adding a story

Copy a nearby JSON record and assign a unique, stable `id`. Put optimized web images
under `public/folk/art/`, following the existing cover and story-directory naming
conventions. Then run:

```sh
pnpm validate:folklore
pnpm exec astro build
```

The schema lives in `src/content.config.ts`. `src/lib/folklore.ts` rejects duplicate
IDs, orders the collection, and filters withheld records. A malformed record stops the
build with a validation error.

The practical test is straightforward: can a child or grown-up enjoy this version,
and can they follow the citation to understand where it came from?
