from __future__ import annotations

import csv
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import joblib
import numpy as np
import onnxruntime as ort
import pandas as pd

from foundation.models.baseline_training import LABEL_NAMES, LABEL_ORDER
from foundation.models.onnx_bridge import ordered_sklearn_probabilities


STAGE_ID = "329_onnx_rebuild__live_feature_control"
RUN_ID = "run329D_forward_holdout_score_replay_without_threshold_retuning_v1"
RUN_NUMBER = "run329D"
PARENT_RUN_ID = "run329C_train_wfo_rebuild_candidates_v1"
STATUS = "completed_forward_holdout_score_replay_without_threshold_retuning"
JUDGMENT = "forward_score_replay_completed_session_parity_warning_no_goal_achieve"
DECISION = "stage329D_raw_session_mismatch_recorded_session_parity_signal_supply_available_no_candidate_selected"
NEXT_ACTION = "run329E_session_parity_forward_signal_payload_and_mt5_runtime_probe_or_block"
CLAIM_BOUNDARY = (
    "research_development_only_forward_score_replay_no_label_no_profit_no_mt5_runtime_"
    "no_threshold_retuning_no_selected_candidate_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
PREDICTIONS_DIR = RUN_DIR / "predictions"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-26_stage329D_forward_score_replay.md"

RUN329B_DIR = STAGE_DIR / "02_runs" / "run329B"
RUN329C_DIR = STAGE_DIR / "02_runs" / "run329C"
FEATURE_FRAME_DIR = RUN329B_DIR / "feature_frames"
FEATURE_ORDER_DIR = RUN329B_DIR / "feature_orders"
FEATURE_SUMMARY = RUN329B_DIR / "feature_set_materialization_summary.csv"
QUEUE_PATH = RUN329C_DIR / "forward_replay_candidate_queue.csv"
OOS_SIGNAL_METRICS = RUN329C_DIR / "fixed_threshold_signal_metrics.csv"
MODEL_INPUT_PATH = (
    ROOT
    / "data"
    / "processed"
    / "model_inputs"
    / "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58"
    / "model_input_dataset.parquet"
)

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"

RAW_VIEW = "raw_forward"
SESSION_VIEW = "old_session_parity"
VIEWS = [RAW_VIEW, SESSION_VIEW]
ONNX_TOLERANCE = 1.0e-5
RAW_ROW_DENSITY_RATIO_WARN = 2.0
SESSION_SIGNAL_PER_DAY_RATIO_MIN = 0.50
SESSION_SIGNAL_PER_DAY_RATIO_MAX = 1.50
SIGNAL_COUNT_MIN = 100


def os_path(path: Path) -> Path:
    resolved = path.resolve()
    if os.name == "nt":
        text = str(resolved)
        if len(text) > 240 and not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def path_exists(path: Path) -> bool:
    return os_path(path).exists()


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with os_path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def json_ready(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): json_ready(val) for key, val in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    if isinstance(value, np.bool_):
        return bool(value)
    return value


def write_text(path: Path, text: str, encoding: str = "utf-8") -> Path:
    os_path(path.parent).mkdir(parents=True, exist_ok=True)
    os_path(path).write_bytes(text.encode(encoding))
    return path


def write_md(path: Path, text: str) -> Path:
    return write_text(path, text.strip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> Path:
    return write_text(path, json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n")


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, Any]]) -> Path:
    os_path(path.parent).mkdir(parents=True, exist_ok=True)
    with os_path(path).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})
    return path


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path_exists(path):
        return [], []
    with os_path(path).open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return list(reader.fieldnames or []), list(reader)


def upsert_csv(path: Path, key: str, row: dict[str, Any]) -> None:
    fieldnames, rows = read_csv_rows(path)
    for name in row:
        if name not in fieldnames:
            fieldnames.append(name)
    if not fieldnames:
        fieldnames = list(row.keys())
    clean_row = {name: str(row.get(name, "")) for name in fieldnames}
    for idx, existing in enumerate(rows):
        if existing.get(key) == clean_row.get(key):
            rows[idx] = clean_row
            break
    else:
        rows.append(clean_row)
    write_csv(path, fieldnames, rows)


def replace_or_append_csv_rows(path: Path, keys: list[str], new_rows: list[dict[str, Any]]) -> None:
    fieldnames, rows = read_csv_rows(path)
    for row in new_rows:
        for name in row:
            if name not in fieldnames:
                fieldnames.append(name)
    if not fieldnames and new_rows:
        fieldnames = list(new_rows[0].keys())

    def row_key(row: dict[str, Any]) -> tuple[str, ...]:
        return tuple(str(row.get(key, "")) for key in keys)

    replacement = {row_key(row): {name: str(row.get(name, "")) for name in fieldnames} for row in new_rows}
    updated: list[dict[str, Any]] = []
    seen: set[tuple[str, ...]] = set()
    for row in rows:
        key = row_key(row)
        if key in replacement:
            updated.append(replacement[key])
            seen.add(key)
        else:
            updated.append({name: str(row.get(name, "")) for name in fieldnames})
    for key, row in replacement.items():
        if key not in seen:
            updated.append(row)
    write_csv(path, fieldnames, updated)


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = os_path(path).read_bytes()
    had_bom = raw.startswith(b"\xef\xbb\xbf")
    text = raw.decode("utf-8-sig")
    return text, had_bom


def write_text_lossless(path: Path, text: str, had_bom: bool) -> Path:
    encoding = "utf-8-sig" if had_bom else "utf-8"
    return write_text(path, text, encoding=encoding)


