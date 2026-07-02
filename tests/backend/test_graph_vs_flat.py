"""Tests for captured-scene graph-vs-flat benchmark."""
from pathlib import Path

import pytest

from backend.query.graph_vs_flat import (
    DEFAULT_SCENE_MAP,
    compare_modes_for_query,
    filter_five_scene_queries,
    load_benchmark_queries,
    load_scene_bundle,
    run_five_scene_benchmark,
)


ROOT = Path(__file__).resolve().parents[2]
SCENE_ROOT = ROOT / "backend" / "data" / "scenes"
BENCHMARK = ROOT / "docs" / "benchmarks" / "benchmark_queries_v1.json"


@pytest.mark.skipif(
    not (SCENE_ROOT / "ConferenceHall-capture-pilot" / "views").exists(),
    reason="Captured ConferenceHall scene not present",
)
def test_load_scene_bundle_has_views_and_tree():
    bundle = load_scene_bundle(SCENE_ROOT / "ConferenceHall-capture-pilot")
    assert bundle["views"]
    assert bundle["tree"]
    assert bundle["manifest"]["root_node_id"] == "root" or bundle["manifest"]["root_id"] == "root"


@pytest.mark.skipif(not BENCHMARK.exists(), reason="benchmark_queries_v1.json missing")
def test_filter_five_scene_queries_returns_forty():
    queries = filter_five_scene_queries(load_benchmark_queries(BENCHMARK))
    assert len(queries) == 40
    assert {q["scene_id"] for q in queries} == set(DEFAULT_SCENE_MAP)


@pytest.mark.skipif(
    not (SCENE_ROOT / "ConferenceHall-capture-pilot" / "views").exists() or not BENCHMARK.exists(),
    reason="Captured scene or benchmark missing",
)
def test_graph_checks_fewer_views_than_flat_on_chair_query():
    bundle = load_scene_bundle(SCENE_ROOT / "ConferenceHall-capture-pilot")
    query = next(
        q for q in filter_five_scene_queries(load_benchmark_queries(BENCHMARK))
        if q["query_id"] == "q051"
    )
    row = compare_modes_for_query(bundle, query)
    assert row["flat"]["views_checked"] >= row["graph"]["views_checked"]
    assert row["flat"]["input_tokens"] >= row["graph"]["input_tokens"]


@pytest.mark.skipif(
    not all((SCENE_ROOT / path).exists() for path in DEFAULT_SCENE_MAP.values()) or not BENCHMARK.exists(),
    reason="All five captured scenes or benchmark missing",
)
def test_run_five_scene_benchmark_summary():
    run = run_five_scene_benchmark(
        benchmark_path=BENCHMARK,
        scene_root=SCENE_ROOT,
        include_affordance=True,
    )
    assert run["summary"]["query_count"] == 40
    assert run["summary"]["averages"]["flat_views_checked"] > 0
    assert "savings_views_pct" in run["summary"]["averages"]
