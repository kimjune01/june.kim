import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';

const pagePath = new URL('./pages/research/index.astro', import.meta.url);

describe('research page', () => {
  it('presents the research function, evidence, method, and papers', () => {
    const page = readFileSync(pagePath, 'utf8');

    expect(page).toContain('I audit the inference from benchmark result to capability claim.');
    expect(page).toContain('Selected findings');
    expect(page).toContain('Method');
    expect(page).toContain('Research mechanisms');
    expect(page).toContain('Papers');
    expect(page).toContain('/terminal-bench-frame');
    expect(page).toContain('/a-determinacy-audit-of-swebench-pro');
    expect(page).toContain('/auditing-deepswe');
    expect(page).toContain('/local-replay-auditability');
    expect(page).toContain('/what-cannot-be-false-cannot-be-true');
  });
});
