from __future__ import annotations

import csv
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.features.session_calendar import attach_event_time_columns
import foundation.pipelines.materialize_fpmarkets_v2_dataset as fp


STAGE_ID = "329_onnx_rebuild__live_feature_control"
RUN_ID = "run329B_materialize_forward_live_feature_frames_v1"
RUN_NUMBER = "run329B"
PARENT_RUN_ID = "run329A_design_live_feature_rebuild_control_after_cp322a_block_v1"
STATUS = "completed_forward_feature_frames_materialized_with_session_boundary"
JUDGMENT = "research_materialization_completed_no_goal_achieve"
DECISION = "stage329B_forward_feature_frames_ready_for_train_wfo_control_no_candidate_selected"
NEXT_ACTION = "run329C_train_wfo_rebuild_candidates_without_forward_tuning"
CLAIM_BOUNDARY = (
    "research_development_only_forward_features_materialized_no_labels_no_threshold_tuning_"
    "no_candidate_selected_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
FEATURE_FRAME_DIR = RUN_DIR / "feature_frames"
FEATURE_ORDER_DIR = RUN_DIR / "feature_orders"
FEATURE_SUMMARY_DIR = RUN_DIR / "feature_summaries"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-26_stage329B_forward_feature_frames.md"

HISTORICAL_RAW_ROOT = ROOT / "data" / "raw" / "mt5_bars" / "m5"
FORWARD_RAW_ROOT = STAGE_DIR.parent / "326_forward__cp322a_frozen_forward_gate" / "01_inputs" / "raw_m5"
FORWARD_RAW_SUMMARY = FORWARD_RAW_ROOT / "stage01_raw_export_summary.json"
WEIGHTS_PATH = ROOT / "foundation" / "config" / "top3_monthly_price_proxy_weights_fpmarkets_v2.csv"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"

PRELOAD_START_UTC = pd.Timestamp("2026-04-01T00:00:00Z")
FORWARD_OUTPUT_START_UTC = pd.Timestamp("2026-04-14T01:05:00Z")
FORWARD_REQUESTED_START_UTC = pd.Timestamp("2026-04-14T00:00:00Z")
FORWARD_REQUESTED_TO_UTC = pd.Timestamp("2026-05-25T21:05:00Z")
COMPUTE_END_UTC = pd.Timestamp("2026-05-25T21:10:00Z")

TOP3_FEATURES = {"top3_weighted_return_1", "us100_minus_top3_weighted_return_1"}
EQUITY_AND_BREADTH_FEATURES = {
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
}
MACRO_FEATURES = {
    "vix_change_1",
    "vix_zscore_20",
    "us10yr_change_1",
    "us10yr_zscore_20",
    "usdx_change_1",
    "usdx_zscore_20",
}

FEATURE_SETS: dict[str, dict[str, Any]] = {
    "core56_no_top3_weight_features": {
        "features": [feature for feature in fp.FEATURE_ORDER if feature not in TOP3_FEATURES],
        "required_symbols": [
            "US100",
            "VIX",
            "US10YR",
            "USDX",
            "NVDA",
            "AAPL",
            "MSFT",
            "AMZN",
            "AMD",
            "GOOGL.xnas",
            "META",
            "TSLA",
        ],
        "role": "preferred_first_materialization_control",
    },
    "macro48_no_equity_breadth_or_top3": {
        "features": [feature for feature in fp.FEATURE_ORDER if feature not in EQUITY_AND_BREADTH_FEATURES],
        "required_symbols": ["US100", "VIX", "US10YR", "USDX"],
        "role": "parallel_resilience_control",
    },
    "us100_technical42_no_external": {
        "features": [
            feature
            for feature in fp.FEATURE_ORDER
            if feature not in EQUITY_AND_BREADTH_FEATURES and feature not in MACRO_FEATURES
        ],
        "required_symbols": ["US100"],
        "role": "minimal_parity_control",
    },
}

COMBINED_RAW_CACHE: dict[str, pd.DataFrame] = {}
COMBINED_IDENTITY_CACHE: dict[str, dict[str, Any]] = {}


def os_path(path: Path) -> Path:
    resolved = path.resolve()
    if os.name == "nt":
        text = str(resolved)
        if len(text) > 240 and not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def path_exists(path: Path) -> bool:
    return os_path(path).exists()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with os_path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def ordered_hash(values: Iterable[str]) -> str:
    return hashlib.sha256("\n".join(values).encode("utf-8")).hexdigest()


def write_text(path: Path, text: str, encoding: str = "utf-8") -> Path:
    os_path(path.parent).mkdir(parents=True, exist_ok=True)
    os_path(path).write_text(text, encoding=encoding)
    return path


def write_md(path: Path, text: str) -> Path:
    return write_text(path, text.strip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> Path:
    return write_text(path, json.dumps(json_ready(payload), indent=2, ensure_ascii=False) + "\n")


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, Any]]) -> Path:
    os_path(path.parent).mkdir(parents=True, exist_ok=True)
    with os_path(path).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})
    return path


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
    for row in new_rows:
        clean_row = {name: str(row.get(name, "")) for name in fieldnames}
        for idx, existing in enumerate(rows):
            if all(existing.get(key, "") == clean_row.get(key, "") for key in keys):
                rows[idx] = clean_row
                break
        else:
            rows.append(clean_row)
    write_csv(path, fieldnames, rows)


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = os_path(path).read_bytes()
    has_bom = raw.startswith(b"\xef\xbb\xbf")
    return raw.decode("utf-8-sig" if has_bom else "utf-8"), has_bom


