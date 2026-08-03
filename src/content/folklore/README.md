# Folklore records

Each `.json` file is one complete story. The directory is the `folklore` content
collection; the zod schema in `src/content.config.ts` validates every record during
the Astro build.

- `id` is the permanent URL/storage key and must be unique.
- `originalTitle` is the source-language or traditional title shown beside the English title. If the historical source does not preserve one, say so rather than back-translating.
- `order` controls display order.
- `featured` controls the curated first shelf; all stories still appear under regions.
- `region` creates or selects a regional shelf.
- `culture` is the more specific tradition shown beneath that region.
- `language` describes the adaptation, while `themes` support future discovery.
- `art` selects a built-in illustration. Unknown keys receive a neutral book cover,
  so artwork can be added after editorial entry rather than blocking it.
- `scenes` is an array of pages, each containing an array of paragraphs.
- Story length is editorial, not templated. Use as many pages as the tale's natural
  rhythm needs; five pages is not a target or requirement.
- Each finished story targets exactly three illustrations: its cover, one turning-point
  image, and one ending image. `pageArt` attaches the two interior images to zero-based
  page numbers. Records without both entries are still editorial drafts, even when their
  text and cover are present.
- The reader builds a citation from `sourceTitle`, `sourceAuthor`, `sourceYear`, and
  `sourceUrl` and displays it after the text on the final story page.
- `rights` records the edition-level determination, jurisdiction, basis, and date.
- `review` tracks adaptation and cultural review independently. New work should begin
  as `draft` / `pending`; those states are visible in “For grown-ups & sources.”

Copy an existing record when adding a tale. A malformed record or duplicate ID stops
the build with a filename and validation error.
