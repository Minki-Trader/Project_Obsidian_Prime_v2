from __future__ import annotations

import hashlib
import json
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.models.onnx_bridge import ordered_hash  # noqa: E402
from stage_pipelines.stage307 import design_post_trade_shape_scale_rebuild as s307  # noqa: E402


STAGE_ID = "308_onnx_candidate_campaign__non_return_rank_profit_source_rebuild"
RUN_ID = "run308A_design_non_return_rank_profit_source_rebuild_packet_v1"
RUN_NUMBER = "run308A"
SOURCE_STAGE_ID = "307_onnx_candidate_campaign__post_trade_shape_scale_rebuild"
SOURCE_RUN_ID = "run307C_review_post_trade_shape_scale_mt5_probe_v1"
UPDATED_ON = "2026-05-24"
STATUS = "completed_non_return_rank_profit_source_candidates_materialized_no_selection"
JUDGMENT = "non_return_rank_profit_source_surfaces_materialized_no_candidate_selection"
NEXT_ACTION = "run308B_execute_non_return_rank_profit_source_mt5_probe"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS = STAGE_ROOT / "03_reviews"
SELECTED = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
PAYLOAD_DIR = RUN_ROOT / "payloads"
HANDOFF_DIR = RUN_ROOT / "handoff"
MODEL_DIR = RUN_ROOT / "models"

SOURCE_STAGE = ROOT / "stages" / SOURCE_STAGE_ID
SOURCE_RUN307C = SOURCE_STAGE / "02_runs" / "run307C"
SOURCE_RUN307A = SOURCE_STAGE / "02_runs" / "run307A"
SOURCE_SCOREBOARD = SOURCE_RUN307C / "post_trade_shape_scale_review_scoreboard.csv"
SOURCE_FAILURE_MEMORY = SOURCE_RUN307C / "failure_memory.csv"
SOURCE_SESSION = SOURCE_RUN307C / "session_attribution.csv"
SOURCE_MONTHLY = SOURCE_RUN307C / "monthly_attribution.csv"
SOURCE_CURVE = SOURCE_RUN307C / "curve_quality_summary.csv"
SOURCE_SEED_QUEUE = SOURCE_RUN307C / "stage308_seed_queue.csv"
SOURCE_REVIEW = SOURCE_STAGE / "03_reviews" / "run307C_review_stage308_open.md"

BRANCH_QUEUE = RUN_ROOT / "branch_design_queue.csv"
MODEL_SCOREBOARD = RUN_ROOT / "model_scout_scoreboard.csv"
CANDIDATE_SUPPLY = RUN_ROOT / "candidate_supply_diagnostics.csv"
PAYLOAD_MANIFEST = RUN_ROOT / "candidate_payload_manifest.csv"
MT5_QUEUE = RUN_ROOT / "mt5_probe_queue.csv"
MODEL_MANIFEST = RUN_ROOT / "model_artifact_manifest.csv"
WFO_FOLD_SCOREBOARD = RUN_ROOT / "wfo_fold_scoreboard.csv"
EXPERIMENT_DESIGN = RUN_ROOT / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_ROOT / "data_integrity_receipt.json"
RESULT_JUDGMENT = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT = RUN_ROOT / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
LINEAGE = RUN_ROOT / "artifact_lineage_receipt.json"
REPORT = REVIEWS / "run308A_materialization.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

RUNTIME_FEATURE_ORDER = ("route_signal_value",)
DECISION_FEATURES = (
    "hour",
    "dayofweek",
    "minutes_from_cash_open",
    "return_zscore_20",
    "bb_position_20",
    "historical_vol_5_over_20",
    "adx_14",
    "di_spread_14",
    "ppo_hist_12_26_9",
    "ema20_ema50_diff",
    "profit_quality_score",
    "profit_scale_score",
    "smooth_curve_score",
    "payoff_edge_score",
    "payoff_edge_direction",
    "mega8_equal_return_1",
    "top3_weighted_return_1",
    "mega8_pos_breadth_1",
    "us100_minus_mega8_equal_return_1",
    "us100_minus_top3_weighted_return_1",
    "vix_zscore_20",
    "us10yr_zscore_20",
    "usdx_zscore_20",
)

MANIFEST_COLUMNS = (
    "queue_id",
    "materialized_branch_id",
    "stage308_branch_id",
    "stage307_branch_id",
    "stage306_branch_id",
    "stage305_branch_id",
    "stage304_branch_id",
    "stage303_branch_id",
    "stage301_branch_id",
    "stage293_branch_id",
    "stage291_branch_id",
    "stage290_branch_id",
    "package_id",
    "queue_role",
    "payload_path",
    "payload_hash",
    "handoff_path",
    "handoff_hash",
    "model_artifact_path",
    "model_artifact_hash",
    "model_feature_order_path",
    "model_feature_order_hash",
    "direction_surface_hash",
    "direction_feature_order_hash",
    "max_hold_bars",
    "close_on_flat_signal",
    "same_direction_reentry_cooldown_bars",
    "atr_sltp_enabled",
    "atr_period",
    "atr_stop_multiplier",
    "atr_take_profit_multiplier",
    "atr_min_stop_points",
    "atr_max_stop_points",
    "atr_min_take_profit_points",
    "atr_max_take_profit_points",
    "exit_risk_overlay_enabled",
    "exit_risk_close_long_feature_index",
    "exit_risk_close_short_feature_index",
    "exit_risk_close_threshold",
    "exit_risk_min_hold_bars",
    "exit_risk_max_hold_feature_index",
    "model_risk_sizing_enabled",
    "model_risk_min_pct",
    "model_risk_max_pct",
    "model_risk_confidence_floor",
    "model_risk_confidence_ceiling",
    "model_risk_fallback_lot",
    "fixed_lot",
    "approx_validation_trades_per_day",
    "approx_oos_trades_per_day",
    "selected_candidate",
    "adapter_package",
    "onnx_readiness",
    "claim_boundary",
)

BRANCH_COLUMNS = (
    "branch_id",
    "package_id",
    "source_stage_id",
    "source_run_id",
    "hypothesis",
    "decision_use",
    "comparison_baseline",
    "control_variables",
    "changed_variables",
    "sample_scope",
    "success_criteria",
    "failure_criteria",
    "invalid_conditions",
    "stop_conditions",
    "evidence_plan",
    "feature_surface",
    "model_surface",
    "decision_surface",
    "risk_logic",
    "adapter_path",
    "runtime_handoff",
    "failure_memory_plan",
    "claim_boundary",
)


@dataclass(frozen=True)
class CandidateSpec:
    package_id: str
    decision_surface: str
    target_density: float
    max_hold_bars: int
    fixed_lot: float
    atr_stop_multiplier: float
    atr_take_profit_multiplier: float
    model_risk_sizing_enabled: bool
    model_risk_max_pct: float
    hypothesis: str
    changed_variables: str
    close_on_flat_signal: bool = True
    same_direction_reentry_cooldown_bars: int = 0
    atr_sltp_enabled: bool = True
    atr_period: int = 14
    model_risk_min_pct: float = 0.006
    model_risk_confidence_floor: float = 0.54
    model_risk_confidence_ceiling: float = 0.99
    model_risk_fallback_lot: float = 0.10


