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
from foundation.control_plane.mechanism_role_map import STAGE_ID
from foundation.control_plane.mt5_handoff_identity_helpers import read_json, rel, resolve_path, write_json, write_markdown
from foundation.control_plane.score_table_signalcard_probe import RUN_ID as SOURCE_RUN_ID
from foundation.models.onnx_bridge import sha256_file


RUN_ID = "run27G_score_table_mt5_handoff_identity_audit_v1"
PACKET_ID = "stage33_run27G_score_table_mt5_handoff_identity_audit_v1"
BOUNDARY = "score_table_mt5_handoff_identity_audit_only_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
SELECTED_SOURCE_STAGE_ID = "32_sequence_model__tcn_temporal_convolution_context"
SELECTED_SOURCE_RUN_ID = "run26D_torch_tcn_native_temporal_runtime_probe_v1"
REQUIRE_COMMON_COPIES = True


def configure_score_table_mt5_handoff_identity_audit(
    *,
    run_id: str,
    packet_id: str,
    boundary: str,
    source_run_id: str,
    selected_source_stage_id: str,
    selected_source_run_id: str,
    require_common_copies: bool = True,
) -> None:
    global RUN_ID, PACKET_ID, BOUNDARY, SOURCE_RUN_ID, SELECTED_SOURCE_STAGE_ID, SELECTED_SOURCE_RUN_ID, REQUIRE_COMMON_COPIES
    RUN_ID = run_id
    PACKET_ID = packet_id
    BOUNDARY = boundary
    SOURCE_RUN_ID = source_run_id
    SELECTED_SOURCE_STAGE_ID = selected_source_stage_id
    SELECTED_SOURCE_RUN_ID = selected_source_run_id
    REQUIRE_COMMON_COPIES = bool(require_common_copies)


def current_score_table_mt5_handoff_identity_config() -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "boundary": BOUNDARY,
        "source_run_id": SOURCE_RUN_ID,
        "selected_source_stage_id": SELECTED_SOURCE_STAGE_ID,
        "selected_source_run_id": SELECTED_SOURCE_RUN_ID,
        "require_common_copies": REQUIRE_COMMON_COPIES,
    }


@dataclass(frozen=True)
class ScoreTableMt5HandoffIdentityAuditResult:
    summary: dict[str, Any]
    report: dict[str, Any]
    matrix_rows: list[dict[str, Any]]
    stage_rows: list[dict[str, Any]]
    run_registry_row: dict[str, Any]
    artifact_rows: list[dict[str, Any]]


def build_score_table_mt5_handoff_identity_audit(root: Path | str = Path(".")) -> ScoreTableMt5HandoffIdentityAuditResult:
    root_path = Path(root)
    adapter_pack_path = (
        root_path
        / "stages"
        / STAGE_ID
        / "02_runs"
        / SOURCE_RUN_ID
        / "adapter_pack"
        / "adapter_pack_manifest.json"
    )
    source_run_root = root_path / "stages" / SELECTED_SOURCE_STAGE_ID / "02_runs" / SELECTED_SOURCE_RUN_ID
    adapter_pack = read_json(adapter_pack_path)
    source_manifest = read_json(source_run_root / "run_manifest.json")
    source_kpi = read_json(source_run_root / "kpi_record.json")
    source_summary = _read_json_optional(source_run_root / "summary.json")
    artifact_checks, artifact_rows = _artifact_identity_checks(root_path, adapter_pack, source_manifest)
    attempt_checks, attempt_rows = _attempt_identity_checks(root_path, adapter_pack, source_manifest, source_summary)
    blocking_findings = _blocking_findings(artifact_checks, attempt_checks, source_manifest, source_summary)
    summary = _summary(adapter_pack, source_manifest, source_kpi, source_summary, artifact_checks, attempt_checks, blocking_findings)
    matrix_rows = artifact_rows + attempt_rows
    report = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "selected_source_run_id": SELECTED_SOURCE_RUN_ID,
        "selected_source_stage_id": SELECTED_SOURCE_STAGE_ID,
        "summary": summary,
        "adapter_pack_identity": {
            "path": rel(root_path, adapter_pack_path),
            "sha256_lf_normalized": sha256_file_lf_normalized(adapter_pack_path),
            "adapter_pack_id": adapter_pack.get("adapter_pack_id"),
        },
        "source_manifest_identity": {
            "path": rel(root_path, source_run_root / "run_manifest.json"),
            "sha256_lf_normalized": sha256_file_lf_normalized(source_run_root / "run_manifest.json"),
            "external_verification_status": source_manifest.get("external_verification_status"),
            "judgment": source_manifest.get("judgment"),
        },
        "artifact_checks": artifact_checks,
        "attempt_checks": attempt_checks,
        "blocking_findings": blocking_findings,
        "claim_boundary": BOUNDARY,
    }
    return ScoreTableMt5HandoffIdentityAuditResult(
        summary=summary,
        report=report,
        matrix_rows=matrix_rows,
        stage_rows=_stage_ledger_rows(summary),
        run_registry_row=_run_registry_row(summary),
        artifact_rows=_artifact_rows(),
    )


