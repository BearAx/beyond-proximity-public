#!/usr/bin/env python3
"""Batch-query a native ConceptGraphs map for one SemanticSplat scene."""
from __future__ import annotations

import argparse
import gzip
import json
import pickle
import time
from pathlib import Path
from typing import Any

import numpy as np
import open_clip
import torch

from conceptgraph.slam.slam_classes import MapObjectList


def _bbox_record(obj: dict[str, Any]) -> dict[str, Any] | None:
    bbox = obj.get("bbox")
    if bbox is None:
        return None
    points = np.asarray(bbox.get_box_points(), dtype=float)
    return {
        "representation": "axis_aligned_min_max",
        "coordinate_frame": "conceptgraphs_map",
        "minimum": points.min(axis=0).tolist(),
        "maximum": points.max(axis=0).tolist(),
    }


def _bbox_2d(obj: dict[str, Any], width: int, height: int) -> list[float] | None:
    boxes = obj.get("xyxy")
    if not boxes:
        return None
    box = np.asarray(boxes[0], dtype=float).reshape(-1)
    if box.size != 4 or width <= 0 or height <= 0:
        return None
    x1, y1, x2, y2 = box.tolist()
    return [
        max(0.0, min(1.0, x1 / width)),
        max(0.0, min(1.0, y1 / height)),
        max(0.0, min(1.0, x2 / width)),
        max(0.0, min(1.0, y2 / height)),
    ]


