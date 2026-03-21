"""
clone.py — Repository cloning with optional workspace scaffold.
"""

import os

from .core import get_authenticated_url, repo_name_from_url, run
from .scaffold import scaffold_workspace


def clone_repo(repo_url: str, scaffold: bool = True) -> None:
    """
    Clone a remote GitHub repository using the token from .env.

    Args:
        repo_url: Full HTTPS URL of the repository.
        scaffold: When True (default), apply the workspace protocol to the
                  freshly cloned directory after a successful clone.
    """
    authenticated_url = get_authenticated_url(repo_url)
    name = repo_name_from_url(repo_url)
    target_dir = os.path.join(os.getcwd(), name)

    print(f"Cloning into: {target_dir}")
    result = run(["git", "clone", authenticated_url, name])

    if result.returncode == 0:
        print(f"Repository '{name}' cloned successfully.")
        if scaffold:
            print("Applying workspace protocol...")
            scaffold_workspace(target_dir, repo_name=name)
    else:
        print(f"Clone failed (exit code: {result.returncode})")
