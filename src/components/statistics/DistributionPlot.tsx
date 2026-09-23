import React, { useId } from 'react';

interface Props {
  values: number[]; min: number; max: number; bins?: number; title: string; unit: string;
  marker?: { value: number; label: string }; highlightFrom?: number; ticks?: number[];
}
export default function DistributionPlot({ values, min, max, bins = 40, title, unit, marker, highlightFrom, ticks = [min, (min + max) / 2, max] }: Props) {
  const id = useId();
  const counts = Array<number>(bins).fill(0);
  for (const value of values) if (value >= min && value <= max) counts[Math.min(bins - 1, Math.floor((value - min) / (max - min) * bins))]++;
  const peak = Math.ceil(Math.max(2, ...counts) / 2) * 2;
  const x = (value: number) => Number((50 + (value - min) / (max - min) * 450).toFixed(3));
  return <figure className="stats-histogram">
    <figcaption>{title}</figcaption>
    <svg viewBox="0 0 540 230" role="img" aria-labelledby={`${id}-title`}>
      <title id={`${id}-title`}>{`${title}. ${values.length} values; exact bin counts are available below.`}</title>
      {[0, .5, 1].map(part => <g key={part}><line x1="50" x2="500" y1={180 - part * 140} y2={180 - part * 140} className="stats-grid" /><text x="42" y={184 - part * 140} textAnchor="end">{Math.round(peak * part)}</text></g>)}
      <text x="50" y="22">Frequency</text>
      {counts.map((count, i) => <rect key={i} x={50 + i * 450 / bins + .5} y={180 - count / peak * 140} width={Math.max(1, 450 / bins - 1)} height={count / peak * 140}
        className={highlightFrom !== undefined && min + (i + .5) * (max - min) / bins >= highlightFrom ? 'stats-bar-saved' : 'stats-bar'} />)}
      {marker && <line x1={x(marker.value)} x2={x(marker.value)} y1="32" y2="180" className="stats-truth" />}
      {ticks.map(value => <text key={value} x={x(value)} y="204" textAnchor="middle">{Number(value.toFixed(1))}</text>)}
      <text x="275" y="228" textAnchor="middle">{unit}</text>
      {!values.length && <text x="275" y="110" textAnchor="middle" className="stats-chart-empty">Run an experiment to add values.</text>}
    </svg>
    {marker && <p className="stats-small">Dashed line: {marker.label} = {marker.value.toFixed(1)}.</p>}
    <details className="stats-data"><summary>Read the chart as a table</summary><div className="stats-table-scroll"><table>
      <caption>{title}</caption><thead><tr><th scope="col">Value range</th><th scope="col">Count</th></tr></thead>
      <tbody>{counts.map((count, i) => <tr key={i}><th scope="row">{(min + i * (max - min) / bins).toFixed(1)}–{(min + (i + 1) * (max - min) / bins).toFixed(1)}</th><td>{count}</td></tr>)}</tbody>
    </table></div><p className="stats-small">Each range includes its lower end and excludes its upper end, except the last range, which includes both.</p></details>
  </figure>;
}
