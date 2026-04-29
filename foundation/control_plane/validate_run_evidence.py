from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import yaml

from foundation.control_plane.audit_result import COMPLETION_CLAIMS, AuditFinding, AuditResult
from foundation.control_plane.ledger import io_path, path_exists, read_csv_rows


DEFAULT_N_A_REGISTRY = Path("docs/agent_control/n_a_reason_registry.yaml")
DEFAULT_ROW_GRAIN_CONTRACT = Path("docs/agent_control/row_grain_contract.yaml")


def audit_run_evidence(
    *,
    root: Path | str = Path("."),
    normalized_jsonl_paths: Sequence[Path | str] = (),
    enriched_jsonl_paths: Sequence[Path | str] = (),
    stage_ledger_paths: Sequence[Path | str] = (),
    project_ledger_path: Path | str | None = None,
    n_a_registry_path: Path | str = DEFAULT_N_A_REGISTRY,
    row_grain_contract_path: Path | str = DEFAULT_ROW_GRAIN_CONTRACT,
    run_roots: Sequence[Path | str] = (),
) -> AuditResult:
    root_path = Path(root)
    findings: list[AuditFinding] = []
    counts: dict[str, Any] = {
        "normalized_records": 0,
        "enriched_records": 0,
        "n_a_cells_checked": 0,
        "row_grain_cells_checked": 0,
        "ledger_rows_loaded": 0,
    }

    allowed_reasons = _load_allowed_reasons(root_path / Path(n_a_registry_path))
    row_grain_allowed = _load_row_grain_allowed(root_path / Path(row_grain_contract_path))
    ledger_keys = _load_ledger_keys(root_path, stage_ledger_paths, project_ledger_path)
    ledger_check_requested = bool(stage_ledger_paths or project_ledger_path)
    counts["ledger_rows_loaded"] = len(ledger_keys)

    for run_root in run_roots:
        _check_run_root(root_path / Path(run_root), findings)

    normalized_records = _read_jsonl_records(root_path, normalized_jsonl_paths, findings, "normalized")
    enriched_records = _read_jsonl_records(root_path, enriched_jsonl_paths, findings, "enriched")
    counts["normalized_records"] = len(normalized_records)
    counts["enriched_records"] = len(enriched_records)

    for source_name, records in (("normalized", normalized_records), ("enriched", enriched_records)):
        for record_index, record in enumerate(records, start=1):
            _check_n_a_cells(
                record,
                findings,
                allowed_reasons=allowed_reasons,
                source_name=source_name,
                record_index=record_index,
                counts=counts,
            )
            if source_name == "normalized":
                _check_row_grain(
                    record,
                    findings,
                    allowed_values=row_grain_allowed,
                    record_index=record_index,
                    counts=counts,
                )
                _check_ledger_counterpart(
                    record,
                    findings,
                    ledger_keys=ledger_keys,
                    ledger_check_requested=ledger_check_requested,
                    record_index=record_index,
                )

    status = "blocked" if any(finding.is_blocking for finding in findings) else "pass"
    return AuditResult(
        audit_name="run_evidence_validator",
        status=status,
        findings=tuple(findings),
        counts=counts,
        allowed_claims=("evidence_records_consistent",) if status == "pass" else ("partial", "blocked"),
        forbidden_claims=() if status == "pass" else tuple(sorted(COMPLETION_CLAIMS)),
    )


def _load_allowed_reasons(path: Path) -> set[str]:
    payload = yaml.safe_load(io_path(path).read_text(encoding="utf-8-sig"))
    allowed = payload.get("allowed_reasons", {}) if isinstance(payload, Mapping) else {}
    return {str(key) for key in allowed}


def _load_row_grain_allowed(path: Path) -> dict[str, set[str]]:
    payload = yaml.safe_load(io_path(path).read_text(encoding="utf-8-sig"))
    allowed = payload.get("allowed_values", {}) if isinstance(payload, Mapping) else {}
    return {str(key): {str(item) for item in values or ()} for key, values in allowed.items()}


