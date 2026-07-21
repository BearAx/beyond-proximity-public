# Workshop Paper Figure Checklist

Status date: 2026-07-21.

## Required by plan

| Figure | Status | Path / note |
|---|---|---|
| Evidence-backed method workflow (RGB-D -> ViewJSON -> hierarchy -> graph/flat -> evidence) | **done** | `fig_method_workflow.pdf` via `scripts/export_twinworld_figures.py`; real Conference Hall v018, frozen qv2_010, and construction audit |
| Controlled evaluation protocol | **done** | `fig_evaluation_protocol.pdf` |
| Captured-scene visual examples | **done** | `fig_scene_gallery.pdf` (needs `git lfs pull` for scene PNGs) |
| Graph/tree traversal | **done** | `fig_tree_traversal.pdf` |
| Query → node/view/object/bbox example | **done** | `fig_qualitative_bbox.pdf` (default scene v018/v012) |
| Internal five-scene cost/quality | **done** | `fig_five_scene_summary.pdf` (regenerated from frozen JSON) |
| Cumulative tokens | **done** | `fig_cumulative.pdf` |
| Per-type / per-scene breakdown | **done** | `fig_by_query_type.pdf`, `fig_by_scene.pdf` |
| Failure / case studies | **done** | `fig_failure_cases.pdf` |
| Public-dataset pilot result figure | **done** | `fig_scannet_pilot.pdf`, `fig_replica_pilot.pdf` |

## Do not invent

- Fake BBQ comparison bars from paper-reported numbers as if they were our runs.
- Fake 3D IoU improvements without Acc@k outputs.
