# Revised Project Plan — SemanticSplat

## 0. Main Goal

Build a system that helps a computer understand indoor 3D environments and use that understanding for semantic search, orientation, intent navigation, and map freshness.

Core idea:

```text
Visual observations / 3D scene
  -> semantic understanding
  -> semantic map / graph
  -> graph-based reasoning
  -> search, orientation, intent navigation, freshness
```

The project does not replace VPS.
It adds a semantic understanding layer around VPS/map context.

---

## 1. Main Claim

Primary claim:

```text
SemanticSplat enables computer understanding of indoor environments by converting visual/3D observations into a structured semantic map that can be searched and reasoned over.
```

Secondary technical claim:

```text
Graph-based reasoning over the semantic map is faster and more targeted than flat semantic search.
```

Partner value claim:

```text
The semantic layer helps indoor systems answer not only “where am I?”, but also “what is around me?”, “where should I go?”, and “what changed?”.
```

---

## 2. Correct Scope

### Core

```text
semantic scene understanding
semantic map construction
hierarchical graph representation
semantic search
intent navigation
map freshness / update detection
graph vs flat search evaluation
final ScanNet validation
```

### Temporary / Pilot Only

```text
manual scene loading
manual ViewJSON / semantic annotation
manual semantic graph construction
```

Manual annotation is temporary scaffolding.
The final direction is full automation through VLM/AI scene analysis.

### Not Core Right Now

```text
phone deployment constraints
full VPS replacement
continuous AR tracking
real-time production system
full automatic pipeline from day one
```

---

## 3. Project Stages

## Stage 1 — Manual Pilot: Build the Understanding Format

Goal:

```text
Define what “understanding the environment” means in our project.
```

Tasks:

```text
load/capture 5–10 indoor scenes manually
create semantic annotations manually
define semantic entities:
- zones
- rooms
- corridors
- signs
- exits
- POIs
- facilities
- landmarks
- objects
- regions
- relations
build semantic tree / graph
```

Output:

```text
fixed semantic map dataset
manual semantic indexes
scene graphs
validation report
```

Why this matters:

```text
Before automating understanding, we need a clear target representation.
```

---

## Stage 2 — Search and Orientation over the Semantic Map

Goal:

```text
Show that the system can use semantic understanding to orient and search.
```

Tasks:

```text
create 100–150 verified queries
label query types:
- simple search
- relational search
- multi-hop search
- intent navigation
- POI search
- freshness/update queries
- ambiguity queries
```

Examples:

```text
Where is the nearest exit?
How do I find the reception desk?
Where can I charge my phone?
Which sign is near the elevator?
What changed in this corridor?
Find the seating area near the lobby.
```

GT for now:

```text
expected object
expected region
expected zone
expected view
expected POI
```

GT boxes are optional and only needed for 3D IoU.

---

## Stage 3 — Main Experiment: Graph Search vs Flat Search

Goal:

```text
Prove that graph-based reasoning uses semantic understanding more efficiently than flat search.
```

Compare:

```text
flat search over all semantic entries
flat embedding search
graph search
graph search + pruning/top-k
```

Metrics:

```text
latency_ms
objects_checked
views_checked
semantic_entries_scanned
context_size / tokens
hit@1
hit@3
wrong_zone_rate
wrong_room_rate
```

Expected result:

```text
Graph search checks fewer candidates, uses less context, and makes fewer wrong-zone mistakes than flat search.
```

This is the main quantitative proof.

---

## Stage 4 — Partner-Focused Capabilities

Goal:

```text
Show that environment understanding is useful for real indoor systems.
```

Experiments:

### 4.1 Intent Navigation

Queries like:

```text
I need to exit.
I want to find reception.
I need a charging point.
Where should I go for the elevator?
```

Metrics:

```text
intent_resolution_success
correct_target_region
wrong_zone_rate
```

### 4.2 Map Freshness

Use two versions of the same scene:

```text
version A = old semantic map
version B = changed semantic map
```

Changes:

```text
POI added
POI removed
sign changed
facility blocked
seating moved
```

Metrics:

```text
changed_items_detected
missed_updates
false_update_flags
operator_review_items
```

### 4.3 Repetitive-Space Ambiguity

Cases:

```text
similar corridors
similar columns
similar doors
similar parking/basement areas
similar signs
```

Metric:

```text
wrong-zone / wrong-region failures
```

---

## Stage 5 — Move from Manual to Automatic Understanding

Goal:

```text
Replace manual annotation with automatic VLM-based semantic extraction.
```

Tasks:

```text
take a subset of manually annotated scenes
run automatic VLM/AI scene analysis
produce ViewJSON automatically
compare automatic semantic map against manual reference
```

Metrics:

