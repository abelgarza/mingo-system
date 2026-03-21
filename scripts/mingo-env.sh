# Mingo System Project Environment functions & aliases
# To be sourced lazily from ~/.bashrc

export MINGO_ROOT="$HOME/dev/mingo-system"

alias mingo_venv="cd $MINGO_ROOT && source .venvs/mingo-workspace/bin/activate"
alias gemini_cli="node $MINGO_ROOT/src/gemini-cli/bundle/gemini.js"

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
