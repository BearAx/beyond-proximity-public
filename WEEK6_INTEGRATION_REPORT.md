# Week 6 Integration Report

Status date: 2026-07-14.

Integrated branch: `codex/week6-integration`.

## Integration Result

The four Week 6 branches form a clean linear history, so no work was dropped or
manually reimplemented:

| Role | Branch tip | Integration status | Primary evidence |
|---|---|---|---|
| Person 1: public data and GT | `4cc58e8` | `DONE` | `docs/datasets/replica_scannet_plan.md`, import manifests, validation reports |
| Person 2: algorithm and evaluation | `ae9f120` | `DONE_WITH_LIMITATIONS` | `scripts/evaluate_grounding.py`, `outputs/public_datasets/*_pilot_v1/` |
| Person 3: BBQ and baselines | `a142efb` | `DONE` | `docs/baselines/bbq_comparison.md`, baseline matrix and status |
| Person 4: paper and submission package | `62cf94a` | `DONE_REPOSITORY_SIDE` | `papers/twinworld/`, claim audit, figure and submission checklists |

`week6-person2` contains Person 1, `week6-person3` contains Persons 1-2, and
`week6-person4` contains Persons 1-3. The integration branch starts from the
Person 4 tip and therefore contains every commit from all four branches.

## Completed Evidence

- Eight official BBQ-aligned Replica scenes: 575 GT boxes and 56 queries.
- Eight official BBQ-aligned ScanNet scenes: 392 GT instances, 39 selected
  RGB-D views, 48 Nr3D/Sr3D+ queries, and complete object/bbox mappings.
- Eight grounding variants on each public track: graph, graph+fallback, flat
  lexical, flat embedding, and four ablations.
- BBQ-aligned Recall@1 and Acc@0.1/0.25/0.5, plus checked nodes/views/objects,
  context, estimated tokens, runtime, construction cost, and failure labels.
- Living BBQ comparison with direct/partial/invalid comparison rules.
- Anonymous TwinWorld ECCV 2026 paper source, eleven-page PDF, ten figures,
  number gate, claim audit, reproducibility notes, and submission checklist.

## Verification Performed

| Check | Result |
|---|---|
| Full Python test suite | `144 passed` |
| Tracked JSON parse audit | `2538/2538` parsed |
| TwinWorld number gate | `33/33` matched frozen JSON |
| Replica all-variant clean rerun | All deterministic quality/efficiency fields matched frozen output |
| ScanNet all-variant clean rerun | All deterministic quality/efficiency fields matched frozen output |
| Paper compilation | Passed with Tectonic 0.16.9; 11-page anonymous PDF |
| PDF visual inspection | No clipping, overlap, missing figures, or unreadable tables found |
| ECCV template provenance | Three core files exactly match official ECCV 2026 kit commit `da8c09c` |

Runtime is expected to vary across reruns and was therefore not used as a
bit-for-bit reproducibility field. The measured quality, traversal, object-count,
context, and token-estimate fields matched.

## Honest Limitations

1. Internal graph pruning reduces views by 75.5% and estimated input tokens by
   68.2%, but stub-lexical hit@1 is 0.680 versus 0.768 for flat search.
2. ScanNet graph and flat lexical Acc@0.25 are both 0.2708. The no-relation
   ablation reaches 0.2917, so current relation reranking is not an improvement.
3. Replica Acc@k of 1.0 is an oracle-map ceiling sanity check, not independent
   semantic-perception accuracy.
4. Public tracks use official GT semantic objects as map candidates. They do not
   evaluate learned RGB-D segmentation, so mAcc/mIoU/fmIoU remain `N/A`.
5. Tokens are deterministic input estimates in stub mode. There are no provider
   calls, provider tokens, provider latency, or provider cost.
6. BBQ official code has not been run under the same protocol. ConceptGraphs is
   a captured-scene run with limitations; LangSplat remains an official smoke.
   No external-baseline superiority claim is supported.
7. Raw Replica/ScanNet data and per-query licensed working files stay local and
   ignored. Public code, manifests, aggregate evidence, and reproduction
   commands are tracked.

These limitations do not mean a Person 1-4 branch task is missing. They define
the next research work needed to strengthen the result beyond the current
workshop-ready prototype.

## External Actions Before Submission

- Replace `ID=XXXXX` after OpenReview assigns the paper ID.
- Verify every author's OpenReview profile and conflicts.
- Perform a final human authorship, citation, anonymity, and license review.
- Upload the anonymous PDF by 2026-07-31.
- If accepted, prepare affiliations, camera-ready author metadata, registration,
  and an in-person presentation.

Official references checked during integration:

- TwinWorld: <https://twin-world.github.io/>
- ECCV 2026 policies and author kit:
  <https://eccv.ecva.net/Conferences/2026/SubmissionPolicies>
- Official ECCV 2026 template repository:
  <https://github.com/paolo-favaro/paper-template>
