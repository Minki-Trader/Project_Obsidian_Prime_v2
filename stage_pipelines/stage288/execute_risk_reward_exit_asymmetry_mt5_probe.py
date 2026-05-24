from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.mt5_tier_balance_completion import (  # noqa: E402
    COMMON_FILES_ROOT_DEFAULT,
    METAEDITOR_PATH_DEFAULT,
    TERMINAL_DATA_ROOT_DEFAULT,
    TERMINAL_PATH_DEFAULT,
    TESTER_PROFILE_ROOT_DEFAULT,
)
from foundation.models.onnx_bridge import ordered_hash  # noqa: E402
from foundation.mt5 import runtime_support as mt5  # noqa: E402
from stage_pipelines.stage279 import execute_or_prepare_directional_runtime_mapping_mt5_probe as base  # noqa: E402


STAGE_ID = "288_onnx_candidate_campaign__risk_reward_exit_asymmetry_rebuild"
RUN_ID = "run288B_risk_reward_exit_asymmetry_mt5_probe_v1"
RUN_NUMBER = "run288B"
SOURCE_RUN_ID = "run288A_design_materialize_risk_reward_exit_asymmetry_candidates_v1"
STATUS_PREPARED = "prepared_risk_reward_exit_asymmetry_mt5_probe_no_runtime_kpi"
UPDATED_ON = "2026-05-24"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)
EXPLORATION_LABEL = "stage288_Model__RiskRewardExitAsymmetryReplay"
SIGNAL_COLUMN = "run288b_route_signal"
FEATURE_ORDER = (
    SIGNAL_COLUMN,
    "exit_close_long_flag",
    "exit_close_short_flag",
    "exit_max_hold_bars",
)
COMMON_ROOT = "Project_Obsidian_Prime_v2/stage288/run288B_risk_reward_exit_asymmetry"

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN288A = STAGE_ROOT / "02_runs" / "run288A"
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS = STAGE_ROOT / "03_reviews"
SELECTED = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
FEATURE_DIR = RUN_ROOT / "features"
MODEL_DIR = RUN_ROOT / "models"
MT5_DIR = RUN_ROOT / "mt5"
MT5_QUEUE = RUN288A / "mt5_probe_queue.csv"
SOURCE_MANIFEST = RUN288A / "candidate_payload_manifest.csv"
SOURCE_RUN_MANIFEST = RUN288A / "run_manifest.json"
PRODUCER = Path("stage_pipelines/stage288/execute_risk_reward_exit_asymmetry_mt5_probe.py")

ATTEMPT_SUMMARY = RUN_ROOT / "attempt_summary.csv"
RUNTIME_SUPPLY = RUN_ROOT / "runtime_supply_matrix.csv"
EXECUTION_RESULT = RUN_ROOT / "execution_result.json"
MT5_KPI_SUMMARY = RUN_ROOT / "mt5_kpi_summary.csv"
RUNTIME_PARITY_RECEIPT = RUN_ROOT / "runtime_parity_receipt.json"
RESULT_JUDGMENT = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT = RUN_ROOT / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
LINEAGE = RUN_ROOT / "artifact_lineage_receipt.json"
REPORT = REVIEWS / "run288B_risk_reward_exit_asymmetry_mt5_probe_report.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def bool_value(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def int_value(value: Any, default: int) -> int:
    try:
        text = str(value).strip()
        return int(float(text)) if text else default
    except (TypeError, ValueError):
        return default


def float_value(value: Any, default: float = 0.0) -> float:
    try:
        text = str(value).strip()
        return float(text) if text else default
    except (TypeError, ValueError):
        return default


def mt5_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def export_multifeature_signal_score_table(path: Path, feature_order: Sequence[str]) -> dict[str, Any]:
    if not feature_order or feature_order[0] != SIGNAL_COLUMN:
        raise ValueError("first feature must be route signal")
    rows: list[dict[str, Any]] = [
        {"record_type": "intercept", "feature_index": -1, "item_index": -1, "value": "", "score_short": "0", "score_flat": "0", "score_long": "0"},
        {"record_type": "cut", "feature_index": 0, "item_index": 0, "value": "-0.5", "score_short": "", "score_flat": "", "score_long": ""},
        {"record_type": "cut", "feature_index": 0, "item_index": 1, "value": "0.5", "score_short": "", "score_flat": "", "score_long": ""},
        {"record_type": "score", "feature_index": 0, "item_index": 0, "value": "", "score_short": "4", "score_flat": "-4", "score_long": "-4"},
        {"record_type": "score", "feature_index": 0, "item_index": 1, "value": "", "score_short": "4", "score_flat": "-4", "score_long": "-4"},
        {"record_type": "score", "feature_index": 0, "item_index": 2, "value": "", "score_short": "-4", "score_flat": "4", "score_long": "-4"},
        {"record_type": "score", "feature_index": 0, "item_index": 3, "value": "", "score_short": "-4", "score_flat": "-4", "score_long": "4"},
    ]
    for feature_index in range(1, len(feature_order)):
        rows.extend(
            [
                {"record_type": "cut", "feature_index": feature_index, "item_index": 0, "value": "-0.5", "score_short": "", "score_flat": "", "score_long": ""},
                {"record_type": "cut", "feature_index": feature_index, "item_index": 1, "value": "0.5", "score_short": "", "score_flat": "", "score_long": ""},
            ]
        )
        for item_index in range(4):
            rows.append({"record_type": "score", "feature_index": feature_index, "item_index": item_index, "value": "", "score_short": "0", "score_flat": "0", "score_long": "0"})
    base.io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with base.io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=("record_type", "feature_index", "item_index", "value", "score_short", "score_flat", "score_long"), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return {
        "path": path.as_posix(),
        "sha256": base.sha256_file_lf_normalized(path),
        "format": "multifeature_route_signal_neutral_overlay_ebm_table_csv_v1",
        "feature_order": list(feature_order),
        "feature_order_hash": ordered_hash(feature_order),
        "runtime_policy": "feature0 route signal decides; extra features are neutral for model and available to exit overlay(0번 피처 경로 신호 결정, 추가 피처는 모델 중립/청산 오버레이용)",
    }


