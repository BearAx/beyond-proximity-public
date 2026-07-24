# Complete Qwen Instruction-Agent Benchmark

Status: **DONE_AND_VALIDATED**
Run date: 2026-07-24

## Scope

`Qwen/Qwen2.5-0.5B-Instruct` revision
`7ae557604adf67be50417f59c2c2f167def9a775` executed hierarchical
branch selection and view grounding for all 150 internal benchmark queries.
This is local deterministic CPU inference, not a lexical stub, API provider
call, or cache replay.

Each candidate receives a binary semantic-relevance instruction. Candidates
are ranked by the model's normalized first-token `Yes` probability. Every
system prompt, rendered candidate prompt, generated decision, candidate score,
branch choice, ranked view, native token count, call latency, and quality label
is stored in a per-query trace.

## Results

| Metric | Result |
|---|---:|
| Queries | 150 |
| Positive quality denominator | 125 |
| Complete traces | 150 |
| Valid response rate | 1.000 |
| hit@1 | 0.368 |
| hit@3 | 0.696 |
| MRR | 0.509 |
| Mean views checked | 9.63 |
| Mean model calls/query | 2.00 |
| Total model calls | 300 |
| Mean native input tokens/query | 1,582.9 |
| Mean output tokens/query | 16.4 |
| Total exact tokens | 239,893 |
| Mean CPU latency/query | 6.238 s |

The execution requirement is fully met. The small instruction model is a weak
ranker relative to the deterministic controls, so the result supports
operational agent integration and complete accounting, not an LLM-superiority
claim.

## Evidence

- `outputs/instruction_agent/five_scene_qwen25_05b_graph_v1/metrics_summary.json`
- `outputs/instruction_agent/five_scene_qwen25_05b_graph_v1/per_query_results.json`
- `outputs/instruction_agent/five_scene_qwen25_05b_graph_v1/per_query_metrics.csv`
- `outputs/instruction_agent/five_scene_qwen25_05b_graph_v1/traces/`
- `outputs/instruction_agent/five_scene_qwen25_05b_graph_v1/validation_report.json`

## Reproduce

```powershell
python -m pip install -r backend\requirements-experiments.txt
python -B scripts\run_instruction_agent_benchmark.py `
  --methods graph_instruction `
  --out outputs\instruction_agent\five_scene_qwen25_05b_graph_v1
python -B scripts\validate_instruction_agent_benchmark.py `
  --output outputs\instruction_agent\five_scene_qwen25_05b_graph_v1 `
  --expected-queries 150
```
