#!/usr/bin/env python3
"""Batch-query rendered LangSplat feature maps for one public RGB-D scene."""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np
import open_clip
import torch

sys.path.insert(0, "/opt/langsplat")
from autoencoder.model import Autoencoder  # noqa: E402


NEGATIVES = ("object", "things", "stuff", "texture")


def token_usage(row: torch.Tensor) -> dict[str, Any]:
    count = int(torch.count_nonzero(row).item())
    return {
        "input_tokens": count,
        "output_tokens": 0,
        "total_tokens": count,
        "tokenizer": "open_clip:ViT-B-16",
        "token_count_type": "non_padding_text_encoder_tokens",
        "provider_billing_tokens": False,
        "encoded_by_model": True,
    }


def bbox_bounds(box: Any) -> tuple[np.ndarray, np.ndarray] | None:
    if not isinstance(box, dict):
        return None
    low = box.get("min") or box.get("minimum")
    high = box.get("max") or box.get("maximum")
    if low is None or high is None:
        center, size = box.get("center"), box.get("size")
        if center is None or size is None:
            return None
        center_array = np.asarray(center, dtype=float)
        half = np.asarray(size, dtype=float) / 2.0
        return center_array - half, center_array + half
    return np.asarray(low, dtype=float), np.asarray(high, dtype=float)


