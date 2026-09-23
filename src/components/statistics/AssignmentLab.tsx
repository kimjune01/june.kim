import React, { useState } from 'react';
import { mean, randomizedGroups } from '../../../reading-src/lib/statistics/inference';
const students = Array.from({ length: 40 }, (_, id) => ({ id, baseline: id < 20 ? 50 + id % 5 : 75 + id % 5 }));
export default function AssignmentLab() {
  const [groups, setGroups] = useState<{ treatment: typeof students; control: typeof students } | null>(null);
  const [method, setMethod] = useState('');
  return <section className="stats-lab bg-zinc-800 rounded-lg p-5 mb-8 callout" aria-label="Treatment assignment experiment">
    <p className="stats-eyebrow">Does the study app work?</p><p>In this invented class, the app adds exactly zero points to anyone’s score. The already stronger students are more eager to use it. Compare their choice with a random split.</p>
    <div className="stats-actions"><button type="button" onClick={() => { setGroups({ treatment: students.slice(20), control: students.slice(0, 20) }); setMethod('Students chose'); }}>Let students choose</button><button type="button" onClick={() => { setGroups(randomizedGroups(students)); setMethod('Randomly assigned'); }}>Randomly assign</button></div>
    <div role="status">{groups ? <p>{method}: app group {mean(groups.treatment.map(p => p.baseline)).toFixed(1)} points; comparison group {mean(groups.control.map(p => p.baseline)).toFixed(1)} points. Apparent difference: <strong>{(mean(groups.treatment.map(p => p.baseline)) - mean(groups.control.map(p => p.baseline))).toFixed(1)} points</strong>.</p> : <p>Choose a way to form the groups.</p>}</div>
    <p className="stats-small">Every random split assigns 20 students to each group. Try several: random assignment balances starting differences on average, not perfectly in every trial.</p>
  </section>;
}
