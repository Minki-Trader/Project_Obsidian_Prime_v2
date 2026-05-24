from __future__ import annotations

import csv
import hashlib
import json
import sys
import warnings
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesRegressor, HistGradientBoostingClassifier, HistGradientBoostingRegressor


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import (  # noqa: E402
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
    write_csv_rows,
)
from foundation.models.onnx_bridge import ordered_hash  # noqa: E402
from stage_pipelines.stage290 import design_materialize_payoff_weighted_edge_model_rebuild as s290  # noqa: E402


STAGE_ID = "293_onnx_candidate_campaign__profit_scale_density_calibration_rebuild"
RUN_ID = "run293A_design_profit_scale_density_calibration_rebuild_v1"
RUN_NUMBER = "run293A"
SOURCE_RUN_ID = "run292C_review_anti_direction_meta_label_trade_simulator_mt5_probe_v1"
STATUS = "completed_profit_scale_density_calibration_candidates_materialized_no_selection"
JUDGMENT = "profit_scale_density_calibration_inputs_materialized_no_candidate_selection"
NEXT_ACTION = "run293B_execute_profit_scale_density_calibration_mt5_probe"
UPDATED_ON = "2026-05-24"
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
MODEL_DIR = RUN_ROOT / "models"
HANDOFF_DIR = RUN_ROOT / "handoff"

STAGE292 = ROOT / "stages" / "292_onnx_candidate_campaign__anti_direction_meta_label_trade_simulator_rebuild"
STAGE293_SEED_QUEUE = STAGE_ROOT / "01_inputs" / "stage293_seed_queue.csv"
SOURCE_SCOREBOARD = STAGE292 / "02_runs" / "run292C" / "anti_direction_meta_trade_sim_review_scoreboard.csv"
SOURCE_FAILURE = STAGE292 / "02_runs" / "run292C" / "failure_memory.csv"

BRANCH_QUEUE = RUN_ROOT / "branch_design_queue.csv"
MODEL_SCOREBOARD = RUN_ROOT / "model_scout_scoreboard.csv"
CANDIDATE_SUPPLY = RUN_ROOT / "candidate_supply_diagnostics.csv"
PAYLOAD_MANIFEST = RUN_ROOT / "candidate_payload_manifest.csv"
MT5_QUEUE = RUN_ROOT / "mt5_probe_queue.csv"
MODEL_MANIFEST = RUN_ROOT / "model_artifact_manifest.csv"
WFO_FOLD_SCOREBOARD = RUN_ROOT / "wfo_fold_scoreboard.csv"
EXPERIMENT_DESIGN = RUN_ROOT / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_ROOT / "data_integrity_receipt.json"
LINEAGE = RUN_ROOT / "artifact_lineage_receipt.json"
RESULT_JUDGMENT = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT = RUN_ROOT / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
REPORT = REVIEWS / "run293A_profit_scale_density_calibration_materialization_report.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

LABEL_ORDER = (0, 1, 2)


@dataclass(frozen=True)
class CandidateSpec:
    package_id: str
    model_family: str
    prediction_kind: str
    dataset_id: str
    max_hold_bars: int
    precondition: str
    sample_weight_policy: str
    objective_surface: str
    hypothesis: str
    changed_variables: str
    target_density: float
    modes: tuple[str, ...]


@dataclass
class PreparedModel:
    spec: CandidateSpec
    model: Any
    feature_order: list[str]
    medians: dict[str, float]
    payoff_units: dict[str, float]
    model_path: Path | None = None
    feature_order_path: Path | None = None
    imputation_path: Path | None = None


BRANCH_COLUMNS = (
    "stage293_branch_id",
    "materialized_branch_id",
    "package_id",
    "idea_id",
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
    "model_family",
    "dataset_id",
    "prediction_kind",
    "objective_surface",
    "selection_mode",
    "selection_quantile",
    "selection_threshold",
    "precondition",
    "risk_logic",
    "adapter_path",
    "runtime_handoff",
    "claim_boundary",
)
SCOREBOARD_COLUMNS = (
    "materialized_branch_id",
    "package_id",
    "dataset_id",
    "model_family",
    "prediction_kind",
    "mode",
    "quantile",
    "threshold",
    "precondition",
    "wfo_net_bp",
    "wfo_positive_fold_share",
    "wfo_worst_fold_net_bp",
    "wfo_mean_trades_per_day",
    "wfo_min_trades_per_day",
    "wfo_max_trades_per_day",
    "validation_proxy_net_bp",
    "validation_proxy_pf",
    "validation_proxy_trade_count",
    "validation_proxy_trades_per_day",
    "validation_proxy_recovery",
    "validation_proxy_worst_month_bp",
    "validation_proxy_worst_rolling_20_bp",
    "validation_proxy_worst_rolling_50_bp",
    "validation_proxy_positive_month_share",
    "validation_proxy_underwater_ratio",
    "oos_proxy_net_bp",
    "oos_proxy_pf",
    "oos_proxy_trade_count",
    "oos_proxy_trades_per_day",
    "oos_proxy_recovery",
    "oos_proxy_worst_month_bp",
    "oos_proxy_worst_rolling_20_bp",
    "oos_proxy_worst_rolling_50_bp",
    "oos_proxy_positive_month_share",
    "oos_proxy_underwater_ratio",
    "density_gate",
    "proxy_edge_gate",
    "curve_proxy_gate",
    "selection_score",
    "selected_candidate",
    "adapter_package",
    "onnx_readiness",
    "claim_boundary",
)
SUPPLY_COLUMNS = (
    "materialized_branch_id",
    "package_id",
    "tier_scope",
    "split",
    "days",
    "rows",
    "active_signal_count",
    "active_signals_per_day",
    "long_signal_count",
    "short_signal_count",
    "max_hold_bars",
    "approx_trade_count",
    "approx_trades_per_day",
    "trade_density_screen",
)
MANIFEST_COLUMNS = (
    "queue_id",
    "materialized_branch_id",
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
    "approx_validation_trades_per_day",
    "approx_oos_trades_per_day",
    "selected_candidate",
    "adapter_package",
    "onnx_readiness",
    "claim_boundary",
)
MODEL_COLUMNS = (
    "materialized_branch_id",
    "package_id",
    "model_family",
    "prediction_kind",
    "dataset_id",
    "model_artifact_path",
    "model_artifact_hash",
    "model_feature_order_path",
    "model_feature_order_hash",
    "imputation_path",
    "imputation_hash",
    "classes",
    "payoff_weight_policy",
    "onnx_exportability_note",
)
WFO_COLUMNS = (
    "materialized_branch_id",
    "package_id",
    "fold_id",
    "mode",
    "quantile",
    "threshold",
    "net_bp",
    "pf",
    "trade_count",
    "trades_per_day",
    "recovery",
    "worst_month_bp",
    "worst_rolling_20_bp",
    "worst_rolling_50_bp",
    "positive_month_share",
    "underwater_ratio",
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


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(str(path))
    try:
        return item.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    write_csv_rows(path, columns, rows)


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def upsert_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], key: str) -> None:
    upsert_csv_rows(path, columns, rows, key=key)


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


