import React, { useState } from 'react';
import { fairCoinTail, nullCounts } from '../../../reading-src/lib/statistics/inference';
import DistributionPlot from './DistributionPlot';
export default function NullLab() {
  const [observed, setObserved] = useState(15), [counts, setCounts] = useState<number[]>([]);
  const extreme = counts.filter(count => count >= observed).length;
  const exact = fairCoinTail(20, observed) * 100;
  const formatted = exact < .01 ? exact.toFixed(6) : exact.toFixed(2);
  return <section className="stats-lab" id="null-lab" aria-label="Test a fair-coin explanation">
    <p className="stats-eyebrow">A world where the coin really is fair</p>
    <p>Our question, chosen before looking at the data: does this coin favor heads? Every simulated experiment flips a fair coin 20 independent times.</p>
    <label className="stats-control">Observed heads in 20 flips<select aria-label="Observed heads" value={observed} onChange={e => setObserved(Number(e.target.value))}>{[10, 12, 14, 15, 16, 18, 20].map(n => <option key={n} value={n}>{n} heads</option>)}</select></label>
    <div className="stats-actions"><button type="button" onClick={() => setCounts([...counts, ...nullCounts(20, 1)].slice(-10000))}>Simulate one experiment</button><button type="button" onClick={() => setCounts([...counts, ...nullCounts(20, 1000)].slice(-10000))}>Simulate 1,000 experiments</button><button type="button" onClick={() => setCounts([])}>Start over</button></div>
    <p role="status">{counts.length ? `${extreme.toLocaleString('en-US')} of ${counts.length.toLocaleString('en-US')} fair-coin experiments had ${observed} or more heads (${(100 * extreme / counts.length).toFixed(2)}%).` : 'No fair-coin experiments recorded yet.'}</p>
    <DistributionPlot values={counts} min={-.5} max={20.5} bins={21} ticks={[0, 10, 20]} title="Outcomes under the fair-coin model" unit="Heads in 20 flips" highlightFrom={observed} marker={{ value: observed, label: 'observed head count' }} />
    <p className="stats-small">Amber bars are the outcomes counted: {observed} heads or more. Changing the observed count reuses the same simulated fair-coin outcomes.</p>
    <details className="stats-extra"><summary>Check the exact probability</summary><p>For a fair coin, the probability of {observed} or more heads in 20 flips is <strong>{formatted}%</strong>. The simulation estimates this value. If no simulated experiment reached the tail, the probability still need not be zero.</p></details>
    <p className="stats-small">The latest 10,000 simulated experiments are retained. This is a one-sided test for an excess of heads; a question about bias in either direction would need both tails.</p>
  </section>;
}
