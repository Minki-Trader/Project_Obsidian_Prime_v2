from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

try:
    from foundation.pipelines.materialize_fpmarkets_v2_dataset import (
        DATASET_ID,
        EXPECTED_FEATURE_ORDER_HASH,
        PARSER_VERSION,
        build_feature_frame,
    )
    from foundation.pipelines import materialize_fpmarkets_v2_stage06_followup_pack as followup
    from foundation.pipelines import materialize_fpmarkets_v2_stage06_tier_b_reduced_context as reduced_context
except ModuleNotFoundError:
    dataset_module_path = Path(__file__).with_name("materialize_fpmarkets_v2_dataset.py")
    dataset_spec = importlib.util.spec_from_file_location(
        "materialize_fpmarkets_v2_dataset_for_stage07_dual_verdict",
        dataset_module_path,
    )
    if dataset_spec is None or dataset_spec.loader is None:
        raise RuntimeError(f"Could not load dataset materializer from {dataset_module_path}")
    dataset_module = importlib.util.module_from_spec(dataset_spec)
    sys.modules[dataset_spec.name] = dataset_module
    dataset_spec.loader.exec_module(dataset_module)
    DATASET_ID = dataset_module.DATASET_ID
    EXPECTED_FEATURE_ORDER_HASH = dataset_module.EXPECTED_FEATURE_ORDER_HASH
    PARSER_VERSION = dataset_module.PARSER_VERSION
    build_feature_frame = dataset_module.build_feature_frame

    followup_module_path = Path(__file__).with_name("materialize_fpmarkets_v2_stage06_followup_pack.py")
    followup_spec = importlib.util.spec_from_file_location(
        "materialize_fpmarkets_v2_stage06_followup_pack_for_stage07_dual_verdict",
        followup_module_path,
    )
    if followup_spec is None or followup_spec.loader is None:
        raise RuntimeError(f"Could not load follow-up pack materializer from {followup_module_path}")
    followup = importlib.util.module_from_spec(followup_spec)
    sys.modules[followup_spec.name] = followup
    followup_spec.loader.exec_module(followup)

    reduced_context_module_path = Path(__file__).with_name("materialize_fpmarkets_v2_stage06_tier_b_reduced_context.py")
    reduced_context_spec = importlib.util.spec_from_file_location(
        "materialize_fpmarkets_v2_stage06_tier_b_reduced_context_for_stage07_dual_verdict",
        reduced_context_module_path,
    )
    if reduced_context_spec is None or reduced_context_spec.loader is None:
        raise RuntimeError(f"Could not load reduced-context materializer from {reduced_context_module_path}")
    reduced_context = importlib.util.module_from_spec(reduced_context_spec)
    sys.modules[reduced_context_spec.name] = reduced_context
    reduced_context_spec.loader.exec_module(reduced_context)


STAGE_NAME = "07_alpha_search"
RUN_ID = "tier_b_dual_verdict_0001"
PACK_ID = "tier_b_dual_verdict_pack_fpmarkets_v2_0001"
BUNDLE_ID = "bundle_fpmarkets_v2_stage07_tier_b_dual_verdict_0001"
REPORT_ID = "report_fpmarkets_v2_tier_b_dual_verdict_0001"
DECISION_ID = "decision_fpmarkets_v2_tier_b_dual_verdict_0001"
LOCAL_SPEC_REF = "stages/07_alpha_search/01_inputs/stage07_tier_b_dual_verdict_local_spec.md@2026-04-23"
STAGE07_PACKET_DECISION_REF = "docs/decisions/2026-04-23_stage07_tier_b_dual_verdict_packet_adopted.md@2026-04-23"
UPSTREAM_STAGE06_DECISION_REF = "docs/decisions/2026-04-22_stage06_close_and_stage07_open.md@2026-04-22"
UPSTREAM_STAGE06_BASELINE_DECISION_REF = "docs/decisions/2026-04-22_stage06_v2_baseline_seed_first.md@2026-04-22"
UPSTREAM_CHARTER_REF = "docs/adr/0003_tier_b_reduced_risk_experiment_charter.md@2026-04-22"

MANIFEST_FILENAME = "tier_b_dual_verdict_manifest_fpmarkets_v2_0001.json"
EVALUATION_SUMMARY_FILENAME = "tier_b_dual_verdict_evaluation_summary_fpmarkets_v2_0001.json"
CONTROL_SUMMARY_FILENAME = "tier_b_dual_verdict_control_summary_fpmarkets_v2_0001.json"
VERDICT_SUMMARY_FILENAME = "tier_b_dual_verdict_summary_fpmarkets_v2_0001.json"
REPORT_FILENAME = "report_fpmarkets_v2_tier_b_dual_verdict_0001.md"
DECISION_FILENAME = "decision_fpmarkets_v2_tier_b_dual_verdict_0001.md"