def ground_point(
    x: int,
    y: int,
    view_id: str,
    scene_root: Path,
    frame: dict[str, Any],
    intrinsics: dict[str, float],
) -> list[float] | None:
    depth_path = scene_root / "depth" / f"{view_id}.npy"
    if not depth_path.is_file():
        return None
    depth = np.load(depth_path)
    if not (0 <= y < depth.shape[0] and 0 <= x < depth.shape[1]):
        return None
    z = float(depth[y, x])
    if not np.isfinite(z) or z <= 0:
        return None
    camera = np.array([
        (x - intrinsics["cx"]) * z / intrinsics["fx"],
        (y - intrinsics["cy"]) * z / intrinsics["fy"],
        z,
        1.0,
    ])
    c2w = np.asarray(frame["camera_to_world"], dtype=float)
    return (c2w @ camera)[:3].tolist()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--features-dir", type=Path, required=True)
    parser.add_argument("--ae-checkpoint", type=Path, required=True)
    parser.add_argument("--clip-checkpoint", required=True)
    parser.add_argument("--benchmark", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--scene-root", type=Path, required=True)
    parser.add_argument("--scene-id", required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--native-command", required=True)
    parser.add_argument("--artifact-record", action="append", required=True)
    parser.add_argument("--chunk-size", type=int, default=32768)
    args = parser.parse_args()
    if not torch.cuda.is_available():
        raise SystemExit("LangSplat native batch query requires CUDA")
    for path in (args.features_dir, args.ae_checkpoint, args.benchmark, args.manifest):
        if not path.exists():
            raise SystemExit(f"Missing LangSplat input: {path}")

    benchmark = json.loads(args.benchmark.read_text(encoding="utf-8"))
    queries = [
        query for query in benchmark.get("queries", [])
        if isinstance(query, dict) and str(query.get("scene_id")) == args.scene_id
    ]
    if not queries:
        raise SystemExit(f"No benchmark queries for {args.scene_id}")
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    frames = manifest.get("frames")
    intrinsics = manifest.get("intrinsics")
    feature_paths = sorted(args.features_dir.glob("*.npy"))
    if not isinstance(frames, list) or len(feature_paths) != len(frames):
        raise SystemExit("Rendered feature maps do not match conversion manifest frames")
    if not isinstance(intrinsics, dict):
        raise SystemExit("Conversion manifest lacks intrinsics")

    started = time.perf_counter()
    device = torch.device("cuda")
    decoder = Autoencoder([256, 128, 64, 32, 3], [16, 32, 64, 128, 256, 256, 512]).to(device)
    decoder.load_state_dict(torch.load(args.ae_checkpoint, map_location=device))
    decoder.eval()
    model, _, _ = open_clip.create_model_and_transforms(
        "ViT-B-16", pretrained=args.clip_checkpoint, precision="fp16"
    )
    model = model.eval().to(device)
    tokenizer = open_clip.get_tokenizer("ViT-B-16")
    query_texts = [str(query["query"]) for query in queries]
    query_tokens = tokenizer(query_texts).to(device)
    negative_tokens = tokenizer(list(NEGATIVES)).to(device)
    with torch.no_grad():
        query_embeddings = model.encode_text(query_tokens)
        negative_embeddings = model.encode_text(negative_tokens)
        query_embeddings /= query_embeddings.norm(dim=-1, keepdim=True)
        negative_embeddings /= negative_embeddings.norm(dim=-1, keepdim=True)

    best_scores = torch.full((len(queries),), -1.0, device=device)
    best_indices = torch.full((len(queries),), -1, dtype=torch.long, device=device)
    best_views = torch.full((len(queries),), -1, dtype=torch.long, device=device)
    map_shapes: list[list[int]] = []
    with torch.no_grad():
        for view_index, feature_path in enumerate(feature_paths):
            compressed = np.load(feature_path)
            if compressed.ndim != 3 or compressed.shape[-1] != 3:
                raise SystemExit(f"Expected HxWx3 feature map, got {compressed.shape}")
            map_shapes.append(list(compressed.shape))
            flat = torch.from_numpy(compressed.reshape(-1, 3)).float()
            for offset in range(0, flat.shape[0], args.chunk_size):
                restored = decoder.decode(flat[offset:offset + args.chunk_size].to(device))
                positive = restored @ query_embeddings.to(restored.dtype).T
                negative = restored @ negative_embeddings.to(restored.dtype).T
                pairwise = torch.stack((
                    positive.unsqueeze(-1).expand(-1, -1, len(NEGATIVES)),
                    negative.unsqueeze(1).expand(-1, len(queries), -1),
                ), dim=-1)
                probabilities = torch.softmax(10 * pairwise, dim=-1)[..., 0]
                relevance = probabilities.min(dim=-1).values
                chunk_scores, chunk_indices = relevance.max(dim=0)
                improved = chunk_scores > best_scores
                best_scores[improved] = chunk_scores[improved]
                best_indices[improved] = offset + chunk_indices[improved]
                best_views[improved] = view_index

    runtime = time.perf_counter() - started
    predictions: list[dict[str, Any]] = []
    for query_index, query in enumerate(queries):
        view_index = int(best_views[query_index].item())
        frame = frames[view_index]
        view_id = str(frame["view_id"])
        height, width, _ = map_shapes[view_index]
        y, x = divmod(int(best_indices[query_index].item()), width)
        point = ground_point(x, y, view_id, args.scene_root, frame, intrinsics)
        bounds = bbox_bounds(query.get("expected_bbox_3d"))
        point_inside = None
        if point is not None and bounds is not None:
            point_array = np.asarray(point)
            point_inside = bool(np.all(point_array >= bounds[0]) and np.all(point_array <= bounds[1]))
        score = float(best_scores[query_index].item())
        predictions.append({
            "query_id": str(query["query_id"]),
            "found": score >= 0.5,
            "matched_label": str(query["query"]),
            "selected_view_id": view_id,
            "trace": ["language_field", "feature_level_3", f"view:{view_id}"],
            "relevancy_score": score,
            "bbox_2d": None,
            "bbox_3d": None,
            "grounded_point_3d": point,
            "point_inside_gt_bbox": point_inside,
            "feature_level": 3,
            "explanation": f"Native LangSplat relevancy peaked at ({x}, {y}) in {view_id} with score {score:.6f}.",
            "metrics": {
                "runtime_seconds": runtime / len(queries),
                "stage_runtime_seconds": {"native_language_field_batch_total": runtime},
                "model_call_count": 1,
                "cache_hits": 0,
                "token_usage": token_usage(query_tokens[query_index]),
                "checked_view_count": len(feature_paths),
                "construction_cost": {
                    "rendered_feature_map_count": len(feature_paths),
                    "feature_map_shapes": map_shapes,
                    "peak_pixel": [x, y],
                },
            },
            "warnings": [
                "Reduced-resource ScanNet pilot: 3,000 RGB and language iterations on a 6 GB GPU, not the paper's 30,000-iteration/24 GB configuration.",
                "Point-in-box is diagnostic only; no predicted 3D box is emitted, so official 3D IoU remains unavailable.",
            ],
        })

    output = {
        "provenance": {
            "native_execution": True,
            "baseline": "langsplat",
            "scene_id": args.scene_id,
            "repository": "https://github.com/minghanqin/LangSplat",
            "revision": args.revision,
            "command": args.native_command,
            "checkpoints": [
                "locally trained ScanNet RGB 3DGS checkpoint (3000 iterations)",
                "locally trained ScanNet LangSplat feature-level-3 checkpoint (3000 iterations)",
                "locally trained scene autoencoder",
                "laion/CLIP-ViT-B-16-laion2b_s34b_b88k",
            ],
            "native_artifacts": args.artifact_record,
        },
        "predictions": predictions,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(f"LangSplat batch query wrote {len(predictions)} predictions to {args.out}")


if __name__ == "__main__":
    main()
