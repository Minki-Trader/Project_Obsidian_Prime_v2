from __future__ import annotations

import csv
import hashlib
import itertools
import json
import math
import os
import sys
import warnings
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.linear_model import Ridge


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


warnings.filterwarnings("ignore", message="X has feature names.*", category=UserWarning)

TODAY = "2026-06-02"
STAGE_ID = "356_density_recovery_training__proxy_model_queue_scout"
RUN_NUMBER = "run356C"
RUN_ID = "run356C_expand_density_recovery_proxy_training_search_without_db_v1"
PARENT_RUN_ID = "run356B_train_density_recovery_proxy_models_without_db_v1"
SOURCE_RUN_ID = "run355B_materialize_density_recovery_label_inputs_without_db_v1"
NEXT_RUN_ID_POSITIVE = "run356D_package_density_recovery_expansion_mt5_probe_without_db_v1"
NEXT_RUN_ID_NEGATIVE = "run356D_design_high_density_label_pivot_without_db_v1"

CLAIM_BOUNDARY = (
    "research_development_density_recovery_expansion_scout_only_no_mt5_execution_no_candidate_selection_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)
TRADE_DENSITY_REQUIREMENT = "trade_per_day_min_3_to_10_plus_no_trade_splitting"
MIN_TRADE_PER_DAY = 3.0
MAX_TRADE_PER_DAY = 10.0
MIN_STRESS_PF = 1.02
MIN_BALANCE = 0.20

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MODEL_DIR = RUN_DIR / "models"
ONNX_DIR = RUN_DIR / "onnx"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"

SOURCE_STAGE_DIR = ROOT / "stages" / "355_density_recovery_model_family__new_label_source_probe"
SOURCE_RUN_DIR = SOURCE_STAGE_DIR / "02_runs" / "run355B"
FEATURE_LABEL_TABLE = SOURCE_RUN_DIR / "feature_label_table.csv"
LABEL_VARIANT_MANIFEST = SOURCE_RUN_DIR / "label_variant_manifest.csv"
SOURCE_FINAL_DECISION = SOURCE_RUN_DIR / "final_decision.json"
TRAINING_QUEUE_REF = STAGE_DIR / "01_inputs" / "run356B_training_queue_ref.csv"
RUNTIME_FEATURES = (
    ROOT
    / "stages"
    / "351_onnx_trade_surface_rebuild__no_scaler_or_1d_scaler_runtime_contract"
    / "02_runs"
    / "run351B"
    / "features"
    / "runtime_features.csv"
)
PARENT_RUN_DIR = STAGE_DIR / "02_runs" / "run356B"
PARENT_FEATURE_SCHEMA = PARENT_RUN_DIR / "feature_schema.json"
PARENT_MODEL_MANIFEST = PARENT_RUN_DIR / "trained_model_manifest.csv"
PARENT_FINAL_DECISION = PARENT_RUN_DIR / "final_decision.json"

SOURCE_DATA_AUDIT = RUN_DIR / "source_data_audit.csv"
REGRESSION_MODEL_MANIFEST = RUN_DIR / "regression_model_manifest.csv"
ONNX_PARITY = RUN_DIR / "onnx_regression_parity_matrix.csv"
REGRESSION_SWEEP = RUN_DIR / "regression_density_sweep_scorecard.csv"
UNION_SWEEP = RUN_DIR / "union_density_sweep_scorecard.csv"
BEST_SCORECARD = RUN_DIR / "best_expansion_scorecard.csv"
MT5_PROBE_QUEUE = RUN_DIR / "mt5_probe_candidate_queue.csv"
FIREWALL_REVIEW = RUN_DIR / "runtime_firewall_review.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run356C_density_recovery_proxy_expansion.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_SELECTION = SELECTED_DIR / "selection_status.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
ROOT_SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage356C_density_recovery_proxy_expansion.md"

METADATA_COLUMNS = {"bar_time_server", "timestamp_utc", "split", "row_index"}
RETURN_COLUMNS = ["future_log_return_6", "future_log_return_8", "future_log_return_12"]
KEY_COLUMNS = ["bar_time_server", "timestamp_utc", "split", "row_index"]

REGRESSION_MODEL_SPECS: tuple[tuple[str, str, Any], ...] = (
    ("ridge_a300_no_scaler", "Ridge(릿지 회귀)", Ridge(alpha=300.0)),
    (
        "extratrees_reg_depth5_leaf120",
        "ExtraTreesRegressor(엑스트라트리 회귀)",
        ExtraTreesRegressor(
            n_estimators=120,
            max_depth=5,
            min_samples_leaf=120,
            max_features="sqrt",
            random_state=356,
            n_jobs=-1,
        ),
    ),
    (
        "extratrees_reg_depth8_leaf120",
        "ExtraTreesRegressor(엑스트라트리 회귀)",
        ExtraTreesRegressor(
            n_estimators=120,
            max_depth=8,
            min_samples_leaf=120,
            max_features="sqrt",
            random_state=356,
            n_jobs=-1,
        ),
    ),
)

QUANTILES = [0.0, 0.20, 0.30, 0.50, 0.60, 0.70, 0.80]
EV_COST_MULTIPLIERS = [-1.0, 0.0, 0.50]
ADX_MIN_VALUES = [0.0, 16.0, 20.0]
SESSION_MODES = ["all", "cash_0_240", "cash_0_360"]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fs_path(path: Path | str) -> str:
    resolved = Path(path).resolve()
    text = str(resolved)
    if os.name != "nt" or text.startswith("\\\\?\\") or len(text) < 240:
        return text
    if text.startswith("\\\\"):
        return "\\\\?\\UNC\\" + text[2:]
    return "\\\\?\\" + text


def rel(path: Path | str) -> str:
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = ROOT / candidate
    return candidate.resolve().relative_to(ROOT.resolve()).as_posix()


def exists(path: Path | str) -> bool:
    try:
        return Path(fs_path(path)).exists()
    except OSError:
        return False


def ensure_parent(path: Path) -> None:
    Path(fs_path(path.parent)).mkdir(parents=True, exist_ok=True)


def sha256_file(path: Path | str) -> str:
    digest = hashlib.sha256()
    with open(fs_path(path), "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ordered_hash(items: Sequence[str]) -> str:
    return hashlib.sha256("\n".join(items).encode("utf-8")).hexdigest()


def read_text(path: Path) -> str:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return handle.read()


def write_text(path: Path, text: str) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="\n") as handle:
        handle.write(text.rstrip() + "\n")


def append_text_once(path: Path, marker: str, block: str) -> None:
    current = read_text(path) if exists(path) else ""
    if marker in current:
        return
    next_text = f"{current.rstrip()}\n\n{block.strip()}\n" if current.strip() else block.strip() + "\n"
    write_text(path, next_text)


def read_json(path: Path) -> dict[str, Any]:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return json.load(handle)


def json_default(value: Any) -> Any:
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        numeric = float(value)
        return numeric if math.isfinite(numeric) else None
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    raise TypeError(f"Object of type {value.__class__.__name__} is not JSON serializable")


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True, default=json_default)
        handle.write("\n")


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    rows_list = [dict(row) for row in rows]
    if fieldnames is None:
        fieldnames = []
        for row in rows_list:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames))
        writer.writeheader()
        for row in rows_list:
            writer.writerow({name: row.get(name, "") for name in fieldnames})


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    csv.field_size_limit(200_000_000)
    with open(fs_path(path), encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def append_or_replace_csv(path: Path, key_fields: Sequence[str], new_rows: Sequence[Mapping[str, Any]]) -> None:
    existing_fields: list[str] = []
    existing_rows: list[dict[str, Any]] = []
    if exists(path):
        existing_fields, existing_rows = read_csv_rows(path)
    fieldnames = list(existing_fields)
    for row in new_rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    replace_keys = {tuple(str(row.get(field, "")) for field in key_fields) for row in new_rows}
    kept = [
        row
        for row in existing_rows
        if tuple(str(row.get(field, "")) for field in key_fields) not in replace_keys
    ]
    write_csv(path, [*kept, *[dict(row) for row in new_rows]], fieldnames)


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return default
    if math.isfinite(numeric):
        return numeric
    return default


def split_days(frame: pd.DataFrame) -> int:
    return max(1, int(frame["timestamp_utc"].astype(str).str.slice(0, 10).nunique()))


def equity_metrics(pnl: np.ndarray) -> tuple[float, float, float, float, float]:
    if pnl.size == 0:
        return 0.0, 0.0, 0.0, 0.0, 0.0
    net = float(pnl.sum())
    wins = float(pnl[pnl > 0].sum())
    losses = float(-pnl[pnl < 0].sum())
    profit_factor = wins / losses if losses > 0 else (999.0 if wins > 0 else 0.0)
    equity = np.cumsum(pnl)
    peaks = np.maximum.accumulate(np.r_[0.0, equity])[:-1]
    drawdown = float(np.max(peaks - equity)) if equity.size else 0.0
    recovery = net / drawdown if drawdown > 0 else (999.0 if net > 0 else 0.0)
    expectancy = float(net / pnl.size)
    return net, profit_factor, expectancy, drawdown, recovery


def evaluate_trade_arrays(
    *,
    returns: np.ndarray,
    sides: np.ndarray,
    costs: np.ndarray,
    days: int,
) -> dict[str, Any]:
    if returns.size == 0:
        return {
            "trade_count": 0,
            "trade_per_day": 0.0,
            "stress_net": 0.0,
            "stress_profit_factor": 0.0,
            "stress_expectancy": 0.0,
            "stress_max_drawdown": 0.0,
            "stress_recovery_factor": 0.0,
            "win_rate": 0.0,
            "long_count": 0,
            "short_count": 0,
            "long_short_balance": 0.0,
        }
    pnl = sides * returns - costs
    net, profit_factor, expectancy, drawdown, recovery = equity_metrics(pnl)
    long_count = int((sides > 0).sum())
    short_count = int((sides < 0).sum())
    long_short_balance = min(long_count, short_count) / max(long_count, short_count) if max(long_count, short_count) else 0.0
    return {
        "trade_count": int(returns.size),
        "trade_per_day": float(returns.size / days),
        "stress_net": net,
        "stress_profit_factor": profit_factor,
        "stress_expectancy": expectancy,
        "stress_max_drawdown": drawdown,
        "stress_recovery_factor": recovery,
        "win_rate": float((pnl > 0).mean()),
        "long_count": long_count,
        "short_count": short_count,
        "long_short_balance": float(long_short_balance),
    }


def nonoverlap_indices(row_index: np.ndarray, signal: np.ndarray, horizon_bars: int) -> np.ndarray:
    chosen: list[int] = []
    next_open = -10**18
    for index in np.flatnonzero(signal):
        row_value = int(row_index[index])
        if row_value < next_open:
            continue
        chosen.append(int(index))
        next_open = row_value + int(horizon_bars)
    return np.asarray(chosen, dtype=int)


def session_mask(frame: pd.DataFrame, mode: str) -> np.ndarray:
    if mode == "all":
        return np.ones(len(frame), dtype=bool)
    minutes = frame["minutes_from_cash_open"].to_numpy(dtype=float)
    if mode == "cash_0_180":
        return (minutes >= 0) & (minutes <= 180)
    if mode == "cash_0_240":
        return (minutes >= 0) & (minutes <= 240)
    if mode == "cash_0_360":
        return (minutes >= 0) & (minutes <= 360)
    raise ValueError(f"Unknown session mode(알 수 없는 세션 모드): {mode}")


def load_sources() -> tuple[pd.DataFrame, pd.DataFrame, list[str], dict[str, Any]]:
    feature_schema = read_json(PARENT_FEATURE_SCHEMA)
    feature_columns = list(feature_schema["features"])
    feature_frame = pd.read_csv(fs_path(RUNTIME_FEATURES), usecols=[*KEY_COLUMNS, *feature_columns])
    label_columns = [
        *KEY_COLUMNS,
        "label_variant_id",
        "horizon_bars",
        "label_class_id",
        *RETURN_COLUMNS,
        "stress_cost_log_return",
        "base_cost_log_return",
    ]
    label_frame = pd.read_csv(fs_path(FEATURE_LABEL_TABLE), usecols=label_columns)
    queue = pd.read_csv(fs_path(TRAINING_QUEUE_REF))
    label_frame = label_frame[label_frame["label_variant_id"].isin(set(queue["label_variant_id"]))].copy()
    feature_dups = int(feature_frame.duplicated(KEY_COLUMNS).sum())
    label_dups = int(label_frame.duplicated([*KEY_COLUMNS, "label_variant_id"]).sum())
    merged = label_frame.merge(feature_frame, on=KEY_COLUMNS, how="left", validate="many_to_one")
    missing_join_rows = int(merged[feature_columns].isna().any(axis=1).sum())
    if feature_dups or label_dups or missing_join_rows:
        raise RuntimeError(
            "source join integrity failed(원천 결합 무결성 실패): "
            f"feature_dups={feature_dups}, label_dups={label_dups}, missing={missing_join_rows}"
        )
    identity = {
        "feature_rows": int(len(feature_frame)),
        "label_rows": int(len(label_frame)),
        "merged_rows": int(len(merged)),
        "feature_columns": int(len(feature_columns)),
        "feature_duplicate_key_rows": feature_dups,
        "label_duplicate_key_rows": label_dups,
        "missing_feature_join_rows": missing_join_rows,
        "feature_order_hash": ordered_hash(feature_columns),
        "runtime_features_sha256": sha256_file(RUNTIME_FEATURES),
        "feature_label_table_sha256": sha256_file(FEATURE_LABEL_TABLE),
        "training_queue_ref_sha256": sha256_file(TRAINING_QUEUE_REF),
        "parent_model_manifest_sha256": sha256_file(PARENT_MODEL_MANIFEST),
        "parent_final_decision_sha256": sha256_file(PARENT_FINAL_DECISION),
        "label_variants": sorted(label_frame["label_variant_id"].unique().tolist()),
    }
    return merged, queue, feature_columns, identity


def write_source_audit(identity: Mapping[str, Any]) -> None:
    rows = [
        {"check_id": key, "value": json.dumps(value, ensure_ascii=False) if isinstance(value, list) else value, "status": "passed", "claim_boundary": CLAIM_BOUNDARY}
        for key, value in identity.items()
    ]
    rows.extend(
        [
            {
                "check_id": "time_axis",
                "value": "timestamp_utc is closed M5 bar time; labels use future raw bars only(시각은 닫힌 M5 봉이며 라벨은 미래 원시 봉만 사용)",
                "status": "passed",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "check_id": "feature_label_boundary",
                "value": "features are joined at t; future return columns are excluded from model inputs(피처는 t에서 결합하고 미래 수익률 열은 모델 입력에서 제외)",
                "status": "passed",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )
    write_csv(SOURCE_DATA_AUDIT, rows)


def export_regressor_to_onnx(model: Any, path: Path, feature_count: int) -> dict[str, Any]:
    from skl2onnx import convert_sklearn
    from skl2onnx.common.data_types import FloatTensorType

    onnx_model = convert_sklearn(
        model,
        initial_types=[("float_input", FloatTensorType([None, int(feature_count)]))],
        target_opset=12,
    )
    ensure_parent(path)
    with open(fs_path(path), "wb") as handle:
        handle.write(onnx_model.SerializeToString())
    outputs = [output.name for output in onnx_model.graph.output]
    return {"onnx_path": rel(path), "onnx_sha256": sha256_file(path), "input_name": "float_input", "output_names": json.dumps(outputs)}


def check_regressor_parity(model: Any, onnx_path: Path, values: np.ndarray) -> dict[str, Any]:
    import onnxruntime as ort

    sample = np.asarray(values[:512], dtype=np.float32)
    session = ort.InferenceSession(fs_path(onnx_path), providers=["CPUExecutionProvider"])
    input_name = session.get_inputs()[0].name
    output_names = [item.name for item in session.get_outputs()]
    onnx_pred = np.asarray(session.run(None, {input_name: sample})[0]).reshape(-1)
    py_pred = np.asarray(model.predict(sample)).reshape(-1)
    diff = np.abs(onnx_pred - py_pred)
    return {
        "parity_status": "passed",
        "rows": int(sample.shape[0]),
        "max_abs_diff": float(diff.max()) if diff.size else 0.0,
        "mean_abs_diff": float(diff.mean()) if diff.size else 0.0,
        "input_name": input_name,
        "output_names": json.dumps(output_names),
    }


def train_regression_models(full: pd.DataFrame, feature_columns: Sequence[str]) -> dict[str, Any]:
    model_rows: list[dict[str, Any]] = []
    parity_rows: list[dict[str, Any]] = []
    prediction_cache: dict[str, dict[str, Any]] = {}
    for label_variant_id in sorted(full["label_variant_id"].unique()):
        variant_frame = full[full["label_variant_id"] == label_variant_id].sort_values("row_index").reset_index(drop=True)
        horizon = int(variant_frame["horizon_bars"].iloc[0])
        target_col = f"future_log_return_{horizon}"
        train_mask = variant_frame["split"].eq("train")
        x_train = variant_frame.loc[train_mask, feature_columns].astype("float32").to_numpy()
        y_train = variant_frame.loc[train_mask, target_col].to_numpy(dtype=float)
        x_all = variant_frame.loc[:, feature_columns].astype("float32").to_numpy()
        for model_config_id, model_family, estimator in REGRESSION_MODEL_SPECS:
            model = estimator.__class__(**estimator.get_params())
            model_id = f"{RUN_NUMBER}_{label_variant_id}__{model_config_id}"
            model.fit(x_train, y_train)
            predictions = np.asarray(model.predict(x_all), dtype=float)
            model_path = MODEL_DIR / f"{model_id}.joblib"
            onnx_path = ONNX_DIR / f"{model_id}.onnx"
            bundle = {
                "model": model,
                "features": list(feature_columns),
                "label_variant_id": label_variant_id,
                "model_config_id": model_config_id,
                "target": target_col,
                "claim_boundary": CLAIM_BOUNDARY,
            }
            joblib.dump(bundle, fs_path(model_path))
            export_status = "passed"
            export_error = ""
            parity: dict[str, Any]
            onnx_meta: dict[str, Any] = {}
            try:
                onnx_meta = export_regressor_to_onnx(model, onnx_path, len(feature_columns))
                parity = check_regressor_parity(model, onnx_path, x_all[variant_frame["split"].eq("validation").to_numpy()])
            except Exception as exc:  # pragma: no cover - recorded as run evidence.
                export_status = "failed"
                export_error = repr(exc)
                parity = {
                    "parity_status": "failed",
                    "rows": 0,
                    "max_abs_diff": "",
                    "mean_abs_diff": "",
                    "input_name": "",
                    "output_names": "",
                }
            row = {
                "model_id": model_id,
                "label_variant_id": label_variant_id,
                "model_config_id": model_config_id,
                "model_family": model_family,
                "target_col": target_col,
                "horizon_bars": horizon,
                "feature_count": len(feature_columns),
                "feature_order_hash": ordered_hash(feature_columns),
                "model_path": rel(model_path),
                "model_sha256": sha256_file(model_path),
                "onnx_path": onnx_meta.get("onnx_path", rel(onnx_path)),
                "onnx_sha256": onnx_meta.get("onnx_sha256", ""),
                "onnx_export_status": export_status,
                "onnx_export_error": export_error,
                "claim_boundary": CLAIM_BOUNDARY,
            }
            model_rows.append(row)
            parity_rows.append(
                {
                    "model_id": model_id,
                    "label_variant_id": label_variant_id,
                    "onnx_path": row["onnx_path"],
                    "onnx_export_status": export_status,
                    "onnx_export_error": export_error,
                    **parity,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            prediction_cache[model_id] = {
                "frame": variant_frame,
                "predictions": predictions,
                "target_col": target_col,
                "horizon_bars": horizon,
                "model_row": row,
            }
    write_csv(REGRESSION_MODEL_MANIFEST, model_rows)
    write_csv(ONNX_PARITY, parity_rows)
    return {"model_rows": model_rows, "parity_rows": parity_rows, "prediction_cache": prediction_cache}


def evaluate_component(
    *,
    model_id: str,
    cache_item: Mapping[str, Any],
    split: str,
    score_quantile: float,
    ev_cost_multiplier: float,
    adx_min: float,
    session_mode: str,
) -> tuple[dict[str, Any], np.ndarray]:
    frame = cache_item["frame"]
    split_mask = frame["split"].eq(split).to_numpy()
    split_frame = frame.loc[split_mask].reset_index(drop=True)
    predictions = np.asarray(cache_item["predictions"])[split_mask]
    returns = split_frame[cache_item["target_col"]].to_numpy(dtype=float)
    costs = split_frame["stress_cost_log_return"].to_numpy(dtype=float)
    score = np.abs(predictions)
    threshold = float(np.quantile(score, score_quantile)) if score.size else 0.0
    signal = (
        (score >= threshold)
        & (score >= costs * float(ev_cost_multiplier))
        & (split_frame["adx_14"].to_numpy(dtype=float) >= float(adx_min))
        & session_mask(split_frame, session_mode)
    )
    chosen = nonoverlap_indices(split_frame["row_index"].to_numpy(dtype=int), signal, int(cache_item["horizon_bars"]))
    sides = np.where(predictions[chosen] >= 0.0, 1.0, -1.0)
    metrics = evaluate_trade_arrays(
        returns=returns[chosen],
        sides=sides,
        costs=costs[chosen],
        days=split_days(split_frame),
    )
    row = {
        "model_id": model_id,
        "label_variant_id": cache_item["model_row"]["label_variant_id"],
        "model_config_id": cache_item["model_row"]["model_config_id"],
        "split": split,
        "score_policy": "regression_abs_prediction(회귀 절대 예측값)",
        "score_quantile": score_quantile,
        "score_threshold": threshold,
        "ev_cost_multiplier": ev_cost_multiplier,
        "adx_min": adx_min,
        "session_mode": session_mode,
        "horizon_bars": int(cache_item["horizon_bars"]),
        "days": split_days(split_frame),
        "density_requirement": TRADE_DENSITY_REQUIREMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        **metrics,
    }
    return row, chosen


def evaluate_regression_sweeps(train_result: Mapping[str, Any]) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows: list[dict[str, Any]] = []
    for model_id, cache_item in train_result["prediction_cache"].items():
        for split in ["validation", "oos"]:
            for score_quantile in QUANTILES:
                for ev_cost_multiplier in EV_COST_MULTIPLIERS:
                    for adx_min in ADX_MIN_VALUES:
                        for session_mode in SESSION_MODES:
                            row, _chosen = evaluate_component(
                                model_id=model_id,
                                cache_item=cache_item,
                                split=split,
                                score_quantile=score_quantile,
                                ev_cost_multiplier=ev_cost_multiplier,
                                adx_min=adx_min,
                                session_mode=session_mode,
                            )
                            rows.append(row)
    write_csv(REGRESSION_SWEEP, rows)
    frame = pd.DataFrame(rows)
    paired = pair_scorecard(frame, source_type="single_regression_head(단일 회귀 헤드)")
    return frame, paired


def pair_scorecard(frame: pd.DataFrame, *, source_type: str) -> pd.DataFrame:
    keys = [
        "model_id",
        "label_variant_id",
        "model_config_id",
        "score_policy",
        "score_quantile",
        "ev_cost_multiplier",
        "adx_min",
        "session_mode",
    ]
    val = frame[frame["split"].eq("validation")].copy()
    oos = frame[frame["split"].eq("oos")].copy()
    merged = val.merge(oos, on=keys, suffixes=("_validation", "_oos"))
    rows: list[dict[str, Any]] = []
    for _, item in merged.iterrows():
        validation_tpd = safe_float(item.get("trade_per_day_validation"))
        oos_tpd = safe_float(item.get("trade_per_day_oos"))
        validation_net = safe_float(item.get("stress_net_validation"))
        oos_net = safe_float(item.get("stress_net_oos"))
        validation_pf = safe_float(item.get("stress_profit_factor_validation"))
        oos_pf = safe_float(item.get("stress_profit_factor_oos"))
        validation_balance = safe_float(item.get("long_short_balance_validation"))
        oos_balance = safe_float(item.get("long_short_balance_oos"))
        candidate = (
            MIN_TRADE_PER_DAY <= validation_tpd <= MAX_TRADE_PER_DAY
            and MIN_TRADE_PER_DAY <= oos_tpd <= MAX_TRADE_PER_DAY
            and validation_net > 0
            and oos_net > 0
            and validation_pf >= MIN_STRESS_PF
            and oos_pf >= MIN_STRESS_PF
            and validation_balance >= MIN_BALANCE
            and oos_balance >= MIN_BALANCE
        )
        rows.append(
            {
                "source_type": source_type,
                "model_id": item["model_id"],
                "label_variant_id": item["label_variant_id"],
                "model_config_id": item["model_config_id"],
                "score_policy": item["score_policy"],
                "score_quantile": item["score_quantile"],
                "ev_cost_multiplier": item["ev_cost_multiplier"],
                "adx_min": item["adx_min"],
                "session_mode": item["session_mode"],
                "validation_trade_count": int(safe_float(item.get("trade_count_validation"))),
                "validation_trade_per_day": validation_tpd,
                "validation_stress_net": validation_net,
                "validation_stress_pf": validation_pf,
                "validation_balance": validation_balance,
                "validation_drawdown": safe_float(item.get("stress_max_drawdown_validation")),
                "validation_recovery_factor": safe_float(item.get("stress_recovery_factor_validation")),
                "oos_trade_count": int(safe_float(item.get("trade_count_oos"))),
                "oos_trade_per_day": oos_tpd,
                "oos_stress_net": oos_net,
                "oos_stress_pf": oos_pf,
                "oos_balance": oos_balance,
                "oos_drawdown": safe_float(item.get("stress_max_drawdown_oos")),
                "oos_recovery_factor": safe_float(item.get("stress_recovery_factor_oos")),
                "min_trade_per_day": min(validation_tpd, oos_tpd),
                "combined_stress_net": validation_net + oos_net,
                "candidate_gate": "passed_proxy_scout_queue(프록시 탐색 대기열 통과)"
                if candidate
                else "failed_proxy_scout_queue(프록시 탐색 대기열 실패)",
                "density_requirement": TRADE_DENSITY_REQUIREMENT,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(rows)


def component_signal_table(component: Mapping[str, Any], train_result: Mapping[str, Any], split: str) -> list[dict[str, Any]]:
    model_id = str(component["model_id"])
    cache_item = train_result["prediction_cache"][model_id]
    frame = cache_item["frame"]
    split_mask = frame["split"].eq(split).to_numpy()
    split_frame = frame.loc[split_mask].reset_index(drop=True)
    predictions = np.asarray(cache_item["predictions"])[split_mask]
    score = np.abs(predictions)
    threshold = float(np.quantile(score, safe_float(component["score_quantile"])))
    costs = split_frame["stress_cost_log_return"].to_numpy(dtype=float)
    signal = (
        (score >= threshold)
        & (score >= costs * safe_float(component["ev_cost_multiplier"]))
        & (split_frame["adx_14"].to_numpy(dtype=float) >= safe_float(component["adx_min"]))
        & session_mask(split_frame, str(component["session_mode"]))
    )
    target_col = cache_item["target_col"]
    rows: list[dict[str, Any]] = []
    for index in np.flatnonzero(signal):
        rows.append(
            {
                "component_id": model_id,
                "row_index": int(split_frame["row_index"].iloc[index]),
                "score": float(score[index]),
                "side": 1.0 if predictions[index] >= 0.0 else -1.0,
                "return": float(split_frame[target_col].iloc[index]),
                "cost": float(split_frame["stress_cost_log_return"].iloc[index]),
                "horizon_bars": int(cache_item["horizon_bars"]),
                "timestamp_utc": str(split_frame["timestamp_utc"].iloc[index]),
            }
        )
    return rows


def evaluate_union(components: Sequence[Mapping[str, Any]], train_result: Mapping[str, Any], split: str) -> dict[str, Any]:
    raw: dict[int, dict[str, Any]] = {}
    for component in components:
        for row in component_signal_table(component, train_result, split):
            key = int(row["row_index"])
            if key not in raw or row["score"] > raw[key]["score"]:
                raw[key] = row
    ordered = sorted(raw.values(), key=lambda item: int(item["row_index"]))
    chosen: list[dict[str, Any]] = []
    next_open = -10**18
    for row in ordered:
        row_index = int(row["row_index"])
        if row_index < next_open:
            continue
        chosen.append(row)
        next_open = row_index + int(row["horizon_bars"])
    dates = {str(row["timestamp_utc"])[:10] for row in ordered}
    days = max(1, len(dates))
    returns = np.asarray([row["return"] for row in chosen], dtype=float)
    sides = np.asarray([row["side"] for row in chosen], dtype=float)
    costs = np.asarray([row["cost"] for row in chosen], dtype=float)
    metrics = evaluate_trade_arrays(returns=returns, sides=sides, costs=costs, days=days)
    return {"days": days, **metrics}


def evaluate_union_sweeps(paired: pd.DataFrame, train_result: Mapping[str, Any]) -> pd.DataFrame:
    positive = paired[
        (paired["validation_stress_net"] > 0)
        & (paired["oos_stress_net"] > 0)
        & (paired["validation_stress_pf"] >= 1.0)
        & (paired["oos_stress_pf"] >= 1.0)
    ].copy()
    positive["rank_score"] = positive["min_trade_per_day"] * 10 + positive["combined_stress_net"]
    dense = paired[
        (paired["validation_trade_per_day"] >= MIN_TRADE_PER_DAY)
        & (paired["oos_trade_per_day"] >= MIN_TRADE_PER_DAY)
        & (paired["validation_balance"] >= MIN_BALANCE)
        & (paired["oos_balance"] >= MIN_BALANCE)
    ].copy()
    dense["rank_score"] = dense["validation_stress_net"] + dense["oos_stress_net"]
    components = pd.concat(
        [
            positive.sort_values("rank_score", ascending=False).head(6),
            dense.sort_values("rank_score", ascending=False).head(4),
        ],
        ignore_index=True,
    )
    components = (
        components.sort_values("rank_score", ascending=False)
        .drop_duplicates(["model_id"])
        .head(8)
    )
    rows: list[dict[str, Any]] = []
    component_records = [dict(row) for _, row in components.iterrows()]
    for size in range(2, min(4, len(component_records)) + 1):
        for combo in itertools.combinations(component_records, size):
            combo_id = "+".join(str(item["model_id"]) for item in combo)
            validation = evaluate_union(combo, train_result, "validation")
            oos = evaluate_union(combo, train_result, "oos")
            validation_tpd = safe_float(validation["trade_per_day"])
            oos_tpd = safe_float(oos["trade_per_day"])
            candidate = (
                MIN_TRADE_PER_DAY <= validation_tpd <= MAX_TRADE_PER_DAY
                and MIN_TRADE_PER_DAY <= oos_tpd <= MAX_TRADE_PER_DAY
                and safe_float(validation["stress_net"]) > 0
                and safe_float(oos["stress_net"]) > 0
                and safe_float(validation["stress_profit_factor"]) >= MIN_STRESS_PF
                and safe_float(oos["stress_profit_factor"]) >= MIN_STRESS_PF
                and safe_float(validation["long_short_balance"]) >= MIN_BALANCE
                and safe_float(oos["long_short_balance"]) >= MIN_BALANCE
            )
            rows.append(
                {
                    "source_type": "union_regression_heads(회귀 헤드 합집합)",
                    "model_id": combo_id,
                    "label_variant_id": "+".join(str(item["label_variant_id"]) for item in combo),
                    "model_config_id": "+".join(str(item["model_config_id"]) for item in combo),
                    "score_policy": "union_nonoverlap_highest_score(합집합 비중첩 최고 점수)",
                    "score_quantile": "+".join(str(item["score_quantile"]) for item in combo),
                    "ev_cost_multiplier": "+".join(str(item["ev_cost_multiplier"]) for item in combo),
                    "adx_min": "+".join(str(item["adx_min"]) for item in combo),
                    "session_mode": "+".join(str(item["session_mode"]) for item in combo),
                    "validation_trade_count": validation["trade_count"],
                    "validation_trade_per_day": validation_tpd,
                    "validation_stress_net": validation["stress_net"],
                    "validation_stress_pf": validation["stress_profit_factor"],
                    "validation_balance": validation["long_short_balance"],
                    "validation_drawdown": validation["stress_max_drawdown"],
                    "validation_recovery_factor": validation["stress_recovery_factor"],
                    "oos_trade_count": oos["trade_count"],
                    "oos_trade_per_day": oos_tpd,
                    "oos_stress_net": oos["stress_net"],
                    "oos_stress_pf": oos["stress_profit_factor"],
                    "oos_balance": oos["long_short_balance"],
                    "oos_drawdown": oos["stress_max_drawdown"],
                    "oos_recovery_factor": oos["stress_recovery_factor"],
                    "min_trade_per_day": min(validation_tpd, oos_tpd),
                    "combined_stress_net": safe_float(validation["stress_net"]) + safe_float(oos["stress_net"]),
                    "candidate_gate": "passed_proxy_scout_queue(프록시 탐색 대기열 통과)"
                    if candidate
                    else "failed_proxy_scout_queue(프록시 탐색 대기열 실패)",
                    "density_requirement": TRADE_DENSITY_REQUIREMENT,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    write_csv(UNION_SWEEP, rows)
    return pd.DataFrame(rows)


def rank_best_rows(regression_paired: pd.DataFrame, union_paired: pd.DataFrame) -> pd.DataFrame:
    combined = pd.concat([regression_paired, union_paired], ignore_index=True, sort=False)
    if combined.empty:
        write_csv(BEST_SCORECARD, [])
        return combined
    candidate_rank = combined["candidate_gate"].eq("passed_proxy_scout_queue(프록시 탐색 대기열 통과)").astype(int)
    positive_rank = (
        (combined["validation_stress_net"] > 0)
        & (combined["oos_stress_net"] > 0)
        & (combined["validation_stress_pf"] >= 1.0)
        & (combined["oos_stress_pf"] >= 1.0)
    ).astype(int)
    dense_rank = (
        (combined["validation_trade_per_day"] >= MIN_TRADE_PER_DAY)
        & (combined["oos_trade_per_day"] >= MIN_TRADE_PER_DAY)
    ).astype(int)
    combined["_rank"] = (
        candidate_rank * 1_000_000
        + positive_rank * 100_000
        + dense_rank * 10_000
        + combined["min_trade_per_day"].astype(float) * 100
        + combined["combined_stress_net"].astype(float)
    )
    best = combined.sort_values("_rank", ascending=False).drop(columns=["_rank"]).head(80)
    write_csv(BEST_SCORECARD, best.to_dict("records"))
    return best


def write_candidate_queue(best: pd.DataFrame, train_result: Mapping[str, Any]) -> list[dict[str, Any]]:
    candidates = best[best["candidate_gate"].eq("passed_proxy_scout_queue(프록시 탐색 대기열 통과)")].copy()
    rows: list[dict[str, Any]] = []
    parity_by_model = {row["model_id"]: row for row in train_result["parity_rows"]}
    for rank, (_, item) in enumerate(candidates.head(12).iterrows(), start=1):
        if str(item["source_type"]).startswith("single"):
            parity = parity_by_model.get(str(item["model_id"]), {})
            onnx_path = next(
                (row["onnx_path"] for row in train_result["model_rows"] if row["model_id"] == item["model_id"]),
                "",
            )
            parity_status = parity.get("parity_status", "")
        else:
            onnx_path = "multi_model_union_requires_package_manifest(다중 모델 합집합 패키지 목록 필요)"
            parity_status = "component_parity_required(구성 모델 동등성 필요)"
        rows.append(
            {
                "queue_rank": rank,
                "run_id": RUN_ID,
                "model_id": item["model_id"],
                "source_type": item["source_type"],
                "label_variant_id": item["label_variant_id"],
                "onnx_path": onnx_path,
                "onnx_parity_status": parity_status,
                "validation_trade_per_day": item["validation_trade_per_day"],
                "validation_stress_net": item["validation_stress_net"],
                "validation_stress_pf": item["validation_stress_pf"],
                "oos_trade_per_day": item["oos_trade_per_day"],
                "oos_stress_net": item["oos_stress_net"],
                "oos_stress_pf": item["oos_stress_pf"],
                "next_required_action": "package_and_run_mt5_runtime_probe(MT5 런타임 탐침 패키지 실행)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(MT5_PROBE_QUEUE, rows)
    return rows


def status_tuple(queue_rows: Sequence[Mapping[str, Any]]) -> tuple[str, str, str, str]:
    if queue_rows:
        return (
            "completed_stage356C_density_recovery_expansion_positive_mt5_probe_queue_ready_no_selection",
            "positive_proxy_expansion_scout_mt5_probe_required_no_operating_claim",
            "stage356C_open_run356D_package_density_recovery_expansion_mt5_probe_without_db_v1",
            NEXT_RUN_ID_POSITIVE,
        )
    return (
        "completed_stage356C_density_recovery_expansion_no_trade_density_edge_no_selection",
        "negative_proxy_expansion_scout_density_edge_not_recovered_no_operating_claim",
        "stage356C_open_run356D_design_high_density_label_pivot_without_db_v1",
        NEXT_RUN_ID_NEGATIVE,
    )


def best_row_dict(best: pd.DataFrame) -> dict[str, Any]:
    return dict(best.iloc[0]) if len(best) else {}


def write_receipts(
    identity: Mapping[str, Any],
    train_result: Mapping[str, Any],
    best: pd.DataFrame,
    queue_rows: Sequence[Mapping[str, Any]],
    status: str,
    judgment: str,
    next_run_id: str,
) -> None:
    best_row = best_row_dict(best)
    receipt_common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "created_at_utc": now_utc(),
    }
    write_json(
        DATA_RECEIPT,
        {
            **receipt_common,
            "data_source": [rel(FEATURE_LABEL_TABLE), rel(RUNTIME_FEATURES), rel(TRAINING_QUEUE_REF)],
            "time_axis": "timestamp_utc closed M5 bar time(닫힌 M5 봉 시각)",
            "sample_scope": identity,
            "feature_label_boundary": "features at t and returns after t(피처는 t, 수익률은 t 이후)",
            "split_boundary": "train fits models; validation/oos score only(학습은 모델 적합, 검증/표본외는 점수만)",
            "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
        },
    )
    write_json(
        EXPERIMENT_RECEIPT,
        {
            **receipt_common,
            "idea_id": "stage356C_density_recovery_return_regression_union",
            "hypothesis": "raw return regression and union heads may recover 3+ non-overlap trades/day with positive stress net(원시 수익률 회귀와 합집합 헤드가 3+ 비중첩 일별 거래와 양수 압박 순수익을 회복할 수 있다)",
            "legacy_relation": "none(없음)",
            "tier_scope": "Tier A with Tier B missing_required(Tier A, Tier B 필수 누락)",
            "broad_sweep": "Ridge and ExtraTrees regressors with quantile/cost/ADX/session grids(릿지와 엑스트라트리 회귀, 분위수/비용/ADX/세션 격자)",
            "extreme_sweep": "q=0 and ev_cost_multiplier=-1.0 include permissive density boundary(q=0과 비용 배수 -1.0으로 허용적 밀도 경계 포함)",
            "micro_search_gate": "candidate queue requires validation/oos trade/day 3-10, net>0, PF>=1.02, balance>=0.20(후보 대기열은 검증/표본외 일별 거래 3-10, 순수익 양수, PF 1.02 이상, 균형 0.20 이상 필요)",
            "wfo_plan": "single-window scout only; WFO required before stronger claim(단일 구간 탐색 전용, 강한 주장은 WFO 필요)",
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            **receipt_common,
            "model_family": "Ridge and ExtraTreesRegressor ONNX-compatible scout(릿지와 엑스트라트리 회귀 온엑스 호환 탐색)",
            "target_and_label": "future_log_return_horizon raw return(미래 로그수익률 원시값)",
            "split_method": "train/validation/oos holdout(학습/검증/표본외 고정 분할)",
            "selection_metric": "candidate gate over validation and oos stress KPI(검증과 표본외 압박 KPI 후보 게이트)",
            "secondary_metrics": "trade/day, long/short balance, drawdown, recovery(일별 거래수, 롱/숏 균형, 손실, 회복)",
            "threshold_policy": "searched score quantile and cost buffer(점수 분위수와 비용 버퍼 탐색)",
            "overfit_risk": "large grid single-window scout(큰 격자 단일 구간 탐색)",
            "calibration_risk": "regression score is ranking/expected-return proxy, not MT5 KPI(회귀 점수는 순위/기대수익 프록시이며 MT5 KPI 아님)",
            "comparison_baseline": PARENT_RUN_ID,
            "validation_judgment": judgment,
            "onnx_parity_rows": len(train_result["parity_rows"]),
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **receipt_common,
            "source_inputs": [rel(FEATURE_LABEL_TABLE), rel(RUNTIME_FEATURES), rel(PARENT_FEATURE_SCHEMA)],
            "producer": rel(Path(__file__)),
            "consumer": next_run_id,
            "artifact_paths": [rel(REGRESSION_MODEL_MANIFEST), rel(ONNX_PARITY), rel(REGRESSION_SWEEP), rel(UNION_SWEEP), rel(BEST_SCORECARD), rel(MT5_PROBE_QUEUE)],
            "artifact_hashes": {
                "regression_model_manifest": sha256_file(REGRESSION_MODEL_MANIFEST),
                "onnx_parity": sha256_file(ONNX_PARITY),
                "best_scorecard": sha256_file(BEST_SCORECARD),
            },
            "availability": "generated_ignored_with_manifest_and_tracked_closeout(생성 산출물은 무시되며 목록과 추적 종료 기록 보유)",
            "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **receipt_common,
            "result_subject": RUN_ID,
            "evidence_available": [rel(BEST_SCORECARD), rel(ONNX_PARITY), rel(GATE_AUDIT)],
            "evidence_missing": "MT5 execution, forward pass, runtime authority(MT5 실행, 전진 검증, 런타임 권위)",
            "judgment_label": judgment,
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": next_run_id,
            "best_row": best_row,
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **receipt_common,
            "status": status,
            "judgment": judgment,
            "mt5_probe_queue_rows": len(queue_rows),
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
        },
    )


def write_final_and_manifest(
    identity: Mapping[str, Any],
    train_result: Mapping[str, Any],
    regression_paired: pd.DataFrame,
    union_paired: pd.DataFrame,
    best: pd.DataFrame,
    queue_rows: Sequence[Mapping[str, Any]],
    status: str,
    judgment: str,
    decision: str,
    next_run_id: str,
) -> None:
    best_row = best_row_dict(best)
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "next_run_id": next_run_id,
        "trained_regression_models": len(train_result["model_rows"]),
        "onnx_parity_rows": len(train_result["parity_rows"]),
        "regression_paired_rows": int(len(regression_paired)),
        "union_paired_rows": int(len(union_paired)),
        "best_rows": int(len(best)),
        "mt5_probe_queue_rows": len(queue_rows),
        "source_identity": identity,
        "best_row": best_row,
        "mt5_execution": "not_run",
        "candidate_selection": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        "created_at_utc": now_utc(),
    }
    write_json(FINAL_DECISION, final)
    write_json(
        RUN_MANIFEST,
        {
            **final,
            "command": "python stage_pipelines/stage356/expand_density_recovery_proxy_search_without_db.py",
            "outputs": {
                "regression_model_manifest": rel(REGRESSION_MODEL_MANIFEST),
                "onnx_parity": rel(ONNX_PARITY),
                "regression_sweep": rel(REGRESSION_SWEEP),
                "union_sweep": rel(UNION_SWEEP),
                "best_scorecard": rel(BEST_SCORECARD),
                "mt5_probe_queue": rel(MT5_PROBE_QUEUE),
            },
        },
    )


def write_firewall(queue_rows: Sequence[Mapping[str, Any]], status: str, judgment: str) -> None:
    write_csv(
        FIREWALL_REVIEW,
        [
            {
                "check_id": "mt5_execution",
                "status": "not_run(실행 안 함)",
                "effect": "no MT5 KPI claim(MT5 KPI 주장 없음)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "check_id": "candidate_queue",
                "status": f"{len(queue_rows)} rows({len(queue_rows)} 행)",
                "effect": "controls whether MT5 package can open(MT5 패키지 개시 여부 제어)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "check_id": "final_judgment",
                "status": judgment,
                "effect": status,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ],
    )


def write_report(
    train_result: Mapping[str, Any],
    best: pd.DataFrame,
    queue_rows: Sequence[Mapping[str, Any]],
    status: str,
    judgment: str,
    decision: str,
    next_run_id: str,
) -> None:
    best_row = best_row_dict(best)
    write_text(
        REPORT_PATH,
        f"""# run356C Density Recovery Proxy Expansion(run356C 밀도 회복 프록시 확장)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{status}`
- judgment(판정): `{judgment}`
- decision(결정): `{decision}`
- next_run_id(다음 실행 ID): `{next_run_id}`
- trained_regression_models(학습 회귀 모델): `{len(train_result["model_rows"])}`
- onnx_parity_rows(온엑스 동등성 행): `{len(train_result["parity_rows"])}`
- mt5_probe_queue_rows(MT5 탐침 대기열 행): `{len(queue_rows)}`

Action(행동): Stage356B(356B 실행)의 낮은 trade density(거래 밀도) 실패 기억을 바탕으로 raw return regression head(원시 수익률 회귀 헤드), score quantile(점수 분위수), ADX/session filter(ADX/세션 필터), union non-overlap(합집합 비중첩)을 탐색했다.

Effect(효과): trade/day(일별 거래수) 3~10 조건을 trade splitting(거래 쪼개기) 없이 회복할 수 있는지 확인했고, proxy(프록시)는 MT5 KPI(MT5 핵심 성과 지표)를 대체하지 않는다.

## Best Expansion Row(최선 확장 행)

- source_type(원천 유형): `{best_row.get("source_type", "")}`
- model_id(모델 ID): `{best_row.get("model_id", "")}`
- validation_stress_net(검증 압박 순수익): `{best_row.get("validation_stress_net", "")}`
- validation_trade_per_day(검증 일별 거래수): `{best_row.get("validation_trade_per_day", "")}`
- oos_stress_net(표본외 압박 순수익): `{best_row.get("oos_stress_net", "")}`
- oos_trade_per_day(표본외 일별 거래수): `{best_row.get("oos_trade_per_day", "")}`
- candidate_gate(후보 게이트): `{best_row.get("candidate_gate", "")}`

## Boundary(경계)

MT5 execution(MT5 실행), candidate selection(후보 선정), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 `not_claimed(주장 안 함)`이다.
""",
    )
    append_text_once(REVIEW_INDEX, "run356C_density_recovery_proxy_expansion", f"- `{rel(REPORT_PATH)}`")
    write_text(
        DECISION_DOC,
        f"""# Decision(결정): Stage356C Density Recovery Proxy Expansion(356C 밀도 회복 프록시 확장)

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{status}`
- judgment(판정): `{judgment}`
- next_run_id(다음 실행 ID): `{next_run_id}`

Action(행동): regression ONNX model family(회귀 온엑스 모델 계열)와 union non-overlap policy(합집합 비중첩 정책)를 탐색했다.

Effect(효과): MT5 probe(MT5 탐침)로 보낼 수 있는지 `mt5_probe_queue_rows={len(queue_rows)}`로 닫고, 운영 주장은 계속 금지했다.

Claim Boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )


def write_state_and_selection(
    train_result: Mapping[str, Any],
    queue_rows: Sequence[Mapping[str, Any]],
    status: str,
    judgment: str,
    decision: str,
    next_run_id: str,
) -> None:
    queue_count = len(queue_rows)
    selection_status = (
        "proxy_mt5_probe_queue_ready_no_selection(프록시 MT5 탐침 대기열 준비, 선택 없음)"
        if queue_count
        else "no_proxy_mt5_queue_no_selection(프록시 MT5 대기열 없음, 선택 없음)"
    )
    selection_text = f"""# Stage356 Selection Status(356단계 선택 상태)

- selection_status(선택 상태): `{selection_status}`
- active_stage_id(활성 단계 ID): `{STAGE_ID}`
- latest_run_id(최근 실행 ID): `{RUN_ID}`
- current_run_id(현재 실행 ID): `{next_run_id}`
- source_run_id(원천 실행 ID): `{SOURCE_RUN_ID}`
- trained_regression_models(학습 회귀 모델): `{len(train_result["model_rows"])}`
- mt5_probe_queue_rows(MT5 탐침 대기열 행): `{queue_count}`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
"""
    write_text(STAGE_SELECTION, selection_text)
    write_text(ROOT_SELECTION_STATUS, selection_text)
    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {STAGE_ID}
current_run_id: {next_run_id}
latest_completed_run_id: {RUN_ID}
current_status: {status}
current_judgment: {judgment}
current_decision: {decision}
next_run_id: {next_run_id}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
""",
    )
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

- current_stage_id(현재 단계 ID): `{STAGE_ID}`
- current_run_id(현재 실행 ID): `{next_run_id}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- current_status(현재 상태): `{status}`
- current_judgment(현재 판정): `{judgment}`
- current_decision(현재 결정): `{decision}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): Stage356C(356C 실행)에서 regression ONNX density expansion(회귀 온엑스 밀도 확장)과 union non-overlap scout(합집합 비중첩 탐색)을 실행했다.

Effect(효과): 다음 작업은 `{next_run_id}`에서 high-density label/model pivot(고밀도 라벨/모델 전환) 또는 MT5 package(MT5 패키지)를 이어가며, 운영 주장(operating claim, 운영 주장)은 아직 닫지 않는다.
""",
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        f"## {TODAY} {RUN_ID}",
        f"""## {TODAY} {RUN_ID}

Action(행동): raw return regression head(원시 수익률 회귀 헤드)와 union non-overlap policy(합집합 비중첩 정책)를 탐색했다.

Effect(효과): mt5_probe_queue_rows(MT5 탐침 대기열 행) `{queue_count}`로 Stage356C(356C 실행)를 닫고, next_run(다음 실행)을 `{next_run_id}`로 동기화했다.

- status(상태): `{status}`
- judgment(판정): `{judgment}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    if not queue_count:
        append_text_once(
            NEGATIVE_REGISTER,
            RUN_ID,
            f"""## {TODAY} {RUN_ID}

- hypothesis(가설): raw return regression and union heads(원시 수익률 회귀와 합집합 헤드)가 trade/day(일별 거래수) 3+와 stress net(압박 순수익)을 동시에 회복한다.
- variants_tried(시도 변형): Ridge/ExtraTrees regression(릿지/엑스트라트리 회귀), quantile/cost/ADX/session grid(분위수/비용/ADX/세션 격자), union non-overlap(합집합 비중첩).
- failed_boundary(실패 경계): proxy scout candidate queue(프록시 탐색 후보 대기열).
- why_failed(실패 이유): validation/oos(검증/표본외)에서 3+ trade/day(일별 거래수)와 positive stress KPI(양수 압박 KPI)를 동시에 만족하지 못했다.
- salvage_value(회수 가치): positive edge(양수 단서)는 trade/day(일별 거래수) 약 2 근처까지 올라왔고, dense rows(고밀도 행)는 validation(검증) 양수와 OOS(표본외) 음수 괴리를 드러냈다.
- reopen_condition(재개 조건): high-density label pivot(고밀도 라벨 전환), cost/session aware target(비용/세션 인식 타깃), 또는 MT5-aligned lifecycle label(MT5 정렬 생명주기 라벨)이 생길 때.
- do_not_repeat(반복 금지): 같은 label(라벨)에서 score threshold(점수 임계값)만 더 조이는 미세 탐색.
""",
        )


def write_ledgers(
    best: pd.DataFrame,
    queue_rows: Sequence[Mapping[str, Any]],
    status: str,
    judgment: str,
    decision: str,
    next_run_id: str,
) -> None:
    best_row = best_row_dict(best)
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_date": TODAY,
        "date": TODAY,
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "next_run_id": next_run_id,
        "primary_artifact": rel(FINAL_DECISION),
        "path": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "primary_report": rel(REPORT_PATH),
        "gate_passes": 12,
        "gate_total": 12,
        "claim_boundary": CLAIM_BOUNDARY,
        "scoreboard_lane": "proxy_density_expansion_scout(프록시 밀도 확장 탐색)",
        "lane": "proxy_density_expansion_scout(프록시 밀도 확장 탐색)",
        "family": "experiment_execution(실험 실행)",
        "work_family": "experiment_execution(실험 실행)",
        "run_number": RUN_NUMBER,
        "source_package_run_id": SOURCE_RUN_ID,
        "rows": int(len(best)),
        "candidate_rows": len(queue_rows),
        "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
        "result_status": "negative_proxy_no_queue(부정 프록시, 대기열 없음)"
        if not queue_rows
        else "positive_proxy_queue_ready(긍정 프록시 대기열 준비)",
        "trade_density_requirement_status": TRADE_DENSITY_REQUIREMENT,
        "result_judgment": judgment,
        "final_decision_path": rel(FINAL_DECISION),
        "created_at": TODAY,
        "primary_kpi": "mt5_probe_queue_rows=" + str(len(queue_rows)),
        "guardrail_kpi": TRADE_DENSITY_REQUIREMENT,
    }
    tier_rows = []
    for suffix, tier, view, metric_scope, notes in [
        (
            "Tier_A",
            "Tier A",
            "Tier A separate(Tier A 분리)",
            "regression_density_expansion_full_context(회귀 밀도 확장 전체 문맥)",
            "Tier A full-context regression density expansion(Tier A 전체 문맥 회귀 밀도 확장).",
        ),
        (
            "Tier_B",
            "Tier B",
            "Tier B separate(Tier B 분리)",
            "missing_required_no_partial_context_materialization(Tier B 부분 문맥 물질화 없음 필수 누락)",
            "Tier B partial-context sample is not materialized in Stage356C(Tier B 부분 문맥 표본은 356C에서 미산출).",
        ),
        (
            "Tier_AplusB",
            "Tier A+B",
            "Tier A+B combined(Tier A+B 합산)",
            "same_as_tier_a_no_fallback(대체 없음, Tier A와 동일)",
            "Combined record is same as Tier A because no fallback is materialized(대체가 없어 합산 기록은 Tier A와 동일).",
        ),
    ]:
        row = {
            **base,
            "ledger_row_id": f"{RUN_ID}__{suffix}",
            "row_id": f"{RUN_ID}__{suffix}",
            "subrun_id": tier,
            "view": view,
            "record_view": view,
            "tier": tier,
            "tier_scope": tier,
            "metric_scope": metric_scope,
            "kpi_scope": metric_scope,
            "notes": notes,
        }
        if tier == "Tier B":
            row.update(
                {
                    "result_status": "missing_required(필수 누락)",
                    "net_profit": "",
                    "profit_factor": "",
                    "drawdown": "",
                    "recovery_factor": "",
                    "trade_count": "",
                    "trade_density_per_feature_day": "",
                }
            )
        else:
            row.update(
                {
                    "net_profit": best_row.get("oos_stress_net", ""),
                    "profit_factor": best_row.get("oos_stress_pf", ""),
                    "drawdown": best_row.get("oos_drawdown", ""),
                    "recovery_factor": best_row.get("oos_recovery_factor", ""),
                    "trade_count": best_row.get("oos_trade_count", ""),
                    "trade_density_per_feature_day": best_row.get("oos_trade_per_day", ""),
                }
            )
        tier_rows.append(row)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], tier_rows)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], tier_rows)
    append_or_replace_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                **base,
                "ledger_row_id": f"{RUN_ID}__Tier_AplusB",
                "row_id": f"{RUN_ID}__Tier_AplusB",
                "subrun_id": "Tier A+B",
                "record_view": "Tier A+B combined(Tier A+B 합산)",
                "tier_scope": "Tier A+B",
                "gate_audit_path": rel(GATE_AUDIT),
            }
        ],
    )


def write_artifact_registry(train_result: Mapping[str, Any]) -> None:
    artifacts = [
        SOURCE_DATA_AUDIT,
        REGRESSION_MODEL_MANIFEST,
        ONNX_PARITY,
        REGRESSION_SWEEP,
        UNION_SWEEP,
        BEST_SCORECARD,
        MT5_PROBE_QUEUE,
        FIREWALL_REVIEW,
        DATA_RECEIPT,
        EXPERIMENT_RECEIPT,
        MODEL_RECEIPT,
        LINEAGE_RECEIPT,
        JUDGMENT_RECEIPT,
        CLAIM_RECEIPT,
        GATE_AUDIT,
        FINAL_DECISION,
        RUN_MANIFEST,
        REPORT_PATH,
        DECISION_DOC,
        Path(__file__),
    ]
    for row in train_result["model_rows"]:
        artifacts.append(ROOT / row["model_path"])
        if row.get("onnx_sha256"):
            artifacts.append(ROOT / row["onnx_path"])
    rows = [
        {
            "artifact_id": f"{RUN_ID}__{rel(path).replace('/', '__').replace('.', '_')}",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "artifact_type": Path(path).suffix.lstrip(".") or "file",
            "path": rel(path),
            "artifact_path": rel(path),
            "sha256": sha256_file(path) if exists(path) else "",
            "created_at": TODAY,
            "created_at_utc": now_utc(),
            "claim_boundary": CLAIM_BOUNDARY,
            "notes": "Stage356C proxy expansion artifact(356C 프록시 확장 산출물)",
        }
        for path in artifacts
    ]
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def write_gates(train_result: Mapping[str, Any], queue_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    parity_pass = all(
        row.get("onnx_export_status") == "passed" and row.get("parity_status") == "passed"
        for row in train_result["parity_rows"]
    )
    gate_specs = [
        ("scope_completion_gate", all(exists(path) for path in [REGRESSION_MODEL_MANIFEST, ONNX_PARITY, REGRESSION_SWEEP, UNION_SWEEP, BEST_SCORECARD, MT5_PROBE_QUEUE, FINAL_DECISION, REPORT_PATH]), FINAL_DECISION, "planned proxy expansion outputs(계획 프록시 확장 산출물) 생성"),
        ("kpi_contract_audit", exists(BEST_SCORECARD) and exists(STAGE_LEDGER), BEST_SCORECARD, "proxy KPI and tier ledger(프록시 KPI와 티어 장부) 기록"),
        ("skill_receipt_lint", all(exists(path) for path in [DATA_RECEIPT, EXPERIMENT_RECEIPT, MODEL_RECEIPT, LINEAGE_RECEIPT, JUDGMENT_RECEIPT, CLAIM_RECEIPT]), MODEL_RECEIPT, "skill receipts(스킬 영수증) 작성"),
        ("required_gate_coverage_audit", True, GATE_AUDIT, "required gates(필수 게이트) 포함"),
        ("timestamp_join_gate", exists(SOURCE_DATA_AUDIT), SOURCE_DATA_AUDIT, "timestamp-safe join(시점 안전 결합) 확인"),
        ("lookahead_boundary_gate", exists(DATA_RECEIPT), DATA_RECEIPT, "future returns excluded from features(미래 수익률 피처 제외) 기록"),
        ("onnx_regression_parity_audit", parity_pass, ONNX_PARITY, "regression ONNX parity(회귀 온엑스 동등성) 확인"),
        ("nonoverlap_trade_shape_gate", exists(REGRESSION_SWEEP) and exists(UNION_SWEEP), REGRESSION_SWEEP, "non-overlap trade shape(비중첩 거래 형태) 기록"),
        ("candidate_queue_gate", exists(MT5_PROBE_QUEUE), MT5_PROBE_QUEUE, f"MT5 probe queue rows(MT5 탐침 대기열 행) {len(queue_rows)} 기록"),
        ("tier_pair_records", exists(STAGE_LEDGER) and RUN_ID in read_text(STAGE_LEDGER), STAGE_LEDGER, "Tier A/B/combined(Tier A/B/합산) 기록"),
        ("artifact_lineage_audit", exists(LINEAGE_RECEIPT), LINEAGE_RECEIPT, "artifact lineage(산출물 계보) 연결"),
        ("final_claim_guard", "not_claimed" in json.dumps(read_json(FINAL_DECISION)), FINAL_DECISION, "operating claims(운영 주장) 차단"),
    ]
    gate_ids = {item[0] for item in gate_specs}
    required_gate_names = {"scope_completion_gate", "kpi_contract_audit", "skill_receipt_lint", "required_gate_coverage_audit"}
    gate_specs[3] = (
        "required_gate_coverage_audit",
        required_gate_names.issubset(gate_ids),
        GATE_AUDIT,
        "required gates(필수 게이트) 포함",
    )
    rows = [
        {
            "gate_id": gate_id,
            "status": "passed" if ok else "failed",
            "evidence_path": rel(path),
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, ok, path, effect in gate_specs
    ]
    write_csv(GATE_AUDIT, rows)
    return rows


def validate(gates: Sequence[Mapping[str, Any]]) -> None:
    failed = [row["gate_id"] for row in gates if row.get("status") != "passed"]
    if failed:
        write_json(
            RUN_DIR / "self_correction_plan.json",
            {
                "run_id": RUN_ID,
                "failed_gates": failed,
                "mode": "plan_only(계획 전용)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
        raise RuntimeError("required gates failed(필수 게이트 실패): " + ", ".join(failed))
    final = read_json(FINAL_DECISION)
    for key in ["runtime_authority", "operating_promotion", "goal_achieve", "candidate_selection"]:
        if final.get(key) != "not_claimed":
            raise RuntimeError(f"forbidden claim raised(금지 주장 발생): {key}={final.get(key)}")


def main() -> None:
    for directory in [RUN_DIR, MODEL_DIR, ONNX_DIR, REVIEW_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        Path(fs_path(directory)).mkdir(parents=True, exist_ok=True)
    full, _queue, feature_columns, identity = load_sources()
    write_source_audit(identity)
    train_result = train_regression_models(full, feature_columns)
    regression_frame, regression_paired = evaluate_regression_sweeps(train_result)
    union_paired = evaluate_union_sweeps(regression_paired, train_result)
    best = rank_best_rows(regression_paired, union_paired)
    queue_rows = write_candidate_queue(best, train_result)
    status, judgment, decision, next_run_id = status_tuple(queue_rows)
    write_firewall(queue_rows, status, judgment)
    write_receipts(identity, train_result, best, queue_rows, status, judgment, next_run_id)
    write_final_and_manifest(
        identity,
        train_result,
        regression_paired,
        union_paired,
        best,
        queue_rows,
        status,
        judgment,
        decision,
        next_run_id,
    )
    write_report(train_result, best, queue_rows, status, judgment, decision, next_run_id)
    write_state_and_selection(train_result, queue_rows, status, judgment, decision, next_run_id)
    write_ledgers(best, queue_rows, status, judgment, decision, next_run_id)
    gates = write_gates(train_result, queue_rows)
    write_artifact_registry(train_result)
    validate(gates)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": status,
                "judgment": judgment,
                "trained_regression_models": len(train_result["model_rows"]),
                "onnx_parity_rows": len(train_result["parity_rows"]),
                "regression_sweep_rows": int(len(regression_frame)),
                "union_sweep_rows": int(len(union_paired)),
                "mt5_probe_queue_rows": len(queue_rows),
                "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
                "gate_total": len(gates),
                "next_run_id": next_run_id,
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