DEFAULT_OUTPUT_ROOT = Path("stages/07_alpha_search/02_runs/tier_b_dual_verdict_0001")
DEFAULT_REVIEWS_ROOT = Path("stages/07_alpha_search/03_reviews")
DEFAULT_ROW_LABELS_PATH = reduced_context.DEFAULT_ROW_LABELS_PATH
DEFAULT_BASELINE_SUMMARY_PATH = reduced_context.DEFAULT_BASELINE_SUMMARY_PATH

VALIDATED_WEIGHTS_SOURCE_STATUS = "validated_user_csv"
CURRENT_KEEP42_SURFACE_NOTE = (
    "the current keep42 active surface stays weight-neutral because `top3_weighted_return_1` and "
    "`us100_minus_top3_weighted_return_1` remain outside the shared active set"
)
EXPECTED_WEIGHT_COLUMNS = (
    "month",
    "msft_xnas_weight",
    "nvda_xnas_weight",
    "aapl_xnas_weight",
)
EXPECTED_MONTHS = tuple(pd.period_range("2022-08", "2026-04", freq="M").astype(str))


class BlockedWeightsError(RuntimeError):
    def __init__(self, reason_code: str, message: str):
        super().__init__(message)
        self.reason_code = reason_code
        self.message = message

    def to_payload(self, *, weights_path: Path) -> dict[str, object]:
        return {
            "status": "blocked",
            "reason_code": self.reason_code,
            "weights_path": str(weights_path),
            "message": self.message,
        }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Materialize the first Stage 07 Tier B dual-verdict pack from a user-provided monthly-frozen weights CSV."
    )
    parser.add_argument(
        "--weights-path",
        required=True,
        help="Path to the user-provided monthly-frozen top3 weights CSV.",
    )
    parser.add_argument(
        "--weights-version-label",
        default=None,
        help="Optional stable label to record for the user-provided weights source.",
    )
    parser.add_argument(
        "--raw-root",
        default="data/raw/mt5_bars/m5",
        help="Repo-relative root containing raw M5 MT5 bar exports.",
    )
    parser.add_argument(
        "--row-labels-path",
        default=str(DEFAULT_ROW_LABELS_PATH),
        help="Repo-relative readiness row-label parquet produced by scorecard_0001.",
    )
    parser.add_argument(
        "--baseline-summary-path",
        default=str(DEFAULT_BASELINE_SUMMARY_PATH),
        help="Repo-relative Stage 06 baseline summary used as the comparison floor.",
    )
    parser.add_argument(
        "--output-root",
        default=str(DEFAULT_OUTPUT_ROOT),
        help="Repo-relative output root for the Stage 07 dual-verdict JSON artifacts.",
    )
    parser.add_argument(
        "--reviews-root",
        default=str(DEFAULT_REVIEWS_ROOT),
        help="Repo-relative output root for the rendered Stage 07 review markdown files.",
    )
    parser.add_argument(
        "--reviewed-on",
        default=pd.Timestamp.now(tz="Asia/Seoul").date().isoformat(),
        help="Review date to stamp into the rendered outputs.",
    )
    return parser.parse_args()


def _to_builtin(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _to_builtin(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_to_builtin(item) for item in value]
    if isinstance(value, tuple):
        return [_to_builtin(item) for item in value]
    if isinstance(value, (np.floating,)):
        return float(value)
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.bool_,)):
        return bool(value)
    return value


def default_weights_version_label(weights_path: Path, explicit_label: str | None) -> str:
    if explicit_label is not None:
        return explicit_label
    return f"{weights_path.as_posix()} (monthly_frozen_user_csv)"


