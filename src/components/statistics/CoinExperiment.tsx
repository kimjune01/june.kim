import React, { useId, useState } from 'react';
import { addRounds, coinRounds, emptyRounds, type RoundResults } from '../../../reading-src/lib/statistics/experiments';

type View = 'count' | 'proportion';
function Histogram({ result, view, domain, ceiling, saved = false }: { result: RoundResults; view: View; domain: number; ceiling: number; saved?: boolean }) {
  const id = useId();
  const left = 48, width = 460, baseline = 188, height = 146;
  const scale = view === 'count' ? domain : 1;
  // Common padding keeps both charts' endpoints aligned even with different n.
  const slot = width / (domain + 1);
  const position = (heads: number) => left + slot / 2 + heads / (view === 'count' ? domain : result.coins) * (width - slot);
  const barWidth = Math.max(2, slot * 0.76);
  const label = saved ? 'Saved experiment' : 'Current experiment';
  return <figure className="stats-histogram">
    <figcaption>{label} · {result.coins} coins per round · {result.total.toLocaleString()} rounds</figcaption>
    <svg viewBox="0 0 540 238" role="img" aria-labelledby={`${id}-title ${id}-desc`}>
      <title id={`${id}-title`}>{label}: distribution of {view === 'count' ? 'head counts' : 'head proportions'}</title>
      <desc id={`${id}-desc`}>Each bar shows the percentage of rounds with that result. {result.total ? `${result.total} rounds recorded. Exact values follow in the data table.` : 'Run a round to add the first result.'}</desc>
      {[0, 0.5, 1].map(fraction => <g key={fraction}>
        <line x1={left} x2={520} y1={baseline - fraction * height} y2={baseline - fraction * height} className="stats-grid" />
        <text x={left - 8} y={baseline - fraction * height + 4} textAnchor="end">{Math.round(ceiling * fraction * 100)}%</text>
      </g>)}
      <text x={left} y={20}>Share of rounds</text>
      {result.histogram.map((frequency, heads) => {
        const barHeight = result.total ? frequency / result.total / ceiling * height : 0;
        return <rect key={heads} x={position(heads) - barWidth / 2} y={baseline - barHeight} width={barWidth} height={barHeight}
          className={saved ? 'stats-bar-saved' : 'stats-bar'}><title>{heads} heads ({Math.round(heads / result.coins * 100)}%): {frequency} rounds</title></rect>;
      })}
      {[0, scale / 2, scale].map((value, i) => <text key={i} x={position(i * (view === 'count' ? domain : result.coins) / 2)} y={baseline + 21} textAnchor="middle">{view === 'count' ? value : `${value * 100}%`}</text>)}
      <text x={284} y={233} textAnchor="middle">{view === 'count' ? 'Number of heads in one round' : 'Proportion of heads in one round'}</text>
      {!result.total && <text x={284} y={110} textAnchor="middle" className="stats-chart-empty">Your first round will go here.</text>}
    </svg>
    <details className="stats-data"><summary>Read {saved ? 'saved' : 'current'} chart as a table</summary>
      <div className="stats-table-scroll"><table>
        <caption>{label}: every possible head count</caption>
        <thead><tr><th scope="col">Heads</th><th scope="col">Proportion</th><th scope="col">Rounds</th></tr></thead>
        <tbody>{result.histogram.map((frequency, heads) => <tr key={heads}><th scope="row">{heads}</th><td>{Math.round(heads / result.coins * 100)}%</td><td>{frequency}</td></tr>)}</tbody>
      </table></div>
    </details>
  </figure>;
}