def configure_base() -> None:
    base.STAGE_ID = STAGE_ID
    base.RUN_ID = RUN_ID
    base.RUN_NUMBER = RUN_NUMBER
    base.SOURCE_RUN_ID = SOURCE_RUN_ID
    base.PARENT_RUN_ID = "run287C_review_density_scale_curve_pocket_mt5_probe_v1"
    base.STATUS_PREPARED = STATUS_PREPARED
    base.UPDATED_ON = UPDATED_ON
    base.BOUNDARY = BOUNDARY
    base.EXPLORATION_LABEL = EXPLORATION_LABEL
    base.SIGNAL_COLUMN = SIGNAL_COLUMN
    base.COMMON_ROOT = COMMON_ROOT
    base.STAGE_ROOT = STAGE_ROOT
    base.RUN279B = RUN288A
    base.RUN_ROOT = RUN_ROOT
    base.REVIEWS = REVIEWS
    base.SELECTED = SELECTED
    base.REPORT_PATH = REPORT
    base.FEATURE_DIR = FEATURE_DIR
    base.MODEL_DIR = MODEL_DIR
    base.MT5_DIR = MT5_DIR
    base.MT5_QUEUE = MT5_QUEUE
    base.RUN279B_MANIFEST = SOURCE_RUN_MANIFEST
    base.RUN279B_PAYLOAD_MANIFEST = SOURCE_MANIFEST
    base.RUN279B_SIGNAL_RECEIPT = SOURCE_MANIFEST
    base.RUN279B_REPORT = REVIEWS / "run288A_risk_reward_exit_asymmetry_materialization_report.md"
    base.RUN_REGISTRY = RUN_REGISTRY
    base.ALPHA_LEDGER = ALPHA_LEDGER
    base.ARTIFACT_REGISTRY = ARTIFACT_REGISTRY
    base.STAGE_LEDGER = STAGE_LEDGER
    base.CURRENT_STATE = CURRENT_STATE
    base.WORKSPACE_STATE = WORKSPACE_STATE
    base.CHANGELOG = CHANGELOG
    base.REVIEW_INDEX = REVIEW_INDEX
    base.PRODUCER_PATH = PRODUCER
    base.ATTEMPT_SUMMARY = ATTEMPT_SUMMARY
    base.RUNTIME_SUPPLY = RUNTIME_SUPPLY
    base.EXECUTION_RESULT = EXECUTION_RESULT
    base.MT5_KPI_SUMMARY = MT5_KPI_SUMMARY
    base.RUNTIME_PARITY_RECEIPT = RUNTIME_PARITY_RECEIPT
    base.RESULT_JUDGMENT = RESULT_JUDGMENT
    base.GATE_AUDIT = GATE_AUDIT
    base.RUN_MANIFEST = RUN_MANIFEST
    base.LINEAGE_RECEIPT = LINEAGE
    base.export_feature_matrices = export_feature_matrices
    base.build_all_attempts = build_all_attempts


def load_payload(queue_row: Mapping[str, str]) -> pd.DataFrame:
    payload_path = ROOT / str(queue_row["payload_path"])
    frame = pd.read_parquet(base.io_path(payload_path)).copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    frame[SIGNAL_COLUMN] = pd.to_numeric(frame["route_signal_value"], errors="coerce").fillna(0).astype("int8")
    for name in FEATURE_ORDER[1:]:
        if name not in frame.columns:
            frame[name] = 0.0
    frame["materialized_branch_id"] = str(queue_row.get("materialized_branch_id", ""))
    frame["queue_role"] = str(queue_row.get("queue_role", ""))
    return frame


