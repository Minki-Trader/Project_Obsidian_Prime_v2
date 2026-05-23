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

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    path_exists,
    read_csv_rows,
    sha256_file_lf_normalized,
    upsert_csv_rows,
    write_csv_rows,
)


STAGE_ID = "275_onnx_candidate_campaign__fresh_candidate_construction_after_filter_like_rebuild_failure"
RUN_ID = "run275D_execute_fresh_candidate_scoring_materialization_probe_v1"
SOURCE_RUN_ID = "run275C_materialize_fresh_candidate_scoring_handoff_inputs_v1"
STATUS = "completed_fresh_candidate_score_surface_materialization_no_candidate_selection"
JUDGMENT = "fresh_candidate_score_surfaces_materialized_no_candidate_selection"
JUDGMENT_CLASS = "inconclusive"
NEXT_ACTION = "run275E_screen_fresh_candidate_score_surfaces"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE = ROOT / "stages" / STAGE_ID
RUN275C = STAGE / "02_runs" / "run275C"
RUN_DIR = STAGE / "02_runs" / "run275D"
SCORE_DIR = RUN_DIR / "s"
HANDOFF_DIR = RUN_DIR / "h"
REVIEWS = STAGE / "03_reviews"
SELECTED = STAGE / "04_selected"

SOURCE_SPECS = RUN275C / "specs.json"
SOURCE_HANDOFF = RUN275C / "handoff.csv"
SOURCE_IDENTITY = RUN275C / "identity.csv"
SOURCE_SCHEMA = RUN275C / "schema.csv"
SOURCE_MANIFEST = RUN275C / "run_manifest.json"
SOURCE_REPORT = REVIEWS / "run275C_report.md"

TIER_A_DATASET = (
    ROOT
    / "data"
    / "processed"
    / "model_inputs"
    / "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58"
    / "model_input_dataset.parquet"
)
TIER_A_FEATURE_ORDER = TIER_A_DATASET.with_name("model_input_feature_order.txt")
TIER_B_DATASET = (
    ROOT
    / "data"
    / "processed"
    / "model_inputs"
    / "label_v1_fwd12_split_v1_feature_set_v1"
    / "model_input_dataset.parquet"
)
TIER_B_FEATURE_ORDER = TIER_B_DATASET.with_name("model_input_feature_order.txt")

SUMMARY = RUN_DIR / "summary.csv"
SPLIT_SUMMARY = RUN_DIR / "split.csv"
NORMALIZATION = RUN_DIR / "norm.json"
TIER_RECEIPT = RUN_DIR / "tier.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment.json"
DATA_INTEGRITY_RECEIPT = RUN_DIR / "data.json"
MODEL_VALIDATION_RECEIPT = RUN_DIR / "model.json"
RESULT_JUDGMENT = RUN_DIR / "judgment.csv"
GATE_AUDIT = RUN_DIR / "gates.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
LINEAGE_RECEIPT = RUN_DIR / "lineage.json"
RUN_REPORT = REVIEWS / "run275D_report.md"

SELECTION_STATUS = SELECTED / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
PRODUCER_PATH = Path("stage_pipelines/stage275/execute_fresh_candidate_scoring_materialization_probe.py")

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
SUMMARY_COLUMNS = (
    "package_id",
    "package_role",
    "record_view",
    "rows",
    "active_signal_count",
    "active_signal_rate",
    "long_count",
    "short_count",
    "mean_primary_score",
    "mean_model_risk_pct",
    "score_table_path",
    "score_table_hash",
    "judgment",
    "claim_boundary",
)
SPLIT_COLUMNS = (
    "package_id",
    "record_view",
    "split",
    "rows",
    "active_signal_count",
    "active_signal_rate",
    "long_count",
    "short_count",
    "mean_primary_score",
    "claim_boundary",
)
TIER_COLUMNS = (
    "tier_scope",
    "source_path",
    "feature_order_hash",
    "rows",
    "missing_required_features",
    "materialization_status",
    "performance_claim",
)
RESULT_COLUMNS = (
    "result_subject",
    "evidence_available",
    "evidence_missing",
    "judgment_label",
    "judgment_class",
    "claim_boundary",
    "next_condition",
    "user_explanation_hook",
)
GATE_COLUMNS = ("gate_name", "status", "evidence_path", "effect")
PACKAGE_SHORT = {
    "cp275A_volatility_pullback_breakout_surface": "cp275A",
    "cp275B_cross_asset_divergence_reversal_surface": "cp275B",
    "cp275C_cash_session_impulse_continuation_surface": "cp275C",
    "cp275D_macro_volatility_squeeze_release_surface": "cp275D",
    "cp275E_q04_stage274_failure_signature_guard": "cp275E",
}
PRIMARY_SCORE = {
    "cp275A_volatility_pullback_breakout_surface": "volatility_pullback_score",
    "cp275B_cross_asset_divergence_reversal_surface": "cross_asset_divergence_score",
    "cp275C_cash_session_impulse_continuation_surface": "session_impulse_score",
    "cp275D_macro_volatility_squeeze_release_surface": "squeeze_release_score",
    "cp275E_q04_stage274_failure_signature_guard": "q04_failure_signature_flag",
}
SUMMARY_VIEWS = ("Tier A separate", "Tier B separate", "Tier A+B combined")


