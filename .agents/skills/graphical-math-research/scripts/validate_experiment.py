"""Validate a math-viz-lab experiment manifest and its named states."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys
from typing import Any

import yaml


ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
EVIDENCE_CLASSES = {
    "visual_observation",
    "numerical_evidence",
    "conjecture",
    "counterexample",
    "lean_proved",
}


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ValueError(f"cannot read YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("document root must be a mapping")
    return data


def find_repo_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / ".git").exists() and (candidate / "AGENTS.md").exists():
            return candidate
    raise ValueError("repository root with .git and AGENTS.md was not found")


def require_mapping(data: dict[str, Any], key: str, errors: list[str]) -> dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        errors.append(f"{key}: required mapping")
        return {}
    return value


def require_text(data: dict[str, Any], key: str, prefix: str, errors: list[str]) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{prefix}.{key}: required non-empty string")
        return ""
    return value


def resolve_repo_path(repo: Path, raw: str, label: str, errors: list[str]) -> Path:
    candidate = (repo / raw).resolve()
    try:
        candidate.relative_to(repo.resolve())
    except ValueError:
        errors.append(f"{label}: path escapes repository: {raw}")
        return candidate
    if not candidate.exists():
        errors.append(f"{label}: referenced path does not exist: {raw}")
    return candidate


def validate_manifest(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        data = load_yaml(path)
        repo = find_repo_root(path.resolve().parent)
    except ValueError as exc:
        return [str(exc)]

    if data.get("schema_version") != 1:
        errors.append("schema_version: expected 1")

    experiment = require_mapping(data, "experiment", errors)
    experiment_id = require_text(experiment, "id", "experiment", errors)
    if experiment_id and not ID_PATTERN.fullmatch(experiment_id):
        errors.append("experiment.id: expected kebab-case identifier")
    require_text(experiment, "title", "experiment", errors)
    require_text(experiment, "status", "experiment", errors)

    mathematical_object = require_mapping(data, "object", errors)
    for key in ("family", "parameter_space", "state_space", "solution_locus"):
        require_text(mathematical_object, key, "object", errors)

    paths = require_mapping(data, "paths", errors)
    resolved: dict[str, Path] = {}
    for key in ("renderer", "lean_source", "notes", "states_dir", "renders_dir"):
        raw = require_text(paths, key, "paths", errors)
        if raw:
            resolved[key] = resolve_repo_path(repo, raw, f"paths.{key}", errors)

    view = require_mapping(data, "view", errors)
    sequence = view.get("projection_sequence")
    if not isinstance(sequence, list) or not sequence or not all(isinstance(item, str) for item in sequence):
        errors.append("view.projection_sequence: expected non-empty string list")
    default_state = require_text(view, "default_state", "view", errors)

    research = require_mapping(data, "research", errors)
    require_text(research, "question", "research", errors)
    for key in ("observations", "conjectures", "proved_claims"):
        if not isinstance(research.get(key), list):
            errors.append(f"research.{key}: expected list")
    for collection in ("observations", "conjectures", "proved_claims"):
        for index, item in enumerate(research.get(collection, [])):
            if not isinstance(item, dict):
                errors.append(f"research.{collection}[{index}]: expected mapping")
                continue
            evidence = item.get("evidence")
            if evidence not in EVIDENCE_CLASSES:
                errors.append(f"research.{collection}[{index}].evidence: invalid class {evidence!r}")

    render = require_mapping(data, "render", errors)
    if render.get("format") not in {"svg", "png"}:
        errors.append("render.format: expected svg or png")
    if render.get("browser_based") is not False:
        errors.append("render.browser_based: must be false")
    for key in ("deterministic", "axes_required", "legends_required", "equal_comparison_panels"):
        if not isinstance(render.get(key), bool):
            errors.append(f"render.{key}: expected boolean")

    validation = require_mapping(data, "validation", errors)
    commands = validation.get("commands")
    if not isinstance(commands, list) or not commands or not all(isinstance(item, str) and item.strip() for item in commands):
        errors.append("validation.commands: expected non-empty string list")

    states_dir = resolved.get("states_dir")
    state_ids: set[str] = set()
    if states_dir and states_dir.is_dir():
        state_files = sorted(states_dir.glob("*.yaml"))
        if not state_files:
            errors.append("paths.states_dir: no state YAML files found")
        for state_path in state_files:
            try:
                state = load_yaml(state_path)
            except ValueError as exc:
                errors.append(f"{state_path.name}: {exc}")
                continue
            if state.get("schema_version") != 1:
                errors.append(f"{state_path.name}: schema_version must be 1")
            if state.get("experiment_id") != experiment_id:
                errors.append(f"{state_path.name}: experiment_id does not match manifest")
            state_id = state.get("state_id")
            if not isinstance(state_id, str) or not ID_PATTERN.fullmatch(state_id):
                errors.append(f"{state_path.name}: invalid state_id")
            elif state_id in state_ids:
                errors.append(f"{state_path.name}: duplicate state_id {state_id}")
            else:
                state_ids.add(state_id)
            for key in ("projection", "question", "evidence_status"):
                require_text(state, key, state_path.name, errors)
            if not isinstance(state.get("parameters"), dict):
                errors.append(f"{state_path.name}.parameters: expected mapping")
            if not isinstance(state.get("expected"), dict):
                errors.append(f"{state_path.name}.expected: expected mapping")
            if state.get("evidence_status") not in EVIDENCE_CLASSES:
                errors.append(f"{state_path.name}.evidence_status: invalid evidence class")
            if state.get("evidence_status") == "lean_proved":
                require_text(state, "lean_theorem", state_path.name, errors)
            if isinstance(state_id, str) and state_path.stem != state_id:
                errors.append(
                    f"{state_path.name}: filename must match state_id {state_id!r}"
                )
        if default_state and default_state not in state_ids:
            errors.append(f"view.default_state: unknown state_id {default_state!r}")

    return errors


def discover_manifests(repo: Path) -> list[Path]:
    return sorted((repo / "experiments").glob("*/experiment.yaml"))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", nargs="?", type=Path)
    parser.add_argument("--all", action="store_true", help="validate every experiment")
    args = parser.parse_args()
    repo = find_repo_root(Path.cwd().resolve())
    manifests = discover_manifests(repo) if args.all else [args.manifest or Path("experiment.yaml")]
    if not manifests:
        raise SystemExit("no experiment manifests found")

    failure = False
    for manifest in manifests:
        manifest = manifest if manifest.is_absolute() else (Path.cwd() / manifest)
        errors = validate_manifest(manifest.resolve())
        if errors:
            failure = True
            print(f"FAIL {manifest}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"OK   {manifest}")
    raise SystemExit(1 if failure else 0)


if __name__ == "__main__":
    main()