def export_feature_matrices(
    queue_rows: Sequence[Mapping[str, str]],
) -> tuple[dict[str, Any], dict[str, pd.DataFrame], list[dict[str, Any]]]:
    feature_exports: dict[str, Any] = {}
    split_frames: dict[str, pd.DataFrame] = {}
    supply_rows: list[dict[str, Any]] = []
    metadata_columns = (
        "symbol",
        "split",
        "tier_scope",
        "materialized_branch_id",
        "package_id",
        "queue_role",
        "route_signal_value",
        "route_signal_label",
        "feature_order_hash",
    )
    for queue_row in queue_rows:
        token = base.variant_token(queue_row)
        materialized_id = str(queue_row["materialized_branch_id"])
        package_id = str(queue_row["package_id"])
        payload = load_payload(queue_row)
        for tier_key, tier_label, tier_scope in (("tier_a", mt5.TIER_A, "Tier A"), ("tier_b", mt5.TIER_B, "Tier B")):
            tier_frame = payload.loc[payload["tier_scope"].astype(str).eq(tier_scope)].copy()
            for source_split, runtime_split, split_token in (("validation", "validation_is", "val"), ("oos", "oos", "oos")):
                split_frame = tier_frame.loc[tier_frame["split"].astype(str).eq(source_split)].copy()
                split_frame["runtime_split"] = runtime_split
                key = f"{materialized_id}__{tier_key}__{runtime_split}"
                out_path = FEATURE_DIR / f"{token}_{tier_key}_{split_token}_features.csv"
                feature_exports[key] = mt5.export_mt5_feature_matrix_csv(
                    split_frame,
                    FEATURE_ORDER,
                    out_path,
                    metadata_columns=metadata_columns,
                )
                split_frames[key] = split_frame
                nonflat = int(split_frame[SIGNAL_COLUMN].ne(0).sum())
                rows = int(len(split_frame))
                supply_rows.append(
                    {
                        "queue_id": queue_row.get("queue_id", ""),
                        "materialized_branch_id": materialized_id,
                        "package_id": package_id,
                        "queue_role": queue_row.get("queue_role", ""),
                        "tier_scope": tier_label,
                        "split": runtime_split,
                        "rows": rows,
                        "nonflat_signal_count": nonflat,
                        "long_signal_count": int(split_frame[SIGNAL_COLUMN].eq(1).sum()),
                        "short_signal_count": int(split_frame[SIGNAL_COLUMN].eq(-1).sum()),
                        "nonflat_signal_rate": round(float(nonflat / rows) if rows else 0.0, 8),
                        "feature_matrix_path": base.rel(out_path),
                        "feature_matrix_hash": feature_exports[key]["sha256"],
                    }
                )
    return feature_exports, split_frames, supply_rows


def extra_set_values(queue_row: Mapping[str, str]) -> dict[str, Any]:
    return {
        "InpEntryTransitionOnly": False,
        "InpReentryCooldownBars": 0,
        "InpSameDirectionReentryCooldownBars": int_value(queue_row.get("same_direction_reentry_cooldown_bars"), 0),
        "InpAtrSltpEnabled": bool_value(queue_row.get("atr_sltp_enabled")),
        "InpAtrPeriod": int_value(queue_row.get("atr_period"), 14),
        "InpAtrStopMultiplier": float_value(queue_row.get("atr_stop_multiplier"), 0.0),
        "InpAtrTakeProfitMultiplier": float_value(queue_row.get("atr_take_profit_multiplier"), 0.0),
        "InpAtrMinStopPoints": float_value(queue_row.get("atr_min_stop_points"), 0.0),
        "InpAtrMaxStopPoints": float_value(queue_row.get("atr_max_stop_points"), 0.0),
        "InpAtrMinTakeProfitPoints": float_value(queue_row.get("atr_min_take_profit_points"), 0.0),
        "InpAtrMaxTakeProfitPoints": float_value(queue_row.get("atr_max_take_profit_points"), 0.0),
        "InpExitRiskOverlayEnabled": bool_value(queue_row.get("exit_risk_overlay_enabled")),
        "InpExitRiskCloseLongFeatureIndex": int_value(queue_row.get("exit_risk_close_long_feature_index"), -1),
        "InpExitRiskCloseShortFeatureIndex": int_value(queue_row.get("exit_risk_close_short_feature_index"), -1),
        "InpExitRiskCloseThreshold": float_value(queue_row.get("exit_risk_close_threshold"), 0.5),
        "InpExitRiskMinHoldBars": int_value(queue_row.get("exit_risk_min_hold_bars"), 0),
        "InpExitRiskMaxHoldFeatureIndex": int_value(queue_row.get("exit_risk_max_hold_feature_index"), -1),
        "InpModelRiskSizingEnabled": bool_value(queue_row.get("model_risk_sizing_enabled")),
        "InpModelRiskMinPct": float_value(queue_row.get("model_risk_min_pct"), 0.005),
        "InpModelRiskMaxPct": float_value(queue_row.get("model_risk_max_pct"), 0.015),
        "InpModelRiskConfidenceFloor": float_value(queue_row.get("model_risk_confidence_floor"), 0.55),
        "InpModelRiskConfidenceCeiling": float_value(queue_row.get("model_risk_confidence_ceiling"), 0.99),
        "InpModelRiskFallbackLot": float_value(queue_row.get("model_risk_fallback_lot"), 0.10),
    }


