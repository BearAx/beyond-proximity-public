# Relation reasoning audit

- Relation-bearing queries inspected: 16
- Parsed relation: 8
- Unparsed relation: 8
- Hit@1 with / without relation: 1.0 / 1.0
- Beneficial / harmful / neutral: 0 / 0 / 16
- Validated relation-driven top-1 changes: 0

| Relation | Queries | Hit@1 with | Hit@1 without | Beneficial | Harmful | Validated changes |
|---|---:|---:|---:|---:|---:|---:|
| near | 8 | 1.0 | 1.0 | 0 | 0 | 0 |
| unparsed | 8 | 1.0 | 1.0 | 0 | 0 | 0 |

Relations are allowed to affect ranking only after anchor-confidence, bbox-validity, relation-confidence, and lexical score-margin gates.