def candidate_specs() -> list[CandidateSpec]:
    return [
        CandidateSpec(
            package_id="cp308A_realized_session_edge_density60_hold5_surface",
            decision_surface="realized_session_edge_router",
            target_density=6.0,
            max_hold_bars=5,
            fixed_lot=0.30,
            atr_stop_multiplier=1.45,
            atr_take_profit_multiplier=4.70,
            model_risk_sizing_enabled=True,
            model_risk_max_pct=0.032,
            hypothesis="Actual MT5 session attribution can turn Stage307 positive pockets into a broader non-return-rank source.",
            changed_variables="session PnL state score, Stage306 base direction, shock guard, density 6/day, hold5.",
            close_on_flat_signal=False,
            same_direction_reentry_cooldown_bars=1,
        ),
        CandidateSpec(
            package_id="cp308B_curve_pocket_guard_density70_hold4_surface",
            decision_surface="curve_pocket_guard_router",
            target_density=7.0,
            max_hold_bars=4,
            fixed_lot=0.26,
            atr_stop_multiplier=1.25,
            atr_take_profit_multiplier=3.90,
            model_risk_sizing_enabled=True,
            model_risk_max_pct=0.026,
            hypothesis="A smooth-curve and shock-guard score can keep density while removing the local pockets that killed Stage307.",
            changed_variables="smooth_curve/profit_quality score gate, volatility shock penalty, density 7/day, tighter hold4.",
        ),
        CandidateSpec(
            package_id="cp308C_macro_breadth_divergence_density55_hold6_surface",
            decision_surface="macro_breadth_divergence_router",
            target_density=5.5,
            max_hold_bars=6,
            fixed_lot=0.30,
            atr_stop_multiplier=1.55,
            atr_take_profit_multiplier=5.10,
            model_risk_sizing_enabled=True,
            model_risk_max_pct=0.033,
            hypothesis="Mega-cap breadth and macro divergence can provide an orthogonal direction source not tied to return-rank labels.",
            changed_variables="breadth/macro direction, session penalty, density 5.5/day, hold6.",
            close_on_flat_signal=False,
            same_direction_reentry_cooldown_bars=1,
        ),
        CandidateSpec(
            package_id="cp308D_volatility_reversion_density85_hold3_surface",
            decision_surface="volatility_reversion_router",
            target_density=8.5,
            max_hold_bars=3,
            fixed_lot=0.22,
            atr_stop_multiplier=1.10,
            atr_take_profit_multiplier=3.40,
            model_risk_sizing_enabled=False,
            model_risk_max_pct=0.0,
            hypothesis="Short-hold volatility reversion may create trade count and smoother small edges without using return-rank scores.",
            changed_variables="return-zscore/bollinger reversion direction, high density 8.5/day, hold3, fixed risk.",
        ),
        CandidateSpec(
            package_id="cp308E_trend_quality_continuation_density50_hold7_surface",
            decision_surface="trend_quality_continuation_router",
            target_density=5.0,
            max_hold_bars=7,
            fixed_lot=0.32,
            atr_stop_multiplier=1.65,
            atr_take_profit_multiplier=5.60,
            model_risk_sizing_enabled=True,
            model_risk_max_pct=0.035,
            hypothesis="Trend quality plus smooth-curve state may recover scale from fewer but cleaner continuation trades.",
            changed_variables="ADX/DI/PPO/EMA trend direction, smooth score, density 5/day, hold7.",
            close_on_flat_signal=False,
            same_direction_reentry_cooldown_bars=2,
        ),
        CandidateSpec(
            package_id="cp308F_opening_breadth_impulse_density90_hold3_surface",
            decision_surface="opening_breadth_impulse_router",
            target_density=9.0,
            max_hold_bars=3,
            fixed_lot=0.22,
            atr_stop_multiplier=1.15,
            atr_take_profit_multiplier=3.50,
            model_risk_sizing_enabled=False,
            model_risk_max_pct=0.0,
            hypothesis="Opening and mid-session breadth impulse tests whether scale comes from broad intraday participation.",
            changed_variables="cash-session breadth impulse, macro guard, density 9/day, hold3, fixed risk.",
        ),
    ]


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return s307.rel(path)


def read_text(path: Path) -> str:
    return s307.read_text(path)


def write_json(path: Path, payload: Any, *, bom: bool = False) -> None:
    s307.write_json(path, payload, bom=bom)


def write_md(path: Path, text: str) -> None:
    s307.write_md(path, text)


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    return s307.read_csv_dicts(path)


def safe_upsert_csv_rows(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], key: str) -> None:
    s307.safe_upsert_csv_rows(path, columns, rows, key)


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    return s307.replace_line_prefix(text, prefix, replacement)


def append_once(text: str, marker: str, addition: str) -> str:
    return s307.append_once(text, marker, addition)


def prepend_focus(text: str, focus: str, marker: str) -> str:
    return s307.prepend_focus(text, focus, marker)


def add_time_features(payload: pd.DataFrame) -> pd.DataFrame:
    frame = payload.copy()
    timestamp = pd.to_datetime(frame["timestamp"], utc=True)
    frame["hour"] = timestamp.dt.hour.astype(float)
    frame["dayofweek"] = timestamp.dt.dayofweek.astype(float)
    frame["month_num"] = timestamp.dt.month.astype(float)
    frame["hour_sin"] = np.sin(2.0 * np.pi * frame["hour"] / 24.0)
    frame["hour_cos"] = np.cos(2.0 * np.pi * frame["hour"] / 24.0)
    frame["dow_sin"] = np.sin(2.0 * np.pi * frame["dayofweek"] / 5.0)
    frame["dow_cos"] = np.cos(2.0 * np.pi * frame["dayofweek"] / 5.0)
    return frame


def ncol(frame: pd.DataFrame, column: str, default: float = 0.0) -> np.ndarray:
    if column not in frame:
        return np.full(len(frame), default, dtype="float64")
    return pd.to_numeric(frame[column], errors="coerce").fillna(default).to_numpy(dtype="float64")


def zscore(values: np.ndarray) -> np.ndarray:
    finite = values[np.isfinite(values)]
    if finite.size == 0:
        return np.zeros_like(values, dtype="float64")
    median = float(np.median(finite))
    q75, q25 = np.percentile(finite, [75, 25])
    scale = float(q75 - q25) or float(np.std(finite)) or 1.0
    return np.clip((values - median) / scale, -4.0, 4.0)


def positive(values: np.ndarray) -> np.ndarray:
    return np.maximum(values, 0.0)


def base_direction(frame: pd.DataFrame) -> np.ndarray:
    direction = np.sign(ncol(frame, "payoff_edge_direction"))
    fallback = np.sign(ncol(frame, "route_signal_value"))
    direction = np.where(direction != 0, direction, fallback)
    return direction.astype("int8")


