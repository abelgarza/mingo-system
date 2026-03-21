"""
cli.py — Command-line entry point for git-protocol.

Usage:
    python3 -m src.git_protocol.cli <command> [options]
    git-protocol <command> [options]   (when installed via pip)
"""

import argparse

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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="git-protocol",
        description="GitHub repository and submodule management protocol",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", metavar="<command>")

    # ── clone ────────────────────────────────────────────────────────────────
    p = sub.add_parser("clone", help="Clone a remote repository")
    p.add_argument("url", help="Repository HTTPS URL")
    p.add_argument(
        "--no-scaffold",
        action="store_true",
        help="Skip workspace protocol after cloning",
    )

    # ── add ──────────────────────────────────────────────────────────────────
    p = sub.add_parser("add", help="Add a repository as a git submodule")
    p.add_argument("url", help="Repository HTTPS URL")
    p.add_argument(
        "--path",
        default=None,
        metavar="PATH",
        help="Local path for the submodule (default: src/<repo-name>)",
    )

    # ── init ─────────────────────────────────────────────────────────────────
    sub.add_parser("init", help="Initialize all submodules from .gitmodules")

    # ── update ───────────────────────────────────────────────────────────────
    sub.add_parser("update", help="Update all submodules to latest remote commit")

    # ── remove ───────────────────────────────────────────────────────────────
    p = sub.add_parser("remove", help="Fully remove a submodule")
    p.add_argument("path", help="Local path of the submodule to remove")

    # ── status ───────────────────────────────────────────────────────────────
    sub.add_parser("status", help="Show status of main repo and all submodules")

    # ── pull ─────────────────────────────────────────────────────────────────
    p = sub.add_parser("pull", help="Pull main repo and all submodules")
    p.add_argument("--dir", default=None, metavar="DIR", help="Repository root (default: cwd)")

    # ── fetch ────────────────────────────────────────────────────────────────
    p = sub.add_parser("fetch", help="Fetch all remotes for repo and submodules")
    p.add_argument("--dir", default=None, metavar="DIR", help="Repository root (default: cwd)")

    # ── sync ─────────────────────────────────────────────────────────────────
    sub.add_parser("sync", help="Sync submodule URLs from .gitmodules into local git config")

    # ── scaffold ─────────────────────────────────────────────────────────────
    p = sub.add_parser(
        "scaffold",
        help="Apply workspace protocol to an existing directory",
    )
    p.add_argument("dir", help="Target repository directory")
    p.add_argument("--name", default=None, metavar="NAME", help="Override repo name in templates")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    match args.command:
        case "clone":
            clone_repo(args.url, scaffold=not args.no_scaffold)
        case "add":
            add_submodule(args.url, args.path)
        case "init":
            init_submodules()
        case "update":
            update_submodules()
        case "remove":
            remove_submodule(args.path)
        case "status":
            status_all()
            status_submodules()
        case "pull":
            pull_all(args.dir)
        case "fetch":
            fetch_all(args.dir)
        case "sync":
            sync_submodule_urls()
        case "scaffold":
            scaffold_workspace(args.dir, repo_name=args.name)
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
