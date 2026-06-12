---
title: "Reasoning — where is the projection screen in the ballroom"
run: 2026-06-11_1911
case: 3
graph_verdict: correct_room
flat_verdict: correct_room
---

[← Run dashboard](../README.md) · [← Docs hub](../../../README.md) · [Benchmark report](../../../benchmark_graph_vs_flat.md)

# Case 3: where is the projection screen in the ballroom

## Summary

| | Graph search | Flat search |
|--|:-------------|:------------|
| **Answer** | `v017` | `v012` |
| **Verdict** | ✅ `correct_room` | ✅ `correct_room` |

## Contents

- [Graph traversal](#graph-traversal)
- [Flat scan](#flat-scan)
- [Takeaway](#takeaway)

---

## Graph traversal

| Step | Node / view | Decision |
|-----:|-------------|----------|
| 1 | Decomposition | Parsed query 'where is the projection screen in the ballroom'. Target keywords and room constraints extracted; naviga… |
| 2 | **Conference Hall** | Descend → `zone_ballroom` |
| 3 | **Ballroom** | Descend → `leaf_ballroom_stage_front` |

### Step details

#### Decomposition

Parsed query 'where is the projection screen in the ballroom'. Target keywords and room constraints extracted; navigating semantic tree instead of scanning all views.

#### Traversal — Conference Hall

At 'Conference Hall' (root). Zone summary: Full venue: lobby reception wing and main ballroom with stage, service, and exits. Descending into 'Ballroom' — summary 'Grand event hall with banquet tables, projection screen, stage wall, service corner, and egress.' matches query room/object constraints. Siblings not taken: Lobby & reception.

**Branch taken:** `zone_ballroom`

#### Traversal — Ballroom

At 'Ballroom' (zone). Zone summary: Grand event hall with banquet tables, projection screen, stage wall, service corner, and egress. Descending into 'Ballroom — stage & screen' — summary 'Presentation end of the hall facing lowered projection screen, podium, and marble-trimmed stage wall.' matches query room/object constraints. Siblings not taken: Ballroom — floor & sides, Ballroom — exit passage.

**Branch taken:** `leaf_ballroom_stage_front`

#### Leaf — `v017` (✓ match)

Confirm object in view v017 within leaf 'Ballroom — stage & screen'. Match — correct zone for query.

---

## Flat scan

> Flat mode scans views in order. First keyword match wins — **room constraints are not enforced**.

| View | Result | Reasoning |
|------|--------|-------------|
| `v001` | skip | Scanned v001. No match, continue to next view. |
| `v002` | skip | Scanned v002. No match, continue to next view. |
| `v003` | skip | Scanned v003. No match, continue to next view. |
| `v004` | skip | Scanned v004. No match, continue to next view. |
| `v005` | skip | Scanned v005. No match, continue to next view. |
| `v006` | skip | Scanned v006. No match, continue to next view. |
| `v007` | skip | Scanned v007. No match, continue to next view. |
| `v008` | skip | Scanned v008. No match, continue to next view. |
| `v009` | skip | Scanned v009. No match, continue to next view. |
| `v010` | skip | Scanned v010. No match, continue to next view. |
| `v011` | skip | Scanned v011. No match, continue to next view. |
| `v012` | ✓ **STOP** | Scanned v012. First keyword match — STOP. Accepted as answer. |

---

## Takeaway

Both found the correct room; graph checked fewer views.

---

[← Back to run dashboard](../README.md)
