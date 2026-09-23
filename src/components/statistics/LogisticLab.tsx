import React, {useId,useState} from 'react';
import {logistic} from '../../../reading-src/lib/statistics/relationships';
import Question from './Question';
export default function LogisticLab() {
 const id=useId(),[hours,setHours]=useState(4),[coefficient,setCoefficient]=useState(.8);
 const p=logistic(-4+coefficient*hours), x=(v:number)=>45+v*45,y=(v:number)=>200-v*160;
 const path=Array.from({length:101},(_,i)=>`${i?'L':'M'}${x(i/10).toFixed(2)},${y(logistic(-4+coefficient*i/10)).toFixed(2)}`).join(' ');
 return <section className="stats-lab" id="logistic-lab" aria-label="Logistic probability experiment">
  <p className="stats-eyebrow">Predicting a yes or a no</p><p>Imagine a model for passing a practice test. A straight line could predict a probability below zero or above one. A logistic curve keeps the prediction between those limits.</p>
  <p className="stats-small">These coefficients are invented for exploration, not fitted to evidence about studying. The model is predictive; changing a slider does not establish a causal effect.</p>
  <div className="stats-settings"><label className="stats-control">Study hours: {hours}<input aria-label="Study hours" type="range" min="0" max="10" step=".5" value={hours} onChange={e=>setHours(Number(e.target.value))}/></label><label className="stats-control">Hour coefficient: {coefficient.toFixed(1)}<input aria-label="Hour coefficient" type="range" min="-.5" max="1.5" step=".1" value={coefficient} onChange={e=>setCoefficient(Number(e.target.value))}/></label></div>
  <figure className="stats-histogram"><figcaption>Model probability of passing</figcaption><svg viewBox="0 0 540 255" role="img" aria-labelledby={`${id}-title`}><title id={`${id}-title`}>{`Logistic curve; at ${hours} hours the model predicts ${(p*100).toFixed(1)} percent.`}</title>{[0,.5,1].map(v=><g key={v}><line x1="45" x2="495" y1={y(v)} y2={y(v)} className="stats-grid"/><text x="38" y={y(v)+4} textAnchor="end">{v*100}%</text></g>)}<path d={path} fill="none" className="stats-median"/><line x1={x(hours)} x2={x(hours)} y1={Number(y(p).toFixed(3))} y2="200" className="stats-truth"/><circle cx={x(hours)} cy={Number(y(p).toFixed(3))} r="5" className="stats-bar"/>{[0,5,10].map(v=><text key={v} x={x(v)} y="225" textAnchor="middle">{v}</text>)}<text x="270" y="252" textAnchor="middle">Study hours</text></svg></figure>
  <p role="status">At {hours} hours, predicted probability: <strong>{(p*100).toFixed(1)}%</strong>. Odds: {(p/(1-p)).toFixed(2)} to 1.</p>
  <p>Keep the coefficient fixed and move along the curve. One more hour always adds the same amount to <em>log odds</em>, but its change in probability depends on where you start.</p>
  <details className="stats-data"><summary>Read the curve as a table</summary><table><thead><tr><th scope="col">Hours</th><th scope="col">Probability</th></tr></thead><tbody>{Array.from({length:11},(_,h)=><tr key={h}><td>{h}</td><td>{(100*logistic(-4+coefficient*h)).toFixed(1)}%</td></tr>)}</tbody></table></details>
  <details className="stats-extra"><summary>Compress the curve into a model</summary><p>log(p / (1 − p)) = b₀ + b₁x. Here b₀ = −4 and b₁ = {coefficient.toFixed(1)}. p / (1 − p) is odds; log means the natural logarithm. Each extra hour multiplies the odds by e<sup>b₁</sup> = {Math.exp(coefficient).toFixed(2)}.</p><p>Equivalently, p = 1 / (1 + e<sup>−(b₀ + b₁x)</sup>). Multiple logistic regression adds more predictors inside the same expression.</p></details>
  <Question id="logistic-transfer" prompt="A coefficient implies that one extra unit doubles the odds, holding other predictors fixed. Does it also double the probability?" choices={[
   {label:'Yes; odds and probability are interchangeable.',correct:false,feedback:'A probability of 50% means odds of 1 to 1. Doubling those odds to 2 to 1 gives probability 2/3, not 100%.'},
   {label:'No; odds are p divided by 1 − p.',correct:true,feedback:'The same multiplier on odds corresponds to different probability changes at different starting probabilities.'}
  ]} explanation="An odds ratio is a multiplier on odds. Convert back to probability before interpreting it as a chance."/>
 </section>;
}