def attach_identity(attempt: dict[str, Any], queue_row: Mapping[str, str]) -> None:
    base.attach_attempt_identity(attempt, queue_row)
    attempt["stage288_branch_id"] = queue_row.get("stage288_branch_id", "")
    attempt["max_hold_bars"] = int_value(queue_row.get("max_hold_bars"), 12)
    attempt["close_on_flat_signal"] = bool_value(queue_row.get("close_on_flat_signal"))
    attempt["atr_stop_multiplier"] = float_value(queue_row.get("atr_stop_multiplier"), 0.0)
    attempt["atr_take_profit_multiplier"] = float_value(queue_row.get("atr_take_profit_multiplier"), 0.0)


def build_all_attempts(
    queue_rows: Sequence[Mapping[str, str]],
    feature_exports: Mapping[str, Any],
    split_frames: Mapping[str, pd.DataFrame],
    model_artifact: Mapping[str, Any],
    *,
    include_routed: bool,
) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    model_name = Path(str(model_artifact["path"])).name
    feature_hash = ordered_hash(FEATURE_ORDER)
    for queue_row in queue_rows:
        materialized_id = str(queue_row["materialized_branch_id"])
        token = base.variant_token(queue_row, 44)
        max_hold = int_value(queue_row.get("max_hold_bars"), 12)
        close_on_flat = bool_value(queue_row.get("close_on_flat_signal"))
        extras = extra_set_values(queue_row)
        for runtime_split, split_token in (("validation_is", "val"), ("oos", "oos")):
            for tier_key, tier_label, tier_token in (("tier_a", mt5.TIER_A, "tier_a"), ("tier_b", mt5.TIER_B, "tier_b")):
                key = f"{materialized_id}__{tier_key}__{runtime_split}"
                from_date, to_date = base.split_dates(split_frames[key])
                feature_name = Path(str(feature_exports[key]["path"])).name
                attempt = base.attempt_payload(
                    run_root=RUN_ROOT,
                    run_id=RUN_ID,
                    stage_number=288,
                    exploration_label=EXPLORATION_LABEL,
                    attempt_name=f"{token}_{tier_token}_{split_token}",
                    tier=tier_label,
                    split=runtime_split,
                    model_path=f"{COMMON_ROOT}/models/{model_name}",
                    model_id=f"{RUN_ID}_{token}_{tier_token}_route_signal_table",
                    model_backend="ebm_table",
                    feature_path=f"{COMMON_ROOT}/features/{feature_name}",
                    feature_count=len(FEATURE_ORDER),
                    feature_order_hash=feature_hash,
                    short_threshold=0.55,
                    long_threshold=0.55,
                    min_margin=0.0,
                    invert_signal=False,
                    from_date=from_date,
                    to_date=to_date,
                    primary_active_tier=tier_key,
                    attempt_role="tier_only_total" if tier_key == "tier_a" else "tier_b_fallback_only_total",
                    record_view_prefix=f"mt5_{token}_{tier_token}",
                    max_hold_bars=max_hold,
                    common_root=COMMON_ROOT,
                    close_on_flat_signal=close_on_flat,
                    reverse_on_opposite_signal=True,
                    close_only_on_opposite_signal=False,
                    extra_set_values=extras,
                )
                attach_identity(attempt, queue_row)
                attempt["signal_policy"] = "route signal with neutral overlay features(경로 신호 + 중립 오버레이 피처)"
                attempts.append(attempt)
            if include_routed:
                tier_a_key = f"{materialized_id}__tier_a__{runtime_split}"
                tier_b_key = f"{materialized_id}__tier_b__{runtime_split}"
                from_date, to_date = base.split_dates(split_frames[tier_a_key])
                tier_a_feature = Path(str(feature_exports[tier_a_key]["path"])).name
                tier_b_feature = Path(str(feature_exports[tier_b_key]["path"])).name
                attempt = base.attempt_payload(
                    run_root=RUN_ROOT,
                    run_id=RUN_ID,
                    stage_number=288,
                    exploration_label=EXPLORATION_LABEL,
                    attempt_name=f"{token}_routed_{split_token}",
                    tier=mt5.TIER_AB,
                    split=runtime_split,
                    model_path=f"{COMMON_ROOT}/models/{model_name}",
                    model_id=f"{RUN_ID}_{token}_tier_a_route_signal_table",
                    model_backend="ebm_table",
                    feature_path=f"{COMMON_ROOT}/features/{tier_a_feature}",
                    feature_count=len(FEATURE_ORDER),
                    feature_order_hash=feature_hash,
                    short_threshold=0.55,
                    long_threshold=0.55,
                    min_margin=0.0,
                    invert_signal=False,
                    from_date=from_date,
                    to_date=to_date,
                    primary_active_tier="tier_a",
                    attempt_role="actual_routed_total",
                    record_view_prefix=f"mt5_{token}_actual_routed",
                    max_hold_bars=max_hold,
                    common_root=COMMON_ROOT,
                    fallback_enabled=True,
                    fallback_model_path=f"{COMMON_ROOT}/models/{model_name}",
                    fallback_model_id=f"{RUN_ID}_{token}_tier_b_route_signal_table",
                    fallback_model_backend="ebm_table",
                    fallback_feature_path=f"{COMMON_ROOT}/features/{tier_b_feature}",
                    fallback_feature_count=len(FEATURE_ORDER),
                    fallback_feature_order_hash=feature_hash,
                    fallback_short_threshold=0.55,
                    fallback_long_threshold=0.55,
                    fallback_min_margin=0.0,
                    fallback_invert_signal=False,
                    close_on_flat_signal=close_on_flat,
                    reverse_on_opposite_signal=True,
                    close_only_on_opposite_signal=False,
                    extra_set_values=extras,
                )
                attach_identity(attempt, queue_row)
                attempt["signal_policy"] = "Tier A primary + Tier B fallback with neutral overlay features(티어 A 우선 + 티어 B 대체, 중립 오버레이 피처)"
                attempts.append(attempt)
    return attempts


