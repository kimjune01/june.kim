import { describe, it, expect } from 'vitest';
import { numberHeadings } from './remark-section-numbers.mjs';

const H = (depth, opts = {}) => ({ depth, unnumbered: false, appendix: false, ...opts });

describe('numberHeadings', () => {
  it('numbers body h2/h3 and resets sub-counter per section', () => {
    expect(numberHeadings([
      H(2), H(3), H(3), H(2), H(3),
    ])).toEqual(['1.', '1.1', '1.2', '2.', '2.1']);
  });

  it('skips unnumbered headings without advancing the counter', () => {
    expect(numberHeadings([
      H(2, { unnumbered: true }), // Abstract
      H(2),                       // 1.
      H(2),                       // 2.
      H(2, { unnumbered: true }), // Acknowledgments
    ])).toEqual(['', '1.', '2.', '']);
  });

  it('switches to lettered appendices and sub-numbers them', () => {
    expect(numberHeadings([
      H(2), H(2),                          // 1., 2.
      H(2, { appendix: true }), H(3), H(3),// Appendix A., A.1, A.2
      H(2, { appendix: true }), H(3),      // Appendix B., B.1
    ])).toEqual(['1.', '2.', 'Appendix A.', 'A.1', 'A.2', 'Appendix B.', 'B.1']);
  });

  it('mirrors the methodeutic paper shape (abstract, 10 numbered, 2 appendices)', () => {
    const seq = [
      H(2, { unnumbered: true }),               // Abstract
      H(2), H(2), H(2),                         // 1,2,3 Intro/Grounding/Method
      H(3), H(3),                               // 3.1, 3.2
      H(2),                                     // 4
      H(2, { unnumbered: true }),               // LLM disclosure (trailing, before appendices)
      H(2, { appendix: true }), H(3),           // Appendix A, A.1
      H(2, { appendix: true }), H(3),           // Appendix B, B.1
    ];
    expect(numberHeadings(seq)).toEqual([
      '', '1.', '2.', '3.', '3.1', '3.2', '4.', '', 'Appendix A.', 'A.1', 'Appendix B.', 'B.1',
    ]);
  });
});
