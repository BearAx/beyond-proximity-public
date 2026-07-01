# Failure Modes

Run: `phase1_evaluator_smoke`

Missing result files are coverage gaps and are not assigned a semantic failure category.

| Category | Count |
|---|---:|
| wrong room / zone | 0 |
| wrong object | 1 |
| wrong view | 1 |
| missing object in semantic description | 0 |
| bad query parsing | 0 |
| bad traversal | 0 |
| bad bbox | 0 |
| invalid depth | 6 |
| ambiguous ground truth | 0 |
| baseline adapter issue | 0 |
| missing GT | 0 |

## Per-query failures

- `q001`: invalid depth
- `q011`: invalid depth
- `q019`: invalid depth, wrong object, wrong view
- `q029`: invalid depth
- `q036`: invalid depth
- `q044`: invalid depth

## Coverage gaps

Missing results (44): q002, q003, q004, q005, q006, q007, q008, q009, q010, q012, q013, q014, q015, q016, q017, q018, q020, q021, q022, q023, q024, q025, q026, q027, q028, q030, q031, q032, q033, q034, q035, q037, q038, q039, q040, q041, q042, q043, q045, q046, q047, q048, q049, q050
