#!/usr/bin/env python3
"""Generate TwinWorld qualitative / overview figures for Person 4."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "papers" / "twinworld" / "figures"

GRAPH_C = "#0b559f"
FLAT_C = "#c1440e"
OK_C = "#2a7f4f"
GRAY = "#6b7280"
SOFT = "#eef2f7"


def _setup():
    import matplotlib as mpl

    mpl.rcParams.update({
        "figure.dpi": 200,
        "savefig.dpi": 300,
        "font.family": "serif",
        "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
        "font.size": 9,
        "axes.titlesize": 10,
        "axes.titleweight": "bold",
        "axes.spines.top": False,
        "axes.spines.right": False,
    })


def _save(fig, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for ext in ("pdf", "png"):
        p = OUT / f"{name}.{ext}"
        fig.savefig(p, bbox_inches="tight", pad_inches=0.03)
        print(f"Wrote {p}")


def render_system_overview() -> None:
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

    fig, ax = plt.subplots(figsize=(7.2, 2.4))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4)
    ax.axis("off")

    boxes = [
        (0.3, 1.2, 2.2, 1.8, "1. Capture\n3DGS / RGB-D\nviews + poses", SOFT),
        (3.0, 1.2, 2.2, 1.8, "2. Semantic index\nobjects, landmarks,\nroom cues", "#e8f1fb"),
        (5.7, 1.2, 2.2, 1.8, "3. Hierarchy\nzone / region /\nobject tree", "#e7f5ee"),
        (8.4, 1.2, 3.2, 1.8, "4. Query traversal\nprune flat search\nsame items", "#fff1e8"),
    ]
    for x, y, w, h, text, color in boxes:
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05,rounding_size=0.15",
                                    facecolor=color, edgecolor=GRAPH_C, linewidth=1.2))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=8.5)

    for x0 in (2.5, 5.2, 7.9):
        ax.add_patch(FancyArrowPatch((x0, 2.1), (x0 + 0.45, 2.1),
                                     arrowstyle="-|>", mutation_scale=12, color=GRAY, lw=1.2))

    ax.text(6, 3.6, "SemanticSplat pipeline for queryable 3DGS digital twins",
            ha="center", va="center", fontsize=10, fontweight="bold")
    ax.text(6, 0.45, "Graph and flat methods consume identical semantic items; only the search structure differs.",
            ha="center", va="center", fontsize=7.5, color=GRAY)
    _save(fig, "fig_system_overview")
    plt.close(fig)


def render_tree_traversal() -> None:
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch

    fig, ax = plt.subplots(figsize=(7.0, 3.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")

    # Tree nodes
    nodes = {
        "root": (5.0, 5.2, "Conference Hall\n(root)"),
        "lobby": (2.0, 3.6, "Lobby zone"),
        "ball": (5.0, 3.6, "Ballroom zone"),
        "corr": (8.0, 3.6, "Corridor"),
        "stage": (4.0, 2.0, "Stage / screen\nleaf"),
        "floor": (6.0, 2.0, "Main floor\nleaf"),
        "v018": (4.0, 0.6, "v018\ncorrect"),
        "v012": (6.0, 0.6, "v012\nwrong room"),
    }
    keep = {"root", "ball", "stage", "v018"}
    prune = {"lobby", "corr", "floor", "v012"}

    def draw_node(key):
        x, y, label = nodes[key]
        if key in keep:
            face, edge = "#e7f5ee", OK_C
        else:
            face, edge = "#f3f4f6", "#9ca3af"
        ax.add_patch(FancyBboxPatch((x - 0.85, y - 0.45), 1.7, 0.9,
                                    boxstyle="round,pad=0.02,rounding_size=0.1",
                                    facecolor=face, edgecolor=edge, lw=1.2,
                                    linestyle="-" if key in keep else "--"))
        ax.text(x, y, label, ha="center", va="center", fontsize=7.2,
                color="#111" if key in keep else "#6b7280")

    for k in nodes:
        draw_node(k)

    edges = [
        ("root", "lobby", False), ("root", "ball", True), ("root", "corr", False),
        ("ball", "stage", True), ("ball", "floor", False),
        ("stage", "v018", True), ("floor", "v012", False),
    ]
    for a, b, on in edges:
        x0, y0, _ = nodes[a]
        x1, y1, _ = nodes[b]
        ax.add_patch(FancyArrowPatch((x0, y0 - 0.45), (x1, y1 + 0.45),
                                     arrowstyle="-|>", mutation_scale=10,
                                     color=OK_C if on else "#cbd5e1",
                                     lw=1.6 if on else 0.9,
                                     linestyle="-" if on else "--"))

    ax.text(5, 5.85, 'Query: "where is the screen in the conference room?"',
            ha="center", fontsize=9, fontweight="bold")
    ax.text(1.2, 0.35, "Solid green = graph path kept\nDashed gray = pruned branches",
            fontsize=7, color=GRAY, va="center")
    _save(fig, "fig_tree_traversal")
    plt.close(fig)


def _open_rgb(path: Path):
    """Open image if it is a real raster file (skip Git LFS pointer stubs)."""
    from PIL import Image

    if not path.exists() or path.stat().st_size < 1024:
        return None
    head = path.read_bytes()[:64]
    if head.startswith(b"version https://git-lfs.github.com"):
        return None
    try:
        return Image.open(path).convert("RGB")
    except Exception:
        return None


def render_scene_gallery() -> None:
    import matplotlib.pyplot as plt
    import numpy as np

    picks = [
        ("ConferenceHall-capture-pilot", "v001.png", "Conference Hall"),
        ("Museume-capture", "v001.png", "Museum"),
        ("Theater-capture", "v001.png", "Theater"),
        ("outdoor-drone-capture", "v001.png", "Outdoor drone"),
        ("outdoor-street-capture", "v001.png", "Outdoor street"),
        ("default", "v018.png", "Demo Conference (default)"),
    ]
    panels = []
    for scene, fname, title in picks:
        p = ROOT / "backend" / "data" / "scenes" / scene / "images" / fname
        img = _open_rgb(p)
        if img is not None:
            panels.append((img, title))
    if len(panels) < 3:
        for name in ("v012.png", "v013.png", "v018.png"):
            p = ROOT / "backend" / "data" / "scenes" / "default" / "images" / name
            img = _open_rgb(p)
            if img is not None:
                panels.append((img, f"Demo {name[:-4]}"))
    if not panels:
        raise SystemExit("No readable scene images for gallery (git lfs pull may be required).")
    panels = panels[:6]
    cols = 3
    rows = int(np.ceil(len(panels) / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(7.2, 2.35 * rows))
    axes = np.array(axes).reshape(-1)
    for ax in axes:
        ax.axis("off")
    for ax, (img, title) in zip(axes, panels):
        ax.imshow(img)
        ax.set_title(title, fontsize=8)
        ax.axis("off")
    fig.suptitle("Digital-twin pilot scenes (manual captures)", fontsize=10, y=1.01)
    fig.tight_layout()
    _save(fig, "fig_scene_gallery")
    plt.close(fig)


def render_qualitative_bbox() -> None:
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    import numpy as np

    scene = ROOT / "backend" / "data" / "scenes" / "default"
    view = json.loads((scene / "views" / "v018.json").read_text(encoding="utf-8"))
    pil = _open_rgb(scene / "images" / "v018.png")
    if pil is None:
        print("Skip qualitative: missing/unreadable v018.png (git lfs pull?)")
        return
    img = np.asarray(pil)
    h, w = img.shape[:2]

    # Find projection screen bbox
    target = None
    for obj in view.get("objects", []):
        if "screen" in str(obj.get("label", "")).lower():
            target = obj
            break
    if target is None and view.get("objects"):
        target = view["objects"][0]

    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.0))
    # Left: correct view with bbox
    axes[0].imshow(img)
    if target and target.get("bbox_2d"):
        x0, y0, x1, y1 = target["bbox_2d"]
        rect = patches.Rectangle((x0 * w, y0 * h), (x1 - x0) * w, (y1 - y0) * h,
                                 linewidth=2.0, edgecolor=OK_C, facecolor="none")
        axes[0].add_patch(rect)
        axes[0].text(x0 * w, max(8, y0 * h - 8),
                     f"{target.get('label', 'object')} (graph path)",
                     color="white", fontsize=7.5,
                     bbox=dict(boxstyle="round,pad=0.25", facecolor=OK_C, edgecolor="none"))
    axes[0].set_title("Graph: v018 stage / conference end")
    axes[0].axis("off")

    # Right: alternative wrong-room view if exists (v012)
    wrong_pil = _open_rgb(scene / "images" / "v012.png")
    if wrong_pil is not None:
        wimg = np.asarray(wrong_pil)
        axes[1].imshow(wimg)
        axes[1].text(0.02, 0.97, "Flat full-scan distractor view\n(ballroom floor through doors)",
                     transform=axes[1].transAxes, va="top", fontsize=7.5, color="white",
                     bbox=dict(boxstyle="round,pad=0.3", facecolor=FLAT_C, edgecolor="none"))
        axes[1].set_title("Flat risk: near-miss screen view")
    else:
        axes[1].axis("off")
        axes[1].text(0.5, 0.5, "v012 unavailable", ha="center")
    axes[1].axis("off")

    fig.suptitle('Qualitative case: "screen in the conference room"', fontsize=10, y=1.02)
    fig.tight_layout()
    _save(fig, "fig_qualitative_bbox")
    plt.close(fig)


def main() -> int:
    _setup()
    render_system_overview()
    render_tree_traversal()
    render_scene_gallery()
    render_qualitative_bbox()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
