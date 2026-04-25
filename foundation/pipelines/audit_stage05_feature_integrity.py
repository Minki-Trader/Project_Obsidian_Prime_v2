from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.features.session_calendar import broker_clock_key_to_event_utc  # noqa: E402
from foundation.features.top3_price_proxy_weights import (  # noqa: E402
    PriceProxyWeightSpec,
    validate_price_proxy_weights,
)
from foundation.pipelines.materialize_feature_frame_freeze import (  # noqa: E402
    FreezeSelectionSpec,
    select_freeze_rows,
)
from foundation.pipelines.materialize_fpmarkets_v2_dataset import (  # noqa: E402
    EXPECTED_FEATURE_ORDER_HASH,
    FEATURE_ORDER,
    SYMBOL_BINDINGS,
    build_feature_frame,
    feature_order_hash,
)


RUN_ID = "20260425_stage05_feature_integrity_audit_v1"
STAGE_ID = "05_feature_integrity__formula_time_alignment_leakage_audit"
MATERIALIZER_VERSION = "fpmarkets_v2_stage05_feature_integrity_audit_v1"

SOURCE_DATASET_ID = "dataset_fpmarkets_v2_us100_m5_20220901_20260413_cashopen_fullcash_proxyw58"
SOURCE_TRAINING_DATASET_ID = "training_fpmarkets_v2_us100_m5_label_v1_fwd12_split_v1_proxyw58"
MODEL_INPUT_DATASET_ID = "model_input_fpmarkets_v2_us100_m5_label_v1_fwd12_split_v1_proxyw58_feature_set_v2"
FEATURE_SET_ID = "feature_set_v2_mt5_price_proxy_top3_weights_58_features"

DEFAULT_RAW_ROOT = Path("data/raw/mt5_bars/m5")
DEFAULT_FEATURE_FRAME_PATH = Path("data/processed/datasets") / SOURCE_DATASET_ID / "features.parquet"
DEFAULT_DATASET_SUMMARY_PATH = DEFAULT_FEATURE_FRAME_PATH.with_name("dataset_summary.json")
DEFAULT_TRAINING_DATASET_PATH = (
    Path("data/processed/training_datasets/label_v1_fwd12_split_v1_proxyw58") / "training_dataset.parquet"
)
DEFAULT_TRAINING_SUMMARY_PATH = DEFAULT_TRAINING_DATASET_PATH.with_name("training_dataset_summary.json")
DEFAULT_MODEL_INPUT_PATH = (
    Path("data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58")
    / "model_input_dataset.parquet"
)
DEFAULT_MODEL_INPUT_SUMMARY_PATH = DEFAULT_MODEL_INPUT_PATH.with_name("model_input_summary.json")
DEFAULT_MODEL_INPUT_FEATURE_ORDER_PATH = DEFAULT_MODEL_INPUT_PATH.with_name("model_input_feature_order.txt")
DEFAULT_WEIGHTS_PATH = Path("foundation/config/top3_monthly_price_proxy_weights_fpmarkets_v2.csv")
DEFAULT_RUN_OUTPUT_ROOT = Path("stages") / STAGE_ID / "02_runs" / RUN_ID

DEFAULT_FLOAT_TOLERANCE = 1e-5
LABEL_TOLERANCE = 1e-8
HORIZON_MINUTES = 60
TRAIN_VALIDATION_START = pd.Timestamp("2025-01-01T00:00:00Z")
VALIDATION_OOS_START = pd.Timestamp("2025-10-01T00:00:00Z")
WINDOW_END_INCLUSIVE = pd.Timestamp("2026-04-13T23:55:00Z")

IDENTITY_COLUMNS = ["timestamp", "symbol"]
LABEL_COLUMNS = [
    "future_timestamp",
    "future_log_return_12",
    "label",
    "label_class",
    "label_id",
    "split",
    "split_id",
    "horizon_bars",
    "horizon_minutes",
]
BINARY_FEATURES = [
    "is_us_cash_open",
    "is_first_30m_after_open",
    "is_last_30m_before_cash_close",
]
EXTERNAL_FEATURE_COLUMNS = [
    "vix_change_1",
    "vix_zscore_20",
    "us10yr_change_1",
    "us10yr_zscore_20",
    "usdx_change_1",
    "usdx_zscore_20",
    "nvda_xnas_log_return_1",
    "aapl_xnas_log_return_1",
    "msft_xnas_log_return_1",
    "amzn_xnas_log_return_1",
    "mega8_equal_return_1",
    "top3_weighted_return_1",
    "mega8_pos_breadth_1",
    "mega8_dispersion_5",
    "us100_minus_mega8_equal_return_1",
    "us100_minus_top3_weighted_return_1",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Stage 05 integrated feature integrity audit.")
    parser.add_argument("--raw-root", default=str(DEFAULT_RAW_ROOT))
    parser.add_argument("--feature-frame-path", default=str(DEFAULT_FEATURE_FRAME_PATH))
    parser.add_argument("--dataset-summary-path", default=str(DEFAULT_DATASET_SUMMARY_PATH))
    parser.add_argument("--training-dataset-path", default=str(DEFAULT_TRAINING_DATASET_PATH))
    parser.add_argument("--training-summary-path", default=str(DEFAULT_TRAINING_SUMMARY_PATH))
    parser.add_argument("--model-input-path", default=str(DEFAULT_MODEL_INPUT_PATH))
    parser.add_argument("--model-input-summary-path", default=str(DEFAULT_MODEL_INPUT_SUMMARY_PATH))
    parser.add_argument("--model-input-feature-order-path", default=str(DEFAULT_MODEL_INPUT_FEATURE_ORDER_PATH))
    parser.add_argument("--weights-path", default=str(DEFAULT_WEIGHTS_PATH))
    parser.add_argument("--run-output-root", default=str(DEFAULT_RUN_OUTPUT_ROOT))
    parser.add_argument("--float-tolerance", type=float, default=DEFAULT_FLOAT_TOLERANCE)
    return parser.parse_args()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _io_path(path: Path) -> Path:
    resolved = path.resolve()
    if sys.platform == "win32":
        text = str(resolved)
        if not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def write_text(path: Path, text: str, *, encoding: str) -> None:
    _io_path(path.parent).mkdir(parents=True, exist_ok=True)
    _io_path(path).write_text(text, encoding=encoding)


def _json_ready(value: Any) -> Any:
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, dict):
        return {key: _json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_ready(item) for item in value]
    if isinstance(value, tuple):
        return [_json_ready(item) for item in value]
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    if isinstance(value, np.bool_):
        return bool(value)
    return value


