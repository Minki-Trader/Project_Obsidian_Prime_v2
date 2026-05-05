from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    read_csv_rows,
    sha256_file_lf_normalized,
    upsert_csv_rows,
    write_csv_rows,
)
from foundation.control_plane.mt5_handoff_identity_helpers import (
    as_float,
    basename,
    exists,
    float_close,
    hash_text,
    nested,
    parse_key_value_file,
    path_text,
    paths_same,
    read_json,
    rel,
    resolve_path,
    under_root,
    write_json,
    write_markdown,
    write_matrix_csv,
)
from foundation.control_plane.mechanism_role_map import STAGE_ID
from foundation.control_plane.signalcard_adapter_probe import RUN_ID as SOURCE_RUN_ID
from foundation.models.onnx_bridge import sha256_file


RUN_ID = "run27D_mt5_handoff_identity_audit_v1"
PACKET_ID = "stage33_run27D_mt5_handoff_identity_audit_v1"
BOUNDARY = "mt5_handoff_identity_audit_only_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
SELECTED_SOURCE_STAGE_ID = "12_model_family_challenge__extratrees_training_effect"
SELECTED_SOURCE_RUN_ID = "run03H_et_v13_tier_balance_mt5_v1"


@dataclass(frozen=True)
class Mt5HandoffIdentityAuditResult:
    summary: dict[str, Any]
    report: dict[str, Any]
    matrix_rows: list[dict[str, Any]]
    stage_rows: list[dict[str, Any]]
    run_registry_row: dict[str, Any]
    artifact_rows: list[dict[str, Any]]


def build_mt5_handoff_identity_audit(root: Path | str = Path(".")) -> Mt5HandoffIdentityAuditResult:
    root_path = Path(root)
    run27c_pack_path = (
        root_path
        / "stages"
        / STAGE_ID
        / "02_runs"
        / SOURCE_RUN_ID
        / "model_pack"
        / "model_pack_manifest.json"
    )
    source_run_root = root_path / "stages" / SELECTED_SOURCE_STAGE_ID / "02_runs" / SELECTED_SOURCE_RUN_ID
    model_pack = read_json(run27c_pack_path)
    source_manifest = read_json(source_run_root / "run_manifest.json")
    source_kpi = read_json(source_run_root / "kpi_record.json")

    model_pack_checks = _model_pack_checks(root_path, model_pack)
    attempts = list(source_manifest.get("attempts") or [])
    execution_results = _execution_results(source_manifest, source_kpi)
    reports = _strategy_tester_reports(source_manifest, source_kpi)
    kpi_records = _kpi_records(source_kpi)
    attempts_payload: list[dict[str, Any]] = []
    matrix_rows: list[dict[str, Any]] = []
    for attempt in attempts:
        payload, rows = _attempt_identity(root_path, source_run_root, attempt, execution_results, reports, kpi_records, model_pack)
        attempts_payload.append(payload)
        matrix_rows.extend(rows)

    cross_checks = _cross_checks(source_manifest, source_kpi, model_pack_checks, attempts_payload)
    blocking_findings = _blocking_findings(model_pack_checks, attempts_payload, cross_checks)
    summary = _summary(source_manifest, source_kpi, model_pack_checks, attempts_payload, cross_checks, blocking_findings)
    report = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "selected_source_run_id": SELECTED_SOURCE_RUN_ID,
        "selected_source_stage_id": SELECTED_SOURCE_STAGE_ID,
        "summary": summary,
        "model_pack_checks": model_pack_checks,
        "source_manifest_identity": {
            "path": rel(root_path, source_run_root / "run_manifest.json"),
            "sha256_lf_normalized": sha256_file_lf_normalized(source_run_root / "run_manifest.json"),
            "external_verification_status": source_manifest.get("external_verification_status"),
            "judgment": source_manifest.get("judgment"),
        },
        "source_kpi_identity": {
            "path": rel(root_path, source_run_root / "kpi_record.json"),
            "sha256_lf_normalized": sha256_file_lf_normalized(source_run_root / "kpi_record.json"),
            "external_verification_status": source_kpi.get("external_verification_status")
            or nested(source_kpi, ("mt5", "external_verification_status")),
            "judgment": source_kpi.get("judgment"),
        },
        "attempts": attempts_payload,
        "cross_checks": cross_checks,
        "claim_boundary": BOUNDARY,
    }
    return Mt5HandoffIdentityAuditResult(
        summary=summary,
        report=report,
        matrix_rows=matrix_rows,
        stage_rows=_stage_ledger_rows(summary),
        run_registry_row=_run_registry_row(summary),
        artifact_rows=_artifact_rows(),
    )


