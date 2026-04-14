# Typography
Source: /practical-typography

## Use When
- Reviewing any text-heavy interface (blog, docs, email, dashboard, forms)
- Setting up or auditing typographic styles
- Text "looks fine" but feels hard to read

## Look For
- **Line length**: lines longer than 90 characters or shorter than 45 characters
- **Line spacing**: line-height below 120% or above 145% of font size
- **Font size**: body text below 15-16px on screen
- **Paragraph spacing**: missing or inconsistent spacing between paragraphs
- **Heading hierarchy**: headings that don't form a clear size/weight ladder
- **System font fallback**: custom font with no fallback, causing layout shift on load
- **Measure violations**: full-width text on wide screens with no max-width constraint

## Common Findings
- violation: Body text at 13-14px (below minimum readable size on screen)
- violation: Line length exceeds 90 characters on desktop (eye loses tracking on return)
- violation: No paragraph spacing — paragraphs separated only by indent or nothing
- risk: Line-height at 1.0 or 1.1 (too tight for comfortable reading)
- risk: Headings use only size, not weight, making hierarchy ambiguous at smaller sizes
- suggestion: Add max-width to text containers to keep line length in 45-90 character range

## Evidence Required
- Measure body font size in px (inspect computed styles, not just CSS declaration)
- Count characters per line at the most common viewport width
- Measure line-height as percentage of font size
- Check paragraph spacing (should be 50-100% of body text size per Butterick)
- Verify heading hierarchy: h1 > h2 > h3 visually distinct through size and/or weight
- Reference: practicaltypography.com (line-length, line-spacing, font-size, headings pages)

## Recommendations
- Body font size: 16-20px on screen (never below 15px)
- Line length: 45-90 characters (roughly 500-700px max-width for body text)
- Line-height: 120-145% of font size (1.4-1.5 for body text is a safe default)
- Paragraph spacing: 50-100% of body font size
- Heading hierarchy: clear visual ladder using size + weight
- Font choice: system fonts are safe; web fonts add voice but are a user decision, not an agent decision
- Vertical rhythm: paragraph spacing and line-height should share the spacing system's base unit

## Avoid
- Recommending specific typefaces without asking the user about tone/voice
- Treating typographic rules as style preferences (readability research predates screens)
- Adjusting only one metric (e.g., font size) without checking its effect on line length and line-height