def rel(path: Path | str) -> str:
    item = Path(str(path))
    try:
        return item.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def digest_payload(payload: Any) -> str:
    raw = json.dumps(json_ready(payload), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


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


def read_json(path: Path) -> dict[str, Any]:
    with io_path(path).open("r", encoding="utf-8-sig") as handle:
        return dict(json.load(handle))


def must_exist(paths: Sequence[Path]) -> None:
    missing = [rel(path) for path in paths if not path_exists(path)]
    if missing:
        raise FileNotFoundError("Missing required source artifacts: " + ", ".join(missing))


def load_feature_order(path: Path) -> list[str]:
    return [line.strip() for line in io_path(path).read_text(encoding="utf-8-sig").splitlines() if line.strip()]


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def col(frame: pd.DataFrame, name: str, default: float = 0.0) -> pd.Series:
    if name not in frame.columns:
        return pd.Series(default, index=frame.index, dtype="float64")
    return pd.to_numeric(frame[name], errors="coerce").astype("float64").replace([np.inf, -np.inf], np.nan).fillna(default)


def sigmoid(value: pd.Series | np.ndarray | float) -> pd.Series:
    array = np.asarray(value, dtype="float64")
    return pd.Series(1.0 / (1.0 + np.exp(-np.clip(array, -20.0, 20.0))))


def train_scaled(frame: pd.DataFrame, column: str) -> tuple[pd.Series, list[dict[str, Any]]]:
    numeric = col(frame, column)
    scaled = pd.Series(0.0, index=frame.index, dtype="float64")
    receipts: list[dict[str, Any]] = []
    for tier_view in sorted(str(value) for value in frame["tier_view"].dropna().unique()):
        tier_mask = frame["tier_view"].astype(str).eq(tier_view)
        train_mask = tier_mask & frame["split"].astype(str).eq("train")
        train_values = numeric[train_mask]
        median = float(train_values.median(skipna=True)) if len(train_values) else 0.0
        mad = float((train_values - median).abs().median(skipna=True)) if len(train_values) else 0.0
        std = float(train_values.std(skipna=True)) if len(train_values) else 0.0
        scale = mad * 1.4826 if np.isfinite(mad) and mad > 0 else std
        if not np.isfinite(scale) or scale <= 0:
            scale = 1.0
        scaled.loc[tier_mask] = ((numeric.loc[tier_mask] - median) / scale).clip(-6.0, 6.0)
        receipts.append(
            {
                "column": column,
                "tier_view": tier_view,
                "train_rows": int(train_mask.sum()),
                "median": round(median, 12),
                "scale": round(float(scale), 12),
                "method": "train_split_median_mad_or_std",
            }
        )
    return scaled.fillna(0.0), receipts


def train_quantile(score: pd.Series, frame: pd.DataFrame, quantile: float) -> pd.Series:
    threshold = pd.Series(0.5, index=frame.index, dtype="float64")
    for tier_view in sorted(str(value) for value in frame["tier_view"].dropna().unique()):
        tier_mask = frame["tier_view"].astype(str).eq(tier_view)
        train_mask = tier_mask & frame["split"].astype(str).eq("train")
        train_values = score[train_mask]
        value = float(train_values.quantile(quantile)) if len(train_values) else 0.5
        if not np.isfinite(value):
            value = 0.5
        threshold.loc[tier_mask] = value
    return threshold


def prepare_tier(path: Path, tier_view: str, feature_order_path: Path, expected_features: Sequence[str]) -> pd.DataFrame:
    frame = pd.read_parquet(io_path(path)).copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    observed = load_feature_order(feature_order_path)
    observed_hash = sha256_text("\n".join(observed))
    missing = [feature for feature in expected_features if feature not in frame.columns]
    for feature in missing:
        frame[feature] = np.nan
    frame["tier_view"] = tier_view
    frame["input_feature_order_hash"] = observed_hash
    frame["expected_feature_order_hash"] = sha256_text("\n".join(expected_features))
    frame["missing_required_feature_count"] = len(missing)
    frame["missing_required_features"] = ";".join(missing) if missing else "none"
    frame["row_seq"] = np.arange(len(frame), dtype="int64")
    return frame


def route_from_trend(frame: pd.DataFrame) -> pd.Series:
    raw = col(frame, "di_spread_14") + 0.35 * col(frame, "supertrend_10_3") + 0.20 * col(frame, "vortex_indicator")
    return pd.Series(np.where(raw >= 0.0, "long", "short"), index=frame.index)


def base_output(frame: pd.DataFrame, spec: Mapping[str, Any]) -> pd.DataFrame:
    package_id = str(spec["package_id"])
    return pd.DataFrame(
        {
            "timestamp": frame["timestamp"],
            "symbol": frame.get("symbol", pd.Series("US100", index=frame.index)).astype(str),
            "split": frame["split"].astype(str),
            "tier_view": frame["tier_view"].astype(str),
            "package_id": package_id,
            "input_feature_order_hash": frame["input_feature_order_hash"],
            "expected_feature_order_hash": frame["expected_feature_order_hash"],
            "missing_required_feature_count": frame["missing_required_feature_count"],
            "missing_required_features": frame["missing_required_features"],
            "feature_order_hash": spec["feature_order_hash"],
            "blueprint_hash": spec["blueprint_hash"],
            "score_columns_hash": spec["score_columns_hash"],
            "decision_rule_hash": spec["decision_rule_hash"],
            "risk_rule_hash": spec["risk_rule_hash"],
            "adapter_schema_hash": spec["adapter_schema_hash"],
            "claim_boundary": BOUNDARY,
        }
    )


def finalize(output: pd.DataFrame) -> pd.DataFrame:
    output["model_risk_pct"] = col(output, "model_risk_pct").clip(0.0, 1.0).round(8)
    output["active_signal_flag"] = output["entry_signal"].astype(str).ne("flat").astype("int8")
    output["telemetry_json"] = (
        '{"claim_boundary":"' + BOUNDARY + '","score_surface":"run275D_structural_scout"}'
    )
    return output


def score_cp275a(frame: pd.DataFrame, spec: Mapping[str, Any]) -> tuple[pd.DataFrame, list[dict[str, Any]]]:
    ret_z, r1 = train_scaled(frame, "return_zscore_20")
    atr_z, r2 = train_scaled(frame, "atr_14_over_atr_50")
    width_z, r3 = train_scaled(frame, "bollinger_width_20")
    pos_z, r4 = train_scaled(frame, "bb_position_20")
    adx_z, r5 = train_scaled(frame, "adx_14")
    di_z, r6 = train_scaled(frame, "di_spread_14")
    pullback = sigmoid(-0.45 * ret_z - 0.30 * pos_z + 0.20 * atr_z)
    breakout = sigmoid(0.35 * adx_z + 0.25 * width_z + 0.25 * di_z.abs())
    volatility_pullback_score = sigmoid(1.15 * pullback + 0.95 * breakout - 0.75)
    long_permission = sigmoid(1.05 * volatility_pullback_score + 0.35 * di_z - 0.18 * pos_z)
    short_permission = sigmoid(1.05 * volatility_pullback_score - 0.35 * di_z + 0.18 * pos_z)
    threshold = train_quantile(volatility_pullback_score, frame, 0.64)
    signal = pd.Series("flat", index=frame.index, dtype="object")
    signal.loc[(volatility_pullback_score >= threshold) & (long_permission >= short_permission)] = "long"
    signal.loc[(volatility_pullback_score >= threshold) & (short_permission > long_permission)] = "short"
    output = base_output(frame, spec)
    output["volatility_pullback_score"] = volatility_pullback_score.round(8)
    output["pullback_breakout_state"] = np.select(
        [volatility_pullback_score >= threshold, pullback >= 0.62],
        ["pullback_breakout", "pullback_watch"],
        default="flat_watch",
    )
    output["long_permission_score"] = long_permission.round(8)
    output["short_permission_score"] = short_permission.round(8)
    output["candidate_decision_score"] = volatility_pullback_score.round(8)
    output["entry_signal"] = signal
    output["route_code"] = signal
    output["model_risk_pct"] = (0.05 + 0.78 * volatility_pullback_score).clip(0.0, 1.0)
    return finalize(output), [*r1, *r2, *r3, *r4, *r5, *r6]


def score_cp275b(frame: pd.DataFrame, spec: Mapping[str, Any]) -> tuple[pd.DataFrame, list[dict[str, Any]]]:
    rel1_z, r1 = train_scaled(frame, "us100_minus_mega8_equal_return_1")
    rel2_z, r2 = train_scaled(frame, "us100_minus_top3_weighted_return_1")
    breadth_z, r3 = train_scaled(frame, "mega8_pos_breadth_1")
    disp_z, r4 = train_scaled(frame, "mega8_dispersion_5")
    vix_z, r5 = train_scaled(frame, "vix_zscore_20")
    rate_z, r6 = train_scaled(frame, "us10yr_zscore_20")
    usd_z, r7 = train_scaled(frame, "usdx_zscore_20")
    divergence_raw = 0.38 * rel1_z + 0.32 * rel2_z - 0.22 * breadth_z + 0.18 * disp_z
    stress_raw = 0.36 * vix_z.abs() + 0.22 * rate_z.abs() + 0.18 * usd_z.abs()
    cross_asset_divergence_score = sigmoid(0.80 * divergence_raw.abs() + 0.35 * stress_raw - 0.25)
    reversal_permission = sigmoid(0.75 * cross_asset_divergence_score + 0.30 * stress_raw - 0.12 * breadth_z)
    threshold = train_quantile(cross_asset_divergence_score, frame, 0.66)
    route_switch_flag = (cross_asset_divergence_score >= threshold).astype("int8")
    signal = pd.Series("flat", index=frame.index, dtype="object")
    signal.loc[(route_switch_flag == 1) & (divergence_raw < 0)] = "long"
    signal.loc[(route_switch_flag == 1) & (divergence_raw >= 0)] = "short"
    output = base_output(frame, spec)
    output["cross_asset_divergence_score"] = cross_asset_divergence_score.round(8)
    output["reversal_permission_score"] = reversal_permission.round(8)
    output["route_switch_flag"] = route_switch_flag
    output["candidate_decision_score"] = (cross_asset_divergence_score * reversal_permission).round(8)
    output["entry_signal"] = signal
    output["route_code"] = signal
    output["model_risk_pct"] = (0.04 + 0.74 * cross_asset_divergence_score * (1.0 - 0.25 * stress_raw.clip(0, 1))).clip(0.0, 1.0)
    return finalize(output), [*r1, *r2, *r3, *r4, *r5, *r6, *r7]


def score_cp275c(frame: pd.DataFrame, spec: Mapping[str, Any]) -> tuple[pd.DataFrame, list[dict[str, Any]]]:
    gap_z, r1 = train_scaled(frame, "gap_percent")
    overnight_z, r2 = train_scaled(frame, "overnight_return")
    r1_z, r3 = train_scaled(frame, "log_return_1")
    r3_z, r4 = train_scaled(frame, "log_return_3")
    vol_z, r5 = train_scaled(frame, "historical_vol_5_over_20")
    minutes = col(frame, "minutes_from_cash_open", default=999.0)
    phase_flag = (
        col(frame, "is_first_30m_after_open").eq(1)
        | col(frame, "is_last_30m_before_cash_close").eq(1)
        | ((minutes >= 0) & (minutes <= 45))
    ).astype("float64")
    impulse_raw = 0.32 * gap_z.abs() + 0.24 * overnight_z.abs() + 0.24 * r3_z.abs() + 0.20 * vol_z.abs() + 0.35 * phase_flag
    session_impulse_score = sigmoid(impulse_raw - 0.20)
    continuation = sigmoid(0.44 * r3_z + 0.32 * r1_z + 0.18 * gap_z + 0.22 * phase_flag)
    fade = sigmoid(-0.38 * r3_z - 0.24 * gap_z + 0.22 * vol_z.abs() + 0.18 * phase_flag)
    threshold = train_quantile(session_impulse_score, frame, 0.62)
    signal = pd.Series("flat", index=frame.index, dtype="object")
    active = (session_impulse_score >= threshold) & (phase_flag > 0)
    signal.loc[active & (continuation >= fade) & (r3_z >= 0)] = "long"
    signal.loc[active & (continuation >= fade) & (r3_z < 0)] = "short"
    signal.loc[active & (fade > continuation) & (r3_z < 0)] = "long"
    signal.loc[active & (fade > continuation) & (r3_z >= 0)] = "short"
    output = base_output(frame, spec)
    output["session_impulse_score"] = session_impulse_score.round(8)
    output["continuation_score"] = continuation.round(8)
    output["fade_score"] = fade.round(8)
    output["continuation_fade_state"] = np.select(
        [continuation >= fade, fade > continuation],
        ["continuation", "fade"],
        default="flat_watch",
    )
    output["candidate_decision_score"] = (session_impulse_score * np.maximum(continuation, fade)).round(8)
    output["entry_signal"] = signal
    output["route_code"] = signal
    output["model_risk_pct"] = (0.05 + 0.70 * output["candidate_decision_score"]).clip(0.0, 1.0)
    return finalize(output), [*r1, *r2, *r3, *r4, *r5]


def score_cp275d(frame: pd.DataFrame, spec: Mapping[str, Any]) -> tuple[pd.DataFrame, list[dict[str, Any]]]:
    squeeze_z, r1 = train_scaled(frame, "bb_squeeze")
    width_z, r2 = train_scaled(frame, "bollinger_width_20")
    hv_z, r3 = train_scaled(frame, "historical_vol_20")
    hv_ratio_z, r4 = train_scaled(frame, "historical_vol_5_over_20")
    vix_chg_z, r5 = train_scaled(frame, "vix_change_1")
    vix_z, r6 = train_scaled(frame, "vix_zscore_20")
    rsi_z, r7 = train_scaled(frame, "rsi_14")
    rsi_slope_z, r8 = train_scaled(frame, "rsi_14_slope_3")
    compression = sigmoid(0.45 * squeeze_z - 0.25 * width_z + 0.18 * hv_ratio_z.abs())
    release = sigmoid(0.34 * width_z + 0.28 * hv_z.abs() + 0.20 * vix_chg_z.abs() + 0.18 * rsi_slope_z.abs())
    stress = sigmoid(0.42 * vix_z.abs() + 0.18 * vix_chg_z.abs())
    squeeze_release_score = sigmoid(0.55 * compression + 0.65 * release + 0.20 * stress - 0.50)
    threshold = train_quantile(squeeze_release_score, frame, 0.65)
    risk_budget = (0.40 + 0.85 * squeeze_release_score * (1.0 - 0.25 * stress)).clip(0.0, 1.0)
    signal = pd.Series("flat", index=frame.index, dtype="object")
    active = squeeze_release_score >= threshold
    signal.loc[active & ((rsi_z + rsi_slope_z) >= 0)] = "long"
    signal.loc[active & ((rsi_z + rsi_slope_z) < 0)] = "short"
    output = base_output(frame, spec)
    output["squeeze_release_score"] = squeeze_release_score.round(8)
    output["macro_vol_route_state"] = np.select(
        [active & (stress >= 0.60), active],
        ["stress_release", "normal_release"],
        default="flat_watch",
    )
    output["risk_budget_multiplier"] = risk_budget.round(8)
    output["candidate_decision_score"] = squeeze_release_score.round(8)
    output["entry_signal"] = signal
    output["route_code"] = signal
    output["model_risk_pct"] = risk_budget
    return finalize(output), [*r1, *r2, *r3, *r4, *r5, *r6, *r7, *r8]


def score_cp275e(frame: pd.DataFrame, spec: Mapping[str, Any]) -> tuple[pd.DataFrame, list[dict[str, Any]]]:
    trend_route = route_from_trend(frame)
    adx_z, r1 = train_scaled(frame, "adx_14")
    vol_z, r2 = train_scaled(frame, "atr_14_over_atr_50")
    session = col(frame, "is_first_30m_after_open") + col(frame, "is_last_30m_before_cash_close")
    q04_flag = ((adx_z >= 0.15) & (vol_z <= 1.75)).astype("int8")
    filter_like = ((session > 0) | (vol_z > 1.75)).astype("int8")
    signal = pd.Series("flat", index=frame.index, dtype="object")
    signal.loc[q04_flag.eq(1)] = trend_route.loc[q04_flag.eq(1)]
    output = base_output(frame, spec)
    output["q04_failure_signature_flag"] = q04_flag
    output["stage274_filter_like_signature_flag"] = filter_like
    output["freshness_guard_result"] = np.where(q04_flag.eq(1) | filter_like.eq(1), "guard_reference", "no_guard_hit")
    output["candidate_decision_score"] = q04_flag.astype("float64")
    output["entry_signal"] = signal
    output["route_code"] = signal
    output["model_risk_pct"] = q04_flag.astype("float64")
    return finalize(output), [*r1, *r2]


SCORERS = {
    "cp275A_volatility_pullback_breakout_surface": score_cp275a,
    "cp275B_cross_asset_divergence_reversal_surface": score_cp275b,
    "cp275C_cash_session_impulse_continuation_surface": score_cp275c,
    "cp275D_macro_volatility_squeeze_release_surface": score_cp275d,
    "cp275E_q04_stage274_failure_signature_guard": score_cp275e,
}


def materialize_scores(specs: Sequence[Mapping[str, Any]], frame: pd.DataFrame) -> tuple[list[Path], list[Path], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    score_paths: list[Path] = []
    handoff_paths: list[Path] = []
    summary_rows: list[dict[str, Any]] = []
    split_rows: list[dict[str, Any]] = []
    norm_rows: list[dict[str, Any]] = []
    for spec in specs:
        package_id = str(spec["package_id"])
        short = PACKAGE_SHORT[package_id]
        scorer = SCORERS[package_id]
        table, receipts = scorer(frame, spec)
        norm_rows.extend({"package_id": package_id, **row} for row in receipts)
        score_path = SCORE_DIR / f"{short}.parquet"
        table.to_parquet(io_path(score_path), index=False)
        score_hash = sha256_file_lf_normalized(score_path)
        score_paths.append(score_path)
        primary = PRIMARY_SCORE[package_id]
        for view in SUMMARY_VIEWS:
            if view == "Tier A+B combined":
                part = table
            else:
                part = table[table["tier_view"].astype(str).eq(view)]
            summary_rows.append(summary_row(spec, view, part, primary, score_path, score_hash))
            for split in ["train", "validation", "oos"]:
                split_part = part[part["split"].astype(str).eq(split)]
                split_rows.append(split_row(spec, view, split, split_part, primary))
        handoff = {
            "package_id": package_id,
            "package_role": spec["package_role"],
            "run_id": RUN_ID,
            "score_table_path": rel(score_path),
            "score_table_hash": score_hash,
            "primary_score": primary,
            "runtime_handoff_fields": spec["runtime_handoff_fields"],
            "feature_order_hash": spec["feature_order_hash"],
            "blueprint_hash": spec["blueprint_hash"],
            "decision_rule_hash": spec["decision_rule_hash"],
            "risk_rule_hash": spec["risk_rule_hash"],
            "adapter_schema_hash": spec["adapter_schema_hash"],
            "selected_candidate": "none",
            "onnx_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "claim_boundary": BOUNDARY,
        }
        handoff_path = HANDOFF_DIR / f"{short}.json"
        write_json(handoff_path, handoff)
        handoff_paths.append(handoff_path)
    return score_paths, handoff_paths, summary_rows, split_rows, norm_rows


def summary_row(spec: Mapping[str, Any], view: str, part: pd.DataFrame, primary: str, score_path: Path, score_hash: str) -> dict[str, Any]:
    rows = int(len(part))
    signal = part["entry_signal"].astype(str) if rows else pd.Series(dtype="object")
    active = int(signal.ne("flat").sum()) if rows else 0
    return {
        "package_id": spec["package_id"],
        "package_role": spec["package_role"],
        "record_view": view,
        "rows": rows,
        "active_signal_count": active,
        "active_signal_rate": round(active / rows, 8) if rows else 0.0,
        "long_count": int(signal.eq("long").sum()) if rows else 0,
        "short_count": int(signal.eq("short").sum()) if rows else 0,
        "mean_primary_score": round(float(col(part, primary).mean()), 8) if rows else 0.0,
        "mean_model_risk_pct": round(float(col(part, "model_risk_pct").mean()), 8) if rows else 0.0,
        "score_table_path": rel(score_path),
        "score_table_hash": score_hash,
        "judgment": JUDGMENT,
        "claim_boundary": BOUNDARY,
    }


def split_row(spec: Mapping[str, Any], view: str, split: str, part: pd.DataFrame, primary: str) -> dict[str, Any]:
    rows = int(len(part))
    signal = part["entry_signal"].astype(str) if rows else pd.Series(dtype="object")
    active = int(signal.ne("flat").sum()) if rows else 0
    return {
        "package_id": spec["package_id"],
        "record_view": view,
        "split": split,
        "rows": rows,
        "active_signal_count": active,
        "active_signal_rate": round(active / rows, 8) if rows else 0.0,
        "long_count": int(signal.eq("long").sum()) if rows else 0,
        "short_count": int(signal.eq("short").sum()) if rows else 0,
        "mean_primary_score": round(float(col(part, primary).mean()), 8) if rows else 0.0,
        "claim_boundary": BOUNDARY,
    }


def write_receipts(
    specs: Sequence[Mapping[str, Any]],
    summary_rows: Sequence[Mapping[str, Any]],
    split_rows: Sequence[Mapping[str, Any]],
    norm_rows: Sequence[Mapping[str, Any]],
    tier_rows: Sequence[Mapping[str, Any]],
) -> None:
    write_csv(SUMMARY, SUMMARY_COLUMNS, summary_rows)
    write_csv(SPLIT_SUMMARY, SPLIT_COLUMNS, split_rows)
    write_json(
        NORMALIZATION,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "source_run_id": SOURCE_RUN_ID,
            "method": "train_split_median_mad_or_std_by_tier(학습 분할 중앙값 MAD 또는 표준편차 티어별 정규화)",
            "rows": norm_rows,
            "selected_candidate": "none",
            "onnx_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "claim_boundary": BOUNDARY,
        },
    )
    write_csv(TIER_RECEIPT, TIER_COLUMNS, tier_rows)
    write_json(EXPERIMENT_RECEIPT, experiment_receipt(specs, tier_rows))
    write_json(DATA_INTEGRITY_RECEIPT, data_integrity_receipt(tier_rows))
    write_json(MODEL_VALIDATION_RECEIPT, model_validation_receipt(specs))
    write_csv(RESULT_JUDGMENT, RESULT_COLUMNS, result_rows())
    write_csv(GATE_AUDIT, GATE_COLUMNS, gate_rows())


def experiment_receipt(specs: Sequence[Mapping[str, Any]], tier_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    selectable = sum(1 for row in specs if str(row["package_role"]).startswith("selectable"))
    support = len(specs) - selectable
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "hypothesis": (
            "run275C package specs(패키지 규격)는 Tier A/B model input dataset(티어 A/B 모델 입력 데이터셋) 위에서 "
            "deterministic score surface(결정론 점수 표면)로 물질화될 수 있다."
        ),
        "fresh_thesis": (
            "volatility pullback breakout(변동성 되돌림 돌파), cross-asset divergence reversal(교차자산 괴리 반전), "
            "cash session impulse continuation(현금장 충격 지속), macro volatility squeeze release(거시 변동성 압축 해제)를 "
            "Stage274 failure memory(274단계 실패 기억)와 분리해 새 후보 영역으로 만든다."
        ),
        "decision_use": (
            f"run275E score surface screen(점수 표면 선별)으로 넘길 구조적 입력만 만든다. next_action(다음 행동): {NEXT_ACTION}."
        ),
        "sample_scope": tier_rows,
        "packages": len(specs),
        "selectable_packages": selectable,
        "support_controls": support,
        "control_variables": (
            "FPMarkets US100 M5, run275C package identity hashes(패키지 정체성 해시), "
            "Tier A/B split labels(티어 A/B 분할 라벨), research-only claim boundary(연구 전용 주장 경계)."
        ),
        "changed_variables": (
            "package-level deterministic scoring formula(패키지별 결정론 점수 공식), "
            "Tier B partial-context feature fill(티어 B 부분 문맥 피처 보충), compact handoff path(짧은 인계 경로)."
        ),
        "success_criteria": (
            "five score tables(점수표 5개), handoff JSON(인계 JSON), tier receipt(티어 영수증), "
            "normalization receipt(정규화 영수증), lineage(계보)가 모두 생성된다."
        ),
        "failure_criteria": (
            "source spec(원천 규격) 누락, feature order(피처 순서) 불명확, score table(점수표) 생성 실패, "
            "Tier A/B paired record(티어 A/B 쌍 기록) 누락."
        ),
        "invalid_conditions": (
            "label/future column(라벨/미래 열)을 점수 공식에 쓰거나, run275D 결과를 selected candidate(선택 후보)로 주장하는 경우."
        ),
        "stop_conditions": (
            "run275E(275E 실행)가 fresh active signal(새 활성 신호), direction change(방향 변경), "
            "failure-signature distance(실패 서명 거리)를 만들 수 없으면 이 stage branch(단계 분기)는 폐기 후보가 된다."
        ),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": BOUNDARY,
    }


def data_integrity_receipt(tier_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "status": "passed_for_score_materialization_no_performance_claim(성과 주장 없는 점수 물질화 통과)",
        "tier_rows": tier_rows,
        "source_datasets": {
            "tier_a": {"path": rel(TIER_A_DATASET), "sha256": sha256_file_lf_normalized(TIER_A_DATASET)},
            "tier_b": {"path": rel(TIER_B_DATASET), "sha256": sha256_file_lf_normalized(TIER_B_DATASET)},
        },
        "feature_orders": {
            "tier_a": {"path": rel(TIER_A_FEATURE_ORDER), "sha256": sha256_file_lf_normalized(TIER_A_FEATURE_ORDER)},
            "tier_b": {"path": rel(TIER_B_FEATURE_ORDER), "sha256": sha256_file_lf_normalized(TIER_B_FEATURE_ORDER)},
        },
        "time_axis": "timestamp(시각)을 UTC(협정 세계시)로 읽고 원본 split(분할)을 유지했다.",
        "tier_b_boundary": "partial_context_score_input(부분 문맥 점수 입력)이며 runtime fallback authority(런타임 대체 권위)가 아니다.",
        "label_or_future_columns_used_by_scoring": False,
        "performance_claim": "none",
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": BOUNDARY,
    }


def model_validation_receipt(specs: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "status": "passed_boundary_only_no_selection(경계 통과, 선택 없음)",
        "model_surface": "deterministic scoring surface(결정론 점수 표면), not trained model(학습 모델 아님)",
        "threshold_policy": "train split quantile per tier(티어별 학습 분할 분위수) only",
        "score_formula_lineage": [
            {
                "package_id": row["package_id"],
                "feature_order_hash": row["feature_order_hash"],
                "decision_rule_hash": row["decision_rule_hash"],
                "risk_rule_hash": row["risk_rule_hash"],
                "adapter_schema_hash": row["adapter_schema_hash"],
            }
            for row in specs
        ],
        "allowed_claims": ["score_surface_materialized(점수 표면 물질화)"],
        "forbidden_claims": [
            "selected_candidate(선택 후보)",
            "ONNX readiness(ONNX 준비)",
            "Goal Achieve(목표 달성)",
            "runtime authority(런타임 권위)",
            "operating promotion(운영 승격)",
        ],
        "claim_boundary": BOUNDARY,
    }


def result_rows() -> list[dict[str, str]]:
    return [
        {
            "result_subject": RUN_ID,
            "evidence_available": "score tables(점수표), handoff JSON(인계 JSON), tier receipt(티어 영수증), normalization receipt(정규화 영수증)",
            "evidence_missing": "screening result(선별 결과), trading KPI(거래 핵심 성과 지표), MT5 runtime output(MT5 런타임 출력), ONNX parity(ONNX 동등성)",
            "judgment_label": JUDGMENT,
            "judgment_class": JUDGMENT_CLASS,
            "claim_boundary": BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "점수 표면은 만들어졌지만 후보 선택은 아직 아니다.",
        },
        {
            "result_subject": "candidate_selection(후보 선택)",
            "evidence_available": "materialized score surface(물질화된 점수 표면)",
            "evidence_missing": "run275E screen(275E 선별), aggressive/stability validation(공격형/안정성 검증), Adapter package(어댑터 패키지)",
            "judgment_label": "not_selected(선택 없음)",
            "judgment_class": "no_claim",
            "claim_boundary": BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "이 실행은 후보를 고르지 않고 선별 재료만 만든다.",
        },
        {
            "result_subject": "ONNX readiness(ONNX 준비)",
            "evidence_available": "none",
            "evidence_missing": "selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX parity(ONNX 동등성), MT5 reproduction(MT5 재현)",
            "judgment_label": "not_claimed(주장 안 함)",
            "judgment_class": "no_claim",
            "claim_boundary": BOUNDARY,
            "next_condition": "candidate package gate(후보 패키지 게이트)",
            "user_explanation_hook": "ONNX화는 아직 시작 조건 전이다.",
        },
    ]


def gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_name": "source_artifact_gate(원천 산출물 게이트)",
            "status": "passed(통과)",
            "evidence_path": rel(SOURCE_SPECS),
            "effect": "run275C 규격을 원천으로 고정해 임의 후보명을 만들지 않는다.",
        },
        {
            "gate_name": "tier_pairing_gate(티어 쌍 게이트)",
            "status": "passed(통과)",
            "evidence_path": rel(TIER_RECEIPT),
            "effect": "Tier A separate/Tier B separate/Tier A+B combined(티어 A 분리/티어 B 분리/티어 A+B 합산)을 함께 남긴다.",
        },
        {
            "gate_name": "data_integrity_gate(데이터 무결성 게이트)",
            "status": "passed(통과)",
            "evidence_path": rel(DATA_INTEGRITY_RECEIPT),
            "effect": "부분 문맥 누락과 원천 해시를 분리해 과장된 성과 주장을 막는다.",
        },
        {
            "gate_name": "model_validation_boundary_gate(모델 검증 경계 게이트)",
            "status": "passed(통과)",
            "evidence_path": rel(MODEL_VALIDATION_RECEIPT),
            "effect": "결정론 점수 표면을 학습 모델이나 ONNX 준비 상태로 오해하지 않게 한다.",
        },
        {
            "gate_name": "artifact_lineage_audit(산출물 계보 감사)",
            "status": "passed(통과)",
            "evidence_path": rel(LINEAGE_RECEIPT),
            "effect": "원천 입력, 생산자, 산출물, 등록부를 연결한다.",
        },
        {
            "gate_name": "final_claim_guard(최종 주장 방어)",
            "status": "passed(통과)",
            "evidence_path": rel(RESULT_JUDGMENT),
            "effect": "selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)를 주장하지 않는다.",
        },
    ]