export default function CoinExperiment() {
  const [result, setResult] = useState(() => emptyRounds(10, 0.5));
  const [saved, setSaved] = useState<RoundResults | null>(null);
  const [view, setView] = useState<View>('count');
  const [batch, setBatch] = useState(100);
  const [notice, setNotice] = useState('Start with one round. Its head count will add one entry to the chart.');
  const [roundKey, setRoundKey] = useState(0);
  const [animate, setAnimate] = useState(false);
  function reset(coins = result.coins, probability = result.probability) {
    setResult(emptyRounds(coins, probability));
    setNotice('Fresh experiment. Previous rounds are cleared; any saved comparison stays below.');
  }
  function run(rounds: number) {
    const next = addRounds(result, coinRounds(result.coins, result.probability, rounds));
    setResult(next); setRoundKey(roundKey + 1); setAnimate(rounds === 1);
    setNotice(`${next.total.toLocaleString()} ${next.total === 1 ? 'round' : 'rounds'} recorded. Last round: ${next.lastFlips.filter(Boolean).length} heads out of ${next.coins} coins.`);
  }
  const heads = result.lastFlips.filter(Boolean).length;
  const domain = Math.max(result.coins, saved?.coins ?? 0);
  const maximumFrequency = (data: RoundResults) => data.total ? Math.max(...data.histogram) / data.total : 0;
  const ceiling = Math.max(0.1, Math.ceil(Math.max(maximumFrequency(result), saved ? maximumFrequency(saved) : 0) * 10) / 10);
  return <section id="coin-experiment" className="stats-lab" aria-label="Repeated coin experiment">
    <div className="stats-lab-heading"><span className="stats-eyebrow">Make a distribution</span><span className="stats-tag">One round, one entry</span></div>
    <label className="stats-control">Coins per round
      <select aria-label="Coins per round" value={result.coins} onChange={e => reset(Number(e.target.value))}>
        {[2, 5, 10, 20, 40].map(n => <option value={n} key={n}>{n} coins</option>)}
      </select>
    </label>
    <p className="stats-small">Each coin is independent. Start with a 50% chance of heads.</p>
    <div className={`stats-coins ${animate ? 'stats-coins-animate' : ''}`} key={roundKey} aria-hidden="true">
      {Array.from({ length: result.coins }, (_, i) => <span className={`stats-coin ${result.lastFlips.length ? result.lastFlips[i] ? 'heads' : 'tails' : ''}`} style={{ animationDelay: `${i * 15}ms` }} key={i}>{result.lastFlips.length ? result.lastFlips[i] ? 'H' : 'T' : '·'}</span>)}
    </div>
    <div className="stats-actions"><button type="button" onClick={() => run(1)}>Flip one round</button><button type="button" className="stats-quiet" onClick={() => reset()}>Start over</button></div>
    <p className="stats-status" role="status">{notice}</p>
    {result.lastFlips.length > 0 && <p className="stats-small">Last round: {heads} / {result.coins} = {Math.round(heads / result.coins * 100)}% heads. H = heads; T = tails.</p>}
    <div className="stats-batch">
      <label className="stats-control">Now repeat: rounds to run
        <select aria-label="Rounds to run" value={batch} onChange={e => setBatch(Number(e.target.value))}>
          {[10, 100, 1000].map(n => <option value={n} key={n}>{n.toLocaleString()} rounds</option>)}
        </select>
      </label>
      <button type="button" onClick={() => run(batch)}>Run these rounds</button>
    </div>
    <div className="stats-view" role="group" aria-label="Horizontal axis">
      <button type="button" aria-pressed={view === 'count'} onClick={() => setView('count')}>Number of heads</button>
      <button type="button" aria-pressed={view === 'proportion'} onClick={() => setView('proportion')}>Proportion of heads</button>
    </div>
    <p className="stats-small">{result.total.toLocaleString()} {result.total === 1 ? 'round' : 'rounds'} recorded. Bar height shows the percentage of rounds, so you can compare runs of different lengths.</p>
    <Histogram result={result} view={view} domain={domain} ceiling={ceiling} />
    <div className="stats-actions"><button type="button" disabled={!result.total} onClick={() => { setSaved({ ...result, histogram: [...result.histogram], lastFlips: [...result.lastFlips] }); setNotice('Comparison saved. Try another number of coins, then run some rounds.'); }}>Keep for comparison</button>
      {saved && <button type="button" className="stats-quiet" onClick={() => { setSaved(null); setNotice('Saved comparison removed. Your current experiment is unchanged.'); }}>Remove comparison</button>}
    </div>
    {saved && <div className="stats-comparison">
      <p className="stats-small">Saved: {saved.coins} coins · {saved.probability * 100}% chance of heads. Both charts use the same axes.</p>
      <Histogram result={saved} view={view} domain={domain} ceiling={ceiling} saved />
    </div>}
    <details className="stats-extra"><summary>Another thing to try: change the coin</summary>
      <p>So far, heads and tails have had equal chances. What shape would you expect if heads were more likely?</p>
      <label className="stats-control">Chance of heads
        <select aria-label="Chance of heads" value={result.probability * 100} onChange={e => reset(result.coins, Number(e.target.value) / 100)}>
          {[0, 25, 50, 75, 100].map(p => <option value={p} key={p}>{p}%</option>)}
        </select>
      </label>
      <p className="stats-small">Changing the number of coins or their chance of heads clears the current experiment. A saved comparison stays labeled with its own settings.</p>
    </details>
  </section>;
}
