#!/bin/bash
# scripts/ensure-venv.sh
# Shared utility to ensure the Python virtual environment exists and is ready.

MINGO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_PATH="$MINGO_ROOT/.venvs/mingo-workspace"
REQUIREMENTS="$MINGO_ROOT/requirements.txt"

# Ensure we are in the root directory
cd "$MINGO_ROOT"

# Check if venv exists
if [ ! -d "$VENV_PATH" ]; then
    echo "[INFO] Virtual environment not found. Creating one at $VENV_PATH..."
    mkdir -p "$MINGO_ROOT/.venvs"
    python3 -m venv "$VENV_PATH"
    echo "[OK] Created new virtual environment."
    
    # Fresh venv needs dependencies
    echo "[INFO] Installing initial dependencies..."
    source "$VENV_PATH/bin/activate"
    pip install --upgrade pip
    pip install -r "$REQUIREMENTS"
    echo "[OK] Initial dependencies installed."
else
    # If it exists, we just ensure it's functional (optional: could check for requirements update here)
    # For now, we just return success
    :
fi

# Export VENV_PATH for other scripts to use
export VENV_PATH
echo "[INFO] Environment ready."
