import { describe, it, expect, beforeEach } from 'vitest';
import { JSDOM } from 'jsdom';
import { createHighlighter } from './highlighter.js';

// ── Helpers ──

function makeDOM(html) {
  var dom = new JSDOM(`<body>${html}</body>`, { url: 'http://localhost/reading/test/' });
  return dom.window.document;
}

function fakeStorage() {
  var store = {};
  return {
    getItem: (k) => store[k] || null,
    setItem: (k, v) => { store[k] = v; },
    removeItem: (k) => { delete store[k]; },
    _store: store
  };
}

// Select text within a single text node of an element
function selectText(doc, el, startOffset, endOffset) {
  var textNode = null;
  var walker = doc.createTreeWalker(el, 4 /* NodeFilter.SHOW_TEXT */, null, false);
  var n, cumulative = 0;
  while (n = walker.nextNode()) {
    if (cumulative + n.nodeValue.length >= startOffset) {
      textNode = n;
      break;
    }
    cumulative += n.nodeValue.length;
  }
  var range = doc.createRange();
  range.setStart(textNode, startOffset - cumulative);
  // Find end node
  var endNode = textNode, endCumulative = cumulative;
  if (cumulative + textNode.nodeValue.length < endOffset) {
    walker = doc.createTreeWalker(el, 4, null, false);
    endCumulative = 0;
    while (n = walker.nextNode()) {
      if (endCumulative + n.nodeValue.length >= endOffset) {
        endNode = n;
        break;
      }
      endCumulative += n.nodeValue.length;
    }
  }
  range.setEnd(endNode, endOffset - endCumulative);

  // Build a selection-like object
  var sel = {
    isCollapsed: false,
    rangeCount: 1,
    getRangeAt: () => range,
    toString: () => range.toString(),
    containsNode: (node, allowPartial) => {
      if (!allowPartial) return range.isPointInRange(node, 0);
      var nodeRange = doc.createRange();
      nodeRange.selectNode(node);
      var R = doc.defaultView.Range;
      return range.compareBoundaryPoints(R.END_TO_START, nodeRange) <= 0 &&
             range.compareBoundaryPoints(R.START_TO_END, nodeRange) >= 0;
    },
    removeAllRanges: () => {}
  };
  return sel;
}

// Select across a mark and unhighlighted text
function selectAcross(doc, startNode, startOffset, endNode, endOffset) {
  var range = doc.createRange();
  range.setStart(startNode, startOffset);
  range.setEnd(endNode, endOffset);
  return {
    isCollapsed: false,
    rangeCount: 1,
    getRangeAt: () => range,
    toString: () => range.toString(),
    containsNode: (node, allowPartial) => {
      if (!allowPartial) return range.isPointInRange(node, 0);
      var nodeRange = doc.createRange();
      nodeRange.selectNode(node);
      var R = doc.defaultView.Range;
      return range.compareBoundaryPoints(R.END_TO_START, nodeRange) <= 0 &&
             range.compareBoundaryPoints(R.START_TO_END, nodeRange) >= 0;
    },
    removeAllRanges: () => {}
  };
}

function getMarks(doc) {
  return Array.from(doc.querySelectorAll('mark.user-highlight'));
}

// ── Tests ──

