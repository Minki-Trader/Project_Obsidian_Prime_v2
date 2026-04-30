from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

import yaml

from foundation.control_plane.audit_result import COMPLETION_CLAIMS, AuditFinding, AuditResult
from foundation.control_plane.ledger import io_path, path_exists, read_csv_rows


CURRENT_TRUTH_SYNC_CLAIMS = ("current_truth_synced", "state_sync_completed", "stage_transition_completed")


@dataclass(frozen=True)
class CurrentTruthSnapshot:
    active_stage: str
    workspace_active_branch: str
    actual_git_branch: str
    workspace_current_run: str
    current_working_run: str
    selection_status_run: str
    stage_brief_boundary: str
    registry_has_current_run: bool
    stage_ledger_has_current_run: bool
    source_paths: Mapping[str, str]

    def current_run_values(self) -> dict[str, str]:
        return {
            key: value
            for key, value in {
                "workspace_state": self.workspace_current_run,
                "current_working_state": self.current_working_run,
                "selection_status": self.selection_status_run,
            }.items()
            if value
        }

    def to_counts(self) -> dict[str, Any]:
        return {
            "active_stage": self.active_stage,
            "workspace_active_branch": self.workspace_active_branch,
            "actual_git_branch": self.actual_git_branch,
            "current_run_values": self.current_run_values(),
            "stage_brief_boundary": self.stage_brief_boundary,
            "registry_has_current_run": self.registry_has_current_run,
            "stage_ledger_has_current_run": self.stage_ledger_has_current_run,
            "source_paths": dict(self.source_paths),
        }


def audit_state_sync(
    root: Path | str = Path("."),
    *,
    active_stage: str | None = None,
    current_branch: str | None = None,
) -> AuditResult:
    root_path = Path(root)
    snapshot = load_current_truth_snapshot(root_path, active_stage=active_stage, current_branch=current_branch)
    findings: list[AuditFinding] = []

    values = snapshot.current_run_values()
    grouped: dict[str, list[str]] = {}
    for source, value in values.items():
        grouped.setdefault(value, []).append(source)
    if len(grouped) > 1:
        findings.append(
            AuditFinding(
                check_id="current_run_conflict",
                message="Current run differs across current-truth documents.",
                details={"values": grouped},
            )
        )

    canonical_run = snapshot.workspace_current_run
    if canonical_run and not snapshot.registry_has_current_run:
        findings.append(
            AuditFinding(
                check_id="current_run_missing_from_run_registry",
                message="Workspace current run is not present in the run registry.",
                details={"current_run": canonical_run},
            )
        )
    if canonical_run and not snapshot.stage_ledger_has_current_run:
        findings.append(
            AuditFinding(
                check_id="current_run_missing_from_stage_ledger",
                message="Workspace current run is not present in the active stage ledger.",
                details={"current_run": canonical_run},
            )
        )

    if _brief_is_stale_python_only(snapshot.stage_brief_boundary, canonical_run):
        findings.append(
            AuditFinding(
                check_id="stage_brief_boundary_stale",
                message="Stage brief still describes the stage as Python-only while the current run is an MT5 runtime probe.",
                details={"current_run": canonical_run, "boundary": snapshot.stage_brief_boundary},
            )
        )
    if snapshot.workspace_active_branch and snapshot.actual_git_branch and snapshot.workspace_active_branch != snapshot.actual_git_branch:
        findings.append(
            AuditFinding(
                check_id="active_branch_mismatch",
                message="Workspace active_branch does not match the current git branch.",
                details={
                    "workspace_active_branch": snapshot.workspace_active_branch,
                    "actual_git_branch": snapshot.actual_git_branch,
                },
            )
        )

    status = "blocked" if any(finding.is_blocking for finding in findings) else "pass"
    return AuditResult(
        audit_name="state_sync_audit",
        status=status,
        findings=tuple(findings),
        counts=snapshot.to_counts(),
        allowed_claims=("current_truth_synced", "state_sync_completed") if status == "pass" else ("state_sync_findings_reported", "blocked"),
        forbidden_claims=() if status == "pass" else tuple(sorted(set(COMPLETION_CLAIMS).union(CURRENT_TRUTH_SYNC_CLAIMS))),
    )