def _view_ids_for_object(obj: dict[str, Any], manifest: dict[str, Any]) -> list[str]:
    frames = manifest.get("frames", [])
    if not isinstance(frames, list):
        frames = []
    ids: list[str] = []
    for raw_index in obj.get("image_idx") or []:
        try:
            index = int(raw_index)
        except (TypeError, ValueError):
            continue
        if 0 <= index < len(frames) and isinstance(frames[index], dict):
            view_id = frames[index].get("view_id")
            if view_id is not None:
                ids.append(str(view_id))
    return sorted(set(ids))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--map", type=Path, required=True)
    parser.add_argument("--benchmark", type=Path, required=True)
    parser.add_argument("--benchmark-scene-id", required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--scene-id", required=True)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--native-command", required=True)
    parser.add_argument("--artifact-record", action="append", required=True)
    parser.add_argument("--image-width", type=int, default=640)
    parser.add_argument("--image-height", type=int, default=320)
    args = parser.parse_args()

    if not args.map.is_file():
        raise SystemExit(f"ConceptGraphs map does not exist: {args.map}")
    if not args.benchmark.is_file():
        raise SystemExit(f"Benchmark does not exist: {args.benchmark}")
    if not args.manifest.is_file():
        raise SystemExit(f"Conversion manifest does not exist: {args.manifest}")

    benchmark = json.loads(args.benchmark.read_text(encoding="utf-8"))
    queries = [
        query
        for query in benchmark.get("queries", [])
        if isinstance(query, dict) and str(query.get("scene_id")) == args.benchmark_scene_id
    ]
    if not queries:
        raise SystemExit(f"No benchmark queries for scene {args.benchmark_scene_id}")
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))

    load_started = time.perf_counter()
    with gzip.open(args.map, "rb") as handle:
        native_map = pickle.load(handle)
    serialized_objects = native_map.get("objects")
    if not isinstance(serialized_objects, list):
        raise SystemExit("ConceptGraphs native map has invalid objects field")
    if not serialized_objects:
        load_seconds = time.perf_counter() - load_started
        predictions = []
        for query in queries:
            predictions.append({
                "query_id": str(query["query_id"]),
                "found": False,
                "matched_object": None,
                "selected_object_id": None,
                "selected_view_ids": [],
                "trace_node_ids": [],
                "confidence": None,
                "bbox_2d": None,
                "bbox_3d": None,
                "native_query_type": "empty_native_object_map",
                "explanation": (
                    "Native ConceptGraphs produced a saved map artifact, but the "
                    "serialized object map contained zero objects for this scene."
                ),
                "metrics": {
                    "runtime_seconds": 0.0,
                    "stage_runtime_seconds": {
                        "native_map_load": load_seconds,
                        "native_batch_query_total": 0.0,
                        "native_batch_query_per_query": 0.0,
                    },
                    "model_call_count": 0,
                    "cache_hits": 0,
                    "checked_view_count": 0,
                    "failure_count": 1,
                    "construction_cost": {
                        "native_map_object_count": 0,
                        "scene_query_count": len(queries),
                    },
                },
                "warnings": [
                    "Native ConceptGraphs detection/mapping completed with a saved map artifact, but no objects were available for retrieval.",
                    "This is recorded as an explicit baseline miss, not as a semantic answer.",
                ],
            })
        output = {
            "provenance": {
                "native_execution": True,
                "baseline": "conceptgraphs",
                "scene_id": args.scene_id,
                "repository": "https://github.com/concept-graphs/concept-graphs",
                "revision": args.revision,
                "command": args.native_command,
                "checkpoints": [
                    "ultralytics/yolov8l-world.pt",
                    "ultralytics/mobile_sam.pt",
                    "laion/CLIP-ViT-H-14-laion2b_s32b_b79K",
                ],
                "native_artifacts": args.artifact_record,
            },
            "predictions": predictions,
        }
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
        print(
            "ConceptGraphs native map contained zero objects; "
            f"wrote {len(predictions)} explicit miss prediction(s) to {args.out}"
        )
        return

    objects = MapObjectList(device="cuda")
    objects.load_serializable(serialized_objects)
    model, _, _ = open_clip.create_model_and_transforms(
        "ViT-H-14", pretrained="laion2b_s32b_b79k"
    )
    model = model.eval().cuda()
    tokenizer = open_clip.get_tokenizer("ViT-H-14")
    object_features = objects.get_stacked_values_torch("clip_ft").cuda()
    object_features /= object_features.norm(dim=-1, keepdim=True)
    load_seconds = time.perf_counter() - load_started

    query_started = time.perf_counter()
    query_texts = [str(query["query"]) for query in queries]
    with torch.no_grad():
        tokens = tokenizer(query_texts).cuda()
        query_features = model.encode_text(tokens)
        query_features /= query_features.norm(dim=-1, keepdim=True)
        similarities = query_features @ object_features.T
        top_scores, top_indices = similarities.max(dim=1)
    total_query_seconds = time.perf_counter() - query_started
    per_query_seconds = total_query_seconds / max(1, len(queries))

    predictions = []
    for query, score, index_tensor in zip(queries, top_scores, top_indices):
        index = int(index_tensor.item())
        selected = objects[index]
        selected_id = str(selected.get("id", f"object_{index}"))
        matched_object = str(selected.get("class_name", "unknown"))
        selected_views = _view_ids_for_object(selected, manifest)
        confidence = float(score.item())
        predictions.append({
            "query_id": str(query["query_id"]),
            "found": True,
            "matched_object": matched_object,
            "selected_object_id": selected_id,
            "selected_view_ids": selected_views,
            "trace_node_ids": [selected_id],
            "confidence": confidence,
            "bbox_2d": _bbox_2d(selected, args.image_width, args.image_height),
            "bbox_3d": _bbox_record(selected),
            "native_query_type": "batch_clip_object_map_retrieval",
            "explanation": (
                f"Native ConceptGraphs CLIP retrieval selected object {index} "
                f"with class '{matched_object}' and cosine similarity {confidence:.6f}."
            ),
            "metrics": {
                "runtime_seconds": per_query_seconds,
                "stage_runtime_seconds": {
                    "native_map_and_model_load": load_seconds,
                    "native_batch_query_total": total_query_seconds,
                    "native_batch_query_per_query": per_query_seconds,
                },
                "model_call_count": 1,
                "cache_hits": 0,
                "checked_view_count": len(selected_views),
                "construction_cost": {
                    "native_map_object_count": len(objects),
                    "scene_query_count": len(queries),
                },
            },
            "warnings": [
                "Native ConceptGraphs returns the top CLIP object for every query; no calibrated absence threshold is applied.",
                "Selected views are derived from native image_idx observations, not independent GT.",
            ],
        })

    output = {
        "provenance": {
            "native_execution": True,
            "baseline": "conceptgraphs",
            "scene_id": args.scene_id,
            "repository": "https://github.com/concept-graphs/concept-graphs",
            "revision": args.revision,
            "command": args.native_command,
            "checkpoints": [
                "ultralytics/yolov8l-world.pt",
                "ultralytics/mobile_sam.pt",
                "laion/CLIP-ViT-H-14-laion2b_s32b_b79K",
            ],
            "native_artifacts": args.artifact_record,
        },
        "predictions": predictions,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(
        f"ConceptGraphs batch query wrote {len(predictions)} prediction(s) to {args.out}"
    )


if __name__ == "__main__":
    main()
