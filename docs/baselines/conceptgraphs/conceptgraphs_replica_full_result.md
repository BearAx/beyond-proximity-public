# ConceptGraphs Replica Full-Query Result

Status date: 2026-07-15. Status: `COMPLETE_WITH_PROTOCOL_LIMITATIONS`.

## Scope

ConceptGraphs was executed natively through Docker on all eight official
NICE-SLAM Replica scenes (`room0`--`room2`, `office0`--`office4`) and all 56
BBQ-aligned project queries. Five evenly spaced RGB-D frames were sampled from
each 2,000-frame trajectory, for 40 frames total. This is a complete
eight-scene / full-query sampled-map run, not full-trajectory reconstruction.

The native pipeline ran YOLO-World and MobileSAM detection, absolute-pose
ConceptGraphs mapping, and OpenCLIP ViT-H-14 object retrieval. All eight maps
were nonempty, with 27--66 serialized objects per scene.

## Results

| Metric | Result |
|---|---:|
| Canonical/schema-valid outputs | 56 / 56 |
| Positive-query object-label hit | 7 / 48 (0.1458) |
| Exact GT object-ID hit | 0 / 48 |
| Mean 3D IoU | 0.0624 |
| Acc@0.1 | 8 / 48 (0.1667) |
| Acc@0.25 | 3 / 48 (0.0625) |
| Acc@0.5 | 2 / 48 (0.0417) |
| Negative-query correctness | 0 / 8 |
| Mean query runtime | 0.2743 s |
| Measured local text tokens | 459 |

The 459 tokens are non-padding OpenCLIP text-encoder tokens, not provider/API
billing tokens. Returning a top-ranked map object is not an accuracy metric.

## Evidence

- `outputs/baselines/conceptgraphs_replica_full_v1/run_config.json`
- `outputs/baselines/conceptgraphs_replica_full_v1/baseline_summary.md`
- `outputs/baselines/conceptgraphs_replica_full_v1/metrics_summary.json`
- `outputs/baselines/conceptgraphs_replica_full_v1/query_results/`
- `scripts/run_conceptgraphs_public.ps1`
- `scripts/prepare_conceptgraphs_replica_scene.py`

Reproduction command:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_conceptgraphs_public.ps1 `
  -Dataset replica -ReplicaFramesPerScene 5
```

## Interpretation

This run establishes native predicted-map evidence on official Replica data.
It is not a same-protocol ranking against SemanticSplat: ConceptGraphs builds
objects from 40 sampled RGB-D frames, while the SemanticSplat Replica pilot
retrieves over oracle GT-map candidates. The run therefore must not be used to
claim external-baseline superiority.
