"""
git_protocol — Workspace protocol for GitHub repository management.

Public API:
    clone_repo          Clone and scaffold a repository
    add_submodule       Register a repo as a git submodule
    init_submodules     Initialize submodules from .gitmodules
    update_submodules   Update submodules to latest remote commit
    remove_submodule    Fully remove a submodule
    sync_submodule_urls Sync URLs from .gitmodules into local config
    status_submodules   Show submodule status
    pull_all            Pull main repo + all submodules
    fetch_all           Fetch all remotes for repo + submodules
    status_all          Show status of repo + all submodules
    scaffold_workspace  Apply workspace protocol to a directory
"""

from .clone import clone_repo
from .maintenance import fetch_all, pull_all, status_all
from .scaffold import scaffold_workspace
from .submodules import (
    add_submodule,
    init_submodules,
    remove_submodule,
    status_submodules,
    sync_submodule_urls,
    update_submodules,
)

__all__ = [
    "clone_repo",
    "add_submodule",
    "init_submodules",
    "update_submodules",
    "remove_submodule",
    "sync_submodule_urls",
    "status_submodules",
    "pull_all",
    "fetch_all",
    "status_all",
    "scaffold_workspace",
]
