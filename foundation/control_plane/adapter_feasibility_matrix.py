from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

from foundation.control_plane.adapter_probe_shortlist import RUN_ID as SOURCE_RUN_ID
from foundation.control_plane.adapter_probe_shortlist import build_adapter_probe_shortlist
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


RUN_ID = "run27E_adapter_feasibility_matrix_v1"
PACKET_ID = "stage33_run27E_adapter_feasibility_matrix_v1"
BOUNDARY = "adapter_feasibility_matrix_only_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
CONSUMED_CANDIDATE_ID = "stage12_run03H_et_v13_tier_balance_mt5_v1"
NEXT_PROBE_CANDIDATE_ID = "stage32_run26D_torch_tcn_native_temporal_runtime_probe_v1"


@dataclass(frozen=True)
class AdapterFeasibilityMatrixResult:
    summary: dict[str, Any]
    matrix_rows: list[dict[str, Any]]
    stage_rows: list[dict[str, Any]]
    run_registry_row: dict[str, Any]
    artifact_rows: list[dict[str, Any]]


def build_adapter_feasibility_matrix(root: Path | str = Path(".")) -> AdapterFeasibilityMatrixResult:
    root_path = Path(root)
    shortlist = build_adapter_probe_shortlist(root_path).shortlist
    matrix_rows = [_candidate_row(root_path, index + 1, row) for index, row in enumerate(shortlist)]
    selected_next = _select_next_probe(matrix_rows)
    for row in matrix_rows:
        row["selected_next_probe"] = row["candidate_id"] == selected_next.get("candidate_id")
    summary = _summary(root_path, matrix_rows, selected_next)
    return AdapterFeasibilityMatrixResult(
        summary=summary,
        matrix_rows=matrix_rows,
        stage_rows=_stage_ledger_rows(summary),
        run_registry_row=_run_registry_row(summary),
        artifact_rows=_artifact_rows(),
    )


def write_adapter_feasibility_matrix_packet(root: Path | str = Path("."), *, generated_at_utc: str | None = None) -> dict[str, Any]:
    root_path = Path(root)
    generated_at = generated_at_utc or datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    result = build_adapter_feasibility_matrix(root_path)
    run_root = root_path / "stages" / STAGE_ID / "02_runs" / RUN_ID
    reports_root = run_root / "reports"
    packet_root = root_path / "docs/agent_control/packets" / PACKET_ID
    io_path(reports_root).mkdir(parents=True, exist_ok=True)
    io_path(packet_root).mkdir(parents=True, exist_ok=True)

    report_path = run_root / "adapter_feasibility_report.json"
    matrix_path = run_root / "adapter_feasibility_matrix.csv"
    manifest_path = run_root / "run_manifest.json"
    result_summary_path = reports_root / "result_summary.md"
    aggregate_summary_path = packet_root / "aggregate_summary.json"

    _write_json(report_path, {"generated_at_utc": generated_at, **result.summary})
    _write_matrix_csv(matrix_path, result.matrix_rows)
    manifest = _manifest(root_path, generated_at, report_path, matrix_path, result)
    _write_json(manifest_path, manifest)
    _write_markdown(result_summary_path, _result_summary_markdown(generated_at, result))
    aggregate = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "status": "reviewed_adapter_feasibility_matrix_completed",
        "judgment": result.summary["judgment"],
        "boundary": BOUNDARY,
        "generated_at_utc": generated_at,
        "report_path": _rel(root_path, report_path),
        "matrix_path": _rel(root_path, matrix_path),
        "run_manifest_path": _rel(root_path, manifest_path),
        "result_summary_path": _rel(root_path, result_summary_path),
        "counts": result.summary["counts"],
        "selected_next_probe": result.summary["selected_next_probe"],
        "onnx_readiness_decision": result.summary["onnx_readiness_decision"],
        "required_gates": result.summary["required_gates"],
    }
    _write_json(aggregate_summary_path, aggregate)
    _upsert_registers(root_path, result)
    upsert_csv_rows(
        root_path / "stages" / STAGE_ID / "03_reviews/stage_run_ledger.csv",
        ALPHA_LEDGER_COLUMNS,
        result.stage_rows,
        key="ledger_row_id",
    )
    return aggregate


