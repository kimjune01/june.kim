// @vitest-environment jsdom
import React, { act } from 'react';
import { createRoot, type Root } from 'react-dom/client';
import { renderToString } from 'react-dom/server';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import Question from './Question';
import Spinner from './Spinner';
import CoinExperiment from './CoinExperiment';
import SymbolSummary from './SymbolSummary';

let host: HTMLDivElement;
let root: Root;
beforeEach(() => {
  (globalThis as Record<string, unknown>).IS_REACT_ACT_ENVIRONMENT = true;
  host = document.createElement('div');
  document.body.append(host);
  root = createRoot(host);
});
afterEach(() => { act(() => root.unmount()); host.remove(); vi.restoreAllMocks(); });
function render(component: React.ReactNode) { act(() => root.render(component)); }
function click(label: string) {
  const button = [...host.querySelectorAll('button')].find(el => el.textContent?.trim() === label);
  if (!button) throw new Error(`Missing button: ${label}`);
  act(() => button.click());
}
function change(label: string, value: string) {
  const control = host.querySelector(`[aria-label="${label}"]`) as HTMLSelectElement;
  if (!control) throw new Error(`Missing control: ${label}`);
  act(() => { control.value = value; control.dispatchEvent(new Event('change', { bubbles: true })); });
}

describe('explanatory questions', () => {
  const question = <Question id="coin-check" prompt="What happens next?" explanation="Independent flips have the same chance."
    choices={[
      { label: 'Tails is due', feedback: 'Earlier flips do not create a debt.', correct: false },
      { label: 'Still half', feedback: 'Yes. The coin has not changed.', correct: true },
    ]} />;
  it('explains a wrong answer and retains its feedback through a retry', () => {
    render(question);
    act(() => (host.querySelectorAll('input')[0] as HTMLInputElement).click());
    click('Check answer');
    expect(host.textContent).toContain('Earlier flips do not create a debt.');
    act(() => (host.querySelectorAll('input')[1] as HTMLInputElement).click());
    expect(host.textContent).toContain('Earlier flips do not create a debt.');
    click('Check answer');
    expect(host.textContent).toContain('Yes. The coin has not changed.');
  });
  it('offers the explanation without requiring an answer', () => {
    render(question);
    click('See explanation');
    expect(host.textContent).toContain('Independent flips have the same chance.');
    expect(host.querySelector('fieldset')?.disabled).toBe(false);
  });
});

describe('experiments', () => {
  it('renders SVG titles as text on the server for matching hydration', () => {
    const server = document.createElement('div');
    server.innerHTML = renderToString(<CoinExperiment />);
    expect(server.querySelector('svg > title')?.textContent).toBe('Current experiment: distribution of head counts');
    expect(server.querySelector('rect > title')?.textContent).toBe('0 heads (0%): 0 rounds');
  });
  it('keeps model probability separate from observations and resets a changed model', () => {
    vi.spyOn(Math, 'random').mockReturnValue(0.1);
    render(<Spinner />);
    click('Spin 10 times');
    expect(host.textContent).toContain('10 blue out of 10 spins');
    expect(host.textContent).toContain('50%');
    change('Chance of blue', '25');
    expect(host.textContent).toContain('No spins yet');
    click('Spin once');
    expect(host.textContent).toContain('1 blue out of 1 spin');
    click('Start over');
    expect(host.textContent).toContain('No spins yet');
  });
  it('preserves a saved comparison but never pools rounds from changed settings', () => {
    vi.spyOn(Math, 'random').mockReturnValue(0.1);
    render(<CoinExperiment />);
    click('Flip one round');
    expect(host.textContent).toContain('1 round recorded');
    click('Keep for comparison');
    change('Coins per round', '20');
    expect(host.textContent).toContain('0 rounds recorded');
    expect(host.textContent).toContain('Saved: 10 coins');
    click('Flip one round');
    expect(host.textContent).toContain('20 heads out of 20 coins');
    click('Proportion of heads');
    expect(host.textContent).toContain('100%');
    const charts = [...host.querySelectorAll('svg')];
    const rightTick = (chart: SVGSVGElement) => [...chart.querySelectorAll('text')].find(el => el.textContent === '100%' && el.getAttribute('y') === '209')?.getAttribute('x');
    expect(rightTick(charts[0])).toBe(rightTick(charts[1]));
    change('Chance of heads', '0');
    expect(host.textContent).toContain('0 rounds recorded');
    click('Flip one round');
    expect(host.textContent).toContain('0 heads out of 20 coins');
  });
  it('provides text explanations for symbolic pieces without prerequisites', () => {
    render(<SymbolSummary kind="proportion" />);
    click('n');
    expect(host.textContent).toContain('number of coins in one round');
    click('p̂');
    expect(host.textContent).toContain('p-hat');
    expect(host.querySelector('a')?.getAttribute('href')).toBe('#coin-experiment');
  });
});
