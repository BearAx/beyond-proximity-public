# Agent-MCP Method Contract

Status date: 2026-07-23

Protocol ID: `mcp_hierarchical_semantic_traversal.v1`

This document freezes the scientific method for the next evaluation. The
project name remains a working name until the separate rename phase is
completed.

## 1. Main Method

The main method is an agent-agnostic MCP protocol for hierarchical semantic
retrieval over a captured 3D scene:

```text
natural-language query
  -> agent query decomposition
  -> MCP root and child inspection
  -> conservative top-down branch selection
  -> MCP leaf/view retrieval
  -> semantic confirmation and ranking
  -> grounded object/view result
  -> complete replayable trace
```

Cursor Agent is the interactive product client. The backend MCP tools expose
scene data, hierarchy traversal, geometry, persistence, and trace recording.
The backend does not impersonate Cursor or make hidden provider calls.

The reproducible experimental client is the pinned local model
`BAAI/bge-small-en-v1.5`, executed through FastEmbed ONNX on CPU. It replaces
agent language generation with neural semantic similarity while preserving
the same top-down MCP decision boundary. It is a semantic model baseline, not
an LLM and not evidence of Cursor Agent quality.

## 2. System Boundaries

One-time map construction:

- posed RGB-D capture and saved ViewJSON records;
- geometric proximity clustering;
- conservative deterministic semantic merge;
- agent-assisted zone/region naming and hierarchy persistence;
- optional precomputation of static embeddings.

Per-query execution:

- query understanding;
- branch scoring and pruning;
- view/object ranking;
- fallback expansion;
- grounding and output validation.

Construction time and construction tokens must never be mixed with per-query
cost.

## 3. Controlled Variants

The four required variants use identical scenes, records, queries, and view
ground truth:

| Variant | Hierarchy | Query scorer | Purpose |
|---|---|---|---|
| `flat_lexical` | no | deterministic token overlap | exhaustive control |
| `graph_lexical` | yes | deterministic token overlap | isolates lexical pruning |
| `flat_semantic_embedding` | no | pinned local BGE model | exhaustive semantic control |
| `graph_semantic_embedding` | yes | pinned local BGE model | reproducible semantic traversal |

The comparison does not claim that an embedding encoder is equivalent to
Cursor Agent. Cursor traces and local-model traces share the same trace
contract so their behavior can be audited without conflating them.

## 4. Frozen Evaluation Inputs

- Benchmark: `docs/benchmarks/benchmark_queries_v2.json`
- Query count: 150
- Query types: 25 each of simple-object, attribute, relational, functional,
  multi-hop, and negative
- Captured scenes: five
- Quality denominator: 125 queries with verified expected view IDs
- Negative-query quality: not reported because independent negative GT is
  unavailable

## 5. Required Measurements

Every method records:

- selected and ranked view IDs;
- visited nodes and checked views;
- semantic entries scanned;
- serialized context characters;
- input tokens and the token-counting method;
- model/agent call count;
- model inference and end-to-end latency;
- observed process RSS, labeled as process-level rather than per-method memory;
- model/backend identity;
- fallback or pruning decisions.

Quality over the 125 eligible queries:

- hit@1;
- hit@3;
- MRR over the complete produced ranking;
- expected-object-label hit;
- expected-zone-view hit and wrong-zone-view rate;
- paired graph-minus-flat confidence intervals.

Wrong-room rate is unavailable because the benchmark has manual zone
references but no independent room-level GT.

Efficiency over all 150 queries:

- mean checked views;
- mean context characters and input tokens;
- mean runtime;
- mean per-query graph-versus-flat reduction;
- paired bootstrap confidence intervals.

## 6. Token Accounting

Lexical variants:

- `input_tokens` is a local `cl100k_base` tokenizer count over inspected
  serialized context;
- `model_call_count` and provider tokens are zero because no model runs.

Local semantic variants:

- `input_tokens` is the actual native tokenizer count for
  `BAAI/bge-small-en-v1.5`;
- `model_input_tokens` equals the text processed by that encoder;
- `model_output_tokens` is zero because an embedding encoder emits vectors,
  not text.

Cursor Agent traces:

- use agent-reported input/output token usage when exposed;
- otherwise store null, never zero;
- identify the model and token method or mark them `unreported`.

## 7. Claim Boundary

The experiment may support:

> A hierarchy can reduce the amount of scene text and number of views processed
> by an identical lexical or local semantic scorer on the same semantic map.

It may not support without separate evidence:

- that Cursor Agent outperforms flat search;
- that the map or hierarchy was built automatically;
- semantic perception accuracy;
- provider cost or provider token claims;
- general superiority over ConceptGraphs, LangSplat, BBQ, SayPlan, or Search3D.

## 8. Acceptance Criteria

Phase 1 is complete when:

- the main method, controls, boundaries, denominators, and claims are fixed;
- Cursor and the reproducible local model are explicitly distinguished;
- construction and query cost are separated;
- negative and unavailable metrics cannot silently become zero.

Phase 3 is complete when:

- Cursor can start, append to, finish, and reload an MCP query trace;
- trace steps preserve requests, responses, model identity, tokens, and latency;
- a pinned local semantic client executes flat and graph traversal;
- local semantic traces are replayable JSON conforming to the published schema.

Phase 4 is complete when:

- all four variants finish all 150 queries;
- 125 eligible queries receive hit@1, hit@3, and MRR;
- paired uncertainty and efficiency comparisons are saved;
- commands, environment, hardware, model provenance, and per-query outputs are
  released with the aggregate metrics.
