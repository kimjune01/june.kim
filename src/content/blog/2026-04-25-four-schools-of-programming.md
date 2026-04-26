---
variant: post-wide
title: "Four schools of programming"
tags: coding
---

Open any React codebase and you're touching three programming paradigms at once: JSX is declarative, components are functional, useEffect is imperative. The fourth (actors, isolated entities passing messages) is what React doesn't have. Multi-agent LLM frameworks are all scrambling to bolt it on. There are four schools of programming, and most of the interesting work happens at their seams.

<table style="max-width:980px; margin:1em auto; font-size:13px;">
<colgroup><col style="width:7em"><col style="width:9em"><col style="width:6em"><col><col style="width:11em"><col style="width:16em"></colgroup>
<thead><tr><th style="background:#f0f0f0">School</th><th style="background:#f0f0f0">Unit</th><th style="background:#f0f0f0">Exemplar</th><th style="background:#f0f0f0">Irreducible because</th><th style="background:#f0f0f0">Breaks at</th><th style="background:#f0f0f0">Patched by</th></tr></thead>
<tr><td>Imperative</td><td>Statement</td><td>C</td><td>The world is mutable; you can't perceive your way out of pressing a button</td><td>Concurrency safety</td><td>Functional types (Rust borrow checker)</td></tr>
<tr><td>Functional</td><td>Expression</td><td>Haskell</td><td>A function has no inside; replace it with a lookup table and nothing changes</td><td>Side effects</td><td>Monads, then algebraic effects</td></tr>
<tr><td>Declarative</td><td>Relation, constraint</td><td>Prolog, SQL</td><td>Goals describe what, not how</td><td>Performance and dynamism</td><td>Imperative escape hatches (PL/pgSQL, useEffect)</td></tr>
<tr><td>Actors</td><td>Process, message</td><td>Erlang</td><td>Identity, parallel cognition, no shared state</td><td>Large-grain orchestration</td><td>Declarative workflows (Temporal, BPMN)</td></tr>
</table>

Each paradigm's complement patches exactly the seam it can't reach alone.

## Same program, four worldviews

The same toy program (Alice transfers 100 to Bob) becomes four different things, one per school. Each picture is a claim about what a program *is*.

### Imperative: state mutates in time

"Do this, then this." Named locations hold values; instructions overwrite them.

<div style="max-width:720px;margin:1.5em auto 3em;">
<img src="/assets/four-schools-imperative.svg" alt="Imperative paradigm: Alice and Bob's balances shown at t=0 and t=1, with mutation arrows labeled -=100 and +=100 between them. Code shows alice.balance -= 100 and bob.balance += 100." style="width:100%; display:block;">
</div>

<hr>

### Functional: state is a value, function transforms it

No mutation. The old value still exists; a new value is computed from it.

<div style="max-width:720px;margin:1.5em auto 3em;">
<img src="/assets/four-schools-functional.svg" alt="Functional paradigm: an input value record {Alice: 500, Bob: 200} flows through a transfer function and produces a separate output value record {Alice: 400, Bob: 300}. Both values coexist; nothing was mutated." style="width:100%; display:block;">
</div>

<hr>

### Declarative: relations must hold

No order, no time. The solver finds bindings that satisfy every constraint.

<div style="max-width:720px;margin:1.5em auto 3em;">
<img src="/assets/four-schools-declarative.svg" alt="Declarative paradigm: A.bal, Amt, B.bal as entity boxes connected to A_new and B_new by constraint nodes labeled greater-than-or-equal, minus, and plus. No flow direction; the relations simply must hold." style="width:100%; display:block;">
</div>

<hr>

### Actors: isolated state, messages cross

No shared memory. Each actor has a mailbox; the program is a conversation.

<div style="max-width:720px;margin:1.5em auto 3em;">
<img src="/assets/four-schools-actors.svg" alt="Actors paradigm: a caller sends a transfer message to Alice's mailbox; Alice processes it, decrements her local balance from 500 to 400, then sends a credit message to Bob's mailbox; Bob processes and increments his balance from 200 to 300. No shared memory between actors." style="width:100%; display:block;">
</div>

<hr>

Imperative says a program is a sequence of state changes. Functional says it is a transformation between values. Declarative says it is a constraint network. Actors say it is a conversation between isolated entities.

## The category-theoretic spine

Each paradigm has an algebraic structure underneath. Programming-language theory and category theory converge on the same definitions from different directions ([natural breadcrumbs](/reading/natural-breadcrumbs/) maps the translation in detail).

<table style="max-width:700px; margin:1em auto; font-size:13px;">
<colgroup><col style="width:10em"><col style="width:28em"><col style="width:14em"></colgroup>
<thead><tr><th style="background:#f0f0f0">Paradigm / Pair</th><th style="background:#f0f0f0">Categorical structure</th><th style="background:#f0f0f0">Category Theory paper</th></tr></thead>
<tr><td>Imperative</td><td>Kleisli over an effect monad</td><td><a href="https://en.wikipedia.org/wiki/Eugenio_Moggi">Moggi 1989</a></td></tr>
<tr><td>Functional</td><td>Morphisms in a Cartesian closed category</td><td><a href="https://en.wikipedia.org/wiki/Joachim_Lambek">Lambek & Scott 1986</a></td></tr>
<tr><td>Declarative</td><td>Predicates in a fibration over the base</td><td><a href="https://en.wikipedia.org/wiki/Robert_Kowalski">Kowalski 1974</a></td></tr>
<tr><td>Actors</td><td>Coalgebras for a behavior functor</td><td><a href="https://en.wikipedia.org/wiki/F-coalgebra">Rutten 2000</a></td></tr>
<tr><td>Imp + Func</td><td>Kleisli composition (monads, graded monads)</td><td><a href="https://en.wikipedia.org/wiki/Philip_Wadler">Wadler 1992</a></td></tr>
<tr><td>Imp + Dec</td><td>Hoare logic = predicate fibration over Kleisli</td><td><a href="https://en.wikipedia.org/wiki/Hoare_logic">Atkey 2009</a></td></tr>
<tr><td>Imp + Actors</td><td>Coalgebras in Kleisli (effectful processes)</td><td><a href="https://en.wikipedia.org/wiki/Gordon_Plotkin">Plotkin & Power 2001</a></td></tr>
<tr><td>Func + Dec</td><td>Dependent types, fibrations over CCCs</td><td><a href="https://en.wikipedia.org/wiki/Per_Martin-L%C3%B6f">Martin-Löf 1984</a></td></tr>
<tr><td>Func + Actors</td><td>Final coalgebras, FRP signals</td><td><a href="https://en.wikipedia.org/wiki/Paul_Hudak">Elliott & Hudak 1997</a></td></tr>
<tr><td>Dec + Actors</td><td>Bisimulation logic, behavior specs over coalgebras</td><td><a href="https://en.wikipedia.org/wiki/Robin_Milner">Milner 1989</a></td></tr>
</table>

