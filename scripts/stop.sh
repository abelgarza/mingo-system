#!/bin/bash
set -e

MINGO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$MINGO_ROOT"

echo "[INFO] Shutting down Mingo System Services..."

# 1. Stop Ollama Backend
if [ -f "tmp/ollama.pid" ]; then
    OLLAMA_PID=$(cat tmp/ollama.pid)
    echo "[INFO] Stopping Ollama Service (PID: $OLLAMA_PID)..."
    kill -15 $OLLAMA_PID 2>/dev/null || true
    rm -f tmp/ollama.pid
    echo "[OK] Ollama stopped."
else
    echo "[OK] Ollama is not currently running."
fi

echo "[SUCCESS] All background services stopped."
