from __future__ import annotations

import argparse
import csv
import glob
import json
import sys
from pathlib import Path
from typing import Any

from foundation.control_plane.kpi_contract_audit import KpiContract
from foundation.control_plane.ledger import io_path, path_exists
from foundation.control_plane.scope_completion_gate import ScopeCountCheck
from foundation.control_plane.skill_receipt_lint import SkillReceipt
from foundation.control_plane.skill_receipt_schema_lint import audit_skill_receipt_schemas, load_receipts
from foundation.control_plane.state_sync_audit import audit_state_sync
from foundation.control_plane.work_packet_gate import evaluate_work_packet_closeout
from foundation.control_plane.work_packet_schema_lint import audit_work_packet_schema_path


def _read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def _write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _csv_row_count(path: Path) -> int:
    if not path_exists(path):
        return 0
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def _glob_count(pattern: str) -> int:
    return len([path for path in glob.glob(pattern, recursive=True) if path_exists(Path(path))])


def _scope_checks_from_args(args: argparse.Namespace) -> list[ScopeCountCheck]:
    checks: list[ScopeCountCheck] = []
    for check_id, expected, path, label in args.scope_csv_rows:
        checks.append(
            ScopeCountCheck(
                check_id=check_id,
                expected_count=int(expected),
                actual_count=_csv_row_count(Path(path)),
                evidence_label=label,
            )
        )
    for check_id, expected, pattern, label in args.scope_file_count:
        checks.append(
            ScopeCountCheck(
                check_id=check_id,
                expected_count=int(expected),
                actual_count=_glob_count(pattern),
                evidence_label=label,
            )
        )
    for check_id, expected, actual, label in args.scope_count:
        checks.append(
            ScopeCountCheck(
                check_id=check_id,
                expected_count=int(expected),
                actual_count=int(actual),
                evidence_label=label,
            )
        )
    return checks


def _skill_receipts_from_args(args: argparse.Namespace) -> list[SkillReceipt]:
    if not args.skill_receipt_json:
        return []
    payload = _read_json(Path(args.skill_receipt_json))
    rows = payload.get("receipts", payload) if isinstance(payload, dict) else payload
    if not isinstance(rows, list):
        raise ValueError("skill receipt JSON must be a list or an object with a `receipts` list")
    return [SkillReceipt.from_mapping(row) for row in rows]


def _kpi_contract_from_args(args: argparse.Namespace) -> list[KpiContract]:
    if not args.kpi_run_id:
        return []
    required_files = tuple(args.required_kpi_file) if args.required_kpi_file else KpiContract(args.kpi_run_id).required_files
    return [
        KpiContract(
            run_id=args.kpi_run_id,
            stage_id=args.kpi_stage_id,
            run_root=Path(args.kpi_run_root) if args.kpi_run_root else None,
            required_files=required_files,
            stage_ledger_path=Path(args.stage_ledger) if args.stage_ledger else None,
            project_ledger_path=Path(args.project_ledger) if args.project_ledger else None,
            expected_stage_ledger_rows=args.expected_stage_ledger_rows,
            expected_project_ledger_rows=args.expected_project_ledger_rows,
        )
    ]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evaluate Project Obsidian work-packet closeout gates before final completion claims."
    )
    parser.add_argument("--packet-id", required=True)
    parser.add_argument("--requested-claim", action="append", default=[])
    parser.add_argument("--work-packet")
    parser.add_argument("--validate-work-packet-schema", action="store_true")
    parser.add_argument("--state-sync-audit", action="store_true")
    parser.add_argument(
        "--scope-csv-rows",
        action="append",
        nargs=4,
        metavar=("CHECK_ID", "EXPECTED", "CSV_PATH", "LABEL"),
        default=[],
        help="Compare expected count to data rows in a CSV file.",
    )
    parser.add_argument(
        "--scope-file-count",
        action="append",
        nargs=4,
        metavar=("CHECK_ID", "EXPECTED", "GLOB", "LABEL"),
        default=[],
        help="Compare expected count to files matching a glob pattern.",
    )
    parser.add_argument(
        "--scope-count",
        action="append",
        nargs=4,
        metavar=("CHECK_ID", "EXPECTED", "ACTUAL", "LABEL"),
        default=[],
        help="Compare expected count to an explicit actual count.",
    )
    parser.add_argument("--required-skill", action="append", default=[])
    parser.add_argument("--skill-receipt-json")
    parser.add_argument("--skill-receipt-schema")
    parser.add_argument("--kpi-run-id")
    parser.add_argument("--kpi-stage-id", default="")
    parser.add_argument("--kpi-run-root")
    parser.add_argument("--required-kpi-file", action="append", default=[])
    parser.add_argument("--stage-ledger")
    parser.add_argument("--project-ledger")
    parser.add_argument("--expected-stage-ledger-rows", type=int)
    parser.add_argument("--expected-project-ledger-rows", type=int)
    parser.add_argument("--output-json")
    parser.add_argument("--allow-blocked-exit-zero", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    claims = tuple(args.requested_claim or ("completed",))
    extra_audits = []
    if args.validate_work_packet_schema:
        if not args.work_packet:
            raise ValueError("--validate-work-packet-schema requires --work-packet")
        extra_audits.append(audit_work_packet_schema_path(Path(args.work_packet)))
    if args.state_sync_audit:
        extra_audits.append(audit_state_sync(Path(".")))
    if args.skill_receipt_schema:
        if not args.skill_receipt_json:
            raise ValueError("--skill-receipt-schema requires --skill-receipt-json")
        extra_audits.append(
            audit_skill_receipt_schemas(
                load_receipts(Path(args.skill_receipt_json)),
                schema_path=Path(args.skill_receipt_schema),
                root=Path("."),
                requested_claims=claims,
            )
        )
    report = evaluate_work_packet_closeout(
        packet_id=args.packet_id,
        requested_claims=claims,
        scope_checks=_scope_checks_from_args(args),
        required_skills=args.required_skill,
        skill_receipts=_skill_receipts_from_args(args),
        kpi_contracts=_kpi_contract_from_args(args),
        extra_audits=extra_audits,
    )
    payload = report.to_dict()
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.output_json:
        _write_json(Path(args.output_json), payload)
    print(text)
    if args.allow_blocked_exit_zero:
        return 0
    return 2 if report.completed_forbidden else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
