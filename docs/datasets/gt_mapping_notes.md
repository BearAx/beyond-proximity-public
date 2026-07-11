# Ground-Truth Mapping Notes

## Current Default Pilot

| Mapping | Availability | Interpretation |
|---|---|---|
| View to room | Predicted only | `ViewJSON.room_type` and tree membership are semantic-index outputs, not independent GT room labels. |
| Query to expected view | Available for benchmark v1 | Expectations were manually checked against saved ViewJSON records. |
| Query to expected node/zone | Available for benchmark v1 | Expectations reference the existing root-connected semantic tree, not a dataset hierarchy. |
| Query to expected instance | Label-level only | `expected_object_labels` identify semantic labels; no stable dataset instance IDs exist. |
| Query to expected region | Partial | Existing leaf/zone IDs provide semantic-index regions. |
| 2D bbox GT | Unavailable | ViewJSON bboxes are model/prompt outputs and must not be used as independent GT. |
| 3D bbox GT | Unavailable | No reliable instance boxes or masks are present. |
| Room GT | Unavailable | Existing names such as ballroom, foyer, and lounge are semantic annotations. |

## Replica Mapping

Official Replica v1 semantic metadata is now available locally for the
BBQ-aligned subset. The current importer uses
`habitat/info_semantic.json` object IDs, class labels, and `oriented_bbox`
values. This enables object-level GT and 3D box evaluation for:

- `replica_room0`
- `replica_room1`
- `replica_room2`
- `replica_office0`
- `replica_office1`
- `replica_office2`
- `replica_office3`
- `replica_office4`

Available Replica GT:

- query-to-instance/object GT for the 56 mixed-type pilot queries;
- official object labels;
- official 3D object boxes in Replica habitat mesh coordinates.

Unavailable Replica GT in the current importer:

- rendered RGB-D frame-level GT;
- room hierarchy GT;
- segmentation metrics such as mAcc, mIoU, and fmIoU.

No default-scene or manual captured-scene label may be copied and presented as
Replica GT. Replica GT must come from the official Replica metadata or a
documented conversion from official Replica assets.

## Benchmark Consequence

`docs/benchmarks/benchmark_queries_v1.json` is a semantic-index regression benchmark. Expected IDs are valid for testing traversal/output behavior, but its metrics are not independent visual recognition or Replica-GT accuracy.

`docs/benchmarks/replica_scannet_pilot_queries.json` contains the current
GT-backed Replica object-box pilot. The ScanNet part remains inactive until
official ScanNet access and query labels are available.
