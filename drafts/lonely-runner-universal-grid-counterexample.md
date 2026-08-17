# A universal-grid conjecture fails by letting the tuple follow the grid

Status: research note, 2026-08-16. This is a counterexample to Conjecture 7.1 of Sungkawichai and Trakulthongchai's 2026 preprint as written, not a counterexample to the Lonely Runner Conjecture.

The conjecture proposes that for each fixed number of runners there is a universal denominator threshold: beyond it, every coprime non-tight speed tuple has a witness on every rational grid.

The quantifiers allow the tuple to depend on the grid. That kills the statement.

For any integer $r\ge1$, take

\[
d=6r+1,\qquad (v_1,v_2)=(1,3r).
\]

This is already a three-runner example. Moreover,

\[
\gcd(d,v_1v_2)=\gcd(6r+1,3r)=1,
\]

so excluding speeds that share factors with the denominator does not save the conjecture.

The tuple is non-tight. When $3r$ is odd, time $1/2$ puts both runners at distance $1/2$. When $3r=2a$, time

\[
t=\frac{a}{2a+1}
\]

puts both at distance $a/(2a+1)>1/3$.

But no time $j/d$ is a witness. Outside the middle third of the grid, speed $1$ is too close to an integer. Inside the middle third, write $j=2s$ or $j=2s+1$. Since $6r\equiv-1\pmod d$,

\[
3r(2s)\equiv-s\pmod d,
\qquad
3r(2s+1)\equiv3r-s\pmod d.
\]

In both cases the second runner's distance is at most

\[
\frac{2r}{6r+1}<\frac13.
\]

Thus every grid point fails, for an unbounded sequence of denominators.

The broader lesson is about multiscale proofs. Compatible residues across prime-power grids can converge to a profinite integer that is not one fixed positive integer speed. A lift tree that quantifies over every compatible modular branch is therefore too strong. It must retain an Archimedean height condition or another invariant of fixed-integer realizability.

The exact family, the first 100 rational replays, and the hypothesis-graph node are recorded in `/Users/junekim/Documents/lonely-runner`.

Reference: Touch Sungkawichai and Tanupat Trakulthongchai, [*Eleven, twelve, and thirteen lonely runners*](https://arxiv.org/abs/2604.23906), Conjecture 7.1.
