# Project Mandates: mingo-system

This document establishes the foundational architectural principles, coding standards, and project policies for **mingo-system**. These instructions take absolute precedence over general defaults.

## Project Scope & Architecture
`mingo-system` is a polyglot **Composite Workspace** designed as an AI-powered development toolkit. It integrates three primary domains:

1.  **AI Orchestration (`src/gemini-cli`):** The primary user interface and "brain" of the system. Built with TypeScript/Node.js, it handles agentic workflows and tool execution.
2.  **Workspace Protocol (`src/my-manager`):** A Python-based management layer that enforces the workspace structure, handles submodules, and automates repository maintenance.
3.  **Local Inference (`src/ollama`):** A Go-based backend providing local LLM serving capabilities, acting as a provider for the AI orchestrator.

## Code Organization & Policies

### Environment & Initialization
- **System Bootstrapping:** All initialization, dependency resolution, and lifecycle management scripts must reside in `scripts/`.
  - `bootstrap.sh`: Automates dependency installation (`pip`, `npm`, `venv`) and scaffolds `.env`.
  - `start.sh` & `stop.sh`: Unified service loop for background daemons like `ollama`.
  - `mingo-env.sh`: Interactive shell exports and aliases (lazy-loaded by the host `~/.bashrc`).
- **Secrets Management:** Project-specific secrets must strictly reside in `mingo-system/.env` to avoid polluting the host's global environment. Do not push `.env` to version control.

### Where to Place New Features
- **AI Logic & CLI Tools:** All agent-related features, new tools for the CLI, or UI/UX improvements must reside in `src/gemini-cli/`.
- **Git & Repository Lifecycle:** Any logic related to how the workspace is structured, how submodules are managed, or custom Git automation must reside in `src/my-manager/`.
- **Model Serving & LLM Backend:** Enhancements to the local inference engine or model management go into `src/ollama/`.

### Directory Structure Integrity
- Do not add top-level directories to `src/` without explicit justification.
- Maintain the modularity of each component; they should interact via clearly defined APIs or CLI interfaces, avoiding tight coupling.

## Engineering Standards

### Core Principles
- **Object-Oriented Programming (OOP):** Strictly adhere to OOP principles (Encapsulation, Inheritance, Polymorphism, Abstraction). Focus on clean, modular abstractions rather than procedural scripts.
- **Language:** All code (symbols, variables, classes), comments, documentation, and commit messages must be in **English**.
- **Naming:** Use descriptive, intentional names. Favor readability over brevity.

### Python Standards (`src/my-manager`)
- **PEP 8:** Mandatory adherence to PEP 8 style guidelines.
- **Typing:** Use Python type hints (`typing` module) for all function signatures and class members.
- **Documentation:** Use Google-style docstrings for all public classes and methods.

### TypeScript/Node Standards (`src/gemini-cli`)
- Follow modern TypeScript best practices (strict mode, interfaces over types when applicable).
- Maintain high test coverage for all new packages within the monorepo.

## Validation & Quality Assurance
- **Testing:** Every new feature or bug fix **must** include automated tests (Unit/Integration).
- **Static Analysis:** All code must pass the project's configured linters and type-checkers before being considered complete.
- **Refactoring:** Prioritize consolidating logic into clean abstractions during the development process. Avoid "just-in-case" code.
