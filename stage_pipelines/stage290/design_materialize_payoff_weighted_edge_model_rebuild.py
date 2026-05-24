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
from sklearn.ensemble import ExtraTreesClassifier, HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


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


STAGE_ID = "290_onnx_candidate_campaign__payoff_weighted_edge_model_rebuild"
RUN_ID = "run290A_design_materialize_payoff_weighted_edge_model_rebuild_v1"
RUN_NUMBER = "run290A"
STATUS = "completed_payoff_weighted_edge_model_candidates_materialized_no_selection"
JUDGMENT = "payoff_weighted_model_inputs_materialized_no_candidate_selection"
NEXT_ACTION = "run290B_execute_payoff_weighted_edge_model_mt5_probe"
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

FWD12_DATASET = ROOT / "data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet"
FWD18_DATASET = ROOT / "data/processed/model_inputs/label_v1_fwd18_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet"
STAGE290_SEED_QUEUE = STAGE_ROOT / "01_inputs" / "stage290_payoff_weighted_edge_seed_queue.csv"
PRIOR_STAGE_REFS = (
    ROOT / "stages/287_onnx_candidate_campaign__density_scale_curve_pocket_rebuild/03_reviews/run287C_density_scale_curve_pocket_review_stage288_open_report.md",
    ROOT / "stages/288_onnx_candidate_campaign__risk_reward_exit_asymmetry_rebuild/03_reviews/run288C_risk_reward_exit_review_stage289_open_report.md",
    ROOT / "stages/289_onnx_candidate_campaign__regime_conditioned_edge_surface_rebuild/03_reviews/run289C_regime_conditioned_edge_review_stage290_open_report.md",
)

BRANCH_QUEUE = RUN_ROOT / "branch_design_queue.csv"
MODEL_SCOREBOARD = RUN_ROOT / "model_scout_scoreboard.csv"
CANDIDATE_SUPPLY = RUN_ROOT / "candidate_supply_diagnostics.csv"
PAYLOAD_MANIFEST = RUN_ROOT / "candidate_payload_manifest.csv"
MT5_QUEUE = RUN_ROOT / "mt5_probe_queue.csv"
MODEL_MANIFEST = RUN_ROOT / "model_artifact_manifest.csv"
EXPERIMENT_DESIGN = RUN_ROOT / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_ROOT / "data_integrity_receipt.json"
LINEAGE = RUN_ROOT / "artifact_lineage_receipt.json"
RESULT_JUDGMENT = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT = RUN_ROOT / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
REPORT = REVIEWS / "run290A_payoff_weighted_edge_model_materialization_report.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
PRODUCER = Path("stage_pipelines/stage290/design_materialize_payoff_weighted_edge_model_rebuild.py")

LABEL_ORDER = (0, 1, 2)
TRANSACTION_COST_LOGRET = 0.00012
warnings.filterwarnings("ignore", message="Converting to PeriodArray/Index representation")
warnings.filterwarnings("ignore", message="X does not have valid feature names")

BRANCH_COLUMNS = (
    "stage290_branch_id",
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
    "objective_surface",
    "selection_orientation",
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
    "orientation",
    "threshold",
    "precondition",
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
MODEL_MANIFEST_COLUMNS = (
    "materialized_branch_id",
    "package_id",
    "model_family",
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
    dataset_id: str
    max_hold_bars: int
    precondition: str
    sample_weight_policy: str
    objective_surface: str
    hypothesis: str
    changed_variables: str


@dataclass
class PreparedModel:
    spec: CandidateSpec
    model: Any
    feature_order: list[str]
    medians: dict[str, float]
    payoff_units: dict[str, float]
    model_path: Path
    feature_order_path: Path
    imputation_path: Path


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(str(path))
    try:
        return item.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def write_json(path: Path, payload: Any, *, bom: bool = False) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8-sig" if bom else "utf-8",
    )


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
            package_id="cp290A_xgb_payoff_fwd12_density_hold4_surface",
            model_family="xgboost_multiclass_payoff_weighted",
            dataset_id="fwd12_proxy58",
            max_hold_bars=4,
            precondition="all_rows",
            sample_weight_policy="abs_forward_return_x_class_balance",
            objective_surface="payoff_weighted_class_probability_edge",
            hypothesis="Payoff-weighted XGBoost can rank high-frequency long/short edge without inherited route filtering.",
            changed_variables="new XGBoost model; payoff sample weights; validation-selected density threshold; hold4",
        ),
        CandidateSpec(
            package_id="cp290B_lgbm_payoff_cash_hold6_surface",
            model_family="lightgbm_multiclass_payoff_weighted",
            dataset_id="fwd12_proxy58",
            max_hold_bars=6,
            precondition="cash_non_extreme",
            sample_weight_policy="abs_forward_return_x_class_balance_x_recency",
            objective_surface="cash_session_payoff_probability_edge",
            hypothesis="Cash-session payoff weighting can keep 4-10 trades/day while reducing weak-session curve pockets.",
            changed_variables="new LightGBM model; recency/payoff weights; cash non-extreme precondition; hold6",
        ),
        CandidateSpec(
            package_id="cp290C_extratrees_direction_session_hold6_surface",
            model_family="extratrees_multiclass_session_direction",
            dataset_id="fwd12_proxy58",
            max_hold_bars=6,
            precondition="cash_or_late_liquid",
            sample_weight_policy="abs_forward_return_x_class_balance",
            objective_surface="direction_specific_session_edge",
            hypothesis="Session-aware ExtraTrees can capture non-linear direction switches missed by filter-style surfaces.",
            changed_variables="new ExtraTrees model; nonlinear feature interactions; session liquidity precondition; hold6",
        ),
        CandidateSpec(
            package_id="cp290D_logreg_smooth_curve_hold4_surface",
            model_family="elastic_logistic_payoff_proxy",
            dataset_id="fwd12_proxy58",
            max_hold_bars=4,
            precondition="non_extreme_all",
            sample_weight_policy="abs_forward_return_x_class_balance",
            objective_surface="smooth_curve_penalized_linear_edge",
            hypothesis="A simpler linear surface may trade less jaggedly when threshold selection penalizes curve pockets.",
            changed_variables="new scaled logistic model; smoothness-first threshold objective; non-extreme precondition; hold4",
        ),
        CandidateSpec(
            package_id="cp290E_xgb_payoff_fwd18_aggressive_hold8_surface",
            model_family="xgboost_multiclass_payoff_weighted",
            dataset_id="fwd18_proxy58",
            max_hold_bars=8,
            precondition="all_rows",
            sample_weight_policy="abs_forward_return_x_class_balance_x_tail",
            objective_surface="longer_horizon_payoff_edge",
            hypothesis="A longer payoff horizon can improve profit scale while preserving the required trade density.",
            changed_variables="new fwd18 XGBoost model; tail-amplified payoff weights; hold8",
        ),
        CandidateSpec(
            package_id="cp290F_histgb_payoff_defensive_hold5_surface",
            model_family="histgb_multiclass_payoff_weighted",
            dataset_id="fwd12_proxy58",
            max_hold_bars=5,
            precondition="volatility_balanced",
            sample_weight_policy="abs_forward_return_x_class_balance",
            objective_surface="defensive_hist_gradient_payoff_edge",
            hypothesis="Histogram gradient boosting can provide a lower-variance payoff surface than tree ensembles with wider leaves.",
            changed_variables="new HistGradientBoosting model; volatility-balanced precondition; hold5",
        ),
    ]