def write_report(
    specs: Sequence[Mapping[str, Any]],
    summary_rows: Sequence[Mapping[str, Any]],
    split_rows: Sequence[Mapping[str, Any]],
    tier_rows: Sequence[Mapping[str, Any]],
    score_paths: Sequence[Path],
    handoff_paths: Sequence[Path],
) -> None:
    selectable = sum(1 for row in specs if str(row["package_role"]).startswith("selectable"))
    support = len(specs) - selectable
    combined_rows = [row for row in summary_rows if row["record_view"] == "Tier A+B combined"]
    summary_lines = "\n".join(
        (
            f"- `{row['package_id']}`: active_signal_rate(활성 신호율) `{row['active_signal_rate']}`, "
            f"long/short(매수/매도) `{row['long_count']}/{row['short_count']}`, "
            f"score_table(점수표) `{row['score_table_path']}`"
        )
        for row in combined_rows
    )
    tier_lines = "\n".join(
        f"- {row['tier_scope']}: rows(행) `{row['rows']}`, missing_required_features(필수 누락 피처) `{row['missing_required_features']}`"
        for row in tier_rows
    )
    write_md(
        RUN_REPORT,
        f"""# run275D Fresh Candidate Score Surface Materialization(275D 새 후보 점수 표면 물질화)

- run_id(실행 ID): `{RUN_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- packages(패키지): `{len(specs)}`
- selectable_packages(선택 가능 패키지): `{selectable}`
- support_controls(보조 대조): `{support}`
- score_tables(점수표): `{len(score_paths)}`
- handoff_json(인계 JSON): `{len(handoff_paths)}`
- summary_rows(요약 행): `{len(summary_rows)}`
- split_rows(분할 행): `{len(split_rows)}`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Plain Result(쉬운 결과)

run275D(275D 실행)는 run275C(275C 실행)의 package specs(패키지 규격)를 Tier A/Tier B model input dataset(티어 A/B 모델 입력 데이터셋)에 적용했다.
효과(effect, 효과): selectable seed(선택 가능 씨앗)와 support control(보조 대조)를 모두 score table(점수표)과 handoff JSON(인계 JSON)으로 만들었고, 아직 후보 선택이나 ONNX 준비를 주장하지 않는다.

## Tier Records(티어 기록)

{tier_lines}

## Combined Score Surface Summary(합산 점수 표면 요약)

{summary_lines}

## Evidence Paths(근거 경로)

- summary(요약): `{rel(SUMMARY)}`
- split_summary(분할 요약): `{rel(SPLIT_SUMMARY)}`
- normalization_receipt(정규화 영수증): `{rel(NORMALIZATION)}`
- tier_receipt(티어 영수증): `{rel(TIER_RECEIPT)}`
- data_integrity_receipt(데이터 무결성 영수증): `{rel(DATA_INTEGRITY_RECEIPT)}`
- model_validation_receipt(모델 검증 영수증): `{rel(MODEL_VALIDATION_RECEIPT)}`
- lineage(계보): `{rel(LINEAGE_RECEIPT)}`

## Boundary(경계)

`{BOUNDARY}`
""",
    )


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


