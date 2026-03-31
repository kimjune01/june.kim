# SVG Dark Mode

Make an SVG work in both light and dark mode using CSS inversion.

## When to use

After creating or editing an SVG that will be displayed on a page with a dark/light theme toggle.

## Process

1. **Audit the SVG fills.** Any `fill:#fff` or `fill:white` will invert to black. Change to `fill:none` (transparent). Backgrounds must be transparent, not white.

2. **Design for light mode.** Use dark strokes and text on transparent background. The inversion handles dark mode automatically.

3. **Color rules:**
   - Backgrounds/box fills: `none` (never `#fff`)
   - Strokes: dark grays (`#999`, `#666`, `#333`)
   - Text: dark (`#1f2937` or similar)
   - Accents (green, blue, etc.): will shift hue when inverted — test both modes

4. **Register for inversion.** Add a CSS selector in the site's global styles that targets the SVG and applies `filter: invert(1)` in dark mode, `filter: none` in light mode. Match by `src` attribute or `alt` tag.

   Pattern (junekim-reading site — `src/layouts/Base.astro`, `is:global` block):
   ```css
   img[src$="-pipeline.svg"] { filter: invert(1); }
   :root.light img[src$="-pipeline.svg"] { filter: none; }
   ```

   Or use an alt-tag convention for a category of SVGs:
   ```css
   img[alt="diagram"] { filter: invert(1); }
   :root.light img[alt="diagram"] { filter: none; }
   ```

5. **Verify both modes.** Toggle the theme and check:
   - Text is readable in both
   - No black rectangles (leftover `fill:#fff`)
   - Strokes are visible but not loud
   - Accent colors still make sense after inversion

## Gotchas

- `filter: invert(1)` inverts everything including accent colors. A green (`#4ade80`) becomes magenta. If accent color fidelity matters, use `currentColor` with `opacity` instead of inversion.
- SVGs with embedded raster images (screenshots, photos) can't use inversion — the photo will look wrong.
- The `is:global` block is required on the junekim-reading site because `@layer base` loses to browser UA defaults.
