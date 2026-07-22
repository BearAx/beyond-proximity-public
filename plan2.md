# Revised Plan — SemanticSplat

## 0. Main Direction

The project is about **computer understanding of indoor environments**.

SemanticSplat converts visual / 3D observations into a structured semantic map that helps the system answer:

```text
What is around me?
Where should I go?
What does this place mean?
What changed in the environment?
```

The system does not replace VPS / localization.
It adds a semantic understanding layer above the existing map and positioning stack.

---

## 1. Main Goal

Build and evaluate a semantic map intelligence layer for indoor environments.

Core pipeline:

```text
indoor scene / visual observations
  -> semantic understanding
  -> semantic map / graph
  -> graph-based reasoning
  -> semantic search / intent navigation / map freshness
```

---

## 2. Main Claims

### Claim 1 — Environment Understanding

```text
SemanticSplat enables a computer to understand indoor environments by representing zones, objects, landmarks, signs, POIs, facilities, and relations in a structured semantic map.
```

### Claim 2 — Semantic Map Utility

```text
The semantic map supports natural-language semantic search, intent navigation, and map freshness monitoring.
```

### Claim 3 — Efficient Reasoning

```text
Graph-based reasoning over the semantic map is more efficient than flat semantic search while preserving useful target accuracy.
```

---

## 3. Current Scope

### Core Scope

```text
semantic scene understanding
semantic map construction
hierarchical graph representation
semantic search
intent navigation
map freshness / update detection
graph vs flat search comparison
ScanNet final validation
```

### Temporary Scope

```text
manual scene loading
manual ViewJSON / semantic annotation
manual semantic graph construction
```

Manual annotation is temporary.
It is used as a controlled reference while automatic VLM-based understanding is not ready.

Correct wording:

```text
Manual annotations are used as reference semantic maps for pilot validation. The final system should replace this step with automatic VLM-based semantic extraction.
```

---

## 4. What Is Not the Main Focus Now

```text
full production automation from day one
VPS replacement
continuous AR tracking
phone-budget deployment
3D IoU as the main metric
ConceptGraphs / LangSplat superiority
full ScanNet benchmark at the beginning
```

These can be future work or secondary validation, but not the first priority.

---

# Phase 1 — Define Environment Understanding

## Goal

Define what “computer understands the environment” means in this project.

## Tasks

Create a semantic schema with:

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

Define relation types:

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

## Output

```text
semantic_schema.md
scene_entity_taxonomy.md
relation_taxonomy.md
example semantic map JSON
```

## Exit Criterion

The team has a clear target representation for indoor semantic understanding.

---

# Phase 2 — Manual Semantic Map Dataset

## Goal

Create a pilot dataset where the environment is manually represented as a semantic map.

## Tasks

```text
load/capture 5–10 indoor scenes manually
create semantic annotations manually
build scene-level semantic graphs
validate completeness and consistency
```

Scene types should include:

```text
lobby
corridor
reception
exit area
elevator / facility area
seating area
mall-like area
basement / repetitive-space area
```

## Output

```text
manual semantic maps
ViewJSON files
semantic graph/tree files
scene validation reports
```

## Exit Criterion

A fixed manually constructed semantic understanding dataset exists.

---

# Phase 3 — Semantic Search and Intent Benchmark

## Goal

Evaluate whether the semantic map supports useful indoor queries.

## Benchmark Size

Minimum:

```text
100 verified queries
```

Target:

```text
150 verified queries
```

## Query Types

```text
simple semantic search
relational search
multi-hop search
intent navigation
POI search
map freshness / update query
repetitive-space ambiguity query
```

## Query Examples

```text
Where is the nearest exit?
Where is the reception desk?
I need to charge my phone.
Find the seating area near the lobby.
Which sign is near the elevator?
What changed in this corridor?
Which elevator is next to the blue sign?
```

## Ground Truth

For now, use simple GT:

