#!/usr/bin/env python3
"""Export TwinWorld figures and LaTeX macros from the new frozen experiments."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


ROOT = Path(__file__).resolve().parents[1]
GREEN = "#18794e"
BLUE = "#1769aa"
ORANGE = "#c44e0b"
GRAY = "#667085"
PALETTE = (GRAY, BLUE, GREEN)

plt.rcParams.update(
    {
        "font.family": "serif",
        "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
        "font.size": 7.5,
        "axes.titlesize": 8.5,
        "axes.labelsize": 7.5,
        "xtick.labelsize": 7,
        "ytick.labelsize": 7,
        "legend.fontsize": 6.8,
    }
)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def finish(fig: plt.Figure, stem: Path) -> None:
    stem.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(stem.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(stem.with_suffix(".png"), dpi=240, bbox_inches="tight")
    plt.close(fig)


def annotate(
    ax: plt.Axes,
    bars,
    *,
    digits: int = 2,
    skip_indices: frozenset[int] = frozenset(),
) -> None:
    for index, bar in enumerate(bars):
        if index in skip_indices:
            continue
        value = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value,
            f"{value:.{digits}f}",
            ha="center",
            va="bottom",
            fontsize=6.8,
        )


def instruction_figure(agent: dict, controls: dict, output: Path) -> None:
    qwen = agent["methods"]["graph_instruction"]
    methods = [
        ("Lexical\ngraph", controls["methods"]["graph_lexical"]),
        ("BGE\ngraph", controls["methods"]["graph_semantic_embedding"]),
        ("Qwen\nagent", qwen),
    ]
    quality = []
    views = []
    tokens = []
    latency = []
    for label, value in methods:
        if "quality" in value:
            quality.append(
                [
                    value["quality"]["hit_at_1"],
                    value["quality"]["hit_at_3"],
                    value["quality"]["mrr"],
                ]
            )
            efficiency = value["efficiency"]
            views.append(efficiency["views_checked"])
            tokens.append(efficiency["input_tokens"])
            latency.append(efficiency["elapsed_ms"])
        else:
            quality.append([value["hit_at_1"], value["hit_at_3"], value["mrr"]])
            views.append(value["mean_views_checked"])
            tokens.append(value["mean_input_tokens"])
            latency.append(value["mean_latency_ms"])

    fig, axes = plt.subplots(1, 3, figsize=(5.2, 2.3))
    x = np.arange(3)
    width = 0.24
    quality_matrix = np.asarray(quality)
    for index, (metric, color) in enumerate(
        zip(("hit@1", "hit@3", "MRR"), (BLUE, GREEN, ORANGE), strict=True)
    ):
        bars = axes[0].bar(
            x + (index - 1) * width,
            quality_matrix[:, index],
            width,
            color=color,
            label=metric,
        )
        annotate(axes[0], bars, digits=2)
    axes[0].set_xticks(x, [value[0] for value in methods])
    axes[0].set_ylim(0, 1.12)
    axes[0].set_ylabel("Quality (125 labeled queries)")
    axes[0].legend(
        frameon=False,
        ncols=3,
        loc="upper center",
        bbox_to_anchor=(0.5, 1.16),
    )

    bars = axes[1].bar(x, views, color=PALETTE)
    annotate(axes[1], bars, digits=1)
    axes[1].set_xticks(x, [value[0] for value in methods])
    axes[1].set_ylabel("Mean views checked")
    axes[1].set_ylim(0, max(views) * 1.22)

    bars = axes[2].bar(x, tokens, color=PALETTE)
    annotate(axes[2], bars, digits=0)
    axes[2].set_xticks(x, [value[0] for value in methods])
    axes[2].set_ylabel("Native / measured input tokens")
    axes[2].set_ylim(0, max(tokens) * 1.22)
    for ax in axes:
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", color="#e4e7ec", linewidth=0.6)
        ax.set_axisbelow(True)
    fig.suptitle("Complete 150-query instruction-agent evaluation", fontsize=8.8, y=1.03)
    fig.tight_layout()
    finish(fig, output)


def hierarchy_figure(raw: dict, output: Path) -> None:
    keys = ("flat_clip", "manual_hierarchy_clip", "raw_rgbd_hierarchy_clip")
    labels = ("Flat\nCLIP", "Manual\nzones", "Raw RGB-D\nclusters")
    values = [raw["methods"][key] for key in keys]
    quality = np.asarray(
        [[value["hit_at_1"], value["hit_at_3"], value["mrr"]] for value in values]
    )
    views = [value["mean_views_checked"] for value in values]
    structure = raw["structure"]

    fig, axes = plt.subplots(1, 3, figsize=(5.2, 2.3))
    x = np.arange(3)
    width = 0.24
    for index, (metric, color) in enumerate(
        zip(("hit@1", "hit@3", "MRR"), (BLUE, GREEN, ORANGE), strict=True)
    ):
        bars = axes[0].bar(
            x + (index - 1) * width,
            quality[:, index],
            width,
            color=color,
            label=metric,
        )
        annotate(axes[0], bars, digits=2)
    axes[0].set_xticks(x, labels)
    axes[0].set_ylim(0, 1.12)
    axes[0].set_ylabel("Quality (125 labeled queries)")
    axes[0].legend(
        frameon=False,
        ncols=3,
        loc="upper center",
        bbox_to_anchor=(0.5, 1.16),
    )

    bars = axes[1].bar(x, views, color=PALETTE)
    annotate(axes[1], bars, digits=1)
    axes[1].set_xticks(x, labels)
    axes[1].set_ylabel("Mean views checked")
    axes[1].set_ylim(0, max(views) * 1.22)

    structural_values = [
        structure["macro_pairwise_f1"],
        structure["macro_rand_index"],
    ]
    bars = axes[2].bar(
        np.arange(2),
        structural_values,
        color=(GREEN, BLUE),
        width=0.62,
    )
    annotate(axes[2], bars, digits=2)
    axes[2].set_xticks(np.arange(2), ("Pairwise F1", "Rand index"))
    axes[2].set_ylim(0, 1.12)
    axes[2].set_ylabel("Agreement with manual zones")
    for ax in axes:
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", color="#e4e7ec", linewidth=0.6)
        ax.set_axisbelow(True)
    fig.suptitle("Automatic raw RGB-D hierarchy versus manual reference", fontsize=8.8, y=1.03)
    fig.tight_layout()
    finish(fig, output)


def construction_variants_figure(hierarchy: dict, output: Path) -> None:
    variant_keys = (
        "manual_reference",
        "pose_only",
        "pose_semantic_merge",
        "cursor_agent_mcp",
    )
    labels = ("Manual\nreference", "Pose\nonly", "Pose +\nsemantic", "Cursor\n+ MCP")
    colors = (GRAY, BLUE, GREEN, ORANGE)
    variants = [hierarchy["variants"][key] for key in variant_keys]

    fig, axes = plt.subplots(1, 3, figsize=(5.2, 2.35))
    x = np.arange(len(variants))

    structural = np.asarray(
        [
            [
                value["assignment_agreement"]["pairwise_f1"],
                value["assignment_agreement"]["weighted_best_zone_jaccard"],
            ]
            for value in variants
        ]
    )
    width = 0.34
    for index, (metric, color) in enumerate(
        zip(("Pairwise F1", "Best-zone Jaccard"), (GREEN, BLUE), strict=True)
    ):
        bars = axes[0].bar(
            x + (index - 0.5) * width,
            structural[:, index],
            width,
            color=color,
            label=metric,
        )
        annotate(axes[0], bars, skip_indices=frozenset({0}))
    axes[0].set_xticks(x, labels)
    axes[0].set_ylim(0, 1.16)
    axes[0].set_ylabel("Agreement with manual zones")
    axes[0].legend(
        frameon=False,
        loc="upper center",
        bbox_to_anchor=(0.5, 1.2),
    )

    quality = np.asarray(
        [
            [
                value["query_metrics"]["hit_at_1"],
                value["query_metrics"]["hit_at_3"],
            ]
            for value in variants
        ]
    )
    for index, (metric, color) in enumerate(
        zip(("hit@1", "hit@3"), (BLUE, GREEN), strict=True)
    ):
        bars = axes[1].bar(
            x + (index - 0.5) * width,
            quality[:, index],
            width,
            color=color,
            label=metric,
        )
        annotate(axes[1], bars)
    axes[1].set_xticks(x, labels)
    axes[1].set_ylim(0, 1.16)
    axes[1].set_ylabel("Retrieval quality (125 queries)")
    axes[1].legend(
        frameon=False,
        loc="upper center",
        bbox_to_anchor=(0.5, 1.18),
        ncols=2,
    )

    views = [value["query_metrics"]["mean_views_checked"] for value in variants]
    bars = axes[2].bar(x, views, color=colors)
    annotate(axes[2], bars, digits=1)
    axes[2].set_xticks(x, labels)
    axes[2].set_ylim(0, max(views) * 1.3)
    axes[2].set_ylabel("Mean views checked")

    for ax in axes:
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", color="#e4e7ec", linewidth=0.55)
        ax.set_axisbelow(True)
    fig.suptitle(
        "Hierarchy construction from shared semantic records",
        fontsize=8.8,
        y=1.03,
    )
    fig.tight_layout()
    finish(fig, output)


def workflow_figure(output: Path) -> None:
    fig, ax = plt.subplots(figsize=(5.2, 3.15))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis("off")

    def box(
        x: float,
        y: float,
        width: float,
        height: float,
        text: str,
        *,
        face: str = "#f7f8fa",
        edge: str = GRAY,
        dashed: bool = False,
        font_size: float = 7.2,
    ) -> None:
        ax.add_patch(
            FancyBboxPatch(
                (x - width / 2, y - height / 2),
                width,
                height,
                boxstyle="round,pad=0.03,rounding_size=0.08",
                facecolor=face,
                edgecolor=edge,
                linewidth=1.0,
                linestyle="--" if dashed else "-",
            )
        )
        ax.text(
            x,
            y,
            text,
            ha="center",
            va="center",
            fontsize=font_size,
            color="#111827",
        )

    def arrow(
        start: tuple[float, float],
        end: tuple[float, float],
        *,
        color: str = GRAY,
        dashed: bool = False,
    ) -> None:
        ax.add_patch(
            FancyArrowPatch(
                start,
                end,
                arrowstyle="-|>",
                mutation_scale=9,
                color=color,
                linewidth=1.1,
                linestyle="--" if dashed else "-",
            )
        )

    ax.text(
        0.2,
        7.65,
        "ONE-TIME HIERARCHY CONSTRUCTION",
        fontsize=7.3,
        fontweight="bold",
        color=BLUE,
    )
    ax.text(
        0.2,
        3.05,
        "PER-QUERY RETRIEVAL",
        fontsize=7.3,
        fontweight="bold",
        color=BLUE,
    )

    box(1.35, 6.55, 2.35, 0.95, "ViewJSON summaries\n+ camera poses", face="#eef6ff", edge=BLUE)
    box(4.15, 6.55, 2.2, 0.95, "MCP proximity\nclusters", face="#eef6ff", edge=BLUE)
    box(7.0, 6.55, 2.25, 0.95, "Cursor semantic\npartition + labels", face="#fff5eb", edge=ORANGE)
    box(10.45, 5.55, 2.35, 1.05, "Frozen scene\nhierarchy", face="#eaf7ef", edge=GREEN)
    arrow((2.47, 6.55), (3.02, 6.55), color=BLUE)
    arrow((5.28, 6.55), (5.85, 6.55), color=ORANGE)
    arrow((8.15, 6.55), (9.28, 5.78), color=GREEN)

    box(1.35, 4.55, 2.2, 0.95, "Raw RGB-D\n+ camera poses", face="#eef6ff", edge=BLUE)
    box(4.15, 4.55, 2.2, 0.95, "CLIP + depth\n+ pose features", face="#eef6ff", edge=BLUE)
    box(7.0, 4.55, 2.25, 0.95, "Predicted clusters\n+ CLIP labels", face="#eaf7ef", edge=GREEN)
    arrow((2.47, 4.55), (3.02, 4.55), color=BLUE)
    arrow((5.28, 4.55), (5.85, 4.55), color=GREEN)
    arrow((8.15, 4.55), (9.28, 5.32), color=GREEN)

    box(
        10.45,
        7.15,
        2.35,
        0.7,
        "Manual zones\n(evaluation only)",
        face="#ffffff",
        edge=GRAY,
        dashed=True,
        font_size=6.8,
    )
    arrow((10.45, 6.78), (10.45, 6.12), dashed=True)

    box(1.35, 1.85, 2.2, 0.95, "Natural-language\nquery", face="#eef6ff", edge=BLUE)
    box(4.15, 1.85, 2.35, 0.95, "Branch gate\nQwen / BGE / lexical", face="#fff5eb", edge=ORANGE)
    box(7.0, 1.85, 2.35, 0.95, "Shared leaf scorer\non retained records", face="#f7f8fa", edge=GRAY)
    box(10.45, 1.85, 2.35, 0.95, "Grounded view\nor object evidence", face="#eaf7ef", edge=GREEN)
    arrow((2.47, 1.85), (3.02, 1.85), color=BLUE)
    arrow((5.28, 1.85), (5.85, 1.85), color=ORANGE)
    arrow((8.15, 1.85), (9.25, 1.85), color=GREEN)
    arrow((10.45, 4.98), (5.15, 2.36), color=GREEN, dashed=True)

    ax.text(
        6.0,
        0.45,
        "Construction and query costs are reported separately; Cursor UI tokens are unavailable, never imputed.",
        ha="center",
        fontsize=6.8,
        color=GRAY,
    )
    finish(fig, output)


def macros(agent: dict, raw: dict, hierarchy: dict, bootstrap: dict) -> str:
    a = agent["methods"]["graph_instruction"]
    c = raw["construction"]
    s = raw["structure"]
    r = raw["methods"]["raw_rgbd_hierarchy_clip"]
    m = raw["methods"]["manual_hierarchy_clip"]
    f = raw["methods"]["flat_clip"]
    cursor = hierarchy["variants"]["cursor_agent_mcp"]
    pose = hierarchy["variants"]["pose_only"]
    semantic = hierarchy["variants"]["pose_semantic_merge"]
    intervals = bootstrap["metrics"]
    values = {
        "AgentHitOne": f"{a['hit_at_1']:.3f}",
        "AgentHitThree": f"{a['hit_at_3']:.3f}",
        "AgentMRR": f"{a['mrr']:.3f}",
        "AgentViews": f"{a['mean_views_checked']:.2f}",
        "AgentCalls": f"{a['mean_model_calls']:.2f}",
        "AgentInputTokens": f"{a['mean_input_tokens']:.1f}",
        "AgentOutputTokens": f"{a['mean_output_tokens']:.1f}",
        "AgentLatencySeconds": f"{a['mean_latency_ms'] / 1000:.2f}",
        "AgentTotalCalls": str(a["total_model_calls"]),
        "AgentTotalTokens": str(a["total_tokens"]),
        "RawConstructionCalls": str(c["model_call_count"]),
        "RawConstructionTokens": str(c["text_tokens"]),
        "RawConstructionSeconds": f"{c['construction_latency_ms'] / 1000:.2f}",
        "RawPairwiseFOne": f"{s['macro_pairwise_f1']:.3f}",
        "RawRandIndex": f"{s['macro_rand_index']:.3f}",
        "RawHitOne": f"{r['hit_at_1']:.3f}",
        "RawHitThree": f"{r['hit_at_3']:.3f}",
        "RawMRR": f"{r['mrr']:.3f}",
        "RawViews": f"{r['mean_views_checked']:.2f}",
        "ManualHitOne": f"{m['hit_at_1']:.3f}",
        "ManualHitThree": f"{m['hit_at_3']:.3f}",
        "ManualViews": f"{m['mean_views_checked']:.2f}",
        "FlatClipHitOne": f"{f['hit_at_1']:.3f}",
        "FlatClipHitThree": f"{f['hit_at_3']:.3f}",
        "FlatClipViews": f"{f['mean_views_checked']:.2f}",
        "CursorMcpCalls": str(hierarchy["agent_evidence"]["mcp_tool_call_count"]),
        "CursorZones": str(cursor["structure"]["zone_count"]),
        "CursorPairwiseFOne": f"{cursor['assignment_agreement']['pairwise_f1']:.3f}",
        "CursorJaccard": f"{cursor['assignment_agreement']['weighted_best_zone_jaccard']:.3f}",
        "CursorHitOne": f"{cursor['query_metrics']['hit_at_1']:.3f}",
        "CursorHitThree": f"{cursor['query_metrics']['hit_at_3']:.3f}",
        "CursorMRR": f"{cursor['query_metrics']['mrr']:.3f}",
        "CursorViews": f"{cursor['query_metrics']['mean_views_checked']:.2f}",
        "CursorQueryTokens": f"{cursor['query_metrics']['mean_input_tokens']:.0f}",
        "PosePairwiseFOne": f"{pose['assignment_agreement']['pairwise_f1']:.3f}",
        "PoseHitThree": f"{pose['query_metrics']['hit_at_3']:.3f}",
        "SemanticPairwiseFOne": f"{semantic['assignment_agreement']['pairwise_f1']:.3f}",
        "SemanticHitOne": f"{semantic['query_metrics']['hit_at_1']:.3f}",
        "SemanticHitThree": f"{semantic['query_metrics']['hit_at_3']:.3f}",
        "ViewSavingsPerQuery": f"{intervals['view_savings_pct']['estimate']:.1f}",
        "ViewSavingsLow": f"{intervals['view_savings_pct']['ci_95']['low']:.1f}",
        "ViewSavingsHigh": f"{intervals['view_savings_pct']['ci_95']['high']:.1f}",
        "TokenSavingsPerQuery": f"{intervals['token_savings_pct']['estimate']:.1f}",
        "TokenSavingsLow": f"{intervals['token_savings_pct']['ci_95']['low']:.1f}",
        "TokenSavingsHigh": f"{intervals['token_savings_pct']['ci_95']['high']:.1f}",
        "HitOneDelta": f"{intervals['hit_at_1_graph_minus_flat']['estimate']:.3f}",
        "HitOneLow": f"{intervals['hit_at_1_graph_minus_flat']['ci_95']['low']:.3f}",
        "HitOneHigh": f"{intervals['hit_at_1_graph_minus_flat']['ci_95']['high']:.3f}",
        "HitThreeDelta": f"{intervals['hit_at_3_graph_minus_flat']['estimate']:.3f}",
        "HitThreeLow": f"{intervals['hit_at_3_graph_minus_flat']['ci_95']['low']:.3f}",
        "HitThreeHigh": f"{intervals['hit_at_3_graph_minus_flat']['ci_95']['high']:.3f}",
    }
    lines = ["% Generated by scripts/export_twinworld_agent_figures.py."]
    lines.extend(f"\\newcommand{{\\{name}}}{{{value}}}" for name, value in values.items())
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--agent",
        type=Path,
        default=ROOT
        / "outputs"
        / "instruction_agent"
        / "five_scene_qwen25_05b_graph_v1"
        / "metrics_summary.json",
    )
    parser.add_argument(
        "--raw",
        type=Path,
        default=ROOT
        / "outputs"
        / "raw_rgbd_hierarchy"
        / "five_scene_clip_v1"
        / "metrics_summary.json",
    )
    parser.add_argument(
        "--controls",
        type=Path,
        default=ROOT
        / "outputs"
        / "agent_semantic"
        / "five_scene_four_variant_v1"
        / "metrics_summary.json",
    )
    parser.add_argument(
        "--hierarchy",
        type=Path,
        default=ROOT
        / "docs"
        / "experiments"
        / "hierarchy_construction"
        / "four_variant_v1"
        / "hierarchy_evaluation.json",
    )
    parser.add_argument(
        "--bootstrap",
        type=Path,
        default=ROOT
        / "docs"
        / "reports"
        / "final"
        / "twinworld_bootstrap_ci.json",
    )
    parser.add_argument(
        "--paper",
        type=Path,
        default=ROOT / "papers" / "twinworld",
    )
    args = parser.parse_args()
    agent = read_json(args.agent.resolve())
    raw = read_json(args.raw.resolve())
    controls = read_json(args.controls.resolve())
    hierarchy = read_json(args.hierarchy.resolve())
    bootstrap = read_json(args.bootstrap.resolve())
    figures = args.paper.resolve() / "figures"
    instruction_figure(agent, controls, figures / "fig_instruction_agent")
    hierarchy_figure(raw, figures / "fig_raw_rgbd_hierarchy")
    construction_variants_figure(
        hierarchy,
        figures / "fig_hierarchy_construction_variants",
    )
    workflow_figure(figures / "fig_agent_mcp_workflow")
    tables = args.paper.resolve() / "tables"
    tables.mkdir(parents=True, exist_ok=True)
    (tables / "new_experiment_macros.tex").write_text(
        macros(agent, raw, hierarchy, bootstrap),
        encoding="utf-8",
    )
    print(f"Wrote figures and macros under {args.paper.resolve()}")


if __name__ == "__main__":
    main()
