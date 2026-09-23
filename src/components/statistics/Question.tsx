import React, { useState } from 'react';

interface Choice { label: string; feedback: string; correct: boolean }
interface Props { id: string; prompt: string; choices: Choice[]; explanation: string }

export default function Question({ id, prompt, choices, explanation }: Props) {
  const [selected, setSelected] = useState<number | null>(null);
  const [reviewed, setReviewed] = useState<number[]>([]);
  const [showExplanation, setShowExplanation] = useState(false);
  return <section className="stats-check" aria-label="A moment to think">
    <p className="stats-eyebrow">A moment to think</p>
    <fieldset>
      <legend>{prompt}</legend>
      <div className="stats-choices">
        {choices.map((choice, i) => <label key={i} className={selected === i ? 'is-selected' : ''}>
          <input type="radio" name={id} value={i} checked={selected === i} onChange={() => setSelected(i)} />
          <span>{choice.label}</span>
        </label>)}
      </div>
    </fieldset>
    <div className="stats-actions">
      <button type="button" disabled={selected === null} onClick={() => {
        if (selected !== null && !reviewed.includes(selected)) setReviewed([...reviewed, selected]);
      }}>Check answer</button>
      <button type="button" className="stats-quiet" onClick={() => setShowExplanation(true)}>See explanation</button>
    </div>
    <div aria-live="polite" aria-atomic="true">
      {reviewed.map(i => <p className="stats-feedback" key={i}>
        <strong>{choices[i].correct ? 'Yes. ' : 'Let’s look at that. '}</strong>{choices[i].feedback}
      </p>)}
      {showExplanation && <p className="stats-feedback">{explanation}</p>}
    </div>
  </section>;
}
