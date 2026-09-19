"""Run the deterministic renderer declared by an experiment manifest."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys

import yaml


def repo_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / ".git").exists() and (candidate / "AGENTS.md").exists():
            return candidate
    raise SystemExit("repository root was not found")


def contained(root: Path, raw: str) -> Path:
    result = (root / raw).resolve()
    try:
        result.relative_to(root.resolve())
    except ValueError as exc:
        raise SystemExit(f"manifest path escapes repository: {raw}") from exc
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    manifest = args.manifest.resolve()
    root = repo_root(manifest.parent)
    try:
        data = yaml.safe_load(manifest.read_text(encoding="utf-8"))
        paths = data["paths"]
        renderer_raw = paths["renderer"]
        output_raw = paths["renders_dir"]
    except (OSError, yaml.YAMLError, TypeError, KeyError) as exc:
        raise SystemExit(f"cannot read renderer paths from {manifest}: {exc}") from exc
    if not isinstance(renderer_raw, str) or not isinstance(output_raw, str):
        raise SystemExit("manifest renderer and renders_dir paths must be strings")
    renderer = contained(root, renderer_raw)
    output = contained(root, output_raw)
    if renderer.suffix != ".py" or not renderer.is_file():
        raise SystemExit(f"renderer is not a Python file: {renderer}")
    output.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [sys.executable, str(renderer), "--export", "--output", str(output)],
        cwd=root,
        check=True,
    )


if __name__ == "__main__":
    main()