def _candidate_row(root: Path, rank: int, candidate: Mapping[str, Any]) -> dict[str, Any]:
    source_root = root / str(candidate["source_path"])
    assets = _scan_assets(source_root)
    classification = _classify_candidate(candidate, assets)
    return {
        "selected_rank": rank,
        "candidate_id": candidate["candidate_id"],
        "stage_id": candidate["stage_id"],
        "run_id": candidate["run_id"],
        "mechanism_class": candidate["mechanism_class"],
        "roles": list(candidate["roles"]),
        "source_path": candidate["source_path"],
        "artifact_state": assets["state"],
        "adapter_probe_route": classification["route"],
        "feasibility_state": classification["state"],
        "next_action": classification["next_action"],
        "blockers": classification["blockers"],
        "runtime_advantage_read": classification["runtime_advantage_read"],
        "onnx_readiness": classification["onnx_readiness"],
        "feature_contract_state": classification["feature_contract_state"],
        "has_run_manifest": assets["has_run_manifest"],
        "has_kpi_record": assets["has_kpi_record"],
        "has_summary": assets["has_summary"],
        "has_source_model": assets["has_source_model"],
        "has_onnx": assets["has_onnx"],
        "has_score_table": assets["has_score_table"],
        "has_feature_csv": assets["has_feature_csv"],
        "has_predictions": assets["has_predictions"],
        "has_mt5_files": assets["has_mt5_files"],
        "external_verification_completed": bool(candidate["external_verification_completed"]),
        "validation_net_profit_best": candidate["validation_net_profit_best"],
        "oos_net_profit_best": candidate["oos_net_profit_best"],
        "asset_counts": assets["counts"],
        "sample_assets": assets["samples"],
        "claim_boundary": BOUNDARY,
    }


def _scan_assets(source_root: Path) -> dict[str, Any]:
    base = io_path(source_root)
    if not base.exists():
        return {
            "state": "missing_source_run_root",
            "files": [],
            "counts": {},
            "samples": {},
            "has_run_manifest": False,
            "has_kpi_record": False,
            "has_summary": False,
            "has_source_model": False,
            "has_onnx": False,
            "has_score_table": False,
            "has_feature_csv": False,
            "has_predictions": False,
            "has_mt5_files": False,
        }
    files = sorted(path.relative_to(base).as_posix() for path in base.rglob("*") if path.is_file())
    groups = {
        "run_manifest": [path for path in files if path.endswith("run_manifest.json")],
        "kpi_record": [path for path in files if path.endswith("kpi_record.json")],
        "summary": [path for path in files if path.endswith("summary.json")],
        "source_model": [path for path in files if path.lower().endswith((".joblib", ".pkl"))],
        "onnx": [path for path in files if path.lower().endswith(".onnx")],
        "score_table": [path for path in files if path.lower().endswith(".csv") and "score_table" in path.lower()],
        "feature_csv": [path for path in files if _is_feature_csv(path)],
        "predictions": [path for path in files if path.lower().endswith(".parquet") and "prediction" in path.lower()],
        "mt5_files": [path for path in files if _is_mt5_file(path)],
    }
    return {
        "state": "source_run_root_found",
        "files": files,
        "counts": {key: len(value) for key, value in groups.items()},
        "samples": {key: value[:8] for key, value in groups.items() if value},
        "has_run_manifest": bool(groups["run_manifest"]),
        "has_kpi_record": bool(groups["kpi_record"]),
        "has_summary": bool(groups["summary"]),
        "has_source_model": bool(groups["source_model"]),
        "has_onnx": bool(groups["onnx"]),
        "has_score_table": bool(groups["score_table"]),
        "has_feature_csv": bool(groups["feature_csv"]),
        "has_predictions": bool(groups["predictions"]),
        "has_mt5_files": bool(groups["mt5_files"]),
    }


