"""
The graded-Elgot gap, in Python.

The whole question is about ONE thing: what index does a value's type carry,
and what happens to that index when you put the value in a loop.

  Layer 1.  a graded monad           — the return type carries a GRADE m
  Layer 2.  ordinary Elgot iteration — run the loop, get the value, but the
                                        grade you end at is k*m for whatever k
                                        the loop happened to run: DATA-dependent
  Layer 3.  the gap                  — a static effect system needs ONE grade m*
                                        for the whole loop, computed from m ALONE
                                        (no k). That operator m |-> m* is the
                                        thing nobody has packaged categorically.

Run me:  python3 graded_elgot_in_python.py
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Union

INF = float("inf")


# ----------------------------------------------------------------------
# Layer 1: a GRADED MONAD.
#
# Math:  an ordered effect monoid (E, ., 1, <=) and a functor T : E -> [C,C],
#        m |-> T_m, with graded unit eta : Id -> T_1 and graded multiplication
#        mu_{m,n} : T_m T_n -> T_{m.n}.
#
# Here E = (N u {inf}, +, 0, <=): "cost". The grade m is a number that rides
# along with the value. In the real type theory it sits in the TYPE T_m X;
# Python has no dependent types, so we carry it as data on the object.
# ----------------------------------------------------------------------
class E:
    """The effect monoid (E, ., 1, <=).  Cost under addition."""
    one = 0                                    # 1_E, the monoid identity
    mul = staticmethod(lambda m, n: m + n)     # m . n   (grade composition)
    leq = staticmethod(lambda m, n: m <= n)    # m <= n  (subeffecting order)


@dataclass
class T:
    """T_m X : a value x:X tagged with the grade m:E it was produced at."""
    grade: float
    value: object


def eta(x) -> T:                 # graded unit:  X -> T_1 X   (grade = 1_E = 0)
    return T(E.one, x)


def bind(tx: T, k: Callable[[object], T]) -> T:
    """Kleisli bind. This is mu after T(k): it COMPOSES the grades.
       T_m X  and  k : X -> T_n Y   give   T_{m.n} Y."""
    ty = k(tx.value)
    return T(E.mul(tx.grade, ty.grade), ty.value)


# ----------------------------------------------------------------------
# Y + X, the coproduct a loop body returns: exit-with-Y, or continue-with-X.
# ----------------------------------------------------------------------
@dataclass
class Exit:      # Left:  leave the loop carrying a Y
    y: object
@dataclass
class Loop:      # Right: go around again carrying an X
    x: object
Either = Union[Exit, Loop]


# ----------------------------------------------------------------------
# Layer 2: ORDINARY ELGOT ITERATION (the dagger), the thing that ALREADY exists.
#
# Math:  f : X -> T(Y + X)   gives   f-dagger : X -> T(Y).
# Note the monad T here is UNGRADED in the iteration theory (Elgot/while/Kleene
# monads, "Shades of Iteration"). The dagger produces a value. If we try to read
# a grade off it, we get k.m -- and k is how many times THIS run looped.
# ----------------------------------------------------------------------
def elgot_dagger(f: Callable[[object], T], x) -> T:
    grade = E.one
    step = f(x)
    grade = E.mul(grade, step.grade)
    while isinstance(step.value, Loop):
        step = f(step.value.x)
        grade = E.mul(grade, step.grade)
    return T(grade, step.value.y)            # the grade here is k.m -- DYNAMIC


# A concrete loop body  f : X -> T_m(Y + X).  Every step costs the SAME grade m=1.
def countdown(n) -> T:
    if n <= 0:
        return T(1, Exit("done"))
    return T(1, Loop(n - 1))


# ----------------------------------------------------------------------
# Layer 3: THE GAP -- the grade-level closure (-)* and the GRADED dagger.
#
# A static effect system must annotate the whole loop with ONE grade, before
# running it, knowing only the body's grade m. That grade is the closure m*.
#
# Gordon's "laxly iterable" condition (TOPLAS 2021): m* = the least p that is
#   (i)  subidempotent:  p . p <= p     (looping the result doesn't grow it)
#   (ii) above the body: p >= m  (and >= 1_E, so the zero-iteration case is covered)
# For E = (N u {inf}, +): p + p <= p forces p in {0, inf}. So:
# ----------------------------------------------------------------------
def star_additive(m):
    """m* for the cost monoid (N u {inf}, +).  Pure body stays pure; any real
       cost, iterated without a static bound, is unbounded."""
    subidempotents_above = [p for p in (0, INF) if E.leq(m, p)]
    return min(subidempotents_above)         # least subidempotent >= m


# The GRADED dagger we WANT but which no categorical iteration operator provides:
#     f : X -> T_m(Y + X)    =>    f-dagger : X -> T_{m*}(Y)
# Its index changes  m |-> m*.  THAT index map, with coherence vs mu/eta, is the gap.
def graded_dagger(f: Callable[[object], T], x, m, star) -> T:
    result = elgot_dagger(f, x)              # the VALUE comes from ordinary Elgot...
    return T(star(m), result.value)          # ...but the TYPE-GRADE is star(m), from m alone


# ----------------------------------------------------------------------
# A SECOND monoid, to show m* is not always trivial.
# E = (N u {inf}, max): "highest privilege level touched". max is IDEMPOTENT,
# so every element is subidempotent (max(p,p)=p) and m* = m. The grade passes
# through a loop UNCHANGED -- the closure is the identity here. Same gap, different
# closure: looping at privilege m stays at privilege m.
# ----------------------------------------------------------------------
class Emax:
    one = 0
    mul = staticmethod(lambda m, n: max(m, n))
    leq = staticmethod(lambda m, n: m <= n)

def star_max(m):
    return m                                  # every elt subidempotent -> closure = id


# ----------------------------------------------------------------------
if __name__ == "__main__":
    print("Layer 1 -- graded monad: grades COMPOSE under bind\n")
    prog = bind(T(2, 10), lambda v: bind(T(3, v + 1), lambda w: eta(w * w)))
    print(f"  bind chain at grades 2 then 3 then 1(eta):  grade={prog.grade}  value={prog.value}")
    print(f"  -> 2 . 3 . 0 = {prog.grade}  (cost adds; eta contributes the identity 0)\n")

    print("Layer 2 -- ordinary Elgot dagger: the grade you end at is k.m, DATA-dependent\n")
    for start in (3, 5, 20):
        r = elgot_dagger(countdown, start)
        print(f"  countdown({start:2d}): ran the loop, ended grade={r.grade:>2}  value={r.value!r}"
              f"   <- that {r.grade} is k.m for THIS run, not a static fact")
    print()

    print("Layer 3 -- the GAP: one static grade m* for the loop, from m alone\n")
    m = 1                                     # the body grade of `countdown`
    print(f"  body grade m = {m}")
    print(f"  star_additive(m) = {star_additive(m)}   <- the WHOLE loop is typed T_inf,"
          f" before running, independent of the start value")
    gd = graded_dagger(countdown, 5, m, star_additive)
    print(f"  graded_dagger(countdown, 5): value={gd.value!r}  TYPE-grade={gd.grade}"
          f"   (sound over-approx of every per-run k.m)")
    print(f"  star_additive(0) = {star_additive(0)}   <- a PURE loop body (cost 0) stays pure\n")

    print("  Same gap, different monoid -- (N u {inf}, max), 'highest level touched':")
    for m in (0, 2, 7):
        print(f"    star_max({m}) = {star_max(m)}   <- looping at level {m} stays at level {m}"
              f" (closure = identity, grade SURVIVES non-trivially)")
    print()

    print("WHY IT'S A GAP (what the code is showing):")
    print("  * Ordinary Elgot iteration EXISTS and gives the VALUE (elgot_dagger).")
    print("  * But its grade is k.m -- read off the run, useless as a static type.")
    print("  * The thing a graded effect system needs is the INDEX MAP  m |-> m*")
    print("    plus a dagger typed  f:X->T_m(Y+X)  =>  f†:X->T_{m*}(Y),")
    print("    coherent with graded mu/eta. That packaged operator is unpublished.")
    print("  * The one near-spoiler (Goncharov-Milius-Rauch) has a dagger that")
    print("    DISCARDS its parameter at the unit -- exactly elgot_dagger losing the")
    print("    grade. Orchard-Wadler-Eades proved graded != parametrized, so you")
    print("    can't borrow GMR's dagger and bolt a grade on. star() has no home yet.")
