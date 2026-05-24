from __future__ import annotations

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


STAGE_ID = "291_onnx_candidate_campaign__walk_forward_payoff_generalization_rebuild"
RUN_ID = "run291A_design_walk_forward_payoff_generalization_rebuild_v1"
RUN_NUMBER = "run291A"
STATUS = "completed_walk_forward_payoff_generalization_candidates_materialized_no_selection"
JUDGMENT = "walk_forward_payoff_generalization_inputs_materialized_no_candidate_selection"
NEXT_ACTION = "run291B_execute_walk_forward_payoff_generalization_mt5_probe"
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

STAGE290 = ROOT / "stages" / "290_onnx_candidate_campaign__payoff_weighted_edge_model_rebuild"
STAGE291_SEED_QUEUE = STAGE_ROOT / "01_inputs" / "stage291_seed_queue.csv"
SOURCE_SCOREBOARD = STAGE290 / "02_runs" / "run290C" / "payoff_weighted_edge_scoreboard.csv"
SOURCE_FAILURE = STAGE290 / "02_runs" / "run290C" / "failure_memory.csv"
SOURCE_MODEL_SCOREBOARD = STAGE290 / "02_runs" / "run290A" / "model_scout_scoreboard.csv"

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
REPORT = REVIEWS / "run291A_walk_forward_payoff_generalization_materialization_report.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

LABEL_ORDER = (0, 1, 2)


BRANCH_COLUMNS = (
    "stage291_branch_id",
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
    "selection_orientation",
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
    "orientation",
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
    "orientation",
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
        import csv

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
            package_id="cp291A_wfo_lgbm_cash_hold6_surface",
            model_family="lightgbm_multiclass_wfo",
            prediction_kind="multiclass_probability",
            dataset_id="fwd12_proxy58",
            max_hold_bars=6,
            precondition="cash_non_extreme",
            sample_weight_policy="abs_forward_return_x_class_balance_x_recency",
            objective_surface="walk_forward_quantile_payoff_edge",
            hypothesis="Walk-forward quantile selection can keep the Stage290 density clue while reducing validation-fit OOS shrinkage.",
            changed_variables="fold-trained LightGBM; quantile threshold chosen on train-only WFO folds; hold6 cash precondition",
            target_density=6.5,
        ),
        CandidateSpec(
            package_id="cp291B_side_return_xgb_hold8_surface",
            model_family="xgboost_return_regressor_wfo",
            prediction_kind="return_regression",
            dataset_id="fwd18_proxy58",
            max_hold_bars=8,
            precondition="all_rows",
            sample_weight_policy="abs_forward_return_x_recency_x_tail",
            objective_surface="side_relabel_return_expectation",
            hypothesis="A return-regression side surface can avoid the universal inverse-orientation clue from Stage290 class labels.",
            changed_variables="XGBoost regressor; side relabel from predicted return sign; WFO quantile selection; hold8",
            target_density=5.5,
        ),
        CandidateSpec(
            package_id="cp291C_cost_curve_lgbm_hold5_surface",
            model_family="lightgbm_return_regressor_curve",
            prediction_kind="return_regression",
            dataset_id="fwd12_proxy58",
            max_hold_bars=5,
            precondition="liquid_not_extreme",
            sample_weight_policy="abs_forward_return_x_recency",
            objective_surface="native_cost_curve_penalized_return",
            hypothesis="Putting rolling-pocket and cost penalties into train-fold selection can improve curve smoothness before MT5 rejection.",
            changed_variables="LightGBM return regressor; native curve/cost WFO selection; liquid-not-extreme precondition; hold5",
            target_density=6.0,
        ),
        CandidateSpec(
            package_id="cp291D_defensive_density_histgb_hold4_surface",
            model_family="histgb_multiclass_density_lift",
            prediction_kind="multiclass_probability",
            dataset_id="fwd12_proxy58",
            max_hold_bars=4,
            precondition="volatility_balanced_loose",
            sample_weight_policy="abs_forward_return_x_class_balance",
            objective_surface="defensive_density_lift_wfo",
            hypothesis="The Stage290 defensive PF clue may become usable if density is lifted through WFO quantiles rather than threshold repair.",
            changed_variables="HistGradientBoosting classifier; looser volatility balance; train-only WFO density target; hold4",
            target_density=5.0,
        ),
        CandidateSpec(
            package_id="cp291E_side_relabel_extratrees_hold6_surface",
            model_family="extratrees_return_regressor_side",
            prediction_kind="return_regression",
            dataset_id="fwd12_proxy58",
            max_hold_bars=6,
            precondition="cash_or_late_liquid",
            sample_weight_policy="abs_forward_return_x_side_balance",
            objective_surface="nonlinear_side_relabel_return_surface",
            hypothesis="A nonlinear side-regression surface can test whether direction label alignment, not thresholding, caused Stage290 inversion.",
            changed_variables="ExtraTrees return regressor; side-balanced weights; cash/late liquid precondition; hold6",
            target_density=6.0,
        ),
        CandidateSpec(
            package_id="cp291F_wfo_xgb_fwd12_hold6_surface",
            model_family="xgboost_multiclass_wfo",
            prediction_kind="multiclass_probability",
            dataset_id="fwd12_proxy58",
            max_hold_bars=6,
            precondition="all_rows",
            sample_weight_policy="abs_forward_return_x_class_balance_x_recency",
            objective_surface="broad_wfo_payoff_classifier",
            hypothesis="A broad all-row WFO classifier can test whether Stage290 cash filters left too much profit scale out of sample.",
            changed_variables="XGBoost classifier; no session prefilter; train-only WFO quantile selection; hold6",
            target_density=7.0,
        ),
    ]


