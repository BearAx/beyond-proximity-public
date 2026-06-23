import json

import pytest

from backend.query.model_client import (
    CACHE_SCHEMA,
    CachedModelClient,
    ModelCacheError,
    ModelConfigurationError,
    StubModelClient,
    create_model_client,
)


def _tree():
    return {
        "root": {
            "node_id": "root",
            "type": "root",
            "name": "Root",
            "summary": "Whole scene",
            "view_ids": [],
            "children_ids": ["leaf"],
        },
        "leaf": {
            "node_id": "leaf",
            "type": "leaf",
            "name": "Lounge",
            "summary": "Lounge with a red chair",
            "view_ids": ["v001"],
            "children_ids": [],
        },
    }


def _views():
    return {
        "v001": {
            "view_id": "v001",
            "scene_summary": "A red chair in the lounge.",
            "room_type": "lounge",
            "objects": [{"label": "chair", "bbox_2d": [0.1, 0.2, 0.4, 0.8]}],
            "spatial_relations": [],
            "functional_context": "seating",
        }
    }


def test_stub_client_is_explicit_and_has_no_model_usage():
    client = StubModelClient()
    answer = client.answer_query(
        {"query": "Find the red chair", "query_type": "attribute"},
        _tree(),
        _views(),
    )

    assert client.mode == "stub"
    assert answer["result"]["found"] is True
    assert answer["result"]["selected_view_id"] == "v001"
    assert answer["visited_nodes"] == ["root", "leaf"]
    assert any("not live" in warning.lower() for warning in answer["warnings"])
    assert client.stats_snapshot()["model_call_count"] == 0
    assert client.stats_snapshot()["total_tokens"] is None


def test_stub_client_searches_captured_viewjson_fields():
    client = StubModelClient()
    views = {
        "v001": {
            "view_id": "v001",
            "summary": "Conference room seating.",
            "visible_regions": [
                {"label": "conference table area", "approx_location": "center"}
            ],
            "visible_objects": [
                {
                    "label": "chair",
                    "attributes": ["red"],
                    "approx_location": "left of table",
                    "bbox_2d": None,
                }
            ],
            "landmarks": [],
            "free_text_notes": "",
        }
    }
    tree = {
        "root": {
            "node_id": "root",
            "node_type": "root",
            "name": "Root",
            "summary": "Captured scene",
            "view_ids": ["v001"],
            "children_ids": ["object_v001_001_chair"],
        },
        "object_v001_001_chair": {
            "node_id": "object_v001_001_chair",
            "node_type": "object",
            "name": "chair",
            "summary": "Object observation",
            "view_ids": ["v001"],
            "children_ids": [],
        },
    }

    answer = client.answer_query("Find the red chair", tree, views)

    assert answer["result"]["found"] is True
    assert answer["result"]["matched_object"] == "chair"
    assert answer["result"]["selected_view_id"] == "v001"
    assert answer["visited_nodes"] == ["root", "object_v001_001_chair"]


def test_cached_client_replays_only_verified_live_entry(tmp_path):
    query = {"query": "Find the red chair", "query_type": "attribute"}
    payload = {"query": query, "tree": _tree(), "views": _views()}
    response = {
        "structured_plan": {"target": "chair"},
        "visited_nodes": ["root", "leaf"],
        "selected_views": ["v001"],
        "result": {"found": True, "selected_view_id": "v001"},
        "warnings": [],
    }
    CachedModelClient.write_cache_entry(
        tmp_path,
        "answer_query",
        payload,
        response,
        provider="test_provider",
        model="test_model",
        version="1",
        token_usage={"input_tokens": 10, "output_tokens": 4, "total_tokens": 14},
    )

    client = CachedModelClient(tmp_path)
    replayed = client.answer_query(query, _tree(), _views())

    assert replayed == response
    assert client.mode == "cached_live"
    assert client.provider == "test_provider"
    assert client.model == "test_model"
    assert client.stats_snapshot()["cache_hits"] == 1
    assert client.stats_snapshot()["model_call_count"] == 0
    assert client.stats_snapshot()["total_tokens"] == 14


def test_cached_client_rejects_stub_provenance(tmp_path):
    client = CachedModelClient(tmp_path)
    payload = {"query": "x", "tree": {}, "views": {}}
    path = client.cache_path("answer_query", payload)
    path.parent.mkdir(parents=True)
    path.write_text(
        json.dumps({
            "cache_schema": CACHE_SCHEMA,
            "source_mode": "stub",
            "method": "answer_query",
            "request_hash": path.stem,
            "response": {},
        }),
        encoding="utf-8",
    )

    with pytest.raises(ModelCacheError, match="not verified live provenance"):
        client.answer_query("x", {}, {})


def test_live_mode_fails_gracefully_without_credentials(monkeypatch):
    for name in ("SEMANTICSPLAT_PROVIDER", "SEMANTICSPLAT_MODEL", "SEMANTICSPLAT_API_KEY"):
        monkeypatch.delenv(name, raising=False)

    with pytest.raises(ModelConfigurationError, match="missing environment variables"):
        create_model_client("live")


def test_nonzero_temperature_is_rejected():
    with pytest.raises(ModelConfigurationError, match="temperature=0"):
        create_model_client("stub", temperature=0.2)
