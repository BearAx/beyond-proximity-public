"""Provider-independent model clients for headless SemanticSplat experiments."""
from __future__ import annotations

import hashlib
import json
import os
import re
from abc import ABC, abstractmethod
from copy import deepcopy
from pathlib import Path
from typing import Any


CACHE_SCHEMA = "semanticsplat.model_cache.v1"
VALID_MODES = {"stub", "live", "cached_live"}


class ModelClientError(RuntimeError):
    """Base error for provider and cache failures."""


class ModelConfigurationError(ModelClientError):
    """Raised when requested model execution is not configured."""


class ModelCacheError(ModelClientError):
    """Raised when cached-live data is missing or has invalid provenance."""


class ModelClient(ABC):
    """Provider-independent semantic scene and query interface."""

    mode: str
    provider: str | None
    model: str | None
    version: str | None
    temperature: float

    def __init__(
        self,
        *,
        mode: str,
        provider: str | None,
        model: str | None,
        version: str | None = None,
        temperature: float = 0.0,
    ) -> None:
        if mode not in VALID_MODES:
            raise ValueError(f"Unsupported model mode: {mode}")
        self.mode = mode
        self.provider = provider
        self.model = model
        self.version = version
        self.temperature = temperature
        self._stats: dict[str, Any] = {
            "model_call_count": 0,
            "cache_hits": 0,
            "retry_count": 0,
            "failure_count": 0,
            "input_tokens": None,
            "output_tokens": None,
            "total_tokens": None,
        }

    @abstractmethod
    def describe_view(self, image_path: str | Path, metadata: dict[str, Any]) -> dict[str, Any]:
        """Return a semantic description for one view."""

    @abstractmethod
    def build_tree(
        self,
        view_summaries: dict[str, dict[str, Any]],
        scene_context: dict[str, Any],
    ) -> dict[str, dict[str, Any]]:
        """Return a semantic tree keyed by node ID."""

    @abstractmethod
    def answer_query(
        self,
        query: str | dict[str, Any],
        tree: dict[str, dict[str, Any]],
        views: dict[str, dict[str, Any]],
    ) -> dict[str, Any]:
        """Return a canonical-query payload without run-level metrics."""

    def stats_snapshot(self) -> dict[str, Any]:
        return deepcopy(self._stats)

    def provenance(self) -> dict[str, Any]:
        return {
            "mode": self.mode,
            "provider": self.provider,
            "model": self.model,
            "version": self.version,
            "temperature": self.temperature,
        }

    def _record_usage(self, usage: dict[str, Any] | None) -> None:
        if not isinstance(usage, dict):
            return
        aliases = {
            "input_tokens": ("input_tokens", "prompt_tokens", "input"),
            "output_tokens": ("output_tokens", "completion_tokens", "output"),
            "total_tokens": ("total_tokens", "total"),
        }
        for target, keys in aliases.items():
            value = next((usage.get(key) for key in keys if isinstance(usage.get(key), int)), None)
            if value is None:
                continue
            current = self._stats[target]
            self._stats[target] = int(value) + (int(current) if current is not None else 0)


_STOPWORDS = {
    "a", "an", "the", "to", "is", "in", "on", "at", "for", "of", "and", "or",
    "find", "where", "what", "which", "how", "me", "my", "can", "could", "please",
    "there", "all", "inside", "area", "someone", "people", "guests",
}

_SYNONYMS = {
    "slides": {"projection", "screen", "presentation"},
    "presenter": {"presentation", "podium", "lectern", "screen"},
    "drinks": {"bar", "hospitality"},
    "check": {"reception"},
    "emergency": {"exit", "egress"},
    "leave": {"exit", "egress"},
    "catering": {"service", "prep", "plates"},
    "play": {"piano", "performance"},
    "av": {"projector", "equipment", "presentation"},
}


def _tokens(text: str) -> set[str]:
    values = {token for token in re.findall(r"[a-z0-9]+", text.lower()) if token not in _STOPWORDS}
    expanded = set(values)
    for value in values:
        expanded.update(_SYNONYMS.get(value, set()))
    return expanded