def validate_user_weights_csv(path: Path) -> pd.DataFrame:
    try:
        weights = pd.read_csv(reduced_context._fs_path(path))
    except FileNotFoundError as exc:
        raise BlockedWeightsError("weights_path_missing", f"blocked: weights path is missing: {path}") from exc
    except Exception as exc:
        raise BlockedWeightsError("weights_csv_unreadable", f"blocked: could not read weights CSV: {path}") from exc

    if tuple(weights.columns) != EXPECTED_WEIGHT_COLUMNS:
        raise BlockedWeightsError(
            "weights_columns_invalid",
            "blocked: weights CSV must contain only `month`, `msft_xnas_weight`, `nvda_xnas_weight`, and `aapl_xnas_weight` in that order",
        )

    validated = weights.copy()
    validated["month"] = validated["month"].astype(str)
    if validated["month"].duplicated().any():
        duplicates = sorted(validated.loc[validated["month"].duplicated(), "month"].unique().tolist())
        raise BlockedWeightsError(
            "weights_month_duplicate",
            f"blocked: duplicate month rows were found in the weights CSV: {duplicates}",
        )

    month_set = set(validated["month"].tolist())
    expected_set = set(EXPECTED_MONTHS)
    missing_months = sorted(expected_set.difference(month_set))
    unexpected_months = sorted(month_set.difference(expected_set))
    if missing_months or unexpected_months:
        raise BlockedWeightsError(
            "weights_month_coverage_invalid",
            f"blocked: weights CSV month coverage must match 2022-08 through 2026-04 exactly; missing={missing_months}, unexpected={unexpected_months}",
        )

    numeric_columns = list(EXPECTED_WEIGHT_COLUMNS[1:])
    for column_name in numeric_columns:
        numeric = pd.to_numeric(validated[column_name], errors="coerce")
        if numeric.isna().any():
            bad_rows = validated.loc[numeric.isna(), "month"].tolist()
            raise BlockedWeightsError(
                "weights_non_numeric",
                f"blocked: non-numeric weight values were found in `{column_name}` for months {bad_rows}",
            )
        validated[column_name] = numeric.astype(float)

    bad_sum_mask = ~np.isclose(validated[numeric_columns].sum(axis=1), 1.0, atol=1e-9)
    if bad_sum_mask.any():
        bad_months = validated.loc[bad_sum_mask, "month"].tolist()
        raise BlockedWeightsError(
            "weights_sum_invalid",
            f"blocked: monthly weights must sum to 1.0 within tolerance for every month; failing months={bad_months}",
        )

    return validated.sort_values("month").reset_index(drop=True)


def load_json(path: Path) -> dict[str, object]:
    with open(reduced_context._fs_path(path), "r", encoding="utf-8") as handle:
        return json.load(handle)


def build_evaluation_summary(
    *,
    row_labels_path: Path,
    baseline_summary_path: Path,
    weights_version: str,
    weights_path: Path,
    weights_source_status: str,
    probability_table: pd.DataFrame,
    baseline_summary: dict[str, object],
) -> dict[str, object]:
    upstream_summary = reduced_context.build_evaluation_summary(
        probability_table,
        row_labels_path=row_labels_path.as_posix(),
        baseline_summary=baseline_summary,
    )
    stage06_baseline_holdout = baseline_summary["splits"]["holdout"]["tier_b_exploration"]["log_loss"]
    return {
        "dataset_id": DATASET_ID,
        "scorecard_id": reduced_context.SCORECARD_ID,
        "stage07_packet_id": PACK_ID,
        "bundle_id": BUNDLE_ID,
        "report_id": REPORT_ID,
        "model_family_id": reduced_context.MODEL_FAMILY_ID,
        "produced_by_stage": STAGE_NAME,
        "parser_version": PARSER_VERSION,
        "feature_order_hash": EXPECTED_FEATURE_ORDER_HASH,
        "row_labels_path": row_labels_path.as_posix(),
        "baseline_summary_path": baseline_summary_path.as_posix(),
        "weights_path": str(weights_path),
        "weights_version": weights_version,
        "weights_source_status": weights_source_status,
        "local_spec_ref": LOCAL_SPEC_REF,
        "decision_ref": STAGE07_PACKET_DECISION_REF,
        "upstream_stage06_decision_ref": UPSTREAM_STAGE06_DECISION_REF,
        "upstream_stage06_baseline_decision_ref": UPSTREAM_STAGE06_BASELINE_DECISION_REF,
        "upstream_charter_ref": UPSTREAM_CHARTER_REF,
        "fit_lane": reduced_context.FIT_LANE,
        "probability_output_order": reduced_context.PROBABILITY_COLUMNS,
        "active_surface": {
            "active_feature_count": len(reduced_context.ACTIVE_FEATURES),
            "conditional_feature_count": len(reduced_context.CONDITIONAL_FEATURES),
            "dropped_feature_count": len(reduced_context.DROPPED_FEATURES),
            "active_feature_names": reduced_context.ACTIVE_FEATURES,
            "conditional_feature_names": reduced_context.CONDITIONAL_FEATURES,
            "dropped_feature_names": reduced_context.DROPPED_FEATURES,
            "weights_surface_note": CURRENT_KEEP42_SURFACE_NOTE,
        },
        "stage06_full_baseline_reference": {
            "path": baseline_summary_path.as_posix(),
            "holdout_tier_b_log_loss": float(stage06_baseline_holdout),
        },
        "splits": _to_builtin(upstream_summary["splits"]),
        "comparison_to_stage06_full_baseline_seed": _to_builtin(upstream_summary["comparison_to_full_baseline_seed"]),
        "tier_b_subtype_info_only": _to_builtin(upstream_summary["tier_b_subtype_info_only"]),
    }