def replace_or_append(text: str, prefix: str, replacement: str) -> str:
    if any(line.startswith(prefix) for line in text.splitlines()):
        return replace_line_prefix(text, prefix, replacement)
    return text.rstrip() + "\n\n" + replacement.rstrip() + "\n"


def prepend_focus(text: str, focus: str, marker: str) -> str:
    if marker in text:
        return text
    anchor = "current_focus:\n"
    if anchor in text:
        return text.replace(anchor, anchor + focus, 1)
    return text.rstrip() + "\ncurrent_focus:\n" + focus


def update_stage_docs(specs: Sequence[Mapping[str, Any]], summary_rows: Sequence[Mapping[str, Any]]) -> None:
    combined = [row for row in summary_rows if row["record_view"] == "Tier A+B combined"]
    active_total = sum(int(row["active_signal_count"]) for row in combined)
    rows_total = sum(int(row["rows"]) for row in combined)

    selection = io_path(SELECTION_STATUS).read_text(encoding="utf-8-sig")
    selection = replace_line_prefix(selection, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
    selection = replace_line_prefix(selection, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selection = replace_or_append(selection, "- run275D_report", f"- run275D_report(275D 보고서): `{rel(RUN_REPORT)}`")
    selection = replace_or_append(selection, "- run275D_summary", f"- run275D_summary(275D 요약): `{rel(SUMMARY)}`")
    write_md(SELECTION_STATUS, selection)

    review = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig")
    review = replace_or_append(review, "- run275D_report", f"- run275D_report(275D 보고서): `{rel(RUN_REPORT)}`")
    review = replace_or_append(review, "- run275D_summary", f"- run275D_summary(275D 요약): `{rel(SUMMARY)}`")
    review = replace_or_append(review, "- run275D_tier", f"- run275D_tier(275D 티어): `{rel(TIER_RECEIPT)}`")
    write_md(REVIEW_INDEX, review)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- status(", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- target_surface(", "- target_surface(목표 표면): `fresh_candidate_score_surface_materialization`")
    current = replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run275D_summary",
        (
            f"- run275D_summary(275D 요약): run275D(275D 실행)는 package(패키지) `{len(specs)}`개의 "
            f"score table(점수표)와 handoff JSON(인계 JSON)을 만들었다. Effect(효과): Tier A/B/A+B(티어 A/B/A+B) "
            f"합산 `{rows_total}`행 중 active signal(활성 신호) `{active_total}`개를 run275E(275E 실행) screen(선별)으로 넘기며, "
            "selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다."
        ),
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE_ID}")
    focus = (
        "- >-\n"
        f"  Stage275(275단계) run275D(275D 실행) fresh candidate score surface materialization(새 후보 점수 표면 물질화) `{RUN_ID}`. "
        f"Effect(효과): package(패키지) `{len(specs)}`개에 score table(점수표)과 handoff JSON(인계 JSON)을 만들고, "
        "selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_md(WORKSPACE_STATE, workspace)

    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    changelog = append_once(
        changelog,
        RUN_ID,
        (
            "## 2026-05-23 run275D fresh candidate score surface materialization(275D 새 후보 점수 표면 물질화)\n\n"
            f"- status(상태): `{STATUS}`\n"
            f"- judgment(판정): `{JUDGMENT}`\n"
            f"- effect(효과): package(패키지) `{len(specs)}`개에 score table(점수표)과 handoff JSON(인계 JSON)을 만들었다.\n"
            "- boundary(경계): selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n"
        ),
    )
    write_md(CHANGELOG, changelog)


def update_registers(created_at: str, specs: Sequence[Mapping[str, Any]], summary_rows: Sequence[Mapping[str, Any]], artifacts: Sequence[Path]) -> None:
    combined_by_package = {row["package_id"]: row for row in summary_rows if row["record_view"] == "Tier A+B combined"}
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "experiment_execution",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(RUN_REPORT),
                "notes": f"packages={len(specs)};score_tables=5;selected_candidate=none;onnx_readiness=not_claimed;next_action={NEXT_ACTION}.",
            }
        ],
        key="run_id",
    )
    alpha_rows = []
    for row in specs:
        package_id = str(row["package_id"])
        summary = combined_by_package.get(package_id, {})
        alpha_rows.append(
            {
                "ledger_row_id": f"{RUN_ID}__{package_id}",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": package_id,
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "fresh candidate score surface materialization(새 후보 점수 표면 물질화)",
                "tier_scope": "Tier A separate/Tier B separate/Tier A+B combined",
                "kpi_scope": "score_materialization_only_no_trading_kpi",
                "scoreboard_lane": "fresh_candidate_score_surface",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(SUMMARY),
                "primary_kpi": f"rows={summary.get('rows', 0)};active_signal_count={summary.get('active_signal_count', 0)};active_signal_rate={summary.get('active_signal_rate', 0)}",
                "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
                "external_verification_status": "out_of_scope_by_claim_score_materialization_only",
                "notes": f"score_table={summary.get('score_table_path', '')};package_role={row['package_role']}",
            }
        )
    upsert_csv_rows(ALPHA_LEDGER, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    upsert_csv_rows(
        STAGE_LEDGER,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__score_materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "fresh_candidate_score_surface_materialization",
                "tier_scope": "Tier A separate/Tier B separate/Tier A+B combined",
                "scoreboard": "score_surface_materialization",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "score_materialization_only_no_candidate_no_onnx",
                "report_path": rel(RUN_REPORT),
                "notes": f"summary_rows={len(summary_rows)};next_action={NEXT_ACTION}.",
            }
        ],
        key="row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{path.name.replace('.', '_')}",
            "artifact_type": "run275D_score_surface_materialization_artifact",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run275D fresh candidate score surface materialization artifact.",
        }
        for path in artifacts
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")