def session_arrays(frame: pd.DataFrame) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    hour = ncol(frame, "hour")
    outside = ((hour < 16) | (hour > 23)).astype("float64")
    cash_open = ((hour >= 16) & (hour < 18)).astype("float64")
    mid = ((hour >= 18) & (hour < 21)).astype("float64")
    late = ((hour >= 21) & (hour <= 23)).astype("float64")
    return outside, cash_open, mid, late


def shock_score(frame: pd.DataFrame) -> np.ndarray:
    vol = positive(zscore(ncol(frame, "historical_vol_5_over_20", 1.0)))
    ret = np.abs(zscore(ncol(frame, "return_zscore_20")))
    vix = np.abs(zscore(ncol(frame, "vix_zscore_20")))
    rates = np.abs(zscore(ncol(frame, "us10yr_zscore_20")))
    usd = np.abs(zscore(ncol(frame, "usdx_zscore_20")))
    return 0.35 * vol + 0.30 * ret + 0.15 * vix + 0.10 * rates + 0.10 * usd


def signal_for_spec(spec: CandidateSpec, frame: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    outside, cash_open, mid, late = session_arrays(frame)
    minutes = ncol(frame, "minutes_from_cash_open")
    session_edge = 0.35 * outside + 0.25 * cash_open + 0.95 * mid + 0.80 * late
    quality = zscore(ncol(frame, "profit_quality_score"))
    scale = zscore(ncol(frame, "profit_scale_score"))
    smooth = zscore(ncol(frame, "smooth_curve_score"))
    payoff = zscore(ncol(frame, "payoff_edge_score"))
    shock = shock_score(frame)
    base = base_direction(frame)

    if spec.decision_surface == "realized_session_edge_router":
        raw = base.astype("float64")
        score = 1.35 * session_edge + 0.45 * positive(quality) + 0.35 * positive(scale) + 0.25 * positive(smooth) - 0.55 * shock
        keep = score > np.nanpercentile(score, 38)
    elif spec.decision_surface == "curve_pocket_guard_router":
        raw = base.astype("float64")
        score = 0.90 * positive(quality) + 1.10 * positive(smooth) + 0.30 * positive(payoff) + 0.40 * mid - 0.90 * shock
        keep = (score > np.nanpercentile(score, 30)) & (shock < np.nanpercentile(shock, 78))
    elif spec.decision_surface == "macro_breadth_divergence_router":
        breadth = zscore(ncol(frame, "mega8_pos_breadth_1"))
        mega = zscore(ncol(frame, "mega8_equal_return_1"))
        top3 = zscore(ncol(frame, "top3_weighted_return_1"))
        under = -zscore(ncol(frame, "us100_minus_mega8_equal_return_1"))
        macro = -0.35 * zscore(ncol(frame, "us10yr_zscore_20")) - 0.30 * zscore(ncol(frame, "usdx_zscore_20"))
        raw = breadth + 0.60 * mega + 0.45 * top3 + 0.35 * under + macro
        score = np.abs(raw) + 0.45 * session_edge + 0.25 * positive(smooth) - 0.45 * shock
        keep = score > np.nanpercentile(score, 42)
    elif spec.decision_surface == "volatility_reversion_router":
        ret = zscore(ncol(frame, "return_zscore_20"))
        bb = zscore(ncol(frame, "bb_position_20", 0.5) - 0.5)
        raw = -(0.75 * ret + 0.65 * bb)
        score = np.abs(raw) + 0.35 * positive(zscore(ncol(frame, "historical_vol_5_over_20", 1.0))) + 0.20 * session_edge - 0.30 * shock
        keep = score > np.nanpercentile(score, 25)
    elif spec.decision_surface == "trend_quality_continuation_router":
        trend = zscore(ncol(frame, "ema20_ema50_diff")) + 0.55 * zscore(ncol(frame, "di_spread_14")) + 0.35 * zscore(ncol(frame, "ppo_hist_12_26_9"))
        adx = positive(zscore(ncol(frame, "adx_14", 20.0)))
        raw = trend
        score = np.abs(raw) + 0.75 * adx + 0.50 * positive(smooth) + 0.25 * late - 0.40 * shock
        keep = score > np.nanpercentile(score, 48)
    elif spec.decision_surface == "opening_breadth_impulse_router":
        impulse = zscore(ncol(frame, "mega8_equal_return_1")) + 0.65 * zscore(ncol(frame, "top3_weighted_return_1")) + 0.45 * zscore(ncol(frame, "ppo_hist_12_26_9"))
        open_mid = (((minutes >= 20) & (minutes <= 330)).astype("float64") + mid + 0.35 * late)
        raw = impulse
        score = np.abs(raw) + 0.70 * open_mid + 0.25 * positive(quality) - 0.35 * shock
        keep = score > np.nanpercentile(score, 18)
    else:
        raise ValueError(f"unsupported decision_surface: {spec.decision_surface}")

    signal = np.sign(raw).astype("int8")
    signal = np.where(keep, signal, 0).astype("int8")
    signal = s307.prev.s294.trim_to_density(frame, signal, np.asarray(score, dtype="float64"), spec.max_hold_bars, spec.target_density)
    return signal.astype("int8"), np.asarray(score, dtype="float64")


def risk_manifest_fields(spec: CandidateSpec) -> dict[str, Any]:
    return {
        "atr_sltp_enabled": int(spec.atr_sltp_enabled),
        "atr_period": spec.atr_period,
        "atr_stop_multiplier": spec.atr_stop_multiplier,
        "atr_take_profit_multiplier": spec.atr_take_profit_multiplier,
        "atr_min_stop_points": 0.0,
        "atr_max_stop_points": 0.0,
        "atr_min_take_profit_points": 0.0,
        "atr_max_take_profit_points": 0.0,
        "exit_risk_overlay_enabled": 0,
        "exit_risk_close_long_feature_index": -1,
        "exit_risk_close_short_feature_index": -1,
        "exit_risk_close_threshold": 0.5,
        "exit_risk_min_hold_bars": 0,
        "exit_risk_max_hold_feature_index": -1,
        "model_risk_sizing_enabled": int(spec.model_risk_sizing_enabled),
        "model_risk_min_pct": spec.model_risk_min_pct,
        "model_risk_max_pct": spec.model_risk_max_pct,
        "model_risk_confidence_floor": spec.model_risk_confidence_floor,
        "model_risk_confidence_ceiling": spec.model_risk_confidence_ceiling,
        "model_risk_fallback_lot": spec.model_risk_fallback_lot,
        "fixed_lot": spec.fixed_lot,
    }


def supply_rows_for_payload(payload: pd.DataFrame, spec: CandidateSpec) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    frame = payload.copy()
    frame["date"] = pd.to_datetime(frame["timestamp"], utc=True).dt.date.astype(str)
    for (tier_scope, split), part in frame.groupby(["tier_scope", "split"], observed=True):
        active = part.loc[pd.to_numeric(part["route_signal_value"], errors="coerce").fillna(0).ne(0)]
        days = max(1, int(part["date"].nunique()))
        approx_trade_count = int(len(active) / max(1, spec.max_hold_bars))
        approx_tpd = approx_trade_count / days
        rows.append(
            {
                "materialized_branch_id": str(part["materialized_branch_id"].iloc[0]),
                "package_id": spec.package_id,
                "tier_scope": tier_scope,
                "split": split,
                "rows": len(part),
                "days": days,
                "active_signal_count": len(active),
                "long_signal_count": int((pd.to_numeric(part["route_signal_value"], errors="coerce").fillna(0) > 0).sum()),
                "short_signal_count": int((pd.to_numeric(part["route_signal_value"], errors="coerce").fillna(0) < 0).sum()),
                "active_signals_per_day": len(active) / days,
                "approx_trade_count": approx_trade_count,
                "approx_trades_per_day": approx_tpd,
                "max_hold_bars": spec.max_hold_bars,
                "trade_density_screen": "passed" if 4.0 <= approx_tpd <= 10.0 else "failed",
            }
        )
    return rows


def source_stage307_seed() -> str:
    rows = read_csv_dicts(SOURCE_SEED_QUEUE)
    return rows[0].get("materialized_branch_id", "stage307_failure_memory_mixed") if rows else "stage307_failure_memory_mixed"


def materialize_payload(
    spec: CandidateSpec,
    base: pd.DataFrame,
    seed: Mapping[str, str],
    stage307_seed: str,
    frame: pd.DataFrame,
) -> tuple[pd.DataFrame, dict[str, Any], dict[str, Any], dict[str, Any]]:
    signal, score = signal_for_spec(spec, frame)
    branch_id = f"run308A_{spec.package_id.replace('_surface', '')}"
    payload = base.copy()
    payload["stage308_branch_id"] = branch_id
    payload["stage307_branch_id"] = stage307_seed
    payload["stage306_branch_id"] = seed.get("materialized_branch_id", "")
    payload["stage305_branch_id"] = seed.get("stage305_branch_id", "")
    payload["stage304_branch_id"] = seed.get("stage304_branch_id", "")
    payload["stage303_branch_id"] = seed.get("stage303_branch_id", "")
    payload["stage301_branch_id"] = seed.get("stage301_branch_id", "")
    payload["stage293_branch_id"] = branch_id
    payload["stage291_branch_id"] = branch_id
    payload["stage290_branch_id"] = branch_id
    payload["materialized_branch_id"] = branch_id
    payload["package_id"] = spec.package_id
    payload["queue_role"] = "non_return_rank_profit_source_surface"
    payload["candidate_decision_score"] = score
    payload["non_return_rank_score_value"] = score
    payload["direction_signal_value"] = signal
    payload["route_signal_value"] = signal
    payload["route_signal_label"] = [s307.prev.s290.signal_label(int(value)) for value in signal]
    payload["signal_active"] = (signal != 0).astype("int8")
    payload["model_risk_pct"] = spec.model_risk_max_pct if spec.model_risk_sizing_enabled else 0.0
    payload["max_hold_bars"] = spec.max_hold_bars
    payload["close_on_flat_signal"] = spec.close_on_flat_signal
    payload["same_direction_reentry_cooldown_bars"] = spec.same_direction_reentry_cooldown_bars
    identity = {
        "package_id": spec.package_id,
        "source_stage_id": SOURCE_STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "decision_surface": spec.decision_surface,
        "target_density": spec.target_density,
        "max_hold_bars": spec.max_hold_bars,
        "runtime_feature_order": list(RUNTIME_FEATURE_ORDER),
        "model_feature_order": list(DECISION_FEATURES),
        "model_feature_order_hash": ordered_hash(DECISION_FEATURES),
        "risk_logic": risk_manifest_fields(spec),
        "claim_boundary": BOUNDARY,
    }
    surface_hash = hashlib.sha256(json.dumps(identity, sort_keys=True).encode("utf-8")).hexdigest()
    payload["direction_surface_hash"] = surface_hash
    payload["variant_decision_surface_hash"] = surface_hash
    payload["direction_feature_order_hash"] = ordered_hash(RUNTIME_FEATURE_ORDER)
    payload["model_feature_order_hash"] = ordered_hash(DECISION_FEATURES)
    payload["payload_claim_boundary"] = BOUNDARY
    validation_metrics = s307.prev.metrics_for_payload(spec, payload, "validation")
    oos_metrics = s307.prev.metrics_for_payload(spec, payload, "oos")
    drop_columns = [name for name in payload.columns if name.startswith(("label", "future_")) or name in {"label_class", "evaluation_label_available"}]
    payload = payload.drop(columns=drop_columns, errors="ignore")
    return payload, identity | {"direction_surface_hash": surface_hash}, validation_metrics, oos_metrics


def gate_label(validation: Mapping[str, Any], oos: Mapping[str, Any], gate: str) -> str:
    return s307.prev.gate_label(validation, oos, gate)


def build_outputs() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[Path]]:
    base, seed = s307.base_payload()
    frame = add_time_features(base)
    stage307_seed = source_stage307_seed()
    branch_rows: list[dict[str, Any]] = []
    scoreboard_rows: list[dict[str, Any]] = []
    supply_rows: list[dict[str, Any]] = []
    manifest_rows: list[dict[str, Any]] = []
    model_rows: list[dict[str, Any]] = []
    wfo_rows: list[dict[str, Any]] = []
    artifacts: list[Path] = []
    for index, spec in enumerate(candidate_specs(), start=1):
        payload, identity, validation_metrics, oos_metrics = materialize_payload(spec, base, seed, stage307_seed, frame)
        branch_id = f"run308A_{spec.package_id.replace('_surface', '')}"
        payload_path = PAYLOAD_DIR / f"{branch_id}_payload.parquet"
        handoff_path = HANDOFF_DIR / f"{branch_id}_handoff.json"
        model_spec_path = MODEL_DIR / f"{branch_id}_rule_surface.json"
        s307.prev.io_path(payload_path.parent).mkdir(parents=True, exist_ok=True)
        payload.to_parquet(s307.prev.io_path(payload_path), index=False)
        write_json(model_spec_path, identity)
        write_json(
            handoff_path,
            {
                "stage308_branch_id": branch_id,
                "source_stage_id": SOURCE_STAGE_ID,
                "package_id": spec.package_id,
                "runtime_feature_order": list(RUNTIME_FEATURE_ORDER),
                "runtime_feature_order_hash": ordered_hash(RUNTIME_FEATURE_ORDER),
                "model_feature_order": list(DECISION_FEATURES),
                "model_feature_order_hash": ordered_hash(DECISION_FEATURES),
                "decision_surface": identity,
                "risk_logic": risk_manifest_fields(spec),
                "runtime_handoff": "precomputed route_signal_value replay for Stage308 MT5 probe",
                "claim_boundary": BOUNDARY,
            },
        )
        candidate_supply = supply_rows_for_payload(payload, spec)
        supply_rows.extend(candidate_supply)
        val_supply = next(row for row in candidate_supply if row["tier_scope"] == "Tier A" and row["split"] == "validation")
        oos_supply = next(row for row in candidate_supply if row["tier_scope"] == "Tier A" and row["split"] == "oos")
        den_gate = gate_label(validation_metrics, oos_metrics, "density")
        edge_gate = gate_label(validation_metrics, oos_metrics, "edge")
        curve_gate = gate_label(validation_metrics, oos_metrics, "curve")
        selection_score = (
            s307.prev.s290.selection_score(validation_metrics)
            + s307.prev.s290.selection_score(oos_metrics)
            + min(float(validation_metrics["net_bp"]), float(oos_metrics["net_bp"])) * 1.50
        )
        branch_rows.append(
            {
                "branch_id": branch_id,
                "package_id": spec.package_id,
                "source_stage_id": SOURCE_STAGE_ID,
                "source_run_id": SOURCE_RUN_ID,
                "hypothesis": spec.hypothesis,
                "decision_use": "Check whether a non-return-rank source can create a profit-scale ONNX-worthy seed.",
                "comparison_baseline": "Stage307 actual MT5 failure: inverse return-rank had density or split/curve damage.",
                "control_variables": "US100 M5 split_v1; Stage306 feature base; Stage307 failure memory; Tier A/B paired runtime accounting; no Adapter or ONNX claim.",
                "changed_variables": spec.changed_variables,
                "sample_scope": "Tier A/Tier B validation/OOS signal replay; MT5 runtime is decisive.",
                "success_criteria": "MT5 validation/OOS positive, minimum trade count, 4-10 trades/day, profit scale, PF/recovery/expectancy, and no deep parsed curve pocket.",
                "failure_criteria": "Profit scale absent, OOS negative, density outside 4-10, or parsed curve pocket remains deep.",
                "invalid_conditions": "source payload missing, feature-label leakage, feature order mismatch, or MT5 report parse missing.",
                "stop_conditions": "candidate gate pass opens Adapter package; otherwise pivot to a new profit source instead of repairing this source.",
                "evidence_plan": "branch queue, proxy scoreboard, payload manifest, MT5 queue, run308B KPI, run308C parsed curve review.",
                "feature_surface": "Stage306 feature base plus Stage307 actual MT5 attribution features and time/session transforms.",
                "model_surface": "rule_surface_no_return_rank_model",
                "decision_surface": spec.decision_surface,
                "risk_logic": json.dumps(risk_manifest_fields(spec), sort_keys=True),
                "adapter_path": "deferred_until_candidate_gate",
                "runtime_handoff": "route_signal_value replay now; decision feature order retained for Adapter trace if candidate gate passes.",
                "failure_memory_plan": "Record whether session, curve guard, breadth, volatility reversion, trend, or opening impulse source failed.",
                "claim_boundary": BOUNDARY,
            }
        )
        manifest_rows.append(
            {
                "queue_id": f"run308A_queue_{index:02d}",
                "materialized_branch_id": branch_id,
                "stage308_branch_id": branch_id,
                "stage307_branch_id": stage307_seed,
                "stage306_branch_id": seed.get("materialized_branch_id", ""),
                "stage305_branch_id": seed.get("stage305_branch_id", ""),
                "stage304_branch_id": seed.get("stage304_branch_id", ""),
                "stage303_branch_id": seed.get("stage303_branch_id", ""),
                "stage301_branch_id": seed.get("stage301_branch_id", ""),
                "stage293_branch_id": branch_id,
                "stage291_branch_id": branch_id,
                "stage290_branch_id": branch_id,
                "package_id": spec.package_id,
                "queue_role": "non_return_rank_profit_source_surface",
                "payload_path": rel(payload_path),
                "payload_hash": s307.prev.sha256_file_lf_normalized(payload_path),
                "handoff_path": rel(handoff_path),
                "handoff_hash": s307.prev.sha256_file_lf_normalized(handoff_path),
                "model_artifact_path": rel(model_spec_path),
                "model_artifact_hash": s307.prev.sha256_file_lf_normalized(model_spec_path),
                "model_feature_order_path": rel(model_spec_path),
                "model_feature_order_hash": ordered_hash(DECISION_FEATURES),
                "direction_surface_hash": identity["direction_surface_hash"],
                "direction_feature_order_hash": ordered_hash(RUNTIME_FEATURE_ORDER),
                "max_hold_bars": spec.max_hold_bars,
                "close_on_flat_signal": int(spec.close_on_flat_signal),
                "same_direction_reentry_cooldown_bars": spec.same_direction_reentry_cooldown_bars,
                **risk_manifest_fields(spec),
                "approx_validation_trades_per_day": val_supply["approx_trades_per_day"],
                "approx_oos_trades_per_day": oos_supply["approx_trades_per_day"],
                "selected_candidate": "none",
                "adapter_package": "none",
                "onnx_readiness": "not_claimed",
                "claim_boundary": BOUNDARY,
            }
        )
        model_rows.append(
            {
                "materialized_branch_id": branch_id,
                "package_id": spec.package_id,
                "model_family": "non_return_rank_rule_surface",
                "prediction_kind": "runtime_state_profit_source",
                "dataset_id": "stage307_actual_mt5_failure_memory_plus_stage306_features",
                "model_artifact_path": rel(model_spec_path),
                "model_artifact_hash": s307.prev.sha256_file_lf_normalized(model_spec_path),
                "model_feature_order_path": rel(model_spec_path),
                "model_feature_order_hash": ordered_hash(DECISION_FEATURES),
                "imputation_path": rel(model_spec_path),
                "imputation_hash": s307.prev.sha256_file_lf_normalized(model_spec_path),
                "classes": "-1,0,1",
                "payoff_weight_policy": spec.decision_surface,
                "onnx_exportability_note": "Adapter required before ONNX; rule surface feature order and route_signal handoff are traceable.",
            }
        )
        scoreboard_rows.append(
            {
                "materialized_branch_id": branch_id,
                "package_id": spec.package_id,
                "dataset_id": "stage307_actual_mt5_failure_memory_plus_stage306_features",
                "model_family": "non_return_rank_rule_surface",
                "prediction_kind": "runtime_state_profit_source",
                "mode": spec.decision_surface,
                "quantile": "",
                "threshold": "",
                "precondition": spec.decision_surface,
                "wfo_net_bp": float(validation_metrics["net_bp"]) + float(oos_metrics["net_bp"]),
                "wfo_positive_fold_share": float((float(validation_metrics["net_bp"]) > 0.0) + (float(oos_metrics["net_bp"]) > 0.0)) / 2.0,
                "wfo_worst_fold_net_bp": min(float(validation_metrics["net_bp"]), float(oos_metrics["net_bp"])),
                "wfo_mean_trades_per_day": (float(validation_metrics["trades_per_day"]) + float(oos_metrics["trades_per_day"])) / 2.0,
                "wfo_min_trades_per_day": min(float(validation_metrics["trades_per_day"]), float(oos_metrics["trades_per_day"])),
                "wfo_max_trades_per_day": max(float(validation_metrics["trades_per_day"]), float(oos_metrics["trades_per_day"])),
                "validation_proxy_net_bp": validation_metrics["net_bp"],
                "validation_proxy_pf": validation_metrics["pf"],
                "validation_proxy_trade_count": validation_metrics["trade_count"],
                "validation_proxy_trades_per_day": validation_metrics["trades_per_day"],
                "validation_proxy_recovery": validation_metrics["recovery"],
                "validation_proxy_worst_month_bp": validation_metrics["worst_month_bp"],
                "validation_proxy_worst_rolling_20_bp": validation_metrics["worst_rolling_20_bp"],
                "validation_proxy_worst_rolling_50_bp": validation_metrics["worst_rolling_50_bp"],
                "validation_proxy_positive_month_share": validation_metrics["positive_month_share"],
                "validation_proxy_underwater_ratio": validation_metrics["underwater_ratio"],
                "oos_proxy_net_bp": oos_metrics["net_bp"],
                "oos_proxy_pf": oos_metrics["pf"],
                "oos_proxy_trade_count": oos_metrics["trade_count"],
                "oos_proxy_trades_per_day": oos_metrics["trades_per_day"],
                "oos_proxy_recovery": oos_metrics["recovery"],
                "oos_proxy_worst_month_bp": oos_metrics["worst_month_bp"],
                "oos_proxy_worst_rolling_20_bp": oos_metrics["worst_rolling_20_bp"],
                "oos_proxy_worst_rolling_50_bp": oos_metrics["worst_rolling_50_bp"],
                "oos_proxy_positive_month_share": oos_metrics["positive_month_share"],
                "oos_proxy_underwater_ratio": oos_metrics["underwater_ratio"],
                "density_gate": den_gate,
                "proxy_edge_gate": edge_gate,
                "curve_proxy_gate": curve_gate,
                "selection_score": selection_score,
                "selected_candidate": "none",
                "adapter_package": "none",
                "onnx_readiness": "not_claimed",
                "claim_boundary": BOUNDARY,
            }
        )
        for split_name, metrics in (("validation", validation_metrics), ("oos", oos_metrics)):
            wfo_rows.append(
                {
                    "materialized_branch_id": branch_id,
                    "package_id": spec.package_id,
                    "fold_id": split_name,
                    "mode": spec.decision_surface,
                    "quantile": "",
                    "threshold": "",
                    "net_bp": metrics["net_bp"],
                    "pf": metrics["pf"],
                    "trade_count": metrics["trade_count"],
                    "trades_per_day": metrics["trades_per_day"],
                    "recovery": metrics["recovery"],
                    "worst_month_bp": metrics["worst_month_bp"],
                    "worst_rolling_20_bp": metrics["worst_rolling_20_bp"],
                    "worst_rolling_50_bp": metrics["worst_rolling_50_bp"],
                    "positive_month_share": metrics["positive_month_share"],
                    "underwater_ratio": metrics["underwater_ratio"],
                }
            )
        artifacts.extend([payload_path, handoff_path, model_spec_path])
    return branch_rows, scoreboard_rows, supply_rows, manifest_rows, model_rows, wfo_rows, artifacts