def build_control_summary(
    *,
    weights_version: str,
    weights_path: Path,
    weights_source_status: str,
    probability_table: pd.DataFrame,
) -> dict[str, object]:
    calibration_summary = followup.build_calibration_fit_summary(probability_table)
    upstream_control = followup.build_control_sensitivity_summary(probability_table, calibration_summary)
    return {
        "dataset_id": DATASET_ID,
        "scorecard_id": reduced_context.SCORECARD_ID,
        "stage07_packet_id": PACK_ID,
        "bundle_id": BUNDLE_ID,
        "report_id": REPORT_ID,
        "model_family_id": reduced_context.MODEL_FAMILY_ID,
        "produced_by_stage": STAGE_NAME,
        "parser_version": PARSER_VERSION,
        "feature_order_hash": EXPECTED_FEATURE_ORDER_HASH,
        "weights_path": str(weights_path),
        "weights_version": weights_version,
        "weights_source_status": weights_source_status,
        "local_spec_ref": LOCAL_SPEC_REF,
        "decision_ref": STAGE07_PACKET_DECISION_REF,
        "probability_source": upstream_control["probability_source"],
        "fitted_temperatures": {
            lane_name: calibration_summary["fit_candidates"][f"{lane_name}_temperature_fit"]["temperature"]
            for lane_name in reduced_context.REPORTING_LANE_ORDER
        },
        "entry_threshold_grid": list(followup.ENTRY_THRESHOLD_GRID),
        "exposure_cap_grid": list(followup.EXPOSURE_CAP_GRID),
        "risk_size_grid": list(followup.RISK_SIZE_GRID),
        "weights_surface_note": CURRENT_KEEP42_SURFACE_NOTE,
        "splits": _to_builtin(upstream_control["splits"]),
    }


def build_verdict_summary(
    *,
    weights_version: str,
    weights_source_status: str,
    evaluation_summary: dict[str, object],
    control_summary: dict[str, object],
) -> dict[str, object]:
    holdout_tier_b = evaluation_summary["splits"]["holdout"]["tier_b_exploration"]
    holdout_control = control_summary["splits"]["holdout"]["tier_b_exploration"]["draft_findings"]
    stage06_holdout_floor = evaluation_summary["stage06_full_baseline_reference"]["holdout_tier_b_log_loss"]
    positive_config_count = int(holdout_control["positive_config_count"])
    separate_lane_keep = holdout_tier_b["log_loss"] < stage06_holdout_floor and positive_config_count > 0
    separate_lane_verdict = "keep" if separate_lane_keep else "prune"
    mt5_candidate_verdict = "yes" if separate_lane_keep and weights_source_status == VALIDATED_WEIGHTS_SOURCE_STATUS else "no"
    verdict_reason = (
        "the validated user-weight rerun kept `Tier B holdout log_loss (Tier B 보류 평가 로그 손실)` below the "
        "Stage 06 full-baseline floor and still preserved at least one positive `proxy config (프록시 구성)` on the holdout slice"
        if separate_lane_keep
        else "the validated user-weight rerun did not keep the Stage 07 separate-lane boundary above both the Stage 06 full-baseline floor and the positive proxy-config threshold"
    )
    carry_forward_risk_note = (
        "the best positive holdout proxy slice is still sparse, and the current keep42 active surface is weight-neutral, so this verdict should be read as next-stage candidacy only rather than as live-path readiness"
    )
    return {
        "dataset_id": DATASET_ID,
        "scorecard_id": reduced_context.SCORECARD_ID,
        "stage07_packet_id": PACK_ID,
        "report_id": REPORT_ID,
        "decision_id": DECISION_ID,
        "produced_by_stage": STAGE_NAME,
        "weights_source_status": weights_source_status,
        "weights_version": weights_version,
        "separate_lane_verdict": separate_lane_verdict,
        "mt5_candidate_verdict": mt5_candidate_verdict,
        "verdict_reason": verdict_reason,
        "carry_forward_risk_note": carry_forward_risk_note,
        "decision_boundary": {
            "stage06_full_baseline_holdout_tier_b_log_loss": float(stage06_holdout_floor),
            "observed_holdout_tier_b_log_loss": float(holdout_tier_b["log_loss"]),
            "observed_holdout_tier_b_macro_f1": float(holdout_tier_b["macro_f1"]),
            "holdout_positive_proxy_config_count": positive_config_count,
            "holdout_best_proxy_config": _to_builtin(holdout_control["best_proxy_config"]),
        },
        "weights_surface_note": CURRENT_KEEP42_SURFACE_NOTE,
    }


