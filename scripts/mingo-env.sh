# Mingo System Project Environment functions & aliases
# To be sourced lazily from ~/.bashrc

export MINGO_ROOT="$HOME/dev/mingo-system"

# Load dynamic aliases from my-manager
if [ -f "$MINGO_ROOT/mingo" ]; then
    eval "$($MINGO_ROOT/mingo alias --show)"
else
    # Fallback to old aliases if mingo script is missing
    alias mingo_venv="cd $MINGO_ROOT && source .venvs/mingo-workspace/bin/activate"
    alias gemini-cli="node $MINGO_ROOT/src/gemini-cli/bundle/gemini.js"
    alias gemini_cli="gemini-cli"
fi

alias git-protocol="source $MINGO_ROOT/.venvs/mingo-workspace/bin/activate && $MINGO_ROOT/mingo git"
alias vpn-manager="source $MINGO_ROOT/.venvs/mingo-workspace/bin/activate && vpn-manager"

# Provide an init function for interactive shells to safely load secrets if needed in bash
mingo_init() {
    if [ -f "$MINGO_ROOT/.env" ]; then
        # Load local .env without overwriting existing environment vars, unless requested
        export $(grep -v '^#' "$MINGO_ROOT/.env" | xargs)
        echo "[OK] Loaded mingo-system environment (.env)"
    else
        echo "[WARN] No .env file found in $MINGO_ROOT. Run scripts/bootstrap.sh first."
    fi
}
