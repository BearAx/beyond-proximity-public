# ConceptGraphs Smoke Setup

Status date: 2026-06-23. Setup blocked; no heavy installation attempted.

Official source: https://github.com/concept-graphs/concept-graphs

The official Replica path requires a ConceptGraphs checkout, Python 3.10 environment, PyTorch/CUDA/PyTorch3D, Grounded-SAM or related segmentation stack, LLaVA and checkpoints, Nice-SLAM Replica RGB-D trajectories, and generated segmentation/detection outputs.

Official mapping entrypoint shape:

```text
python slam/cfslam_pipeline_batch.py dataset_root=<REPLICA_ROOT> dataset_config=<REPLICA_CONFIG_PATH> ...
```

## Local Gaps

- No ConceptGraphs checkout or pinned revision.
- No `conceptgraph` Conda environment.
- No segmentation, FastSAM/MobileSAM/HQ-SAM, or LLaVA checkpoints.
- No baseline GSA preprocessing outputs.
- Captured scenes are not converted to the official Nice-SLAM Replica/config layout.
- No native map (`pkl.gz`) exists for canonical adaptation.

The RTX 3060 Laptop GPU is visible, but hardware visibility alone does not clear software, checkpoint, or data-format gates.

## Canonical Adapter

`scripts/adapt_conceptgraphs_output.py` accepts a JSON export only when it includes `native_execution=true`, repository revision, exact native command, checkpoint identifiers, existing native artifact paths, and per-query predictions/metrics. It refuses incomplete provenance before creating an output directory.

Expected adaptation command after a real native run:

```powershell
python -B scripts\adapt_conceptgraphs_output.py `
  --native outputs\baselines\conceptgraphs_smoke_v1\native_results.json `
  --benchmark docs\benchmarks\benchmark_queries_v1.json `
  --scene-id ConferenceHall-capture-pilot `
  --benchmark-scene-id ConferenceHall `
  --mode live `
  --out outputs\baselines\conceptgraphs_smoke_v1
```
