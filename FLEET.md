# Recommended vLLM Fleet

## Full catalog

| Model | VRAM needed | Recommended GPU | Price/hr | Role |
|---|---|---|---|---|
| **Qwen2.5-Coder-32B-AWQ** | 20GB | RTX 5090 (32GB) | $0.29 | Chat / design / review — max context, full quality |
| **Qwen3-32B-AWQ** (thinking) | 20GB | RTX 5090 (32GB) | $0.29 | Hard reasoning, algorithms, architecture decisions |
| **DeepSeek-R1-32B-AWQ** | 20GB | RTX 4090 (24GB) | $0.20 | Reasoning alt — cheaper than 5090, still fits |
| **Codestral-22B** | 14GB | RTX 4090 (24GB) | $0.20 | Best FIM/completion quality |
| **Qwen2.5-Coder-14B** | 9GB | RTX 3090 (24GB) | $0.12 | Fast mid-tier — cheaper per task than 32B |
| **Qwen2.5-Coder-7B** | 5GB | RTX 4070 Ti (12GB) | $0.12 | Ultra-fast completion, always-on cheaply |
| **Qwen2.5-Coder-3B** | 3GB | RTX 3060 (12GB) | $0.08 | Cheapest possible completion |
| **Llama-4-Scout-17B-Q4** | 12GB | RTX 4070 Ti (12GB) | $0.12 | 10M token context — whole-codebase analysis |

## Recommended starter fleet

| Name | Model | GPU | Price/hr | Notes |
|---|---|---|---|---|
| `oc1` | Qwen2.5-Coder-32B-AWQ | RTX 5090 | $0.29 | Already deployed |
| `qwen-2-5-coder-3b` | Qwen2.5-Coder-3B | RTX 3060 | $0.08 | Currently on 5090 — overkill, reassign |
| `codestral-22b` | Codestral-22B | RTX 4090 | $0.20 | Best completion quality |
| `qwen3-32b` | Qwen3-32B-AWQ | RTX 5090 | $0.29 | Thinking/reasoning mode for hard problems |

**Total when all running: ~$0.86/hr. In practice you run what you need.**

## Notes

- All models use `--enable-prefix-caching` and AWQ/Q4 quantization where applicable.
- 3B is massively overspecced on a 5090 — reassign to RTX 3060 to save $0.21/hr.
- Codestral is purpose-built for FIM (fill-in-the-middle) and outperforms general models at inline completion.
- Qwen3-32B thinking mode is a distinct use case from the Qwen2.5-Coder-32B — use it for problems that need step-by-step reasoning, not routine coding.
- Llama-4-Scout is the only viable option for whole-codebase analysis (10M token context).
