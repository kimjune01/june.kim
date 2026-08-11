import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';

const paperPath = new URL('./content/blog/2026-08-11-local-replay-auditability.md', import.meta.url);
const paper = readFileSync(paperPath, 'utf8');

describe('local replay mechanism paper', () => {
  it('states the approach and concrete existence result in the abstract', () => {
    const abstract = paper.match(/## Abstract\n\n([\s\S]*?)\n\n## /)?.[1] ?? '';

    expect(abstract).toContain('This paper introduces **local replay auditability**');
    expect(abstract).toContain('all eight committed probes');
    expect(abstract).toContain('existence witness');
  });

  it('separates the mechanism claim from an efficacy estimate', () => {
    expect(paper).toContain('This is a mechanism paper, not an efficacy study.');
    expect(paper).toContain('does not estimate how often local replay improves agent performance');
  });

  it('discloses the broader null results and companion evaluation', () => {
    expect(paper).toContain('Most interventions in the broader evaluation were null');
    expect(paper).toContain('companion Hypothesis Graph paper');
  });
});
