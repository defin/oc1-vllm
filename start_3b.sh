#!/bin/bash
# Wait for 32B to be ready before starting 3B to avoid GPU memory race
echo "Waiting for 32B to be ready..."
until curl -sf http://localhost:8000/v1/models > /dev/null 2>&1; do
    sleep 15
done
echo "32B ready, starting 3B..."
exec /opt/vllm-env/bin/python -m vllm.entrypoints.openai.api_server \
    --model              /models/qwen2.5-coder-3b \
    --host               127.0.0.1 \
    --port               8001 \
    --served-model-name  qwen2.5-coder-3b \
    --max-model-len      8192 \
    --gpu-memory-utilization 0.20 \
    --enable-prefix-caching