def _classify_candidate(candidate: Mapping[str, Any], assets: Mapping[str, Any]) -> dict[str, Any]:
    blockers = _blockers(candidate, assets)
    mechanism = str(candidate["mechanism_class"])
    candidate_id = str(candidate["candidate_id"])
    if candidate_id == CONSUMED_CANDIDATE_ID:
        return {
            "route": "existing_onnx_signalcard_consumed",
            "state": "completed_by_run27C_run27D",
            "next_action": "do_not_repeat_unless_comparing_adapter_versions",
            "blockers": [],
            "runtime_advantage_read": "existing_onnx_pack_identity_already_linked_to_mt5_probe",
            "onnx_readiness": "existing_onnx_manifest_packaged_no_new_export",
            "feature_contract_state": "fixed_by_run27C_model_pack",
        }
    if blockers:
        return {
            "route": "deferred_missing_required_artifacts",
            "state": "blocked_or_deferred",
            "next_action": "repair_or_reconstruct_missing_artifacts_before_adapter_probe",
            "blockers": blockers,
            "runtime_advantage_read": "not_assessable_until_artifact_gap_closes",
            "onnx_readiness": "blocked",
            "feature_contract_state": "blocked",
        }
    if assets["has_score_table"]:
        return {
            "route": "score_table_signalcard_adapter",
            "state": "score_table_signalcard_probe_ready",
            "next_action": "implement_score_table_signalcard_adapter_probe",
            "blockers": [],
            "runtime_advantage_read": "score_table_handoff_already_exists;_onnx_advantage_not_shown",
            "onnx_readiness": "defer_onnx_runtime_advantage_absent",
            "feature_contract_state": "feature_order_from_model_artifacts_or_feature_csv_required",
        }
    if assets["has_onnx"] and assets["has_source_model"]:
        segmented = _is_segmented_candidate(assets)
        duplicate = mechanism == "model_probability_surface"
        return {
            "route": "existing_onnx_segmented_signalcard_adapter" if segmented else "existing_onnx_signalcard_adapter",
            "state": "onnx_segmented_signalcard_probe_ready"
            if segmented
            else "onnx_signalcard_probe_ready_duplicate_mechanism"
            if duplicate
            else "onnx_signalcard_probe_ready",
            "next_action": "defer_until_non_duplicate_or_segment_specific_contract_probe"
            if duplicate
            else "implement_segmented_signalcard_onnx_adapter_probe"
            if segmented
            else "implement_signalcard_onnx_adapter_probe",
            "blockers": [],
            "runtime_advantage_read": "existing_onnx_artifacts_can_be_wrapped;_new_export_not_needed",
            "onnx_readiness": "existing_onnx_probe_possible_not_new_export_ready",
            "feature_contract_state": "feature_csv_present_segment_contract_required" if segmented else "feature_csv_present",
        }
    return {
        "route": "deferred_unknown_adapter_route",
        "state": "deferred",
        "next_action": "manual_adapter_contract_design_needed",
        "blockers": ["unknown_adapter_route"],
        "runtime_advantage_read": "not_assessed",
        "onnx_readiness": "not_applicable",
        "feature_contract_state": "not_assessed",
    }


def _blockers(candidate: Mapping[str, Any], assets: Mapping[str, Any]) -> list[str]:
    blockers: list[str] = []
    for name in ("has_run_manifest", "has_kpi_record", "has_feature_csv", "has_predictions"):
        if not assets[name]:
            blockers.append(name)
    if not bool(candidate["external_verification_completed"]):
        blockers.append("external_verification_not_completed")
    if not assets["has_score_table"] and not (assets["has_onnx"] and assets["has_source_model"]):
        blockers.append("missing_runtime_model_artifact")
    return blockers


