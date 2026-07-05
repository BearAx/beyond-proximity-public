# Failure Modes

Run: `benchmark_v2_stub_manual_bbox_gt_v4`

Missing result files are coverage gaps and are not assigned a semantic failure category.

| Category | Count |
|---|---:|
| wrong room / zone | 12 |
| wrong object | 40 |
| wrong view | 36 |
| missing object in semantic description | 0 |
| bad query parsing | 0 |
| bad traversal | 5 |
| bad bbox | 79 |
| invalid depth | 0 |
| ambiguous ground truth | 0 |
| baseline adapter issue | 0 |
| missing GT | 0 |

## Per-query failures

- `qv2_001`: bad bbox
- `qv2_002`: bad bbox, wrong object, wrong view
- `qv2_003`: bad bbox
- `qv2_004`: bad bbox
- `qv2_005`: bad bbox
- `qv2_006`: bad bbox
- `qv2_007`: bad bbox, wrong object, wrong view
- `qv2_008`: bad bbox
- `qv2_009`: bad bbox, wrong object, wrong view
- `qv2_010`: bad bbox
- `qv2_011`: bad bbox, wrong object, wrong view
- `qv2_012`: bad bbox, wrong object, wrong view
- `qv2_013`: bad bbox, wrong object
- `qv2_014`: bad bbox, wrong room / zone, wrong view
- `qv2_015`: bad bbox, wrong object
- `qv2_016`: bad bbox, wrong object, wrong view
- `qv2_017`: bad bbox
- `qv2_018`: bad bbox, wrong room / zone, wrong view
- `qv2_021`: bad bbox, bad traversal, wrong view
- `qv2_022`: bad bbox, bad traversal, wrong view
- `qv2_023`: bad bbox, wrong object, wrong view
- `qv2_024`: bad bbox
- `qv2_025`: bad bbox, wrong object, wrong view
- `qv2_033`: bad bbox
- `qv2_034`: bad bbox
- `qv2_035`: bad bbox
- `qv2_038`: bad bbox
- `qv2_039`: bad bbox
- `qv2_040`: bad bbox
- `qv2_042`: bad bbox, wrong object
- `qv2_044`: bad bbox, wrong object
- `qv2_045`: bad bbox
- `qv2_048`: bad bbox, wrong object, wrong view
- `qv2_050`: bad bbox
- `qv2_051`: bad bbox, wrong object
- `qv2_052`: bad bbox, bad traversal, wrong view
- `qv2_053`: bad bbox, wrong object
- `qv2_054`: bad bbox, wrong object
- `qv2_055`: bad bbox, wrong object, wrong room / zone, wrong view
- `qv2_060`: wrong object
- `qv2_064`: bad bbox, wrong object, wrong view
- `qv2_067`: bad bbox, wrong object, wrong view
- `qv2_069`: bad bbox
- `qv2_070`: bad bbox
- `qv2_081`: bad bbox, wrong object, wrong room / zone, wrong view
- `qv2_082`: bad bbox, bad traversal, wrong view
- `qv2_083`: bad bbox
- `qv2_084`: bad bbox, wrong object, wrong room / zone, wrong view
- `qv2_085`: bad bbox, wrong object, wrong view
- `qv2_091`: bad bbox, wrong object, wrong view
- `qv2_092`: bad bbox, wrong object, wrong room / zone, wrong view
- `qv2_097`: bad bbox
- `qv2_099`: bad bbox, wrong room / zone, wrong view
- `qv2_102`: bad bbox, wrong object
- `qv2_103`: bad bbox
- `qv2_105`: bad bbox, wrong object, wrong room / zone, wrong view
- `qv2_107`: bad bbox, wrong object, wrong room / zone, wrong view
- `qv2_108`: bad bbox, wrong object
- `qv2_111`: bad bbox, bad traversal, wrong view
- `qv2_112`: bad bbox, wrong object, wrong view
- `qv2_113`: bad bbox, wrong object, wrong room / zone, wrong view
- `qv2_114`: bad bbox, wrong object, wrong view
- `qv2_115`: bad bbox, wrong object, wrong room / zone, wrong view
- `qv2_118`: wrong object
- `qv2_120`: wrong object
- `qv2_122`: bad bbox
- `qv2_123`: bad bbox
- `qv2_124`: bad bbox
- `qv2_127`: bad bbox
- `qv2_128`: bad bbox
- `qv2_129`: bad bbox
- `qv2_130`: bad bbox, wrong view
- `qv2_131`: bad bbox
- `qv2_133`: bad bbox
- `qv2_135`: bad bbox, wrong object, wrong view
- `qv2_136`: bad bbox
- `qv2_137`: bad bbox, wrong object, wrong view
- `qv2_141`: bad bbox, wrong object
- `qv2_142`: bad bbox
- `qv2_143`: bad bbox
- `qv2_144`: bad bbox, wrong object, wrong room / zone, wrong view
- `qv2_145`: bad bbox, wrong object, wrong view

## Coverage gaps

Missing results (0): none