def result_rows(scoreboard_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    density_pass = sum(1 for row in scoreboard_rows if row["density_gate"] == "passed")
    edge_pass = sum(1 for row in scoreboard_rows if row["proxy_edge_gate"] == "passed")
    curve_pass = sum(1 for row in scoreboard_rows if row["curve_proxy_gate"] == "passed")
    result = [
        {
            "result_subject": "Stage308 non-return-rank profit source materialization",
            "evidence_available": f"candidate_rows={len(scoreboard_rows)};mt5_queue_rows={len(manifest_rows)};density_proxy_pass={density_pass};edge_proxy_pass={edge_pass};curve_proxy_pass={curve_pass}",
            "evidence_missing": "MT5 runtime KPI, Adapter package, ONNX parity",
            "judgment_label": "exploratory",
            "judgment_class": JUDGMENT,
            "claim_boundary": BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "Stage308 replaces return-rank ML with non-return-rank state/rule profit sources and does not select before MT5 evidence.",
        }
    ]
    gates = [
        {"gate_name": "fresh_thesis", "status": "passed", "evidence_path": rel(EXPERIMENT_DESIGN), "effect": "Stage307 return-rank failure is replaced with session, curve, breadth, volatility, trend, and opening impulse sources."},
        {"gate_name": "source_lineage", "status": "passed", "evidence_path": rel(LINEAGE), "effect": "Each branch points back to Stage307 actual MT5 failure memory and Stage306 feature base."},
        {"gate_name": "proxy_density_edge_curve_screen", "status": "passed" if density_pass and edge_pass else "partial", "evidence_path": rel(MODEL_SCOREBOARD), "effect": "4-10 trades/day and proxy edge are screened before MT5."},
        {"gate_name": "mt5_runtime_probe", "status": "prepared", "evidence_path": rel(MT5_QUEUE), "effect": "run308B can execute Tier A, Tier B fallback, and actual routed total attempts."},
        {"gate_name": "adapter_package", "status": "not_started", "evidence_path": "", "effect": "No Adapter before candidate gate."},
        {"gate_name": "onnx_readiness", "status": "not_started", "evidence_path": "", "effect": "ONNX waits for Adapter and parity gates."},
    ]
    return result, gates


def report_markdown(scoreboard_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]]) -> str:
    ordered = sorted(scoreboard_rows, key=lambda row: float(row["selection_score"]), reverse=True)
    lines = [
        "# run308A Non-Return-Rank Profit Source Materialization(308A 비수익순위 수익 원천 물질화)",
        "",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        "- selected_candidate(선택 후보): `none`",
        "- Adapter package(어댑터 패키지): `none`",
        "- ONNX readiness(온엑스 준비): `not_claimed`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "",
        "Effect(효과): Stage307(307단계)의 return-rank(수익 순위) 실패를 버리고 session/breadth/volatility/trend(세션/브레드스/변동성/추세) 기반 비수익순위 후보를 만들었다.",
        "",
        "| package(패키지) | surface(표면) | val bp(검증 bp) | val/day(검증 일거래) | OOS bp(표본외 bp) | OOS/day(표본외 일거래) | density(밀도) | edge(우위) | curve(곡선) |",
        "|---|---|---:|---:|---:|---:|---|---|---|",
    ]
    for row in ordered:
        lines.append(
            "| {pkg} | {mode} | {vn:.1f} | {vtd:.2f} | {on:.1f} | {otd:.2f} | {den} | {edge} | {curve} |".format(
                pkg=row["package_id"],
                mode=row["mode"],
                vn=float(row["validation_proxy_net_bp"]),
                vtd=float(row["validation_proxy_trades_per_day"]),
                on=float(row["oos_proxy_net_bp"]),
                otd=float(row["oos_proxy_trades_per_day"]),
                den=row["density_gate"],
                edge=row["proxy_edge_gate"],
                curve=row["curve_proxy_gate"],
            )
        )
    lines.extend(["", f"- mt5_queue_rows(MT5 대기열 수): `{len(manifest_rows)}`", f"- claim_boundary(주장 경계): `{BOUNDARY}`"])
    return "\n".join(lines)


