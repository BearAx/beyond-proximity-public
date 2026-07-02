# LangSplat Smoke Setup

Status date: 2026-06-23. Setup blocked; no heavy installation attempted.

Official source: https://github.com/minghanqin/LangSplat

The official smoke path requires a LangSplat checkout/environment, compatible SfM/3DGS scene, pretrained RGB Gaussian checkpoint, SAM-derived language features, autoencoder/checkpoints, and a trained or downloaded LangSplat model.

Official pretrained render entrypoint shape:

```text
python render.py -m output/<case_name> --include_feature
```

## Local Gaps

- No LangSplat checkout or pinned revision.
- No `langsplat` Conda environment.
- No compatible pretrained RGB 3DGS or LangSplat model.
- No SAM checkpoint, language features, or autoencoder checkpoint.
- Captured scenes are not converted to the expected SfM/LangSplat layout.
- The local GPU has 6 GB VRAM versus the README's 24 GB paper-quality training recommendation.

A pretrained render smoke could require less memory than training, but no compatible model or dataset is available.

## Canonical Adapter

`scripts/adapt_langsplat_output.py` accepts a JSON export only when it includes `native_execution=true`, repository revision, exact native command, checkpoint identifiers, existing native artifact paths, and per-query relevancy predictions/metrics. It refuses incomplete provenance before creating an output directory.

Expected adaptation command after a real native run:

```powershell
python -B scripts\adapt_langsplat_output.py `
  --native outputs\baselines\langsplat_smoke_v1\native_results.json `
  --benchmark docs\benchmarks\benchmark_queries_v1.json `
  --scene-id ConferenceHall-capture-pilot `
  --benchmark-scene-id ConferenceHall `
  --mode live `
  --out outputs\baselines\langsplat_smoke_v1
```
