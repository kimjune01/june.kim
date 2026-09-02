from agreement import cohen_kappa, summarize_field


def test_cohen_kappa_perfect_and_chance_corrected():
    assert cohen_kappa(["yes", "no"], ["yes", "no"]) == 1.0
    assert cohen_kappa(["yes", "yes", "no", "no"], ["yes", "no", "yes", "no"]) == 0.0


def test_summarize_field_counts_disagreements():
    a = [{"id": 1, "admitted": "yes"}, {"id": 2, "admitted": "no"}]
    b = [{"id": 1, "admitted": "no"}, {"id": 2, "admitted": "no"}]
    result = summarize_field(a, b, "admitted")
    assert result["n"] == 2
    assert result["agreement"] == 0.5
    assert result["a_yes"] == 1
    assert result["b_yes"] == 0
    assert result["disagreement_ids"] == [1]
