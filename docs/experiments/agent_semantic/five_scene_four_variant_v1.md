# Four-Variant Agent-Semantic Benchmark V1

Status: completed and validated

Date: 2026-07-23

Protocol: `mcp_hierarchical_semantic_traversal.v1`

## Scope

This run completes the first controlled comparison of:

- flat lexical search;
- graph lexical search;
- flat neural semantic search;
- graph neural semantic traversal.

All methods use the same five captured scenes, 150 queries, saved semantic
records, and 125-query verified-view quality denominator. Negative-query
correctness is not reported because independent negative GT is unavailable.

The neural methods use `BAAI/bge-small-en-v1.5` through FastEmbed ONNX on CPU.
This is a real local semantic model, but it is not an LLM or a Cursor Agent
execution.

## Command

```powershell
python -B scripts\run_agent_semantic_benchmark.py `
  --out outputs\agent_semantic\five_scene_four_variant_v1 `
  --bootstrap-samples 10000

python -B scripts\validate_agent_semantic_benchmark.py `
  --output outputs\agent_semantic\five_scene_four_variant_v1
```

## Aggregate Results

| Method | hit@1 | hit@3 | MRR | Object hit | Zone-view hit | Views/query | Tokens/query | Runtime ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Flat lexical | 0.768 | 0.928 | 0.846 | 0.648 | 0.768 | 19.40 | 3,168.20 | 6.39 |
| Graph lexical | 0.680 | 0.808 | 0.742 | 0.632 | 0.680 | 4.77 | 1,014.26 | 5.53 |
| Flat semantic | 0.680 | 0.928 | 0.800 | 0.640 | 0.680 | 19.40 | 2,321.39 | 872.42 |
| Graph semantic | 0.664 | 0.784 | 0.717 | 0.624 | 0.664 | 3.90 | 1,566.97 | 364.19 |

Lexical graph versus flat:

- views: 75.43% reduction by ratio of means;
- input tokens: 67.99% reduction by ratio of means;
- hit@1 difference: -0.088, 95% CI [-0.184, 0.008];
- hit@3 difference: -0.120, 95% CI [-0.184, -0.056].

Semantic graph versus flat:

- views: 79.90% reduction by ratio of means;
- native model input tokens: 32.50% reduction by ratio of means;
- mean per-query token reduction: 32.73%, 95% CI [27.11, 38.21];
- hit@1 difference: -0.016, 95% CI [-0.096, 0.064];
- hit@3 difference: -0.144, 95% CI [-0.224, -0.072];
- MRR difference: -0.082, 95% CI [-0.150, -0.016].

The semantic hierarchy therefore reduces model input and checked views, but
the frozen pruning rule does not preserve top-3 quality. The hit@1 difference
is inconclusive at 95%; the hit@3 and MRR declines are significant.

## Accounting

- Flat semantic: 348,209 native model input tokens and 450 encoder calls.
- Graph semantic: 235,045 native model input tokens and 1,237 encoder calls.
- Model load: 9.459 seconds.
- Model warmup: 0.006 seconds.
- Scene bundle load: 0.334 seconds.
- Process RSS after model load: 212.88 MB.
- Peak process RSS observed after method calls: 471.00 MB.

The graph uses more small encoder calls because it makes decisions at multiple
hierarchy levels. It processes fewer tokens and is faster in this CPU run, but
call count is reported separately so an API-backed agent cost is not inferred.

## Evidence

Local generated evidence:

```text
outputs/agent_semantic/five_scene_four_variant_v1/run_config.json
outputs/agent_semantic/five_scene_four_variant_v1/metrics_summary.json
outputs/agent_semantic/five_scene_four_variant_v1/metrics_summary.md
outputs/agent_semantic/five_scene_four_variant_v1/per_query_results.json
outputs/agent_semantic/five_scene_four_variant_v1/per_query_metrics.csv
outputs/agent_semantic/five_scene_four_variant_v1/traces/
outputs/agent_semantic/five_scene_four_variant_v1/validation_report.json
```

Validation result:

```text
150 queries
125 quality-eligible queries
4 methods
600 per-query method rows
300 semantic traces
0 validation errors
```

## Claim Boundary

This run proves that a pinned neural semantic scorer can execute through the
same hierarchical decision boundary as the MCP agent workflow. It does not
measure Cursor Agent, an instruction-tuned LLM, automatic map construction, or
semantic perception accuracy.
