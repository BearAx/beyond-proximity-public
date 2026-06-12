---
title: "Reasoning — where is the exit sign in the lobby"
run: 2026-06-12_1829
case: 5
graph_verdict: miss
flat_verdict: miss
---

[← Run dashboard](../README.md) · [← Docs hub](../../../README.md) · [Benchmark report](../../../benchmark_graph_vs_flat.md)

# Case 5: where is the exit sign in the lobby

## Summary

| | Graph search | Flat search |
|--|:-------------|:------------|
| **Answer** | `—` | `—` |
| **Verdict** | ⚠️ `miss` | ⚠️ `miss` |

## Contents

- [Graph traversal](#graph-traversal)
- [Flat scan](#flat-scan)
- [Takeaway](#takeaway)

---

## Graph traversal

| Step | Node / view | Decision |
|-----:|-------------|----------|
| 1 | Decomposition | Parsed query 'where is the exit sign in the lobby'. Target keywords and room constraints extracted; navigating semant… |
| 2 | **Conference Hall** | Descend → `zone_lobby_reception` |
| 3 | **Lobby & reception** | Descend → `leaf_lobby_foyer_prefunction` |

### Step details

#### Decomposition

Parsed query 'where is the exit sign in the lobby'. Target keywords and room constraints extracted; navigating semantic tree instead of scanning all views.

#### Traversal — Conference Hall

At 'Conference Hall' (root). Zone summary: Full venue: lobby reception wing and main ballroom with stage, service, and exits. Descending into 'Lobby & reception' — summary 'Circulation, lounges, foyer, bar, vestibule, and reception desk before the main ballroom doors.' matches query room/object constraints. Siblings not taken: Ballroom.

**Branch taken:** `zone_lobby_reception`

#### Traversal — Lobby & reception

At 'Lobby & reception' (zone). Zone summary: Circulation, lounges, foyer, bar, vestibule, and reception desk before the main ballroom doors. Descending into 'Foyer & pre-function lounge' — summary 'Grand piano foyer, double doors, and pre-function lounge with artwork and egress signage.' matches query room/object constraints. Siblings not taken: Corridor & lounge wing, Bar, vestibule & reception.

**Branch taken:** `leaf_lobby_foyer_prefunction`

#### Leaf — `v006` (✗ no match)

Confirm object in view v006 within leaf 'Foyer & pre-function lounge'. No match.

#### Leaf — `v007` (✗ no match)

Confirm object in view v007 within leaf 'Foyer & pre-function lounge'. No match.

#### Leaf — `v008` (✗ no match)

Confirm object in view v008 within leaf 'Foyer & pre-function lounge'. No match.

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
| `v013` | skip | Scanned v013. No match, continue to next view. |
| `v014` | skip | Scanned v014. No match, continue to next view. |
| `v015` | skip | Scanned v015. No match, continue to next view. |
| `v016` | skip | Scanned v016. No match, continue to next view. |
| `v017` | skip | Scanned v017. No match, continue to next view. |
| `v018` | skip | Scanned v018. No match, continue to next view. |
| `v019` | skip | Scanned v019. No match, continue to next view. |

---

## Takeaway

Both modes missed — likely a simulation/oracle gap. Run with a real LLM session via Query Flow for this query.

---

[← Back to run dashboard](../README.md)