def prepare(args: argparse.Namespace) -> dict[str, Any]:
    queue_rows = base.load_queue_rows()
    feature_exports, split_frames, supply_rows = base.export_feature_matrices(queue_rows)
    base.write_csv(RUNTIME_SUPPLY, supply_rows)
    model_artifact = export_multifeature_signal_score_table(
        MODEL_DIR / "stage288_run288B_route_signal_neutral_overlay_score_table.csv",
        FEATURE_ORDER,
    )
    common_copies = base.copy_runtime_inputs(feature_exports, model_artifact, Path(args.common_files_root))
    full_attempts = base.build_all_attempts(queue_rows, feature_exports, split_frames, model_artifact, include_routed=not args.no_routed)
    start_index = max(0, int(args.start_index))
    end_index = start_index + int(args.limit) if args.limit is not None else None
    attempts = full_attempts[start_index:end_index]
    return {
        "stage_id": STAGE_ID,
        "stage_number": 288,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "source_run_id": SOURCE_RUN_ID,
        "run_root": RUN_ROOT,
        "attempts": attempts,
        "planned_attempt_count": len(full_attempts),
        "common_copies": common_copies,
        "feature_exports": feature_exports,
        "model_artifact": model_artifact,
        "runtime_supply_matrix": supply_rows,
        "route_coverage": base.route_coverage_from_supply(supply_rows),
        "model_family": "multifeature_discrete_signal_neutral_overlay_table",
        "feature_set_id": "stage288_risk_reward_exit_overlay_features",
        "label_id": "not_applicable_precomputed_route_signal",
        "split_contract": "Stage288 run288A payload split labels validation and oos",
        "claim_boundary": BOUNDARY,
    }


def classify_status(result: Mapping[str, Any], materialize_only: bool) -> tuple[str, str, str, str]:
    execution_results = list(result.get("execution_results", []))
    kpis = list(result.get("mt5_kpi_records", []))
    planned = int(result.get("planned_attempt_count", len(result.get("attempts", []))) or 0)
    limited = len(execution_results) < planned
    if materialize_only:
        return (STATUS_PREPARED, "risk_reward_exit_probe_prepared_no_external_execution", "out_of_scope_by_claim_materialize_only", "run288B_execute_risk_reward_exit_asymmetry_mt5_probe_external_check")
    completed_exec = sum(1 for item in execution_results if item.get("status") == "completed")
    if planned and completed_exec >= planned and len(kpis) >= planned:
        return ("completed_risk_reward_exit_asymmetry_mt5_probe_no_selection", "runtime_probe_completed_requires_curve_quality_review_no_selection", "completed", "run288C_review_risk_reward_exit_asymmetry_mt5_probe")
    if kpis:
        return ("partial_risk_reward_exit_asymmetry_mt5_probe_no_selection", "runtime_probe_partial_requires_continuation_or_review_no_selection", "partial_or_blocked", "run288B_continue_risk_reward_exit_asymmetry_mt5_probe" if limited else "run288C_review_with_runtime_gaps")
    return ("blocked_risk_reward_exit_asymmetry_mt5_probe_no_kpi", "runtime_probe_blocked_no_kpi_no_selection", "blocked_or_invalid", "run288B_repair_or_block_risk_reward_exit_asymmetry_mt5_probe")


