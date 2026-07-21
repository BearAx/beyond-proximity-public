# Failure Modes

Run: `conceptgraphs_scannet_full_v1`

Missing result files are coverage gaps and are not assigned a semantic failure category.

| Category | Count |
|---|---:|
| wrong room / zone | 0 |
| wrong object | 48 |
| wrong view | 21 |
| missing object in semantic description | 0 |
| bad query parsing | 0 |
| bad traversal | 0 |
| bad bbox | 48 |
| invalid depth | 0 |
| ambiguous ground truth | 0 |
| baseline adapter issue | 0 |
| missing GT | 0 |

## Per-query failures

- `scannet_0011_00_nr3d_001`: bad bbox, wrong object, wrong view
- `scannet_0011_00_nr3d_002`: bad bbox, wrong object, wrong view
- `scannet_0011_00_nr3d_003`: bad bbox, wrong object
- `scannet_0011_00_sr3d_plus_001`: bad bbox, wrong object
- `scannet_0011_00_sr3d_plus_002`: bad bbox, wrong object, wrong view
- `scannet_0011_00_sr3d_plus_003`: bad bbox, wrong object
- `scannet_0030_00_nr3d_001`: bad bbox, wrong object
- `scannet_0030_00_nr3d_002`: bad bbox, wrong object, wrong view
- `scannet_0030_00_nr3d_003`: bad bbox, wrong object, wrong view
- `scannet_0030_00_sr3d_plus_001`: bad bbox, wrong object, wrong view
- `scannet_0030_00_sr3d_plus_002`: bad bbox, wrong object, wrong view
- `scannet_0030_00_sr3d_plus_003`: bad bbox, wrong object, wrong view
- `scannet_0046_00_nr3d_001`: bad bbox, wrong object
- `scannet_0046_00_nr3d_002`: bad bbox, wrong object
- `scannet_0046_00_nr3d_003`: bad bbox, wrong object, wrong view
- `scannet_0046_00_sr3d_plus_001`: bad bbox, wrong object
- `scannet_0046_00_sr3d_plus_002`: bad bbox, wrong object
- `scannet_0046_00_sr3d_plus_003`: bad bbox, wrong object
- `scannet_0086_00_nr3d_001`: bad bbox, wrong object
- `scannet_0086_00_nr3d_002`: bad bbox, wrong object
- `scannet_0086_00_nr3d_003`: bad bbox, wrong object
- `scannet_0086_00_sr3d_plus_001`: bad bbox, wrong object
- `scannet_0086_00_sr3d_plus_002`: bad bbox, wrong object
- `scannet_0086_00_sr3d_plus_003`: bad bbox, wrong object
- `scannet_0222_00_nr3d_001`: bad bbox, wrong object
- `scannet_0222_00_nr3d_002`: bad bbox, wrong object, wrong view
- `scannet_0222_00_nr3d_003`: bad bbox, wrong object
- `scannet_0222_00_sr3d_plus_001`: bad bbox, wrong object, wrong view
- `scannet_0222_00_sr3d_plus_002`: bad bbox, wrong object
- `scannet_0222_00_sr3d_plus_003`: bad bbox, wrong object, wrong view
- `scannet_0378_00_nr3d_001`: bad bbox, wrong object, wrong view
- `scannet_0378_00_nr3d_002`: bad bbox, wrong object
- `scannet_0378_00_nr3d_003`: bad bbox, wrong object, wrong view
- `scannet_0378_00_sr3d_plus_001`: bad bbox, wrong object, wrong view
- `scannet_0378_00_sr3d_plus_002`: bad bbox, wrong object
- `scannet_0378_00_sr3d_plus_003`: bad bbox, wrong object, wrong view
- `scannet_0389_00_nr3d_001`: bad bbox, wrong object
- `scannet_0389_00_nr3d_002`: bad bbox, wrong object
- `scannet_0389_00_nr3d_003`: bad bbox, wrong object, wrong view
- `scannet_0389_00_sr3d_plus_001`: bad bbox, wrong object
- `scannet_0389_00_sr3d_plus_002`: bad bbox, wrong object
- `scannet_0389_00_sr3d_plus_003`: bad bbox, wrong object
- `scannet_0435_00_nr3d_001`: bad bbox, wrong object
- `scannet_0435_00_nr3d_002`: bad bbox, wrong object, wrong view
- `scannet_0435_00_nr3d_003`: bad bbox, wrong object, wrong view
- `scannet_0435_00_sr3d_plus_001`: bad bbox, wrong object, wrong view
- `scannet_0435_00_sr3d_plus_002`: bad bbox, wrong object
- `scannet_0435_00_sr3d_plus_003`: bad bbox, wrong object, wrong view

## Coverage gaps

Missing results (0): none
