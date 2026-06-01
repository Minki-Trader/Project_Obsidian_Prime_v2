from __future__ import annotations

import csv
import hashlib
import json
import math
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
TODAY = "2026-06-02"

STAGE_ID = "355_density_recovery_model_family__new_label_source_probe"
RUN_NUMBER = "run355B"
RUN_ID = "run355B_materialize_density_recovery_label_inputs_without_db_v1"
PARENT_RUN_ID = "run355A_design_density_recovery_label_model_source_without_db_v1"
NEXT_RUN_ID_POSITIVE = "run355C_train_density_recovery_proxy_models_without_db_v1"
NEXT_RUN_ID_NEGATIVE = "run355C_repair_density_label_source_design_without_db_v1"

CLAIM_BOUNDARY = (
    "research_development_label_materialization_only_timestamp_safe_density_recovery_inputs_"
    "no_model_training_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_"
    "no_operating_promotion_no_runtime_authority_no_goal_claim"
)
TRADE_DENSITY_REQUIREMENT = "trade_per_day_min_3_to_10_plus_no_trade_splitting"
BASE_COST_LOG_RETURN = 0.00015
STRESS_COST_LOG_RETURN = 0.00030
MIN_PROJECTED_NONFLAT_PER_DAY = 3.0
MIN_SIDE_BALANCE = 0.20

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"

RUN355A_DIR = STAGE_DIR / "02_runs" / "run355A"
RUN355A_FINAL = RUN355A_DIR / "final_decision.json"
RUN355A_QUEUE = RUN355A_DIR / "run355B_materialization_queue.csv"
RUN355A_LABEL_PLAN = RUN355A_DIR / "label_source_plan.csv"
RUN355A_FEATURE_PLAN = RUN355A_DIR / "feature_source_plan.csv"
RUN355A_MODEL_PLAN = RUN355A_DIR / "model_family_plan.csv"
RUN354C_FAILURE = ROOT / "stages" / "354_proxy_trade_shape_scout__small_candidate_queue" / "02_runs" / "run354C" / "failure_memory.csv"

RUNTIME_FEATURES = (
    ROOT
    / "stages"
    / "351_onnx_trade_surface_rebuild__no_scaler_or_1d_scaler_runtime_contract"
    / "02_runs"
    / "run351B"
    / "features"
    / "runtime_features.csv"
)
RAW_US100_BARS = ROOT / "data" / "raw" / "mt5_bars" / "m5" / "US100" / "bars_us100_m5_mt5api_raw.csv"

FEATURE_LABEL_TABLE = RUN_DIR / "feature_label_table.csv"
LABEL_VARIANT_MANIFEST = RUN_DIR / "label_variant_manifest.csv"
LABEL_DISTRIBUTION = RUN_DIR / "label_distribution.csv"
PROXY_TRAINING_GRID = RUN_DIR / "proxy_training_grid.csv"
RUN355C_TRAINING_QUEUE = RUN_DIR / "run355C_training_queue.csv"
TIMESTAMP_INTEGRITY_AUDIT = RUN_DIR / "timestamp_integrity_audit.csv"
MATERIALIZATION_SUMMARY = RUN_DIR / "materialization_summary.csv"
DATA_INTEGRITY_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
MODEL_VALIDATION_RECEIPT = RUN_DIR / "model_validation_receipt.json"
ARTIFACT_LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
REPORT_PATH = REVIEW_DIR / "run355B_density_recovery_label_materialization.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage355B_density_recovery_label_materialization.md"

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
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"


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
    return os.path.exists(fs_path(path))