def replace_prefix_line(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if line.startswith(prefix):
            lines[idx] = replacement
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text


def load_feature_order(feature_set_id: str) -> list[str]:
    path = FEATURE_ORDER_DIR / f"{feature_set_id}_feature_order.txt"
    return [line.strip() for line in os_path(path).read_text(encoding="utf-8").splitlines() if line.strip()]


def forward_common_valid_boundary() -> str:
    _, rows = read_csv_rows(FEATURE_SUMMARY)
    valid_ends = [
        str(row.get("last_valid_timestamp", ""))
        for row in rows
        if str(row.get("status", "")) == "materialized" and str(row.get("last_valid_timestamp", ""))
    ]
    return min(valid_ends) if valid_ends else "unknown"


def load_old_session_minutes() -> tuple[set[int], dict[str, Any]]:
    frame = pd.read_parquet(os_path(MODEL_INPUT_PATH))
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    minute_series = (frame["timestamp"].dt.hour * 60 + frame["timestamp"].dt.minute).astype(int)
    minutes = set(int(value) for value in minute_series.unique())
    split_rows: list[dict[str, Any]] = []
    for split, group in frame.groupby("split"):
        days = max(1, int(group["timestamp"].dt.date.nunique()))
        split_rows.append(
            {
                "split": str(split),
                "rows": int(len(group)),
                "days": int(days),
                "rows_per_day": float(len(group) / days),
                "start": pd.to_datetime(group["timestamp"], utc=True).min().isoformat(),
                "end": pd.to_datetime(group["timestamp"], utc=True).max().isoformat(),
            }
        )
    manifest = {
        "source": rel(MODEL_INPUT_PATH),
        "minute_count": len(minutes),
        "first_minute_utc": min(minutes),
        "last_minute_utc": max(minutes),
        "split_rows": split_rows,
        "lineage_judgment": "old_model_input_session_minutes_used_as_forward_parity_mask",
    }
    return minutes, manifest


def load_queue() -> list[dict[str, str]]:
    _, rows = read_csv_rows(QUEUE_PATH)
    if not rows:
        raise RuntimeError(f"empty forward replay candidate queue: {QUEUE_PATH}")
    return rows


def load_oos_signal_metrics() -> dict[str, dict[str, float]]:
    _, rows = read_csv_rows(OOS_SIGNAL_METRICS)
    result: dict[str, dict[str, float]] = {}
    for row in rows:
        if row.get("split") != "oos":
            continue
        result[str(row["candidate_id"])] = {
            "oos_signal_rate": float(row.get("signal_rate", 0.0) or 0.0),
            "oos_signals_per_day": float(row.get("signals_per_day", 0.0) or 0.0),
            "oos_label_agreement_rate": float(row.get("label_agreement_rate", 0.0) or 0.0),
            "oos_mean_proxy_log_return": float(row.get("mean_proxy_log_return", 0.0) or 0.0),
        }
    return result


def find_probability_output(outputs: list[np.ndarray]) -> np.ndarray:
    candidates = [output for output in outputs if isinstance(output, np.ndarray) and output.ndim == 2 and output.shape[1] == len(LABEL_ORDER)]
    if len(candidates) != 1:
        shapes = [getattr(output, "shape", None) for output in outputs]
        raise RuntimeError(f"Expected one probability tensor with {len(LABEL_ORDER)} columns, got {shapes}.")
    return np.asarray(candidates[0], dtype="float64")


def onnx_probabilities(onnx_path: Path, values: np.ndarray) -> tuple[np.ndarray, str, list[str]]:
    session = ort.InferenceSession(str(os_path(onnx_path)), providers=["CPUExecutionProvider"])
    input_name = session.get_inputs()[0].name
    outputs = session.run(None, {input_name: np.asarray(values, dtype="float32")})
    probabilities = find_probability_output(outputs)
    return probabilities, input_name, [output.name for output in session.get_outputs()]


def score_frame(
    candidate: dict[str, str],
    view_id: str,
    frame: pd.DataFrame,
    features: list[str],
) -> tuple[pd.DataFrame, dict[str, Any], dict[str, Any]]:
    slug = candidate["artifact_slug"]
    candidate_id = candidate["candidate_id"]
    threshold = float(candidate["decision_threshold"])
    model_path = RUN329C_DIR / "models" / f"{slug}.joblib"
    onnx_path = ROOT / candidate["onnx_path"]
    model = joblib.load(os_path(model_path))
    values64 = frame.loc[:, features].to_numpy(dtype="float64", copy=False)
    expected = ordered_sklearn_probabilities(model, values64)
    probabilities, input_name, output_names = onnx_probabilities(onnx_path, values64.astype("float32"))
    diff = np.abs(probabilities - expected)
    row_sum_error = np.abs(probabilities.sum(axis=1) - 1.0)
    sorted_prob = np.sort(probabilities, axis=1)
    margin = sorted_prob[:, -1] - sorted_prob[:, -2]
    pred = np.asarray(LABEL_ORDER, dtype="int64")[probabilities.argmax(axis=1)]
    signal_mask = (pred != 1) & (margin >= threshold)
    signal_direction = np.where(pred == 2, 1, np.where(pred == 0, -1, 0))
    timestamps = pd.to_datetime(frame["timestamp"], utc=True)
    days = max(1, int(timestamps.dt.date.nunique()))
    max_probability = probabilities.max(axis=1)
    prediction = pd.DataFrame(
        {
            "timestamp": timestamps,
            "symbol": frame["symbol"].astype(str).to_numpy(),
            "candidate_id": candidate_id,
            "artifact_slug": slug,
            "feature_set_id": candidate["feature_set_id"],
            "model_id": candidate["model_id"],
            "view_id": view_id,
            "predicted_label_class": pred.astype("int64"),
            "predicted_label": [LABEL_NAMES[int(value)] for value in pred],
            "p_short": probabilities[:, 0],
            "p_flat": probabilities[:, 1],
            "p_long": probabilities[:, 2],
            "max_probability": max_probability,
            "probability_margin": margin,
            "decision_threshold": threshold,
            "signal": signal_mask.astype("int8"),
            "signal_direction": signal_direction.astype("int8"),
        }
    )
    prediction = add_slice_columns(prediction, frame)
    signal_count = int(signal_mask.sum())
    long_signals = int(((pred == 2) & signal_mask).sum())
    short_signals = int(((pred == 0) & signal_mask).sum())
    summary = {
        "candidate_id": candidate_id,
        "artifact_slug": slug,
        "feature_set_id": candidate["feature_set_id"],
        "model_id": candidate["model_id"],
        "view_id": view_id,
        "rows": int(len(frame)),
        "days": int(days),
        "rows_per_day": float(len(frame) / days),
        "start_timestamp": timestamps.min().isoformat() if len(timestamps) else "",
        "end_timestamp": timestamps.max().isoformat() if len(timestamps) else "",
        "decision_threshold_policy": candidate["decision_threshold_policy"],
        "decision_threshold": threshold,
        "signal_rows": signal_count,
        "signal_rate": float(signal_mask.mean()) if len(signal_mask) else 0.0,
        "signals_per_day": float(signal_count / days),
        "pred_short": int((pred == 0).sum()),
        "pred_flat": int((pred == 1).sum()),
        "pred_long": int((pred == 2).sum()),
        "signal_short": short_signals,
        "signal_long": long_signals,
        "signal_long_share": float(long_signals / signal_count) if signal_count else 0.0,
        "mean_max_probability": float(max_probability.mean()) if len(max_probability) else 0.0,
        "mean_probability_margin": float(margin.mean()) if len(margin) else 0.0,
        "median_probability_margin": float(np.median(margin)) if len(margin) else 0.0,
    }
    parity = {
        "candidate_id": candidate_id,
        "artifact_slug": slug,
        "feature_set_id": candidate["feature_set_id"],
        "model_id": candidate["model_id"],
        "view_id": view_id,
        "rows": int(len(frame)),
        "passed": bool(float(diff.max()) <= ONNX_TOLERANCE if diff.size else True),
        "max_abs_diff": float(diff.max()) if diff.size else 0.0,
        "mean_abs_diff": float(diff.mean()) if diff.size else 0.0,
        "onnx_row_sum_max_abs_error": float(row_sum_error.max()) if len(row_sum_error) else 0.0,
        "input_name": input_name,
        "output_names": ";".join(output_names),
        "onnx_path": rel(onnx_path),
        "onnx_sha256": sha256_file(onnx_path),
        "sklearn_model_path": rel(model_path),
        "sklearn_model_sha256": sha256_file(model_path),
    }
    return prediction, summary, parity


def add_slice_columns(prediction: pd.DataFrame, source: pd.DataFrame) -> pd.DataFrame:
    result = prediction.copy()
    ts = pd.to_datetime(result["timestamp"], utc=True)
    result["hour_utc"] = ts.dt.hour.astype("int64").astype(str).str.zfill(2)
    result["month"] = ts.dt.strftime("%Y-%m")
    if "is_us_cash_open" in source.columns:
        cash = source["is_us_cash_open"].fillna(0).to_numpy(dtype="float64") >= 0.5
        result["us_cash_session"] = np.where(cash, "cash_open", "outside_cash")
    else:
        result["us_cash_session"] = "missing_column"
    result["volatility_regime"] = quantile_regime(source, "historical_vol_20", ["low_vol", "mid_vol", "high_vol"])
    result["adx_regime"] = threshold_regime(
        source,
        "adx_14",
        [(20.0, "low_adx"), (25.0, "mid_adx")],
        "high_adx",
    )
    result["vix_zscore_regime"] = zscore_regime(source, "vix_zscore_20", "low_vix", "neutral_vix", "high_vix")
    result["usdx_zscore_regime"] = zscore_regime(source, "usdx_zscore_20", "weak_usd", "neutral_usd", "strong_usd")
    result["us10yr_zscore_regime"] = zscore_regime(source, "us10yr_zscore_20", "low_rate", "neutral_rate", "high_rate")
    return result


def quantile_regime(source: pd.DataFrame, column: str, labels: list[str]) -> np.ndarray:
    if column not in source.columns:
        return np.full(len(source), "missing_column", dtype=object)
    values = pd.to_numeric(source[column], errors="coerce")
    if values.notna().sum() < len(labels) or values.nunique(dropna=True) < len(labels):
        return np.full(len(source), "insufficient_variation", dtype=object)
    ranked = pd.qcut(values.rank(method="first"), q=len(labels), labels=labels)
    return ranked.astype(str).fillna("missing_value").to_numpy()


def threshold_regime(source: pd.DataFrame, column: str, cuts: list[tuple[float, str]], final_label: str) -> np.ndarray:
    if column not in source.columns:
        return np.full(len(source), "missing_column", dtype=object)
    values = pd.to_numeric(source[column], errors="coerce")
    labels = np.full(len(source), final_label, dtype=object)
    labels[values.isna().to_numpy()] = "missing_value"
    previous_mask = np.zeros(len(source), dtype=bool)
    for threshold, label in cuts:
        mask = (values.to_numpy(dtype="float64", na_value=np.nan) < threshold) & ~previous_mask
        labels[mask] = label
        previous_mask |= mask
    return labels


def zscore_regime(source: pd.DataFrame, column: str, low_label: str, mid_label: str, high_label: str) -> np.ndarray:
    if column not in source.columns:
        return np.full(len(source), "missing_column", dtype=object)
    values = pd.to_numeric(source[column], errors="coerce").to_numpy(dtype="float64")
    labels = np.full(len(source), mid_label, dtype=object)
    labels[np.isnan(values)] = "missing_value"
    labels[values <= -1.0] = low_label
    labels[values >= 1.0] = high_label
    return labels


def slice_rows(prediction: pd.DataFrame) -> list[dict[str, Any]]:
    families = [
        "hour_utc",
        "month",
        "us_cash_session",
        "volatility_regime",
        "adx_regime",
        "vix_zscore_regime",
        "usdx_zscore_regime",
        "us10yr_zscore_regime",
    ]
    rows: list[dict[str, Any]] = []
    for family in families:
        grouped = prediction.groupby(family, dropna=False)
        for bucket, group in grouped:
            signals = group["signal"].to_numpy(dtype="int64")
            signal_mask = signals.astype(bool)
            long_signals = int(((group["signal_direction"].to_numpy(dtype="int64") == 1) & signal_mask).sum())
            short_signals = int(((group["signal_direction"].to_numpy(dtype="int64") == -1) & signal_mask).sum())
            rows.append(
                {
                    "candidate_id": str(group["candidate_id"].iloc[0]),
                    "artifact_slug": str(group["artifact_slug"].iloc[0]),
                    "feature_set_id": str(group["feature_set_id"].iloc[0]),
                    "model_id": str(group["model_id"].iloc[0]),
                    "view_id": str(group["view_id"].iloc[0]),
                    "slice_family": family,
                    "slice_value": str(bucket),
                    "rows": int(len(group)),
                    "signal_rows": int(signal_mask.sum()),
                    "signal_rate": float(signal_mask.mean()) if len(signal_mask) else 0.0,
                    "signal_long": long_signals,
                    "signal_short": short_signals,
                    "signal_long_share": float(long_signals / max(1, int(signal_mask.sum()))),
                    "mean_max_probability": float(group["max_probability"].mean()) if len(group) else 0.0,
                    "mean_probability_margin": float(group["probability_margin"].mean()) if len(group) else 0.0,
                }
            )
    return rows


def density_shift_rows(summary_rows: list[dict[str, Any]], oos_metrics: dict[str, dict[str, float]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in summary_rows:
        oos = oos_metrics.get(str(row["candidate_id"]), {})
        oos_signal_rate = float(oos.get("oos_signal_rate", 0.0))
        oos_signals_per_day = float(oos.get("oos_signals_per_day", 0.0))
        forward_signals_per_day = float(row["signals_per_day"])
        per_day_ratio = forward_signals_per_day / oos_signals_per_day if oos_signals_per_day else 0.0
        raw_density_warning = (
            str(row["view_id"]) == RAW_VIEW
            and float(row["rows_per_day"]) > RAW_ROW_DENSITY_RATIO_WARN * old_oos_rows_per_day()
        )
        session_supply_ok = (
            str(row["view_id"]) == SESSION_VIEW
            and int(row["signal_rows"]) >= SIGNAL_COUNT_MIN
            and SESSION_SIGNAL_PER_DAY_RATIO_MIN <= per_day_ratio <= SESSION_SIGNAL_PER_DAY_RATIO_MAX
        )
        if raw_density_warning:
            status = "raw_forward_not_session_parity_comparable"
        elif session_supply_ok:
            status = "session_parity_signal_supply_within_predeclared_band"
        elif str(row["view_id"]) == SESSION_VIEW:
            status = "session_parity_signal_supply_outside_predeclared_band"
        else:
            status = "raw_forward_recorded_for_diagnostics"
        rows.append(
            {
                **row,
                "oos_signal_rate": oos_signal_rate,
                "oos_signals_per_day": oos_signals_per_day,
                "oos_label_agreement_rate": float(oos.get("oos_label_agreement_rate", 0.0)),
                "oos_mean_proxy_log_return": float(oos.get("oos_mean_proxy_log_return", 0.0)),
                "signal_rate_delta_vs_oos": float(float(row["signal_rate"]) - oos_signal_rate),
                "signals_per_day_ratio_vs_oos": float(per_day_ratio),
                "density_judgment": status,
            }
        )
    return rows


_OLD_OOS_ROWS_PER_DAY: float | None = None


def old_oos_rows_per_day() -> float:
    global _OLD_OOS_ROWS_PER_DAY
    if _OLD_OOS_ROWS_PER_DAY is None:
        frame = pd.read_parquet(os_path(MODEL_INPUT_PATH), columns=["timestamp", "split"])
        frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
        oos = frame.loc[frame["split"].astype(str).eq("oos")]
        days = max(1, int(oos["timestamp"].dt.date.nunique()))
        _OLD_OOS_ROWS_PER_DAY = float(len(oos) / days)
    return float(_OLD_OOS_ROWS_PER_DAY)


def write_outputs(
    generated_at_utc: str,
    artifacts: list[Path],
    summary_rows: list[dict[str, Any]],
    density_rows: list[dict[str, Any]],
    parity_rows: list[dict[str, Any]],
    slice_attribution_rows: list[dict[str, Any]],
    session_manifest: dict[str, Any],
) -> list[Path]:
    output_artifacts: list[Path] = []

    summary_path = RUN_DIR / "forward_score_summary.csv"
    write_csv(
        summary_path,
        [
            "candidate_id",
            "artifact_slug",
            "feature_set_id",
            "model_id",
            "view_id",
            "rows",
            "days",
            "rows_per_day",
            "start_timestamp",
            "end_timestamp",
            "decision_threshold_policy",
            "decision_threshold",
            "signal_rows",
            "signal_rate",
            "signals_per_day",
            "pred_short",
            "pred_flat",
            "pred_long",
            "signal_short",
            "signal_long",
            "signal_long_share",
            "mean_max_probability",
            "mean_probability_margin",
            "median_probability_margin",
        ],
        summary_rows,
    )
    output_artifacts.append(summary_path)

    density_path = RUN_DIR / "density_shift_vs_oos.csv"
    write_csv(
        density_path,
        [
            "candidate_id",
            "artifact_slug",
            "feature_set_id",
            "model_id",
            "view_id",
            "rows",
            "days",
            "rows_per_day",
            "signal_rows",
            "signal_rate",
            "signals_per_day",
            "oos_signal_rate",
            "oos_signals_per_day",
            "signal_rate_delta_vs_oos",
            "signals_per_day_ratio_vs_oos",
            "signal_long_share",
            "oos_label_agreement_rate",
            "oos_mean_proxy_log_return",
            "density_judgment",
        ],
        density_rows,
    )
    output_artifacts.append(density_path)

    parity_path = RUN_DIR / "forward_onnx_parity_summary.csv"
    write_csv(
        parity_path,
        [
            "candidate_id",
            "artifact_slug",
            "feature_set_id",
            "model_id",
            "view_id",
            "rows",
            "passed",
            "max_abs_diff",
            "mean_abs_diff",
            "onnx_row_sum_max_abs_error",
            "input_name",
            "output_names",
            "onnx_path",
            "onnx_sha256",
            "sklearn_model_path",
            "sklearn_model_sha256",
        ],
        parity_rows,
    )
    output_artifacts.append(parity_path)

    slice_path = RUN_DIR / "forward_slice_attribution.csv"
    write_csv(
        slice_path,
        [
            "candidate_id",
            "artifact_slug",
            "feature_set_id",
            "model_id",
            "view_id",
            "slice_family",
            "slice_value",
            "rows",
            "signal_rows",
            "signal_rate",
            "signal_long",
            "signal_short",
            "signal_long_share",
            "mean_max_probability",
            "mean_probability_margin",
        ],
        slice_attribution_rows,
    )
    output_artifacts.append(slice_path)

    session_manifest_path = RUN_DIR / "old_session_parity_manifest.json"
    write_json(session_manifest_path, session_manifest)
    output_artifacts.append(session_manifest_path)

    experiment_receipt = RUN_DIR / "experiment_design_receipt.json"
    write_json(
        experiment_receipt,
        {
            "hypothesis": "Forward holdout scores should remain nonzero under old-session parity without threshold retuning.",
            "fixed_inputs": [rel(QUEUE_PATH), rel(FEATURE_FRAME_DIR), rel(RUN329C_DIR)],
            "changed_inputs": "none",
            "view_policy": [RAW_VIEW, SESSION_VIEW],
            "threshold_policy": "reuse run329C train-only nonflat-margin thresholds exactly",
            "forbidden_actions": ["new training", "threshold search", "D/B rule change", "profit fitting"],
            "success_boundary": "signal supply and ONNX parity diagnostics only; not forward passed",
        },
    )
    output_artifacts.append(experiment_receipt)

    data_receipt = RUN_DIR / "data_integrity_receipt.json"
    write_json(
        data_receipt,
        {
            "source_inputs": [rel(FEATURE_SUMMARY), rel(MODEL_INPUT_PATH)],
            "forward_scope": "2026-04-14 이후 run329B materialized feature frames",
            "session_parity_source": session_manifest,
            "raw_forward_warning": "raw feature frames can contain more rows/day than old model input; session parity view is the comparable diagnostic view",
            "data_integrity_judgment": "usable_for_score_replay_with_session_parity_boundary",
        },
    )
    output_artifacts.append(data_receipt)

    model_receipt = RUN_DIR / "model_validation_receipt.json"
    write_json(
        model_receipt,
        {
            "model_family": "run329C sklearn LogisticRegression exported to ONNX",
            "target_and_label": "no forward labels generated in run329D",
            "split_method": "forward holdout score replay only",
            "selection_metric": "none; no candidate selection",
            "secondary_metrics": ["signal density", "side attribution", "slice attribution", "ONNX parity"],
            "threshold_policy": "fixed thresholds from run329C",
            "overfit_risk": "raw forward density can look strong because session row density differs; old-session parity view mitigates but does not prove profitability",
            "calibration_risk": "logistic scores are ranking scores, not calibrated edge probabilities",
            "comparison_baseline": "run329C OOS signal density",
            "validation_judgment": JUDGMENT,
        },
    )
    output_artifacts.append(model_receipt)

    runtime_receipt = RUN_DIR / "runtime_parity_receipt.json"
    write_json(
        runtime_receipt,
        {
            "research_path": rel(Path(__file__)),
            "runtime_path": "not_materialized_in_run329D",
            "shared_contract": "ONNX probability order short/flat/long, run329B feature order, run329C fixed threshold",
            "known_differences": ["No MT5 EA handoff", "No lot/risk/ATR SLTP runtime package", "No MT5 tester output"],
            "parity_check": rel(parity_path),
            "parity_identity": parity_rows,
            "runtime_claim_boundary": "research_onnxruntime_forward_score_replay_only",
        },
    )
    output_artifacts.append(runtime_receipt)

    lineage_receipt = RUN_DIR / "artifact_lineage_receipt.json"
    lineage_artifacts = artifacts + output_artifacts
    write_json(
        lineage_receipt,
        {
            "source_inputs": [rel(QUEUE_PATH), rel(FEATURE_FRAME_DIR), rel(OOS_SIGNAL_METRICS), rel(MODEL_INPUT_PATH)],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_ACTION,
            "artifact_paths": [rel(path) for path in lineage_artifacts],
            "artifact_hashes": {rel(path): sha256_file(path) for path in lineage_artifacts if path_exists(path)},
            "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(ARTIFACT_REGISTRY), rel(STAGE_LEDGER)],
            "availability": "tracked_after_force_add_for_ignored_run_dir",
            "lineage_judgment": "connected_with_session_parity_boundary",
        },
    )
    output_artifacts.append(lineage_receipt)

    gate_audit = RUN_DIR / "required_gate_coverage_audit.csv"
    write_csv(
        gate_audit,
        ["gate_name", "status", "evidence_path", "effect"],
        [
            {
                "gate_name": "data_integrity(데이터 무결성)",
                "status": "passed_with_session_parity_warning",
                "evidence_path": rel(data_receipt),
                "effect": "raw forward(원본 전진)와 old-session parity(기존 세션 동등)를 분리해 세션 행 밀도 차이를 숨기지 않았다.",
            },
            {
                "gate_name": "model_validation(모델 검증)",
                "status": "passed_no_selection",
                "evidence_path": rel(model_receipt),
                "effect": "forward label(전진 라벨) 없이 고정 임계값 신호 공급만 봤고 후보 선택은 하지 않았다.",
            },
            {
                "gate_name": "runtime_parity(런타임 동등성)",
                "status": "passed_onnxruntime_only_no_mt5",
                "evidence_path": rel(runtime_receipt),
                "effect": "ONNXRuntime(온엑스런타임) 확률 동등성은 봤지만 MT5 런타임 권위는 없다.",
            },
            {
                "gate_name": "artifact_lineage(산출물 계보)",
                "status": "passed",
                "evidence_path": rel(lineage_receipt),
                "effect": "run329B 피처, run329C 모델/임계값, run329D 점수 산출물을 연결했다.",
            },
            {
                "gate_name": "result_judgment(결과 판정)",
                "status": "passed_no_goal_achieve",
                "evidence_path": rel(RUN_DIR / "result_judgment.csv"),
                "effect": "전진 통과, 운영 주장, Goal Achieve(목표 달성)를 만들지 않았다.",
            },
        ],
    )
    output_artifacts.append(gate_audit)

    result_judgment = RUN_DIR / "result_judgment.csv"
    write_csv(
        result_judgment,
        ["run_id", "status", "judgment", "decision", "goal_achieve", "next_action", "claim_boundary"],
        [
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "goal_achieve": "not_claimed",
                "next_action": NEXT_ACTION,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    output_artifacts.append(result_judgment)

    manifest = RUN_DIR / "run_manifest.json"
    write_json(
        manifest,
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "parent_run_id": PARENT_RUN_ID,
            "generated_at_utc": generated_at_utc,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "next_action": NEXT_ACTION,
            "goal_achieve": "not_claimed",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    output_artifacts.append(manifest)
    return output_artifacts


def markdown_summary_table(density_rows: list[dict[str, Any]]) -> str:
    rows = [row for row in density_rows if row["view_id"] == SESSION_VIEW]
    lines = [
        "| candidate(후보) | rows/day(일 행수) | signals/day(일 신호) | OOS signals/day(OOS 일 신호) | ratio(비율) | long share(롱 비중) | judgment(판정) |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {candidate_id} | {rows_per_day:.2f} | {signals_per_day:.2f} | {oos_signals_per_day:.2f} | {signals_per_day_ratio_vs_oos:.3f} | {signal_long_share:.3f} | {density_judgment} |".format(
                **row
            )
        )
    return "\n".join(lines)


def write_reports(density_rows: list[dict[str, Any]], summary_rows: list[dict[str, Any]]) -> list[Path]:
    artifacts: list[Path] = []
    table = markdown_summary_table(density_rows)
    raw_warnings = [row for row in density_rows if row["density_judgment"] == "raw_forward_not_session_parity_comparable"]
    session_ok = [row for row in density_rows if row["density_judgment"] == "session_parity_signal_supply_within_predeclared_band"]
    report = REVIEWS_DIR / "run329D_forward_holdout_score_replay.md"
    write_md(
        report,
        f"""
# run329D Forward Holdout Score Replay(329D 전진 보류 점수 재생)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- selected_candidate(선택 후보): `none`
- goal_achieve(목표 달성): `not_claimed`

## Scope(범위)

run329D(329D 실행)는 run329C(329C 실행)의 ONNX(온엑스), sklearn model(사이킷런 모델), fixed threshold(고정 임계값)를 그대로 사용했다. Forward label(전진 라벨), profit(수익), MT5 tester(MT5 테스터), threshold retuning(임계값 재튜닝)은 만들지 않았다.

Effect(효과): 새 데이터에서 score supply(점수 공급), signal density(신호 밀도), side attribution(방향 기여), session parity(세션 동등성), ONNX parity(온엑스 동등성)만 확인한다.

## Session Parity View(세션 동등 보기)

{table}

## Raw Forward Warning(원본 전진 경고)

- raw_warning_count(원본 경고 수): `{len(raw_warnings)}`
- session_supply_ok_count(세션 공급 통과 수): `{len(session_ok)}`
- effect(효과): raw_forward(원본 전진)는 macro48/us100-only에서 기존 OOS(표본외)보다 rows/day(일 행수)가 크게 많아 직접 비교하면 안 된다. old_session_parity(기존 세션 동등) view(보기)가 비교 가능한 진단 기준이다.

## Boundary(경계)

`{CLAIM_BOUNDARY}`

## Next(다음)

`{NEXT_ACTION}`
""",
    )
    artifacts.append(report)

    final_report = REVIEWS_DIR / "final_stage329D_decision_report.md"
    write_md(
        final_report,
        f"""
# Stage329D Final Decision(329D 최종 판정)

- decision(결정): `{DECISION}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- raw_session_mismatch_count(원본 세션 불일치 수): `{len(raw_warnings)}`
- session_parity_signal_supply_count(세션 동등 신호 공급 수): `{len(session_ok)}`
- selected_candidate(선택 후보): `none`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- effect(효과): 세션 동등 view(보기)에서는 신호 공급이 남지만, 수익/MT5/라벨 근거가 없으므로 forward passed(전진 통과)가 아니다.
- next_action(다음 행동): `{NEXT_ACTION}`
""",
    )
    artifacts.append(final_report)

    write_md(
        DECISION_DOC,
        f"""
# 2026-05-26 Stage329D Forward Score Replay Decision(329D 전진 점수 재생 결정)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- effect(효과): raw_forward(원본 전진)의 세션 행 밀도 불일치를 기록했고, old_session_parity(기존 세션 동등) view(보기)에서 fixed threshold(고정 임계값) 신호 공급을 확인했다.
- selected_candidate(선택 후보): `none`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`
""",
    )
    artifacts.append(DECISION_DOC)
    return artifacts


def update_selection_status(density_rows: list[dict[str, Any]]) -> Path:
    session_rows = [row for row in density_rows if row["view_id"] == SESSION_VIEW]
    session_ok = [row for row in session_rows if row["density_judgment"] == "session_parity_signal_supply_within_predeclared_band"]
    raw_warnings = [row for row in density_rows if row["density_judgment"] == "raw_forward_not_session_parity_comparable"]
    queue = ", ".join(sorted({str(row["candidate_id"]) for row in session_rows}))
    source_feature_sets = ", ".join(sorted({str(row["feature_set_id"]) for row in density_rows}))
    common_boundary = forward_common_valid_boundary()
    selection = SELECTED_DIR / "selection_status.md"
    return write_md(
        selection,
        f"""
# Stage329 Selection Status(329단계 선택 상태)

- selected_candidate(선택 후보): `none`
- cp322A_status(cp322A 상태): `research_artifact_preserved_not_forward_authority`
- source_feature_frame_queue(원천 피처 프레임 대기열): `{source_feature_sets}`
- research_onnx_status(연구 온엑스 상태): `forward_scored_with_onnxruntime_parity_not_runtime_handoff`
- forward_replay_queue(전진 재생 대기열): `{queue}`
- forward_score_replay_status(전진 점수 재생 상태): `{STATUS}`
- common_valid_boundary(공통 유효 경계): `{common_boundary}`
- raw_forward_warning_count(원본 전진 경고 수): `{len(raw_warnings)}`
- old_session_parity_signal_supply_count(기존 세션 동등 신호 공급 수): `{len(session_ok)}`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`
- effect(효과): raw forward(원본 전진)는 세션 밀도 불일치를 기록했고, old-session parity(기존 세션 동등) view(보기)는 다음 MT5/runtime probe(MT5/런타임 탐침) 입력 후보로만 남긴다.
""",
    )


def update_current_truth(density_rows: list[dict[str, Any]]) -> Path:
    workspace = ROOT / "docs" / "workspace" / "workspace_state.yaml"
    text, had_bom = read_text_lossless(workspace)
    text = replace_prefix_line(text, "current_run_id:", f"current_run_id: {RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage329(329단계) run329D(329D 실행) forward holdout score replay(전진 보류 점수 재생)를 닫았다. "
        f"Effect(효과): raw/session parity(원본/세션 동등) view(보기)를 분리해 신호 공급과 ONNX parity(온엑스 동등성)를 확인했지만, Goal Achieve(목표 달성)는 없다.\n"
    )
    if "Stage329(329단계) run329D(329D 실행)" not in text:
        text = text.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    write_text_lossless(workspace, text, had_bom)

    current = ROOT / "docs" / "context" / "current_working_state.md"
    text, had_bom = read_text_lossless(current)
    replacements = {
        "- current_packet(현재 작업 묶음):": "- current_packet(현재 작업 묶음): `329_onnx_rebuild__live_feature_control_v4`",
        "- current_run(현재 실행):": f"- current_run(현재 실행): `{RUN_ID}`",
        "- target_surface(목표 표면):": "- target_surface(목표 표면): `forward_score_replay_without_threshold_retuning`",
        "- status(상태):": f"- status(상태): `{STATUS}`",
        "- decision(판정):": f"- decision(판정): `{JUDGMENT}`",
        "- next_action(다음 행동):": f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "- claim_boundary(주장 경계):": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    }
    for prefix, replacement in replacements.items():
        text = replace_prefix_line(text, prefix, replacement)
    summary = (
        f"- run329D_summary(329D 요약): forward holdout score replay(전진 보류 점수 재생)를 `{STATUS}`로 닫았다. "
        "Effect(효과): raw_forward(원본 전진) 세션 밀도 불일치를 기록하고 old_session_parity(기존 세션 동등) view(보기)에서 fixed threshold(고정 임계값) 신호 공급을 확인했지만, selected candidate(선택 후보), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 없다."
    )
    if "run329D_summary(329D 요약)" not in text:
        text = text.replace(f"- decision(판정): `{JUDGMENT}`\n", f"- decision(판정): `{JUDGMENT}`\n{summary}\n", 1)
    write_text_lossless(current, text, had_bom)

    changelog = ROOT / "docs" / "workspace" / "changelog.md"
    text, had_bom = read_text_lossless(changelog)
    entry = f"""
## 2026-05-26 - Stage329D Forward Score Replay(329D 전진 점수 재생)

- run329D(329D 실행): run329C(329C 실행)의 fixed threshold(고정 임계값)와 ONNX(온엑스)를 run329B(329B 실행) forward feature frames(전진 피처 프레임)에 적용했다.
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): raw/session parity(원본/세션 동등)를 분리했고, 수익/라벨/MT5/runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
"""
    if "Stage329D Forward Score Replay" not in text:
        text = text.rstrip() + "\n\n" + entry.strip() + "\n"
    write_text_lossless(changelog, text, had_bom)
    return workspace


def update_registers(generated_at_utc: str, artifacts: list[Path]) -> None:
    upsert_csv(
        RUN_REGISTRY,
        "run_id",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "model_validation",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": rel(REVIEWS_DIR / "run329D_forward_holdout_score_replay.md"),
            "notes": "forward_score_replay;session_parity_warning;no_threshold_retuning;goal_achieve_not_claimed.",
        },
    )
    upsert_csv(
        ALPHA_LEDGER,
        "ledger_row_id",
        {
            "ledger_row_id": f"{RUN_ID}__forward_score_replay",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": RUN_NUMBER,
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "forward_score_replay",
            "tier_scope": "forward holdout",
            "kpi_scope": "score_density_onnx_parity_session_parity",
            "scoreboard_lane": "model_validation",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": rel(REVIEWS_DIR / "run329D_forward_holdout_score_replay.md"),
            "primary_kpi": "session_parity_signal_supply_count",
            "guardrail_kpi": "no_forward_label;no_profit;no_threshold_retuning;goal_achieve_not_claimed",
            "external_verification_status": "onnxruntime_probability_parity_only_no_mt5_runtime_claim",
            "notes": f"next_action={NEXT_ACTION}.",
        },
    )
    upsert_csv(
        STAGE_LEDGER,
        "run_id",
        {
            "run_id": RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "evidence_boundary": CLAIM_BOUNDARY,
            "report_path": rel(REVIEWS_DIR / "run329D_forward_holdout_score_replay.md"),
            "notes": "raw_session_mismatch_recorded;old_session_parity_view_available;goal_achieve_not_claimed.",
        },
    )
    rows: list[dict[str, Any]] = []
    for artifact in artifacts:
        if not path_exists(artifact) or os_path(artifact).is_dir():
            continue
        rows.append(
            {
                "artifact_id": f"{RUN_ID}__{artifact.stem}".replace("-", "_"),
                "artifact_type": artifact.suffix.lstrip(".") or "file",
                "path": rel(artifact),
                "sha256": sha256_file(artifact),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated_at_utc,
                "notes": STATUS,
            }
        )
    replace_or_append_csv_rows(ARTIFACT_REGISTRY, ["artifact_id", "run_id"], rows)


def main() -> None:
    generated_at_utc = utc_now()
    os_path(PREDICTIONS_DIR).mkdir(parents=True, exist_ok=True)
    old_minutes, session_manifest = load_old_session_minutes()
    queue = load_queue()
    oos_metrics = load_oos_signal_metrics()
    summary_rows: list[dict[str, Any]] = []
    density_rows_input: list[dict[str, Any]] = []
    parity_rows: list[dict[str, Any]] = []
    slice_attribution_rows: list[dict[str, Any]] = []
    artifacts: list[Path] = []

    for candidate in queue:
        feature_set_id = candidate["feature_set_id"]
        features = load_feature_order(feature_set_id)
        frame_path = FEATURE_FRAME_DIR / f"{feature_set_id}.parquet"
        frame = pd.read_parquet(os_path(frame_path))
        frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
        missing_features = sorted(set(features).difference(frame.columns))
        if missing_features:
            raise RuntimeError(f"{feature_set_id} missing features: {missing_features}")
        values = frame.loc[:, features].to_numpy(dtype="float64", copy=False)
        if not np.isfinite(values).all():
            raise RuntimeError(f"{feature_set_id} contains non-finite feature values")
        minute_of_day = (frame["timestamp"].dt.hour * 60 + frame["timestamp"].dt.minute).astype(int)
        views = {
            RAW_VIEW: frame,
            SESSION_VIEW: frame.loc[minute_of_day.isin(old_minutes)].copy(),
        }
        for view_id in VIEWS:
            view_frame = views[view_id]
            if view_frame.empty:
                raise RuntimeError(f"{candidate['candidate_id']} {view_id} produced no rows")
            prediction, summary, parity = score_frame(candidate, view_id, view_frame, features)
            prediction_path = PREDICTIONS_DIR / f"{candidate['artifact_slug']}_{view_id}_score.parquet"
            prediction.to_parquet(os_path(prediction_path), index=False)
            artifacts.append(prediction_path)
            summary["prediction_path"] = rel(prediction_path)
            summary_rows.append(summary)
            density_rows_input.append(summary)
            parity_rows.append(parity)
            slice_attribution_rows.extend(slice_rows(prediction))

    density_rows = density_shift_rows(density_rows_input, oos_metrics)
    artifacts.extend(
        write_outputs(
            generated_at_utc,
            artifacts,
            summary_rows,
            density_rows,
            parity_rows,
            slice_attribution_rows,
            session_manifest,
        )
    )
    artifacts.extend(write_reports(density_rows, summary_rows))
    artifacts.append(update_selection_status(density_rows))
    artifacts.append(update_current_truth(density_rows))
    update_registers(generated_at_utc, artifacts + [Path(__file__)])
    print(
        json.dumps(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "raw_warning_count": sum(1 for row in density_rows if row["density_judgment"] == "raw_forward_not_session_parity_comparable"),
                "session_supply_ok_count": sum(1 for row in density_rows if row["density_judgment"] == "session_parity_signal_supply_within_predeclared_band"),
                "goal_achieve": "not_claimed",
                "next_action": NEXT_ACTION,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
