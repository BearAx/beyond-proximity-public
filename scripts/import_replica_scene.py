"""Import Nikita's unified scene format into backend/data/scenes/<scene_id>/.

Input layout (Week 1):
  scene/
    rgb/
    depth/
    poses.json
    intrinsics.json
    metadata.json

Output layout (backend):
  backend/data/scenes/<scene_id>/
    transforms.json
    images/
    depths/
"""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)


def import_scene(input_dir: Path, scene_id: str, backend_root: Path) -> Path:
    poses_path = input_dir / "poses.json"
    intrinsics_path = input_dir / "intrinsics.json"
    if not poses_path.exists():
        raise FileNotFoundError(f"Missing poses.json: {poses_path}")
    if not intrinsics_path.exists():
        raise FileNotFoundError(f"Missing intrinsics.json: {intrinsics_path}")

    poses = load_json(poses_path)
    intrinsics = load_json(intrinsics_path)
    frames_in = poses.get("frames", [])
    if not frames_in:
        raise ValueError(f"No frames in {poses_path}")

    scene_dir = backend_root / "backend" / "data" / "scenes" / scene_id
    images_dir = scene_dir / "images"
    depths_dir = scene_dir / "depths"
    images_dir.mkdir(parents=True, exist_ok=True)
    depths_dir.mkdir(parents=True, exist_ok=True)

    backend_frames = []
    for frame in frames_in:
        view_id = frame.get("view_id") or f"v{frame['frame_index'] + 1:03d}"
        rgb_src = input_dir / frame["rgb_file"]
        depth_src = input_dir / frame["depth_file"]
        if not rgb_src.exists():
            raise FileNotFoundError(f"Missing RGB file: {rgb_src}")
        if not depth_src.exists():
            raise FileNotFoundError(f"Missing depth file: {depth_src}")

        rgb_name = f"{view_id}.png"
        depth_name = f"{view_id}_depth.npy"
        shutil.copy2(rgb_src, images_dir / rgb_name)
        shutil.copy2(depth_src, depths_dir / depth_name)

        backend_frames.append({
            "file_path": f"images/{rgb_name}",
            "depth_file_path": f"depths/{depth_name}",
            "view_id": view_id,
            "transform_matrix": frame["transform_matrix"],
        })

    transforms = {
        "fl_x": intrinsics.get("fx", intrinsics.get("fl_x", 800.0)),
        "fl_y": intrinsics.get("fy", intrinsics.get("fl_y", 800.0)),
        "cx": intrinsics.get("cx", 400.0),
        "cy": intrinsics.get("cy", 300.0),
        "w": intrinsics.get("width", 800),
        "h": intrinsics.get("height", 600),
        "camera_model": intrinsics.get("camera_model", "OPENCV"),
        "frames": backend_frames,
    }
    write_json(scene_dir / "transforms.json", transforms)

    metadata_src = input_dir / "metadata.json"
    if metadata_src.exists():
        shutil.copy2(metadata_src, scene_dir / "source_metadata.json")

    return scene_dir, metadata_src if metadata_src.exists() else None


def print_metadata_warnings(metadata_path: Path | None) -> None:
    if metadata_path is None:
        return
    metadata = load_json(metadata_path)
    for warning in metadata.get("warnings", []):
        print(f"WARNING: {warning}")


def copy_annotations(from_scene_id: str, to_scene_dir: Path, backend_root: Path) -> None:
    src = backend_root / "backend" / "data" / "scenes" / from_scene_id
    for sub in ("views", "tree"):
        src_dir = src / sub
        if not src_dir.exists():
            continue
        dst_dir = to_scene_dir / sub
        if dst_dir.exists():
            shutil.rmtree(dst_dir)
        shutil.copytree(src_dir, dst_dir)


def main() -> None:
    parser = argparse.ArgumentParser(description="Import unified RGB-D scene into backend format.")
    parser.add_argument("--input", required=True, help="Input scene folder, e.g. data/replica/pilot_scene_001")
    parser.add_argument("--scene-id", required=True, help="Backend scene id, e.g. replica_pilot_001")
    parser.add_argument(
        "--copy-annotations-from",
        default=None,
        help="Optional existing backend scene id whose views/tree should be copied (stub helper).",
    )
    parser.add_argument(
        "--backend-root",
        default=".",
        help="Project root containing backend/ (default: current directory).",
    )
    args = parser.parse_args()

    backend_root = Path(args.backend_root).resolve()
    scene_dir, metadata_path = import_scene(Path(args.input).resolve(), args.scene_id, backend_root)
    print(f"Imported scene to {scene_dir}")
    print_metadata_warnings(metadata_path)

    if args.copy_annotations_from:
        copy_annotations(args.copy_annotations_from, scene_dir, backend_root)
        print(f"Copied views/tree from '{args.copy_annotations_from}'")


if __name__ == "__main__":
    main()
