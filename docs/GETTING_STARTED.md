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

The bootstrap script performs the following actions:
- **Initialize Submodules**: Recursively initializes all internal modules and repositories.
- **Environment Setup**: Creates a local `.env` file from the provided `.env.example`.
- **Python Virtualenv**: Sets up an isolated Python virtual environment in `.venvs/mingo-workspace`.
- **Dependency Installation**: Installs core ecosystem requirements and links internal Python packages from `src/*` in editable mode.
- **Node.js Build**: Installs and compiles the `gemini-cli` orchestration layer.

> [!IMPORTANT]
> Open the generated `.env` file and fill in your API keys (e.g., `GEMINI_ML`).

### 2. Configure Shell Environment
To integrate Mingo seamlessly with your shell, you should source the environment script in your `~/.bashrc`:

```bash
# Add this to your ~/.bashrc
source /path/to/mingo-system/scripts/mingo-env.sh
```

This provides several key helpers:
- `mingo_venv`: Quickly activate the project's Python virtual environment.
- `mingo_init`: Explicitly load the `.env` secrets into your current bash session.
- `gemini_cli`: Launch the AI orchestrator from any directory.
- `git_protocol`: Invoke the workspace management tool.

### 3. Launch the System
To spin up all necessary background daemons (like Ollama) and prepare the system for execution:

```bash
./scripts/start.sh
```

### 4. Development Workflow
Maintain the modularity of the system by following these structural mandates:

- **AI Logic & CLI Tools**: New agent-related features or CLI improvements go into `src/gemini-cli/`.
- **Git & Repository Lifecycle**: Logic for workspace structure or Git automation goes into `src/git_protocol/`.
- **Model Serving**: Enhancements to the local inference engine go into `src/ollama/`.

### 5. Teardown
To gracefully stop all background services:
```bash
./scripts/stop.sh
```

## Documentation & Architecture
Please refer to `GEMINI.md` for architectural mandates and coding standards.

