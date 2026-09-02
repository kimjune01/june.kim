import argparse
import json
import random
import re
from pathlib import Path


MARKER = re.compile(
    r"\b(?:we\s+(?:expect|anticipate|believe|plan|intend|estimate|target|project)|"
    r"(?:is|are|was|were)\s+expected\s+to|will\s+(?:improve|reduce|increase|"
    r"decrease|deliver|enable|generate|result|continue|begin|complete))\b",
    re.IGNORECASE,
)
SENTENCE = re.compile(r"(?<=[.!?])\s+(?=[A-Z])")


def candidate_sentences(text: str) -> list[str]:
    normalized = re.sub(r"\s+", " ", text).strip()
    candidates = []
    for sentence in SENTENCE.split(normalized):
        sentence = sentence.strip()
        if not 25 <= len(sentence) <= 700:
            continue
        if "forward-looking statements" in sentence.lower():
            continue
        if MARKER.search(sentence):
            candidates.append(sentence)
    return candidates


def balanced_sample(
    docs: dict[str, list[str]], total: int, seed: int
) -> list[dict[str, object]]:
    names = sorted(docs)
    base, extra = divmod(total, len(names))
    rng = random.Random(seed)
    rows = []
    for index, name in enumerate(names):
        count = base + (index < extra)
        if len(docs[name]) < count:
            raise ValueError(f"{name} has only {len(docs[name])} candidates")
        for sentence in rng.sample(docs[name], count):
            rows.append({"company": name, "sentence": sentence})
    rng.shuffle(rows)
    for index, row in enumerate(rows, 1):
        row["id"] = index
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", action="append", nargs=2, metavar=("COMPANY", "PATH"))
    parser.add_argument("--output", required=True)
    parser.add_argument("--total", type=int, default=50)
    parser.add_argument("--seed", type=int, default=20260902)
    args = parser.parse_args()
    docs = {
        company: candidate_sentences(Path(path).read_text())
        for company, path in args.input
    }
    rows = balanced_sample(docs, args.total, args.seed)
    Path(args.output).write_text(json.dumps(rows, indent=2) + "\n")
    for company in sorted(docs):
        selected = sum(row["company"] == company for row in rows)
        print(f"{company}: {len(docs[company])} candidates, {selected} selected")


if __name__ == "__main__":
    main()