def build_manifest(
    *,
    row_labels_path: Path,
    baseline_summary_path: Path,
    weights_path: Path,
    weights_version: str,
    reviewed_on: str,
    probability_table: pd.DataFrame,
    thresholds: dict[str, float],
    evaluation_summary: dict[str, object],
) -> dict[str, object]:
    train_rows = probability_table.loc[probability_table["row_used_for_fit"]].copy()
    return {
        "dataset_id": DATASET_ID,
        "scorecard_id": reduced_context.SCORECARD_ID,
        "stage07_packet_id": PACK_ID,
        "bundle_id": BUNDLE_ID,
        "report_id": REPORT_ID,
        "decision_id": DECISION_ID,
        "produced_by_stage": STAGE_NAME,
        "reviewed_on": reviewed_on,
        "parser_version": PARSER_VERSION,
        "feature_order_hash": EXPECTED_FEATURE_ORDER_HASH,
        "row_labels_path": row_labels_path.as_posix(),
        "baseline_summary_path": baseline_summary_path.as_posix(),
        "weights_path": str(weights_path),
        "weights_version": weights_version,
        "weights_csv_sha256": reduced_context.sha256_file(weights_path),
        "local_spec_ref": LOCAL_SPEC_REF,
        "decision_ref": STAGE07_PACKET_DECISION_REF,
        "upstream_stage06_decision_ref": UPSTREAM_STAGE06_DECISION_REF,
        "upstream_stage06_baseline_decision_ref": UPSTREAM_STAGE06_BASELINE_DECISION_REF,
        "upstream_charter_ref": UPSTREAM_CHARTER_REF,
        "fit_lane": reduced_context.FIT_LANE,
        "model_type": "gaussian_naive_bayes",
        "class_order": reduced_context.TARGET_LABEL_ORDER,
        "probability_output_order": reduced_context.PROBABILITY_COLUMNS,
        "train_window": {
            "start": reduced_context.TRAIN_START_UTC.isoformat(),
            "end_inclusive": reduced_context.TRAIN_END_UTC.isoformat(),
            "readiness_tier": "tier_a",
            "row_count": int(len(train_rows)),
        },
        "validation_window": {
            "start": reduced_context.VALIDATION_START_UTC.isoformat(),
            "end_inclusive": reduced_context.VALIDATION_END_UTC.isoformat(),
        },
        "holdout_window": {
            "start": reduced_context.HOLDOUT_START_UTC.isoformat(),
            "end_inclusive": reduced_context.HOLDOUT_END_UTC.isoformat(),
        },
        "label_rule": {
            "future_target": "future_log_return_1",
            "q33": thresholds["q33"],
            "q67": thresholds["q67"],
            "rule": "x <= q33 -> short; q33 < x < q67 -> flat; x >= q67 -> long",
        },
        "active_surface": evaluation_summary["active_surface"],
        "included_artifacts": {
            "evaluation_summary": EVALUATION_SUMMARY_FILENAME,
            "control_summary": CONTROL_SUMMARY_FILENAME,
            "verdict_summary": VERDICT_SUMMARY_FILENAME,
            "report": REPORT_FILENAME,
            "decision_memo": DECISION_FILENAME,
        },
    }


def _format_class_balance(class_balance: dict[str, int]) -> str:
    return ", ".join(f"{label}={class_balance[label]}" for label in reduced_context.TARGET_LABEL_ORDER)


def _metric_row(split_name: str, lane_name: str, metrics: dict[str, object]) -> str:
    return (
        f"| {split_name} | {lane_name} | {metrics['row_count']} | {_format_class_balance(metrics['class_balance'])} | "
        f"{metrics['log_loss']:.6f} | {metrics['macro_f1']:.6f} | {metrics['balanced_accuracy']:.6f} | "
        f"{metrics['multiclass_brier_score']:.6f} |"
    )


