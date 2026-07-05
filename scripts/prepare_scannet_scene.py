from pathlib import Path
import argparse
import json
import shutil


def write_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Prepare ScanNet scene skeleton into unified format.")
    parser.add_argument("--input", required=True, help="Extracted ScanNet scene folder, e.g. scene0000_00")
    parser.add_argument("--output", required=True, help="Output folder, e.g. data/scannet/scene0000_00")
    args = parser.parse_args()

    src = Path(args.input)
    out = Path(args.output)

    # Common ScanNet extracted structure usually contains color/, depth/, pose/, intrinsic/.
    color = src / "color"
    depth = src / "depth"
    pose = src / "pose"
    intrinsic = src / "intrinsic"

    missing = [str(p) for p in [color, depth, pose, intrinsic] if not p.exists()]
    if missing:
        raise FileNotFoundError(
            "Missing expected ScanNet folders. Need extracted ScanNet data first: " + ", ".join(missing)
        )

    raise NotImplementedError(
        "ScanNet conversion needs a real extracted ScanNet scene. This skeleton validates folder availability only. "
        "Next step: parse intrinsic_depth.txt / intrinsic_color.txt and pose/*.txt."
    )


if __name__ == "__main__":
    main()