def load_current_truth_snapshot(
    root: Path,
    *,
    active_stage: str | None = None,
    current_branch: str | None = None,
) -> CurrentTruthSnapshot:
    workspace_path = root / "docs/workspace/workspace_state.yaml"
    current_working_path = root / "docs/context/current_working_state.md"
    workspace = _load_yaml(workspace_path)
    stage_id = active_stage or str(workspace.get("active_stage", ""))
    stage_root = root / "stages" / stage_id
    selection_path = stage_root / "04_selected/selection_status.md"
    stage_brief_path = stage_root / "00_spec/stage_brief.md"
    stage_ledger_path = stage_root / "03_reviews/stage_run_ledger.csv"
    registry_path = root / "docs/registers/run_registry.csv"

    workspace_current_run = _current_run_from_workspace(workspace, stage_id)
    current_working_text = _read_text(current_working_path)
    selection_text = _read_text(selection_path)
    stage_brief_text = _read_text(stage_brief_path)
    current_working_run = _extract_current_run(current_working_text)
    selection_status_run = _extract_current_run(selection_text)
    registry_rows = read_csv_rows(registry_path)
    stage_rows = read_csv_rows(stage_ledger_path)

    return CurrentTruthSnapshot(
        active_stage=stage_id,
        workspace_active_branch=str(workspace.get("active_branch", "")),
        actual_git_branch=current_branch if current_branch is not None else _current_git_branch(root),
        workspace_current_run=workspace_current_run,
        current_working_run=current_working_run,
        selection_status_run=selection_status_run,
        stage_brief_boundary=_extract_boundary(stage_brief_text),
        registry_has_current_run=any(row.get("run_id") == workspace_current_run and row.get("stage_id") == stage_id for row in registry_rows),
        stage_ledger_has_current_run=any(row.get("run_id") == workspace_current_run and row.get("stage_id") == stage_id for row in stage_rows),
        source_paths={
            "workspace_state": workspace_path.as_posix(),
            "current_working_state": current_working_path.as_posix(),
            "selection_status": selection_path.as_posix(),
            "stage_brief": stage_brief_path.as_posix(),
            "run_registry": registry_path.as_posix(),
            "stage_ledger": stage_ledger_path.as_posix(),
        },
    )


def _load_yaml(path: Path) -> Mapping[str, Any]:
    if not path_exists(path):
        return {}
    payload = yaml.safe_load(io_path(path).read_text(encoding="utf-8-sig"))
    return payload if isinstance(payload, Mapping) else {}


def _read_text(path: Path) -> str:
    if not path_exists(path):
        return ""
    return io_path(path).read_text(encoding="utf-8-sig")


def _current_run_from_workspace(workspace: Mapping[str, Any], active_stage: str) -> str:
    for value in workspace.values():
        if isinstance(value, Mapping) and value.get("stage_id") == active_stage:
            run_id = value.get("current_run_id") or value.get("current_run")
            if run_id:
                return str(run_id)
    return str(workspace.get("current_run_id", ""))


def _current_git_branch(root: Path) -> str:
    try:
        completed = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    if completed.returncode != 0:
        return ""
    return completed.stdout.strip()


def _extract_current_run(text: str) -> str:
    preferred: list[str] = []
    fallback: list[str] = []
    for line in text.splitlines():
        lowered = line.lower()
        if "current run packet" in lowered or "현재 실행 묶음" in line:
            continue
        if "current run" not in lowered and "현재 실행" not in line and "현재 기준" not in line:
            continue
        matches = re.findall(r"`([^`]+)`", line)
        for value in matches:
            value = value.strip()
            if _looks_like_full_run_id(value):
                preferred.append(value)
            else:
                fallback.append(value)
    if preferred:
        return preferred[0]
    if fallback:
        return fallback[0]
    return ""


def _looks_like_full_run_id(value: str) -> bool:
    return bool(re.match(r"run\d+[A-Z]*_[a-z0-9_]+", value, flags=re.IGNORECASE))


def _extract_boundary(text: str) -> str:
    match = re.search(r"## 경계.*?(?=\n## |\Z)", text, flags=re.DOTALL)
    if match:
        return " ".join(match.group(0).split())
    return ""


def _brief_is_stale_python_only(boundary: str, current_run: str) -> bool:
    if not boundary or not current_run:
        return False
    runtime_like = ("mt5" in current_run.lower()) or ("run03f" in current_run.lower())
    python_only = "Python structural scout" in boundary and "만 주장" in boundary
    return runtime_like and python_only


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit current-truth state synchronization.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--active-stage")
    parser.add_argument("--current-branch")
    parser.add_argument("--output-json")
    parser.add_argument("--allow-blocked-exit-zero", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    result = audit_state_sync(Path(args.root), active_stage=args.active_stage, current_branch=args.current_branch)
    payload = result.to_dict()
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.output_json:
        output = Path(args.output_json)
        io_path(output.parent).mkdir(parents=True, exist_ok=True)
        io_path(output).write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if args.allow_blocked_exit_zero or result.status == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
