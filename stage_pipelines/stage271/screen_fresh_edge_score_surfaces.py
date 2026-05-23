from __future__ import annotations

import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import (  # noqa: E402
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    path_exists,
    read_csv_rows,
    upsert_csv_rows,
    write_csv_rows,
)


STAGE_ID = "271_onnx_candidate_campaign__fresh_edge_rebuild_after_nonfilter_failure"
RUN_ID = "run271E_screen_fresh_edge_score_surfaces_v1"
SOURCE_RUN_ID = "run271D_execute_fresh_edge_scoring_probe_v1"
NEXT_ACTION = "run271F_close_stage271_open_stage272_time_risk_router_pressure_probe"
STATUS = "completed_fresh_edge_score_surface_screen_no_candidate_selection"
JUDGMENT = "screened_probe_seed_and_failure_memory_no_candidate_selection"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_ROOT / "02_runs" / "run271E"
REVIEWS = STAGE_ROOT / "03_reviews"
SELECTED = STAGE_ROOT / "04_selected"
RUN271D_DIR = STAGE_ROOT / "02_runs" / "run271D"
RUN271D_SCORES = RUN271D_DIR / "scores"
RUN271D_HANDOFF = RUN271D_DIR / "handoff"

SOURCE_MANIFEST = RUN271D_DIR / "run_manifest.json"
SOURCE_SCORE_SUMMARY = RUN271D_DIR / "score_materialization_summary.csv"
SOURCE_SIGNAL_SUMMARY = RUN271D_DIR / "signal_read_summary.csv"
SOURCE_WEAK_SUMMARY = RUN271D_DIR / "weak_slice_score_summary.csv"
SOURCE_TIER_RECEIPTS = RUN271D_DIR / "tier_scope_receipts.csv"
SOURCE_THRESHOLD_RECEIPT = RUN271D_DIR / "threshold_receipt.csv"
SOURCE_HANDOFF_RESOLUTION = RUN271D_DIR / "handoff_path_resolution.csv"
SOURCE_DATA_INTEGRITY = RUN271D_DIR / "data_integrity_receipt.json"
SOURCE_MODEL_VALIDATION = RUN271D_DIR / "model_validation_receipt.json"
SOURCE_LINEAGE = RUN271D_DIR / "artifact_lineage_receipt.json"
SOURCE_RESULT_JUDGMENT = RUN271D_DIR / "result_judgment.csv"
SOURCE_REPORT = REVIEWS / "run271D_report.md"

SCREENING_SUMMARY = RUN_DIR / "package_screening_summary.csv"
STAGE272_QUEUE = RUN_DIR / "stage272_probe_queue.csv"
FAILURE_MEMORY = RUN_DIR / "screening_failure_memory.csv"
SUPPORT_CONTROL_CARRY = RUN_DIR / "support_control_carry.csv"
WEAK_SLICE_SCREEN = RUN_DIR / "weak_slice_screen_summary.csv"
SCREENING_RECEIPT = RUN_DIR / "screening_decision_receipt.json"
DATA_INTEGRITY_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_VALIDATION_RECEIPT = RUN_DIR / "model_validation_receipt.json"
ARTIFACT_LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
RESULT_JUDGMENT = RUN_DIR / "result_judgment.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
RUN_REPORT = REVIEWS / "run271E_report.md"
SELECTION_STATUS = SELECTED / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
CURRENT_STATE = ROOT / "docs/context/current_working_state.md"
WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CHANGELOG = ROOT / "docs/workspace/changelog.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs/registers/artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs/registers/idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs/registers/negative_result_register.md"
PRODUCER_PATH = Path("stage_pipelines/stage271/screen_fresh_edge_score_surfaces.py")

STAGE_LEDGER_COLUMNS = (
    "row_id",
    "stage_id",
    "run_id",
    "view",
    "tier_scope",
    "scoreboard",
    "status",
    "judgment",
    "evidence_boundary",
    "report_path",
    "notes",
)
ARTIFACT_COLUMNS = (
    "artifact_id",
    "artifact_type",
    "path",
    "sha256",
    "stage_id",
    "run_id",
    "created_at_utc",
    "notes",
)
RESULT_COLUMNS = (
    "result_subject",
    "evidence_available",
    "evidence_missing",
    "judgment_label",
    "claim_boundary",
    "next_condition",
    "user_explanation_hook",
)

PACKAGE_META = {
    "cp271A_damage_first_loss_asymmetry_surface": {
        "short_id": "cp271A",
        "role": "selectable_blueprint",
        "fresh_thesis": "damage_first_loss_asymmetry",
    },
    "cp271B_time_risk_phase_router_surface": {
        "short_id": "cp271B",
        "role": "selectable_blueprint",
        "fresh_thesis": "time_risk_phase_router",
    },
    "cp271C_recovery_tail_payoff_rebalance_surface": {
        "short_id": "cp271C",
        "role": "selectable_blueprint",
        "fresh_thesis": "recovery_tail_payoff_rebalance",
    },
    "cp271D_stage270_reference_control_boundary": {
        "short_id": "cp271D",
        "role": "support_control",
        "fresh_thesis": "stage270_reference_control_boundary",
    },
}


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    write_csv_rows(path, columns, rows)


