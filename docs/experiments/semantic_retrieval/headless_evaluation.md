# Headless Evaluation

The Week 2/3 runner is independent of Cursor and UI interaction.

## Commands

```powershell
python scripts/run_experiment.py --config configs/week2_replica.yaml
python scripts/run_experiment.py --config configs/week3_replica.yaml
python -B scripts\run_experiment.py --config configs\week3_replica.yaml --mode live --limit 5 --out outputs\week3\live_gate_v1
```

Both committed configs default to `stub`. CLI overrides can select a mode, query limit, and complete run output directory. The Week 3 config contains the five validated capture scenes.

## Modes

| Mode | Behavior | Current status |
|---|---|---|
| `stub` | Reuses saved ViewJSON/tree data and deterministic lexical traversal. | Implemented and tested. |
| `cached_live` | Replays cache entries whose envelope declares verified `source_mode=live`. | Implemented and tested; no project live cache is available yet. |
| `live` | Runs query reasoning through the OpenAI Responses API over the validated manual semantic index. | Adapter implemented and tested; real run blocked on environment configuration. |

Stub mode always records zero model calls, null token usage, and warnings that the result is not live reasoning.

## Live Configuration

Live mode reads credentials only from environment variables:

```text
SEMANTICSPLAT_PROVIDER
SEMANTICSPLAT_MODEL
SEMANTICSPLAT_API_KEY
```

Set the variables in the current PowerShell process. Use an OpenAI model available to the account that supports the Responses API:

```powershell
$env:SEMANTICSPLAT_PROVIDER = "openai"
$env:SEMANTICSPLAT_MODEL = "<responses-api-model>"
$env:SEMANTICSPLAT_API_KEY = "<api-key>"

python -B scripts\run_experiment.py `
  --config configs\week3_replica.yaml `
  --mode live `
  --limit 5 `
  --out outputs\week3\live_gate_v1
```

No secrets are stored in config, logs, cache envelopes, or source files. Existing manual ViewJSON and trees are reused; the provider performs query reasoning only. This keeps the five-query gate to five provider calls rather than re-captioning all 96 images.

GPT-5-style reasoning models reject legacy sampling parameters. When the selected model starts with `gpt-5`, `o1`, `o3`, or `o4`, the adapter omits `temperature`, `top_p`, `presence_penalty`, `frequency_penalty`, `logprobs`, `top_logprobs`, and `logit_bias`. Older model families retain `temperature=0` for deterministic evaluation where the API supports it.

The 2026-06-23 attempt stopped before provider execution because all three variables were absent. It wrote a failed `run_config.json` and `logs.json`, zero query results, and zero cache entries.

## Cached-live Contract

`CachedModelClient` requires cache envelopes using `semanticsplat.model_cache.v1`, a matching request hash, and `source_mode=live`. Stub responses cannot be replayed as cached-live. The envelope retains provider/model/version, token usage, the canonical response, and the raw provider response without authorization headers or API keys.

## Resume

When `resume=true`, schema-compatible results with the same mode are retained and logged as `resumed`. Missing or invalid result files are recomputed. A run with `resume=false` refuses to overwrite an existing run directory.

## Current Data Limitation

The five capture scenes have valid non-constant depth, but independent GT and predicted 3D boxes are unavailable. The evaluator therefore keeps 3D IoU at `N/A`. Manual semantic annotations are model inputs, not independent accuracy GT.
