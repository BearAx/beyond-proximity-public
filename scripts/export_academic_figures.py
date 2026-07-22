#!/usr/bin/env python3
"""Generate evidence-backed overview figures for the academic preprint."""
from __future__ import annotations

import argparse
from pathlib import Path

import export_twinworld_figures as figures


ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=ROOT / "papers" / "beyond-proximity" / "figures",
    )
    args = parser.parse_args()
    figures.OUT = args.out_dir.resolve()
    figures._setup()
    figures.render_system_overview()
    figures.render_evaluation_protocol()
    figures.render_tree_traversal()
    figures.render_scene_gallery()
    figures.render_qualitative_bbox()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
