// Highlighter — testable core logic
// DOM manipulation + storage for text highlighting in prose elements.
// The inline script in Base.astro wires this to mouse/keyboard events.

var ALLOWED = 'p, h1, h2, h3, h4';

export function createHighlighter(doc, storage, pathname) {
  var KEY = 'highlights';
  var page = pathname;
  var lastHighlightText = null;
  var win = doc.defaultView || globalThis;

  // ── Storage helpers ──
  function loadAll() {
    try { return JSON.parse(storage.getItem(KEY) || '{}'); } catch(e) { return {}; }
  }
  function saveAll(store) { storage.setItem(KEY, JSON.stringify(store)); }
  function loadPage() { return (loadAll()[page] || []).slice(); }
  function savePage(entries) {
    var store = loadAll();
    if (entries.length) store[page] = entries;
    else delete store[page];
    saveAll(store);
  }

  // ── Approximate index: fraction of total text length ──
  function approxIndex(node) {
    var all = doc.querySelectorAll(ALLOWED);
    var cumulative = 0, target = 0, total = 0;
    for (var i = 0; i < all.length; i++) total += all[i].textContent.length;
    if (!total) return 0;
    for (var i = 0; i < all.length; i++) {
      if (all[i] === node || all[i].contains(node)) { target = cumulative; break; }
      cumulative += all[i].textContent.length;
    }
    return target / total;
  }

  // ── Find the allowed ancestor element ──
  function allowedAncestor(node) {
    while (node && node !== doc.body) {
      if (node.nodeType === 1 && node.matches(ALLOWED)) return node;
      node = node.parentNode;
    }
    return null;
  }

  // ── Apply a single highlight to the DOM ──
  function applyHighlight(el, text) {
    var walker = doc.createTreeWalker(el, 4 /* NodeFilter.SHOW_TEXT */, null, false);
    var nodes = [], n;
    while (n = walker.nextNode()) nodes.push(n);

    var concat = '', map = [];
    for (var i = 0; i < nodes.length; i++) {
      for (var j = 0; j < nodes[i].nodeValue.length; j++) {
        map.push({ node: nodes[i], offset: j });
      }
      concat += nodes[i].nodeValue;
    }

    var idx = concat.indexOf(text);
    if (idx === -1) return false;

    var startInfo = map[idx];
    var endInfo = map[idx + text.length - 1];

    var range = doc.createRange();
    range.setStart(startInfo.node, startInfo.offset);
    range.setEnd(endInfo.node, endInfo.offset + 1);

    var mark = doc.createElement('mark');
    mark.className = 'user-highlight';
    range.surroundContents(mark);
    return true;
  }

  // ── Get all highlight marks inside an element ──
  function getMarksIn(el) {
    return el ? Array.prototype.slice.call(el.querySelectorAll('mark.user-highlight')) : [];
  }

  // ── Check if a range intersects a mark ──
  function rangeIntersectsMark(range, mark) {
    var markRange = doc.createRange();
    markRange.selectNodeContents(mark);
    return range.compareBoundaryPoints(win.Range.END_TO_START, markRange) <= 0 &&
           range.compareBoundaryPoints(win.Range.START_TO_END, markRange) >= 0;
  }

  // ── Unwrap a mark element, merging text nodes ──
  function unwrapMark(mark) {
    var parent = mark.parentNode;
    while (mark.firstChild) parent.insertBefore(mark.firstChild, mark);
    parent.removeChild(mark);
    parent.normalize();
  }

  // ── Rebuild storage entries from current DOM marks ──
  function syncStorage() {
    var entries = [];
    var marks = doc.querySelectorAll('mark.user-highlight');
    for (var i = 0; i < marks.length; i++) {
      var el = allowedAncestor(marks[i]);
      if (!el) continue;
      entries.push({
        text: marks[i].textContent,
        approxIdx: approxIndex(el)
      });
    }
    savePage(entries);
  }

  // ── Merge adjacent marks inside an element ──
  function mergeAdjacentMarks(el) {
    var marks = getMarksIn(el);
    for (var i = 0; i < marks.length - 1; i++) {
      var a = marks[i], b = marks[i + 1];
      var between = a.nextSibling;
      if (between === b || (between && between.nodeType === 3 && between.nodeValue.trim() === '' && between.nextSibling === b)) {
        if (between !== b) a.appendChild(between);
        while (b.firstChild) a.appendChild(b.firstChild);
        b.parentNode.removeChild(b);
        marks = getMarksIn(el);
        i--;
      }
    }
  }

  // ── Restore highlights on page load ──
  function restoreHighlights() {
    var entries = loadPage();
    var surviving = [];
    for (var i = 0; i < entries.length; i++) {
      var entry = entries[i];
      var all = doc.querySelectorAll(ALLOWED);
      var candidates = [];
      for (var j = 0; j < all.length; j++) {
        if (all[j].textContent.indexOf(entry.text) !== -1) {
          candidates.push(all[j]);
        }
      }
      if (!candidates.length) continue;

      var best = candidates[0], bestDist = Math.abs(approxIndex(best) - entry.approxIdx);
      for (var k = 1; k < candidates.length; k++) {
        var d = Math.abs(approxIndex(candidates[k]) - entry.approxIdx);
        if (d < bestDist) { best = candidates[k]; bestDist = d; }
      }

      if (applyHighlight(best, entry.text)) {
        surviving.push(entry);
      }
    }
    savePage(surviving);
  }

  // ── Undo ──
  function undoLast() {
    if (!lastHighlightText) return;
    var marks = doc.querySelectorAll('mark.user-highlight');
    for (var i = 0; i < marks.length; i++) {
      if (marks[i].textContent === lastHighlightText) {
        unwrapMark(marks[i]);
        syncStorage();
        break;
      }
    }
    lastHighlightText = null;
  }

  // ── Core highlight action ──
  // Accepts a Selection object (or duck-type with isCollapsed, getRangeAt, toString, containsNode, removeAllRanges)
  function doHighlight(sel) {
    if (!sel || sel.isCollapsed || !sel.rangeCount) {
      undoLast();
      return;
    }

    var range = sel.getRangeAt(0);
    var selText = sel.toString();
    if (!selText.trim()) return;

    var el = allowedAncestor(range.startContainer);
    if (!el) return;

    var startMark = range.startContainer.nodeType === 3 ? range.startContainer.parentNode : range.startContainer;
    var endMark = range.endContainer.nodeType === 3 ? range.endContainer.parentNode : range.endContainer;

    if (startMark.closest && startMark.closest('mark.user-highlight')) startMark = startMark.closest('mark.user-highlight');
    else startMark = null;
    if (endMark.closest && endMark.closest('mark.user-highlight')) endMark = endMark.closest('mark.user-highlight');
    else endMark = null;

    var extendsBeyond = false;
    if (startMark || endMark) {
      var touchedMarks = getMarksIn(el).filter(function(m) { return rangeIntersectsMark(range, m); });
      if (touchedMarks.length > 0) {
        var unionRange = doc.createRange();
        unionRange.setStartBefore(touchedMarks[0]);
        unionRange.setEndAfter(touchedMarks[touchedMarks.length - 1]);
        if (range.compareBoundaryPoints(win.Range.START_TO_START, unionRange) < 0 ||
            range.compareBoundaryPoints(win.Range.END_TO_END, unionRange) > 0) {
          extendsBeyond = true;
        }
      }
    }

    var touchedMarks = getMarksIn(el).filter(function(m) { return rangeIntersectsMark(range, m); });

    var selInside = touchedMarks.length === 1 &&
      touchedMarks[0].textContent.indexOf(selText.trim()) !== -1;

    if (touchedMarks.length === 1 && (!extendsBeyond || selInside)) {
      lastHighlightText = null;
      unwrapMark(touchedMarks[0]);
      syncStorage();
      sel.removeAllRanges();
      return;
    }

    var mergeText = null;
    if (touchedMarks.length > 0) {
      var mergeRange = doc.createRange();
      var firstMark = touchedMarks[0];
      var lastMark = touchedMarks[touchedMarks.length - 1];
      var tempRange = doc.createRange();
      tempRange.setStartBefore(firstMark);
      tempRange.setEndAfter(firstMark);
      if (range.compareBoundaryPoints(win.Range.START_TO_START, tempRange) < 0) {
        mergeRange.setStart(range.startContainer, range.startOffset);
      } else {
        mergeRange.setStartBefore(firstMark);
      }
      tempRange.setStartBefore(lastMark);
      tempRange.setEndAfter(lastMark);
      if (range.compareBoundaryPoints(win.Range.END_TO_END, tempRange) > 0) {
        mergeRange.setEnd(range.endContainer, range.endOffset);
      } else {
        mergeRange.setEndAfter(lastMark);
      }
      mergeText = mergeRange.toString();
      for (var i = 0; i < touchedMarks.length; i++) unwrapMark(touchedMarks[i]);
    }

    try {
      var newRange = doc.createRange();
      var elText = el.textContent;
      var selStr = mergeText || selText;
      var startIdx = elText.indexOf(selStr);
      if (startIdx === -1) { sel.removeAllRanges(); return; }

      var walker = doc.createTreeWalker(el, 4 /* NodeFilter.SHOW_TEXT */, null, false);
      var charCount = 0, node, startNode, startOffset, endNode, endOffset;
      while (node = walker.nextNode()) {
        var len = node.nodeValue.length;
        if (!startNode && charCount + len > startIdx) {
          startNode = node;
          startOffset = startIdx - charCount;
        }
        if (charCount + len >= startIdx + selStr.length) {
          endNode = node;
          endOffset = startIdx + selStr.length - charCount;
          break;
        }
        charCount += len;
      }

      if (!startNode || !endNode) { sel.removeAllRanges(); return; }

      newRange.setStart(startNode, startOffset);
      newRange.setEnd(endNode, endOffset);

      var mark = doc.createElement('mark');
      mark.className = 'user-highlight';
      newRange.surroundContents(mark);
      mergeAdjacentMarks(el);
      lastHighlightText = mark.textContent;
    } catch(e) {
      // surroundContents can fail — bail
    }

    syncStorage();
    sel.removeAllRanges();
  }

  return {
    restoreHighlights: restoreHighlights,
    doHighlight: doHighlight,
    undoLast: undoLast,
    // Exposed for testing
    _allowedAncestor: allowedAncestor,
    _approxIndex: approxIndex,
    _applyHighlight: applyHighlight,
    _getMarksIn: getMarksIn,
    _unwrapMark: unwrapMark,
    _syncStorage: syncStorage,
    _loadPage: loadPage,
    get lastHighlightText() { return lastHighlightText; }
  };
}
