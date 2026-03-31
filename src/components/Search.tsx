import { useCallback, useEffect, useRef, useState } from 'react';

interface Result {
  url: string;
  title: string;
  snippet: string;
  license: string;
  semantic_score: number;
}

const API = 'https://pageleft.cc/api/search';

export default function Search() {
  const [query, setQuery] = useState('');
  const [modalOpen, setModalOpen] = useState(false);
  const [animating, setAnimating] = useState(false);
  const debounceRef = useRef<ReturnType<typeof setTimeout>>();
  const cacheRef = useRef<{ query: string; results: Result[] } | null>(null);
  const fetchRef = useRef<Promise<Result[]> | null>(null);
  const [displayResults, setDisplayResults] = useState<Result[]>([]);
  const [showResults, setShowResults] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  function prefetch(q: string) {
    if (!q.trim()) { cacheRef.current = null; fetchRef.current = null; return; }
    const promise = fetch(`${API}?q=${encodeURIComponent(q)}&limit=8`)
      .then(r => r.json())
      .then(data => {
        const results = data.results || [];
        cacheRef.current = { query: q, results };
        return results;
      })
      .catch(() => [] as Result[]);
    fetchRef.current = promise;
  }

  function onInput(value: string) {
    setQuery(value);
    clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(() => prefetch(value), 200);
  }

  const openModal = useCallback(async () => {
    if (!query.trim()) return;
    if (!fetchRef.current) prefetch(query);

    setModalOpen(true);
    setAnimating(true);
    setShowResults(false);
    setDisplayResults([]);

    const animationDone = new Promise(r => setTimeout(r, 400));

    let results: Result[];
    if (cacheRef.current?.query === query) {
      results = cacheRef.current.results;
    } else {
      const res = fetchRef.current || fetch(`${API}?q=${encodeURIComponent(query)}&limit=8`)
        .then(r => r.json()).then(d => d.results || []).catch(() => []);
      results = await res;
    }

    await animationDone;
    setAnimating(false);
    setDisplayResults(results);
    setShowResults(true);
  }, [query]);

  function close() {
    setModalOpen(false);
    setAnimating(false);
    setShowResults(false);
    setDisplayResults([]);
    inputRef.current?.focus();
  }

  function onKeyDown(e: React.KeyboardEvent) {
    if (e.key === 'Enter') {
      e.preventDefault();
      clearTimeout(debounceRef.current);
      openModal();
    }
    if (e.key === 'Escape') {
      if (modalOpen) { close(); }
      else { setQuery(''); cacheRef.current = null; fetchRef.current = null; }
    }
  }

  function onBackdropClick(e: React.MouseEvent) {
    if (e.target === e.currentTarget) close();
  }

  useEffect(() => {
    if (!modalOpen) return;
    function handleKey(e: KeyboardEvent) {
      if (e.key === 'Escape') close();
    }
    window.addEventListener('keydown', handleKey);
    return () => window.removeEventListener('keydown', handleKey);
  }, [modalOpen]);

  return (
    <div className="search-widget my-6">
      <div className="relative">
        <input
          ref={inputRef}
          type="text"
          value={query}
          onChange={e => onInput(e.target.value)}
          onKeyDown={onKeyDown}
          placeholder="Search open-source textbooks..."
          className="search-input"
        />
        {query && (
          <button onClick={openModal} className="search-btn" aria-label="Search">Search</button>
        )}
      </div>

      <p className="search-powered">
        Powered by <a href="https://pageleft.cc" className="bare-link">PageLeft</a>
      </p>

      {modalOpen && (
        <div className="search-overlay" onClick={onBackdropClick}>
          <div className="search-modal">
            <div className="search-modal-header">
              <span>Results for "{query}"</span>
              <button onClick={close} aria-label="Close">×</button>
            </div>

            {!showResults ? (
              <div className="search-skeletons">
                {[0,1,2,3,4].map(i => (
                  <div key={i} className="search-skeleton" style={{ animationDelay: `${i * 0.1}s` }}>
                    <div className="skel-title" style={{ width: `${60 + i * 5}%` }} />
                    <div className="skel-line" style={{ width: '90%' }} />
                    <div className="skel-line" style={{ width: '40%' }} />
                  </div>
                ))}
              </div>
            ) : displayResults.length === 0 ? (
              <p className="search-empty">No results found.</p>
            ) : (
              <ul className="search-results">
                {displayResults.map((r, i) => (
                  <li key={i} className="search-result" style={{ animationDelay: `${i * 0.03}s` }}>
                    <a href={r.url} className="search-result-title bare-link">
                      <img
                        src={`https://www.google.com/s2/favicons?domain=${new URL(r.url).hostname}&sz=32`}
                        alt=""
                        width={18}
                        height={18}
                        className="search-result-favicon"
                        loading="lazy"
                      />
                      {r.title || r.url}
                    </a>
                    <p className="search-result-snippet">{r.snippet}</p>
                    <span className="search-result-license">{r.license}</span>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      )}

      <style>{`
        .search-input {
          width: 100%; padding: 8px 16px; border-radius: 8px;
          font-size: 14px; font-family: inherit; outline: none;
          box-sizing: border-box; transition: border-color 0.2s;
          background: #27272a; border: 1px solid #3f3f46; color: #e4e4e7;
        }
        .search-input::placeholder { color: #71717a; }
        .search-input:focus { border-color: #52525b; }

        .search-btn {
          position: absolute; right: 6px; top: 6px; bottom: 6px;
          padding: 0 12px; font-size: 12px; border-radius: 4px;
          background: transparent; border: 1px solid #3b82f6;
          color: #60a5fa; cursor: pointer; transition: all 0.2s;
        }
        .search-btn:hover { color: #93c5fd; border-color: #60a5fa; }

        .search-powered { font-size: 12px; color: #52525b; margin-top: 8px; }
        .search-powered a { text-decoration: underline; color: inherit; }
        .search-powered a:hover { color: #a1a1aa; }

        .search-overlay {
          position: fixed; inset: 0; z-index: 100;
          background: rgba(0,0,0,0.6);
          display: flex; align-items: flex-start; justify-content: center;
          padding-top: 12vh;
          animation: searchFadeIn 0.4s ease-out;
        }
        .search-modal {
          width: 100%; max-width: 600px; max-height: 70vh; overflow-y: auto;
          background: #1c1c1e; border-radius: 12px; padding: 20px;
          animation: searchSlideUp 0.4s ease-out; box-sizing: border-box;
          color: #d4d4d8;
        }
        .search-modal-header {
          display: flex; justify-content: space-between; align-items: center;
          margin-bottom: 16px; font-size: 14px; color: #a1a1aa;
        }
        .search-modal-header button {
          background: none; border: none; color: #71717a; font-size: 18px;
          cursor: pointer; padding: 4px 8px;
        }
        .search-modal-header button:hover { color: #d4d4d8; }

        .search-skeletons { display: flex; flex-direction: column; gap: 12px; }
        .search-skeleton { animation: shimmer 1.5s ease-in-out infinite; }
        .skel-title { height: 14px; background: #333; border-radius: 4px; margin-bottom: 8px; }
        .skel-line { height: 10px; background: #2a2a2a; border-radius: 3px; margin-bottom: 4px; }

        .search-empty { font-size: 14px; color: #71717a; }

        .search-results {
          display: flex; flex-direction: column; gap: 8px;
          list-style: none; padding: 0; margin: 0;
        }
        .search-result {
          border: 1px solid #27272a; border-radius: 8px; padding: 12px 16px;
          animation: searchFadeIn 0.2s ease-out; animation-fill-mode: both;
        }
        .search-result-title {
          display: flex; align-items: center; gap: 6px;
          font-size: 14px; font-weight: 500;
          color: #fbbf24; text-decoration: none;
        }
        .search-result-favicon {
          flex-shrink: 0; border-radius: 2px;
        }
        .search-result-title:hover { color: #fde68a; }
        .search-result-snippet {
          font-size: 12px; color: #71717a; margin-top: 4px;
          display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
        }
        .search-result-license { font-size: 12px; color: #52525b; margin-top: 4px; display: inline-block; }

        /* Light mode overrides */
        :root.light .search-input {
          background: #f5f5f4; border-color: #d6d3d1; color: #1c1917;
        }
        :root.light .search-input::placeholder { color: #a8a29e; }
        :root.light .search-input:focus { border-color: #a8a29e; }

        :root.light .search-btn { border-color: #2563eb; color: #2563eb; }
        :root.light .search-btn:hover { color: #1d4ed8; border-color: #1d4ed8; }

        :root.light .search-powered { color: #a8a29e; }
        :root.light .search-powered a:hover { color: #57534e; }

        :root.light .search-overlay { background: rgba(0,0,0,0.3); }
        :root.light .search-modal { background: #fafaf9; color: #1c1917; }
        :root.light .search-modal-header { color: #78716c; }
        :root.light .search-modal-header button { color: #a8a29e; }
        :root.light .search-modal-header button:hover { color: #44403c; }

        :root.light .skel-title { background: #e7e5e4; }
        :root.light .skel-line { background: #f0efed; }

        :root.light .search-result { border-color: #e7e5e4; }
        :root.light .search-result-title { color: #92400e; }
        :root.light .search-result-title:hover { color: #78350f; }
        :root.light .search-result-snippet { color: #78716c; }
        :root.light .search-result-license { color: #a8a29e; }

        @keyframes searchFadeIn {
          from { opacity: 0; } to { opacity: 1; }
        }
        @keyframes searchSlideUp {
          from { opacity: 0; transform: translateY(20px); }
          to { opacity: 1; transform: translateY(0); }
        }
        @keyframes shimmer {
          0%, 100% { opacity: 0.4; } 50% { opacity: 0.8; }
        }
      `}</style>
    </div>
  );
}