def _is_feature_csv(path: str) -> bool:
    lower = path.lower()
    return lower.endswith(".csv") and (
        "feature_matrix" in lower
        or lower.startswith("features/")
        or "/features/" in lower
        or lower.endswith("_features.csv")
    )


def _is_mt5_file(path: str) -> bool:
    lower = path.lower()
    return lower.startswith("mt5/") and lower.endswith((".set", ".ini", ".htm", ".html", ".xml", ".csv"))


def _is_segmented_candidate(assets: Mapping[str, Any]) -> bool:
    samples = assets.get("samples", {}).get("feature_csv", [])
    return any("/high_" in str(path) or "/mid_" in str(path) or "/low_" in str(path) for path in samples)


def _select_next_probe(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    for row in rows:
        if row["candidate_id"] == NEXT_PROBE_CANDIDATE_ID and row["feasibility_state"] == "score_table_signalcard_probe_ready":
            return dict(row)
    for row in rows:
        if row["feasibility_state"] == "score_table_signalcard_probe_ready":
            return dict(row)
    for row in rows:
        if str(row["feasibility_state"]).endswith("probe_ready") and row["candidate_id"] != CONSUMED_CANDIDATE_ID:
            return dict(row)
    return {}


def _summary(root: Path, rows: Sequence[Mapping[str, Any]], selected_next: Mapping[str, Any]) -> dict[str, Any]:
    route_counts = _counts(row["adapter_probe_route"] for row in rows)
    state_counts = _counts(row["feasibility_state"] for row in rows)
    counts = {
        "shortlist_count": len(rows),
        "consumed_count": sum(1 for row in rows if row["candidate_id"] == CONSUMED_CANDIDATE_ID),
        "score_table_probe_ready": state_counts.get("score_table_signalcard_probe_ready", 0),
        "existing_onnx_probe_ready": sum(1 for row in rows if str(row["onnx_readiness"]).startswith("existing_onnx_probe_possible")),
        "new_onnx_export_ready": 0,
        "blocked_or_deferred": sum(1 for row in rows if row["feasibility_state"] in {"blocked_or_deferred", "deferred"}),
    }
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "judgment": "inconclusive_adapter_feasibility_matrix_completed_next_score_table_probe_selected",
        "claim_boundary": BOUNDARY,
        "why_needed": "run27C consumed only the first ExtraTrees ONNX adapter; remaining run27B candidates need artifact-level feasibility before more adapter work.",
        "evidence_gap": "which shortlisted mechanisms have current feature contracts, runtime model artifacts, predictions, and MT5 evidence available for the next probe",
        "input_scope": {
            "source_shortlist": SOURCE_RUN_ID,
            "candidate_count": len(rows),
            "tier_scope": "Tier A+B shortlisted evidence",
        },
        "counts": counts,
        "route_counts": route_counts,
        "state_counts": state_counts,
        "selected_next_probe": _selected_summary(selected_next),
        "onnx_readiness_decision": {
            "decision": "no_new_onnx_export_ready;_existing_onnx_probe_possible_for_segmented_candidates;_next_probe_prefers_score_table_adapter_diversity",
            "new_onnx_export_ready": 0,
            "existing_onnx_probe_ready": counts["existing_onnx_probe_ready"],
            "reason": "ONNX remains optional packaging; a score-table mechanism has reusable runtime evidence and no ONNX runtime advantage is established.",
        },
        "required_gates": {
            "why_this_work": "completed",
            "evidence_gap": "completed",
            "input_data_features_split_run_id": "completed",
            "artifact_paths": "completed",
            "validation_oos_wfo_mt5_results": "consumes_existing_run27B_metrics_and_source_runtime_evidence",
            "failure_or_defer_reason": "completed_per_candidate",
            "claim_boundary": BOUNDARY,
            "next_action_or_stop_rule": "selected_next_score_table_signalcard_probe_or_defer_if_artifacts_move",
        },
        "source_hashes": {
            "run_registry": sha256_file_lf_normalized(root / "docs/registers/run_registry.csv"),
            "alpha_run_ledger": sha256_file_lf_normalized(root / "docs/registers/alpha_run_ledger.csv"),
        },
    }


