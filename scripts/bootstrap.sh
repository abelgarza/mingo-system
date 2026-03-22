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
    if [ -n "$GITHUB_TOKEN" ]; then
        echo "[INFO] GITHUB_TOKEN detected. Configuring git to use HTTPS for submodules..."
        # Force git to use HTTPS with token instead of SSH for github.com
        git config --global url."https://${GITHUB_TOKEN}@github.com/".insteadOf "git@github.com:"
    fi

    git submodule update --init --recursive
    echo "[OK] Submodules initialized."
    
    # Cleanup global config if we set it
    if [ -n "$GITHUB_TOKEN" ]; then
        git config --global --unset url."https://${GITHUB_TOKEN}@github.com/".insteadOf
    fi
else
    echo "[WARN] No .gitmodules found. Skipping submodule initialization."
fi

# 1. Provide an .env if it doesn't exist
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        echo "[INFO] Creating .env file from .env.example..."
        cp .env.example .env
        echo "[WARN] Action required: Please fill in your specific secrets in the newly created .env file."
    else
        touch .env
        echo "[INFO] Created empty .env file."
    fi
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
source .venvs/mingo-workspace/bin/activate

# 3. Install Root Python Dependencies
echo "[INFO] Installing Python dependencies from requirements.txt..."
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
    echo "[OK] Root Python dependencies installed."
fi

# 3.1 Install Local Python Packages (Editable mode)
echo "[INFO] Linking internal Python packages (src/*)..."
for d in src/*/ ; do
    dir_name=$(basename "$d")
    
    # Skip legacy or external inspiration modules that might break the build
    if [ "$dir_name" = "InteligenciaComercial" ] || [ "$dir_name" = "flux_scraper" ]; then
        echo "       Skipping $dir_name (legacy/external module)..."
        continue
    fi

    if [ -f "${d}pyproject.toml" ] || [ -f "${d}setup.py" ]; then
        echo "       Installing ${d} in editable mode..."
        pip install -e "${d}"
    fi
done
echo "[OK] Internal packages linked."

# 4. Install Node.js Dependencies (gemini-cli)
echo "[INFO] Checking Node.js dependencies for agent orchestration layer..."
if [ -d "src/gemini-cli" ]; then
    cd src/gemini-cli
    if command -v npm >/dev/null 2>&1; then
        npm install
        if grep -q '"build":' package.json; then
            npm run build
        fi
        echo "[OK] Node dependencies installed and built."
    else
        echo "[WARN] 'npm' command not found! Cannot build gemini-cli."
    fi
    cd "$MINGO_ROOT"
fi

echo "[SUCCESS] Bootstrap complete! Mingo System is ready."