```text
expected_object
expected_region
expected_zone
expected_view
expected_poi
```

Do not make GT boxes mandatory at this stage.

## Output

```text
benchmark_queries_v2.json
benchmark_status.md
manual_gt_coverage_report.md
```

## Exit Criterion

The project has a verified benchmark for semantic search, intent navigation, and freshness queries.

---

# Phase 4 — Main Technical Experiment: Graph vs Flat Search

## Goal

Show that graph-based reasoning makes semantic understanding more efficient to use.

## Compare

```text
flat search over all semantic entries
flat embedding search
graph search
graph search + pruning / top-k
```

## Metrics

### Efficiency

```text
latency_ms
semantic_entries_scanned
objects_checked
views_checked
context_size / tokens
speedup_vs_flat
```

### Quality

```text
hit@1
hit@3
expected_object_hit
expected_region_hit
expected_zone_hit
wrong_zone_rate
wrong_room_rate
```

## Output

```text
graph_vs_flat_results.json
metrics_summary.json
speedup_table.md
wrong_zone_failure_cases.md
```

## Exit Criterion

A quantitative table proves that graph-based reasoning is faster / cheaper than flat search while keeping useful accuracy.

---

# Phase 5 — Partner-Value Experiments

## 5.1 Semantic Search

Question:

```text
Can the system find meaningful indoor places and objects through natural language?
```

Metrics:

```text
search_success_rate
hit@1
hit@3
wrong_region_rate
```

---

## 5.2 Intent Navigation

Question:

```text
Can the system convert a user goal into a semantic map target?
```

Examples:

```text
I need to exit.
I want to find reception.
I need a charging point.
Where can I sit?
```

Metrics:

```text
intent_resolution_success
correct_target_region
correct_target_object
wrong_zone_rate
```

---

## 5.3 Map Freshness

Question:

```text
Can the system detect meaningful semantic changes between two versions of a place?
```

Setup:

```text
Scene version A
Scene version B
```

Manual changes:

```text
POI added
POI removed
sign changed
facility blocked
seating moved
shop name changed
```

Metrics:

```text
changed_items_detected
missed_updates
false_update_flags
operator_review_items
```

---

## 5.4 Repetitive-Space Ambiguity

Question:

```text
Can semantic graph context reduce confusion in repetitive indoor spaces?
```

Cases:

```text
similar corridors
similar columns
similar doors
similar parking/basement areas
similar signs
```

Metrics:

```text
wrong_zone_rate
wrong_region_rate
ambiguity_resolution_success
```

## Exit Criterion

The system demonstrates value for semantic search, intent navigation, map freshness, and ambiguity reduction.

---

# Phase 6 — Transition from Manual to Automatic Understanding

## Goal

Start replacing manual annotations with automatic VLM-based semantic extraction.

## Tasks

```text
select a subset of manually annotated scenes
run automatic VLM / AI scene analysis
generate ViewJSON automatically
build automatic semantic map
compare automatic output with manual reference
```

## Metrics

```text
object_coverage
landmark_coverage
region_coverage
relation_correctness
important_object_miss_rate
wrong_label_rate
query_performance_drop_vs_manual
```

## Output

```text
automatic_vs_manual_report.md
auto_viewjson_outputs
semantic_extraction_errors.md
```

## Exit Criterion

There is a demonstrated path from manual semantic maps to automatic computer understanding.

---

# Phase 7 — External Baselines

## Goal

Show compatibility with known semantic mapping approaches.

## Baselines

```text
ConceptGraphs
LangSplat
```

## Role

These are secondary baselines, not the main success condition.

Minimum acceptable result:

```text
native smoke run
canonical output
documented limitations
```

Strong result:

```text
same scene / same query subset comparison
```

## Output

```text
conceptgraphs_status.md
langsplat_status.md
baseline_smoke_results.md
```

## Exit Criterion

