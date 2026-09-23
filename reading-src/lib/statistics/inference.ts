import type { RandomSource } from './experiments';

export const mean = (values: number[]) => values.reduce((a, b) => a + b, 0) / values.length;
export function median(values: number[]) {
  const sorted = [...values].sort((a, b) => a - b);
  const middle = Math.floor(sorted.length / 2);
  return sorted.length % 2 ? sorted[middle] : (sorted[middle - 1] + sorted[middle]) / 2;
}
export function populationSD(values: number[]) {
  const center = mean(values);
  return Math.sqrt(mean(values.map(value => (value - center) ** 2)));
}
function boundedSamples(size: number, repeats: number) {
  if (!Number.isInteger(size) || size < 1 || size > 200 || !Number.isInteger(repeats) || repeats < 1 || repeats > 1000)
    throw new RangeError('Use 1–200 observations and 1–1,000 repetitions.');
}
export function sampleWithoutReplacement<T>(population: T[], size: number, random: RandomSource = Math.random): T[] {
  boundedSamples(size, 1);
  if (size > population.length) throw new RangeError('A sample cannot exceed the available population.');
  const shuffled = [...population];
  for (let i = 0; i < size; i++) {
    const j = i + Math.floor(random() * (shuffled.length - i));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled.slice(0, size);
}

// A fictional town; the tall basketball-court subgroup is intentionally selected.
export const town = Array.from({ length: 200 }, (_, id) => ({
  id, height: id < 40 ? 180 + (id * 7 % 21) : 150 + (id * 7 % 31), court: id < 40,
}));
export function randomizedGroups<T>(people: T[], random: RandomSource = Math.random) {
  const shuffled = sampleWithoutReplacement(people, people.length, random);
  const middle = Math.floor(people.length / 2);
  return { treatment: shuffled.slice(0, middle), control: shuffled.slice(middle) };
}
export const populations = {
  uniform: Array.from({ length: 101 }, (_, i) => i),
  skewed: Array.from({ length: 101 }, (_, i) => 100 * (i / 100) ** 4),
  bimodal: Array.from({ length: 100 }, (_, i) => (i < 50 ? 20 : 80) + (i % 11 - 5)),
};
export type PopulationShape = keyof typeof populations;
export function sampleMeans(population: number[], size: number, repeats: number, random: RandomSource = Math.random) {
  boundedSamples(size, repeats);
  if (!population.length) throw new RangeError('Choose a nonempty population.');
  return Array.from({ length: repeats }, () => mean(Array.from({ length: size }, () => population[Math.floor(random() * population.length)])));
}

export const normalModel = { mean: 170, sd: 10 };
export const confidenceZ = { 80: 1.2815515655, 95: 1.9599639845, 99: 2.5758293035 };
export type Confidence = keyof typeof confidenceZ;
export interface Interval { mean: number; low: number; high: number; covers: boolean }
export function normalInterval(center: number, size: number, confidence: Confidence): Interval {
  boundedSamples(size, 1);
  const margin = confidenceZ[confidence] * normalModel.sd / Math.sqrt(size);
  return { mean: center, low: center - margin, high: center + margin, covers: Math.abs(center - normalModel.mean) <= margin };
}
export function confidenceIntervals(size: number, confidence: Confidence, repeats: number, random: RandomSource = Math.random) {
  boundedSamples(size, repeats);
  return Array.from({ length: repeats }, () => {
    const values = Array.from({ length: size }, () => {
      const z = Math.sqrt(-2 * Math.log(1 - random())) * Math.cos(2 * Math.PI * random());
      return normalModel.mean + normalModel.sd * z;
    });
    return normalInterval(mean(values), size, confidence);
  });
}

export function nullCounts(coins: number, repeats: number, random: RandomSource = Math.random) {
  boundedSamples(coins, repeats);
  return Array.from({ length: repeats }, () => Array.from({ length: coins }, () => Number(random() < .5)).reduce((a, b) => a + b, 0));
}
/** P(X >= observed) for X ~ Binomial(coins, 1/2): a prespecified upper-tail test. */
export function fairCoinTail(coins: number, observed: number) {
  boundedSamples(coins, 1);
  if (!Number.isInteger(observed) || observed < 0 || observed > coins) throw new RangeError('Head count is outside the experiment.');
  let probability = 2 ** -coins, tail = 0;
  for (let heads = 0; heads <= coins; heads++) {
    if (heads >= observed) tail += probability;
    probability *= (coins - heads) / (heads + 1);
  }
  return Math.min(1, tail);
}