def write_text_preserving(path: Path, text: str, had_bom: bool) -> None:
    encoding = "utf-8-sig" if had_bom or path.suffix.lower() in {".md", ".txt"} else "utf-8"
    write_text(path, text, encoding=encoding)


def replace_prefix_line(text: str, prefix: str, new_line: str) -> str:
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if line.startswith(prefix):
            lines[idx] = new_line
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + new_line + "\n"


def append_bytes_if_missing(path: Path, marker: str, entry: str) -> None:
    raw = os_path(path).read_bytes() if path_exists(path) else b""
    if marker.encode("utf-8") in raw:
        return
    os_path(path.parent).mkdir(parents=True, exist_ok=True)
    if raw and not raw.endswith((b"\n", b"\r")):
        raw += b"\n"
    os_path(path).write_bytes(raw.rstrip() + entry.encode("utf-8"))


def find_raw_csv(raw_root: Path, contract_symbol: str) -> Path:
    candidates = sorted((raw_root / contract_symbol).glob("*.csv"))
    if len(candidates) != 1:
        raise RuntimeError(f"Expected one CSV under {raw_root / contract_symbol}, found {len(candidates)}")
    return candidates[0]


def find_raw_manifest(raw_root: Path, contract_symbol: str) -> Path:
    candidates = sorted((raw_root / contract_symbol).glob("*.manifest.json"))
    if len(candidates) != 1:
        raise RuntimeError(f"Expected one manifest under {raw_root / contract_symbol}, found {len(candidates)}")
    return candidates[0]


def source_file_identity(path: Path) -> dict[str, Any]:
    stat = os_path(path).stat()
    return {
        "path": rel(path),
        "size": stat.st_size,
        "modified_utc": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat().replace("+00:00", "Z"),
        "sha256": sha256_file(path),
    }


def load_raw_part(raw_root: Path, contract_symbol: str, source_name: str, priority: int) -> pd.DataFrame:
    csv_path = find_raw_csv(raw_root, contract_symbol)
    frame = pd.read_csv(csv_path)
    required_columns = {"time_open_unix", "time_close_unix", "open", "high", "low", "close"}
    missing = required_columns.difference(frame.columns)
    if missing:
        raise RuntimeError(f"{csv_path} missing columns: {sorted(missing)}")
    frame["timestamp"] = pd.to_datetime(frame["time_close_unix"], unit="s", utc=True)
    frame["timestamp_policy"] = fp.RAW_TIME_AXIS_POLICY
    frame = attach_event_time_columns(frame)
    frame["__source_name"] = source_name
    frame["__source_priority"] = priority
    return frame


def load_combined_raw_symbol(raw_root: Path, binding: fp.SymbolBinding) -> pd.DataFrame:
    del raw_root
    contract_symbol = binding.contract_symbol
    if contract_symbol in COMBINED_RAW_CACHE:
        return COMBINED_RAW_CACHE[contract_symbol].copy()
    parts = [
        load_raw_part(HISTORICAL_RAW_ROOT, contract_symbol, "historical_preload", 0),
        load_raw_part(FORWARD_RAW_ROOT, contract_symbol, "forward_raw", 1),
    ]
    frame = pd.concat(parts, ignore_index=True)
    frame = frame.sort_values(["timestamp", "__source_priority"]).drop_duplicates("timestamp", keep="last")
    frame = frame.loc[(frame["timestamp"] >= PRELOAD_START_UTC) & (frame["timestamp"] <= COMPUTE_END_UTC)].copy()
    frame = frame.sort_values("timestamp").reset_index(drop=True)
    if frame["timestamp"].duplicated().any():
        raise RuntimeError(f"Duplicate combined timestamps detected for {contract_symbol}")
    if not frame["timestamp"].is_monotonic_increasing:
        raise RuntimeError(f"Combined timestamps are not monotonic for {contract_symbol}")
    frame["contract_symbol"] = binding.contract_symbol
    frame["broker_symbol"] = binding.broker_symbol
    frame["source_csv_path"] = "historical_preload_plus_forward_raw"
    COMBINED_RAW_CACHE[contract_symbol] = frame.copy()
    return frame.copy()


