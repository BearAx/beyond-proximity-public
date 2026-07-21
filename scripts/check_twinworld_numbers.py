#!/usr/bin/env python3
"""Cross-check TwinWorld paper numbers against frozen JSON evidence."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CAPTURE_SCENES = (
    "ConferenceHall-capture-pilot",
    "Museume-capture",
    "Theater-capture",
    "outdoor-street-capture",
    "outdoor-drone-capture",
)

# Freeze values that must appear in papers/twinworld/main.tex (source: JSON below).
FIVE = {
    "views_flat": 19.4,
    "views_graph": 4.77,
    "tok_flat": 3168.2,
    "tok_graph": 1014.26,
    "sav_views": 75.5,
    "sav_tok": 68.2,
    "hit1_flat": 0.768,
    "hit1_graph": 0.68,
    "hit3_flat": 0.928,
    "hit3_graph": 0.808,
    "tok_sum_flat": 475230,
    "tok_sum_graph": 152139,
}


def main() -> int:
    five = json.loads(
        (ROOT / "outputs/graph_vs_flat/five_scene_graph_vs_flat_v2/metrics_summary.json").read_text(
            encoding="utf-8"
        )
    )
    s = five["summary"]
    avg = s["averages"]
    q = s["quality"]
    checks = []

    def check(name, got, expected, tol=0.015):
        ok = abs(float(got) - float(expected)) <= tol
        checks.append((name, got, expected, ok))
        print(("OK " if ok else "MISMATCH "), name, f"got={got} expected={expected}")

    check("five.views_flat", avg["flat_views_checked"], FIVE["views_flat"])
    check("five.views_graph", avg["graph_views_checked"], FIVE["views_graph"])
    check("five.tok_flat", avg["flat_input_tokens"], FIVE["tok_flat"], tol=1)
    check("five.tok_graph", avg["graph_input_tokens"], FIVE["tok_graph"], tol=1)
    check("five.sav_views", avg["savings_views_pct"], FIVE["sav_views"])
    check("five.sav_tok", avg["savings_tokens_pct"], FIVE["sav_tok"])
    check("five.hit1_flat", q["hit_at_1_flat"], FIVE["hit1_flat"])
    check("five.hit1_graph", q["hit_at_1_graph"], FIVE["hit1_graph"])
    check("five.hit3_flat", q["hit_at_3_flat"], FIVE["hit3_flat"])
    check("five.hit3_graph", q["hit_at_3_graph"], FIVE["hit3_graph"])

    rows = json.loads(
        (ROOT / "outputs/graph_vs_flat/five_scene_graph_vs_flat_v2/per_query_results.json").read_text(
            encoding="utf-8"
        )
    )
    if isinstance(rows, dict):
        rows = rows.get("queries") or rows.get("results") or []
    tok_sum_flat = sum(float(r["flat"].get("input_tokens", 0)) for r in rows)
    tok_sum_graph = sum(float(r["graph"].get("input_tokens", 0)) for r in rows)
    check("five.tok_sum_flat", tok_sum_flat, FIVE["tok_sum_flat"], tol=5)
    check("five.tok_sum_graph", tok_sum_graph, FIVE["tok_sum_graph"], tol=5)

    captured_view_count = sum(
        len(list((ROOT / "backend/data/scenes" / scene_id / "views").glob("*.json")))
        for scene_id in CAPTURE_SCENES
    )
    check("five.captured_view_count", captured_view_count, 97, tol=0)

    construction = json.loads(
        (ROOT / "docs/reports/final/graph_construction_cost.json").read_text(encoding="utf-8")
    )
    construction_totals = construction["totals"]
    provider_usage = construction["provider_usage"]
    annotation_usage = construction["annotation_usage"]
    check("construction.provider_calls", provider_usage["model_call_count"], 0, tol=0)
    check("construction.provider_tokens", provider_usage["total_tokens"], 0, tol=0)
    check("construction.views", construction_totals["view_count"], 97, tol=0)
    check("construction.items", construction_totals["semantic_item_count"], 1066, tol=0)
    check("construction.nodes", construction_totals["node_count"], 1064, tol=0)
    check(
        "construction.source_characters",
        construction_totals["source_viewjson_serialized_characters"],
        267877,
        tol=0,
    )
    check(
        "construction.source_token_equivalent",
        construction_totals["source_viewjson_estimated_tokens_chars_div_4"],
        66937,
        tol=0,
    )
    check(
        "construction.tree_token_equivalent",
        construction_totals["constructed_tree_estimated_tokens_chars_div_4"],
        179817,
        tol=0,
    )
    check(
        "construction.serialized_io_token_equivalent",
        construction_totals["serialized_io_estimated_tokens_chars_div_4"],
        246754,
        tol=0,
    )
    check("annotation.records", annotation_usage["viewjson_record_count"], 97, tol=0)
    check("annotation.items", annotation_usage["semantic_item_count"], 1066, tol=0)
    check(
        "annotation.characters",
        annotation_usage["canonical_serialized_characters"],
        267877,
        tol=0,
    )
    check(
        "annotation.token_equivalent",
        annotation_usage["estimated_tokens_chars_div_4"],
        66937,
        tol=0,
    )

    for track, n, g_obj, f_obj, acc in [
        ("replica_pilot_v1", 56, 12.107143, 71.875, 1.0),
        ("scannet_pilot_v1", 48, 11.229167, 49.0, 0.270833),
    ]:
        g = json.loads(
            (ROOT / f"outputs/public_datasets/{track}/graph/grounding_summary.json").read_text(
                encoding="utf-8"
            )
        )
        f = json.loads(
            (
                ROOT / f"outputs/public_datasets/{track}/flat_lexical/grounding_summary.json"
            ).read_text(encoding="utf-8")
        )
        check(f"{track}.n", g["metrics"]["query_count"], n, tol=0)
        check(f"{track}.acc025_graph", g["metrics"]["acc_at_0_25"]["value"], acc, tol=0.002)
        check(
            f"{track}.acc025_flat",
            f["metrics"]["acc_at_0_25"]["value"],
            acc if track.startswith("replica") else 0.270833,
            tol=0.002,
        )
        check(
            f"{track}.obj_graph",
            g["metrics"]["efficiency"]["checked_objects"]["mean"],
            g_obj,
            tol=0.05,
        )
        check(
            f"{track}.obj_flat",
            f["metrics"]["efficiency"]["checked_objects"]["mean"],
            f_obj,
            tol=0.05,
        )

    conceptgraphs = json.loads(
        (ROOT / "outputs/baselines/conceptgraphs_scannet_full_v1/metrics_summary.json").read_text(
            encoding="utf-8"
        )
    )["metrics"]
    check("conceptgraphs_scannet.n", conceptgraphs["bbox_acc_at_0_25"]["denominator"], 48, tol=0)
    check("conceptgraphs_scannet.acc025", conceptgraphs["bbox_acc_at_0_25"]["value"], 0.0625, tol=0)
    check("conceptgraphs_scannet.mean_iou", conceptgraphs["bbox_3d_iou"]["value"], 0.0696, tol=0.0001)
    check("conceptgraphs_scannet.runtime", conceptgraphs["runtime_seconds"]["mean"], 0.3363, tol=0.0001)
    check("conceptgraphs_scannet.tokens", conceptgraphs["token_usage"]["total"], 627, tol=0)

    conceptgraphs_replica = json.loads(
        (ROOT / "outputs/baselines/conceptgraphs_replica_full_v1/metrics_summary.json").read_text(
            encoding="utf-8"
        )
    )["metrics"]
    check(
        "conceptgraphs_replica.n",
        conceptgraphs_replica["bbox_acc_at_0_25"]["denominator"],
        48,
        tol=0,
    )
    check(
        "conceptgraphs_replica.acc025",
        conceptgraphs_replica["bbox_acc_at_0_25"]["value"],
        0.0625,
        tol=0,
    )
    check(
        "conceptgraphs_replica.mean_iou",
        conceptgraphs_replica["bbox_3d_iou"]["value"],
        0.0624,
        tol=0.0001,
    )
    check(
        "conceptgraphs_replica.runtime",
        conceptgraphs_replica["runtime_seconds"]["mean"],
        0.2743,
        tol=0.0001,
    )
    check(
        "conceptgraphs_replica.tokens",
        conceptgraphs_replica["token_usage"]["total"],
        459,
        tol=0,
    )

    langsplat = json.loads(
        (ROOT / "outputs/baselines/langsplat_scannet_full_v1/metrics_summary.json").read_text(
            encoding="utf-8"
        )
    )["metrics"]
    check("langsplat_scannet.n", langsplat["retrieval_success"]["denominator"], 6, tol=0)
    check("langsplat_scannet.view_hit", langsplat["expected_view_hit"]["value"], 0.6667, tol=0.0001)
    check("langsplat_scannet.runtime", langsplat["runtime_seconds"]["mean"], 2.0365, tol=0.0001)
    check("langsplat_scannet.tokens", langsplat["token_usage"]["total"], 74, tol=0)
    check("langsplat_scannet.iou_na", langsplat["bbox_3d_iou"]["denominator"], 0, tol=0)

    # Paper must not still claim the superseded PERSON1_DELIVERABLE roundings.
    tex = (ROOT / "papers/twinworld/main.tex").read_text(encoding="utf-8")
    forbidden = [
        "71.4\\%",
        "65.1\\%",
        "0.792",
        "19.2 to 5.39",
        "from 19.2",
        "3104 to 1062",
        "96 views",
        "Person 1",
        "Person 2",
        "Person 3",
        "Person 4",
        "Person~",
        "calibrated fallback",
        "\\subsection{Capture and semantic index}",
        "XXXXX",
    ]
    for s_bad in forbidden:
        present = s_bad in tex
        checks.append((f"tex_free_of:{s_bad}", 0 if present else 1, 1, not present))
        print(("OK " if not present else "MISMATCH "), f"tex must not contain {s_bad!r}")

    required = [
        "97 views", "75.5\\%", "68.2\\%", "0.68", "19.4", "4.77",
        "Acc@.25 $=.063$", "view hit $=.667$", "0.0696", "0.0624",
        "CG--Replica", "& .274 & 459",
        "[73.2,77.7]", "[65.3,71.0]", "[-0.184,0.008]", "20,260,715",
        "\\subsection{Hierarchical query representation}",
        "Hierarchical semantic tree used at query time",
        "through zone, region, object, and view-observation levels",
        "c_i=(\\mathrm{id}_i,\\tau_i,A_i,y_i,x_i,R_i,B_i,V_i)",
        "\\subsection{Captured-scene zone pruning}",
        "\\subsection{Object-level lexical and intent scoring}",
        "\\subsection{Target--anchor spatial reasoning}",
        "\\subsection{Fallback, variants, and measured cost}",
        "\\subsection{Input representation and index construction}",
        "figures/fig_method_workflow.pdf",
        "provider calls and zero provider input/output tokens",
        "66,937",
        "179,817",
        "267,877",
        "246,754",
        "1.822\\,s",
        "manual-annotation artifact workload is measured",
    ]
    for s_ok in required:
        present = s_ok in tex
        checks.append((f"tex_has:{s_ok}", 1 if present else 0, 1, present))
        print(("OK " if present else "MISMATCH "), f"tex must contain {s_ok!r}")

    site = (ROOT / "site/index.html").read_text(encoding="utf-8")
    for site_required in (
        "<dt>Manual records</dt><dd>97",
        "<dt>Semantic items</dt><dd>1,066",
        "<dt>Annotation payload</dt><dd>66,937",
        "<dt>Serialized I/O</dt><dd>246,754",
    ):
        present = site_required in site
        checks.append((f"site_has:{site_required}", 1 if present else 0, 1, present))
        print(("OK " if present else "MISMATCH "), f"site must contain {site_required!r}")
    site_has_na = "N/A" in site
    checks.append(("site_free_of:N/A", 0 if site_has_na else 1, 1, not site_has_na))
    print(("OK " if not site_has_na else "MISMATCH "), "site must not contain 'N/A'")

    bad = [c for c in checks if not c[3]]
    out = ROOT / "docs/reports/final/twinworld_number_check.md"
    lines = [
        "# TwinWorld number cross-check",
        "",
        "Source of truth: `outputs/graph_vs_flat/five_scene_graph_vs_flat_v2/metrics_summary.json`",
        "",
        f"Checks: {len(checks)} - mismatches: {len(bad)}",
        "",
        "| Name | Got | Expected | OK |",
        "|---|---:|---:|:---:|",
    ]
    for name, got, exp, ok in checks:
        lines.append(f"| `{name}` | {got} | {exp} | {'yes' if ok else 'NO'} |")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {out}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
