"""
maintenance.py — Day-to-day repo maintenance: pull, fetch, status.
"""

import os

from .core import run


def pull_all(repo_dir: str | None = None) -> None:
    """
    Pull the latest changes for the main repository and all its submodules.

    Args:
        repo_dir: Path to the repository root. Defaults to the current directory.
    """
    cwd = repo_dir or os.getcwd()
    print(f"Pulling main repo at: {cwd}")
    run(["git", "pull"], cwd=cwd)

    print("Pulling all submodules...")
    run(
        ["git", "submodule", "foreach", "--recursive", "git pull origin HEAD"],
        cwd=cwd,
    )
    print("Pull complete.")


def fetch_all(repo_dir: str | None = None) -> None:
    """
    Fetch all remotes for the main repository and all its submodules.

    Args:
        repo_dir: Path to the repository root. Defaults to the current directory.
    """
    cwd = repo_dir or os.getcwd()
    print("Fetching main repo...")
    run(["git", "fetch", "--all", "--prune"], cwd=cwd)

    print("Fetching submodules...")
    run(
        ["git", "submodule", "foreach", "--recursive", "git fetch --all --prune"],
        cwd=cwd,
    )
    print("Fetch complete.")


def status_all(repo_dir: str | None = None) -> None:
    """
    Show git status of the main repository and each submodule.

    Args:
        repo_dir: Path to the repository root. Defaults to the current directory.
    """
    cwd = repo_dir or os.getcwd()
    print(f"── Main repo status ({cwd}) ──")
    run(["git", "status", "-s"], cwd=cwd)

    print("\n── Submodule status ──")
    run(
        ["git", "submodule", "foreach", "--recursive", "echo '→ $name:' && git status -s"],
        cwd=cwd,
    )
