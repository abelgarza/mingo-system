"""
scaffold.py — Workspace protocol: write standard project files into a target repo.

Any repository that is cloned, forked, or connected through git-protocol will
receive these files, ensuring a consistent workspace structure across all repos.
"""

import os
import shutil
from pathlib import Path

# Directory containing the template files shipped with this package
TEMPLATES_DIR = Path(__file__).parent / "templates"


def get_template(name: str) -> str:
    """
    Read a template file from the templates/ directory.

    Args:
        name: Template filename (e.g. 'gitignore.tmpl').

    Returns:
        Raw template string.
    """
    template_path = TEMPLATES_DIR / name
    return template_path.read_text(encoding="utf-8")


def scaffold_workspace(target_dir: str, repo_name: str | None = None) -> None:
    """
    Apply the workspace protocol to a target directory by writing all standard
    project files. Existing files are NOT overwritten — the protocol only fills
    in what is missing.

    Files written:
      - .gitignore
      - pyproject.toml  (repo_name substituted)
      - requirements.txt
      - .vscode/settings.json (repo_name substituted)
      - src/__init__.py

    Args:
        target_dir: Absolute or relative path to the repository root.
        repo_name:  Name used in generated file templates. Defaults to the
                    base name of target_dir.
    """
    root = Path(target_dir)
    root.mkdir(parents=True, exist_ok=True)

    name = repo_name or root.name

    _write_if_missing(root / ".gitignore", get_template("gitignore.tmpl"))
    _write_if_missing(
        root / "pyproject.toml",
        get_template("pyproject.tmpl").replace("{repo_name}", name),
    )
    _write_if_missing(root / "requirements.txt", get_template("requirements.tmpl"))

    vscode_dir = root / ".vscode"
    vscode_dir.mkdir(exist_ok=True)
    _write_if_missing(
        vscode_dir / "settings.json",
        get_template("vscode_settings.tmpl").replace("{repo_name}", name),
    )

    src_pkg_dir = root / "src" / name
    src_pkg_dir.mkdir(parents=True, exist_ok=True)
    _write_if_missing(src_pkg_dir / "__init__.py", f'"""\n{name} — package initialization.\n"""\n')
    _install_pre_commit_hook(root)

    print(f"Workspace protocol applied to: {root.resolve()}")
    print(f"  .gitignore, pyproject.toml, requirements.txt, .vscode/settings.json, src/{name}/__init__.py, .git/hooks/pre-commit")


def _install_pre_commit_hook(root: Path) -> None:
    """Install the secret-scanning pre-commit hook if the git repo exists."""
    hooks_dir = root / ".git" / "hooks"
    if hooks_dir.exists():
        hook_path = hooks_dir / "pre-commit"
        _write_if_missing(hook_path, get_template("pre-commit.tmpl"))
        # Ensure it is executable
        if hook_path.exists():
            os.chmod(hook_path, 0o755)


def _write_if_missing(path: Path, content: str) -> None:
    """Write content to path only if the file does not already exist."""
    if path.exists():
        print(f"  [skip] {path.name} already exists")
    else:
        path.write_text(content, encoding="utf-8")
        print(f"  [write] {path.name}")
