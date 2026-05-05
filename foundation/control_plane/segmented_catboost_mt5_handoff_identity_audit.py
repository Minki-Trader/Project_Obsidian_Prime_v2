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
from foundation.control_plane.segmented_catboost_onnx_signalcard_probe import RUN_ID as SOURCE_RUN_ID
from foundation.models.onnx_bridge import sha256_file


RUN_ID = "run27I_segmented_catboost_mt5_handoff_identity_audit_v1"
PACKET_ID = "stage33_run27I_segmented_catboost_mt5_handoff_identity_audit_v1"
BOUNDARY = "segmented_catboost_mt5_handoff_identity_audit_only_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
SELECTED_SOURCE_STAGE_ID = "18_model_family_challenge__catboost_ordered_boosting_scout"
SELECTED_SOURCE_RUN_ID = "run12G_catboost_probability_calibration_probe_v1"


def configure_segmented_catboost_mt5_handoff_identity_audit(
    *,
    run_id: str,
    packet_id: str,
    boundary: str,
    source_run_id: str,
    selected_source_run_id: str,
) -> None:
    global RUN_ID, PACKET_ID, BOUNDARY, SOURCE_RUN_ID, SELECTED_SOURCE_RUN_ID
    RUN_ID = run_id
    PACKET_ID = packet_id
    BOUNDARY = boundary
    SOURCE_RUN_ID = source_run_id
    SELECTED_SOURCE_RUN_ID = selected_source_run_id


def current_segmented_catboost_mt5_handoff_identity_config() -> dict[str, str]:
    return {
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "boundary": BOUNDARY,
        "source_run_id": SOURCE_RUN_ID,
        "selected_source_run_id": SELECTED_SOURCE_RUN_ID,
    }


@dataclass(frozen=True)
class SegmentedCatBoostMt5HandoffIdentityAuditResult:
    summary: dict[str, Any]
    report: dict[str, Any]
    matrix_rows: list[dict[str, Any]]
    stage_rows: list[dict[str, Any]]
    run_registry_row: dict[str, Any]
    artifact_rows: list[dict[str, Any]]


def build_segmented_catboost_mt5_handoff_identity_audit(root: Path | str = Path(".")) -> SegmentedCatBoostMt5HandoffIdentityAuditResult:
    root_path = Path(root)
    model_pack_path = (
        root_path
        / "stages"
        / STAGE_ID
        / "02_runs"
        / SOURCE_RUN_ID
        / "model_pack"
        / "model_pack_manifest.json"
    )
    source_run_root = root_path / "stages" / SELECTED_SOURCE_STAGE_ID / "02_runs" / SELECTED_SOURCE_RUN_ID
    model_pack = read_json(model_pack_path)
    source_manifest = read_json(source_run_root / "run_manifest.json")
    source_summary = read_json(source_run_root / "summary.json")
    artifact_checks, artifact_rows = _artifact_identity_checks(root_path, model_pack, source_manifest)
    attempt_checks, attempt_rows = _attempt_identity_checks(root_path, model_pack, source_manifest)
    blocking_findings = _blocking_findings(artifact_checks, attempt_checks, source_manifest, source_summary)
    summary = _summary(model_pack, source_manifest, source_summary, artifact_checks, attempt_checks, blocking_findings)
    matrix_rows = artifact_rows + attempt_rows
    report = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "selected_source_run_id": SELECTED_SOURCE_RUN_ID,
        "selected_source_stage_id": SELECTED_SOURCE_STAGE_ID,
        "summary": summary,
        "model_pack_identity": {
            "path": rel(root_path, model_pack_path),
            "sha256_lf_normalized": sha256_file_lf_normalized(model_pack_path),
            "model_pack_id": model_pack.get("model_pack_id"),
        },
        "source_manifest_identity": {
            "path": rel(root_path, source_run_root / "run_manifest.json"),
            "sha256_lf_normalized": sha256_file_lf_normalized(source_run_root / "run_manifest.json"),
            "runtime_probe_external_verification_status": (source_manifest.get("runtime_probe") or {}).get("external_verification_status"),
            "judgment": (source_manifest.get("runtime_probe") or {}).get("judgment"),
        },
        "artifact_checks": artifact_checks,
        "attempt_checks": attempt_checks,
        "blocking_findings": blocking_findings,
        "claim_boundary": BOUNDARY,
    }
    return SegmentedCatBoostMt5HandoffIdentityAuditResult(
        summary=summary,
        report=report,
        matrix_rows=matrix_rows,
        stage_rows=_stage_ledger_rows(summary),
        run_registry_row=_run_registry_row(summary),
        artifact_rows=_artifact_rows(),
    )


