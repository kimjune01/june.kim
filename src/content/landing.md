# 🍞 Natural Breadcrumbs

You're a programmer. You can read code. You can't read this:

> *The Kleisli category of the subdistribution monad on a distributive copy-discard category is a posetal imperative category.*

But you *can* read this:

```python
# Stochastic functions compose. Assertions chain through composition.
# That's it. That's the sentence above.

def f(x):
    return {x*2: 0.7, x+1: 0.3}  # 70% double, 30% increment

def g(y):
    return {y-1: 1.0}             # always decrement

# Compose them
def compose(f, g):
    result = {}
    for y, py in f(3).items():
        for z, pz in g(y).items():
            result[z] = result.get(z, 0) + py * pz
    return result

print(compose(f, g))  # {5: 0.7, 3: 0.3}
```

Same idea. Different notation. This site translates one into the other.

---

## What is this

An interactive companion to a [research project](https://june.kim/framework-lexicon) that connects several academic communities working on the same problem with different vocabulary.

The project has three parts:
- A [Lean 4 proof](https://github.com/kimjune01/natural-framework) that machine-checks the connections (for the skeptics)
- A [vocabulary table](https://june.kim/framework-lexicon) that maps terms across communities (for the researchers)
- **This site** — the same ideas, in code you can run (for everyone else)

## How to use it

**If you want to look something up** → use the [symbol grid](/notation/). Click any symbol, see what it means in code, run the example.

**If you want to understand a specific paper** → pick one from the list below. Each page explains the paper's key idea in plain language and runnable Python, then links to the real paper when you're ready.

**If you want the big picture** → the [cognition series](https://june.kim/cognition) explains why this pipeline exists and what it models. Start with [The Natural Framework](https://june.kim/the-natural-framework) for the overview, [The Handshake](https://june.kim/the-handshake) for why the stages compose.

## The papers

Each paper has a 🍞 page that translates its key ideas into code.

| Paper | One sentence | 🍞 |
|-------|-------------|-----|
| Staton 2025 | Every Hoare rule (`assert/run/assert`) is a theorem, not an axiom, in stochastic systems | [read](/notation/staton-2025/) |
| Fritz 2020 | Stochastic functions form a category with copy and discard — that's the world the pipeline lives in | [read](/notation/fritz-2020/) |
| Fritz, Perrone, Rezagholi 2021 | "Which outputs are possible?" is a monad morphism — collapse probabilities to yes/no | [read](/notation/fritz-perrone-2021/) |
| Gaboardi 2021 | Hoare logic with grades — track side effects through composition | [read](/notation/gaboardi-2021/) |
| Kura 2026 | Stage N's guarantee becomes stage N+1's assumption — that's a graded monad | [read](/notation/kura-2026/) |
| Hedges, Ghani 2018 | Nash equilibrium composes the same way contracts compose | [read](/notation/hedges-2018/) |
| Capucci 2021 | "What is a goal but a predicate on a system?" — optimization as composition | [read](/notation/capucci-2021/) |
| Baez, Fritz, Leinster 2011 | Shannon entropy is the only information loss measure that respects composition | [read](/notation/baez-fritz-2011/) |
| Liell-Cock, Staton 2025 | Graded monads and Markov categories are the same structure | [read](/notation/liell-cock-2025/) |
| Sato, Katsumata 2023 | Distance between programs = enrichment on the category | [read](/notation/sato-2023/) |

## Why does this exist

The author submitted a [paper](https://june.kim/framework-lexicon) to a category theory conference and realized that the notation barrier goes both ways — mathematicians can't read his code, and he can't read their papers. So he built the translation layer he wished he'd had.

If you can read Python, you can read category theory. You just need the breadcrumbs.
