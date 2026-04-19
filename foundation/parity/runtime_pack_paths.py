from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_MT5_REQUEST = Path(
    "stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/"
    "mt5_snapshot_request_fpmarkets_v2_runtime_minimum_0001.json"
)


@dataclass(frozen=True)
class ResolvedRuntimePackPaths:
    mt5_request_path: Path
    stage_name: str
    stage_root: Path
    run_root: Path
    fixture_bindings_path: Path
    python_snapshot_path: Path
    mt5_snapshot_path: Path
    comparison_json_path: Path
    report_path: Path
    tester_ini_path: Path | None
    mt5_request: dict[str, Any]


def read_text_robust(path: Path) -> str:
    payload = path.read_bytes()
    for encoding in ("utf-8-sig", "utf-8", "cp1252"):
        try:
            return payload.decode(encoding)
        except UnicodeDecodeError:
            continue
    raise RuntimeError(f"Could not decode text from {path}")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text_robust(path))


def trim_leading_token(value: str, token: str) -> str:
    return value[len(token) :] if value.startswith(token) else value


def find_stage_name(path: Path) -> str:
    parts = path.parts
    try:
        stage_index = parts.index("stages")
    except ValueError as exc:  # pragma: no cover - defensive path guard
        raise RuntimeError(f"Could not infer stage root from MT5 request path: {path}") from exc
    if stage_index + 1 >= len(parts):
        raise RuntimeError(f"Could not infer stage name from MT5 request path: {path}")
    return parts[stage_index + 1]


def find_stage_root(path: Path) -> Path:
    parts = path.parts
    try:
        stage_index = parts.index("stages")
    except ValueError as exc:  # pragma: no cover - defensive path guard
        raise RuntimeError(f"Could not infer stage root from MT5 request path: {path}") from exc
    return Path(*parts[: stage_index + 2])


def find_single_tester_ini(run_root: Path) -> Path | None:
    ini_candidates = sorted(run_root.glob("mt5_tester_*.ini"))
    if not ini_candidates:
        return None
    if len(ini_candidates) > 1:
        joined = ", ".join(candidate.as_posix() for candidate in ini_candidates)
        raise RuntimeError(
            f"Expected exactly one mt5_tester_*.ini inside {run_root.as_posix()}, found: {joined}"
        )
    return ini_candidates[0]


def resolve_runtime_pack_paths(
    mt5_request_path: Path,
    *,
    fixture_bindings_path: Path | None = None,
    python_snapshot_path: Path | None = None,
    mt5_snapshot_path: Path | None = None,
    comparison_json_path: Path | None = None,
    report_path: Path | None = None,
    tester_ini_path: Path | None = None,
) -> ResolvedRuntimePackPaths:
    mt5_request = load_json(mt5_request_path)
    stage_name = find_stage_name(mt5_request_path)
    stage_root = find_stage_root(mt5_request_path)
    run_root = mt5_request_path.parent

    fixture_slug = trim_leading_token(str(mt5_request["fixture_set_id"]), "fixture_")
    bundle_slug = trim_leading_token(str(mt5_request["bundle_id"]), "bundle_")
    report_filename = f"{mt5_request['report_id']}.md"

    resolved_fixture_bindings_path = (
        fixture_bindings_path
        if fixture_bindings_path is not None
        else run_root / f"fixture_bindings_{fixture_slug}.json"
    )
    resolved_python_snapshot_path = (
        python_snapshot_path
        if python_snapshot_path is not None
        else run_root / f"python_snapshot_{fixture_slug}.json"
    )
    resolved_mt5_snapshot_path = (
        mt5_snapshot_path if mt5_snapshot_path is not None else Path(str(mt5_request["repo_import_path"]))
    )
    resolved_comparison_json_path = (
        comparison_json_path
        if comparison_json_path is not None
        else run_root / f"runtime_parity_comparison_{bundle_slug}.json"
    )
    resolved_report_path = (
        report_path if report_path is not None else stage_root / "03_reviews" / report_filename
    )
    resolved_tester_ini_path = (
        tester_ini_path if tester_ini_path is not None else find_single_tester_ini(run_root)
    )

    return ResolvedRuntimePackPaths(
        mt5_request_path=mt5_request_path,
        stage_name=stage_name,
        stage_root=stage_root,
        run_root=run_root,
        fixture_bindings_path=resolved_fixture_bindings_path,
        python_snapshot_path=resolved_python_snapshot_path,
        mt5_snapshot_path=resolved_mt5_snapshot_path,
        comparison_json_path=resolved_comparison_json_path,
        report_path=resolved_report_path,
        tester_ini_path=resolved_tester_ini_path,
        mt5_request=mt5_request,
    )
