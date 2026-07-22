#!/usr/bin/env python3
"""Cross-check the academic preprint and public page against frozen evidence."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PAPER = ROOT / "papers" / "beyond-proximity" / "main.tex"
SITE = ROOT / "site" / "index.html"
CITATION = ROOT / "CITATION.cff"
RETIRED_SUBTITLE = "Queryable 3DGS " + "Digital Twins"
RETIRED_PROJECT_NAME = "Beyond " + "Proximity"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def require(text: str, needle: str, source: Path, failures: list[str]) -> None:
    if needle not in text:
        failures.append(f"{source}: missing {needle!r}")


def forbid(text: str, needle: str, source: Path, failures: list[str]) -> None:
    if needle.lower() in text.lower():
        failures.append(f"{source}: forbidden stale marker {needle!r}")


def main() -> int:
    paper = PAPER.read_text(encoding="utf-8")
    site = SITE.read_text(encoding="utf-8")
    citation = CITATION.read_text(encoding="utf-8")
    internal = load(
        ROOT
        / "outputs"
        / "graph_vs_flat"
        / "five_scene_graph_vs_flat_v2"
        / "metrics_summary.json"
    )
    construction = load(ROOT / "docs" / "reports" / "final" / "graph_construction_cost.json")
    ci = load(ROOT / "docs" / "reports" / "final" / "twinworld_bootstrap_ci.json")
    scannet = load(ROOT / "outputs" / "public_datasets" / "scannet_pilot_v1" / "variant_comparison.json")
    replica = load(ROOT / "outputs" / "public_datasets" / "replica_pilot_v1" / "variant_comparison.json")
    langsplat_run = load(
        ROOT / "outputs" / "baselines" / "langsplat_scannet_full_v1" / "run_config.json"
    )
    langsplat_metrics = load(
        ROOT / "outputs" / "baselines" / "langsplat_scannet_full_v1" / "metrics_summary.json"
    )

    failures: list[str] = []
    for marker in (
        "TwinWorld",
        "Anonymous Authors",
        "Paper ID",
        "#XXXXX",
        "Person 1",
        "Person 2",
        RETIRED_SUBTITLE,
        RETIRED_PROJECT_NAME,
        "LangSplat is evaluated on one scene under reduced resources",
        "LangSplat and ConceptGraphs are smoke baselines",
    ):
        forbid(paper, marker, PAPER, failures)

    required_paper_strings = (
        "97 RGB-D views",
        "1,066 semantic items",
        "150 queries",
        "75.5\\%",
        "68.2\\%",
        "0.680",
        "0.768",
        "0.808",
        "0.928",
        "575 official object boxes",
        "392 official object boxes",
        "66,937",
        "179,817",
        "246,754",
        "1.822 seconds",
        "10,000-resample",
        "[-0.184, 0.008]",
        "[-0.184, -0.056]",
        "Acc@.25=.063",
        "view hit=.667",
        "complete native pipeline execution rather than a smoke",
        "No official BBQ execution artifact",
        "Query-result schema",
        "Metric prerequisites and denominators",
        "Prediction requirement",
        "Reference requirement",
        "\\begin{table*}",
        "\\begin{lstlisting}[style=commandblock]",
    )
    for value in required_paper_strings:
        require(paper, value, PAPER, failures)

    expected_json = {
        "internal query count": internal["summary"]["query_count"] == 150,
        "construction views": construction["totals"]["view_count"] == 97,
        "construction items": construction["totals"]["semantic_item_count"] == 1066,
        "construction annotation tokens": construction["annotation_usage"]["estimated_tokens_chars_div_4"] == 66937,
        "construction tree tokens": construction["totals"]["constructed_tree_estimated_tokens_chars_div_4"] == 179817,
        "construction I/O tokens": construction["totals"]["serialized_io_estimated_tokens_chars_div_4"] == 246754,
        "construction runtime": round(construction["totals"]["median_runtime_seconds_sum"], 3) == 1.822,
        "bootstrap count": ci["bootstrap_samples"] == 10000,
        "ScanNet graph Acc@0.25": scannet["variants"][0]["acc_at_0_25"] == 0.270833,
        "Replica graph Acc@0.25": replica["variants"][0]["acc_at_0_25"] == 1.0,
        "LangSplat run complete": langsplat_run["status"] == "complete",
        "LangSplat native execution": langsplat_run["provenance"]["native_execution"] is True,
        "LangSplat one-scene coverage": langsplat_run["scene_ids"] == ["scannet_0011_00"],
        "LangSplat six results": langsplat_run["result_count"] == 6,
        "LangSplat resource status": (
            langsplat_run["resource_profile"]["status"] == "reduced_resource_end_to_end"
        ),
        "LangSplat RGB iterations": langsplat_run["resource_profile"]["rgb_iterations"] == 3000,
        "LangSplat language iterations": (
            langsplat_run["resource_profile"]["language_iterations"] == 3000
        ),
        "LangSplat expected-view hit": (
            langsplat_metrics["metrics"]["expected_view_hit"]["numerator"] == 4
            and langsplat_metrics["metrics"]["expected_view_hit"]["denominator"] == 6
        ),
        "LangSplat local tokens": langsplat_metrics["metrics"]["token_usage"]["total"] == 74,
    }
    failures.extend(f"frozen evidence mismatch: {name}" for name, ok in expected_json.items() if not ok)

    for marker in (
        "<dt>Provider calls</dt>",
        "<dt>Provider tokens</dt>",
        "BearAx/beyond-proximity",
        "Anonymous Authors",
        RETIRED_SUBTITLE,
        RETIRED_PROJECT_NAME,
    ):
        forbid(site, marker, SITE, failures)
    for marker in (
        "Manual records</dt><dd>97",
        "Semantic items</dt><dd>1,066",
        "Annotation payload</dt><dd>66,937",
        "Constructed tree</dt><dd>179,817",
        "Serialized I/O</dt><dd>246,754",
        "Local rebuild</dt><dd>1.822 s",
        "https://leopython2006.github.io/beyond-proximity-public/",
        "papers/beyond-proximity",
    ):
        require(site, marker, SITE, failures)

    for marker in (
        "SemanticSplat: Graph-Pruned Semantic Search",
        "family-names: \"Mousatat\"",
        "family-names: \"Medvedev\"",
        "https://leopython2006.github.io/beyond-proximity-public/",
    ):
        require(citation, marker, CITATION, failures)
    for marker in (RETIRED_SUBTITLE, RETIRED_PROJECT_NAME):
        forbid(citation, marker, CITATION, failures)

    if failures:
        print("Academic release consistency check FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Academic release consistency check passed (paper, site, and frozen JSON).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
