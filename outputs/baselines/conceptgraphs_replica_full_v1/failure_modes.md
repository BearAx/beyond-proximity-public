# Failure Modes

Run: `conceptgraphs_replica_full_v1`

Missing result files are coverage gaps and are not assigned a semantic failure category.

| Category | Count |
|---|---:|
| wrong room / zone | 0 |
| wrong object | 56 |
| wrong view | 48 |
| missing object in semantic description | 0 |
| bad query parsing | 0 |
| bad traversal | 0 |
| bad bbox | 46 |
| invalid depth | 0 |
| ambiguous ground truth | 0 |
| baseline adapter issue | 0 |
| missing GT | 0 |

## Per-query failures

- `replica_room0_simple_001`: bad bbox, wrong object, wrong view
- `replica_room0_simple_002`: bad bbox, wrong object, wrong view
- `replica_room0_attribute_001`: bad bbox, wrong object, wrong view
- `replica_room0_relational_001`: bad bbox, wrong object, wrong view
- `replica_room0_multi_hop_001`: bad bbox, wrong object, wrong view
- `replica_room0_functional_001`: bad bbox, wrong object, wrong view
- `replica_room0_negative_001`: wrong object
- `replica_room1_simple_001`: bad bbox, wrong object, wrong view
- `replica_room1_simple_002`: bad bbox, wrong object, wrong view
- `replica_room1_attribute_001`: bad bbox, wrong object, wrong view
- `replica_room1_relational_001`: bad bbox, wrong object, wrong view
- `replica_room1_multi_hop_001`: bad bbox, wrong object, wrong view
- `replica_room1_functional_001`: bad bbox, wrong object, wrong view
- `replica_room1_negative_001`: wrong object
- `replica_room2_simple_001`: bad bbox, wrong object, wrong view
- `replica_room2_simple_002`: bad bbox, wrong object, wrong view
- `replica_room2_attribute_001`: bad bbox, wrong object, wrong view
- `replica_room2_relational_001`: bad bbox, wrong object, wrong view
- `replica_room2_multi_hop_001`: bad bbox, wrong object, wrong view
- `replica_room2_functional_001`: bad bbox, wrong object, wrong view
- `replica_room2_negative_001`: wrong object
- `replica_office0_simple_001`: bad bbox, wrong object, wrong view
- `replica_office0_simple_002`: bad bbox, wrong object, wrong view
- `replica_office0_attribute_001`: bad bbox, wrong object, wrong view
- `replica_office0_relational_001`: bad bbox, wrong object, wrong view
- `replica_office0_multi_hop_001`: bad bbox, wrong object, wrong view
- `replica_office0_functional_001`: bad bbox, wrong object, wrong view
- `replica_office0_negative_001`: wrong object
- `replica_office1_simple_001`: bad bbox, wrong object, wrong view
- `replica_office1_simple_002`: wrong object, wrong view
- `replica_office1_attribute_001`: bad bbox, wrong object, wrong view
- `replica_office1_relational_001`: bad bbox, wrong object, wrong view
- `replica_office1_multi_hop_001`: bad bbox, wrong object, wrong view
- `replica_office1_functional_001`: wrong object, wrong view
- `replica_office1_negative_001`: wrong object
- `replica_office2_simple_001`: bad bbox, wrong object, wrong view
- `replica_office2_simple_002`: bad bbox, wrong object, wrong view
- `replica_office2_attribute_001`: bad bbox, wrong object, wrong view
- `replica_office2_relational_001`: bad bbox, wrong object, wrong view
- `replica_office2_multi_hop_001`: bad bbox, wrong object, wrong view
- `replica_office2_functional_001`: bad bbox, wrong object, wrong view
- `replica_office2_negative_001`: wrong object
- `replica_office3_simple_001`: bad bbox, wrong object, wrong view
- `replica_office3_simple_002`: bad bbox, wrong object, wrong view
- `replica_office3_attribute_001`: bad bbox, wrong object, wrong view
- `replica_office3_relational_001`: bad bbox, wrong object, wrong view
- `replica_office3_multi_hop_001`: bad bbox, wrong object, wrong view
- `replica_office3_functional_001`: bad bbox, wrong object, wrong view
- `replica_office3_negative_001`: wrong object
- `replica_office4_simple_001`: bad bbox, wrong object, wrong view
- `replica_office4_simple_002`: bad bbox, wrong object, wrong view
- `replica_office4_attribute_001`: bad bbox, wrong object, wrong view
- `replica_office4_relational_001`: bad bbox, wrong object, wrong view
- `replica_office4_multi_hop_001`: bad bbox, wrong object, wrong view
- `replica_office4_functional_001`: bad bbox, wrong object, wrong view
- `replica_office4_negative_001`: wrong object

## Coverage gaps

Missing results (0): none
