# Failure Modes

Run: `langsplat_scannet_full_v1`

Missing result files are coverage gaps and are not assigned a semantic failure category.

| Category | Count |
|---|---:|
| wrong room / zone | 0 |
| wrong object | 6 |
| wrong view | 2 |
| missing object in semantic description | 0 |
| bad query parsing | 0 |
| bad traversal | 5 |
| bad bbox | 0 |
| invalid depth | 0 |
| ambiguous ground truth | 0 |
| baseline adapter issue | 0 |
| missing GT | 0 |

## Per-query failures

- `scannet_0011_00_nr3d_001`: bad traversal, wrong object
- `scannet_0011_00_nr3d_002`: bad traversal, wrong object, wrong view
- `scannet_0011_00_nr3d_003`: wrong object
- `scannet_0011_00_sr3d_plus_001`: bad traversal, wrong object
- `scannet_0011_00_sr3d_plus_002`: bad traversal, wrong object, wrong view
- `scannet_0011_00_sr3d_plus_003`: bad traversal, wrong object

## Coverage gaps

Missing results (0): none
