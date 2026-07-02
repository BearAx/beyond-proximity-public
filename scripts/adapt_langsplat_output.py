#!/usr/bin/env python3
"""Adapt a provenance-backed LangSplat JSON export to canonical results."""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from scripts.baseline_adapter_common import BaselineAdapterError, canonical_metrics, write_adapter_run
except ModuleNotFoundError:  # Direct script execution adds scripts/ rather than the repo root.
    from baseline_adapter_common import BaselineAdapterError, canonical_metrics, write_adapter_run


def adapt_prediction(prediction: dict[str, Any], query: dict[str, Any]) -> dict[str, Any]:
    found = prediction.get("found")
    if not isinstance(found, bool):
        raise BaselineAdapterError("LangSplat prediction requires boolean found")
    selected_view = prediction.get("selected_view_id")
    selected_views = [str(selected_view)] if selected_view is not None else []
    trace = [str(value) for value in prediction.get("trace", [])]
    confidence = prediction.get("relevancy_score")
    if confidence is not None and (isinstance(confidence, bool) or not isinstance(confidence, (int, float))):
        raise BaselineAdapterError("LangSplat relevancy_score must be numeric or null")
    return {
        "structured_plan": {
            "adapter": "langsplat_native_export_v1",
            "feature_level": prediction.get("feature_level"),
        },
        "visited_nodes": trace,
        "selected_views": selected_views,
        "result": {
            "found": found,
            "matched_object": prediction.get("matched_label"),
            "selected_node_id": None,
            "selected_view_id": str(selected_view) if selected_view is not None else None,
            "bbox_2d": prediction.get("bbox_2d"),
            "bbox_3d": prediction.get("bbox_3d"),
            "camera_pose": prediction.get("camera_pose"),
            "confidence": float(confidence) if confidence is not None else None,
            "explanation": str(prediction.get("explanation", "")),
        },
        "metrics_log": canonical_metrics(prediction, trace, selected_views),
        "warnings": [str(value) for value in prediction.get("warnings", [])],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--native", type=Path, required=True)
    parser.add_argument("--benchmark", type=Path, required=True)
    parser.add_argument("--scene-id", required=True)
    parser.add_argument("--benchmark-scene-id", required=True)
    parser.add_argument("--run-id", default="langsplat_smoke_v1")
    parser.add_argument("--mode", choices=("live", "cached_live"), required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    try:
        output = write_adapter_run(
            native_path=args.native,
            benchmark_path=args.benchmark,
            output_dir=args.out,
            run_id=args.run_id,
            method="langsplat",
            mode=args.mode,
            scene_id=args.scene_id,
            benchmark_scene_id=args.benchmark_scene_id,
            adapt_prediction=adapt_prediction,
        )
    except BaselineAdapterError as exc:
        raise SystemExit(f"LangSplat adapter blocked: {exc}") from exc
    print(f"Adapted LangSplat output: {output}")


if __name__ == "__main__":
    main()
