import React, { useState } from 'react';
import { mean, median, populationSD } from '../../../reading-src/lib/statistics/inference';
const money = (thousands: number) => `$${Math.round(thousands * 1000).toLocaleString('en-US')}`;
export default function DataExplorer() {
  const [salaries, setSalaries] = useState([40, 50, 60, 70, 80]);
  const [newcomer, setNewcomer] = useState(false);
  const values = newcomer ? [...salaries, 1000] : salaries;
  const average = mean(values), middle = median(values), max = newcomer ? 1050 : 110;
  const x = (value: number) => 45 + value / max * 450;
  return <section className="stats-lab" id="data-lab" aria-label="Salary experiment">
    <p className="stats-eyebrow">Five people, five salaries</p>
    <p>Change a salary with its slider. The plot and summaries follow your changes. All amounts are fictional annual salaries.</p>
    <div className="stats-salary-controls">{salaries.map((salary, i) => <label className="stats-control" key={i}>Person {i + 1}: {money(salary)}<input type="range" min="0" max="100" step="1" value={salary} aria-label={`Salary for person ${i + 1}`} onChange={e => setSalaries(salaries.map((v, j) => j === i ? Number(e.target.value) : v))} /></label>)}</div>
    <div className="stats-actions"><button type="button" onClick={() => setNewcomer(!newcomer)}>{newcomer ? 'Remove the newcomer' : 'Add a $1m salary'}</button><button type="button" onClick={() => { setSalaries([40, 50, 60, 70, 80]); setNewcomer(false); }}>Start over</button></div>
    <figure className="stats-histogram"><figcaption>One row per person; position shows salary</figcaption><svg viewBox="0 0 540 205" role="img" aria-label="Salary positions, with mean and median marked">
      {values.map((salary, i) => <g key={i}><text x="20" y={36 + i * 22}>{i + 1}</text><circle cx={x(salary)} cy={32 + i * 22} r="6" className="stats-bar"><title>{`Person ${i + 1}: ${money(salary)}`}</title></circle></g>)}
      <line x1={x(average)} x2={x(average)} y1="18" y2="165" className="stats-truth" /><line x1={x(middle)} x2={x(middle)} y1="18" y2="165" className="stats-median" />
      <text x="45" y="189">$0</text><text x="495" y="189" textAnchor="end">{money(max)}</text>
    </svg></figure>
    <div className="stats-readouts stats-readouts-row" aria-live="polite"><div><span className="stats-small">Mean · dashed line</span><strong>{money(average)}</strong></div><div><span className="stats-small">Median · solid line</span><strong>{money(middle)}</strong></div></div>
    <p className="stats-worked-example">Your mean: {money(values.reduce((a, b) => a + b, 0))} shared across {values.length} people = {money(average)} each.</p>
    <details className="stats-extra"><summary>Same mean, different spread</summary><p>Try these two groups. Both have a mean and median of $60,000.</p><div className="stats-actions"><button type="button" onClick={() => { setSalaries([55, 58, 60, 62, 65]); setNewcomer(false); }}>Close together</button><button type="button" onClick={() => { setSalaries([20, 40, 60, 80, 100]); setNewcomer(false); }}>Far apart</button></div><p className="stats-small">Population standard deviation for these {values.length} people: {money(populationSD(values))}. Larger means more spread around the mean.</p></details>
  </section>;
}
