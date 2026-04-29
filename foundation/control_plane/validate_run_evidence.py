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
    derive_run_roots_from_records: bool = False,
    require_stage_and_project_ledger_counterparts: bool = False,
    require_completed_mt5_report_parse: bool = False,
    require_mt5_identity: bool = False,
    work_packet_paths: Sequence[Path | str] = (),
    require_skill_receipts: bool = False,
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
    stage_ledger_keys, project_ledger_keys = _load_ledger_key_sets(root_path, stage_ledger_paths, project_ledger_path)
    ledger_keys = stage_ledger_keys | project_ledger_keys
    ledger_check_requested = bool(stage_ledger_paths or project_ledger_path)
    counts["ledger_rows_loaded"] = len(ledger_keys)

    for run_root in run_roots:
        _check_run_root(root_path / Path(run_root), findings)

    if require_skill_receipts:
        _check_skill_receipts(root_path, work_packet_paths, findings)

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
                    stage_ledger_keys=stage_ledger_keys,
                    project_ledger_keys=project_ledger_keys,
                    ledger_check_requested=ledger_check_requested,
                    require_stage_and_project=require_stage_and_project_ledger_counterparts,
                    record_index=record_index,
                )
                if derive_run_roots_from_records:
                    _check_derived_run_root(root_path, record, findings, record_index=record_index)
                if require_completed_mt5_report_parse:
                    _check_mt5_report_parse_status(record, findings, record_index=record_index)
                if require_mt5_identity:
                    _check_mt5_identity(root_path, record, findings, record_index=record_index)

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
    stage_keys, project_keys = _load_ledger_key_sets(root, stage_ledger_paths, project_ledger_path)
    return stage_keys | project_keys


def _load_ledger_key_sets(
    root: Path,
    stage_ledger_paths: Sequence[Path | str],
    project_ledger_path: Path | str | None,
) -> tuple[set[tuple[str, str]], set[tuple[str, str]]]:
    stage_keys: set[tuple[str, str]] = set()
    project_keys: set[tuple[str, str]] = set()
    for raw_path in [Path(path) for path in stage_ledger_paths]:
        stage_keys.update(_ledger_keys_from_path(root / raw_path))
    if project_ledger_path is not None:
        project_keys.update(_ledger_keys_from_path(root / Path(project_ledger_path)))
    return stage_keys, project_keys


def _ledger_keys_from_path(path: Path) -> set[tuple[str, str]]:
    keys: set[tuple[str, str]] = set()
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
    stage_ledger_keys: set[tuple[str, str]] | None = None,
    project_ledger_keys: set[tuple[str, str]] | None = None,
    ledger_check_requested: bool,
    require_stage_and_project: bool = False,
    record_index: int,
) -> None:
    if not ledger_check_requested:
        return
    row_grain = record.get("row_grain", {})
    if not isinstance(row_grain, Mapping):
        return
    run_id = _cell_value(row_grain, "run_id")
    record_view = _cell_value(row_grain, "record_view")
    if not str(record_view).startswith("mt5_"):
        return
    key = (str(run_id), str(record_view))
    if require_stage_and_project:
        if key not in (stage_ledger_keys or set()):
            findings.append(
                AuditFinding(
                    check_id="ledger::missing_stage_counterpart",
                    message="A normalized MT5 KPI row has no matching stage ledger row.",
                    details={"record_index": record_index, "run_id": str(run_id), "record_view": str(record_view)},
                )
            )
        if key not in (project_ledger_keys or set()):
            findings.append(
                AuditFinding(
                    check_id="ledger::missing_project_counterpart",
                    message="A normalized MT5 KPI row has no matching project ledger row.",
                    details={"record_index": record_index, "run_id": str(run_id), "record_view": str(record_view)},
                )
            )
        return
    if key not in ledger_keys:
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


def _check_derived_run_root(
    root: Path,
    record: Mapping[str, Any],
    findings: list[AuditFinding],
    *,
    record_index: int,
) -> None:
    source = record.get("source_evidence", {})
    kpi_record_path = source.get("kpi_record_path") if isinstance(source, Mapping) else None
    if not kpi_record_path:
        return
    run_root = _resolve_path(root, str(kpi_record_path)).parent
    for relative in ("run_manifest.json", "kpi_record.json", "reports/result_summary.md"):
        if not path_exists(run_root / relative):
            findings.append(
                AuditFinding(
                    check_id="run_root::missing_required_file",
                    message="Record-derived run root is missing a required evidence file.",
                    details={"record_index": record_index, "run_root": run_root.as_posix(), "missing_file": relative},
                )
            )