def write_score_table_mt5_handoff_identity_audit_packet(
    root: Path | str = Path("."),
    *,
    generated_at_utc: str | None = None,
) -> dict[str, Any]:
    root_path = Path(root)
    generated_at = generated_at_utc or datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    result = build_score_table_mt5_handoff_identity_audit(root_path)
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
    _write_matrix_csv(matrix_path, result.matrix_rows)
    manifest = _manifest(root_path, generated_at, report_path, matrix_path, result)
    write_json(manifest_path, manifest)
    write_markdown(result_summary_path, _result_summary_markdown(generated_at, result))
    aggregate = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "status": "reviewed_score_table_mt5_handoff_identity_audit_completed"
        if result.summary["passed"]
        else "blocked_score_table_mt5_handoff_identity_audit",
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


def _artifact_identity_checks(
    root: Path,
    adapter_pack: Mapping[str, Any],
    source_manifest: Mapping[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    tier_checks: dict[str, Any] = {}
    common_lookup = {str(item.get("source") or "").replace("\\", "/"): item for item in source_manifest.get("common_copies") or []}
    source_artifacts = dict(source_manifest.get("model_artifacts") or {})
    for tier_name, tier_payload in dict(adapter_pack.get("tiers") or {}).items():
        checks: list[bool] = []
        tier_result: dict[str, Any] = {"feature_order_hash": tier_payload.get("feature_order_hash")}
        table_payload = dict(tier_payload["score_table"])
        table_path = root / str(table_payload["path"])
        source_table_key = "tier_a_score_table" if tier_name == "tier_a" else "tier_b_score_table"
        source_table_payload = dict(source_artifacts.get(source_table_key) or {})
        table_check = _hash_check(root, table_path, str(table_payload.get("sha256") or ""), "sha256")
        table_check["matches_source_manifest_sha"] = table_check["actual_sha256"] == source_table_payload.get("sha256")
        checks.append(bool(table_check["passed"] and table_check["matches_source_manifest_sha"]))
        rows.append(_matrix_row(tier_name, "score_table_repo_hash", table_check["passed"], table_path, table_check))
        common_table = _common_copy_check(root, common_lookup, str(table_payload["path"]))
        checks.append(bool(common_table["passed"]))
        rows.append(_matrix_row(tier_name, "score_table_common_copy_hash", common_table["passed"], Path(str(common_table["path"] or "")), common_table))
        tier_result["score_table"] = {**table_check, "common_copy": common_table}

        matrix_checks: dict[str, Any] = {}
        for split_name, matrix_payload in dict(tier_payload.get("feature_matrices") or {}).items():
            matrix_path = root / str(matrix_payload["path"])
            matrix_check = _hash_check(root, matrix_path, str(matrix_payload.get("sha256_lf_normalized") or ""), "sha256_lf_normalized")
            checks.append(bool(matrix_check["passed"]))
            rows.append(_matrix_row(tier_name, f"{split_name}_feature_matrix_repo_hash", matrix_check["passed"], matrix_path, matrix_check))
            common_matrix = _common_copy_check(root, common_lookup, str(matrix_payload["path"]))
            checks.append(bool(common_matrix["passed"]))
            rows.append(_matrix_row(tier_name, f"{split_name}_feature_matrix_common_copy_hash", common_matrix["passed"], Path(str(common_matrix["path"] or "")), common_matrix))
            matrix_checks[split_name] = {**matrix_check, "common_copy": common_matrix}
        prediction_path = root / str(tier_payload["prediction_path"])
        prediction_check = _hash_check(root, prediction_path, str(tier_payload.get("prediction_sha256") or ""), "sha256")
        checks.append(bool(prediction_check["passed"]))
        rows.append(_matrix_row(tier_name, "prediction_repo_hash", prediction_check["passed"], prediction_path, prediction_check))
        tier_result["feature_matrices"] = matrix_checks
        tier_result["prediction"] = prediction_check
        tier_result["passed"] = all(checks)
        tier_checks[tier_name] = tier_result
    return {"tiers": tier_checks, "passed": all(bool(item["passed"]) for item in tier_checks.values())}, rows


def _attempt_identity_checks(
    root: Path,
    adapter_pack: Mapping[str, Any],
    source_manifest: Mapping[str, Any],
    source_summary: Mapping[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    source_runtime_probe = dict(source_manifest.get("runtime_probe") or {})
    attempts_by_name = {
        str(item.get("attempt_name")): item
        for item in (source_manifest.get("attempts") or source_runtime_probe.get("attempts") or source_summary.get("expected_attempts") or [])
    }
    expected_feature_hashes = {str(tier.get("feature_order_hash")) for tier in dict(adapter_pack.get("tiers") or {}).values()}
    expected_model_ids = _expected_model_ids(source_manifest, source_summary)
    attempt_payloads: list[dict[str, Any]] = []
    executions = source_manifest.get("execution_results") or source_runtime_probe.get("execution_results") or source_summary.get("execution_results") or []
    for execution in executions:
        attempt_name = str(execution.get("attempt_name") or "")
        attempt = attempts_by_name.get(attempt_name, {})
        runtime_outputs = dict(execution.get("runtime_outputs") or {})
        last_summary = dict(runtime_outputs.get("last_summary") or {})
        ini_payload = dict(attempt.get("ini") or {})
        ini_path = resolve_path(root, str(execution.get("ini_path") or ini_payload.get("path") or ""))
        checks = {
            "returncode_zero": execution.get("returncode") == 0,
            "runtime_status_completed": runtime_outputs.get("status") == "completed",
            "summary_exists_flag": bool(runtime_outputs.get("summary_exists")),
            "telemetry_exists_flag": bool(runtime_outputs.get("telemetry_exists")),
            "summary_path_exists": _path_exists(runtime_outputs.get("summary_path")),
            "telemetry_path_exists": _path_exists(runtime_outputs.get("telemetry_path")),
            "last_summary_run_id_matches": last_summary.get("run_id") == SELECTED_SOURCE_RUN_ID,
            "feature_order_hash_matches": last_summary.get("feature_order_hash") in expected_feature_hashes,
            "model_id_expected": last_summary.get("model_id") in expected_model_ids,
            "feature_ready_positive": _as_int(last_summary.get("feature_ready_count")) > 0,
            "orders_filled_equal_attempted": _as_int(last_summary.get("order_fill_count")) == _as_int(last_summary.get("order_attempt_count")),
        }
        if ini_path is not None:
            ini_hash = _matching_text_or_raw_hash(ini_path, str(ini_payload.get("sha256") or "")) if io_path(ini_path).exists() else None
            checks["ini_exists"] = io_path(ini_path).exists()
            checks["ini_hash_matches_manifest"] = ini_hash == ini_payload.get("sha256")
        else:
            checks["ini_exists"] = False
            checks["ini_hash_matches_manifest"] = False
        passed = all(bool(value) for value in checks.values())
        payload = {
            "attempt_name": attempt_name,
            "attempt_role": execution.get("attempt_role"),
            "checks": checks,
            "last_summary": {
                key: last_summary.get(key)
                for key in (
                    "run_id",
                    "model_id",
                    "feature_order_hash",
                    "feature_ready_count",
                    "order_attempt_count",
                    "order_fill_count",
                    "short_count",
                    "flat_count",
                    "long_count",
                )
            },
            "ini_path": rel(root, ini_path) if ini_path else None,
            "summary_path": runtime_outputs.get("summary_path"),
            "telemetry_path": runtime_outputs.get("telemetry_path"),
            "passed": passed,
        }
        attempt_payloads.append(payload)
        for check_name, value in checks.items():
            rows.append(
                {
                    "subject": attempt_name,
                    "check_type": check_name,
                    "passed": bool(value),
                    "path": payload["ini_path"] if check_name.startswith("ini") else "",
                    "expected_sha256": ini_payload.get("sha256") if check_name == "ini_hash_matches_manifest" else "",
                    "actual_sha256": _matching_text_or_raw_hash(ini_path, str(ini_payload.get("sha256") or ""))
                    if ini_path and check_name == "ini_hash_matches_manifest" and io_path(ini_path).exists()
                    else "",
                    "failed_checks": "" if value else check_name,
                    "claim_boundary": BOUNDARY,
                }
            )
    return {
        "attempts": attempt_payloads,
        "attempt_count": len(attempt_payloads),
        "attempts_passed": sum(1 for item in attempt_payloads if item["passed"]),
        "passed": bool(attempt_payloads) and all(bool(item["passed"]) for item in attempt_payloads),
    }, rows


def _expected_model_ids(source_manifest: Mapping[str, Any], source_summary: Mapping[str, Any]) -> set[str]:
    model_family = str(source_manifest.get("model_family") or source_summary.get("model_family") or "")
    if "quantile_boosting_tail" in model_family:
        return {
            f"{SELECTED_SOURCE_RUN_ID}_tier_a_quantile_tail_table",
            f"{SELECTED_SOURCE_RUN_ID}_tier_b_quantile_tail_table",
        }
    return {
        f"{SELECTED_SOURCE_RUN_ID}_tier_a_score_table",
        f"{SELECTED_SOURCE_RUN_ID}_tier_b_score_table",
    }


def _hash_check(root: Path, path: Path, expected_hash: str, hash_type: str) -> dict[str, Any]:
    exists = io_path(path).exists()
    if not exists:
        actual = None
    elif hash_type == "sha256_lf_normalized":
        actual = sha256_file_lf_normalized(path)
    else:
        actual = sha256_file(path)
    return {
        "path": rel(root, path),
        f"expected_{hash_type}": expected_hash,
        f"actual_{hash_type}": actual,
        "exists": exists,
        "passed": exists and actual == expected_hash,
    }


def _read_json_optional(path: Path) -> dict[str, Any]:
    if not io_path(path).exists():
        return {}
    return read_json(path)


def _common_copy_check(root: Path, common_lookup: Mapping[str, Mapping[str, Any]], source_path: str) -> dict[str, Any]:
    copy = common_lookup.get(source_path.replace("\\", "/"))
    if not copy:
        if not REQUIRE_COMMON_COPIES:
            return {"path": None, "exists": False, "passed": True, "reason": "source_manifest_has_no_common_copy_manifest_not_required"}
        return {"path": None, "exists": False, "passed": False, "reason": "missing_common_copy_manifest_row"}
    absolute = Path(str(copy.get("absolute_path") or ""))
    exists = io_path(absolute).exists()
    expected = str(copy.get("sha256") or "")
    actual = _matching_text_or_raw_hash(absolute, expected) if exists else None
    return {
        "path": rel(root, absolute),
        "expected_sha256": expected,
        "actual_sha256": actual,
        "exists": exists,
        "passed": exists and actual == expected,
    }


def _matrix_row(subject: str, check_type: str, passed: bool, path: Path, payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "subject": subject,
        "check_type": check_type,
        "passed": bool(passed),
        "path": payload.get("path") or path.as_posix(),
        "expected_sha256": payload.get("expected_sha256") or payload.get("expected_sha256_lf_normalized") or payload.get("expected_sha256"),
        "actual_sha256": payload.get("actual_sha256") or payload.get("actual_sha256_lf_normalized") or payload.get("actual_sha256"),
        "failed_checks": "" if passed else check_type,
        "claim_boundary": BOUNDARY,
    }


def _blocking_findings(
    artifact_checks: Mapping[str, Any],
    attempt_checks: Mapping[str, Any],
    source_manifest: Mapping[str, Any],
    source_summary: Mapping[str, Any],
) -> list[str]:
    findings: list[str] = []
    if not artifact_checks.get("passed"):
        findings.append("adapter_pack_artifact_identity_failed")
    if not attempt_checks.get("passed"):
        findings.append("mt5_runtime_attempt_identity_failed")
    external_status = source_manifest.get("external_verification_status") or source_summary.get("external_verification_status")
    if external_status != "completed":
        findings.append("source_mt5_external_verification_not_completed")
    return findings


def _summary(
    adapter_pack: Mapping[str, Any],
    source_manifest: Mapping[str, Any],
    source_kpi: Mapping[str, Any],
    source_summary: Mapping[str, Any],
    artifact_checks: Mapping[str, Any],
    attempt_checks: Mapping[str, Any],
    blocking_findings: Sequence[str],
) -> dict[str, Any]:
    passed = not blocking_findings
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "selected_source_run_id": SELECTED_SOURCE_RUN_ID,
        "adapter_pack_id": adapter_pack.get("adapter_pack_id"),
        "passed": passed,
        "judgment": "inconclusive_score_table_mt5_handoff_identity_audit_completed" if passed else "blocked_score_table_mt5_handoff_identity_audit",
        "counts": {
            "tier_count": len((adapter_pack.get("tiers") or {})),
            "attempt_count": attempt_checks.get("attempt_count", 0),
            "attempts_passed": attempt_checks.get("attempts_passed", 0),
            "blocking_findings": len(blocking_findings),
        },
        "source_mt5_external_verification_status": source_manifest.get("external_verification_status")
        or source_kpi.get("external_verification_status")
        or source_summary.get("external_verification_status"),
        "runtime_handoff_decision": _runtime_handoff_decision(passed),
        "blocking_findings": list(blocking_findings),
        "claim_boundary": BOUNDARY,
        "required_gates": {
            "research_path": "foundation.adapters.score_table_signal_adapter; foundation.control_plane.score_table_signalcard_probe",
            "runtime_path": f"foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.ex5 and {SELECTED_SOURCE_RUN_ID} tester ini/runtime telemetry",
            "shared_contract": "runtime_feature_order_hash, score-table hashes, feature matrices, SignalCard output",
            "known_differences": (source_manifest.get("model_artifacts") or {}).get("known_runtime_difference")
            or "existing MT5 runtime probe is score-table handoff, not source-native runtime",
            "parity_check": "adapter pack hash identity plus existing MT5 runtime output identity",
            "parity_identity": "adapter pack, source score tables, common files, ini files, telemetry summaries",
            "runtime_claim_boundary": "runtime_probe_identity_reference_not_runtime_authority",
        },
    }


def _runtime_handoff_decision(passed: bool) -> str:
    if (
        SOURCE_RUN_ID == "run27F_score_table_signalcard_adapter_probe_v1"
        and SELECTED_SOURCE_RUN_ID == "run26D_torch_tcn_native_temporal_runtime_probe_v1"
    ):
        return (
            "existing_stage32_mt5_probe_identity_linked_to_run27f_score_table_adapter_pack"
            if passed
            else "blocked_existing_stage32_mt5_probe_identity_not_linked"
        )
    if passed:
        return f"existing_{SELECTED_SOURCE_STAGE_ID}_mt5_probe_identity_linked_to_{SOURCE_RUN_ID}_score_table_adapter_pack"
    return f"blocked_existing_{SELECTED_SOURCE_STAGE_ID}_mt5_probe_identity_not_linked"


def _stage_ledger_rows(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    run_root = f"stages/{STAGE_ID}/02_runs/{RUN_ID}"
    return [
        {
            "ledger_row_id": f"{RUN_ID}__adapter_pack_identity",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "adapter_pack_identity",
            "parent_run_id": RUN_ID,
            "record_view": "score_table_adapter_pack_identity",
            "tier_scope": "Tier A+B",
            "kpi_scope": "artifact_lineage",
            "scoreboard_lane": "runtime_parity",
            "status": "completed" if summary["passed"] else "blocked",
            "judgment": summary["judgment"],
            "path": f"{run_root}/mt5_handoff_identity_report.json",
            "primary_kpi": ledger_pairs((("tier_count", summary["counts"]["tier_count"]),)),
            "guardrail_kpi": "hash_identity_required=true",
            "external_verification_status": "referenced_existing_completed",
            "notes": f"{SOURCE_RUN_ID} adapter pack score tables, feature matrices, predictions, and available common-file copies are checked.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__mt5_runtime_identity",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "mt5_runtime_identity",
            "parent_run_id": RUN_ID,
            "record_view": "score_table_mt5_runtime_handoff_identity",
            "tier_scope": "Tier A+B routed",
            "kpi_scope": "runtime_parity",
            "scoreboard_lane": "runtime_parity",
            "status": "completed" if summary["passed"] else "blocked",
            "judgment": summary["runtime_handoff_decision"],
            "path": f"{run_root}/handoff_identity_matrix.csv",
            "primary_kpi": ledger_pairs(
                (
                    ("attempt_count", summary["counts"]["attempt_count"]),
                    ("attempts_passed", summary["counts"]["attempts_passed"]),
                )
            ),
            "guardrail_kpi": "runtime_authority=false;new_terminal_run=false",
            "external_verification_status": "referenced_existing_completed",
            "notes": f"Existing {SELECTED_SOURCE_RUN_ID} MT5 runtime probe identity is linked to the {SOURCE_RUN_ID} score-table adapter pack.",
        },
    ]


def _run_registry_row(summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "score_table_mt5_handoff_identity_audit",
        "status": "reviewed" if summary["passed"] else "blocked",
        "judgment": summary["judgment"],
        "path": f"stages/{STAGE_ID}/02_runs/{RUN_ID}",
        "notes": ledger_pairs(
            (
                ("source_run_id", SOURCE_RUN_ID),
                ("selected_source_run_id", SELECTED_SOURCE_RUN_ID),
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
            "type": "score_table_mt5_handoff_identity_report",
            "path": f"{run_root}/mt5_handoff_identity_report.json",
            "status": "tracked_reviewed",
            "notes": f"Identity audit linking {SOURCE_RUN_ID} score-table adapter pack to existing {SELECTED_SOURCE_RUN_ID} MT5 runtime evidence.",
        },
        {
            "artifact_id": f"{RUN_ID}__handoff_identity_matrix",
            "type": "score_table_handoff_identity_matrix",
            "path": f"{run_root}/handoff_identity_matrix.csv",
            "status": "tracked_reviewed",
            "notes": "Per-artifact and per-attempt handoff identity checks.",
        },
        {
            "artifact_id": f"{RUN_ID}__result_summary",
            "type": "result_summary",
            "path": f"{run_root}/reports/result_summary.md",
            "status": "tracked_reviewed",
            "notes": "Human readout for run27G score-table MT5 handoff identity audit.",
        },
    ]


def _manifest(root: Path, generated_at: str, report_path: Path, matrix_path: Path, result: ScoreTableMt5HandoffIdentityAuditResult) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "packet_id": PACKET_ID,
        "source_run_id": SOURCE_RUN_ID,
        "generated_at_utc": generated_at,
        "producer": "foundation.control_plane.score_table_mt5_handoff_identity_audit",
        "outputs": {
            "mt5_handoff_identity_report": {"path": rel(root, report_path), "sha256": sha256_file_lf_normalized(report_path)},
            "handoff_identity_matrix": {"path": rel(root, matrix_path), "sha256": sha256_file_lf_normalized(matrix_path)},
        },
        "claim_boundary": BOUNDARY,
        "passed": result.summary["passed"],
    }


def _result_summary_markdown(generated_at: str, result: ScoreTableMt5HandoffIdentityAuditResult) -> str:
    summary = result.summary
    lines = [
        f"# Stage33 {RUN_ID} Score-Table MT5 Handoff Identity Audit(33단계 {RUN_ID} 점수표 MT5 인계 정체성 감사)",
        "",
        f"- generated_at_utc(생성 시각 UTC): `{generated_at}`",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- source_run_id(원천 실행 ID): `{SOURCE_RUN_ID}`",
        f"- selected_source_run_id(선택 원천 실행 ID): `{SELECTED_SOURCE_RUN_ID}`",
        f"- passed(통과): `{summary['passed']}`",
        f"- attempts passed(통과 시도): `{summary['counts']['attempts_passed']}/{summary['counts']['attempt_count']}`",
        f"- runtime handoff decision(런타임 인계 결정): `{summary['runtime_handoff_decision']}`",
        "",
        f"효과(effect, 효과)는 {SOURCE_RUN_ID}(원천 실행)의 score-table adapter pack(점수표 어댑터 팩)이 기존 {SELECTED_SOURCE_RUN_ID}(선택 원천 실행) MT5 runtime probe(MT5 런타임 탐침) 산출물과 같은 정체성(identity, 정체성)을 갖는지 확인하는 것이다.",
        "",
        "## Explicit Non-Claims(명시적 비주장)",
        "",
        "- alpha quality(알파 품질) 주장 없음",
        "- operating baseline(운영 기준선) 주장 없음",
        "- promotion candidate(승격 후보) 주장 없음",
        "- runtime authority(런타임 권위) 주장 없음",
        "- live readiness(실거래 준비) 주장 없음",
    ]
    return "\n".join(lines) + "\n"


def _write_matrix_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    columns = ("subject", "check_type", "passed", "path", "expected_sha256", "actual_sha256", "failed_checks", "claim_boundary")
    write_csv_rows(path, columns, rows)


def _upsert_registers(root: Path, result: ScoreTableMt5HandoffIdentityAuditResult) -> None:
    upsert_csv_rows(root / "docs/registers/run_registry.csv", RUN_REGISTRY_COLUMNS, [result.run_registry_row], key="run_id")
    upsert_csv_rows(root / "docs/registers/alpha_run_ledger.csv", ALPHA_LEDGER_COLUMNS, result.stage_rows, key="ledger_row_id")
    artifact_path = root / "docs/registers/artifact_registry.csv"
    existing = read_csv_rows(artifact_path)
    columns = ("artifact_id", "type", "path", "status", "notes")
    new_ids = {row["artifact_id"] for row in result.artifact_rows}
    rows = [row for row in existing if row.get("artifact_id") not in new_ids]
    rows.extend(result.artifact_rows)
    write_csv_rows(artifact_path, columns, rows)


def _path_exists(value: Any) -> bool:
    if not value:
        return False
    return io_path(Path(str(value))).exists()


def _matching_text_or_raw_hash(path: Path, expected_hash: str) -> str | None:
    raw_hash = sha256_file(path)
    if raw_hash == expected_hash:
        return raw_hash
    lf_hash = sha256_file_lf_normalized(path)
    if lf_hash == expected_hash:
        return lf_hash
    return raw_hash


def _as_int(value: Any) -> int:
    try:
        return int(float(str(value)))
    except (TypeError, ValueError):
        return -1


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Stage33 score-table MT5 handoff identity audit.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args(argv)
    if args.summary_only:
        result = build_score_table_mt5_handoff_identity_audit(Path(args.root))
        print(json.dumps(json_ready(result.summary), ensure_ascii=False, indent=2))
    else:
        aggregate = write_score_table_mt5_handoff_identity_audit_packet(Path(args.root))
        print(json.dumps(json_ready(aggregate), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
