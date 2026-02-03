---
layout: post
title: "Condensation: Preprocess by Source"
tags: coding
---

> This post was written by Claude Opus 4.5. The pattern is my contribution to [Little Bird](https://verylittlebird.com). I validated it against existing RAG literature and asked Claude to write it up in my voice.

---

RAG preprocessing literature focuses on document types. PDF chunking. HTML cleaning. Markdown parsing.

But what about the same format from different sources?

A scraped e-commerce page and a scraped blog post are both HTML. But product pages are 80% navigation and ads. Blog posts are 80% content. If you embed both the same way, you're polluting your vector space with noise.

### The Pattern

Detect the source type. Apply source-specific LLM filtering. Then embed.

```python
def get_condense_prompt(source_type: str) -> str | None:

    if source_type == "terminal":
        return """
        Extract only:
        - User-entered commands
        - Essential command outputs
        Exclude UI elements. Limit to 50 lines.
        """

    if source_type == "conversation":
        return """
        Extract the complete dialogue:
        - Preserve messages verbatim
        - Include timestamps
        - Filter out buttons and navigation
        """

    if source_type == "task_tracker":
        return """
        Extract user-generated content:
        - Tasks, deliverables, deadlines
        - Filter out UI clutter
        """

    if source_type == "ecommerce":
        return """
        Extract product information:
        - Name, price, specs, reviews
        - Filter out navigation, ads, recommendations
        """

    return None
```

### Why This Works

The LLM acts as a semantic filter. It knows what's signal vs noise for each source:

| Source | Signal | Noise |
|--------|--------|-------|
| Terminal | Commands, outputs | Window chrome, prompts |
| Conversation | Messages, timestamps | Buttons, navigation |
| Task tracker | Tasks, deadlines | UI clutter, empty states |
| E-commerce | Product details, reviews | Ads, nav, recommendations |
| Documentation | Content, code blocks | Sidebars, footers |

By filtering before embedding, you get cleaner vectors. Similar content clusters together instead of being scattered by structural noise.

### The Pipeline

```
Scrape → Extract Text → Detect Source → Condense → Chunk → Embed
                              ↓
                    Source-specific LLM prompt
```

Without condensation, a 2000-token terminal dump might have 200 tokens of actual commands. With condensation, you embed those 200 tokens directly.

### When to Skip

Not every source needs condensation. Return `None` for unknown sources—just embed the raw text. Condensation is for sources where you've validated the noise ratio is high enough to warrant the extra LLM call.

```python
prompt = get_condense_prompt(source_type)
if prompt:
    condensed = await llm_condense(text, prompt)
    return embed(condensed)
else:
    return embed(text)
```

### Beyond Filtering: Validation Thresholds

The same principle applies to scraping validation. In [Linky](https://github.com/kimjune01/linky), different LinkedIn resources have different "completeness" expectations:

```python
# Profile: need substantial data before considering it complete
await wait_for_file(file_path, min_lines=20, max_wait=10)

# Search results: just need header + some results
await wait_for_file(file_path, min_lines=2, max_wait=20)
```

| Resource | Min Lines | Max Wait | Why |
|----------|-----------|----------|-----|
| Profile | 20 | 10s | Full profile is substantial |
| Search | 2 | 20s | Just needs header + results |

A profile with 5 lines is probably incomplete. A search result with 5 lines is fine. Source-aware heuristics, not one-size-fits-all.

### Results

Retrieval improved after adding source-aware condensation. Terminal commands actually surface when you search for them. Conversations stay coherent. Task queries find tasks, not button labels.

The tradeoff is latency—one extra LLM call per input. Worth it for async pipelines.

Most RAG guides tell you to preprocess by file type. This is preprocessing by semantic source. Different sources, different noise, different filters.

---

> This post was written by Claude Opus 4.5.