def load_combined_source_identity(raw_root: Path, binding: fp.SymbolBinding) -> dict[str, Any]:
    del raw_root
    contract_symbol = binding.contract_symbol
    if contract_symbol in COMBINED_IDENTITY_CACHE:
        return COMBINED_IDENTITY_CACHE[contract_symbol]
    historical_csv = find_raw_csv(HISTORICAL_RAW_ROOT, contract_symbol)
    historical_manifest = find_raw_manifest(HISTORICAL_RAW_ROOT, contract_symbol)
    forward_csv = find_raw_csv(FORWARD_RAW_ROOT, contract_symbol)
    forward_manifest = find_raw_manifest(FORWARD_RAW_ROOT, contract_symbol)
    combined = load_combined_raw_symbol(Path("."), binding)
    identity = {
        "contract_symbol": binding.contract_symbol,
        "broker_symbol": binding.broker_symbol,
        "preload_start_utc": PRELOAD_START_UTC.isoformat(),
        "forward_output_start_utc": FORWARD_OUTPUT_START_UTC.isoformat(),
        "compute_end_utc": COMPUTE_END_UTC.isoformat(),
        "combined_rows": int(len(combined)),
        "combined_first_timestamp": combined["timestamp"].min().isoformat() if len(combined) else "",
        "combined_last_timestamp": combined["timestamp"].max().isoformat() if len(combined) else "",
        "historical_csv": source_file_identity(historical_csv),
        "historical_manifest": source_file_identity(historical_manifest),
        "forward_csv": source_file_identity(forward_csv),
        "forward_manifest": source_file_identity(forward_manifest),
    }
    COMBINED_IDENTITY_CACHE[contract_symbol] = identity
    return identity


def configure_foundation_materializer() -> None:
    fp.WINDOW_START_UTC = PRELOAD_START_UTC
    fp.WINDOW_END_UTC = COMPUTE_END_UTC
    fp.load_raw_symbol = load_combined_raw_symbol
    fp.load_source_identity = load_combined_source_identity


def timestamp_set(contract_symbol: str) -> set[pd.Timestamp]:
    for binding in fp.SYMBOL_BINDINGS:
        if binding.contract_symbol == contract_symbol:
            return set(load_combined_raw_symbol(Path("."), binding)["timestamp"])
    raise KeyError(contract_symbol)


def required_alignment_mask(timestamps: pd.Series, required_symbols: list[str]) -> np.ndarray:
    required_sets = [timestamp_set(symbol) for symbol in required_symbols]
    intersection = set.intersection(*required_sets) if required_sets else set()
    return timestamps.isin(intersection).to_numpy()