def candidate_specs() -> list[CandidateSpec]:
    return [
        CandidateSpec(
            package_id="cp293A_runtime_calibrated_histgb_hold5_surface",
            model_family="histgb_return_runtime_calibrated",
            prediction_kind="return_regression",
            dataset_id="fwd12_proxy58",
            max_hold_bars=5,
            precondition="runtime_gap_balanced",
            sample_weight_policy="abs_forward_return_x_recency_x_runtime_gap",
            objective_surface="runtime_aware_trade_simulator_calibration",
            hypothesis="runtime-aware simulator calibration(런타임 인식 시뮬레이터 보정)이 Stage292(292단계)의 proxy-positive/runtime-negative gap(대리 양수/런타임 음수 공백)을 줄일 수 있다.",
            changed_variables="runtime calibration score, inverse/direct routing blend, hold5",
            target_density=7.0,
            modes=("runtime_calibrated_inverse", "density_profit_scale_router"),
        ),
        CandidateSpec(
            package_id="cp293B_profit_scale_lgbm_hold7_surface",
            model_family="lightgbm_return_profit_scale",
            prediction_kind="return_regression",
            dataset_id="fwd18_proxy58",
            max_hold_bars=7,
            precondition="cash_midvol_profit",
            sample_weight_policy="abs_forward_return_x_recency_x_tail",
            objective_surface="profit_scale_density_router",
            hypothesis="profit-scale router(순수익 규모 라우터)가 적은 순수익을 버리고, 일 4-10거래 안에서 더 큰 net profit(순수익)을 직접 노린다.",
            changed_variables="profit-scale activation, direct/inverse asymmetry, hold7",
            target_density=6.5,
            modes=("profit_scale_direct", "profit_scale_inverse", "quality_veto_direct"),
        ),
        CandidateSpec(
            package_id="cp293C_smooth_curve_extratrees_hold4_surface",
            model_family="extratrees_return_smooth_curve",
            prediction_kind="return_regression",
            dataset_id="fwd12_proxy58",
            max_hold_bars=4,
            precondition="smooth_session_balance",
            sample_weight_policy="abs_forward_return_x_side_balance",
            objective_surface="smooth_curve_objective",
            hypothesis="smooth curve objective(매끈한 곡선 목적함수)가 확대 구간의 deep pocket(깊은 포켓)을 직접 벌점화해 안정적인 우상향 후보만 남긴다.",
            changed_variables="smooth-curve activation, session-balance precondition, hold4",
            target_density=6.0,
            modes=("smooth_curve_router", "conditional_inverse"),
        ),
        CandidateSpec(
            package_id="cp293D_density_band_xgb_hold6_surface",
            model_family="xgboost_return_density_band",
            prediction_kind="return_regression",
            dataset_id="fwd12_proxy58",
            max_hold_bars=6,
            precondition="dense_band",
            sample_weight_policy="abs_forward_return_x_recency",
            objective_surface="density_band_profit_router",
            hypothesis="density band router(밀도 대역 라우터)가 cp292C(292C 후보)의 거래수 장점을 유지하면서 validation loss(검증 손실)를 줄일 수 있다.",
            changed_variables="density-band activation, target 4-10 trades/day, hold6",
            target_density=8.0,
            modes=("density_profit_scale_router", "direct"),
        ),
        CandidateSpec(
            package_id="cp293E_hybrid_meta_lgbm_hold8_surface",
            model_family="lightgbm_multiclass_hybrid_meta",
            prediction_kind="multiclass_probability",
            dataset_id="fwd18_proxy58",
            max_hold_bars=8,
            precondition="runtime_gap_balanced",
            sample_weight_policy="abs_forward_return_x_class_balance_x_recency_x_runtime_gap",
            objective_surface="hybrid_meta_runtime_calibration",
            hypothesis="hybrid meta router(혼합 메타 라우터)가 class probability(분류 확률)와 runtime calibration(런타임 보정)을 결합해 과소/과대 거래를 동시에 줄인다.",
            changed_variables="multiclass model, runtime-calibrated inverse, smooth router, hold8",
            target_density=5.5,
            modes=("runtime_calibrated_inverse", "smooth_curve_router"),
        ),
        CandidateSpec(
            package_id="cp293F_asymmetric_tail_control_xgb_hold5_surface",
            model_family="xgboost_multiclass_tail_control",
            prediction_kind="multiclass_probability",
            dataset_id="fwd12_proxy58",
            max_hold_bars=5,
            precondition="controlled_tail",
            sample_weight_policy="abs_forward_return_x_class_balance_x_recency_x_tail",
            objective_surface="asymmetric_tail_control",
            hypothesis="asymmetric tail control(비대칭 꼬리 제어)이 공격형 upside(상방)를 허용하되, 저밀도 고PF 착시를 최소 거래수 게이트로 막는다.",
            changed_variables="tail-control classifier, profit-scale inverse, density router, hold5",
            target_density=6.0,
            modes=("profit_scale_inverse", "density_profit_scale_router"),
        ),
    ]


def col(frame: pd.DataFrame, name: str, default: float = 0.0) -> pd.Series:
    if name in frame.columns:
        return pd.to_numeric(frame[name], errors="coerce").fillna(default)
    return pd.Series(default, index=frame.index, dtype="float64")


def precondition_mask(frame: pd.DataFrame, name: str) -> np.ndarray:
    rows = len(frame)
    if name == "all_rows":
        return np.ones(rows, dtype=bool)
    cash = col(frame, "is_us_cash_open", 0).to_numpy() > 0.5
    zabs = col(frame, "return_zscore_20", 0).abs().to_numpy()
    vol = col(frame, "historical_vol_5_over_20", 1).to_numpy()
    minutes = col(frame, "minutes_from_cash_open", 0).to_numpy()
    hour = pd.to_datetime(frame["timestamp"], utc=True).dt.hour.to_numpy()
    if name == "cash_non_extreme":
        return cash & (zabs <= 1.80) & (vol <= 1.80)
    if name == "volatility_balanced_loose":
        return (vol >= 0.45) & (vol <= 1.95) & (zabs <= 2.20)
    if name == "us_cash_edge":
        return cash & (minutes >= 20) & (minutes <= 360) & (zabs <= 2.10)
    if name == "not_extreme_midvol":
        return (zabs <= 1.95) & (vol >= 0.55) & (vol <= 1.75)
    if name == "late_or_reversal_window":
        return ((cash & (minutes >= 180)) | (hour >= 18)) & (zabs >= 0.35) & (zabs <= 2.40)
    if name == "runtime_gap_balanced":
        return (vol >= 0.50) & (vol <= 1.85) & (zabs >= 0.25) & (zabs <= 2.05) & (hour >= 7) & (hour <= 22)
    if name == "cash_midvol_profit":
        return cash & (minutes >= 15) & (minutes <= 430) & (vol >= 0.55) & (vol <= 1.70) & (zabs <= 1.90)
    if name == "smooth_session_balance":
        return (hour >= 8) & (hour <= 21) & (vol >= 0.45) & (vol <= 1.65) & (zabs <= 1.75)
    if name == "dense_band":
        return (vol >= 0.38) & (vol <= 2.05) & (zabs >= 0.15) & (zabs <= 2.20)
    if name == "controlled_tail":
        return ((cash & (minutes >= 90)) | (hour >= 17)) & (zabs >= 0.45) & (zabs <= 2.15) & (vol <= 1.95)
    return np.ones(rows, dtype=bool)


def sample_weights(train: pd.DataFrame, spec: CandidateSpec) -> np.ndarray:
    returns = train["future_log_return_12"].astype(float).to_numpy()
    scale = float(np.nanmedian(np.abs(returns)))
    if not np.isfinite(scale) or scale <= 0.0:
        scale = 0.001
    magnitude = np.clip(np.abs(returns) / scale, 0.25, 7.5)
    if "tail" in spec.sample_weight_policy:
        magnitude = np.power(magnitude, 1.28)
    weights = 1.0 + magnitude
    if spec.prediction_kind == "multiclass_probability":
        weights *= s290.class_balance_weights(train["label_class"].astype(int).to_numpy())
    if "side_balance" in spec.sample_weight_policy:
        signs = np.sign(returns).astype(int)
        total = float(len(signs))
        counts = {side: max(1, int((signs == side).sum())) for side in (-1, 0, 1)}
        weights *= np.asarray([total / (3.0 * counts[int(side)]) for side in signs], dtype="float64")
    if "runtime_gap" in spec.sample_weight_policy:
        zabs = col(train, "return_zscore_20", 0).abs().to_numpy()
        vol = col(train, "historical_vol_5_over_20", 1).to_numpy()
        cash = (col(train, "is_us_cash_open", 0).to_numpy() > 0.5).astype("float64")
        gap_weight = np.clip(1.0 + 0.16 * cash + 0.10 * (zabs >= 0.45) - 0.22 * (vol > 1.90), 0.55, 1.35)
        weights *= gap_weight
    if "recency" in spec.sample_weight_policy:
        weights *= np.linspace(0.78, 1.28, len(weights), dtype="float64")
    return weights.astype("float64")