def _pass_fail(failures: list[str]) -> str:
    return "pass" if not failures else "fail"


def _required_columns_missing(frame: pd.DataFrame, columns: list[str]) -> list[str]:
    return sorted(set(columns).difference(frame.columns))


def _timestamp_series(frame: pd.DataFrame, column: str = "timestamp") -> pd.Series:
    return pd.to_datetime(frame[column], utc=True).reset_index(drop=True)


def _finite_feature_check(frame: pd.DataFrame, feature_columns: list[str]) -> dict[str, Any]:
    values = frame.loc[:, feature_columns].to_numpy(dtype="float64", copy=False)
    finite_mask = np.isfinite(values)
    return {
        "finite": bool(finite_mask.all()),
        "non_finite_count": int((~finite_mask).sum()),
    }


def compute_ordered_hash(names: list[str] | tuple[str, ...]) -> str:
    return hashlib.sha256("\n".join(names).encode("utf-8")).hexdigest()


def audit_identity_schema(
    feature_frame: pd.DataFrame,
    training_frame: pd.DataFrame,
    model_input_frame: pd.DataFrame,
    dataset_summary: dict[str, Any],
    training_summary: dict[str, Any],
    model_input_summary: dict[str, Any],
) -> dict[str, Any]:
    failures: list[str] = []
    expected_feature_columns = IDENTITY_COLUMNS + FEATURE_ORDER
    expected_training_columns = IDENTITY_COLUMNS + FEATURE_ORDER + LABEL_COLUMNS

    current_feature_hash = feature_order_hash()
    if current_feature_hash != EXPECTED_FEATURE_ORDER_HASH:
        failures.append("feature_order_hash_mismatch")
    if compute_ordered_hash(FEATURE_ORDER) != EXPECTED_FEATURE_ORDER_HASH:
        failures.append("ordered_hash_mismatch")

    missing_feature = _required_columns_missing(feature_frame, expected_feature_columns)
    missing_training = _required_columns_missing(training_frame, expected_training_columns)
    missing_model_input = _required_columns_missing(model_input_frame, expected_training_columns)
    if missing_feature:
        failures.append("feature_frame_missing_columns")
    if missing_training:
        failures.append("training_dataset_missing_columns")
    if missing_model_input:
        failures.append("model_input_missing_columns")

    frame_checks: dict[str, dict[str, Any]] = {}
    for name, frame, expected_rows in (
        ("feature_frame", feature_frame, dataset_summary.get("selected_rows")),
        ("training_dataset", training_frame, training_summary.get("rows")),
        ("model_input", model_input_frame, model_input_summary.get("rows")),
    ):
        timestamp = _timestamp_series(frame)
        feature_check = _finite_feature_check(frame, FEATURE_ORDER) if not _required_columns_missing(frame, FEATURE_ORDER) else {
            "finite": False,
            "non_finite_count": None,
        }
        frame_checks[name] = {
            "rows": int(len(frame)),
            "expected_rows": int(expected_rows) if expected_rows is not None else None,
            "columns": int(len(frame.columns)),
            "duplicate_timestamps": int(timestamp.duplicated().sum()),
            "timestamp_monotonic_increasing": bool(timestamp.is_monotonic_increasing),
            "features_finite": feature_check["finite"],
            "feature_non_finite_count": feature_check["non_finite_count"],
        }
        if expected_rows is not None and len(frame) != int(expected_rows):
            failures.append(f"{name}_row_count_mismatch")
        if timestamp.duplicated().any():
            failures.append(f"{name}_duplicate_timestamps")
        if not timestamp.is_monotonic_increasing:
            failures.append(f"{name}_timestamps_not_monotonic")
        if not feature_check["finite"]:
            failures.append(f"{name}_non_finite_feature_values")

    if int(dataset_summary.get("feature_count", -1)) != len(FEATURE_ORDER):
        failures.append("dataset_summary_feature_count_mismatch")
    if dataset_summary.get("feature_order_hash") != EXPECTED_FEATURE_ORDER_HASH:
        failures.append("dataset_summary_feature_hash_mismatch")
    if training_summary.get("feature_order_hash") != EXPECTED_FEATURE_ORDER_HASH:
        failures.append("training_summary_feature_hash_mismatch")
    if model_input_summary.get("included_feature_order_hash") != EXPECTED_FEATURE_ORDER_HASH:
        failures.append("model_input_feature_hash_mismatch")
    if int(model_input_summary.get("included_feature_count", -1)) != len(FEATURE_ORDER):
        failures.append("model_input_feature_count_mismatch")

    return {
        "status": _pass_fail(failures),
        "feature_order_hash": current_feature_hash,
        "expected_feature_order_hash": EXPECTED_FEATURE_ORDER_HASH,
        "missing_columns": {
            "feature_frame": missing_feature,
            "training_dataset": missing_training,
            "model_input": missing_model_input,
        },
        "frame_checks": frame_checks,
        "failures": failures,
    }