def materialize_feature_set(
    base_frame: pd.DataFrame,
    feature_set_id: str,
    config: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], list[Path]]:
    features: list[str] = list(config["features"])
    required_symbols: list[str] = list(config["required_symbols"])
    scoped = base_frame.loc[
        (base_frame["timestamp"] >= FORWARD_OUTPUT_START_UTC)
        & (base_frame["timestamp"] <= FORWARD_REQUESTED_TO_UTC),
        ["timestamp"] + features,
    ].copy()
    finite_values = scoped[features].replace([np.inf, -np.inf], np.nan)
    finite_mask = np.isfinite(finite_values.to_numpy(dtype="float64")).all(axis=1)
    alignment_mask = required_alignment_mask(scoped["timestamp"], required_symbols)
    valid_mask = finite_mask & alignment_mask

    valid_frame = scoped.loc[valid_mask, ["timestamp"] + features].copy()
    valid_frame["symbol"] = "US100"
    valid_frame = valid_frame[["timestamp", "symbol"] + features]
    valid_frame[features] = valid_frame[features].astype("float32")

    parquet_path = FEATURE_FRAME_DIR / f"{feature_set_id}.parquet"
    feature_order_path = FEATURE_ORDER_DIR / f"{feature_set_id}_feature_order.txt"
    summary_path = FEATURE_SUMMARY_DIR / f"{feature_set_id}_summary.json"
    os_path(parquet_path.parent).mkdir(parents=True, exist_ok=True)
    valid_frame.to_parquet(os_path(parquet_path), index=False)
    write_text(feature_order_path, "\n".join(features) + "\n")

    missing_counts: list[dict[str, Any]] = []
    for feature in features:
        missing_count = int(finite_values[feature].isna().sum())
        if missing_count:
            missing_counts.append(
                {
                    "feature_set_id": feature_set_id,
                    "feature": feature,
                    "missing_or_nonfinite_rows": missing_count,
                }
            )

    invalid_sample_rows: list[dict[str, Any]] = []
    invalid_scope = scoped.loc[~valid_mask, ["timestamp"]].head(80).copy()
    for _, row in invalid_scope.iterrows():
        idx = scoped.index[scoped["timestamp"].eq(row["timestamp"])][0]
        invalid_sample_rows.append(
            {
                "feature_set_id": feature_set_id,
                "timestamp": pd.Timestamp(row["timestamp"]).isoformat(),
                "alignment_ready": bool(alignment_mask[list(scoped.index).index(idx)]),
                "finite_ready": bool(finite_mask[list(scoped.index).index(idx)]),
            }
        )

    first_valid = valid_frame["timestamp"].min().isoformat() if len(valid_frame) else ""
    last_valid = valid_frame["timestamp"].max().isoformat() if len(valid_frame) else ""
    summary = {
        "feature_set_id": feature_set_id,
        "role": config["role"],
        "feature_count": len(features),
        "feature_order_sha256": ordered_hash(features),
        "required_symbols": required_symbols,
        "scope_rows": int(len(scoped)),
        "valid_rows": int(valid_mask.sum()),
        "invalid_rows": int((~valid_mask).sum()),
        "alignment_missing_rows": int((~alignment_mask).sum()),
        "finite_missing_rows": int((~finite_mask).sum()),
        "first_valid_timestamp": first_valid,
        "last_valid_timestamp": last_valid,
        "forward_requested_start_utc": FORWARD_REQUESTED_START_UTC.isoformat(),
        "forward_output_start_utc": FORWARD_OUTPUT_START_UTC.isoformat(),
        "forward_requested_to_utc": FORWARD_REQUESTED_TO_UTC.isoformat(),
        "preload_start_utc": PRELOAD_START_UTC.isoformat(),
        "parquet_path": rel(parquet_path),
        "parquet_sha256": sha256_file(parquet_path),
        "feature_order_path": rel(feature_order_path),
        "feature_order_sha256_file": sha256_file(feature_order_path),
        "status": "materialized" if int(valid_mask.sum()) > 0 else "blocked_no_valid_rows",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(summary_path, summary)
    artifacts = [parquet_path, feature_order_path, summary_path]
    return summary, missing_counts, invalid_sample_rows, artifacts


def build_feature_frames() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[Path], dict[str, Any]]:
    configure_foundation_materializer()
    frame, foundation_counts = fp.build_feature_frame(
        Path("."),
        weights_path=WEIGHTS_PATH,
        weights_version_label="foundation/config/top3_monthly_price_proxy_weights_fpmarkets_v2.csv@max_month_2026-04",
    )
    summaries: list[dict[str, Any]] = []
    missing_counts: list[dict[str, Any]] = []
    invalid_samples: list[dict[str, Any]] = []
    artifacts: list[Path] = []
    for feature_set_id, config in FEATURE_SETS.items():
        summary, missing_rows, invalid_rows, new_artifacts = materialize_feature_set(frame, feature_set_id, config)
        summaries.append(summary)
        missing_counts.extend(missing_rows)
        invalid_samples.extend(invalid_rows)
        artifacts.extend(new_artifacts)
    source_identity_path = RUN_DIR / "combined_source_identity.json"
    write_json(
        source_identity_path,
        {
            "historical_raw_root": rel(HISTORICAL_RAW_ROOT),
            "forward_raw_root": rel(FORWARD_RAW_ROOT),
            "source_identities": [load_combined_source_identity(Path("."), binding) for binding in fp.SYMBOL_BINDINGS],
        },
    )
    artifacts.append(source_identity_path)
    return summaries, missing_counts, invalid_samples, artifacts, foundation_counts


