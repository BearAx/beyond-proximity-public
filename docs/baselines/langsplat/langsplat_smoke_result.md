# LangSplat Smoke Result

Status date: 2026-06-26. Result: native smoke executed.

## Commands Run

```powershell
docker pull pytorch/pytorch:1.13.1-cuda11.6-cudnn8-devel
docker build --progress=plain -t semanticsplat-langsplat:d70edb8 baselines\langsplat
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_langsplat_smoke.ps1
python -B scripts\evaluate_results.py --benchmark docs\benchmarks\baseline_smoke_queries_v1.json --run-dir outputs\baselines\langsplat_smoke_v1
```

## Build Fixes Required

- `baselines/langsplat/Dockerfile` now pins `setuptools<81` because PyTorch 1.13 extension code imports `pkg_resources`.
- `baselines/langsplat/Dockerfile` installs CUDA extensions with `--no-build-isolation` so the extension build can see the base-image `torch`.
- `scripts/run_langsplat_smoke.ps1` discovers the actual LangSplat render output path. The official render wrote `train/ours_None/renders_npy/00000.npy`, not `train/ours_30000/renders_npy/00000.npy`.
- `scripts/run_langsplat_smoke.ps1` treats Docker stderr as log output and checks `$LASTEXITCODE` explicitly.

## Evidence

| Artifact | Status |
|---|---|
| Docker image | `semanticsplat-langsplat:d70edb8` built |
| Native render log | `outputs/baselines/langsplat_smoke_v1/native_render.log` |
| Rendered feature map | `C:/GitProjects/baseline-deps/LangSplat-assets/output/sofa_1/train/ours_None/renders_npy/00000.npy` |
| Native query log | `outputs/baselines/langsplat_smoke_v1/native_query.log` |
| Native result | `outputs/baselines/langsplat_smoke_v1/native_results.json` |
| Canonical result | `outputs/baselines/langsplat_smoke_v1/query_results/ls001.json` |
| Metrics summary | `outputs/baselines/langsplat_smoke_v1/metrics_summary.json` |

## Result

```text
baseline process executed = true
native outputs = 1
canonical query results = 1
schema-valid results = 1
measured native query runtime = 106.7092 seconds
native relevancy score = 0.4495883882045746
found = false
accuracy = N/A, no GT
3D IoU = N/A, no reliable GT 3D box or predicted 3D box
```

This run uses the official pretrained LangSplat sofa assets. It is not a run on the five captured SemanticSplat scenes and does not establish head-to-head accuracy. The query is marked `missing_gt`, so the valid claim is native execution plus canonical adapter compatibility.