def recompute_selected_feature_frame(raw_root: Path, weights_path: Path) -> tuple[pd.DataFrame, dict[str, Any]]:
    frame, counts = build_feature_frame(
        raw_root,
        weights_path=weights_path,
        weights_version_label=(
            "foundation/config/top3_monthly_price_proxy_weights_fpmarkets_v2.csv@2026-04-25 "
            "(mt5_price_proxy_close_share_v1)"
        ),
    )
    selection = FreezeSelectionSpec(
        target_id="practical_start_full_cash_day_valid_rows_only",
        start_utc=pd.Timestamp("2022-09-01T00:00:00Z"),
        row_scope="valid_row_only",
        session_scope="cash_open_rows_only",
        day_scope="full_cash_session_days_only",
    )
    selection_payload = select_freeze_rows(frame, counts, selection)
    return selection_payload["selected_frame"], selection_payload["selection_summary"]


def audit_feature_formula(
    stored_feature_frame: pd.DataFrame,
    recomputed_feature_frame: pd.DataFrame,
    selection_summary: dict[str, Any],
    *,
    float_tolerance: float,
) -> dict[str, Any]:
    failures: list[str] = []
    stored_timestamps = _timestamp_series(stored_feature_frame)
    recomputed_timestamps = _timestamp_series(recomputed_feature_frame)
    timestamps_match = bool(stored_timestamps.equals(recomputed_timestamps))
    if not timestamps_match:
        failures.append("selected_timestamps_mismatch")

    stored_values = stored_feature_frame.loc[:, FEATURE_ORDER].to_numpy(dtype="float64", copy=False)
    recomputed_values = (
        recomputed_feature_frame.loc[:, FEATURE_ORDER]
        .astype("float32")
        .to_numpy(dtype="float64", copy=False)
    )
    abs_diff = np.abs(stored_values - recomputed_values)
    max_abs_diff_by_feature = dict(zip(FEATURE_ORDER, abs_diff.max(axis=0), strict=True))
    max_feature = max(max_abs_diff_by_feature, key=max_abs_diff_by_feature.get)
    max_abs_diff = float(max_abs_diff_by_feature[max_feature])
    features_over_tolerance = [
        feature for feature, value in max_abs_diff_by_feature.items() if float(value) > float_tolerance
    ]
    if features_over_tolerance:
        failures.append("feature_values_over_tolerance")

    binary_feature_mismatches: dict[str, int] = {}
    for feature in BINARY_FEATURES:
        mismatch_count = int(
            (
                stored_feature_frame[feature].astype("float64").round(8)
                != recomputed_feature_frame[feature].astype("float64").round(8)
            ).sum()
        )
        binary_feature_mismatches[feature] = mismatch_count
        if mismatch_count:
            failures.append(f"{feature}_binary_mismatch")

    return {
        "status": _pass_fail(failures),
        "stored_rows": int(len(stored_feature_frame)),
        "recomputed_rows": int(len(recomputed_feature_frame)),
        "timestamps_match": timestamps_match,
        "float_tolerance": float_tolerance,
        "max_abs_diff": max_abs_diff,
        "max_abs_diff_feature": max_feature,
        "features_over_tolerance": features_over_tolerance,
        "binary_feature_mismatches": binary_feature_mismatches,
        "selection_summary": selection_summary,
        "failures": failures,
    }


def audit_dst_conversion_samples() -> dict[str, Any]:
    samples = pd.Series(
        pd.to_datetime(
            [
                "2022-08-01T16:35:00Z",
                "2023-01-03T16:35:00Z",
            ],
            utc=True,
        )
    )
    converted = broker_clock_key_to_event_utc(samples)
    expected = pd.Series(
        pd.to_datetime(
            [
                "2022-08-01T13:35:00Z",
                "2023-01-03T14:35:00Z",
            ],
            utc=True,
        )
    )
    rows = []
    failures: list[str] = []
    for raw_key, actual, expected_value in zip(samples, converted, expected, strict=True):
        passed = bool(actual == expected_value)
        if not passed:
            failures.append(f"dst_conversion_mismatch_{raw_key.isoformat()}")
        rows.append(
            {
                "raw_broker_clock_key": raw_key.isoformat(),
                "event_utc": actual.isoformat(),
                "expected_event_utc": expected_value.isoformat(),
                "status": "pass" if passed else "fail",
            }
        )
    return {"status": _pass_fail(failures), "samples": rows, "failures": failures}