def precondition_mask(frame: pd.DataFrame, name: str) -> np.ndarray:
    rows = len(frame)
    if name == "all_rows":
        return np.ones(rows, dtype=bool)
    cash = pd.to_numeric(frame.get("is_us_cash_open", 0), errors="coerce").fillna(0).to_numpy() > 0.5
    zabs = pd.to_numeric(frame.get("return_zscore_20", 0), errors="coerce").fillna(0).abs().to_numpy()
    vol = pd.to_numeric(frame.get("historical_vol_5_over_20", 1), errors="coerce").fillna(1).to_numpy()
    minutes = pd.to_numeric(frame.get("minutes_from_cash_open", 0), errors="coerce").fillna(0).to_numpy()
    if name == "cash_non_extreme":
        return cash & (zabs <= 1.85) & (vol <= 1.85)
    if name == "cash_or_late_liquid":
        return ((cash & (minutes <= 390)) | (minutes >= 300)) & (zabs <= 2.15) & (vol <= 2.05)
    if name == "liquid_not_extreme":
        return (cash | (minutes >= 240)) & (zabs <= 1.95) & (vol <= 1.90)
    if name == "volatility_balanced_loose":
        return (vol >= 0.45) & (vol <= 1.85) & (zabs <= 2.20)
    return np.ones(rows, dtype=bool)


def sample_weights(train: pd.DataFrame, spec: CandidateSpec) -> np.ndarray:
    returns = train["future_log_return_12"].astype(float).to_numpy()
    scale = float(np.nanmedian(np.abs(returns)))
    if not np.isfinite(scale) or scale <= 0.0:
        scale = 0.001
    magnitude = np.clip(np.abs(returns) / scale, 0.25, 6.5)
    if "tail" in spec.sample_weight_policy:
        magnitude = np.power(magnitude, 1.25)
    weights = 1.0 + magnitude
    if spec.prediction_kind == "multiclass_probability":
        weights *= s290.class_balance_weights(train["label_class"].astype(int).to_numpy())
    if "side_balance" in spec.sample_weight_policy:
        signs = np.sign(returns).astype(int)
        total = float(len(signs))
        counts = {side: max(1, int((signs == side).sum())) for side in (-1, 0, 1)}
        weights *= np.asarray([total / (3.0 * counts[int(side)]) for side in signs], dtype="float64")
    if "recency" in spec.sample_weight_policy:
        weights *= np.linspace(0.80, 1.25, len(weights), dtype="float64")
    return weights.astype("float64")


