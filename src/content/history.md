# History

The ideas on this site didn't start in 2020. They're the convergence of five lineages that developed independently for decades and are now discovering they were building the same thing.

---

## The five threads

### 1. Program correctness (1936 → Staton 2025)

**[Alonzo Church](https://en.wikipedia.org/wiki/Alonzo_Church)** (1936) invented the [lambda calculus](https://en.wikipedia.org/wiki/Lambda_calculus) — a formal system where everything is a function. `lambda x: x + 1` is Church's notation, literally. Every programming language descends from this. Church proved some things are uncomputable before Turing did, using pure math instead of machines.

**[Alan Turing](https://en.wikipedia.org/wiki/Alan_Turing)** (1936) independently proved the same thing with a different model — a machine reading symbols on a tape. Church's lambda calculus and Turing's machine turned out to compute exactly the same things ([Church-Turing thesis](https://en.wikipedia.org/wiki/Church%E2%80%93Turing_thesis)). One lineage became functional programming. The other became the physical computer — from [punch cards](https://en.wikipedia.org/wiki/Punched_card) to CPUs. Both are still with us.

Turing (1949) also wrote the first proof that a program was correct — a hand-checked argument about a factorial routine. Nobody followed up for 18 years.

**[Robert Floyd](https://en.wikipedia.org/wiki/Robert_W._Floyd)** (1967) attached assertions to flowchart edges. If the assertion holds before a step and after a step, the step is correct. First systematic method.

**[Tony Hoare](https://en.wikipedia.org/wiki/Tony_Hoare)** (1969) formalized Floyd's idea into `{P} c {Q}` — the [Hoare triple](https://en.wikipedia.org/wiki/Hoare_logic). Precondition, command, postcondition. The notation every CS student learns. Hoare later said his biggest contribution was the `null` pointer, which he called his "billion-dollar mistake."

**[Edsger Dijkstra](https://en.wikipedia.org/wiki/Edsger_W._Dijkstra)** (1975) flipped the question: instead of "does this precondition work?", ask "what's the weakest precondition that guarantees this postcondition?" His [guarded command language](https://en.wikipedia.org/wiki/Guarded_Command_Language) is the internal language in Staton's paper.

**[Bonchi, Di Lavore, Román, Staton](https://arxiv.org/abs/2507.18238)** (2025) proved that Hoare's rules aren't axioms — they're theorems of categorical structure. Any category with the right properties (traced, distributive, copy-discard) gets every Hoare rule for free. [🍞 read](/notation/staton-2025/)

### 2. Category theory (1945 → Fritz 2020)

**[Samuel Eilenberg](https://en.wikipedia.org/wiki/Samuel_Eilenberg)** and **[Saunders Mac Lane](https://en.wikipedia.org/wiki/Saunders_Mac_Lane)** (1945) invented [category theory](https://en.wikipedia.org/wiki/Category_theory) to formalize natural transformations in algebraic topology. It was "abstract nonsense" for decades — a language for talking about mathematical structure.

**[F. William Lawvere](https://en.wikipedia.org/wiki/William_Lawvere)** (1963) realized categories could describe logic and computation, not just algebra. His thesis connected categories to universal algebra.

**[Eugenio Moggi](https://en.wikipedia.org/wiki/Eugenio_Moggi)** (1991) used [monads](https://en.wikipedia.org/wiki/Monad_(functional_programming)) to model side effects in programming languages. A monad wraps a computation that might do something extra — randomness, failure, state. This is why Haskell has monads.

**[Haskell Curry](https://en.wikipedia.org/wiki/Haskell_Curry)** (1934–1958) discovered the [Curry-Howard correspondence](https://en.wikipedia.org/wiki/Curry%E2%80%93Howard_correspondence): proofs are programs, propositions are types. A logical statement IS a type signature. A proof IS a program that inhabits that type. This is why Lean works.

**[Tobias Fritz](https://arxiv.org/abs/1908.07021)** (2020) built [Markov categories](https://en.wikipedia.org/wiki/Markov_category) — category theory for probability. Stochastic functions form a category. Deterministic functions are the ones that commute with copy. This is the world the pipeline lives in. [🍞 read](/notation/fritz-2020/)

### 3. Information theory (1948 → Baez, Fritz, Leinster 2011)

**[Claude Shannon](https://en.wikipedia.org/wiki/Claude_Shannon)** (1948) invented [information theory](https://en.wikipedia.org/wiki/Information_theory). [Entropy](https://en.wikipedia.org/wiki/Entropy_(information_theory)) measures surprise. A coin flip is 1 bit. A loaded coin is less. Communication is compression.

**[Andrey Kolmogorov](https://en.wikipedia.org/wiki/Andrey_Kolmogorov)** (1933) axiomatized [probability](https://en.wikipedia.org/wiki/Probability_axioms). Shannon built on this foundation. Every probability distribution is a measure. Every stochastic function preserves the measure structure.

**[Rolf Landauer](https://en.wikipedia.org/wiki/Rolf_Landauer)** (1961) proved that [erasing a bit costs energy](https://en.wikipedia.org/wiki/Landauer%27s_principle) — at least kT ln 2 of heat. Information is physical. Computation has thermodynamic costs. This is why the pipeline's Consolidate step is lossy: compression costs entropy.

**[John Baez](https://en.wikipedia.org/wiki/John_C._Baez), Fritz, [Tom Leinster](https://en.wikipedia.org/wiki/Tom_Leinster)** (2011) proved Shannon entropy is the *unique* functorial information loss measure. There's only one way to measure information loss that respects composition. [🍞 read](/notation/baez-fritz-2011/)

### 4. Game theory (1928 → Hedges 2018)

**[John von Neumann](https://en.wikipedia.org/wiki/John_von_Neumann)** (1928) proved the [minimax theorem](https://en.wikipedia.org/wiki/Minimax_theorem). Two-player zero-sum games have optimal strategies.

**[John Nash](https://en.wikipedia.org/wiki/John_Forbes_Nash_Jr.)** (1950) generalized to [Nash equilibrium](https://en.wikipedia.org/wiki/Nash_equilibrium) — every finite game has a mixed-strategy equilibrium. But Nash's equilibrium is a *global* property. You check it by looking at the whole game at once.

**[Jules Hedges](https://arxiv.org/abs/1603.04641), [Neil Ghani](https://en.wikipedia.org/wiki/Neil_Ghani)** (2018) made equilibrium *compositional*. Check it locally on subgames. Compose subgames. Equilibrium propagates through composition — the same way contracts propagate through Hoare's COMP rule. Same structure, different category. [🍞 read](/notation/hedges-2018/)

### 5. Cybernetics (1948 → Capucci 2021)

**[Norbert Wiener](https://en.wikipedia.org/wiki/Norbert_Wiener)** (1948) named [cybernetics](https://en.wikipedia.org/wiki/Cybernetics) — the study of feedback loops in machines and organisms. Control, communication, goal-directed behavior.

**[W. Ross Ashby](https://en.wikipedia.org/wiki/W._Ross_Ashby)** (1956) formalized the [law of requisite variety](https://en.wikipedia.org/wiki/Variety_(cybernetics)#Law_of_requisite_variety): a controller must have at least as many states as the system it controls. This is why Filter and Attend need different strategies — one reduces variety, the other preserves it.

**[Matteo Capucci](https://arxiv.org/abs/2105.06332)** (2021) rebuilt cybernetics in category theory. Goals are predicates on systems. Optimization is composition. "What is a goal but a predicate on a system?" — that's a contract in the pipeline's language. [🍞 read](/notation/capucci-2021/)

---

## The convergence

All five threads arrive at the same place: **behavioral predicates preserved under composition**.

| Thread | Their word for it | SE word | Pipeline word |
|--------|------------------|---------|---------------|
| Program correctness | Hoare triple | `assert` | Contract |
| Category theory | Morphism property | Interface | Kernel predicate |
| Information theory | Data processing inequality | Lossy pipeline | Non-expansion |
| Game theory | Nash equilibrium | SLA | Compositional predicate |
| Cybernetics | Goal / selection relation | Acceptance test | Contract |

The Natural Framework is what happens when you notice this convergence and machine-check it.

---

## Timeline

| Year | Person | Contribution |
|------|--------|-------------|
| 1928 | von Neumann | Minimax theorem |
| 1933 | Kolmogorov | Probability axioms |
| 1934 | Curry | Curry-Howard (early form) |
| 1936 | Church | Lambda calculus |
| 1936 | Turing | Turing machine, computability |
| 1945 | Eilenberg, Mac Lane | Category theory |
| 1948 | Shannon | Information theory |
| 1948 | Wiener | Cybernetics |
| 1949 | Turing | First correctness proof |
| 1950 | Nash | Nash equilibrium |
| 1956 | Ashby | Law of requisite variety |
| 1961 | Landauer | Erasure costs energy |
| 1963 | Lawvere | Categories for logic |
| 1967 | Floyd | Flowchart assertions |
| 1969 | Hoare | `{P} c {Q}` |
| 1975 | Dijkstra | Weakest precondition, guarded commands |
| 1991 | Moggi | Monads for computation |
| 2011 | Baez, Fritz, Leinster | Entropy is functorial |
| 2018 | Hedges, Ghani | Compositional game theory |
| 2020 | Fritz | Markov categories |
| 2021 | Capucci | Categorical cybernetics |
| 2021 | Fritz, Perrone, Rezagholi | Support as monad morphism |
| 2025 | Bonchi, Di Lavore, Román, Staton | Hoare rules as theorems |
| 2025 | Liell-Cock, Staton | Graded monads = Markov categories |
| 2026 | Kura, Gaboardi | Indexed graded monads |
| 2026 | Kim | The crosswalk (this project) |

Every row is a breadcrumb. Every link is a Wikipedia article or an arXiv paper. The ideas are old. The connections are new.
