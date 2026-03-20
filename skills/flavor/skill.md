---
name: flavor
description: Scan a blog post for unlinked pop culture refs, proper nouns, named theories, and historical figures. Suggest hyperlinks with research. Don't change anything until the user approves.
argument-hint: <file_path>
allowed-tools: Read, Edit, Grep, Glob, WebSearch, WebFetch, AskUserQuestion
---

# Flavor: Link Pop Culture and Proper Nouns

Scan a blog post for pop culture references, proper nouns, named theories, historical figures, and film/book/music references that lack hyperlinks. Suggest links that give the reader instant context. Do not fix anything until the user approves.

## Process

1. Read the file.
2. **Scan** for every unlinked reference that a reader might not recognize.
3. **Research** each reference. Use WebSearch to find the best link: YouTube trailers/clips for films, DOIs for papers, Wikipedia for historical figures. Verify the link exists and points to the right thing.
4. Report each as: `L{line}: {type} — "{quoted text}" → [link] {why this link}`
5. Present the list. Wait for the user to say which to fix.
6. Apply fixes. Link inline, don't add footnotes.

## What to Link

**Pop culture.** Films, TV shows, books, albums, characters. Link to a YouTube trailer, clip, or scene when available. Prefer the most recognizable moment. If no YouTube link exists, use Wikipedia or IMDB.

**Historical figures and events.** People, battles, legislation, court cases. Link to Wikipedia or the most authoritative short summary.

**Economic/scientific theories.** Named theorems, models, papers. Link to the original paper (DOI preferred), or Wikipedia if the paper is paywalled.

**Proper nouns the reader might not know.** Companies, products, organizations, places that aren't household names. Link to the company site or Wikipedia.

## What NOT to Link

- Household names that need no explanation (Google, Apple, Microsoft, etc.)
- Terms already linked elsewhere in the same post
- The author's own posts (those are internal links, not flavor)
- Generic concepts that don't have a single canonical reference
- **Terms that appear as examples, not as arguments.** If a reference is illustrating a point made elsewhere (e.g., "prions" in a post about courage, not about biology), linking it adds context the reader doesn't need for *this* post's argument. Only link references that substantiate the argument being made.

## Link Waterfall

For each reference, try link types in this order. Use the first one that exists and fits:

1. **Video / interactive** — YouTube clip, trailer, demo, or interactive explainer. Most engaging; the reader gets context in 60 seconds.
2. **High-quality article** — A well-written news piece, blog post, or profile (TechCrunch, Stratechery, Ars Technica, etc.) that gives narrative context, not just facts.
3. **Official page** — Company site, product page, project README, or conference landing page. Good when the thing *is* the product.
4. **Wikipedia** — Reliable and fast-loading. Best for historical figures, named theories, established companies.
5. **Academic paper** — arXiv, DOI, or SSRN. Use when the post is citing research and the reader might want to verify the claim. Prefer open-access links.
6. **Hugging Face / GitHub** — For models, libraries, and tools. The reader can see the thing itself.

Move down the waterfall when higher options don't exist or feel forced. A Vickrey auction deserves Wikipedia, not a YouTube video. A startup deserves its launch post, not a dry Crunchbase page.

## Judgment Calls

- For references that work as jokes or Easter eggs, the link IS the joke. A reader who clicks should smile.
- When multiple link options exist, pick the one that loads fastest and requires no login.
- One link per reference. Don't double-link the same thing.
- Match the link's tone to the post's tone. Technical posts can link to papers. Narrative posts should prefer articles and videos.