def render_report(
    *,
    manifest: dict[str, object],
    evaluation_summary: dict[str, object],
    control_summary: dict[str, object],
    verdict_summary: dict[str, object],
) -> str:
    holdout_control = control_summary["splits"]["holdout"]["tier_b_exploration"]["draft_findings"]
    lines = [
        "# Stage 07 Tier B Dual Verdict Report (Stage 07 Tier B 이중 판정 보고서)",
        "",
        "## Identity (식별 정보)",
        f"- reviewed_on: `{manifest['reviewed_on']}`",
        f"- stage: `{STAGE_NAME}`",
        f"- stage07_packet_id: `{PACK_ID}`",
        f"- report_id: `{REPORT_ID}`",
        f"- decision_id: `{DECISION_ID}`",
        f"- local_spec_ref: `{LOCAL_SPEC_REF}`",
        "",
        "## Boundary Read (경계 판독)",
        "- this packet answers only whether `Tier B (Tier B)` should stay open as a `separate lane (별도 레인)` and whether it may move forward as an `MT5 feasibility candidate (MT5 가능성 후보)`",
        "- `MT5 candidate (MT5 후보)` means next-stage handoff only and does not claim an opened `MT5 path (MT5 경로)`",
        "- the current strict `Tier A runtime rule (엄격 Tier A 런타임 규칙)` remains unchanged",
        "- no promoted operating-line meaning (승격 운영선 의미) is claimed here",
        "",
        "## Weights Source (가중치 소스)",
        f"- weights_path: `{manifest['weights_path']}`",
        f"- weights_version: `{manifest['weights_version']}`",
        f"- weights_source_status: `{evaluation_summary['weights_source_status']}`",
        f"- weights_surface_note: `{CURRENT_KEEP42_SURFACE_NOTE}`",
        "",
        "## KPI Summary (핵심 지표 요약)",
        "| split (분할) | lane (레인) | row_count (행 수) | class_balance (클래스 분포) | log_loss (로그 손실) | macro_f1 (매크로 F1) | balanced_accuracy (균형 정확도) | multiclass_brier_score (다중분류 브라이어 점수) |",
        "| --- | --- | ---: | --- | ---: | ---: | ---: | ---: |",
    ]

    for split_name in reduced_context.DATA_SPLIT_ORDER:
        split_payload = evaluation_summary["splits"].get(split_name, {})
        for lane_name in reduced_context.REPORTING_LANE_ORDER:
            metrics = split_payload.get(lane_name)
            if metrics is None:
                continue
            lines.append(_metric_row(split_name, lane_name, metrics))

    lines.extend(
        [
            "",
            "## Control Read (제어 판독)",
            f"- holdout_tier_b_positive_config_count: `{holdout_control['positive_config_count']}`",
            f"- holdout_tier_b_control_read: `{holdout_control['control_read']}`",
            f"- holdout_tier_b_best_proxy_config: `{json.dumps(_to_builtin(holdout_control['best_proxy_config']), sort_keys=True)}`",
            "",
            "## Dual Verdict (이중 판정)",
            f"- separate_lane_verdict: `{verdict_summary['separate_lane_verdict']}`",
            f"- mt5_candidate_verdict: `{verdict_summary['mt5_candidate_verdict']}`",
            f"- verdict_reason: `{verdict_summary['verdict_reason']}`",
            f"- carry_forward_risk_note: `{verdict_summary['carry_forward_risk_note']}`",
            "",
            "## Notes (메모)",
            "- this packet keeps `Tier A (Tier A)` and `Tier B (Tier B)` on separate `reporting lanes (보고 레인)`",
            "- the user-weight rerun clears the weight-source evidence boundary for this packet, but the keep42 active surface still remains weight-neutral on its direct inputs",
            "- any later `MT5 feasibility (MT5 가능성)` step still needs its own bounded packet",
        ]
    )
    return "\n".join(lines) + "\n"