def make_model(spec: CandidateSpec, seed: int) -> Any:
    if spec.model_family.startswith("xgboost_multiclass"):
        from xgboost import XGBClassifier

        return XGBClassifier(
            n_estimators=210,
            max_depth=3,
            learning_rate=0.04,
            subsample=0.86,
            colsample_bytree=0.82,
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
            n_estimators=260,
            learning_rate=0.035,
            max_depth=4,
            num_leaves=18,
            min_child_samples=70,
            subsample=0.86,
            colsample_bytree=0.80,
            random_state=seed,
            n_jobs=-1,
            verbose=-1,
        )
    if spec.model_family.startswith("xgboost_return"):
        from xgboost import XGBRegressor

        return XGBRegressor(
            n_estimators=240,
            max_depth=3,
            learning_rate=0.035,
            subsample=0.86,
            colsample_bytree=0.82,
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
            n_estimators=260,
            learning_rate=0.032,
            max_depth=4,
            num_leaves=18,
            min_child_samples=70,
            subsample=0.86,
            colsample_bytree=0.80,
            random_state=seed,
            n_jobs=-1,
            verbose=-1,
        )
    if spec.model_family.startswith("extratrees_return"):
        return ExtraTreesRegressor(
            n_estimators=420,
            max_features=0.55,
            min_samples_leaf=22,
            random_state=seed,
            n_jobs=-1,
        )
    if spec.model_family.startswith("histgb_multiclass"):
        return HistGradientBoostingClassifier(
            max_iter=170,
            learning_rate=0.045,
            max_leaf_nodes=18,
            l2_regularization=0.08,
            min_samples_leaf=55,
            random_state=seed,
        )
    return HistGradientBoostingRegressor(
        max_iter=180,
        learning_rate=0.04,
        max_leaf_nodes=18,
        l2_regularization=0.08,
        min_samples_leaf=55,
        random_state=seed,
    )


def train_prepared(spec: CandidateSpec, train: pd.DataFrame, *, seed: int, persist: bool) -> PreparedModel:
    features = s290.feature_columns(train)
    x_train, medians = s290.matrix(train, features)
    y_train: np.ndarray
    if spec.prediction_kind == "multiclass_probability":
        y_train = train["label_class"].astype(int).to_numpy()
    else:
        y_train = train["future_log_return_12"].astype(float).to_numpy()
    weights = sample_weights(train, spec)
    model = make_model(spec, seed)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        model.fit(x_train, y_train, sample_weight=weights)
    prepared = PreparedModel(
        spec=spec,
        model=model,
        feature_order=features,
        medians=medians,
        payoff_units=s290.payoff_units(train),
    )
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
        edge = (
            proba[:, 2] * units["long_unit"]
            - proba[:, 0] * units["short_unit"]
            - proba[:, 1] * units["flat_penalty"] * 0.20
        )
        confidence = np.abs(edge) * np.clip(1.0 - proba[:, 1] * 0.35, 0.10, 1.0)
        out["prob_short"] = proba[:, 0]
        out["prob_flat"] = proba[:, 1]
        out["prob_long"] = proba[:, 2]
    else:
        edge = np.asarray(prepared.model.predict(x_values), dtype="float64")
        confidence = np.abs(edge)
        out["prob_short"] = np.nan
        out["prob_flat"] = np.nan
        out["prob_long"] = np.nan
    out["payoff_edge_score"] = edge
    out["payoff_edge_confidence"] = confidence
    out["payoff_edge_direction"] = np.where(edge >= 0.0, 1, -1).astype("int8")
    out["precondition_pass"] = precondition_mask(out, prepared.spec.precondition).astype("int8")
    return out


def threshold_for_quantile(scored: pd.DataFrame, quantile: float) -> float:
    mask = scored["precondition_pass"].astype(bool).to_numpy()
    values = scored.loc[mask, "payoff_edge_confidence"].astype(float).replace([np.inf, -np.inf], np.nan).dropna().to_numpy()
    if len(values) == 0:
        return 0.0
    return float(np.quantile(values, min(max(float(quantile), 0.0), 0.995)))


