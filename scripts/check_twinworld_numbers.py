#!/usr/bin/env python3
"""Cross-check TwinWorld paper numbers against frozen JSON evidence."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

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

    # Paper must not still claim the superseded PERSON1_DELIVERABLE roundings.
    tex = (ROOT / "papers/twinworld/main.tex").read_text(encoding="utf-8")
    forbidden = ["71.4\\%", "65.1\\%", "0.792", "19.2 to 5.39", "from 19.2", "3104 to 1062"]
    for s_bad in forbidden:
        present = s_bad in tex
        checks.append((f"tex_free_of:{s_bad}", 0 if present else 1, 1, not present))
        print(("OK " if not present else "MISMATCH "), f"tex must not contain {s_bad!r}")

    required = ["75.5\\%", "68.2\\%", "0.68", "19.4", "4.77"]
    for s_ok in required:
        present = s_ok in tex
        checks.append((f"tex_has:{s_ok}", 1 if present else 0, 1, present))
        print(("OK " if present else "MISMATCH "), f"tex must contain {s_ok!r}")

    bad = [c for c in checks if not c[3]]
    out = ROOT / "docs/reports/final/twinworld_number_check.md"
    lines = [
        "# TwinWorld number cross-check",
        "",
        "Source of truth: `outputs/graph_vs_flat/five_scene_graph_vs_flat_v2/metrics_summary.json`",
        "",
        f"Checks: {len(checks)} · mismatches: {len(bad)}",
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
