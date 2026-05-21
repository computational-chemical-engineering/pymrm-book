"""Execute notebooks needed for the deployed book before the HTML build.

The MyST/Jupyter Book execution manager can leave a kernel/server wait open on
GitHub Actions after all visible pages have built. Running nbconvert explicitly
keeps execution one notebook at a time and gives every notebook a hard process
timeout before the static site build starts.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import sys

import yaml


DEFAULT_DIRS = (
    Path("content/lecture_notes"),
    Path("pymrm/tutorials"),
    Path("pymrm/examples"),
)


def iter_file_entries(node: object) -> list[Path]:
    entries: list[Path] = []
    if isinstance(node, dict):
        file_entry = node.get("file")
        if isinstance(file_entry, str):
            entries.append(Path(file_entry))
        for value in node.values():
            entries.extend(iter_file_entries(value))
    elif isinstance(node, list):
        for item in node:
            entries.extend(iter_file_entries(item))
    return entries


def is_under(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def iter_notebooks(paths: list[Path], toc_path: Path) -> list[Path]:
    toc = yaml.safe_load(toc_path.read_text(encoding="utf-8"))
    candidates = [
        path
        for path in iter_file_entries(toc)
        if path.suffix == ".ipynb" and any(is_under(path, root) for root in paths)
    ]
    seen: set[Path] = set()
    notebooks: list[Path] = []
    for path in candidates:
        if path not in seen and path.exists():
            notebooks.append(path)
            seen.add(path)
    return notebooks


def execute_notebook(path: Path, timeout: int, cell_timeout: int) -> None:
    command = [
        sys.executable,
        "-m",
        "nbconvert",
        "--to",
        "notebook",
        "--execute",
        "--inplace",
        f"--ExecutePreprocessor.timeout={cell_timeout}",
        str(path),
    ]
    env = os.environ.copy()
    env.setdefault("MPLBACKEND", "Agg")
    env.setdefault("PYTHONUNBUFFERED", "1")

    print(f"Executing {path}", flush=True)
    try:
        result = subprocess.run(
            command,
            check=False,
            env=env,
            text=True,
            capture_output=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        print(f"Timed out after {timeout} s while executing {path}", file=sys.stderr)
        if exc.stdout:
            print(exc.stdout, file=sys.stderr)
        if exc.stderr:
            print(exc.stderr, file=sys.stderr)
        raise SystemExit(124) from exc

    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        default=list(DEFAULT_DIRS),
        help="Notebook files or directories to execute.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=300,
        help="Maximum wall time per notebook process in seconds.",
    )
    parser.add_argument(
        "--cell-timeout",
        type=int,
        default=180,
        help="Maximum execution time per notebook cell in seconds.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print notebooks that would be executed and exit.",
    )
    parser.add_argument(
        "--toc",
        type=Path,
        default=Path("myst.yml"),
        help="Book TOC/config file used to select referenced notebooks.",
    )
    args = parser.parse_args()

    notebooks = iter_notebooks(args.paths, args.toc)
    if not notebooks:
        raise SystemExit("No notebooks found to execute.")

    print(f"Found {len(notebooks)} notebooks to execute.", flush=True)
    for notebook in notebooks:
        if args.dry_run:
            print(notebook)
        else:
            execute_notebook(notebook, args.timeout, args.cell_timeout)


if __name__ == "__main__":
    main()
