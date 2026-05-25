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
from sklearn.ensemble import ExtraTreesRegressor, RandomForestRegressor
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import RobustScaler


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.models.onnx_bridge import ordered_hash  # noqa: E402
from stage_pipelines.stage305 import design_runtime_realized_curve_attribution_rebuild as prev  # noqa: E402


STAGE_ID = "307_onnx_candidate_campaign__post_trade_shape_scale_rebuild"
RUN_ID = "run307A_design_post_trade_shape_scale_rebuild_v1"
RUN_NUMBER = "run307A"
SOURCE_STAGE_ID = "306_onnx_candidate_campaign__anti_surface_trade_shape_rebuild"
SOURCE_RUN_ID = "run306C_review_anti_surface_trade_shape_mt5_probe_v1"
UPDATED_ON = "2026-05-24"
STATUS = "completed_post_trade_shape_scale_candidates_materialized_no_selection"
JUDGMENT = "post_trade_shape_scale_ml_surfaces_materialized_no_candidate_selection"
NEXT_ACTION = "run307B_execute_post_trade_shape_scale_mt5_probe"
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
SOURCE_RUN306A = SOURCE_STAGE / "02_runs" / "run306A"
SOURCE_RUN306C = SOURCE_STAGE / "02_runs" / "run306C"
SOURCE_MANIFEST = SOURCE_RUN306A / "candidate_payload_manifest.csv"
SOURCE_SCOREBOARD = SOURCE_RUN306C / "anti_surface_trade_shape_review_scoreboard.csv"
SOURCE_TRADE_QUALITY = SOURCE_RUN306C / "trade_quality_summary.csv"
SOURCE_SESSION = SOURCE_RUN306C / "session_attribution.csv"
SOURCE_MONTHLY = SOURCE_RUN306C / "monthly_attribution.csv"
SOURCE_SEED_QUEUE = SOURCE_RUN306C / "stage307_seed_queue.csv"
SOURCE_REVIEW = SOURCE_STAGE / "03_reviews" / "run306C_anti_surface_trade_shape_review_stage307_open_report.md"

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
REPORT = REVIEWS / "run307A_post_trade_shape_scale_materialization_report.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

RUNTIME_FEATURE_ORDER = ("route_signal_value",)

MANIFEST_COLUMNS = (
    "queue_id",
    "materialized_branch_id",
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
    model_key: str
    decision_surface: str
    signal_policy: str
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
            package_id="cp307A_hgb_inverse_rank_density55_hold4_surface",
            model_key="hgb_return",
            decision_surface="rank_tail_balanced",
            signal_policy="inverse_rank",
            target_density=5.5,
            max_hold_bars=4,
            fixed_lot=0.30,
            atr_stop_multiplier=1.45,
            atr_take_profit_multiplier=4.60,
            model_risk_sizing_enabled=True,
            model_risk_max_pct=0.030,
            hypothesis="A fresh HistGradientBoosting inverse-rank surface tests whether the direct return-rank sign was anti-correlated with runtime profit.",
            changed_variables="new ML score surface; inverse rank tails after direct-sign proxy failure; target 5.5 trades/day; payoff asymmetric risk.",
        ),
        CandidateSpec(
            package_id="cp307B_extratrees_inverse_rank_density70_hold4_surface",
            model_key="extratrees_return",
            decision_surface="rank_tail_wide",
            signal_policy="inverse_rank",
            target_density=7.0,
            max_hold_bars=4,
            fixed_lot=0.26,
            atr_stop_multiplier=1.35,
            atr_take_profit_multiplier=4.10,
            model_risk_sizing_enabled=True,
            model_risk_max_pct=0.028,
            hypothesis="An ExtraTrees inverse-rank surface may capture nonlinear anti-pockets that the Stage306 rule surface missed.",
            changed_variables="new ExtraTrees score surface; inverse direction; wider density 7/day; moderate payoff asymmetry.",
        ),
        CandidateSpec(
            package_id="cp307C_ensemble_inverse_consensus_density60_hold5_surface",
            model_key="ensemble_return",
            decision_surface="consensus_rank_tail",
            signal_policy="inverse_rank",
            target_density=6.0,
            max_hold_bars=5,
            fixed_lot=0.28,
            atr_stop_multiplier=1.50,
            atr_take_profit_multiplier=4.80,
            model_risk_sizing_enabled=True,
            model_risk_max_pct=0.032,
            hypothesis="Inverse consensus between gradient and tree rankers checks whether agreement marks crowding risk rather than direct edge.",
            changed_variables="HGB/ExtraTrees/RF ensemble consensus; inverse direction; target 6/day; hold5.",
            close_on_flat_signal=False,
            same_direction_reentry_cooldown_bars=1,
        ),
        CandidateSpec(
            package_id="cp307D_outside_late_inverse_amplified_density50_hold6_surface",
            model_key="ensemble_return",
            decision_surface="outside_late_amplified_rank",
            signal_policy="inverse_rank",
            target_density=5.0,
            max_hold_bars=6,
            fixed_lot=0.30,
            atr_stop_multiplier=1.60,
            atr_take_profit_multiplier=5.30,
            model_risk_sizing_enabled=True,
            model_risk_max_pct=0.034,
            hypothesis="Stage306 showed large outside/late pockets; an inverse ML ranker tests whether those pockets were contrarian rather than directional.",
            changed_variables="ensemble rank with outside/late score amplification; inverse direction; target 5/day; longer hold6.",
            close_on_flat_signal=False,
            same_direction_reentry_cooldown_bars=1,
        ),
        CandidateSpec(
            package_id="cp307E_inverse_tail_asymmetry_density45_hold8_surface",
            model_key="hgb_return",
            decision_surface="extreme_tail_asymmetry",
            signal_policy="inverse_rank",
            target_density=4.5,
            max_hold_bars=8,
            fixed_lot=0.34,
            atr_stop_multiplier=1.75,
            atr_take_profit_multiplier=6.00,
            model_risk_sizing_enabled=True,
            model_risk_max_pct=0.036,
            hypothesis="A lower-density inverse extreme-tail surface tests whether strong predicted returns identify exhaustion zones with better payoff asymmetry.",
            changed_variables="inverse extreme rank tails, target 4.5/day, hold8, high TP asymmetry.",
            close_on_flat_signal=False,
            same_direction_reentry_cooldown_bars=2,
        ),
        CandidateSpec(
            package_id="cp307F_inverse_high_density_rf_rank_density90_hold3_surface",
            model_key="rf_return",
            decision_surface="high_density_rank",
            signal_policy="inverse_rank",
            target_density=9.0,
            max_hold_bars=3,
            fixed_lot=0.22,
            atr_stop_multiplier=1.20,
            atr_take_profit_multiplier=3.60,
            model_risk_sizing_enabled=False,
            model_risk_max_pct=0.0,
            hypothesis="A high-density inverse random-forest rank surface tests whether broad small anti-edges can create smoother scale.",
            changed_variables="inverse RF rank surface, 9/day, hold3, fixed risk.",
        ),
    ]


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return prev.rel(path)


