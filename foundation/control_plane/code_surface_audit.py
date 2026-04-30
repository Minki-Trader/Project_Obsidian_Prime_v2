from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Mapping

import yaml

from foundation.control_plane.audit_result import AuditFinding, AuditResult
from foundation.control_plane.ledger import io_path, path_exists


CODE_SUFFIXES = {".py", ".mq5", ".mqh"}
DEFAULT_SCAN_ROOTS = ("foundation", "stage_pipelines", "tests", "stages", ".agents/skills")
DEFAULT_BASELINE_PATH = Path("docs/agent_control/code_surface_baseline.yaml")
CONTROL_PLANE_STAGE_IMPORT_RE = re.compile(
    r"^\s*(?:from\s+foundation\.pipelines(?:\.run_stage\d+[\w_]*)?\s+import|"
    r"import\s+foundation\.pipelines\.run_stage\d+|"
    r"from\s+stage_pipelines(?:\.[\w_]+)*\s+import|"
    r"import\s+stage_pipelines(?:\.[\w_]+)+)",
    re.MULTILINE,
)
STAGE_RUNTIME_COMPAT_IMPORT_RE = re.compile(r"foundation\.pipelines.*run_stage10_logreg_mt5_scout")


def audit_code_surface(root: Path | str = Path("."), baseline_path: Path | str | None = None) -> AuditResult:
    root_path = Path(root)
    baseline = _load_baseline(root_path, baseline_path)
    line_policy = baseline.get("line_count_policy", {})
    attention_lines = int(line_policy.get("attention_lines", 800))
    blocking_lines = int(line_policy.get("blocking_lines", 1600))
    max_lines_by_path = _max_lines_by_path(line_policy)

    findings: list[AuditFinding] = []
    counts: dict[str, Any] = {
        "attention_lines": attention_lines,
        "blocking_lines": blocking_lines,
        "scanned_files": 0,
        "files_over_attention": 0,
    }

    for path in _iter_code_files(root_path):
        rel = path.relative_to(root_path).as_posix()
        text = io_path(path).read_text(encoding="utf-8-sig")
        line_count = _line_count(text)
        counts["scanned_files"] += 1
        counts[f"lines::{rel}"] = line_count

        baseline_max = max_lines_by_path.get(rel)
        if baseline_max is not None and line_count > baseline_max:
            findings.append(
                AuditFinding(
                    check_id=f"line_budget::{rel}",
                    message="Code file exceeds its registered line budget.",
                    details={"path": rel, "lines": line_count, "max_lines": baseline_max},
                )
            )
        elif baseline_max is None and line_count > blocking_lines:
            findings.append(
                AuditFinding(
                    check_id=f"line_budget::{rel}",
                    message="Large code file has no registered code-surface baseline.",
                    details={"path": rel, "lines": line_count, "blocking_lines": blocking_lines},
                )
            )
        elif line_count > attention_lines:
            counts["files_over_attention"] += 1
            findings.append(
                AuditFinding(
                    check_id=f"large_file::{rel}",
                    message="Large code file requires code-surface guard before future edits.",
                    severity="warning",
                    details={"path": rel, "lines": line_count, "attention_lines": attention_lines},
                )
            )

        _check_cross_owner_imports(rel, text, findings)

    status = "blocked" if any(finding.is_blocking for finding in findings) else "pass"
    return AuditResult(
        audit_name="code_surface_audit",
        status=status,
        findings=tuple(findings),
        counts=counts,
        allowed_claims=("code_surface_guarded",) if status == "pass" else ("blocked",),
        forbidden_claims=() if status == "pass" else ("code_surface_guarded",),
    )


def _load_baseline(root: Path, baseline_path: Path | str | None) -> Mapping[str, Any]:
    path = root / (Path(baseline_path) if baseline_path is not None else DEFAULT_BASELINE_PATH)
    if not path_exists(path):
        return {}
    payload = yaml.safe_load(io_path(path).read_text(encoding="utf-8-sig")) or {}
    if not isinstance(payload, Mapping):
        return {}
    return payload


def _max_lines_by_path(line_policy: Mapping[str, Any]) -> dict[str, int]:
    raw = line_policy.get("max_lines_by_path", {})
    if not isinstance(raw, Mapping):
        return {}
    budgets: dict[str, int] = {}
    for path, payload in raw.items():
        if isinstance(payload, Mapping):
            budgets[str(path)] = int(payload.get("max_lines", 0))
        else:
            budgets[str(path)] = int(payload)
    return budgets


def _iter_code_files(root: Path) -> list[Path]:
    paths: list[Path] = []
    for relative in DEFAULT_SCAN_ROOTS:
        scan_root = root / relative
        if not scan_root.exists():
            continue
        paths.extend(
            path
            for path in scan_root.rglob("*")
            if path.is_file()
            and path.suffix.lower() in CODE_SUFFIXES
            and "__pycache__" not in path.parts
        )
    return sorted(set(paths))


def _line_count(text: str) -> int:
    if not text:
        return 0
    return text.count("\n") + (0 if text.endswith("\n") else 1)


def _check_cross_owner_imports(rel: str, text: str, findings: list[AuditFinding]) -> None:
    if rel.startswith("foundation/control_plane/") and CONTROL_PLANE_STAGE_IMPORT_RE.search(text):
        findings.append(
            AuditFinding(
                check_id=f"cross_owner_import::{rel}",
                message="Control-plane code must not import stage pipeline modules directly.",
                details={"path": rel, "owner_module": "foundation/control_plane", "forbidden_owner": "foundation/pipelines/run_stage*"},
            )
        )
    if rel == "foundation/mt5/runtime_support.py" and STAGE_RUNTIME_COMPAT_IMPORT_RE.search(text):
        findings.append(
            AuditFinding(
                check_id="compatibility_shim::foundation/mt5/runtime_support.py",
                message="MT5 runtime support still delegates to the legacy Stage 10 orchestration file.",
                severity="warning",
                details={"path": rel, "next_refactor": "move shared runtime helpers into foundation/mt5 modules"},
            )
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit Project Obsidian code-surface size and owner boundaries.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--baseline", default=None)
    parser.add_argument("--output-json", default=None)
    args = parser.parse_args()

    result = audit_code_surface(Path(args.root), Path(args.baseline) if args.baseline else None)
    payload = result.to_dict()
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.output_json:
        output_path = Path(args.output_json)
        io_path(output_path.parent).mkdir(parents=True, exist_ok=True)
        io_path(output_path).write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if result.status == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