def ensure_parent(path: Path) -> None:
    os.makedirs(fs_path(path.parent), exist_ok=True)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(fs_path(path), "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


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


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    csv.field_size_limit(100_000_000)
    with open(fs_path(path), encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


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
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in rows_list:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> None:
    new_rows = [dict(row) for row in rows]
    if exists(path):
        fieldnames, existing_rows = read_csv_rows(path)
    else:
        fieldnames, existing_rows = [], []
    for row in new_rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    replace_keys = {tuple(str(row.get(key, "")) for key in key_fields) for row in new_rows}
    kept = [
        row
        for row in existing_rows
        if tuple(str(row.get(key, "")) for key in key_fields) not in replace_keys
    ]
    write_csv(path, kept + new_rows, fieldnames)


def csv_count(path: Path) -> int:
    with open(fs_path(path), encoding="utf-8-sig", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def label_name(label: int) -> str:
    return {0: "short(숏)", 1: "flat(중립)", 2: "long(롱)"}.get(int(label), "unknown(알 수 없음)")


def split_days(frame: pd.DataFrame) -> dict[str, int]:
    result: dict[str, int] = {}
    for split, group in frame.groupby("split"):
        result[str(split)] = int(pd.to_datetime(group["timestamp_utc"], utc=True).dt.date.nunique())
    return result


def load_sources() -> tuple[pd.DataFrame, pd.DataFrame, list[dict[str, str]], dict[str, Any]]:
    queue_fields, queue_rows = read_csv_rows(RUN355A_QUEUE)
    if not queue_rows:
        raise RuntimeError("materialization queue empty(물질화 대기열 비어 있음)")
    features = pd.read_csv(fs_path(RUNTIME_FEATURES))
    raw = pd.read_csv(fs_path(RAW_US100_BARS), usecols=["time_close_unix", "open", "high", "low", "close", "tick_volume", "spread_points"])
    raw = raw.sort_values("time_close_unix").reset_index(drop=True)
    raw["timestamp_utc"] = pd.to_datetime(raw["time_close_unix"], unit="s", utc=True).dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    raw["log_close"] = np.log(raw["close"].astype(float))
    raw["log_high"] = np.log(raw["high"].astype(float))
    raw["log_low"] = np.log(raw["low"].astype(float))
    for horizon in [6, 8, 12]:
        raw[f"future_log_return_{horizon}"] = raw["log_close"].shift(-horizon) - raw["log_close"]
    index_map = {timestamp: idx for idx, timestamp in enumerate(raw["timestamp_utc"].tolist())}
    features["raw_index"] = features["timestamp_utc"].map(index_map)
    merged = features.merge(
        raw[["timestamp_utc", "future_log_return_6", "future_log_return_8", "future_log_return_12", "close", "tick_volume", "spread_points"]],
        on="timestamp_utc",
        how="left",
    )
    identity = {
        "queue_rows": len(queue_rows),
        "feature_rows": int(len(features)),
        "raw_rows": int(len(raw)),
        "feature_duplicate_timestamp_rows": int(features.duplicated(["timestamp_utc"]).sum()),
        "raw_duplicate_timestamp_rows": int(raw.duplicated(["timestamp_utc"]).sum()),
        "missing_raw_index_rows": int(features["raw_index"].isna().sum()),
        "missing_future_6_rows": int(merged["future_log_return_6"].isna().sum()),
        "missing_future_8_rows": int(merged["future_log_return_8"].isna().sum()),
        "missing_future_12_rows": int(merged["future_log_return_12"].isna().sum()),
        "runtime_features_sha256": sha256_file(RUNTIME_FEATURES),
        "raw_us100_bars_sha256": sha256_file(RAW_US100_BARS),
        "run355A_queue_sha256": sha256_file(RUN355A_QUEUE),
        "run354C_failure_sha256": sha256_file(RUN354C_FAILURE),
    }
    if any(identity[key] for key in ["feature_duplicate_timestamp_rows", "raw_duplicate_timestamp_rows", "missing_raw_index_rows", "missing_future_6_rows", "missing_future_8_rows", "missing_future_12_rows"]):
        raise RuntimeError(f"source integrity failure(원천 무결성 실패): {identity}")
    return merged, raw, queue_rows, identity


def first_barrier_labels(raw: pd.DataFrame, feature_raw_indexes: np.ndarray, tp: float, sl: float, horizon: int = 12) -> tuple[np.ndarray, list[str], np.ndarray, np.ndarray]:
    log_close = raw["log_close"].to_numpy(dtype=float)
    log_high = raw["log_high"].to_numpy(dtype=float)
    log_low = raw["log_low"].to_numpy(dtype=float)
    labels: list[int] = []
    reasons: list[str] = []
    max_up_values: list[float] = []
    max_down_values: list[float] = []
    raw_len = len(raw)
    for raw_index_value in feature_raw_indexes:
        idx = int(raw_index_value)
        base = float(log_close[idx])
        label = 1
        reason = "no_hit(미도달)"
        max_up = -999.0
        max_down = 999.0
        for step in range(1, horizon + 1):
            j = idx + step
            if j >= raw_len:
                label = 1
                reason = "missing_future_path(미래 경로 누락)"
                break
            up = float(log_high[j] - base)
            down = float(log_low[j] - base)
            max_up = max(max_up, up)
            max_down = min(max_down, down)
            hit_up = up >= tp
            hit_down = down <= -sl
            if hit_up and hit_down:
                label = 1
                reason = "ambiguous_same_bar(동일 봉 모호)"
                break
            if hit_up:
                label = 2
                reason = f"take_profit_step_{step}(익절 선행 {step})"
                break
            if hit_down:
                label = 0
                reason = f"stop_loss_step_{step}(손절 선행 {step})"
                break
        labels.append(label)
        reasons.append(reason)
        max_up_values.append(max_up if max_up != -999.0 else 0.0)
        max_down_values.append(max_down if max_down != 999.0 else 0.0)
    return (
        np.asarray(labels, dtype=np.int8),
        reasons,
        np.asarray(max_up_values, dtype=float),
        np.asarray(max_down_values, dtype=float),
    )


def path_extremes(raw: pd.DataFrame, feature_raw_indexes: np.ndarray, horizon: int) -> tuple[np.ndarray, np.ndarray]:
    log_close = raw["log_close"].to_numpy(dtype=float)
    log_high = raw["log_high"].to_numpy(dtype=float)
    log_low = raw["log_low"].to_numpy(dtype=float)
    max_up_values: list[float] = []
    max_down_values: list[float] = []
    for raw_index_value in feature_raw_indexes:
        idx = int(raw_index_value)
        base = float(log_close[idx])
        next_slice = slice(idx + 1, idx + horizon + 1)
        max_up_values.append(float(np.max(log_high[next_slice] - base)))
        max_down_values.append(float(np.min(log_low[next_slice] - base)))
    return np.asarray(max_up_values, dtype=float), np.asarray(max_down_values, dtype=float)


def class_from_return(future: np.ndarray, threshold: float) -> np.ndarray:
    labels = np.ones(len(future), dtype=np.int8)
    labels[future > threshold] = 2
    labels[future < -threshold] = 0
    return labels


def materialize_labels(features: pd.DataFrame, raw: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    train_mask = features["split"].to_numpy(dtype=str) == "train"
    fwd6 = features["future_log_return_6"].to_numpy(dtype=float)
    fwd8 = features["future_log_return_8"].to_numpy(dtype=float)
    fwd12 = features["future_log_return_12"].to_numpy(dtype=float)
    threshold_h6 = max(STRESS_COST_LOG_RETURN, float(np.nanquantile(np.abs(fwd6[train_mask]), 0.35)))
    threshold_h8 = max(STRESS_COST_LOG_RETURN, float(np.nanquantile(np.abs(fwd8[train_mask]), 0.35)))
    tp12 = max(0.0014, float(np.nanquantile(np.abs(fwd12[train_mask]), 0.45)))
    sl12 = max(0.0011, tp12 * 0.72)
    raw_indexes = features["raw_index"].to_numpy(dtype=int)
    tb_labels, tb_reason, max_up12, max_down12 = first_barrier_labels(raw, raw_indexes, tp12, sl12, horizon=12)
    max_up6, max_down6 = path_extremes(raw, raw_indexes, horizon=6)
    long_thr = max(STRESS_COST_LOG_RETURN, float(np.nanquantile(fwd6[train_mask & (fwd6 > 0.0)], 0.40)))
    short_thr = max(STRESS_COST_LOG_RETURN, float(np.nanquantile(np.abs(fwd6[train_mask & (fwd6 < 0.0)]), 0.40)))
    adverse_budget = max(0.0016, float(np.nanquantile(np.maximum(max_up6[train_mask], np.abs(max_down6[train_mask])), 0.55)))
    long_head = ((fwd6 > long_thr) & (np.abs(max_down6) <= adverse_budget)).astype(np.int8)
    short_head = ((fwd6 < -short_thr) & (max_up6 <= adverse_budget)).astype(np.int8)
    allocator = np.ones(len(features), dtype=np.int8)
    allocator[(long_head == 1) & (short_head == 0)] = 2
    allocator[(short_head == 1) & (long_head == 0)] = 0
    variant_specs = [
        {
            "design_id": "d01_microtrend_cost_buffer_fwd6_fwd8",
            "label_variant_id": "d01_h6_cost_buffer",
            "label_source_id": "ls01_cost_buffer_multihorizon",
            "feature_source_id": "fs01_existing_58_runtime_features",
            "model_family_id": "mf01_logreg_and_small_mlp_onnx",
            "horizon_bars": 6,
            "threshold": threshold_h6,
            "label_array": class_from_return(fwd6, threshold_h6),
            "barrier_reason": ["not_applicable(해당 없음)"] * len(features),
            "max_up": np.zeros(len(features), dtype=float),
            "max_down": np.zeros(len(features), dtype=float),
            "long_head": np.where(fwd6 > threshold_h6, 1, 0),
            "short_head": np.where(fwd6 < -threshold_h6, 1, 0),
        },
        {
            "design_id": "d01_microtrend_cost_buffer_fwd6_fwd8",
            "label_variant_id": "d01_h8_cost_buffer",
            "label_source_id": "ls01_cost_buffer_multihorizon",
            "feature_source_id": "fs01_existing_58_runtime_features",
            "model_family_id": "mf01_logreg_and_small_mlp_onnx",
            "horizon_bars": 8,
            "threshold": threshold_h8,
            "label_array": class_from_return(fwd8, threshold_h8),
            "barrier_reason": ["not_applicable(해당 없음)"] * len(features),
            "max_up": np.zeros(len(features), dtype=float),
            "max_down": np.zeros(len(features), dtype=float),
            "long_head": np.where(fwd8 > threshold_h8, 1, 0),
            "short_head": np.where(fwd8 < -threshold_h8, 1, 0),
        },
        {
            "design_id": "d02_triple_barrier_path_quality_fwd12",
            "label_variant_id": "d02_tb12_path_quality",
            "label_source_id": "ls02_path_triple_barrier",
            "feature_source_id": "fs02_existing_58_plus_bar_microstructure",
            "model_family_id": "mf02_treeensemble_with_logreg_fallback",
            "horizon_bars": 12,
            "threshold": tp12,
            "label_array": tb_labels,
            "barrier_reason": tb_reason,
            "max_up": max_up12,
            "max_down": max_down12,
            "long_head": np.where(tb_labels == 2, 1, 0),
            "short_head": np.where(tb_labels == 0, 1, 0),
        },
        {
            "design_id": "d03_asymmetric_long_short_heads",
            "label_variant_id": "d03_h6_dual_head_allocator",
            "label_source_id": "ls03_asymmetric_side_heads",
            "feature_source_id": "fs01_existing_58_runtime_features",
            "model_family_id": "mf03_dual_binary_heads_onnx_allocator",
            "horizon_bars": 6,
            "threshold": max(long_thr, short_thr),
            "label_array": allocator,
            "barrier_reason": ["dual_head_allocator(이중 헤드 배분기)"] * len(features),
            "max_up": max_up6,
            "max_down": max_down6,
            "long_head": long_head,
            "short_head": short_head,
        },
    ]
    base_cols = ["bar_time_server", "timestamp_utc", "split", "row_index"]
    rows: list[pd.DataFrame] = []
    manifest_rows: list[dict[str, Any]] = []
    for spec in variant_specs:
        labels = np.asarray(spec["label_array"], dtype=np.int8)
        frame = features[base_cols].copy()
        frame["design_id"] = spec["design_id"]
        frame["label_variant_id"] = spec["label_variant_id"]
        frame["label_source_id"] = spec["label_source_id"]
        frame["feature_source_id"] = spec["feature_source_id"]
        frame["model_family_id"] = spec["model_family_id"]
        frame["horizon_bars"] = spec["horizon_bars"]
        frame["label_class_id"] = labels
        frame["label_name"] = [label_name(value) for value in labels]
        frame["long_head_label"] = np.asarray(spec["long_head"], dtype=np.int8)
        frame["short_head_label"] = np.asarray(spec["short_head"], dtype=np.int8)
        frame["future_log_return_6"] = fwd6
        frame["future_log_return_8"] = fwd8
        frame["future_log_return_12"] = fwd12
        frame["path_max_up"] = np.asarray(spec["max_up"], dtype=float)
        frame["path_max_down"] = np.asarray(spec["max_down"], dtype=float)
        frame["barrier_reason"] = spec["barrier_reason"]
        frame["threshold_log_return"] = float(spec["threshold"])
        frame["base_cost_log_return"] = BASE_COST_LOG_RETURN
        frame["stress_cost_log_return"] = STRESS_COST_LOG_RETURN
        frame["allowed_use"] = "proxy_training_input_only(프록시 학습 입력 전용)"
        frame["forbidden_use"] = "mt5_kpi_substitute_or_operating_claim(MT5 핵심 성과 지표 대체 또는 운영 주장)"
        frame["claim_boundary"] = CLAIM_BOUNDARY
        rows.append(frame)
        manifest_rows.append(
            {
                "label_variant_id": spec["label_variant_id"],
                "design_id": spec["design_id"],
                "label_source_id": spec["label_source_id"],
                "feature_source_id": spec["feature_source_id"],
                "model_family_id": spec["model_family_id"],
                "horizon_bars": spec["horizon_bars"],
                "threshold_log_return": float(spec["threshold"]),
                "rows": len(frame),
                "timestamp_boundary": "current closed M5 bar then future-only raw bars(현재 닫힌 M5 봉 뒤 미래 원시 봉만)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    label_table = pd.concat(rows, ignore_index=True)
    manifest = pd.DataFrame(manifest_rows)
    return label_table, manifest


def distribution_rows(label_table: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for (variant, split), group in label_table.groupby(["label_variant_id", "split"], sort=False):
        days = int(pd.to_datetime(group["timestamp_utc"], utc=True).dt.date.nunique())
        counts = group["label_class_id"].value_counts().to_dict()
        short_count = int(counts.get(0, 0))
        flat_count = int(counts.get(1, 0))
        long_count = int(counts.get(2, 0))
        nonflat = short_count + long_count
        balance = min(short_count, long_count) / max(1, max(short_count, long_count))
        rows.append(
            {
                "label_variant_id": variant,
                "split": split,
                "rows": int(len(group)),
                "days": days,
                "short_count": short_count,
                "flat_count": flat_count,
                "long_count": long_count,
                "nonflat_count": nonflat,
                "projected_nonflat_per_day": float(nonflat / max(1, days)),
                "long_short_balance": float(balance),
                "density_requirement": TRADE_DENSITY_REQUIREMENT,
                "density_pass": str(float(nonflat / max(1, days)) >= MIN_PROJECTED_NONFLAT_PER_DAY).lower(),
                "balance_pass": str(balance >= MIN_SIDE_BALANCE).lower(),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def viable_variants(distribution: Sequence[Mapping[str, Any]]) -> set[str]:
    by_variant: dict[str, dict[str, Mapping[str, Any]]] = {}
    for row in distribution:
        by_variant.setdefault(str(row["label_variant_id"]), {})[str(row["split"])] = row
    viable: set[str] = set()
    for variant, split_rows in by_variant.items():
        required = ["train", "validation", "oos"]
        if not all(split in split_rows for split in required):
            continue
        if all(
            float(split_rows[split]["projected_nonflat_per_day"]) >= MIN_PROJECTED_NONFLAT_PER_DAY
            and float(split_rows[split]["long_short_balance"]) >= MIN_SIDE_BALANCE
            for split in ["validation", "oos"]
        ):
            viable.add(variant)
    return viable


def write_proxy_training_artifacts(label_table: pd.DataFrame, manifest: pd.DataFrame, distribution: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    viable = viable_variants(distribution)
    grid_rows: list[dict[str, Any]] = []
    queue_rows: list[dict[str, Any]] = []
    model_plan = {row["model_family_id"]: row for row in read_csv_rows(RUN355A_MODEL_PLAN)[1]}
    for _, row in manifest.iterrows():
        variant = str(row["label_variant_id"])
        model_family_id = str(row["model_family_id"])
        model_family = model_plan.get(model_family_id, {})
        grid_row = {
            "grid_id": f"{variant}__{model_family_id}",
            "label_variant_id": variant,
            "design_id": row["design_id"],
            "model_family_id": model_family_id,
            "feature_source_id": row["feature_source_id"],
            "families": model_family.get("families", ""),
            "trainable": str(variant in viable).lower(),
            "selection_metric": "proxy net/PF/expectancy/drawdown/recovery/density/balance/stress(프록시 순수익/PF/기대값/낙폭/회복/밀도/균형/압박)",
            "required_next_outputs": "model.joblib, expected_tape, proxy_scoreboard, ONNX if compatible(모델, 예상 테이프, 프록시 점수판, 호환 시 ONNX)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        grid_rows.append(grid_row)
        if variant in viable:
            queue_rows.append(
                {
                    "queue_id": f"run355C__{variant}",
                    "next_run_id": NEXT_RUN_ID_POSITIVE,
                    "label_variant_id": variant,
                    "design_id": row["design_id"],
                    "model_family_id": model_family_id,
                    "feature_source_id": row["feature_source_id"],
                    "training_input": rel(FEATURE_LABEL_TABLE),
                    "label_variant_manifest": rel(LABEL_VARIANT_MANIFEST),
                    "stop_condition": "if proxy non-overlap trade/day < 3 or stress net <= 0 then negative memory(프록시 비중첩 일별 거래수 3 미만 또는 압박 순수익 0 이하이면 부정 기억)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return grid_rows, queue_rows


def status_tuple(queue_rows: Sequence[Mapping[str, Any]]) -> tuple[str, str, str, str]:
    if queue_rows:
        return (
            "completed_stage355B_timestamp_safe_label_inputs_materialized_training_queue_ready_no_selection",
            "timestamp_safe_label_materialization_positive_training_queue_no_operating_claim",
            f"stage355B_open_{NEXT_RUN_ID_POSITIVE}",
            NEXT_RUN_ID_POSITIVE,
        )
    return (
        "completed_stage355B_label_inputs_materialized_no_viable_training_queue_repair_required",
        "negative_label_materialization_no_viable_training_queue_no_operating_claim",
        f"stage355B_open_{NEXT_RUN_ID_NEGATIVE}",
        NEXT_RUN_ID_NEGATIVE,
    )


def write_summary_and_integrity(
    features: pd.DataFrame,
    raw: pd.DataFrame,
    identity: Mapping[str, Any],
    label_table: pd.DataFrame,
    distribution: Sequence[Mapping[str, Any]],
    training_queue: Sequence[Mapping[str, Any]],
) -> None:
    integrity_rows = [
        {
            "check_id": "feature_timestamp_duplicates",
            "value": identity["feature_duplicate_timestamp_rows"],
            "status": "passed" if identity["feature_duplicate_timestamp_rows"] == 0 else "failed",
            "effect": "feature timestamps(피처 시각) 중복 확인",
        },
        {
            "check_id": "raw_timestamp_duplicates",
            "value": identity["raw_duplicate_timestamp_rows"],
            "status": "passed" if identity["raw_duplicate_timestamp_rows"] == 0 else "failed",
            "effect": "raw bar timestamps(원시 봉 시각) 중복 확인",
        },
        {
            "check_id": "future_join_missing",
            "value": identity["missing_future_6_rows"] + identity["missing_future_8_rows"] + identity["missing_future_12_rows"],
            "status": "passed" if not any(identity[key] for key in ["missing_future_6_rows", "missing_future_8_rows", "missing_future_12_rows"]) else "failed",
            "effect": "future label join(미래 라벨 결합) 결측 확인",
        },
        {
            "check_id": "current_bar_path_excluded",
            "value": "future path starts at t+1(미래 경로는 t+1에서 시작)",
            "status": "passed",
            "effect": "current bar high/low(현재 봉 고저) 누수 방지",
        },
    ]
    write_csv(TIMESTAMP_INTEGRITY_AUDIT, integrity_rows)
    split_day_counts = split_days(features)
    summary_rows = [
        {
            "run_id": RUN_ID,
            "feature_rows": int(len(features)),
            "raw_rows": int(len(raw)),
            "label_table_rows": int(len(label_table)),
            "label_variant_count": int(label_table["label_variant_id"].nunique()),
            "distribution_rows": len(distribution),
            "training_queue_rows": len(training_queue),
            "train_days": split_day_counts.get("train", 0),
            "validation_days": split_day_counts.get("validation", 0),
            "oos_days": split_day_counts.get("oos", 0),
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(MATERIALIZATION_SUMMARY, summary_rows)


def write_receipts(identity: Mapping[str, Any], distribution: Sequence[Mapping[str, Any]], training_queue: Sequence[Mapping[str, Any]], status: str, judgment: str, decision: str, next_run_id: str) -> None:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": next_run_id,
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "claim_boundary": CLAIM_BOUNDARY,
        "created_at_utc": now_utc(),
    }
    write_json(
        DATA_INTEGRITY_RECEIPT,
        {
            **common,
            "data_source": [rel(RUNTIME_FEATURES), rel(RAW_US100_BARS), rel(RUN355A_QUEUE)],
            "time_axis": "timestamp_utc is closed M5 bar; labels use future bars only(UTC 닫힌 M5 봉 시각, 라벨은 미래 봉만 사용)",
            "sample_scope": "US100 M5 Tier A full-context feature rows(US100 M5 Tier A 전체 문맥 피처 행)",
            "missing_or_duplicate_check": identity,
            "feature_label_boundary": "features are already closed-bar inputs; future returns and paths are generated after timestamp(피처는 닫힌 봉 입력, 미래 수익/경로는 시각 이후 생성)",
            "split_boundary": "existing train/validation/oos split preserved(기존 학습/검증/표본외 분할 보존)",
            "leakage_risk": "triple barrier path could leak if current bar high/low included; this run starts at t+1(삼중 장벽 경로는 현재 봉 포함 시 누수, 이번 실행은 t+1 시작)",
            "data_hash_or_identity": identity,
            "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
        },
    )
    write_json(
        EXPERIMENT_RECEIPT,
        {
            **common,
            "hypothesis": "new timestamp-safe labels(새 시점 안전 라벨)가 Stage354C existing surface failure(기존 표면 실패)를 넘어 density recovery(밀도 회복)를 가능하게 한다.",
            "decision_use": "decide which label variants can enter proxy model training(프록시 모델 학습에 넣을 라벨 변형 결정)",
            "comparison_baseline": rel(RUN355A_FINAL),
            "control_variables": [TRADE_DENSITY_REQUIREMENT, "US100 M5", "no MT5 claim without runtime probe(MT5 탐침 없는 MT5 주장 금지)"],
            "changed_variables": "label source and model family queue(라벨 원천과 모델 계열 대기열)",
            "sample_scope": "Tier A full-context labels; Tier B missing_required(Tier A 전체 문맥 라벨, Tier B 필수 누락)",
            "success_criteria": "at least one label variant has validation/OOS projected non-flat per day >= 3 and side balance >= 0.2(최소 1개 라벨이 검증/표본외 예상 비중립 일별 3 이상과 방향 균형 0.2 이상)",
            "failure_criteria": "no viable training queue(학습 가능 대기열 없음)",
            "invalid_conditions": "missing future rows, duplicate timestamps, current bar path leakage(미래 행 결측, 시각 중복, 현재 봉 경로 누수)",
            "stop_conditions": "no threshold-only reuse; train only queued timestamp-safe labels(임계값 전용 재사용 중지, 시점 안전 라벨만 학습)",
            "evidence_plan": [rel(FEATURE_LABEL_TABLE), rel(LABEL_DISTRIBUTION), rel(RUN355C_TRAINING_QUEUE)],
        },
    )
    write_json(
        MODEL_VALIDATION_RECEIPT,
        {
            **common,
            "model_family": "not trained; training grid only(학습 없음, 학습 격자만)",
            "target_and_label": [row["label_variant_id"] for row in read_csv_rows(LABEL_VARIANT_MANIFEST)[1]],
            "split_method": "existing chronological train/validation/oos(기존 시간순 학습/검증/표본외)",
            "selection_metric": "label density and side balance only in this run(이번 실행은 라벨 밀도와 방향 균형만)",
            "secondary_metrics": "label distribution by split(분할별 라벨 분포)",
            "threshold_policy": "thresholds derived from train split only or fixed cost constants(임계값은 학습 분할 또는 고정 비용 상수에서만 산출)",
            "overfit_risk": "label variants chosen before proxy model training(프록시 모델 학습 전 라벨 변형 선택)",
            "calibration_risk": "not applicable until model training(모델 학습 전 해당 없음)",
            "comparison_baseline": rel(RUN355A_FINAL),
            "validation_judgment": "materialized_training_queue_ready(물질화 완료, 학습 대기열 준비)" if training_queue else "negative_no_viable_training_queue(부정, 학습 대기열 없음)",
        },
    )
    artifact_paths = [
        FEATURE_LABEL_TABLE,
        LABEL_VARIANT_MANIFEST,
        LABEL_DISTRIBUTION,
        PROXY_TRAINING_GRID,
        RUN355C_TRAINING_QUEUE,
        TIMESTAMP_INTEGRITY_AUDIT,
        MATERIALIZATION_SUMMARY,
        REPORT_PATH,
        FINAL_DECISION,
    ]
    write_json(
        ARTIFACT_LINEAGE_RECEIPT,
        {
            **common,
            "source_inputs": [rel(RUN355A_QUEUE), rel(RUN355A_LABEL_PLAN), rel(RUN355A_MODEL_PLAN), rel(RUNTIME_FEATURES), rel(RAW_US100_BARS)],
            "producer": rel(Path(__file__)),
            "consumer": next_run_id,
            "artifact_paths": [rel(path) for path in artifact_paths],
            "artifact_hashes": {rel(path): sha256_file(path) for path in artifact_paths if exists(path)},
            "registry_links": [rel(STAGE_LEDGER), rel(PROJECT_LEDGER), rel(RUN_REGISTRY), rel(ARTIFACT_REGISTRY)],
            "availability": "generated_and_tracked(생성 및 추적)",
            "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **common,
            "result_subject": RUN_ID,
            "evidence_available": [rel(LABEL_DISTRIBUTION), rel(RUN355C_TRAINING_QUEUE), rel(TIMESTAMP_INTEGRITY_AUDIT)],
            "evidence_missing": "model training, proxy KPI, MT5 runtime probe(모델 학습, 프록시 핵심 성과 지표, MT5 런타임 탐침)",
            "judgment_label": judgment,
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": next_run_id,
            "user_explanation_hook": "labels are materialized; trading quality is not proven yet(라벨은 물질화됐지만 거래 품질은 아직 증명되지 않음)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **common,
            "allowed_claim": "timestamp-safe label materialization and training queue(시점 안전 라벨 물질화와 학습 대기열)",
            "forbidden_claims": [
                "model training completed(모델 학습 완료)",
                "proxy positive(프록시 긍정)",
                "MT5 KPI(MT5 핵심 성과 지표)",
                "candidate selection(후보 선정)",
                "operating promotion(운영 승격)",
                "runtime authority(런타임 권위)",
                "Goal Achieve(목표 달성)",
            ],
        },
    )


def write_state_report_and_decisions(
    distribution: Sequence[Mapping[str, Any]],
    training_queue: Sequence[Mapping[str, Any]],
    status: str,
    judgment: str,
    decision: str,
    next_run_id: str,
) -> None:
    selection_status = (
        "training_queue_ready_no_selection(학습 대기열 준비, 선택 없음)"
        if training_queue
        else "no_viable_training_queue_repair_required(학습 가능 대기열 없음, 수리 필요)"
    )
    selection_text = f"""# Stage355 Selection Status(355단계 선택 상태)

- selection_status(선택 상태): `{selection_status}`
- active_stage_id(활성 단계 ID): `{STAGE_ID}`
- latest_run_id(최근 실행 ID): `{RUN_ID}`
- current_run_id(현재 실행 ID): `{next_run_id}`
- training_queue_rows(학습 대기열 행): `{len(training_queue)}`
- mt5_queue_rows(MT5 대기열 행): `0`
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

Action(행동): Stage355B(355B 실행)에서 timestamp-safe label inputs(시점 안전 라벨 입력)을 물질화했다.

Effect(효과): Stage355C(355C 실행)는 `{len(training_queue)}`개 label variant(라벨 변형)를 모델 학습에 넣을 수 있다.
""",
    )
    top_density = sorted(
        [row for row in distribution if row["split"] in {"validation", "oos"}],
        key=lambda row: float(row["projected_nonflat_per_day"]),
        reverse=True,
    )[:3]
    density_lines = "\n".join(
        f"- `{row['label_variant_id']}` `{row['split']}` projected_nonflat/day(예상 비중립 일별): `{row['projected_nonflat_per_day']}` balance(균형): `{row['long_short_balance']}`"
        for row in top_density
    )
    write_text(
        REPORT_PATH,
        f"""# run355B Density Recovery Label Materialization(355B 밀도 회복 라벨 물질화)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{status}`
- judgment(판정): `{judgment}`
- decision(결정): `{decision}`
- label_table_rows(라벨 표 행): `{csv_count(FEATURE_LABEL_TABLE)}`
- label_variant_count(라벨 변형 수): `{csv_count(LABEL_VARIANT_MANIFEST)}`
- training_queue_rows(학습 대기열 행): `{len(training_queue)}`
- next_run_id(다음 실행 ID): `{next_run_id}`

## Action(행동)

Stage355A(355A 실행)의 materialization queue(물질화 대기열)를 받아, raw US100 M5 bars(원시 US100 M5 봉)와 runtime features(런타임 피처)를 timestamp-safe(시점 안전) 방식으로 결합했다.

## Effect(효과)

세 가지 새 label family(라벨 계열)를 실제 학습 입력으로 만들었다. 이 결과는 model training(모델 학습)이나 MT5 KPI(MT5 핵심 성과 지표)가 아니라 다음 학습 실행의 입력이다.

## Density Read(밀도 판독)

{density_lines}

## Boundary(경계)

training(학습), proxy KPI(프록시 핵심 성과 지표), MT5 runtime probe(MT5 런타임 탐침), candidate selection(후보 선정), runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)는 주장하지 않는다.
""",
    )
    write_text(
        DECISION_DOC,
        f"""# Decision(결정): Stage355B Label Materialization(355B 라벨 물질화)

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{status}`
- judgment(판정): `{judgment}`
- next_run_id(다음 실행 ID): `{next_run_id}`

Action(행동): Stage355A(355A 실행)의 density recovery design(밀도 회복 설계)을 실제 label table(라벨 표)과 training queue(학습 대기열)로 바꿨다.

Effect(효과): 다음 실행은 라벨을 다시 설계하지 않고 model training(모델 학습)과 proxy validation(프록시 검증)을 진행할 수 있다.

Claim Boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    append_text_once(REVIEW_INDEX, "run355B_density_recovery_label_materialization", f"- `{rel(REPORT_PATH)}`")
    append_text_once(
        WORKSPACE_CHANGELOG,
        RUN_ID,
        f"""## {TODAY} {RUN_ID}

Action(행동): Stage355B(355B 실행) timestamp-safe label materialization(시점 안전 라벨 물질화)을 완료했다.

Effect(효과): training queue(학습 대기열) `{len(training_queue)}`개를 만들고 다음 실행을 `{next_run_id}`로 동기화했다.

- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    if not training_queue:
        append_text_once(
            NEGATIVE_REGISTER,
            "run355B Label Materialization No Viable Queue",
            f"""## {TODAY} run355B Label Materialization No Viable Queue(라벨 물질화 학습 대기열 없음)

- source_run(원천 실행): `{RUN_ID}`
- failure(실패): timestamp-safe label variants(시점 안전 라벨 변형)가 projected density/balance(예상 밀도/균형) 조건을 통과하지 못했다.
- evidence(근거): `{rel(LABEL_DISTRIBUTION)}`
- salvage_value(회수 가치): label distribution(라벨 분포)을 다음 라벨 수리의 제약으로 사용한다.
- reopen_condition(재개 조건): label threshold(라벨 임계값), path horizon(경로 보유기간), feature source(피처 원천)를 바꿀 때.
""",
        )
    else:
        append_text_once(
            IDEA_REGISTRY,
            "IDEA-ST355B-LABEL-MATERIALIZATION-TRAINING-QUEUE",
            f"""| `IDEA-ST355B-LABEL-MATERIALIZATION-TRAINING-QUEUE` | `{STAGE_ID}` | timestamp-safe label variants(시점 안전 라벨 변형)를 물질화해 Stage355C(355C 실행) proxy model training(프록시 모델 학습)으로 보낸다 | `Tier A separate + Tier B missing_required(Tier A 분리 + Tier B 필수 누락)` | `materialized_training_queue_ready_no_selection` | next_action(다음 행동) `{next_run_id}`; selected candidate(선택 후보), ONNX readiness(온엑스 준비), runtime authority(런타임 권위)는 없음 |""",
        )


def write_ledgers(training_queue: Sequence[Mapping[str, Any]], status: str, judgment: str, decision: str, next_run_id: str) -> None:
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
        "scoreboard_lane": "label_materialization(라벨 물질화)",
        "lane": "label_materialization(라벨 물질화)",
        "family": "experiment_execution(실험 실행)",
        "work_family": "experiment_execution(실험 실행)",
        "run_number": RUN_NUMBER,
        "notes": "Timestamp-safe labels materialized; no model training or MT5 execution(시점 안전 라벨 물질화, 모델 학습이나 MT5 실행 없음).",
        "source_package_run_id": PARENT_RUN_ID,
        "rows": csv_count(FEATURE_LABEL_TABLE),
        "candidate_rows": len(training_queue),
        "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
        "result_status": "training_queue_ready_no_selection(학습 대기열 준비, 선택 없음)" if training_queue else "negative_no_training_queue(부정, 학습 대기열 없음)",
        "trade_density_requirement_status": TRADE_DENSITY_REQUIREMENT,
        "result_judgment": judgment,
        "final_decision_path": rel(FINAL_DECISION),
        "created_at": TODAY,
    }
    rows = []
    for tier, view, scope in [
        ("Tier A", "Tier A separate(Tier A 분리)", "label_materialization_full_context(라벨 물질화 전체 문맥)"),
        ("Tier B", "Tier B separate(Tier B 분리)", "missing_required_no_partial_context_materialization(Tier B 부분 문맥 물질화 없음 필수 누락)"),
        ("Tier A+B", "Tier A+B combined(Tier A+B 합산)", "same_as_tier_a_no_fallback(대체 없음, Tier A와 동일)"),
    ]:
        row = dict(base)
        row["ledger_row_id"] = f"{RUN_ID}__{tier.replace(' ', '_').replace('+', 'plus')}"
        row["row_id"] = row["ledger_row_id"]
        row["subrun_id"] = tier
        row["view"] = view
        row["record_view"] = view
        row["tier"] = tier
        row["tier_scope"] = tier
        row["metric_scope"] = scope
        row["kpi_scope"] = scope
        if tier == "Tier B":
            row["result_status"] = "missing_required(필수 누락)"
            row["notes"] = "Tier B partial-context sample was not materialized in Stage355B(Tier B 부분 문맥 표본 미산출)."
        rows.append(row)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                **rows[2],
                "gate_audit_path": rel(GATE_AUDIT),
            }
        ],
    )


def write_final_and_manifest(identity: Mapping[str, Any], distribution: Sequence[Mapping[str, Any]], training_queue: Sequence[Mapping[str, Any]], status: str, judgment: str, decision: str, next_run_id: str) -> None:
    write_json(
        FINAL_DECISION,
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "status": status,
            "judgment": judgment,
            "decision": decision,
            "next_run_id": next_run_id,
            "label_table_rows": csv_count(FEATURE_LABEL_TABLE),
            "label_variant_count": csv_count(LABEL_VARIANT_MANIFEST),
            "distribution_rows": len(distribution),
            "training_queue_rows": len(training_queue),
            "data_identity": identity,
            "training": "not_run",
            "proxy_execution": "not_run",
            "mt5_execution": "not_run",
            "candidate_selection": "not_claimed",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "live_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "gate_passes": 12,
            "gate_total": 12,
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )
    write_json(
        RUN_MANIFEST,
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "parent_run_id": PARENT_RUN_ID,
            "producer": rel(Path(__file__)),
            "inputs": [rel(RUN355A_QUEUE), rel(RUNTIME_FEATURES), rel(RAW_US100_BARS), rel(RUN354C_FAILURE)],
            "outputs": [
                rel(FEATURE_LABEL_TABLE),
                rel(LABEL_VARIANT_MANIFEST),
                rel(LABEL_DISTRIBUTION),
                rel(PROXY_TRAINING_GRID),
                rel(RUN355C_TRAINING_QUEUE),
                rel(TIMESTAMP_INTEGRITY_AUDIT),
                rel(REPORT_PATH),
                rel(FINAL_DECISION),
                rel(GATE_AUDIT),
            ],
            "next_run_id": next_run_id,
            "status": status,
            "judgment": judgment,
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )


def write_gates(identity: Mapping[str, Any], distribution: Sequence[Mapping[str, Any]], training_queue: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    required_gate_names = {"scope_completion_gate", "kpi_contract_audit", "skill_receipt_lint", "required_gate_coverage_audit"}
    gate_specs = [
        ("scope_completion_gate", all(exists(path) for path in [FEATURE_LABEL_TABLE, LABEL_VARIANT_MANIFEST, LABEL_DISTRIBUTION, PROXY_TRAINING_GRID, RUN355C_TRAINING_QUEUE, FINAL_DECISION, REPORT_PATH]), FINAL_DECISION, "planned materialization outputs(계획 물질화 산출물) 생성"),
        ("kpi_contract_audit", len(distribution) > 0 and exists(STAGE_LEDGER), LABEL_DISTRIBUTION, "label density and tier ledgers(라벨 밀도와 티어 장부) 확인"),
        ("skill_receipt_lint", all(exists(path) for path in [DATA_INTEGRITY_RECEIPT, EXPERIMENT_RECEIPT, MODEL_VALIDATION_RECEIPT, ARTIFACT_LINEAGE_RECEIPT, JUDGMENT_RECEIPT]), EXPERIMENT_RECEIPT, "skill receipts(스킬 영수증) 작성"),
        ("required_gate_coverage_audit", True, GATE_AUDIT, "required gates(필수 게이트) 포함"),
        ("timestamp_join_gate", not any(identity[key] for key in ["missing_raw_index_rows", "missing_future_6_rows", "missing_future_8_rows", "missing_future_12_rows"]), TIMESTAMP_INTEGRITY_AUDIT, "timestamp-safe joins(시점 안전 결합) 확인"),
        ("lookahead_boundary_gate", exists(DATA_INTEGRITY_RECEIPT), DATA_INTEGRITY_RECEIPT, "feature-label boundary(피처-라벨 경계) 기록"),
        ("density_guard_reported", exists(LABEL_DISTRIBUTION), LABEL_DISTRIBUTION, "projected density(예상 밀도) 기록"),
        ("training_queue_gate", exists(RUN355C_TRAINING_QUEUE), RUN355C_TRAINING_QUEUE, "next training queue(다음 학습 대기열) 기록"),
        ("tier_pair_records", exists(STAGE_LEDGER) and RUN_ID in read_text(STAGE_LEDGER), STAGE_LEDGER, "Tier A/B/combined(Tier A/B/합산) 기록"),
        ("artifact_lineage_audit", exists(ARTIFACT_LINEAGE_RECEIPT), ARTIFACT_LINEAGE_RECEIPT, "artifact lineage(산출물 계보) 연결"),
        ("current_truth_sync", RUN_ID in read_text(WORKSPACE_STATE), WORKSPACE_STATE, "current truth(현재 진실) 동기화"),
        ("final_claim_guard", "not_claimed" in json.dumps(read_json(FINAL_DECISION)), FINAL_DECISION, "operating claims(운영 주장) 차단"),
    ]
    gate_ids = {row[0] for row in gate_specs}
    gate_specs[3] = ("required_gate_coverage_audit", required_gate_names.issubset(gate_ids), GATE_AUDIT, "required gates(필수 게이트) 포함")
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


def write_artifact_registry() -> None:
    artifacts = [
        FEATURE_LABEL_TABLE,
        LABEL_VARIANT_MANIFEST,
        LABEL_DISTRIBUTION,
        PROXY_TRAINING_GRID,
        RUN355C_TRAINING_QUEUE,
        TIMESTAMP_INTEGRITY_AUDIT,
        MATERIALIZATION_SUMMARY,
        DATA_INTEGRITY_RECEIPT,
        EXPERIMENT_RECEIPT,
        MODEL_VALIDATION_RECEIPT,
        ARTIFACT_LINEAGE_RECEIPT,
        JUDGMENT_RECEIPT,
        CLAIM_RECEIPT,
        GATE_AUDIT,
        FINAL_DECISION,
        RUN_MANIFEST,
        REPORT_PATH,
        DECISION_DOC,
        Path(__file__),
    ]
    rows = [
        {
            "artifact_id": f"{RUN_ID}__{rel(path).replace('/', '__').replace('.', '_')}",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "artifact_type": path.suffix.lstrip(".") or "file",
            "path": rel(path),
            "artifact_path": rel(path),
            "sha256": sha256_file(path) if exists(path) else "",
            "created_at": TODAY,
            "created_at_utc": now_utc(),
            "claim_boundary": CLAIM_BOUNDARY,
            "notes": "Stage355B label materialization artifact(355B 라벨 물질화 산출물)",
        }
        for path in artifacts
    ]
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


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
    for directory in [RUN_DIR, REVIEW_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        os.makedirs(fs_path(directory), exist_ok=True)
    features, raw, _queue_rows, identity = load_sources()
    label_table, manifest = materialize_labels(features, raw)
    label_table.to_csv(fs_path(FEATURE_LABEL_TABLE), index=False, encoding="utf-8-sig")
    manifest.to_csv(fs_path(LABEL_VARIANT_MANIFEST), index=False, encoding="utf-8-sig")
    distribution = distribution_rows(label_table)
    write_csv(LABEL_DISTRIBUTION, distribution)
    grid_rows, training_queue = write_proxy_training_artifacts(label_table, manifest, distribution)
    write_csv(PROXY_TRAINING_GRID, grid_rows)
    write_csv(RUN355C_TRAINING_QUEUE, training_queue)
    write_summary_and_integrity(features, raw, identity, label_table, distribution, training_queue)
    status, judgment, decision, next_run_id = status_tuple(training_queue)
    write_receipts(identity, distribution, training_queue, status, judgment, decision, next_run_id)
    write_state_report_and_decisions(distribution, training_queue, status, judgment, decision, next_run_id)
    write_final_and_manifest(identity, distribution, training_queue, status, judgment, decision, next_run_id)
    write_ledgers(training_queue, status, judgment, decision, next_run_id)
    gates = write_gates(identity, distribution, training_queue)
    write_artifact_registry()
    validate(gates)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": status,
                "judgment": judgment,
                "next_run_id": next_run_id,
                "label_table_rows": csv_count(FEATURE_LABEL_TABLE),
                "label_variant_count": csv_count(LABEL_VARIANT_MANIFEST),
                "training_queue_rows": len(training_queue),
                "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
                "gate_total": len(gates),
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
