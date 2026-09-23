import React, {useId,useState} from 'react';
import {fitLine,regressionPoints,squaredError} from '../../../reading-src/lib/statistics/relationships';
import Question from './Question';
export default function RegressionLab() {
 const id=useId(), [slope,setSlope]=useState(.5), [intercept,setIntercept]=useState(2), [outlier,setOutlier]=useState(false);
 const points=outlier?[...regressionPoints,{x:9,y:2}]:regressionPoints;
 const best=fitLine(points),error=squaredError(points,{slope,intercept});
 const x=(v:number)=>40+v*45, y=(v:number)=>250-v*18;
 return <section className="stats-lab bg-zinc-800 rounded-lg p-5 mb-8 callout" id="regression-lab" aria-label="Fit a line experiment">
  <p className="stats-eyebrow">How close can your line get?</p>
  <p>Each dot is an invented observation. Move the line to make the vertical gaps small. Those gaps are <strong>residuals</strong>: observed value minus predicted value.</p>
  <div className="stats-settings"><label className="stats-control">Slope: {slope.toFixed(2)}<input aria-label="Line slope" type="range" min="-1" max="2" step=".01" value={slope} onChange={e=>setSlope(Number(e.target.value))}/></label><label className="stats-control">Intercept: {intercept.toFixed(2)}<input aria-label="Line intercept" type="range" min="-2" max="5" step=".01" value={intercept} onChange={e=>setIntercept(Number(e.target.value))}/></label></div>
  <figure className="stats-histogram"><figcaption>Predict y from x · dashed vertical lines are residuals</figcaption><svg viewBox="0 0 540 300" role="img" aria-labelledby={`${id}-title`}><title id={`${id}-title`}>Observations, fitted line, and residuals; exact values are in the table.</title><defs><clipPath id={`${id}-clip`}><rect x="40" y="20" width="450" height="230"/></clipPath></defs>
   {[0,5,10].map(v=><g key={v}><line x1="40" x2="490" y1={y(v)} y2={y(v)} className="stats-grid"/><text x="30" y={y(v)+4} textAnchor="end">{v}</text><text x={x(v)} y="275" textAnchor="middle">{v}</text></g>)}
   <g clipPath={`url(#${id}-clip)`}><line x1={x(0)} x2={x(10)} y1={y(intercept)} y2={y(intercept+slope*10)} className="stats-median"/>{points.map((p,i)=><g key={i}><line x1={x(p.x)} x2={x(p.x)} y1={y(p.y)} y2={y(intercept+slope*p.x)} className="stats-truth"/><circle cx={x(p.x)} cy={y(p.y)} r="5" className="stats-bar"/></g>)}</g><text x="270" y="298">x</text><text x="15" y="20">y</text>
  </svg></figure>
  <p role="status">Sum of squared residuals: <strong>{error.toFixed(2)}</strong>. Best possible for these points: {squaredError(points,best).toFixed(2)}.</p>
  <div className="stats-actions"><button type="button" onClick={()=>{setSlope(best.slope);setIntercept(best.intercept);}}>Show the least-squares line</button><button type="button" onClick={()=>setOutlier(!outlier)}>{outlier?'Remove the unusual point':'Add an unusual point'}</button></div>
  <p className="stats-small">Adding a point keeps your current line. Predict how the best line will change, then fit again. Axes stay fixed; parts of a trial line outside the plot are clipped.</p>
  <details className="stats-data"><summary>Read predictions and residuals</summary><div className="stats-table-scroll"><table><thead><tr><th scope="col">x</th><th scope="col">Observed y</th><th scope="col">Predicted y</th><th scope="col">Residual</th></tr></thead><tbody>{points.map((p,i)=><tr key={i}><td>{p.x}</td><td>{p.y}</td><td>{(intercept+slope*p.x).toFixed(2)}</td><td>{(p.y-intercept-slope*p.x).toFixed(2)}</td></tr>)}</tbody></table></div></details>
  <details className="stats-extra"><summary>The line you have built</summary><p>ŷ = b₀ + b₁x. The hat on y marks a prediction. b₀ is the intercept; b₁ is the slope. Your current line is ŷ = {intercept.toFixed(2)} + ({slope.toFixed(2)})x. Least squares chooses the coefficients that minimize the sum of squared residuals, ∑(y − ŷ)².</p><p>A good fit does not establish causation. Extrapolating beyond observed x values needs additional justification.</p></details>
  <Question id="residual-transfer" prompt="One prediction is 3 units too high and another is 3 too low. Is the fit perfect because the errors cancel?" choices={[
   {label:'Yes; their total error is zero.',correct:false,feedback:'Both predictions missed. Adding signed errors can hide that; squaring keeps their contributions positive.'},
   {label:'No; they contribute 9 + 9 = 18 to squared error.',correct:true,feedback:'Squared residuals measure misses without letting opposite directions cancel.'}
  ]} explanation="Least squares minimizes squared misses, not the signed total. Large misses count especially heavily, which also makes unusual points influential." />
 </section>;
}