The project can show external baseline execution or clearly documented blockers.

---

# Phase 8 — ScanNet Validation

## Goal

Show that the approach can move beyond custom manually captured scenes.

ScanNet is mandatory, but it is late-stage validation.

## Tasks

```text
select small ScanNet subset
ingest RGB-D / poses / labels
convert ScanNet scenes into project semantic format
run semantic map construction
run graph vs flat benchmark
compare against available ScanNet labels where possible
```

## Minimum Success

```text
1–3 ScanNet scenes
working ingestion
semantic map generated
benchmark queries run
graph vs flat metrics reported
```

## Strong Success

```text
5+ ScanNet scenes
verified queries
object/region GT comparison
baseline comparison
```

## Output

```text
scannet_ingestion_report.md
scannet_graph_vs_flat_results.md
scannet_limitations.md
```

## Exit Criterion

ScanNet validates that the project is not only a custom-scene demo.

---

# Revised Timeline

## Week 1 — Understanding Target

```text
define claims
define semantic schema
define entity taxonomy
define relation taxonomy
define benchmark format
select scenes
```

Deliverables:

```text
claims_sheet.md
semantic_schema.md
benchmark_schema.md
scene_plan.md
```

---

## Week 2 — Manual Semantic Understanding Dataset

```text
load/capture scenes
create manual annotations
build semantic graphs
validate scene consistency
```

Deliverables:

```text
5–10 semantic maps
ViewJSON files
graph/tree files
validation reports
```

---

## Week 3 — Search / Intent / Freshness Benchmark

```text
create 100–150 verified queries
label query types
add expected objects/regions/views/POIs
prepare freshness and ambiguity cases
```

Deliverables:

```text
benchmark_queries_v2.json
manual_gt_report.md
query_type_distribution.md
```

---

## Week 4 — Graph Reasoning Experiments

```text
run flat search
run flat embedding search
run graph search
run graph + pruning
compare metrics
```

Deliverables:

```text
graph_vs_flat_results.json
speedup_table.md
failure_cases.md
```

---

## Week 5 — Partner Capabilities + Automation Transition

```text
run intent navigation experiment
run map freshness pilot
run ambiguity cases
start automatic VLM semantic extraction on subset
compare auto output against manual reference
```

Deliverables:

```text
intent_navigation_results.md
freshness_pilot_results.md
ambiguity_results.md
automatic_vs_manual_report.md
```

---

## Week 6 — ScanNet + Final Report

```text
run small ScanNet validation
prepare final figures/tables
write report/paper draft
clean README
prepare demo
document limitations
```

Deliverables:

```text
scannet_validation.md
final_report.pdf
paper_draft.md
demo_video
updated README
```

---

# Final Story

The final report should tell this story:

```text
1. Indoor positioning gives coordinates, but not meaning.
2. SemanticSplat builds semantic understanding of indoor environments.
3. This understanding is represented as a structured semantic graph.
4. The graph supports semantic search, intent navigation, and map freshness.
5. Graph reasoning is faster and more targeted than flat search.
6. Manual annotations are used first as a reference target.
7. Automatic VLM extraction begins replacing manual annotation.
8. ScanNet validates the approach beyond custom scenes.
```

---

# Allowed Claims

```text
SemanticSplat builds a structured semantic representation of indoor environments.
```

```text
The semantic graph supports semantic search, intent navigation, and map freshness.
```

```text
Graph-based reasoning is more efficient than flat search over the same semantic map.
```

```text
Manual annotations are used as reference semantic maps for evaluating automatic VLM extraction.
```

```text
ScanNet is used as final validation for generalization beyond custom scenes.
```

---

# Claims Not Allowed Yet

```text
fully automatic production-ready environment understanding
VPS replacement
phone-deployable real-time system
complete ScanNet-scale superiority
3D IoU accuracy without GT boxes
full ConceptGraphs/LangSplat superiority without fair comparison
```
