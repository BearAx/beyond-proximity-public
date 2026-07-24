# Relation reasoning audit

- Relation-bearing queries inspected: 40
- Parsed relation: 35
- Unparsed relation: 5
- Hit@1 with / without relation: 0.675 / 0.55
- Beneficial / harmful / neutral: 5 / 0 / 35
- Validated relation-driven top-1 changes: 5

| Relation | Queries | Hit@1 with | Hit@1 without | Beneficial | Harmful | Validated changes |
|---|---:|---:|---:|---:|---:|---:|
| above | 3 | 0.666667 | 0.666667 | 0 | 0 | 0 |
| between | 8 | 0.75 | 0.625 | 1 | 0 | 1 |
| closest | 12 | 0.75 | 0.666667 | 1 | 0 | 1 |
| farthest | 8 | 0.75 | 0.375 | 3 | 0 | 3 |
| front | 2 | 0.5 | 0.5 | 0 | 0 | 0 |
| near | 1 | 1.0 | 1.0 | 0 | 0 | 0 |
| right | 1 | 1.0 | 1.0 | 0 | 0 | 0 |
| unparsed | 5 | 0.2 | 0.2 | 0 | 0 | 0 |

Relations are allowed to affect ranking only after anchor-confidence, bbox-validity, relation-confidence, and lexical score-margin gates.
