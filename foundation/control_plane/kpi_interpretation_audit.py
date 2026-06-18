from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

from foundation.control_plane.audit_result import COMPLETION_CLAIMS, AuditFinding, AuditResult
from foundation.control_plane.ledger import io_path, path_exists


ECONOMIC_METRIC_COLUMNS = (
    "net_profit",
    "profit_factor",
    "drawdown",
    "drawdown_percent",
    "max_drawdown_amount",
    "max_drawdown_percent",
    "recovery_factor",
    "trade_count",
    "long_trade_count",
    "short_trade_count",
    "trades_per_day",
    "selected_net_profit",
    "selected_profit_factor",
    "selected_trade_density",
    "expected_net_profit",
    "expected_profit_factor",
    "expected_trade_count",
    "expected_trade_density",
    "oos_net_profit",
    "oos_profit_factor",
    "oos_trade_count",
    "oos_drawdown_percent",
    "oos_trades_per_day",
)
ROW_IDENTITY_FIELDS = (
    "ledger_row_id",
    "run_id",
    "stage_id",
    "record_view",
    "tier_scope",
    "kpi_scope",
    "scoreboard_lane",
    "status",
    "judgment",
    "result_judgment",
    "external_verification_status",
)
MISSING_SCOPE_MARKERS = ("missing_required", "out_of_scope_by_claim")
ROUTED_TOTAL_MARKERS = (
    "actual_routed_total",
    "actual routed total",
    "routed_total",
    "runtime evidence",
    "stage_closeout",
    "closeout",
    "gap_analysis",
    "materialization",
)


def audit_kpi_interpretation_ledgers(paths: Sequence[Path | str]) -> AuditResult:
    findings: list[AuditFinding] = []
    counts = {
        "ledger_files": 0,
        "rows_checked": 0,
        "economic_rows": 0,
        "missing_scope_economic_rows": 0,
        "mixed_scope_warning_rows": 0,
    }

    for raw_path in paths:
        path = Path(raw_path)
        if not path_exists(path):
            findings.append(
                AuditFinding(
                    check_id="kpi_interpretation::ledger_missing",
                    message="KPI interpretation ledger path is missing.",
                    details={"path": path.as_posix()},
                )
            )
            continue
        counts["ledger_files"] += 1
        for line_number, row in _read_csv_rows(path):
            counts["rows_checked"] += 1
            economic_values = _economic_values(row)
            if economic_values:
                counts["economic_rows"] += 1
            identity_text = _identity_text(row)
            if economic_values and _is_direct_missing_scope_row(row):
                counts["missing_scope_economic_rows"] += 1
                findings.append(
                    AuditFinding(
                        check_id="kpi_interpretation::missing_or_out_of_scope_row_has_economic_metrics",
                        message="A missing_required/out_of_scope_by_claim row must not populate economic KPI columns.",
                        details={
                            "path": path.as_posix(),
                            "line": line_number,
                            "ledger_row_id": row.get("ledger_row_id", ""),
                            "run_id": row.get("run_id", ""),
                            "record_view": row.get("record_view", ""),
                            "tier_scope": row.get("tier_scope", ""),
                            "kpi_scope": row.get("kpi_scope", ""),
                            "economic_values": economic_values,
                        },
                    )
                )
            elif economic_values and _has_missing_scope_marker(identity_text) and not _has_routed_total_context(identity_text):
                counts["mixed_scope_warning_rows"] += 1
                findings.append(
                    AuditFinding(
                        check_id="kpi_interpretation::mixed_scope_economic_metrics_need_boundary",
                        message="A row mixes missing/out-of-scope tier language with economic KPI columns; it needs an explicit attribution boundary.",
                        severity="warning",
                        details={
                            "path": path.as_posix(),
                            "line": line_number,
                            "ledger_row_id": row.get("ledger_row_id", ""),
                            "run_id": row.get("run_id", ""),
                            "tier_scope": row.get("tier_scope", ""),
                            "kpi_scope": row.get("kpi_scope", ""),
                            "economic_values": economic_values,
                        },
                    )
                )
            if economic_values:
                _check_economic_row_context(path, line_number, row, findings)

    status = "blocked" if any(finding.is_blocking for finding in findings) else "pass"
    return AuditResult(
        audit_name="kpi_interpretation_audit",
        status=status,
        findings=tuple(findings),
        counts=counts,
        allowed_claims=("kpi_interpretation_consistent",) if status == "pass" else ("partial", "blocked"),
        forbidden_claims=() if status == "pass" else tuple(sorted(COMPLETION_CLAIMS)),
    )


