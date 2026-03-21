"""
submodules.py — Git submodule lifecycle management.
"""

import os

from .core import commit_if_dirty, get_authenticated_url, repo_name_from_url, run


def add_submodule(repo_url: str, path: str | None = None) -> None:
    """
    Register a repository as a git submodule of the current repo.

    Args:
        repo_url: Full HTTPS URL of the repository to add.
        path:     Local path for the submodule. Defaults to src/<repo_name>.
    """
    authenticated_url = get_authenticated_url(repo_url)
    name = repo_name_from_url(repo_url)
    submodule_path = path or os.path.join("src", name)

    print(f"Adding submodule: {name} → {submodule_path}")
    result = run(["git", "submodule", "add", authenticated_url, submodule_path])

    if result.returncode == 0:
        print(f"Submodule '{name}' added at '{submodule_path}'.")
        
        # Scrub authentication token from the tracked .gitmodules
        import re
        clean_url = re.sub(r"https://[^@]+@", "https://", authenticated_url)
        run(["git", "config", "--file", ".gitmodules", f"submodule.{submodule_path}.url", clean_url])
        run(["git", "add", ".gitmodules"])
        
        commit_if_dirty(f"chore: add submodule {name}")
    else:
        print(f"Failed to add submodule (exit code: {result.returncode})")


def init_submodules() -> None:
    """Initialize and clone all submodules registered in .gitmodules."""
    print("Initializing submodules...")
    result = run(["git", "submodule", "update", "--init", "--recursive"])
    if result.returncode == 0:
        print("Submodules initialized successfully.")
    else:
        print(f"Failed to initialize submodules (exit code: {result.returncode})")


def update_submodules() -> None:
    """
    Update all submodules to the latest commit on their remote branch.
    Equivalent to: git submodule update --remote --merge
    """
    print("Updating submodules to latest remote commit...")
    result = run(["git", "submodule", "update", "--remote", "--merge"])
    if result.returncode == 0:
        print("Submodules updated.")
        commit_if_dirty("chore: update submodules to latest")
    else:
        print(f"Failed to update submodules (exit code: {result.returncode})")


def _get_all_submodule_paths() -> list[str]:
    """Helper to list all registered submodule paths from .gitmodules."""
    result = run(["git", "config", "--file", ".gitmodules", "--get-regexp", "path"], capture=True)
    if result.returncode != 0:
        return []
    # Lines look like: submodule.src/BaseID.path src/BaseID
    paths = []
    for line in result.stdout.strip().splitlines():
        if " " in line:
            paths.append(line.split(" ", 1)[1])
    return paths


def remove_submodule(submodule_path: str) -> None:
    """
    Fully remove a submodule: deinitialize, remove from index, and clean up
    the .git/modules cache. Supports passing the repo name instead of the full path.

    Args:
        submodule_path: Local path or repository name of the submodule to remove.
    """
    registered_paths = _get_all_submodule_paths()
    resolved_path = None

    # 1. Exact match
    if submodule_path in registered_paths:
        resolved_path = submodule_path
    else:
        # 2. Match by repo name (e.g. "BaseID" matches "src/BaseID")
        matches = [p for p in registered_paths if os.path.basename(p) == submodule_path]
        if len(matches) == 1:
            resolved_path = matches[0]
        elif len(matches) > 1:
            print(f"Error: Multiple submodules match '{submodule_path}': {', '.join(matches)}")
            return

    if not resolved_path:
        print(f"Error: Could not find submodule matching '{submodule_path}' in .gitmodules.")
        print(f"Registered submodules: {', '.join(registered_paths) or 'none'}")
        return

    print(f"Removing submodule: {resolved_path}")

    # Deinit
    deinit_res = run(["git", "submodule", "deinit", "-f", resolved_path])
    if deinit_res.returncode != 0:
        print(f"Warning: git submodule deinit failed for '{resolved_path}' (already removed?)")

    # Git rm
    rm_res = run(["git", "rm", "-f", resolved_path])
    if rm_res.returncode != 0:
        print(f"Error: Failed to remove submodule '{resolved_path}' from git index.")
        return

    # Cleanup .git/modules cache
    git_modules_path = os.path.join(".git", "modules", resolved_path)
    if os.path.exists(git_modules_path):
        import shutil
        shutil.rmtree(git_modules_path)

    commit_if_dirty(f"chore: remove submodule {resolved_path}")
    print(f"Submodule '{resolved_path}' successfully removed.")


def sync_submodule_urls() -> None:
    """
    Synchronize submodule URLs from .gitmodules into the local git config.
    Run this after changing remote URLs in .gitmodules.
    """
    print("Syncing submodule URLs from .gitmodules...")
    result = run(["git", "submodule", "sync", "--recursive"])
    if result.returncode == 0:
        print("Submodule URLs synchronized.")
    else:
        print(f"Sync failed (exit code: {result.returncode})")


def status_submodules() -> None:
    """Display the current status of all submodules."""
    print("Submodule status:")
    run(["git", "submodule", "status", "--recursive"])
