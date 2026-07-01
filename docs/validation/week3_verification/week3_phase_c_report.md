# Week 3 Phase C Report

Status date: 2026-06-23. Adapter complete; real live acceptance blocked on credentials.

## Implemented

- Added `OpenAIModelClient` behind the provider-independent `ModelClient` interface.
- Reused validated manual ViewJSON/tree data and limited provider work to query reasoning.
- Added retry/failure counters, real token usage accounting, and measured runtime.
- Added verified-live cache envelopes with canonical and raw provider responses, excluding API keys and authorization headers.
- Added `--limit` and `--out` CLI overrides. A five-query limit prepares only the scene needed by those queries.
- Added regression tests for provider selection, retries, cache provenance, secret exclusion, and CLI overrides.
- Added model-family payload filtering: `gpt-5*`, `o1*`, `o3*`, and `o4*` omit unsupported sampling parameters, while older models receive `temperature=0`.

## Configure And Run

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

Do not store the key in repository files. After a successful run, verify:

```powershell
Get-ChildItem outputs\week3\live_gate_v1\query_results\*.json
Get-Content outputs\week3\live_gate_v1\run_config.json
Get-ChildItem outputs\week3\model_cache -Recurse -Filter *.json
```

Acceptance requires at least one result with `mode: live` and `metrics_log.model_call_count > 0`. Token usage must be provider-reported or `null`.

## Current Attempt

The expected command was run with the current environment. It failed explicitly because all three variables were absent. The failed run has zero query results and zero cache entries. Phase D must not start until a real live result and verified-live cache exist.

A later manual `gpt-5.5` attempt reached the provider but failed with HTTP 400 because the request included unsupported `temperature`. The adapter now omits `temperature`, `top_p`, `presence_penalty`, `frequency_penalty`, `logprobs`, `top_logprobs`, and `logit_bias` for GPT-5/o-series models. This fix is covered by payload-level tests; a new credentialed live run is still required.
