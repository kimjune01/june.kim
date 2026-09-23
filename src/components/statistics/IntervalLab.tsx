import React, { useId, useState } from 'react';
import { confidenceIntervals, normalInterval, type Confidence, type Interval } from '../../../reading-src/lib/statistics/inference';
export default function IntervalLab() {
  const id = useId();
  const [size, setSize] = useState(25), [confidence, setConfidence] = useState<Confidence>(95);
  const [intervals, setIntervals] = useState<Interval[]>([]), [revealed, setRevealed] = useState(false);
  const margin = normalInterval(170, size, confidence).high - 170;
  const visible = intervals.slice(-40), covered = intervals.filter(i => i.covers).length;
  const min = Math.min(140, ...visible.map(i => i.low)) - 1, max = Math.max(200, ...visible.map(i => i.high)) + 1;
  const x = (value: number) => 45 + (value - min) / (max - min) * 450;
  function run(repeats: number) { setIntervals([...intervals, ...confidenceIntervals(size, confidence, repeats)].slice(-10000)); }
  return <section className="stats-lab bg-zinc-800 rounded-lg p-5 mb-8 callout" id="interval-lab" aria-label="Confidence interval experiment">
    <p className="stats-eyebrow">Give each estimate some room</p>
    <p>Each sample comes from a simulated normal population. Its standard deviation is known to be 10 cm. Its mean is hidden until you reveal it.</p>
    <div className="stats-settings"><label className="stats-control">Sample size<select aria-label="Interval sample size" value={size} onChange={e => { setSize(Number(e.target.value)); setIntervals([]); }}>{[5, 25, 100].map(n => <option key={n} value={n}>{n}</option>)}</select></label><label className="stats-control">Confidence level<select aria-label="Confidence level" value={confidence} onChange={e => { setConfidence(Number(e.target.value) as Confidence); setIntervals([]); }}>{[80, 95, 99].map(c => <option key={c} value={c}>{c}%</option>)}</select></label></div>
    <p className="stats-small">Each interval reaches {margin.toFixed(2)} cm either side of its sample mean. Changing a setting begins a new record.</p>
    <div className="stats-actions"><button type="button" onClick={() => run(1)}>Make one interval</button><button type="button" onClick={() => run(100)}>Make 100 intervals</button>{!revealed && <button type="button" onClick={() => setRevealed(true)}>Reveal the true mean</button>}<button type="button" onClick={() => setIntervals([])}>Start over</button></div>
    <p role="status">{intervals.length.toLocaleString('en-US')} intervals recorded.{revealed && intervals.length > 0 && ` ${covered.toLocaleString('en-US')} contain 170 cm (${(100 * covered / intervals.length).toFixed(1)}%).`}</p>
    <figure className="stats-histogram"><figcaption>Most recent {visible.length} intervals{revealed ? ' · dashed line: true mean 170 cm' : ''}</figcaption><svg viewBox="0 0 540 330" role="img" aria-labelledby={id}><title id={id}>{`Confidence intervals. ${revealed ? 'Solid intervals contain the true mean; dashed intervals miss.' : 'Reveal the mean to see which intervals cover it.'}`}</title>
      {revealed && <line x1={x(170)} x2={x(170)} y1="15" y2="295" className="stats-truth" />}
      {visible.map((interval, i) => <g key={i}><line x1={x(interval.low)} x2={x(interval.high)} y1={20 + i * 6.7} y2={20 + i * 6.7} className={revealed && !interval.covers ? 'stats-interval-miss' : 'stats-interval'} /><circle cx={x(interval.mean)} cy={20 + i * 6.7} r="2" fill="currentColor" /></g>)}
      {!visible.length && <text x="275" y="140" textAnchor="middle">Make a sample to get an interval.</text>}
      {[140, 170, 200].map(v => <text key={v} x={x(v)} y="315" textAnchor="middle">{v} cm</text>)}
    </svg></figure>
    {revealed && <p className="stats-small">Solid blue intervals contain the truth; dashed amber intervals miss. The true mean stays fixed. Each new sample moves the interval.</p>}
    {intervals.length > 0 && <details className="stats-data"><summary>Read the intervals as a table</summary><div className="stats-table-scroll"><table><thead><tr><th scope="col">Mean</th><th scope="col">Lower</th><th scope="col">Upper</th>{revealed && <th scope="col">Covers truth?</th>}</tr></thead><tbody>{visible.map((v, i) => <tr key={i}><td>{v.mean.toFixed(2)}</td><td>{v.low.toFixed(2)}</td><td>{v.high.toFixed(2)}</td>{revealed && <td>{v.covers ? 'Yes' : 'No'}</td>}</tr>)}</tbody></table></div></details>}
    <p className="stats-small">Coverage counts include the latest 10,000 intervals; the plot shows the latest 40. An observed percentage need not equal the chosen confidence level exactly.</p>
  </section>;
}