def _check_mt5_report_parse_status(
    record: Mapping[str, Any],
    findings: list[AuditFinding],
    *,
    record_index: int,
) -> None:
    row_grain = record.get("row_grain", {})
    if not isinstance(row_grain, Mapping):
        return
    record_view = str(_cell_value(row_grain, "record_view") or "")
    route_role = str(_cell_value(row_grain, "route_role") or "")
    if not record_view.startswith("mt5_"):
        return
    source = record.get("source_evidence", {})
    source = source if isinstance(source, Mapping) else {}
    parse_status = source.get("mt5_report_parse_status")
    if route_role in {"routed_total", "tier_only_total", "tier_b_fallback_only_total"}:
        if parse_status != "completed":
            findings.append(
                AuditFinding(
                    check_id="mt5_report_parse::partial_required_metrics",
                    message="MT5 trading total row requires a completed Strategy Tester report parse.",
                    details={
                        "record_index": record_index,
                        "record_view": record_view,
                        "route_role": route_role,
                        "parse_status": parse_status,
                        "missing_required_metrics": source.get("mt5_report_missing_required_metrics", []),
                    },
                )
            )
    elif route_role in {"primary_used", "fallback_used"}:
        if not parse_status or not source.get("mt5_report_path"):
            findings.append(
                AuditFinding(
                    check_id="mt5_report_parse::component_missing_source_report_status",
                    message="MT5 routed component row must preserve source report path and parse status.",
                    details={"record_index": record_index, "record_view": record_view, "route_role": route_role},
                )
            )


def _check_mt5_identity(
    root: Path,
    record: Mapping[str, Any],
    findings: list[AuditFinding],
    *,
    record_index: int,
) -> None:
    row_grain = record.get("row_grain", {})
    if not isinstance(row_grain, Mapping):
        return
    record_view = str(_cell_value(row_grain, "record_view") or "")
    route_role = str(_cell_value(row_grain, "route_role") or "")
    if not record_view.startswith("mt5_") or route_role not in {"routed_total", "tier_only_total", "tier_b_fallback_only_total"}:
        return
    source = record.get("source_evidence", {})
    source = source if isinstance(source, Mapping) else {}
    if not source.get("mt5_report_sha256"):
        findings.append(
            AuditFinding(
                check_id="mt5_identity::missing_report_hash",
                message="MT5 total row is missing report sha256 lineage.",
                details={"record_index": record_index, "record_view": record_view},
            )
        )
    kpi_record_path = source.get("kpi_record_path")
    if not kpi_record_path:
        findings.append(
            AuditFinding(
                check_id="mt5_identity::missing_kpi_record_path",
                message="MT5 total row is missing kpi_record path lineage.",
                details={"record_index": record_index, "record_view": record_view},
            )
        )
        return
    run_root = _resolve_path(root, str(kpi_record_path)).parent
    if not path_exists(run_root / "run_manifest.json"):
        findings.append(
            AuditFinding(
                check_id="mt5_identity::missing_manifest_for_mt5_run",
                message="MT5 total row has no run_manifest.json next to its kpi_record.",
                details={"record_index": record_index, "record_view": record_view, "run_root": run_root.as_posix()},
            )
        )


def _check_skill_receipts(
    root: Path,
    work_packet_paths: Sequence[Path | str],
    findings: list[AuditFinding],
) -> None:
    for raw_path in work_packet_paths:
        packet_path = _resolve_path(root, str(raw_path))
        if not path_exists(packet_path):
            findings.append(
                AuditFinding(
                    check_id="skill_receipt::missing_work_packet",
                    message="Work packet file is missing.",
                    details={"path": Path(raw_path).as_posix()},
                )
            )
            continue
        payload = yaml.safe_load(io_path(packet_path).read_text(encoding="utf-8-sig")) or {}
        required = []
        if isinstance(payload, Mapping):
            required.extend(payload.get("required_skill_receipts", []) or [])
            skill_routing = payload.get("skill_routing", {})
            if isinstance(skill_routing, Mapping):
                required.extend(skill_routing.get("required_skill_receipts", []) or [])
        for receipt in required:
            receipt_path = _resolve_path(root, str(receipt), base=packet_path.parent)
            if not path_exists(receipt_path):
                findings.append(
                    AuditFinding(
                        check_id="skill_receipt::missing_required_receipt",
                        message="Required skill receipt path is missing.",
                        details={"work_packet": packet_path.as_posix(), "receipt": str(receipt)},
                    )
                )


def _resolve_path(root: Path, raw_path: str, *, base: Path | None = None) -> Path:
    path = Path(raw_path)
    if path.is_absolute():
        return path
    primary = root / path
    if path_exists(primary):
        return primary
    if base is not None:
        return base / path
    return primary


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
    parser.add_argument("--derive-run-roots-from-records", action="store_true")
    parser.add_argument("--require-stage-and-project-ledger-counterparts", action="store_true")
    parser.add_argument("--require-completed-mt5-report-parse", action="store_true")
    parser.add_argument("--require-mt5-identity", action="store_true")
    parser.add_argument("--work-packet", action="append", default=[])
    parser.add_argument("--require-skill-receipts", action="store_true")
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
        derive_run_roots_from_records=args.derive_run_roots_from_records,
        require_stage_and_project_ledger_counterparts=args.require_stage_and_project_ledger_counterparts,
        require_completed_mt5_report_parse=args.require_completed_mt5_report_parse,
        require_mt5_identity=args.require_mt5_identity,
        work_packet_paths=[Path(path) for path in args.work_packet],
        require_skill_receipts=args.require_skill_receipts,
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