def report_markdown(result: Mapping[str, Any], status: str, judgment: str, external_status: str, next_action: str) -> str:
    attempts = list(result.get("attempts", []))
    execution_results = list(result.get("execution_results", []))
    kpis = list(result.get("mt5_kpi_records", []))
    completed = sum(1 for item in execution_results if item.get("status") == "completed")
    blocked = sum(1 for item in execution_results if item.get("status") == "blocked")
    return f"""# run288B Risk Reward Exit Asymmetry MT5 Probe(288B 위험/보상/청산 비대칭 MT5 탐침)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{status}`
- judgment(판정): `{judgment}`
- external_verification_status(외부 검증 상태): `{external_status}`
- attempts(시도): `{len(execution_results)}/{len(attempts)}`
- completed_attempts(완료 시도): `{completed}`
- blocked_attempts(차단 시도): `{blocked}`
- mt5_kpi_records(MT5 KPI 기록): `{len(kpis)}`
- feature_order(피처 순서): `{ "|".join(FEATURE_ORDER) }`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- next_action(다음 행동): `{next_action}`

Effect(효과): run288A(288A 실행)의 risk/reward/exit(위험/보상/청산) 후보를 MT5(MetaTrader 5, 메타트레이더5) 테스터에 넘겼다. 선택 후보 판정은 run288C(288C 실행) 검토 전까지 보류한다.
"""


def rewrite_outputs(result: Mapping[str, Any], status: str, judgment: str, external_status: str, next_action: str, created_at: str) -> list[Path]:
    attempts = list(result.get("attempts", []))
    execution_results = list(result.get("execution_results", []))
    kpis = list(result.get("mt5_kpi_records", []))
    base.write_json(RUNTIME_PARITY_RECEIPT, {"run_id": RUN_ID, "feature_order": list(FEATURE_ORDER), "feature_order_hash": ordered_hash(FEATURE_ORDER), "runtime_claim_boundary": "runtime_probe_only_no_candidate_selection(런타임 탐침만, 후보 선택 없음)"})
    base.write_csv(RESULT_JUDGMENT, [{"result_subject": RUN_ID, "evidence_available": f"attempts={len(attempts)};execution_results={len(execution_results)};mt5_kpi_records={len(kpis)};report={base.rel(REPORT)}", "evidence_missing": "reviewed curve pockets;candidate package;Adapter package;ONNX parity;final candidate report", "judgment_label": judgment, "judgment_class": "runtime_probe(런타임 탐침)" if kpis else "blocked_or_prepared(차단 또는 준비)", "claim_boundary": BOUNDARY, "next_condition": next_action, "user_explanation_hook": "MT5 탐침 결과는 후보 선택 전 재료다."}], base.RESULT_COLUMNS)
    base.write_csv(GATE_AUDIT, [{"gate_name": "multifeature_handoff(다중 피처 인계)", "status": "passed", "evidence_path": base.rel(RUNTIME_SUPPLY), "effect": "route signal(경로 신호)과 exit overlay features(청산 오버레이 피처)를 EA에 넘긴다."}, {"gate_name": "external_runtime_attempt(외부 런타임 시도)", "status": external_status, "evidence_path": base.rel(EXECUTION_RESULT), "effect": "MT5 tester(MT5 테스터) 실행 또는 준비 상태를 남긴다."}, {"gate_name": "candidate_claim_boundary(후보 주장 경계)", "status": "passed", "evidence_path": base.rel(RESULT_JUDGMENT), "effect": "selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비)를 주장하지 않는다."}], base.GATE_COLUMNS)
    base.write_md(REPORT, report_markdown(result, status, judgment, external_status, next_action))
    final_paths = [EXECUTION_RESULT, ATTEMPT_SUMMARY, RUNTIME_SUPPLY, MT5_KPI_SUMMARY, RUNTIME_PARITY_RECEIPT, RESULT_JUDGMENT, GATE_AUDIT, REPORT]
    base.write_json(RUN_MANIFEST, {"run_id": RUN_ID, "stage_id": STAGE_ID, "source_run_id": SOURCE_RUN_ID, "status": status, "judgment": judgment, "external_verification_status": external_status, "created_at_utc": created_at, "attempt_count": len(attempts), "execution_result_count": len(execution_results), "mt5_kpi_record_count": len(kpis), "selected_candidate": "none", "adapter_package": "none", "onnx_readiness": "not_claimed", "goal_achieve": "not_claimed", "next_action": next_action, "claim_boundary": BOUNDARY, "output_hashes": {base.rel(path): base.sha256_file_lf_normalized(path) for path in final_paths if base.path_exists(path)}})
    final_paths.append(RUN_MANIFEST)
    base.write_json(LINEAGE, {"run_id": RUN_ID, "source_inputs": [base.rel(MT5_QUEUE), base.rel(SOURCE_MANIFEST), base.rel(SOURCE_RUN_MANIFEST), base.rel(ROOT / PRODUCER)], "producer": base.rel(ROOT / PRODUCER), "consumer": next_action, "artifact_paths": [base.rel(path) for path in final_paths if base.path_exists(path)], "artifact_hashes": {base.rel(path): base.sha256_file_lf_normalized(path) for path in final_paths if base.path_exists(path)}, "claim_boundary": BOUNDARY})
    final_paths.append(LINEAGE)
    return final_paths


def upsert_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], key: str) -> None:
    existing = base.read_csv_rows(path) if base.path_exists(path) else []
    new_keys = {str(row.get(key, "")).strip() for row in rows}
    merged = [row for row in existing if str(row.get(key, "")).strip() not in new_keys]
    merged.extend(dict(row) for row in rows)
    base.write_csv(path, merged, columns)