def build_signal(scored: pd.DataFrame, threshold: float, orientation: str) -> np.ndarray:
    direction = scored["payoff_edge_direction"].astype("int8").to_numpy()
    if orientation == "inverse":
        direction = (-direction).astype("int8")
    active = (
        scored["payoff_edge_confidence"].astype(float).to_numpy() >= float(threshold)
    ) & scored["precondition_pass"].astype(bool).to_numpy()
    return np.where(active, direction, 0).astype("int8")


def split_days(frame: pd.DataFrame) -> int:
    return int(pd.to_datetime(frame["timestamp"], utc=True).dt.date.nunique())


def train_folds(frame: pd.DataFrame) -> list[tuple[str, pd.DataFrame, pd.DataFrame]]:
    train = frame.loc[frame["split"].astype(str).eq("train")].sort_values("timestamp").reset_index(drop=True)
    n = len(train)
    windows = [(0.42, 0.56), (0.56, 0.70), (0.70, 0.84), (0.84, 1.00)]
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
    density_penalty = sum(abs(item - spec.target_density) * 35.0 for item in densities)
    density_penalty += sum(650.0 + abs(item - spec.target_density) * 95.0 for item in densities if item < 4.0 or item > 10.0)
    pocket_penalty = sum(abs(min(0.0, item)) * 0.42 for item in pockets20)
    pocket_penalty += sum(abs(min(0.0, item)) * 0.26 for item in pockets50)
    month_penalty = sum(abs(min(0.0, item)) * 0.18 for item in worst_months)
    water_penalty = sum(max(0.0, item - 0.86) * 180.0 for item in underwater)
    consistency_bonus = sum(1 for item in nets if item > 0.0) / len(nets) * 280.0
    pf_bonus = sum(max(0.0, item - 1.0) * 160.0 for item in pfs)
    recovery_bonus = sum(max(0.0, item) * 18.0 for item in recoveries)
    worst_fold_penalty = abs(min(0.0, min(nets))) * 0.70
    return float(sum(nets) + consistency_bonus + pf_bonus + recovery_bonus - density_penalty - pocket_penalty - month_penalty - water_penalty - worst_fold_penalty)