def write_mt5_handoff_identity_audit_packet(root: Path | str = Path("."), *, generated_at_utc: str | None = None) -> dict[str, Any]:
    root_path = Path(root)
    generated_at = generated_at_utc or datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    result = build_mt5_handoff_identity_audit(root_path)
    run_root = root_path / "stages" / STAGE_ID / "02_runs" / RUN_ID
    reports_root = run_root / "reports"
    packet_root = root_path / "docs/agent_control/packets" / PACKET_ID
    io_path(reports_root).mkdir(parents=True, exist_ok=True)
    io_path(packet_root).mkdir(parents=True, exist_ok=True)

    report_path = run_root / "mt5_handoff_identity_report.json"
    matrix_path = run_root / "handoff_identity_matrix.csv"
    manifest_path = run_root / "run_manifest.json"
    result_summary_path = reports_root / "result_summary.md"
    aggregate_summary_path = packet_root / "aggregate_summary.json"

    write_json(report_path, {"generated_at_utc": generated_at, **result.report})
    write_matrix_csv(matrix_path, result.matrix_rows)
    manifest = _manifest(root_path, generated_at, report_path, matrix_path, result)
    write_json(manifest_path, manifest)
    write_markdown(result_summary_path, _result_summary_markdown(generated_at, result))
    aggregate = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "status": "reviewed_mt5_handoff_identity_audit_completed"
        if result.summary["passed"]
        else "blocked_mt5_handoff_identity_audit",
        "judgment": result.summary["judgment"],
        "boundary": BOUNDARY,
        "generated_at_utc": generated_at,
        "report_path": rel(root_path, report_path),
        "matrix_path": rel(root_path, matrix_path),
        "run_manifest_path": rel(root_path, manifest_path),
        "result_summary_path": rel(root_path, result_summary_path),
        "counts": result.summary["counts"],
        "runtime_handoff_decision": result.summary["runtime_handoff_decision"],
        "blocking_findings": result.summary["blocking_findings"],
        "required_gates": result.summary["required_gates"],
    }
    write_json(aggregate_summary_path, aggregate)
    _upsert_registers(root_path, result)
    upsert_csv_rows(
        root_path / "stages" / STAGE_ID / "03_reviews/stage_run_ledger.csv",
        ALPHA_LEDGER_COLUMNS,
        result.stage_rows,
        key="ledger_row_id",
    )
    return aggregate


def _model_pack_checks(root: Path, model_pack: Mapping[str, Any]) -> dict[str, Any]:
    tiers: dict[str, Any] = {}
    all_checks: list[bool] = []
    for tier_name, tier_payload in dict(model_pack.get("tiers") or {}).items():
        source_model = _artifact_hash_check(root, path_text(tier_payload.get("source_model")), hash_text(tier_payload.get("source_model")))
        onnx_model = _artifact_hash_check(root, path_text(tier_payload.get("onnx_model")), hash_text(tier_payload.get("onnx_model")))
        matrices: dict[str, Any] = {}
        for split_name, matrix_payload in dict(tier_payload.get("feature_matrices") or {}).items():
            expected_hash = str(matrix_payload.get("sha256_lf_normalized") or "")
            matrix_path = root / str(matrix_payload.get("path") or "")
            matrices[split_name] = {
                "path": rel(root, matrix_path),
                "expected_sha256_lf_normalized": expected_hash,
                "actual_sha256_lf_normalized": sha256_file_lf_normalized(matrix_path) if exists(matrix_path) else None,
                "exists": exists(matrix_path),
                "passed": exists(matrix_path) and sha256_file_lf_normalized(matrix_path) == expected_hash,
            }
        tier_checks = [bool(source_model["passed"]), bool(onnx_model["passed"])]
        tier_checks.extend(bool(payload["passed"]) for payload in matrices.values())
        all_checks.extend(tier_checks)
        tiers[tier_name] = {
            "feature_order_hash": tier_payload.get("feature_order_hash"),
            "feature_count": tier_payload.get("feature_count"),
            "nonflat_threshold": tier_payload.get("nonflat_threshold"),
            "source_model": source_model,
            "onnx_model": onnx_model,
            "feature_matrices": matrices,
            "passed": all(tier_checks),
        }
    return {
        "model_pack_id": model_pack.get("model_pack_id"),
        "packaging_policy": model_pack.get("packaging_policy"),
        "parity_passed": model_pack.get("parity_passed"),
        "tiers": tiers,
        "passed": bool(all_checks) and all(all_checks),
    }