def write_outputs(
    branch_rows: Sequence[Mapping[str, Any]],
    scoreboard_rows: Sequence[Mapping[str, Any]],
    supply_rows: Sequence[Mapping[str, Any]],
    manifest_rows: Sequence[Mapping[str, Any]],
    model_rows: Sequence[Mapping[str, Any]],
    wfo_rows: Sequence[Mapping[str, Any]],
    payload_artifacts: Sequence[Path],
    created_at: str,
) -> list[Path]:
    result, gates = result_rows(scoreboard_rows, manifest_rows)
    s307.prev.write_csv_rows(BRANCH_QUEUE, BRANCH_COLUMNS, branch_rows)
    s307.prev.write_csv_rows(MODEL_SCOREBOARD, s307.prev.s293.SCOREBOARD_COLUMNS, scoreboard_rows)
    s307.prev.write_csv_rows(CANDIDATE_SUPPLY, s307.prev.s293.SUPPLY_COLUMNS, supply_rows)
    s307.prev.write_csv_rows(PAYLOAD_MANIFEST, MANIFEST_COLUMNS, manifest_rows)
    s307.prev.write_csv_rows(MT5_QUEUE, MANIFEST_COLUMNS, manifest_rows)
    s307.prev.write_csv_rows(MODEL_MANIFEST, s307.prev.MODEL_COLUMNS, model_rows)
    s307.prev.write_csv_rows(WFO_FOLD_SCOREBOARD, s307.prev.s293.WFO_COLUMNS, wfo_rows)
    s307.prev.write_csv_rows(RESULT_JUDGMENT, s307.prev.s293.RESULT_COLUMNS, result)
    s307.prev.write_csv_rows(GATE_AUDIT, s307.prev.s293.GATE_COLUMNS, gates)
    write_json(
        EXPERIMENT_DESIGN,
        {
            "hypothesis": "Non-return-rank state/rule profit sources can create profit scale after Stage307 return-rank ML failure.",
            "decision_use": "Open or reject MT5 runtime probe candidates before Adapter and ONNX work.",
            "comparison_baseline": "Stage307 actual MT5 negative return-rank review with cp307E scale watch but OOS/density/curve failure.",
            "control_variables": ["US100 M5", "split_v1", "Stage306 feature base", "Stage307 actual MT5 failure memory", "Tier A/B paired accounting"],
            "changed_variables": ["decision source", "session attribution", "curve-pocket guard", "breadth/macro direction", "volatility reversion", "trend continuation", "opening impulse", "risk logic"],
            "sample_scope": "Tier A/Tier B validation/OOS proxy and MT5 runtime probe.",
            "success_criteria": ["MT5 validation/OOS positive", "minimum trade count", "4-10 trades/day", "profit scale", "PF/recovery/expectancy acceptable", "no deep parsed curve pocket"],
            "failure_criteria": ["weak net scale", "density outside 4-10", "OOS negative", "deep curve pocket"],
            "invalid_conditions": ["source payload missing", "feature-label leakage", "runtime report parse missing"],
            "stop_conditions": ["candidate gate pass moves to Adapter package", "otherwise pivot away from this non-return-rank source"],
            "evidence_plan": [rel(MODEL_SCOREBOARD), rel(PAYLOAD_MANIFEST), rel(MT5_QUEUE), "run308B MT5 KPI", "run308C parsed curve review"],
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            "source_scoreboard": rel(SOURCE_SCOREBOARD),
            "source_failure_memory": rel(SOURCE_FAILURE_MEMORY),
            "source_session_attribution": rel(SOURCE_SESSION),
            "source_monthly_attribution": rel(SOURCE_MONTHLY),
            "source_curve_quality": rel(SOURCE_CURVE),
            "source_seed_queue": rel(SOURCE_SEED_QUEUE),
            "decision_feature_count": len(DECISION_FEATURES),
            "model_feature_order_hash": ordered_hash(DECISION_FEATURES),
            "runtime_feature_order_hash": ordered_hash(RUNTIME_FEATURE_ORDER),
            "stage307_direct_failure_boundary": "no selected candidate; Adapter and ONNX not started",
        },
    )
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "source_run_id": SOURCE_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "selected_candidate": "none",
            "adapter_package": "none",
            "onnx_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "next_action": NEXT_ACTION,
            "artifacts": [rel(path) for path in [BRANCH_QUEUE, MODEL_SCOREBOARD, CANDIDATE_SUPPLY, PAYLOAD_MANIFEST, MT5_QUEUE, MODEL_MANIFEST, WFO_FOLD_SCOREBOARD, EXPERIMENT_DESIGN, DATA_RECEIPT, RESULT_JUDGMENT, GATE_AUDIT, LINEAGE, REPORT]],
            "claim_boundary": BOUNDARY,
        },
    )
    write_json(
        LINEAGE,
        {
            "run_id": RUN_ID,
            "producer": "stage_pipelines/stage308/design_non_return_rank_profit_source_rebuild.py",
            "source_inputs": [rel(SOURCE_SCOREBOARD), rel(SOURCE_FAILURE_MEMORY), rel(SOURCE_SESSION), rel(SOURCE_MONTHLY), rel(SOURCE_CURVE), rel(SOURCE_SEED_QUEUE), rel(SOURCE_REVIEW)],
            "consumer": NEXT_ACTION,
            "artifact_paths": {"scoreboard": rel(MODEL_SCOREBOARD), "mt5_queue": rel(MT5_QUEUE), "report": rel(REPORT)},
            "artifact_hashes": {"model_feature_order_hash": ordered_hash(DECISION_FEATURES), "runtime_feature_order_hash": ordered_hash(RUNTIME_FEATURE_ORDER)},
            "lineage_judgment": "connected_with_boundary",
            "claim_boundary": BOUNDARY,
        },
    )
    write_md(REPORT, report_markdown(scoreboard_rows, manifest_rows))
    return list(payload_artifacts) + [BRANCH_QUEUE, MODEL_SCOREBOARD, CANDIDATE_SUPPLY, PAYLOAD_MANIFEST, MT5_QUEUE, MODEL_MANIFEST, WFO_FOLD_SCOREBOARD, EXPERIMENT_DESIGN, DATA_RECEIPT, RESULT_JUDGMENT, GATE_AUDIT, RUN_MANIFEST, LINEAGE, REPORT]


