from build_sample import candidate_sentences, balanced_sample


def test_candidate_sentences_require_forward_marker_and_substance():
    text = (
        "Revenue increased last year. "
        "We expect volume to decline in 2024. "
        "Forward-looking statements include expects, plans, and believes. "
        "We plan to open three terminals by December 2024."
    )
    assert candidate_sentences(text) == [
        "We expect volume to decline in 2024.",
        "We plan to open three terminals by December 2024.",
    ]


def test_balanced_sample_is_deterministic_and_balanced():
    docs = {
        "a": [f"a{i}" for i in range(30)],
        "b": [f"b{i}" for i in range(30)],
        "c": [f"c{i}" for i in range(30)],
    }
    first = balanced_sample(docs, total=50, seed=20260902)
    second = balanced_sample(docs, total=50, seed=20260902)
    assert first == second
    counts = {name: sum(row["company"] == name for row in first) for name in docs}
    assert sorted(counts.values()) == [16, 17, 17]
    assert [row["id"] for row in first] == list(range(1, 51))