def _check_economic_row_context(
    path: Path,
    line_number: int,
    row: Mapping[str, str],
    findings: list[AuditFinding],
) -> None:
    missing = [
        field
        for field in ("kpi_scope", "scoreboard_lane", "judgment", "external_verification_status")
        if not str(row.get(field, "")).strip()
    ]
    if missing:
        findings.append(
            AuditFinding(
                check_id="kpi_interpretation::economic_row_missing_context",
                message="Rows with economic KPI columns need KPI scope, scoreboard lane, judgment, and external verification status.",
                severity="warning",
                details={
                    "path": path.as_posix(),
                    "line": line_number,
                    "ledger_row_id": row.get("ledger_row_id", ""),
                    "run_id": row.get("run_id", ""),
                    "missing": missing,
                },
            )
        )


def _is_direct_missing_scope_row(row: Mapping[str, str]) -> bool:
    record_view = str(row.get("record_view", "")).lower()
    tier_scope = str(row.get("tier_scope", "")).lower()
    kpi_scope = str(row.get("kpi_scope", "")).lower()
    if _is_direct_missing_scope_field(kpi_scope):
        return True
    if _is_direct_missing_scope_field(record_view):
        return True
    if _is_direct_tier_scope_missing_row(tier_scope):
        return True
    return False


def _is_direct_missing_scope_field(value: str) -> bool:
    lowered = value.strip().lower()
    if not lowered or _has_routed_total_context(lowered):
        return False
    return lowered.startswith(MISSING_SCOPE_MARKERS)


def _is_direct_tier_scope_missing_row(value: str) -> bool:
    lowered = value.strip().lower()
    if not lowered or _has_routed_total_context(lowered):
        return False
    if ";" in lowered or " unless " in lowered:
        return False
    return (
        ("missing_required" in lowered and lowered.startswith(("tier b", "tier_b")))
        or ("out_of_scope_by_claim" in lowered and lowered.startswith(("tier a+b", "tier_ab", "combined")))
    )


def _has_missing_scope_marker(text: str) -> bool:
    lowered = text.lower()
    return any(marker in lowered for marker in MISSING_SCOPE_MARKERS)


def _has_routed_total_context(text: str) -> bool:
    lowered = text.lower()
    return any(marker in lowered for marker in ROUTED_TOTAL_MARKERS)


def _economic_values(row: Mapping[str, str]) -> dict[str, str]:
    values: dict[str, str] = {}
    for field in ECONOMIC_METRIC_COLUMNS:
        value = str(row.get(field, "")).strip()
        if value and value.upper() not in {"NA", "N/A", "NONE", "NULL"}:
            values[field] = value
    return values


def _identity_text(row: Mapping[str, str]) -> str:
    return "\n".join(str(row.get(field, "")) for field in ROW_IDENTITY_FIELDS).lower()


def _read_csv_rows(path: Path) -> list[tuple[int, dict[str, str]]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [(index, dict(row)) for index, row in enumerate(csv.DictReader(handle), start=2)]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit KPI/PnL/trade interpretation ledger boundaries.")
    parser.add_argument("ledger_paths", nargs="+")
    parser.add_argument("--output-json")
    parser.add_argument("--allow-blocked-exit-zero", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    result = audit_kpi_interpretation_ledgers([Path(path) for path in args.ledger_paths])
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
