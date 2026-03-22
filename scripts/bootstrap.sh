#!/bin/bash
set -e

# Mingo System Scaffolding & Bootstrap Script
# Ensures that the environment is fully built, dependencies installed, and secrets prepared.
# Designed to be idempotent and friendly for both host initialization and future Dockerfiles.

MINGO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$MINGO_ROOT"

echo "[INFO] Starting Mingo System Initialization..."

# 0. Initialize Submodules
echo "[INFO] Initializing git submodules..."
if [ -f .gitmodules ]; then
    # Stage .gitmodules if there are changes (like commenting out broken submodules)
    git add .gitmodules 2>/dev/null || true
    git submodule update --init --recursive
    echo "[OK] Submodules initialized."
else
    echo "[WARN] No .gitmodules found. Skipping submodule initialization."
fi

# 1. Provide an .env if it doesn't exist
if [ ! -f .env ]; then
    echo "[INFO] Creating .env file from .env.example..."
    cp .env.example .env
    echo "[WARN] Action required: Please fill in your specific secrets in the newly created .env file."
else
    echo "[OK] .env file already exists."
fi

# 2. Setup Python Virtual Environment
echo "[INFO] Setting up Python Virtual Environment..."
source scripts/ensure-venv.sh
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to ensure virtual environment."
    exit 1
fi

# 3. Install Python Dependencies
echo "[INFO] Installing Python dependencies from requirements.txt..."
source .venvs/mingo-workspace/bin/activate
pip install -r requirements.txt
echo "[OK] Python dependencies installed."

# 4. Install Node.js Dependencies (gemini-cli)
echo "[INFO] Checking Node.js dependencies for agent orchestration layer..."
if [ -d "src/gemini-cli" ]; then
    cd src/gemini-cli
    if command -v npm >/dev/null 2>&1; then
        npm install
        # Check if we should build (if there's a build script in package.json)
        if grep -q '"build":' package.json; then
            npm run build
        fi
        echo "[OK] Node dependencies installed and built."
    else
        echo "[WARN] 'npm' command not found! Cannot build gemini-cli."
        echo "       Please install Node.js and npm (e.g., sudo apt install nodejs npm)."
    fi
    cd "$MINGO_ROOT"
fi

echo "[SUCCESS] Bootstrap complete! Mingo System is ready."