def audit_session_time(recomputed_feature_frame: pd.DataFrame) -> dict[str, Any]:
    failures: list[str] = []
    required = [
        "timestamp_event_utc",
        "timestamp_ny",
        "date_ny",
        "is_us_cash_open",
        "minutes_from_cash_open",
        "is_first_30m_after_open",
        "is_last_30m_before_cash_close",
        "overnight_return",
        "cash_row_count",
        "is_full_cash_day",
    ]
    missing = _required_columns_missing(recomputed_feature_frame, required)
    if missing:
        return {
            "status": "fail",
            "missing_columns": missing,
            "failures": ["session_time_missing_columns"],
        }

    minutes = recomputed_feature_frame["minutes_from_cash_open"].astype("float64")
    is_cash_open_all = bool(recomputed_feature_frame["is_us_cash_open"].eq(1.0).all())
    full_cash_day_all = bool(recomputed_feature_frame["is_full_cash_day"].eq(True).all())
    cash_row_count_all_full = bool(recomputed_feature_frame["cash_row_count"].eq(78).all())
    minutes_in_cash_window = bool(minutes.ge(5).all() and minutes.le(390).all())
    if not is_cash_open_all:
        failures.append("selected_rows_not_all_cash_open")
    if not full_cash_day_all or not cash_row_count_all_full:
        failures.append("selected_rows_not_all_full_cash_days")
    if not minutes_in_cash_window:
        failures.append("minutes_from_cash_open_outside_cash_window")

    expected_first = ((minutes > 0) & (minutes <= 30)).astype("float64")
    first_mismatches = int((recomputed_feature_frame["is_first_30m_after_open"].astype("float64") != expected_first).sum())
    if first_mismatches:
        failures.append("first_30m_flag_mismatch")

    minutes_to_cash_close = 390.0 - minutes
    expected_last = ((minutes_to_cash_close >= 0) & (minutes_to_cash_close <= 25)).astype("float64")
    last_mismatches = int(
        (recomputed_feature_frame["is_last_30m_before_cash_close"].astype("float64") != expected_last).sum()
    )
    if last_mismatches:
        failures.append("last_30m_flag_mismatch")

    overnight_unique_counts = (
        recomputed_feature_frame.groupby("date_ny")["overnight_return"].nunique(dropna=False).astype(int)
    )
    max_overnight_values_per_day = int(overnight_unique_counts.max()) if len(overnight_unique_counts) else 0
    if max_overnight_values_per_day > 1:
        failures.append("overnight_return_changes_within_day")

    dst_samples = audit_dst_conversion_samples()
    if dst_samples["status"] != "pass":
        failures.append("dst_conversion_samples_failed")

    return {
        "status": _pass_fail(failures),
        "selected_rows": int(len(recomputed_feature_frame)),
        "selected_ny_days": int(recomputed_feature_frame["date_ny"].nunique()),
        "cash_row_count_min": int(recomputed_feature_frame["cash_row_count"].min()),
        "cash_row_count_max": int(recomputed_feature_frame["cash_row_count"].max()),
        "minutes_from_cash_open_min": float(minutes.min()),
        "minutes_from_cash_open_max": float(minutes.max()),
        "first_30m_flag_mismatches": first_mismatches,
        "last_30m_flag_mismatches": last_mismatches,
        "max_overnight_values_per_day": max_overnight_values_per_day,
        "dst_conversion_samples": dst_samples,
        "failures": failures,
    }


def read_raw_timestamps(raw_root: Path, contract_symbol: str) -> pd.Series:
    symbol_dir = raw_root / contract_symbol
    csv_candidates = sorted(symbol_dir.glob("*.csv"))
    if len(csv_candidates) != 1:
        raise RuntimeError(f"Expected one raw CSV under {symbol_dir}, found {len(csv_candidates)}")
    raw = pd.read_csv(csv_candidates[0], usecols=["time_close_unix"])
    return pd.to_datetime(raw["time_close_unix"], unit="s", utc=True)


def audit_external_timestamp_alignment(
    selected_timestamps: pd.Series,
    source_timestamps_by_symbol: dict[str, pd.Series],
) -> dict[str, Any]:
    selected_index = pd.Index(pd.to_datetime(selected_timestamps, utc=True))
    missing_counts = {}
    duplicate_counts = {}
    failures: list[str] = []
    for symbol, timestamps in source_timestamps_by_symbol.items():
        source_index = pd.Index(pd.to_datetime(timestamps, utc=True))
        missing = selected_index.difference(source_index)
        duplicate_count = int(pd.Series(source_index).duplicated().sum())
        missing_counts[symbol] = int(len(missing))
        duplicate_counts[symbol] = duplicate_count
        if len(missing):
            failures.append(f"{symbol}_missing_exact_timestamps")
        if duplicate_count:
            failures.append(f"{symbol}_duplicate_raw_timestamps")
    return {
        "status": _pass_fail(failures),
        "selected_rows": int(len(selected_index)),
        "missing_counts": missing_counts,
        "duplicate_counts": duplicate_counts,
        "failures": failures,
    }


