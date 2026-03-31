export interface Symbol {
  id: string;
  symbol: string;
  name: string;
  python: string;
  category: 'hoare' | 'cat' | 'logic';
  description: string;
  example: string;
}

export const symbols: Symbol[] = [
  // Hoare Logic
  {
    id: 'triple',
    symbol: '{P} c {Q}',
    name: 'Hoare triple',
    python: 'assert P; c(); assert Q',
    category: 'hoare',
    description: 'If P holds before c runs, Q holds after.',
    example: `# Hoare triple: {P} c {Q}
# "If P holds before c runs, Q holds after."

P = lambda x: x > 0
c = lambda x: x * 2
Q = lambda y: y > 0

# Check the triple
for x in range(-5, 6):
    if P(x):
        result = c(x)
        assert Q(result), f"Failed: {x} -> {result}"
        print(f"  {x} -> {result} ✓")
    else:
        print(f"  {x} skipped (P doesn't hold)")
`,
  },
  {
    id: 'comp',
    symbol: 'c₁ ; c₂',
    name: 'Sequential composition',
    python: 'c2(c1(x))  # or >>=',
    category: 'hoare',
    description: 'Run c1, then feed its output to c2. The COMP rule: {P} c1 {R} and {R} c2 {Q} implies {P} c1;c2 {Q}.',
    example: `# COMP rule: chain postconditions through composition
# {P} c1 {R}  and  {R} c2 {Q}  implies  {P} c1;c2 {Q}
# R is the HANDSHAKE — stage 1's guarantee is stage 2's assumption.

double = lambda x: x * 2     # {x > 0} double {y > 0}
add_one = lambda x: x + 1    # {y > 0} add_one {z > 1}
pipeline = lambda x: add_one(double(x))  # {x > 0} pipeline {z > 1}

for x in range(1, 6):
    result = pipeline(x)
    print(f"  {x} -> {result}  (> 1? {result > 1})")
`,
  },
  {
    id: 'wp',
    symbol: 'wp(c, Q)',
    name: 'Weakest precondition',
    python: 'lambda a: all(Q(b) for b in support(c(a)))',
    category: 'hoare',
    description: 'The weakest P such that {P} c {Q} holds. The most permissive input that still guarantees Q.',
    example: `# Weakest precondition: what's the minimum input requirement?
# wp(c, Q) = the weakest P such that {P} c {Q}

c = lambda x: x - 3
Q = lambda y: y >= 0

# What inputs make Q hold after c?
# y = x - 3 >= 0  means  x >= 3
# So wp(c, Q) = lambda x: x >= 3

wp = lambda x: x >= 3  # the weakest precondition

for x in range(0, 8):
    result = c(x)
    ok = Q(result)
    predicted = wp(x)
    print(f"  x={x}: wp={predicted}, Q(c(x))={ok}  {'✓' if predicted == ok else '✗'}")
`,
  },
  {
    id: 'skip',
    symbol: '{P} skip {P}',
    name: 'SKIP rule',
    python: 'lambda x: x  # identity',
    category: 'hoare',
    description: 'Doing nothing preserves any property.',
    example: `# SKIP: doing nothing preserves any property
skip = lambda x: x

P = lambda x: x > 0
for x in [1, 5, 100]:
    assert P(skip(x)) == P(x)
    print(f"  skip({x}): P preserved ✓")
`,
  },
  {
    id: 'while',
    symbol: '{P} while b do c {P ∧ ¬b}',
    name: 'WHILE rule',
    python: 'while b(x): x = c(x)',
    category: 'hoare',
    description: 'If the body preserves P, the loop preserves P, and when it exits b is false.',
    example: `# WHILE rule: loop invariant
# If {b ∧ P} c {P}, then {P} while b do c {P ∧ ¬b}

# Count down to zero. Invariant: x >= 0
x = 10
print(f"  start: x={x}, x>=0 is {x >= 0}")

while x > 0:        # guard b: x > 0
    x = x - 1        # body c: decrement
    # invariant P: x >= 0 still holds

print(f"  end: x={x}, x>=0 is {x >= 0}, x>0 is {x > 0}")
print(f"  P ∧ ¬b: x>=0 and not x>0, so x==0 ✓")
`,
  },
  {
    id: 'top-pre',
    symbol: '{⊤} f {Q}',
    name: 'Trivial precondition',
    python: '# no restriction on input',
    category: 'hoare',
    description: 'Q holds for ALL inputs. This is ContractPreserving — an unconditional guarantee.',
    example: `# {⊤} f {Q} — trivial precondition means Q holds for ALL inputs
# This is ContractPreserving in the Lean artifact.

f = lambda x: abs(x)       # absolute value
Q = lambda y: y >= 0        # output is non-negative

# No precondition needed — works for any input
for x in [-5, -1, 0, 1, 5]:
    result = f(x)
    assert Q(result)
    print(f"  f({x}) = {result}, Q={Q(result)} ✓")

print("  Holds for ALL inputs — that's {⊤} f {Q}")
`,
  },

  // Category Theory
  {
    id: 'tensor',
    symbol: '⊗',
    name: 'Tensor product',
    python: '(x, y)  # tuple / parallel',
    category: 'cat',
    description: 'Run two things on separate state in parallel. Not intersection.',
    example: `# ⊗ = tensor product = parallel composition
# Think of it as a tuple: X ⊗ Y ≈ (X, Y)

# Two independent processes run on separate state
def process_a(x): return x * 2
def process_b(y): return y + 1

# Tensor: run both in parallel
def tensor(a, b):
    return lambda xy: (a(xy[0]), b(xy[1]))

parallel = tensor(process_a, process_b)
result = parallel((3, 7))
print(f"  (3, 7) ⊗-mapped to {result}")  # (6, 8)
`,
  },
  {
    id: 'kleisli',
    symbol: '>=>',
    name: 'Kleisli composition',
    python: 'lambda x: f(x) >>= g',
    category: 'cat',
    description: 'Compose monadic functions. f returns M β, g takes β and returns M γ.',
    example: `# Kleisli composition: compose functions that return distributions
# f: α → D(β),  g: β → D(γ)  =>  f >=> g: α → D(γ)

def f(x):
    """50/50 chance of x or x+1"""
    return {x: 0.5, x+1: 0.5}

def g(y):
    """Always double"""
    return {y*2: 1.0}

def kleisli_comp(f, g):
    def composed(x):
        result = {}
        for y, py in f(x).items():
            for z, pz in g(y).items():
                result[z] = result.get(z, 0) + py * pz
        return result
    return composed

h = kleisli_comp(f, g)
print(f"  f >=> g applied to 3: {h(3)}")
# {6: 0.5, 8: 0.5} — 50% chance of 6, 50% chance of 8
`,
  },
  {
    id: 'copy',
    symbol: 'ν',
    name: 'Copy morphism',
    python: 'lambda x: (x, x)',
    category: 'cat',
    description: 'Duplicate the state. A morphism is deterministic iff it commutes with copy.',
    example: `# ν (nu) = copy morphism: duplicate the state
copy = lambda x: (x, x)

# A morphism f is DETERMINISTIC if f;copy = copy;(f⊗f)
# "Apply then copy" = "copy then apply to both"

double = lambda x: x * 2

# Deterministic check:
x = 5
lhs = copy(double(x))           # apply then copy: (10, 10)
rhs = tuple(map(double, copy(x)))  # copy then apply: (10, 10)
print(f"  double is deterministic: {lhs} == {rhs}: {lhs == rhs}")

# Stochastic functions FAIL this test — that's the whole point
import random
def coin(x):
    return x if random.random() > 0.5 else -x

results = set()
for _ in range(100):
    a, b = coin(5), coin(5)  # two independent calls
    results.add((a, b))
print(f"  coin is stochastic: got {len(results)} distinct (a,b) pairs")
`,
  },
  {
    id: 'discard',
    symbol: 'ε',
    name: 'Discard morphism',
    python: 'lambda x: None',
    category: 'cat',
    description: 'Throw away the state. A morphism is total iff it commutes with discard.',
    example: `# ε (epsilon) = discard morphism: throw away the state
discard = lambda x: None

# A morphism f is TOTAL if f;discard = discard
# "Every input produces some output" (nothing is lost)

double = lambda x: x * 2
# discard(double(5)) == None == discard(5) ✓ total

def partial(x):
    if x > 0: return x
    else: return None  # partial! no output for x <= 0

print(f"  double is total: always produces output")
print(f"  partial is NOT total: partial(0) = {partial(0)}")
`,
  },
  {
    id: 'leq',
    symbol: '≤',
    name: 'Refinement order',
    python: '# one program "does less" than another',
    category: 'cat',
    description: 'Ordering on morphisms. f ≤ g means f refines g — it is more constrained, does less.',
    example: `# ≤ on morphisms = refinement
# f ≤ g means "f does less than g" or "f is more constrained"
# In Stoch: f ≤ g means f's support is contained in g's support

def f(x):
    return {x*2: 1.0}  # deterministic: always double

def g(x):
    return {x*2: 0.5, x*3: 0.5}  # stochastic: double or triple

# f ≤ g because f's support ⊆ g's support
# f is more constrained (deterministic), g is less (stochastic)
print(f"  f(3) support: {set(f(3).keys())}")
print(f"  g(3) support: {set(g(3).keys())}")
print(f"  f ≤ g: {set(f(3).keys()).issubset(set(g(3).keys()))}")
`,
  },

  // Logic
  {
    id: 'top',
    symbol: '⊤',
    name: 'Top / True',
    python: 'True  # or lambda _: True',
    category: 'logic',
    description: 'The predicate that is always true. No restriction.',
    example: `# ⊤ = top = always true = no restriction
top = lambda _: True

for x in [-5, 0, 5, "hello", None]:
    print(f"  ⊤({x}) = {top(x)}")
`,
  },
  {
    id: 'bot',
    symbol: '⊥',
    name: 'Bottom / False',
    python: 'False  # or lambda _: False',
    category: 'logic',
    description: 'The predicate that is always false. Nothing satisfies it.',
    example: `# ⊥ = bottom = always false = nothing satisfies it
bot = lambda _: False

# {⊥} c {Q} is always valid — no input qualifies, nothing to check
# This is the VACUOUS case your nontriviality counterexample rules out
for x in [-5, 0, 5]:
    print(f"  ⊥({x}) = {bot(x)}")
print("  {⊥} c {Q} is trivially true — that's why nontriviality matters")
`,
  },
  {
    id: 'and',
    symbol: '∧',
    name: 'Conjunction (and)',
    python: 'and  # or &&',
    category: 'logic',
    description: 'Both must hold.',
    example: `# ∧ = and = both must hold
P = lambda x: x > 0
Q = lambda x: x < 10

both = lambda x: P(x) and Q(x)  # P ∧ Q

for x in [-1, 0, 5, 10, 15]:
    print(f"  P∧Q({x}) = {both(x)}")
`,
  },
  {
    id: 'or',
    symbol: '∨',
    name: 'Disjunction (or)',
    python: 'or  # or ||',
    category: 'logic',
    description: 'At least one must hold.',
    example: `# ∨ = or = at least one
P = lambda x: x > 10
Q = lambda x: x < 0

either = lambda x: P(x) or Q(x)  # P ∨ Q

for x in [-5, 0, 5, 15]:
    print(f"  P∨Q({x}) = {either(x)}")
`,
  },
  {
    id: 'not',
    symbol: '¬',
    name: 'Negation',
    python: 'not',
    category: 'logic',
    description: 'Flip the truth value.',
    example: `# ¬ = not = flip
P = lambda x: x > 0
not_P = lambda x: not P(x)  # ¬P

for x in [-2, 0, 2]:
    print(f"  P({x})={P(x)}, ¬P({x})={not_P(x)}")
`,
  },
  {
    id: 'implies',
    symbol: '⇒',
    name: 'Implies',
    python: 'if P then Q  # not P or Q',
    category: 'logic',
    description: 'If P then Q. False only when P is true and Q is false.',
    example: `# ⇒ = implies = "if P then Q"
# P ⇒ Q is the same as (not P) or Q

implies = lambda p, q: (not p) or q

for p in [True, False]:
    for q in [True, False]:
        print(f"  {p} ⇒ {q} = {implies(p, q)}")
`,
  },
  {
    id: 'forall',
    symbol: '∀',
    name: 'For all',
    python: 'all(P(x) for x in xs)',
    category: 'logic',
    description: 'Every element satisfies the predicate.',
    example: `# ∀ = for all = every element satisfies P
P = lambda x: x > 0

xs_good = [1, 2, 3, 4, 5]
xs_bad = [1, 2, -1, 4, 5]

print(f"  ∀x∈{xs_good}: P(x) = {all(P(x) for x in xs_good)}")
print(f"  ∀x∈{xs_bad}: P(x) = {all(P(x) for x in xs_bad)}")
`,
  },
  {
    id: 'exists',
    symbol: '∃',
    name: 'There exists',
    python: 'any(P(x) for x in xs)',
    category: 'logic',
    description: 'At least one element satisfies the predicate.',
    example: `# ∃ = there exists = at least one satisfies P
P = lambda x: x > 100

xs = [1, 2, 3, 150, 5]
print(f"  ∃x∈{xs}: P(x) = {any(P(x) for x in xs)}")

xs2 = [1, 2, 3, 4, 5]
print(f"  ∃x∈{xs2}: P(x) = {any(P(x) for x in xs2)}")
`,
  },
];