def must_exist(paths: Sequence[Path]) -> None:
    missing = [rel(path) for path in paths if not path_exists(path)]
    if missing:
        raise FileNotFoundError("Missing required source artifacts: " + ", ".join(missing))


def source_hashes(paths: Sequence[Path]) -> dict[str, str]:
    return {rel(path): sha256_file(path) for path in paths}


def as_float(value: Any) -> float:
    if value is None:
        return float("nan")
    text = str(value).strip()
    if not text:
        return float("nan")
    try:
        return float(text)
    except ValueError:
        return float("nan")


def metric(signal_rows: Sequence[Mapping[str, str]], package_id: str, tier_view: str, split: str, field: str) -> float:
    for row in signal_rows:
        if row["package_id"] == package_id and row["tier_view"] == tier_view and row["split"] == split:
            return as_float(row.get(field, ""))
    return float("nan")


def score_metric(score_rows: Sequence[Mapping[str, str]], package_id: str, tier_view: str, split: str, field: str) -> float:
    for row in score_rows:
        if row["package_id"] == package_id and row["tier_view"] == tier_view and row["split"] == split:
            return as_float(row.get(field, ""))
    return float("nan")


def finite_or_blank(value: float, digits: int = 8) -> float | str:
    return round(float(value), digits) if np.isfinite(value) else ""


def classify_package(package_id: str, row: Mapping[str, Any]) -> tuple[str, str, str, str, str]:
    if PACKAGE_META[package_id]["role"] == "support_control":
        return (
            "support_control_carry",
            "carry_as_stage272_identity_control",
            "support control(보조 대조)는 후보가 아니라 feature/order and handoff identity(피처/순서와 인계 정체성) 대조다.",
            "keep_for_stage272_handoff_identity_checks",
            "do_not_read_support_control_as_candidate",
        )
    val_align = as_float(row["tier_a_validation_alignment"])
    oos_align = as_float(row["tier_a_oos_alignment"])
    val_rate = as_float(row["tier_a_validation_decision_rate"])
    oos_rate = as_float(row["tier_a_oos_decision_rate"])
    tier_delta = as_float(row["tier_ab_decision_rate_delta"])
    val_long = as_float(row["tier_a_validation_long_share"])
    oos_long = as_float(row["tier_a_oos_long_share"])
    balanced_route = (
        np.isfinite(val_long)
        and np.isfinite(oos_long)
        and 0.35 <= val_long <= 0.65
        and 0.35 <= oos_long <= 0.65
    )
    bounded_supply = (
        np.isfinite(val_rate)
        and np.isfinite(oos_rate)
        and 0.12 <= val_rate <= 0.55
        and 0.12 <= oos_rate <= 0.55
    )
    if (
        val_align >= 0.51
        and oos_align >= 0.49
        and bounded_supply
        and balanced_route
        and tier_delta <= 0.08
    ):
        return (
            "stage272_probe_seed_oos_watch",
            "queue_for_stage272_time_risk_router_pressure_probe",
            "validation(검증) 구조 신호가 살아 있고 route mix(경로 혼합)와 Tier B(티어 B) 대칭성이 유지되지만 OOS(표본외)는 약해서 탐침 씨앗만 가능하다.",
            "validation_and_oos_alignment_above_0_50_with_stable_supply_after_pressure_probe",
            "do_not_call_selected_candidate_before_MT5_and_adapter_package",
        )
    if tier_delta > 0.25:
        return (
            "failure_memory_partial_context_collapse",
            "record_failure_memory",
            "Tier A(티어 A)와 Tier B(티어 B) decision rate(판단 비율)가 크게 갈라져 partial-context fallback(부분 문맥 대체) 구조가 불안정하다.",
            "new_surface_without_top3_dependency_or_explicit_partial_context_adapter",
            "do_not_repeat_full_context_only_payoff_surface_as_candidate",
        )
    if not bounded_supply:
        return (
            "failure_memory_supply_shape_unbounded",
            "record_failure_memory",
            "decision supply(판단 공급)가 너무 넓거나 좁아 score surface(점수 표면) 선별 경계에 맞지 않는다.",
            "bounded_decision_rate_0_12_to_0_55_on_validation_and_oos",
            "do_not_treat_supply_volume_as_edge",
        )
    if not balanced_route:
        return (
            "failure_memory_route_bias",
            "record_failure_memory",
            "long/short route mix(롱/숏 경로 혼합)가 한쪽으로 기울어 구조 신호를 왜곡할 위험이 있다.",
            "route_mix_between_35_and_65_percent_in_validation_and_oos",
            "do_not_promote_direction_bias_without_side_specific_model",
        )
    return (
        "failure_memory_signal_alignment_weak",
        "record_failure_memory",
        "validation/OOS(검증/표본외) structural alignment(구조 정렬)가 약해 다음 단계 씨앗으로 부족하다.",
        "validation_and_oos_alignment_above_0_50_with_bounded_supply",
        "do_not_repeat_same_score_surface_without_new_decision_surface",
    )


