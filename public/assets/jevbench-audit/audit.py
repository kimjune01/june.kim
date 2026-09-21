"""Offline audit; no credentials, model calls or modifications to upstream files.

Run: uv run --no-project python audit.py
Checks published arithmetic independently, then probes the official scorer.
Assertions describe consistency requirements, not claims of task validity.
"""
import hashlib
import json
import math
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT / "upstream"
sys.path.insert(0, str(REPO))
from jevbench import composite_v12 as C
from jevbench.metrics import ece_top_label
from jevbench.scoring import score_task
from jevbench.tasks import Task


def read(path):
    return json.loads((REPO / path).read_text())


def close(a, b):
    assert (a is None and b is None) or (
        a is not None and b is not None and math.isclose(a, b, abs_tol=1e-8)
    ), (a, b)


def clamp(x):
    return max(0, min(100, x))


def independent_axes(s):
    weights = {"easy": .14, "standard": .28, "judge": .28, "hard": .30}
    tiers = {t: x for t, x in s["tiers"].items() if x is not None}
    intelligence = 100 * sum(weights[t] * x for t, x in tiers.items()) / sum(weights[t] for t in tiers)
    ece, fidelity = s["calibration"]["ece_hard"], s["calibration"]["probability_fidelity"]
    calibration = None if ece is None else max(0, 100 * (1 - 2 * ece))
    if calibration is not None and fidelity is not None:
        calibration = (calibration + fidelity) / 2
    latencies = [s["speed"][k] for k in ("p50_s_raw", "p95_s_raw")]
    if any(x is None for x in latencies):
        speed = None
    else:
        if s["endpoint_kind"] != "api":
            latencies = [x * 2 + (.15 if s["endpoint_kind"] in ("cpu", "gpu") else 0) for x in latencies]
        speed = sum(clamp(100 - 20 * math.log10(x / .1)) for x in latencies) / 2
    cost = clamp(100 - 30 * math.log10(s["cost"]["usd_per_1000"] / .001))
    return dict(intelligence=intelligence, calibration=calibration, speed=speed, cost=cost)


def probability_probe(tasks, sharpen=False):
    pairs, distances, outcomes = [], [], []
    for t in tasks:
        gold = t.provenance.get("gold_probs")
        onehot = {k: float(k == str(t.expected)) for k in t.labels}
        p = onehot if sharpen or gold is None else gold
        scored = score_task(p, t)
        assert scored["valid"] and scored["correct"], (t.id, scored)
        pairs.append((max(scored["probs"].values()), scored["correct"]))
        if gold is not None:
            distances.append(C.tvd(scored["probs"], gold, t.labels))
        outcomes.append({"id": t.id, "probs": scored["probs"], "correct": scored["correct"]})
    ece = ece_top_label(pairs)["ece"]
    tvd = sum(distances) / len(distances)
    return {"n": len(tasks), "n_probability": len(distances), "accuracy": 1,
            "ece": ece, "mean_tvd": tvd, "calibration_score": C.calibration(ece, tvd),
            "outcomes": outcomes}