def upsert_ledgers(result: Mapping[str, Any], status: str, judgment: str, external_status: str, next_action: str) -> None:
    attempt_count = len(result.get("attempts", []))
    kpi_count = len(result.get("mt5_kpi_records", []))
    upsert_csv(RUN_REGISTRY, base.RUN_REGISTRY_COLUMNS, [{"run_id": RUN_ID, "stage_id": STAGE_ID, "lane": "risk_reward_exit_asymmetry_mt5_probe", "status": status, "judgment": judgment, "path": base.rel(REPORT), "notes": f"attempts={attempt_count};mt5_kpi_records={kpi_count};selected_candidate=none;onnx_readiness=not_claimed;next_action={next_action}."}], key="run_id")
    upsert_csv(ALPHA_LEDGER, base.ALPHA_LEDGER_COLUMNS, [{"ledger_row_id": f"{RUN_ID}__mt5_probe", "stage_id": STAGE_ID, "run_id": RUN_ID, "subrun_id": RUN_NUMBER, "parent_run_id": SOURCE_RUN_ID, "record_view": "risk_reward_exit_asymmetry_mt5_probe(위험/보상/청산 비대칭 MT5 탐침)", "tier_scope": "Tier A used/Tier B fallback stress/actual routed total", "kpi_scope": "runtime_probe", "scoreboard_lane": "risk_reward_exit_asymmetry", "status": status, "judgment": judgment, "path": base.rel(REPORT), "primary_kpi": f"attempts={attempt_count};mt5_kpi_records={kpi_count}", "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed", "external_verification_status": external_status, "notes": f"next_action={next_action}."}], key="ledger_row_id")
    upsert_csv(STAGE_LEDGER, base.STAGE_LEDGER_COLUMNS, [{"row_id": f"{RUN_ID}__mt5_probe", "stage_id": STAGE_ID, "run_id": RUN_ID, "view": "risk_reward_exit_asymmetry_mt5_probe", "tier_scope": "Tier A used/Tier B fallback stress/actual routed total", "scoreboard": "runtime_probe", "status": status, "judgment": judgment, "evidence_boundary": "runtime_probe_no_candidate_no_onnx", "report_path": base.rel(REPORT), "notes": f"attempts={attempt_count};mt5_kpi_records={kpi_count}."}], key="row_id")


def update_artifact_registry(paths: Sequence[Path], created_at: str) -> None:
    rows = [{"artifact_id": f"{RUN_ID}__{hashlib.sha1(base.rel(path).encode('utf-8')).hexdigest()[:12]}", "artifact_type": "stage288_risk_reward_exit_mt5_artifact", "path": base.rel(path), "sha256": base.sha256_file_lf_normalized(path), "stage_id": STAGE_ID, "run_id": RUN_ID, "created_at_utc": created_at, "notes": "run288B risk reward exit asymmetry MT5 probe(288B 위험/보상/청산 비대칭 MT5 탐침)"} for path in paths if base.path_exists(path)]
    upsert_csv(ARTIFACT_REGISTRY, base.ARTIFACT_COLUMNS, rows, key="artifact_id")