def _attempt_identity(
    root: Path,
    source_run_root: Path,
    attempt: Mapping[str, Any],
    execution_results: Sequence[Mapping[str, Any]],
    reports: Sequence[Mapping[str, Any]],
    kpi_records: Sequence[Mapping[str, Any]],
    model_pack: Mapping[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    attempt_name = str(attempt.get("attempt_name") or "")
    execution = _find_by(execution_results, "attempt_name", attempt_name)
    report_name = str(nested(attempt, ("ini", "tester", "Report")) or f"Project_Obsidian_Prime_v2_{SELECTED_SOURCE_RUN_ID}_{attempt_name}")
    report = _find_by(reports, "report_name", report_name)
    kpi_record = _find_kpi_record(kpi_records, attempt_name)
    set_check = _set_ini_hash_check(
        root,
        path_text(attempt.get("set")),
        hash_text(attempt.get("set")),
        nested(execution, ("tester_profile_set_copy", "sha256")),
        "set",
    )
    ini_check = _set_ini_hash_check(
        root,
        path_text(attempt.get("ini")),
        hash_text(attempt.get("ini")),
        nested(execution, ("tester_profile_ini_copy", "sha256")),
        "ini",
    )
    report_check = _report_hash_check(root, source_run_root, report_name, report)
    chart_check = _chart_hash_check(root, source_run_root, report_name, report)
    runtime_output_check = _runtime_output_check(execution)
    set_contract = _set_contract_check(root, set_check.get("path"), attempt, model_pack)
    ledger_check = _ledger_attempt_check(kpi_record, report_check, attempt)
    required = [
        set_check["passed"],
        ini_check["passed"],
        report_check["passed"],
        chart_check["passed"],
        runtime_output_check["passed"],
        set_contract["passed"],
        ledger_check["passed"],
        str(attempt.get("source_variant_id") or "") == "v13_base_margin002_q90",
    ]
    payload = {
        "attempt_name": attempt_name,
        "attempt_role": attempt.get("attempt_role"),
        "tier": attempt.get("tier"),
        "split": attempt.get("split"),
        "source_variant_id": attempt.get("source_variant_id"),
        "set": set_check,
        "ini": ini_check,
        "strategy_tester_report": report_check,
        "strategy_tester_chart": chart_check,
        "runtime_outputs": runtime_output_check,
        "set_contract": set_contract,
        "ledger_record": ledger_check,
        "passed": all(bool(item) for item in required),
    }
    rows = [_matrix_row(attempt_name, "set", set_check), _matrix_row(attempt_name, "ini", ini_check)]
    rows.extend(
        [
            _matrix_row(attempt_name, "strategy_tester_report", report_check),
            _matrix_row(attempt_name, "strategy_tester_chart", chart_check),
            _matrix_row(attempt_name, "runtime_outputs", runtime_output_check),
            _matrix_row(attempt_name, "set_contract", set_contract),
            _matrix_row(attempt_name, "ledger_record", ledger_check),
        ]
    )
    return payload, rows


def _set_contract_check(root: Path, set_path_text: Any, attempt: Mapping[str, Any], model_pack: Mapping[str, Any]) -> dict[str, Any]:
    path = resolve_path(root, str(set_path_text or ""))
    if not path or not exists(path):
        return {"passed": False, "reason": "set_file_missing", "path": str(set_path_text or "")}
    values = parse_key_value_file(path)
    tier_name = _tier_key(str(attempt.get("tier") or ""))
    split_key = "validation" if str(attempt.get("split")) == "validation_is" else str(attempt.get("split") or "")
    tier_payload = dict(dict(model_pack.get("tiers") or {}).get(tier_name) or {})
    checks = {
        "run_id_matches": values.get("InpRunId") == SELECTED_SOURCE_RUN_ID,
        "symbol_us100": values.get("InpMainSymbol") == "US100",
        "timeframe_m5": values.get("InpTimeframe") == "5",
        "timestamp_match_required": values.get("InpFeatureRequireTimestampMatch") == "true",
        "latest_fallback_disabled": values.get("InpFeatureAllowLatestFallback") == "false",
        "strict_header": values.get("InpFeatureStrictHeader") == "true",
        "feature_order_hash_matches": values.get("InpFeatureOrderHash") == str(tier_payload.get("feature_order_hash") or ""),
        "feature_count_matches": values.get("InpFeatureCount") == str(tier_payload.get("feature_count") or ""),
        "threshold_matches": float_close(values.get("InpShortThreshold"), tier_payload.get("nonflat_threshold"))
        and float_close(values.get("InpLongThreshold"), tier_payload.get("nonflat_threshold")),
        "model_path_matches_pack": basename(values.get("InpModelPath")) == basename(path_text(tier_payload.get("onnx_model"))),
        "feature_matrix_split_matches": split_key in str(values.get("InpFeatureCsvPath") or ""),
    }
    if str(attempt.get("tier") or "") == "Tier A+B":
        tier_b = dict(dict(model_pack.get("tiers") or {}).get("tier_b") or {})
        checks.update(
            {
                "fallback_enabled": values.get("InpFallbackEnabled") == "true",
                "fallback_feature_order_hash_matches": values.get("InpFallbackFeatureOrderHash")
                == str(tier_b.get("feature_order_hash") or ""),
                "fallback_feature_count_matches": values.get("InpFallbackFeatureCount") == str(tier_b.get("feature_count") or ""),
                "fallback_threshold_matches": float_close(values.get("InpFallbackShortThreshold"), tier_b.get("nonflat_threshold"))
                and float_close(values.get("InpFallbackLongThreshold"), tier_b.get("nonflat_threshold")),
                "fallback_model_path_matches_pack": basename(values.get("InpFallbackModelPath"))
                == basename(path_text(tier_b.get("onnx_model"))),
            }
        )
    else:
        checks["fallback_disabled_for_separate_view"] = values.get("InpFallbackEnabled") == "false"
    failed = [key for key, value in checks.items() if not value]
    return {
        "path": rel(root, path),
        "passed": not failed,
        "checks": checks,
        "failed_checks": failed,
        "set_run_id": values.get("InpRunId"),
        "feature_order_hash": values.get("InpFeatureOrderHash"),
        "model_path": values.get("InpModelPath"),
        "feature_csv_path": values.get("InpFeatureCsvPath"),
        "fallback_model_path": values.get("InpFallbackModelPath"),
        "fallback_feature_csv_path": values.get("InpFallbackFeatureCsvPath"),
    }


def _artifact_hash_check(root: Path, path_text: Any, expected_hash: Any) -> dict[str, Any]:
    path = resolve_path(root, str(path_text or ""))
    expected = str(expected_hash or "")
    exists_value = bool(path and exists(path))
    actual = sha256_file(path) if exists_value and path is not None else None
    return {
        "path": rel(root, path) if path and under_root(root, path) else str(path_text or ""),
        "exists": exists_value,
        "expected_sha256": expected,
        "actual_sha256": actual,
        "passed": exists_value and bool(expected) and actual == expected,
    }


def _set_ini_hash_check(root: Path, path_text: Any, manifest_hash: Any, executed_copy_hash: Any, kind: str) -> dict[str, Any]:
    path = resolve_path(root, str(path_text or ""))
    exists_value = bool(path and exists(path))
    actual = sha256_file(path) if exists_value and path is not None else None
    accepted = {
        "manifest_materialized_hash": str(manifest_hash or ""),
        "executed_profile_copy_hash": str(executed_copy_hash or ""),
    }
    matched_source = next((name for name, expected in accepted.items() if expected and expected == actual), "")
    return {
        "path": rel(root, path) if path and under_root(root, path) else str(path_text or ""),
        "exists": exists_value,
        "expected_sha256": str(manifest_hash or ""),
        "executed_profile_copy_sha256": str(executed_copy_hash or ""),
        "actual_sha256": actual,
        "matched_expected_source": matched_source,
        "passed": exists_value and bool(matched_source),
        "note": f"{kind}_hash_accepts_executed_profile_copy_hash_when_manifest_materialization_hash_is_stale",
    }


def _report_hash_check(root: Path, source_run_root: Path, report_name: str, report: Mapping[str, Any] | None) -> dict[str, Any]:
    html_payload = dict((report or {}).get("html_report") or {})
    path_text = html_payload.get("path") or source_run_root / "mt5" / "reports" / f"{report_name}.htm"
    return {**_artifact_hash_check(root, path_text, html_payload.get("sha256")), "report_name": report_name}


def _chart_hash_check(root: Path, source_run_root: Path, report_name: str, report: Mapping[str, Any] | None) -> dict[str, Any]:
    chart_payload = dict((report or {}).get("chart") or {})
    path_text = chart_payload.get("path") or source_run_root / "mt5" / "reports" / f"{report_name}.png"
    return {**_artifact_hash_check(root, path_text, chart_payload.get("sha256")), "report_name": report_name}


def _runtime_output_check(execution: Mapping[str, Any] | None) -> dict[str, Any]:
    runtime = dict((execution or {}).get("runtime_outputs") or {})
    last_summary = dict(runtime.get("last_summary") or {})
    checks = {
        "execution_status_completed": str((execution or {}).get("status") or "") == "completed",
        "returncode_zero": (execution or {}).get("returncode") == 0,
        "runtime_wait_completed": runtime.get("wait_status") == "completed",
        "runtime_summary_exists": bool(runtime.get("summary_exists")),
        "runtime_telemetry_exists": bool(runtime.get("telemetry_exists")),
        "runtime_run_id_matches": last_summary.get("run_id") == SELECTED_SOURCE_RUN_ID,
        "runtime_model_ok_positive": int(last_summary.get("model_ok_count") or 0) > 0,
    }
    failed = [key for key, value in checks.items() if not value]
    return {
        "passed": not failed,
        "checks": checks,
        "failed_checks": failed,
        "summary_sha256": runtime.get("summary_sha256"),
        "telemetry_sha256": runtime.get("telemetry_sha256"),
        "model_ok_count": last_summary.get("model_ok_count"),
        "feature_ready_count": last_summary.get("feature_ready_count"),
        "order_fill_count": last_summary.get("order_fill_count"),
    }


def _ledger_attempt_check(
    kpi_record: Mapping[str, Any] | None,
    report_check: Mapping[str, Any],
    attempt: Mapping[str, Any],
) -> dict[str, Any]:
    metrics = dict((kpi_record or {}).get("metrics") or {})
    checks = {
        "kpi_record_present": bool(kpi_record),
        "kpi_completed": str((kpi_record or {}).get("status") or "") == "completed",
        "path_matches_report": paths_same(
            (kpi_record or {}).get("path") or metrics.get("report_path"),
            report_check.get("path"),
        ),
        "trade_count_present": as_float(metrics.get("trade_count")) is not None,
        "net_profit_present": as_float(metrics.get("net_profit")) is not None,
        "profit_factor_present": as_float(metrics.get("profit_factor")) is not None,
        "tier_scope_matches": str((kpi_record or {}).get("tier_scope") or "") == str(attempt.get("tier") or ""),
    }
    failed = [key for key, value in checks.items() if not value]
    return {
        "passed": not failed,
        "ledger_row_id": (kpi_record or {}).get("ledger_row_id"),
        "record_view": (kpi_record or {}).get("record_view"),
        "checks": checks,
        "failed_checks": failed,
        "metrics": {
            "net_profit": metrics.get("net_profit"),
            "profit_factor": metrics.get("profit_factor"),
            "trade_count": metrics.get("trade_count"),
        },
    }


def _cross_checks(
    source_manifest: Mapping[str, Any],
    source_kpi: Mapping[str, Any],
    model_pack_checks: Mapping[str, Any],
    attempts: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    attempt_names = [str(attempt.get("attempt_name") or "") for attempt in attempts]
    expected = {
        "tier_a_only_validation_is",
        "tier_b_fallback_only_validation_is",
        "routed_validation_is",
        "tier_a_only_oos",
        "tier_b_fallback_only_oos",
        "routed_oos",
    }
    checks = {
        "source_manifest_completed": source_manifest.get("external_verification_status") == "completed",
        "source_kpi_completed": (source_kpi.get("external_verification_status") or nested(source_kpi, ("mt5", "external_verification_status")))
        == "completed",
        "model_pack_passed": bool(model_pack_checks.get("passed")),
        "model_pack_parity_passed": bool(model_pack_checks.get("parity_passed")),
        "six_expected_attempts_present": set(attempt_names) == expected,
        "all_attempts_passed": all(bool(attempt.get("passed")) for attempt in attempts),
    }
    failed = [key for key, value in checks.items() if not value]
    return {"passed": not failed, "checks": checks, "failed_checks": failed, "expected_attempt_names": sorted(expected)}


def _summary(
    source_manifest: Mapping[str, Any],
    source_kpi: Mapping[str, Any],
    model_pack_checks: Mapping[str, Any],
    attempts: Sequence[Mapping[str, Any]],
    cross_checks: Mapping[str, Any],
    blocking_findings: Sequence[str],
) -> dict[str, Any]:
    passed = not blocking_findings
    return {
        "selected_candidate": f"stage12_{SELECTED_SOURCE_RUN_ID}",
        "source_run_id": SELECTED_SOURCE_RUN_ID,
        "source_run_external_status": source_manifest.get("external_verification_status"),
        "source_kpi_external_status": source_kpi.get("external_verification_status")
        or nested(source_kpi, ("mt5", "external_verification_status")),
        "passed": passed,
        "judgment": "inconclusive_mt5_handoff_identity_audit_completed_existing_probe_identity_passed"
        if passed
        else "blocked_mt5_handoff_identity_audit_mismatch",
        "runtime_handoff_decision": "existing_stage12_mt5_probe_identity_linked_to_run27c_model_pack"
        if passed
        else "defer_runtime_handoff_until_identity_mismatch_is_repaired",
        "counts": {
            "attempt_count": len(attempts),
            "attempts_passed": sum(1 for attempt in attempts if attempt.get("passed")),
            "model_pack_tiers_passed": sum(1 for tier in dict(model_pack_checks.get("tiers") or {}).values() if tier.get("passed")),
            "blocking_findings": len(blocking_findings),
        },
        "blocking_findings": list(blocking_findings),
        "required_gates": {
            "evidence_gate": "completed_run27C_signalcard_adapter_probe_consumed",
            "model_pack_hash_gate": "passed" if model_pack_checks.get("passed") else "blocked",
            "mt5_report_hash_gate": "passed"
            if all(bool(nested(attempt, ("strategy_tester_report", "passed"))) for attempt in attempts)
            else "blocked",
            "set_contract_gate": "passed" if all(bool(nested(attempt, ("set_contract", "passed"))) for attempt in attempts) else "blocked",
            "runtime_output_gate": "passed" if all(bool(nested(attempt, ("runtime_outputs", "passed"))) for attempt in attempts) else "blocked",
            "claim_boundary": BOUNDARY,
        },
        "claim_boundary": BOUNDARY,
    }


def _blocking_findings(
    model_pack_checks: Mapping[str, Any],
    attempts: Sequence[Mapping[str, Any]],
    cross_checks: Mapping[str, Any],
) -> list[str]:
    findings: list[str] = []
    if not model_pack_checks.get("passed"):
        findings.append("model_pack_hash_identity_mismatch")
    if not cross_checks.get("passed"):
        findings.extend(f"cross_check_failed:{name}" for name in cross_checks.get("failed_checks", []))
    for attempt in attempts:
        if not attempt.get("passed"):
            findings.append(f"attempt_identity_failed:{attempt.get('attempt_name')}")
    return findings


def _stage_ledger_rows(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    run_root = f"stages/{STAGE_ID}/02_runs/{RUN_ID}"
    status = "completed" if summary["passed"] else "blocked"
    return [
        {
            "ledger_row_id": f"{RUN_ID}__mt5_handoff_identity_report",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "mt5_handoff_identity_report",
            "parent_run_id": RUN_ID,
            "record_view": "MT5_handoff_identity_audit",
            "tier_scope": "Tier A+B",
            "kpi_scope": "runtime_handoff_identity",
            "scoreboard_lane": "runtime_parity",
            "status": status,
            "judgment": summary["judgment"],
            "path": f"{run_root}/mt5_handoff_identity_report.json",
            "primary_kpi": ledger_pairs(
                (
                    ("attempt_count", summary["counts"]["attempt_count"]),
                    ("attempts_passed", summary["counts"]["attempts_passed"]),
                    ("blocking_findings", summary["counts"]["blocking_findings"]),
                )
            ),
            "guardrail_kpi": "model_pack_hash_gate;mt5_report_hash_gate;set_contract_gate;runtime_output_gate",
            "external_verification_status": "referenced_existing_completed" if summary["passed"] else "blocked",
            "notes": "Existing Stage12 MT5 runtime probe identity linked to run27C model pack; no runtime authority claim.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__handoff_identity_matrix",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "handoff_identity_matrix",
            "parent_run_id": RUN_ID,
            "record_view": "handoff_identity_matrix",
            "tier_scope": "Tier A+B",
            "kpi_scope": "artifact_identity",
            "scoreboard_lane": "runtime_parity",
            "status": status,
            "judgment": summary["runtime_handoff_decision"],
            "path": f"{run_root}/handoff_identity_matrix.csv",
            "primary_kpi": ledger_pairs((("attempts_passed", summary["counts"]["attempts_passed"]),)),
            "guardrail_kpi": "hashes_recomputed_from_local_artifacts=true",
            "external_verification_status": "referenced_existing_completed" if summary["passed"] else "blocked",
            "notes": "Matrix records per-attempt .set/.ini/report/runtime-output/ledger identity checks.",
        },
    ]


def _run_registry_row(summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "mt5_handoff_identity_audit",
        "status": "reviewed" if summary["passed"] else "blocked",
        "judgment": summary["judgment"],
        "path": f"stages/{STAGE_ID}/02_runs/{RUN_ID}",
        "notes": ledger_pairs(
            (
                ("selected_candidate", summary["selected_candidate"]),
                ("attempt_count", summary["counts"]["attempt_count"]),
                ("attempts_passed", summary["counts"]["attempts_passed"]),
                ("blocking_findings", summary["counts"]["blocking_findings"]),
                ("boundary", BOUNDARY),
            )
        ),
    }


def _artifact_rows() -> list[dict[str, Any]]:
    run_root = f"stages/{STAGE_ID}/02_runs/{RUN_ID}"
    return [
        {
            "artifact_id": f"{RUN_ID}__mt5_handoff_identity_report",
            "type": "mt5_handoff_identity_report",
            "path": f"{run_root}/mt5_handoff_identity_report.json",
            "status": "tracked_reviewed",
            "notes": "Stage33 run27D audit linking existing Stage12 MT5 probe identity to run27C model pack.",
        },
        {
            "artifact_id": f"{RUN_ID}__handoff_identity_matrix",
            "type": "mt5_handoff_identity_matrix",
            "path": f"{run_root}/handoff_identity_matrix.csv",
            "status": "tracked_reviewed",
            "notes": "Per-attempt artifact and contract identity matrix for Stage12 selected adapter probe.",
        },
    ]


def _manifest(
    root: Path,
    generated_at: str,
    report_path: Path,
    matrix_path: Path,
    result: Mt5HandoffIdentityAuditResult,
) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "packet_id": PACKET_ID,
        "source_run_id": SOURCE_RUN_ID,
        "generated_at_utc": generated_at,
        "producer": "foundation.control_plane.mt5_handoff_identity_audit",
        "outputs": {
            "mt5_handoff_identity_report": {"path": rel(root, report_path), "sha256": sha256_file_lf_normalized(report_path)},
            "handoff_identity_matrix": {"path": rel(root, matrix_path), "sha256": sha256_file_lf_normalized(matrix_path)},
        },
        "summary": result.summary,
        "claim_boundary": BOUNDARY,
    }


def _result_summary_markdown(generated_at: str, result: Mt5HandoffIdentityAuditResult) -> str:
    summary = result.summary
    lines = [
        "# Stage33 RUN27D MT5 Handoff Identity Audit(33단계 실행27D MT5 인계 정체성 감사)",
        "",
        f"- generated_at_utc(생성 시각 UTC): `{generated_at}`",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- source run(원천 실행): `{SELECTED_SOURCE_RUN_ID}`",
        f"- attempts passed(통과 시도): `{summary['counts']['attempts_passed']}/{summary['counts']['attempt_count']}`",
        f"- runtime handoff decision(런타임 인계 결정): `{summary['runtime_handoff_decision']}`",
        f"- judgment(판정): `{summary['judgment']}`",
        "",
        "## Evidence Gate(근거 게이트)",
        "",
        "run27D(27D 실행)는 run27C(27C 실행)의 model pack(모델 팩)이 참조한 Stage12(12단계) MT5 runtime probe(MT5 런타임 탐침)를 다시 실행하지 않고, durable artifact identity(지속 산출물 정체성)를 재계산했다.",
        "",
        "효과(effect, 효과)는 기존 `.set`/`.ini`, Strategy Tester report(전략 테스터 보고서), runtime telemetry(런타임 기록), model pack hash(모델 팩 해시)가 같은 후보를 가리키는지 확인해서 runtime handoff(런타임 인계) 주장의 범위를 좁히는 것이다.",
        "",
        "## Result(결과)",
        "",
        f"- model pack hash gate(모델 팩 해시 게이트): `{summary['required_gates']['model_pack_hash_gate']}`",
        f"- MT5 report hash gate(MT5 보고서 해시 게이트): `{summary['required_gates']['mt5_report_hash_gate']}`",
        f"- set contract gate(설정 계약 게이트): `{summary['required_gates']['set_contract_gate']}`",
        f"- runtime output gate(런타임 출력 게이트): `{summary['required_gates']['runtime_output_gate']}`",
        "",
        "## Explicit Non-Claims(명시적 비주장)",
        "",
        "- alpha quality(알파 품질) 주장 없음",
        "- operating baseline(운영 기준선) 주장 없음",
        "- promotion candidate(승격 후보) 주장 없음",
        "- runtime authority(런타임 권위) 주장 없음",
        "- live readiness(실거래 준비) 주장 없음",
    ]
    if summary["blocking_findings"]:
        lines.extend(["", "## Blockers(차단)", ""])
        lines.extend(f"- `{finding}`" for finding in summary["blocking_findings"])
    return "\n".join(lines) + "\n"


def _execution_results(source_manifest: Mapping[str, Any], source_kpi: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    return list(source_manifest.get("execution_results") or nested(source_kpi, ("mt5", "execution_results")) or [])


def _strategy_tester_reports(source_manifest: Mapping[str, Any], source_kpi: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    return list(source_manifest.get("strategy_tester_reports") or nested(source_kpi, ("mt5", "strategy_tester_reports")) or [])


def _kpi_records(source_kpi: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    return list(nested(source_kpi, ("mt5", "kpi_records")) or source_kpi.get("mt5_records") or [])


def _find_by(rows: Sequence[Mapping[str, Any]], key: str, value: str) -> Mapping[str, Any] | None:
    for row in rows:
        if str(row.get(key) or "") == value:
            return row
    return None


def _find_kpi_record(rows: Sequence[Mapping[str, Any]], attempt_name: str) -> Mapping[str, Any] | None:
    split = "validation_is" if attempt_name.endswith("validation_is") else "oos"
    if attempt_name.startswith("tier_a_only"):
        view = f"mt5_tier_a_only_{split}"
    elif attempt_name.startswith("tier_b_fallback_only"):
        view = f"mt5_tier_b_fallback_only_{split}"
    elif attempt_name.startswith("routed"):
        view = f"mt5_routed_total_{split}"
    else:
        view = attempt_name
    for row in rows:
        if str(row.get("record_view") or "") == view:
            return row
        if str(row.get("record_view") or "").endswith(attempt_name) or str(row.get("ledger_row_id") or "").endswith(attempt_name):
            return row
        if view in str(row.get("record_view") or ""):
            return row
    return None


def _matrix_row(attempt_name: str, check_type: str, payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "attempt_name": attempt_name,
        "check_type": check_type,
        "passed": bool(payload.get("passed")),
        "path": payload.get("path") or payload.get("summary_path") or "",
        "expected_sha256": payload.get("expected_sha256") or "",
        "actual_sha256": payload.get("actual_sha256") or "",
        "failed_checks": ",".join(str(item) for item in payload.get("failed_checks", [])),
        "claim_boundary": BOUNDARY,
    }


def _tier_key(tier: str) -> str:
    if tier == "Tier B":
        return "tier_b"
    return "tier_a"


def _upsert_registers(root: Path, result: Mt5HandoffIdentityAuditResult) -> None:
    upsert_csv_rows(root / "docs/registers/run_registry.csv", RUN_REGISTRY_COLUMNS, [result.run_registry_row], key="run_id")
    upsert_csv_rows(root / "docs/registers/alpha_run_ledger.csv", ALPHA_LEDGER_COLUMNS, result.stage_rows, key="ledger_row_id")
    artifact_path = root / "docs/registers/artifact_registry.csv"
    existing = read_csv_rows(artifact_path)
    columns = ("artifact_id", "type", "path", "status", "notes")
    new_ids = {row["artifact_id"] for row in result.artifact_rows}
    rows = [row for row in existing if row.get("artifact_id") not in new_ids]
    rows.extend(result.artifact_rows)
    write_csv_rows(artifact_path, columns, rows)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Stage33 MT5 handoff identity audit for the selected SignalCard adapter.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args(argv)
    if args.summary_only:
        result = build_mt5_handoff_identity_audit(Path(args.root))
        print(json.dumps(json_ready(result.summary), ensure_ascii=False, indent=2))
        return 0 if result.summary["passed"] else 1
    aggregate = write_mt5_handoff_identity_audit_packet(Path(args.root))
    print(json.dumps(json_ready(aggregate), ensure_ascii=False, indent=2))
    return 0 if aggregate["status"].startswith("reviewed") else 1


if __name__ == "__main__":
    raise SystemExit(main())