def main():
    artifact = read("results/v1.2/jevbench-v1.2-results.json")
    per = read("results/v1.2/jevbench-v1.2-per-task.json")
    rows = artifact["systems"]
    checks = []
    for s in rows:
        axes = independent_axes(s)
        for k, v in axes.items():
            close(v, s["axes"][k])
        score = math.prod(max(v or 0, 1) for v in axes.values()) ** .25
        close(score, s["jevbench_score"])
        if s["hard"]:
            families = s["hard"]["by_family"]
            n = sum(f["n"] for f in families.values())
            correct = sum(f["correct"] for f in families.values())
            close(correct / n, s["hard"]["accuracy"])
        checks.append({"key": s["key"], "score": score, "axes": axes})
    ranked = sorted((s for s in rows if s["ranked"]), key=lambda s: -s["jevbench_score"])
    for rank, s in enumerate(ranked, 1):
        assert rank == s["rank"]
    tasks = []
    for file in sorted((REPO / "datasets/public").glob("*.jsonl")):
        tasks += [Task.from_dict(json.loads(line)) for line in file.read_text().splitlines() if line]
    assert len({t.id for t in tasks}) == len(tasks)
    public_ids = {t["id"] for t in per["tasks"] if t["public"]}
    assert {t.id for t in tasks} == public_ids
    # A key/grader compatibility check only: it cannot verify the prose's answer.
    for t in tasks:
        r = score_task({k: float(k == str(t.expected)) for k in t.labels}, t)
        assert r["valid"] and r["correct"], (t.id, r)
    hard = [t for t in tasks if t.id.startswith("hard-")]
    witness = next(t for t in hard if t.id == "hard-opus-b-probability-02")
    # Independent calculation from the table: no-deploy column has 4, 13, 3 / 20.
    assert witness.provenance["gold_probs"] == {"bad_push": 4/20, "upstream_provider": 13/20, "database_hardware": 3/20}
    exact = probability_probe([witness])
    sharpened = probability_probe([witness], sharpen=True)
    close(exact["calibration_score"], 65)
    close(sharpened["calibration_score"], 82.5)
    # This local ordering is NOT a claim that sharpening improves the full board.
    assert sharpened["mean_tvd"] > exact["mean_tvd"]
    assert sharpened["calibration_score"] > exact["calibration_score"]
    gold_all_hard = probability_probe(hard)
    # Output contract mutations: documented rounding is accepted; malformed maps fail.
    base = {k: float(k == str(witness.expected)) for k in witness.labels}
    mutations = {
        "missing_label": {k: v for k, v in base.items() if k != "bad_push"},
        "extra_label": {**base, "extraneous": 0},
        "negative": {**base, "bad_push": -.1, "upstream_provider": 1.1},
        "nan": {**base, "bad_push": float("nan")},
        "sum_zero": {k: 0 for k in base},
        "rounding_1.01": {"bad_push": .20, "database_hardware": .15, "upstream_provider": .66},
    }
    mutation_results = {}
    for name, p in mutations.items():
        result = score_task(p, witness)
        assert result["valid"] == (name == "rounding_1.01")
        mutation_results[name] = result
    ceiling = C.jevbench_score(dict(intelligence=100, calibration=None, speed=100, cost=100))
    close(ceiling, 100 ** .75)
    comparisons = {}
    indexed = {s["key"]: s for s in rows}
    for key in ("jev-1.13.0", "gemini-3.1-flash-lite", "deepseek-flash"):
        s = indexed[key]
        outcomes = per["systems"][key]["public_tasks"]
        assert set(outcomes) == public_ids
        h = [outcomes[t.id][0] for t in hard]
        comparisons[key] = {"tiers": s["tiers"], "hard_counts": dict(Counter(h)),
                            "hard_by_family": s["hard"]["by_family"], "cost": s["cost"], "speed": s["speed"]}
    # Paired public-hard outcomes; hidden task-level verdicts are not shipped.
    paired = {}
    for key in ("gemini-3.1-flash-lite", "deepseek-flash"):
        counts = Counter((per["systems"]["jev-1.13.0"]["public_tasks"][t.id][0] == "c",
                          per["systems"][key]["public_tasks"][t.id][0] == "c") for t in hard)
        b, c = counts[True, False], counts[False, True]
        discordant = b + c
        p = min(1, 2 * sum(math.comb(discordant, i) for i in range(min(b,c)+1)) / 2**discordant) if discordant else 1
        paired[key] = {"both_correct": counts[True,True], "jev_only": b, "other_only": c,
                       "neither_correct": counts[False,False], "exact_mcnemar_p": p,
                       "scope": "111 fixed public hard tasks; descriptive, not evidence of production representativeness"}
    files = ["results/v1.2/jevbench-v1.2-results.json", "results/v1.2/jevbench-v1.2-per-task.json",
             "jevbench/composite_v12.py", "jevbench/scoring.py", "jevbench/metrics.py", "jevbench/summarize.py",
             "datasets/public/hard.jsonl", "datasets/public/easy.jsonl", "datasets/public/original.jsonl"]
    out = {"upstream_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO, text=True).strip(),
           "revision": artifact["revision"], "sha256": {p: hashlib.sha256((REPO/p).read_bytes()).hexdigest() for p in files},
           "aggregate_checks": checks, "ranked_count": len(ranked), "public_key_compatibility_passed": len(tasks),
           "task_counts": per["task_counts"], "single_task_exact_gold": exact, "single_task_sharpened": sharpened,
           "public_hard_gold": gold_all_hard, "mutation_results": mutation_results,
           "label_only_maximum_score": ceiling, "comparisons": comparisons, "paired_public_hard": paired,
           "haiku_present": any("haiku" in json.dumps(s).lower() for s in rows)}
    phishing_repo = ROOT / "phishing-upstream"
    metrics_file = phishing_repo / "results/metrics.json"
    phishing = json.loads(metrics_file.read_text())
    confusion = {}
    for key in ("jev", "llm"):
        m = phishing[key]
        n = sum(m[k] for k in ("tp", "tn", "fp", "fn"))
        assert n == 2000
        close((m["tp"] + m["tn"]) / n, m["accuracy"])
        confusion[key] = {k: m[k] for k in ("tp", "tn", "fp", "fn", "accuracy", "recall", "fpr")}
    out["phishing_supplement"] = {
        "commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=phishing_repo, text=True).strip(),
        "metrics_sha256": hashlib.sha256(metrics_file.read_bytes()).hexdigest(),
        "confusion": confusion,
        "scope": "aggregate arithmetic and code/report inspection only; raw model responses not shipped",
        "additional_jev_errors_per_1000": (phishing["llm"]["accuracy"] - phishing["jev"]["accuracy"]) * 1000,
        "reported_list_price_saving_per_1000": .462 - .038,
        "saving_usd_per_additional_error": (.462 - .038) / ((phishing["llm"]["accuracy"] - phishing["jev"]["accuracy"]) * 1000),
    }
    full_counts = {}
    for key in ("jev-1.13.0", "deepseek-flash"):
        tiers = per["systems"][key]["by_tier"]
        n = sum(t[k] for t in tiers.values() for k in ("c", "w", "f", "n"))
        assert n == 534
        full_counts[key] = {"correct": sum(t["c"] for t in tiers.values()), "n": n}
    assert full_counts["jev-1.13.0"]["correct"] == 468
    assert full_counts["deepseek-flash"]["correct"] == 511
    cost_delta = indexed["deepseek-flash"]["cost"]["usd_per_1000"] - indexed["jev-1.13.0"]["cost"]["usd_per_1000"]
    correct_delta = (511 - 468) / 534 * 1000
    out["full_cohort_economics"] = {
        "counts": full_counts,
        "deepseek_extra_usd_per_1000": cost_delta,
        "deepseek_extra_correct_per_1000": correct_delta,
        "usd_per_additional_correct": cost_delta / correct_delta,
        "scope": "aggregate 534-item mix; equal error costs; excludes latency, retries and downstream costs",
    }
    (ROOT / "audit-results.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({k: v for k,v in out.items() if k not in ("sha256", "aggregate_checks", "comparisons", "public_hard_gold")}, indent=2))
    print("Public-hard gold calibration:", {k:v for k,v in gold_all_hard.items() if k != "outcomes"})
    print("PASS: all assertions;", len(rows), "aggregate rows;", len(tasks), "public keys")


if __name__ == "__main__":
    main()