def dataset_path(dataset_id: str) -> Path:
    if dataset_id == "fwd18_proxy58":
        return FWD18_DATASET
    return FWD12_DATASET


def load_dataset(dataset_id: str) -> pd.DataFrame:
    frame = pd.read_parquet(io_path(dataset_path(dataset_id))).copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    frame = frame.sort_values("timestamp").reset_index(drop=True)
    return frame


def feature_columns(frame: pd.DataFrame) -> list[str]:
    excluded = {
        "timestamp",
        "symbol",
        "future_timestamp",
        "future_log_return_12",
        "label",
        "label_class",
        "label_id",
        "split",
        "split_id",
        "horizon_bars",
        "horizon_minutes",
    }
    return [name for name in frame.columns if name not in excluded and pd.api.types.is_numeric_dtype(frame[name])]


def matrix(frame: pd.DataFrame, features: Sequence[str], medians: Mapping[str, float] | None = None) -> tuple[np.ndarray, dict[str, float]]:
    values = frame.loc[:, list(features)].replace([np.inf, -np.inf], np.nan)
    if medians is None:
        med = values.median(numeric_only=True).fillna(0.0).astype(float).to_dict()
    else:
        med = {str(key): float(value) for key, value in medians.items()}
    values = values.fillna(med)
    return values.astype("float32").to_numpy(), med


def class_balance_weights(labels: np.ndarray) -> np.ndarray:
    labels = labels.astype(int)
    counts = {label: max(1, int((labels == label).sum())) for label in LABEL_ORDER}
    total = float(len(labels))
    return np.asarray([total / (len(LABEL_ORDER) * counts[int(label)]) for label in labels], dtype="float64")


def sample_weights(train: pd.DataFrame, policy: str) -> np.ndarray:
    returns = train["future_log_return_12"].astype(float).to_numpy()
    scale = float(np.nanmedian(np.abs(returns)))
    if not np.isfinite(scale) or scale <= 0.0:
        scale = 0.001
    magnitude = np.clip(np.abs(returns) / scale, 0.25, 6.0)
    if "tail" in policy:
        magnitude = np.power(magnitude, 1.25)
    weights = 1.0 + magnitude
    weights *= class_balance_weights(train["label_class"].astype(int).to_numpy())
    if "recency" in policy:
        order = np.linspace(0.80, 1.25, len(weights), dtype="float64")
        weights *= order
    return weights.astype("float64")


def payoff_units(train: pd.DataFrame) -> dict[str, float]:
    returns = train["future_log_return_12"].astype(float)
    long_unit = float(returns.loc[train["label_class"].eq(2)].clip(lower=0).mean())
    short_unit = float((-returns.loc[train["label_class"].eq(0)]).clip(lower=0).mean())
    if not np.isfinite(long_unit) or long_unit <= 0:
        long_unit = float(np.nanmean(np.abs(returns))) or 0.001
    if not np.isfinite(short_unit) or short_unit <= 0:
        short_unit = float(np.nanmean(np.abs(returns))) or 0.001
    flat_penalty = float(returns.loc[train["label_class"].eq(1)].abs().mean())
    if not np.isfinite(flat_penalty):
        flat_penalty = 0.0
    return {"long_unit": long_unit, "short_unit": short_unit, "flat_penalty": flat_penalty}


