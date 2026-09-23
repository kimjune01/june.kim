import React, { useState } from 'react';

const symbols = {
  probability: [
    { symbol: 'P', meaning: 'Read P as “the probability of.” It asks for a chance, expressed as a number from 0 to 1.', example: 'A quarter of the spinner is blue → the chance of blue is 0.25.' },
    { symbol: '(A)', meaning: 'A names the event we care about. Here, A means “the spinner lands on blue.” The parentheses tell us which event P refers to.', example: 'A = landing on blue. Another event could be landing on amber.' },
    { symbol: 'p', meaning: 'Little p is the probability assigned by our model. It belongs to the spinner’s rule, even when the observed results wander away from it.', example: 'p = 0.25 means 25%, or one chance in four. It does not promise one blue in every four spins.' },
  ],
  proportion: [
    { symbol: 'p̂', meaning: 'Read this as “p-hat.” It is the observed proportion of heads. The little hat marks an estimate of the coin’s probability, made from data.', example: 'Three heads in five flips gives p-hat = 0.6. The true probability can still be 0.5.' },
    { symbol: 'X', meaning: 'X is the number of heads in one round. Before we flip, we do not know which count we will get. That makes X a random variable.', example: 'H · T · H · H · T → X = 3 heads.' },
    { symbol: 'n', meaning: 'n is the number of coins in one round. It is the setting you chose, not the number of rounds recorded in the histogram.', example: 'H · T · H · H · T → n = 5 coins. So X / n = 3 / 5 = 0.6.' },
  ],
};

export default function SymbolSummary({ kind }: { kind: keyof typeof symbols }) {
  const [active, setActive] = useState(0);
  const parts = symbols[kind];
  const button = (i: number) => <button type="button" className="stats-symbol" aria-pressed={active === i} onClick={() => setActive(i)}>{parts[i].symbol}</button>;
  return <section className="stats-symbol-summary bg-zinc-800 rounded-lg p-5 mb-8 callout" aria-label="You can now write this">
    <p className="stats-eyebrow">You can now write this</p>
    <div className="stats-equation" aria-label={kind === 'probability' ? 'P of A equals p' : 'p-hat equals X divided by n'}>
      {kind === 'probability' ? <>{button(0)}{button(1)}<span>=</span>{button(2)}</> : <>{button(0)}<span>=</span><span className="stats-fraction">{button(1)}{button(2)}</span></>}
    </div>
    <p className="stats-small">Choose a piece to read it in words.</p>
    <div className="stats-symbol-reading" aria-live="polite" aria-atomic="true">
      <p>{parts[active].meaning}</p>
      <p className="stats-worked-example">{parts[active].example}</p>
    </div>
    <a href={kind === 'probability' ? '#spinner' : '#coin-experiment'}>Find it in your experiment ↑</a>
  </section>;
}
