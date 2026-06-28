# Headless Evaluation

The Week 2/3 runner is independent of Cursor and UI interaction.

## Commands

```powershell
python scripts/run_experiment.py --config configs/week2_replica.yaml
python scripts/run_experiment.py --config configs/week3_replica.yaml
```

Both committed configs default to `stub`. CLI overrides can select a query limit and complete run output directory. The Week 3 config contains the five validated capture scenes.

## Modes

| Mode | Behavior | Current status |
|---|---|---|
| `stub` | Reuses saved ViewJSON/tree data and deterministic lexical traversal. | Implemented and tested. |
| `cached_live` | Legacy replay path for verified live envelopes. | Out of scope for the next phase; no project live cache is available. |
| `live` | Legacy provider-backed query reasoning path. | Out of scope for the next phase. |

Stub mode always records zero model calls, null token usage, and warnings that the result is not live reasoning.

## Live / Cached-Live Scope

Live and cached-live are no longer part of the active evaluation plan. Keep any existing code paths honest if they remain in the repository, but do not spend next-phase work on provider credentials, provider calls, or cached-live replay.

## Cached-live Contract

`CachedModelClient` requires cache envelopes using `semanticsplat.model_cache.v1`, a matching request hash, and `source_mode=live`. Stub responses cannot be replayed as cached-live. Since no verified live cache exists and cached-live is out of scope, no cached-live metric is reported.

## Resume

When `resume=true`, schema-compatible results with the same mode are retained and logged as `resumed`. Missing or invalid result files are recomputed. A run with `resume=false` refuses to overwrite an existing run directory.

## Current Data Limitation

The five capture scenes have valid non-constant depth, but independent GT and predicted 3D boxes are unavailable. The evaluator therefore keeps 3D IoU at `N/A`. Manual semantic annotations are model inputs, not independent accuracy GT.
