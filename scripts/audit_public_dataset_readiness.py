#!/usr/bin/env python3
"""Audit whether Replica/ScanNet-style public dataset evaluation is ready."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.import_replica_scene import detect_layout  # noqa: E402


REQUIRED_REPLICA_FILES = ("rgb", "depth", "poses.json", "intrinsics.json")
REQUIRED_SCANNET_FOLDERS = ("color", "depth", "pose", "intrinsic")
CAPTURED_PILOT_SCENES = {
    "ConferenceHall-capture-pilot",
    "Museume-capture",
    "Theater-capture",
    "outdoor-drone-capture",
    "outdoor-street-capture",
}
LEGACY_SCENES = {"default"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def git_revision() -> str | None:
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    return data if isinstance(data, dict) else {}


def manual_scene_inventory(scene_root: Path) -> list[dict[str, Any]]:
    scenes = []
    for scene in sorted(scene_root.iterdir()) if scene_root.exists() else []:
        if not scene.is_dir():
            continue
        views = sorted((scene / "views").glob("*.json")) if (scene / "views").exists() else []
        transforms = load_json(scene / "transforms.json")
        frames = transforms.get("frames") if isinstance(transforms.get("frames"), list) else []
        if views or frames:
            scenes.append({
                "scene_id": scene.name,
                "category": (
                    "captured_pilot"
                    if scene.name in CAPTURED_PILOT_SCENES
                    else "legacy_demo"
                    if scene.name in LEGACY_SCENES
                    else "other"
                ),
                "view_json_count": len(views),
                "frame_count": len(frames),
                "has_tree": (scene / "tree").exists(),
                "has_manual_bbox_gt_v2": (scene / "ground_truth" / "manual_bbox_gt_v2.json").exists(),
            })
    return scenes


def replica_inventory(replica_root: Path) -> list[dict[str, Any]]:
    rows = []
    for scene in sorted(replica_root.iterdir()) if replica_root.exists() else []:
        if not scene.is_dir():
            continue
        metadata = load_json(scene / "metadata.json")
        missing = [name for name in REQUIRED_REPLICA_FILES if not (scene / name).exists()]
        try:
            layout = detect_layout(scene)
            layout_error = None
        except Exception as exc:  # noqa: BLE001 - record exact readiness blocker
            layout = None
            layout_error = str(exc)
        source_dataset = str(metadata.get("source_dataset", "unknown"))
        official = source_dataset.lower() in {"replica", "replica_dataset", "replica official", "habitat_replica"}
        rows.append({
            "scene_id": scene.name,
            "path": str(scene.relative_to(ROOT)),
            "layout": layout,
            "layout_error": layout_error,
            "missing_required": missing,
            "source_dataset": source_dataset,
            "official_public_dataset": official,
            "frame_count": metadata.get("num_frames"),
            "has_independent_gt": bool(metadata.get("has_ground_truth_labels")),
            "status": "READY_PUBLIC" if official and not missing else "PROXY_OR_NOT_READY",
        })
    return rows


def scannet_inventory(scannet_root: Path) -> list[dict[str, Any]]:
    rows = []
    for scene in sorted(scannet_root.iterdir()) if scannet_root.exists() else []:
        if not scene.is_dir():
            continue
        missing = [name for name in REQUIRED_SCANNET_FOLDERS if not (scene / name).exists()]
        rows.append({
            "scene_id": scene.name,
            "path": str(scene.relative_to(ROOT)),
            "missing_required": missing,
            "status": "READY_FOR_CONVERSION" if not missing else "NOT_READY",
        })
    return rows


def summarize(report: dict[str, Any]) -> dict[str, Any]:
    replica_ready = [row for row in report["replica"] if row["status"] == "READY_PUBLIC"]
    scannet_ready = [row for row in report["scannet"] if row["status"] == "READY_FOR_CONVERSION"]
    captured = [row for row in report["manual_scenes"] if row["category"] == "captured_pilot"]
    legacy = [row for row in report["manual_scenes"] if row["category"] == "legacy_demo"]
    return {
        "captured_pilot_scene_count": len(captured),
        "captured_pilot_view_json_count": sum(row["view_json_count"] for row in captured),
        "legacy_demo_scene_count": len(legacy),
        "legacy_demo_view_json_count": sum(row["view_json_count"] for row in legacy),
        "replica_scene_count": len(report["replica"]),
        "replica_ready_public_count": len(replica_ready),
        "scannet_scene_count": len(report["scannet"]),
        "scannet_ready_for_conversion_count": len(scannet_ready),
        "publication_readiness": {
            "twinworld_workshop": "READY_WITH_MANUAL_SCENES_PLUS_BASELINE_SMOKES",
            "aaai_main": "NOT_READY_WITHOUT_PUBLIC_DATASET_GT_AND_FAIR_BASELINES",
        },
    }


def write_markdown(report: dict[str, Any], path: Path) -> None:
    summary = report["summary"]
    lines = [
        "# Public Dataset Readiness Audit",
        "",
        f"Generated: {report['generated_at']}",
        "",
        "## Summary",
        "",
        f"- Captured pilot scenes: {summary['captured_pilot_scene_count']}",
        f"- Captured pilot ViewJSON annotations: {summary['captured_pilot_view_json_count']}",
        f"- Legacy demo scenes: {summary['legacy_demo_scene_count']}",
        f"- Legacy demo ViewJSON annotations: {summary['legacy_demo_view_json_count']}",
        f"- Replica-style local folders: {summary['replica_scene_count']}",
        f"- Official/public Replica scenes ready: {summary['replica_ready_public_count']}",
        f"- ScanNet local folders: {summary['scannet_scene_count']}",
        f"- ScanNet folders ready for conversion: {summary['scannet_ready_for_conversion_count']}",
        "",
        "## Decision",
        "",
        "- Keep the five captured scenes as pilot/system evidence.",
        "- Add official Replica first for a public-dataset workshop extension.",
        "- Add ScanNet only after Replica is reproducible; ScanNet requires licensed data access and a completed converter.",
        "- Do not call local `data/replica/pilot_scene_001` an official Replica result unless its source metadata changes to an official dataset scene.",
        "",
        "## Manual Captured Scenes",
        "",
        "| Scene | Category | ViewJSON | Frames | Tree | Manual bbox GT v2 |",
        "|---|---|---:|---:|---|---|",
    ]
    for row in report["manual_scenes"]:
        lines.append(
            f"| `{row['scene_id']}` | `{row['category']}` | {row['view_json_count']} | {row['frame_count']} | "
            f"{row['has_tree']} | {row['has_manual_bbox_gt_v2']} |"
        )
    lines.extend([
        "",
        "## Replica-Style Inputs",
        "",
        "| Scene | Status | Source dataset | Missing | Independent GT |",
        "|---|---|---|---|---|",
    ])
    if report["replica"]:
        for row in report["replica"]:
            missing = ", ".join(row["missing_required"]) if row["missing_required"] else "none"
            lines.append(
                f"| `{row['scene_id']}` | `{row['status']}` | `{row['source_dataset']}` | "
                f"{missing} | {row['has_independent_gt']} |"
            )
    else:
        lines.append("| N/A | `NOT_PRESENT` | N/A | all | false |")
    lines.extend([
        "",
        "## ScanNet Inputs",
        "",
        "| Scene | Status | Missing |",
        "|---|---|---|",
    ])
    if report["scannet"]:
        for row in report["scannet"]:
            missing = ", ".join(row["missing_required"]) if row["missing_required"] else "none"
            lines.append(f"| `{row['scene_id']}` | `{row['status']}` | {missing} |")
    else:
        lines.append("| N/A | `NOT_PRESENT` | color, depth, pose, intrinsic |")
    lines.extend([
        "",
        "## What Must Be Supplied For Public-Dataset Claims",
        "",
        "- Official Replica scene folders or a documented legal download path.",
        "- Official ScanNet extracted scene folders after accepting ScanNet terms.",
        "- Independent labels or dataset-provided instance/semantic annotations mapped to query GT.",
        "- Baseline outputs generated on the same public scenes, not only smoke scenes.",
    ])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scene-root", default="backend/data/scenes")
    parser.add_argument("--replica-root", default="data/replica")
    parser.add_argument("--scannet-root", default="data/scannet")
    parser.add_argument("--out-json", default="docs/datasets/public_dataset_readiness.json")
    parser.add_argument("--out-md", default="docs/datasets/public_dataset_readiness.md")
    args = parser.parse_args()

    report = {
        "generated_at": utc_now(),
        "git_revision": git_revision(),
        "manual_scenes": manual_scene_inventory(ROOT / args.scene_root),
        "replica": replica_inventory(ROOT / args.replica_root),
        "scannet": scannet_inventory(ROOT / args.scannet_root),
    }
    report["summary"] = summarize(report)
    out_json = ROOT / args.out_json
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_markdown(report, ROOT / args.out_md)
    print(f"Wrote public dataset readiness audit to {out_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