def update_docs(status: str, judgment: str, next_action: str, kpi_count: int, attempt_count: int) -> None:
    selected = base.io_path(SELECTED).read_text(encoding="utf-8-sig") if base.path_exists(SELECTED) else ""
    selected = base.replace_line_prefix(selected, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{status}`")
    selected = base.replace_line_prefix(selected, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = base.replace_line_prefix(selected, "- next_action(다음 행동):", f"- next_action(다음 행동): `{next_action}`")
    selected = base.append_once(selected, "run288B_report", f"- run288B_report(288B 보고서): `{base.rel(REPORT)}`")
    selected = base.append_once(selected, "run288B_execution_result", f"- run288B_execution_result(288B 실행 결과): `{base.rel(EXECUTION_RESULT)}`")
    base.write_md(SELECTED, selected)
    review_index = base.io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if base.path_exists(REVIEW_INDEX) else "# Stage288 Review Index(288단계 검토 색인)\n"
    review_index = base.append_once(review_index, "run288B_report", f"- run288B_report(288B 보고서): `{base.rel(REPORT)}`\n- run288B_execution_result(288B 실행 결과): `{base.rel(EXECUTION_RESULT)}`\n- run288B_mt5_kpi_summary(288B MT5 KPI 요약): `{base.rel(MT5_KPI_SUMMARY)}`")
    base.write_md(REVIEW_INDEX, review_index)
    current = base.io_path(CURRENT_STATE).read_text(encoding="utf-8-sig") if base.path_exists(CURRENT_STATE) else ""
    current = base.replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = base.replace_line_prefix(current, "- status(상태):", f"- status(상태): `{status}`")
    current = base.replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{next_action}`")
    current = base.append_once(current, "run288B_summary", f"- run288B_summary(288B 요약): risk/reward/exit asymmetry MT5 probe(위험/보상/청산 비대칭 MT5 탐침)를 실행했다. Effect(효과): attempts(시도) `{attempt_count}`개와 MT5 KPI records(MT5 KPI 기록) `{kpi_count}`개를 남겼고, 후보/어댑터/온엑스 주장은 하지 않는다.")
    base.write_md(CURRENT_STATE, current)
    workspace = base.io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig") if base.path_exists(WORKSPACE_STATE) else ""
    workspace = base.replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = base.replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = f"- >-\n  Stage288(288단계) run288B(288B 실행) risk reward exit asymmetry MT5 probe(위험/보상/청산 비대칭 MT5 탐침) `{RUN_ID}`. Effect(효과): attempts(시도) `{attempt_count}`개와 MT5 KPI records(MT5 KPI 기록) `{kpi_count}`개를 남겼고 selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비)는 주장하지 않는다.\n"
    workspace = base.prepend_focus(workspace, focus, RUN_ID)
    base.write_md(WORKSPACE_STATE, workspace)
    changelog = base.io_path(CHANGELOG).read_text(encoding="utf-8-sig") if base.path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    changelog = base.append_once(changelog, RUN_ID, f"## {UPDATED_ON} run288B Risk reward exit asymmetry MT5 probe(288B 위험/보상/청산 비대칭 MT5 탐침)\n\n- status(상태): `{status}`\n- judgment(판정): `{judgment}`\n- effect(효과): attempts(시도) `{attempt_count}`개와 MT5 KPI records(MT5 KPI 기록) `{kpi_count}`개를 기록했다.\n- boundary(경계): selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n")
    base.write_md(CHANGELOG, changelog)


def run_probe(args: argparse.Namespace) -> dict[str, Any]:
    configure_base()
    created_at = utc_now()
    for path in (RUN_ROOT, FEATURE_DIR, MODEL_DIR, MT5_DIR, REVIEWS):
        base.io_path(path).mkdir(parents=True, exist_ok=True)
    prepared = prepare(args)
    if args.materialize_only:
        result = {**prepared, "compile": {"status": "not_attempted_materialize_only"}, "execution_results": [], "strategy_tester_reports": [], "mt5_kpi_records": []}
    else:
        result = base.execute_prepared(prepared, terminal_path=Path(args.terminal_path), metaeditor_path=Path(args.metaeditor_path), terminal_data_root=Path(args.terminal_data_root), common_files_root=Path(args.common_files_root), tester_profile_root=Path(args.tester_profile_root), timeout_seconds=int(args.timeout_seconds), runtime_timeout_seconds=int(args.runtime_timeout_seconds))
    if args.merge_existing:
        result = base.merge_existing_result(result, start_index=max(0, int(args.start_index)), limit=args.limit)
    status, judgment, external_status, next_action = classify_status(result, bool(args.materialize_only))
    result = {**dict(result), "status": status, "judgment": judgment, "external_verification_status": external_status, "selected_candidate": "none", "selected_research_baseline": "none", "adapter_package": "none", "onnx_readiness": "not_claimed", "goal_achieve": "not_claimed", "next_action": next_action, "created_at_utc": created_at}
    base.write_outputs(result, status, judgment, external_status, next_action, created_at)
    final_paths = rewrite_outputs(result, status, judgment, external_status, next_action, created_at)
    upsert_ledgers(result, status, judgment, external_status, next_action)
    update_artifact_registry(final_paths, created_at)
    update_docs(status, judgment, next_action, len(result.get("mt5_kpi_records", [])), len(result.get("attempts", [])))
    return result


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Execute or prepare Stage288 risk reward exit asymmetry MT5 probe.")
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--start-index", type=int, default=0)
    parser.add_argument("--merge-existing", action="store_true")
    parser.add_argument("--no-routed", action="store_true")
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(METAEDITOR_PATH_DEFAULT))
    parser.add_argument("--terminal-data-root", default=str(TERMINAL_DATA_ROOT_DEFAULT))
    parser.add_argument("--common-files-root", default=str(COMMON_FILES_ROOT_DEFAULT))
    parser.add_argument("--tester-profile-root", default=str(TESTER_PROFILE_ROOT_DEFAULT))
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--runtime-timeout-seconds", type=int, default=180)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    result = run_probe(parse_args(argv or sys.argv[1:]))
    print(json.dumps({"run_id": RUN_ID, "status": result["status"], "judgment": result["judgment"], "external_verification_status": result["external_verification_status"], "attempt_count": len(result.get("attempts", [])), "planned_attempt_count": result.get("planned_attempt_count"), "execution_result_count": len(result.get("execution_results", [])), "mt5_kpi_records": len(result.get("mt5_kpi_records", [])), "selected_candidate": result.get("selected_candidate"), "adapter_package": result.get("adapter_package"), "onnx_readiness": result.get("onnx_readiness"), "goal_achieve": result.get("goal_achieve"), "next_action": result.get("next_action"), "report": base.rel(REPORT)}, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
