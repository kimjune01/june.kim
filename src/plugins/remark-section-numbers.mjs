// Auto-numbers paper-style section headings at build time.
//
// WHY: so you can reorder sections freely without hand-renumbering. You write
// plain headings; the build assigns the numbers. Cross-references are ordinary
// markdown links to heading ids (e.g. `[Future Work](#future-work)`), so they
// never go stale on reorder.
//
// OPT-IN: only runs on posts with `autonumber: true` in frontmatter.
//
// AUTHORING SYNTAX (directives go at the end of a heading, in braces):
//   ## Introduction              -> "1. Introduction"        (numbered, id auto-slugged)
//   ## Method {#method}          -> "2. Method"              (explicit id for linking)
//   ### The inquiry frame        -> "2.1 The inquiry frame"  (sub-numbered under its h2)
//   ## Abstract {-}              -> "Abstract"               (unnumbered, skipped by counter)
//   ## Search protocol {.appendix}-> "Appendix A. Search protocol"
//   ### Queries (under appendix) -> "A.1 Queries"
// Directives compose: `## Acknowledgments {-} {#ack}`.
//
// This runs as a REMARK plugin (operates on the markdown AST before HTML id
// generation), and sets each heading's id via `data.hProperties.id` so Astro's
// own heading-id pass leaves it alone. Ids are derived from heading TEXT, never
// from the assigned number, so reordering changes numbers but not ids/links.

/** Slugify heading text into a stable id (GitHub-style, dependency-free). */
function slug(text) {
  return text
    .toLowerCase()
    .replace(/[^\w\s-]/g, '')
    .trim()
    .replace(/\s+/g, '-');
}

/**
 * Pure numbering core. Given an ordered list of parsed headings, return the
 * display label for each (or '' for unnumbered). Exported for unit testing.
 * @param {{depth:number, unnumbered:boolean, appendix:boolean}[]} headings
 * @returns {string[]} label per heading, e.g. "8.", "8.3", "Appendix A.", "A.1", ""
 */
export function numberHeadings(headings) {
  let h2 = 0, h3 = 0;            // body counters
  let inAppendix = false;
  let apIdx = -1, apLetter = '', apH3 = 0;
  return headings.map(({ depth, unnumbered, appendix }) => {
    if (unnumbered) return '';
    if (appendix && depth === 2) {
      inAppendix = true;
      apIdx += 1;
      apLetter = String.fromCharCode(65 + apIdx); // A, B, C...
      apH3 = 0;
      return `Appendix ${apLetter}.`;
    }
    if (inAppendix) {
      if (depth === 2) { apIdx += 1; apLetter = String.fromCharCode(65 + apIdx); apH3 = 0; return `Appendix ${apLetter}.`; }
      if (depth === 3) { apH3 += 1; return `${apLetter}.${apH3}`; }
      return '';
    }
    if (depth === 2) { h2 += 1; h3 = 0; return `${h2}.`; }
    if (depth === 3) { h3 += 1; return `${h2}.${h3}`; }
    return '';
  });
}

/** Concatenate the plain-text content of an mdast heading's children. */
function headingText(node) {
  let s = '';
  for (const c of node.children) {
    if (c.type === 'text' || c.type === 'inlineCode') s += c.value;
    else if (c.children) s += headingText(c);
  }
  return s;
}

/** Parse + strip trailing `{...}` directives from a heading's last text node. */
function parseDirectives(node) {
  const dir = { unnumbered: false, appendix: false, id: null };
  // Find trailing run of brace groups across the heading's serialized text.
  const full = headingText(node);
  const m = full.match(/((?:\s*\{[^}]*\})+)\s*$/);
  if (m) {
    for (const tok of m[1].match(/\{[^}]*\}/g)) {
      const inner = tok.slice(1, -1).trim();
      if (inner === '-' || inner === '.unnumbered') dir.unnumbered = true;
      else if (inner === '.appendix') dir.appendix = true;
      else if (inner.startsWith('#')) dir.id = inner.slice(1);
    }
    // Strip the matched directive text from the last text-bearing child.
    for (let i = node.children.length - 1; i >= 0; i--) {
      const c = node.children[i];
      if (c.type === 'text') { c.value = c.value.replace(/((?:\s*\{[^}]*\})+)\s*$/, ''); break; }
    }
  }
  return dir;
}

export default function remarkSectionNumbers() {
  return (tree, file) => {
    const fm = file?.data?.astro?.frontmatter;
    if (!fm || fm.autonumber !== true) return;

    // Collect h2/h3 headings in document order.
    const headings = [];
    for (const node of tree.children) {
      if (node.type === 'heading' && (node.depth === 2 || node.depth === 3)) {
        const dir = parseDirectives(node);
        headings.push({ node, depth: node.depth, ...dir });
      }
    }

    const labels = numberHeadings(headings);

    // id -> display string for cross-references, e.g. "§4.6" or "Appendix A".
    const refDisplay = {};

    headings.forEach(({ node, id }, i) => {
      const cleanText = headingText(node).trim();
      const finalId = id || slug(cleanText);
      node.data = node.data || {};
      node.data.id = finalId;
      node.data.hProperties = { ...(node.data.hProperties || {}), id: finalId };

      const label = labels[i];
      if (label) {
        const bare = label.replace(/\.$/, '');
        refDisplay[finalId] = bare.startsWith('Appendix') ? bare : `§${bare}`;
        // Prepend "8.3 " (note trailing space) to the heading text.
        node.children.unshift({ type: 'text', value: `${label} ` });
      }
    });

    // Resolve cross-reference tokens `§(id)` in body text into clickable links
    // showing the live number ("§4.6") or appendix letter ("Appendix A").
    resolveRefs(tree, refDisplay);
  };
}

const REF_TOKEN = /§\(([a-z0-9-]+)\)/g;

/** Replace `§(id)` tokens inside text nodes with link nodes. */
function resolveRefs(node, refDisplay) {
  if (!node.children) return;
  const out = [];
  for (const child of node.children) {
    if (child.type === 'html' && child.value.includes('§(')) {
      // Raw HTML block (e.g. a <figcaption> or <td>): rewrite tokens to <a> in place.
      child.value = child.value.replace(REF_TOKEN, (m, id) =>
        refDisplay[id] ? `<a href="#${id}">${refDisplay[id]}</a>` : m);
      out.push(child);
    } else if (child.type === 'text' && REF_TOKEN.test(child.value)) {
      REF_TOKEN.lastIndex = 0;
      let last = 0, m;
      while ((m = REF_TOKEN.exec(child.value))) {
        const disp = refDisplay[m[1]];
        if (m.index > last) out.push({ type: 'text', value: child.value.slice(last, m.index) });
        if (disp) out.push({ type: 'link', url: `#${m[1]}`, children: [{ type: 'text', value: disp }] });
        else out.push({ type: 'text', value: m[0] }); // unknown id: leave token visible
        last = m.index + m[0].length;
      }
      if (last < child.value.length) out.push({ type: 'text', value: child.value.slice(last) });
    } else {
      resolveRefs(child, refDisplay);
      out.push(child);
    }
  }
  node.children = out;
}
