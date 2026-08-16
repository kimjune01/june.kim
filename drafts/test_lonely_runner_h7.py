import importlib.util
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("lonely_runner_h7.py")
SPEC = importlib.util.spec_from_file_location("lonely_runner_h7", MODULE_PATH)
lrc = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(lrc)


def test_cover_uses_exact_integer_arithmetic():
    # D = (k + 1)p = 28. At j = 1, v = 7 is exactly 1/4 away,
    # so the strict bad-time predicate must not count it as covered.
    assert not lrc.covers(v=7, j=1, k=3, p=7, denominator=4)
    assert lrc.covers(v=6, j=1, k=3, p=7, denominator=4)


def test_gcd_constraint_checks_every_omitted_speed():
    assert lrc.gcd_constraint((1, 2, 3), k=3, p=7)
    assert not lrc.gcd_constraint((2, 4, 5), k=3, p=7)


def test_reproduces_published_working_modulus():
    result = lrc.find_bad_cover(k=3, p=7, denominator=4)
    assert result is None


def test_reproduces_published_exception():
    result = lrc.find_bad_cover(k=6, p=17, denominator=7)
    assert result is not None
    assert len(result) <= 6
    assert lrc.gcd_constraint(result, k=6, p=17)
    assert lrc.covers_universe(result, k=6, p=17, denominator=7)


def test_smt_search_matches_backtracking_on_known_cases():
    assert lrc.find_bad_cover_smt(k=3, p=7, denominator=4) is None
    result = lrc.find_bad_cover_smt(k=6, p=17, denominator=7)
    assert result is not None
    assert lrc.gcd_constraint(result, k=6, p=17)
    assert lrc.covers_universe(result, k=6, p=17, denominator=7)


def test_k8_p43_certificate_replays():
    witness = (1, 7, 9, 45, 54, 63, 72, 117)
    assert lrc.gcd_constraint(witness, k=8, p=43)
    assert lrc.covers_universe(witness, k=8, p=43, denominator=9)