def build_screening_rows(score_rows: Sequence[Mapping[str, str]], signal_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for package_id, meta in PACKAGE_META.items():
        val_align = metric(signal_rows, package_id, "Tier A separate", "validation", "label_alignment_rate")
        oos_align = metric(signal_rows, package_id, "Tier A separate", "oos", "label_alignment_rate")
        val_rate = metric(signal_rows, package_id, "Tier A separate", "validation", "decision_rate")
        oos_rate = metric(signal_rows, package_id, "Tier A separate", "oos", "decision_rate")
        val_long = metric(signal_rows, package_id, "Tier A separate", "validation", "long_route_share")
        oos_long = metric(signal_rows, package_id, "Tier A separate", "oos", "long_route_share")
        tier_b_val_rate = metric(signal_rows, package_id, "Tier B separate", "validation", "decision_rate")
        tier_b_oos_rate = metric(signal_rows, package_id, "Tier B separate", "oos", "decision_rate")
        tier_delta = abs(val_rate - tier_b_val_rate) + abs(oos_rate - tier_b_oos_rate)
        train_rate = metric(signal_rows, package_id, "Tier A separate", "train", "decision_rate")
        avg_score = metric(signal_rows, package_id, "Tier A separate", "validation", "avg_candidate_decision_score")
        oos_score = metric(signal_rows, package_id, "Tier A separate", "oos", "avg_candidate_decision_score")
        structural_screen_score = (
            max(val_align - 0.50, 0.0) * 120.0
            + max(oos_align - 0.49, 0.0) * 80.0
            + max(0.55 - abs(val_rate - oos_rate), 0.0) * 4.0
            + max(0.08 - tier_delta, 0.0) * 10.0
        )
        row: dict[str, Any] = {
            "package_id": package_id,
            "package_role": meta["role"],
            "fresh_thesis": meta["fresh_thesis"],
            "tier_a_train_decision_rate": finite_or_blank(train_rate),
            "tier_a_validation_decision_rate": finite_or_blank(val_rate),
            "tier_a_oos_decision_rate": finite_or_blank(oos_rate),
            "tier_b_validation_decision_rate": finite_or_blank(tier_b_val_rate),
            "tier_b_oos_decision_rate": finite_or_blank(tier_b_oos_rate),
            "tier_ab_decision_rate_delta": finite_or_blank(tier_delta),
            "tier_a_validation_alignment": finite_or_blank(val_align),
            "tier_a_oos_alignment": finite_or_blank(oos_align),
            "tier_a_validation_long_share": finite_or_blank(val_long),
            "tier_a_oos_long_share": finite_or_blank(oos_long),
            "tier_a_validation_avg_score": finite_or_blank(avg_score),
            "tier_a_oos_avg_score": finite_or_blank(oos_score),
            "structural_screen_score": finite_or_blank(structural_screen_score, 6),
            "selected_candidate": "none",
            "onnx_readiness": "not_claimed",
            "performance_claim": "none",
        }
        judgment, next_action, reason, reopen_condition, do_not_repeat = classify_package(package_id, row)
        row.update(
            {
                "screening_judgment": judgment,
                "next_action": next_action,
                "reason": reason,
                "reopen_condition": reopen_condition,
                "do_not_repeat_note": do_not_repeat,
            }
        )
        rows.append(row)
    return rows


def build_stage272_queue(screening_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    queue: list[dict[str, Any]] = []
    for row in screening_rows:
        if row["screening_judgment"] != "stage272_probe_seed_oos_watch":
            continue
        queue.append(
            {
                "queue_id": "stage272_seed_cp271B_time_risk_phase_router_pressure_probe",
                "package_id": row["package_id"],
                "source_run": RUN_ID,
                "queue_role": "time_risk_router_pressure_probe_seed",
                "required_support_control": "cp271D_stage270_reference_control_boundary",
                "fresh_thesis": "time-risk phase router(시간 위험 국면 라우터)가 약한 구간을 거르는지 압박한다.",
                "upside_condition": "validation/OOS(검증/표본외) 둘 다 alignment(정렬률)와 bounded supply(경계 공급)를 유지해야 한다.",
                "failure_mode_to_watch": "OOS(표본외) alignment(정렬률) 약함, session/month(세션/월) 집중, route mix(경로 혼합) 붕괴",
                "discard_condition": "MT5 probe(MT5 탐침) 또는 stability review(안정성 검토)에서 PF/DD/trade quality(수익 팩터/손실폭/거래 품질)가 무너지면 폐기한다.",
                "required_evidence": "score_table;handoff_json;tier_receipts;weak_slice_screen;future_MT5_probe",
                "claim_boundary": BOUNDARY,
            }
        )
    return queue


def build_failure_memory(screening_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in screening_rows:
        judgment = str(row["screening_judgment"])
        if not judgment.startswith("failure_memory"):
            continue
        rows.append(
            {
                "package_id": row["package_id"],
                "failed_boundary": judgment,
                "why_failed_or_not_ready": row["reason"],
                "salvage_value": "new_decision_surface_or_partial_context_adapter",
                "reopen_condition": row["reopen_condition"],
                "do_not_repeat_note": row["do_not_repeat_note"],
            }
        )
    return rows


def build_support_control_rows(screening_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "package_id": row["package_id"],
            "support_role": "stage272_identity_and_handoff_control",
            "screening_judgment": row["screening_judgment"],
            "carry_condition": row["next_action"],
            "claim_boundary": BOUNDARY,
        }
        for row in screening_rows
        if row["package_role"] == "support_control"
    ]


def build_weak_slice_screen(weak_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    frame = pd.DataFrame(weak_rows)
    if frame.empty:
        return []
    frame["decision_rate"] = pd.to_numeric(frame["decision_rate"], errors="coerce")
    frame["avg_candidate_decision_score"] = pd.to_numeric(frame["avg_candidate_decision_score"], errors="coerce")
    output: list[dict[str, Any]] = []
    for (package_id, tier_view, split, slice_type), group in frame.groupby(["package_id", "tier_view", "split", "slice_type"], dropna=False):
        max_row = group.sort_values("decision_rate", ascending=False).iloc[0]
        min_row = group.sort_values("decision_rate", ascending=True).iloc[0]
        output.append(
            {
                "package_id": package_id,
                "tier_view": tier_view,
                "split": split,
                "slice_type": slice_type,
                "max_slice_value": max_row["slice_value"],
                "max_decision_rate": finite_or_blank(float(max_row["decision_rate"])),
                "min_slice_value": min_row["slice_value"],
                "min_decision_rate": finite_or_blank(float(min_row["decision_rate"])),
                "decision_rate_spread": finite_or_blank(float(max_row["decision_rate"] - min_row["decision_rate"])),
                "screen_claim": "screening_input_only_not_trading_kpi",
            }
        )
    return output


def data_integrity_payload(hashes: Mapping[str, str], queue_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "data_source": "run271D score summaries(271D 점수 요약) and score tables(점수표)",
        "time_axis": "run271E(271E 실행)는 새 bar(봉)를 만들지 않고 run271D(271D 실행)의 timestamp(타임스탬프) 정체성을 소비한다.",
        "sample_scope": "Tier A separate, Tier B separate, Tier A+B combined(티어 A 분리, 티어 B 분리, 티어 A+B 합산) screening records(선별 기록)",
        "missing_or_duplicate_check": "source manifest(원천 목록)과 tier receipt(티어 영수증)가 존재한다.",
        "feature_label_boundary": "signal alignment(신호 정렬)은 run271D(271D 실행) decision flag(판단 플래그) 생성 뒤 판독으로만 사용한다.",
        "split_boundary": "train/validation/oos(학습/검증/표본외) split(분할)을 보존하고 validation/oos(검증/표본외)를 조율에 쓰지 않는다.",
        "leakage_risk": "screening rule(선별 규칙)이 label(라벨)을 후보 선택으로 쓰지 않고 probe seed(탐침 씨앗) 여부만 낮은 범위로 기록한다.",
        "data_hash_or_identity": dict(hashes),
        "integrity_judgment": "usable_with_boundary",
        "queue_rows": len(queue_rows),
    }


def model_validation_payload(queue_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "model_family": "deterministic score surface screen(결정적 점수 표면 선별), no trained model(학습 모델 없음)",
        "target_and_label": "label alignment(라벨 정렬)은 structural scout(구조 스카우트) 판독일 뿐 trading target(거래 목표)이 아니다.",
        "split_method": "fixed train/validation/oos(고정 학습/검증/표본외)",
        "selection_metric": "probe seed screen(탐침 씨앗 선별), not selected candidate(선택 후보 아님)",
        "secondary_metrics": "decision supply(판단 공급), Tier A/B symmetry(티어 A/B 대칭), route balance(경로 균형), weak slice spread(약한 구간 분산)",
        "threshold_policy": "no new threshold selected(새 임계값 선택 없음)",
        "overfit_risk": "validation(검증) alignment(정렬률)이 cp271B(271B 패키지)에만 약하게 남아 있어 Stage272(272단계) 압박 검증이 필요하다.",
        "calibration_risk": "scores(점수)는 probability(확률)가 아니라 rank/ordering(순위/정렬)이다.",
        "comparison_baseline": "cp271D support control(보조 대조), Stage270 failure memory(270단계 실패 기억)",
        "validation_judgment": JUDGMENT,
        "queued_probe_seed_count": len(queue_rows),
    }


def result_rows(queue_rows: Sequence[Mapping[str, Any]], failure_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, str]]:
    return [
        {
            "result_subject": RUN_ID,
            "evidence_available": "screening_summary;stage272_probe_queue;failure_memory;support_control;weak_slice_screen;receipts;ledgers",
            "evidence_missing": "MT5 runtime probe;balance/equity curve;trade quality;Adapter package;ONNX export/parity;MT5 runtime reproduction",
            "judgment_label": "exploratory_probe_seed_screen",
            "claim_boundary": BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": f"probe seed(탐침 씨앗) {len(queue_rows)}개와 failure memory(실패 기억) {len(failure_rows)}개를 만들었지만 선택 후보는 아니다.",
        }
    ]


def manifest_payload(
    hashes: Mapping[str, str],
    output_hashes: Mapping[str, str],
    screened: int,
    queue_rows: int,
    failure_rows: int,
    support_rows: int,
) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run": SOURCE_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "producer": rel(ROOT / PRODUCER_PATH),
        "entry_command": f"python {PRODUCER_PATH.as_posix()}",
        "created_at_utc": utc_now(),
        "source_inputs": list(hashes.keys()),
        "source_hashes": dict(hashes),
        "output_artifacts": list(output_hashes.keys()),
        "output_hashes": dict(output_hashes),
        "screened_packages": screened,
        "stage272_probe_queue_rows": queue_rows,
        "failure_memory_rows": failure_rows,
        "support_control_rows": support_rows,
        "scoreboard": "structural_scout",
        "parity_level": "P1_dataset_feature_aligned",
        "wfo_status": "not_applicable",
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "external_verification_status": "out_of_scope_by_claim_score_screening_only",
        "claim_boundary": BOUNDARY,
        "next_action": NEXT_ACTION,
    }


def lineage_payload(paths: Sequence[Path], hashes: Mapping[str, str]) -> dict[str, Any]:
    return {
        "source_inputs": dict(hashes),
        "producer": rel(ROOT / PRODUCER_PATH),
        "consumer": NEXT_ACTION,
        "artifact_paths": [rel(path) for path in paths],
        "artifact_hashes": {rel(path): sha256_file(path) for path in paths if path_exists(path)},
        "registry_links": {
            "run_registry": rel(RUN_REGISTRY),
            "alpha_ledger": rel(ALPHA_LEDGER),
            "stage_ledger": rel(STAGE_LEDGER),
            "artifact_registry": rel(ARTIFACT_REGISTRY),
        },
        "availability": "tracked_or_reproducible_from_command",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": BOUNDARY,
    }


def report_markdown(screening_rows: Sequence[Mapping[str, Any]], queue_rows: Sequence[Mapping[str, Any]], failure_rows: Sequence[Mapping[str, Any]]) -> str:
    screen_lines = "\n".join(
        f"- `{row['package_id']}`: judgment(판정) `{row['screening_judgment']}`, val_align(검증 정렬) `{row['tier_a_validation_alignment']}`, oos_align(표본외 정렬) `{row['tier_a_oos_alignment']}`"
        for row in screening_rows
    )
    queue_line = "; ".join(str(row["package_id"]) for row in queue_rows) if queue_rows else "none"
    failure_line = "; ".join(str(row["package_id"]) for row in failure_rows) if failure_rows else "none"
    return f"""# run271E Fresh Edge Score Surface Screen(271E 새 거래 우위 점수 표면 선별)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- scoreboard(점수판): `structural_scout(구조 스카우트)`
- stage272_probe_queue_rows(272단계 탐침 대기열 행): `{len(queue_rows)}`
- failure_memory_rows(실패 기억 행): `{len(failure_rows)}`
- queued_seed(대기열 씨앗): `{queue_line}`
- failure_memory_packages(실패 기억 패키지): `{failure_line}`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Plain Result(쉬운 결과)

run271E(271E 실행)는 run271D(271D 실행)의 score table(점수표)을 후보 선택이 아니라 다음 압박 탐침(probe, 탐침)용으로 선별했다.
효과(effect, 효과): `cp271B_time_risk_phase_router_surface`는 Stage272(272단계) pressure probe(압박 탐침) seed(씨앗)로만 보존하고, cp271A/cp271C(271A/271C 패키지)는 같은 형태로 반복하지 않도록 failure memory(실패 기억)에 둔다.

## Screening Rows(선별 행)

{screen_lines}

## Gate Coverage(게이트 커버리지)

- measurement_scope(측정 범위): structural_scout(구조 스카우트) signal KPI(신호 KPI)만 사용했다.
- management_state(관리 상태): run manifest(실행 목록), screening summary(선별 요약), queue(대기열), failure memory(실패 기억), ledgers(장부)를 만들었다.
- judgment_class(판정 분류): exploratory(탐색) probe seed screen(탐침 씨앗 선별)이다.
- parity_level(동등성 수준): `P1_dataset_feature_aligned(P1 데이터셋 피처 정렬)`까지만 주장한다.
- hard_gate_applicable(강한 게이트 적용): `no(아니오)`, operating promotion(운영 승격)이나 runtime authority(런타임 권위)가 아니다.
- final_claim_guard(최종 주장 방어): selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.

## Boundary(경계)

`{BOUNDARY}`
"""


def write_selection_status() -> None:
    text = f"""# Stage271 Selection Status(271단계 선택 상태)

- stage_status(단계 상태): `{STATUS}`
- current_packet(현재 작업 묶음): `stage271_fresh_edge_rebuild_after_nonfilter_failure_v1`
- current_run(현재 실행): `{RUN_ID}`
- last_completed_run(마지막 완료 실행): `{RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준선): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- package_screening_summary(패키지 선별 요약): `{rel(SCREENING_SUMMARY)}`
- stage272_probe_queue(272단계 탐침 대기열): `{rel(STAGE272_QUEUE)}`
- screening_failure_memory(선별 실패 기억): `{rel(FAILURE_MEMORY)}`
- next_action(다음 행동): `{NEXT_ACTION}`

## Current Meaning(현재 의미)

run271E(271E 실행)는 cp271B(271B 패키지)를 probe seed(탐침 씨앗)로만 보존했다.
효과(effect, 효과): 다음에는 Stage271(271단계)을 닫고 Stage272(272단계)에서 압박 검증을 열 수 있지만, 아직 candidate package(후보 패키지) 선택이나 ONNX readiness(온엑스 준비)는 없다.

## Boundary(경계)

`{BOUNDARY}`
"""
    write_md(SELECTION_STATUS, text)


def write_review_index() -> None:
    text = f"""# Stage271 Review Index(271단계 검토 색인)

## Current State(현재 상태)

Stage271(271단계)은 run271E(271E 실행) score surface screen(점수 표면 선별)까지 완료됐다.
효과(effect, 효과): cp271B(271B 패키지)를 Stage272(272단계) pressure probe(압박 탐침) seed(씨앗)로 넘길 수 있는 대기열을 만들었다.

## Reports(보고서)

- run271A report(271A 보고서): `stages/271_onnx_candidate_campaign__fresh_edge_rebuild_after_nonfilter_failure/03_reviews/run271A_report.md`
- run271B report(271B 보고서): `stages/271_onnx_candidate_campaign__fresh_edge_rebuild_after_nonfilter_failure/03_reviews/run271B_report.md`
- run271C report(271C 보고서): `stages/271_onnx_candidate_campaign__fresh_edge_rebuild_after_nonfilter_failure/03_reviews/run271C_report.md`
- run271D report(271D 보고서): `stages/271_onnx_candidate_campaign__fresh_edge_rebuild_after_nonfilter_failure/03_reviews/run271D_report.md`
- run271E report(271E 보고서): `{rel(RUN_REPORT)}`
- run271E stage272 queue(271E 272단계 대기열): `{rel(STAGE272_QUEUE)}`
"""
    write_md(REVIEW_INDEX, text)


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def append_once(text: str, marker: str, addition: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + addition.rstrip() + "\n"


def prepend_focus(text: str, focus: str, marker: str) -> str:
    if marker in text:
        return text
    anchor = "current_focus:\n"
    if anchor in text:
        return text.replace(anchor, anchor + focus, 1)
    return text.rstrip() + "\ncurrent_focus:\n" + focus


def update_state_docs(queue_rows: int, failure_rows: int) -> None:
    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- target_surface(목표 표면):", "- target_surface(목표 표면): `fresh_edge_score_surface_screen`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run271E_summary(271E 요약)",
        f"- run271E_summary(271E 요약): run271E(271E 실행)는 Stage272 probe queue(272단계 탐침 대기열) `{queue_rows}`행과 failure memory(실패 기억) `{failure_rows}`행을 만들었다. Effect(효과): cp271B(271B 패키지)는 probe seed(탐침 씨앗)로만 남기고 selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE_ID}")
    focus = (
        "- >-\n"
        f"  Stage271(271단계) run271E(271E 실행) fresh edge score surface screen(새 거래 우위 점수 표면 선별) `{RUN_ID}`. "
        f"Effect(효과): Stage272 probe queue(272단계 탐침 대기열) `{queue_rows}`행과 failure memory(실패 기억) `{failure_rows}`행을 만들었고, selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus, "Stage271(271단계) run271E(271E 실행)")
    write_md(WORKSPACE_STATE, workspace)

    change = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    change = append_once(
        change,
        RUN_ID,
        f"## 2026-05-23 run271E fresh edge score surface screen(271E 새 거래 우위 점수 표면 선별)\n\n- status(상태): `{STATUS}`\n- judgment(판정): `{JUDGMENT}`\n- effect(효과): cp271B(271B 패키지)를 Stage272(272단계) pressure probe(압박 탐침) seed(씨앗)로 넘기는 queue(대기열)를 만들었다.\n- boundary(경계): selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n",
    )
    write_md(CHANGELOG, change)


def update_register_docs(queue_rows: int, failure_rows: int) -> None:
    idea = io_path(IDEA_REGISTER).read_text(encoding="utf-8-sig")
    idea = append_once(
        idea,
        "IDEA-ST271-CP271B-TIME-RISK-PHASE-ROUTER",
        "| `IDEA-ST271-CP271B-TIME-RISK-PHASE-ROUTER` | `271_onnx_candidate_campaign__fresh_edge_rebuild_after_nonfilter_failure` | time-risk phase router(시간 위험 국면 라우터)가 Stage270(270단계) 실패 뒤 약한 구간을 분리할 수 있다 | `Tier A + Tier B paired structural scout(Tier A + Tier B 쌍 구조 스카우트)` | `probe_seed_not_candidate` | run271E(271E 실행); Stage272 probe queue(272단계 탐침 대기열) 1행, selected candidate(선택 후보) 아님 |",
    )
    write_md(IDEA_REGISTER, idea)

    negative = io_path(NEGATIVE_REGISTER).read_text(encoding="utf-8-sig")
    negative = append_once(
        negative,
        "NR-036",
        "| `NR-036` | `IDEA-ST271-FRESH-EDGE-REBUILD-AFTER-NONFILTER-FAILURE` | cp271A damage-first loss asymmetry(손상 우선 손실 비대칭)와 cp271C recovery-tail payoff rebalance(회복 꼬리 보상 재균형)가 Stage272(272단계) 탐침 씨앗이 될 수 있다 | run271E(271E 실행)에서 cp271A는 validation/OOS(검증/표본외) alignment(정렬률)가 약하고 route bias(경로 편향)가 있었으며, cp271C는 Tier A/Tier B(티어 A/티어 B) decision rate(판단 비율)가 크게 갈라졌다 | 손실 비대칭과 회복 보상 축은 버리지 않지만 같은 score surface(점수 표면) 그대로 반복하지 않는다 | partial-context adapter(부분 문맥 어댑터) 또는 새 decision surface(판단 표면)가 생길 때 |",
    )
    write_md(NEGATIVE_REGISTER, negative)


def update_registers(created_at: str, artifacts: Sequence[Path], screened: int, queue_rows: int, failure_rows: int, support_rows: int) -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "kpi_evidence",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(RUN_REPORT),
                "notes": f"screened_packages={screened};stage272_queue_rows={queue_rows};failure_memory_rows={failure_rows};selected_candidate=none;onnx_readiness=not_claimed.",
            }
        ],
        key="run_id",
    )
    alpha_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__tier_a_screen",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "tier_a_screen",
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": "Tier A score surface screen(티어 A 점수 표면 선별)",
            "tier_scope": "Tier A separate",
            "kpi_scope": "structural_signal_screening",
            "scoreboard_lane": "structural_scout",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": rel(SCREENING_SUMMARY),
            "primary_kpi": f"stage272_queue_rows={queue_rows};failure_memory_rows={failure_rows}",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed;trading_kpi=none",
            "external_verification_status": "out_of_scope_by_claim_score_screening_only",
            "notes": "Tier A structural screen completed.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__tier_b_screen",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "tier_b_screen",
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": "Tier B score surface screen(티어 B 점수 표면 선별)",
            "tier_scope": "Tier B separate",
            "kpi_scope": "structural_signal_screening",
            "scoreboard_lane": "structural_scout",
            "status": STATUS,
            "judgment": "partial_context_screen_completed_with_boundary",
            "path": rel(SCREENING_SUMMARY),
            "primary_kpi": f"support_control_rows={support_rows};partial_context_checked=yes",
            "guardrail_kpi": "no_fallback_authority_claimed",
            "external_verification_status": "out_of_scope_by_claim_score_screening_only",
            "notes": "Tier B used only for paired exploration screen.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__tier_ab_screen",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "tier_ab_screen",
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": "Tier A+B score surface screen(티어 A+B 점수 표면 선별)",
            "tier_scope": "Tier A+B combined",
            "kpi_scope": "structural_signal_screening",
            "scoreboard_lane": "structural_scout",
            "status": STATUS,
            "judgment": "combined_screen_view_no_routed_pnl_claim",
            "path": rel(STAGE272_QUEUE),
            "primary_kpi": f"stage272_queue_rows={queue_rows}",
            "guardrail_kpi": "performance_claim=none;synthetic_screen_view_only",
            "external_verification_status": "out_of_scope_by_claim_score_screening_only",
            "notes": "Combined record is screen view, not routed account performance.",
        },
    ]
    upsert_csv_rows(ALPHA_LEDGER, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    upsert_csv_rows(
        STAGE_LEDGER,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__score_surface_screen",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "fresh_edge_score_surface_screen",
                "tier_scope": "Tier A+B paired score surface screen",
                "scoreboard": "structural_scout",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "probe_seed_only_no_candidate_no_onnx",
                "report_path": rel(RUN_REPORT),
                "notes": f"stage272_queue_rows={queue_rows};next_action={NEXT_ACTION}.",
            }
        ],
        key="row_id",
    )
    if path_exists(ARTIFACT_REGISTRY):
        existing = [row for row in read_csv_rows(ARTIFACT_REGISTRY) if str(row.get("run_id", "")).strip() != RUN_ID]
        write_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, existing)
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{path.name.replace('.', '_')}",
            "artifact_type": "run271E_score_screen_artifact",
            "path": rel(path),
            "sha256": sha256_file(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run271E fresh edge score surface screen artifact.",
        }
        for path in artifacts
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")


