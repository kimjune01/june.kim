import React,{useState} from 'react';
import {anova,chiSquareFit,formatP} from '../../../reading-src/lib/statistics/course-models';
export default function MoreGroupsLab(){
 const [imbalance,setImbalance]=useState(0),[separation,setSeparation]=useState(0),[spread,setSpread]=useState(1);
 const counts=[30+imbalance,30,30-imbalance],chi=chiSquareFit(counts);
 const groups=[0,1,2].map(g=>[-5,-3,-1,1,3,5].map(v=>50+g*separation+spread*v)),f=anova(groups);
 return <section className="stats-lab bg-zinc-800 rounded-lg p-5 mb-8 callout" id="groups-lab" aria-label="Compare more than two groups">
  <p className="stats-eyebrow">Counts or measurements?</p><p>These constructed examples let you change a pattern while holding other features fixed. They are not repeated random samples.</p>
  <h3>Three categories: count the choices</h3><p>Ninety independently sampled people choose one of three meeting times. The null model gives each option probability one third, so each expected count is 30.</p>
  <label className="stats-control">Move choices from C to A<select aria-label="Count imbalance" value={imbalance} onChange={e=>setImbalance(Number(e.target.value))}>{[0,5,10,20,25].map(v=><option key={v} value={v}>{v} choices</option>)}</select></label>
  <table><thead><tr><th scope="col">Option</th><th scope="col">Observed</th><th scope="col">Expected under null</th></tr></thead><tbody>{counts.map((v,i)=><tr key={i}><th scope="row">{['A','B','C'][i]}</th><td>{v}</td><td>30</td></tr>)}</tbody></table>
  <p role="status">Chi-square statistic {chi.statistic.toFixed(2)}, df = 2. Right-tail p-value {formatP(chi.p)}.</p>
  <h3>Three groups: compare numerical outcomes</h3><p>Now three independent groups each provide six quiz scores. Compare their mean differences with the variation within groups.</p>
  <div className="stats-settings"><label className="stats-control">Separation between group means<select aria-label="Group separation" value={separation} onChange={e=>setSeparation(Number(e.target.value))}>{[0,2,5,10].map(v=><option key={v} value={v}>{v} points</option>)}</select></label><label className="stats-control">Within-group spread multiplier<select aria-label="Within-group spread" value={spread} onChange={e=>setSpread(Number(e.target.value))}>{[1,2,4].map(v=><option key={v} value={v}>{v}×</option>)}</select></label></div>
  <div className="stats-table-scroll"><table><thead><tr><th scope="col">Group</th><th scope="col">Mean</th><th scope="col">Observed scores</th></tr></thead><tbody>{groups.map((g,i)=><tr key={i}><th scope="row">{i+1}</th><td>{50+i*separation}</td><td>{g.join(', ')}</td></tr>)}</tbody></table></div>
  <p role="status">ANOVA F = {f.statistic.toFixed(2)}, df = (2, 15). Right-tail p-value {formatP(f.p)}.</p>
  <p className="stats-small">The chi-square approximation requires independent cases and adequate expected counts (all are 30 here). Classical one-way ANOVA assumes independent observations, approximately normal errors, and equal population variances. A small omnibus p-value says at least one null restriction fails; it does not identify every pair that differs.</p>
 </section>;
}
