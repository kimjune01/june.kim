---
variant: post-wide
title: "Four schools of programming"
tags: coding
---

There are four schools of programming.

| School | Unit of composition | Exemplar | Irreducible because |
|---|---|---|---|
| Imperative | Statement | C | The world is mutable; you can't perceive your way out of pressing a button |
| Functional | Expression | Haskell | Same input, same output; inference must be referentially transparent |
| Declarative | Relation, constraint | Prolog, SQL | Goals describe what, not how |
| Actors | Process, message | Erlang | Identity, parallel cognition, no shared state |

OOP is not one of the four. It is complexity management you can layer on any of them: OO in C with structs and function pointers, in Haskell with records of closures, in Erlang with named processes. Mainstream OOP (Java, C++) is procedural code with namespacing and dispatch. [Smalltalk](https://en.wikipedia.org/wiki/Smalltalk)'s actual intent (isolated entities, message passing, no shared state) was reborn as actors.

## Same program, four worldviews

The same toy program (Alice transfers 100 to Bob) looks like four different things depending on which school you stand in. Each picture is a claim about what a program *is*.

<div style="max-width:720px;margin:1.5em auto;">
<img src="/assets/four-schools-imperative.svg" alt="Imperative paradigm: Alice and Bob's balances shown at t=0 and t=1, with mutation arrows labeled -=100 and +=100 between them. Code shows alice.balance -= 100 and bob.balance += 100." style="width:100%; display:block;">
</div>

<div style="max-width:720px;margin:1.5em auto;">
<img src="/assets/four-schools-functional.svg" alt="Functional paradigm: an input value record {Alice: 500, Bob: 200} flows through a transfer function and produces a separate output value record {Alice: 400, Bob: 300}. Both values coexist; nothing was mutated." style="width:100%; display:block;">
</div>

<div style="max-width:720px;margin:1.5em auto;">
<img src="/assets/four-schools-declarative.svg" alt="Declarative paradigm: A.bal, Amt, B.bal as entity boxes connected to A_new and B_new by constraint nodes labeled greater-than-or-equal, minus, and plus. No flow direction; the relations simply must hold." style="width:100%; display:block;">
</div>

<div style="max-width:720px;margin:1.5em auto;">
<img src="/assets/four-schools-actors.svg" alt="Actors paradigm: a caller sends a transfer message to Alice's mailbox; Alice processes it, decrements her local balance from 500 to 400, then sends a credit message to Bob's mailbox; Bob processes and increments his balance from 200 to 300. No shared memory between actors." style="width:100%; display:block;">
</div>

Imperative says a program is a sequence of state changes. Functional says it is a transformation between values. Declarative says it is a constraint network. Actors say it is a conversation between isolated entities.

## The category-theoretic spine

Each paradigm has an algebraic structure underneath. Programming-language theory and category theory converge on the same definitions from different directions ([natural breadcrumbs](/reading/natural-breadcrumbs/) maps the translation in detail).

| Paradigm | Categorical structure |
|---|---|
| Imperative | Kleisli over an effect monad |
| Functional | Morphisms in a Cartesian closed category |
| Declarative | Predicates in a fibration over the base |
| Actors | Coalgebras for a behavior functor |

The same algebra dictates the bridges between paradigms.

| Pair | Bridge |
|---|---|
| Imp + Func | Kleisli composition (monads, graded monads) |
| Imp + Dec | Hoare logic = predicate fibration over Kleisli |
| Imp + Actors | Coalgebras in Kleisli (effectful processes) |
| Func + Dec | Dependent types, fibrations over CCCs |
| Func + Actors | Final coalgebras, FRP signals |
| Dec + Actors | Bisimulation logic, behavior specs over coalgebras |

## What mainstream CS teaches

Undergraduate CS curricula teach one paradigm and call the other three electives.

| Paradigm | Required core course | What gets called the "real" thing |
|---|---|---|
| Imperative | DS&A, OS, networks, compilers | Yes — the canonical CS sequence |
| Functional | One semester (sometimes SICP, often skipped) | Elective |
| Declarative | One week of Prolog in an AI elective | Specialty |
| Actors | One lecture in distributed systems | Advanced topic |

The graduate is fluent in arrays, hash tables, and big-O over a single sequential machine. The other three paradigms get bolted on later as if peripheral to "real" programming. Three of the four legs of the table sit outside the core.

## Each paradigm breaks somewhere

| Paradigm | Breaks at | Patched by |
|---|---|---|
| Functional | I/O and identity | Actors (Erlang) or monads (Haskell) |
| Imperative | Concurrency safety | Functional types (Rust borrow checker) |
| Declarative | Performance and dynamism | Imperative escape hatches (PL/pgSQL, useEffect) |
| Actors | Large-grain orchestration | Declarative workflows (Temporal, BPMN) |

Each paradigm gets patched by the complementary paradigm exactly at the seam it cannot reach on its own.

## Six pairs

Four paradigms, choose two — six pairs. Each synthesis has its own history, canonical languages, and open frontier.

| Pair | Mature | Frontier |
|---|---|---|
| Imperative + Functional | Monads, Rust borrow checker, monad transformers | Algebraic effects (Koka, OCaml 5, Eff) replacing transformers; effect inference catching up with type inference |
| Imperative + Declarative | Hoare logic, separation logic, Liquid Haskell, F*, Dafny | LLM-assisted proof; the cost of writing a spec is collapsing, which changes which projects are economical to verify |
| Imperative + Actors | Erlang, Akka, Go's CSP-lite, Pony's no-data-race actors | Durable execution (Temporal, Restate, Dapr); actors absorbing the database |
| Functional + Declarative | Datalog, Mercury, Idris, Agda, Lean | Egraphs (egg, eqlog), differentiable Datalog, neuro-symbolic |
| Functional + Actors | Erlang, Elixir, Akka Typed | Unison: content-addressed pure functions distributed across actors; pure-vs-stateful becomes a deployment concern, not a language concern |
| Declarative + Actors | Session types, choreographies, behavior trees, BPMN | Multi-agent LLM orchestration. *Almost nothing is settled.* |

The least-explored pair is the one multi-agent systems are about to live in.

## Triples and the missing quadruple

Four artifacts touch three paradigms each.

| Artifact | Three of four |
|---|---|
| Behavior trees | Declarative + Imperative + Actors |
| Algebraic effects | Functional + Imperative + Declarative-via-types |
| Erlang OTP | Functional + Imperative + Actors |
| React + Hooks | Declarative + Functional + Imperative |

Nothing canonically touches all four. That four-way intersection is what a cognitive architecture is.

| Paradigm | Aspect of mind |
|---|---|
| Imperative | Embodiment, action |
| Functional | Inference, perception |
| Declarative | Knowledge, goals |
| Actors | Identity, parallel cognition |

[Soar](https://en.wikipedia.org/wiki/Soar_(cognitive_architecture)) and [ACT-R](https://en.wikipedia.org/wiki/ACT-R) wire all four together: production rules (declarative), motor output (imperative), activation and utility math (functional), modular buffers running in parallel (actor-ish). Modern LLM agent stacks land in the same place: LLM call (functional), tool use (imperative), system prompt and memory (declarative), multi-agent orchestration (actors). There is no Smalltalk or Erlang for the four-way synthesis. The slot is open.

## Lineage

<div style="max-width:720px;margin:1em auto;">
<img src="/assets/four-schools-lineage.svg" alt="Vertical diagram showing the lineage of each of the four programming paradigms (imperative, functional, declarative, actors), the language exemplars of each pairwise synthesis, and the languages associated with the four-way intersection (cognitive architectures)." style="width:100%; display:block;">
</div>

## What if

Four schools, six bridges, one missing quad. Each pair has a decade of work in it; the quad has a generation.

- What if effect handling and resource ownership shared one type system?
- What if LLM-aided spec and proof collapsed the cost of formal verification by orders of magnitude?
- What if actors became independent of process, machine, and time?
- What if multi-agent orchestration had its own language, instead of YAML over a function call?
- What does the canonical four-way synthesis — the language for cognitive architectures — look like?