def audit_external_alignment(
    recomputed_feature_frame: pd.DataFrame,
    raw_root: Path,
    weights_path: Path,
) -> dict[str, Any]:
    failures: list[str] = []
    external_symbols = [binding.contract_symbol for binding in SYMBOL_BINDINGS if binding.contract_symbol != "US100"]
    timestamp_sources = {
        symbol: read_raw_timestamps(raw_root, symbol)
        for symbol in external_symbols
    }
    timestamp_alignment = audit_external_timestamp_alignment(
        recomputed_feature_frame["timestamp"],
        timestamp_sources,
    )
    if timestamp_alignment["status"] != "pass":
        failures.append("external_timestamp_alignment_failed")

    external_finite = _finite_feature_check(recomputed_feature_frame, EXTERNAL_FEATURE_COLUMNS)
    if not external_finite["finite"]:
        failures.append("external_feature_non_finite_values")

    weights = pd.read_csv(weights_path)
    weights_validation_status = "pass"
    weights_failure = None
    try:
        validate_price_proxy_weights(weights, PriceProxyWeightSpec(start_month="2022-08", end_month="2026-04"))
    except Exception as exc:  # pragma: no cover - surfaced in audit output.
        weights_validation_status = "fail"
        weights_failure = str(exc)
        failures.append("price_proxy_weight_validation_failed")

    return {
        "status": _pass_fail(failures),
        "timestamp_alignment": timestamp_alignment,
        "external_feature_columns": EXTERNAL_FEATURE_COLUMNS,
        "external_feature_non_finite_count": external_finite["non_finite_count"],
        "weight_table": {
            "path": weights_path.as_posix(),
            "rows": int(len(weights)),
            "first_month": str(weights["month"].iloc[0]) if len(weights) else None,
            "last_month": str(weights["month"].iloc[-1]) if len(weights) else None,
            "weight_sum_max_abs_error": float(
                (weights[["msft_xnas_weight", "nvda_xnas_weight", "aapl_xnas_weight"]].sum(axis=1) - 1.0)
                .abs()
                .max()
            )
            if len(weights)
            else None,
            "validation_status": weights_validation_status,
            "validation_failure": weights_failure,
            "boundary": "MT5 price-proxy weights only; not actual NDX/QQQ weights.",
        },
        "forward_fill_rule_used": False,
        "future_fill_rule_used": False,
        "failures": failures,
    }


def compute_train_threshold_from_frame(training_frame: pd.DataFrame, quantile: float = 0.33) -> float:
    train_returns = training_frame.loc[training_frame["split"].eq("train"), "future_log_return_12"].abs()
    if train_returns.empty:
        raise RuntimeError("Training split is empty; cannot compute label threshold.")
    return float(train_returns.quantile(quantile))


def expected_label_frame(training_frame: pd.DataFrame, threshold: float) -> pd.DataFrame:
    result = training_frame[["timestamp", "future_log_return_12"]].copy()
    returns = result["future_log_return_12"].astype("float64")
    result["expected_label"] = "flat"
    result.loc[returns > threshold, "expected_label"] = "long"
    result.loc[returns < -threshold, "expected_label"] = "short"
    result["expected_label_class"] = result["expected_label"].map({"short": 0, "flat": 1, "long": 2}).astype("int8")
    return result


def read_us100_close_frame(raw_root: Path) -> pd.DataFrame:
    symbol_dir = raw_root / "US100"
    csv_candidates = sorted(symbol_dir.glob("*.csv"))
    if len(csv_candidates) != 1:
        raise RuntimeError(f"Expected one US100 raw CSV under {symbol_dir}, found {len(csv_candidates)}")
    raw = pd.read_csv(csv_candidates[0], usecols=["time_close_unix", "close"])
    raw["timestamp"] = pd.to_datetime(raw["time_close_unix"], unit="s", utc=True)
    raw = raw[["timestamp", "close"]].drop_duplicates("timestamp").sort_values("timestamp")
    return raw


