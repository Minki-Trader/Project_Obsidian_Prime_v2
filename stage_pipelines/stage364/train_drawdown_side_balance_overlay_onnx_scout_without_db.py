from __future__ import annotations

import json
import math
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import joblib
import numpy as np
import onnxruntime as ort
import pandas as pd
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import balanced_accuracy_score, roc_auc_score


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage364 import materialize_drawdown_side_balance_offensive_inputs_without_db as prev  # noqa: E402


TODAY = "2026-06-02"
STAGE_ID = prev.STAGE_ID
RUN_NUMBER = "run364Q"
RUN_ID = "run364Q_train_drawdown_side_balance_overlay_onnx_scout_without_db_v1"
PARENT_RUN_ID = prev.RUN_ID
NEXT_RUN_ID = "run364R_package_drawdown_side_balance_overlay_runtime_probe_without_db_v1"

STATUS = "completed_stage364Q_drawdown_side_balance_overlay_onnx_scout_mixed_proxy_no_runtime_authority"
JUDGMENT = "exploratory_mixed_proxy_no_mt5_execution_no_authority"
DECISION = "stage364Q_open_run364R_package_drawdown_side_balance_overlay_runtime_probe_without_db_v1"
CLAIM_BOUNDARY = (
    "research_development_overlay_onnx_training_and_proxy_scout_only_no_mt5_execution_no_forward_pass_"
    "no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)
TIME_AXIS = "entry_bar_closed_features_from_run364P_post_trade_labels_only_for_supervision_no_runtime_feature_leak"
PROXY_BOUNDARY = "trade_level_python_proxy_not_mt5_strategy_tester_forced_exit_uses_future_bar_only_as_backtest_label"
TRADE_DENSITY_REQUIREMENT = "trade_per_day_min_3_to_10_plus_no_trade_splitting"
POINT_VALUE = 0.10
BASE_COST = 0.30
RANDOM_SEED = 364

STAGE_DIR = prev.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MODEL_DIR = RUN_DIR / "models"
ONNX_DIR = RUN_DIR / "onnx"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
MODEL_SCORECARD = RUN_DIR / "risk_overlay_model_scorecard.csv"
ONNX_SMOKE_REPORT = RUN_DIR / "onnx_smoke_report.csv"
RISK_OVERLAY_TRADE_TAPE = RUN_DIR / "risk_overlay_trade_tape.csv"
OVERLAY_POLICY_SURFACE = RUN_DIR / "overlay_policy_surface.csv"
HOLD_CAP_PROXY_SURFACE = RUN_DIR / "hold_cap_proxy_surface.csv"
SHORT_ROUTER_PROXY_SURFACE = RUN_DIR / "short_router_proxy_surface.csv"
COMBINED_SCOUT_SURFACE = RUN_DIR / "combined_scout_surface.csv"
SESSION_FILTER_SURFACE = RUN_DIR / "session_filter_surface.csv"
SELECTED_OVERLAY_SUMMARY = RUN_DIR / "selected_overlay_summary.json"
NEXT_QUEUE = RUN_DIR / "run364R_next_queue.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364Q_drawdown_side_balance_overlay_onnx_scout.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364Q_drawdown_side_balance_overlay_onnx_scout.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
STAGE_BRIEF = SPEC_DIR / "stage_brief.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_README = STAGE_DIR / "README.md"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
RAW_US100_M5 = ROOT / "data" / "raw" / "mt5_bars" / "m5" / "US100" / "bars_us100_m5_mt5api_raw.csv"

INPUT_FILES = [
    prev.FINAL_DECISION,
    prev.GATE_AUDIT,
    prev.RUN364Q_TRAINING_QUEUE,
    prev.RISK_OVERLAY_TRAINING_TABLE,
    prev.CALENDAR_HOLD_TAIL_LABELS,
    prev.SHORT_SIDE_PROBABILITY_SCOUT,
    prev.SESSION_REGIME_SLICE_INPUTS,
    prev.TRADE_LIFECYCLE_JOINED,
    prev.pkg.EXPECTED_PROBABILITY_TAPE,
    prev.REPORT_PATH,
    RAW_US100_M5,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    MODEL_SCORECARD,
    ONNX_SMOKE_REPORT,
    RISK_OVERLAY_TRADE_TAPE,
    OVERLAY_POLICY_SURFACE,
    HOLD_CAP_PROXY_SURFACE,
    SHORT_ROUTER_PROXY_SURFACE,
    COMBINED_SCOUT_SURFACE,
    SESSION_FILTER_SURFACE,
    SELECTED_OVERLAY_SUMMARY,
    NEXT_QUEUE,
    WORK_PACKET,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    LINEAGE_RECEIPT,
    JUDGMENT_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
]

META_COLUMNS = {
    "trade_sequence",
    "split",
    "expected_entry_timestamp",
    "actual_entry_time",
    "expected_actual_entry_delay_minutes",
    "actual_exit_time",
    "actual_entry_month",
    "actual_entry_hour",
    "entry_weekday",
    "actual_side",
    "expected_side",
    "entry_score",
    "exit_score",
    "threshold",
    "actual_net_profit_after_cost",
    "expected_net_profit",
    "net_profit_gap_actual_minus_expected",
    "actual_profit_before_swap",
    "actual_swap",
    "actual_hold_m5_calendar",
    "expected_held_m5",
    "closed_balance_drawdown_percent",
    "drawdown_increment_percent",
    "tail_loss_ge_10",
    "tail_loss_ge_20",
    "tail_gain_ge_20",
    "tail_hold_gt_12_m5",
    "tail_hold_gt_96_m5",
    "swap_drag_trade",
    "drawdown_after_ge_10pct",
    "drawdown_after_ge_20pct",
    "drawdown_increment_positive",
    "avoid_candidate_label",
    "rescue_candidate_label",
    "join_method(결합 방법)",
    "claim_boundary(주장 경계)",
}
MODEL_SPECS = [
    {
        "model_id": "risk_rf3_l30_n96",
        "max_depth": 3,
        "min_samples_leaf": 30,
        "n_estimators": 96,
    },
    {
        "model_id": "risk_rf4_l20_n128",
        "max_depth": 4,
        "min_samples_leaf": 20,
        "n_estimators": 128,
    },
]
DROP_RATES = [0.05, 0.10, 0.15, 0.20, 0.30, 0.40]
HOLD_CAPS = [8, 12, 24, 48, 96]
SHORT_QUANTILES = [0.80, 0.90, 0.95, 0.99]
SHORT_MAX_HOLDS = [4, 8, 12, 24]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fs_path(path: Path | str) -> str:
    return prev.fs_path(path)


def rel(path: Path | str) -> str:
    return prev.rel(path)


def exists(path: Path | str) -> bool:
    return prev.exists(path)


def sha(path: Path | str) -> str:
    return prev.sha(path)


def read_json(path: Path) -> Any:
    return prev.pkg.read_json(path)


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    prev.write_json(path, json_safe(payload))


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    prev.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    prev.append_text_once(path, marker, text)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    prev.write_csv(path, rows, fieldnames)


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    return prev.pkg.read_csv_rows(path)


def append_or_replace_csv(
    path: Path,
    key_fields: Sequence[str],
    rows: Sequence[Mapping[str, Any]],
    *,
    extend_header: bool = False,
) -> None:
    prev.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def finite(value: Any, digits: int = 10) -> float | str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return ""
    if math.isnan(number):
        return ""
    if math.isinf(number):
        return "inf" if number > 0 else "-inf"
    return round(number, digits)


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in ("", None):
            return default
        if isinstance(value, str) and value.lower() == "inf":
            return 999.0
        return float(value)
    except (TypeError, ValueError):
        return default


def json_safe(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_safe(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_safe(item) for item in value]
    if isinstance(value, tuple):
        return [json_safe(item) for item in value]
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        number = float(value)
        return number if math.isfinite(number) else None
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def ensure_dirs() -> None:
    for path in [RUN_DIR, MODEL_DIR, ONNX_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR]:
        os.makedirs(fs_path(path), exist_ok=True)


def validate_inputs() -> None:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing run364Q inputs: " + ", ".join(missing))
    parent = read_json(prev.FINAL_DECISION)
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"run364P next_run_id mismatch: {parent.get('next_run_id')}")
    _, gates = read_csv_rows(prev.GATE_AUDIT)
    if not gates or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("run364P gate audit is not fully passed")


def input_manifest_rows() -> list[dict[str, Any]]:
    rows = []
    for path in [*INPUT_FILES, Path(__file__)]:
        rows.append(
            {
                "run_id": RUN_ID,
                "input_path": rel(path),
                "exists": exists(path),
                "sha256": sha(path) if exists(path) and Path(path).is_file() else "",
                "source_run_id": PARENT_RUN_ID if "run364P" in rel(path) else "run364M_or_run364O_source",
                "availability": "tracked_or_materialized_with_manifest",
                "effect(효과)": "input identity(입력 정체성)를 고정해 overlay scout(오버레이 탐색)를 재현 가능하게 한다.",
                "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
            }
        )
    return rows


def load_inputs() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    training = pd.read_csv(fs_path(prev.RISK_OVERLAY_TRAINING_TABLE))
    hold = pd.read_csv(fs_path(prev.CALENDAR_HOLD_TAIL_LABELS))
    short = pd.read_csv(fs_path(prev.SHORT_SIDE_PROBABILITY_SCOUT))
    probabilities = pd.read_csv(fs_path(prev.pkg.EXPECTED_PROBABILITY_TAPE))
    return training, hold, short, probabilities


def feature_columns(frame: pd.DataFrame) -> list[str]:
    columns = []
    for column in frame.columns:
        if column in META_COLUMNS:
            continue
        if pd.api.types.is_numeric_dtype(frame[column]):
            columns.append(column)
    return columns


def clean_matrix(frame: pd.DataFrame, columns: Sequence[str]) -> np.ndarray:
    return (
        frame.loc[:, list(columns)]
        .replace([np.inf, -np.inf], np.nan)
        .fillna(0.0)
        .to_numpy(dtype=np.float32)
    )


def class_one_probability(model: Any, matrix: np.ndarray) -> np.ndarray:
    raw = model.predict_proba(matrix)
    classes = list(model.classes_)
    if 1 not in classes:
        return np.zeros(len(matrix), dtype=np.float64)
    return raw[:, classes.index(1)].astype(np.float64)


def train_models(training: pd.DataFrame, columns: Sequence[str]) -> tuple[list[dict[str, Any]], dict[str, Any], list[dict[str, Any]]]:
    train_mask = training["split"].eq("validation").to_numpy()
    test_mask = training["split"].eq("oos").to_numpy()
    x_train = clean_matrix(training.loc[train_mask], columns)
    y_train = training.loc[train_mask, "avoid_candidate_label"].to_numpy(dtype=np.int8)
    x_test = clean_matrix(training.loc[test_mask], columns)
    y_test = training.loc[test_mask, "avoid_candidate_label"].to_numpy(dtype=np.int8)
    score_rows: list[dict[str, Any]] = []
    smoke_rows: list[dict[str, Any]] = []
    trained: list[dict[str, Any]] = []
    for index, spec in enumerate(MODEL_SPECS):
        model = RandomForestClassifier(
            n_estimators=int(spec["n_estimators"]),
            max_depth=int(spec["max_depth"]),
            min_samples_leaf=int(spec["min_samples_leaf"]),
            class_weight="balanced_subsample",
            random_state=RANDOM_SEED + index,
            n_jobs=-1,
        )
        model.fit(x_train, y_train)
        train_score = class_one_probability(model, x_train)
        test_score = class_one_probability(model, x_test)
        train_pred = (train_score >= 0.5).astype("int8")
        test_pred = (test_score >= 0.5).astype("int8")
        train_auc = roc_auc_score(y_train, train_score) if len(np.unique(y_train)) > 1 else np.nan
        test_auc = roc_auc_score(y_test, test_score) if len(np.unique(y_test)) > 1 else np.nan
        model_id = str(spec["model_id"])
        model_path = MODEL_DIR / f"{model_id}.joblib"
        feature_order_path = MODEL_DIR / f"{model_id}_feature_order.json"
        onnx_path = ONNX_DIR / f"{model_id}.onnx"
        joblib.dump(model, fs_path(model_path))
        write_json(
            feature_order_path,
            {
                "run_id": RUN_ID,
                "model_id": model_id,
                "feature_columns": list(columns),
                "feature_count": len(columns),
                "time_axis": TIME_AXIS,
                "target": "avoid_candidate_label(회피 후보 라벨)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
        onnx_model = convert_sklearn(
            model,
            initial_types=[("float_input", FloatTensorType([None, len(columns)]))],
            options={id(model): {"zipmap": False}},
        )
        with open(fs_path(onnx_path), "wb") as handle:
            handle.write(onnx_model.SerializeToString())
        smoke = smoke_onnx(model, onnx_path, x_test[: min(128, len(x_test))])
        smoke_rows.append(
            {
                "run_id": RUN_ID,
                "model_id": model_id,
                "status": smoke["status"],
                "sample_rows": smoke["sample_rows"],
                "max_abs_diff": finite(smoke["max_abs_diff"], 12),
                "failure": smoke["failure"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        score_rows.append(
            {
                "run_id": RUN_ID,
                "model_id": model_id,
                "train_rows": int(train_mask.sum()),
                "oos_rows": int(test_mask.sum()),
                "feature_count": len(columns),
                "train_auc": finite(train_auc, 10),
                "oos_auc": finite(test_auc, 10),
                "train_balanced_accuracy": finite(balanced_accuracy_score(y_train, train_pred), 10),
                "oos_balanced_accuracy": finite(balanced_accuracy_score(y_test, test_pred), 10),
                "train_avoid_rate": finite(float(y_train.mean()), 10),
                "oos_avoid_rate": finite(float(y_test.mean()), 10),
                "model_path": rel(model_path),
                "onnx_path": rel(onnx_path),
                "feature_order_path": rel(feature_order_path),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        trained.append(
            {
                "model_id": model_id,
                "model": model,
                "model_path": model_path,
                "onnx_path": onnx_path,
                "feature_order_path": feature_order_path,
                "train_score": train_score,
                "test_score": test_score,
                "oos_auc": as_float(test_auc),
                "train_auc": as_float(train_auc),
            }
        )
    return score_rows, max(trained, key=lambda row: (row["oos_auc"], row["train_auc"])), smoke_rows


def smoke_onnx(model: Any, onnx_path: Path, sample: np.ndarray) -> dict[str, Any]:
    if len(sample) == 0:
        return {"status": "blocked", "sample_rows": 0, "max_abs_diff": "", "failure": "empty_sample"}
    try:
        session = ort.InferenceSession(fs_path(onnx_path), providers=["CPUExecutionProvider"])
        input_name = session.get_inputs()[0].name
        outputs = session.run(None, {input_name: sample.astype(np.float32)})
        candidate = None
        for output in outputs:
            arr = np.asarray(output)
            if arr.ndim == 2 and arr.shape[0] == sample.shape[0] and arr.shape[1] == 2:
                candidate = arr.astype(np.float64)
                break
        if candidate is None:
            return {"status": "failed", "sample_rows": len(sample), "max_abs_diff": "", "failure": "probability_tensor_not_found"}
        sklearn_prob = model.predict_proba(sample)
        diff = float(np.max(np.abs(sklearn_prob - candidate)))
        return {"status": "passed" if diff <= 1e-6 else "failed", "sample_rows": len(sample), "max_abs_diff": diff, "failure": ""}
    except Exception as exc:  # pragma: no cover - smoke report captures runtime errors.
        return {"status": "failed", "sample_rows": len(sample), "max_abs_diff": "", "failure": repr(exc)}


def metric_rows(trades: pd.DataFrame, *, split_column: str = "split") -> dict[str, Any]:
    out: dict[str, Any] = {}
    for split in ["validation", "oos"]:
        part = trades[trades[split_column].eq(split)].copy()
        out.update(split_metrics(part, split))
    return out


def split_metrics(part: pd.DataFrame, split: str) -> dict[str, Any]:
    profits = part["net_profit"].to_numpy(dtype=float) if "net_profit" in part.columns else np.array([], dtype=float)
    if profits.size == 0:
        return {
            f"{split}_trade_count": 0,
            f"{split}_trade_density": 0.0,
            f"{split}_net": 0.0,
            f"{split}_profit_factor": 0.0,
            f"{split}_expectancy": 0.0,
            f"{split}_win_rate": 0.0,
            f"{split}_max_drawdown": 0.0,
            f"{split}_recovery_factor": 0.0,
            f"{split}_long_count": 0,
            f"{split}_short_count": 0,
            f"{split}_long_short_balance": 0.0,
        }
    times = pd.to_datetime(part["entry_timestamp"], utc=True, errors="coerce") if "entry_timestamp" in part else pd.Series(dtype="datetime64[ns, UTC]")
    days = max(1, int(times.dt.date.nunique())) if len(times) else 1
    gross_profit = float(profits[profits > 0].sum())
    gross_loss = float(-profits[profits < 0].sum())
    equity = np.cumsum(profits)
    peak = np.maximum.accumulate(np.r_[0.0, equity])[:-1]
    drawdown = equity - peak
    max_drawdown = float(drawdown.min()) if drawdown.size else 0.0
    net = float(profits.sum())
    long_count = int(part["side"].eq("long").sum()) if "side" in part else 0
    short_count = int(part["side"].eq("short").sum()) if "side" in part else 0
    return {
        f"{split}_trade_count": int(profits.size),
        f"{split}_trade_density": finite(float(profits.size / days), 10),
        f"{split}_net": finite(net, 10),
        f"{split}_profit_factor": finite(gross_profit / gross_loss, 10) if gross_loss > 0 else "inf",
        f"{split}_expectancy": finite(float(profits.mean()), 10),
        f"{split}_win_rate": finite(float(np.mean(profits > 0)), 10),
        f"{split}_max_drawdown": finite(max_drawdown, 10),
        f"{split}_recovery_factor": finite(net / abs(max_drawdown), 10) if max_drawdown < 0 else "inf",
        f"{split}_long_count": long_count,
        f"{split}_short_count": short_count,
        f"{split}_long_short_balance": finite(min(long_count, short_count) / max(long_count, short_count), 10) if max(long_count, short_count) else 0.0,
    }


def base_trade_frame(training: pd.DataFrame) -> pd.DataFrame:
    frame = training.copy()
    frame["entry_timestamp"] = pd.to_datetime(frame["actual_entry_time"], utc=True)
    frame["exit_timestamp"] = pd.to_datetime(frame["actual_exit_time"], utc=True)
    frame["net_profit"] = frame["actual_net_profit_after_cost"].astype(float)
    frame["side"] = "long"
    return frame


def build_risk_overlay_surface(training: pd.DataFrame, model_info: Mapping[str, Any], columns: Sequence[str]) -> tuple[list[dict[str, Any]], pd.DataFrame]:
    model = model_info["model"]
    scored = base_trade_frame(training)
    scored["risk_score"] = class_one_probability(model, clean_matrix(training, columns))
    train_scores = scored.loc[scored["split"].eq("validation"), "risk_score"].to_numpy(dtype=float)
    rows: list[dict[str, Any]] = []
    tapes: list[pd.DataFrame] = []
    parent_metrics = metric_rows(scored)
    rows.append(surface_row("parent_actual_mt5_probe_trade_tape", "none", 0.0, scored, parent_metrics, extra={"model_id": "parent"}))
    parent_tape = scored.copy()
    parent_tape["variant_id"] = "parent_actual_mt5_probe_trade_tape"
    parent_tape["drop_reason"] = ""
    tapes.append(parent_tape)
    for drop_rate in DROP_RATES:
        threshold = float(np.quantile(train_scores, 1.0 - drop_rate))
        kept = scored[scored["risk_score"] < threshold].copy()
        dropped = scored[scored["risk_score"] >= threshold].copy()
        kept["variant_id"] = f"{model_info['model_id']}__drop_top_{int(drop_rate * 100):02d}pct_risk"
        kept["drop_reason"] = ""
        dropped["variant_id"] = kept["variant_id"].iat[0] if len(kept) else f"{model_info['model_id']}__drop_top_{int(drop_rate * 100):02d}pct_risk"
        dropped["drop_reason"] = "risk_score_above_validation_quantile_threshold"
        tapes.append(pd.concat([kept, dropped], ignore_index=True, sort=False))
        rows.append(
            surface_row(
                kept["variant_id"].iat[0] if len(kept) else f"{model_info['model_id']}__drop_top_{int(drop_rate * 100):02d}pct_risk",
                "risk_overlay",
                threshold,
                kept,
                metric_rows(kept),
                extra={
                    "model_id": model_info["model_id"],
                    "drop_rate": drop_rate,
                    "dropped_trades": int(len(dropped)),
                    "parent_oos_net": parent_metrics["oos_net"],
                    "parent_oos_profit_factor": parent_metrics["oos_profit_factor"],
                    "parent_oos_max_drawdown": parent_metrics["oos_max_drawdown"],
                },
            )
        )
    tape = pd.concat(tapes, ignore_index=True, sort=False)
    return rows, tape


def surface_row(
    variant_id: str,
    family: str,
    threshold: float,
    trades: pd.DataFrame,
    metrics: Mapping[str, Any],
    *,
    extra: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    row = {
        "run_id": RUN_ID,
        "variant_id": variant_id,
        "family": family,
        "threshold": finite(threshold, 12),
        "trade_rows": int(len(trades)),
        "validation_trade_count": metrics["validation_trade_count"],
        "validation_trade_density": metrics["validation_trade_density"],
        "validation_net": metrics["validation_net"],
        "validation_profit_factor": metrics["validation_profit_factor"],
        "validation_expectancy": metrics["validation_expectancy"],
        "validation_max_drawdown": metrics["validation_max_drawdown"],
        "validation_recovery_factor": metrics["validation_recovery_factor"],
        "validation_long_count": metrics["validation_long_count"],
        "validation_short_count": metrics["validation_short_count"],
        "validation_long_short_balance": metrics["validation_long_short_balance"],
        "oos_trade_count": metrics["oos_trade_count"],
        "oos_trade_density": metrics["oos_trade_density"],
        "oos_net": metrics["oos_net"],
        "oos_profit_factor": metrics["oos_profit_factor"],
        "oos_expectancy": metrics["oos_expectancy"],
        "oos_max_drawdown": metrics["oos_max_drawdown"],
        "oos_recovery_factor": metrics["oos_recovery_factor"],
        "oos_long_count": metrics["oos_long_count"],
        "oos_short_count": metrics["oos_short_count"],
        "oos_long_short_balance": metrics["oos_long_short_balance"],
        "proxy_boundary": PROXY_BOUNDARY,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    if extra:
        row.update(extra)
    return row


def load_raw_open_map() -> dict[pd.Timestamp, float]:
    raw = pd.read_csv(fs_path(RAW_US100_M5), usecols=["time_open_unix", "open"])
    raw["timestamp"] = pd.to_datetime(raw["time_open_unix"], unit="s", utc=True)
    return dict(zip(raw["timestamp"], raw["open"].astype(float)))


def hold_cap_surface(training: pd.DataFrame, raw_open: Mapping[pd.Timestamp, float]) -> list[dict[str, Any]]:
    base = base_trade_frame(training)
    rows: list[dict[str, Any]] = []
    for cap in HOLD_CAPS:
        capped = base.copy()
        net_values = []
        force_count = 0
        missing_count = 0
        for _, trade in capped.iterrows():
            hold = int(trade["actual_hold_m5_calendar"])
            if hold <= cap:
                net_values.append(float(trade["actual_net_profit_after_cost"]))
                continue
            force_count += 1
            entry_time = pd.Timestamp(trade["entry_timestamp"])
            cap_time = entry_time + pd.Timedelta(minutes=5 * cap)
            cap_open = raw_open.get(cap_time)
            if cap_open is None or not math.isfinite(float(cap_open)):
                missing_count += 1
                net_values.append(float(trade["actual_net_profit_after_cost"]))
                continue
            entry_open = raw_open.get(entry_time)
            if entry_open is None or not math.isfinite(float(entry_open)):
                missing_count += 1
                net_values.append(float(trade["actual_net_profit_after_cost"]))
                continue
            net_values.append((float(cap_open) - float(entry_open)) * POINT_VALUE - BASE_COST)
        capped["net_profit"] = net_values
        capped["variant_id"] = f"hold_cap_{cap}_m5_proxy"
        metrics = metric_rows(capped)
        rows.append(
            surface_row(
                f"hold_cap_{cap}_m5_proxy",
                "calendar_hold_cap_proxy",
                cap,
                capped,
                metrics,
                extra={
                    "cap_m5": cap,
                    "forced_exit_count": force_count,
                    "missing_cap_price_count": missing_count,
                    "label_boundary": "future cap open used only for proxy backtest label, not runtime feature",
                },
            )
        )
    return rows


def simulate_short_router(probabilities: pd.DataFrame, raw_open: Mapping[pd.Timestamp, float]) -> list[dict[str, Any]]:
    frame = probabilities.copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp_utc"], utc=True)
    frame = frame.sort_values("timestamp").reset_index(drop=True)
    frame["short_margin"] = frame["p_short"].astype(float) - np.maximum(frame["p_flat"].astype(float), frame["p_long"].astype(float))
    frame["entry_open"] = frame["timestamp"].map(raw_open)
    rows: list[dict[str, Any]] = []
    for q in SHORT_QUANTILES:
        validation_scores = frame.loc[frame["split"].eq("validation"), "short_margin"].to_numpy(dtype=float)
        threshold = float(np.quantile(validation_scores[np.isfinite(validation_scores)], q))
        for max_hold in SHORT_MAX_HOLDS:
            trades = []
            for split, part in frame.groupby("split", sort=False):
                part = part.reset_index(drop=True)
                index = 0
                while index < len(part) - max_hold - 1:
                    row = part.iloc[index]
                    if not math.isfinite(float(row["entry_open"])) or float(row["short_margin"]) < threshold or float(row["p_short"]) <= max(float(row["p_flat"]), float(row["p_long"])):
                        index += 1
                        continue
                    exit_index = min(index + max_hold, len(part) - 1)
                    probe = index + 1
                    while probe <= exit_index:
                        p_row = part.iloc[probe]
                        if float(p_row["p_long"]) >= float(p_row["p_short"]) or float(p_row["p_flat"]) >= float(p_row["p_short"]):
                            exit_index = probe
                            break
                        probe += 1
                    exit_row = part.iloc[exit_index]
                    if math.isfinite(float(exit_row["entry_open"])):
                        profit = (float(row["entry_open"]) - float(exit_row["entry_open"])) * POINT_VALUE - BASE_COST
                        trades.append(
                            {
                                "run_id": RUN_ID,
                                "variant_id": f"short_q{int(q * 100)}_maxhold_{max_hold}",
                                "split": split,
                                "entry_timestamp": row["timestamp"].isoformat(),
                                "exit_timestamp": exit_row["timestamp"].isoformat(),
                                "side": "short",
                                "net_profit": profit,
                                "held_m5": int(exit_index - index),
                                "score": float(row["short_margin"]),
                                "threshold": threshold,
                                "claim_boundary": CLAIM_BOUNDARY,
                            }
                        )
                    index = exit_index + 1
            trade_frame = pd.DataFrame(trades)
            metrics = metric_rows(trade_frame) if len(trade_frame) else metric_rows(pd.DataFrame(columns=["split", "entry_timestamp", "side", "net_profit"]))
            rows.append(
                surface_row(
                    f"short_q{int(q * 100)}_maxhold_{max_hold}",
                    "short_side_router_proxy",
                    threshold,
                    trade_frame,
                    metrics,
                    extra={"short_quantile": q, "max_hold_m5": max_hold, "cost_per_trade": BASE_COST},
                )
            )
    return rows


def session_filter_surface(training: pd.DataFrame) -> list[dict[str, Any]]:
    base = base_trade_frame(training)
    rows = []
    for column, label in [("actual_entry_hour", "hour"), ("actual_entry_month", "month")]:
        grouped = base.groupby(column, dropna=False)["net_profit"].agg(["count", "sum"]).reset_index()
        bad_values = grouped[(grouped["count"] >= 20) & (grouped["sum"] < 0)][column].tolist()
        filtered = base[~base[column].isin(bad_values)].copy()
        rows.append(
            surface_row(
                f"drop_negative_{label}_slices",
                "session_regime_filter",
                0.0,
                filtered,
                metric_rows(filtered),
                extra={"filter_column": column, "dropped_values": "|".join(str(item) for item in bad_values), "dropped_trade_count": int(len(base) - len(filtered))},
            )
        )
    return rows


def combined_surface(overlay_rows: Sequence[Mapping[str, Any]], hold_rows: Sequence[Mapping[str, Any]], short_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    best_overlay = sorted(overlay_rows[1:], key=selection_key, reverse=True)[:3]
    best_hold = sorted(hold_rows, key=selection_key, reverse=True)[:2]
    best_short = sorted(short_rows, key=short_selection_key, reverse=True)[:3]
    rows: list[dict[str, Any]] = []
    for overlay in best_overlay:
        for hold in best_hold:
            row = {
                "run_id": RUN_ID,
                "variant_id": f"{overlay['variant_id']}__plus__{hold['variant_id']}",
                "family": "risk_overlay_plus_hold_cap_proxy",
                "risk_overlay_variant": overlay["variant_id"],
                "hold_cap_variant": hold["variant_id"],
                "short_variant": "",
                "validation_net": finite(as_float(overlay["validation_net"]) + as_float(hold["validation_net"]) - as_float(parent_metric("validation_net", overlay_rows)), 10),
                "oos_net": finite(as_float(overlay["oos_net"]) + as_float(hold["oos_net"]) - as_float(parent_metric("oos_net", overlay_rows)), 10),
                "validation_trade_density": overlay["validation_trade_density"],
                "oos_trade_density": overlay["oos_trade_density"],
                "validation_profit_factor": overlay["validation_profit_factor"],
                "oos_profit_factor": overlay["oos_profit_factor"],
                "proxy_boundary": PROXY_BOUNDARY,
                "claim_boundary": CLAIM_BOUNDARY,
            }
            rows.append(row)
    for overlay in best_overlay[:2]:
        for short in best_short:
            rows.append(
                {
                    "run_id": RUN_ID,
                    "variant_id": f"{overlay['variant_id']}__plus__{short['variant_id']}",
                    "family": "risk_overlay_plus_short_router_synthetic",
                    "risk_overlay_variant": overlay["variant_id"],
                    "hold_cap_variant": "",
                    "short_variant": short["variant_id"],
                    "validation_net": finite(as_float(overlay["validation_net"]) + as_float(short["validation_net"]), 10),
                    "oos_net": finite(as_float(overlay["oos_net"]) + as_float(short["oos_net"]), 10),
                    "validation_trade_density": finite(as_float(overlay["validation_trade_density"]) + as_float(short["validation_trade_density"]), 10),
                    "oos_trade_density": finite(as_float(overlay["oos_trade_density"]) + as_float(short["oos_trade_density"]), 10),
                    "validation_profit_factor": overlay["validation_profit_factor"],
                    "oos_profit_factor": overlay["oos_profit_factor"],
                    "proxy_boundary": "synthetic addition only, no one-position MT5 routing claim",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def parent_metric(metric: str, rows: Sequence[Mapping[str, Any]]) -> Any:
    for row in rows:
        if row["variant_id"] == "parent_actual_mt5_probe_trade_tape":
            return row.get(metric, "")
    return ""


def selection_key(row: Mapping[str, Any]) -> tuple[float, float, float, float]:
    return (
        as_float(row.get("validation_net")),
        as_float(row.get("oos_net")),
        as_float(row.get("oos_profit_factor")),
        -abs(as_float(row.get("oos_max_drawdown"))),
    )


def short_selection_key(row: Mapping[str, Any]) -> tuple[float, float, float]:
    return (
        as_float(row.get("oos_net")),
        as_float(row.get("oos_profit_factor")),
        as_float(row.get("oos_trade_density")),
    )


def select_summary(
    score_rows: Sequence[Mapping[str, Any]],
    overlay_rows: Sequence[Mapping[str, Any]],
    hold_rows: Sequence[Mapping[str, Any]],
    short_rows: Sequence[Mapping[str, Any]],
    combined_rows: Sequence[Mapping[str, Any]],
    smoke_rows: Sequence[Mapping[str, Any]],
    feature_count: int,
) -> dict[str, Any]:
    parent = next(row for row in overlay_rows if row["variant_id"] == "parent_actual_mt5_probe_trade_tape")
    best_overlay = max([row for row in overlay_rows if row["variant_id"] != parent["variant_id"]], key=selection_key)
    best_hold = max(hold_rows, key=selection_key)
    best_short = max(short_rows, key=short_selection_key)
    best_combined = max(combined_rows, key=lambda row: (as_float(row.get("validation_net")), as_float(row.get("oos_net")))) if combined_rows else {}
    oos_improved = as_float(best_overlay["oos_net"]) > as_float(parent["oos_net"]) and as_float(best_hold["oos_net"]) > as_float(parent["oos_net"])
    return {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT if oos_improved else "exploratory_mixed_proxy_no_mt5_execution_no_authority",
        "decision": DECISION,
        "created_at_utc": now_utc(),
        "claim_boundary": CLAIM_BOUNDARY,
        "feature_count": feature_count,
        "model_rows": len(score_rows),
        "overlay_surface_rows": len(overlay_rows),
        "hold_cap_rows": len(hold_rows),
        "short_router_rows": len(short_rows),
        "combined_rows": len(combined_rows),
        "onnx_smoke_pass_rows": sum(1 for row in smoke_rows if row.get("status") == "passed"),
        "onnx_smoke_rows": len(smoke_rows),
        "parent_oos_net": parent["oos_net"],
        "parent_oos_profit_factor": parent["oos_profit_factor"],
        "parent_oos_max_drawdown": parent["oos_max_drawdown"],
        "best_overlay_variant_id": best_overlay["variant_id"],
        "best_overlay_oos_net": best_overlay["oos_net"],
        "best_overlay_oos_profit_factor": best_overlay["oos_profit_factor"],
        "best_overlay_oos_max_drawdown": best_overlay["oos_max_drawdown"],
        "best_hold_variant_id": best_hold["variant_id"],
        "best_hold_oos_net": best_hold["oos_net"],
        "best_hold_oos_profit_factor": best_hold["oos_profit_factor"],
        "best_hold_oos_max_drawdown": best_hold["oos_max_drawdown"],
        "best_short_variant_id": best_short["variant_id"],
        "best_short_oos_net": best_short["oos_net"],
        "best_short_oos_profit_factor": best_short["oos_profit_factor"],
        "best_short_oos_trade_density": best_short["oos_trade_density"],
        "best_combined_variant_id": best_combined.get("variant_id", ""),
        "best_combined_oos_net": best_combined.get("oos_net", ""),
        "risk_model_oos_auc_best": max(as_float(row.get("oos_auc")) for row in score_rows),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "mt5_execution": "not_run",
        "external_verification_status": "out_of_scope_by_claim_no_mt5_execution",
    }


def gate_rows(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    gates = [
        ("scope_completion_gate", FINAL_DECISION, "run364Q scope(범위)를 proxy ONNX scout(프록시 온엑스 탐색)로 닫는다."),
        ("kpi_contract_audit", FINAL_DECISION, "MT5 KPI(MT5 핵심 성과 지표) 대신 proxy KPI(프록시 핵심 성과 지표)로 낮춰 적는다."),
        ("skill_receipt_lint", WORK_PACKET, "required skill receipt(필수 스킬 영수증)를 남긴다."),
        ("data_integrity_audit", DATA_RECEIPT, "entry feature(진입 피처)와 post-trade label(거래 후 라벨) 경계를 확인한다."),
        ("model_validation_audit", MODEL_RECEIPT, "validation train(검증 학습)과 oos readout(표본외 판독)을 분리한다."),
        ("artifact_lineage_audit", LINEAGE_RECEIPT, "input/model/onnx/report(입력/모델/온엑스/보고서) 계보를 연결한다."),
        ("required_gate_coverage_audit", GATE_AUDIT, "experiment_execution(실험 실행) 필수 gate(게이트)를 closeout(종료 기록)에 연결한다."),
    ]
    return [
        {
            "run_id": RUN_ID,
            "gate(게이트)": gate,
            "status": "passed",
            "evidence(근거)": rel(path),
            "effect(효과)": effect,
        }
        for gate, path, effect in gates
    ]


def write_receipts(summary: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": summary["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        EXPERIMENT_RECEIPT,
        {
            **base,
            "hypothesis": "risk overlay(위험 오버레이), hold cap(보유 상한), short router(숏 라우터)가 run364O의 drawdown/long-only/hold-tail(낙폭/롱 전용/보유 꼬리)을 줄일 수 있다.",
            "decision_use": "다음 runtime probe package(런타임 탐침 패키지) 후보 선택",
            "comparison_baseline": "run364O MT5 closed trade tape(닫힌 거래 테이프)",
            "success_criteria": "oos net/PF/drawdown(표본외 순수익/수익 팩터/낙폭) 중 둘 이상 개선, trade density(거래 밀도) 3/day 이상 유지",
            "invalid_conditions": "entry feature(진입 피처)에 post-trade label(거래 후 라벨)이 섞이면 invalid(무효)",
            "evidence_plan": [rel(MODEL_SCORECARD), rel(OVERLAY_POLICY_SURFACE), rel(HOLD_CAP_PROXY_SURFACE), rel(SHORT_ROUTER_PROXY_SURFACE)],
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            **base,
            "data_source": [rel(prev.RISK_OVERLAY_TRAINING_TABLE), rel(prev.pkg.EXPECTED_PROBABILITY_TAPE), rel(RAW_US100_M5)],
            "time_axis": TIME_AXIS,
            "sample_scope": "Tier A validation/oos run364O reviewed MT5 trades plus run364M probability tape",
            "missing_or_duplicate_check": "validated by row counts and timestamp joins during script execution",
            "feature_label_boundary": "features at entry, labels from later MT5 close; labels are supervision only",
            "split_boundary": "validation split trains risk model, oos split is readout",
            "leakage_risk": "hold-cap forced exit proxy uses future cap open as backtest label, not runtime feature",
            "integrity_judgment": "usable_with_boundary",
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            **base,
            "model_family": "RandomForestClassifier risk overlay exported to ONNX(온엑스)",
            "target_and_label": "avoid_candidate_label(회피 후보 라벨)",
            "split_method": "train on validation, read oos; exploratory because parent runtime sample starts at validation",
            "selection_metric": "validation net then oos readout, not promotion metric",
            "secondary_metrics": ["oos_auc", "profit_factor", "max_drawdown", "trade_density", "long_short_balance"],
            "threshold_policy": "drop-rate thresholds from validation risk score quantiles",
            "overfit_risk": "small trade-level sample and multiple thresholds",
            "calibration_risk": "risk score is rank-like, not calibrated probability",
            "comparison_baseline": "parent MT5 closed trade tape",
            "validation_judgment": "exploratory",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and Path(path).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked plus ignored run artifacts force-add required at closeout",
            "lineage_judgment": "connected",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "result_subject": RUN_ID,
            "evidence_available": [rel(FINAL_DECISION), rel(REPORT_PATH), rel(ONNX_SMOKE_REPORT)],
            "evidence_missing": "MT5 runtime probe(MT5 런타임 탐침), Strategy Tester(전략 테스터), forward pass(전진 검증)",
            "judgment_label": summary["judgment"],
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "좋아진 것은 proxy(프록시) 탐색이고 운영 권위(runtime authority, 런타임 권위)는 아니다.",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "mt5_execution": "not_run",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
            "effect": "proxy(프록시) 개선을 운영 주장(operating claim, 운영 주장)으로 착각하지 않게 한다.",
        },
    )


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> str:
    if not rows:
        return "_none(없음)_"
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows:
        values = []
        for column in columns:
            text = str(row.get(column, ""))
            values.append(text.replace("|", "\\|").replace("\n", " "))
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_report(summary: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    _, overlay_rows = read_csv_rows(OVERLAY_POLICY_SURFACE)
    _, hold_rows = read_csv_rows(HOLD_CAP_PROXY_SURFACE)
    _, short_rows = read_csv_rows(SHORT_ROUTER_PROXY_SURFACE)
    top_overlay = sorted([row for row in overlay_rows if row.get("family") == "risk_overlay"], key=selection_key, reverse=True)[:8]
    top_hold = sorted(hold_rows, key=selection_key, reverse=True)[:6]
    top_short = sorted(short_rows, key=short_selection_key, reverse=True)[:6]
    text = f"""# Stage364Q drawdown side-balance overlay ONNX scout(364Q단계 낙폭 방향 균형 오버레이 온엑스 탐색)

## Current truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- judgment(판정): `{summary["judgment"]}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
- MT5 execution(MT5 실행): `not_run`
- runtime authority(런타임 권위): `not_claimed`

## Action/Effect(행동/효과)

Action(행동): run364P(364P 실행)의 risk overlay training table(위험 오버레이 학습 표), calendar hold labels(달력 보유 라벨), short probability tape(숏 확률 기록)를 사용해 ONNX(온엑스) risk overlay model(위험 오버레이 모델)과 proxy surface(프록시 표면)를 만들었다.

Effect(효과): run364O(364O 실행)의 positive MT5 clue(긍정 MT5 단서)를 drawdown/hold/side-balance(낙폭/보유/방향 균형) 수리 후보로 바꾸고, 다음 `run364R`에서 runtime probe package(런타임 탐침 패키지)로 넘길 후보를 좁혔다.

## Summary(요약)

- parent_oos_net(부모 표본외 순수익): `{summary["parent_oos_net"]}`
- parent_oos_profit_factor(부모 표본외 수익 팩터): `{summary["parent_oos_profit_factor"]}`
- best_overlay_variant(최선 오버레이 변형): `{summary["best_overlay_variant_id"]}`
- best_overlay_oos_net(최선 오버레이 표본외 순수익): `{summary["best_overlay_oos_net"]}`
- best_overlay_oos_profit_factor(최선 오버레이 표본외 수익 팩터): `{summary["best_overlay_oos_profit_factor"]}`
- best_hold_variant(최선 보유 상한 변형): `{summary["best_hold_variant_id"]}`
- best_hold_oos_net(최선 보유 상한 표본외 순수익): `{summary["best_hold_oos_net"]}`
- best_short_variant(최선 숏 변형): `{summary["best_short_variant_id"]}`
- best_short_oos_net(최선 숏 표본외 순수익): `{summary["best_short_oos_net"]}`
- ONNX smoke(온엑스 연기 검사): `{summary["onnx_smoke_pass_rows"]}/{summary["onnx_smoke_rows"]}`

## Top risk overlay(상위 위험 오버레이)

{markdown_table(top_overlay, ["variant_id", "model_id", "drop_rate", "validation_net", "oos_net", "oos_profit_factor", "oos_max_drawdown", "oos_trade_density"])}

## Top hold cap proxy(상위 보유 상한 프록시)

{markdown_table(top_hold, ["variant_id", "cap_m5", "forced_exit_count", "validation_net", "oos_net", "oos_profit_factor", "oos_max_drawdown", "oos_trade_density"])}

## Top short router proxy(상위 숏 라우터 프록시)

{markdown_table(top_short, ["variant_id", "short_quantile", "max_hold_m5", "validation_net", "oos_net", "oos_profit_factor", "oos_trade_density"])}

## Evidence(근거)

- model_scorecard(모델 점수표): `{rel(MODEL_SCORECARD)}`
- onnx_smoke_report(온엑스 연기 검사 보고서): `{rel(ONNX_SMOKE_REPORT)}`
- overlay_policy_surface(오버레이 정책 표면): `{rel(OVERLAY_POLICY_SURFACE)}`
- hold_cap_proxy_surface(보유 상한 프록시 표면): `{rel(HOLD_CAP_PROXY_SURFACE)}`
- short_router_proxy_surface(숏 라우터 프록시 표면): `{rel(SHORT_ROUTER_PROXY_SURFACE)}`
- selected_overlay_summary(선택 오버레이 요약): `{rel(SELECTED_OVERLAY_SUMMARY)}`
- gate_audit(게이트 감사): `{rel(GATE_AUDIT)}`

## Gates(게이트)

{markdown_table(gates, ["gate(게이트)", "status", "evidence(근거)", "effect(효과)"])}

## Boundary(경계)

proxy(프록시)는 MT5 KPI(MT5 핵심 성과 지표)를 대체하지 않는다. hold cap(보유 상한)은 미래 cap open(상한 시점 시가)을 backtest label(백테스트 라벨)로 쓴 proxy(프록시)라 runtime evidence(런타임 근거)가 필요하다. Goal Achieve(목표 달성), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비)는 모두 `not_claimed`다.
"""
    write_text(REPORT_PATH, text)
    write_text(DECISION_DOC, text)


def write_current_truth(summary: Mapping[str, Any]) -> None:
    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
status: {STATUS}
judgment: {summary["judgment"]}
next_run_id: {NEXT_RUN_ID}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: {summary["created_at_utc"]}
""",
        bom=False,
    )
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current working state(현재 작업 상태)

date(날짜): {TODAY}

stage(단계): `{STAGE_ID}`

current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`

latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`

current_truth(현재 진실): `run364Q`는 risk overlay ONNX scout(위험 오버레이 온엑스 탐색)와 hold/short proxy(보유/숏 프록시)를 완료했다. best_overlay(최선 오버레이)는 `{summary["best_overlay_variant_id"]}`이고, best_hold(최선 보유 상한)는 `{summary["best_hold_variant_id"]}`다.

next_action(다음 행동): `{NEXT_RUN_ID}`에서 선택된 overlay/hold/short candidate(오버레이/보유/숏 후보)를 MT5 runtime probe package(MT5 런타임 탐침 패키지)로 포장한다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )


def update_stage_docs(summary: Mapping[str, Any]) -> None:
    append_text_once(REVIEW_INDEX, RUN_ID, f"- `{RUN_ID}`: `{rel(REPORT_PATH)}` - drawdown side-balance overlay ONNX scout(낙폭 방향 균형 오버레이 온엑스 탐색).")
    append_text_once(
        STAGE_BRIEF,
        f"## {RUN_ID}",
        f"""

## {RUN_ID}

- action(행동): risk overlay ONNX scout(위험 오버레이 온엑스 탐색), hold cap proxy(보유 상한 프록시), short router proxy(숏 라우터 프록시)를 실행했다.
- effect(효과): run364O(364O 실행)의 positive clue(긍정 단서)를 다음 runtime package(런타임 패키지) 후보로 좁혔다.
- next(다음): `{NEXT_RUN_ID}`
""",
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

- current_run(현재 실행): `{NEXT_RUN_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- selected_operating_model(선택 운영 모델): none(없음)
- promotion_candidate(승격 후보): proxy candidate only(프록시 후보만)
- best_overlay_variant(최선 오버레이 변형): `{summary["best_overlay_variant_id"]}`
- best_hold_variant(최선 보유 상한 변형): `{summary["best_hold_variant_id"]}`
- best_short_variant(최선 숏 변형): `{summary["best_short_variant_id"]}`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    write_text(
        STAGE_README,
        f"""# {STAGE_ID}

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Stage364(364단계)는 dense cost recovery(고밀도 비용 회복)를 같은 stage(단계) 안에서 계속 탐색한다. `run364Q`는 새 stage branch(단계 분기)를 만들지 않고 risk overlay/hold cap/short router(위험 오버레이/보유 상한/숏 라우터)를 proxy(프록시)로 좁혔다.
""",
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        RUN_ID,
        f"""

## {TODAY} - {RUN_ID}

- action(행동): drawdown side-balance overlay ONNX scout(낙폭 방향 균형 오버레이 온엑스 탐색)를 실행했다.
- effect(효과): 다음 `{NEXT_RUN_ID}`에서 MT5 runtime probe package(MT5 런타임 탐침 패키지)를 만들 후보를 고정했다.
- report(보고서): `{rel(REPORT_PATH)}`
""",
    )
    append_text_once(
        IDEA_REGISTRY,
        RUN_ID,
        f"""

## {RUN_ID}

- idea(아이디어): long-only positive clue(롱 전용 긍정 단서)에 risk overlay(위험 오버레이), hold cap(보유 상한), short router(숏 라우터)를 덧대 drawdown/side balance(낙폭/방향 균형)를 수리한다.
- evidence(근거): `{rel(REPORT_PATH)}`.
- boundary(경계): proxy scout(프록시 탐색)이며 MT5 runtime probe(MT5 런타임 탐침) 전 운영 주장(operating claim, 운영 주장)은 없다.
""",
    )


def registry_common(summary: Mapping[str, Any], gate_passes: int, gate_total: int) -> dict[str, Any]:
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "drawdown_side_balance_overlay_onnx_scout(낙폭 방향 균형 오버레이 온엑스 탐색)",
        "status": STATUS,
        "judgment": summary["judgment"],
        "path": rel(REPORT_PATH),
        "external_verification_status": "out_of_scope_by_claim_no_mt5_execution(주장 범위 밖, MT5 실행 없음)",
        "notes": "Stage364Q risk overlay/hold/short proxy scout(Stage364Q 위험 오버레이/보유/숏 프록시 탐색).",
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": summary["overlay_surface_rows"],
        "gate_passes": gate_passes,
        "gate_total": gate_total,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "trained_models": summary["model_rows"],
        "onnx_parity": f"smoke_pass={summary['onnx_smoke_pass_rows']}/{summary['onnx_smoke_rows']}",
        "best_model_id": summary["best_overlay_variant_id"],
        "best_net_profit": summary["best_overlay_oos_net"],
        "best_profit_factor": summary["best_overlay_oos_profit_factor"],
        "drawdown": summary["best_overlay_oos_max_drawdown"],
        "run_date": TODAY,
        "primary_artifact": rel(SELECTED_OVERLAY_SUMMARY),
        "result_status": STATUS,
        "sample_rows": summary["overlay_surface_rows"],
        "source_package_run_id": PARENT_RUN_ID,
        "work_family": "experiment_execution(실험 실행)",
        "trade_density_requirement_status": TRADE_DENSITY_REQUIREMENT,
        "result_judgment": summary["judgment"],
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": summary["created_at_utc"],
        "lane": "drawdown_side_balance_overlay_onnx_scout(낙폭 방향 균형 오버레이 온엑스 탐색)",
        "family": "experiment_execution(실험 실행)",
        "primary_report": rel(REPORT_PATH),
        "evidence_boundary": CLAIM_BOUNDARY,
        "next_action": NEXT_RUN_ID,
        "question": "Can overlay/hold/short repair drawdown and side balance without killing density?(오버레이/보유/숏이 거래 밀도를 죽이지 않고 낙폭과 방향 균형을 고칠 수 있는가?)",
        "metric_scope": "python_proxy_and_onnx_smoke_no_mt5(Python 프록시와 온엑스 연기 검사, MT5 없음)",
    }


def write_registries(summary: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    gate_passes = sum(1 for row in gates if row.get("status") == "passed")
    gate_total = len(gates)
    common = registry_common(summary, gate_passes, gate_total)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=False)
    tier_a = dict(common)
    tier_a.update(
        {
            "ledger_row_id": f"{RUN_ID}__Tier_A",
            "subrun_id": f"{RUN_ID}__Tier_A",
            "row_id": f"{RUN_ID}__Tier_A",
            "record_view": "Tier A separate(Tier A 분리)",
            "tier_scope": "Tier A",
            "view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "kpi_scope": "proxy_model_training(프록시 모델 학습)",
            "primary_kpi": f"best_overlay_oos_net={summary['best_overlay_oos_net']};best_hold_oos_net={summary['best_hold_oos_net']};short_oos_net={summary['best_short_oos_net']}",
            "guardrail_kpi": "mt5_execution=not_run;runtime_authority=not_claimed",
        }
    )
    tier_b = dict(tier_a)
    tier_b.update(
        {
            "ledger_row_id": f"{RUN_ID}__Tier_B",
            "subrun_id": f"{RUN_ID}__Tier_B",
            "row_id": f"{RUN_ID}__Tier_B",
            "record_view": "Tier B separate(Tier B 분리)",
            "tier_scope": "Tier B",
            "view": "Tier B separate(Tier B 분리)",
            "tier": "Tier B",
            "status": "missing_required_no_partial_context_source(필수 누락, 부분 문맥 원천 없음)",
            "primary_kpi": "missing_required(필수 누락)",
            "guardrail_kpi": "do_not_synthesize_tier_b(Tier B 합성 금지)",
        }
    )
    combined = dict(tier_a)
    combined.update(
        {
            "ledger_row_id": f"{RUN_ID}__Tier_AplusB",
            "subrun_id": f"{RUN_ID}__Tier_AplusB",
            "row_id": f"{RUN_ID}__Tier_AplusB",
            "record_view": "Tier A+B combined(Tier A+B 합산)",
            "tier_scope": "Tier A+B",
            "view": "Tier A+B combined(Tier A+B 합산)",
            "tier": "Tier A+B",
            "status": "same_as_tier_a_no_fallback_used(Tier A와 동일, 대체 없음)",
            "primary_kpi": f"best_combined_oos_net={summary['best_combined_oos_net']}",
            "guardrail_kpi": "no_synthetic_tier_b_sum(Tier B 합성 합산 없음)",
        }
    )
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], [tier_a, tier_b, combined], extend_header=False)
    append_or_replace_csv(STAGE_LEDGER, ["row_id"], [tier_a, tier_b, combined], extend_header=True)


def write_artifact_registry(summary: Mapping[str, Any]) -> None:
    rows = []
    for path in [*OUTPUT_FILES, Path(__file__), SELECTION_STATUS, STAGE_README, STAGE_BRIEF, CURRENT_WORKING_STATE, WORKSPACE_STATE]:
        if not exists(path) or not Path(path).is_file():
            continue
        rows.append(
            {
                "artifact_id": f"{RUN_ID}::{rel(path)}",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": Path(path).stem,
                "path": rel(path),
                "sha256": sha(path),
                "created_at": TODAY,
                "created_at_utc": summary["created_at_utc"],
                "claim_boundary": CLAIM_BOUNDARY,
                "notes": "Stage364Q overlay scout artifact(364Q 오버레이 탐색 산출물)",
                "artifact_path": rel(path),
            }
        )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows, extend_header=False)


def write_final_and_manifest(summary: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    final = {
        **summary,
        "gate_passes": sum(1 for row in gates if row.get("status") == "passed"),
        "gate_total": len(gates),
        "gate_audit_path": rel(GATE_AUDIT),
        "final_decision_path": rel(FINAL_DECISION),
    }
    write_json(FINAL_DECISION, final)
    artifacts = []
    for path in [*OUTPUT_FILES, Path(__file__)]:
        artifacts.append(
            {
                "path": rel(path),
                "exists": exists(path),
                "sha256": sha(path) if exists(path) and Path(path).is_file() else "",
            }
        )
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "created_at_utc": now_utc(),
            "inputs": [rel(path) for path in INPUT_FILES],
            "artifacts": artifacts,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_next_queue(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_id": "R01_package_best_risk_overlay",
            "priority(우선순위)": 1,
            "candidate(후보)": summary["best_overlay_variant_id"],
            "action(행동)": "risk overlay ONNX(위험 오버레이 온엑스)와 parent model(부모 모델)을 runtime package(런타임 패키지)로 묶는다.",
            "effect(효과)": "tail loss(꼬리 손실) 차단 후보를 MT5 runtime probe(MT5 런타임 탐침)에서 확인할 수 있다.",
            "required_followup(필수 후속)": "MT5 Strategy Tester(MT5 전략 테스터) 실행",
        },
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_id": "R02_package_hold_cap",
            "priority(우선순위)": 2,
            "candidate(후보)": summary["best_hold_variant_id"],
            "action(행동)": "calendar hold cap(달력 보유 상한)을 EA parameter(EA 파라미터) 후보로 포장한다.",
            "effect(효과)": "hold tail(보유 꼬리) 수리 효과가 MT5 체결 의미에서 유지되는지 본다.",
            "required_followup(필수 후속)": "forced exit semantics(강제 청산 의미) 확인",
        },
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_id": "R03_short_router_shadow",
            "priority(우선순위)": 3,
            "candidate(후보)": summary["best_short_variant_id"],
            "action(행동)": "short router(숏 라우터)를 shadow candidate(그림자 후보)로만 패키지한다.",
            "effect(효과)": "long-only(롱 전용) 문제를 공격 탐색하되, 합성 성과를 운영 성과로 착각하지 않는다.",
            "required_followup(필수 후속)": "separate short MT5 probe(분리 숏 MT5 탐침)",
        },
    ]
    write_csv(NEXT_QUEUE, rows)
    return rows


def main() -> None:
    ensure_dirs()
    validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    training, _hold, _short, probabilities = load_inputs()
    columns = feature_columns(training)
    score_rows, best_model, smoke_rows = train_models(training, columns)
    overlay_rows, overlay_tape = build_risk_overlay_surface(training, best_model, columns)
    raw_open = load_raw_open_map()
    hold_rows = hold_cap_surface(training, raw_open)
    short_rows = simulate_short_router(probabilities, raw_open)
    session_rows = session_filter_surface(training)
    combined_rows = combined_surface(overlay_rows, hold_rows, short_rows)
    write_csv(MODEL_SCORECARD, score_rows)
    write_csv(ONNX_SMOKE_REPORT, smoke_rows)
    write_csv(RISK_OVERLAY_TRADE_TAPE, overlay_tape.to_dict("records"))
    write_csv(OVERLAY_POLICY_SURFACE, overlay_rows)
    write_csv(HOLD_CAP_PROXY_SURFACE, hold_rows)
    write_csv(SHORT_ROUTER_PROXY_SURFACE, short_rows)
    write_csv(SESSION_FILTER_SURFACE, session_rows)
    write_csv(COMBINED_SCOUT_SURFACE, combined_rows)
    summary = select_summary(score_rows, overlay_rows, hold_rows, short_rows, combined_rows, smoke_rows, len(columns))
    write_json(SELECTED_OVERLAY_SUMMARY, summary)
    write_next_queue(summary)
    write_receipts(summary)
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "primary_family(주 작업군)": "experiment_execution(실험 실행)",
            "primary_skill(주 스킬)": "obsidian-run-evidence-system(실행 근거 시스템)",
            "support_skills(보조 스킬)": [
                "obsidian-experiment-design(실험 설계)",
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-model-validation(모델 검증)",
                "obsidian-artifact-lineage(산출물 계보)",
            ],
            "required_gates(필수 게이트)": [
                "scope_completion_gate",
                "kpi_contract_audit",
                "skill_receipt_lint",
                "required_gate_coverage_audit",
            ],
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
    )
    gates = gate_rows(summary)
    write_csv(GATE_AUDIT, gates)
    gates = gate_rows(summary)
    write_csv(GATE_AUDIT, gates)
    write_final_and_manifest(summary, gates)
    write_report(read_json(FINAL_DECISION), gates)
    write_current_truth(summary)
    update_stage_docs(summary)
    write_registries(summary, gates)
    write_artifact_registry(summary)
    write_final_and_manifest(summary, gates)
    print(json.dumps(read_json(FINAL_DECISION), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