def train_model(spec: CandidateSpec, frame: pd.DataFrame) -> PreparedModel:
    features = feature_columns(frame)
    train = frame.loc[frame["split"].astype(str).eq("train")].copy()
    x_train, medians = matrix(train, features)
    y_train = train["label_class"].astype(int).to_numpy()
    weights = sample_weights(train, spec.sample_weight_policy)
    if spec.model_family.startswith("xgboost"):
        from xgboost import XGBClassifier

        model = XGBClassifier(
            n_estimators=220,
            max_depth=3,
            learning_rate=0.045,
            subsample=0.86,
            colsample_bytree=0.82,
            objective="multi:softprob",
            eval_metric="mlogloss",
            num_class=3,
            tree_method="hist",
            random_state=290,
            n_jobs=-1,
            verbosity=0,
        )
    elif spec.model_family.startswith("lightgbm"):
        from lightgbm import LGBMClassifier

        model = LGBMClassifier(
            objective="multiclass",
            num_class=3,
            n_estimators=260,
            learning_rate=0.035,
            max_depth=4,
            num_leaves=18,
            min_child_samples=70,
            subsample=0.86,
            colsample_bytree=0.80,
            random_state=290,
            n_jobs=-1,
            verbose=-1,
        )
    elif spec.model_family.startswith("extratrees"):
        model = ExtraTreesClassifier(
            n_estimators=420,
            max_features=0.55,
            min_samples_leaf=24,
            class_weight="balanced_subsample",
            random_state=290,
            n_jobs=-1,
        )
    elif spec.model_family.startswith("histgb"):
        model = HistGradientBoostingClassifier(
            max_iter=170,
            learning_rate=0.045,
            max_leaf_nodes=18,
            l2_regularization=0.08,
            min_samples_leaf=55,
            random_state=290,
        )
    else:
        model = make_pipeline(
            StandardScaler(),
            LogisticRegression(
                C=0.35,
                penalty="l2",
                class_weight="balanced",
                max_iter=1200,
                random_state=290,
            ),
        )
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        if hasattr(model, "named_steps"):
            last_step = list(model.named_steps)[-1]
            model.fit(x_train, y_train, **{f"{last_step}__sample_weight": weights})
        else:
            model.fit(x_train, y_train, sample_weight=weights)
    model_path = MODEL_DIR / f"{spec.package_id}.joblib"
    feature_order_path = MODEL_DIR / f"{spec.package_id}_feature_order.txt"
    imputation_path = MODEL_DIR / f"{spec.package_id}_imputation.json"
    io_path(MODEL_DIR).mkdir(parents=True, exist_ok=True)
    joblib.dump(model, io_path(model_path))
    io_path(feature_order_path).write_text("\n".join(features) + "\n", encoding="utf-8")
    write_json(imputation_path, {"feature_order": features, "medians": medians})
    return PreparedModel(
        spec=spec,
        model=model,
        feature_order=features,
        medians=medians,
        payoff_units=payoff_units(train),
        model_path=model_path,
        feature_order_path=feature_order_path,
        imputation_path=imputation_path,
    )


def ordered_probabilities(model: Any, values: np.ndarray) -> np.ndarray:
    raw = np.asarray(model.predict_proba(values), dtype="float64")
    classes = getattr(model, "classes_", None)
    if classes is None and hasattr(model, "named_steps"):
        for step in reversed(list(model.named_steps.values())):
            if hasattr(step, "classes_"):
                classes = step.classes_
                break
    if classes is None:
        raise ValueError("model lacks classes_")
    class_to_index = {int(label): index for index, label in enumerate(classes)}
    ordered = np.zeros((len(raw), len(LABEL_ORDER)), dtype="float64")
    for out_index, label in enumerate(LABEL_ORDER):
        ordered[:, out_index] = raw[:, class_to_index[int(label)]]
    return ordered


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
        return ((cash & (minutes <= 390)) | (minutes >= 300)) & (zabs <= 2.20)
    if name == "non_extreme_all":
        return (zabs <= 1.65) & (vol <= 1.75)
    if name == "volatility_balanced":
        return (vol >= 0.55) & (vol <= 1.60) & (zabs <= 2.05)
    return np.ones(rows, dtype=bool)


def score_edges(prepared: PreparedModel, frame: pd.DataFrame) -> pd.DataFrame:
    x_values, _ = matrix(frame, prepared.feature_order, prepared.medians)
    proba = ordered_probabilities(prepared.model, x_values)
    units = prepared.payoff_units
    edge = (
        proba[:, 2] * units["long_unit"]
        - proba[:, 0] * units["short_unit"]
        - proba[:, 1] * units["flat_penalty"] * 0.20
    )
    confidence = np.abs(edge) * np.clip(1.0 - proba[:, 1] * 0.35, 0.10, 1.0)
    direction = np.where(edge >= 0.0, 1, -1).astype("int8")
    out = frame.copy()
    out["prob_short"] = proba[:, 0]
    out["prob_flat"] = proba[:, 1]
    out["prob_long"] = proba[:, 2]
    out["payoff_edge_score"] = edge
    out["payoff_edge_confidence"] = confidence
    out["payoff_edge_direction"] = direction
    out["precondition_pass"] = precondition_mask(out, prepared.spec.precondition).astype("int8")
    return out


def signal_label(value: int) -> str:
    return "long" if value > 0 else "short" if value < 0 else "flat"


def build_signal(scored: pd.DataFrame, threshold: float, orientation: str) -> np.ndarray:
    direction = scored["payoff_edge_direction"].astype("int8").to_numpy()
    if orientation == "inverse":
        direction = (-direction).astype("int8")
    active = (
        scored["payoff_edge_confidence"].astype(float).to_numpy() >= float(threshold)
    ) & scored["precondition_pass"].astype(bool).to_numpy()
    return np.where(active, direction, 0).astype("int8")


