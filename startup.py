#!/usr/bin/env python3
"""
Salad container startup script.
Set as the container command: python3 /startup.py
Installs vLLM, downloads the model, then starts serving.
"""

import os
import subprocess
from pathlib import Path

MODEL_ID   = "Qwen/Qwen2.5-Coder-32B-Instruct-AWQ"
MODEL_DIR  = "/models/qwen2.5-coder-32b-awq"
VENV       = "/opt/vllm-env"
PIP        = f"{VENV}/bin/pip"
PYTHON     = f"{VENV}/bin/python"
PORT       = 3333


def run(cmd, **kwargs):
    print(f"+ {' '.join(cmd)}", flush=True)
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

config_file = Path(MODEL_DIR) / "config.json"
if not config_file.exists():
    step(f"Downloading {MODEL_ID}")
    Path(MODEL_DIR).mkdir(parents=True, exist_ok=True)
    env = {**os.environ, "HF_HUB_ENABLE_HF_TRANSFER": "1"}
    run(
        [f"{VENV}/bin/hf", "download", MODEL_ID, "--local-dir", MODEL_DIR],
        env=env,
    )
else:
    step("Model already present — skipping download")

# ── 3. vLLM server ────────────────────────────────────────────────────────────

step(f"Starting vLLM on port {PORT}")
os.execv(PYTHON, [
    PYTHON, "-m", "vllm.entrypoints.openai.api_server",
    "--model",              MODEL_DIR,
    "--host",               "0.0.0.0",
    "--port",               str(PORT),
    "--served-model-name",  "qwen2.5-coder-32b",
    "--quantization",       "awq_marlin",
    "--max-model-len",      "32768",
    "--gpu-memory-utilization", "0.92",
    "--enable-prefix-caching",
])
