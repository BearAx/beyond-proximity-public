# ChatGPT Project Description: SemanticSplat / Beyond Proximity

Status date: 2026-06-28.

This file is project context for ChatGPT. Use it to understand the goal, evaluation direction, required claims, and current evidence for SemanticSplat / Beyond Proximity.

## One-Sentence Description

SemanticSplat / Beyond Proximity is a semantic-map intelligence layer that turns captured visual and 3D observations into a structured semantic graph so a computer can answer useful questions about what is around it, where to go, what a place means, and what changed in the environment.

## Main Goal

The main research and product goal is to prove, with reproducible evidence, that a structured semantic graph can answer environment-understanding queries with less context, fewer tokens, and lower latency than comparable flat or baseline approaches while preserving useful answer quality.

This must be measured, not assumed. Until measurements exist, phrase it as a target claim:

```text
Target claim: SemanticSplat graph-based reasoning should use fewer tokens and answer faster than flat semantic search or comparable semantic-map algorithms on the same scenes and queries.
```

Do not claim this is already proven unless there is a saved benchmark result with matching methods, inputs, token/context metrics, runtime metrics, and quality metrics.

## Core Understanding Questions

The system exists to help a computer understand what happened around it and maintain that understanding over time. It must be able to answer:

```text
What is around me?
Where should I go?
What does this place mean?
What changed in the environment?
```

These questions define the project, benchmark, and demo scope.

## What "Computer Understands The Environment" Means

In this project, environment understanding means the system can maintain a structured semantic representation of a place, including:

```text
zones
rooms
corridors
landmarks
signs
exits
POIs
facilities
objects
regions
relations
view references
map-change status
```

It should represent relationships such as:

```text
inside
near
left_of / right_of
connected_to
visible_from
belongs_to_zone
leads_to
changed_from_previous_version
```

The system does not replace VPS, localization, AR tracking, or a 3D reconstruction engine. It adds semantic meaning above the existing map and positioning stack.

## Project Pipeline

The intended pipeline is:

```text
captured RGB-D views / visual observations
  -> ViewJSON annotations or automatic semantic extraction
  -> semantic index
  -> scene tree / semantic graph
  -> query pipeline
  -> result JSON
  -> evaluation reports
```

The current prototype uses manual semantic indexes as controlled reference maps. The final system should replace this manual step with automatic VLM-based semantic extraction.

## Primary Experiment: Token And Speed Efficiency

The main technical experiment is graph reasoning versus flat alternatives.

Compare:

```text
flat search over all semantic entries
flat embedding search
VLM or LLM over all available scene context
graph search
graph search + pruning / top-k
ConceptGraphs, LangSplat, or other baselines when fair execution is available
```

Measure efficiency:

```text
latency_ms
semantic_entries_scanned
objects_checked
views_checked
context_size_chars
estimated_or_actual_input_tokens
estimated_or_actual_output_tokens
total_tokens
model_call_count
cache_hit_count
speedup_vs_flat
token_reduction_vs_flat
```

Measure quality only when Ground Truth is available:

```text
hit@1
hit@3
expected_object_hit
expected_region_hit
expected_zone_hit
expected_view_hit
wrong_zone_rate
wrong_room_rate
negative_correctness
```

Without independent GT, do not report semantic accuracy. Report only schema validity, availability, coverage, runtime, mode, model_call_count, cache_hit_count, and token/context counts.

## Required Benchmark Query Types

The benchmark should cover:

```text
simple semantic search
relational search
multi-hop search
intent navigation
POI search
map freshness / update query
repetitive-space ambiguity query
```

Example queries:

```text
Where is the nearest exit?
Where is the reception desk?
I need to charge my phone.
Find the seating area near the lobby.
Which sign is near the elevator?
What changed in this corridor?
Which elevator is next to the blue sign?
What is around me?
Where should I go?
What does this place mean?
```

## Current Evidence

The current safe project status is:

```text
5 captured scenes
96 RGB-D captured views
96 manual ViewJSON annotations
1,046 semantic items
5 semantic indexes
5 generated trees
40 five-scene stub benchmark outputs
50 default-scene stub benchmark outputs
90 total benchmark queries
87 passing backend tests
```

Current scene set:

```text
backend/data/scenes/ConferenceHall-capture-pilot
backend/data/scenes/Museume-capture
backend/data/scenes/Theater-capture
backend/data/scenes/outdoor-street-capture
backend/data/scenes/outdoor-drone-capture
```

Important spelling note: `Museume-capture` is intentionally spelled this way in current data and docs unless renamed globally.

## Current Safe Claim

Use this as the safest honest description:

