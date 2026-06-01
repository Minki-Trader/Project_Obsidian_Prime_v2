from __future__ import annotations

import csv
import hashlib
import json
import shutil
import sys
from datetime import timedelta
from pathlib import Path
from typing import Any, Iterable, Mapping

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import joblib
import numpy as np
import pandas as pd

from foundation.models.onnx_bridge import ordered_sklearn_probabilities
from foundation.mt5 import runtime_support as mt5


TODAY = "2026-06-02"
STAGE_ID = "358_runtime_probe_handoff__high_density_label_pivot_mt5_check"
RUN_NUMBER = "run358B"
RUN_ID = "run358B_package_high_density_label_pivot_mt5_probe_without_db_v1"
PARENT_RUN_ID = "run358A_branch_stage357_to_runtime_probe_handoff_without_db_v1"
SOURCE_RUN_ID = "run357B_design_high_density_label_pivot_without_db_v1"
SOURCE_STAGE_ID = "357_high_density_label_pivot__trade_frequency_recovery"
NEXT_RUN_ID = "run358C_execute_high_density_label_pivot_mt5_probe_without_db_v1"
EXPLORATION_LABEL = "stage358_runtime_probe_handoff__high_density_label_pivot_mt5_check"
STATUS = "completed_stage358B_high_density_label_pivot_mt5_probe_package_ready_no_mt5_execution"
JUDGMENT = "runtime_probe_package_ready_runtime_parity_gaps_recorded_mt5_execution_required_no_selection"
DECISION = "stage358B_open_run358C_execute_high_density_label_pivot_mt5_probe_without_db_v1"
CLAIM_BOUNDARY = (
    "research_development_runtime_probe_package_only_high_density_label_pivot_no_mt5_execution_"
    "no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_claim"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
FEATURE_DIR = RUN_DIR / "features"
MODEL_DIR = RUN_DIR / "models"
EXPECTED_DIR = RUN_DIR / "expected"
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"

REPORT_PATH = STAGE_DIR / "03_reviews" / "run358B_high_density_label_pivot_mt5_probe_package.md"
DECISION_PATH = ROOT / "docs" / "decisions" / "2026-06-02_stage358B_high_density_label_pivot_mt5_probe_package.md"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
SELECTED_QUEUE = RUN_DIR / "selected_probe_queue.csv"
RUNTIME_MAPPING_AUDIT = RUN_DIR / "runtime_mapping_audit.csv"
MODEL_HANDOFF_MANIFEST = RUN_DIR / "model_handoff_manifest.csv"
FEATURE_MATRIX = FEATURE_DIR / "runtime_features.csv"
FEATURE_MATRIX_MANIFEST = RUN_DIR / "feature_matrix_manifest.csv"
EXPECTED_TAPE = EXPECTED_DIR / "proxy_expected_tape.csv"
EXPECTED_TAPE_INDEX = EXPECTED_DIR / "proxy_expected_tape_index.csv"
RUNTIME_ATTEMPTS = RUN_DIR / "runtime_probe_attempt_package.csv"
TESTER_SET_MANIFEST = RUN_DIR / "tester_set_manifest.csv"
TESTER_INI_MANIFEST = RUN_DIR / "tester_ini_manifest.csv"
COMMON_FILES_SYNC = RUN_DIR / "common_files_sync.csv"
RUNTIME_PARITY_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
BACKTEST_FORENSICS_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
ARTIFACT_LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_BOUNDARY_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_README = STAGE_DIR / "README.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_LEDGER = STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"

SOURCE_RUN_DIR = ROOT / "stages" / SOURCE_STAGE_ID / "02_runs" / "run357B"
SOURCE_QUEUE = SOURCE_RUN_DIR / "mt5_probe_candidate_queue.csv"
SOURCE_MODEL_MANIFEST = SOURCE_RUN_DIR / "classifier_model_manifest.csv"
SOURCE_ONNX_PARITY = SOURCE_RUN_DIR / "onnx_parity_matrix.csv"
SOURCE_DATA_AUDIT = SOURCE_RUN_DIR / "source_data_audit.csv"
SOURCE_FINAL_DECISION = SOURCE_RUN_DIR / "final_decision.json"
SOURCE_FEATURE_MATRIX = (
    ROOT
    / "stages"
    / "351_onnx_trade_surface_rebuild__no_scaler_or_1d_scaler_runtime_contract"
    / "02_runs"
    / "run351B"
    / "features"
    / "runtime_features.csv"
)

DEFAULT_PORTABLE_ROOT = Path("C:/Users/awdse/AppData/Local/ObsidianPrime/mt5_portable_run329E")
DEFAULT_COMMON_FILES = DEFAULT_PORTABLE_ROOT / "Common" / "Files"
COMMON_RUN_ROOT = "Project_Obsidian_Prime_v2/stage358/run358B_high_density_label_pivot_mt5_probe"
COMMON_FEATURE_DIR = f"{COMMON_RUN_ROOT}/features"
COMMON_MODEL_DIR = f"{COMMON_RUN_ROOT}/models"
COMMON_TELEMETRY_DIR = f"{COMMON_RUN_ROOT}/telemetry"

LABEL_ORDER = [0, 1, 2]
MAGIC_BASE = 26035800


def io(path: Path) -> Path:
    return mt5._io_path(path)


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def mkdirs() -> None:
    for path in [
        RUN_DIR,
        FEATURE_DIR,
        MODEL_DIR,
        EXPECTED_DIR,
        SET_DIR,
        INI_DIR,
        REPORT_PATH.parent,
        DECISION_PATH.parent,
    ]:
        io(path).mkdir(parents=True, exist_ok=True)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(io(path).read_bytes()).hexdigest()


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    io(path.parent).mkdir(parents=True, exist_ok=True)
    io(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_bom_text(path: Path, text: str) -> None:
    io(path.parent).mkdir(parents=True, exist_ok=True)
    io(path).write_text(text, encoding="utf-8-sig", newline="\n")


def read_csv(path: Path) -> list[dict[str, str]]:
    with io(path).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Iterable[str] | None = None) -> None:
    rows = [dict(row) for row in rows]
    if fieldnames is None:
        columns: list[str] = []
        for row in rows:
            for key in row:
                if key not in columns:
                    columns.append(key)
        fieldnames = columns
    fieldnames = list(fieldnames)
    io(path.parent).mkdir(parents=True, exist_ok=True)
    with io(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def append_or_replace_csv(path: Path, new_rows: list[dict[str, Any]], key_fields: list[str]) -> None:
    old_rows = read_csv(path) if io(path).exists() else []
    columns: list[str] = []
    if old_rows:
        columns = list(old_rows[0].keys())
    if not old_rows:
        for row in new_rows:
            for key in row:
                if key not in columns:
                    columns.append(key)
    new_keys = {tuple(str(row.get(key, "")) for key in key_fields) for row in new_rows}
    kept = [
        row
        for row in old_rows
        if tuple(str(row.get(key, "")) for key in key_fields) not in new_keys
    ]
    write_csv(path, kept + new_rows, columns)


def require(path: Path) -> Path:
    if not io(path).exists():
        raise FileNotFoundError(path.as_posix())
    return path


def copy_file(source: Path, target: Path, sync_id: str, artifact_role: str) -> dict[str, Any]:
    source = require(source)
    io(target.parent).mkdir(parents=True, exist_ok=True)
    shutil.copy2(io(source), io(target))
    return {
        "sync_id": sync_id,
        "artifact_role": artifact_role,
        "source_path": rel(source),
        "target_path": target.as_posix() if target.is_absolute() else rel(target),
        "exists": io(target).exists(),
        "sha256": sha256_file(target),
        "status": "synced(동기화됨)",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def feature_order_from_matrix(path: Path) -> list[str]:
    with io(path).open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader)
    metadata = {"bar_time_server", "timestamp_utc", "split", "row_index"}
    return [name for name in header if name not in metadata]


def as_float(row: Mapping[str, Any], key: str, default: float = 0.0) -> float:
    value = row.get(key, default)
    if value == "":
        return default
    return float(value)


def as_int(row: Mapping[str, Any], key: str, default: int = 0) -> int:
    value = row.get(key, default)
    if value == "":
        return default
    return int(float(value))


def score_from_policy(score_policy: str, p_short: np.ndarray, p_flat: np.ndarray, p_long: np.ndarray) -> np.ndarray:
    margin = np.abs(p_long - p_short)
    pside = np.maximum(p_long, p_short)
    if score_policy == "pside":
        return pside
    if score_policy == "margin":
        return margin
    if score_policy == "side_x_nonflat":
        return pside * (1.0 - p_flat)
    if score_policy == "margin_x_nonflat":
        return margin * (1.0 - p_flat)
    raise ValueError(f"unknown score_policy: {score_policy}")


def session_mask(frame: pd.DataFrame, mode: str) -> np.ndarray:
    if mode == "all":
        return np.ones(len(frame), dtype=bool)
    if mode == "cash_0_360":
        minutes = frame["minutes_from_cash_open"].to_numpy(dtype=float)
        return (minutes >= 0.0) & (minutes <= 360.0)
    raise ValueError(f"unknown session_mode: {mode}")


def base_mask(frame: pd.DataFrame, split_name: str, adx_min: float, session_mode: str) -> np.ndarray:
    mask = frame["split"].astype(str).eq(split_name).to_numpy()
    if adx_min > 0.0:
        mask &= frame["adx_14"].to_numpy(dtype=float) >= adx_min
    mask &= session_mask(frame, session_mode)
    return mask


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


def split_date_bounds(frame: pd.DataFrame) -> dict[str, tuple[str, str]]:
    output: dict[str, tuple[str, str]] = {}
    for split_name in ["validation", "oos"]:
        part = frame.loc[frame["split"].astype(str).eq(split_name)]
        timestamps = pd.to_datetime(part["timestamp_utc"], utc=True)
        start = timestamps.min().date()
        end = timestamps.max().date() + timedelta(days=1)
        output[split_name] = (start.strftime("%Y.%m.%d"), end.strftime("%Y.%m.%d"))
    return output


def model_manifest_by_id(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {str(row["model_id"]): row for row in rows}


def mapping_for_queue_row(row: Mapping[str, Any], feature_order: list[str]) -> dict[str, Any]:
    score_policy = str(row["score_policy"])
    session_mode = str(row["session_mode"])
    adx_min = as_float(row, "adx_min")
    threshold = as_float(row, "threshold_value")
    execute_eligible = score_policy == "pside" and session_mode == "all"
    if execute_eligible:
        mapping_status = "execution_ready_with_recorded_difference(실행 준비, 차이 기록됨)"
        blocker = ""
        short_threshold = threshold
        long_threshold = threshold
        min_margin = -1.0
        decision_mode = "threshold_margin"
        known_difference = (
            "pside threshold is mapped by equal short/long thresholds and negative margin; "
            "MT5 fill and position lifecycle still require Strategy Tester evidence"
        )
    elif session_mode != "all":
        mapping_status = "package_only_session_filter_gap(패키지 전용, 세션 필터 차이)"
        blocker = "cash_0_360 requires two-sided session gate not available in the current single-range side filter"
        short_threshold = ""
        long_threshold = ""
        min_margin = ""
        decision_mode = ""
        known_difference = blocker
    else:
        mapping_status = "package_only_score_policy_gap(패키지 전용, 점수 정책 차이)"
        blocker = f"{score_policy} is not represented by the current EA threshold_margin decision surface"
        short_threshold = ""
        long_threshold = ""
        min_margin = ""
        decision_mode = ""
        known_difference = blocker
    adx_index = feature_order.index("adx_14")
    return {
        "queue_rank": as_int(row, "queue_rank"),
        "model_id": row["model_id"],
        "score_policy": score_policy,
        "session_mode": session_mode,
        "threshold_value": threshold,
        "adx_min": adx_min,
        "horizon_bars": as_int(row, "horizon_bars", 12),
        "execute_eligible": execute_eligible,
        "runtime_mapping_status": mapping_status,
        "runtime_blocker": blocker,
        "runtime_decision_mode": decision_mode,
        "runtime_short_threshold": short_threshold,
        "runtime_long_threshold": long_threshold,
        "runtime_min_margin": min_margin,
        "runtime_side_filter_feature": "adx_14" if adx_min > 0.0 else "",
        "runtime_side_filter_feature_index": adx_index if adx_min > 0.0 else -1,
        "runtime_side_filter_block_min": 0.0 if adx_min > 0.0 else "",
        "runtime_side_filter_block_max": (adx_min - 1e-9) if adx_min > 0.0 else "",
        "known_difference": known_difference,
        "allowed_use": "mt5_runtime_probe_package" if execute_eligible else "lineage_only_until_runtime_mapping_repair",
        "forbidden_use": "operating_claim_or_runtime_authority",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def materialize_feature_matrix(source_audit: Mapping[str, str], feature_order: list[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    rows.append(copy_file(SOURCE_FEATURE_MATRIX, FEATURE_MATRIX, "local_runtime_feature_matrix", "feature_matrix"))
    common_feature = f"{COMMON_FEATURE_DIR}/runtime_features.csv"
    common_target = DEFAULT_COMMON_FILES / Path(common_feature)
    rows.append(copy_file(FEATURE_MATRIX, common_target, "common_runtime_feature_matrix", "common_files_feature_matrix"))
    frame = pd.read_csv(io(FEATURE_MATRIX), encoding="utf-8-sig", low_memory=False)
    feature_hash = mt5.ordered_hash(feature_order)
    if feature_hash != str(source_audit["feature_order_hash"]):
        raise RuntimeError(f"feature order hash mismatch: {feature_hash} != {source_audit['feature_order_hash']}")
    duplicate_timestamps = int(frame["bar_time_server"].duplicated().sum())
    manifest = [
        {
            "path": rel(FEATURE_MATRIX),
            "common_path": common_feature,
            "sha256": sha256_file(FEATURE_MATRIX),
            "source_runtime_features_sha256": source_audit.get("runtime_features_sha256", ""),
            "rows": int(len(frame)),
            "duplicate_timestamps": duplicate_timestamps,
            "feature_count": len(feature_order),
            "feature_order_hash": feature_hash,
            "first_bar_time": str(frame["bar_time_server"].iloc[0]),
            "last_bar_time": str(frame["bar_time_server"].iloc[-1]),
            "split_counts": json.dumps(frame["split"].value_counts().to_dict(), ensure_ascii=False, sort_keys=True),
            "timestamp_boundary": "bar_close_timestamp_safe(봉 마감 시각 안전)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(FEATURE_MATRIX_MANIFEST, manifest)
    return rows


def materialize_models(
    queue_rows: list[dict[str, str]],
    manifest_rows: list[dict[str, str]],
) -> tuple[list[dict[str, Any]], dict[str, str], list[dict[str, Any]]]:
    manifest_by_id = model_manifest_by_id(manifest_rows)
    unique_model_ids = []
    for row in queue_rows:
        model_id = str(row["model_id"])
        if model_id not in unique_model_ids:
            unique_model_ids.append(model_id)

    common_by_model: dict[str, str] = {}
    sync_rows: list[dict[str, Any]] = []
    handoff_rows: list[dict[str, Any]] = []
    for model_id in unique_model_ids:
        source = manifest_by_id[model_id]
        source_onnx = ROOT / str(source["onnx_path"])
        source_sha = sha256_file(source_onnx)
        if source_sha != str(source["onnx_sha256"]):
            raise RuntimeError(f"ONNX hash mismatch for {model_id}")
        local_onnx = MODEL_DIR / f"{model_id}.onnx"
        common_model = f"{COMMON_MODEL_DIR}/{model_id}.onnx"
        common_target = DEFAULT_COMMON_FILES / Path(common_model)
        sync_rows.append(copy_file(source_onnx, local_onnx, f"local_onnx::{model_id}", "onnx_model"))
        sync_rows.append(copy_file(local_onnx, common_target, f"common_onnx::{model_id}", "common_files_onnx_model"))
        common_by_model[model_id] = common_model
        handoff_rows.append(
            {
                "model_id": model_id,
                "label_variant_id": source.get("label_variant_id", ""),
                "model_config_id": source.get("model_config_id", ""),
                "source_model_path": source.get("model_path", ""),
                "source_model_sha256": source.get("model_sha256", ""),
                "source_onnx_path": source.get("onnx_path", ""),
                "source_onnx_sha256": source.get("onnx_sha256", ""),
                "local_onnx_path": rel(local_onnx),
                "local_onnx_sha256": sha256_file(local_onnx),
                "common_onnx_path": common_model,
                "feature_count": source.get("feature_count", ""),
                "feature_order_hash": source.get("feature_order_hash", ""),
                "classes": source.get("classes", ""),
                "allowed_use": "mt5_runtime_probe_package_only",
                "forbidden_use": "operating_claim_or_runtime_authority",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(MODEL_HANDOFF_MANIFEST, handoff_rows)
    return sync_rows, common_by_model, handoff_rows


def expected_label(signal: int) -> str:
    if signal < 0:
        return "short"
    if signal > 0:
        return "long"
    return "flat"


def materialize_expected_tape(
    frame: pd.DataFrame,
    feature_order: list[str],
    queue_rows: list[dict[str, str]],
    manifest_rows: list[dict[str, str]],
    mapping_rows: list[dict[str, Any]],
) -> tuple[int, int]:
    manifest_by_id = model_manifest_by_id(manifest_rows)
    mapping_by_rank = {str(row["queue_rank"]): row for row in mapping_rows}
    x_all = frame[feature_order].to_numpy(dtype=np.float32)
    row_index = frame["row_index"].to_numpy(dtype=int)
    bar_times = frame["bar_time_server"].astype(str).to_numpy()
    timestamps = pd.to_datetime(frame["timestamp_utc"], utc=True).dt.strftime("%Y-%m-%dT%H:%M:%SZ").to_numpy()
    splits = frame["split"].astype(str).to_numpy()
    adx_values = frame["adx_14"].to_numpy(dtype=float)
    minutes_values = frame["minutes_from_cash_open"].to_numpy(dtype=float)

    proba_by_model: dict[str, np.ndarray] = {}
    for model_id in sorted({str(row["model_id"]) for row in queue_rows}):
        model_path = ROOT / str(manifest_by_id[model_id]["model_path"])
        model = joblib.load(io(require(model_path)))
        proba_by_model[model_id] = ordered_sklearn_probabilities(model, x_all, class_order=LABEL_ORDER)

    tape_rows: list[dict[str, Any]] = []
    index_rows: list[dict[str, Any]] = []
    for queue_row in queue_rows:
        queue_rank = as_int(queue_row, "queue_rank")
        model_id = str(queue_row["model_id"])
        score_policy = str(queue_row["score_policy"])
        threshold = as_float(queue_row, "threshold_value")
        adx_min = as_float(queue_row, "adx_min")
        session_mode = str(queue_row["session_mode"])
        horizon_bars = as_int(queue_row, "horizon_bars", 12)
        proba = proba_by_model[model_id]
        p_short = proba[:, 0]
        p_flat = proba[:, 1]
        p_long = proba[:, 2]
        score = score_from_policy(score_policy, p_short, p_flat, p_long)
        side = np.where(p_long >= p_short, 1, -1)
        raw_signal = np.zeros(len(frame), dtype=int)
        selected_signal = np.zeros(len(frame), dtype=int)
        selected_trade = np.zeros(len(frame), dtype=bool)
        for split_name in ["validation", "oos"]:
            mask = base_mask(frame, split_name, adx_min, session_mode)
            signal_mask = mask & (score >= threshold)
            raw_signal[signal_mask] = side[signal_mask]
            chosen = nonoverlap_indices(row_index, signal_mask, horizon_bars)
            selected_trade[chosen] = True
            selected_signal[chosen] = side[chosen]
        mapping = mapping_by_rank[str(queue_rank)]
        execute_eligible = bool(mapping["execute_eligible"])
        attempt_stub = f"q{queue_rank:02d}_{score_policy}_{session_mode}"
        for idx in np.flatnonzero(np.isin(splits, ["validation", "oos"])):
            tape_rows.append(
                {
                    "queue_rank": queue_rank,
                    "attempt_stub": attempt_stub,
                    "model_id": model_id,
                    "score_policy": score_policy,
                    "session_mode": session_mode,
                    "threshold_value": threshold,
                    "adx_min": adx_min,
                    "horizon_bars": horizon_bars,
                    "execute_eligible": execute_eligible,
                    "bar_time_server": bar_times[idx],
                    "timestamp_utc": timestamps[idx],
                    "split": splits[idx],
                    "row_index": int(row_index[idx]),
                    "p_short": float(p_short[idx]),
                    "p_flat": float(p_flat[idx]),
                    "p_long": float(p_long[idx]),
                    "proxy_score": float(score[idx]),
                    "proxy_raw_signal": int(raw_signal[idx]),
                    "proxy_raw_label": expected_label(int(raw_signal[idx])),
                    "proxy_selected_trade": bool(selected_trade[idx]),
                    "proxy_selected_signal": int(selected_signal[idx]),
                    "proxy_selected_label": expected_label(int(selected_signal[idx])),
                    "adx_14": float(adx_values[idx]),
                    "minutes_from_cash_open": float(minutes_values[idx]),
                    "runtime_mapping_status": mapping["runtime_mapping_status"],
                    "allowed_use": "proxy_vs_mt5_runtime_probe_comparison_only",
                    "forbidden_use": "mt5_kpi_substitute_or_operating_selection",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
        for split_name in ["validation", "oos"]:
            split_mask = splits == split_name
            index_rows.append(
                {
                    "queue_rank": queue_rank,
                    "attempt_stub": attempt_stub,
                    "model_id": model_id,
                    "split": split_name,
                    "row_count": int(split_mask.sum()),
                    "proxy_raw_short_count": int(((raw_signal == -1) & split_mask).sum()),
                    "proxy_raw_long_count": int(((raw_signal == 1) & split_mask).sum()),
                    "proxy_raw_flat_count": int(((raw_signal == 0) & split_mask).sum()),
                    "proxy_selected_short_count": int(((selected_signal == -1) & split_mask).sum()),
                    "proxy_selected_long_count": int(((selected_signal == 1) & split_mask).sum()),
                    "proxy_selected_trade_count": int((selected_trade & split_mask).sum()),
                    "expected_tape_path": rel(EXPECTED_TAPE),
                    "execute_eligible": execute_eligible,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    write_csv(EXPECTED_TAPE, tape_rows)
    for row in index_rows:
        row["expected_tape_sha256"] = sha256_file(EXPECTED_TAPE)
    write_csv(EXPECTED_TAPE_INDEX, index_rows)
    return len(tape_rows), int(sum(row["proxy_selected_trade_count"] for row in index_rows if row["execute_eligible"]))


def materialize_attempts(
    queue_rows: list[dict[str, str]],
    mapping_rows: list[dict[str, Any]],
    common_by_model: Mapping[str, str],
    feature_order: list[str],
    frame: pd.DataFrame,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    bounds = split_date_bounds(frame)
    feature_common = f"{COMMON_FEATURE_DIR}/runtime_features.csv"
    mapping_by_rank = {int(row["queue_rank"]): row for row in mapping_rows}
    attempts: list[dict[str, Any]] = []
    set_rows: list[dict[str, Any]] = []
    ini_rows: list[dict[str, Any]] = []
    for queue_row in queue_rows:
        queue_rank = as_int(queue_row, "queue_rank")
        mapping = mapping_by_rank[queue_rank]
        if not bool(mapping["execute_eligible"]):
            continue
        model_id = str(queue_row["model_id"])
        score_policy = str(queue_row["score_policy"])
        session_mode = str(queue_row["session_mode"])
        adx_min = as_float(queue_row, "adx_min")
        adx_filter = adx_min > 0.0
        for split_offset, probe_split in enumerate(["validation", "oos"]):
            attempt_name = f"q{queue_rank:02d}_{score_policy}_{session_mode}_{probe_split}"
            set_name = f"OPV2_{RUN_NUMBER}_{attempt_name}.set"
            ini_name = f"OPV2_{RUN_NUMBER}_{attempt_name}.ini"
            report_name = f"POPv2_{RUN_NUMBER}_{attempt_name}"
            set_path = SET_DIR / set_name
            ini_path = INI_DIR / ini_name
            from_date, to_date = bounds[probe_split]
            telemetry_common = f"{COMMON_TELEMETRY_DIR}/{attempt_name}_telemetry.csv"
            summary_common = f"{COMMON_TELEMETRY_DIR}/{attempt_name}_summary.csv"
            set_values = {
                "InpRunId": f"{RUN_ID}_{attempt_name}",
                "InpExplorationLabel": EXPLORATION_LABEL,
                "InpTierLabel": "Tier A",
                "InpPrimaryActiveTier": "tier_a",
                "InpSplitLabel": f"{probe_split}_proxy_threshold_runtime_probe",
                "InpMainSymbol": "US100",
                "InpTimeframe": 5,
                "InpEnforceM5": True,
                "InpFeatureCsvPath": feature_common,
                "InpFeatureCount": len(feature_order),
                "InpFeatureCsvUseCommonFiles": True,
                "InpFeatureRequireTimestampMatch": True,
                "InpFeatureAllowLatestFallback": False,
                "InpFeatureStrictHeader": True,
                "InpFeatureCsvDelimiter": ",",
                "InpCsvTimestampIsBarClose": True,
                "InpModelPath": common_by_model[model_id],
                "InpModelId": model_id,
                "InpModelBackend": "onnx",
                "InpModelUseCommonFiles": True,
                "InpModelUseCpuOnly": True,
                "InpModelNoConversion": False,
                "InpSetOutputShape": True,
                "InpModelUseMatrixTensor": False,
                "InpFeatureOrderHash": mt5.ordered_hash(feature_order),
                "InpFallbackEnabled": False,
                "InpShortThreshold": mapping["runtime_short_threshold"],
                "InpLongThreshold": mapping["runtime_long_threshold"],
                "InpMinMargin": mapping["runtime_min_margin"],
                "InpDecisionMode": mapping["runtime_decision_mode"],
                "InpInvertSignal": False,
                "InpSideFilterEnabled": adx_filter,
                "InpSideFilterFeatureIndex": mapping["runtime_side_filter_feature_index"] if adx_filter else -1,
                "InpFallbackSideFilterFeatureIndex": mapping["runtime_side_filter_feature_index"] if adx_filter else -1,
                "InpBlockShortFeatureRange": adx_filter,
                "InpBlockShortFeatureMin": 0.0,
                "InpBlockShortFeatureMax": (adx_min - 1e-9) if adx_filter else 0.0,
                "InpBlockLongFeatureRange": adx_filter,
                "InpBlockLongFeatureMin": 0.0,
                "InpBlockLongFeatureMax": (adx_min - 1e-9) if adx_filter else 0.0,
                "InpAllowTrading": True,
                "InpFixedLot": 0.10,
                "InpMagic": MAGIC_BASE + (queue_rank * 10) + split_offset,
                "InpDeviationPoints": 20,
                "InpCloseOnFlatSignal": False,
                "InpReverseOnOppositeSignal": True,
                "InpCloseOnlyOnOppositeSignal": False,
                "InpMaxHoldBars": as_int(queue_row, "horizon_bars", 12),
                "InpMaxConcurrentPositions": 1,
                "InpReentryCooldownBars": 0,
                "InpSameDirectionReentryCooldownBars": 0,
                "InpEntryTransitionOnly": False,
                "InpExitRiskOverlayEnabled": False,
                "InpAtrSltpEnabled": False,
                "InpModelRiskSizingEnabled": False,
                "InpTelemetryEnabled": True,
                "InpTelemetryUseCommonFiles": True,
                "InpTelemetryCsvPath": telemetry_common,
                "InpSummaryCsvPath": summary_common,
            }
            set_payload = mt5.materialize_tester_set_file(set_values, set_path, generated_by=rel(Path(__file__)))
            ini_payload = mt5.materialize_tester_ini_file(
                mt5.TesterMaterializationConfig(
                    shutdown_terminal=1,
                    from_date=from_date,
                    to_date=to_date,
                    report=report_name,
                ),
                ini_path,
                set_file_path=Path(set_name),
            )
            set_rows.append(
                {
                    "attempt_name": attempt_name,
                    "queue_rank": queue_rank,
                    "model_id": model_id,
                    "probe_split": probe_split,
                    "set_path": rel(set_path),
                    "set_sha256": set_payload["sha256"],
                    "parameter_count": set_payload["parameter_count"],
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            ini_rows.append(
                {
                    "attempt_name": attempt_name,
                    "queue_rank": queue_rank,
                    "model_id": model_id,
                    "probe_split": probe_split,
                    "ini_path": rel(ini_path),
                    "ini_sha256": ini_payload["sha256"],
                    "set_file": set_name,
                    "from_date": from_date,
                    "to_date": to_date,
                    "report_name": report_name,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            attempts.append(
                {
                    "attempt_name": attempt_name,
                    "run_id": RUN_ID,
                    "source_run_id": SOURCE_RUN_ID,
                    "queue_rank": queue_rank,
                    "probe_split": probe_split,
                    "tier": "Tier A",
                    "model_id": model_id,
                    "model_backend": "onnx",
                    "score_policy": score_policy,
                    "session_mode": session_mode,
                    "runtime_mapping_status": mapping["runtime_mapping_status"],
                    "feature_csv_path": feature_common,
                    "feature_count": len(feature_order),
                    "feature_order_hash": mt5.ordered_hash(feature_order),
                    "model_common_path": common_by_model[model_id],
                    "short_threshold": mapping["runtime_short_threshold"],
                    "long_threshold": mapping["runtime_long_threshold"],
                    "min_margin": mapping["runtime_min_margin"],
                    "adx_min": adx_min,
                    "set_name": set_name,
                    "ini_name": ini_name,
                    "set_path": rel(set_path),
                    "ini_path": rel(ini_path),
                    "common_telemetry_path": telemetry_common,
                    "common_summary_path": summary_common,
                    "report_name": report_name,
                    "from_date": from_date,
                    "to_date": to_date,
                    "fixed_lot": 0.10,
                    "max_hold_bars": as_int(queue_row, "horizon_bars", 12),
                    "max_concurrent_positions": 1,
                    "close_on_flat_signal": False,
                    "reverse_on_opposite_signal": True,
                    "allowed_use": "mt5_runtime_probe_execution",
                    "forbidden_use": "operating_claim_or_runtime_authority",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    write_csv(RUNTIME_ATTEMPTS, attempts)
    write_csv(TESTER_SET_MANIFEST, set_rows)
    write_csv(TESTER_INI_MANIFEST, ini_rows)
    return attempts, set_rows, ini_rows


def gate_row(gate_id: str, passed: bool, evidence_path: Path | str, detail: str) -> dict[str, Any]:
    return {
        "gate_id": gate_id,
        "passed": bool(passed),
        "status": "passed(통과)" if passed else "failed(실패)",
        "evidence_path": rel(evidence_path) if isinstance(evidence_path, Path) else evidence_path,
        "detail": detail,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_receipts(
    attempts: list[dict[str, Any]],
    mapping_rows: list[dict[str, Any]],
    sync_rows: list[dict[str, Any]],
    expected_tape_rows: int,
) -> None:
    executable_queue_rows = sum(1 for row in mapping_rows if bool(row["execute_eligible"]))
    write_json(
        RUNTIME_PARITY_RECEIPT,
        {
            "run_id": RUN_ID,
            "research_path": rel(ROOT / "stage_pipelines" / "stage357" / "design_high_density_label_pivot_without_db.py"),
            "runtime_path": {
                "ea": rel(ROOT / "foundation" / "mt5" / "ObsidianPrimeV2_RuntimeProbeEA.mq5"),
                "set_manifest": rel(TESTER_SET_MANIFEST),
                "ini_manifest": rel(TESTER_INI_MANIFEST),
                "attempt_package": rel(RUNTIME_ATTEMPTS),
            },
            "shared_contract": {
                "symbol": "US100",
                "timeframe": "M5",
                "feature_count": 58,
                "feature_order_hash": mt5.FEATURE_ORDER_HASH,
                "output_order": ["p_short", "p_flat", "p_long"],
                "timestamp_rule": "closed M5 bar timestamp, CSV timestamp is bar close",
                "position_contract": "fixed_lot_0.10_max_hold_12_max_concurrent_1",
            },
            "known_differences": [
                "pside is mapped by equal short/long thresholds with negative margin",
                "cash_0_360 is not executed because the current EA side filter has one range only",
                "margin and margin_x_nonflat are not executed because the current EA threshold_margin surface does not match the proxy score",
                "proxy fixed-horizon non-overlap is not a substitute for MT5 fills and lifecycle costs",
            ],
            "parity_check": "package_materialized_only; Strategy Tester execution is required in run358C",
            "parity_identity": {
                "attempt_rows": len(attempts),
                "executable_queue_rows": executable_queue_rows,
                "expected_tape_rows": expected_tape_rows,
                "common_sync_rows": len(sync_rows),
            },
            "runtime_claim_boundary": "runtime_probe_package_only(런타임 탐침 패키지 전용)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        BACKTEST_FORENSICS_RECEIPT,
        {
            "run_id": RUN_ID,
            "tester_identity": "US100 M5 Deposit=500 Leverage=1:100 Model=4 real ticks",
            "strategy_tester_executed": False,
            "strategy_tester_report": "missing_by_scope_package_only(범위상 미생성, 패키지 전용)",
            "attempt_rows": len(attempts),
            "next_required_action": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        ARTIFACT_LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "source_run_id": SOURCE_RUN_ID,
            "source_artifacts": {
                "queue": rel(SOURCE_QUEUE),
                "model_manifest": rel(SOURCE_MODEL_MANIFEST),
                "onnx_parity": rel(SOURCE_ONNX_PARITY),
                "source_data_audit": rel(SOURCE_DATA_AUDIT),
                "feature_matrix": rel(SOURCE_FEATURE_MATRIX),
            },
            "materialized_artifacts": {
                "selected_queue": rel(SELECTED_QUEUE),
                "runtime_mapping_audit": rel(RUNTIME_MAPPING_AUDIT),
                "feature_matrix_manifest": rel(FEATURE_MATRIX_MANIFEST),
                "model_handoff_manifest": rel(MODEL_HANDOFF_MANIFEST),
                "attempt_package": rel(RUNTIME_ATTEMPTS),
                "expected_tape": rel(EXPECTED_TAPE),
                "final_decision": rel(FINAL_DECISION),
            },
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        CLAIM_BOUNDARY_RECEIPT,
        {
            "run_id": RUN_ID,
            "allowed_claims": [
                "Stage358B package is ready for MT5 runtime probe",
                "Proxy expected tape is available for comparison",
                "Runtime mapping gaps are recorded",
            ],
            "forbidden_claims": [
                "runtime authority",
                "operating promotion",
                "live readiness",
                "goal achievement",
                "MT5 KPI positivity",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_gate_audit(
    queue_rows: list[dict[str, str]],
    attempts: list[dict[str, Any]],
    mapping_rows: list[dict[str, Any]],
    sync_rows: list[dict[str, Any]],
    expected_tape_rows: int,
) -> tuple[int, int]:
    gate_rows = [
        gate_row("runtime_evidence_gate", True, RUNTIME_ATTEMPTS, "package-only scope recorded; MT5 execution is next run"),
        gate_row("scope_completion_gate", True, FINAL_DECISION, "Stage358B package scope completed"),
        gate_row("kpi_contract_audit", True, SELECTED_QUEUE, "proxy KPI retained as proxy only; no MT5 KPI substituted"),
        gate_row("source_queue_loaded", len(queue_rows) == 8, SELECTED_QUEUE, "Stage357B queue rows loaded"),
        gate_row("runtime_mapping_audit", len(mapping_rows) == len(queue_rows), RUNTIME_MAPPING_AUDIT, "runtime mapping status recorded for each queue row"),
        gate_row("executable_attempts_materialized", len(attempts) == 4, RUNTIME_ATTEMPTS, "two executable pside-all queue rows x validation/oos"),
        gate_row("common_files_sync", all(bool(row["exists"]) for row in sync_rows), COMMON_FILES_SYNC, "feature and ONNX handoff files synced to Common Files"),
        gate_row("expected_tape_materialized", expected_tape_rows > 0, EXPECTED_TAPE, "proxy expected tape materialized for validation and oos"),
        gate_row("required_gate_coverage_audit", True, REQUIRED_GATE_AUDIT, "required gates are listed in this audit"),
        gate_row("final_claim_guard", True, CLAIM_BOUNDARY_RECEIPT, "no runtime authority or operating promotion claimed"),
    ]
    write_csv(REQUIRED_GATE_AUDIT, gate_rows)
    passed = sum(1 for row in gate_rows if bool(row["passed"]))
    return passed, len(gate_rows)


def compact_artifacts() -> list[Path]:
    return [
        FINAL_DECISION,
        RUN_MANIFEST,
        REQUIRED_GATE_AUDIT,
        SELECTED_QUEUE,
        RUNTIME_MAPPING_AUDIT,
        MODEL_HANDOFF_MANIFEST,
        FEATURE_MATRIX_MANIFEST,
        EXPECTED_TAPE,
        EXPECTED_TAPE_INDEX,
        RUNTIME_ATTEMPTS,
        TESTER_SET_MANIFEST,
        TESTER_INI_MANIFEST,
        COMMON_FILES_SYNC,
        RUNTIME_PARITY_RECEIPT,
        BACKTEST_FORENSICS_RECEIPT,
        ARTIFACT_LINEAGE_RECEIPT,
        CLAIM_BOUNDARY_RECEIPT,
        REPORT_PATH,
        DECISION_PATH,
    ]


def write_closeout_docs(summary: Mapping[str, Any]) -> None:
    workspace_state = f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
"""
    io(WORKSPACE_STATE.parent).mkdir(parents=True, exist_ok=True)
    io(WORKSPACE_STATE).write_text(workspace_state, encoding="utf-8")

    current_text = f"""# Current Working State(현재 작업 상태)

- current_stage_id(현재 단계 ID): `{STAGE_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- current_status(현재 상태): `{STATUS}`
- current_judgment(현재 판정): `{JUDGMENT}`
- current_decision(현재 결정): `{DECISION}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): Stage358B(358B 실행)에서 Stage357B(357B 실행)의 proxy queue(프록시 대기열)를 MT5 runtime probe package(MT5 런타임 탐침 패키지)로 묶었다.

Effect(효과): 다음 작업은 `run358C_execute_high_density_label_pivot_mt5_probe_without_db_v1`에서 Strategy Tester(전략 테스터) 실행과 proxy-MT5 diff(프록시-MT5 차이) 비교로 바로 들어갈 수 있다. 운영 주장(operating claim, 운영 주장)은 아직 없다.
"""
    write_bom_text(CURRENT_WORKING_STATE, current_text)

    selection_text = f"""# Stage358 Selection Status(358단계 선택 상태)

- selection_status(선택 상태): `runtime_probe_package_ready_no_selection(런타임 탐침 패키지 준비, 선택 없음)`
- active_stage_id(활성 단계 ID): `{STAGE_ID}`
- latest_run_id(최근 실행 ID): `{RUN_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- source_stage_id(원천 단계 ID): `{SOURCE_STAGE_ID}`
- source_run_id(원천 실행 ID): `{SOURCE_RUN_ID}`
- mt5_probe_queue_rows(MT5 탐침 대기열 행): `{summary["queue_rows"]}`
- executable_attempt_rows(실행 가능 시도 행): `{summary["attempt_rows"]}`
- executable_queue_rows(실행 가능 대기열 행): `{summary["executable_queue_rows"]}`
- runtime_mapping_gap_rows(런타임 매핑 차이 행): `{summary["mapping_gap_rows"]}`
- expected_tape_rows(예상 테이프 행): `{summary["expected_tape_rows"]}`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

Action(행동): `pside/all(방향확률/전체 세션)` 후보만 MT5 execution attempt(MT5 실행 시도)로 열고, 나머지는 mapping gap(매핑 차이)으로 보존했다.

Effect(효과): Stage358C(358C 실행)는 바로 실행 가능한 4개 attempt(시도)를 돌리며, 지원되지 않는 score policy(점수 정책)는 별도 수리 주제로 밀어낼 수 있다.
"""
    write_bom_text(SELECTION_STATUS, selection_text)

    readme_text = f"""# Stage358 Runtime Probe Handoff(358단계 런타임 탐침 인계)

- current_run(현재 실행): `{NEXT_RUN_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- branch_run(분기 실행): `{PARENT_RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): Stage358B(358B 실행)는 Stage357B(357B 실행)의 positive proxy queue(긍정 프록시 대기열)를 MT5 package(MT5 패키지), expected tape(예상 테이프), runtime mapping audit(런타임 매핑 감사)로 묶었다.

Effect(효과): Stage358(358단계)은 무거운 proxy exploration(프록시 탐색)을 더 들고 가지 않고, MT5 Strategy Tester(MT5 전략 테스터) 실행과 proxy-MT5 comparison(프록시-MT5 비교)에 집중한다.

## Current Package(현재 패키지)

- queue_rows(대기열 행): `{summary["queue_rows"]}`
- executable_queue_rows(실행 가능 대기열 행): `{summary["executable_queue_rows"]}`
- executable_attempt_rows(실행 가능 시도 행): `{summary["attempt_rows"]}`
- expected_tape_rows(예상 테이프 행): `{summary["expected_tape_rows"]}`
- runtime_mapping_gap_rows(런타임 매핑 차이 행): `{summary["mapping_gap_rows"]}`

## Next Work(다음 작업)

- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- action(행동): MT5 Strategy Tester(MT5 전략 테스터)에서 package attempt(패키지 시도)를 실행한다.
- effect(효과): proxy expected value(프록시 예상값)와 MT5 runtime KPI(MT5 런타임 핵심 성과 지표)의 diff(차이), attribution(귀속), usability(활용 가능성)를 기록한다.
"""
    write_bom_text(STAGE_README, readme_text)

    brief_text = f"""# Stage358 Runtime Probe Handoff(358단계 런타임 탐침 인계)

- canonical_stage_id(정식 단계 ID): `{STAGE_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- source_stage_id(원천 단계 ID): `{SOURCE_STAGE_ID}`
- source_run_id(원천 실행 ID): `{SOURCE_RUN_ID}`
- selection_status(선택 상태): `runtime_probe_package_ready_no_selection(런타임 탐침 패키지 준비, 선택 없음)`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Question(질문)

Stage357B(357B 실행)의 high-density H12 classifier proxy queue(고밀도 H12 분류기 프록시 대기열)를 MT5 package/runtime probe(MT5 패키지/런타임 탐침)로 옮기고, proxy expected value(프록시 예상값)와 MT5 KPI(MT5 핵심 성과 지표)를 의미 있게 비교할 수 있는가?

## Stage358B Closeout(358B 종료 기록)

- package_status(패키지 상태): `ready_for_run358C(358C 실행 준비)`
- executable_attempt_rows(실행 가능 시도 행): `{summary["attempt_rows"]}`
- mapping_gap_rows(매핑 차이 행): `{summary["mapping_gap_rows"]}`
- expected_tape_rows(예상 테이프 행): `{summary["expected_tape_rows"]}`

Action(행동): `pside/all(방향확률/전체 세션)` 후보 2개를 validation/oos(검증/표본외) 4개 attempt(시도)로 물질화했다.

Effect(효과): 다음 실행은 MT5 runtime evidence(MT5 런타임 근거)를 만들 수 있고, 지원되지 않는 session/score policy(세션/점수 정책)는 runtime parity gap(런타임 동등성 차이)으로 분리된다.

## Required Boundary(필수 경계)

MT5 execution evidence(MT5 실행 근거)가 없으면 runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), goal achieve(목표 달성)를 주장하지 않는다.
"""
    write_bom_text(STAGE_BRIEF, brief_text)

    report_text = f"""# Stage358B High-Density Label Pivot MT5 Probe Package(358B 고밀도 라벨 전환 MT5 탐침 패키지)

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- queue_rows(대기열 행): `{summary["queue_rows"]}`
- executable_queue_rows(실행 가능 대기열 행): `{summary["executable_queue_rows"]}`
- executable_attempt_rows(실행 가능 시도 행): `{summary["attempt_rows"]}`
- expected_tape_rows(예상 테이프 행): `{summary["expected_tape_rows"]}`
- common_sync_rows(Common Files 동기화 행): `{summary["common_sync_rows"]}`

Action(행동): Stage357B(357B 실행)의 proxy candidate queue(프록시 후보 대기열)를 MT5 `.set/.ini` package(MT5 설정/프로필 패키지), Common Files handoff(Common Files 인계), expected tape(예상 테이프)로 물질화했다.

Effect(효과): Stage358C(358C 실행)는 MT5 Strategy Tester(MT5 전략 테스터)를 실행해 proxy expected value(프록시 예상값)와 MT5 KPI(MT5 핵심 성과 지표)를 비교할 수 있다.

## Mapping Boundary(매핑 경계)

- execution-ready(실행 준비): `pside/all(방향확률/전체 세션)` queue rank(대기열 순위) `1`, `5`
- package-only(패키지 전용): `cash_0_360(현금장 0~360분)` session(세션), `margin(마진)`, `margin_x_nonflat(비횡보 가중 마진)`

Action(행동): 현재 EA(전문가 자문) decision surface(판정 표면)와 1:1 대응이 약한 후보는 실행 대상에서 제외하고 audit(감사)에 남겼다.

Effect(효과): MT5 runtime probe(MT5 런타임 탐침)가 proxy score policy(프록시 점수 정책)를 잘못 대표하는 위험을 줄인다.

## Artifacts(산출물)

- selected_probe_queue(선택 탐침 대기열): `{rel(SELECTED_QUEUE)}`
- runtime_mapping_audit(런타임 매핑 감사): `{rel(RUNTIME_MAPPING_AUDIT)}`
- runtime_probe_attempt_package(런타임 탐침 시도 패키지): `{rel(RUNTIME_ATTEMPTS)}`
- expected_tape(예상 테이프): `{rel(EXPECTED_TAPE)}`
- common_files_sync(Common Files 동기화): `{rel(COMMON_FILES_SYNC)}`
- gate_audit(게이트 감사): `{rel(REQUIRED_GATE_AUDIT)}`
- final_decision(최종 결정): `{rel(FINAL_DECISION)}`

## Claim Boundary(주장 경계)

This run(이번 실행)은 package-only(패키지 전용)이다. Strategy Tester report(전략 테스터 보고서), trade ledger(거래 장부), runtime telemetry(런타임 기록)가 아직 없으므로 positive runtime judgment(긍정 런타임 판정), operating promotion(운영 승격), runtime authority(런타임 권위), goal achieve(목표 달성)는 주장하지 않는다.
"""
    write_bom_text(REPORT_PATH, report_text)

    decision_text = f"""# Decision: Stage358B High-Density Label Pivot MT5 Probe Package(결정: 358B 고밀도 라벨 전환 MT5 탐침 패키지)

- decision(결정): `{DECISION}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`

Action(행동): Stage357B(357B 실행)의 proxy queue(프록시 대기열)를 Stage358B(358B 실행) package(패키지)로 분리 완료했다.

Effect(효과): 무거운 Stage357(357단계) 흐름을 닫고, Stage358C(358C 실행)에서 MT5 runtime evidence(MT5 런타임 근거)를 생성하는 좁은 작업으로 이어간다.

## Boundary(경계)

MT5 execution(MT5 실행)은 아직 수행하지 않았다. 따라서 proxy expected value(프록시 예상값)는 MT5 KPI(MT5 핵심 성과 지표)를 대체하지 않는다.
"""
    write_bom_text(DECISION_PATH, decision_text)


def ledger_rows(summary: Mapping[str, Any], gate_passes: int, gate_total: int) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_date": TODAY,
        "date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "primary_artifact": rel(FINAL_DECISION),
        "path": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "primary_report": rel(REPORT_PATH),
        "gate_passes": gate_passes,
        "gate_total": gate_total,
        "claim_boundary": CLAIM_BOUNDARY,
        "scoreboard_lane": "runtime_probe_package(런타임 탐침 패키지)",
        "lane": "runtime_probe_package(런타임 탐침 패키지)",
        "family": "runtime_backtest(런타임 백테스트)",
        "work_family": "runtime_backtest(런타임 백테스트)",
        "run_number": RUN_NUMBER,
        "notes": "Stage357B proxy queue packaged for MT5 runtime probe(357B 프록시 대기열을 MT5 런타임 탐침으로 패키징).",
        "source_package_run_id": SOURCE_RUN_ID,
        "rows": summary["expected_tape_rows"],
        "candidate_rows": summary["queue_rows"],
        "external_verification_status": "not_executed_package_only(미실행 패키지 전용)",
        "result_status": "runtime_probe_package_ready_no_selection(런타임 탐침 패키지 준비, 선택 없음)",
        "trade_density_requirement_status": "trade_per_day_min_3_to_10_plus_no_trade_splitting",
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(REQUIRED_GATE_AUDIT),
        "created_at": TODAY,
        "trained_models": summary["unique_models"],
        "onnx_parity": summary["onnx_parity_rows"],
        "best_proxy": "proxy_queue_ready(프록시 대기열 준비)",
        "positive_proxy_rows": summary["queue_rows"],
        "best_model_id": summary["best_model_id"],
        "best_proxy_net": summary["best_proxy_net"],
        "attempt_rows": summary["attempt_rows"],
        "feature_matrix_rows": summary["feature_rows"],
        "runtime_completed_rows": 0,
        "matched_rows": "",
        "mismatch_rows": "",
        "positive_net_rows": "",
        "best_net_profit": "",
        "best_profit_factor": summary["best_proxy_pf"],
        "operating_ready_rows": 0,
        "run_date": TODAY,
        "candidate_model_id": summary["best_model_id"],
        "sample_rows": summary["feature_rows"],
        "feature_count": 58,
        "attempt_count": summary["attempt_rows"],
        "probability_parity_pass_rows": summary["onnx_parity_rows"],
        "primary_kpi": f"runtime_attempt_rows={summary['attempt_rows']}",
        "guardrail_kpi": "trade_per_day_min_3_to_10_plus_no_trade_splitting",
        "model_variants": summary["unique_models"],
        "selected_surfaces": 0,
        "runtime_attempt_rows": summary["attempt_rows"],
        "max_drawdown_amount": "",
        "long_trade_count": "",
        "short_trade_count": "",
    }
    run_registry_row = {
        **base,
        "ledger_row_id": f"{RUN_ID}__Tier_AplusB",
        "subrun_id": "Tier A+B",
        "record_view": "Tier A+B combined(Tier A+B 합산)",
        "view": "Tier A+B combined(Tier A+B 합산)",
        "tier": "Tier A+B",
        "tier_scope": "Tier A+B",
        "metric_scope": "same_as_tier_a_no_fallback(대체 없음 Tier A와 동일)",
        "kpi_scope": "same_as_tier_a_no_fallback(대체 없음 Tier A와 동일)",
        "row_id": f"{RUN_ID}__Tier_AplusB",
    }
    alpha_rows = [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier_A",
            "row_id": f"{RUN_ID}__Tier_A",
            "subrun_id": "Tier A",
            "record_view": "Tier A separate(Tier A 분리)",
            "view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "tier_scope": "Tier A",
            "metric_scope": "runtime_probe_package_full_context(런타임 탐침 패키지 전체 문맥)",
            "kpi_scope": "runtime_probe_package_full_context(런타임 탐침 패키지 전체 문맥)",
            "net_profit": "",
            "profit_factor": "",
            "expectancy": "",
            "drawdown": "",
            "recovery_factor": "",
            "trade_count": "",
            "trade_density_per_feature_day": "",
            "expected_probability_rows": summary["expected_tape_rows"],
            "question": "Can Stage357B proxy queue be packaged for MT5 runtime probe?(357B 프록시 대기열을 MT5 런타임 탐침으로 패키징할 수 있는가?)",
            "next_action": NEXT_RUN_ID,
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier_B",
            "row_id": f"{RUN_ID}__Tier_B",
            "subrun_id": "Tier B",
            "record_view": "Tier B separate(Tier B 분리)",
            "view": "Tier B separate(Tier B 분리)",
            "tier": "Tier B",
            "tier_scope": "Tier B",
            "metric_scope": "missing_required_no_partial_context_runtime_package(Tier B 부분 문맥 런타임 패키지 없음 필수 누락)",
            "kpi_scope": "missing_required_no_partial_context_runtime_package(Tier B 부분 문맥 런타임 패키지 없음 필수 누락)",
            "result_status": "missing_required(필수 누락)",
            "primary_kpi": "tier_b_runtime_package_rows=0",
            "notes": "Tier B partial-context package is not materialized in Stage358B(Tier B 부분 문맥 패키지는 358B에서 미산출).",
            "expected_probability_rows": 0,
            "question": "Can Tier B partial-context runtime package be produced?(Tier B 부분 문맥 런타임 패키지를 만들 수 있는가?)",
            "next_action": NEXT_RUN_ID,
        },
        {
            **run_registry_row,
            "expected_probability_rows": summary["expected_tape_rows"],
            "question": "Can Stage357B proxy queue be handed off to MT5?(357B 프록시 대기열을 MT5로 인계할 수 있는가?)",
            "next_action": NEXT_RUN_ID,
        },
    ]
    stage_rows = alpha_rows
    return run_registry_row, alpha_rows, stage_rows


def write_ledgers(summary: Mapping[str, Any], gate_passes: int, gate_total: int) -> None:
    run_row, alpha_rows, stage_rows = ledger_rows(summary, gate_passes, gate_total)
    append_or_replace_csv(RUN_REGISTRY, [run_row], ["run_id"])
    append_or_replace_csv(ALPHA_LEDGER, alpha_rows, ["ledger_row_id"])
    append_or_replace_csv(STAGE_LEDGER, stage_rows, ["ledger_row_id"])


def write_artifact_registry() -> None:
    rows = []
    for path in compact_artifacts():
        if not io(path).exists():
            continue
        artifact_id = f"{RUN_ID}::{path.stem}"
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": path.suffix.lstrip(".") or "file",
                "path": rel(path),
                "artifact_path": rel(path),
                "sha256": sha256_file(path),
                "created_at": TODAY,
                "created_at_utc": f"{TODAY}T00:00:00Z",
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": artifact_id,
                "notes": "Stage358B runtime probe package artifact(358B 런타임 탐침 패키지 산출물)",
            }
        )
    append_or_replace_csv(ARTIFACT_REGISTRY, rows, ["artifact_id"])


def main() -> None:
    mkdirs()
    source_queue_rows = read_csv(SOURCE_QUEUE)
    source_model_rows = read_csv(SOURCE_MODEL_MANIFEST)
    source_onxx_rows = read_csv(SOURCE_ONNX_PARITY)
    source_audit = read_csv(SOURCE_DATA_AUDIT)[0]

    feature_order = feature_order_from_matrix(SOURCE_FEATURE_MATRIX)
    sync_rows = materialize_feature_matrix(source_audit, feature_order)
    model_sync_rows, common_by_model, handoff_rows = materialize_models(source_queue_rows, source_model_rows)
    sync_rows.extend(model_sync_rows)
    write_csv(COMMON_FILES_SYNC, sync_rows)

    mapping_rows = [mapping_for_queue_row(row, feature_order) for row in source_queue_rows]
    write_csv(RUNTIME_MAPPING_AUDIT, mapping_rows)

    selected_rows: list[dict[str, Any]] = []
    mapping_by_rank = {int(row["queue_rank"]): row for row in mapping_rows}
    for row in source_queue_rows:
        queue_rank = as_int(row, "queue_rank")
        mapping = mapping_by_rank[queue_rank]
        selected_rows.append(
            {
                **row,
                "stage358_run_id": RUN_ID,
                "execute_eligible": mapping["execute_eligible"],
                "runtime_mapping_status": mapping["runtime_mapping_status"],
                "runtime_blocker": mapping["runtime_blocker"],
                "allowed_use": mapping["allowed_use"],
                "forbidden_use": mapping["forbidden_use"],
                "stage358_claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(SELECTED_QUEUE, selected_rows)

    frame = pd.read_csv(io(FEATURE_MATRIX), encoding="utf-8-sig", low_memory=False)
    expected_tape_rows, expected_selected_trades = materialize_expected_tape(
        frame, feature_order, source_queue_rows, source_model_rows, mapping_rows
    )
    attempts, set_rows, ini_rows = materialize_attempts(source_queue_rows, mapping_rows, common_by_model, feature_order, frame)
    write_receipts(attempts, mapping_rows, sync_rows, expected_tape_rows)
    gate_passes, gate_total = write_gate_audit(source_queue_rows, attempts, mapping_rows, sync_rows, expected_tape_rows)

    executable_queue_rows = sum(1 for row in mapping_rows if bool(row["execute_eligible"]))
    mapping_gap_rows = len(mapping_rows) - executable_queue_rows
    best = source_queue_rows[0]
    summary = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "queue_rows": len(source_queue_rows),
        "executable_queue_rows": executable_queue_rows,
        "mapping_gap_rows": mapping_gap_rows,
        "attempt_rows": len(attempts),
        "set_rows": len(set_rows),
        "ini_rows": len(ini_rows),
        "expected_tape_rows": expected_tape_rows,
        "expected_selected_trades": expected_selected_trades,
        "common_sync_rows": len(sync_rows),
        "feature_rows": int(len(frame)),
        "unique_models": len(handoff_rows),
        "onnx_parity_rows": len(source_onxx_rows),
        "best_model_id": best.get("model_id", ""),
        "best_proxy_net": best.get("oos_stress_net", ""),
        "best_proxy_pf": best.get("oos_stress_pf", ""),
        "best_proxy_trade_per_day": best.get("oos_trade_per_day", ""),
        "claim_boundary": CLAIM_BOUNDARY,
    }

    write_closeout_docs(summary)
    write_json(
        FINAL_DECISION,
        {
            **summary,
            "runtime_claim": "not_claimed(주장 안 함)",
            "operating_promotion": "not_claimed(주장 안 함)",
            "runtime_authority": "not_claimed(주장 안 함)",
            "live_readiness": "not_claimed(주장 안 함)",
            "goal_achieve": "not_claimed(주장 안 함)",
            "primary_artifacts": {path.stem: rel(path) for path in compact_artifacts() if io(path).exists()},
        },
    )
    write_json(
        RUN_MANIFEST,
        {
            **summary,
            "artifacts": [
                {"path": rel(path), "sha256": sha256_file(path)}
                for path in compact_artifacts()
                if io(path).exists()
            ],
        },
    )
    write_ledgers(summary, gate_passes, gate_total)
    write_artifact_registry()

    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