def make_model(spec: CandidateSpec, seed: int) -> Any:
    if spec.model_family.startswith("xgboost_multiclass"):
        from xgboost import XGBClassifier

        return XGBClassifier(
            n_estimators=260,
            max_depth=3,
            learning_rate=0.035,
            subsample=0.84,
            colsample_bytree=0.80,
            objective="multi:softprob",
            eval_metric="mlogloss",
            num_class=3,
            tree_method="hist",
            random_state=seed,
            n_jobs=-1,
            verbosity=0,
        )
    if spec.model_family.startswith("lightgbm_multiclass"):
        from lightgbm import LGBMClassifier

        return LGBMClassifier(
            objective="multiclass",
            num_class=3,
            n_estimators=300,
            learning_rate=0.032,
            max_depth=4,
            num_leaves=20,
            min_child_samples=72,
            subsample=0.84,
            colsample_bytree=0.78,
            random_state=seed,
            n_jobs=-1,
            verbose=-1,
        )
    if spec.model_family.startswith("xgboost_return"):
        from xgboost import XGBRegressor

        return XGBRegressor(
            n_estimators=280,
            max_depth=3,
            learning_rate=0.032,
            subsample=0.84,
            colsample_bytree=0.80,
            objective="reg:squarederror",
            tree_method="hist",
            random_state=seed,
            n_jobs=-1,
            verbosity=0,
        )
    if spec.model_family.startswith("lightgbm_return"):
        from lightgbm import LGBMRegressor

        return LGBMRegressor(
            objective="regression",
            n_estimators=300,
            learning_rate=0.030,
            max_depth=4,
            num_leaves=20,
            min_child_samples=72,
            subsample=0.84,
            colsample_bytree=0.78,
            random_state=seed,
            n_jobs=-1,
            verbose=-1,
        )
    if spec.model_family.startswith("extratrees_return"):
        return ExtraTreesRegressor(
            n_estimators=520,
            max_features=0.55,
            min_samples_leaf=20,
            random_state=seed,
            n_jobs=-1,
        )
    if spec.model_family.startswith("histgb_return"):
        return HistGradientBoostingRegressor(
            max_iter=220,
            learning_rate=0.038,
            max_leaf_nodes=20,
            l2_regularization=0.10,
            min_samples_leaf=55,
            random_state=seed,
        )
    return HistGradientBoostingClassifier(
        max_iter=220,
        learning_rate=0.038,
        max_leaf_nodes=20,
        l2_regularization=0.10,
        min_samples_leaf=55,
        random_state=seed,
    )


def train_prepared(spec: CandidateSpec, train: pd.DataFrame, *, seed: int, persist: bool) -> PreparedModel:
    features = s290.feature_columns(train)
    x_train, medians = s290.matrix(train, features)
    if spec.prediction_kind == "multiclass_probability":
        y_train = train["label_class"].astype(int).to_numpy()
    else:
        y_train = train["future_log_return_12"].astype(float).to_numpy()
    weights = sample_weights(train, spec)
    model = make_model(spec, seed)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        model.fit(x_train, y_train, sample_weight=weights)
    prepared = PreparedModel(spec=spec, model=model, feature_order=features, medians=medians, payoff_units=s290.payoff_units(train))
    if persist:
        model_path = MODEL_DIR / f"{spec.package_id}.joblib"
        feature_order_path = MODEL_DIR / f"{spec.package_id}_feature_order.txt"
        imputation_path = MODEL_DIR / f"{spec.package_id}_imputation.json"
        io_path(MODEL_DIR).mkdir(parents=True, exist_ok=True)
        joblib.dump(model, io_path(model_path))
        io_path(feature_order_path).write_text("\n".join(features) + "\n", encoding="utf-8")
        write_json(imputation_path, {"feature_order": features, "medians": medians})
        prepared.model_path = model_path
        prepared.feature_order_path = feature_order_path
        prepared.imputation_path = imputation_path
    return prepared


def score_edges(prepared: PreparedModel, frame: pd.DataFrame) -> pd.DataFrame:
    x_values, _ = s290.matrix(frame, prepared.feature_order, prepared.medians)
    out = frame.copy()
    if prepared.spec.prediction_kind == "multiclass_probability":
        proba = s290.ordered_probabilities(prepared.model, x_values)
        units = prepared.payoff_units
        edge = proba[:, 2] * units["long_unit"] - proba[:, 0] * units["short_unit"] - proba[:, 1] * units["flat_penalty"] * 0.18
        out["prob_short"] = proba[:, 0]
        out["prob_flat"] = proba[:, 1]
        out["prob_long"] = proba[:, 2]
    else:
        edge = np.asarray(prepared.model.predict(x_values), dtype="float64")
        out["prob_short"] = np.nan
        out["prob_flat"] = np.nan
        out["prob_long"] = np.nan
    confidence = np.abs(edge)
    zabs = col(out, "return_zscore_20", 0).abs().to_numpy()
    vol = col(out, "historical_vol_5_over_20", 1).to_numpy()
    cash = (col(out, "is_us_cash_open", 0).to_numpy() > 0.5).astype("float64")
    minutes = col(out, "minutes_from_cash_open", 0).to_numpy()
    hour = pd.to_datetime(out["timestamp"], utc=True).dt.hour.to_numpy()
    late = ((minutes >= 210) | (hour >= 18)).astype("float64")
    anti_boost = 1.0 + 0.20 * (zabs >= 0.65) + 0.18 * (vol >= 1.05) + 0.12 * late + 0.08 * cash
    risk_penalty = 0.42 * (zabs > 2.15) + 0.34 * (vol > 2.00) + 0.10 * (cash < 0.5)
    quality_multiplier = np.clip(1.18 - risk_penalty + 0.08 * cash, 0.10, 1.35)
    density_multiplier = np.clip(1.00 + 0.12 * cash + 0.08 * late - 0.18 * (zabs > 2.30), 0.20, 1.30)
    runtime_gap_multiplier = np.clip(
        1.0 + 0.18 * cash + 0.12 * ((zabs >= 0.45) & (zabs <= 1.75)) - 0.30 * (vol > 1.85) - 0.18 * (hour < 7),
        0.15,
        1.42,
    )
    profit_scale_multiplier = np.clip(1.0 + 0.20 * cash + 0.14 * (vol <= 1.35) + 0.10 * (zabs >= 0.35) - 0.34 * (zabs > 2.0), 0.10, 1.45)
    smooth_multiplier = np.clip(1.12 + 0.12 * cash - 0.28 * (zabs > 1.65) - 0.24 * (vol > 1.70) - 0.14 * late, 0.10, 1.30)
    out["payoff_edge_score"] = edge
    out["payoff_edge_confidence"] = confidence
    out["payoff_edge_direction"] = np.where(edge >= 0.0, 1, -1).astype("int8")
    out["anti_meta_score"] = confidence * anti_boost
    out["profit_quality_score"] = confidence * quality_multiplier
    out["density_head_score"] = confidence * density_multiplier
    out["runtime_calibration_score"] = confidence * runtime_gap_multiplier
    out["profit_scale_score"] = confidence * profit_scale_multiplier
    out["smooth_curve_score"] = confidence * smooth_multiplier
    out["anti_regime_flag"] = ((zabs >= 0.65) & (zabs <= 2.25) & (vol <= 2.05)).astype("int8")
    out["smooth_regime_flag"] = ((zabs <= 1.75) & (vol <= 1.70) & (hour >= 8) & (hour <= 21)).astype("int8")
    out["precondition_pass"] = precondition_mask(out, prepared.spec.precondition).astype("int8")
    return out


