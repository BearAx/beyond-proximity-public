# ConceptGraphs Full Five-Scene Result

Status date: 2026-07-06. Status: `DONE_WITH_LIMITATIONS`.

## Command

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_conceptgraphs_full.ps1
```

The command ran ConceptGraphs in Docker image `semanticsplat-conceptgraphs:72f5962`
on all five captured SemanticSplat scenes, then adapted native outputs to the
canonical benchmark schema and evaluated them against
`docs/benchmarks/benchmark_queries_v2.json`.

## Evidence

| Artifact | Path |
|---|---|
| Full output directory | `outputs/baselines/conceptgraphs_full_v1/` |
| Canonical query results | `outputs/baselines/conceptgraphs_full_v1/query_results/` |
| Metrics summary | `outputs/baselines/conceptgraphs_full_v1/metrics_summary.md` |
| Failure modes | `outputs/baselines/conceptgraphs_full_v1/failure_modes.md` |
| Run config/provenance | `outputs/baselines/conceptgraphs_full_v1/run_config.json` |
| Native maps | `outputs/baselines/conceptgraphs_full_v1/native_data/<scene>/exps/semanticsplat_full_mapping_v1/pcd_semanticsplat_full_mapping_v1.pkl.gz` |
| Native result JSONs | `outputs/baselines/conceptgraphs_full_v1/native_results_*.json` |
| Full runner | `scripts/run_conceptgraphs_full.ps1` |
| Native batch query adapter | `baselines/conceptgraphs/native_batch_query.py` |

## Result Summary

| Metric | Value |
|---|---:|
| Captured scenes | 5 |
| Canonical results | 150 / 150 |
| Schema-valid results | 150 / 150 |
| Retrieval success | 0.7000 |
| Expected view hit | 0.2240 |
| Expected node hit | 0.0000 |
| Expected zone hit | 0.0000 |
| Negative not-found correctness | 0.2000 |
| 3D IoU | N/A |
| Token usage | unavailable |

## Per-Scene Native Map Status

| Scene | Frames | Native map objects | Query outputs | Found outputs | Status |
|---|---:|---:|---:|---:|---|
| `ConferenceHall-capture-pilot` | 20 | 313 | 30 | 30 | available |
| `Museume-capture` | 20 | 150 | 30 | 30 | available |
| `Theater-capture` | 20 | 183 | 30 | 30 | available |
| `outdoor-street-capture` | 21 | 43 | 30 | 30 | available |
| `outdoor-drone-capture` | 16 | 0 | 30 | 0 | native map empty |

## Important Limitations

- This is a full five-captured-scene ConceptGraphs run, not an official
  Replica/ScanNet result.
- The query step uses native ConceptGraphs object maps plus batch CLIP object
  retrieval, not SemanticSplat graph traversal.
- The drone scene produced a saved native map artifact with zero serialized
  objects. Its 30 canonical outputs are explicit `found=false` misses.
- The detector wrapper includes a local empty-detection guard for frames where
  YOLO returns zero boxes before MobileSAM. This prevents an empty-tensor crash
  and records the baseline result honestly.
- `bbox_3d_iou` remains `N/A` because independent 3D GT boxes and verified
  metric alignment are not available.
- Negative-query handling is uncalibrated for ConceptGraphs; the native query
  adapter returns top-object matches for non-empty maps and explicit misses only
  for empty maps.

## Valid Claim

ConceptGraphs now has reproducible native Docker evidence across all five
captured SemanticSplat scenes, with 150 canonical outputs and saved provenance.
It is a useful same-captured-scene baseline artifact, but it does not prove
publication-grade superiority, public-dataset generalization, or 3D localization
accuracy.
