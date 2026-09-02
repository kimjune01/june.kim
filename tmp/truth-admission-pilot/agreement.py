import argparse
import json
from pathlib import Path


FIELDS = [
    "is_empirical_claim",
    "forward_claim",
    "observable",
    "boundary",
    "deadline",
    "known_resolution_source",
    "identity_stable",
    "admitted",
]


def cohen_kappa(a: list[str], b: list[str]) -> float:
    if len(a) != len(b) or not a:
        raise ValueError("ratings must be non-empty and equal length")
    n = len(a)
    observed = sum(x == y for x, y in zip(a, b)) / n
    labels = set(a) | set(b)
    expected = sum((a.count(label) / n) * (b.count(label) / n) for label in labels)
    if expected == 1:
        return 1.0 if observed == 1 else 0.0
    return (observed - expected) / (1 - expected)


def summarize_field(a: list[dict], b: list[dict], field: str) -> dict:
    a_by_id = {row["id"]: row for row in a}
    b_by_id = {row["id"]: row for row in b}
    if set(a_by_id) != set(b_by_id):
        raise ValueError("coder IDs differ")
    ids = sorted(a_by_id)
    av = [a_by_id[i][field].lower() for i in ids]
    bv = [b_by_id[i][field].lower() for i in ids]
    return {
        "field": field,
        "n": len(ids),
        "agreement": sum(x == y for x, y in zip(av, bv)) / len(ids),
        "kappa": cohen_kappa(av, bv),
        "a_yes": av.count("yes"),
        "b_yes": bv.count("yes"),
        "disagreement_ids": [i for i, x, y in zip(ids, av, bv) if x != y],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("coder_a")
    parser.add_argument("coder_b")
    parser.add_argument("--output")
    args = parser.parse_args()
    a = json.loads(Path(args.coder_a).read_text())
    b = json.loads(Path(args.coder_b).read_text())
    results = [summarize_field(a, b, field) for field in FIELDS]
    rendered = json.dumps(results, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