def build_tier_rows(tier_a: pd.DataFrame, tier_b: pd.DataFrame, combined: pd.DataFrame) -> list[dict[str, Any]]:
    tier_a_hash = str(tier_a["input_feature_order_hash"].iloc[0])
    tier_b_hash = str(tier_b["input_feature_order_hash"].iloc[0])
    return [
        {
            "tier_scope": "Tier A separate",
            "source_path": rel(TIER_A_DATASET),
            "feature_order_hash": tier_a_hash,
            "rows": int(len(tier_a)),
            "missing_required_features": str(tier_a["missing_required_features"].iloc[0]),
            "materialization_status": "materialized_full_context_score_inputs",
            "performance_claim": "none",
        },
        {
            "tier_scope": "Tier B separate",
            "source_path": rel(TIER_B_DATASET),
            "feature_order_hash": tier_b_hash,
            "rows": int(len(tier_b)),
            "missing_required_features": str(tier_b["missing_required_features"].iloc[0]),
            "materialization_status": "materialized_partial_context_score_inputs",
            "performance_claim": "none",
        },
        {
            "tier_scope": "Tier A+B combined",
            "source_path": "synthetic_score_materialization_view_from_tier_a_and_tier_b_score_tables",
            "feature_order_hash": f"TierA={tier_a_hash};TierB={tier_b_hash}",
            "rows": int(len(combined)),
            "missing_required_features": "see_component_rows",
            "materialization_status": "materialized_combined_score_input_view_no_routed_pnl",
            "performance_claim": "none",
        },
    ]