def update_registers(scoreboard_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]], artifacts: Sequence[Path], created_at: str) -> None:
    safe_upsert_csv_rows(
        RUN_REGISTRY,
        ("run_id", "stage_id", "lane", "status", "judgment", "path", "notes"),
        [{"run_id": RUN_ID, "stage_id": STAGE_ID, "lane": "non_return_rank_profit_source_materialization", "status": STATUS, "judgment": JUDGMENT, "path": rel(REPORT), "notes": f"branches={len(scoreboard_rows)};mt5_queue_rows={len(manifest_rows)};next_action={NEXT_ACTION}"}],
        "run_id",
    )
    safe_upsert_csv_rows(
        ALPHA_LEDGER,
        s307.prev.s293.ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "run_number": RUN_NUMBER,
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "non_return_rank_profit_source_materialization",
                "tier_scope": "Tier A/Tier B paired exploration labels",
                "kpi_scope": "proxy_density_edge_curve_screen",
                "scoreboard_lane": "non_return_rank_profit_source",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "summary": f"materialized={len(scoreboard_rows)};mt5_queue_rows={len(manifest_rows)};selected_candidate=none",
                "claim_boundary": BOUNDARY,
                "external_verification_status": "out_of_scope_by_claim",
                "notes": f"next_action={NEXT_ACTION}.",
            }
        ],
        "ledger_row_id",
    )
    safe_upsert_csv_rows(
        STAGE_LEDGER,
        s307.prev.s293.STAGE_LEDGER_COLUMNS,
        [{"row_id": f"{RUN_ID}__materialization", "stage_id": STAGE_ID, "run_id": RUN_ID, "view": "non_return_rank_profit_source_materialization", "tier_scope": "Tier A/Tier B paired exploration labels", "scoreboard": "model_scout_scoreboard", "status": STATUS, "judgment": JUDGMENT, "evidence_boundary": "materialization_no_candidate_no_onnx", "report_path": rel(REPORT), "notes": f"mt5_queue_rows={len(manifest_rows)};next_action={NEXT_ACTION}"}],
        "row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{hashlib.sha1(rel(path).encode('utf-8')).hexdigest()[:12]}",
            "artifact_type": "stage308_non_return_rank_profit_source_artifact",
            "path": rel(path),
            "sha256": s307.prev.sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run308A non-return-rank profit source materialization",
        }
        for path in artifacts
        if s307.prev.io_path(path).exists()
    ]
    safe_upsert_csv_rows(ARTIFACT_REGISTRY, s307.prev.s293.ARTIFACT_COLUMNS, artifact_rows, "artifact_id")