def audit_label_leakage(
    feature_frame: pd.DataFrame,
    training_frame: pd.DataFrame,
    model_input_frame: pd.DataFrame,
    training_summary: dict[str, Any],
    raw_root: Path,
    model_input_feature_order_path: Path,
) -> dict[str, Any]:
    failures: list[str] = []
    timestamp = _timestamp_series(training_frame)
    future_timestamp = _timestamp_series(training_frame, "future_timestamp")
    expected_future_timestamp = timestamp + pd.Timedelta(minutes=HORIZON_MINUTES)
    future_delta_ok = bool(future_timestamp.equals(expected_future_timestamp))
    if not future_delta_ok:
        failures.append("future_timestamp_not_horizon_60m")

    if "minutes_from_cash_open" in training_frame.columns:
        label_start_ok = bool(training_frame["minutes_from_cash_open"].astype("float64").le(330).all())
    else:
        label_start_ok = False
    if not label_start_ok:
        failures.append("label_start_minutes_violate_contract")

    recomputed_threshold = compute_train_threshold_from_frame(training_frame)
    summary_threshold = float(training_summary.get("threshold_log_return", np.nan))
    threshold_abs_diff = abs(recomputed_threshold - summary_threshold)
    if threshold_abs_diff > LABEL_TOLERANCE:
        failures.append("train_only_threshold_mismatch")

    expected_labels = expected_label_frame(training_frame, recomputed_threshold)
    label_mismatches = int((training_frame["label"].astype(str) != expected_labels["expected_label"].astype(str)).sum())
    label_class_mismatches = int(
        (training_frame["label_class"].astype("int64") != expected_labels["expected_label_class"].astype("int64")).sum()
    )
    if label_mismatches:
        failures.append("label_assignment_mismatch")
    if label_class_mismatches:
        failures.append("label_class_assignment_mismatch")

    split_failures = []
    split_series = training_frame["split"].astype(str)
    if not bool(split_series.loc[timestamp < TRAIN_VALIDATION_START].eq("train").all()):
        split_failures.append("train_boundary")
    validation_mask = (timestamp >= TRAIN_VALIDATION_START) & (timestamp < VALIDATION_OOS_START)
    if not bool(split_series.loc[validation_mask].eq("validation").all()):
        split_failures.append("validation_boundary")
    oos_mask = (timestamp >= VALIDATION_OOS_START) & (timestamp <= WINDOW_END_INCLUSIVE)
    if not bool(split_series.loc[oos_mask].eq("oos").all()):
        split_failures.append("oos_boundary")
    if split_failures:
        failures.append("split_boundary_mismatch")

    feature_timestamp_set = set(_timestamp_series(feature_frame))
    training_timestamps_in_feature_frame = bool(set(timestamp).issubset(feature_timestamp_set))
    if not training_timestamps_in_feature_frame:
        failures.append("training_timestamps_missing_from_feature_frame")

    raw_close = read_us100_close_frame(raw_root)
    current_close = raw_close.rename(columns={"close": "current_close"}).set_index("timestamp")
    future_close = raw_close.rename(columns={"close": "future_close"}).set_index("timestamp")
    close_work = training_frame[["timestamp", "future_timestamp", "future_log_return_12"]].copy()
    close_work = close_work.merge(current_close, left_on="timestamp", right_index=True, how="left")
    close_work = close_work.merge(future_close, left_on="future_timestamp", right_index=True, how="left")
    close_work["recomputed_future_log_return_12"] = np.log(
        close_work["future_close"].astype("float64") / close_work["current_close"].astype("float64")
    )
    label_return_abs_diff = (
        close_work["future_log_return_12"].astype("float64")
        - close_work["recomputed_future_log_return_12"].astype("float64")
    ).abs()
    max_label_return_abs_diff = float(label_return_abs_diff.max())
    if max_label_return_abs_diff > LABEL_TOLERANCE:
        failures.append("future_log_return_recalculation_mismatch")

    model_feature_order = (
        model_input_feature_order_path.read_text(encoding="utf-8").splitlines()
        if model_input_feature_order_path.exists()
        else []
    )
    label_columns_in_feature_order = sorted(set(LABEL_COLUMNS).intersection(FEATURE_ORDER))
    label_columns_in_model_feature_order = sorted(set(LABEL_COLUMNS).intersection(model_feature_order))
    if label_columns_in_feature_order or label_columns_in_model_feature_order:
        failures.append("label_columns_leaked_into_feature_order")

    common_columns = IDENTITY_COLUMNS + FEATURE_ORDER + LABEL_COLUMNS
    model_input_matches_training = True
    if _required_columns_missing(model_input_frame, common_columns):
        model_input_matches_training = False
    else:
        training_compare = training_frame.loc[:, common_columns].reset_index(drop=True)
        model_compare = model_input_frame.loc[:, common_columns].reset_index(drop=True)
        numeric_feature_match = np.allclose(
            training_compare.loc[:, FEATURE_ORDER].to_numpy(dtype="float64"),
            model_compare.loc[:, FEATURE_ORDER].to_numpy(dtype="float64"),
            atol=DEFAULT_FLOAT_TOLERANCE,
            rtol=0.0,
        )
        non_feature_match = bool(
            training_compare.loc[:, IDENTITY_COLUMNS + LABEL_COLUMNS].astype(str).equals(
                model_compare.loc[:, IDENTITY_COLUMNS + LABEL_COLUMNS].astype(str)
            )
        )
        model_input_matches_training = bool(numeric_feature_match and non_feature_match)
    if not model_input_matches_training:
        failures.append("model_input_not_equal_to_training_dataset_58_feature_surface")

    return {
        "status": _pass_fail(failures),
        "future_timestamp_horizon_minutes": HORIZON_MINUTES,
        "future_timestamp_delta_ok": future_delta_ok,
        "label_start_minutes_ok": label_start_ok,
        "recomputed_train_threshold": recomputed_threshold,
        "summary_threshold": summary_threshold,
        "threshold_abs_diff": threshold_abs_diff,
        "label_mismatches": label_mismatches,
        "label_class_mismatches": label_class_mismatches,
        "split_failures": split_failures,
        "training_timestamps_in_feature_frame": training_timestamps_in_feature_frame,
        "max_future_log_return_abs_diff": max_label_return_abs_diff,
        "label_columns_in_model_feature_order": label_columns_in_model_feature_order,
        "model_input_matches_training": model_input_matches_training,
        "failures": failures,
    }


