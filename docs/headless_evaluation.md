# Headless Evaluation

The Week 2/3 runner is independent of Cursor and UI interaction.

## Commands

```powershell
python scripts/run_experiment.py --config configs/week2_replica.yaml
python scripts/run_experiment.py --config configs/week3_replica.yaml
```

Both committed configs use `stub` mode and the available `default` pilot. They generate canonical results, logs, metrics, and failure reports under `outputs/week2/` or `outputs/week3/`.

## Modes

| Mode | Behavior | Current status |
|---|---|---|
| `stub` | Reuses saved ViewJSON/tree data and deterministic lexical traversal. | Implemented and tested. |
| `cached_live` | Replays cache entries whose envelope declares verified `source_mode=live`. | Implemented and tested with fixtures; no project live cache is available. |
| `live` | Makes new provider calls. | Provider interface exists, but no concrete provider adapter is installed. |

Stub mode always records zero model calls, null token usage, and warnings that the result is not live reasoning.

## Live Configuration Blocker

Live mode reads credentials only from environment variables:

```text
SEMANTICSPLAT_PROVIDER
SEMANTICSPLAT_MODEL
SEMANTICSPLAT_API_KEY
```

No secrets are stored in config or source files. Even when these variables are present, live mode currently exits with an explicit error because a provider-specific HTTP/SDK adapter has not been selected or implemented. This is the remaining external-integration blocker.

## Cached-live Contract

`CachedModelClient` requires cache envelopes using `semanticsplat.model_cache.v1`, a matching request hash, and `source_mode=live`. Stub responses cannot be replayed as cached-live. Original provider/model/version and token usage are retained in the envelope.

## Resume

When `resume=true`, schema-compatible results with the same mode are retained and logged as `resumed`. Missing or invalid result files are recomputed. A run with `resume=false` refuses to overwrite an existing run directory.

## Current Data Limitation

The available pilot has constant depth. The runner marks depth unreliable, forces canonical `bbox_3d` to `null`, and the evaluator reports 3D IoU as `N/A`.