def _selected_summary(selected: Mapping[str, Any]) -> dict[str, Any]:
    if not selected:
        return {"candidate_id": None, "decision": "no_feasible_next_probe"}
    return {
        "candidate_id": selected["candidate_id"],
        "stage_id": selected["stage_id"],
        "run_id": selected["run_id"],
        "mechanism_class": selected["mechanism_class"],
        "roles": selected["roles"],
        "adapter_probe_route": selected["adapter_probe_route"],
        "feasibility_state": selected["feasibility_state"],
        "next_action": selected["next_action"],
        "source_path": selected["source_path"],
        "decision": "selected_next_non_onnx_score_table_signalcard_adapter_probe",
    }


def _counts(values: Sequence[Any]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for value in values:
        key = str(value)
        counts[key] = counts.get(key, 0) + 1
    return dict(sorted(counts.items()))


def _stage_ledger_rows(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    run_root = f"stages/{STAGE_ID}/02_runs/{RUN_ID}"
    selected = summary["selected_next_probe"]
    return [
        {
            "ledger_row_id": f"{RUN_ID}__adapter_feasibility_matrix",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "adapter_feasibility_matrix",
            "parent_run_id": RUN_ID,
            "record_view": "artifact_feasibility_matrix",
            "tier_scope": "Tier A+B",
            "kpi_scope": "adapter_feasibility",
            "scoreboard_lane": "structural_scout",
            "status": "completed",
            "judgment": summary["judgment"],
            "path": f"{run_root}/adapter_feasibility_report.json",
            "primary_kpi": ledger_pairs(
                (
                    ("shortlist_count", summary["counts"]["shortlist_count"]),
                    ("score_table_ready", summary["counts"]["score_table_probe_ready"]),
                    ("existing_onnx_probe_ready", summary["counts"]["existing_onnx_probe_ready"]),
                )
            ),
            "guardrail_kpi": "new_onnx_export_ready=0;adapter_probe_not_promotion",
            "external_verification_status": "consumes_existing_evidence",
            "notes": "Artifact-level feasibility matrix over run27B shortlisted adapter candidates.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__next_score_table_probe_selection",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "next_score_table_probe_selection",
            "parent_run_id": RUN_ID,
            "record_view": "adapter_probe_next_action",
            "tier_scope": "Tier A+B",
            "kpi_scope": "SignalCard_score_table_adapter_contract",
            "scoreboard_lane": "structural_scout",
            "status": "completed",
            "judgment": selected.get("decision", "no_feasible_next_probe"),
            "path": f"{run_root}/adapter_feasibility_matrix.csv",
            "primary_kpi": ledger_pairs((("selected_candidate", selected.get("candidate_id")),)),
            "guardrail_kpi": "baseline=false;promotion=false;runtime_authority=false",
            "external_verification_status": "out_of_scope_by_claim",
            "notes": "Next probe is implementation selection only; it does not claim alpha quality.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__onnx_readiness_decision",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "onnx_readiness_decision",
            "parent_run_id": RUN_ID,
            "record_view": "onnx_readiness_gate",
            "tier_scope": "Tier A+B",
            "kpi_scope": "runtime_packaging_gate",
            "scoreboard_lane": "structural_scout",
            "status": "completed",
            "judgment": "defer_new_onnx_export_no_runtime_advantage_selected_for_score_table_probe",
            "path": f"{run_root}/run_manifest.json",
            "primary_kpi": ledger_pairs((("new_onnx_export_ready", 0),)),
            "guardrail_kpi": "parity_plan_required;runtime_handoff_advantage_required",
            "external_verification_status": "out_of_scope_by_claim",
            "notes": "Existing ONNX candidates remain probeable, but run27E selects score-table adapter diversity first.",
        },
    ]


def _run_registry_row(summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "alpha_adapter_feasibility_matrix",
        "status": "reviewed",
        "judgment": summary["judgment"],
        "path": f"stages/{STAGE_ID}/02_runs/{RUN_ID}",
        "notes": ledger_pairs(
            (
                ("source_run_id", SOURCE_RUN_ID),
                ("shortlist_count", summary["counts"]["shortlist_count"]),
                ("selected_next", summary["selected_next_probe"].get("candidate_id")),
                ("new_onnx_export_ready", 0),
                ("boundary", BOUNDARY),
            )
        ),
    }


def _artifact_rows() -> list[dict[str, Any]]:
    run_root = f"stages/{STAGE_ID}/02_runs/{RUN_ID}"
    return [
        {
            "artifact_id": f"{RUN_ID}__adapter_feasibility_report",
            "type": "adapter_feasibility_report",
            "path": f"{run_root}/adapter_feasibility_report.json",
            "status": "tracked_reviewed",
            "notes": "Artifact feasibility report for run27B shortlisted candidates.",
        },
        {
            "artifact_id": f"{RUN_ID}__adapter_feasibility_matrix",
            "type": "adapter_feasibility_matrix",
            "path": f"{run_root}/adapter_feasibility_matrix.csv",
            "status": "tracked_reviewed",
            "notes": "Per-candidate artifact availability, route, blockers, and next action matrix.",
        },
        {
            "artifact_id": f"{RUN_ID}__result_summary",
            "type": "result_summary",
            "path": f"{run_root}/reports/result_summary.md",
            "status": "tracked_reviewed",
            "notes": "Human readout for Stage33 run27E adapter feasibility.",
        },
    ]


def _manifest(
    root: Path,
    generated_at: str,
    report_path: Path,
    matrix_path: Path,
    result: AdapterFeasibilityMatrixResult,
) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "packet_id": PACKET_ID,
        "source_run_id": SOURCE_RUN_ID,
        "generated_at_utc": generated_at,
        "producer": "foundation.control_plane.adapter_feasibility_matrix",
        "inputs": {
            "adapter_probe_shortlist": SOURCE_RUN_ID,
            "run_registry": {
                "path": "docs/registers/run_registry.csv",
                "sha256_lf_normalized": result.summary["source_hashes"]["run_registry"],
            },
            "alpha_run_ledger": {
                "path": "docs/registers/alpha_run_ledger.csv",
                "sha256_lf_normalized": result.summary["source_hashes"]["alpha_run_ledger"],
            },
        },
        "outputs": {
            "adapter_feasibility_report": {"path": _rel(root, report_path), "sha256": sha256_file_lf_normalized(report_path)},
            "adapter_feasibility_matrix": {"path": _rel(root, matrix_path), "sha256": sha256_file_lf_normalized(matrix_path)},
        },
        "claim_boundary": BOUNDARY,
    }


def _result_summary_markdown(generated_at: str, result: AdapterFeasibilityMatrixResult) -> str:
    summary = result.summary
    selected = summary["selected_next_probe"]
    lines = [
        "# Stage33 RUN27E Adapter Feasibility Matrix(33단계 실행27E 어댑터 실현성 행렬)",
        "",
        f"- generated_at_utc(생성 시각 UTC): `{generated_at}`",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- source_run_id(원천 실행 ID): `{SOURCE_RUN_ID}`",
        f"- boundary(경계): `{BOUNDARY}`",
        f"- shortlist count(후보 목록 수): `{summary['counts']['shortlist_count']}`",
        f"- score-table probe ready(점수표 탐침 준비): `{summary['counts']['score_table_probe_ready']}`",
        f"- existing ONNX probe ready(기존 온닉스 탐침 준비): `{summary['counts']['existing_onnx_probe_ready']}`",
        f"- new ONNX export ready(새 온닉스 내보내기 준비): `{summary['counts']['new_onnx_export_ready']}`",
        "",
        "## Decision(결정)",
        "",
        f"- selected next probe(선택된 다음 탐침): `{selected.get('candidate_id')}`",
        f"- mechanism class(메커니즘 클래스): `{selected.get('mechanism_class')}`",
        f"- route(경로): `{selected.get('adapter_probe_route')}`",
        f"- next action(다음 행동): `{selected.get('next_action')}`",
        "",
        "효과(effect, 효과)는 run27C(27C 실행)의 ExtraTrees ONNX(엑스트라트리스 온닉스) 포장만 반복하지 않고, Stage32(32단계) score-table(점수표) sequence-context(순서 문맥) 후보를 SignalCard adapter(신호 카드 어댑터) 구현 대상으로 전진시키는 것이다.",
        "",
        "## ONNX Gate(온닉스 게이트)",
        "",
        f"`{summary['onnx_readiness_decision']['decision']}`",
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


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_markdown(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig")


def _write_matrix_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    columns = (
        "selected_rank",
        "selected_next_probe",
        "candidate_id",
        "stage_id",
        "run_id",
        "mechanism_class",
        "roles",
        "adapter_probe_route",
        "feasibility_state",
        "next_action",
        "blockers",
        "runtime_advantage_read",
        "onnx_readiness",
        "feature_contract_state",
        "has_run_manifest",
        "has_kpi_record",
        "has_summary",
        "has_source_model",
        "has_onnx",
        "has_score_table",
        "has_feature_csv",
        "has_predictions",
        "has_mt5_files",
        "external_verification_completed",
        "validation_net_profit_best",
        "oos_net_profit_best",
        "asset_counts",
        "sample_assets",
        "source_path",
        "claim_boundary",
    )
    flattened: list[dict[str, Any]] = []
    for row in rows:
        flat = dict(row)
        flat["roles"] = "|".join(str(role) for role in row["roles"])
        flat["blockers"] = "|".join(str(item) for item in row["blockers"])
        flat["asset_counts"] = json.dumps(json_ready(row["asset_counts"]), ensure_ascii=False, sort_keys=True)
        flat["sample_assets"] = json.dumps(json_ready(row["sample_assets"]), ensure_ascii=False, sort_keys=True)
        flattened.append(flat)
    write_csv_rows(path, columns, flattened)


def _upsert_registers(root: Path, result: AdapterFeasibilityMatrixResult) -> None:
    upsert_csv_rows(root / "docs/registers/run_registry.csv", RUN_REGISTRY_COLUMNS, [result.run_registry_row], key="run_id")
    upsert_csv_rows(root / "docs/registers/alpha_run_ledger.csv", ALPHA_LEDGER_COLUMNS, result.stage_rows, key="ledger_row_id")
    artifact_path = root / "docs/registers/artifact_registry.csv"
    existing = read_csv_rows(artifact_path)
    columns = ("artifact_id", "type", "path", "status", "notes")
    new_ids = {row["artifact_id"] for row in result.artifact_rows}
    rows = [row for row in existing if row.get("artifact_id") not in new_ids]
    rows.extend(result.artifact_rows)
    write_csv_rows(artifact_path, columns, rows)


def _rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build Stage33 adapter artifact feasibility matrix.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args(argv)
    if args.summary_only:
        result = build_adapter_feasibility_matrix(Path(args.root))
        print(json.dumps(json_ready(result.summary), ensure_ascii=False, indent=2))
    else:
        aggregate = write_adapter_feasibility_matrix_packet(Path(args.root))
        print(json.dumps(json_ready(aggregate), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
