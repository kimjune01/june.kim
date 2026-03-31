import { useEffect, useRef, useState } from 'react';

let biwaReady: Promise<any> | null = null;

function getBiwa(): Promise<any> {
  if (!biwaReady) {
    biwaReady = new Promise((resolve, reject) => {
      if ((window as any).BiwaScheme) {
        resolve((window as any).BiwaScheme);
        return;
      }
      const script = document.createElement('script');
      script.src = 'https://cdn.jsdelivr.net/npm/biwascheme@0.8.3/release/biwascheme-min.js';
      script.onload = () => resolve((window as any).BiwaScheme);
      script.onerror = reject;
      document.head.appendChild(script);
    });
  }
  return biwaReady;
}

function esc(s: string): string {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function highlightScheme(code: string): string {
  const tokens: string[] = [];
  let i = 0;
  const kwSet = new Set(['define','define-syntax','syntax-rules','lambda','let','let*','letrec',
    'if','cond','else','and','or','not','begin','set!','quote',
    'cons-stream','delay','force','map','filter','for-each','apply']);

  while (i < code.length) {
    // Comment
    if (code[i] === ';') {
      const end = code.indexOf('\n', i);
      const comment = end === -1 ? code.slice(i) : code.slice(i, end);
      tokens.push('<span class="hl-comment">' + esc(comment) + '</span>');
      i += comment.length;
      continue;
    }
    // String
    if (code[i] === '"') {
      let j = i + 1;
      while (j < code.length && code[j] !== '"') { if (code[j] === '\\') j++; j++; }
      if (j < code.length) j++;
      tokens.push('<span class="hl-string">' + esc(code.slice(i, j)) + '</span>');
      i = j;
      continue;
    }
    // Boolean
    if (code[i] === '#' && (code[i+1] === 't' || code[i+1] === 'f') &&
        (i+2 >= code.length || /[\s)]/.test(code[i+2]))) {
      tokens.push('<span class="hl-bool">' + code.slice(i, i+2) + '</span>');
      i += 2;
      continue;
    }
    // Word
    if (/[^\s()'"]/.test(code[i])) {
      let j = i;
      while (j < code.length && /[^\s()'"]/.test(code[j])) j++;
      const word = code.slice(i, j);
      const prevChar = i > 0 ? code[i-1] : '';
      if (prevChar === '(' && kwSet.has(word)) {
        tokens.push('<span class="hl-keyword">' + esc(word) + '</span>');
      } else if (/^-?\d+\.?\d*(\/\d+)?$/.test(word)) {
        tokens.push('<span class="hl-number">' + esc(word) + '</span>');
      } else {
        tokens.push(esc(word));
      }
      i = j;
      continue;
    }
    tokens.push(esc(code[i]));
    i++;
  }
  return tokens.join('');
}

export default function SchemeRepl({ initialCode }: { initialCode?: string }) {
  const [code, setCode] = useState(initialCode || '');
  const [output, setOutput] = useState('');
  const [running, setRunning] = useState(false);
  const [ready, setReady] = useState(false);
  const biwaRef = useRef<any>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const preRef = useRef<HTMLPreElement>(null);

  useEffect(() => {
    getBiwa().then(bw => {
      biwaRef.current = bw;
      setReady(true);
    });
  }, []);

  // Sync scroll between textarea and highlight overlay
  function syncScroll() {
    if (textareaRef.current && preRef.current) {
      preRef.current.scrollTop = textareaRef.current.scrollTop;
      preRef.current.scrollLeft = textareaRef.current.scrollLeft;
    }
  }

  async function run() {
    const BiwaScheme = biwaRef.current;
    if (!BiwaScheme) return;
    setRunning(true);
    setOutput('');
    try {
      let out = '';
      const interp = new BiwaScheme.Interpreter((msg: string) => {
        if (msg !== undefined && msg !== null) out += String(msg);
      });
      if (BiwaScheme.Port && BiwaScheme.Port.current_output) {
        BiwaScheme.Port.current_output.put_string = (s: string) => { out += s; };
      }
      const result = await new Promise<any>((resolve, reject) => {
        try {
          interp.evaluate(code, (res: any) => { resolve(res); });
        } catch(e) { reject(e); }
      });
      let resultStr = '';
      try {
        if (result !== undefined && result !== null && result !== BiwaScheme.undef) {
          resultStr = typeof BiwaScheme.to_write === 'function'
            ? BiwaScheme.to_write(result) : String(result);
        }
      } catch(_) {}
      const finalOutput = out + (resultStr ? (out ? '\n' : '') + '=> ' + resultStr : '');
      setOutput(finalOutput || '(no output)');
    } catch (e: any) {
      setOutput(`Error: ${e.message || String(e)}`);
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
        const newCode = code.substring(0, start) + '  ' + code.substring(end);
        setCode(newCode);
        setTimeout(() => { ta.selectionStart = ta.selectionEnd = start + 2; }, 0);
      }
    }
  }

  const rows = code.split('\n').length;

  return (
    <div className="border border-zinc-700 rounded-lg overflow-hidden my-4">
      <div className="flex items-center justify-between px-3 py-1">
        <span className="text-xs text-gray-500 font-mono">Scheme</span>
        <button
          onClick={run}
          disabled={!ready || running}
          className="px-2 py-0.5 border border-blue-700 text-blue-400 bg-transparent hover:bg-blue-900/30 disabled:border-zinc-600 disabled:text-zinc-500 rounded text-xs font-mono transition-colors"
        >
          {!ready ? '○' : running ? '···' : '▶'}
        </button>
      </div>
      <div className="relative">
        <pre
          ref={preRef}
          className="absolute inset-0 font-mono text-sm p-4 overflow-hidden whitespace-pre-wrap break-words"
          style={{ tabSize: 2, background: 'var(--repl-bg, #18181b)', pointerEvents: 'none', lineHeight: '1.5', margin: 0, border: 'none' }}
          aria-hidden="true"
          dangerouslySetInnerHTML={{ __html: highlightScheme(code) + '\n' }}
        />
        <textarea
          ref={textareaRef}
          value={code}
          onChange={e => setCode(e.target.value)}
          onKeyDown={handleKeyDown}
          onScroll={syncScroll}
          spellCheck={false}
          className="repl-input relative w-full font-mono text-sm p-4 resize-none outline-none border-none overflow-hidden"
          style={{ tabSize: 2, color: 'transparent', caretColor: 'var(--repl-caret, #93c5fd)', background: 'transparent', WebkitTextFillColor: 'transparent', lineHeight: '1.5', margin: 0 }}
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
