"""
core.py — Low-level git helpers shared across the protocol package.
"""

import os
import subprocess
import sys

from dotenv import load_dotenv

load_dotenv()


def run(cmd: list[str], cwd: str | None = None, capture: bool = False) -> subprocess.CompletedProcess:
    """Execute a shell command and return the result."""
    return subprocess.run(cmd, cwd=cwd, capture_output=capture, text=True)


def get_authenticated_url(repo_url: str) -> str:
    """
    Build an authenticated GitHub URL by injecting GITHUB_TOKEN from the
    environment. Exits with an error if the token is not set.
    """
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("Error: GITHUB_TOKEN not found in .env")
        sys.exit(1)

    prefix = "https://"
    clean_path = repo_url[len(prefix):] if repo_url.startswith(prefix) else repo_url
    return f"https://{token}@{clean_path}"


def commit_if_dirty(message: str, cwd: str | None = None) -> None:
    """
    Stage all changes and create a commit if there are any uncommitted files.
    Useful after submodule add/remove/update operations.
    """
    result = run(["git", "status", "--porcelain"], cwd=cwd, capture=True)
    if result.stdout.strip():
        run(["git", "add", "-A"], cwd=cwd)
        run(["git", "commit", "-m", message], cwd=cwd)
        print(f"Commit created: '{message}'")


def repo_name_from_url(repo_url: str) -> str:
    """Extract the plain repository name from a git URL."""
    return repo_url.rstrip("/").split("/")[-1].replace(".git", "")