```text
object coverage
region coverage
relation correctness
missing important landmarks
wrong semantic labels
query performance drop vs manual semantic map
```

Important framing:

```text
Manual semantic maps are the reference.
Automatic VLM output is evaluated against them.
```

This connects the current prototype to the final claim: computer understanding of the environment.

---

## Stage 6 — External Baselines

Goal:

```text
Show compatibility and comparison with known semantic mapping approaches.
```

Use:

```text
ConceptGraphs
LangSplat
```

Role:

```text
secondary baselines / external validation
```

They are not the only measure of success.

Minimum acceptable result:

```text
native smoke run
canonical output
documented limitations
```

Strong result:

```text
same scene/query subset comparison
```

---

## Stage 7 — ScanNet Validation

Goal:

```text
Check that the approach is not only a custom-scene demo.
```

ScanNet is mandatory, but late-stage.

Tasks:

```text
select small ScanNet subset
ingest RGB-D / poses / labels
convert to project semantic format
run automatic or semi-automatic semantic map construction
run benchmark queries
compare graph vs flat
report limitations
```

Minimum ScanNet success:

```text
1–3 ScanNet scenes
working ingestion
semantic map generated
queries run
graph vs flat metrics reported
```

Better ScanNet success:

```text
5+ scenes
verified queries
object/region GT comparison
baseline comparison
```

---

## 8. Revised Timeline

### Week 1 — Define Understanding Target

```text
claims sheet
semantic schema
scene/entity taxonomy
benchmark schema
manual dataset plan
```

Exit:

```text
clear definition of environment understanding
```

---

### Week 2 — Manual Semantic Maps

```text
5–10 scenes
manual semantic annotations
semantic graph/tree
scene validation
```

Exit:

```text
manual semantic understanding dataset ready
```

---

### Week 3 — Search, Orientation, and Benchmark

```text
100–150 verified queries
query types
GT labels
flat search
graph search
first graph vs flat result
```

Exit:

```text
main graph-vs-flat evidence exists
```

---

### Week 4 — Partner Capabilities

```text
intent navigation experiment
map freshness pilot
repetitive-space ambiguity cases
```

Exit:

```text
semantic understanding shown useful for partner problems
```

---

### Week 5 — Automation Transition + Baselines

```text
automatic VLM semantic extraction on subset
compare automatic output vs manual reference
ConceptGraphs smoke
LangSplat smoke
prepare ScanNet ingestion
```

Exit:

```text
manual-to-automatic path demonstrated
```

---

### Week 6 — ScanNet + Final Report

```text
ScanNet small-subset run
final graph vs flat table
automatic vs manual comparison
limitations
paper/report/demo
```

Exit:

```text
final report supports the claim:
computer understands indoor environments and uses graph reasoning for efficient semantic orientation/search
```

---

## 9. Main Metrics

### Environment Understanding

```text
object coverage
region coverage
landmark coverage
relation correctness
semantic map completeness
manual-vs-automatic agreement
```

### Search / Orientation

```text
hit@1
hit@3
expected region hit
expected object hit
intent resolution success
wrong-zone rate
wrong-room rate
```

### Efficiency

```text
latency
views checked
objects checked
semantic entries scanned
context size / tokens
speedup vs flat
```

### Freshness

```text
changed items detected
missed updates
false update flags
```

---

## 10. Correct Final Story

The paper/report should tell this story:

```text
1. Indoor positioning gives coordinates, but not meaning.
2. We build a semantic understanding layer for indoor 3D scenes.
3. This layer represents rooms, zones, objects, signs, landmarks, POIs, and relations as a graph.
4. The graph lets the system orient itself semantically and answer user intent queries.
5. Compared with flat search, graph-based reasoning is faster and more targeted.
6. Manual annotation is used first as a reference representation.
7. Automatic VLM-based understanding is introduced later and compared against the manual reference.
8. ScanNet validates that the approach can move beyond custom scenes.
```

---

## 11. Claims Allowed

```text
The system builds a structured semantic representation of indoor environments.
```

```text
The semantic graph supports search, orientation, intent navigation, and map freshness.
```

```text
Graph-based retrieval is more efficient than flat search over the same semantic map.
```

```text
Manual annotations serve as a reference for evaluating automatic VLM-based semantic understanding.
```

```text
ScanNet is used as final validation for generalization beyond custom scenes.
```

---

## 12. Claims Not Allowed Yet

```text
fully automatic production-ready environment understanding
```

```text
VPS replacement
```

```text
phone-deployable real-time system
```

```text
complete ScanNet-scale benchmark superiority
```

```text
3D IoU localization accuracy unless GT boxes are implemented
```

```text
full ConceptGraphs/LangSplat superiority unless fair comparison is completed
```