def render_decision_memo(
    *,
    manifest: dict[str, object],
    verdict_summary: dict[str, object],
) -> str:
    lines = [
        "# Decision Memo",
        "",
        "## Decision Summary",
        "",
        f"- `decision_id`: `{DECISION_ID}`",
        f"- `reviewed_on`: `{manifest['reviewed_on']}`",
        "- `owner`: `codex + user`",
        "- `decision`: use the Stage 07 `Tier B dual verdict packet (Tier B 이중 판정 팩)` on a validated user-weight rerun to decide both `separate lane (별도 레인)` survival and `MT5 feasibility candidate (MT5 가능성 후보)` handoff without changing the current strict Tier A runtime rule (엄격 Tier A 런타임 규칙)",
        "",
        "## What Was Decided",
        "",
        "- adopted:",
        f"  - `separate_lane_verdict`: `{verdict_summary['separate_lane_verdict']}`",
        f"  - `mt5_candidate_verdict`: `{verdict_summary['mt5_candidate_verdict']}`",
        f"  - keep the current keep42 active surface explicit as weight-neutral on direct inputs while still requiring a validated user-weight source for this packet's evidence boundary",
        "- not adopted:",
        "  - any opened `MT5 path (MT5 경로)` work in this same packet",
        "  - any changed `Tier A runtime rule (Tier A 런타임 규칙)`",
        "  - any promoted operating-line claim (승격 운영선 주장)",
        "",
        "## Why",
        "",
        f"- `verdict_reason`: `{verdict_summary['verdict_reason']}`",
        f"- `carry_forward_risk_note`: `{verdict_summary['carry_forward_risk_note']}`",
        "",
        "## Operational Meaning",
        "",
        "- `active_stage changed?`: `no`",
        "- `current strict Tier A runtime rule changed?`: `no`",
        f"- `separate Tier B lane kept?`: `{verdict_summary['separate_lane_verdict'] == 'keep'}`",
        f"- `next-stage MT5 feasibility candidate opened?`: `{verdict_summary['mt5_candidate_verdict'] == 'yes'}`",
        "- `workspace_state result-level update needed?`: `yes, but only in the same pass that reflects this packet's closed verdict as current truth`",
        "- `artifact_registry.csv update needed?`: `yes, but only in the same pass that writes the durable Stage 07 run artifacts into the repo-tracked output root`",
    ]
    return "\n".join(lines) + "\n"


def write_outputs(
    *,
    output_root: Path,
    reviews_root: Path,
    row_labels_path: Path,
    baseline_summary_path: Path,
    weights_path: Path,
    weights_version: str,
    reviewed_on: str,
    probability_table: pd.DataFrame,
    thresholds: dict[str, float],
    evaluation_summary: dict[str, object],
    control_summary: dict[str, object],
    verdict_summary: dict[str, object],
) -> dict[str, object]:
    output_root.mkdir(parents=True, exist_ok=True)
    reviews_root.mkdir(parents=True, exist_ok=True)

    manifest_path = output_root / MANIFEST_FILENAME
    evaluation_path = output_root / EVALUATION_SUMMARY_FILENAME
    control_path = output_root / CONTROL_SUMMARY_FILENAME
    verdict_path = output_root / VERDICT_SUMMARY_FILENAME
    report_path = reviews_root / REPORT_FILENAME
    decision_path = reviews_root / DECISION_FILENAME

    manifest = build_manifest(
        row_labels_path=row_labels_path,
        baseline_summary_path=baseline_summary_path,
        weights_path=weights_path,
        weights_version=weights_version,
        reviewed_on=reviewed_on,
        probability_table=probability_table,
        thresholds=thresholds,
        evaluation_summary=evaluation_summary,
    )
    report_text = render_report(
        manifest=manifest,
        evaluation_summary=evaluation_summary,
        control_summary=control_summary,
        verdict_summary=verdict_summary,
    )
    decision_text = render_decision_memo(
        manifest=manifest,
        verdict_summary=verdict_summary,
    )

    reduced_context._write_text(manifest_path, json.dumps(_to_builtin(manifest), indent=2))
    reduced_context._write_text(evaluation_path, json.dumps(_to_builtin(evaluation_summary), indent=2))
    reduced_context._write_text(control_path, json.dumps(_to_builtin(control_summary), indent=2))
    reduced_context._write_text(verdict_path, json.dumps(_to_builtin(verdict_summary), indent=2))
    reduced_context._write_text(report_path, report_text, bom=True)
    reduced_context._write_text(decision_path, decision_text, bom=True)

    return {
        "manifest_path": manifest_path.as_posix(),
        "evaluation_path": evaluation_path.as_posix(),
        "control_path": control_path.as_posix(),
        "verdict_path": verdict_path.as_posix(),
        "report_path": report_path.as_posix(),
        "decision_path": decision_path.as_posix(),
        "manifest_sha256": reduced_context.sha256_file(manifest_path),
        "evaluation_sha256": reduced_context.sha256_file(evaluation_path),
        "control_sha256": reduced_context.sha256_file(control_path),
        "verdict_sha256": reduced_context.sha256_file(verdict_path),
        "report_sha256": reduced_context.sha256_file(report_path),
        "decision_sha256": reduced_context.sha256_file(decision_path),
        "manifest": manifest,
    }