def read_text(path: Path) -> str:
    return prev.read_text(path)


def write_json(path: Path, payload: Any, *, bom: bool = False) -> None:
    prev.write_json(path, payload, bom=bom)


def write_md(path: Path, text: str) -> None:
    prev.write_md(path, text)


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    return prev.read_csv_dicts(path)


def safe_upsert_csv_rows(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], key: str) -> None:
    prev.safe_upsert_csv_rows(path, columns, rows, key)


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    return prev.replace_line_prefix(text, prefix, replacement)


def append_once(text: str, marker: str, addition: str) -> str:
    return prev.append_once(text, marker, addition)


def prepend_focus(text: str, focus: str, marker: str) -> str:
    return prev.prepend_focus(text, focus, marker)


def source_manifest() -> list[dict[str, str]]:
    return read_csv_dicts(SOURCE_MANIFEST)


def base_payload() -> tuple[pd.DataFrame, dict[str, str]]:
    manifest = source_manifest()
    seed = next((row for row in manifest if row["package_id"].startswith("cp306C_")), manifest[0])
    payload = pd.read_parquet(prev.io_path(ROOT / seed["payload_path"]))
    return payload, seed


def feature_frame(payload: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    frame = payload.copy()
    timestamp = pd.to_datetime(frame["timestamp"], utc=True)
    frame["hour"] = timestamp.dt.hour.astype(float)
    frame["dayofweek"] = timestamp.dt.dayofweek.astype(float)
    frame["month_num"] = timestamp.dt.month.astype(float)
    frame["hour_sin"] = np.sin(2.0 * np.pi * frame["hour"] / 24.0)
    frame["hour_cos"] = np.cos(2.0 * np.pi * frame["hour"] / 24.0)
    frame["dow_sin"] = np.sin(2.0 * np.pi * frame["dayofweek"] / 5.0)
    frame["dow_cos"] = np.cos(2.0 * np.pi * frame["dayofweek"] / 5.0)
    exclude_prefix = ("label", "future_")
    exclude = {
        "timestamp",
        "symbol",
        "split",
        "split_id",
        "tier_scope",
        "materialized_branch_id",
        "package_id",
        "queue_role",
        "route_signal_label",
        "payload_claim_boundary",
        "source_package_id",
        "source_transform_id",
        "direction_surface_hash",
        "variant_decision_surface_hash",
        "direction_feature_order_hash",
        "model_feature_order_hash",
    }
    feature_cols = [
        col
        for col in frame.columns
        if col not in exclude
        and not col.startswith(exclude_prefix)
        and pd.api.types.is_numeric_dtype(frame[col])
    ]
    feature_cols = sorted(dict.fromkeys(feature_cols))
    return frame, feature_cols


def training_frame(payload: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series, pd.DataFrame, list[str]]:
    frame, feature_cols = feature_frame(payload)
    dataset = prev.s290.load_dataset("fwd12_proxy58")[["timestamp", "split", "future_log_return_12"]].copy()
    dataset["timestamp"] = pd.to_datetime(dataset["timestamp"], utc=True)
    frame = frame.merge(dataset, on=["timestamp", "split"], how="left", validate="many_to_one")
    tier_a = frame.loc[frame["tier_scope"].astype(str).eq("Tier A")].copy()
    train = tier_a.loc[tier_a["split"].astype(str).eq("train")].copy()
    feature_cols = [col for col in feature_cols if not train[col].isna().all()]
    x_train = train[feature_cols]
    y_train = pd.to_numeric(train["future_log_return_12"], errors="coerce").fillna(0.0) * 10000.0
    return x_train, y_train, frame, feature_cols


def fit_models(x_train: pd.DataFrame, y_train: pd.Series) -> dict[str, Any]:
    models: dict[str, Any] = {
        "hgb_return": make_pipeline(
            SimpleImputer(strategy="median"),
            HistGradientBoostingRegressor(max_iter=220, learning_rate=0.045, max_leaf_nodes=31, l2_regularization=0.05, random_state=307),
        ),
        "extratrees_return": make_pipeline(
            SimpleImputer(strategy="median"),
            ExtraTreesRegressor(n_estimators=220, max_depth=9, min_samples_leaf=28, max_features=0.70, random_state=307, n_jobs=-1),
        ),
        "rf_return": make_pipeline(
            SimpleImputer(strategy="median"),
            RandomForestRegressor(n_estimators=180, max_depth=8, min_samples_leaf=36, max_features=0.65, random_state=307, n_jobs=-1),
        ),
    }
    for model in models.values():
        model.fit(x_train, y_train)
    return models


def model_scores(models: Mapping[str, Any], frame: pd.DataFrame, feature_cols: Sequence[str]) -> dict[str, np.ndarray]:
    x_all = frame[list(feature_cols)]
    scores = {key: np.asarray(model.predict(x_all), dtype="float64") for key, model in models.items()}
    stacked = np.vstack([scores["hgb_return"], scores["extratrees_return"], scores["rf_return"]])
    scores["ensemble_return"] = np.nanmean(stacked, axis=0)
    return scores


def session_weight(frame: pd.DataFrame, surface: str) -> np.ndarray:
    hour = pd.to_numeric(frame["hour"], errors="coerce").fillna(0.0).to_numpy()
    minutes = pd.to_numeric(frame.get("minutes_from_cash_open", 0.0), errors="coerce").fillna(0.0).to_numpy()
    vol = pd.to_numeric(frame.get("historical_vol_5_over_20", 1.0), errors="coerce").fillna(1.0).to_numpy()
    adx = pd.to_numeric(frame.get("adx_14", 20.0), errors="coerce").fillna(20.0).to_numpy()
    outside = (hour < 16) | (hour > 23)
    late = (hour >= 21) & (hour <= 23)
    mid_good = (hour >= 19) & (hour <= 20)
    bad_mid = (hour == 18) | ((hour == 21) & (vol < 0.85))
    weight = np.ones(len(frame), dtype="float64")
    if surface == "outside_late_amplified_rank":
        weight *= np.where(outside, 1.55, 1.0)
        weight *= np.where(late, 1.35, 1.0)
        weight *= np.where(mid_good & (adx >= 18), 1.15, 1.0)
        weight *= np.where(bad_mid, 0.55, 1.0)
    elif surface == "extreme_tail_asymmetry":
        weight *= np.where(outside | late, 1.25, 1.0)
        weight *= np.where((minutes >= 60) & (minutes <= 330), 1.05, 0.85)
    elif surface == "high_density_rank":
        weight *= np.where((hour >= 17) & (hour <= 23), 1.05, 1.0)
        weight *= np.where(vol < 0.65, 0.75, 1.0)
    elif surface == "consensus_rank_tail":
        weight *= np.where(outside | late | mid_good, 1.15, 1.0)
    return weight


def signal_for_spec(spec: CandidateSpec, frame: pd.DataFrame, scores: Mapping[str, np.ndarray]) -> tuple[np.ndarray, np.ndarray]:
    raw_score = scores[spec.model_key].copy()
    if spec.decision_surface == "consensus_rank_tail":
        hgb = scores["hgb_return"]
        et = scores["extratrees_return"]
        rf = scores["rf_return"]
        consensus = np.sign(hgb) + np.sign(et) + np.sign(rf)
        raw_score = np.where(np.abs(consensus) >= 2, raw_score, 0.0)
    raw_score = raw_score * session_weight(frame, spec.decision_surface)
    if spec.signal_policy == "inverse_rank":
        raw_score = -raw_score
    elif spec.signal_policy != "direct_rank":
        raise ValueError(f"Unsupported signal_policy: {spec.signal_policy}")
    if spec.decision_surface == "extreme_tail_asymmetry":
        signal = np.sign(raw_score).astype("int8")
        score = np.abs(raw_score) ** 1.25
    else:
        signal = np.sign(raw_score).astype("int8")
        score = np.abs(raw_score)
    signal = prev.s294.trim_to_density(frame, signal, score, spec.max_hold_bars, spec.target_density)
    return signal.astype("int8"), score.astype("float64")


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


def materialize_payload(
    spec: CandidateSpec,
    base: pd.DataFrame,
    seed: Mapping[str, str],
    frame: pd.DataFrame,
    feature_cols: Sequence[str],
    scores: Mapping[str, np.ndarray],
) -> tuple[pd.DataFrame, dict[str, Any], dict[str, Any], dict[str, Any]]:
    signal, score = signal_for_spec(spec, frame, scores)
    branch_id = f"run307A_{spec.package_id.replace('_surface', '')}"
    payload = base.copy()
    payload["stage307_branch_id"] = branch_id
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
    payload["queue_role"] = "post_trade_shape_scale_ml_surface"
    payload["candidate_decision_score"] = score
    payload["ml_score_value"] = scores[spec.model_key]
    payload["direction_signal_value"] = signal
    payload["route_signal_value"] = signal
    payload["route_signal_label"] = [prev.s290.signal_label(int(value)) for value in signal]
    payload["signal_active"] = (signal != 0).astype("int8")
    payload["model_risk_pct"] = spec.model_risk_max_pct if spec.model_risk_sizing_enabled else 0.0
    payload["max_hold_bars"] = spec.max_hold_bars
    payload["close_on_flat_signal"] = spec.close_on_flat_signal
    payload["same_direction_reentry_cooldown_bars"] = spec.same_direction_reentry_cooldown_bars
    identity = {
        "package_id": spec.package_id,
        "source_stage_id": SOURCE_STAGE_ID,
        "model_key": spec.model_key,
        "decision_surface": spec.decision_surface,
        "signal_policy": spec.signal_policy,
        "target_density": spec.target_density,
        "max_hold_bars": spec.max_hold_bars,
        "runtime_feature_order": list(RUNTIME_FEATURE_ORDER),
        "model_feature_order": list(feature_cols),
        "model_feature_order_hash": ordered_hash(feature_cols),
        "risk_logic": risk_manifest_fields(spec),
        "claim_boundary": BOUNDARY,
    }
    surface_hash = hashlib.sha256(json.dumps(identity, sort_keys=True).encode("utf-8")).hexdigest()
    payload["direction_surface_hash"] = surface_hash
    payload["variant_decision_surface_hash"] = surface_hash
    payload["direction_feature_order_hash"] = ordered_hash(RUNTIME_FEATURE_ORDER)
    payload["model_feature_order_hash"] = ordered_hash(feature_cols)
    payload["payload_claim_boundary"] = BOUNDARY
    validation_metrics = prev.metrics_for_payload(spec, payload, "validation")
    oos_metrics = prev.metrics_for_payload(spec, payload, "oos")
    drop_columns = [name for name in payload.columns if name.startswith(("label", "future_")) or name in {"label_class", "evaluation_label_available"}]
    payload = payload.drop(columns=drop_columns, errors="ignore")
    return payload, identity | {"direction_surface_hash": surface_hash}, validation_metrics, oos_metrics


def gate_label(validation: Mapping[str, Any], oos: Mapping[str, Any], gate: str) -> str:
    return prev.gate_label(validation, oos, gate)


def build_outputs() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[Path], list[str]]:
    base, seed = base_payload()
    x_train, y_train, frame, feature_cols = training_frame(base)
    models = fit_models(x_train, y_train)
    scores = model_scores(models, frame, feature_cols)
    branch_rows: list[dict[str, Any]] = []
    scoreboard_rows: list[dict[str, Any]] = []
    supply_rows: list[dict[str, Any]] = []
    manifest_rows: list[dict[str, Any]] = []
    model_rows: list[dict[str, Any]] = []
    wfo_rows: list[dict[str, Any]] = []
    artifacts: list[Path] = []
    for index, spec in enumerate(candidate_specs(), start=1):
        payload, identity, validation_metrics, oos_metrics = materialize_payload(spec, base, seed, frame, feature_cols, scores)
        branch_id = f"run307A_{spec.package_id.replace('_surface', '')}"
        payload_path = PAYLOAD_DIR / f"{branch_id}_payload.parquet"
        handoff_path = HANDOFF_DIR / f"{branch_id}_handoff.json"
        model_spec_path = MODEL_DIR / f"{branch_id}_ml_surface.json"
        prev.io_path(payload_path.parent).mkdir(parents=True, exist_ok=True)
        payload.to_parquet(prev.io_path(payload_path), index=False)
        write_json(model_spec_path, identity)
        write_json(
            handoff_path,
            {
                "stage307_branch_id": branch_id,
                "source_stage_id": SOURCE_STAGE_ID,
                "package_id": spec.package_id,
                "runtime_feature_order": list(RUNTIME_FEATURE_ORDER),
                "runtime_feature_order_hash": ordered_hash(RUNTIME_FEATURE_ORDER),
                "model_feature_order": list(feature_cols),
                "model_feature_order_hash": ordered_hash(feature_cols),
                "decision_surface": identity,
                "risk_logic": risk_manifest_fields(spec),
                "runtime_handoff": "precomputed route_signal_value replay for Stage307 MT5 probe",
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
            prev.s290.selection_score(validation_metrics)
            + prev.s290.selection_score(oos_metrics)
            + min(float(validation_metrics["net_bp"]), float(oos_metrics["net_bp"])) * 1.50
        )
        branch_rows.append(
            {
                "branch_id": branch_id,
                "package_id": spec.package_id,
                "source_stage_id": SOURCE_STAGE_ID,
                "source_run_id": SOURCE_RUN_ID,
                "hypothesis": spec.hypothesis,
                "decision_use": "Check whether a fresh ML return-rank surface can create a profit-scale ONNX-worthy seed.",
                "comparison_baseline": "Stage306 actual MT5 trade-shape failure with all candidates negative.",
                "control_variables": "US100 M5 split_v1; Stage306 feature base; Tier A/B paired runtime accounting; no Adapter or ONNX claim.",
                "changed_variables": spec.changed_variables,
                "sample_scope": "Tier A train fit, Tier A/Tier B validation/OOS signal replay; MT5 runtime is decisive.",
                "success_criteria": "MT5 validation/OOS positive, minimum trade count, 4-10 trades/day, profit scale, PF/recovery/expectancy, and no deep parsed curve pocket.",
                "failure_criteria": "Profit scale absent, OOS negative, density outside 4-10, or parsed curve pocket remains deep.",
                "invalid_conditions": "source payload missing, feature-label leakage, feature order mismatch, or MT5 report parse missing.",
                "stop_conditions": "candidate gate pass opens Adapter package; otherwise pivot to a non-return-rank source instead of repairing this stage.",
                "evidence_plan": "branch queue, proxy scoreboard, payload manifest, MT5 queue, run307B KPI, run307C parsed curve review.",
                "feature_surface": "Stage306 feature base plus hour/day cyclic features.",
                "model_surface": spec.model_key,
                "decision_surface": f"{spec.decision_surface};signal_policy={spec.signal_policy}",
                "risk_logic": json.dumps(risk_manifest_fields(spec), sort_keys=True),
                "adapter_path": "deferred_until_candidate_gate",
                "runtime_handoff": "route_signal_value replay now; ML feature order retained for Adapter trace if candidate gate passes.",
                "failure_memory_plan": "Record whether return-rank model family, density, session amplification, or risk scale failed.",
                "claim_boundary": BOUNDARY,
            }
        )
        manifest_rows.append(
            {
                "queue_id": f"run307A_queue_{index:02d}",
                "materialized_branch_id": branch_id,
                "stage307_branch_id": branch_id,
                "stage306_branch_id": seed.get("materialized_branch_id", ""),
                "stage305_branch_id": seed.get("stage305_branch_id", ""),
                "stage304_branch_id": seed.get("stage304_branch_id", ""),
                "stage303_branch_id": seed.get("stage303_branch_id", ""),
                "stage301_branch_id": seed.get("stage301_branch_id", ""),
                "stage293_branch_id": branch_id,
                "stage291_branch_id": branch_id,
                "stage290_branch_id": branch_id,
                "package_id": spec.package_id,
                "queue_role": "post_trade_shape_scale_ml_surface",
                "payload_path": rel(payload_path),
                "payload_hash": prev.sha256_file_lf_normalized(payload_path),
                "handoff_path": rel(handoff_path),
                "handoff_hash": prev.sha256_file_lf_normalized(handoff_path),
                "model_artifact_path": rel(model_spec_path),
                "model_artifact_hash": prev.sha256_file_lf_normalized(model_spec_path),
                "model_feature_order_path": rel(model_spec_path),
                "model_feature_order_hash": ordered_hash(feature_cols),
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
                "model_family": spec.model_key,
                "prediction_kind": "future_return_rank",
                "dataset_id": "fwd12_proxy58",
                "model_artifact_path": rel(model_spec_path),
                "model_artifact_hash": prev.sha256_file_lf_normalized(model_spec_path),
                "model_feature_order_path": rel(model_spec_path),
                "model_feature_order_hash": ordered_hash(feature_cols),
                "imputation_path": rel(model_spec_path),
                "imputation_hash": prev.sha256_file_lf_normalized(model_spec_path),
                "classes": "-1,0,1",
                "payoff_weight_policy": f"{spec.decision_surface};signal_policy={spec.signal_policy}",
                "onnx_exportability_note": "Adapter required before ONNX; model feature order and route_signal handoff are traceable.",
            }
        )
        scoreboard_rows.append(
            {
                "materialized_branch_id": branch_id,
                "package_id": spec.package_id,
                "dataset_id": "fwd12_proxy58",
                "model_family": spec.model_key,
                "prediction_kind": "future_return_rank",
                "mode": f"{spec.decision_surface};signal_policy={spec.signal_policy}",
                "quantile": "",
                "threshold": "",
                "precondition": f"{spec.decision_surface};signal_policy={spec.signal_policy}",
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
                    "mode": f"{spec.decision_surface};signal_policy={spec.signal_policy}",
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
    return branch_rows, scoreboard_rows, supply_rows, manifest_rows, model_rows, wfo_rows, artifacts, feature_cols


def result_rows(scoreboard_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    density_pass = sum(1 for row in scoreboard_rows if row["density_gate"] == "passed")
    edge_pass = sum(1 for row in scoreboard_rows if row["proxy_edge_gate"] == "passed")
    curve_pass = sum(1 for row in scoreboard_rows if row["curve_proxy_gate"] == "passed")
    result = [
        {
            "result_subject": "Stage307 post-trade-shape scale ML materialization",
            "evidence_available": f"candidate_rows={len(scoreboard_rows)};mt5_queue_rows={len(manifest_rows)};density_proxy_pass={density_pass};edge_proxy_pass={edge_pass};curve_proxy_pass={curve_pass}",
            "evidence_missing": "MT5 runtime KPI, Adapter package, ONNX parity",
            "judgment_label": "exploratory",
            "judgment_class": JUDGMENT,
            "claim_boundary": BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "Stage307 replaces Stage306 rule repair with fresh ML return-rank candidates; it does not select before MT5 evidence.",
        }
    ]
    gates = [
        {"gate_name": "fresh_thesis", "status": "passed", "evidence_path": rel(EXPERIMENT_DESIGN), "effect": "Stage306 trade-shape repair is replaced with fresh ML return-rank source."},
        {"gate_name": "source_lineage", "status": "passed", "evidence_path": rel(LINEAGE), "effect": "Each branch points back to Stage306 feature base and actual MT5 failure evidence."},
        {"gate_name": "proxy_density_edge_curve_screen", "status": "passed" if density_pass and edge_pass else "partial", "evidence_path": rel(MODEL_SCOREBOARD), "effect": "4-10 trades/day and proxy edge are screened before MT5."},
        {"gate_name": "mt5_runtime_probe", "status": "prepared", "evidence_path": rel(MT5_QUEUE), "effect": "run307B can execute Tier A, Tier B fallback, and actual routed total attempts."},
        {"gate_name": "adapter_package", "status": "not_started", "evidence_path": "", "effect": "No Adapter before candidate gate."},
        {"gate_name": "onnx_readiness", "status": "not_started", "evidence_path": "", "effect": "ONNX waits for Adapter and parity gates."},
    ]
    return result, gates


def report_markdown(scoreboard_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]]) -> str:
    ordered = sorted(scoreboard_rows, key=lambda row: float(row["selection_score"]), reverse=True)
    lines = [
        "# run307A Post-Trade-Shape Scale Materialization",
        "",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        "- selected_candidate(선택 후보): `none`",
        "- Adapter package(어댑터 패키지): `none`",
        "- ONNX readiness(온엑스 준비): `not_claimed`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "",
        "Effect(효과): Stage306(306단계)의 rule repair(규칙 수리)를 버리고 ML return-rank(머신러닝 수익 순위) 표면으로 새 수익 규모 후보를 만들었다.",
        "",
        "| package(패키지) | model(모델) | surface(표면) | val bp(검증 bp) | val/day(검증 일거래) | OOS bp(표본외 bp) | OOS/day(표본외 일거래) | density(밀도) | edge(우위) | curve(곡선) |",
        "|---|---|---|---:|---:|---:|---:|---|---|---|",
    ]
    for row in ordered:
        lines.append(
            "| {pkg} | {model} | {mode} | {vn:.1f} | {vtd:.2f} | {on:.1f} | {otd:.2f} | {den} | {edge} | {curve} |".format(
                pkg=row["package_id"],
                model=row["model_family"],
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
    feature_cols: Sequence[str],
    created_at: str,
) -> list[Path]:
    result, gates = result_rows(scoreboard_rows, manifest_rows)
    prev.write_csv_rows(BRANCH_QUEUE, BRANCH_COLUMNS, branch_rows)
    prev.write_csv_rows(MODEL_SCOREBOARD, prev.s293.SCOREBOARD_COLUMNS, scoreboard_rows)
    prev.write_csv_rows(CANDIDATE_SUPPLY, prev.s293.SUPPLY_COLUMNS, supply_rows)
    prev.write_csv_rows(PAYLOAD_MANIFEST, MANIFEST_COLUMNS, manifest_rows)
    prev.write_csv_rows(MT5_QUEUE, MANIFEST_COLUMNS, manifest_rows)
    prev.write_csv_rows(MODEL_MANIFEST, prev.MODEL_COLUMNS, model_rows)
    prev.write_csv_rows(WFO_FOLD_SCOREBOARD, prev.s293.WFO_COLUMNS, wfo_rows)
    prev.write_csv_rows(RESULT_JUDGMENT, prev.s293.RESULT_COLUMNS, result)
    prev.write_csv_rows(GATE_AUDIT, prev.s293.GATE_COLUMNS, gates)
    write_json(
        EXPERIMENT_DESIGN,
        {
            "hypothesis": "Fresh ML return-rank surfaces can create profit scale after Stage306 trade-shape failure.",
            "decision_use": "Open or reject MT5 runtime probe candidates before Adapter and ONNX work.",
            "comparison_baseline": "Stage306 actual MT5 negative trade-shape review.",
            "control_variables": ["US100 M5", "split_v1", "Stage306 feature base", "Tier A/B paired accounting"],
            "changed_variables": ["model family", "feature order", "decision surface", "density target", "hold horizon", "risk logic"],
            "sample_scope": "Tier A train fit with validation/OOS proxy and MT5 runtime probe.",
            "success_criteria": ["MT5 validation/OOS positive", "minimum trade count", "4-10 trades/day", "profit scale", "PF/recovery/expectancy acceptable", "no deep parsed curve pocket"],
            "failure_criteria": ["weak net scale", "density outside 4-10", "OOS negative", "deep curve pocket"],
            "invalid_conditions": ["source payload missing", "feature-label leakage", "runtime report parse missing"],
            "stop_conditions": ["candidate gate pass moves to Adapter package", "otherwise pivot away from return-rank ML source"],
            "evidence_plan": [rel(MODEL_SCOREBOARD), rel(PAYLOAD_MANIFEST), rel(MT5_QUEUE), "run307B MT5 KPI", "run307C parsed curve review"],
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            "source_manifest": rel(SOURCE_MANIFEST),
            "source_scoreboard": rel(SOURCE_SCOREBOARD),
            "source_trade_quality": rel(SOURCE_TRADE_QUALITY),
            "source_session_attribution": rel(SOURCE_SESSION),
            "source_monthly_attribution": rel(SOURCE_MONTHLY),
            "source_seed_queue": rel(SOURCE_SEED_QUEUE),
            "feature_count": len(feature_cols),
            "model_feature_order_hash": ordered_hash(feature_cols),
            "payload_future_label_columns_removed": True,
            "runtime_feature_order_hash": ordered_hash(RUNTIME_FEATURE_ORDER),
            "claim_boundary": BOUNDARY,
        },
    )
    artifacts = [
        BRANCH_QUEUE,
        MODEL_SCOREBOARD,
        CANDIDATE_SUPPLY,
        PAYLOAD_MANIFEST,
        MT5_QUEUE,
        MODEL_MANIFEST,
        WFO_FOLD_SCOREBOARD,
        EXPERIMENT_DESIGN,
        DATA_RECEIPT,
        RESULT_JUDGMENT,
        GATE_AUDIT,
        RUN_MANIFEST,
        LINEAGE,
        REPORT,
        *payload_artifacts,
    ]
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
            "artifacts": [rel(path) for path in artifacts if path != RUN_MANIFEST and prev.path_exists(path)],
            "created_at_utc": created_at,
            "claim_boundary": BOUNDARY,
        },
    )
    write_json(
        LINEAGE,
        {
            "run_id": RUN_ID,
            "producer": "stage_pipelines/stage307/design_post_trade_shape_scale_rebuild.py",
            "source_inputs": [rel(SOURCE_REVIEW), rel(SOURCE_MANIFEST), rel(SOURCE_SCOREBOARD), rel(SOURCE_TRADE_QUALITY), rel(SOURCE_SESSION), rel(SOURCE_MONTHLY), rel(SOURCE_SEED_QUEUE)],
            "consumer": "run307B_execute_post_trade_shape_scale_mt5_probe",
            "artifact_paths": {"scoreboard": rel(MODEL_SCOREBOARD), "mt5_queue": rel(MT5_QUEUE), "report": rel(REPORT)},
            "artifact_hashes": {"model_feature_order_hash": ordered_hash(feature_cols), "runtime_feature_order_hash": ordered_hash(RUNTIME_FEATURE_ORDER)},
            "availability": "tracked_manifest_plus_reproducible_payloads",
            "lineage_judgment": "connected_with_boundary",
            "claim_boundary": BOUNDARY,
            "created_at_utc": created_at,
        },
    )
    write_md(REPORT, report_markdown(scoreboard_rows, manifest_rows))
    return artifacts


def update_docs(created_at: str, artifacts: Sequence[Path], manifest_rows: Sequence[Mapping[str, Any]], scoreboard_rows: Sequence[Mapping[str, Any]]) -> None:
    safe_upsert_csv_rows(
        RUN_REGISTRY,
        prev.RUN_REGISTRY_COLUMNS,
        [{"run_id": RUN_ID, "stage_id": STAGE_ID, "lane": "post_trade_shape_scale_materialization", "status": STATUS, "judgment": JUDGMENT, "path": rel(REPORT), "notes": f"branches={len(scoreboard_rows)};mt5_queue_rows={len(manifest_rows)};next_action={NEXT_ACTION}"}],
        key="run_id",
    )
    safe_upsert_csv_rows(
        ALPHA_LEDGER,
        prev.ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "post_trade_shape_scale_materialization",
                "tier_scope": "Tier A/Tier B paired exploration labels",
                "kpi_scope": "proxy_runtime_handoff_readiness",
                "scoreboard_lane": "post_trade_shape_scale_ml",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "primary_kpi": f"mt5_queue_rows={len(manifest_rows)};proxy_rows={len(scoreboard_rows)}",
                "guardrail_kpi": "selected_candidate=none;adapter_package=none;onnx_readiness=not_claimed",
                "external_verification_status": "out_of_scope_by_claim_materialization_only",
                "notes": f"next_action={NEXT_ACTION}.",
            }
        ],
        key="ledger_row_id",
    )
    safe_upsert_csv_rows(
        STAGE_LEDGER,
        prev.s293.STAGE_LEDGER_COLUMNS,
        [{"row_id": f"{RUN_ID}__materialization", "stage_id": STAGE_ID, "run_id": RUN_ID, "view": "post_trade_shape_scale_materialization", "tier_scope": "Tier A/Tier B paired exploration labels", "scoreboard": "model_scout_scoreboard", "status": STATUS, "judgment": JUDGMENT, "evidence_boundary": "materialization_no_candidate_no_onnx", "report_path": rel(REPORT), "notes": f"mt5_queue_rows={len(manifest_rows)};next_action={NEXT_ACTION}"}],
        key="row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{hashlib.sha1(rel(path).encode('utf-8')).hexdigest()[:12]}",
            "artifact_type": "stage307_post_trade_shape_scale_artifact",
            "path": rel(path),
            "sha256": prev.sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run307A post-trade-shape scale materialization",
        }
        for path in artifacts
        if prev.path_exists(path)
    ]
    safe_upsert_csv_rows(ARTIFACT_REGISTRY, prev.s293.ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")
    selected = read_text(SELECTED)
    selected = replace_line_prefix(selected, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
    selected = replace_line_prefix(selected, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = append_once(selected, "run307A_report", f"- run307A_report(307A 보고서): `{rel(REPORT)}`\n- run307A_mt5_queue(307A MT5 대기열): `{rel(MT5_QUEUE)}`")
    write_md(SELECTED, selected)
    review_index = read_text(REVIEW_INDEX) or "# Stage307 Review Index(307단계 검토 색인)\n"
    review_index = append_once(review_index, "run307A_report", f"- run307A_report(307A 보고서): `{rel(REPORT)}`\n- run307A_mt5_queue(307A MT5 대기열): `{rel(MT5_QUEUE)}`")
    write_md(REVIEW_INDEX, review_index)
    idea_text = read_text(IDEA_REGISTER)
    idea_text = append_once(
        idea_text,
        "stage307_post_trade_shape_scale_ml",
        "## stage307_post_trade_shape_scale_ml\n\n- hypothesis(가설): fresh ML return-rank(새 머신러닝 수익 순위) surface(표면)가 Stage306(306단계) rule repair(규칙 수리)보다 큰 profit scale(수익 규모)을 만들 수 있다.\n- boundary(경계): exploratory(탐색), no selected candidate(선택 후보 없음), no Adapter(어댑터 없음), no ONNX(온엑스 없음).\n",
    )
    write_md(IDEA_REGISTER, idea_text)
    current = read_text(CURRENT_STATE)
    current = replace_line_prefix(current, "- current_packet(", f"- current_packet(현재 작업 묶음): `{STAGE_ID}_v1`")
    current = replace_line_prefix(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- active_stage(", f"- active_stage(활성 단계): `{STAGE_ID}`")
    current = replace_line_prefix(current, "- source_stage(", f"- source_stage(원천 단계): `{SOURCE_STAGE_ID}`")
    current = replace_line_prefix(current, "- status(", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run307A_summary",
        f"- run307A_summary(307A 요약): post-trade-shape scale ML(거래 형태 이후 수익 규모 머신러닝) 후보 `{len(scoreboard_rows)}`개를 materialized(물질화)했다. Effect(효과): 새 model surface(모델 표면)로 MT5 queue(MT5 대기열) `{len(manifest_rows)}`개를 만들었으며 선택 후보/Adapter(어댑터)/ONNX(온엑스)는 주장하지 않는다.",
    )
    write_md(CURRENT_STATE, current)
    workspace = read_text(WORKSPACE_STATE)
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE_ID}")
    workspace = replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = (
        f"- >-\n"
        f"  Stage307(307단계) run307A(307A 실행) post-trade-shape scale ML materialization(거래 형태 이후 수익 규모 머신러닝 물질화) `{RUN_ID}`. "
        f"Effect(효과): branch(분기) `{len(scoreboard_rows)}`개와 MT5 probe queue(MT5 탐침 대기열) `{len(manifest_rows)}`개를 만들었고 selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비)는 주장하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_md(WORKSPACE_STATE, workspace)
    changelog = read_text(CHANGELOG) or "# Changelog(변경 기록)\n"
    changelog = append_once(
        changelog,
        RUN_ID,
        f"## {UPDATED_ON} run307A Post-trade-shape scale ML materialization(307A 거래 형태 이후 수익 규모 머신러닝 물질화)\n\n"
        f"- status(상태): `{STATUS}`\n"
        f"- judgment(판정): `{JUDGMENT}`\n"
        f"- effect(효과): candidate payload(후보 페이로드) `{len(manifest_rows)}`개와 MT5 queue(MT5 대기열)를 만들었다.\n"
        f"- boundary(경계): selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비)는 아직 없다.\n",
    )
    write_md(CHANGELOG, changelog)


def main() -> None:
    created_at = utc_now()
    branch_rows, scoreboard_rows, supply_rows, manifest_rows, model_rows, wfo_rows, payload_artifacts, feature_cols = build_outputs()
    artifacts = write_outputs(branch_rows, scoreboard_rows, supply_rows, manifest_rows, model_rows, wfo_rows, payload_artifacts, feature_cols, created_at)
    update_docs(created_at, artifacts, manifest_rows, scoreboard_rows)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "branch_count": len(scoreboard_rows),
                "mt5_queue_rows": len(manifest_rows),
                "model_feature_count": len(feature_cols),
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
