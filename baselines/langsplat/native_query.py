#!/usr/bin/env python3
"""Query a real rendered LangSplat feature map and emit native evidence."""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, "/opt/langsplat")
sys.path.insert(0, "/opt/langsplat/eval")

from autoencoder.model import Autoencoder  # noqa: E402
from openclip_encoder import OpenCLIPNetwork  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--feature-map", type=Path, required=True)
    parser.add_argument("--ae-checkpoint", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--scene-id", required=True)
    parser.add_argument("--query-id", required=True)
    parser.add_argument("--query", required=True)
    parser.add_argument("--selected-view-id", required=True)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--native-command", required=True)
    parser.add_argument("--artifact-record", action="append", required=True)
    parser.add_argument("--chunk-size", type=int, default=65536)
    args = parser.parse_args()

    if not args.feature_map.is_file():
        raise SystemExit(f"LangSplat rendered feature map is missing: {args.feature_map}")
    if not args.ae_checkpoint.is_file():
        raise SystemExit(f"LangSplat autoencoder checkpoint is missing: {args.ae_checkpoint}")
    if not torch.cuda.is_available():
        raise SystemExit("LangSplat native query requires CUDA")

    started = time.perf_counter()
    device = torch.device("cuda")
    compressed = np.load(args.feature_map)
    if compressed.ndim != 3 or compressed.shape[-1] != 3:
        raise SystemExit(f"Expected HxWx3 LangSplat feature map, got {compressed.shape}")

    decoder = Autoencoder(
        [256, 128, 64, 32, 3], [16, 32, 64, 128, 256, 256, 512]
    ).to(device)
    checkpoint = torch.load(args.ae_checkpoint, map_location=device)
    decoder.load_state_dict(checkpoint)
    decoder.eval()

    clip = OpenCLIPNetwork(device)
    clip.set_positives([args.query])
    phrases = torch.cat([clip.pos_embeds, clip.neg_embeds], dim=0)

    flat = torch.from_numpy(compressed.reshape(-1, 3)).float()
    best_score = -1.0
    best_index = -1
    with torch.no_grad():
        for offset in range(0, flat.shape[0], args.chunk_size):
            restored = decoder.decode(flat[offset : offset + args.chunk_size].to(device))
            logits = restored @ phrases.to(restored.dtype).T
            positive = logits[:, :1].repeat(1, len(clip.negatives))
            negatives = logits[:, 1:]
            pairwise = torch.stack((positive, negatives), dim=-1)
            softmax = torch.softmax(10 * pairwise, dim=-1)
            best_negative = softmax[..., 0].argmin(dim=1)
            relevance = torch.gather(
                softmax,
                1,
                best_negative[:, None, None].expand(-1, len(clip.negatives), 2),
            )[:, 0, 0]
            score, local_index = relevance.max(dim=0)
            score_value = float(score.item())
            if score_value > best_score:
                best_score = score_value
                best_index = offset + int(local_index.item())

    height, width, _ = compressed.shape
    y, x = divmod(best_index, width)
    runtime = time.perf_counter() - started
    output = {
        "provenance": {
            "native_execution": True,
            "baseline": "langsplat",
            "scene_id": args.scene_id,
            "repository": "https://github.com/minghanqin/LangSplat",
            "revision": args.revision,
            "command": args.native_command,
            "checkpoints": [
                "official LangSplat sofa pretrained output",
                "official LangSplat sofa autoencoder checkpoint",
                "laion/CLIP-ViT-B-16-laion2b_s34b_b88k",
            ],
            "native_artifacts": args.artifact_record,
        },
        "predictions": [{
            "query_id": args.query_id,
            "found": best_score >= 0.5,
            "matched_label": args.query,
            "selected_view_id": args.selected_view_id,
            "trace": ["language_field", "feature_level_1"],
            "relevancy_score": best_score,
            "bbox_2d": None,
            "bbox_3d": None,
            "feature_level": 1,
            "explanation": (
                f"Native LangSplat feature query peaked at pixel ({x}, {y}) "
                f"with official relevancy score {best_score:.6f}."
            ),
            "metrics": {
                "runtime_seconds": runtime,
                "stage_runtime_seconds": {"native_language_field_query": runtime},
                "model_call_count": 1,
                "cache_hits": 0,
                "checked_view_count": 1,
                "construction_cost": {
                    "feature_map_shape": list(compressed.shape),
                    "peak_pixel": [x, y],
                },
            },
            "warnings": [
                "Official pretrained sofa smoke scene is separate from the SemanticSplat five-scene benchmark."
            ],
        }],
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(f"LangSplat native query wrote {args.out}")


if __name__ == "__main__":
    main()
