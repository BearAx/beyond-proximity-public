# Phase 5: Hierarchy Construction Evaluation

Status: complete on the five captured pilot scenes.

## Protocol

Four hierarchy-construction variants were evaluated over the same 97 captured
views, the same semantic records, the same 150 benchmark queries, and the same
fixed query policy:

1. `manual_reference`: the existing human/Cursor-assisted hierarchy.
2. `pose_only`: deterministic clustering from camera positions.
3. `pose_semantic_merge`: deterministic position clustering with semantic
   summary merging.
4. `cursor_agent_mcp`: Cursor Agent decisions produced from five direct
   `semantic-splat/build_spatial_clusters` MCP calls.

The agent run used the UI-labelled model `Cursor Grok 4.5 High Fast`, called the
MCP tool exactly once per scene with `geometry_assisted=true`, did not read the
manual-zone reference, did not call `save_node`, and did not modify scene data.
The five MCP cluster counts were `1, 1, 1, 2, 3`. The resulting hierarchy has
complete, duplicate-free coverage of all 97 views.

The manual zones are a project reference, not independent dataset GT. They are
overlapping by design: 47 views have multiple reference memberships and one
view is not assigned to a reference zone. Agreement therefore uses
multi-membership pairwise scoring and a bounded best-zone Jaccard.

## Results

| Variant | Zones | Pairwise F1 | Best-zone Jaccard | Hit@1 | Hit@3 | MRR | Views/query | Est. tokens/query |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Manual reference | 26 | 1.000 | 1.000 | 0.680 | 0.808 | 0.742 | 4.77 | 1,014 |
| Pose only | 10 | 0.588 | 0.526 | 0.760 | 0.880 | 0.829 | 6.07 | 1,780 |
| Pose + semantic merge | 8 | 0.570 | 0.504 | 0.784 | 0.904 | 0.845 | 5.80 | 1,747 |
| Cursor Agent + MCP | 18 | 0.616 | 0.610 | 0.704 | 0.784 | 0.749 | 5.53 | 1,193 |

Query quality has a denominator of 125 verified-view-label queries. Efficiency
uses all 150 completed queries. The hierarchy variants change grouping and
therefore pruning behavior, but do not change the underlying semantic records.

## Construction Accounting

| Variant | Local construction time | Provider tokens | Serialized input context |
|---|---:|---:|---:|
| Manual reference | historical time unavailable | unavailable | 8,939 estimated tokens |
| Pose only | 0.042 s | 0 | 8,939 estimated tokens |
| Pose + semantic merge | 0.042 s | 0 | 8,939 estimated tokens |
| Cursor Agent + MCP | UI runtime unavailable | unavailable | 8,939 estimated tokens |

`0` is used only where no provider call occurred. Cursor's UI did not expose an
auditable provider-token or model-token counter, so those fields are
`unavailable`, not zero. The serialized-context count is measured locally and
is not presented as provider billing.

## Conclusion

The deterministic semantic merge gives the highest query quality in this
five-scene experiment, while the Cursor-MCP hierarchy is structurally closer
to the overlapping manual reference than either deterministic alternative.
The agent hierarchy also uses substantially less query context than the two
deterministic alternatives, but does not beat their Hit@k. No single variant is
therefore dominant on both structural agreement, quality, and query cost.

## Evidence and Reproduction

- Fixed config: `configs/hierarchy_construction_v1.json`
- Direct MCP decisions:
  `docs/experiments/hierarchy_construction/cursor_agent_mcp_v1/agent_hierarchy_decisions.json`
- Full evaluation:
  `docs/experiments/hierarchy_construction/four_variant_v1/hierarchy_evaluation.json`
- Per-scene structure:
  `docs/experiments/hierarchy_construction/four_variant_v1/hierarchy_structure.csv`
- Per-query results:
  `docs/experiments/hierarchy_construction/four_variant_v1/hierarchy_query_results.csv`

```powershell
python -B scripts/evaluate_hierarchy_construction.py `
  --config configs/hierarchy_construction_v1.json `
  --out docs/experiments/hierarchy_construction/four_variant_v1
```
