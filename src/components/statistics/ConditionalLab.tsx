import React, {useState} from 'react';
import {flagCounts} from '../../../reading-src/lib/statistics/relationships';
import Question from './Question';
export default function ConditionalLab() {
 const [rate,setRate]=useState(1),[given,setGiven]=useState<'flag'|'defect'>('flag');
 const c=flagCounts(rate), denominator=given==='flag'?c.defectFlagged+c.goodFlagged:c.defectFlagged+c.defectMissed;
 return <section className="stats-lab bg-zinc-800 rounded-lg p-5 mb-8 callout" id="conditional-lab" aria-label="Conditional probability experiment">
  <p className="stats-eyebrow">What does a warning tell you?</p>
  <p>A fictional factory scanner flags 90% of defective items. It also flags 10% of good items. If an item gets flagged, is it probably defective? Predict first, then change how common defects are.</p>
  <label className="stats-control">Defective items in the factory<select value={rate} onChange={e=>setRate(Number(e.target.value))}>{[1,5,10,25,50].map(n=><option key={n} value={n}>{n}%</option>)}</select></label>
  <p className="stats-small">These are expected counts per 10,000 items, not a simulated batch. The scanner’s two conditional rates stay fixed.</p>
  <div className="stats-table-scroll"><table><thead><tr><th scope="col">Items</th><th scope="col">Flagged</th><th scope="col">Passed</th></tr></thead><tbody><tr className={given==='defect'?'stats-selected-row':''}><th scope="row">Defective</th><td className="stats-selected-cell">{c.defectFlagged}</td><td>{c.defectMissed}</td></tr><tr><th scope="row">Good</th><td className={given==='flag'?'stats-selected-cell':''}>{c.goodFlagged}</td><td>{c.goodPassed}</td></tr></tbody></table></div>
  <div className="stats-actions"><button type="button" aria-pressed={given==='flag'} onClick={()=>setGiven('flag')}>Among flagged items</button><button type="button" aria-pressed={given==='defect'} onClick={()=>setGiven('defect')}>Among defective items</button></div>
  <p role="status">{given==='flag'?'Defective among flagged':'Flagged among defective'}: {c.defectFlagged} ÷ {denominator} = <strong>{(100*c.defectFlagged/denominator).toFixed(1)}%</strong>.</p>
  <p>“Given” changes the denominator. At a 1% defect rate, 90 defective and 990 good items are flagged. Only 90 of those 1,080 flagged items are defective, despite catching 90% of all defects.</p>
  <details className="stats-extra"><summary>The idea in one line</summary><p>P(A | B) = P(A and B) / P(B), provided P(B) is positive. Keep only cases in B; among those, count the ones also in A. Reversing A and B usually changes the question and the answer.</p></details>
  <Question id="conditional-transfer" prompt="A spam filter catches 90% of spam. Does that mean 90% of flagged messages are spam?" choices={[
   {label:'Yes; those are the same percentage.',correct:false,feedback:'The first percentage counts within spam messages. The second counts within flagged messages, which can include legitimate mail.'},
   {label:'No; we also need the spam rate and the rate of flagging legitimate messages.',correct:true,feedback:'Those quantities determine how many true and false warnings appear in the flagged group.'}
  ]} explanation="Conditioning restricts the comparison group. P(flag | spam) and P(spam | flag) use different denominators." />
 </section>;
}
