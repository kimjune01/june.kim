---
variant: post-wide
title: "Abduction Tuner"
tags: coding
---

<!-- TODO: Add section on the transition graph — which parameters interact and why (BLOCK_M → {BLOCK_K, num_warps, ...}) -->
<!-- TODO: Add section on phase 1 (follow the edge) — improvement names the bottleneck, graph predicts what else it touches -->
<!-- TODO: Add section on phase 2 (speculative depth) — lateral moves as saddle point signatures, regression + rescue via graph neighbors -->
<!-- Draft material: draft/transplant-mechanism.md -->

*Part of the [methodology](/methodology) series. Sequel to [Investigate](/investigate).*

Two compilers, same architecture, different search budgets. One generates 200 candidate kernel configs and benchmarks all of them. The other generates 15. Same generate-and-test loop. Same coordinate descent finish. The difference is degree, not kind.

### Generate and test

Both tinygrad and PyTorch's Inductor compile ML operations into GPU kernels through the same mechanism: heuristics produce candidate configurations, a benchmarking harness times each one, the fastest wins.

In tinygrad, the linearizer defines a combinatorial search space of axis splits, upcasts, and local sizes. [BEAM search](https://github.com/tinygrad/tinygrad/blob/master/tinygrad/engine/search.py) explores it — 200 candidates per kernel, evaluated on real hardware. The search space is explicit: each action transforms a kernel, and you search over action sequences.

In Inductor, [`triton_heuristics.py`](https://github.com/pytorch/pytorch/blob/main/torch/_inductor/runtime/triton_heuristics.py) generates 15-20 configs. `pointwise(size_hints)` returns a `list[Config]`. `reduction(size_hints, reduction_hint)` returns a `list[Config]`. Each config is `{XBLOCK, YBLOCK, RBLOCK, num_warps, num_stages}`. The harness benchmarks all of them, picks the min. Then coordinate descent fine-tunes.

The interface is identical. Given a kernel description, output a list of configs, benchmark each, return the winner. One system searches a large space with a capable search. The other searches a small space with hand-tuned starting points. The architecture is the same.

<div style="max-width:85%; margin:2em auto;">
<img src="/assets/transplant-concept-map.svg" alt="Concept map: tinygrad components mapped to their PyTorch/Inductor equivalents. BEAM search maps to Triton autotuner. heuristic.py maps to triton_heuristics.py. Both pairs highlighted as the seam where the abduction engine connects." style="width:100%; display:block;">
</div>

### The heuristic exists because the search is weak

Inductor's `triton_heuristics.py` is 4,000 lines of hand-tuned config generators. Pointwise kernels get one set of defaults. Reductions get another. Cooperative reductions get a third. Each has special cases for ROCm, for small tensors, for high-occupancy targets. The code works. It also encodes exactly the kind of knowledge that a strong search renders unnecessary.

Coordinate descent needs a good starting point. If you start in a saddle point's basin, coordesc will never escape — it only moves along one axis at a time, and saddle points trap single-axis search. The heuristics exist to place you near a good basin. Remove the saddle-point problem, remove the heuristics.

The abduction engine forms theories about *why* a kernel is slow, then tests only the relevant transformations. [52 trials vs BEAM's 193 actions](https://github.com/kimjune01/tinygrad-experiments), 1.85x geometric mean speedup over the heuristic on 4/5 workloads. The difference: BEAM searches blindly across the full action space. The abduction engine narrows the space by explaining the bottleneck first.

The strongest finding: cache the *theory*, not the *schedule*. "Tall-skinny matmuls benefit from tensor cores + UPCAST N + UNROLL K" is a semantic theory. It transfers across 7 different matmul shapes with zero additional measurements. Exact schedules — the literal BEAM outputs — fail on 3 of 6 shapes they weren't tuned for. The theory is more portable than the artifact.

### What transplants

Findings confirmed in one compiler sometimes transfer to another. [The transplanted hypothesis graph](https://github.com/kimjune01/pytorch/blob/abduction-engine/TRANSPLANTED_HYPOTHESES.md) maps 11 confirmed tinygrad findings to their PyTorch equivalents. Three have the highest expected impact.

**Lazy dequant chains.** The single largest speedup across all investigations: 12.4x. Quantized models create lazy dequantization chains — 130 intermediate operations per weight tensor — that fuse into the matmul kernel. The fused kernel re-executes the entire dequant graph on every forward pass, producing 328-line kernels with 271 scalar byte loads achieving 3 GB/s. Peak bandwidth is 354 GB/s. The kernel runs at 2% of the hardware's capability. Fix: `.contiguous()` on weights (a fusion barrier) plus onetime detection on the JIT. Two lines. 141 tok/s after, 11 tok/s before. The question for Inductor: does `torch.compile` constant-fold weight dequant subgraphs when using bitsandbytes or GPTQ? If not, every quantized LLM deployment on compiled PyTorch has the same regression.

**Theory-guided autotuning.** Inductor's autotuner retunes from scratch for every new shape. A model with 50 matmul layers at different dimensions runs 50 independent autotuning sessions, each exploring the same config space without learning from the previous results. The theory cache predicts that structural insights transfer: if a 1024x1024 matmul is memory-bound and benefits from tile config X, a 2048x2048 matmul with the same arithmetic intensity will too. The theory transfers; the exact config doesn't. For MoE models with dozens of expert sizes, or attention heads at varying sequence lengths, this eliminates redundant autotuning across shapes that share structural properties.

**Operations research formulations.** Five compiler optimization problems map to classical OR problems that the OR community solved decades ago:

| Compiler problem | OR formulation |
|---|---|
| Instruction scheduling | [RCPSP](https://en.wikipedia.org/wiki/Resource-constrained_project_scheduling_problem) (Pritsker 1969) |
| Bank conflict avoidance | GF(2) assignment (XOR-swizzle) |
| Fusion decisions | [Weighted hypergraph partitioning](https://en.wikipedia.org/wiki/Hypergraph#Partitioning) |
| Quantization bitwidth | Integer linear programming |
| Autotuning search | [Branch-and-bound](https://en.wikipedia.org/wiki/Branch_and_bound) |

Inductor's fusion heuristic (`scheduler.py`, `can_fuse()`) is 100+ lines of special cases. The OR formulation says it's a hypergraph partitioning problem with known algorithms — [METIS](https://github.com/KarypisLab/METIS), [Kernighan-Lin](https://en.wikipedia.org/wiki/Kernighan%E2%80%93Lin_algorithm) — that provide optimality bounds. The heuristic provides no bounds. You can't prove your fusion decisions are good; you can only observe that they haven't been bad yet.

### The seam

Where does the abduction engine bolt on? `triton_heuristics.py` has clean functions: given size hints and kernel shape, return `list[Config]`. The abduction engine is a drop-in replacement. Same interface, different search. The heuristic generates 15 configs from rules. The abduction engine generates configs from theories about why the kernel is slow.

The fusion decisions in `scheduler.py` are the bigger prize but a harder surgery. `can_fuse()` is entangled with stream boundaries, device types, template-specific logic, buffer mutation checks. No clean seam. The config search is the entry point. Fusion is the next target, once the entry point proves the approach.

### Provenance

Each transplanted hypothesis traces to a confirmed finding with a source investigation, a hypothesis graph, and measured evidence. The [full transplant document](https://github.com/kimjune01/pytorch/blob/abduction-engine/TRANSPLANTED_HYPOTHESES.md) has the provenance table, the perturbation instructions, and the predicted trajectories.

The code is [AGPL-3.0](https://github.com/kimjune01/pytorch/blob/abduction-engine/LICENSE). The [experiment repos](https://github.com/kimjune01/tinygrad-experiments) are public. This prose is [CC BY-SA](https://creativecommons.org/licenses/by-sa/4.0/).

---

*The [abduction engine prototype](https://github.com/kimjune01/pytorch/tree/abduction-engine) is on a PyTorch fork. The [transplanted hypotheses](https://github.com/kimjune01/pytorch/blob/abduction-engine/TRANSPLANTED_HYPOTHESES.md) map 11 tinygrad findings to their Inductor equivalents. The investigation methodology is described in [Investigate](/investigate); the underlying primitive in [Abduction](/abduction).*
