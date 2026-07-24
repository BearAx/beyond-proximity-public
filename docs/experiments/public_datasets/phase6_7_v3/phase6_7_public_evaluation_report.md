# Phases 6 and 7: Public-Data Evaluation and Relation Audit

Status: complete for the available official Replica and ScanNet oracle-map
protocols. Native predicted-map baselines remain protocol-separated.

## Evaluation Tracks

| Track | Scenes | Queries | Positive quality denominator | Verified negatives | Map type |
|---|---:|---:|---:|---:|---|
| Replica | 8 | 56 | 48 | 8 | official GT object map |
| ScanNet original | 8 | 48 | 48 | 0 | official GT object map |
| ScanNet extended | 8 | 64 | 56 | 8 | official GT object map |

The ScanNet original track preserves the 48 Nr3D/Sr3D+ queries. The extended
track adds one GT-backed functional query and one verified-absence query per
scene. Its eight functional queries include `Find a place to sit`, workstation
seating, sleeping, and hand-washing requests. All functional answers are
declared official ScanNet object IDs and boxes. Every negative label was checked
against all imported official instance labels in its scene.

These are retrieval tests over oracle semantic maps. They do not measure
automatic semantic-map construction or segmentation accuracy.

## Main Results

| Track / method | R@1 | R@3 | R@5 | MRR | Acc@0.25 | Neg. acc. | Objects/query | Est. tokens/query |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Replica graph | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 12.11 | 303 |
| Replica graph + fallback | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 51.82 | 1,275 |
| Replica flat lexical | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 71.88 | 1,765 |
| ScanNet graph | 0.604 | 0.812 | 0.854 | 0.718 | 0.604 | N/A | 4.73 | 219 |
| ScanNet graph + fallback | 0.625 | 0.833 | 0.875 | 0.743 | 0.604 | N/A | 36.75 | 1,589 |
| ScanNet flat lexical | 0.625 | 0.833 | 0.875 | 0.743 | 0.604 | N/A | 49.00 | 2,117 |
| ScanNet extended graph | 0.607 | 0.786 | 0.821 | 0.705 | 0.589 | 1.000 | 4.38 | 200 |
| ScanNet extended graph + fallback | 0.625 | 0.821 | 0.857 | 0.732 | 0.589 | 1.000 | 39.81 | 1,720 |
| ScanNet extended flat lexical | 0.625 | 0.821 | 0.857 | 0.732 | 0.589 | 1.000 | 49.00 | 2,115 |

On original ScanNet, calibrated fallback preserves flat lexical R@1, R@3, R@5,
MRR, and Acc@0.25 exactly while checking 25.0% fewer objects and using 24.9%
fewer estimated tokens. Aggressive graph pruning checks 90.3% fewer objects
and uses 89.6% fewer estimated tokens, with a 2.1 percentage-point loss at
R@1, R@3, and R@5.

On Replica, graph + fallback preserves the flat ceiling while checking 27.9%
fewer objects and using 27.8% fewer estimated tokens. Because the Replica
queries are lexically easy under the oracle map, this is a protocol sanity
ceiling rather than a discriminative quality result.

On extended ScanNet, graph + fallback again matches flat lexical quality while
reducing objects by 18.8% and estimated tokens by 18.7%. Aggressive graph
pruning reduces objects by 91.1% and tokens by 90.5%, with R@1 lower by 1.8
points and R@3/R@5 lower by 3.6 points.

## Hard-Query Breakdown

For the extended ScanNet graph + fallback run:

| Query type | Queries | R@1 | R@3 | R@5 | MRR / negative acc. |
|---|---:|---:|---:|---:|---:|
| Functional | 8 | 0.625 | 0.750 | 0.750 | MRR 0.667 |
| Relational | 40 | 0.675 | 0.850 | 0.900 | MRR 0.774 |
| Attribute | 2 | 0.000 | 0.500 | 0.500 | MRR 0.313 |
| Verified negative | 8 | N/A | N/A | N/A | accuracy 1.000 |

The remaining weakness is attribute disambiguation, not basic negative
detection. Functional requests such as finding a place to sit now execute and
are scored against declared GT IDs; they are not merely demo queries.

## Controlled Relation Audit

The relation ablation compares `graph_fallback` with the identical pipeline
under `no_relation=true`. All other inputs and policy values are unchanged.

### ScanNet

- 40 relation-labelled queries inspected one by one.
- 35 parsed into a supported target-anchor predicate; 5 are descriptive,
  contrastive, containment, or viewpoint-only phrases without a valid
  target-anchor relation.
- Hit@1 is 0.675 with relation reasoning and 0.550 without it.
- Five top-1 changes are beneficial, zero are harmful, and every changed top-1
  winner passed the relation-confidence gate.
- Validated gains comprise one `between`, one `closest`, and three `farthest`
  queries.

The five intentionally unparsed forms are retained in the audit with their
query text: cardinality description, middle-shelf containment, handle-side
attribute, color contrast/negation, and viewpoint-only left without a camera
frame. They are not silently scored as spatial successes.

### Replica

All eight parsed `near` queries and all eight multi-hop queries remain correct
with or without relation reranking. Relation reasoning changes no top-1 result.
The multi-hop prompts are sequential instructions rather than target-anchor
spatial predicates and are recorded as unparsed.

## Relation Safety Policy

Relation evidence may affect ranking only after:

1. anchor score and anchor-margin validation;
2. valid 2D/3D geometry;
3. relation confidence at least `0.65`;
4. lexical score within `0.15` of the best lexical candidate;
5. a deterministic fallback when the relation or geometry is unresolved.

Low-confidence relation evidence no longer breaks lexical ties. ScanNet and
Replica world-coordinate boxes are not used for viewpoint-relative
left/right/front/behind predicates when the required camera frame is absent.

## Baseline Boundary

ConceptGraphs and LangSplat are not placed in this table. Their saved native
runs use predicted maps, different frame sampling, different output geometry,
and different resource settings. Comparing their native numbers directly with
SemanticSplat's oracle-map runs would not be a fair method ranking.

## Evidence

This directory contains:

- three `*_variant_comparison.json` and CSV files;
- graph, graph-fallback, flat-lexical, and no-relation summaries with explicit
  metric denominators;
- complete ScanNet and Replica relation audits in JSON, CSV, and Markdown.

Reproduce the primary runs with:

```powershell
python -B scripts/run_grounding_variants.py `
  --config configs/scannet_benchmark.yaml `
  --out outputs/public_datasets/phase6_scannet_calibrated_v3

python -B scripts/run_grounding_variants.py `
  --config configs/scannet_extended_benchmark.yaml `
  --out outputs/public_datasets/phase6_scannet_extended_v3

python -B scripts/run_grounding_variants.py `
  --config configs/replica_benchmark.yaml `
  --out outputs/public_datasets/phase6_replica_calibrated_v3
```