def trade_records(timestamps: Sequence[pd.Timestamp], returns: Sequence[float], signal: Sequence[int], hold_limit: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    position = 0
    hold = 0
    for timestamp, future_return, raw_signal in zip(timestamps, returns, signal):
        current = int(raw_signal)
        if position == 0:
            if current:
                profit = (float(future_return) * current) - TRANSACTION_COST_LOGRET
                rows.append({"timestamp": timestamp, "direction": current, "profit_bp": profit * 10000.0})
                position = current
                hold = 1
            continue
        hold += 1
        if current == 0:
            position = 0
            hold = 0
        elif current == -position:
            profit = (float(future_return) * current) - TRANSACTION_COST_LOGRET
            rows.append({"timestamp": timestamp, "direction": current, "profit_bp": profit * 10000.0})
            position = current
            hold = 1
        elif hold >= hold_limit:
            position = 0
            hold = 0
    return rows


def profit_factor(values: Sequence[float]) -> float:
    gross_profit = sum(value for value in values if value > 0)
    gross_loss = sum(value for value in values if value < 0)
    if gross_loss < 0:
        return float(gross_profit / abs(gross_loss))
    return 9.99 if gross_profit > 0 else 0.0


def rolling_min(values: Sequence[float], window: int) -> float:
    if len(values) < window:
        return 0.0
    return float(pd.Series([float(value) for value in values]).rolling(window).sum().min())


def curve_metrics(scored: pd.DataFrame, signal: np.ndarray, hold_limit: int) -> dict[str, Any]:
    records = trade_records(
        pd.to_datetime(scored["timestamp"], utc=True).tolist(),
        scored["future_log_return_12"].astype(float).tolist(),
        signal.tolist(),
        hold_limit,
    )
    values = [float(row["profit_bp"]) for row in records]
    days = int(pd.to_datetime(scored["timestamp"], utc=True).dt.date.nunique())
    balance = 0.0
    peak = 0.0
    max_dd = 0.0
    underwater = 0
    for value in values:
        balance += value
        peak = max(peak, balance)
        dd = peak - balance
        max_dd = max(max_dd, dd)
        if balance < peak:
            underwater += 1
    trade_frame = pd.DataFrame(records)
    if not trade_frame.empty:
        trade_frame["timestamp"] = pd.to_datetime(trade_frame["timestamp"], utc=True)
        trade_frame["month"] = trade_frame["timestamp"].dt.to_period("M").astype(str)
        month_net = trade_frame.groupby("month")["profit_bp"].sum()
        positive_month_share = float((month_net > 0).sum() / len(month_net)) if len(month_net) else 0.0
        worst_month = float(month_net.min()) if len(month_net) else 0.0
    else:
        positive_month_share = 0.0
        worst_month = 0.0
    return {
        "net_bp": float(sum(values)),
        "pf": profit_factor(values),
        "trade_count": len(values),
        "trades_per_day": float(len(values) / days) if days else 0.0,
        "max_drawdown_bp": max_dd,
        "recovery": float(sum(values) / max_dd) if max_dd > 0 else (9.99 if sum(values) > 0 else 0.0),
        "worst_month_bp": worst_month,
        "worst_rolling_20_bp": rolling_min(values, 20),
        "worst_rolling_50_bp": rolling_min(values, 50),
        "positive_month_share": positive_month_share,
        "underwater_ratio": float(underwater / len(values)) if values else 0.0,
    }


def selection_score(metrics: Mapping[str, Any]) -> float:
    density = float(metrics["trades_per_day"])
    density_penalty = abs(density - 7.0) * 35.0
    pocket_penalty = abs(min(0.0, float(metrics["worst_rolling_20_bp"]))) * 0.60
    pocket_penalty += abs(min(0.0, float(metrics["worst_rolling_50_bp"]))) * 0.35
    month_penalty = abs(min(0.0, float(metrics["worst_month_bp"]))) * 0.25
    underwater_penalty = max(0.0, float(metrics["underwater_ratio"]) - 0.82) * 250.0
    pf_bonus = max(0.0, float(metrics["pf"]) - 1.0) * 240.0
    recovery_bonus = max(0.0, float(metrics["recovery"])) * 35.0
    return float(metrics["net_bp"]) + pf_bonus + recovery_bonus - density_penalty - pocket_penalty - month_penalty - underwater_penalty


def threshold_grid(confidence: np.ndarray, mask: np.ndarray) -> list[float]:
    active_conf = np.asarray(confidence[mask], dtype="float64")
    active_conf = active_conf[np.isfinite(active_conf)]
    if len(active_conf) == 0:
        return [0.0]
    quantiles = np.linspace(0.01, 0.98, 70)
    values = sorted({float(np.quantile(active_conf, q)) for q in quantiles})
    values.insert(0, float(np.nanmin(active_conf)) - 1e-12)
    return values


def choose_threshold(scored: pd.DataFrame, spec: CandidateSpec) -> tuple[str, float, dict[str, Any], np.ndarray, float]:
    validation = scored.loc[scored["split"].astype(str).eq("validation")].copy()
    mask = validation["precondition_pass"].astype(bool).to_numpy()
    grid = threshold_grid(validation["payoff_edge_confidence"].astype(float).to_numpy(), mask)
    best: tuple[str, float, dict[str, Any], np.ndarray, float] | None = None
    for orientation in ("direct", "inverse"):
        for threshold in grid:
            signal = build_signal(validation, threshold, orientation)
            metrics = curve_metrics(validation, signal, spec.max_hold_bars)
            density_ok = 4.0 <= float(metrics["trades_per_day"]) <= 10.0
            score = selection_score(metrics)
            if not density_ok:
                score -= 900.0 + abs(float(metrics["trades_per_day"]) - 7.0) * 120.0
            if best is None or score > best[4]:
                best = (orientation, float(threshold), metrics, signal, float(score))
    if best is None:
        empty = np.zeros(len(validation), dtype="int8")
        return "direct", 0.0, curve_metrics(validation, empty, spec.max_hold_bars), empty, -999999.0
    return best


def split_metrics(scored: pd.DataFrame, threshold: float, orientation: str, hold_limit: int, split: str) -> tuple[dict[str, Any], np.ndarray]:
    part = scored.loc[scored["split"].astype(str).eq(split)].copy()
    signal = build_signal(part, threshold, orientation)
    return curve_metrics(part, signal, hold_limit), signal


def materialize_payload(prepared: PreparedModel, scored: pd.DataFrame, threshold: float, orientation: str) -> tuple[pd.DataFrame, dict[str, Any]]:
    spec = prepared.spec
    signal = build_signal(scored, threshold, orientation)
    runtime = scored.copy()
    runtime["stage290_branch_id"] = f"run290A_{spec.package_id.replace('_surface', '')}"
    runtime["materialized_branch_id"] = runtime["stage290_branch_id"]
    runtime["package_id"] = spec.package_id
    runtime["queue_role"] = "payoff_weighted_edge_model_surface"
    runtime["candidate_decision_score"] = runtime["payoff_edge_confidence"].astype(float)
    runtime["route_signal_value"] = signal
    runtime["route_signal_label"] = [signal_label(int(value)) for value in signal]
    runtime["signal_active"] = (signal != 0).astype("int8")
    runtime["model_risk_pct"] = 0.01
    runtime["max_hold_bars"] = spec.max_hold_bars
    runtime["close_on_flat_signal"] = True
    runtime["same_direction_reentry_cooldown_bars"] = 0
    surface_identity = {
        "package_id": spec.package_id,
        "model_family": spec.model_family,
        "dataset_id": spec.dataset_id,
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


def approximate_trades(signal: np.ndarray, hold_limit: int) -> int:
    trades = 0
    position = 0
    hold = 0
    for raw_value in signal.astype("int8"):
        current = int(raw_value)
        if position == 0:
            if current:
                trades += 1
                position = current
                hold = 1
            continue
        hold += 1
        if current == 0:
            position = 0
            hold = 0
        elif current == -position:
            trades += 1
            position = current
            hold = 1
        elif hold >= hold_limit:
            position = 0
            hold = 0
    return trades


def supply_rows_for_payload(payload: pd.DataFrame, spec: CandidateSpec) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for (tier, split), group in payload.groupby(["tier_scope", "split"], sort=False):
        if split not in {"validation", "oos"}:
            continue
        signal = pd.to_numeric(group["route_signal_value"], errors="coerce").fillna(0).astype("int8").to_numpy()
        days = int(pd.to_datetime(group["timestamp"], utc=True).dt.date.nunique())
        approx = approximate_trades(signal, spec.max_hold_bars)
        rows.append(
            {
                "materialized_branch_id": str(group["materialized_branch_id"].iloc[0]),
                "package_id": spec.package_id,
                "tier_scope": tier,
                "split": split,
                "days": days,
                "rows": len(group),
                "active_signal_count": int((signal != 0).sum()),
                "active_signals_per_day": float((signal != 0).sum() / days) if days else 0.0,
                "long_signal_count": int((signal == 1).sum()),
                "short_signal_count": int((signal == -1).sum()),
                "max_hold_bars": spec.max_hold_bars,
                "approx_trade_count": approx,
                "approx_trades_per_day": float(approx / days) if days else 0.0,
                "trade_density_screen": "in_target_band" if days and 4.0 <= (approx / days) <= 10.0 else "outside_target_band",
            }
        )
    return rows


def gate_label(metrics: Mapping[str, Any], oos_metrics: Mapping[str, Any], gate: str) -> str:
    if gate == "density":
        ok = 4.0 <= float(metrics["trades_per_day"]) <= 10.0 and 4.0 <= float(oos_metrics["trades_per_day"]) <= 10.0
    elif gate == "edge":
        ok = float(metrics["net_bp"]) > 0.0 and float(metrics["pf"]) >= 1.02 and float(oos_metrics["net_bp"]) > -250.0
    else:
        ok = (
            float(metrics["worst_rolling_20_bp"]) >= -280.0
            and float(metrics["positive_month_share"]) >= 0.45
            and float(metrics["underwater_ratio"]) <= 0.92
        )
    return "passed" if ok else "failed"


def build_outputs() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[Path]]:
    branch_rows: list[dict[str, Any]] = []
    scoreboard_rows: list[dict[str, Any]] = []
    supply_rows: list[dict[str, Any]] = []
    manifest_rows: list[dict[str, Any]] = []
    model_rows: list[dict[str, Any]] = []
    gate_seed_rows: list[dict[str, Any]] = []
    artifacts: list[Path] = []
    dataset_cache: dict[str, pd.DataFrame] = {}
    for index, spec in enumerate(candidate_specs(), start=1):
        frame = dataset_cache.setdefault(spec.dataset_id, load_dataset(spec.dataset_id))
        prepared = train_model(spec, frame)
        scored = score_edges(prepared, frame)
        orientation, threshold, validation_metrics, _validation_signal, score = choose_threshold(scored, spec)
        oos_metrics, _oos_signal = split_metrics(scored, threshold, orientation, spec.max_hold_bars, "oos")
        payload, surface_identity = materialize_payload(prepared, scored, threshold, orientation)
        branch_id = f"run290A_{spec.package_id.replace('_surface', '')}"
        payload_path = PAYLOAD_DIR / f"{branch_id}_payload.parquet"
        handoff_path = HANDOFF_DIR / f"{branch_id}_handoff.json"
        io_path(payload_path.parent).mkdir(parents=True, exist_ok=True)
        payload.to_parquet(io_path(payload_path), index=False)
        write_json(
            handoff_path,
            {
                "stage290_branch_id": branch_id,
                "package_id": spec.package_id,
                "model_family": spec.model_family,
                "dataset_id": spec.dataset_id,
                "feature_order": prepared.feature_order,
                "feature_order_hash": ordered_hash(prepared.feature_order),
                "selection_threshold": threshold,
                "selection_orientation": orientation,
                "precondition": spec.precondition,
                "max_hold_bars": spec.max_hold_bars,
                "close_on_flat_signal": True,
                "runtime_handoff": "precomputed route_signal_value replay for MT5 probe; model artifact retained for Adapter/ONNX if candidate survives",
                "claim_boundary": BOUNDARY,
                "surface_identity": surface_identity,
            },
        )
        candidate_supply = supply_rows_for_payload(payload, spec)
        supply_rows.extend(candidate_supply)
        val_supply = next(row for row in candidate_supply if row["tier_scope"] == "Tier A" and row["split"] == "validation")
        oos_supply = next(row for row in candidate_supply if row["tier_scope"] == "Tier A" and row["split"] == "oos")
        manifest_rows.append(
            {
                "queue_id": f"run290A_queue_{index:02d}",
                "materialized_branch_id": branch_id,
                "stage290_branch_id": branch_id,
                "package_id": spec.package_id,
                "queue_role": "payoff_weighted_edge_model_surface",
                "payload_path": rel(payload_path),
                "payload_hash": sha256_file_lf_normalized(payload_path),
                "handoff_path": rel(handoff_path),
                "handoff_hash": sha256_file_lf_normalized(handoff_path),
                "model_artifact_path": rel(prepared.model_path),
                "model_artifact_hash": sha256_file_lf_normalized(prepared.model_path),
                "model_feature_order_path": rel(prepared.feature_order_path),
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
                "dataset_id": spec.dataset_id,
                "model_artifact_path": rel(prepared.model_path),
                "model_artifact_hash": sha256_file_lf_normalized(prepared.model_path),
                "model_feature_order_path": rel(prepared.feature_order_path),
                "model_feature_order_hash": ordered_hash(prepared.feature_order),
                "imputation_path": rel(prepared.imputation_path),
                "imputation_hash": sha256_file_lf_normalized(prepared.imputation_path),
                "classes": "|".join(str(item) for item in LABEL_ORDER),
                "payoff_weight_policy": spec.sample_weight_policy,
                "onnx_exportability_note": "candidate model family has project ONNX path or known converter path; export deferred until candidate package gate",
            }
        )
        scoreboard_rows.append(
            {
                "materialized_branch_id": branch_id,
                "package_id": spec.package_id,
                "dataset_id": spec.dataset_id,
                "model_family": spec.model_family,
                "orientation": orientation,
                "threshold": threshold,
                "precondition": spec.precondition,
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
                "selection_score": score,
                "selected_candidate": "none",
                "adapter_package": "none",
                "onnx_readiness": "not_claimed",
                "claim_boundary": BOUNDARY,
            }
        )
        branch_rows.append(
            {
                "stage290_branch_id": branch_id,
                "materialized_branch_id": branch_id,
                "package_id": spec.package_id,
                "idea_id": "IDEA-ST290-PAYOFF-WEIGHTED-EDGE-MODEL",
                "hypothesis": spec.hypothesis,
                "decision_use": "MT5 runtime probe seed only; no candidate selection until run290B/run290C evidence",
                "comparison_baseline": "Stage287/288/289 no-candidate failure memory and Stage289 density-pass/profit-fail scoreboard",
                "control_variables": "FPMarkets US100 M5 split_v1; feature_set_v2 proxy58; validation/oos splits; single-feature route-signal replay handoff",
                "changed_variables": spec.changed_variables,
                "sample_scope": f"{spec.dataset_id}; train/validation/oos; Tier A and Tier B duplicated for paired runtime accounting",
                "success_criteria": "4-10 trades/day in validation and OOS, positive MT5 net/PF/recovery/expectancy, no deep local curve pockets",
                "failure_criteria": "MT5 validation or OOS net/PF fails, density outside 4-10, or local curve pockets dominate",
                "invalid_conditions": "payload contains label/future columns, missing model feature order, MT5 report missing, or runtime handoff mismatch",
                "stop_conditions": "after full run290B MT5 probe and run290C review; no narrow threshold repair inside Stage290",
                "evidence_plan": "model_scout_scoreboard; candidate_supply_diagnostics; payload_manifest; mt5_probe_queue; run290B MT5 KPI; run290C curve/time-slice review",
                "model_family": spec.model_family,
                "dataset_id": spec.dataset_id,
                "objective_surface": spec.objective_surface,
                "selection_orientation": orientation,
                "selection_threshold": threshold,
                "precondition": spec.precondition,
                "risk_logic": f"max_hold_bars={spec.max_hold_bars};close_on_flat_signal=true;same_direction_reentry_cooldown_bars=0",
                "adapter_path": "deferred_until_candidate_survives_run290B_run290C",
                "runtime_handoff": "route_signal_value replay now; model artifact and feature order retained for Adapter package if selected",
                "claim_boundary": BOUNDARY,
            }
        )
        gate_seed_rows.append({"package_id": spec.package_id, "score": score})
        artifacts.extend(
            [
                payload_path,
                handoff_path,
                prepared.model_path,
                prepared.feature_order_path,
                prepared.imputation_path,
            ]
        )
    return branch_rows, scoreboard_rows, supply_rows, manifest_rows, model_rows, gate_seed_rows, artifacts


def report_markdown(scoreboard_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = []
    for row in sorted(scoreboard_rows, key=lambda item: float(item["selection_score"]), reverse=True):
        lines.append(
            "- `{package}`: validation proxy(검증 대리) net `{vnet:.1f}`bp PF `{vpf:.2f}` "
            "tpd `{vtpd:.2f}`, OOS proxy(표본외 대리) net `{onet:.1f}`bp PF `{opf:.2f}` "
            "tpd `{otpd:.2f}`, gates(게이트) `{density}/{edge}/{curve}`.".format(
                package=row["package_id"],
                vnet=float(row["validation_proxy_net_bp"]),
                vpf=float(row["validation_proxy_pf"]),
                vtpd=float(row["validation_proxy_trades_per_day"]),
                onet=float(row["oos_proxy_net_bp"]),
                opf=float(row["oos_proxy_pf"]),
                otpd=float(row["oos_proxy_trades_per_day"]),
                density=row["density_gate"],
                edge=row["proxy_edge_gate"],
                curve=row["curve_proxy_gate"],
            )
        )
    queue_lines = [
        f"- `{row['package_id']}`: validation approx(검증 근사) `{float(row['approx_validation_trades_per_day']):.2f}`, "
        f"OOS approx(표본외 근사) `{float(row['approx_oos_trades_per_day']):.2f}` trades/day(일 거래)."
        for row in manifest_rows
    ]
    return f"""# run290A Payoff Weighted Edge Model Materialization(290A 손익가중 엣지 모델 물질화)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- branch_count(분기 수): `{len(manifest_rows)}`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Fresh Thesis(새 논제)

Inherited signal filtering(계승 신호 필터링)을 더 깎지 않고, payoff-weighted model surface(손익가중 모델 표면)가 trade density(거래 밀도), profit scale(수익 규모), curve smoothness(곡선 매끈함)를 같이 만들 수 있는지 본다.

## Proxy Scoreboard(대리 점수판)

{chr(10).join(lines)}

## MT5 Queue(MT5 대기열)

{chr(10).join(queue_lines)}

## Boundary(경계)

`{BOUNDARY}`
"""


def write_outputs(
    branch_rows: Sequence[Mapping[str, Any]],
    scoreboard_rows: Sequence[Mapping[str, Any]],
    supply_rows: Sequence[Mapping[str, Any]],
    manifest_rows: Sequence[Mapping[str, Any]],
    model_rows: Sequence[Mapping[str, Any]],
    artifacts: Sequence[Path],
    created_at: str,
) -> list[Path]:
    for path in (RUN_ROOT, PAYLOAD_DIR, MODEL_DIR, HANDOFF_DIR, REVIEWS):
        io_path(path).mkdir(parents=True, exist_ok=True)
    write_csv(BRANCH_QUEUE, BRANCH_COLUMNS, branch_rows)
    write_csv(MODEL_SCOREBOARD, SCOREBOARD_COLUMNS, scoreboard_rows)
    write_csv(CANDIDATE_SUPPLY, SUPPLY_COLUMNS, supply_rows)
    write_csv(PAYLOAD_MANIFEST, MANIFEST_COLUMNS, manifest_rows)
    write_csv(MT5_QUEUE, MANIFEST_COLUMNS, manifest_rows)
    write_csv(MODEL_MANIFEST, MODEL_MANIFEST_COLUMNS, model_rows)
    write_json(
        EXPERIMENT_DESIGN,
        {
            "hypothesis": "Payoff-weighted model surfaces can replace inherited filtering and create an ONNX-worthy candidate seed.",
            "decision_use": "Decide whether Stage290 should proceed to full MT5 runtime probe and candidate review.",
            "comparison_baseline": [rel(path) for path in PRIOR_STAGE_REFS],
            "control_variables": "US100 M5 split_v1, proxy58 feature order, validation/OOS windows, MT5 route-signal replay contract",
            "changed_variables": "model family, payoff weighting, threshold objective, precondition, hold bars",
            "sample_scope": "Tier A/Tier B paired exploration labels with fwd12 and fwd18 proxy58 model inputs",
            "success_criteria": "4-10 trades/day and positive/credible MT5 net PF recovery expectancy with smooth curve",
            "failure_criteria": "profit scale too weak, PF/recovery below credible level, density outside band, or deep local curve pockets",
            "invalid_conditions": "future/label columns in runtime payload, model feature order missing, MT5 report missing, or handoff mismatch",
            "stop_conditions": "complete run290B and run290C, then pivot or select; do not micro-repair thresholds in this stage",
            "evidence_plan": [rel(MODEL_SCOREBOARD), rel(CANDIDATE_SUPPLY), rel(MT5_QUEUE), "run290B MT5 KPI", "run290C review"],
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            "datasets": [rel(FWD12_DATASET), rel(FWD18_DATASET)],
            "runtime_payload_label_future_columns_removed": True,
            "feature_order_sources": [row["model_feature_order_path"] for row in model_rows],
            "tier_scope": "Tier A and Tier B duplicated for paired exploration accounting; profit attribution deferred to actual routed total",
            "claim_boundary": BOUNDARY,
        },
    )
    write_csv(
        RESULT_JUDGMENT,
        RESULT_COLUMNS,
        [
            {
                "result_subject": RUN_ID,
                "evidence_available": f"model_rows={len(model_rows)};mt5_queue_rows={len(manifest_rows)};report={rel(REPORT)}",
                "evidence_missing": "MT5 runtime KPI; trade report curve review; candidate package; Adapter package; ONNX parity",
                "judgment_label": JUDGMENT,
                "judgment_class": "structural_scout(구조 스카우트)",
                "claim_boundary": BOUNDARY,
                "next_condition": NEXT_ACTION,
                "user_explanation_hook": "모델 후보 입력은 만들어졌지만 실제 MT5 성능 검토 전에는 후보가 아니다.",
            }
        ],
    )
    write_csv(
        GATE_AUDIT,
        GATE_COLUMNS,
        [
            {
                "gate_name": "fresh_thesis(새 논제)",
                "status": "passed",
                "evidence_path": rel(EXPERIMENT_DESIGN),
                "effect": "계승 필터 수선이 아니라 새 모델 목적함수와 손익가중 표면을 만들었다.",
            },
            {
                "gate_name": "runtime_payload_hygiene(런타임 페이로드 위생)",
                "status": "passed",
                "evidence_path": rel(DATA_RECEIPT),
                "effect": "label/future(라벨/미래) 컬럼을 런타임 페이로드에서 제거해 누수 주장을 막는다.",
            },
            {
                "gate_name": "candidate_claim_boundary(후보 주장 경계)",
                "status": "passed",
                "evidence_path": rel(RESULT_JUDGMENT),
                "effect": "선택 후보, Adapter, ONNX 준비를 아직 주장하지 않는다.",
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
        EXPERIMENT_DESIGN,
        DATA_RECEIPT,
        RESULT_JUDGMENT,
        GATE_AUDIT,
        REPORT,
        *artifacts,
    ]
    write_json(
        LINEAGE,
        {
            "run_id": RUN_ID,
            "producer": PRODUCER.as_posix(),
            "source_artifacts": [rel(STAGE290_SEED_QUEUE), rel(FWD12_DATASET), rel(FWD18_DATASET), *[rel(path) for path in PRIOR_STAGE_REFS]],
            "produced_artifacts": [rel(path) for path in final if path_exists(path)],
            "claim_boundary": BOUNDARY,
        },
    )
    final.append(LINEAGE)
    write_json(
        RUN_MANIFEST,
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
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
                "lane": "payoff_weighted_edge_model_materialization",
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
                "parent_run_id": "run289C_review_regime_conditioned_edge_mt5_probe_v1",
                "record_view": "payoff_weighted_edge_model_materialization",
                "tier_scope": "Tier A/Tier B/Tier A+B",
                "kpi_scope": "structural_scout",
                "scoreboard_lane": "payoff_weighted_edge_model",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "primary_kpi": f"mt5_queue_rows={len(manifest_rows)}",
                "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed",
                "external_verification_status": "not_attempted_run290A_materialization",
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
                "view": "payoff_weighted_edge_model_materialization",
                "tier_scope": "Tier A/Tier B/Tier A+B",
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
            "artifact_type": "stage290_payoff_weighted_edge_artifact",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run290A payoff weighted edge model materialization",
        }
        for path in artifacts
        if path_exists(path)
    ]
    upsert_csv(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")

    selected = io_path(SELECTED).read_text(encoding="utf-8-sig") if path_exists(SELECTED) else ""
    selected = replace_line_prefix(selected, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
    selected = replace_line_prefix(selected, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = append_once(selected, "run290A_report", f"- run290A_report(290A 보고): `{rel(REPORT)}`")
    selected = append_once(selected, "run290A_mt5_queue", f"- run290A_mt5_queue(290A MT5 대기열): `{rel(MT5_QUEUE)}`")
    write_md(SELECTED, selected)

    review_index = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX) else "# Stage290 Review Index(290단계 검토 색인)\n"
    review_index = append_once(review_index, "run290A_report", f"- run290A_report(290A 보고): `{rel(REPORT)}`")
    write_md(REVIEW_INDEX, review_index)

    best = max(scoreboard_rows, key=lambda row: float(row["selection_score"]))
    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig") if path_exists(CURRENT_STATE) else ""
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run290A_summary",
        f"- run290A_summary(290A 요약): payoff-weighted edge model(손익가중 엣지 모델) 후보 `{len(manifest_rows)}`개를 물질화했다. Effect(효과): best proxy(최고 대리 점수)는 `{best['package_id']}`지만, MT5 runtime probe(MT5 런타임 탐침) 전에는 선택 후보가 아니다.",
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig") if path_exists(WORKSPACE_STATE) else ""
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = (
        f"- >-\n"
        f"  Stage290(290단계) run290A(290A 실행) payoff-weighted edge model materialization(손익가중 엣지 모델 물질화) `{RUN_ID}`. "
        f"Effect(효과): 모델/페이로드 후보 `{len(manifest_rows)}`개와 MT5 probe queue(MT5 탐침 대기열)를 만들었고 selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비)는 주장하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_md(WORKSPACE_STATE, workspace)

    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    changelog = append_once(
        changelog,
        RUN_ID,
        f"## {UPDATED_ON} run290A Payoff-weighted edge model materialization(290A 손익가중 엣지 모델 물질화)\n\n"
        f"- status(상태): `{STATUS}`\n"
        f"- judgment(판정): `{JUDGMENT}`\n"
        f"- effect(효과): model surface(모델 표면) `{len(manifest_rows)}`개를 MT5 probe queue(MT5 탐침 대기열)로 만들었다.\n"
        f"- boundary(경계): selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n",
    )
    write_md(CHANGELOG, changelog)


def main() -> None:
    created_at = utc_now()
    branch_rows, scoreboard_rows, supply_rows, manifest_rows, model_rows, _gate_seed_rows, payload_artifacts = build_outputs()
    artifacts = write_outputs(branch_rows, scoreboard_rows, supply_rows, manifest_rows, model_rows, payload_artifacts, created_at)
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
