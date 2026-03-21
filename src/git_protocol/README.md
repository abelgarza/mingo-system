# Git Protocol

A GitHub repository and submodule management protocol for structured workspaces.

## Features

- **Clone & Scaffold**: Clone repositories and automatically set up workspace templates.
- **Submodule Management**: Add, initialize, update, and remove submodules with ease.
- **Maintenance**: Unified status, pull, and fetch commands for the main repository and all submodules.
- **Sync**: Keep local git configuration in sync with `.gitmodules`.

## Usage

You can run `git-protocol` directly if installed via pip, or using the module interface:

```bash
python3 -m src.git_protocol.cli <command> [options]
```

### Getting Help

The protocol includes built-in help documentation for all commands. Use the `--help` flag to see available options:

```bash
# General help
python3 -m src.git_protocol.cli --help

# Help for a specific subcommand
python3 -m src.git_protocol.cli clone --help
```

### Help Output

```text
usage: git-protocol [-h] <command> ...

GitHub repository and submodule management protocol

positional arguments:
  <command>
    clone     Clone a remote repository
    add       Add a repository as a git submodule
    init      Initialize all submodules from .gitmodules
    update    Update all submodules to latest remote commit
    remove    Fully remove a submodule
    status    Show status of main repo and all submodules
    pull      Pull main repo and all submodules
    fetch     Fetch all remotes for repo and submodules
    sync      Sync submodule URLs from .gitmodules into local git config
    scaffold  Apply workspace protocol to an existing directory

options:
  -h, --help  show this help message and exit
```

## Commands

- `clone <url>`: Clones a repo and runs the scaffolding protocol.
- `add <url> [--path PATH]`: Adds a repo as a git submodule (default path: `src/<repo-name>`).
- `init`: Initializes all submodules from `.gitmodules`.
- `update`: Updates all submodules to the latest remote commit.
- `remove <path>`: Fully removes a submodule from the project.
- `status`: Shows status of the main repo and all submodules.
- `pull [--dir DIR]`: Pulls main repo and all submodules.
- `fetch [--dir DIR]`: Fetches all remotes for repo and submodules.
- `sync`: Syncs submodule URLs from `.gitmodules` into local git config.
- `scaffold <dir> [--name NAME]`: Applies workspace protocol templates.
