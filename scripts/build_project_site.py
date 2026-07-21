#!/usr/bin/env python3
"""Assemble the static SemanticSplat project site from tracked evidence."""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "site"
DEFAULT_OUTPUT = ROOT / "site-dist"

ASSETS = {
    ROOT / "backend/data/scenes/ConferenceHall-capture-pilot/images/v018.png": "assets/hero-conference-hall.png",
    ROOT / "papers/twinworld/figures/fig_method_workflow.png": "assets/method-workflow.png",
    ROOT / "papers/twinworld/figures/fig_tree_traversal.png": "assets/tree-traversal.png",
    ROOT / "papers/twinworld/figures/fig_evaluation_protocol.png": "assets/evaluation-protocol.png",
    ROOT / "papers/twinworld/figures/fig_five_scene_summary.png": "assets/five-scene-summary.png",
    ROOT / "papers/twinworld/figures/fig_scannet_pilot.png": "assets/scannet-pilot.png",
    ROOT / "papers/twinworld/figures/fig_replica_pilot.png": "assets/replica-pilot.png",
    ROOT / "papers/twinworld/figures/fig_scene_gallery.png": "assets/scene-gallery.png",
    ROOT / "papers/twinworld/figures/fig_qualitative_bbox.png": "assets/qualitative-bbox.png",
    ROOT / "papers/twinworld/main_preprint.pdf": "assets/semanticsplat-paper.pdf",
    ROOT / "docs/reports/final/graph_construction_cost.json": "data/graph-construction-cost.json",
    ROOT / "outputs/graph_vs_flat/five_scene_graph_vs_flat_v2/metrics_summary.json": "data/internal-metrics.json",
}


def is_lfs_pointer(path: Path) -> bool:
    return path.stat().st_size < 1024 and path.read_bytes().startswith(
        b"version https://git-lfs.github.com/spec"
    )


def prepare_output(output: Path) -> None:
    resolved = output.resolve()
    if resolved.parent != ROOT.resolve() or resolved.name != "site-dist":
        raise ValueError(f"Refusing to replace unexpected site output: {resolved}")
    if resolved.exists():
        shutil.rmtree(resolved)
    resolved.mkdir(parents=True)


def build(output: Path) -> dict[str, object]:
    prepare_output(output)
    for source_path in SOURCE.rglob("*"):
        if not source_path.is_file() or source_path.name == "README.md":
            continue
        relative = source_path.relative_to(SOURCE)
        destination = output / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, destination)

    copied_assets: list[str] = []
    for source_path, relative in ASSETS.items():
        if not source_path.is_file():
            raise FileNotFoundError(f"Required site artifact is missing: {source_path}")
        if is_lfs_pointer(source_path):
            raise RuntimeError(f"Required LFS asset is still a pointer; run git lfs pull: {source_path}")
        destination = output / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, destination)
        copied_assets.append(relative)

    (output / ".nojekyll").write_text("\n", encoding="ascii")
    shutil.copy2(output / "index.html", output / "404.html")
    report = {
        "output": str(output),
        "asset_count": len(copied_assets),
        "assets": copied_assets,
        "licensed_raw_data_included": False,
    }
    (output / "build-manifest.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    report = build(args.output)
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
