import { describe, expect, it } from 'vitest';
import { mean, median, populationSD, sampleWithoutReplacement, sampleMeans, populations, town, confidenceIntervals, normalInterval, fairCoinTail, nullCounts, randomizedGroups } from './inference';

describe('data and sampling', () => {
  it('distinguishes center from sensitivity to extreme values', () => {
    expect(mean([40, 50, 60, 70, 80])).toBe(60);
    expect(median([80, 40, 70, 50, 60])).toBe(60);
    expect(median([40, 50, 60, 70, 80, 1000])).toBe(65);
    expect(mean([40, 50, 60, 70, 80, 1000])).toBeCloseTo(216.6667);
    expect(populationSD([60, 60, 60])).toBe(0);
  });
  it('draws without replacement, does not mutate the population, and can take a census', () => {
    const people = [1, 2, 3, 4, 5];
    expect(sampleWithoutReplacement(people, 3, () => 0)).toEqual([1, 2, 3]);
    expect(new Set(sampleWithoutReplacement(people, 5)).size).toBe(5);
    expect(people).toEqual([1, 2, 3, 4, 5]);
    expect(() => sampleWithoutReplacement(people, 6)).toThrow();
  });
  it('makes selection bias visible even in a census of the selected subgroup', () => {
    const court = town.filter(p => p.court);
    expect(court.length).toBe(40);
    expect(mean(court.map(p => p.height))).toBeGreaterThan(mean(town.map(p => p.height)) + 10);
  });
  it('randomly partitions subjects exactly once, without changing their potential outcomes', () => {
    const groups = randomizedGroups(town.slice(0, 10), () => 0);
    expect(groups.treatment.length).toBe(5);
    expect(groups.control.length).toBe(5);
    expect(new Set([...groups.treatment, ...groups.control].map(p => p.id)).size).toBe(10);
  });
});

describe('sampling distributions and intervals', () => {
  it('averages independent draws with replacement and records one mean per sample', () => {
    const draws = [0, .9, 0, .9, .9, .9];
    expect(sampleMeans([0, 10], 2, 3, () => draws.shift()!)).toEqual([5, 5, 10]);
    expect(sampleMeans([7], 100, 3)).toEqual([7, 7, 7]);
    expect(populations.skewed.length).toBeGreaterThan(20);
  });
  it('scales the known-sigma interval with confidence and square root of sample size', () => {
    const small = normalInterval(170, 4, 95);
    const large = normalInterval(170, 16, 95);
    expect(small.high - small.mean).toBeCloseTo(2 * (large.high - large.mean));
    expect(normalInterval(170, 4, 99).high).toBeGreaterThan(small.high);
    expect(normalInterval(200, 4, 95).covers).toBe(false);
    expect(small.covers).toBe(true);
  });
  it('generates reproducible intervals and bounds interactive work', () => {
    const intervals = confidenceIntervals(5, 95, 3, () => 0);
    expect(intervals).toHaveLength(3);
    expect(intervals.every(i => i.mean === 170 && i.covers)).toBe(true);
    expect(() => sampleMeans([1, 2], 0, 3)).toThrow();
    expect(() => confidenceIntervals(10, 95, 1001)).toThrow();
  });
});

describe('a prespecified one-sided fair-coin test', () => {
  it('counts equality in the tail and computes exact fair-coin probabilities', () => {
    expect(fairCoinTail(2, 0)).toBe(1);
    expect(fairCoinTail(2, 1)).toBe(.75);
    expect(fairCoinTail(2, 2)).toBe(.25);
    expect(fairCoinTail(20, 15)).toBeCloseTo(.0206947);
  });
  it('simulates the null rather than the observed proportion', () => {
    expect(nullCounts(4, 3, () => .49)).toEqual([4, 4, 4]);
    expect(nullCounts(4, 3, () => .51)).toEqual([0, 0, 0]);
  });
});
