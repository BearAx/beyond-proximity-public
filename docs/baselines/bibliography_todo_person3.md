# Bibliography Status: Person 3

Status date: 2026-07-03  
Checked files:

- `papers/beyond-proximity/refs.bib`
- `docs/baselines/refs_person3_desired.bib`

The desired-key bibliography has been verified and collected in `docs/baselines/refs_person3_desired.bib`. That file is a draft/reference bibliography for Person 3 and is not currently used by the article build.

## Main Article Bibliography Status

The article bibliography at `papers/beyond-proximity/refs.bib` still uses a small seed set and different key names for some papers. Do not switch LaTeX citations to the desired keys unless the desired entries are copied into the article bibliography or the build is updated to include `docs/baselines/refs_person3_desired.bib`.

| Desired key | Current key in `papers/beyond-proximity/refs.bib` | Status |
|---|---|---|
| `lerf2023` | `kerr2023lerf` | Verified in desired-key draft; main refs uses old key. |
| `langsplat2024` | Missing | Verified in desired-key draft; add to main refs before citing. |
| `scanrefer2020` | Missing | Verified in desired-key draft; add to main refs before citing. |
| `hovsg2024` | Missing | Verified in desired-key draft; add to main refs before citing. |
| `openlex3d2025` | Missing | Verified in desired-key draft; add to main refs before citing. |
| `conceptgraphs2023` | `gu2023conceptgraphs` | Verified in desired-key draft; main refs uses old key. |
| `semanticgaussians2024` | Missing | Verified in desired-key draft; add to main refs before citing. |
| `legs2024` | Missing | Verified in desired-key draft; add to main refs before citing. |
| `openmask3d2023` | Missing | Verified in desired-key draft; add to main refs before citing. |
| `conceptfusion2023` | Missing | Verified in desired-key draft; add to main refs before citing. |
| `openscene2023` | Missing | Verified in desired-key draft; add to main refs before citing. |
| `hydra2022` | Missing | Verified in desired-key draft; add to main refs before citing. |
| `bbq2024` | Missing | Verified in desired-key draft; add to main refs before citing. |
| `attentionrag2025` | Missing | Verified in desired-key draft; add to main refs before citing. |
| `provence2025` | Missing | Verified in desired-key draft; add to main refs before citing. |
| `promptcompression2024` | Missing | Verified in desired-key draft; add to main refs before citing. |
| `tearag2026` | Missing | Verified in desired-key draft; add to main refs before citing. Key is `tearag2026`, but verified BibTeX year is 2025. |
| `spathrag2026` | Missing | Verified in desired-key draft; add to main refs before citing. |

## Local Paper Files

| Desired key | Local file status |
|---|---|
| `lerf2023` | `papers/new-papers/3d-scene-understanding/LERF.pdf` |
| `langsplat2024` | `papers/new-papers/3d-scene-understanding/LangSplat.pdf` |
| `scanrefer2020` | `papers/new-papers/3d-scene-understanding/ScanRefer.pdf` |
| `hovsg2024` | `papers/new-papers/3d-scene-understanding/HOV-SG.pdf` |
| `openlex3d2025` | `papers/new-papers/3d-scene-understanding/OpenLex3D.pdf` |
| `conceptgraphs2023` | `papers/new-papers/3d-scene-understanding/ConceptGraphs.pdf` |
| `semanticgaussians2024` | `papers/Semantic Gaussians.pdf` |
| `legs2024` | `papers/LEGS.pdf` |
| `openmask3d2023` | `papers/new-papers/3d-scene-understanding/OpenMask3D.pdf` |
| `conceptfusion2023` | `papers/new-papers/3d-scene-understanding/ConceptFusion.pdf` |
| `openscene2023` | `papers/new-papers/3d-scene-understanding/OpenScene.pdf` |
| `hydra2022` | `papers/new-papers/3d-scene-understanding/Hydra.pdf` |
| `bbq2024` | `papers/new-papers/3d-scene-understanding/BBQ.pdf` |
| `attentionrag2025` | `papers/new-papers/context-efficiency/AttentionRAG.pdf` |
| `provence2025` | `papers/new-papers/context-efficiency/Provence.pdf` |
| `promptcompression2024` | `papers/new-papers/context-efficiency/PromptCompressionSurvey.pdf` |
| `tearag2026` | `papers/new-papers/context-efficiency/TeaRAG.pdf` |
| `spathrag2026` | `papers/new-papers/context-efficiency/S-Path-RAG.pdf` |

## Remaining Action

If Person 4 wants to use the desired citation keys in LaTeX, copy the needed entries from `docs/baselines/refs_person3_desired.bib` into `papers/beyond-proximity/refs.bib` and update the corresponding `\cite{...}` keys. Until then, the desired-key file should be treated as a verified bibliography draft.
