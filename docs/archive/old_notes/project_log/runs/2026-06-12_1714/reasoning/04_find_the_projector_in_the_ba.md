---
title: "Reasoning — find the projector in the ballroom"
run: 2026-06-12_1714
case: 4
graph_verdict: correct_room
flat_verdict: correct_room
---

[← Run dashboard](../README.md) · [← Docs hub](../../../README.md) · [Benchmark report](../../../benchmark_graph_vs_flat.md)

# Case 4: find the projector in the ballroom

## Summary

| | Graph search | Flat search |
|--|:-------------|:------------|
| **Answer** | `v013` | `v013` |
| **Verdict** | ✅ `correct_room` | ✅ `correct_room` |

## Contents

- [Graph traversal](#graph-traversal)
- [Flat scan](#flat-scan)
- [Takeaway](#takeaway)

---

## Graph traversal

| Step | Node / view | Decision |
|-----:|-------------|----------|
| 1 | Decomposition | Parsed query 'find the projector in the ballroom'. Target keywords and room constraints extracted; navigating semanti… |
| 2 | **Conference Hall** | Descend → `zone_lobby_reception` |
| 3 | **Lobby & reception** | Descend → `leaf_lobby_corridor_lounge` |
| 4 | **Corridor & lounge wing** | Descend → `leaf_lobby_foyer_prefunction` |
| 5 | **Foyer & pre-function lounge** | Descend → `leaf_lobby_bar_reception` |
| 6 | **Bar, vestibule & reception** | Descend → `zone_ballroom` |
| 7 | **Ballroom** | Descend → `leaf_ballroom_main_floor` |

### Step details

#### Decomposition

Parsed query 'find the projector in the ballroom'. Target keywords and room constraints extracted; navigating semantic tree instead of scanning all views.

#### Traversal — Conference Hall

At 'Conference Hall' (root). Zone summary: Full venue: lobby reception wing and main ballroom with stage, service, and exits. Descending into 'Lobby & reception' — summary 'Circulation, lounges, foyer, bar, vestibule, and reception desk before the main ballroom doors.' matches query room/object constraints. Siblings not taken: Ballroom.

**Branch taken:** `zone_lobby_reception`

#### Traversal — Lobby & reception

At 'Lobby & reception' (zone). Zone summary: Circulation, lounges, foyer, bar, vestibule, and reception desk before the main ballroom doors. Descending into 'Corridor & lounge wing' — summary 'Hotel corridor, marble pillars, and upholstered lounge seating along the main circulation spine.' matches query room/object constraints. Siblings not taken: Foyer & pre-function lounge, Bar, vestibule & reception.

**Branch taken:** `leaf_lobby_corridor_lounge`

#### Traversal — Corridor & lounge wing

At 'Corridor & lounge wing' (leaf). Zone summary: Hotel corridor, marble pillars, and upholstered lounge seating along the main circulation spine. Descending into 'Foyer & pre-function lounge' — summary 'Grand piano foyer, double doors, and pre-function lounge with artwork and egress signage.' matches query room/object constraints. Siblings not taken: none.

**Branch taken:** `leaf_lobby_foyer_prefunction`

#### Traversal — Foyer & pre-function lounge

At 'Foyer & pre-function lounge' (leaf). Zone summary: Grand piano foyer, double doors, and pre-function lounge with artwork and egress signage. Descending into 'Bar, vestibule & reception' — summary 'Curved bar counter, wood-panelled vestibule with ornate doors, and hotel reception desk with banquet staging.' matches query room/object constraints. Siblings not taken: none.

**Branch taken:** `leaf_lobby_bar_reception`

#### Traversal — Bar, vestibule & reception

At 'Bar, vestibule & reception' (leaf). Zone summary: Curved bar counter, wood-panelled vestibule with ornate doors, and hotel reception desk with banquet staging. Descending into 'Ballroom' — summary 'Grand event hall with banquet tables, projection screen, stage wall, service corner, and egress.' matches query room/object constraints. Siblings not taken: none.

**Branch taken:** `zone_ballroom`

#### Traversal — Ballroom

At 'Ballroom' (zone). Zone summary: Grand event hall with banquet tables, projection screen, stage wall, service corner, and egress. Descending into 'Ballroom — floor & sides' — summary 'Entrance through double doors, side wall with AV, service prep corner, main banquet tables, and ceiling chandelier view.' matches query room/object constraints. Siblings not taken: Ballroom — stage & screen, Ballroom — exit passage.

**Branch taken:** `leaf_ballroom_main_floor`

#### Leaf — `v012` (✗ no match)

Confirm object in view v012 within leaf 'Ballroom — floor & sides'. No match.

#### Leaf — `v013` (✓ match)

Confirm object in view v013 within leaf 'Ballroom — floor & sides'. Match — correct zone for query.

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
| `v012` | skip | Scanned v012. No match, continue to next view. |
| `v013` | ✓ **STOP** | Scanned v013. First keyword match — STOP. Accepted as answer. |

---

## Takeaway

Both found the correct room; graph checked fewer views.

---

[← Back to run dashboard](../README.md)