def materialize_dual_verdict(
    *,
    raw_root: Path,
    weights_path: Path,
    weights_version_label: str | None,
    row_labels_path: Path,
    baseline_summary_path: Path,
    output_root: Path,
    reviews_root: Path,
    reviewed_on: str,
) -> dict[str, object]:
    validate_user_weights_csv(weights_path)
    weights_version = default_weights_version_label(weights_path, weights_version_label)
    baseline_summary = load_json(baseline_summary_path)

    frame, _ = build_feature_frame(
        raw_root,
        weights_path=weights_path,
        weights_version_label=weights_version,
    )
    row_labels = reduced_context.load_row_labels(row_labels_path)
    model_frame = reduced_context.build_model_frame(frame, row_labels)
    probability_table, thresholds = reduced_context.build_probability_table(model_frame)
    evaluation_summary = build_evaluation_summary(
        row_labels_path=row_labels_path,
        baseline_summary_path=baseline_summary_path,
        weights_version=weights_version,
        weights_path=weights_path,
        weights_source_status=VALIDATED_WEIGHTS_SOURCE_STATUS,
        probability_table=probability_table,
        baseline_summary=baseline_summary,
    )
    control_summary = build_control_summary(
        weights_version=weights_version,
        weights_path=weights_path,
        weights_source_status=VALIDATED_WEIGHTS_SOURCE_STATUS,
        probability_table=probability_table,
    )
    verdict_summary = build_verdict_summary(
        weights_version=weights_version,
        weights_source_status=VALIDATED_WEIGHTS_SOURCE_STATUS,
        evaluation_summary=evaluation_summary,
        control_summary=control_summary,
    )
    output_paths = write_outputs(
        output_root=output_root,
        reviews_root=reviews_root,
        row_labels_path=row_labels_path,
        baseline_summary_path=baseline_summary_path,
        weights_path=weights_path,
        weights_version=weights_version,
        reviewed_on=reviewed_on,
        probability_table=probability_table,
        thresholds=thresholds,
        evaluation_summary=evaluation_summary,
        control_summary=control_summary,
        verdict_summary=verdict_summary,
    )
    return {
        "weights_version": weights_version,
        "thresholds": thresholds,
        "evaluation_summary": evaluation_summary,
        "control_summary": control_summary,
        "verdict_summary": verdict_summary,
        **output_paths,
    }


def main() -> int:
    args = parse_args()
    weights_path = Path(args.weights_path)
    try:
        outputs = materialize_dual_verdict(
            raw_root=Path(args.raw_root),
            weights_path=weights_path,
            weights_version_label=args.weights_version_label,
            row_labels_path=Path(args.row_labels_path),
            baseline_summary_path=Path(args.baseline_summary_path),
            output_root=Path(args.output_root),
            reviews_root=Path(args.reviews_root),
            reviewed_on=args.reviewed_on,
        )
    except BlockedWeightsError as exc:
        print(json.dumps(exc.to_payload(weights_path=weights_path), indent=2))
        return 2

    holdout_tier_b = outputs["evaluation_summary"]["splits"]["holdout"]["tier_b_exploration"]
    payload = {
        "status": "ok",
        "dataset_id": DATASET_ID,
        "stage07_packet_id": PACK_ID,
        "report_id": REPORT_ID,
        "decision_id": DECISION_ID,
        "weights_version": outputs["weights_version"],
        "separate_lane_verdict": outputs["verdict_summary"]["separate_lane_verdict"],
        "mt5_candidate_verdict": outputs["verdict_summary"]["mt5_candidate_verdict"],
        "holdout_tier_b_log_loss": holdout_tier_b["log_loss"],
        "holdout_positive_proxy_config_count": outputs["verdict_summary"]["decision_boundary"]["holdout_positive_proxy_config_count"],
        "paths": {
            "manifest_path": outputs["manifest_path"],
            "evaluation_path": outputs["evaluation_path"],
            "control_path": outputs["control_path"],
            "verdict_path": outputs["verdict_path"],
            "report_path": outputs["report_path"],
            "decision_path": outputs["decision_path"],
        },
        "hashes": {
            "manifest_sha256": outputs["manifest_sha256"],
            "evaluation_sha256": outputs["evaluation_sha256"],
            "control_sha256": outputs["control_sha256"],
            "verdict_sha256": outputs["verdict_sha256"],
            "report_sha256": outputs["report_sha256"],
            "decision_sha256": outputs["decision_sha256"],
        },
    }
    print(json.dumps(_to_builtin(payload), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
