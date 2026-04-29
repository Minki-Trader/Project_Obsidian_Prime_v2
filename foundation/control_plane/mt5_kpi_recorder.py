from __future__ import annotations

import argparse
import json
import os
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml

from foundation.control_plane.ledger import io_path, path_exists, read_csv_rows, sha256_file_lf_normalized, write_csv_rows
from foundation.mt5.strategy_report import extract_mt5_strategy_report_metrics


PACKET_ID_DEFAULT = "kpi_rebuild_mt5_recording_v1"
INVENTORY_PACKET_ID = "kpi_rebuild_inventory_v1"
CONFIRMED_INVENTORY_PATH = Path("docs/agent_control/packets/kpi_rebuild_inventory_v1/experiment_inventory.csv")
TARGET_CONFIRMATION_PATH = Path("docs/agent_control/packets/kpi_rebuild_inventory_v1/target_confirmation.yaml")
NORMALIZED_TEMPLATE_PATH = Path("docs/templates/kpi_record_normalized.template.json")

SUMMARY_COLUMNS = (
    "run_id",
    "stage_id",
    "record_view",
    "split",
    "tier_scope",
    "route_role",
    "report_path",
    "report_sha256",
    "net_profit",
    "profit_factor",
    "trade_count",
    "max_drawdown_amount",
    "status",
)

HEADLINE_MAP = {
    "net_profit": "net_profit",
    "gross_profit": "gross_profit",
    "gross_loss": "gross_loss",
    "profit_factor": "profit_factor",
    "expectancy": "expectancy",
    "trade_count": "trade_count",
    "win_rate": "win_rate_percent",
    "recovery_factor": "recovery_factor",
    "sharpe_ratio": "sharpe_ratio",
}

RISK_MAP = {
    "max_drawdown_amount": "max_drawdown_amount",
    "max_drawdown_percent": "max_drawdown_percent",
    "equity_drawdown_amount": "equity_drawdown_maximal_amount",
    "equity_drawdown_percent": "equity_drawdown_maximal_percent",
}

EXECUTION_MAP = {
    "order_attempt_count": "order_attempt_count",
    "order_fill_count": ("fill_count", "order_fill_count"),
    "fill_rate": "fill_rate",
    "reject_count": "reject_count",
    "skip_count": ("skip_count", "feature_skip_count"),
    "model_fail_count": "model_fail_count",
    "feature_ready_count": "feature_ready_count",
}


def build_mt5_kpi_recording_packet(
    root: Path | str = Path("."),
    *,
    packet_id: str = PACKET_ID_DEFAULT,
    created_at_utc: str | None = None,
) -> dict[str, Any]:
    root_path = Path(root)
    created_at = created_at_utc or _utc_now()
    target_selection = _target_inventory_selection(root_path)
    inventory_rows = target_selection["rows"]
    records, summary_rows, missing_runs, parser_errors = build_normalized_records(root_path, inventory_rows)
    summary = _build_summary(
        root_path,
        packet_id=packet_id,
        created_at_utc=created_at,
        inventory_rows=inventory_rows,
        records=records,
        missing_runs=missing_runs,
        parser_errors=parser_errors,
        target_confirmation=target_selection,
    )
    return {
        "records": records,
        "summary_rows": summary_rows,
        "summary": summary,
        "work_packet": _build_work_packet(packet_id=packet_id, created_at_utc=created_at, summary=summary),
        "run_plan": _build_run_plan(packet_id=packet_id, created_at_utc=created_at, summary=summary),
        "receipts": _build_receipts(packet_id=packet_id, created_at_utc=created_at, summary=summary),
    }