def choose_wfo_quantile(spec: CandidateSpec, frame: pd.DataFrame) -> tuple[str, float, float, list[dict[str, Any]], dict[str, Any]]:
    fold_scored: list[tuple[str, pd.DataFrame]] = []
    for fold_index, (fold_id, fold_train, fold_validation) in enumerate(train_folds(frame), start=1):
        prepared = train_prepared(spec, fold_train, seed=2910 + fold_index, persist=False)
        fold_scored.append((fold_id, score_edges(prepared, fold_validation)))
    if not fold_scored:
        raise RuntimeError(f"No WFO folds available for {spec.package_id}")
    best: tuple[str, float, float, list[dict[str, Any]], dict[str, Any]] | None = None
    quantiles = np.linspace(0.03, 0.96, 78)
    for orientation in ("direct", "inverse"):
        for quantile in quantiles:
            fold_rows: list[dict[str, Any]] = []
            metrics_list: list[dict[str, Any]] = []
            for fold_id, scored in fold_scored:
                threshold = threshold_for_quantile(scored, float(quantile))
                signal = build_signal(scored, threshold, orientation)
                metrics = s290.curve_metrics(scored, signal, spec.max_hold_bars)
                metrics_list.append(metrics)
                fold_rows.append(
                    {
                        "materialized_branch_id": "",
                        "package_id": spec.package_id,
                        "fold_id": fold_id,
                        "orientation": orientation,
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
                best = (orientation, float(quantile), float(score), fold_rows, summary)
    if best is None:
        raise RuntimeError(f"No WFO selection available for {spec.package_id}")
    return best


def split_metrics(scored: pd.DataFrame, quantile: float, orientation: str, hold_limit: int, split: str) -> tuple[dict[str, Any], np.ndarray, float]:
    part = scored.loc[scored["split"].astype(str).eq(split)].copy()
    train_part = scored.loc[scored["split"].astype(str).eq("train")].copy()
    threshold = threshold_for_quantile(train_part, quantile)
    signal = build_signal(part, threshold, orientation)
    return s290.curve_metrics(part, signal, hold_limit), signal, threshold


def materialize_payload(prepared: PreparedModel, scored: pd.DataFrame, quantile: float, threshold: float, orientation: str) -> tuple[pd.DataFrame, dict[str, Any]]:
    spec = prepared.spec
    signal = build_signal(scored, threshold, orientation)
    runtime = scored.copy()
    branch_id = f"run291A_{spec.package_id.replace('_surface', '')}"
    runtime["stage291_branch_id"] = branch_id
    runtime["stage290_branch_id"] = branch_id
    runtime["materialized_branch_id"] = branch_id
    runtime["package_id"] = spec.package_id
    runtime["queue_role"] = "walk_forward_payoff_generalization_surface"
    runtime["candidate_decision_score"] = runtime["payoff_edge_confidence"].astype(float)
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
        "orientation": orientation,
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
        orientation, quantile, score, fold_rows, wfo_summary = choose_wfo_quantile(spec, frame)
        train = frame.loc[frame["split"].astype(str).eq("train")].copy()
        prepared = train_prepared(spec, train, seed=291, persist=True)
        scored = score_edges(prepared, frame)
        train_scored = scored.loc[scored["split"].astype(str).eq("train")].copy()
        threshold = threshold_for_quantile(train_scored, quantile)
        validation_metrics, _validation_signal, _threshold = split_metrics(scored, quantile, orientation, spec.max_hold_bars, "validation")
        oos_metrics, _oos_signal, _threshold = split_metrics(scored, quantile, orientation, spec.max_hold_bars, "oos")
        payload, surface_identity = materialize_payload(prepared, scored, quantile, threshold, orientation)
        branch_id = f"run291A_{spec.package_id.replace('_surface', '')}"
        payload_path = PAYLOAD_DIR / f"{branch_id}_payload.parquet"
        handoff_path = HANDOFF_DIR / f"{branch_id}_handoff.json"
        io_path(payload_path.parent).mkdir(parents=True, exist_ok=True)
        payload.to_parquet(io_path(payload_path), index=False)
        write_json(
            handoff_path,
            {
                "stage291_branch_id": branch_id,
                "package_id": spec.package_id,
                "model_family": spec.model_family,
                "prediction_kind": spec.prediction_kind,
                "dataset_id": spec.dataset_id,
                "feature_order": prepared.feature_order,
                "feature_order_hash": ordered_hash(prepared.feature_order),
                "selection_quantile": quantile,
                "selection_threshold": threshold,
                "selection_orientation": orientation,
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
                "queue_id": f"run291A_queue_{index:02d}",
                "materialized_branch_id": branch_id,
                "stage291_branch_id": branch_id,
                "stage290_branch_id": branch_id,
                "package_id": spec.package_id,
                "queue_role": "walk_forward_payoff_generalization_surface",
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
                "orientation": orientation,
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
                "stage291_branch_id": branch_id,
                "materialized_branch_id": branch_id,
                "package_id": spec.package_id,
                "idea_id": "IDEA-ST291-WFO-PAYOFF-GENERALIZATION",
                "hypothesis": spec.hypothesis,
                "decision_use": "MT5 runtime probe seed only; no candidate selection until run291B/run291C evidence",
                "comparison_baseline": "Stage290 density-positive but profit/curve-fail runtime scoreboard plus Stage290 failure memory",
                "control_variables": "FPMarkets US100 M5 split_v1; feature_set_v2 proxy58; train/validation/oos windows; single-feature route-signal replay handoff",
                "changed_variables": spec.changed_variables,
                "sample_scope": f"{spec.dataset_id}; train-only WFO folds plus validation/oos proxy read; Tier A and Tier B duplicated for paired runtime accounting",
                "success_criteria": "4-10 trades/day in validation and OOS, positive MT5 net/PF/recovery/expectancy, and no deep local curve pockets",
                "failure_criteria": "MT5 validation or OOS net/PF fails, density outside 4-10, or local curve pockets dominate",
                "invalid_conditions": "payload contains label/future columns, WFO folds missing, model feature order missing, MT5 report missing, or runtime handoff mismatch",
                "stop_conditions": "after full run291B MT5 probe and run291C review; no narrow threshold repair inside Stage291",
                "evidence_plan": "wfo_fold_scoreboard; model_scout_scoreboard; candidate_supply_diagnostics; payload_manifest; mt5_probe_queue; run291B MT5 KPI; run291C curve/time-slice review",
                "model_family": spec.model_family,
                "dataset_id": spec.dataset_id,
                "prediction_kind": spec.prediction_kind,
                "objective_surface": spec.objective_surface,
                "selection_orientation": orientation,
                "selection_quantile": quantile,
                "selection_threshold": threshold,
                "precondition": spec.precondition,
                "risk_logic": f"max_hold_bars={spec.max_hold_bars};close_on_flat_signal=true;same_direction_reentry_cooldown_bars=0",
                "adapter_path": "deferred_until_candidate_survives_run291B_run291C",
                "runtime_handoff": "route_signal_value replay now; model artifact and feature order retained for Adapter package if selected",
                "claim_boundary": BOUNDARY,
            }
        )
        artifacts.extend(
            [
                payload_path,
                handoff_path,
                prepared.model_path,
                prepared.feature_order_path,
                prepared.imputation_path,
            ]
        )
    return branch_rows, scoreboard_rows, supply_rows, manifest_rows, model_rows, wfo_rows, [path for path in artifacts if path]


def report_markdown(scoreboard_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = []
    for row in scoreboard_rows:
        lines.append(
            f"- `{row['package_id']}`: WFO(워크포워드) net `{float(row['wfo_net_bp']):.2f}`bp, positive folds(양수 접힘) "
            f"`{float(row['wfo_positive_fold_share']):.2f}`, validation(검증) `{float(row['validation_proxy_net_bp']):.2f}`bp/"
            f"`{float(row['validation_proxy_trades_per_day']):.2f}` trades/day(일 거래), OOS(표본외) "
            f"`{float(row['oos_proxy_net_bp']):.2f}`bp/`{float(row['oos_proxy_trades_per_day']):.2f}` trades/day(일 거래), "
            f"gates(게이트) `{row['density_gate']}/{row['proxy_edge_gate']}/{row['curve_proxy_gate']}`."
        )
    queue_lines = [
        f"- `{row['package_id']}` -> `{row['materialized_branch_id']}` validation approx `{float(row['approx_validation_trades_per_day']):.2f}`/day, OOS approx `{float(row['approx_oos_trades_per_day']):.2f}`/day"
        for row in manifest_rows
    ]
    return f"""# run291A Walk-forward Payoff Generalization Materialization(291A 워크포워드 손익 일반화 물질화)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- branch_count(분기 수): `{len(manifest_rows)}`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Thesis(논제)

Stage290(290단계)의 가까운 후보는 trade density(거래 밀도)는 맞췄지만 OOS profit scale(표본외 수익 규모), recovery(회복), curve pocket(곡선 포켓)에서 탈락했다. Stage291(291단계)은 validation-only threshold fit(검증 단일 임계값 적합)을 피하기 위해 train-only WFO folds(학습 전용 워크포워드 접힘)로 quantile threshold(분위 임계값)와 orientation(방향)을 고른다.

## Scoreboard(점수판)

{chr(10).join(lines)}

## MT5 Queue(MT5 대기열)

{chr(10).join(queue_lines)}

## Boundary(경계)

선택 후보, Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 아직 주장하지 않는다. 이 산출물은 run291B(291B 실행) MT5 runtime probe(MT5 런타임 탐침) 입력이다.
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
            "hypothesis": "Train-only WFO quantile selection plus side relabel/return objectives can improve OOS profit scale and curve quality while preserving 4-10 trades/day.",
            "decision_use": "Decide whether Stage291 should proceed to full MT5 runtime probe and candidate review.",
            "comparison_baseline": "Stage290 MT5 review: cp290B/cp290E density-positive but profit/recovery/curve-fail, cp290F efficiency-positive but density-fail.",
            "control_variables": "FPMarkets US100 M5, split_v1, feature_set_v2 proxy58, Tier A/B paired runtime accounting, route_signal_value replay.",
            "changed_variables": "train-only WFO fold selection, return regression side relabeling, native curve/cost selection penalties, model family and hold logic.",
            "sample_scope": "fwd12 and fwd18 model input datasets; train WFO folds, validation and OOS proxy reads; MT5 probe pending.",
            "success_criteria": "MT5 validation and OOS both 4-10 trades/day with positive net/PF/recovery/expectancy and no deep curve pockets.",
            "failure_criteria": "density outside target, OOS profit scale below target, recovery below 1, or curve/month/session pockets fail.",
            "invalid_conditions": "missing WFO folds, label/future columns in runtime payload, missing feature order, or MT5 handoff mismatch.",
            "stop_conditions": "complete run291B and run291C, then pivot or select; do not micro-repair thresholds in Stage291.",
            "evidence_plan": "wfo_fold_scoreboard, model_scout_scoreboard, payload manifest, MT5 queue, run291B KPI, run291C curve review.",
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            "datasets": [
                rel(s290.dataset_path("fwd12_proxy58")),
                rel(s290.dataset_path("fwd18_proxy58")),
            ],
            "runtime_payload_label_future_columns_removed": True,
            "train_only_wfo_selection": True,
            "tier_pairing": "Tier A and Tier B duplicated for runtime accounting; actual routed total required in MT5.",
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
                "judgment_class": "materialization_no_candidate",
                "claim_boundary": BOUNDARY,
                "next_condition": NEXT_ACTION,
                "user_explanation_hook": "WFO로 후보 입력은 만들었지만, 실제 후보 여부는 MT5와 곡선 리뷰 뒤에만 말한다.",
            }
        ],
    )
    write_csv(
        GATE_AUDIT,
        GATE_COLUMNS,
        [
            {
                "gate_name": "experiment_design_receipt(실험 설계 영수증)",
                "status": "passed",
                "evidence_path": rel(EXPERIMENT_DESIGN),
                "effect": "가설, 비교 기준, 성공/실패/무효 조건을 먼저 고정했다.",
            },
            {
                "gate_name": "train_only_wfo_selection(학습 전용 워크포워드 선택)",
                "status": "passed",
                "evidence_path": rel(WFO_FOLD_SCOREBOARD),
                "effect": "validation(검증) 창 하나로 threshold(임계값)를 고르지 않게 했다.",
            },
            {
                "gate_name": "runtime_handoff_payload(런타임 인계 페이로드)",
                "status": "passed",
                "evidence_path": rel(PAYLOAD_MANIFEST),
                "effect": "route_signal_value와 feature order(피처 순서)를 추적 가능하게 만들었다.",
            },
            {
                "gate_name": "candidate_claim_boundary(후보 주장 경계)",
                "status": "passed",
                "evidence_path": rel(RESULT_JUDGMENT),
                "effect": "MT5 전에는 후보/어댑터/온엑스를 주장하지 않는다.",
            },
        ],
    )
    write_md(REPORT, report_markdown(scoreboard_rows, manifest_rows))
    final_paths = [
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
            "producer": "stage_pipelines/stage291/design_materialize_walk_forward_payoff_generalization_rebuild.py",
            "source_artifacts": [
                rel(STAGE291_SEED_QUEUE),
                rel(SOURCE_SCOREBOARD),
                rel(SOURCE_FAILURE),
                rel(SOURCE_MODEL_SCOREBOARD),
            ],
            "produced_artifacts": [rel(path) for path in final_paths if path and path_exists(path)],
            "claim_boundary": BOUNDARY,
        },
    )
    final_paths.append(LINEAGE)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "created_at_utc": created_at,
            "branch_count": len(manifest_rows),
            "mt5_queue_rows": len(manifest_rows),
            "selected_candidate": "none",
            "adapter_package": "none",
            "onnx_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "next_action": NEXT_ACTION,
            "claim_boundary": BOUNDARY,
            "output_hashes": {rel(path): sha256_file_lf_normalized(path) for path in final_paths if path and path_exists(path)},
        },
    )
    final_paths.append(RUN_MANIFEST)
    return [path for path in final_paths if path and path_exists(path)]


def update_docs(created_at: str, artifacts: Sequence[Path], manifest_rows: Sequence[Mapping[str, Any]], scoreboard_rows: Sequence[Mapping[str, Any]]) -> None:
    upsert_csv(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "walk_forward_payoff_generalization_materialization",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "notes": f"branches={len(manifest_rows)};next_action={NEXT_ACTION}",
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
                "parent_run_id": "run290C_review_payoff_weighted_edge_model_mt5_probe_v1",
                "record_view": "walk_forward_payoff_generalization_materialization",
                "tier_scope": "Tier A/Tier B paired exploration labels",
                "kpi_scope": "model_proxy_and_runtime_queue",
                "scoreboard_lane": "walk_forward_payoff_generalization",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "primary_kpi": f"mt5_queue_rows={len(manifest_rows)};wfo_fold_rows={len(scoreboard_rows) * 4}",
                "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed",
                "external_verification_status": "out_of_scope_by_claim_run291B_required",
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
                "view": "walk_forward_payoff_generalization_materialization",
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
            "artifact_type": "stage291_walk_forward_payoff_artifact",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run291A walk-forward payoff generalization materialization",
        }
        for path in artifacts
        if path_exists(path)
    ]
    upsert_csv(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")

    selected = io_path(SELECTED).read_text(encoding="utf-8-sig") if path_exists(SELECTED) else ""
    selected = replace_line_prefix(selected, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
    selected = replace_line_prefix(selected, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = append_once(selected, "run291A_report", f"- run291A_report(291A 보고): `{rel(REPORT)}`")
    selected = append_once(selected, "run291A_mt5_queue", f"- run291A_mt5_queue(291A MT5 대기열): `{rel(MT5_QUEUE)}`")
    write_md(SELECTED, selected)

    review_index = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX) else "# Stage291 Review Index(291단계 검토 색인)\n"
    review_index = append_once(review_index, "run291A_report", f"- run291A_report(291A 보고): `{rel(REPORT)}`\n- run291A_mt5_queue(291A MT5 대기열): `{rel(MT5_QUEUE)}`")
    write_md(REVIEW_INDEX, review_index)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig") if path_exists(CURRENT_STATE) else ""
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run291A_summary",
        f"- run291A_summary(291A 요약): train-only WFO quantile selection(학습 전용 워크포워드 분위 선택), side relabel(방향 재라벨), native cost/curve objective(비용/곡선 내장 목적)를 가진 후보 `{len(manifest_rows)}`개를 물질화했다. Effect(효과): MT5 runtime probe(MT5 런타임 탐침)로 수익 규모와 곡선을 검증할 수 있고, 선택 후보/어댑터/온엑스는 아직 주장하지 않는다.",
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig") if path_exists(WORKSPACE_STATE) else ""
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = (
        f"- >-\n"
        f"  Stage291(291단계) run291A(291A 실행) walk-forward payoff generalization materialization(워크포워드 손익 일반화 물질화) `{RUN_ID}`. "
        f"Effect(효과): 후보 `{len(manifest_rows)}`개와 MT5 probe queue(MT5 탐침 대기열)를 만들었고 selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비)는 주장하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_md(WORKSPACE_STATE, workspace)

    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    changelog = append_once(
        changelog,
        RUN_ID,
        f"## {UPDATED_ON} run291A Walk-forward payoff generalization materialization(291A 워크포워드 손익 일반화 물질화)\n\n"
        f"- status(상태): `{STATUS}`\n"
        f"- judgment(판정): `{JUDGMENT}`\n"
        f"- effect(효과): train-only WFO(학습 전용 워크포워드) 후보 `{len(manifest_rows)}`개를 MT5 probe queue(MT5 탐침 대기열)로 만들었다.\n"
        f"- boundary(경계): selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n",
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
                "branch_count": len(manifest_rows),
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