describe('Highlighter', () => {
  var doc, storage, hl;

  beforeEach(() => {
    doc = makeDOM('<p>The quick brown fox jumps over the lazy dog.</p><h2>Section title</h2><p>Another paragraph with some text.</p>');
    storage = fakeStorage();
    hl = createHighlighter(doc, storage, '/reading/test/');
  });

  describe('create highlight', () => {
    it('wraps selected text in a mark element', () => {
      var p = doc.querySelector('p');
      var sel = selectText(doc, p, 4, 9); // "quick"
      hl.doHighlight(sel);
      var marks = getMarks(doc);
      expect(marks.length).toBe(1);
      expect(marks[0].textContent).toBe('quick');
    });

    it('persists highlight to storage', () => {
      var p = doc.querySelector('p');
      var sel = selectText(doc, p, 4, 9);
      hl.doHighlight(sel);
      var stored = JSON.parse(storage.getItem('highlights'));
      expect(stored['/reading/test/']).toHaveLength(1);
      expect(stored['/reading/test/'][0].text).toBe('quick');
      expect(typeof stored['/reading/test/'][0].approxIdx).toBe('number');
    });

    it('works on heading elements', () => {
      var h2 = doc.querySelector('h2');
      var sel = selectText(doc, h2, 0, 7); // "Section"
      hl.doHighlight(sel);
      var marks = getMarks(doc);
      expect(marks.length).toBe(1);
      expect(marks[0].textContent).toBe('Section');
    });

    it('ignores selection outside allowed elements', () => {
      // Add a div (not allowed)
      var div = doc.createElement('div');
      div.textContent = 'Not allowed';
      doc.body.appendChild(div);
      var sel = selectText(doc, div, 0, 3);
      hl.doHighlight(sel);
      expect(getMarks(doc).length).toBe(0);
    });
  });

  describe('remove highlight', () => {
    it('removes highlight when selecting fully inside it', () => {
      var p = doc.querySelector('p');
      // First, create a highlight
      hl.doHighlight(selectText(doc, p, 4, 9)); // "quick"
      expect(getMarks(doc).length).toBe(1);

      // Now select inside the mark
      var mark = doc.querySelector('mark.user-highlight');
      var sel = selectText(doc, mark, 0, 5); // "quick" inside the mark
      // Need to make the selection reference the mark's text node
      var markText = mark.firstChild;
      var range = doc.createRange();
      range.setStart(markText, 0);
      range.setEnd(markText, 5);
      sel = {
        isCollapsed: false,
        rangeCount: 1,
        getRangeAt: () => range,
        toString: () => 'quick',
        containsNode: (node, allowPartial) => {
          var nodeRange = doc.createRange();
          nodeRange.selectNode(node);
          var R = doc.defaultView.Range;
          return range.compareBoundaryPoints(R.END_TO_START, nodeRange) <= 0 &&
                 range.compareBoundaryPoints(R.START_TO_END, nodeRange) >= 0;
        },
        removeAllRanges: () => {}
      };
      hl.doHighlight(sel);
      expect(getMarks(doc).length).toBe(0);
    });
  });

  describe('expand highlight', () => {
    it('expands when selection extends beyond existing highlight', () => {
      var p = doc.querySelector('p');
      // Highlight "quick"
      hl.doHighlight(selectText(doc, p, 4, 9));
      expect(getMarks(doc)[0].textContent).toBe('quick');

      // Select "quick brown" — overlaps and extends
      var mark = doc.querySelector('mark.user-highlight');
      var afterMark = mark.nextSibling; // text node: " brown fox..."
      var sel = selectAcross(doc, mark.firstChild, 0, afterMark, 6); // "quick" + " brown"
      hl.doHighlight(sel);

      var marks = getMarks(doc);
      expect(marks.length).toBe(1);
      expect(marks[0].textContent).toBe('quick brown');
    });
  });

  describe('merge highlights', () => {
    it('merges two highlights when selecting across both', () => {
      var p = doc.querySelector('p');
      // Highlight "quick" and "fox"
      hl.doHighlight(selectText(doc, p, 4, 9));   // "quick"
      hl.doHighlight(selectText(doc, p, 16, 19));  // "fox"

      expect(getMarks(doc).length).toBe(2);

      // Select from "quick" through "fox" — should merge
      var marks = getMarks(doc);
      var firstMarkText = marks[0].firstChild;
      var lastMarkText = marks[1].firstChild;
      var sel = selectAcross(doc, firstMarkText, 0, lastMarkText, 3);
      hl.doHighlight(sel);

      var newMarks = getMarks(doc);
      expect(newMarks.length).toBe(1);
      expect(newMarks[0].textContent).toBe('quick brown fox');
    });
  });

  describe('undo', () => {
    it('undoes last highlight when called with no selection', () => {
      var p = doc.querySelector('p');
      hl.doHighlight(selectText(doc, p, 4, 9)); // "quick"
      expect(getMarks(doc).length).toBe(1);

      // Call with collapsed/no selection triggers undo
      hl.doHighlight({ isCollapsed: true, rangeCount: 0 });
      expect(getMarks(doc).length).toBe(0);
    });

    it('only undoes once (not repeatable)', () => {
      var p = doc.querySelector('p');
      hl.doHighlight(selectText(doc, p, 4, 9));   // "quick"
      hl.doHighlight(selectText(doc, p, 16, 19));  // "fox"
      expect(getMarks(doc).length).toBe(2);

      // Undo removes "fox" (last one)
      hl.doHighlight({ isCollapsed: true, rangeCount: 0 });
      expect(getMarks(doc).length).toBe(1);
      expect(getMarks(doc)[0].textContent).toBe('quick');

      // Second undo does nothing
      hl.doHighlight({ isCollapsed: true, rangeCount: 0 });
      expect(getMarks(doc).length).toBe(1);
    });

    it('does not undo a remove operation', () => {
      var p = doc.querySelector('p');
      hl.doHighlight(selectText(doc, p, 4, 9)); // "quick"

      // Remove it
      var mark = doc.querySelector('mark.user-highlight');
      var markText = mark.firstChild;
      var range = doc.createRange();
      range.setStart(markText, 0);
      range.setEnd(markText, 5);
      hl.doHighlight({
        isCollapsed: false,
        rangeCount: 1,
        getRangeAt: () => range,
        toString: () => 'quick',
        containsNode: (node, allowPartial) => {
          var nodeRange = doc.createRange();
          nodeRange.selectNode(node);
          var R = doc.defaultView.Range;
          return range.compareBoundaryPoints(R.END_TO_START, nodeRange) <= 0 &&
                 range.compareBoundaryPoints(R.START_TO_END, nodeRange) >= 0;
        },
        removeAllRanges: () => {}
      });
      expect(getMarks(doc).length).toBe(0);

      // Undo should do nothing — remove is not undoable
      hl.doHighlight({ isCollapsed: true, rangeCount: 0 });
      expect(getMarks(doc).length).toBe(0);
    });
  });

  describe('restore highlights', () => {
    it('restores highlights from storage on load', () => {
      storage.setItem('highlights', JSON.stringify({
        '/reading/test/': [{ text: 'quick', approxIdx: 0 }]
      }));
      hl.restoreHighlights();
      var marks = getMarks(doc);
      expect(marks.length).toBe(1);
      expect(marks[0].textContent).toBe('quick');
    });

    it('drops stale highlights silently', () => {
      storage.setItem('highlights', JSON.stringify({
        '/reading/test/': [{ text: 'nonexistent phrase', approxIdx: 0 }]
      }));
      hl.restoreHighlights();
      expect(getMarks(doc).length).toBe(0);
      // Storage should be cleaned up
      var stored = JSON.parse(storage.getItem('highlights'));
      expect(stored['/reading/test/']).toBeUndefined();
    });

    it('uses approxIdx to disambiguate duplicate text', () => {
      doc = makeDOM('<p>hello world</p><p>hello world</p>');
      storage = fakeStorage();
      hl = createHighlighter(doc, storage, '/reading/test/');

      // Store a highlight for "hello" in the second paragraph (approxIdx ~0.5)
      storage.setItem('highlights', JSON.stringify({
        '/reading/test/': [{ text: 'hello', approxIdx: 0.5 }]
      }));
      hl.restoreHighlights();

      var paragraphs = doc.querySelectorAll('p');
      // Second paragraph should have the mark
      expect(paragraphs[1].querySelector('mark.user-highlight')).not.toBeNull();
      // First paragraph should not
      expect(paragraphs[0].querySelector('mark.user-highlight')).toBeNull();
    });
  });

  describe('single-element clamping', () => {
    it('only highlights within the starting element', () => {
      var p = doc.querySelector('p');
      // Select text that exists in the paragraph
      var sel = selectText(doc, p, 0, 3); // "The"
      hl.doHighlight(sel);
      var marks = getMarks(doc);
      expect(marks.length).toBe(1);
      // Mark should be inside the first p
      expect(marks[0].parentNode).toBe(p);
    });
  });

  describe('storage format', () => {
    it('stores text and approxIdx as float', () => {
      var p = doc.querySelectorAll('p')[1]; // second paragraph
      var sel = selectText(doc, p, 0, 7); // "Another"
      hl.doHighlight(sel);
      var stored = JSON.parse(storage.getItem('highlights'));
      var entry = stored['/reading/test/'][0];
      expect(entry.text).toBe('Another');
      expect(entry.approxIdx).toBeGreaterThan(0);
      expect(entry.approxIdx).toBeLessThan(1);
    });
  });
});
