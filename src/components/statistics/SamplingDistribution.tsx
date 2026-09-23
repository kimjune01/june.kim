import React, { useState } from 'react';
import { populations, sampleMeans, mean, populationSD, type PopulationShape } from '../../../reading-src/lib/statistics/inference';
import DistributionPlot from './DistributionPlot';
export default function SamplingDistribution() {
  const [shape, setShape] = useState<PopulationShape>('skewed');
  const [size, setSize] = useState(1);
  const [means, setMeans] = useState<number[]>([]);
  const [saved, setSaved] = useState<{ values: number[]; size: number; shape: PopulationShape } | null>(null);
  const population = populations[shape], center = mean(population), sd = populationSD(population);
  function run(repeats: number) { setMeans([...means, ...sampleMeans(population, size, repeats)].slice(-10000)); }
  return <section className="stats-lab bg-zinc-800 rounded-lg p-5 mb-8 callout" id="means-lab" aria-label="Build a sampling distribution">
    <p className="stats-eyebrow">One sample becomes one mean</p>
    <div className="stats-settings"><label className="stats-control">Population shape<select aria-label="Population shape" value={shape} onChange={e => { setShape(e.target.value as PopulationShape); setMeans([]); setSaved(null); }}><option value="skewed">A long right tail</option><option value="bimodal">Two separated peaks</option><option value="uniform">An even spread</option></select></label>
    <label className="stats-control">Observations per sample<select aria-label="Observations per sample" value={size} onChange={e => { setSize(Number(e.target.value)); setMeans([]); }}>{[1, 2, 5, 10, 30, 100].map(n => <option key={n} value={n}>{n} {n === 1 ? 'observation' : 'observations'}</option>)}</select></label></div>
    <DistributionPlot values={population} min={0} max={100} title="The population stays this shape" unit="Individual values" marker={{ value: center, label: 'population mean' }} />
    <p>Draw independently <strong>with replacement</strong>: each observation uses the same population again. Average the values, and place that one mean in the lower chart.</p>
    <div className="stats-actions"><button type="button" onClick={() => run(1)}>Take one sample</button><button type="button" onClick={() => run(500)}>Take 500 samples</button><button type="button" onClick={() => setMeans([])}>Start over</button></div>
    <p role="status">{means.length.toLocaleString('en-US')} sample {means.length === 1 ? 'mean' : 'means'} recorded{means.length ? `. Latest mean: ${means.at(-1)!.toFixed(1)} from ${size} observations.` : '.'}</p>
    <DistributionPlot values={means} min={0} max={100} bins={80} title={`Means of samples of ${size}`} unit="Sample means" marker={{ value: center, label: 'population mean' }} />
    <div className="stats-actions"><button type="button" disabled={!means.length} onClick={() => setSaved({ values: [...means], size, shape })}>Keep these means</button>{saved && <button type="button" onClick={() => setSaved(null)}>Remove comparison</button>}</div>
    {saved && <DistributionPlot values={saved.values} min={0} max={100} bins={80} title={`Saved: means of samples of ${saved.size}`} unit="Sample means" marker={{ value: center, label: 'population mean' }} />}
    <p className="stats-small">All horizontal axes stay at 0–100. Each vertical axis counts its own observations. At most the latest 10,000 means are shown. Changing sample size clears the current means; changing population clears both runs.</p>
    <details className="stats-extra"><summary>Put a number on the narrowing</summary><p>The population’s standard deviation is {sd.toFixed(2)}. For samples of {size}, the standard error of the mean is {sd.toFixed(2)} ÷ √{size} = <strong>{(sd / Math.sqrt(size)).toFixed(2)}</strong>. The population’s spread stays the same; the estimates become steadier.</p></details>
  </section>;
}