def activation_score(scored: pd.DataFrame, mode: str) -> np.ndarray:
    if mode == "runtime_calibrated_inverse":
        return scored["runtime_calibration_score"].astype(float).to_numpy()
    if mode in {"profit_scale_direct", "profit_scale_inverse"}:
        return scored["profit_scale_score"].astype(float).to_numpy()
    if mode == "density_profit_scale_router":
        density = scored["density_head_score"].astype(float).to_numpy()
        scale = scored["profit_scale_score"].astype(float).to_numpy()
        return np.sqrt(np.maximum(density, 0.0) * np.maximum(scale, 0.0))
    if mode == "smooth_curve_router":
        return scored["smooth_curve_score"].astype(float).to_numpy()
    if mode in {"conditional_inverse", "quality_veto_inverse"}:
        return scored["anti_meta_score"].astype(float).to_numpy()
    if mode in {"quality_veto_direct"}:
        return scored["profit_quality_score"].astype(float).to_numpy()
    if mode == "two_head_router":
        density = scored["density_head_score"].astype(float).to_numpy()
        quality = scored["profit_quality_score"].astype(float).to_numpy()
        return np.sqrt(np.maximum(density, 0.0) * np.maximum(quality, 0.0))
    return scored["payoff_edge_confidence"].astype(float).to_numpy()


def threshold_for_quantile(scored: pd.DataFrame, quantile: float, mode: str) -> float:
    mask = scored["precondition_pass"].astype(bool).to_numpy()
    values = activation_score(scored, mode)[mask]
    values = values[np.isfinite(values)]
    if len(values) == 0:
        return 0.0
    return float(np.quantile(values, min(max(float(quantile), 0.0), 0.995)))


def build_signal(scored: pd.DataFrame, threshold: float, mode: str) -> np.ndarray:
    base_direction = scored["payoff_edge_direction"].astype("int8").to_numpy()
    active = (activation_score(scored, mode) >= float(threshold)) & scored["precondition_pass"].astype(bool).to_numpy()
    if mode == "direct":
        direction = base_direction
    elif mode == "profit_scale_direct":
        direction = base_direction
        scale = scored["profit_scale_score"].astype(float).to_numpy()
        scale_values = scale[scored["precondition_pass"].astype(bool).to_numpy()]
        scale_cut = float(np.quantile(scale_values[np.isfinite(scale_values)], 0.30)) if len(scale_values) else 0.0
        active = active & (scale >= scale_cut)
    elif mode == "profit_scale_inverse":
        direction = (-base_direction).astype("int8")
        anti = scored["anti_regime_flag"].astype(bool).to_numpy()
        active = active & anti
    elif mode == "runtime_calibrated_inverse":
        anti = scored["anti_regime_flag"].astype(bool).to_numpy()
        smooth = scored["smooth_regime_flag"].astype(bool).to_numpy()
        direction = np.where(anti, -base_direction, base_direction).astype("int8")
        active = active & (anti | smooth)
    elif mode == "density_profit_scale_router":
        density = scored["density_head_score"].astype(float).to_numpy()
        scale = scored["profit_scale_score"].astype(float).to_numpy()
        anti = scored["anti_meta_score"].astype(float).to_numpy() > scale * 1.05
        direction = np.where(anti, -base_direction, base_direction).astype("int8")
        scale_values = scale[scored["precondition_pass"].astype(bool).to_numpy()]
        scale_cut = float(np.quantile(scale_values[np.isfinite(scale_values)], 0.25)) if len(scale_values) else 0.0
        active = active & (scale >= scale_cut) & (density > 0.0)
    elif mode == "smooth_curve_router":
        anti = scored["anti_regime_flag"].astype(bool).to_numpy()
        smooth = scored["smooth_regime_flag"].astype(bool).to_numpy()
        direction = np.where(anti & ~smooth, -base_direction, base_direction).astype("int8")
        active = active & smooth
    elif mode in {"inverse", "quality_veto_inverse"}:
        direction = (-base_direction).astype("int8")
    elif mode == "quality_veto_direct":
        direction = base_direction
    elif mode == "conditional_inverse":
        anti = scored["anti_regime_flag"].astype(bool).to_numpy()
        direction = np.where(anti, -base_direction, 0).astype("int8")
        active = active & anti
    elif mode == "two_head_router":
        quality = scored["profit_quality_score"].astype(float).to_numpy()
        quality_values = quality[scored["precondition_pass"].astype(bool).to_numpy()]
        quality_cut = float(np.quantile(quality_values[np.isfinite(quality_values)], 0.35)) if len(quality_values) else 0.0
        anti = scored["anti_meta_score"].astype(float).to_numpy() > quality * 1.08
        direction = np.where(anti, -base_direction, base_direction).astype("int8")
        active = active & (quality >= quality_cut)
    else:
        direction = base_direction
    return np.where(active, direction, 0).astype("int8")


def train_folds(frame: pd.DataFrame) -> list[tuple[str, pd.DataFrame, pd.DataFrame]]:
    train = frame.loc[frame["split"].astype(str).eq("train")].sort_values("timestamp").reset_index(drop=True)
    n = len(train)
    windows = [(0.38, 0.52), (0.52, 0.66), (0.66, 0.82), (0.82, 1.00)]
    folds = []
    for index, (start_frac, end_frac) in enumerate(windows, start=1):
        start = max(5000, int(n * start_frac))
        end = min(n, int(n * end_frac))
        if end <= start + 500:
            continue
        folds.append((f"fold{index:02d}", train.iloc[:start].copy(), train.iloc[start:end].copy()))
    return folds


def fold_selection_score(metrics: Sequence[Mapping[str, Any]], spec: CandidateSpec) -> float:
    if not metrics:
        return -999999.0
    nets = [float(row["net_bp"]) for row in metrics]
    densities = [float(row["trades_per_day"]) for row in metrics]
    pfs = [float(row["pf"]) for row in metrics]
    recoveries = [float(row["recovery"]) for row in metrics]
    pockets20 = [float(row["worst_rolling_20_bp"]) for row in metrics]
    pockets50 = [float(row["worst_rolling_50_bp"]) for row in metrics]
    worst_months = [float(row["worst_month_bp"]) for row in metrics]
    underwater = [float(row["underwater_ratio"]) for row in metrics]
    density_penalty = sum(abs(item - spec.target_density) * 42.0 for item in densities)
    density_penalty += sum(760.0 + abs(item - spec.target_density) * 105.0 for item in densities if item < 4.0 or item > 10.0)
    pocket_penalty = sum(abs(min(0.0, item)) * 0.50 for item in pockets20)
    pocket_penalty += sum(abs(min(0.0, item)) * 0.32 for item in pockets50)
    month_penalty = sum(abs(min(0.0, item)) * 0.22 for item in worst_months)
    water_penalty = sum(max(0.0, item - 0.84) * 230.0 for item in underwater)
    consistency_bonus = sum(1 for item in nets if item > 0.0) / len(nets) * 360.0
    pf_bonus = sum(max(0.0, item - 1.0) * 210.0 for item in pfs)
    recovery_bonus = sum(max(0.0, item) * 24.0 for item in recoveries)
    worst_fold_penalty = abs(min(0.0, min(nets))) * 0.82
    profit_scale_bonus = max(0.0, sum(nets)) * 0.12
    return float(sum(nets) + profit_scale_bonus + consistency_bonus + pf_bonus + recovery_bonus - density_penalty - pocket_penalty - month_penalty - water_penalty - worst_fold_penalty)