## Six pairs

Four paradigms, choose two: six pairs. Each synthesis has its own history, canonical languages, and open frontier.

<table style="max-width:980px; margin:1em auto; font-size:13px;">
<colgroup><col style="width:11em"><col><col style="width:18em"></colgroup>
<thead><tr><th style="background:#f0f0f0">Pair</th><th style="background:#f0f0f0">Languages</th><th style="background:#f0f0f0">Frontier</th></tr></thead>
<tr>
  <td><span style="color:#1565c0">Imperative</span> + <span style="color:#2e7d32">Functional</span></td>
  <td>1973 ML · 1990 Haskell (IO monad) · 1996 OCaml · 2004 Scala · 2005 F# · 2010 Rust (linear types) · 2011 Kotlin · 2012 Koka · 2014 Swift · 2022 OCaml 5 (effects)</td>
  <td>Algebraic effects replacing monad transformers; effect inference.</td>
</tr>
<tr>
  <td><span style="color:#1565c0">Imperative</span> + <span style="color:#c62828">Declarative</span></td>
  <td>1969 Hoare logic · 1986 Eiffel (DbC) · 2008 Liquid Haskell · 2009 Dafny · 2011 F* · 2021 Lean 4 · 2024 LLM-aided proof (Goedel-Prover, …)</td>
  <td>Cost of writing a spec collapsing; verified projects newly economical.</td>
</tr>
<tr>
  <td><span style="color:#1565c0">Imperative</span> + <span style="color:#ef6c00">Actors</span></td>
  <td>1986 Erlang · 2009 Akka · 2009 Go (CSP-lite) · 2010 Orleans (virtual actors) · 2015 Pony (no data races) · 2019 Temporal · 2023 Restate, Dapr</td>
  <td>Durable execution. Actors absorbing the database.</td>
</tr>
<tr>
  <td><span style="color:#2e7d32">Functional</span> + <span style="color:#c62828">Declarative</span></td>
  <td>1989 Coq · 1995 Mercury · 2007 Agda · 2007 Idris · 2021 Lean 4 (as a language) · 2021 egg / eqlog · Soufflé Datalog · differentiable Datalog (research)</td>
  <td>E-graphs for compilers; neuro-symbolic systems.</td>
</tr>
<tr>
  <td><span style="color:#2e7d32">Functional</span> + <span style="color:#ef6c00">Actors</span></td>
  <td>1986 Erlang · 2011 Elixir · 2017 Akka Typed · 2016 Unison</td>
  <td>Unison-style: content-addressed pure functions distributed across actors. Pure-vs-stateful becomes a deployment concern.</td>
</tr>
<tr>
  <td><span style="color:#c62828">Declarative</span> + <span style="color:#ef6c00">Actors</span></td>
  <td>1993 Honda session types · 2004 BPMN · ~2007 behavior trees (game AI) · 2019 Temporal workflows · 2023+ LangGraph / CrewAI / AutoGen / Inngest agents · multiparty choreographies</td>
  <td>Least settled. Where multi-agent LLM systems are about to live.</td>
</tr>
</table>

The least-explored pair is where multi-agent systems are about to live.

## Lineage of paradigms and their syntheses

Programming-language pointers, oldest at top.

<div style="max-width:460px;margin:1.5em auto;">
<img src="/assets/four-schools-lineage-schools.svg" alt="Long vertical timeline of programming languages from 1936 to 2014, with each entry tagged by a colored dot indicating its paradigm: imperative (blue), functional (green), declarative (red), actors (orange). Synthesis languages have two colored dots. Stars mark foundational works." style="width:100%; display:block;">
</div>

## A language for cognitive architecture

Four schools, six bridges, one missing quad. Each pair has a decade of work behind it; the quad has a generation ahead of it.

The quad is the cognitive-architecture problem cosplaying as a programming language. The closest artifacts (React + Hooks, Erlang OTP, Algebraic effects, Behavior trees) each touch three of the four, but none unifies all. Soar and ACT-R hand-wired all four in the eighties; modern LLM stacks arrive the same way, gluing pure inference (functional) to tool calls (imperative) over a memory store (declarative) under a multi-agent runtime (actors). Each generation invents its own DSL (production rules, chunks, graph specs, role contracts), and the same primitives recur under different names. A canonical four-way language will crystallize the way [Smalltalk](https://en.wikipedia.org/wiki/Smalltalk) did out of message-passing simulators, or Erlang out of Ericsson's telecom: extracted from a generation of frameworks all reaching for the same abstractions.

If the pattern holds, we're about 10 years out from a quad-paradigm language.