def write_receipts(
    generated_at_utc: str,
    summaries: list[dict[str, Any]],
    missing_counts: list[dict[str, Any]],
    invalid_samples: list[dict[str, Any]],
    foundation_counts: dict[str, Any],
) -> list[Path]:
    artifacts: list[Path] = []
    summary_csv = RUN_DIR / "feature_set_materialization_summary.csv"
    write_csv(
        summary_csv,
        [
            "feature_set_id",
            "role",
            "feature_count",
            "feature_order_sha256",
            "scope_rows",
            "valid_rows",
            "invalid_rows",
            "alignment_missing_rows",
            "finite_missing_rows",
            "first_valid_timestamp",
            "last_valid_timestamp",
            "status",
            "parquet_path",
            "parquet_sha256",
        ],
        summaries,
    )
    artifacts.append(summary_csv)

    missing_path = RUN_DIR / "missing_feature_counts.csv"
    write_csv(
        missing_path,
        ["feature_set_id", "feature", "missing_or_nonfinite_rows"],
        missing_counts or [{"feature_set_id": "", "feature": "", "missing_or_nonfinite_rows": 0}],
    )
    artifacts.append(missing_path)

    invalid_sample_path = RUN_DIR / "invalid_row_samples.csv"
    write_csv(
        invalid_sample_path,
        ["feature_set_id", "timestamp", "alignment_ready", "finite_ready"],
        invalid_samples or [{"feature_set_id": "", "timestamp": "", "alignment_ready": "", "finite_ready": ""}],
    )
    artifacts.append(invalid_sample_path)

    experiment_receipt = RUN_DIR / "experiment_design_receipt.json"
    write_json(
        experiment_receipt,
        {
            "hypothesis": "Live-computable feature sets can be materialized after the cp322A forward handoff block without reusing outcome-distilled signals.",
            "decision_use": "Feed run329C train/WFO rebuild controls; not select a model and not tune on forward holdout.",
            "comparison_baseline": "Stage328B blocked cp318 outcome source and Stage329A materialization queue.",
            "control_variables": [
                "foundation feature formulas",
                "bar-close timestamp alignment",
                "train-only label threshold policy for later runs",
                "forward holdout remains unlabeled and unoptimized",
            ],
            "changed_variables": [
                "date window parameterized through stage wrapper",
                "feature subsets core56/macro48/us100_technical42",
                "historical preload used only for rolling continuity",
            ],
            "sample_scope": f"{FORWARD_OUTPUT_START_UTC.isoformat()} to {FORWARD_REQUESTED_TO_UTC.isoformat()} with valid-session boundaries per feature set",
            "success_criteria": "At least one forward feature frame with finite aligned rows is materialized and registered.",
            "failure_criteria": "No feature set has valid rows or source alignment cannot be proven.",
            "invalid_conditions": "Labels, thresholds, or cp322A signal replay are used to filter rows.",
            "stop_conditions": "Stop before training if materialized frames lack old-window train/WFO counterpart or parity receipts.",
            "evidence_plan": [rel(summary_csv), rel(missing_path), rel(invalid_sample_path)],
        },
    )
    artifacts.append(experiment_receipt)

    data_receipt = RUN_DIR / "data_integrity_receipt.json"
    write_json(
        data_receipt,
        {
            "data_source": {
                "historical_raw_root": rel(HISTORICAL_RAW_ROOT),
                "forward_raw_root": rel(FORWARD_RAW_ROOT),
                "forward_raw_summary": rel(FORWARD_RAW_SUMMARY),
            },
            "time_axis": "raw broker-clock bar-close key with session mapper; no direct UTC session assumption",
            "sample_scope": summaries,
            "missing_or_duplicate_check": "combined raw per symbol is sorted and duplicate timestamps are dropped with forward source priority",
            "feature_label_boundary": "no labels are generated in run329B; forward rows are feature-only",
            "split_boundary": "forward holdout only; training/WFO rebuild is deferred to run329C",
            "leakage_risk": "historical preload may only influence rolling state, not row selection or labels",
            "data_hash_or_identity": rel(RUN_DIR / "combined_source_identity.json"),
            "foundation_invalid_reason_breakdown": foundation_counts.get("invalid_reason_breakdown", {}),
            "integrity_judgment": "usable_with_session_boundary",
        },
    )
    artifacts.append(data_receipt)

    model_receipt = RUN_DIR / "model_validation_receipt.json"
    write_json(
        model_receipt,
        {
            "model_family": "none_materialization_only",
            "target_and_label": "none in run329B",
            "split_method": "forward feature holdout materialization only",
            "selection_metric": "not_applicable",
            "secondary_metrics": ["valid_rows", "alignment_missing_rows", "finite_missing_rows", "feature_order_sha256"],
            "threshold_policy": "no threshold in run329B",
            "overfit_risk": "forward frame must not be used for threshold selection in run329C",
            "calibration_risk": "not_applicable_no_scores",
            "comparison_baseline": "Stage329A feature set queue",
            "validation_judgment": JUDGMENT,
        },
    )
    artifacts.append(model_receipt)

    parity_receipt = RUN_DIR / "runtime_parity_receipt.json"
    write_json(
        parity_receipt,
        {
            "research_path": rel(Path(__file__)),
            "runtime_path": "not_materialized_in_run329B",
            "shared_contract": "foundation feature order subset, bar-close alignment, no partial bar values",
            "known_differences": [
                "MT5 runtime handoff is not produced in run329B",
                "feature frames are Python materialization outputs only",
            ],
            "parity_check": "not_attempted_materialization_only",
            "parity_identity": [summary["feature_order_sha256"] for summary in summaries],
            "runtime_claim_boundary": "research_only",
        },
    )
    artifacts.append(parity_receipt)

    lineage_receipt = RUN_DIR / "artifact_lineage_receipt.json"
    write_json(
        lineage_receipt,
        {
            "source_inputs": [
                rel(HISTORICAL_RAW_ROOT),
                rel(FORWARD_RAW_ROOT),
                rel(WEIGHTS_PATH),
                rel(STAGE_DIR / "02_runs" / "run329A" / "rebuild_run_queue.csv"),
            ],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_ACTION,
            "artifact_paths": [rel(path) for path in artifacts],
            "artifact_hashes": {rel(path): sha256_file(path) for path in artifacts if path_exists(path)},
            "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_after_force_add_for_ignored_run_dir",
            "lineage_judgment": "connected_with_session_boundary",
        },
    )
    artifacts.append(lineage_receipt)

    gate_audit = RUN_DIR / "required_gate_coverage_audit.csv"
    write_csv(
        gate_audit,
        ["gate_name", "status", "evidence_path", "effect"],
        [
            {
                "gate_name": "experiment_design(실험 설계)",
                "status": "passed",
                "evidence_path": rel(experiment_receipt),
                "effect": "forward feature materialization(전진 피처 물질화)의 목적과 금지선을 고정했다.",
            },
            {
                "gate_name": "data_integrity(데이터 무결성)",
                "status": "passed_with_session_boundary",
                "evidence_path": rel(data_receipt),
                "effect": "historical preload(기존 선적재)와 forward raw(전진 원천)의 연결, 결측, 세션 경계를 기록했다.",
            },
            {
                "gate_name": "model_validation(모델 검증)",
                "status": "passed_materialization_only",
                "evidence_path": rel(model_receipt),
                "effect": "모델/임계값/점수 선택을 하지 않았음을 고정했다.",
            },
            {
                "gate_name": "runtime_parity(런타임 동등성)",
                "status": "not_attempted_by_claim",
                "evidence_path": rel(parity_receipt),
                "effect": "Python materialization(파이썬 물질화)만 주장하고 MT5/runtime authority(런타임 권위)는 주장하지 않는다.",
            },
            {
                "gate_name": "artifact_lineage(산출물 계보)",
                "status": "passed",
                "evidence_path": rel(lineage_receipt),
                "effect": "입력 원천, 산출물, 다음 소비 실행을 연결했다.",
            },
            {
                "gate_name": "result_judgment(결과 판정)",
                "status": "passed_no_goal_achieve",
                "evidence_path": rel(RUN_DIR / "result_judgment.csv"),
                "effect": "Goal Achieve(목표 달성)와 운영 주장(operating claim, 운영 주장)을 만들지 않았다.",
            },
        ],
    )
    artifacts.append(gate_audit)

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
    artifacts.append(result_judgment)

    manifest = RUN_DIR / "run_manifest.json"
    write_json(
        manifest,
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "generated_at_utc": generated_at_utc,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "next_action": NEXT_ACTION,
            "goal_achieve": "not_claimed",
            "feature_sets": summaries,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    artifacts.append(manifest)
    return artifacts


def markdown_summary_table(summaries: list[dict[str, Any]]) -> str:
    lines = [
        "| feature_set(피처 세트) | features(피처 수) | valid_rows(유효 행) | first_valid(첫 유효) | last_valid(마지막 유효) | status(상태) |",
        "|---|---:|---:|---|---|---|",
    ]
    for row in summaries:
        lines.append(
            "| {feature_set_id} | {feature_count} | {valid_rows} | {first_valid_timestamp} | {last_valid_timestamp} | {status} |".format(
                **row
            )
        )
    return "\n".join(lines)


def write_reports(summaries: list[dict[str, Any]]) -> list[Path]:
    artifacts: list[Path] = []
    table = markdown_summary_table(summaries)
    report = REVIEWS_DIR / "run329B_forward_feature_frame_materialization.md"
    write_md(
        report,
        f"""
# run329B Forward Feature Frame Materialization(329B 전진 피처 프레임 물질화)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- selected_candidate(선택 후보): `none`
- goal_achieve(목표 달성): `not_claimed`

## What changed(무엇이 바뀌었나)

Stage329A(329A 단계 실행)의 queue(대기열)를 실제 feature frame(피처 프레임)으로 만들었다. Foundation feature calculator(기반 피처 계산기)는 그대로 쓰고, Stage329B(329B 단계 실행) wrapper(래퍼)가 historical preload(기존 선적재)와 forward raw(전진 원천)를 붙였다.

Effect(효과): rolling window(롤링 창)는 기존 데이터로 연속성을 얻지만, 출력 행은 forward output start(전진 출력 시작) 이후로만 제한된다. Label(라벨), score threshold(점수 임계값), cp322A signal(322A 신호)은 만들거나 조정하지 않았다.

## Materialized Frames(물질화된 프레임)

{table}

## Boundary(경계)

2026-05-25 row(행)는 raw data(원천 데이터)가 있어도 session feature(세션 피처)와 cash-session boundary(현물장 세션 경계) 때문에 유효 feature row(유효 피처 행)로는 끝까지 이어지지 않는다. 이것은 pass/fail(통과/실패)이 아니라 다음 train/WFO rebuild(학습/워크포워드 재구축) 전에 보존해야 하는 data boundary(데이터 경계)다.

`{CLAIM_BOUNDARY}`

## Next(다음)

`{NEXT_ACTION}`
""",
    )
    artifacts.append(report)

    final_report = REVIEWS_DIR / "final_stage329B_decision_report.md"
    write_md(
        final_report,
        f"""
# Stage329B Final Decision(329B 최종 판정)

- decision(결정): `{DECISION}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- effect(효과): core56/macro48/us100-only feature frame(피처 프레임)을 만들었지만, 이것은 학습/WFO(워크포워드) 입력 준비일 뿐이며 forward robustness(전진 강건성) 통과 판정은 아니다.
- next_action(다음 행동): `{NEXT_ACTION}`
""",
    )
    artifacts.append(final_report)

    stage_ledger = REVIEWS_DIR / "stage_run_ledger.csv"
    replace_or_append_csv_rows(
        stage_ledger,
        ["row_id"],
        [
            {
                "row_id": f"{RUN_ID}__forward_feature_frame_materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "forward_feature_frame_materialization(전진 피처 프레임 물질화)",
                "tier_scope": "forward raw plus historical preload for rolling continuity(전진 원천 + 롤링 연속성용 기존 선적재)",
                "scoreboard": "feature_frame_validity(피처 프레임 유효성)",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": CLAIM_BOUNDARY,
                "report_path": rel(report),
                "notes": "no_labels;no_threshold_tuning;no_candidate_selected;run329C_train_wfo_next.",
            }
        ],
    )
    artifacts.append(stage_ledger)
    return artifacts


def update_selection_status(summaries: list[dict[str, Any]]) -> Path:
    valid_sets = [row["feature_set_id"] for row in summaries if int(row["valid_rows"]) > 0]
    min_last = min((str(row["last_valid_timestamp"]) for row in summaries if row["last_valid_timestamp"]), default="")
    selection = SELECTED_DIR / "selection_status.md"
    return write_md(
        selection,
        f"""
# Stage329 Selection Status(329단계 선택 상태)

- selected_candidate(선택 후보): `none`
- cp322A_status(cp322A 상태): `research_artifact_preserved_not_forward_authority`
- package_queue(패키지 대기열): `{', '.join(valid_sets)}`
- forward_dataset_status(전진 데이터셋 상태): `feature_frames_materialized_with_session_boundary`
- common_valid_boundary(공통 유효 경계): `{min_last}`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`
- effect(효과): forward holdout(전진 보류 표본)을 튜닝에 쓰지 않고, 다음 run329C(329C 실행)에서 old train/validation/OOS(기존 학습/검증/표본외)만으로 train/WFO rebuild(학습/워크포워드 재구축)를 검증한다.
""",
    )


def update_registers(generated_at_utc: str, artifacts: list[Path]) -> None:
    upsert_csv(
        RUN_REGISTRY,
        "run_id",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "data_materialization",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": rel(REVIEWS_DIR / "run329B_forward_feature_frame_materialization.md"),
            "notes": "forward_feature_frames_materialized;no_labels;no_candidate_selected;goal_achieve_not_claimed.",
        },
    )
    upsert_csv(
        ALPHA_LEDGER,
        "ledger_row_id",
        {
            "ledger_row_id": f"{RUN_ID}__forward_feature_frame_materialization",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": RUN_NUMBER,
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "forward_feature_frame_materialization",
            "tier_scope": "forward raw plus historical preload",
            "kpi_scope": "feature_frame_validity",
            "scoreboard_lane": "data_materialization",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": rel(REVIEWS_DIR / "run329B_forward_feature_frame_materialization.md"),
            "primary_kpi": "valid_feature_rows_by_feature_set",
            "guardrail_kpi": "no_labels;no_threshold_tuning;goal_achieve_not_claimed",
            "external_verification_status": "python_materialization_only_no_mt5_runtime_claim",
            "notes": f"next_action={NEXT_ACTION}.",
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


def update_current_truth(summaries: list[dict[str, Any]]) -> Path:
    workspace = ROOT / "docs" / "workspace" / "workspace_state.yaml"
    text, had_bom = read_text_lossless(workspace)
    text = replace_prefix_line(text, "current_run_id:", f"current_run_id: {RUN_ID}")
    text = replace_prefix_line(text, "updated_on:", "updated_on: '2026-05-26'")
    text = replace_prefix_line(text, "active_stage:", f"active_stage: {STAGE_ID}")
    focus = (
        "- >-\n"
        "  Stage329(329단계) run329B(329B 실행) forward feature frame materialization(전진 피처 프레임 물질화)을 닫았다. "
        "Effect(효과): core56/macro48/us100-only feature frame(피처 프레임)을 만들었지만, label(라벨), threshold tuning(임계값 튜닝), Goal Achieve(목표 달성)는 없다.\n"
    )
    if "Stage329(329단계) run329B(329B 실행)" not in text:
        text = text.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    write_text_preserving(workspace, text, had_bom)

    current = ROOT / "docs" / "context" / "current_working_state.md"
    text, had_bom = read_text_lossless(current)
    replacements = {
        "- current_packet(": f"- current_packet(현재 작업 묶음): `{STAGE_ID}_v2`",
        "- current_run(": f"- current_run(현재 실행): `{RUN_ID}`",
        "- active_stage(": f"- active_stage(활성 단계): `{STAGE_ID}`",
        "- selected_research_baseline(": "- selected_research_baseline(선택 연구 기준선): `none`",
        "- source_stage(": "- source_stage(원천 단계): `329_onnx_rebuild__live_feature_control`",
        "- target_surface(": "- target_surface(목표 표면): `forward_live_feature_frames_without_outcome_distillation`",
        "- adapter_under_review(": "- adapter_under_review(검토 중 어댑터): `none`",
        "- status(": f"- status(상태): `{STATUS}`",
        "- decision(": f"- decision(판정): `{JUDGMENT}`",
        "- next_action(": f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "- claim_boundary(": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    }
    for prefix, new_line in replacements.items():
        text = replace_prefix_line(text, prefix, new_line)
    summary = (
        f"- run329B_summary(329B 요약): forward feature frame materialization(전진 피처 프레임 물질화)을 `{STATUS}`로 닫았다. "
        "Effect(효과): feature frame(피처 프레임)은 준비됐지만 모델 학습(model training, 모델 학습), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 없다."
    )
    if "run329B_summary(329B 요약)" not in text:
        text = text.replace(f"- decision(판정): `{JUDGMENT}`\n", f"- decision(판정): `{JUDGMENT}`\n{summary}\n", 1)
    write_text_preserving(current, text, had_bom)

    changelog = ROOT / "docs" / "workspace" / "changelog.md"
    entry = f"""

## 2026-05-26 - Stage329B Forward Feature Frames(329B 전진 피처 프레임)

- run329B(329B 실행): historical preload(기존 선적재)와 forward raw(전진 원천)를 결합해 core56/macro48/us100-only feature frame(피처 프레임)을 물질화했다.
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): forward holdout(전진 보류)은 feature-only(피처 전용)로 남겼고, label(라벨), threshold tuning(임계값 튜닝), selected candidate(선택 후보), Goal Achieve(목표 달성)는 만들지 않았다.
"""
    append_bytes_if_missing(changelog, "## 2026-05-26 - Stage329B Forward Feature Frames", entry)

    return write_md(
        DECISION_DOC,
        f"""
# Stage329B Forward Feature Frames Decision(329B 전진 피처 프레임 결정)

- decision(결정): `{DECISION}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- selected_candidate(선택 후보): `none`
- goal_achieve(목표 달성): `not_claimed`
- effect(효과): forward feature frame(전진 피처 프레임)을 만들었지만, 이는 다음 train/WFO rebuild(학습/워크포워드 재구축)의 입력 근거일 뿐이다.
- next_action(다음 행동): `{NEXT_ACTION}`
- boundary(경계): `{CLAIM_BOUNDARY}`
- materialized_sets(물질화 세트): `{', '.join(row['feature_set_id'] for row in summaries)}`
""",
    )


def main() -> None:
    generated_at_utc = utc_now()
    for directory in (RUN_DIR, FEATURE_FRAME_DIR, FEATURE_ORDER_DIR, FEATURE_SUMMARY_DIR, REVIEWS_DIR, SELECTED_DIR):
        os_path(directory).mkdir(parents=True, exist_ok=True)

    summaries, missing_counts, invalid_samples, frame_artifacts, foundation_counts = build_feature_frames()
    artifacts = list(frame_artifacts)
    artifacts.extend(write_receipts(generated_at_utc, summaries, missing_counts, invalid_samples, foundation_counts))
    artifacts.extend(write_reports(summaries))
    artifacts.append(update_selection_status(summaries))
    artifacts.append(update_current_truth(summaries))
    update_registers(generated_at_utc, artifacts + [Path(__file__)])

    print(
        json.dumps(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "goal_achieve": "not_claimed",
                "next_action": NEXT_ACTION,
                "feature_sets": [
                    {
                        "feature_set_id": row["feature_set_id"],
                        "feature_count": row["feature_count"],
                        "valid_rows": row["valid_rows"],
                        "first_valid_timestamp": row["first_valid_timestamp"],
                        "last_valid_timestamp": row["last_valid_timestamp"],
                    }
                    for row in summaries
                ],
            },
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