def choose_wfo_mode(spec: CandidateSpec, frame: pd.DataFrame) -> tuple[str, float, float, list[dict[str, Any]], dict[str, Any]]:
    fold_scored: list[tuple[str, pd.DataFrame]] = []
    for fold_index, (fold_id, fold_train, fold_validation) in enumerate(train_folds(frame), start=1):
        prepared = train_prepared(spec, fold_train, seed=2930 + fold_index, persist=False)
        fold_scored.append((fold_id, score_edges(prepared, fold_validation)))
    if not fold_scored:
        raise RuntimeError(f"No WFO folds available for {spec.package_id}")
    best: tuple[str, float, float, list[dict[str, Any]], dict[str, Any]] | None = None
    quantiles = np.linspace(0.01, 0.985, 86)
    for mode in spec.modes:
        for quantile in quantiles:
            fold_rows: list[dict[str, Any]] = []
            metrics_list: list[dict[str, Any]] = []
            for fold_id, scored in fold_scored:
                threshold = threshold_for_quantile(scored, float(quantile), mode)
                signal = build_signal(scored, threshold, mode)
                metrics = s290.curve_metrics(scored, signal, spec.max_hold_bars)
                metrics_list.append(metrics)
                fold_rows.append(
                    {
                        "materialized_branch_id": "",
                        "package_id": spec.package_id,
                        "fold_id": fold_id,
                        "mode": mode,
                        "quantile": float(quantile),
                        "threshold": threshold,
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
            score = fold_selection_score(metrics_list, spec)
            summary = {
                "wfo_net_bp": float(sum(float(row["net_bp"]) for row in metrics_list)),
                "wfo_positive_fold_share": float(sum(1 for row in metrics_list if float(row["net_bp"]) > 0.0) / len(metrics_list)),
                "wfo_worst_fold_net_bp": float(min(float(row["net_bp"]) for row in metrics_list)),
                "wfo_mean_trades_per_day": float(np.mean([float(row["trades_per_day"]) for row in metrics_list])),
                "wfo_min_trades_per_day": float(min(float(row["trades_per_day"]) for row in metrics_list)),
                "wfo_max_trades_per_day": float(max(float(row["trades_per_day"]) for row in metrics_list)),
                "selection_score": score,
            }
            if best is None or score > best[2]:
                best = (mode, float(quantile), float(score), fold_rows, summary)
    if best is None:
        raise RuntimeError(f"No WFO selection available for {spec.package_id}")
    return best


def split_metrics(scored: pd.DataFrame, quantile: float, mode: str, hold_limit: int, split: str) -> tuple[dict[str, Any], np.ndarray, float]:
    part = scored.loc[scored["split"].astype(str).eq(split)].copy()
    train_part = scored.loc[scored["split"].astype(str).eq("train")].copy()
    threshold = threshold_for_quantile(train_part, quantile, mode)
    signal = build_signal(part, threshold, mode)
    return s290.curve_metrics(part, signal, hold_limit), signal, threshold


def materialize_payload(prepared: PreparedModel, scored: pd.DataFrame, quantile: float, threshold: float, mode: str) -> tuple[pd.DataFrame, dict[str, Any]]:
    spec = prepared.spec
    signal = build_signal(scored, threshold, mode)
    runtime = scored.copy()
    branch_id = f"run293A_{spec.package_id.replace('_surface', '')}"
    runtime["stage293_branch_id"] = branch_id
    runtime["stage291_branch_id"] = branch_id
    runtime["stage290_branch_id"] = branch_id
    runtime["materialized_branch_id"] = branch_id
    runtime["package_id"] = spec.package_id
    runtime["queue_role"] = "profit_scale_density_calibration_surface"
    runtime["candidate_decision_score"] = activation_score(runtime, mode)
    runtime["route_signal_value"] = signal
    runtime["route_signal_label"] = [s290.signal_label(int(value)) for value in signal]
    runtime["signal_active"] = (signal != 0).astype("int8")
    runtime["model_risk_pct"] = 0.01
    runtime["max_hold_bars"] = spec.max_hold_bars
    runtime["close_on_flat_signal"] = True
    runtime["same_direction_reentry_cooldown_bars"] = 0
    surface_identity = {
        "package_id": spec.package_id,
        "model_family": spec.model_family,
        "prediction_kind": spec.prediction_kind,
        "dataset_id": spec.dataset_id,
        "selection_quantile": quantile,
        "threshold": threshold,
        "mode": mode,
        "precondition": spec.precondition,
        "max_hold_bars": spec.max_hold_bars,
        "feature_order_hash": ordered_hash(prepared.feature_order),
    }
    surface_hash = hashlib.sha256(json.dumps(surface_identity, sort_keys=True).encode("utf-8")).hexdigest()
    runtime["direction_surface_hash"] = surface_hash
    runtime["direction_feature_order_hash"] = ordered_hash(("route_signal_value",))
    runtime["model_feature_order_hash"] = ordered_hash(prepared.feature_order)
    runtime["payload_claim_boundary"] = BOUNDARY
    drop_columns = [
        name
        for name in runtime.columns
        if name.startswith(("label", "future_")) or name in {"label_class", "evaluation_label_available"}
    ]
    runtime = runtime.drop(columns=drop_columns, errors="ignore")
    tier_a = runtime.copy()
    tier_a["tier_scope"] = "Tier A"
    tier_b = runtime.copy()
    tier_b["tier_scope"] = "Tier B"
    payload = pd.concat([tier_a, tier_b], ignore_index=True)
    return payload, surface_identity | {"direction_surface_hash": surface_hash}


def gate_label(metrics: Mapping[str, Any], oos_metrics: Mapping[str, Any], gate: str) -> str:
    if gate == "density":
        ok = 4.0 <= float(metrics["trades_per_day"]) <= 10.0 and 4.0 <= float(oos_metrics["trades_per_day"]) <= 10.0
    elif gate == "edge":
        ok = float(metrics["net_bp"]) > 0.0 and float(oos_metrics["net_bp"]) > 0.0 and float(metrics["pf"]) >= 1.05 and float(oos_metrics["pf"]) >= 1.02
    else:
        ok = (
            float(metrics["worst_rolling_20_bp"]) >= -240.0
            and float(oos_metrics["worst_rolling_20_bp"]) >= -260.0
            and float(metrics["positive_month_share"]) >= 0.50
            and float(oos_metrics["positive_month_share"]) >= 0.45
            and float(metrics["underwater_ratio"]) <= 0.90
            and float(oos_metrics["underwater_ratio"]) <= 0.92
        )
    return "passed" if ok else "failed"


def build_outputs() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[Path]]:
    branch_rows: list[dict[str, Any]] = []
    scoreboard_rows: list[dict[str, Any]] = []
    supply_rows: list[dict[str, Any]] = []
    manifest_rows: list[dict[str, Any]] = []
    model_rows: list[dict[str, Any]] = []
    wfo_rows: list[dict[str, Any]] = []
    artifacts: list[Path] = []
    dataset_cache: dict[str, pd.DataFrame] = {}
    for index, spec in enumerate(candidate_specs(), start=1):
        frame = dataset_cache.setdefault(spec.dataset_id, s290.load_dataset(spec.dataset_id))
        mode, quantile, score, fold_rows, wfo_summary = choose_wfo_mode(spec, frame)
        train = frame.loc[frame["split"].astype(str).eq("train")].copy()
        prepared = train_prepared(spec, train, seed=293, persist=True)
        scored = score_edges(prepared, frame)
        train_scored = scored.loc[scored["split"].astype(str).eq("train")].copy()
        threshold = threshold_for_quantile(train_scored, quantile, mode)
        validation_metrics, _validation_signal, _threshold = split_metrics(scored, quantile, mode, spec.max_hold_bars, "validation")
        oos_metrics, _oos_signal, _threshold = split_metrics(scored, quantile, mode, spec.max_hold_bars, "oos")
        payload, surface_identity = materialize_payload(prepared, scored, quantile, threshold, mode)
        branch_id = f"run293A_{spec.package_id.replace('_surface', '')}"
        payload_path = PAYLOAD_DIR / f"{branch_id}_payload.parquet"
        handoff_path = HANDOFF_DIR / f"{branch_id}_handoff.json"
        io_path(payload_path.parent).mkdir(parents=True, exist_ok=True)
        payload.to_parquet(io_path(payload_path), index=False)
        write_json(
            handoff_path,
            {
                "stage293_branch_id": branch_id,
                "package_id": spec.package_id,
                "model_family": spec.model_family,
                "prediction_kind": spec.prediction_kind,
                "dataset_id": spec.dataset_id,
                "feature_order": prepared.feature_order,
                "feature_order_hash": ordered_hash(prepared.feature_order),
                "selection_quantile": quantile,
                "selection_threshold": threshold,
                "selection_mode": mode,
                "precondition": spec.precondition,
                "max_hold_bars": spec.max_hold_bars,
                "close_on_flat_signal": True,
                "runtime_handoff": "precomputed route_signal_value replay for MT5 probe; model artifact retained for Adapter/ONNX only if candidate survives",
                "claim_boundary": BOUNDARY,
                "surface_identity": surface_identity,
            },
        )
        candidate_supply = s290.supply_rows_for_payload(payload, spec)  # type: ignore[arg-type]
        supply_rows.extend(candidate_supply)
        val_supply = next(row for row in candidate_supply if row["tier_scope"] == "Tier A" and row["split"] == "validation")
        oos_supply = next(row for row in candidate_supply if row["tier_scope"] == "Tier A" and row["split"] == "oos")
        for fold_row in fold_rows:
            fold_row["materialized_branch_id"] = branch_id
            wfo_rows.append(fold_row)
        manifest_rows.append(
            {
                "queue_id": f"run293A_queue_{index:02d}",
                "materialized_branch_id": branch_id,
                "stage293_branch_id": branch_id,
                "stage291_branch_id": branch_id,
                "stage290_branch_id": branch_id,
                "package_id": spec.package_id,
                "queue_role": "profit_scale_density_calibration_surface",
                "payload_path": rel(payload_path),
                "payload_hash": sha256_file_lf_normalized(payload_path),
                "handoff_path": rel(handoff_path),
                "handoff_hash": sha256_file_lf_normalized(handoff_path),
                "model_artifact_path": rel(prepared.model_path or ""),
                "model_artifact_hash": sha256_file_lf_normalized(prepared.model_path) if prepared.model_path else "",
                "model_feature_order_path": rel(prepared.feature_order_path or ""),
                "model_feature_order_hash": ordered_hash(prepared.feature_order),
                "direction_surface_hash": surface_identity["direction_surface_hash"],
                "direction_feature_order_hash": ordered_hash(("route_signal_value",)),
                "max_hold_bars": spec.max_hold_bars,
                "close_on_flat_signal": True,
                "same_direction_reentry_cooldown_bars": 0,
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
                "model_family": spec.model_family,
                "prediction_kind": spec.prediction_kind,
                "dataset_id": spec.dataset_id,
                "model_artifact_path": rel(prepared.model_path or ""),
                "model_artifact_hash": sha256_file_lf_normalized(prepared.model_path) if prepared.model_path else "",
                "model_feature_order_path": rel(prepared.feature_order_path or ""),
                "model_feature_order_hash": ordered_hash(prepared.feature_order),
                "imputation_path": rel(prepared.imputation_path or ""),
                "imputation_hash": sha256_file_lf_normalized(prepared.imputation_path) if prepared.imputation_path else "",
                "classes": "|".join(str(item) for item in LABEL_ORDER) if spec.prediction_kind == "multiclass_probability" else "return_regression",
                "payoff_weight_policy": spec.sample_weight_policy,
                "onnx_exportability_note": "candidate model family has known converter path or project bridge candidate; export deferred until candidate package gate",
            }
        )
        scoreboard_rows.append(
            {
                "materialized_branch_id": branch_id,
                "package_id": spec.package_id,
                "dataset_id": spec.dataset_id,
                "model_family": spec.model_family,
                "prediction_kind": spec.prediction_kind,
                "mode": mode,
                "quantile": quantile,
                "threshold": threshold,
                "precondition": spec.precondition,
                **wfo_summary,
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
                "density_gate": gate_label(validation_metrics, oos_metrics, "density"),
                "proxy_edge_gate": gate_label(validation_metrics, oos_metrics, "edge"),
                "curve_proxy_gate": gate_label(validation_metrics, oos_metrics, "curve"),
                "selected_candidate": "none",
                "adapter_package": "none",
                "onnx_readiness": "not_claimed",
                "claim_boundary": BOUNDARY,
            }
        )
        branch_rows.append(
            {
                "stage293_branch_id": branch_id,
                "materialized_branch_id": branch_id,
                "package_id": spec.package_id,
                "idea_id": "IDEA-ST293-PROFIT-SCALE-DENSITY-CALIBRATION",
                "hypothesis": spec.hypothesis,
                "decision_use": "MT5 runtime probe seed only; no candidate selection until run293B/run293C evidence",
                "comparison_baseline": "Stage292 valid negative runtime scoreboard plus Stage290 density/profit clue",
                "control_variables": "FPMarkets US100 M5 split_v1; feature_set_v2 proxy58; train/validation/oos windows; single-feature route-signal replay handoff",
                "changed_variables": spec.changed_variables,
                "sample_scope": f"{spec.dataset_id}; train-only WFO folds plus validation/oos proxy read; Tier A and Tier B duplicated for paired runtime accounting",
                "success_criteria": "4-10 trades/day in validation and OOS, positive MT5 net/PF/recovery/expectancy, and no deep local curve pockets",
                "failure_criteria": "MT5 validation or OOS net/PF fails, density outside 4-10, or local curve pockets dominate",
                "invalid_conditions": "payload contains label/future columns, WFO folds missing, model feature order missing, MT5 report missing, or runtime handoff mismatch",
                "stop_conditions": "after full run293B MT5 probe and run293C review; no narrow threshold repair inside stage293",
                "evidence_plan": "wfo_fold_scoreboard; model_scout_scoreboard; candidate_supply_diagnostics; payload_manifest; mt5_probe_queue; run293B MT5 KPI; run293C curve/time-slice review",
                "model_family": spec.model_family,
                "dataset_id": spec.dataset_id,
                "prediction_kind": spec.prediction_kind,
                "objective_surface": spec.objective_surface,
                "selection_mode": mode,
                "selection_quantile": quantile,
                "selection_threshold": threshold,
                "precondition": spec.precondition,
                "risk_logic": f"max_hold_bars={spec.max_hold_bars};close_on_flat_signal=true;same_direction_reentry_cooldown_bars=0",
                "adapter_path": "deferred_until_candidate_survives_run293B_run293C",
                "runtime_handoff": "route_signal_value replay now; model artifact and feature order retained for Adapter package if selected",
                "claim_boundary": BOUNDARY,
            }
        )
        artifacts.extend([payload_path, handoff_path, prepared.model_path, prepared.feature_order_path, prepared.imputation_path])
    return branch_rows, scoreboard_rows, supply_rows, manifest_rows, model_rows, wfo_rows, [path for path in artifacts if path]


def report_markdown(scoreboard_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = []
    for row in scoreboard_rows:
        lines.append(
            f"- `{row['package_id']}`: mode(紐⑤뱶) `{row['mode']}`, WFO(?뚰겕?ъ썙?? net `{float(row['wfo_net_bp']):.2f}`bp, "
            f"validation(寃利? `{float(row['validation_proxy_net_bp']):.2f}`bp/`{float(row['validation_proxy_trades_per_day']):.2f}` trades/day(??嫄곕옒), "
            f"OOS(?쒕낯?? `{float(row['oos_proxy_net_bp']):.2f}`bp/`{float(row['oos_proxy_trades_per_day']):.2f}` trades/day(??嫄곕옒), "
            f"gates(愿臾? `{row['density_gate']}/{row['proxy_edge_gate']}/{row['curve_proxy_gate']}`."
        )
    queue_lines = [
        f"- `{row['package_id']}` -> `{row['materialized_branch_id']}` validation approx(寃利?洹쇱궗) `{float(row['approx_validation_trades_per_day']):.2f}`/day, OOS approx(?쒕낯??洹쇱궗) `{float(row['approx_oos_trades_per_day']):.2f}`/day"
        for row in manifest_rows
    ]
    return f"""# run293A Profit-scale Density Calibration Materialization(293A ??갑??硫뷀??쇰꺼 嫄곕옒 ?쒕??덉씠??臾쇱쭏??

- run_id(?ㅽ뻾 ID): `{RUN_ID}`
- status(?곹깭): `{STATUS}`
- judgment(?먯젙): `{JUDGMENT}`
- branch_count(遺꾧린 ??: `{len(manifest_rows)}`
- selected_candidate(?좏깮 ?꾨낫): `none`
- Adapter package(?대뙌???⑦궎吏): `none`
- ONNX readiness(?⑥뿊??以鍮?: `not_claimed`
- next_action(?ㅼ쓬 ?됰룞): `{NEXT_ACTION}`

## Thesis(?쇱젣)

Stage292(292단계)는 밀도는 맞지만 validation loss(검증 손실), 순수익 규모 부족, 곡선 포켓이 동시에 남았다. Stage293(293단계)는 같은 repair(수리)가 아니라 runtime-aware simulator calibration(런타임 인식 시뮬레이터 보정), profit-scale density router(순수익 규모/밀도 라우터), smooth curve objective(매끈한 곡선 목적함수)로 decision surface(판단 표면)를 새로 만든다.

## Scoreboard(?먯닔??

{chr(10).join(lines)}

## MT5 Queue(MT5 ?湲곗뿴)

{chr(10).join(queue_lines)}

## Boundary(寃쎄퀎)

?좏깮 ?꾨낫, Adapter package(?대뙌???⑦궎吏), ONNX readiness(?⑥뿊??以鍮?, Goal Achieve(紐⑺몴 ?ъ꽦)???꾩쭅 二쇱옣?섏? ?딅뒗?? ???곗텧臾쇱? run293B(293B ?ㅽ뻾) MT5 runtime probe(MT5 ?고????먯묠) ?낅젰?대떎.
"""


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
    for path in (RUN_ROOT, PAYLOAD_DIR, MODEL_DIR, HANDOFF_DIR, REVIEWS):
        io_path(path).mkdir(parents=True, exist_ok=True)
    write_csv(BRANCH_QUEUE, BRANCH_COLUMNS, branch_rows)
    write_csv(MODEL_SCOREBOARD, SCOREBOARD_COLUMNS, scoreboard_rows)
    write_csv(CANDIDATE_SUPPLY, SUPPLY_COLUMNS, supply_rows)
    write_csv(PAYLOAD_MANIFEST, MANIFEST_COLUMNS, manifest_rows)
    write_csv(MT5_QUEUE, MANIFEST_COLUMNS, manifest_rows)
    write_csv(MODEL_MANIFEST, MODEL_COLUMNS, model_rows)
    write_csv(WFO_FOLD_SCOREBOARD, WFO_COLUMNS, wfo_rows)
    write_json(
        EXPERIMENT_DESIGN,
        {
            "hypothesis": "Runtime-aware simulator calibration, profit-scale density routing, and smooth curve objectives can reduce the Stage292 proxy-runtime gap and create an ONNX-worthy candidate seed.",
            "decision_use": "Decide whether stage293 should proceed to full MT5 runtime probe and candidate review.",
            "comparison_baseline": "Stage292 runtime-negative anti-direction simulator review plus Stage290 density/profit clue.",
            "control_variables": "FPMarkets US100 M5, split_v1, feature_set_v2 proxy58, Tier A/B paired runtime accounting, route_signal_value replay.",
            "changed_variables": "mode sweep over runtime-calibrated inverse, profit-scale direct/inverse, density-profit router, smooth-curve router, model family, precondition, hold logic, and simulator score.",
            "sample_scope": "Tier A and Tier B paired labels; train/validation/OOS dataset scope from v2 processed datasets.",
            "success_criteria": "4-10 trades/day, positive net/PF/recovery/expectancy, and smooth curve without deep local pockets in MT5 probe.",
            "failure_criteria": "negative validation/OOS MT5 net, density outside 4-10, or deep curve pockets.",
            "invalid_conditions": "missing folds, label/future columns in runtime payload, missing feature order, or MT5 handoff mismatch.",
            "stop_conditions": "review after run293B/run293C; do not keep repairing a narrow mode if MT5 is negative.",
            "evidence_plan": "wfo_fold_scoreboard, model_scout_scoreboard, payload manifest, MT5 queue, run293B KPI, run293C curve review.",
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            "run_id": RUN_ID,
            "feature_source": "stage290.load_dataset feature_set_v2 proxy58",
            "runtime_payload_label_future_columns_removed": True,
            "tier_scope": "Tier A/Tier B paired payload duplication",
            "claim_boundary": BOUNDARY,
        },
    )
    write_csv(
        RESULT_JUDGMENT,
        RESULT_COLUMNS,
        [
            {
                "result_subject": RUN_ID,
                "evidence_available": f"model_rows={len(model_rows)};mt5_queue_rows={len(manifest_rows)};wfo_rows={len(wfo_rows)};report={rel(REPORT)}",
                "evidence_missing": "MT5 runtime KPI; trade report curve review; candidate package; Adapter package; ONNX parity",
                "judgment_label": JUDGMENT,
                "judgment_class": "materialization_no_candidate(臾쇱쭏?? ?꾨낫 ?꾨떂)",
                "claim_boundary": BOUNDARY,
                "next_condition": NEXT_ACTION,
                "user_explanation_hook": "??援ъ“瑜?留뚮뱾?덉?留?MT5濡??뚮━湲??꾩뿉???꾨낫媛 ?꾨땲??",
            }
        ],
    )
    write_csv(
        GATE_AUDIT,
        GATE_COLUMNS,
        [
            {
                "gate_name": "fresh_thesis(???쇱젣)",
                "status": "passed",
                "evidence_path": rel(BRANCH_QUEUE),
                "effect": "Stage292(292단계)의 같은 repair(수리)가 아니라 runtime/profit/curve surface(런타임/순수익/곡선 표면)를 만든다.",
            },
            {
                "gate_name": "runtime_handoff_payload(?고????멸퀎 ?섏씠濡쒕뱶)",
                "status": "passed",
                "evidence_path": rel(MT5_QUEUE),
                "effect": "route_signal_value? feature order(?쇱쿂 ?쒖꽌)瑜?異붿쟻 媛?ν븯寃?留뚮뱾?덈떎.",
            },
            {
                "gate_name": "candidate_claim_boundary(?꾨낫 二쇱옣 寃쎄퀎)",
                "status": "passed",
                "evidence_path": rel(RESULT_JUDGMENT),
                "effect": "MT5 KPI ?꾩뿉???좏깮 ?꾨낫, Adapter(?대뙌??, ONNX(?⑥뿊??瑜?二쇱옣?섏? ?딅뒗??",
            },
        ],
    )
    write_md(REPORT, report_markdown(scoreboard_rows, manifest_rows))
    final = [
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
        REPORT,
        *payload_artifacts,
    ]
    write_json(
        LINEAGE,
        {
            "run_id": RUN_ID,
            "producer": rel(ROOT / "stage_pipelines/stage293/design_materialize_profit_scale_density_calibration_rebuild.py"),
            "source_artifacts": [rel(STAGE293_SEED_QUEUE), rel(SOURCE_SCOREBOARD), rel(SOURCE_FAILURE)],
            "produced_artifacts": [rel(path) for path in final if path_exists(path)],
            "claim_boundary": BOUNDARY,
        },
    )
    final.append(LINEAGE)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "source_run_id": SOURCE_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "created_at_utc": created_at,
            "branch_count": len(branch_rows),
            "mt5_queue_rows": len(manifest_rows),
            "selected_candidate": "none",
            "adapter_package": "none",
            "onnx_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "next_action": NEXT_ACTION,
            "claim_boundary": BOUNDARY,
            "output_hashes": {rel(path): sha256_file_lf_normalized(path) for path in final if path_exists(path)},
        },
    )
    final.append(RUN_MANIFEST)
    return [path for path in final if path_exists(path)]


