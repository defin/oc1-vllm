#!/usr/bin/env python3
"""
Salad container startup script.
Installs vLLM, downloads the model, serves on port 3333.

Swap MODEL_ID / MODEL_DIR / VLLM_ARGS to change models.
"""

import os
import subprocess
from pathlib import Path

VENV   = "/opt/vllm-env"
PIP    = f"{VENV}/bin/pip"
PYTHON = f"{VENV}/bin/python"
HF     = f"{VENV}/bin/hf"

MODEL_ID  = "Qwen/Qwen2.5-Coder-3B-Instruct"
MODEL_DIR = "/models/qwen2.5-coder-3b"

VLLM_ARGS = [
    "--served-model-name",      "qwen2.5-coder-3b",
    "--max-model-len",          "8192",
    "--gpu-memory-utilization", "0.40",
    "--enable-prefix-caching",
]

HF_ENV = {**os.environ, "HF_HUB_ENABLE_HF_TRANSFER": "1"}


def run(cmd, **kwargs):
    print(f"+ {' '.join(str(c) for c in cmd)}", flush=True)
    subprocess.run(cmd, check=True, **kwargs)


def step(msg):
    print(f"\n=== {msg} ===", flush=True)


# ── 1. vLLM ───────────────────────────────────────────────────────────────────

if not Path(f"{VENV}/bin/vllm").exists():
    step("Installing vLLM")
    run(["python3", "-m", "venv", VENV])
    run([PIP, "install", "--upgrade", "pip", "--quiet"])
    run([PIP, "install", "vllm", "huggingface_hub", "hf_transfer", "--quiet"])
else:
    step("vLLM already installed — skipping")

# ── 2. Model ──────────────────────────────────────────────────────────────────

if not (Path(MODEL_DIR) / "config.json").exists():
    step(f"Downloading {MODEL_ID}")
    Path(MODEL_DIR).mkdir(parents=True, exist_ok=True)
    run([HF, "download", MODEL_ID, "--local-dir", MODEL_DIR], env=HF_ENV)
else:
    step("Model already present — skipping")

# ── 3. Serve ──────────────────────────────────────────────────────────────────

step("Starting vLLM on port 3333")
os.execv(PYTHON, [
    PYTHON, "-m", "vllm.entrypoints.openai.api_server",
    "--model", MODEL_DIR,
    "--host",  "::",
    "--port",  "3333",
    *VLLM_ARGS,
])
