I could not firmly verify ~5 qualifying cases from the live repo pages in this run. GitHub repository index pages loaded, but individual issue/PR detail pages and diffs repeatedly failed with cache-miss errors, so I could only verify list-level facts such as PR titles, numbers, open/merge/close dates, and labels. I would not treat the following as benchmark-ready without a second pass through PR discussions/diffs.

**Near-Misses / Leads**

1. `biomejs/biome`  
Issue/PR area: Svelte / HTML parser semantics  
Live-index evidence: closed PR `#10488` “allow TypeScript as const in Svelte each and comma selectors in :global()” was closed May 28, 2026; nearby merged PR `#10487` “allow omitting binding in Svelte {:then} and {:catch} blocks” merged May 29, 2026. Source: GitHub PR list lines showing both PRs and dates.  
Why it is promising: parser edge-case semantics, likely ambiguous Svelte compatibility choices.  
Why not firm: I could not verify that both PRs address the same issue, nor inspect discussion/tests.

2. `biomejs/biome`  
Issue/PR area: Markdown parser list/fence semantics  
Live-index evidence: merged parser PRs `#10466`, `#10471`, and `#10483` landed May 26-29, 2026 around blank-line separators, fenced code blocks at list boundaries, and loose lists across empty items. Source: GitHub PR list lines 305-343.  
Why it is promising: Markdown list looseness and boundary handling are classic convention/intent ambiguities.  
Why not firm: no verified narrow-vs-general sequence or linked issue; could just be independent bug fixes.

3. `astral-sh/ruff`  
Issue/PR area: parser stack overflow  
Live-index evidence: PR `#25462` “[parser] Bound iterative expression chains to avoid stack overflow” was closed May 30, 2026. Source: GitHub PR list lines 344-346.  
Why it is promising: parser robustness, likely narrow “cap recursion” vs broader parser-architecture decision.  
Why not firm: I could not verify a merged general replacement PR or shipped-test oracle gap.

4. `astral-sh/ruff`  
Issue/PR area: Python type checker cycle behavior  
Live-index evidence: PR `#25475` “[ty] Handle cycles in function decorator inference” merged May 30, 2026. Source: GitHub PR list lines 309-310.  
Why it is promising: cycle recovery often encodes policy choices about fallback types/error recovery.  
Why not firm: no verified prior narrow PR or debate; likely DIFFICULTY, not durable ambiguity, unless discussion shows competing intended semantics.

5. `prettier/prettier`  
Issue/PR area: Markdown formatting conventions  
Live-index evidence: open PRs in June 2026 include “preserve original fenced-code-block fence length,” “respect useTabs for indented code blocks and footnote bodies,” and “Cap ordered list mark at 999,999,999.” Source: GitHub PR list lines 312-329.  
Why it is promising: formatter output conventions are high-ambiguity by nature.  
Why not firm: these were open in the live index, not verified merged fixes, so they do not meet your contamination/opened-and-fixed requirement yet.

Bottom line: I found several plausible recent leads, but zero that I can honestly mark as fully qualifying with the available detail-page access. The strongest next pass should target Biome Markdown/Svelte parser PR discussions and Ruff parser/type-checker PRs, checking whether closed drafts or review comments point to the later merged oracle.