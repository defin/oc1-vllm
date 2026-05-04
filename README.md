# vLLM on Salad — Qwen2.5-Coder

Two dedicated Salad containers running vLLM, one per model.

## Containers

| Container | Display Name | Model | GPU | Domain |
|---|---|---|---|---|
| `oc1` | vllm-qwen2.5-coder-32b | Qwen2.5-Coder-32B-Instruct-AWQ | RTX 5090 | `caper-sweetcorn-z3v9kf4mya1rjhm2.salad.cloud` |
| `qwen-2-5-coder-3b` | vllm-qwen2.5-coder-3b | Qwen2.5-Coder-3B-Instruct | RTX 5090 | `jambul-kale-6xz4qzdswdm2a09k.salad.cloud` |

Both containers require a `Salad-Api-Key` header on all requests.

## Images

Built via GitHub Actions → `ghcr.io/defin/oc1-vllm`

| Tag | Dockerfile | Contents |
|---|---|---|
| `:32b` | `Dockerfile` | CUDA 12.6 + vLLM + Qwen2.5-Coder-32B-AWQ |
| `:3b` | `Dockerfile.3b` | CUDA 12.6 + vLLM + Qwen2.5-Coder-3B-Instruct |

Images are public on ghcr.io. They contain **only** the CUDA base, vLLM, and the model weights. No credentials, no config, no local files.

To rebuild: push to `main` — GitHub Actions builds both images in parallel.

## API endpoints

Both containers expose an OpenAI-compatible API on port 3333.

**32B** (chat / design / review):
```
https://caper-sweetcorn-z3v9kf4mya1rjhm2.salad.cloud/v1
```

**3B** (fast completion / realtime):
```
https://jambul-kale-6xz4qzdswdm2a09k.salad.cloud/v1
```

## Managing containers

`salad-vllm` at `~/.local/bin/salad-vllm`. Config at `~/.config/salad/salad.ini`.

```bash
salad-vllm 32b start|stop|status|boot|ssh
salad-vllm 3b  start|stop|status|boot|ssh
```

- `start` — starts the container and waits until vLLM is serving
- `stop`  — stops the container (billing stops)
- `status` — shows container state, instance count, vLLM health, and URL
- `boot`  — starts container only (no vLLM health wait)
- `ssh`   — prints the current SSH connection string

## opencode integration

Default model is the 32B. Config at `~/.config/opencode/opencode.json`.

Required env var (add to shell profile):
```bash
export SALAD_API_KEY=<your-salad-api-key>
```

Workflow:
```bash
salad-vllm 32b start   # wait for vLLM to be ready (~3 min on cached node)
opencode               # uses 32B by default
salad-vllm 32b stop    # when done — stops billing
```

For the 3B, point your completion client at the 3B domain with the same `SALAD_API_KEY` header.

## Cold start times

| Scenario | Time |
|---|---|
| Image cached on node | ~3 min (GPU load + torch.compile from cache) |
| Fresh node (image pull + load) | ~25 min |

Salad caches images per node. If the same node is reused across sessions, cold start is always ~3 min.

## Notes

- Containers have `autostart_policy: false` — they only run when explicitly started
- Both use `restart_policy: always` — if vLLM crashes, Salad restarts it automatically
- `salad-vllm stop` is the only way to stop billing; closing opencode does not stop the container