def _read_jsonl_records(
    root: Path,
    paths: Sequence[Path | str],
    findings: list[AuditFinding],
    source_name: str,
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for raw_path in paths:
        path = root / Path(raw_path)
        if not path_exists(path):
            findings.append(
                AuditFinding(
                    check_id=f"{source_name}_jsonl::missing",
                    message="Evidence JSONL file is missing.",
                    details={"path": Path(raw_path).as_posix()},
                )
            )
            continue
        for line_index, line in enumerate(io_path(path).read_text(encoding="utf-8-sig").splitlines(), start=1):
            if not line.strip():
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError as exc:
                findings.append(
                    AuditFinding(
                        check_id=f"{source_name}_jsonl::parse_error",
                        message="Evidence JSONL line could not be parsed.",
                        details={"path": Path(raw_path).as_posix(), "line": line_index, "error": str(exc)},
                    )
                )
                continue
            if isinstance(payload, dict):
                records.append(payload)
    return records


def _iter_cells(value: Any, path: tuple[str, ...] = ()) -> Iterable[tuple[tuple[str, ...], Mapping[str, Any]]]:
    if isinstance(value, Mapping):
        if "value" in value and "n/a_reason" in value:
            yield path, value
            return
        for key, item in value.items():
            yield from _iter_cells(item, (*path, str(key)))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from _iter_cells(item, (*path, str(index)))


def _check_n_a_cells(
    record: Mapping[str, Any],
    findings: list[AuditFinding],
    *,
    allowed_reasons: set[str],
    source_name: str,
    record_index: int,
    counts: dict[str, Any],
) -> None:
    for cell_path, cell in _iter_cells(record):
        counts["n_a_cells_checked"] += 1
        reason = cell.get("n/a_reason")
        value = cell.get("value")
        if reason not in (None, "") and str(reason) not in allowed_reasons:
            findings.append(
                AuditFinding(
                    check_id="n_a_reason::unregistered",
                    message="A KPI cell uses an n/a_reason not present in the registry.",
                    details={
                        "source": source_name,
                        "record_index": record_index,
                        "cell_path": ".".join(cell_path),
                        "n_a_reason": str(reason),
                    },
                )
            )
        if value is None and reason in (None, ""):
            findings.append(
                AuditFinding(
                    check_id="n_a_reason::missing_for_null",
                    message="A KPI cell has null value without an n/a_reason.",
                    details={"source": source_name, "record_index": record_index, "cell_path": ".".join(cell_path)},
                )
            )
        if value is not None and reason not in (None, ""):
            findings.append(
                AuditFinding(
                    check_id="n_a_reason::present_with_value",
                    message="A KPI cell has a value and an n/a_reason at the same time.",
                    details={"source": source_name, "record_index": record_index, "cell_path": ".".join(cell_path)},
                )
            )


def _check_row_grain(
    record: Mapping[str, Any],
    findings: list[AuditFinding],
    *,
    allowed_values: Mapping[str, set[str]],
    record_index: int,
    counts: dict[str, Any],
) -> None:
    row_grain = record.get("row_grain", {})
    if not isinstance(row_grain, Mapping):
        findings.append(
            AuditFinding(
                check_id="row_grain::missing",
                message="Normalized KPI record is missing row_grain.",
                details={"record_index": record_index},
            )
        )
        return
    for field, allowed in allowed_values.items():
        cell = row_grain.get(field)
        value = cell.get("value") if isinstance(cell, Mapping) else None
        counts["row_grain_cells_checked"] += 1
        if value is None:
            continue
        if str(value) not in allowed:
            findings.append(
                AuditFinding(
                    check_id="row_grain::value_not_allowed",
                    message="A row_grain value is not allowed by row_grain_contract.",
                    details={"record_index": record_index, "field": field, "value": str(value)},
                )
            )


def _load_ledger_keys(
    root: Path,
    stage_ledger_paths: Sequence[Path | str],
    project_ledger_path: Path | str | None,
) -> set[tuple[str, str]]:
    keys: set[tuple[str, str]] = set()
    paths = [Path(path) for path in stage_ledger_paths]
    if project_ledger_path is not None:
        paths.append(Path(project_ledger_path))
    for raw_path in paths:
        path = root / raw_path
        for row in read_csv_rows(path):
            run_id = str(row.get("run_id", "")).strip()
            record_view = str(row.get("record_view", "")).strip()
            if run_id and record_view:
                keys.add((run_id, record_view))
    return keys


def _check_ledger_counterpart(
    record: Mapping[str, Any],
    findings: list[AuditFinding],
    *,
    ledger_keys: set[tuple[str, str]],
    ledger_check_requested: bool,
    record_index: int,
) -> None:
    if not ledger_check_requested:
        return
    row_grain = record.get("row_grain", {})
    if not isinstance(row_grain, Mapping):
        return
    run_id = _cell_value(row_grain, "run_id")
    record_view = _cell_value(row_grain, "record_view")
    if str(record_view).startswith("mt5_") and (str(run_id), str(record_view)) not in ledger_keys:
        findings.append(
            AuditFinding(
                check_id="ledger::missing_counterpart",
                message="A normalized MT5 KPI row has no matching alpha ledger row.",
                details={"record_index": record_index, "run_id": str(run_id), "record_view": str(record_view)},
            )
        )


def _check_run_root(run_root: Path, findings: list[AuditFinding]) -> None:
    for relative in ("run_manifest.json", "kpi_record.json", "reports/result_summary.md"):
        if not path_exists(run_root / relative):
            findings.append(
                AuditFinding(
                    check_id="run_root::missing_required_file",
                    message="Run root is missing a required evidence file.",
                    details={"run_root": run_root.as_posix(), "missing_file": relative},
                )
            )


def _cell_value(section: Mapping[str, Any], field: str) -> Any:
    cell = section.get(field, {})
    return cell.get("value") if isinstance(cell, Mapping) else None


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate normalized run evidence records against KPI contracts.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--normalized-jsonl", action="append", default=[])
    parser.add_argument("--enriched-jsonl", action="append", default=[])
    parser.add_argument("--stage-ledger", action="append", default=[])
    parser.add_argument("--project-ledger")
    parser.add_argument("--n-a-registry", default=DEFAULT_N_A_REGISTRY.as_posix())
    parser.add_argument("--row-grain-contract", default=DEFAULT_ROW_GRAIN_CONTRACT.as_posix())
    parser.add_argument("--run-root", action="append", default=[])
    parser.add_argument("--output-json")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    result = audit_run_evidence(
        root=Path(args.root),
        normalized_jsonl_paths=[Path(path) for path in args.normalized_jsonl],
        enriched_jsonl_paths=[Path(path) for path in args.enriched_jsonl],
        stage_ledger_paths=[Path(path) for path in args.stage_ledger],
        project_ledger_path=Path(args.project_ledger) if args.project_ledger else None,
        n_a_registry_path=Path(args.n_a_registry),
        row_grain_contract_path=Path(args.row_grain_contract),
        run_roots=[Path(path) for path in args.run_root],
    )
    payload = result.to_dict()
    text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.output_json:
        out_path = Path(args.output_json)
        io_path(out_path.parent).mkdir(parents=True, exist_ok=True)
        io_path(out_path).write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0 if result.status == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
