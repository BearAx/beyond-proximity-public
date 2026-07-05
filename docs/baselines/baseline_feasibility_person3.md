# Baseline Feasibility: Person 3

Status date: 2026-07-02  
Branch: `feature-person-3-baselines-literature`

## Decision Table

| Method | Can be measured now? | Required before measurement | Current status |
|---|---:|---|---|
| Flat lexical search | Yes | Person 1 same-input runner and metrics export | Required internal baseline. |
| Graph traversal over our tree | Yes | Person 1 same-input runner and GT-aware denominators | Required proposed method condition. |
| Flat embedding search | Maybe | Embedding model choice, deterministic cache, same semantic items | Optional, useful if time allows. |
| LangSplat | No | Scene conversion, 3DGS-language training path, relevancy-to-result adapter | Literature-only for sprint. |
| ConceptGraphs | No | RGB-D scene adapter, segmentation/model setup, graph export adapter | Literature-only for sprint. |
| HOV-SG | No | Method-specific map input, hierarchy export adapter | Literature-only for sprint. |
| LERF | No | NeRF training setup and relevancy adapter | Literature-only; less direct than LangSplat. |
| Semantic Gaussians | No | 3DGS semantic feature setup and output adapter | Literature-only; optional future baseline. |
| LEGS | No | Robot trajectory / online mapping setup | Literature-only; robot-mapping context. |
| BBQ | No | 3D scene graph adapter, object-grounding output adapter, saved result JSON | Literature-only; close graph-query context. |
| ScanRefer | No | ScanNet-style object proposals and annotated 3D targets | Citation for grounding task. |
| OpenMask3D | No | 3D instance masks/proposals and semantic labels | Future segmentation metric source. |
| OpenLex3D | No | Dataset/benchmark integration | Evaluation framing only. |

## Internal Baselines For Article Results

| Result name | Meaning | Status |
|---|---|---|
| `flat_lexical` | Exhaustive lexical search over the same five-scene semantic items. | Required |
| `graph_traversal` | Existing/adapted graph traversal over the same five-scene semantic items. | Required |
| `flat_embedding` | Embedding search over the same semantic items with deterministic cache. | Optional |
| `graph_affordance_pruned` | Graph traversal with deterministic intent/affordance expansion. | Optional |

## Result Table Naming Rule

| Allowed wording | Avoid wording |
|---|---|
| "We compare graph traversal against flat retrieval over the same semantic items." | "We outperform LangSplat / ConceptGraphs / HOV-SG." |
| "External methods are discussed as related work." | "External methods are baselines." |
| "3D IoU metrics are future work because GT boxes are unavailable." | "We evaluate 3D localization accuracy." |
| "mIoU/AP metrics require masks or semantic labels." | "We report segmentation accuracy." |

## Note on Token / Context Metrics

The reviewed 3D scene understanding papers do not use LLM token count as a primary evaluation metric. HOV-SG mentions semantic tokens as an interface for prompting LLMs, but it evaluates representation size, hierarchy, semantic accuracy, retrieval, and navigation rather than token count.

For token/context metrics, we use RAG and prompt-compression literature. AttentionRAG, Provence, TeaRAG, S-Path-RAG, and prompt-compression surveys motivate measuring how much context is passed to an LLM and how context pruning affects quality and efficiency.

In our project, these are internal graph-vs-flat efficiency metrics:

| Metric | Meaning |
|---|---|
| `context_size_chars` | Character count of context passed to the query model. |
| `estimated_input_tokens` | Estimated or tokenizer-counted input tokens. |
| `token_reduction_vs_flat` | Relative reduction in graph input tokens compared with flat retrieval. |
| `semantic_entries_scanned` | Number of semantic entries touched by the method. |
| `latency_ms` | Query-time latency for the method. |
| `compression_ratio` | Flat input tokens divided by graph input tokens. |

These metrics should only be compared between internal methods that run on the same scenes, semantic items, query strings, and verified labels:

| Method | Status |
|---|---|
| `flat_lexical` | Required |
| `graph_traversal` | Required |
| `flat_embedding` | Optional |
| `graph_affordance_pruned` | Optional |

They should not be presented as standard 3D scene understanding metrics, and they should not be used to claim superiority over AttentionRAG, Provence, TeaRAG, S-Path-RAG, LangSplat, LERF, HOV-SG, or OpenLex3D unless same-input adapters and saved result JSON exist.

