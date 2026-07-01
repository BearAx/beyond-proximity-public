# LangSplat Status

Status date: 2026-06-26. Status: `READY`.

## Evidence

| Check | Status | Evidence |
|---|---|---|
| In-repo checkout | not used | Smoke uses a pinned Docker build from official `https://github.com/minghanqin/LangSplat` |
| External checkout | present | `C:/GitProjects/baseline-deps/LangSplat` exists, but Docker build is the source of execution evidence |
| Conda env | not required | Smoke runs in Docker image `semanticsplat-langsplat:d70edb8` |
| Docker runtime | available | Docker Desktop ran the smoke with `--gpus all` |
| Checkpoints/assets | present | `C:/GitProjects/baseline-deps/LangSplat-assets` contains official sofa `data`, `ckpt`, and `output` folders |
| GPU/CUDA assumption | satisfied for smoke | Docker GPU check reported NVIDIA GeForce RTX 3060 Laptop GPU, 6144 MiB |
| Input format | official sofa only | Current captured SemanticSplat scenes are still not converted to LangSplat native SfM/3DGS layout |
| Smoke command availability | present | `scripts/run_langsplat_smoke.ps1` |
| Native output | present | `outputs/baselines/langsplat_smoke_v1/native_results.json` |
| Canonical output | present | `outputs/baselines/langsplat_smoke_v1/query_results/ls001.json` |
| Metrics summary | present | `outputs/baselines/langsplat_smoke_v1/metrics_summary.json` |
| Canonical adapter | present | `scripts/adapt_langsplat_output.py` |
| Adapter tests | present | `tests/backend/test_baseline_adapters.py` |

## Smoke Result

LangSplat executed on the official pretrained sofa assets. The run rendered feature maps under `C:/GitProjects/baseline-deps/LangSplat-assets/output/sofa_1/train/ours_None/`, queried `renders_npy/00000.npy`, wrote native evidence, and adapted one canonical query result.

This is a smoke result, not a SemanticSplat five-scene comparison. The benchmark query has `verification_status: missing_gt`, so accuracy, retrieval success, and 3D IoU are unavailable.

Observed canonical result:

```text
query_id = ls001
mode = live
schema_valid_result_count = 1
native relevancy score = 0.4495883882045746
found = false
accuracy_eligible_result_count = 0
```

## Reproduction Command

Run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_langsplat_smoke.ps1
```

Then evaluate:

```powershell
python -B scripts\evaluate_results.py `
  --benchmark docs\benchmarks\baseline_smoke_queries_v1.json `
  --run-dir outputs\baselines\langsplat_smoke_v1
```

## Remaining Gap

The official sofa smoke proves LangSplat native execution and canonical adaptation. It does not prove fair comparison on the five captured SemanticSplat scenes. That still requires converting captured scenes into LangSplat's native SfM/3DGS format or training/loading compatible LangSplat scene assets.
