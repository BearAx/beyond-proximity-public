# Experiment Modes

- `stub/`: deterministic local pipeline checks. Stub results are not live-model results.
- `live/`: provider-backed runs. Currently blocked when provider credentials are absent.
- `cached_live/`: replay of verified live responses without provider calls. It requires a real live cache first.
- `semantic_retrieval/`: headless retrieval instructions and implementation notes.

Run artifacts are written under `outputs/`; only small representative evidence should be committed deliberately.
