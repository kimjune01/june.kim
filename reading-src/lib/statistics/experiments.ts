/** Small, bounded experiments. Supply a random source for reproducible tests. */
export type RandomSource = () => number;

function settings(probability: number, count: number) {
  if (!Number.isFinite(probability) || probability < 0 || probability > 1)
    throw new RangeError('Probability must be between 0 and 1.');
  if (!Number.isInteger(count) || count < 1 || count > 1000)
    throw new RangeError('Run between 1 and 1,000 trials at a time.');
}

export function spinBatch(probability: number, count: number, random: RandomSource = Math.random) {
  settings(probability, count);
  const positions = Array.from({ length: count }, () => random());
  const outcomes = positions.map(position => position < probability);
  return { blue: outcomes.filter(Boolean).length, outcomes, lastPosition: positions[count - 1] };
}

export interface RoundResults {
  coins: number;
  probability: number;
  histogram: number[];
  total: number;
  lastFlips: boolean[];
}

export function emptyRounds(coins: number, probability: number): RoundResults {
  settings(probability, 1);
  if (!Number.isInteger(coins) || coins < 1 || coins > 40)
    throw new RangeError('Choose between 1 and 40 coins per round.');
  return { coins, probability, histogram: Array(coins + 1).fill(0), total: 0, lastFlips: [] };
}

export function coinRounds(coins: number, probability: number, rounds: number, random: RandomSource = Math.random): RoundResults {
  settings(probability, rounds);
  const result = emptyRounds(coins, probability);
  for (let round = 0; round < rounds; round++) {
    result.lastFlips = Array.from({ length: coins }, () => random() < probability);
    result.histogram[result.lastFlips.filter(Boolean).length]++;
  }
  result.total = rounds;
  return result;
}

export function addRounds(previous: RoundResults, next: RoundResults): RoundResults {
  if (previous.coins !== next.coins || previous.probability !== next.probability)
    throw new Error('Start a new experiment when the model changes.');
  return {
    ...next,
    histogram: next.histogram.map((frequency, i) => frequency + previous.histogram[i]),
    total: previous.total + next.total,
  };
}