def build_stage05_audit(
    *,
    raw_root: Path,
    feature_frame_path: Path,
    dataset_summary_path: Path,
    training_dataset_path: Path,
    training_summary_path: Path,
    model_input_path: Path,
    model_input_summary_path: Path,
    model_input_feature_order_path: Path,
    weights_path: Path,
    float_tolerance: float,
) -> dict[str, Any]:
    feature_frame = pd.read_parquet(feature_frame_path)
    training_frame = pd.read_parquet(training_dataset_path)
    model_input_frame = pd.read_parquet(model_input_path)
    dataset_summary = read_json(dataset_summary_path)
    training_summary = read_json(training_summary_path)
    model_input_summary = read_json(model_input_summary_path)

    for frame in (feature_frame, training_frame, model_input_frame):
        frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    for frame in (training_frame, model_input_frame):
        frame["future_timestamp"] = pd.to_datetime(frame["future_timestamp"], utc=True)

    recomputed_feature_frame, selection_summary = recompute_selected_feature_frame(raw_root, weights_path)

    identity_schema = audit_identity_schema(
        feature_frame,
        training_frame,
        model_input_frame,
        dataset_summary,
        training_summary,
        model_input_summary,
    )
    feature_formula = audit_feature_formula(
        feature_frame,
        recomputed_feature_frame,
        selection_summary,
        float_tolerance=float_tolerance,
    )
    session_time = audit_session_time(recomputed_feature_frame)
    external_alignment = audit_external_alignment(recomputed_feature_frame, raw_root, weights_path)
    label_leakage = audit_label_leakage(
        feature_frame,
        training_frame,
        model_input_frame,
        training_summary,
        raw_root,
        model_input_feature_order_path,
    )

    sections = {
        "identity_schema": identity_schema,
        "feature_formula": feature_formula,
        "session_time": session_time,
        "external_alignment": external_alignment,
        "label_leakage": label_leakage,
    }
    failures = {
        name: section["failures"]
        for name, section in sections.items()
        if section.get("status") != "pass"
    }
    passed = not failures
    judgment = "positive_feature_integrity_audit_passed" if passed else "invalid_feature_integrity_audit_failed"

    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "evidence",
        "materializer_version": MATERIALIZER_VERSION,
        "status": "reviewed",
        "judgment": judgment,
        "passed": passed,
        "feature_set_id": FEATURE_SET_ID,
        "source_dataset_id": SOURCE_DATASET_ID,
        "source_training_dataset_id": SOURCE_TRAINING_DATASET_ID,
        "model_input_dataset_id": MODEL_INPUT_DATASET_ID,
        "feature_order_hash": feature_order_hash(),
        "float_tolerance": float_tolerance,
        "inputs": {
            "feature_frame_path": feature_frame_path.as_posix(),
            "dataset_summary_path": dataset_summary_path.as_posix(),
            "training_dataset_path": training_dataset_path.as_posix(),
            "training_summary_path": training_summary_path.as_posix(),
            "model_input_path": model_input_path.as_posix(),
            "model_input_summary_path": model_input_summary_path.as_posix(),
            "model_input_feature_order_path": model_input_feature_order_path.as_posix(),
            "weights_path": weights_path.as_posix(),
            "raw_root": raw_root.as_posix(),
        },
        "input_hashes": {
            "feature_frame_sha256": sha256_file(feature_frame_path),
            "training_dataset_sha256": sha256_file(training_dataset_path),
            "model_input_dataset_sha256": sha256_file(model_input_path),
            "weights_sha256": sha256_file(weights_path),
        },
        "sections": sections,
        "failures": failures,
        "evidence_boundary": (
            "Evidence run only. This audits feature formula, time/session, external alignment, "
            "and label leakage for the Stage 04 MT5 price-proxy 58-feature input. It does not "
            "claim model quality, alpha quality, runtime authority, or operating promotion."
        ),
        "external_verification_status": "out_of_scope_by_claim",
    }


def render_result_summary(audit: dict[str, Any]) -> str:
    status_text = "통과(pass, 통과)" if audit["passed"] else "실패(fail, 실패)"
    lines = [
        "# Stage 05 Feature Integrity Audit v1",
        "",
        f"- run_id(실행 ID): `{audit['run_id']}`",
        f"- status(상태): `{status_text}`",
        f"- judgment(판정): `{audit['judgment']}`",
        f"- feature_order_hash(피처 순서 해시): `{audit['feature_order_hash']}`",
        f"- float_tolerance(부동소수 허용오차): `{audit['float_tolerance']}`",
        "",
        "## Audit Results(감사 결과)",
        "",
    ]
    for key, label in (
        ("identity_schema", "identity/schema(정체성/구조)"),
        ("feature_formula", "feature formula(피처 공식)"),
        ("session_time", "time/session(시간/세션)"),
        ("external_alignment", "external alignment(외부 정렬)"),
        ("label_leakage", "label leakage(라벨 누수)"),
    ):
        section = audit["sections"][key]
        lines.append(f"- {label}: `{section['status']}`")

    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            (
                "이 실행(run, 실행)은 Stage 04(4단계)의 MT5 price-proxy 58 feature model input"
                "(MT5 가격 대리 58개 피처 모델 입력)을 감사한다. model training(모델 학습), "
                "alpha quality(알파 품질), runtime authority(런타임 권위), operating promotion"
                "(운영 승격)은 주장하지 않는다."
            ),
        ]
    )
    if audit["failures"]:
        lines.extend(["", "## Failures(실패 항목)", ""])
        for section, failures in audit["failures"].items():
            lines.append(f"- {section}: `{', '.join(failures)}`")
    return "\n".join(lines) + "\n"


