# Finding a Zenodo textbook's parent source

A Zenodo book deposit is an archival copy. The reading experience lives elsewhere, on the "parent source." The metadata says whether a parent exists, and what kind, before you open anything.

## The rule

Parent source exists ⟺ `communities` is non-empty OR `related_identifiers` holds a GitHub or URL target. Neither present means the PDF is the end of the line.

## Three classes

**1. Publisher / institution backed.** The community is the parent. Membership guarantees a live HTML+PDF home on that publisher's platform. `communities` is the giveaway here.

| Record | community | parent platform |
|---|---|---|
| Grammatical theory | `langscipress` | langsci-press.org |
| Economic Principles in Cell Biology | `epcp` | principlescellphysiology.org |
| Základy histológie | `pavol-jozef-safarik-...-kosice` | unibook.upjs.sk |
| Metode i instrumentacija | `msr_etf` | ETF Belgrade dept. |

Checked `langscipress` directly: resolves to Language Science Press, every sampled title carries a `langsci` DOI landing on their HTML book. One community, one reading platform.

**2. Solo author with a build repo.** `communities` empty; `related_identifiers` is the giveaway. Often the best reading UX (Sphinx / Quarto / bookdown / Jupyter Book).

- Deep R Programming: `isSupplementTo → github.com/gagolews/deepr`, `isPublishedIn → deepr.gagolewski.com` (Sphinx/Furo)
- earthlab earth-analytics: `isSupplementTo → github.com/earthlab/...-textbook` (Jupyter Book)

Tell: `isSupplementTo` / `isPublishedIn` pointing at github.com (build source) or a bare URL (rendered book).

**3. Terminal PDF.** Both fields empty. Zenodo is the home. Buku Ajar, Textbook of Engineering Physics, the Šlomo Surayt courses, the Pharmaceutical Chemistry ones. Surayt only leaks `surayt.com` as free text in the description, a weak unstructured third signal.

## Consequence for harvesting

Filtering by `communities` harvests publisher-backed books cleanly but silently drops the solo-authored HTML books, which often read best. Query on community OR a `related_identifiers` URL/GitHub target to catch both.

## API

```
https://zenodo.org/api/records?communities=langscipress&size=6&sort=mostviewed
https://zenodo.org/api/records?q=textbook&type=publication&subtype=book&sort=mostviewed
https://zenodo.org/api/communities/langscipress   # title + website
```

Per record, the fields that matter: `metadata.communities[].id`, `metadata.related_identifiers[]` (relation + identifier), `metadata.title`, license.

## Harvest output

Ran the rule over the `textbook` book search plus the `langscipress` community: 33 unique records, 15 with a parent source, 18 terminal PDFs dropped. Community ids resolved to their reading platform by hand (Zenodo's `website` field is mostly empty).

Class 2, solo author with a build repo. Verified live:

- [Deep R Programming](https://deepr.gagolewski.com) — Gagolewski, Sphinx/Furo, dark mode + sidebar TOC (CC BY-NC-ND 4.0)
- [Economic Principles in Cell Biology](https://principlescellphysiology.org/book-economic-principles/) — lectures + problems + code (CC BY 4.0)
- earth-analytics intermediate — Jupyter Book, source at [github.com/earthlab/...-textbook](https://github.com/earthlab/earth-analytics-intermediate-earth-data-science-textbook) (CC BY-NC-SA 4.0)

Class 1, publisher / institution. Parent is the platform; each title has its own page there:

- [Language Science Press](https://langsci-press.org) — open linguistics press, HTML+PDF per title. From this pull: Grammatical theory; From fieldwork to linguistic theory; A history of English; Corpus linguistics; Analyzing meaning; Phonology in the Twentieth Century; Machine translation for everyone; Arabic and contact-induced change (all CC BY / BY-SA 4.0)
- [unibook.upjs.sk](https://unibook.upjs.sk/) — Univ. of Košice press; Základy histológie I (CC BY 4.0)
- msr_etf — ETF Belgrade dept.; Metode i instrumentacija za električna merenja (CC BY 4.0)
- lory (zhbluzern) — Swiss institutional repo, weak reading UX; Lehrentwicklung by Openness (CC BY-NC-ND 4.0)

Dropped as terminal PDFs (no community, no related URL): Buku Ajar Kimia Analitik, Textbook of Engineering Physics, the four Šlomo Surayt courses, three English-for-EE collections, Pharmaceutical Organic Chemistry, Logistics, and others.

## Reading UX is a second axis

Having a parent source does not mean it reads well. The parent's quality cuts across both classes. Checked each:

Web-native (sidebar TOC, chapter pages, search, dark mode). These went to /reading:

- Deep R Programming — Sphinx/Furo. Added under Computer Science.
- Intermediate Earth Data Science (earthlab) — Jupyter Book, rendered at earthdatascience.org. Added under Computer Science.

PDF-primary (download, or an embedded PDF viewer dressed as "read in browser"). Good content, weak reading UX. Build-your-own candidates:

- Economic Principles in Cell Biology — "read in browser" is an embedded PDF. Structured as lectures + problems + code, so it would rebuild cleanly into an HTML book. Strongest candidate.
- Language Science Press (all 8 sampled titles) — download-only PDF, no HTML reader at all. A press-wide reader would be the high-leverage build, not one title.
- unibook.upjs.sk (Základy histológie), msr_etf, lory — institutional repos, PDF delivery.
- The 18 terminal PDFs — no parent, Zenodo-hosted PDF is all there is.

So the community/repo signal finds a *parent*; a second pass on the parent (Sphinx/Quarto/Jupyter Book vs PDF) decides whether it's a link or a build.

## Notes for reuse

- `size` caps at 25 per unauthenticated request; page or authenticate for more.
- Community `website` field is usually empty, so id-to-platform is a manual map. Worth caching a lookup table for the venues that recur (langscipress, epcp, upjs).
- License lives in `metadata.license.id` (e.g. `cc-by-4.0`) or the `rights` list on older records.
- Community-only records give you the *platform*, not the per-title deep link. The langsci records carry no `related_identifiers` at all, just an ISBN, so the catalog URL has to be resolved on langsci-press.org by title/ISBN. (Where a record does carry a `langsci.bNN` DOI, `NN` is the catalog book number: `langsci-press.org/catalog/book/NN`.)
