import React, { useState } from 'react';
import { spinBatch } from '../../../reading-src/lib/statistics/experiments';

export default function Spinner() {
  const [chance, setChance] = useState(50);
  const [total, setTotal] = useState(0);
  const [blue, setBlue] = useState(0);
  const [recent, setRecent] = useState<boolean[]>([]);
  const [angle, setAngle] = useState(0);
  const [notice, setNotice] = useState('No spins yet. Both colors are possible.');

  function reset(nextChance = chance) {
    setChance(nextChance); setTotal(0); setBlue(0); setRecent([]); setAngle(0);
    setNotice('No spins yet. A fresh experiment is ready.');
  }
  function run(count: number) {
    const result = spinBatch(chance / 100, count);
    setTotal(total + count); setBlue(blue + result.blue);
    setRecent([...recent, ...result.outcomes].slice(-20));
    setAngle(Math.floor(angle / 360) * 360 + 720 + result.lastPosition * 360);
    setNotice(`${blue + result.blue} blue out of ${total + count} ${total + count === 1 ? 'spin' : 'spins'}. Last spin: ${result.outcomes.at(-1) ? 'blue' : 'amber'}.`);
  }

  return <section id="spinner" className="stats-lab" aria-label="Spinner experiment">
    <div className="stats-lab-heading"><span className="stats-eyebrow">Your first experiment</span><span className="stats-tag">One spin, one outcome</span></div>
    <div className="stats-spinner-layout">
      <div className="stats-wheel-wrap">
        <div className="stats-wheel" role="img" aria-label={`Spinner: ${chance}% blue, ${100 - chance}% amber. Each direction is equally likely.`}
          style={{ background: `conic-gradient(var(--stats-blue) 0% ${chance}%, var(--stats-amber) ${chance}% 100%)` }}>
          <div className="stats-needle" style={{ transform: `rotate(${angle}deg)` }}><span /></div>
          <span className="stats-wheel-hub" />
        </div>
        <p className="stats-small">Every direction has the same chance.</p>
      </div>
      <div>
        <label className="stats-control">Chance of blue
          <select aria-label="Chance of blue" value={chance} onChange={e => reset(Number(e.target.value))}>
            {[0, 25, 50, 75, 100].map(value => <option key={value} value={value}>{value}% · {value / 100}</option>)}
          </select>
        </label>
        <p className="stats-small">Changing the chance starts a fresh record.</p>
        <div className="stats-readouts">
          <div><span className="stats-small">The rule you chose</span><strong>{chance}% blue</strong></div>
          <div><span className="stats-small">What happened so far</span><strong>{total ? `${Math.round(100 * blue / total)}% blue` : '—'}</strong></div>
        </div>
      </div>
    </div>
    <div className="stats-actions">
      <button type="button" onClick={() => run(1)}>Spin once</button>
      <button type="button" onClick={() => run(10)}>Spin 10 times</button>
      <button type="button" onClick={() => run(100)}>Spin 100 times</button>
      <button type="button" className="stats-quiet" onClick={() => reset()}>Start over</button>
    </div>
    <p className="stats-status" role="status">{notice}</p>
    {recent.length > 0 && <div>
      <div className="stats-trail" aria-hidden="true">{recent.map((isBlue, i) => <span className={isBlue ? 'blue' : 'amber'} key={`${total - recent.length + i}`}>{isBlue ? 'B' : 'A'}</span>)}</div>
      <p className="stats-small">{total > 20 ? 'Most recent 20 spins' : 'Your spins'}, oldest to newest. B = blue; A = amber.</p>
    </div>}
  </section>;
}