def _view_text(view: dict[str, Any]) -> str:
    pieces: list[str] = [
        str(view.get("scene_summary", "")),
        str(view.get("summary", "")),
        str(view.get("room_type", "")),
        str(view.get("facing", "")),
        str(view.get("functional_context", "")),
        str(view.get("free_text_notes", "")),
    ]
    pieces.extend(str(value) for value in view.get("spatial_relations", []) if value is not None)
    for region in view.get("visible_regions", []):
        if isinstance(region, dict):
            pieces.extend((str(region.get("label", "")), str(region.get("approx_location", ""))))
    for obj in _view_objects(view):
        if not isinstance(obj, dict):
            continue
        pieces.append(str(obj.get("label", "")))
        pieces.append(str(obj.get("approx_location", "")))
        attributes = obj.get("attributes")
        if isinstance(attributes, dict):
            pieces.extend(str(value) for value in attributes.values() if value is not None)
        elif isinstance(attributes, list):
            pieces.extend(str(value) for value in attributes if value is not None)
    for landmark in view.get("landmarks", []):
        if isinstance(landmark, dict):
            pieces.extend(
                (
                    str(landmark.get("label", "")),
                    str(landmark.get("kind", "")),
                    str(landmark.get("approx_location", "")),
                )
            )
    return " ".join(pieces)


def _view_objects(view: dict[str, Any]) -> list[dict[str, Any]]:
    value = view.get("visible_objects")
    if not isinstance(value, list):
        value = view.get("objects", [])
    return [item for item in value if isinstance(item, dict)] if isinstance(value, list) else []


def _score(text: str, query_tokens: set[str]) -> tuple[int, float]:
    haystack = _tokens(text)
    overlap = len(query_tokens & haystack)
    ratio = overlap / len(query_tokens) if query_tokens else 0.0
    return overlap, ratio


def _node_type(node: dict[str, Any]) -> str:
    return str(node.get("node_type", node.get("type", "")))


def _node_id(node: dict[str, Any], fallback: str) -> str:
    return str(node.get("node_id") or fallback)


def _reachable_tree(tree: dict[str, dict[str, Any]]) -> tuple[str | None, set[str], dict[str, str]]:
    root_id = next((key for key, node in tree.items() if _node_type(node) == "root"), None)
    if root_id is None:
        return None, set(tree), {}
    reachable: set[str] = set()
    parents: dict[str, str] = {}
    stack = [root_id]
    while stack:
        current = stack.pop()
        if current in reachable or current not in tree:
            continue
        reachable.add(current)
        for child in tree[current].get("children_ids", []):
            child_id = str(child)
            if child_id in tree:
                parents[child_id] = current
                stack.append(child_id)
    return root_id, reachable, parents


def _path_to(root_id: str | None, target_id: str | None, parents: dict[str, str]) -> list[str]:
    if target_id is None:
        return [root_id] if root_id else []
    path = [target_id]
    while path[-1] in parents:
        path.append(parents[path[-1]])
    path.reverse()
    if root_id and (not path or path[0] != root_id):
        path.insert(0, root_id)
    return path


