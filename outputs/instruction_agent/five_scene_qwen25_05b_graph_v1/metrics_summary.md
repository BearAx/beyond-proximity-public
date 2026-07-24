# Instruction-Agent Benchmark

- Model: `Qwen/Qwen2.5-0.5B-Instruct`
- Model revision: `7ae557604adf67be50417f59c2c2f167def9a775`
- Queries: 150 total / 125 quality-eligible
- Device: `cpu`

| Method | hit@1 | hit@3 | MRR | Views | Calls | Input tokens | Output tokens | ms/query | Valid |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| graph_instruction | 0.368 | 0.696 | 0.509 | 9.63 | 2.00 | 1582.9 | 16.4 | 6238.0 | 1.000 |

Token values are exact native tokenizer counts for the rendered chat prompts and generated responses.
