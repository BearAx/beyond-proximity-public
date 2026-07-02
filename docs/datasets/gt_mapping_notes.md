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

No Replica scene or official annotations are available locally. Consequently:

- view-to-room GT is unknown;
- query-to-instance GT is unknown;
- GT 3D boxes are unknown;
- room and instance mappings must remain empty until licensed data and annotations are supplied;
- no default-scene label may be copied and presented as Replica GT.

## Benchmark Consequence

`docs/benchmarks/benchmark_queries_v1.json` is a semantic-index regression benchmark. Expected IDs are valid for testing traversal/output behavior, but its metrics are not independent visual recognition or Replica-GT accuracy.