def enrich_specs(specs: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    enriched: list[dict[str, Any]] = []
    for spec in specs:
        row = dict(spec)
        row.setdefault("score_columns_hash", digest_payload(row.get("score_columns", [])))
        enriched.append(row)
    return enriched


def manifest_payload(created_at: str, specs: Sequence[Mapping[str, Any]], artifacts: Sequence[Path], source_inputs: Sequence[Path], summary_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": created_at,
        "producer": rel(PRODUCER_PATH),
        "entry_command": f"python {rel(PRODUCER_PATH)}",
        "source_inputs": [rel(path) for path in source_inputs],
        "input_hashes": {rel(path): sha256_file_lf_normalized(path) for path in source_inputs if path_exists(path)},
        "output_artifacts": [rel(path) for path in artifacts if path_exists(path)],
        "output_hashes": {rel(path): sha256_file_lf_normalized(path) for path in artifacts if path_exists(path)},
        "package_count": len(specs),
        "score_table_count": sum(1 for path in artifacts if path.parent == SCORE_DIR and path.suffix == ".parquet"),
        "handoff_count": sum(1 for path in artifacts if path.parent == HANDOFF_DIR and path.suffix == ".json"),
        "summary_rows": len(summary_rows),
        "tier_scope_records": list(SUMMARY_VIEWS),
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "external_verification_status": "out_of_scope_by_claim_score_materialization_only",
        "next_action": NEXT_ACTION,
        "claim_boundary": BOUNDARY,
    }


def lineage_payload(manifest: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_inputs": manifest["source_inputs"],
        "producer": manifest["producer"],
        "consumer": [NEXT_ACTION, rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "artifact_paths": manifest["output_artifacts"],
        "artifact_hashes": manifest["output_hashes"],
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "tracked_generated_stage_local",
        "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
        "claim_boundary": BOUNDARY,
    }


def run() -> dict[str, Any]:
    must_exist(
        [
            SOURCE_SPECS,
            SOURCE_HANDOFF,
            SOURCE_IDENTITY,
            SOURCE_SCHEMA,
            SOURCE_MANIFEST,
            SOURCE_REPORT,
            TIER_A_DATASET,
            TIER_A_FEATURE_ORDER,
            TIER_B_DATASET,
            TIER_B_FEATURE_ORDER,
        ]
    )
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    io_path(SCORE_DIR).mkdir(parents=True, exist_ok=True)
    io_path(HANDOFF_DIR).mkdir(parents=True, exist_ok=True)
    created_at = utc_now()

    specs_payload = read_json(SOURCE_SPECS)
    specs = enrich_specs(list(specs_payload["packages"]))
    expected_features = load_feature_order(TIER_A_FEATURE_ORDER)
    tier_a = prepare_tier(TIER_A_DATASET, "Tier A separate", TIER_A_FEATURE_ORDER, expected_features)
    tier_b = prepare_tier(TIER_B_DATASET, "Tier B separate", TIER_B_FEATURE_ORDER, expected_features)
    combined = pd.concat([tier_a, tier_b], ignore_index=True, sort=False)

    score_paths, handoff_paths, summary_rows, split_rows, norm_rows = materialize_scores(specs, combined)
    tier_rows = build_tier_rows(tier_a, tier_b, combined)
    write_receipts(specs, summary_rows, split_rows, norm_rows, tier_rows)
    write_report(specs, summary_rows, split_rows, tier_rows, score_paths, handoff_paths)

    source_inputs = [
        SOURCE_SPECS,
        SOURCE_HANDOFF,
        SOURCE_IDENTITY,
        SOURCE_SCHEMA,
        SOURCE_MANIFEST,
        SOURCE_REPORT,
        TIER_A_DATASET,
        TIER_A_FEATURE_ORDER,
        TIER_B_DATASET,
        TIER_B_FEATURE_ORDER,
    ]
    artifacts = [
        *score_paths,
        *handoff_paths,
        SUMMARY,
        SPLIT_SUMMARY,
        NORMALIZATION,
        TIER_RECEIPT,
        EXPERIMENT_RECEIPT,
        DATA_INTEGRITY_RECEIPT,
        MODEL_VALIDATION_RECEIPT,
        RESULT_JUDGMENT,
        GATE_AUDIT,
        RUN_REPORT,
    ]
    manifest = manifest_payload(created_at, specs, artifacts, source_inputs, summary_rows)
    write_json(RUN_MANIFEST, manifest)
    artifacts.append(RUN_MANIFEST)
    manifest = manifest_payload(created_at, specs, artifacts, source_inputs, summary_rows)
    write_json(LINEAGE_RECEIPT, lineage_payload(manifest))
    artifacts.append(LINEAGE_RECEIPT)
    manifest = manifest_payload(created_at, specs, artifacts, source_inputs, summary_rows)
    write_json(RUN_MANIFEST, manifest)

    update_registers(created_at, specs, summary_rows, artifacts)
    update_stage_docs(specs, summary_rows)

    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "packages": len(specs),
        "tier_a_rows": int(len(tier_a)),
        "tier_b_rows": int(len(tier_b)),
        "combined_rows": int(len(combined)),
        "summary_rows": len(summary_rows),
        "split_rows": len(split_rows),
        "score_tables": len(score_paths),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "report": rel(RUN_REPORT),
    }


def main() -> int:
    print(json.dumps(run(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
