// Turn a paragraph whose only content is an image into a <figure> with a
// <figcaption> built from the image's alt text. Lets clean-markdown figures
// (`![caption](/assets/x.svg)`) render with a visible caption on the blog,
// matching what the arXiv build does in LaTeX. Dependency-free hast walk.

function isImg(n) {
  return n && n.type === 'element' && n.tagName === 'img';
}
function nonBlank(children) {
  return (children || []).filter(
    (c) => !(c.type === 'text' && !String(c.value).trim())
  );
}

export default function rehypeFigures() {
  return (tree) => {
    const walk = (node) => {
      if (!node || !node.children) return;
      for (const child of node.children) {
        if (child.type === 'element' && child.tagName === 'p') {
          const kids = nonBlank(child.children);
          if (kids.length === 1 && isImg(kids[0])) {
            const img = kids[0];
            const alt = (img.properties && img.properties.alt) || '';
            const caption = String(alt).replace(/[`*]/g, '').trim(); // plain text
            child.tagName = 'figure';
            child.children = [img];
            if (caption) {
              child.children.push({
                type: 'element',
                tagName: 'figcaption',
                properties: {},
                children: [{ type: 'text', value: caption }],
              });
            }
          }
        }
        walk(child);
      }
    };
    walk(tree);
  };
}
