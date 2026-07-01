#!/usr/bin/env python3
"""Query a real ConceptGraphs map and emit strict native smoke evidence."""
from __future__ import annotations

import argparse
import gzip
import json
import pickle
import time
from pathlib import Path

import numpy as np
import open_clip
import torch
import torch.nn.functional as functional

from conceptgraph.slam.slam_classes import MapObjectList


def _bbox_record(obj: dict) -> dict | None:
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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--map", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--scene-id", required=True)
    parser.add_argument("--query-id", required=True)
    parser.add_argument("--query", required=True)
    parser.add_argument("--selected-view-id", required=True)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--native-command", required=True)
    parser.add_argument("--artifact-record", action="append", required=True)
    args = parser.parse_args()

    if not args.map.is_file():
        raise SystemExit(f"ConceptGraphs map does not exist: {args.map}")

    started = time.perf_counter()
    with gzip.open(args.map, "rb") as handle:
        native_map = pickle.load(handle)
    serialized_objects = native_map.get("objects")
    if not isinstance(serialized_objects, list) or not serialized_objects:
        raise SystemExit("ConceptGraphs native map contains no objects")

    objects = MapObjectList(device="cuda")
    objects.load_serializable(serialized_objects)
    model, _, _ = open_clip.create_model_and_transforms(
        "ViT-H-14", pretrained="laion2b_s32b_b79k"
    )
    model = model.eval().cuda()
    tokenizer = open_clip.get_tokenizer("ViT-H-14")
    with torch.no_grad():
        tokens = tokenizer([args.query]).cuda()
        query_feature = model.encode_text(tokens)
        query_feature /= query_feature.norm(dim=-1, keepdim=True)
        object_features = objects.get_stacked_values_torch("clip_ft").cuda()
        object_features /= object_features.norm(dim=-1, keepdim=True)
        similarities = functional.cosine_similarity(query_feature, object_features, dim=-1)
        probabilities = functional.softmax(similarities, dim=0)
        index = int(torch.argmax(probabilities).item())

    selected = objects[index]
    runtime = time.perf_counter() - started
    selected_id = str(selected.get("id", f"object_{index}"))
    matched_object = str(selected.get("class_name", "unknown"))
    confidence = float(similarities[index].item())
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
                "laion/CLIP-ViT-H-14-laion2b_s32b_b79k",
            ],
            "native_artifacts": args.artifact_record,
        },
        "predictions": [{
            "query_id": args.query_id,
            "found": True,
            "matched_object": matched_object,
            "selected_object_id": selected_id,
            "selected_view_ids": [args.selected_view_id],
            "trace_node_ids": [selected_id],
            "confidence": confidence,
            "bbox_2d": None,
            "bbox_3d": _bbox_record(selected),
            "native_query_type": "clip_object_map_retrieval",
            "explanation": (
                f"Native ConceptGraphs CLIP retrieval selected object {index} "
                f"with class '{matched_object}' and cosine similarity {confidence:.6f}."
            ),
            "metrics": {
                "runtime_seconds": runtime,
                "stage_runtime_seconds": {"native_map_query": runtime},
                "model_call_count": 1,
                "cache_hits": 0,
                "checked_view_count": 1,
                "construction_cost": {"native_map_object_count": len(objects)},
            },
            "warnings": [
                "The captured scene has no independent semantic GT; this smoke proves native execution, not accuracy."
            ],
        }],
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(f"ConceptGraphs native query wrote {args.out}")


if __name__ == "__main__":
    main()