```text
SemanticSplat currently provides a reproducible, test-backed evaluation prototype over five manually captured and manually annotated RGB-D pilot scenes. It includes canonical schemas, semantic indexes, generated trees, benchmark queries, and stub-mode query evaluation. Live and cached-live evaluation are out of scope for the next phase. ConceptGraphs has a one-frame smoke result and LangSplat has an official-sofa smoke result, but neither is a fair five-scene comparison or GT-backed accuracy result. The project does not yet provide official Replica/ScanNet results, independent semantic accuracy, 3D IoU, or baseline head-to-head comparison.
```

## Claims To Prove Next

The next phase should prove these claims with evidence:

```text
SemanticSplat graph reasoning uses fewer tokens than flat search over the same semantic map.
SemanticSplat graph reasoning has lower latency than flat search over the same semantic map.
SemanticSplat preserves useful answer quality while reducing context size.
SemanticSplat can answer "what is around me" from a semantic index.
SemanticSplat can resolve "where should I go" into a target zone, object, view, or route hint.
SemanticSplat can explain "what does this place mean" using zones, POIs, landmarks, and relations.
SemanticSplat can report "what changed" when comparing two versions of a semantic map.
```

Each claim needs saved evidence paths, commands, configs, outputs, and metrics before it can be treated as proven.

## Proof And Maintenance Loop

The project must continuously maintain evidence that the system understands the environment. For every major change:

```text
1. Validate scene data and semantic indexes.
2. Run stub-mode regression queries.
3. Run graph-vs-flat efficiency comparison when benchmark code is available.
4. Record token/context counts and runtime for every method.
5. Record quality metrics only for queries with verified GT.
6. Save outputs under versioned output directories.
7. Update project docs with measured results and explicit limitations.
8. Do not overwrite claims with unsupported wording.
```

Recommended recurring evidence files:

```text
docs/validation/semantic_index/
docs/validation/capture_quality/
docs/benchmarks/benchmark_queries_v2.json
outputs/graph_vs_flat/<run_id>/
outputs/token_efficiency/<run_id>/
docs/experiments/stub/
docs/experiments/graph_vs_flat/
docs/project/real_evaluation_status.md
```

## Modes And Honesty Rules

Use these labels exactly:

```text
stub = deterministic local mode, no real model call
live = real provider/API model call
cached_live = replay of verified real live output
manual semantic index = human/Cursor-assisted annotation, not independent GT
GT = Ground Truth, expected correct answer used for accuracy
```

Do not claim:

```text
live model evaluation succeeded without at least one real mode: live output
cached_live succeeded without a verified live cache
ConceptGraphs or LangSplat ran without native output or logged execution attempt
semantic accuracy without independent GT
3D IoU without GT boxes and predicted boxes
Replica or ScanNet results without official dataset ingestion and evaluation
automatic/headless pipeline while manual capture, manual ViewJSON, or manual tree building is required
algorithm superiority without a fair same-input benchmark
```

Live and cached-live evaluation are out of scope for the next phase unless the user explicitly reopens that scope.

## Roadmap Based On Plan2

Phase 1: Define environment understanding.

```text
semantic schema
entity taxonomy
relation taxonomy
example semantic map JSON
```

Phase 2: Build a manual semantic-map dataset.

```text
5-10 scenes
manual ViewJSON annotations
semantic graphs / trees
validation reports
```

Phase 3: Create a semantic search and intent benchmark.

```text
100-150 verified queries
simple GT for objects, regions, zones, views, and POIs
freshness and ambiguity cases
```

Phase 4: Run the graph-vs-flat token and speed experiment.

```text
flat search
flat embedding search
graph search
graph search + pruning / top-k
token reduction table
latency speedup table
quality retention table
failure cases
```

Phase 5: Demonstrate partner-value capabilities.

```text
semantic search
intent navigation
map freshness
repetitive-space ambiguity reduction
```

Phase 6: Transition from manual to automatic understanding.

```text
automatic VLM ViewJSON generation
automatic semantic map construction
automatic-vs-manual comparison
query performance drop analysis
```

Phase 7: External baselines.

```text
ConceptGraphs smoke and documented blockers
LangSplat smoke and documented blockers
fair same-scene comparison only when setup and data are valid
```

Phase 8: ScanNet validation.

```text
small official ScanNet subset
working ingestion
semantic map generated
graph-vs-flat benchmark
comparison against available labels where possible
```

## Final Story To Tell

The final project story should be:

```text
1. Indoor positioning gives coordinates, but not meaning.
2. SemanticSplat builds semantic understanding of indoor environments.
3. This understanding is represented as a structured semantic graph.
4. The graph supports semantic search, intent navigation, and map freshness.
5. Graph reasoning is faster and uses fewer tokens than flat search when measured on the same inputs.
6. Manual annotations are used first as reference semantic maps.
7. Automatic VLM extraction begins replacing manual annotation.
8. ScanNet validates the approach beyond custom scenes.
```

Only use point 5 as a proven claim after graph-vs-flat token and runtime results exist.