class StubModelClient(ModelClient):
    """Deterministic semantic-index fallback with no external model calls."""

    def __init__(self, *, temperature: float = 0.0) -> None:
        super().__init__(
            mode="stub",
            provider="deterministic_local",
            model="semantic_index_lexical_v1",
            version="1",
            temperature=temperature,
        )

    def describe_view(self, image_path: str | Path, metadata: dict[str, Any]) -> dict[str, Any]:
        existing = metadata.get("existing_analysis")
        if isinstance(existing, dict):
            return deepcopy(existing)
        view_id = str(metadata.get("view_id") or Path(image_path).stem)
        return {
            "view_id": view_id,
            "scene_summary": "No saved semantic description is available for this view.",
            "room_type": "unknown",
            "lighting": "unknown",
            "objects": [],
            "spatial_relations": [],
            "functional_context": None,
            "facing": "unknown",
            "visible_landmarks": [],
        }

    def build_tree(
        self,
        view_summaries: dict[str, dict[str, Any]],
        scene_context: dict[str, Any],
    ) -> dict[str, dict[str, Any]]:
        existing = scene_context.get("existing_tree")
        if isinstance(existing, dict) and existing:
            return deepcopy(existing)
        view_ids = sorted(view_summaries)
        return {
            "root_stub": {
                "node_id": "root_stub",
                "type": "root",
                "name": "Deterministic stub root",
                "summary": "Flat fallback tree because no saved hierarchy was available.",
                "view_ids": [],
                "children_ids": ["leaf_stub_all_views"],
            },
            "leaf_stub_all_views": {
                "node_id": "leaf_stub_all_views",
                "type": "leaf",
                "name": "All indexed views",
                "summary": "Deterministic flat fallback containing every selected view.",
                "view_ids": view_ids,
                "children_ids": [],
            },
        }

    def answer_query(
        self,
        query: str | dict[str, Any],
        tree: dict[str, dict[str, Any]],
        views: dict[str, dict[str, Any]],
    ) -> dict[str, Any]:
        if isinstance(query, dict):
            query_text = str(query.get("query", ""))
            query_type = str(query.get("query_type", "simple_object"))
        else:
            query_text = str(query)
            query_type = "simple_object"

        query_tokens = _tokens(query_text)
        ranked: list[tuple[int, float, str, dict[str, Any]]] = []
        for view_id, view in views.items():
            overlap, ratio = _score(_view_text(view), query_tokens)
            ranked.append((overlap, ratio, view_id, view))
        ranked.sort(key=lambda item: (item[0], item[1], item[2]), reverse=True)

        best_overlap, best_ratio, best_view_id, best_view = ranked[0] if ranked else (0, 0.0, "", {})
        found = best_overlap > 0
        matched_object: str | None = None
        bbox_2d: Any = None
        if found:
            object_candidates = []
            for obj in _view_objects(best_view):
                overlap, ratio = _score(str(obj.get("label", "")), query_tokens)
                object_candidates.append((overlap, ratio, str(obj.get("label", "")), obj.get("bbox_2d")))
            object_candidates.sort(reverse=True)
            if object_candidates and object_candidates[0][0] > 0:
                _, _, matched_object, bbox_2d = object_candidates[0]
            else:
                matched_object = next(
                    (str(obj.get("label")) for obj in _view_objects(best_view) if obj.get("label")),
                    None,
                )

        root_id, reachable, parents = _reachable_tree(tree)
        selected_node_id = None
        if found:
            candidates = []
            for key, node in tree.items():
                node_id = _node_id(node, key)
                if node_id not in reachable or best_view_id not in as_string_ids(node.get("view_ids")):
                    continue
                depth = len(_path_to(root_id, node_id, parents))
                candidates.append((depth, node_id))
            if candidates:
                candidates.sort(reverse=True)
                selected_node_id = candidates[0][1]
        visited_nodes = _path_to(root_id, selected_node_id, parents)
        if not found and root_id:
            visited_nodes = [root_id]
            visited_nodes.extend(str(child) for child in tree[root_id].get("children_ids", []) if str(child) in tree)

        selected_views = [best_view_id] if found else []
        checked_view_ids = sorted(views)
        target = " ".join(sorted(query_tokens))
        return {
            "structured_plan": {
                "target": target,
                "query_type": query_type,
                "parser": "deterministic_tokenizer_v1",
            },
            "visited_nodes": visited_nodes,
            "selected_views": selected_views,
            "checked_view_ids": checked_view_ids,
            "result": {
                "found": found,
                "matched_object": matched_object,
                "selected_node_id": selected_node_id,
                "selected_view_id": best_view_id if found else None,
                "bbox_2d": bbox_2d,
                "bbox_3d": None,
                "camera_pose": None,
                "confidence": round(best_ratio, 4) if found else 0.0,
                "explanation": (
                    f"Deterministic lexical fallback selected {best_view_id} with {best_overlap} token matches."
                    if found
                    else "Deterministic lexical fallback found no matching semantic-index tokens."
                ),
            },
            "warnings": [
                "Stub mode uses deterministic lexical matching over saved semantic descriptions.",
                "This result is not live or cached-live model reasoning.",
            ],
        }


def as_string_ids(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value]


