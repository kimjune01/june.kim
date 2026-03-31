import { useEffect, useRef, useState } from 'react';

// Shared Pyodide instance across all Repl components on the page
let pyodidePromise: Promise<any> | null = null;

function getPyodide(): Promise<any> {
  if (!pyodidePromise) {
    pyodidePromise = new Promise((resolve, reject) => {
      if ((window as any).loadPyodide) {
        (window as any).loadPyodide({ indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.27.5/full/' })
          .then(resolve).catch(reject);
        return;
      }
      const script = document.createElement('script');
      script.src = 'https://cdn.jsdelivr.net/pyodide/v0.27.5/full/pyodide.js';
      script.onload = () => {
        (window as any).loadPyodide({ indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.27.5/full/' })
          .then(resolve).catch(reject);
      };
      script.onerror = reject;
      document.head.appendChild(script);
    });
  }
  return pyodidePromise;
}

function esc(s: string): string {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function highlightPython(code: string): string {
  const tokens: string[] = [];
  let i = 0;
  const kwSet = new Set([
    'def','class','return','yield','from','import','as','if','elif','else',
    'for','while','break','continue','pass','try','except','finally','raise','with',
    'and','or','not','in','is','lambda','None','True','False','global','nonlocal',
    'del','assert','async','await',
  ]);
  const builtinSet = new Set([
    'print','range','len','int','float','str','list','dict','set','tuple',
    'sum','min','max','abs','round','sorted','enumerate','zip','map','filter',
    'isinstance','type','hasattr','getattr','super','property',
    'open','format','input','iter','next','reversed','any','all',
    'ValueError','TypeError','NameError','Exception','KeyError','IndexError',
    'math','functools','itertools','operator','collections','fractions',
  ]);

  while (i < code.length) {
    // Comment
    if (code[i] === '#') {
      const end = code.indexOf('\n', i);
      const comment = end === -1 ? code.slice(i) : code.slice(i, end);
      tokens.push('<span class="hl-comment">' + esc(comment) + '</span>');
      i += comment.length;
      continue;
    }
    // Strings: single/double, triple-quoted
    if ((code[i] === '"' || code[i] === "'") ||
        (code[i] === 'f' && (code[i+1] === '"' || code[i+1] === "'"))) {
      let fPrefix = '';
      let si = i;
      if (code[i] === 'f') { fPrefix = 'f'; si = i + 1; }
      const q = code[si];
      const triple = code.slice(si, si+3) === q+q+q;
      const delim = triple ? q+q+q : q;
      let j = si + delim.length;
      while (j < code.length) {
        if (code[j] === '\\') { j += 2; continue; }
        if (code.slice(j, j + delim.length) === delim) { j += delim.length; break; }
        j++;
      }
      tokens.push('<span class="hl-string">' + esc(code.slice(i, j)) + '</span>');
      i = j;
      continue;
    }
    // Decorator
    if (code[i] === '@' && (i === 0 || code[i-1] === '\n')) {
      let j = i;
      while (j < code.length && code[j] !== '\n') j++;
      tokens.push('<span class="hl-decorator">' + esc(code.slice(i, j)) + '</span>');
      i = j;
      continue;
    }
    // Number
    if (/\d/.test(code[i]) && (i === 0 || /[\s([\{,=:+\-*/<>!]/.test(code[i-1]))) {
      let j = i;
      while (j < code.length && /[\d._eExXoObBa-fA-Fj]/.test(code[j])) j++;
      tokens.push('<span class="hl-number">' + esc(code.slice(i, j)) + '</span>');
      i = j;
      continue;
    }
    // Word (identifier, keyword, builtin)
    if (/[a-zA-Z_]/.test(code[i])) {
      let j = i;
      while (j < code.length && /[a-zA-Z0-9_]/.test(code[j])) j++;
      const word = code.slice(i, j);
      if (kwSet.has(word)) {
        tokens.push('<span class="hl-keyword">' + esc(word) + '</span>');
      } else if (builtinSet.has(word)) {
        tokens.push('<span class="hl-builtin">' + esc(word) + '</span>');
      } else {
        tokens.push(esc(word));
      }
      i = j;
      continue;
    }
    // Everything else
    tokens.push(esc(code[i]));
    i++;
  }
  return tokens.join('');
}

export default function Repl({ initialCode }: { initialCode?: string }) {
  const [code, setCode] = useState(initialCode || '');
  const [output, setOutput] = useState('');
  const [running, setRunning] = useState(false);
  const [ready, setReady] = useState(false);
  const pyRef = useRef<any>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const preRef = useRef<HTMLPreElement>(null);

  useEffect(() => {
    getPyodide().then(py => {
      pyRef.current = py;
      setReady(true);
    });
  }, []);

  function syncScroll() {
    if (textareaRef.current && preRef.current) {
      preRef.current.scrollTop = textareaRef.current.scrollTop;
      preRef.current.scrollLeft = textareaRef.current.scrollLeft;
    }
  }

  async function run() {
    const pyodide = pyRef.current;
    if (!pyodide) return;
    setRunning(true);
    setOutput('');
    try {
      pyodide.runPython(`
import sys, io, random, time
sys.stdout = io.StringIO()
sys.stderr = io.StringIO()
random.seed(int(time.time() * 1000) % 2**32)
`);
      await pyodide.runPythonAsync(code);
      const stdout = pyodide.runPython('sys.stdout.getvalue()');
      const stderr = pyodide.runPython('sys.stderr.getvalue()');
      setOutput((stdout || '') + (stderr ? `\n⚠ ${stderr}` : '') || '(no output)');
    } catch (e: any) {
      setOutput(`Error: ${e.message || e}`);
    }
    setRunning(false);
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      run();
    }
    if (e.key === 'Tab') {
      e.preventDefault();
      const ta = textareaRef.current;
      if (ta) {
        const start = ta.selectionStart;
        const end = ta.selectionEnd;
        const newCode = code.substring(0, start) + '    ' + code.substring(end);
        setCode(newCode);
        setTimeout(() => {
          ta.selectionStart = ta.selectionEnd = start + 4;
        }, 0);
      }
    }
  }

  const rows = code.split('\n').length;

  return (
    <div className="border border-zinc-700 rounded-lg overflow-hidden my-4">
      <div className="flex items-center justify-between px-3 py-1">
        <span className="text-xs text-gray-500 font-mono">Python</span>
        <button
          onClick={run}
          disabled={!ready || running}
          className="px-2 py-0.5 border border-green-700 text-green-400 bg-transparent hover:bg-green-900/30 disabled:border-zinc-600 disabled:text-zinc-500 rounded text-xs font-mono transition-colors"
        >
          {!ready ? '○' : running ? '···' : '▶'}
        </button>
      </div>
      <div className="relative">
        <pre
          ref={preRef}
          className="absolute inset-0 font-mono text-sm p-4 overflow-hidden whitespace-pre-wrap break-words"
          style={{ tabSize: 4, background: 'var(--repl-bg, #18181b)', pointerEvents: 'none', lineHeight: '1.5', margin: 0, border: 'none' }}
          aria-hidden="true"
          dangerouslySetInnerHTML={{ __html: highlightPython(code) + '\n' }}
        />
        <textarea
          ref={textareaRef}
          value={code}
          onChange={e => setCode(e.target.value)}
          onKeyDown={handleKeyDown}
          onScroll={syncScroll}
          spellCheck={false}
          className="repl-input relative w-full font-mono text-sm p-4 resize-none outline-none border-none overflow-hidden"
          style={{ tabSize: 4, color: 'transparent', caretColor: 'var(--repl-caret, #86efac)', background: 'transparent', WebkitTextFillColor: 'transparent', lineHeight: '1.5', margin: 0 }}
          rows={rows}
        />
      </div>
      {output && (
        <pre className="p-4 border-t border-zinc-700 text-gray-300 text-sm font-mono whitespace-pre-wrap overflow-auto" style={{ maxHeight: '300px' }}>
          {output}
        </pre>
      )}
    </div>
  );
}
