// Turn a paragraph whose only content is an image into a <figure>.
// Preserve alt text for accessibility without displaying it as a caption.
// Dependency-free hast walk.

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
            child.tagName = 'figure';
            child.children = [img];
          }
        }
        walk(child);
      }
    };
    walk(tree);
  };
}