Formulas:

| Metric | Formula |
|---|---|
| `token_reduction_vs_flat` | `1 - graph_estimated_input_tokens / flat_estimated_input_tokens` |
| `compression_ratio` | `flat_estimated_input_tokens / graph_estimated_input_tokens` |

Only compute these when flat and graph methods are run on the same query and the same semantic item set.

## Recommended Sprint Scope

For the article draft, use external papers as related work and compare experimentally only against internal same-input baselines. This keeps the results defensible even if the external repositories are not installed.

Minimum Person 3 handoff to Persons 1 and 4:

| Need | Handoff |
|---|---|
| Baseline naming | Use `flat_lexical`, `graph_traversal`, optional `flat_embedding`, and optional `graph_affordance_pruned`; avoid calling external systems measured baselines. |
| Metrics language | Report context chars/tokens, scanned entries, visited nodes, latency, and hit@k only where verified labels exist. |
| Related work citations | Use existing `refs.bib` keys only after metadata/key names are verified. See `docs/baselines/bibliography_todo_person3.md`. |
| Claim boundary | No "faster than LangSplat/ConceptGraphs/HOV-SG" without same-input runs. |

## Exact Blockers For External Baselines

| Method | Blocker | Evidence needed to clear it |
|---|---|---|
| LangSplat | Requires language-enhanced 3DGS training and output thresholding. | Saved command, config, trained scene, query adapter, and result JSON. |
| ConceptGraphs | Requires segmentation and multi-view association stack. | Exported object graph with scene IDs matching benchmark queries. |
| HOV-SG | Requires a compatible open-vocabulary segment map. | Hierarchy export with rooms/objects mapped to our scene/query IDs. |
| BBQ | Requires a compatible 3D scene graph/object-grounding path. | Saved adapter outputs and query-result JSON on our scene/query subset. |
| LERF | Requires NeRF training, not current 3DGS/view-summary inputs. | Trained NeRF and fixed relevancy-map adapter. |
| ScanRefer/OpenLex3D/OpenMask3D | Require labeled datasets, object-level GT, masks, or semantic labels not present in captured scenes. | Ground-truth 3D boxes/segments/labels and query mapping. |

## Person 3 Final Handoff

For Person 1, export exactly these method names where implemented:

| Method name | Required? |
|---|---:|
| `flat_lexical` | Yes |
| `graph_traversal` | Yes |
| `flat_embedding` | Optional |
| `graph_affordance_pruned` | Optional |

For Person 1, export these metrics where available:

| Metric | Notes |
|---|---|
| `latency_ms` | Query-time latency; keep construction/preprocessing separate if reported. |
| `semantic_entries_scanned` | Count entries touched by the method. |
| `objects_checked` | Count candidate objects checked. |
| `regions_checked` | Count candidate regions checked. |
| `views_checked` | Count views checked. |
| `visited_nodes` | Graph/tree nodes visited; use `0` or `null` consistently for flat methods. |
| `context_size_chars` | Prompt/context size in characters. |
| `estimated_input_tokens` | Token estimate or provider tokenizer count; document method. |
| `token_reduction_vs_flat` | Compute only for paired flat/graph runs on the same query and semantic items. |
| `compression_ratio` | Compute only for paired flat/graph runs on the same query and semantic items. |
| `hit_at_1` | Compute only where verified expected labels exist. |
| `hit_at_3` | Compute only where verified expected labels exist. |
| `expected_object_hit` | Compute only where expected object labels are verified. |
| `expected_region_hit` | Compute only where expected region labels are verified. |
| `expected_zone_hit` | Compute only where expected zone labels are verified. |
| `expected_view_hit` | Compute only where expected view labels are verified. |

Quality metrics should be computed only where verified expected labels exist. Missing, ambiguous, or unverified labels must be excluded from denominators and reported separately.

For Person 4 article writing:

| Use | Guidance |
|---|---|
| Closest related works | Use HOV-SG, BBQ, and OpenLex3D as closest related works. |
| Language-field context | Use LERF, LangSplat, Semantic Gaussians, and LEGS as language-field / 3DGS semantic representation context. |
| Future metric sources | Use ScanRefer, OpenMask3D, and OpenLex3D as future metric sources. |
| Claim boundary | Do not write that our method beats external systems unless Person 1 produces same-input external baseline results. |
