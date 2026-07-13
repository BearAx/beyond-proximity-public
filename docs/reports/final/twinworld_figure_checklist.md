# TwinWorld Figure Checklist (Person 4)

Status date: 2026-07-13.

## Required by plan

| Figure | Status | Path / note |
|---|---|---|
| System overview (capture → tree → query) | **TODO** | Need diagram (draw.io / TikZ / screenshot collage) |
| Captured-scene visual examples | **TODO** | Use `backend/data/scenes/*-capture*/images/` screenshots |
| Graph/tree traversal | **partial** | described in text; still need a tree visual |
| Query → node/view/object/bbox example | **TODO** | Prefer ScanNet/Replica overlay from P2 outputs if available |
| Internal five-scene cost/quality | **done** | `papers/twinworld/figures/fig_five_scene_summary.pdf` |
| Cumulative tokens | **done** | `fig_cumulative.pdf` |
| Per-type / per-scene breakdown | **done** | `fig_by_query_type.pdf`, `fig_by_scene.pdf` |
| Failure / case studies | **done** | `fig_failure_cases.pdf` |
| Public-dataset pilot result figure | **done** | `fig_scannet_pilot.pdf`, `fig_replica_pilot.pdf` |

## Priority for Days 6–11

1. Public-dataset Acc@k / objects-checked bar or table figure (from P2 JSON).
2. System overview diagram (1 page figure).
3. One qualitative grounding example with bbox overlay.
4. (Optional) ConceptGraphs status as smoke-vs-our-method visual, carefully worded.

## Do not invent

- Fake BBQ comparison bars from paper-reported numbers as if they were our runs.
- Fake 3D IoU improvements without Acc@k outputs.
