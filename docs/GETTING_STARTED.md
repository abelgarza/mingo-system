# Mingo System

A polyglot composite workspace serving as a powerful, AI-driven development toolkit. 

Mingo System is architected across three core microservices:
1. **AI Orchestrator (`src/gemini-cli`)**: The Node/TypeScript-based command-line interface and logic brain.
2. **Workspace Protocol (`src/git_protocol`)**: The Python-based automation and repository management layer.
3. **Local Inference (`src/ollama`)**: The Go-based backend for serving and querying LLMs locally.

## Getting Started

### 1. Bootstrap the Environment
We use a unified initialization script to isolate dependencies, configure Python virtual environments uniquely for this workspace, and generate the required secrets structure.

```bash
./scripts/bootstrap.sh
```

> **Note:** Open the generated `.env` file and fill in your API keys (e.g., `GEMINI_ML`).

### 2. Launch the System
To spin up all necessary background daemons (like Ollama) and prepare the system for execution:

```bash
./scripts/start.sh
```

### 3. Usage
You can drop into the isolated Mingo virtual environment and invoke the Orchestrator via the host-registered aliases (ensure your `~/.bashrc` sources `scripts/mingo-env.sh`):

```bash
# Activate the mingo Python virtualenv explicitly
mingo_venv

# Run the gemini-cli directly
gemini_cli
```

### 4. Teardown
To gracefully stop all background services (reading from PID files):
```bash
./scripts/stop.sh
```

## Documentation & Architecture
Please refer to `GEMINI.md` for architectural mandates and coding standards.
