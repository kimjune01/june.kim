import React, { useState } from 'react';
import { town, mean, sampleWithoutReplacement } from '../../../reading-src/lib/statistics/inference';
export default function TownSampler({ compare = false }: { compare?: boolean }) {
  const [size, setSize] = useState(10);
  const [sample, setSample] = useState<typeof town>([]);
  const [courtSample, setCourtSample] = useState<typeof town>([]);
  const [revealed, setRevealed] = useState(compare);
  const truth = mean(town.map(p => p.height));
  const selected = new Set(sample.map(p => p.id));
  function draw() { setSample(sampleWithoutReplacement(town, size)); if (compare) setCourtSample(sampleWithoutReplacement(town.filter(p => p.court), size)); }
  return <section className="stats-lab bg-zinc-800 rounded-lg p-5 mb-8 callout" id={compare ? 'bias-lab' : 'sampling-lab'} aria-label={compare ? 'Compare sampling rules' : 'Sample a hidden town'}>
    <p className="stats-eyebrow">A fictional town of 200 adults</p>
    <label className="stats-control">People to sample<select aria-label="People to sample" value={size} onChange={e => { setSize(Number(e.target.value)); setSample([]); setCourtSample([]); }}>{(compare ? [5, 10, 20, 40] : [5, 10, 20, 40, 100, 200]).map(n => <option key={n} value={n}>{n} people</option>)}</select></label>
    <p className="stats-small">Sample without replacement: nobody is measured twice in a single sample.</p>
    <div className="stats-town" aria-hidden="true">{town.map(person => <span key={person.id} className={selected.has(person.id) ? 'chosen' : revealed && person.court ? 'court' : ''} />)}</div>
    <p className="stats-small">Each dot is a resident. Filled dots mark the town-wide sample.{revealed && ' Thick outlined dots mark other residents in the basketball-court subgroup.'}</p>
    <div className="stats-actions"><button type="button" onClick={draw}>Draw a sample</button>{!revealed && <button type="button" onClick={() => setRevealed(true)}>Reveal the town</button>}</div>
    <p role="status">{sample.length ? `${sample.length} people measured. Town-wide sample mean: ${mean(sample.map(p => p.height)).toFixed(1)} cm.` : 'No sample yet. What do you think the town’s average height will be?'}</p>
    {compare && courtSample.length > 0 && <p>Court-only sample mean: <strong>{mean(courtSample.map(p => p.height)).toFixed(1)} cm</strong>. These {courtSample.length} people came from the 40 adults in the court subgroup.</p>}
    {revealed && <p className="stats-feedback">Population mean: <strong>{truth.toFixed(1)} cm</strong>. {sample.length > 0 && `Your town-wide estimate is ${(mean(sample.map(p => p.height)) - truth).toFixed(1)} cm from it.`} {compare && 'Measuring all 40 court residents removes uncertainty about that subgroup, but it still does not represent the whole town.'}</p>}
    {sample.length > 0 && <details className="stats-data"><summary>See the sampled observations</summary><div className="stats-table-scroll"><table><caption>Town-wide sample</caption><thead><tr><th scope="col">Resident</th><th scope="col">Height (cm)</th></tr></thead><tbody>{sample.map(p => <tr key={p.id}><th scope="row">{p.id + 1}</th><td>{p.height}</td></tr>)}</tbody></table></div></details>}
  </section>;
}
