import { describe, expect, it } from 'vitest';
import { coinRounds, spinBatch, addRounds, emptyRounds } from './experiments';

describe('independent trials', () => {
  it('uses the chosen probability and retains the actual spinner position', () => {
    const draws = [0, 0.24, 0.25, 0.99];
    const result = spinBatch(0.25, 4, () => draws.shift()!);
    expect(result.blue).toBe(2);
    expect(result.outcomes).toEqual([true, true, false, false]);
    expect(result.lastPosition).toBe(0.99);
  });
  it('handles impossible and certain events without exceptions', () => {
    expect(spinBatch(0, 10, () => 0).blue).toBe(0);
    expect(spinBatch(1, 10, () => 0.999).blue).toBe(10);
  });
  it('makes one histogram entry per round, not per coin', () => {
    const draws = [0.1, 0.2, 0.8, 0.8, 0.2, 0.8];
    const result = coinRounds(3, 0.5, 2, () => draws.shift()!);
    expect(result.histogram).toEqual([0, 1, 1, 0]);
    expect(result.total).toBe(2);
    expect(result.lastFlips).toEqual([false, true, false]);
  });
  it('accumulates rounds without losing counts and keeps the latest round', () => {
    const first = coinRounds(2, 0.5, 3, () => 0);
    const second = coinRounds(2, 0.5, 2, () => 0.9);
    const combined = addRounds(first, second);
    expect(combined.histogram).toEqual([2, 0, 3]);
    expect(combined.total).toBe(5);
    expect(combined.lastFlips).toEqual([false, false]);
    expect(first.histogram).toEqual([0, 0, 3]);
  });
  it('refuses to pool experiments with different coin counts or probabilities', () => {
    expect(() => addRounds(emptyRounds(2, 0.5), emptyRounds(5, 0.5))).toThrow();
    expect(() => addRounds(emptyRounds(2, 0.5), emptyRounds(2, 0.75))).toThrow();
  });
  it('keeps all impossible/certain coin rounds in the right bin', () => {
    expect(coinRounds(5, 0, 100).histogram).toEqual([100, 0, 0, 0, 0, 0]);
    expect(coinRounds(5, 1, 100).histogram).toEqual([0, 0, 0, 0, 0, 100]);
  });
  it('bounds work and rejects invalid settings', () => {
    expect(() => coinRounds(0, 0.5, 1)).toThrow();
    expect(() => coinRounds(10, 0.5, 1001)).toThrow();
    expect(() => spinBatch(-0.1, 10)).toThrow();
    expect(() => spinBatch(0.5, 1.5)).toThrow();
  });
});
