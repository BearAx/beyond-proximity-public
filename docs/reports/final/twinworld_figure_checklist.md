# Workshop Paper Figure Checklist

Status date: 2026-07-24.

## Required by plan

| Figure | Status | Path / note |
|---|---|---|
| Agent/MCP + raw RGB-D workflow | **done** | `fig_agent_mcp_workflow.pdf`; clearly separates Cursor/MCP semantic-record construction, zero-ViewJSON raw construction, and query-time Qwen/BGE/lexical scoring |
| Controlled evaluation protocol | **done** | `fig_evaluation_protocol.pdf` |
| Captured-scene visual examples | **done** | `fig_scene_gallery.pdf` (needs `git lfs pull` for scene PNGs) |
| Graph/tree traversal | **done** | `fig_tree_traversal.pdf` |
| Four hierarchy-construction variants | **done** | `fig_hierarchy_construction_variants.pdf`; manual, pose-only, pose+semantic, and Cursor+MCP |
| Query → node/view/object/bbox example | **done** | `fig_qualitative_bbox.pdf` (default scene v018/v012) |
| Internal five-scene cost/quality | **done** | `fig_five_scene_summary.pdf` (regenerated from frozen JSON) |
| Cumulative tokens | **done** | `fig_cumulative.pdf` |
| Per-type / per-scene breakdown | **done** | `fig_by_query_type.pdf`, `fig_by_scene.pdf` |
| Failure / case studies | **done** | `fig_failure_cases.pdf` |
| Public-dataset pilot result figure | **done** | `fig_scannet_pilot.pdf`, `fig_replica_pilot.pdf` |

## Do not invent

- Fake BBQ comparison bars from paper-reported numbers as if they were our runs.
- Fake 3D IoU improvements without Acc@k outputs.

## Final visual QA

The latest 14-page ID-free PDF was rendered at 120 DPI under
`tmp/pdfs/twinworld-customer-final-v6/`. Figure labels fit their boxes, legends do
not cover data labels, tables remain inside their subsections, and no page is a
displaced float-only page.
