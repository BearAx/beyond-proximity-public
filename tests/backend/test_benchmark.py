"""Tests for graph vs flat query benchmark."""
from backend.query.benchmark import compare_modes, simulate_graph_search, simulate_flat_search


def test_flat_checks_more_views_than_graph():
    r = compare_modes("default", "take me to the projector")
    assert r["flat"]["views_checked"] >= r["graph"]["views_checked"]
    assert r["flat"]["input_tokens"] >= r["graph"]["input_tokens"]


def test_graph_finds_projector():
    g = simulate_graph_search("default", "take me to the projector")
    assert g.views_checked < 19
    assert g.llm_calls < 20


def test_flat_checks_all_views():
    f = simulate_flat_search("default", "find the bar")
    assert f.views_checked == 19
    assert f.llm_calls == 20  # 1 decomposition + 19 leaf checks