def write_segmented_catboost_mt5_handoff_identity_audit_packet(
    root: Path | str = Path("."),
    *,
    generated_at_utc: str | None = None,
) -> dict[str, Any]:
    root_path = Path(root)
    generated_at = generated_at_utc or datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    result = build_segmented_catboost_mt5_handoff_identity_audit(root_path)
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
        "status": "reviewed_segmented_catboost_mt5_handoff_identity_audit_completed"
        if result.summary["passed"]
        else "blocked_segmented_catboost_mt5_handoff_identity_audit",
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
        "warning_findings": result.summary["warning_findings"],
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
    model_pack: Mapping[str, Any],
    source_manifest: Mapping[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    runtime_probe = dict(source_manifest.get("runtime_probe") or {})
    common_lookup = {str(item.get("source") or "").replace("\\", "/"): item for item in runtime_probe.get("common_copies") or []}
    rows: list[dict[str, Any]] = []
    checks: dict[str, Any] = {"segments": {}, "warning_findings": []}
    all_passed: list[bool] = []
    for segment_key, segment_payload in dict(model_pack.get("segments") or {}).items():
        segment_result: dict[str, Any] = {"tiers": {}}
        for tier_name, tier_payload in dict(segment_payload.get("tiers") or {}).items():
            tier_checks: list[bool] = []
            tier_result: dict[str, Any] = {}
            for artifact_key, hash_kind in (
                ("source_model", "sha256"),
                ("onnx_model", "sha256"),
                ("feature_matrix", "sha256_lf_normalized"),
            ):
                payload = dict(tier_payload[artifact_key])
                path = root / str(payload["path"])
                repo_check = _hash_check(root, path, str(payload.get(hash_kind) or ""), hash_kind)
                tier_checks.append(bool(repo_check["passed"]))
                rows.append(_matrix_row(f"{segment_key}:{tier_name}", f"{artifact_key}_repo_hash", repo_check["passed"], repo_check))
                tier_result[artifact_key] = {"repo": repo_check}
                if artifact_key in {"onnx_model", "feature_matrix"}:
                    common_check = _common_copy_current_check(root, common_lookup, str(payload["path"]), str(payload.get(hash_kind) or ""))
                    common_manifest_warning = bool(common_check.get("manifest_expected_sha256") and common_check["actual_sha256"] != common_check["manifest_expected_sha256"])
                    if common_manifest_warning:
                        checks["warning_findings"].append(
                            f"{segment_key}:{tier_name}:{artifact_key}:source_common_copy_manifest_hash_drift"
                        )
                    tier_checks.append(bool(common_check["passed_current_pack_hash"]))
                    rows.append(
                        _matrix_row(
                            f"{segment_key}:{tier_name}",
                            f"{artifact_key}_common_current_matches_model_pack",
                            common_check["passed_current_pack_hash"],
                            common_check,
                        )
                    )
                    tier_result[artifact_key]["common_current"] = common_check
            tier_result["passed"] = all(tier_checks)
            all_passed.extend(tier_checks)
            segment_result["tiers"][tier_name] = tier_result
        checks["segments"][segment_key] = segment_result
    checks["passed"] = bool(all_passed) and all(all_passed)
    return checks, rows


def _attempt_identity_checks(
    root: Path,
    model_pack: Mapping[str, Any],
    source_manifest: Mapping[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    runtime_probe = dict(source_manifest.get("runtime_probe") or {})
    attempts_by_name = {str(item.get("attempt_name")): item for item in runtime_probe.get("attempts") or []}
    expected_feature_hashes = {
        str(tier.get("feature_order_hash"))
        for segment in dict(model_pack.get("segments") or {}).values()
        for tier in dict(segment.get("tiers") or {}).values()
    }
    expected_model_ids = {f"{SELECTED_SOURCE_RUN_ID}_tier_a", f"{SELECTED_SOURCE_RUN_ID}_tier_b"}
    rows: list[dict[str, Any]] = []
    attempts: list[dict[str, Any]] = []
    for execution in runtime_probe.get("execution_results") or []:
        attempt_name = str(execution.get("attempt_name") or "")
        attempt = attempts_by_name.get(attempt_name, {})
        runtime_outputs = dict(execution.get("runtime_outputs") or {})
        last_summary = dict(runtime_outputs.get("last_summary") or {})
        ini_payload = dict(attempt.get("ini") or {})
        set_payload = dict(attempt.get("set") or {})
        report_payload = dict(execution.get("strategy_tester_report") or {})
        checks = {
            "returncode_zero": execution.get("returncode") == 0,
            "execution_status_completed": execution.get("status") == "completed",
            "runtime_status_completed": runtime_outputs.get("status") == "completed",
            "summary_path_exists": _path_exists(runtime_outputs.get("summary_path")),
            "telemetry_path_exists": _path_exists(runtime_outputs.get("telemetry_path")),
            "summary_hash_matches": _path_hash_matches(runtime_outputs.get("summary_path"), runtime_outputs.get("summary_sha256")),
            "telemetry_hash_matches": _path_hash_matches(runtime_outputs.get("telemetry_path"), runtime_outputs.get("telemetry_sha256")),
            "last_summary_run_id_matches": last_summary.get("run_id") == SELECTED_SOURCE_RUN_ID,
            "feature_order_hash_matches": last_summary.get("feature_order_hash") in expected_feature_hashes,
            "model_id_expected": last_summary.get("model_id") in expected_model_ids,
            "feature_ready_positive": _as_int(last_summary.get("feature_ready_count")) > 0,
            "orders_filled_equal_attempted": _as_int(last_summary.get("order_fill_count")) == _as_int(last_summary.get("order_attempt_count")),
            "ini_hash_matches": _path_hash_matches(ini_payload.get("path"), ini_payload.get("sha256")),
            "set_hash_matches": _path_hash_matches(set_payload.get("path"), set_payload.get("sha256")),
            "html_report_hash_matches": _payload_hash_matches(report_payload.get("html_report")),
            "chart_hash_matches": _payload_hash_matches(report_payload.get("chart")),
        }
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
            "passed": passed,
        }
        attempts.append(payload)
        for check_name, value in checks.items():
            rows.append(
                {
                    "subject": attempt_name,
                    "check_type": check_name,
                    "passed": bool(value),
                    "path": "",
                    "expected_sha256": "",
                    "actual_sha256": "",
                    "failed_checks": "" if value else check_name,
                    "claim_boundary": BOUNDARY,
                }
            )
    return {
        "attempts": attempts,
        "attempt_count": len(attempts),
        "attempts_passed": sum(1 for item in attempts if item["passed"]),
        "passed": bool(attempts) and all(bool(item["passed"]) for item in attempts),
    }, rows


def _hash_check(root: Path, path: Path, expected_hash: str, hash_kind: str) -> dict[str, Any]:
    exists = io_path(path).exists()
    actual = None
    if exists:
        actual = sha256_file_lf_normalized(path) if hash_kind == "sha256_lf_normalized" else sha256_file(path)
    return {
        "path": rel(root, path),
        f"expected_{hash_kind}": expected_hash,
        f"actual_{hash_kind}": actual,
        "exists": exists,
        "passed": exists and actual == expected_hash,
    }


def _common_copy_current_check(root: Path, common_lookup: Mapping[str, Mapping[str, Any]], source_path: str, expected_pack_hash: str) -> dict[str, Any]:
    copy = common_lookup.get(source_path.replace("\\", "/"))
    if not copy:
        return {"path": None, "exists": False, "passed_current_pack_hash": False, "reason": "missing_common_copy_manifest_row"}
    absolute = Path(str(copy.get("absolute_path") or ""))
    exists = io_path(absolute).exists()
    actual = _matching_text_or_raw_hash(absolute, expected_pack_hash) if exists else None
    return {
        "path": rel(root, absolute),
        "manifest_expected_sha256": copy.get("sha256"),
        "expected_pack_hash": expected_pack_hash,
        "actual_sha256": actual,
        "exists": exists,
        "passed_current_pack_hash": exists and actual == expected_pack_hash,
    }


def _matrix_row(subject: str, check_type: str, passed: bool, payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "subject": subject,
        "check_type": check_type,
        "passed": bool(passed),
        "path": payload.get("path") or "",
        "expected_sha256": payload.get("expected_sha256")
        or payload.get("expected_sha256_lf_normalized")
        or payload.get("expected_pack_hash")
        or "",
        "actual_sha256": payload.get("actual_sha256") or payload.get("actual_sha256_lf_normalized") or "",
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
    runtime_probe = dict(source_manifest.get("runtime_probe") or {})
    if not artifact_checks.get("passed"):
        findings.append("model_pack_artifact_identity_failed")
    if not attempt_checks.get("passed"):
        findings.append("mt5_runtime_attempt_identity_failed")
    if (runtime_probe.get("external_verification_status") or source_summary.get("external_verification_status")) != "completed":
        findings.append("source_mt5_external_verification_not_completed")
    return findings


def _summary(
    model_pack: Mapping[str, Any],
    source_manifest: Mapping[str, Any],
    source_summary: Mapping[str, Any],
    artifact_checks: Mapping[str, Any],
    attempt_checks: Mapping[str, Any],
    blocking_findings: Sequence[str],
) -> dict[str, Any]:
    warnings = list(artifact_checks.get("warning_findings") or [])
    passed = not blocking_findings
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "selected_source_run_id": SELECTED_SOURCE_RUN_ID,
        "model_pack_id": model_pack.get("model_pack_id"),
        "passed": passed,
        "judgment": "inconclusive_segmented_catboost_mt5_handoff_identity_audit_completed" if passed else "blocked_segmented_catboost_mt5_handoff_identity_audit",
        "counts": {
            "segment_count": len(model_pack.get("segments") or {}),
            "attempt_count": attempt_checks.get("attempt_count", 0),
            "attempts_passed": attempt_checks.get("attempts_passed", 0),
            "blocking_findings": len(blocking_findings),
            "warning_findings": len(warnings),
        },
        "source_mt5_external_verification_status": (source_manifest.get("runtime_probe") or {}).get("external_verification_status")
        or source_summary.get("external_verification_status"),
        "runtime_handoff_decision": f"existing_stage18_mt5_probe_identity_linked_to_{SOURCE_RUN_ID.lower()}_segmented_catboost_model_pack"
        if passed
        else "blocked_existing_stage18_mt5_probe_identity_not_linked",
        "blocking_findings": list(blocking_findings),
        "warning_findings": warnings,
        "claim_boundary": BOUNDARY,
        "required_gates": {
            "research_path": "foundation.adapters.onnx_signal_adapter; foundation.control_plane.segmented_catboost_onnx_signalcard_probe",
            "runtime_path": f"foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.ex5 and Stage18 {SELECTED_SOURCE_RUN_ID} tester ini/set/reports/runtime telemetry",
            "shared_contract": "segment thresholds, feature order hashes, ONNX paths, SignalCard output",
            "known_differences": "existing MT5 runtime probe references current common files; source common-copy manifest may contain historical hash drift warnings",
            "parity_check": "model pack hash identity plus existing MT5 runtime output identity",
            "parity_identity": "model pack, source/ONNX models, segment feature matrices, common files, tester files, telemetry summaries",
            "runtime_claim_boundary": "runtime_probe_identity_reference_not_runtime_authority",
        },
    }


def _stage_ledger_rows(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    run_root = f"stages/{STAGE_ID}/02_runs/{RUN_ID}"
    return [
        {
            "ledger_row_id": f"{RUN_ID}__model_pack_identity",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "model_pack_identity",
            "parent_run_id": RUN_ID,
            "record_view": "segmented_catboost_model_pack_identity",
            "tier_scope": "Tier A+B segmented",
            "kpi_scope": "artifact_lineage",
            "scoreboard_lane": "runtime_parity",
            "status": "completed" if summary["passed"] else "blocked",
            "judgment": summary["judgment"],
            "path": f"{run_root}/mt5_handoff_identity_report.json",
            "primary_kpi": ledger_pairs((("segment_count", summary["counts"]["segment_count"]),)),
            "guardrail_kpi": "hash_identity_required=true",
            "external_verification_status": "referenced_existing_completed",
            "notes": f"{SOURCE_RUN_ID} segmented CatBoost model pack artifacts and current common-file copies are checked.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__mt5_runtime_identity",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "mt5_runtime_identity",
            "parent_run_id": RUN_ID,
            "record_view": "segmented_catboost_mt5_runtime_handoff_identity",
            "tier_scope": "Tier A+B segmented routed",
            "kpi_scope": "runtime_parity",
            "scoreboard_lane": "runtime_parity",
            "status": "completed" if summary["passed"] else "blocked",
            "judgment": summary["runtime_handoff_decision"],
            "path": f"{run_root}/handoff_identity_matrix.csv",
            "primary_kpi": ledger_pairs(
                (
                    ("attempt_count", summary["counts"]["attempt_count"]),
                    ("attempts_passed", summary["counts"]["attempts_passed"]),
                    ("warnings", summary["counts"]["warning_findings"]),
                )
            ),
            "guardrail_kpi": "runtime_authority=false;new_terminal_run=false",
            "external_verification_status": "referenced_existing_completed",
            "notes": f"Existing Stage18 MT5 runtime probe identity is linked to the {SOURCE_RUN_ID} segmented CatBoost model pack.",
        },
    ]


def _run_registry_row(summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "segmented_catboost_mt5_handoff_identity_audit",
        "status": "reviewed" if summary["passed"] else "blocked",
        "judgment": summary["judgment"],
        "path": f"stages/{STAGE_ID}/02_runs/{RUN_ID}",
        "notes": ledger_pairs(
            (
                ("source_run_id", SOURCE_RUN_ID),
                ("selected_source_run_id", SELECTED_SOURCE_RUN_ID),
                ("attempts_passed", summary["counts"]["attempts_passed"]),
                ("warning_findings", summary["counts"]["warning_findings"]),
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
            "type": "segmented_catboost_mt5_handoff_identity_report",
            "path": f"{run_root}/mt5_handoff_identity_report.json",
            "status": "tracked_reviewed",
            "notes": f"Identity audit linking {SOURCE_RUN_ID} segmented CatBoost model pack to existing Stage18 MT5 runtime evidence.",
        },
        {
            "artifact_id": f"{RUN_ID}__handoff_identity_matrix",
            "type": "segmented_catboost_handoff_identity_matrix",
            "path": f"{run_root}/handoff_identity_matrix.csv",
            "status": "tracked_reviewed",
            "notes": "Per-artifact and per-attempt handoff identity checks.",
        },
        {
            "artifact_id": f"{RUN_ID}__result_summary",
            "type": "result_summary",
            "path": f"{run_root}/reports/result_summary.md",
            "status": "tracked_reviewed",
            "notes": "Human readout for run27I segmented CatBoost MT5 handoff identity audit.",
        },
    ]


def _manifest(root: Path, generated_at: str, report_path: Path, matrix_path: Path, result: SegmentedCatBoostMt5HandoffIdentityAuditResult) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "packet_id": PACKET_ID,
        "source_run_id": SOURCE_RUN_ID,
        "generated_at_utc": generated_at,
        "producer": "foundation.control_plane.segmented_catboost_mt5_handoff_identity_audit",
        "outputs": {
            "mt5_handoff_identity_report": {"path": rel(root, report_path), "sha256": sha256_file_lf_normalized(report_path)},
            "handoff_identity_matrix": {"path": rel(root, matrix_path), "sha256": sha256_file_lf_normalized(matrix_path)},
        },
        "claim_boundary": BOUNDARY,
        "passed": result.summary["passed"],
    }


def _result_summary_markdown(generated_at: str, result: SegmentedCatBoostMt5HandoffIdentityAuditResult) -> str:
    summary = result.summary
    lines = [
        f"# Stage33 {RUN_ID} Segmented CatBoost MT5 Handoff Identity Audit(33단계 {RUN_ID} 분할 캣부스트 MT5 인계 정체성 감사)",
        "",
        f"- generated_at_utc(생성 시각 UTC): `{generated_at}`",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- source_run_id(원천 실행 ID): `{SOURCE_RUN_ID}`",
        f"- passed(통과): `{summary['passed']}`",
        f"- attempts passed(통과 시도): `{summary['counts']['attempts_passed']}/{summary['counts']['attempt_count']}`",
        f"- warning findings(경고 발견): `{summary['counts']['warning_findings']}`",
        f"- runtime handoff decision(런타임 인계 결정): `{summary['runtime_handoff_decision']}`",
        "",
        f"효과(effect, 효과): {SOURCE_RUN_ID}({SOURCE_RUN_ID} 실행)의 segmented CatBoost ONNX model pack(분할 캣부스트 온닉스 모델 팩)이 기존 Stage18(18단계) MT5 runtime probe(MT5 런타임 탐침) 산출물과 연결되는지 확인하는 것이다.",
        "",
        "## Explicit Non-Claims(명시 비주장)",
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


def _upsert_registers(root: Path, result: SegmentedCatBoostMt5HandoffIdentityAuditResult) -> None:
    upsert_csv_rows(root / "docs/registers/run_registry.csv", RUN_REGISTRY_COLUMNS, [result.run_registry_row], key="run_id")
    upsert_csv_rows(root / "docs/registers/alpha_run_ledger.csv", ALPHA_LEDGER_COLUMNS, result.stage_rows, key="ledger_row_id")
    artifact_path = root / "docs/registers/artifact_registry.csv"
    existing = read_csv_rows(artifact_path)
    columns = ("artifact_id", "type", "path", "status", "notes")
    new_ids = {row["artifact_id"] for row in result.artifact_rows}
    rows = [row for row in existing if row.get("artifact_id") not in new_ids]
    rows.extend(result.artifact_rows)
    write_csv_rows(artifact_path, columns, rows)


def _payload_hash_matches(payload: Any) -> bool:
    if not isinstance(payload, Mapping):
        return False
    return _path_hash_matches(payload.get("path"), payload.get("sha256"))


def _path_hash_matches(path_value: Any, expected_hash: Any) -> bool:
    if not path_value or not expected_hash:
        return False
    path = Path(str(path_value))
    if not io_path(path).exists():
        return False
    return _matching_text_or_raw_hash(path, str(expected_hash)) == str(expected_hash)


def _path_exists(value: Any) -> bool:
    return bool(value) and io_path(Path(str(value))).exists()


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
    parser = argparse.ArgumentParser(description="Run Stage33 segmented CatBoost MT5 handoff identity audit.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args(argv)
    if args.summary_only:
        result = build_segmented_catboost_mt5_handoff_identity_audit(Path(args.root))
        print(json.dumps(json_ready(result.summary), ensure_ascii=False, indent=2))
    else:
        aggregate = write_segmented_catboost_mt5_handoff_identity_audit_packet(Path(args.root))
        print(json.dumps(json_ready(aggregate), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