def write_stage05_outputs(audit: dict[str, Any], run_output_root: Path) -> dict[str, str]:
    run_output_root.mkdir(parents=True, exist_ok=True)

    paths = {
        "audit_summary": run_output_root / "audit_summary.json",
        "feature_formula_audit": run_output_root / "feature_formula_audit.json",
        "session_time_audit": run_output_root / "session_time_audit.json",
        "external_alignment_audit": run_output_root / "external_alignment_audit.json",
        "label_leakage_audit": run_output_root / "label_leakage_audit.json",
        "run_manifest": run_output_root / "run_manifest.json",
        "kpi_record": run_output_root / "kpi_record.json",
        "result_summary": run_output_root / "result_summary.md",
    }
    for path in paths.values():
        path.parent.mkdir(parents=True, exist_ok=True)

    summary_payload = {key: value for key, value in audit.items() if key != "sections"}
    summary_payload["section_status"] = {
        key: section["status"] for key, section in audit["sections"].items()
    }
    write_text(paths["audit_summary"], json.dumps(_json_ready(summary_payload), indent=2), encoding="utf-8")
    write_text(
        paths["feature_formula_audit"],
        json.dumps(_json_ready(audit["sections"]["feature_formula"]), indent=2),
        encoding="utf-8",
    )
    write_text(
        paths["session_time_audit"],
        json.dumps(_json_ready(audit["sections"]["session_time"]), indent=2),
        encoding="utf-8",
    )
    write_text(
        paths["external_alignment_audit"],
        json.dumps(_json_ready(audit["sections"]["external_alignment"]), indent=2),
        encoding="utf-8",
    )
    write_text(
        paths["label_leakage_audit"],
        json.dumps(_json_ready(audit["sections"]["label_leakage"]), indent=2),
        encoding="utf-8",
    )

    run_manifest = {
        "run_id": audit["run_id"],
        "stage_id": audit["stage_id"],
        "lane": audit["lane"],
        "status": audit["status"],
        "command": "python foundation/pipelines/audit_stage05_feature_integrity.py",
        "inputs": list(audit["inputs"].values()),
        "outputs": [path.as_posix() for path in paths.values()],
        "judgment": audit["judgment"],
        "judgment_boundary": audit["evidence_boundary"],
        "external_verification_status": audit["external_verification_status"],
    }
    write_text(paths["run_manifest"], json.dumps(_json_ready(run_manifest), indent=2), encoding="utf-8")

    kpi_record = {
        "run_id": audit["run_id"],
        "scoreboard": "diagnostic_special",
        "measurement_scope": "feature_formula_time_external_label_integrity",
        "parity_level": "P1_dataset_feature_aligned",
        "wfo_status": "not_applicable",
        "judgment": audit["judgment"],
        "evidence_boundary": "reviewed",
        "hard_gate_applicable": "no",
        "negative_memory_required": "no",
        "registry_update_required": "yes",
        "external_verification_status": audit["external_verification_status"],
        "measurement": {
            "passed": audit["passed"],
            "feature_order_hash": audit["feature_order_hash"],
            "float_tolerance": audit["float_tolerance"],
            "section_status": {
                key: section["status"] for key, section in audit["sections"].items()
            },
            "max_feature_formula_abs_diff": audit["sections"]["feature_formula"]["max_abs_diff"],
            "label_threshold_abs_diff": audit["sections"]["label_leakage"]["threshold_abs_diff"],
            "external_alignment_missing_counts": audit["sections"]["external_alignment"]["timestamp_alignment"][
                "missing_counts"
            ],
        },
    }
    write_text(paths["kpi_record"], json.dumps(_json_ready(kpi_record), indent=2), encoding="utf-8")
    write_text(paths["result_summary"], render_result_summary(audit), encoding="utf-8-sig")

    return {key: path.as_posix() for key, path in paths.items()}


def main() -> int:
    args = parse_args()
    audit = build_stage05_audit(
        raw_root=Path(args.raw_root),
        feature_frame_path=Path(args.feature_frame_path),
        dataset_summary_path=Path(args.dataset_summary_path),
        training_dataset_path=Path(args.training_dataset_path),
        training_summary_path=Path(args.training_summary_path),
        model_input_path=Path(args.model_input_path),
        model_input_summary_path=Path(args.model_input_summary_path),
        model_input_feature_order_path=Path(args.model_input_feature_order_path),
        weights_path=Path(args.weights_path),
        float_tolerance=args.float_tolerance,
    )
    output_paths = write_stage05_outputs(audit, Path(args.run_output_root))
    payload = {
        "status": "ok" if audit["passed"] else "failed",
        "run_id": audit["run_id"],
        "judgment": audit["judgment"],
        "run_output_root": Path(args.run_output_root).as_posix(),
        "outputs": output_paths,
        "failures": audit["failures"],
    }
    print(json.dumps(_json_ready(payload), indent=2))
    return 0 if audit["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