def update_docs(scoreboard_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]]) -> None:
    selected = read_text(SELECTED)
    selected = replace_line_prefix(selected, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
    selected = replace_line_prefix(selected, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = replace_line_prefix(selected, "- run308A_report(", f"- run308A_report(308A 보고서): `{rel(REPORT)}`")
    selected = replace_line_prefix(selected, "- run308A_mt5_queue(", f"- run308A_mt5_queue(308A MT5 대기열): `{rel(MT5_QUEUE)}`")
    write_md(SELECTED, selected)

    review_index = read_text(REVIEW_INDEX) or "# Stage308 Review Index(308단계 검토 색인)\n"
    review_index = replace_line_prefix(review_index, "- run308A_report(", f"- run308A_report(308A 보고서): `{rel(REPORT)}`")
    review_index = replace_line_prefix(review_index, "- run308A_mt5_queue(", f"- run308A_mt5_queue(308A MT5 대기열): `{rel(MT5_QUEUE)}`")
    write_md(REVIEW_INDEX, review_index)

    idea = read_text(IDEA_REGISTER)
    idea = append_once(
        idea,
        "stage308_non_return_rank_profit_source",
        "## stage308_non_return_rank_profit_source\n\n- hypothesis(가설): non-return-rank(비수익순위) state/rule source(상태/규칙 원천)가 Stage307(307단계) return-rank(수익 순위) 실패 이후 수익 규모와 곡선을 동시에 회복할 수 있다.\n- boundary(경계): exploratory(탐색), no selected candidate(선택 후보 없음), no Adapter(어댑터 없음), no ONNX(온엑스 없음).\n",
    )
    write_md(IDEA_REGISTER, idea)

    current = read_text(CURRENT_STATE)
    current = replace_line_prefix(current, "- current_packet(", f"- current_packet(현재 작업 묶음): `{STAGE_ID}_v1`")
    current = replace_line_prefix(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- active_stage(", f"- active_stage(활성 단계): `{STAGE_ID}`")
    current = replace_line_prefix(current, "- source_stage(", f"- source_stage(원천 단계): `{SOURCE_STAGE_ID}`")
    current = replace_line_prefix(current, "- status(", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run308A_summary",
        f"- run308A_summary(308A 요약): non-return-rank profit source(비수익순위 수익 원천) 후보 `{len(scoreboard_rows)}`개를 materialized(물질화)했다. Effect(효과): Stage307(307단계) return-rank failure(수익 순위 실패)를 새 session/breadth/volatility/trend source(세션/브레드스/변동성/추세 원천) MT5 queue(MT5 대기열) `{len(manifest_rows)}`개로 바꿨으며 선택 후보/Adapter(어댑터)/ONNX(온엑스)는 주장하지 않는다.",
    )
    write_md(CURRENT_STATE, current)

    workspace = read_text(WORKSPACE_STATE)
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE_ID}")
    workspace = replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = (
        f"- >-\n"
        f"  Stage308(308단계) run308A(308A 실행) non-return-rank profit source materialization(비수익순위 수익 원천 물질화) `{RUN_ID}`. "
        f"Effect(효과): candidates(후보) `{len(scoreboard_rows)}`개와 MT5 queue(MT5 대기열) `{len(manifest_rows)}`개를 만들었고 selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비)는 주장하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_md(WORKSPACE_STATE, workspace)

    changelog = read_text(CHANGELOG) or "# Changelog(변경 기록)\n"
    changelog = append_once(
        changelog,
        RUN_ID,
        f"## {UPDATED_ON} run308A Non-return-rank profit source materialization(308A 비수익순위 수익 원천 물질화)\n\n"
        f"- run_id(실행 ID): `{RUN_ID}`\n"
        f"- status(상태): `{STATUS}`\n"
        f"- candidates(후보): `{len(scoreboard_rows)}`\n"
        f"- mt5_queue_rows(MT5 대기열 수): `{len(manifest_rows)}`\n"
        f"- next_action(다음 행동): `{NEXT_ACTION}`\n",
    )
    write_md(CHANGELOG, changelog)


def main() -> None:
    created_at = utc_now()
    branch_rows, scoreboard_rows, supply_rows, manifest_rows, model_rows, wfo_rows, payload_artifacts = build_outputs()
    artifacts = write_outputs(branch_rows, scoreboard_rows, supply_rows, manifest_rows, model_rows, wfo_rows, payload_artifacts, created_at)
    update_registers(scoreboard_rows, manifest_rows, artifacts, created_at)
    update_docs(scoreboard_rows, manifest_rows)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "branch_count": len(scoreboard_rows),
                "mt5_queue_rows": len(manifest_rows),
                "decision_feature_count": len(DECISION_FEATURES),
                "selected_candidate": "none",
                "adapter_package": "none",
                "onnx_readiness": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_ACTION,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