class CachedModelClient(ModelClient):
    """Replay raw responses whose cache provenance identifies a live source."""

    def __init__(self, cache_dir: str | Path, *, temperature: float = 0.0) -> None:
        super().__init__(
            mode="cached_live",
            provider="cache_replay",
            model=None,
            version=CACHE_SCHEMA,
            temperature=temperature,
        )
        self.cache_dir = Path(cache_dir)

    @staticmethod
    def request_hash(method: str, payload: dict[str, Any]) -> str:
        canonical = json.dumps(
            {"method": method, "payload": payload},
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            default=str,
        )
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def cache_path(self, method: str, payload: dict[str, Any]) -> Path:
        return self.cache_dir / method / f"{self.request_hash(method, payload)}.json"

    @staticmethod
    def write_cache_entry(
        cache_dir: str | Path,
        method: str,
        payload: dict[str, Any],
        response: dict[str, Any],
        *,
        provider: str,
        model: str,
        version: str | None = None,
        token_usage: dict[str, Any] | None = None,
    ) -> Path:
        client = CachedModelClient(cache_dir)
        path = client.cache_path(method, payload)
        path.parent.mkdir(parents=True, exist_ok=True)
        envelope = {
            "cache_schema": CACHE_SCHEMA,
            "source_mode": "live",
            "provider": provider,
            "model": model,
            "version": version,
            "request_hash": path.stem,
            "method": method,
            "token_usage": token_usage,
            "response": response,
        }
        path.write_text(json.dumps(envelope, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return path

    def _replay(self, method: str, payload: dict[str, Any]) -> dict[str, Any]:
        path = self.cache_path(method, payload)
        if not path.exists():
            self._stats["failure_count"] += 1
            raise ModelCacheError(f"Missing cached-live response: {path}")
        try:
            envelope = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            self._stats["failure_count"] += 1
            raise ModelCacheError(f"Invalid cache file {path}: {exc}") from exc
        if envelope.get("cache_schema") != CACHE_SCHEMA or envelope.get("source_mode") != "live":
            self._stats["failure_count"] += 1
            raise ModelCacheError(f"Cache entry is not verified live provenance: {path}")
        if envelope.get("request_hash") != path.stem or envelope.get("method") != method:
            self._stats["failure_count"] += 1
            raise ModelCacheError(f"Cache request metadata mismatch: {path}")
        response = envelope.get("response")
        if not isinstance(response, dict):
            self._stats["failure_count"] += 1
            raise ModelCacheError(f"Cache response must be a JSON object: {path}")
        self._stats["cache_hits"] += 1
        self._record_usage(envelope.get("token_usage"))
        self.provider = str(envelope.get("provider") or "cache_replay")
        self.model = str(envelope.get("model") or "unknown")
        self.version = str(envelope.get("version")) if envelope.get("version") is not None else None
        return deepcopy(response)

    def describe_view(self, image_path: str | Path, metadata: dict[str, Any]) -> dict[str, Any]:
        payload = {"image_path": str(image_path), "metadata": metadata}
        return self._replay("describe_view", payload)

    def build_tree(
        self,
        view_summaries: dict[str, dict[str, Any]],
        scene_context: dict[str, Any],
    ) -> dict[str, dict[str, Any]]:
        payload = {"view_summaries": view_summaries, "scene_context": scene_context}
        response = self._replay("build_tree", payload)
        return response

    def answer_query(
        self,
        query: str | dict[str, Any],
        tree: dict[str, dict[str, Any]],
        views: dict[str, dict[str, Any]],
    ) -> dict[str, Any]:
        payload = {"query": query, "tree": tree, "views": views}
        return self._replay("answer_query", payload)


def create_model_client(
    mode: str,
    *,
    cache_dir: str | Path | None = None,
    temperature: float = 0.0,
) -> ModelClient:
    """Create a configured client without embedding credentials in code."""
    if temperature != 0:
        raise ModelConfigurationError("Evaluation clients require temperature=0")
    if mode == "stub":
        return StubModelClient(temperature=temperature)
    if mode == "cached_live":
        if cache_dir is None:
            raise ModelConfigurationError("cached_live mode requires a model_cache directory")
        return CachedModelClient(cache_dir, temperature=temperature)
    if mode == "live":
        provider = os.getenv("SEMANTICSPLAT_PROVIDER")
        model = os.getenv("SEMANTICSPLAT_MODEL")
        api_key = os.getenv("SEMANTICSPLAT_API_KEY")
        missing = [
            name
            for name, value in (
                ("SEMANTICSPLAT_PROVIDER", provider),
                ("SEMANTICSPLAT_MODEL", model),
                ("SEMANTICSPLAT_API_KEY", api_key),
            )
            if not value
        ]
        if missing:
            raise ModelConfigurationError(
                "live mode is unavailable; missing environment variables: " + ", ".join(missing)
            )
        raise ModelConfigurationError(
            f"live credentials are configured for provider '{provider}', but no provider adapter is installed"
        )
    raise ModelConfigurationError(f"Unsupported mode: {mode}")
