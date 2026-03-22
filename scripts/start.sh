#!/bin/bash
set -e

MINGO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$MINGO_ROOT"

echo "[INFO] Starting Mingo System Services..."

# Ensure environment is sourced
if [ -f "scripts/mingo-env.sh" ]; then
    source scripts/mingo-env.sh
    mingo_init > /dev/null
fi

mkdir -p logs tmp

# 1. Start Ollama Backend
if [ -d "src/ollama" ]; then
    echo "[INFO] Starting Ollama Local Inference backend..."
    if [ ! -f "tmp/ollama.pid" ]; then
        # Check if the go tool is available
        if command -v go >/dev/null 2>&1; then
            cd src/ollama
            # Run the server in background
            go run main.go serve > ../../logs/ollama.log 2>&1 &
            OLLAMA_PID=$!
            cd "$MINGO_ROOT"
            echo $OLLAMA_PID > tmp/ollama.pid
            echo "[OK] Ollama started with PID $OLLAMA_PID. Logs in logs/ollama.log."
        else
            echo "[WARN] 'go' command not found. Cannot start Ollama backend locally."
        fi
    else
        echo "[OK] Ollama is already running (PID: $(cat tmp/ollama.pid))."
    fi
fi

echo "[SUCCESS] All background services started."
echo "You can now use 'mingo_venv' and 'gemini_cli' aliases. To stop the services, run ./scripts/stop.sh"