def build_normalized_records(
    root: Path,
    inventory_rows: Sequence[Mapping[str, str]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    template = _load_template(root)
    records: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []
    missing_runs: list[dict[str, Any]] = []
    parser_errors: list[dict[str, Any]] = []

    for run_row in inventory_rows:
        run_id = str(run_row.get("run_id", ""))
        run_root = root / str(run_row.get("path", ""))
        kpi_path = run_root / "kpi_record.json"
        if not path_exists(kpi_path):
            missing_runs.append(_missing_run(run_row, "source_artifact_missing", "kpi_record.json missing"))
            continue
        kpi_payload = _load_json(kpi_path)
        mt5_records = _mt5_records_from_kpi(root, run_row, kpi_payload, parser_errors=parser_errors)
        if not mt5_records:
            missing_runs.append(_missing_run(run_row, "mt5_report_missing", "no mt5_records, mt5.kpi_records, or report files"))
            continue

        run_record_count = 0
        for mt5_record in mt5_records:
            report_path = _report_path(root, mt5_record)
            if report_path is None or not path_exists(report_path):
                parser_errors.append(
                    {
                        "run_id": run_id,
                        "record_view": mt5_record.get("record_view"),
                        "error": "mt5_report_missing",
                        "path": "" if report_path is None else report_path.as_posix(),
                    }
                )
                continue
            try:
                parsed_metrics = extract_mt5_strategy_report_metrics(report_path)
            except Exception as exc:  # pragma: no cover - defensive path for malformed real reports
                parser_errors.append(
                    {
                        "run_id": run_id,
                        "record_view": mt5_record.get("record_view"),
                        "error": str(exc),
                        "path": report_path.as_posix(),
                    }
                )
                continue
            merged_metrics = dict(parsed_metrics)
            if isinstance(mt5_record.get("metrics"), Mapping):
                merged_metrics = _merge_metrics(parsed_metrics, mt5_record)
            normalized = _normalized_record(
                template,
                run_row=run_row,
                kpi_payload=kpi_payload,
                kpi_path=kpi_path,
                mt5_record=mt5_record,
                report_path=report_path,
                metrics=merged_metrics,
                parsed_metrics=parsed_metrics,
            )
            records.append(normalized)
            summary_rows.append(_summary_row(normalized, report_path))
            run_record_count += 1
        if run_record_count == 0:
            missing_runs.append(_missing_run(run_row, "mt5_report_missing", "no parseable mt5 report"))
    return records, summary_rows, missing_runs, parser_errors


def write_mt5_kpi_recording_packet(
    root: Path | str = Path("."),
    *,
    packet_id: str = PACKET_ID_DEFAULT,
    output_dir: Path | str | None = None,
    created_at_utc: str | None = None,
) -> dict[str, Any]:
    root_path = Path(root)
    packet = build_mt5_kpi_recording_packet(root_path, packet_id=packet_id, created_at_utc=created_at_utc)
    out_dir = Path(output_dir) if output_dir is not None else root_path / "docs/agent_control/packets" / packet_id
    if not out_dir.is_absolute():
        out_dir = root_path / out_dir
    io_path(out_dir / "skill_receipts").mkdir(parents=True, exist_ok=True)

    _write_jsonl(out_dir / "normalized_kpi_records.jsonl", packet["records"])
    write_csv_rows(out_dir / "normalized_kpi_summary.csv", SUMMARY_COLUMNS, packet["summary_rows"])
    _write_json(out_dir / "recording_summary.json", packet["summary"])
    _write_yaml(out_dir / "work_packet.yaml", packet["work_packet"])
    _write_yaml(out_dir / "run_plan.yaml", packet["run_plan"])
    for name, receipt in packet["receipts"].items():
        _write_yaml(out_dir / "skill_receipts" / f"{name}.yaml", receipt)
    return packet


def _target_inventory_rows(root: Path) -> list[dict[str, str]]:
    return _target_inventory_selection(root)["rows"]


def _target_inventory_selection(root: Path) -> dict[str, Any]:
    rows = read_csv_rows(root / CONFIRMED_INVENTORY_PATH)
    default_rows = [row for row in rows if str(row.get("default_rework_target", "")).lower() in {"1", "true"}]
    confirmation_path = root / TARGET_CONFIRMATION_PATH
    if not path_exists(confirmation_path):
        return {
            "rows": default_rows,
            "status": "missing_fallback_inventory_only",
            "findings": [{"check_id": "target_confirmation_missing", "severity": "warning"}],
            "expected_target_rows": None,
            "excluded_run_ids": [],
            "selected_target_rows": len(default_rows),
        }

    confirmation = yaml.safe_load(io_path(confirmation_path).read_text(encoding="utf-8-sig")) or {}
    interpretation = confirmation.get("interpretation", {}) if isinstance(confirmation, Mapping) else {}
    scope = confirmation.get("next_packet_scope", {}) if isinstance(confirmation, Mapping) else {}
    expected = interpretation.get("kpi_rebuild_default_target_rows") if isinstance(interpretation, Mapping) else None
    excluded = {
        str(run_id)
        for run_id in (interpretation.get("excluded_run_ids", []) if isinstance(interpretation, Mapping) else [])
        if str(run_id)
    }
    do_not_rerun_invalid = bool(scope.get("do_not_rerun_invalid_reference")) if isinstance(scope, Mapping) else False
    excluded_selected = [row for row in default_rows if str(row.get("run_id", "")) in excluded]
    selected = [row for row in default_rows if str(row.get("run_id", "")) not in excluded]

    findings: list[dict[str, Any]] = []
    status = "confirmed"
    if expected is not None and int(expected) != len(selected):
        status = "blocked"
        findings.append(
            {
                "check_id": "target_confirmation_mismatch",
                "expected_target_rows": int(expected),
                "selected_target_rows": len(selected),
            }
        )
    if excluded_selected:
        status = "blocked" if do_not_rerun_invalid else status
        findings.append(
            {
                "check_id": "target_confirmation_excluded_run_selected",
                "excluded_run_ids": [str(row.get("run_id", "")) for row in excluded_selected],
                "do_not_rerun_invalid_reference": do_not_rerun_invalid,
            }
        )
    return {
        "rows": selected,
        "status": status,
        "findings": findings,
        "expected_target_rows": None if expected is None else int(expected),
        "excluded_run_ids": sorted(excluded),
        "selected_target_rows": len(selected),
        "default_target_rows_before_exclusion": len(default_rows),
    }


def _load_template(root: Path) -> dict[str, Any]:
    return json.loads(io_path(root / NORMALIZED_TEMPLATE_PATH).read_text(encoding="utf-8-sig"))


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def _with_report_identity_source(record: Mapping[str, Any], source: str) -> Mapping[str, Any]:
    payload = dict(record)
    payload.setdefault("report_identity_source", source)
    return payload


def _mt5_records_from_kpi(
    root: Path,
    run_row: Mapping[str, str],
    payload: Mapping[str, Any],
    *,
    parser_errors: list[dict[str, Any]] | None = None,
) -> list[Mapping[str, Any]]:
    records = payload.get("mt5_records")
    if isinstance(records, list):
        direct_records = [record for record in records if isinstance(record, Mapping)]
        if direct_records:
            return [_with_report_identity_source(record, "kpi_record_mt5_records") for record in direct_records]

    mt5 = payload.get("mt5", {})
    if isinstance(mt5, Mapping):
        records = mt5.get("kpi_records")
        if isinstance(records, list):
            nested_records = [record for record in records if isinstance(record, Mapping)]
            if nested_records:
                return [_with_report_identity_source(record, "kpi_record_nested_mt5_records") for record in nested_records]

    manifest_records = _mt5_records_from_manifest(root, run_row)
    if manifest_records:
        return manifest_records
    return _mt5_records_from_report_scan(root, run_row, parser_errors=parser_errors)


def _mt5_records_from_manifest(root: Path, run_row: Mapping[str, str]) -> list[Mapping[str, Any]]:
    manifest_path = root / str(run_row.get("path", "")) / "run_manifest.json"
    if not path_exists(manifest_path):
        return []
    try:
        manifest = _load_json(manifest_path)
    except Exception:
        return []

    candidates: list[Mapping[str, Any]] = []
    for key in ("mt5_strategy_tester_reports", "strategy_tester_reports", "mt5_report_records"):
        value = manifest.get(key)
        if isinstance(value, list):
            candidates.extend(record for record in value if isinstance(record, Mapping))
    mt5 = manifest.get("mt5", {})
    if isinstance(mt5, Mapping):
        for key in ("strategy_tester_reports", "report_records", "kpi_records"):
            value = mt5.get(key)
            if isinstance(value, list):
                candidates.extend(record for record in value if isinstance(record, Mapping))
    for result in manifest.get("execution_results", []) if isinstance(manifest.get("execution_results"), list) else []:
        if isinstance(result, Mapping) and isinstance(result.get("strategy_tester_report"), Mapping):
            report = dict(result["strategy_tester_report"])
            report.setdefault("tier", result.get("tier"))
            report.setdefault("split", result.get("split"))
            report.setdefault("routing_mode", result.get("routing_mode"))
            candidates.append(report)

    records: list[Mapping[str, Any]] = []
    for candidate in candidates:
        report_path = _candidate_report_path(candidate)
        if not report_path:
            continue
        identity = _identity_from_report_metadata(candidate)
        if identity is None:
            continue
        records.append(
            _with_report_identity_source(
                {
                    **identity,
                    "status": candidate.get("status", "completed"),
                    "metrics": candidate.get("metrics", {}),
                    "report": {"html_report": {"path": str(report_path)}},
                },
                "run_manifest_report_identity",
            )
        )
    return records


def _candidate_report_path(candidate: Mapping[str, Any]) -> str | None:
    html_report = candidate.get("html_report")
    if isinstance(html_report, Mapping):
        for key in ("path", "source_path"):
            if html_report.get(key):
                return str(html_report[key])
    if candidate.get("report_path"):
        return str(candidate["report_path"])
    report = candidate.get("report")
    if isinstance(report, Mapping):
        return _candidate_report_path(report)
    return None


def _identity_from_report_metadata(candidate: Mapping[str, Any]) -> dict[str, str] | None:
    if all(candidate.get(key) for key in ("record_view", "tier_scope", "split", "route_role")):
        return {
            "record_view": str(candidate["record_view"]),
            "tier_scope": str(candidate["tier_scope"]),
            "split": str(candidate["split"]),
            "route_role": str(candidate["route_role"]),
        }
    tier = str(candidate.get("tier") or candidate.get("tier_scope") or "")
    split = str(candidate.get("split") or "")
    if split not in {"validation_is", "validation", "oos", "train"}:
        return None
    routing_mode = str(candidate.get("routing_mode") or "")
    if routing_mode in {"tier_a_primary_tier_b_fallback", "tier_a_primary_no_fallback"}:
        return {
            "record_view": f"mt5_routed_total_{split}",
            "tier_scope": "Tier A+B",
            "split": split,
            "route_role": "routed_total",
        }
    if tier == "Tier A":
        return {
            "record_view": f"mt5_tier_a_only_{split}",
            "tier_scope": "Tier A",
            "split": split,
            "route_role": "tier_only_total",
        }
    if tier == "Tier B":
        return {
            "record_view": f"mt5_tier_b_fallback_only_{split}",
            "tier_scope": "Tier B",
            "split": split,
            "route_role": "tier_b_fallback_only_total",
        }
    if tier == "Tier A+B":
        return {
            "record_view": f"mt5_routed_total_{split}",
            "tier_scope": "Tier A+B",
            "split": split,
            "route_role": "routed_total",
        }
    return None


def _mt5_records_from_report_scan(
    root: Path,
    run_row: Mapping[str, str],
    *,
    parser_errors: list[dict[str, Any]] | None = None,
) -> list[Mapping[str, Any]]:
    reports_dir = root / str(run_row.get("path", "")) / "mt5" / "reports"
    if not path_exists(reports_dir):
        return []
    records: list[Mapping[str, Any]] = []
    try:
        report_names = sorted(os.listdir(io_path(reports_dir)))
    except OSError:
        return []
    for report_name in report_names:
        if not report_name.lower().endswith((".htm", ".html")):
            continue
        report_path = reports_dir / report_name
        identity = _report_identity_from_name(report_name)
        if identity is None:
            if parser_errors is not None:
                parser_errors.append(
                    {
                        "run_id": run_row.get("run_id"),
                        "record_view": None,
                        "error": "mt5_report_identity_unresolved",
                        "path": report_path.as_posix(),
                    }
                )
            continue
        records.append(
            {
                "record_view": identity["record_view"],
                "tier_scope": identity["tier_scope"],
                "split": identity["split"],
                "status": "completed",
                "route_role": identity["route_role"],
                "metrics": {},
                "report": {"html_report": {"path": report_path.as_posix()}},
                "report_identity_source": "filename_scan_fallback",
            }
        )
    return records


def _report_identity_from_name(report_name: str) -> dict[str, str] | None:
    stem = Path(report_name).stem.lower()
    split = "oos" if stem.endswith("_oos") else "validation_is" if stem.endswith("_validation_is") else None
    if split is None:
        return None

    if "_tier_b_fallback_only_" in stem:
        return {
            "record_view": f"mt5_tier_b_fallback_only_{split}",
            "tier_scope": "Tier B",
            "split": split,
            "route_role": "tier_b_fallback_only_total",
        }
    if "_tier_a_only_" in stem:
        return {
            "record_view": f"mt5_tier_a_only_{split}",
            "tier_scope": "Tier A",
            "split": split,
            "route_role": "tier_only_total",
        }
    if "_routed_" in stem:
        return {
            "record_view": f"mt5_routed_total_{split}",
            "tier_scope": "Tier A+B",
            "split": split,
            "route_role": "routed_total",
        }
    return None


def _merge_metrics(parsed_metrics: Mapping[str, Any], mt5_record: Mapping[str, Any]) -> dict[str, Any]:
    source_metrics = dict(mt5_record.get("metrics", {})) if isinstance(mt5_record.get("metrics"), Mapping) else {}
    if _is_actual_routed_component(mt5_record):
        merged = dict(parsed_metrics)
        merged.update(source_metrics)
        return merged

    merged = dict(source_metrics)
    merged.update(parsed_metrics)
    return merged


def _is_actual_routed_component(mt5_record: Mapping[str, Any]) -> bool:
    if mt5_record.get("route_role") in {"primary_used", "fallback_used"}:
        return True
    metrics = mt5_record.get("metrics", {})
    if isinstance(metrics, Mapping) and metrics.get("aggregation") == "actual_routed_component":
        return True
    report = mt5_record.get("report", {})
    return isinstance(report, Mapping) and report.get("aggregation") == "actual_routed_component"


def _report_path(root: Path, mt5_record: Mapping[str, Any]) -> Path | None:
    report = mt5_record.get("report", {})
    candidates: list[Any] = []
    _collect_report_candidates(report, candidates)
    metrics = mt5_record.get("metrics", {})
    if isinstance(metrics, Mapping):
        candidates.append(metrics.get("report_path"))
    for candidate in candidates:
        if not candidate:
            continue
        path = Path(str(candidate))
        if not path.is_absolute():
            path = root / path
        if path_exists(path):
            return path
    return None


def _collect_report_candidates(value: Any, candidates: list[Any]) -> None:
    if not isinstance(value, Mapping):
        return
    html_report = value.get("html_report", {})
    metrics_report = value.get("metrics", {})
    if isinstance(html_report, Mapping):
        candidates.extend([html_report.get("path"), html_report.get("source_path")])
    if isinstance(metrics_report, Mapping):
        candidates.append(metrics_report.get("report_path"))
    _collect_report_candidates(value.get("source_report"), candidates)


def _normalized_record(
    template: Mapping[str, Any],
    *,
    run_row: Mapping[str, str],
    kpi_payload: Mapping[str, Any],
    kpi_path: Path,
    mt5_record: Mapping[str, Any],
    report_path: Path,
    metrics: Mapping[str, Any],
    parsed_metrics: Mapping[str, Any],
) -> dict[str, Any]:
    record = deepcopy(template)
    run_id = str(run_row.get("run_id", ""))
    stage_id = str(run_row.get("stage_id", ""))
    record_view = str(mt5_record.get("record_view", "not_applicable"))
    split = _normalize_split(str(mt5_record.get("split", "not_applicable")))
    tier_scope = str(mt5_record.get("tier_scope", "not_applicable"))
    route_role = str(mt5_record.get("route_role", "not_applicable"))
    variant_id = _variant_id(kpi_payload)
    report_hash = sha256_file_lf_normalized(report_path)
    kpi_hash = sha256_file_lf_normalized(kpi_path)

    record["row_grain"] = {
        "run_id": _cell(run_id, authority="work_packet_and_run_manifest"),
        "variant_id": _cell(variant_id, "run_has_no_variant_layer" if variant_id is None else None, "work_packet_and_run_manifest"),
        "split": _cell(split, authority="mt5_strategy_tester_report"),
        "tier_scope": _cell(tier_scope, authority="mt5_strategy_tester_report"),
        "record_view": _cell(record_view, authority="mt5_strategy_tester_report"),
        "route_role": _cell(route_role, authority="mt5_strategy_tester_report"),
    }
    record["run_identity"].update(
        {
            "run_id": _cell(run_id, authority="work_packet_and_run_manifest"),
            "variant_id": _cell(variant_id, "run_has_no_variant_layer" if variant_id is None else None, "work_packet_and_run_manifest"),
            "idea_id": _cell(_idea_id(run_row), authority="run_registry"),
            "stage_id": _cell(stage_id, authority="run_registry"),
            "model_family": _cell(_model_family(run_id), "source_artifact_missing" if _model_family(run_id) is None else None, "run_registry"),
            "feature_set_id": _cell(_first_present(kpi_payload, ("feature_set_id", "FEATURE_SET_ID")), "source_artifact_missing", "work_packet_and_run_manifest"),
            "label_id": _cell(_first_present(kpi_payload, ("label_id", "LABEL_ID")), "source_artifact_missing", "work_packet_and_run_manifest"),
            "split_contract": _cell(_first_present(kpi_payload, ("split_contract", "split_id")), "source_artifact_missing", "work_packet_and_run_manifest"),
            "stage_inheritance": _cell(
                _stage_inheritance(kpi_payload, run_id),
                "stage_inheritance_not_recorded",
                "work_packet_and_run_manifest",
            ),
            "artifact_hashes": _cell(
                {
                    "kpi_record_sha256": kpi_hash,
                    "mt5_report_sha256": report_hash,
                    "mt5_report_path": _repo_or_abs(report_path),
                },
                authority="work_packet_and_run_manifest",
            ),
        }
    )

    _fill_signal_model(record, kpi_payload=kpi_payload, mt5_record=mt5_record, metrics=metrics, split=split)
    _fill_mt5_headline(record, metrics)
    _fill_risk(record, metrics)
    _fill_trade_diagnostics(record, metrics)
    _fill_regime(record)
    _fill_execution(record, metrics)
    record["source_evidence"] = {
        "kpi_record_path": _repo_or_abs(kpi_path),
        "mt5_report_path": _repo_or_abs(report_path),
        "mt5_report_sha256": report_hash,
        "mt5_report_parse_status": parsed_metrics.get("status"),
        "mt5_report_missing_required_metrics": list(parsed_metrics.get("missing_required_metrics", []) or []),
        "mt5_report_source_encoding": parsed_metrics.get("source_encoding"),
        "report_identity_source": mt5_record.get("report_identity_source", "unknown"),
        "parser": "foundation.mt5.strategy_report.extract_mt5_strategy_report_metrics",
    }
    return record


def _fill_signal_model(
    record: dict[str, Any],
    *,
    kpi_payload: Mapping[str, Any],
    mt5_record: Mapping[str, Any],
    metrics: Mapping[str, Any],
    split: str,
) -> None:
    python_metrics = kpi_payload.get("python_metrics", {})
    split_python = {}
    if isinstance(python_metrics, Mapping):
        split_python = python_metrics.get(split) or python_metrics.get("validation" if split == "validation" else split) or {}
    if not isinstance(split_python, Mapping):
        split_python = {}
    source_metrics = mt5_record.get("metrics") if isinstance(mt5_record.get("metrics"), Mapping) else {}

    values = {
        "validation_accuracy": split_python.get("directional_hit_rate") if split == "validation" else None,
        "oos_accuracy": split_python.get("directional_hit_rate") if split == "oos" else None,
        "signal_count": source_metrics.get("signal_count") or split_python.get("signal_count"),
        "signal_coverage": source_metrics.get("signal_coverage") or split_python.get("signal_coverage"),
        "short_count": source_metrics.get("short_count") or split_python.get("short_count") or metrics.get("tier_a_short_count"),
        "long_count": source_metrics.get("long_count") or split_python.get("long_count") or metrics.get("tier_a_long_count"),
        "directional_hit_rate": split_python.get("directional_hit_rate"),
        "threshold": _threshold_value(kpi_payload, mt5_record),
        "threshold_method": _threshold_method(kpi_payload),
    }
    for field, value in values.items():
        record["signal_model"][field] = _cell(
            value,
            _signal_na_reason(field, split),
            "python_training_or_signal_output",
        )
    for field in ("train_accuracy", "macro_f1", "log_loss"):
        record["signal_model"][field] = _cell(None, "metric_not_emitted_by_mt5", "python_training_or_signal_output")


def _fill_mt5_headline(record: dict[str, Any], metrics: Mapping[str, Any]) -> None:
    for field, source in HEADLINE_MAP.items():
        value = metrics.get(source)
        if _profit_attribution_not_separable(metrics):
            record["mt5_trading_headline"][field] = _cell(
                None,
                "profit_attribution_not_separable_from_single_routed_account_path",
                "mt5_strategy_tester_report",
            )
        elif field == "profit_factor" and _is_zero_gross_loss(metrics):
            record["mt5_trading_headline"][field] = _cell(
                None,
                "gross_loss_is_zero",
                "mt5_strategy_tester_report",
                extra={"raw_mt5_display": value},
            )
        else:
            record["mt5_trading_headline"][field] = _cell(
                value,
                None if value is not None else "metric_not_emitted_by_mt5",
                "mt5_strategy_tester_report",
            )
    record["mt5_trading_headline"]["avg_win"] = _cell(None, "metric_not_emitted_by_mt5", "mt5_strategy_tester_report")
    record["mt5_trading_headline"]["avg_loss"] = _cell(None, "metric_not_emitted_by_mt5", "mt5_strategy_tester_report")
    record["mt5_trading_headline"]["payoff_ratio"] = _cell(None, "metric_not_emitted_by_mt5", "mt5_strategy_tester_report")


def _fill_risk(record: dict[str, Any], metrics: Mapping[str, Any]) -> None:
    for field, source in RISK_MAP.items():
        value = metrics.get(source)
        if _profit_attribution_not_separable(metrics):
            record["risk"][field] = _cell(
                None,
                "profit_attribution_not_separable_from_single_routed_account_path",
                "mt5_strategy_tester_report",
            )
        else:
            record["risk"][field] = _cell(
                value,
                None if value is not None else "metric_not_emitted_by_mt5",
                "mt5_strategy_tester_report",
            )
    for field in ("time_under_water", "longest_recovery_duration", "ulcer_index"):
        record["risk"][field] = _cell(None, "equity_curve_missing", "equity_curve_reconstruction")
    for field in ("worst_day", "worst_week", "consecutive_losses"):
        record["risk"][field] = _cell(None, "trade_list_missing", "python_recomputed_from_mt5_deals")


def _fill_trade_diagnostics(record: dict[str, Any], metrics: Mapping[str, Any]) -> None:
    record["trade_diagnostics"]["long_trade_count"] = _cell(
        metrics.get("long_trade_count"),
        None if metrics.get("long_trade_count") is not None else "metric_not_emitted_by_mt5",
        "mt5_strategy_tester_report",
    )
    record["trade_diagnostics"]["short_trade_count"] = _cell(
        metrics.get("short_trade_count"),
        None if metrics.get("short_trade_count") is not None else "metric_not_emitted_by_mt5",
        "mt5_strategy_tester_report",
    )
    for field in (
        "long_net_profit",
        "short_net_profit",
        "long_expectancy",
        "short_expectancy",
        "avg_hold_bars",
        "hold_distribution",
        "mfe_mean",
        "mae_mean",
        "realized_over_mfe",
        "loss_trade_mfe",
        "win_trade_mae",
    ):
        record["trade_diagnostics"][field] = _cell(None, "trade_telemetry_missing", "mt5_trade_telemetry")


def _fill_regime(record: dict[str, Any]) -> None:
    for field in ("session_slice", "volatility_regime", "trend_regime", "adx_bucket", "spread_regime", "validation_oos_gap"):
        record["regime_slice_attribution"][field] = _cell(
            None,
            "trade_list_missing",
            "python_attribution_from_signal_and_trade_join",
        )
    for field in ("month_pnl", "quarter_pnl", "subperiod_consistency"):
        record["regime_slice_attribution"][field] = _cell(
            None,
            "trade_list_missing",
            "python_attribution_from_signal_and_trade_join",
        )


def _fill_execution(record: dict[str, Any], metrics: Mapping[str, Any]) -> None:
    for field, source in EXECUTION_MAP.items():
        value = _first_metric(metrics, source)
        record["execution"][field] = _cell(
            value,
            None if value is not None else "runtime_telemetry_missing",
            "mt5_runtime_telemetry_summary",
        )
    for field in ("avg_spread", "avg_slippage"):
        record["execution"][field] = _cell(None, "metric_not_emitted_by_mt5", "mt5_runtime_telemetry_summary")
    record["execution"]["external_mismatch_count"] = _cell(None, "runtime_telemetry_missing", "mt5_runtime_telemetry_summary")
    record["execution"]["data_readiness_failures"] = _cell(None, "runtime_telemetry_missing", "mt5_runtime_telemetry_summary")


def _first_metric(metrics: Mapping[str, Any], source: str | Sequence[str]) -> Any:
    if isinstance(source, str):
        return metrics.get(source)
    for key in source:
        value = metrics.get(key)
        if value is not None:
            return value
    return None


def _build_summary(
    root: Path,
    *,
    packet_id: str,
    created_at_utc: str,
    inventory_rows: Sequence[Mapping[str, str]],
    records: Sequence[Mapping[str, Any]],
    missing_runs: Sequence[Mapping[str, Any]],
    parser_errors: Sequence[Mapping[str, Any]],
    target_confirmation: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    run_ids_with_records = sorted({str(record["row_grain"]["run_id"]["value"]) for record in records})
    status = "blocked_no_mt5_records"
    if records and not missing_runs and not parser_errors:
        status = "mt5_existing_report_recording_complete"
    elif records:
        status = "partial_existing_report_recording"
    target_confirmation = dict(target_confirmation or {})
    if target_confirmation.get("status") == "blocked":
        status = "blocked_target_confirmation"
    return {
        "packet_id": packet_id,
        "created_at_utc": created_at_utc,
        "status": status,
        "inventory_packet_id": INVENTORY_PACKET_ID,
        "target_runs_total": len(inventory_rows),
        "target_runs_with_mt5_records": len(run_ids_with_records),
        "target_runs_missing_mt5_records": len(missing_runs),
        "normalized_records_written": len(records),
        "parser_error_count": len(parser_errors),
        "target_confirmation_status": target_confirmation.get("status", "not_checked"),
        "target_confirmation_expected_target_rows": target_confirmation.get("expected_target_rows"),
        "target_confirmation_selected_target_rows": target_confirmation.get("selected_target_rows"),
        "target_confirmation_default_target_rows_before_exclusion": target_confirmation.get(
            "default_target_rows_before_exclusion"
        ),
        "target_confirmation_excluded_run_ids": target_confirmation.get("excluded_run_ids", []),
        "target_confirmation_findings": target_confirmation.get("findings", []),
        "missing_runs": list(missing_runs),
        "parser_errors": list(parser_errors),
        "source_authority": {
            "mt5_trading_headline": "mt5_strategy_tester_report",
            "risk": "mt5_strategy_tester_report",
            "execution": "mt5_runtime_telemetry_summary_when_available",
            "python": "cross_check_or_signal_layer_only",
        },
        "inputs": {
            "inventory_csv": CONFIRMED_INVENTORY_PATH.as_posix(),
            "target_confirmation": TARGET_CONFIRMATION_PATH.as_posix(),
            "normalized_template": NORMALIZED_TEMPLATE_PATH.as_posix(),
        },
        "outputs": {
            "normalized_kpi_records": f"docs/agent_control/packets/{packet_id}/normalized_kpi_records.jsonl",
            "normalized_kpi_summary": f"docs/agent_control/packets/{packet_id}/normalized_kpi_summary.csv",
            "recording_summary": f"docs/agent_control/packets/{packet_id}/recording_summary.json",
        },
        "workspace_root": root.resolve().as_posix(),
    }


def _build_work_packet(*, packet_id: str, created_at_utc: str, summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "packet_id": packet_id,
        "created_at_utc": created_at_utc,
        "user_request": {
            "user_quote": "이제 진짜 MT5까지 연동해서 KPI 기록 시작하자",
            "requested_action": "record_normalized_kpi_from_mt5_strategy_tester_reports",
            "requested_count": {"value": summary["target_runs_total"], "n_a_reason": None},
            "ambiguous_terms": ["MT5까지 연동", "KPI 기록 시작"],
        },
        "current_truth": {
            "active_stage": "12_model_family_challenge__extratrees_training_effect",
            "source_documents": [
                "docs/agent_control/packets/kpi_rebuild_inventory_v1/target_confirmation.yaml",
                "docs/agent_control/packets/kpi_rebuild_inventory_v1/experiment_inventory.csv",
                "docs/agent_control/kpi_source_authority.yaml",
            ],
        },
        "preflight": {
            "needs_clarification": False,
            "selected_option_id": "existing_mt5_reports_first_no_ledger_overwrite",
            "selected_option_user_quote": "MT5까지 연동해서 KPI 기록 시작",
            "blocked_until_answer": False,
        },
        "interpreted_scope": {
            "target_runs": summary["target_runs_total"],
            "execution_layers": ["existing_mt5_strategy_tester_reports", "existing_runtime_telemetry_summary"],
            "new_mt5_rerun_this_packet": False,
            "no_existing_ledger_overwrite": True,
            "scope_reduction_requires_user_quote": True,
        },
        "acceptance_criteria": [
            {
                "id": "AC-001",
                "text": "Read confirmed KPI rebuild targets from inventory packet.",
                "expected_artifact": "docs/agent_control/packets/kpi_rebuild_inventory_v1/experiment_inventory.csv",
                "verification_method": "target_run_count",
                "required": True,
            },
            {
                "id": "AC-002",
                "text": "Use MT5 Strategy Tester reports as authority for headline and risk KPI.",
                "expected_artifact": f"docs/agent_control/packets/{packet_id}/normalized_kpi_records.jsonl",
                "verification_method": "source_authority_fields",
                "required": True,
            },
            {
                "id": "AC-003",
                "text": "Do not overwrite existing run folders or alpha ledgers.",
                "expected_artifact": f"docs/agent_control/packets/{packet_id}/recording_summary.json",
                "verification_method": "packet_outputs_only",
                "required": True,
            },
        ],
        "kpi_contract": {
            "kpi_standard_version": "kpi_7layer_v1",
            "normalized_record_path": f"docs/agent_control/packets/{packet_id}/normalized_kpi_records.jsonl",
            "source_authority_reference": "docs/agent_control/kpi_source_authority.yaml",
            "n_a_reason_reference": "docs/agent_control/n_a_reason_registry.yaml",
        },
        "artifact_contract": {
            "raw_evidence": ["stages/*/02_runs/*/mt5/reports/*.htm", "stages/*/02_runs/*/kpi_record.json"],
            "machine_readable": [
                f"docs/agent_control/packets/{packet_id}/normalized_kpi_records.jsonl",
                f"docs/agent_control/packets/{packet_id}/normalized_kpi_summary.csv",
                f"docs/agent_control/packets/{packet_id}/recording_summary.json",
            ],
            "human_readable": [f"docs/agent_control/packets/{packet_id}/run_plan.yaml"],
        },
        "skill_routing": {
            "skills_selected": [
                "obsidian-reentry-read",
                "obsidian-run-evidence-system",
                "obsidian-runtime-parity",
                "obsidian-backtest-forensics",
                "obsidian-artifact-lineage",
            ],
            "required_skill_receipts": [
                f"docs/agent_control/packets/{packet_id}/skill_receipts/runtime_parity.yaml",
                f"docs/agent_control/packets/{packet_id}/skill_receipts/backtest_forensics.yaml",
                f"docs/agent_control/packets/{packet_id}/skill_receipts/artifact_lineage.yaml",
            ],
        },
        "final_claim_policy": {
            "allowed_claims": ["mt5_existing_report_recording_started", "partial_kpi_recording_complete"],
            "forbidden_claims": ["all_70_mt5_rerun_complete", "operating_promotion", "runtime_authority"],
            "claim_vocabulary_reference": "docs/agent_control/claim_vocabulary.yaml",
        },
        "summary_counts": {
            "target_runs_total": summary["target_runs_total"],
            "target_runs_with_mt5_records": summary["target_runs_with_mt5_records"],
            "target_runs_missing_mt5_records": summary["target_runs_missing_mt5_records"],
            "normalized_records_written": summary["normalized_records_written"],
        },
    }


def _build_run_plan(*, packet_id: str, created_at_utc: str, summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_plan_id": f"{packet_id}_run_plan",
        "packet_id": packet_id,
        "created_at_utc": created_at_utc,
        "stage_id": "cross_stage_kpi_rebuild_mt5_recording",
        "execution_scope": {
            "target_runs_total": summary["target_runs_total"],
            "existing_mt5_report_ingestion": True,
            "new_mt5_strategy_tester_execution": False,
            "no_existing_ledger_overwrite": True,
            "normalized_records_expected_from_existing_reports": summary["normalized_records_written"],
        },
        "phases": [
            {
                "id": "phase_1_existing_report_ingestion",
                "status": "complete" if summary["normalized_records_written"] else "blocked",
                "effect": "MT5 reports become machine-readable 7-layer KPI rows.",
            },
            {
                "id": "phase_2_missing_mt5_rerun_packet",
                "status": "next_required" if summary["target_runs_missing_mt5_records"] else "not_required",
                "effect": "Runs with no MT5 reports are handled in a separate execution packet.",
            },
        ],
        "missing_mt5_runs": summary["missing_runs"],
        "artifact_plan": summary["outputs"],
        "forbidden_actions": ["overwrite_alpha_run_ledger", "claim_all_70_rerun_complete", "claim_operating_promotion"],
    }


def _build_receipts(*, packet_id: str, created_at_utc: str, summary: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        "runtime_parity": {
            "packet_id": packet_id,
            "created_at_utc": created_at_utc,
            "skill": "obsidian-runtime-parity",
            "status": "executed",
            "research_path": "existing run kpi_record.json and Python signal metrics",
            "runtime_path": "existing MT5 Strategy Tester reports and runtime telemetry summaries",
            "shared_contract": "row grain and KPI source authority contracts",
            "parity_check": "MT5 report authority ingestion; no new runtime authority claim",
            "runtime_claim_boundary": "runtime_probe_existing_report_recording",
        },
        "backtest_forensics": {
            "packet_id": packet_id,
            "created_at_utc": created_at_utc,
            "skill": "obsidian-backtest-forensics",
            "status": "executed",
            "tester_identity": "read from existing .ini/.set/kpi_record where available; missing fields remain n/a",
            "report_identity": summary["outputs"]["normalized_kpi_records"],
            "trade_evidence": "headline and risk KPI parsed from MT5 Strategy Tester reports",
            "backtest_judgment": "usable_with_boundary",
            "boundary": "Existing reports are recorded; missing MT5 runs are not silently filled.",
        },
        "artifact_lineage": {
            "packet_id": packet_id,
            "created_at_utc": created_at_utc,
            "skill": "obsidian-artifact-lineage",
            "status": "executed",
            "source_inputs": [
                "docs/agent_control/packets/kpi_rebuild_inventory_v1/experiment_inventory.csv",
                "stages/*/02_runs/*/kpi_record.json",
                "stages/*/02_runs/*/mt5/reports/*.htm",
            ],
            "producer": "foundation.control_plane.mt5_kpi_recorder",
            "consumer": "next KPI rebuild rerun packet and user review",
            "artifact_paths": list(summary["outputs"].values()),
            "availability": "tracked",
            "lineage_judgment": "connected_with_boundary",
        },
    }


def _summary_row(record: Mapping[str, Any], report_path: Path) -> dict[str, Any]:
    headline = record["mt5_trading_headline"]
    risk = record["risk"]
    return {
        "run_id": record["row_grain"]["run_id"]["value"],
        "stage_id": record["run_identity"]["stage_id"]["value"],
        "record_view": record["row_grain"]["record_view"]["value"],
        "split": record["row_grain"]["split"]["value"],
        "tier_scope": record["row_grain"]["tier_scope"]["value"],
        "route_role": record["row_grain"]["route_role"]["value"],
        "report_path": _repo_or_abs(report_path),
        "report_sha256": record["source_evidence"]["mt5_report_sha256"],
        "net_profit": headline["net_profit"]["value"],
        "profit_factor": headline["profit_factor"]["value"],
        "trade_count": headline["trade_count"]["value"],
        "max_drawdown_amount": risk["max_drawdown_amount"]["value"],
        "status": "recorded",
    }


def _missing_run(run_row: Mapping[str, str], reason: str, detail: str) -> dict[str, Any]:
    return {
        "run_id": run_row.get("run_id"),
        "stage_id": run_row.get("stage_id"),
        "reason": reason,
        "detail": detail,
    }


def _cell(value: Any, n_a_reason: str | None = None, authority: str = "", extra: Mapping[str, Any] | None = None) -> dict[str, Any]:
    reason = n_a_reason if value is None else None
    if value is None and not reason:
        reason = "not_recorded"
    payload = {"value": value, "n/a_reason": reason, "authority": authority}
    if extra:
        payload.update(dict(extra))
    return payload


def _signal_na_reason(field: str, split: str) -> str:
    if field == "validation_accuracy" and split != "validation":
        return "not_applicable_for_split"
    if field == "oos_accuracy" and split != "oos":
        return "not_applicable_for_split"
    if field in {"threshold", "threshold_method"}:
        return "threshold_not_recorded"
    return "python_signal_metric_missing"


def _first_present(payload: Mapping[str, Any], keys: Sequence[str]) -> Any:
    for key in keys:
        if key in payload and payload[key] not in (None, ""):
            return payload[key]
    return None


def _variant_id(payload: Mapping[str, Any]) -> str | None:
    for key in ("source_variant_id", "variant_id"):
        value = payload.get(key)
        if value:
            return str(value)
    return None


def _idea_id(run_row: Mapping[str, str]) -> str:
    return str(run_row.get("judgment") or run_row.get("run_id") or "")


def _model_family(run_id: str) -> str | None:
    lowered = run_id.lower()
    if "logreg" in lowered:
        return "sklearn_logistic_regression_multiclass"
    if "lgbm" in lowered:
        return "lightgbm_lgbmclassifier_multiclass"
    if "extratrees" in lowered or "_et_" in lowered:
        return "sklearn_extratreesclassifier_multiclass"
    return None


def _stage_inheritance(kpi_payload: Mapping[str, Any], run_id: str) -> bool | None:
    if "stage10_11_inheritance" in kpi_payload:
        return bool(kpi_payload["stage10_11_inheritance"])
    boundary = kpi_payload.get("standalone_boundary")
    if isinstance(boundary, Mapping) and "stage10_11_inheritance" in boundary:
        return bool(boundary["stage10_11_inheritance"])
    if run_id.lower().startswith("run03"):
        return False
    return None


def _threshold_value(kpi_payload: Mapping[str, Any], mt5_record: Mapping[str, Any]) -> Any:
    for source in (mt5_record.get("threshold_rule"), kpi_payload.get("threshold_rule")):
        if isinstance(source, Mapping):
            return {
                "short_threshold": source.get("short_threshold"),
                "long_threshold": source.get("long_threshold"),
                "min_margin": source.get("min_margin"),
            }
    return None


def _threshold_method(kpi_payload: Mapping[str, Any]) -> Any:
    return kpi_payload.get("threshold_method") or kpi_payload.get("THRESHOLD_METHOD")


def _normalize_split(value: str) -> str:
    return {"validation_is": "validation", "validation": "validation", "oos": "oos", "train": "train"}.get(value, value)


def _is_zero_gross_loss(metrics: Mapping[str, Any]) -> bool:
    gross_loss = metrics.get("gross_loss")
    try:
        return gross_loss is not None and abs(float(gross_loss)) == 0.0
    except (TypeError, ValueError):
        return False


def _profit_attribution_not_separable(metrics: Mapping[str, Any]) -> bool:
    return metrics.get("profit_attribution") == "not_separable_from_single_routed_account_path"


def _repo_or_abs(path: Path) -> str:
    try:
        return path.resolve().relative_to(Path(".").resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_jsonl(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def _write_yaml(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(yaml.safe_dump(payload, allow_unicode=True, sort_keys=False), encoding="utf-8")


def _utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Record normalized KPI rows from existing MT5 Strategy Tester reports.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--packet-id", default=PACKET_ID_DEFAULT)
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--created-at-utc", default=None)
    args = parser.parse_args(argv)

    packet = write_mt5_kpi_recording_packet(
        args.root,
        packet_id=args.packet_id,
        output_dir=args.output_dir,
        created_at_utc=args.created_at_utc,
    )
    print(json.dumps(packet["summary"], ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
