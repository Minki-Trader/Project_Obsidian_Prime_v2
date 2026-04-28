from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from foundation.control_plane.audit_result import COMPLETION_CLAIMS, AuditFinding, AuditResult
from foundation.control_plane.ledger import path_exists, read_csv_rows


@dataclass(frozen=True)
class KpiContract:
    run_id: str
    stage_id: str = ""
    run_root: Path | None = None
    required_files: tuple[str, ...] = ("run_manifest.json", "kpi_record.json", "summary.json", "reports/result_summary.md")
    stage_ledger_path: Path | None = None
    project_ledger_path: Path | None = None
    expected_stage_ledger_rows: int | None = None
    expected_project_ledger_rows: int | None = None


def _count_rows(path: Path | None, *, run_id: str, stage_id: str = "") -> tuple[int, bool]:
    if path is None:
        return 0, False
    if not path_exists(path):
        return 0, False
    rows = read_csv_rows(path)
    count = 0
    for row in rows:
        if row.get("run_id") != run_id:
            continue
        if stage_id and row.get("stage_id") != stage_id:
            continue
        count += 1
    return count, True


def audit_kpi_contract(contract: KpiContract) -> AuditResult:
    findings: list[AuditFinding] = []
    counts: dict[str, object] = {"run_id": contract.run_id, "stage_id": contract.stage_id}

    if contract.run_root is not None:
        missing_files = []
        for relative in contract.required_files:
            candidate = contract.run_root / relative
            exists = path_exists(candidate)
            counts[f"file::{relative}"] = {"path": candidate.as_posix(), "exists": exists}
            if not exists:
                missing_files.append(relative)
        if missing_files:
            findings.append(
                AuditFinding(
                    check_id="kpi_required_files",
                    message="Run is missing required identity/KPI/report files.",
                    details={"missing_files": missing_files},
                )
            )

    stage_rows, stage_ledger_exists = _count_rows(
        contract.stage_ledger_path, run_id=contract.run_id, stage_id=contract.stage_id
    )
    project_rows, project_ledger_exists = _count_rows(
        contract.project_ledger_path, run_id=contract.run_id, stage_id=contract.stage_id
    )
    counts["stage_ledger_rows"] = stage_rows
    counts["stage_ledger_exists"] = stage_ledger_exists
    counts["project_ledger_rows"] = project_rows
    counts["project_ledger_exists"] = project_ledger_exists

    _check_expected_rows(
        findings,
        check_id="stage_ledger_rows",
        expected=contract.expected_stage_ledger_rows,
        actual=stage_rows,
        ledger_exists=stage_ledger_exists,
    )
    _check_expected_rows(
        findings,
        check_id="project_ledger_rows",
        expected=contract.expected_project_ledger_rows,
        actual=project_rows,
        ledger_exists=project_ledger_exists,
    )

    status = "blocked" if any(finding.is_blocking for finding in findings) else "pass"
    return AuditResult(
        audit_name="kpi_contract_audit",
        status=status,
        findings=tuple(findings),
        counts=counts,
        allowed_claims=("completed", "reviewed") if status == "pass" else ("partial", "incomplete", "blocked"),
        forbidden_claims=() if status == "pass" else tuple(sorted(COMPLETION_CLAIMS)),
    )


def _check_expected_rows(
    findings: list[AuditFinding],
    *,
    check_id: str,
    expected: int | None,
    actual: int,
    ledger_exists: bool,
) -> None:
    if expected is None:
        return
    if not ledger_exists:
        findings.append(
            AuditFinding(
                check_id=check_id,
                message=f"Expected {expected} ledger rows, but the ledger file is missing.",
                details={"expected": expected, "actual": actual},
            )
        )
        return
    if actual < expected:
        findings.append(
            AuditFinding(
                check_id=check_id,
                message=f"Expected {expected} ledger rows, but found {actual}.",
                details={"expected": expected, "actual": actual},
            )
        )


def required_files_for_structural_scout(extra_files: Iterable[str] = ()) -> tuple[str, ...]:
    base = ("run_manifest.json", "kpi_record.json", "summary.json", "reports/result_summary.md")
    return tuple(dict.fromkeys((*base, *extra_files)))