def execute() -> dict[str, Any]:
    source_paths = [
        SOURCE_MANIFEST,
        SOURCE_SCORE_SUMMARY,
        SOURCE_SIGNAL_SUMMARY,
        SOURCE_WEAK_SUMMARY,
        SOURCE_TIER_RECEIPTS,
        SOURCE_THRESHOLD_RECEIPT,
        SOURCE_HANDOFF_RESOLUTION,
        SOURCE_DATA_INTEGRITY,
        SOURCE_MODEL_VALIDATION,
        SOURCE_LINEAGE,
        SOURCE_RESULT_JUDGMENT,
        SOURCE_REPORT,
        *sorted(RUN271D_SCORES.glob("*.parquet")),
        *sorted(RUN271D_HANDOFF.glob("*.json")),
    ]
    must_exist(source_paths)
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    hashes = source_hashes(source_paths)
    score_rows = read_csv_rows(SOURCE_SCORE_SUMMARY)
    signal_rows = read_csv_rows(SOURCE_SIGNAL_SUMMARY)
    weak_rows = read_csv_rows(SOURCE_WEAK_SUMMARY)

    screening_rows = build_screening_rows(score_rows, signal_rows)
    queue_rows = build_stage272_queue(screening_rows)
    failure_rows = build_failure_memory(screening_rows)
    support_rows = build_support_control_rows(screening_rows)
    weak_screen_rows = build_weak_slice_screen(weak_rows)

    write_csv(
        SCREENING_SUMMARY,
        (
            "package_id",
            "package_role",
            "fresh_thesis",
            "tier_a_train_decision_rate",
            "tier_a_validation_decision_rate",
            "tier_a_oos_decision_rate",
            "tier_b_validation_decision_rate",
            "tier_b_oos_decision_rate",
            "tier_ab_decision_rate_delta",
            "tier_a_validation_alignment",
            "tier_a_oos_alignment",
            "tier_a_validation_long_share",
            "tier_a_oos_long_share",
            "tier_a_validation_avg_score",
            "tier_a_oos_avg_score",
            "structural_screen_score",
            "screening_judgment",
            "next_action",
            "reason",
            "reopen_condition",
            "do_not_repeat_note",
            "selected_candidate",
            "onnx_readiness",
            "performance_claim",
        ),
        screening_rows,
    )
    write_csv(
        STAGE272_QUEUE,
        (
            "queue_id",
            "package_id",
            "source_run",
            "queue_role",
            "required_support_control",
            "fresh_thesis",
            "upside_condition",
            "failure_mode_to_watch",
            "discard_condition",
            "required_evidence",
            "claim_boundary",
        ),
        queue_rows,
    )
    write_csv(
        FAILURE_MEMORY,
        (
            "package_id",
            "failed_boundary",
            "why_failed_or_not_ready",
            "salvage_value",
            "reopen_condition",
            "do_not_repeat_note",
        ),
        failure_rows,
    )
    write_csv(
        SUPPORT_CONTROL_CARRY,
        ("package_id", "support_role", "screening_judgment", "carry_condition", "claim_boundary"),
        support_rows,
    )
    write_csv(
        WEAK_SLICE_SCREEN,
        (
            "package_id",
            "tier_view",
            "split",
            "slice_type",
            "max_slice_value",
            "max_decision_rate",
            "min_slice_value",
            "min_decision_rate",
            "decision_rate_spread",
            "screen_claim",
        ),
        weak_screen_rows,
    )
    write_json(
        SCREENING_RECEIPT,
        {
            "measurement_scope": "structural_scout signal KPI(구조 스카우트 신호 KPI)",
            "management_state": "manifest, screening summary, queue, failure memory, ledgers created(목록/선별 요약/대기열/실패 기억/장부 생성)",
            "judgment_class": "exploratory(탐색)",
            "scoreboard": "structural_scout",
            "parity_level": "P1_dataset_feature_aligned",
            "wfo_status": "not_applicable",
            "registry_update_required": "yes",
            "negative_memory_required": "yes",
            "hard_gate_applicable": "no",
            "evidence_boundary": "scout-only",
            "claim_boundary": BOUNDARY,
        },
    )
    write_json(DATA_INTEGRITY_RECEIPT, data_integrity_payload(hashes, queue_rows))
    write_json(MODEL_VALIDATION_RECEIPT, model_validation_payload(queue_rows))
    write_csv(RESULT_JUDGMENT, RESULT_COLUMNS, result_rows(queue_rows, failure_rows))
    provisional_artifacts = [
        SCREENING_SUMMARY,
        STAGE272_QUEUE,
        FAILURE_MEMORY,
        SUPPORT_CONTROL_CARRY,
        WEAK_SLICE_SCREEN,
        SCREENING_RECEIPT,
        DATA_INTEGRITY_RECEIPT,
        MODEL_VALIDATION_RECEIPT,
        RESULT_JUDGMENT,
    ]
    output_hashes = {rel(path): sha256_file(path) for path in provisional_artifacts}
    write_json(
        RUN_MANIFEST,
        manifest_payload(
            hashes,
            output_hashes,
            len(screening_rows),
            len(queue_rows),
            len(failure_rows),
            len(support_rows),
        ),
    )
    write_md(RUN_REPORT, report_markdown(screening_rows, queue_rows, failure_rows))
    write_selection_status()
    write_review_index()
    artifacts = [
        RUN_MANIFEST,
        *provisional_artifacts,
        RUN_REPORT,
        SELECTION_STATUS,
        REVIEW_INDEX,
    ]
    write_json(ARTIFACT_LINEAGE_RECEIPT, lineage_payload([*artifacts, ARTIFACT_LINEAGE_RECEIPT], hashes))
    artifacts.append(ARTIFACT_LINEAGE_RECEIPT)
    created_at = utc_now()
    update_registers(created_at, artifacts, len(screening_rows), len(queue_rows), len(failure_rows), len(support_rows))
    update_state_docs(len(queue_rows), len(failure_rows))
    update_register_docs(len(queue_rows), len(failure_rows))
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "screened_packages": len(screening_rows),
        "stage272_probe_queue_rows": len(queue_rows),
        "failure_memory_rows": len(failure_rows),
        "support_control_rows": len(support_rows),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "report": rel(RUN_REPORT),
    }


def main() -> int:
    print(json.dumps(execute(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