def update_docs(created_at: str, artifacts: Sequence[Path], manifest_rows: Sequence[Mapping[str, Any]], scoreboard_rows: Sequence[Mapping[str, Any]]) -> None:
    upsert_csv(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "profit_scale_density_calibration_materialization",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "notes": f"branches={len(scoreboard_rows)};next_action={NEXT_ACTION}",
            }
        ],
        key="run_id",
    )
    upsert_csv(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "profit_scale_density_calibration_materialization",
                "tier_scope": "Tier A/Tier B paired exploration labels",
                "kpi_scope": "model_proxy_and_runtime_queue",
                "scoreboard_lane": "profit_scale_density_calibration",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "primary_kpi": f"mt5_queue_rows={len(manifest_rows)};wfo_fold_rows={len(scoreboard_rows) * 4}",
                "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed",
                "external_verification_status": "out_of_scope_by_claim_run293B_required",
                "notes": "MT5 probe required before candidate judgment.",
            }
        ],
        key="ledger_row_id",
    )
    upsert_csv(
        STAGE_LEDGER,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "profit_scale_density_calibration_materialization",
                "tier_scope": "Tier A/Tier B paired exploration labels",
                "scoreboard": "model_scout_scoreboard",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "materialization_no_candidate_no_onnx",
                "report_path": rel(REPORT),
                "notes": f"mt5_queue_rows={len(manifest_rows)};next_action={NEXT_ACTION}",
            }
        ],
        key="row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{hashlib.sha1(rel(path).encode('utf-8')).hexdigest()[:12]}",
            "artifact_type": "stage293_materialization_artifact",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run293A Profit-scale Density Calibration materialization",
        }
        for path in artifacts
        if path_exists(path)
    ]
    upsert_csv(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")

    selected = io_path(SELECTED).read_text(encoding="utf-8-sig") if path_exists(SELECTED) else ""
    selected = replace_line_prefix(selected, "- stage_status(?④퀎 ?곹깭):", f"- stage_status(?④퀎 ?곹깭): `{STATUS}`")
    selected = replace_line_prefix(selected, "- current_run(?꾩옱 ?ㅽ뻾):", f"- current_run(?꾩옱 ?ㅽ뻾): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- next_action(?ㅼ쓬 ?됰룞):", f"- next_action(?ㅼ쓬 ?됰룞): `{NEXT_ACTION}`")
    selected = append_once(selected, "run293A_report", f"- run293A_report(293A 蹂닿퀬): `{rel(REPORT)}`")
    selected = append_once(selected, "run293A_mt5_queue", f"- run293A_mt5_queue(293A MT5 ?湲곗뿴): `{rel(MT5_QUEUE)}`")
    write_md(SELECTED, selected)

    review_index = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX) else "# stage293 Review Index(293?④퀎 寃???됱씤)\n"
    review_index = append_once(review_index, "run293A_report", f"- run293A_report(293A 蹂닿퀬): `{rel(REPORT)}`\n- run293A_mt5_queue(293A MT5 ?湲곗뿴): `{rel(MT5_QUEUE)}`")
    write_md(REVIEW_INDEX, review_index)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig") if path_exists(CURRENT_STATE) else ""
    current = replace_line_prefix(current, "- current_packet(?꾩옱 ?묒뾽 臾띠쓬):", f"- current_packet(?꾩옱 ?묒뾽 臾띠쓬): `{STAGE_ID}_v1`")
    current = replace_line_prefix(current, "- current_run(?꾩옱 ?ㅽ뻾):", f"- current_run(?꾩옱 ?ㅽ뻾): `{RUN_ID}`")
    current = replace_line_prefix(current, "- active_stage(?쒖꽦 ?④퀎):", f"- active_stage(?쒖꽦 ?④퀎): `{STAGE_ID}`")
    current = replace_line_prefix(current, "- source_stage(?먯쿇 ?④퀎):", f"- source_stage(?먯쿇 ?④퀎): `{STAGE_ID}`")
    current = replace_line_prefix(current, "- target_surface(紐⑺몴 ?쒕㈃):", "- target_surface(紐⑺몴 ?쒕㈃): `none`")
    current = replace_line_prefix(current, "- status(?곹깭):", f"- status(?곹깭): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(?ㅼ쓬 ?됰룞):", f"- next_action(?ㅼ쓬 ?됰룞): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run293A_summary",
        f"- run293A_summary(293A ?붿빟): profit-scale density calibration(??갑??硫뷀??쇰꺼/嫄곕옒 ?쒕??덉씠?? ?꾨낫 `{len(manifest_rows)}`媛쒕? 臾쇱쭏?뷀뻽?? Effect(?④낵): MT5 runtime probe(MT5 ?고????먯묠)濡???4-10嫄곕옒, ?쒖닔?? PF, ?뚮났, 怨≪꽑??寃利앺븷 ???덇퀬 ?좏깮 ?꾨낫/?대뙌???⑥뿊?ㅻ뒗 ?꾩쭅 二쇱옣?섏? ?딅뒗??",
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig") if path_exists(WORKSPACE_STATE) else ""
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE_ID}")
    workspace = replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = (
        f"- >-\n"
        f"  stage293(293?④퀎) run293A(293A ?ㅽ뻾) profit-scale density calibration materialization(??갑??硫뷀??쇰꺼/嫄곕옒 ?쒕??덉씠??臾쇱쭏?? `{RUN_ID}`. "
        f"Effect(?④낵): ?꾨낫 `{len(manifest_rows)}`媛쒖? MT5 probe queue(MT5 ?먯묠 ?湲곗뿴)瑜?留뚮뱾?덇퀬 selected candidate(?좏깮 ?꾨낫), Adapter package(?대뙌???⑦궎吏), ONNX readiness(?⑥뿊??以鍮???二쇱옣?섏? ?딅뒗??\n"
    )
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_md(WORKSPACE_STATE, workspace)

    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(蹂寃?湲곕줉)\n"
    changelog = append_once(
        changelog,
        RUN_ID,
        f"## {UPDATED_ON} run293A Profit-scale Density Calibration materialization(293A ??갑??硫뷀??쇰꺼 嫄곕옒 ?쒕??덉씠??臾쇱쭏??\n\n"
        f"- status(?곹깭): `{STATUS}`\n"
        f"- judgment(?먯젙): `{JUDGMENT}`\n"
        f"- effect(?④낵): branch(遺꾧린) `{len(manifest_rows)}`媛쒖? MT5 queue(MT5 ?湲곗뿴) `{len(manifest_rows)}`媛쒕? 留뚮뱾?덈떎.\n"
        f"- boundary(寃쎄퀎): selected candidate(?좏깮 ?꾨낫), Adapter package(?대뙌???⑦궎吏), ONNX readiness(?⑥뿊??以鍮?, Goal Achieve(紐⑺몴 ?ъ꽦)??`none/not_claimed`??\n",
    )
    write_md(CHANGELOG, changelog)


def main() -> None:
    created_at = utc_now()
    branch_rows, scoreboard_rows, supply_rows, manifest_rows, model_rows, wfo_rows, payload_artifacts = build_outputs()
    artifacts = write_outputs(branch_rows, scoreboard_rows, supply_rows, manifest_rows, model_rows, wfo_rows, payload_artifacts, created_at)
    update_docs(created_at, artifacts, manifest_rows, scoreboard_rows)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "branch_count": len(branch_rows),
                "mt5_queue_rows": len(manifest_rows),
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

