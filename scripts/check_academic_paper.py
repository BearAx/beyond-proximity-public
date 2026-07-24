#!/usr/bin/env python3
"""Cross-check the academic preprint against frozen experiment evidence."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PAPER = ROOT / "papers" / "beyond-proximity" / "main.tex"
FIGURES = ROOT / "papers" / "beyond-proximity" / "figures"
TABLES = ROOT / "papers" / "beyond-proximity" / "tables"
TABLE_ROW_FILES = (
    "agent_variant_rows.tex",
    "hierarchy_rows.tex",
    "public_rows.tex",
    "relation_rows.tex",
    "external_rows.tex",
)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def variant(data: dict, name: str) -> dict:
    return next(item for item in data["variants"] if item["variant"] == name)


def require(text: str, needle: str, source: Path, failures: list[str]) -> None:
    if needle not in text:
        failures.append(f"{source}: missing {needle!r}")


def forbid(text: str, needle: str, source: Path, failures: list[str]) -> None:
    if needle.lower() in text.lower():
        failures.append(f"{source}: forbidden stale marker {needle!r}")


def main() -> int:
    paper_source = PAPER.read_text(encoding="utf-8")
    table_text = "\n".join(
        (TABLES / name).read_text(encoding="utf-8")
        for name in TABLE_ROW_FILES
        if (TABLES / name).is_file()
    )
    paper = f"{paper_source}\n{table_text}"
    agent = load(
        ROOT
        / "outputs"
        / "agent_semantic"
        / "five_scene_four_variant_v1"
        / "metrics_summary.json"
    )
    hierarchy = load(
        ROOT
        / "docs"
        / "experiments"
        / "hierarchy_construction"
        / "four_variant_v1"
        / "hierarchy_evaluation.json"
    )
    replica = load(
        ROOT
        / "docs"
        / "experiments"
        / "public_datasets"
        / "phase6_7_v3"
        / "replica_variant_comparison.json"
    )
    scannet = load(
        ROOT
        / "docs"
        / "experiments"
        / "public_datasets"
        / "phase6_7_v3"
        / "scannet_original_variant_comparison.json"
    )
    scannet_ext = load(
        ROOT
        / "docs"
        / "experiments"
        / "public_datasets"
        / "phase6_7_v3"
        / "scannet_extended_variant_comparison.json"
    )
    relation = load(
        ROOT
        / "docs"
        / "experiments"
        / "public_datasets"
        / "phase6_7_v3"
        / "scannet_relation_audit.json"
    )
    langsplat_run = load(
        ROOT / "outputs" / "baselines" / "langsplat_scannet_full_v1" / "run_config.json"
    )
    langsplat_metrics = load(
        ROOT
        / "outputs"
        / "baselines"
        / "langsplat_scannet_full_v1"
        / "metrics_summary.json"
    )

    failures: list[str] = []
    for name in TABLE_ROW_FILES:
        path = TABLES / name
        if not path.is_file() or path.stat().st_size == 0:
            failures.append(f"missing generated table rows: {path}")
    manifest_path = TABLES / "table_data_manifest.json"
    if not manifest_path.is_file():
        failures.append(f"missing generated table manifest: {manifest_path}")
    else:
        manifest = load(manifest_path)
        for item in manifest.get("sources", {}).values():
            path = ROOT / item["path"]
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            if digest != item["sha256"]:
                failures.append(f"stale generated table source: {path}")
    for marker in (
        "SemanticSplat",
        "TwinWorld",
        "Anonymous Authors",
        "Paper ID",
        "#XXXXX",
        "Person 1",
        "Person 2",
        "Queryable 3DGS Digital Twins",
        "75.5\\%",
        "matches flat quality",
        "relation reranking underperforms",
        "LangSplat is evaluated on one scene under reduced resources",
    ):
        forbid(paper, marker, PAPER, failures)

    required_strings = (
        "Agent-Guided Hierarchical Semantic Search",
        "Model Context Protocol",
        "Cursor Agent",
        "BAAI/bge-small-en-v1.5",
        "SayPlan",
        "Search3D",
        "97 captured views",
        "150 queries",
        "75.43\\%",
        "67.99\\%",
        "79.90\\%",
        "32.50\\%",
        "[-0.184,0.008]",
        "[-0.184,-0.056]",
        "[-0.096,0.064]",
        "[-0.224,-0.072]",
        "five direct MCP calls",
        "Q_{\\mathrm{total}}",
        "Q_+",
        "Q_-",
        "Q_{\\mathrm{box}}",
        "25.0\\% fewer objects",
        "18.8\\% fewer objects",
        "from .550 to .675",
        "five beneficial",
        "zero harmful",
        "complete native pipeline execution",
        "No official BBQ",
        "Metric prerequisites and denominators",
        "\\begin{lstlisting}[style=commandblock]",
        "figures/fig_agent_mcp_protocol.pdf",
        "figures/fig_agent_semantic_results.pdf",
        "figures/fig_hierarchy_comparison.pdf",
    )
    for value in required_strings:
        require(paper, value, PAPER, failures)

    methods = agent["methods"]
    scan_graph = variant(scannet, "graph")
    scan_fallback = variant(scannet, "graph_fallback")
    scan_flat = variant(scannet, "flat_lexical")
    ext_fallback = variant(scannet_ext, "graph_fallback")
    ext_flat = variant(scannet_ext, "flat_lexical")
    replica_fallback = variant(replica, "graph_fallback")
    replica_flat = variant(replica, "flat_lexical")
    expected = {
        "agent query count": agent["query_count"] == 150,
        "agent quality denominator": agent["quality_query_count"] == 125,
        "flat lexical hit@1": methods["flat_lexical"]["quality"]["hit_at_1"] == 0.768,
        "graph lexical hit@3": methods["graph_lexical"]["quality"]["hit_at_3"] == 0.808,
        "flat semantic hit@3": methods["flat_semantic_embedding"]["quality"]["hit_at_3"] == 0.928,
        "graph semantic hit@1": methods["graph_semantic_embedding"]["quality"]["hit_at_1"] == 0.664,
        "semantic model": (
            methods["graph_semantic_embedding"]["accounting"]["model_name"]
            == "BAAI/bge-small-en-v1.5"
        ),
        "semantic graph tokens": (
            methods["graph_semantic_embedding"]["accounting"]["total_input_tokens"]
            == 235045
        ),
        "hierarchy variants": set(hierarchy["variants"]) == {
            "manual_reference",
            "pose_only",
            "pose_semantic_merge",
            "cursor_agent_mcp",
        },
        "Cursor MCP calls": hierarchy["agent_evidence"]["mcp_tool_call_count"] == 5,
        "Cursor provider usage unavailable": hierarchy["agent_evidence"]["provider_tokens"] is None,
        "Cursor hierarchy hit@3": (
            hierarchy["variants"]["cursor_agent_mcp"]["query_metrics"]["hit_at_3"]
            == 0.784
        ),
        "ScanNet fallback preserves R@1": (
            scan_fallback["recall_at_1"] == scan_flat["recall_at_1"] == 0.625
        ),
        "ScanNet graph objects": scan_graph["avg_checked_objects"] == 4.729167,
        "ScanNet fallback objects": scan_fallback["avg_checked_objects"] == 36.75,
        "ScanNet flat objects": scan_flat["avg_checked_objects"] == 49.0,
        "extended fallback preserves MRR": ext_fallback["mrr"] == ext_flat["mrr"],
        "extended negative accuracy": ext_fallback["negative_accuracy"] == 1.0,
        "Replica fallback preserves ceiling": (
            replica_fallback["recall_at_1"] == replica_flat["recall_at_1"] == 1.0
        ),
        "relation query count": relation["query_count"] == 40,
        "relation parsed/unparsed": (
            relation["parsed_relation_count"] == 35
            and relation["unparsed_relation_count"] == 5
        ),
        "relation gain": (
            relation["overall"]["with_relation_hit_at_1"] == 0.675
            and relation["overall"]["without_relation_hit_at_1"] == 0.55
        ),
        "relation changes safe": (
            relation["overall"]["beneficial"] == 5
            and relation["overall"]["harmful"] == 0
        ),
        "LangSplat complete": (
            langsplat_run["status"] == "complete"
            and langsplat_run["provenance"]["native_execution"] is True
        ),
        "LangSplat view hits": (
            langsplat_metrics["metrics"]["expected_view_hit"]["numerator"] == 4
            and langsplat_metrics["metrics"]["expected_view_hit"]["denominator"] == 6
        ),
    }
    failures.extend(f"frozen evidence mismatch: {name}" for name, ok in expected.items() if not ok)

    for stem in (
        "fig_agent_mcp_protocol",
        "fig_agent_semantic_results",
        "fig_hierarchy_comparison",
    ):
        for suffix in (".pdf", ".png"):
            path = FIGURES / f"{stem}{suffix}"
            if not path.is_file() or path.stat().st_size == 0:
                failures.append(f"missing generated figure: {path}")

    if failures:
        print("Academic paper evidence check FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Academic paper evidence check passed (source, figures, and frozen JSON).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
