# Table Style: Convert Markdown Tables to Styled HTML

Convert markdown tables in blog posts to styled HTML tables matching the site's design system.

## When to use

When a blog post contains markdown tables (`| ... | ... |`) that need to render consistently with the site's existing styled tables.

## Process

1. Read the file.
2. Find all markdown tables.
3. Convert each to the HTML format below.
4. Apply directly — this is a mechanical transformation, not a judgment call.

## HTML format

```html
<table style="max-width:700px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:Xem"><col>...</colgroup>
<thead><tr><th style="background:#f0f0f0">Header</th>...</tr></thead>
<tr><td>Cell</td>...</tr>
</table>
```

## Rules

- `max-width:700px; margin:1em auto; font-size:14px;` on every `<table>`.
- `background:#f0f0f0` on every `<th>`.
- Use `<colgroup>` with `width` in `em` units. Size the first column to fit its longest content; let the last column flex.
- Use `white-space:nowrap` on cells with arrows or type signatures (e.g., `encoded → indexed`).
- Use `font-style:italic` on cells that represent backward/async operations (e.g., Consolidate).
- Links in cells use `<a href="...">` tags, not markdown syntax.
- When a cell has an associated source/reference URL, link the cell text directly with `<a href="...">` instead of adding a separate "Source" column. Fewer columns, same information.
- No `<div class="table-wrap">` unless the table has 5+ columns. For wide tables, wrap in `<div class="table-wrap">`.
- **Mobile:** use `max-width` not `width` so tables can shrink. Wide tables (5+ columns) should use `max-width:70%` on desktop but still be usable on mobile — the `table-wrap` div provides horizontal scroll. Never set a fixed `width` that would overflow the viewport.
- Preserve cell content exactly — do not edit text, only convert format.
