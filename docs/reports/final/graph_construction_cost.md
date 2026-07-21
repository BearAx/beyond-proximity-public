# Graph Construction Cost

This audit rebuilds the five captured-scene semantic graphs from their saved manual ViewJSON records.

## Result

- Provider model calls: **0**
- Provider construction tokens: **0** input + output tokens
- Views: **97**
- Semantic items: **1066**
- Constructed nodes: **1064**
- Manual annotation records: **97**
- Manual semantic items: **1066**
- Manual annotation characters: **267,877** canonical serialized characters
- Source ViewJSON size: **66,937** estimated tokens (characters/4 proxy)
- Constructed tree size: **179,817** estimated tokens (characters/4 proxy)
- Total serialized build I/O: **246,754** estimated tokens (input + output)
- Sum of per-scene median local build times: **1.822177 s**

Provider tokens and serialized token-equivalents are different quantities. Provider usage is an instrumented zero because the graph builder is local and deterministic. Manual annotation workload is metered from the frozen artifacts as record count, semantic-item count, canonical characters, and token-equivalent payload. Historical annotator wall-clock time was not logged, so no person-hour value is inferred.

## Per Scene

| Scene | Views | Items | Nodes | Source est. tokens | Tree est. tokens | Median build (s) | Node IDs match |
|---|---:|---:|---:|---:|---:|---:|:---:|
| ConferenceHall-capture-pilot | 20 | 207 | 206 | 13,310 | 34,364 | 0.355323 | yes |
| Museume-capture | 20 | 225 | 228 | 14,393 | 38,695 | 0.391105 | yes |
| Theater-capture | 20 | 226 | 226 | 13,704 | 36,024 | 0.390635 | yes |
| outdoor-street-capture | 21 | 239 | 240 | 14,416 | 40,573 | 0.405550 | yes |
| outdoor-drone-capture | 16 | 169 | 164 | 11,114 | 30,161 | 0.279564 | yes |

## Reproduce

```powershell
python -B scripts\measure_graph_construction.py --repeats 7
```

Definition: For each canonical compact JSON record, floor(serialized characters / 4), then sum. This is a local representation-size proxy, not provider billing usage.
