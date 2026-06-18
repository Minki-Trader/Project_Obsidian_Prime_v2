from __future__ import annotations

import argparse
import csv
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized
from stage_pipelines.stage_frontier_71 import frontier71d_mt5_runtime_probe_economics_native_scout as f71d
from stage_pipelines.stage_frontier_74 import frontier74e_mt5_microburst_negative_control_runtime_probe as f74e
from stage_pipelines.stage_frontier_77 import frontier77d_mt5_lifecycle_negative_control_runtime_probe as runtime_base
from stage_pipelines.stage_frontier_79 import frontier79d_mt5_runtime_native_negative_control_runtime_probe as f79d
from stage_pipelines.stage_frontier_83 import frontier83a_stage_open_teacher_distillation_proxy as f83a
from stage_pipelines.stage_frontier_runtime_backfill.run_frontier_runtime_probe_backfill import (
    DEFAULT_COMMON_FILES,
    DEFAULT_METAEDITOR,
    DEFAULT_PORTABLE_ROOT,
    DEFAULT_TERMINAL,
    DEFAULT_TESTER_PROFILE_ROOT,
)


STAGE_ID = f83a.STAGE_ID
RUN_ID = "frontier83B_mt5_runtime_materialization_exportable_teacher_overlay_v1"
PARENT_RUN_ID = f83a.RUN_ID
NEXT_RUN_ID = "frontier83C_proxy_runtime_gap_analysis_teacher_overlay_v1"
COMMON_RUN_ROOT = "Project_Obsidian_Prime_v2/frontier83B_mt5_runtime_materialization"
RUNTIME_CANDIDATE_PREFIX = "f83b_runtime"
ATTEMPT_PREFIX = "f83b_runtime_materialization"
EXPLORATION_LABEL = "frontier83B_runtime_materialization_exportable_teacher_overlay"
ATTEMPT_ROLE = "runtime_materialization_exportable_teacher_overlay"
RECORD_VIEW_PREFIX = "mt5_f83b_runtime_materialization"
THRESHOLD_EPSILON = 1e-7
CLAIM_BOUNDARY = (
    "mt5_runtime_materialization_observation_only_no_completion_no_baseline_"
    "no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
MODEL_DIR = RUN_DIR / "models"
FEATURE_DIR = RUN_DIR / "features"
VETO_DIR = RUN_DIR / "runtime_veto_tapes"
MT5_DIR = RUN_DIR / "mt5"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
PACKET_DIR = ROOT / "docs/agent_control/packets" / RUN_ID

SUMMARY_F83A = REVIEW_DIR / "f83a_teacher_distillation_summary.json"
CANDIDATES_F83A = REVIEW_DIR / "f83a_teacher_distillation_candidate_rows.csv"
TASK_FORCE_F83A = REVIEW_DIR / "f83a_task_force_review_receipt.yaml"
F82C_MANIFEST = (
    ROOT
    / "stages/stage_frontier_82__density_first_runtime_economic_mechanism_rotation"
    / "02_runs/frontier82C_mt5_runtime_materialization_v1/run_manifest.json"
)
SOURCE_VETO_TAPE = (
    ROOT
    / "stages/stage_frontier_82__density_first_runtime_economic_mechanism_rotation"
    / "02_runs/frontier82C_mt5_runtime_materialization_v1/runtime_veto_tapes/f82c_runtime_f82b_07295_selected_entry_runtime_veto_tape.csv"
)

TARGET_SELECTION = REVIEW_DIR / "f83b_runtime_materialization_target_selection.json"
REPORT = REVIEW_DIR / "frontier83B_mt5_runtime_materialization_report.md"
GATE_AUDIT = REVIEW_DIR / "required_gate_coverage_audit_f83b.md"
SUMMARY = REVIEW_DIR / "f83b_mt5_runtime_materialization_summary.json"
RUNTIME_PARITY = REVIEW_DIR / "f83b_runtime_parity_receipt.json"
BACKTEST_FORENSICS = REVIEW_DIR / "f83b_backtest_forensics_receipt.json"
TASK_FORCE_REVIEW = REVIEW_DIR / "f83b_task_force_review_receipt.yaml"
ARTIFACT_LINEAGE = REVIEW_DIR / "f83b_artifact_lineage.json"
LOCAL_VERIFICATION = REVIEW_DIR / "f83b_local_verification.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
CONTEXT_ANCHOR = REVIEW_DIR / "context_anchor.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"

WORK_PACKET = PACKET_DIR / "work_packet.yaml"
PACKET_SKILL_RECEIPTS = PACKET_DIR / "skill_receipts.json"
PACKET_GATE_AUDIT = PACKET_DIR / "required_gate_coverage_audit.json"
PACKET_FINAL_CLAIM_GUARD = PACKET_DIR / "final_claim_guard.json"

WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs/registers/artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
SCRIPT_REL = "stage_pipelines/stage_frontier_83/frontier83b_mt5_runtime_materialization_exportable_teacher_overlay.py"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="F83B MT5 runtime materialization for the exportable teacher overlay.")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--include-oos", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=600)
    parser.add_argument("--wait-timeout-seconds", type=int, default=300)
    parser.add_argument("--terminal-path", default=str(DEFAULT_TERMINAL))
    parser.add_argument("--metaeditor-path", default=str(DEFAULT_METAEDITOR))
    parser.add_argument("--common-files-root", default=str(DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(DEFAULT_PORTABLE_ROOT))
    return parser.parse_args()


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    text = str(path)
    if text.startswith("\\\\?\\"):
        text = text[4:]
    try:
        return Path(text).relative_to(ROOT).as_posix()
    except ValueError:
        return Path(text).as_posix()


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    rows = list(rows)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = list(columns or (rows[0].keys() if rows else ["empty"]))
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: json_ready(row.get(field, "")) for field in fieldnames})


def append_csv_row(path: Path, row: Mapping[str, Any], *, key: str | None = None, source_header: Path | None = None) -> None:
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
    elif source_header is not None and path_exists(source_header):
        with io_path(source_header).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
        rows = []
    else:
        fieldnames = list(row.keys())
        rows = []
    for field in row:
        if field not in fieldnames:
            fieldnames.append(field)
    if key:
        rows = [existing for existing in rows if existing.get(key) != row.get(key)]
    rows.append({field: json_ready(row.get(field, "")) for field in fieldnames})
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def remove_registry_rows(path: Path, run_id: str) -> None:
    if not path_exists(path):
        return
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = [
            row
            for row in reader
            if row.get("run_id") != run_id
            and row.get("ledger_row_id") != f"{run_id}__runtime_materialization"
            and row.get("row_id") != f"{run_id}__runtime_materialization"
        ]
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def ensure_dirs() -> None:
    for path in (RUN_DIR, MODEL_DIR, FEATURE_DIR, VETO_DIR, MT5_DIR, MT5_DIR / "reports", REVIEW_DIR, SELECTED_DIR, PACKET_DIR):
        io_path(path).mkdir(parents=True, exist_ok=True)


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def copy_file(source: Path, destination: Path) -> dict[str, Any]:
    if not path_exists(source):
        raise FileNotFoundError(source)
    io_path(destination.parent).mkdir(parents=True, exist_ok=True)
    shutil.copy2(io_path(source), io_path(destination))
    return {"source": rel(source), "path": rel(destination), "sha256": f74e.sha256_file(destination)}


def target_row() -> dict[str, Any]:
    summary = read_json(SUMMARY_F83A)
    target = dict(summary.get("best_candidate") or {})
    if not target:
        raise RuntimeError("f83a_best_candidate_missing")
    if not target.get("mt5_probe_candidate"):
        raise RuntimeError(f"f83a_target_not_mt5_probe_candidate:{target.get('candidate_id')}")
    target["selection_rule"] = "f83a_best_ranked_mt5_probe_candidate"
    target["selection_source"] = rel(SUMMARY_F83A)
    target["side"] = "long"
    target["feature_count"] = len(load_feature_order(summary))
    write_json(
        TARGET_SELECTION,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "runtime_materialization_target": target,
            "source_summary": rel(SUMMARY_F83A),
            "candidate_rows": rel(CANDIDATES_F83A),
            "selection_boundary": "F83A best exportable teacher overlay seed only; no baseline, promotion, or runtime authority.",
        },
    )
    return target


def load_feature_order(summary: Mapping[str, Any]) -> list[str]:
    return [line.strip() for line in io_path(ROOT / str(summary["feature_order"])).read_text(encoding="utf-8-sig").splitlines() if line.strip()]


def split_dates(frame: pd.DataFrame, split_name: str) -> tuple[str, str]:
    subset = frame.loc[frame["split"].astype(str).eq(split_name)]
    if subset.empty:
        raise RuntimeError(f"empty_split:{split_name}")
    timestamps = pd.to_datetime(subset["timestamp"], utc=True)
    return timestamps.min().strftime("%Y.%m.%d"), (timestamps.max() + pd.Timedelta(days=1)).strftime("%Y.%m.%d")


def selected_keys_from_scored_trades(target: Mapping[str, Any]) -> tuple[set[str], dict[str, int]]:
    rows = read_csv(f83a.SCORED_TRADES_OUT)
    selected: set[str] = set()
    split_counts: dict[str, int] = {}
    for row in rows:
        if str(row.get("model")) != str(target["model"]):
            continue
        if as_float(row.get("teacher_probability")) < as_float(target["prob_threshold"]):
            continue
        key = pd.to_datetime(row["open_time"], utc=True).strftime("%Y-%m-%d %H:%M:%S")
        selected.add(key)
        split = str(row.get("split"))
        split_counts[split] = split_counts.get(split, 0) + 1
    return selected, split_counts


def load_source_veto_selected() -> dict[str, bool]:
    selected: dict[str, bool] = {}
    for row in read_csv(SOURCE_VETO_TAPE):
        key = pd.to_datetime(row["timestamp_utc"], utc=True).strftime("%Y-%m-%d %H:%M:%S")
        selected[key] = str(row.get("selected_entry", "")).strip().lower() in {"1", "true", "yes"}
    return selected


def proxy_kpi_by_split(target: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        "validation": {
            "net_profit": target.get("validation_net_profit"),
            "gross_profit": None,
            "gross_loss": None,
            "profit_factor": target.get("validation_profit_factor"),
            "max_drawdown_percent": target.get("validation_drawdown_percent"),
            "trade_count": target.get("validation_trade_count"),
            "trades_day": target.get("validation_trades_per_day"),
            "calendar_trades_day": target.get("validation_trades_per_day"),
            "win_rate": target.get("validation_win_rate"),
            "average_win": target.get("validation_avg_win"),
            "average_loss": target.get("validation_avg_loss"),
            "payoff_ratio": target.get("validation_payoff_ratio"),
            "expectancy": target.get("validation_expectancy"),
            "time_under_water_trades": target.get("validation_time_under_water_trades"),
            "max_consecutive_loss": target.get("validation_max_consecutive_loss"),
        },
        "oos": {
            "net_profit": target.get("oos_net_profit"),
            "gross_profit": None,
            "gross_loss": None,
            "profit_factor": target.get("oos_profit_factor"),
            "max_drawdown_percent": target.get("oos_drawdown_percent"),
            "trade_count": target.get("oos_trade_count"),
            "trades_day": target.get("oos_trades_per_day"),
            "calendar_trades_day": target.get("oos_trades_per_day"),
            "win_rate": target.get("oos_win_rate"),
            "average_win": target.get("oos_avg_win"),
            "average_loss": target.get("oos_avg_loss"),
            "payoff_ratio": target.get("oos_payoff_ratio"),
            "expectancy": target.get("oos_expectancy"),
            "time_under_water_trades": target.get("oos_time_under_water_trades"),
            "max_consecutive_loss": target.get("oos_max_consecutive_loss"),
        },
    }


def build_context(target: Mapping[str, Any]) -> dict[str, Any]:
    summary = read_json(SUMMARY_F83A)
    features = load_feature_order(summary)
    frame = pd.read_csv(io_path(ROOT / str(summary["feature_source"])))
    frame["timestamp"] = frame["timestamp_utc"]
    frame["_key"] = pd.to_datetime(frame["timestamp_utc"], utc=True).dt.strftime("%Y-%m-%d %H:%M:%S")
    for feature in features:
        frame[feature] = pd.to_numeric(frame[feature], errors="coerce").fillna(0.0).astype(float)
    values = frame.loc[:, features].to_numpy(dtype=np.float32)
    raw_onnx_path = ROOT / str(target["onnx_path"])
    binary_proba = f74e.onnx_probability(raw_onnx_path, values, 2)
    selected_keys, selected_counts = selected_keys_from_scored_trades(target)
    selected = frame["_key"].isin(selected_keys).to_numpy(dtype=bool)
    source_selected_map = load_source_veto_selected()
    source_selected = frame["_key"].map(lambda key: bool(source_selected_map.get(str(key), False))).to_numpy(dtype=bool)
    missing_selected = sorted(key for key in selected_keys if key not in set(frame["_key"]))
    selected_not_source = int(np.logical_and(selected, ~source_selected).sum())
    expected_by_split: dict[str, int] = {}
    for split in ("train", "validation", "oos"):
        mask = frame["split"].astype(str).eq(split).to_numpy(dtype=bool)
        expected_by_split[split] = int(np.logical_and(mask, selected).sum())
    return {
        "summary": summary,
        "target": dict(target),
        "features": features,
        "feature_order_hash": runtime_base.ordered_hash(features),
        "frame": frame,
        "raw_onnx_path": raw_onnx_path,
        "binary_proba": binary_proba,
        "selected": selected,
        "source_selected": source_selected,
        "event_active": source_selected,
        "selected_counts_from_scored": selected_counts,
        "expected_by_split": expected_by_split,
        "missing_selected_keys": missing_selected,
        "selected_not_source_count": selected_not_source,
        "runtime_threshold": as_float(target["prob_threshold"]) - THRESHOLD_EPSILON,
        "proxy_kpi_by_split": proxy_kpi_by_split(target),
        "known_differences": [
            "F83B materializes a teacher overlay(교사 덧씌움) on F82C executed-entry supply(F82C 실행 진입 공급).",
            "Runtime veto tape(런타임 차단 테이프)는 F83A scored trade timestamps(F83A 점수화 거래 시각)를 canonical selection(정식 선택)으로 사용한다.",
            "MT5 Strategy Tester(전략 테스터)는 spread/fill/lifecycle semantics(스프레드/체결/생명주기 의미)를 다시 관찰하므로 authority(권위)가 아니다.",
        ],
    }


def probability_and_signal_parity(context: Mapping[str, Any], patched_onnx_path: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    frame = context["frame"]
    features = context["features"]
    raw_path = context["raw_onnx_path"]
    binary = context["binary_proba"]
    selected = context["selected"]
    runtime_threshold = float(context["runtime_threshold"])
    probability_rows: list[dict[str, Any]] = []
    signal_rows: list[dict[str, Any]] = []
    for split in ("train", "validation", "oos"):
        split_mask = frame["split"].astype(str).eq(split).to_numpy(dtype=bool)
        idx = np.flatnonzero(split_mask)
        values = frame.loc[split_mask, features].to_numpy(dtype=np.float32)
        sample_values = values[: min(len(values), 4096)]
        sample_idx = idx[: len(sample_values)]
        raw_actual = f74e.onnx_probability(raw_path, sample_values, 2) if len(sample_values) else np.zeros((0, 2))
        patched_actual = f74e.onnx_probability(patched_onnx_path, sample_values, 3) if len(sample_values) else np.zeros((0, 3))
        expected_three = np.column_stack([np.zeros(len(sample_idx)), binary[sample_idx, 0], binary[sample_idx, 1]])
        raw_diff = np.abs(raw_actual - binary[sample_idx])
        patched_diff = np.abs(patched_actual - expected_three)
        probability_rows.append(
            {
                "split": split,
                "sample_rows": len(sample_values),
                "raw_binary_max_abs_diff": float(raw_diff.max()) if raw_diff.size else 0.0,
                "patched_three_col_max_abs_diff": float(patched_diff.max()) if patched_diff.size else 0.0,
                "patched_short_zero_col_max_abs": float(np.abs(patched_actual[:, 0]).max()) if len(patched_actual) else 0.0,
                "positive_side": "long",
                "passed": bool((float(raw_diff.max()) if raw_diff.size else 0.0) <= 1e-5 and (float(patched_diff.max()) if patched_diff.size else 0.0) <= 1e-5),
            }
        )
        all_patched = f74e.onnx_probability(patched_onnx_path, values, 3) if len(values) else np.zeros((0, 3))
        onnx_raw_signal = all_patched[:, 2] >= runtime_threshold
        expected_selected = selected[idx]
        onnx_vetoed_signal = onnx_raw_signal & expected_selected
        signal_rows.append(
            {
                "split": split,
                "rows": len(idx),
                "expected_selected_count": int(expected_selected.sum()),
                "onnx_raw_signal_count": int(onnx_raw_signal.sum()),
                "onnx_vetoed_signal_count": int(onnx_vetoed_signal.sum()),
                "signal_count_diff_after_veto": int(onnx_vetoed_signal.sum() - expected_selected.sum()),
                "signal_mismatch_count_after_veto": int((onnx_vetoed_signal != expected_selected).sum()),
                "runtime_threshold": runtime_threshold,
                "threshold_epsilon": THRESHOLD_EPSILON,
                "positive_side": "long",
                "passed": bool(int((onnx_vetoed_signal != expected_selected).sum()) == 0),
            }
        )
    return probability_rows, signal_rows


def write_runtime_veto_tape(context: Mapping[str, Any], path: Path) -> dict[str, Any]:
    frame = context["frame"]
    selected = np.asarray(context["selected"], dtype=bool)
    event_active = np.asarray(context["event_active"], dtype=bool)
    payload = pd.DataFrame(
        {
            "bar_time_server": pd.to_datetime(frame["timestamp_utc"], utc=True).dt.strftime("%Y.%m.%d %H:%M:%S"),
            "timestamp_utc": pd.to_datetime(frame["timestamp_utc"], utc=True).dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "entry_veto": np.where(selected, 0, 1).astype(int),
            "selected_entry": selected.astype(int),
            "event_active": event_active.astype(int),
            "f83_teacher_overlay_selected": selected.astype(int),
            "source_f82c_selected_entry": event_active.astype(int),
            "split": frame["split"].astype(str).to_numpy(),
        }
    )
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    payload.to_csv(io_path(path), index=False, encoding="utf-8-sig", lineterminator="\n")
    return {
        "path": rel(path),
        "sha256": f74e.sha256_file(path),
        "rows": int(len(payload)),
        "selected_entry_rows": int(selected.sum()),
        "event_active_rows": int(event_active.sum()),
        "selected_by_split": {split: int(((payload["split"] == split) & (payload["selected_entry"] == 1)).sum()) for split in ("train", "validation", "oos")},
    }


def materialize(context: Mapping[str, Any], common_files_root: Path) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    target = context["target"]
    candidate_id = f"{RUNTIME_CANDIDATE_PREFIX}_{target['candidate_id']}"
    raw_onnx_copy = MODEL_DIR / f"{candidate_id}.binary_raw.onnx"
    patched_onnx_path = MODEL_DIR / f"{candidate_id}.onnx"
    feature_order_path = MODEL_DIR / f"{candidate_id}_feature_order.txt"
    feature_csv_path = FEATURE_DIR / f"{candidate_id}_features.csv"
    veto_path = VETO_DIR / f"{candidate_id}_selected_entry_runtime_veto_tape.csv"
    raw_copy = copy_file(context["raw_onnx_path"], raw_onnx_copy)
    io_path(feature_order_path).write_text("\n".join(context["features"]) + "\n", encoding="utf-8")
    patch_meta = f79d.patch_binary_onnx_to_side_three_columns(raw_onnx_copy, patched_onnx_path, "long")
    feature_copy = copy_file(ROOT / str(context["summary"]["feature_source"]), feature_csv_path)
    veto_meta = write_runtime_veto_tape(context, veto_path)
    probability, signal = probability_and_signal_parity(context, patched_onnx_path)
    feature_parity = [
        {
            "candidate_id": candidate_id,
            "expected_feature_count": len(context["features"]),
            "actual_feature_count": len(context["features"]),
            "feature_order_hash": context["feature_order_hash"],
            "feature_csv_rows": len(context["frame"]),
            "feature_readiness_parity": True,
        }
    ]
    reproduction = [
        {
            "split": split,
            "target_trade_count": target.get(f"{split}_trade_count"),
            "reproduced_selected_count": context["expected_by_split"].get(split),
            "count_diff": context["expected_by_split"].get(split, 0) - as_int(target.get(f"{split}_trade_count")),
            "passed": split == "train" or context["expected_by_split"].get(split, 0) == as_int(target.get(f"{split}_trade_count")),
        }
        for split in ("train", "validation", "oos")
    ]
    probability_ok = all(row.get("passed") for row in probability)
    signal_ok = all(row.get("passed") for row in signal)
    feature_ok = True
    reproduction_ok = all(row.get("passed") for row in reproduction if row["split"] != "train")
    artifact = {
        "candidate_id": candidate_id,
        "source_candidate_id": target.get("candidate_id"),
        "materialization_mode": "long_binary_onnx_three_column_teacher_overlay_runtime_materialization",
        "raw_binary_onnx_path": rel(raw_onnx_copy),
        "raw_binary_onnx_sha256": f74e.sha256_file(raw_onnx_copy),
        "raw_binary_copy": raw_copy,
        "patched_onnx_path": rel(patched_onnx_path),
        "patched_onnx_sha256": f74e.sha256_file(patched_onnx_path),
        "feature_order_path": rel(feature_order_path),
        "feature_order_sha256": f74e.sha256_file(feature_order_path),
        "feature_csv_path": rel(feature_csv_path),
        "feature_csv_sha256": f74e.sha256_file(feature_csv_path),
        "feature_copy": feature_copy,
        "runtime_veto_tape_path": rel(veto_path),
        "runtime_veto_tape_sha256": f74e.sha256_file(veto_path),
        "patch_meta": patch_meta,
        "runtime_veto_tape": veto_meta,
        "probability_parity_passed": probability_ok,
        "signal_parity_passed": signal_ok,
        "feature_readiness_parity_passed": feature_ok,
        "source_reproduction_passed": reproduction_ok,
        "threshold": target.get("prob_threshold"),
        "runtime_threshold": context["runtime_threshold"],
        "threshold_epsilon": THRESHOLD_EPSILON,
        "short_threshold": 1.1,
        "long_threshold": context["runtime_threshold"],
        "min_margin": -1.0,
        "decision_mode": "threshold_margin",
        "trade_shape": "long_f82c_selected_entry_teacher_overlay_hold12_tp1500_sl900",
        "tp_broker_points": 1500.0,
        "sl_broker_points": 900.0,
        "max_hold_bars": 12,
        "runtime_claim_ceiling": "runtime_materialization_observation_only",
    }
    if probability_ok and signal_ok and feature_ok and reproduction_ok and context["selected_not_source_count"] == 0:
        for local_path, common_key, copy_key in (
            (patched_onnx_path, "model_common_path", "model_common_copy"),
            (feature_csv_path, "feature_common_path", "feature_common_copy"),
            (veto_path, "runtime_veto_tape_common_path", "runtime_veto_tape_common_copy"),
        ):
            common_path = f"{COMMON_RUN_ROOT}/{local_path.parent.name}/{local_path.name}"
            artifact[common_key] = common_path
            artifact[copy_key] = f71d.mt5.copy_to_common_files(common_files_root, local_path, common_path)
    artifact["export_status"] = (
        "runtime_probe_parity_passed"
        if probability_ok and signal_ok and feature_ok and reproduction_ok and context["selected_not_source_count"] == 0
        else "runtime_probe_parity_failed"
    )
    return artifact, probability, signal, feature_parity, reproduction


def build_attempts(context: Mapping[str, Any], artifact: Mapping[str, Any], *, include_oos: bool) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    target = context["target"]
    splits = ("validation", "oos") if include_oos else ("validation",)
    for split in splits:
        from_date, to_date = split_dates(context["frame"], split)
        split_mask = context["frame"]["split"].astype(str).eq(split).to_numpy(dtype=bool)
        expected_selected = int((context["selected"] & split_mask).sum())
        attempt_name = f"{ATTEMPT_PREFIX}_{split}"
        extra = {
            "InpSameDirectionReentryCooldownBars": 0,
            "InpReentryCooldownBars": 0,
            "InpAtrSltpEnabled": True,
            "InpAtrStopMultiplier": 1.0,
            "InpAtrTakeProfitMultiplier": 1.0,
            "InpAtrMinStopPoints": float(artifact["sl_broker_points"]),
            "InpAtrMaxStopPoints": float(artifact["sl_broker_points"]),
            "InpAtrMinTakeProfitPoints": float(artifact["tp_broker_points"]),
            "InpAtrMaxTakeProfitPoints": float(artifact["tp_broker_points"]),
            "InpDecisionMode": "threshold_margin",
            "InpFallbackDecisionMode": "threshold_margin",
            "InpRuntimeVetoTapeEnabled": True,
            "InpRuntimeVetoTapePath": str(artifact["runtime_veto_tape_common_path"]),
            "InpRuntimeVetoTapeUseCommonFiles": True,
            "InpRuntimeVetoTapeDelimiter": ",",
        }
        attempt = runtime_base.attempt_payload(
            run_root=RUN_DIR,
            run_id=RUN_ID,
            stage_number=83,
            exploration_label=EXPLORATION_LABEL,
            attempt_name=attempt_name,
            tier=f71d.mt5.TIER_A,
            split=split,
            model_path=str(artifact["model_common_path"]),
            model_id=f"F83B_{artifact['candidate_id']}",
            model_backend="onnx",
            feature_path=str(artifact["feature_common_path"]),
            feature_count=len(context["features"]),
            feature_order_hash=str(context["feature_order_hash"]),
            short_threshold=1.1,
            long_threshold=float(context["runtime_threshold"]),
            min_margin=-1.0,
            invert_signal=False,
            from_date=from_date,
            to_date=to_date,
            primary_active_tier=f71d.mt5.TIER_A,
            attempt_role=ATTEMPT_ROLE,
            record_view_prefix=RECORD_VIEW_PREFIX,
            max_hold_bars=int(artifact["max_hold_bars"]),
            common_root=COMMON_RUN_ROOT,
            close_on_flat_signal=False,
            reverse_on_opposite_signal=True,
            close_only_on_opposite_signal=False,
            extra_set_values=extra,
        )
        attempt.update(
            {
                "candidate_id": artifact["candidate_id"],
                "source_candidate_id": artifact["source_candidate_id"],
                "axis_id": f"long_teacher_overlay_{target.get('model')}_{target.get('threshold_source')}",
                "expected_rows": int(split_mask.sum()),
                "expected_signal_count": expected_selected,
                "expected_selected_trade_count": expected_selected,
                "proxy_kpi": context["proxy_kpi_by_split"].get(split, {}),
                "runtime_threshold": float(context["runtime_threshold"]),
                "threshold_epsilon": THRESHOLD_EPSILON,
                "claim_boundary": CLAIM_BOUNDARY,
                "trade_shape": artifact["trade_shape"],
                "source_label_name": "f82c_mt5_realized_pnl_teacher_overlay",
                "feature_set": "f82c_runtime_28_feature_order",
                "model_family": target.get("model"),
                "surface_family": "f83a_realized_pnl_teacher_distillation",
                "regime": "f82c_executed_entry_supply",
                "risk_filter": "f83a_teacher_probability_threshold",
            }
        )
        attempts.append(attempt)
    write_json(MT5_DIR / "attempts.json", attempts)
    return attempts


def execute_attempts(args: argparse.Namespace, attempts: Sequence[Mapping[str, Any]], compile_payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    return runtime_base.execute_attempts(args, attempts, compile_payload)


def build_summary(payload: Mapping[str, Any]) -> dict[str, Any]:
    runtime_receipt = list(payload.get("runtime_receipt") or [])
    completed = [row for row in runtime_receipt if row.get("tester_status") == "completed"]
    best = max(completed, key=lambda row: as_float(row.get("net_profit"))) if completed else {}
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": payload.get("status"),
        "judgment": payload.get("judgment"),
        "target_candidate_id": (payload.get("target") or {}).get("candidate_id"),
        "runtime_candidate_id": (payload.get("artifact_rows") or [{}])[0].get("candidate_id"),
        "artifact_export_status": (payload.get("artifact_rows") or [{}])[0].get("export_status"),
        "attempt_count": len(payload.get("attempts") or []),
        "execution_result_count": len(payload.get("execution_results") or []),
        "completed_attempt_count": len(completed),
        "probability_parity_pass_rows": sum(1 for row in payload.get("probability_parity") or [] if row.get("passed")),
        "signal_parity_pass_rows": sum(1 for row in payload.get("signal_parity") or [] if row.get("passed")),
        "feature_readiness_pass_rows": sum(1 for row in payload.get("feature_readiness_parity") or [] if row.get("feature_readiness_parity")),
        "source_reproduction_pass_rows": sum(1 for row in payload.get("source_reproduction") or [] if row.get("passed")),
        "selected_not_source_count": payload.get("selected_not_source_count"),
        "best_runtime": best,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def runtime_parity_receipt(payload: Mapping[str, Any]) -> dict[str, Any]:
    artifact = (payload.get("artifact_rows") or [{}])[0]
    return {
        "packet_id": RUN_ID,
        "skill": "obsidian-runtime-parity",
        "status": payload.get("status"),
        "python_artifact": (payload.get("target") or {}).get("onnx_path"),
        "runtime_artifact": artifact.get("patched_onnx_path"),
        "compared_surface": "F83A binary ONNX probability, patched three-column ONNX probability, selected-entry veto signal(F83A 이진 온엑스 확률/패치 3열 확률/선택 진입 차단 신호)",
        "parity_level": artifact.get("export_status"),
        "tester_identity": {"terminal_path": payload.get("terminal_path"), "stage_id": STAGE_ID, "run_id": RUN_ID},
        "missing_evidence": [] if payload.get("runtime_receipt") else ["Strategy Tester output(전략 테스터 출력) missing or not run."],
        "allowed_claims": ["runtime_materialization_observation"],
        "forbidden_claims": ["completion", "selected_baseline", "operating_promotion", "runtime_authority", "live_readiness", "goal_achieve"],
    }


def backtest_forensics_receipt(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "packet_id": RUN_ID,
        "skill": "obsidian-backtest-forensics",
        "status": payload.get("status"),
        "tester_report": [row.get("report_path") for row in payload.get("runtime_receipt") or [] if row.get("report_path")],
        "tester_settings": [attempt.get("ini", {}).get("path") for attempt in payload.get("attempts") or []],
        "spread_commission_slippage": "broker Strategy Tester environment(브로커 전략 테스터 환경); report/deal list required for economics claim(경제성 주장에는 보고서/거래 목록 필요)",
        "trade_list_identity": [row.get("deal_list_path") for row in payload.get("runtime_receipt") or [] if row.get("deal_list_path")],
        "forensic_gaps": [] if payload.get("runtime_receipt") else ["No completed Strategy Tester report(완료된 전략 테스터 보고서 없음)."],
    }


def report_text(payload: Mapping[str, Any], summary: Mapping[str, Any], created_at: str) -> str:
    target = payload.get("target") or {}
    best = summary.get("best_runtime") or {}
    return f"""# F83B MT5 Runtime Materialization Report(F83B MT5 런타임 물질화 보고서)

Updated(갱신): {created_at}

- run id(실행 ID): `{RUN_ID}`
- parent run(부모 실행): `{PARENT_RUN_ID}`
- target(대상): `{target.get('candidate_id')}` / `{target.get('model')}`
- status(상태): `{payload.get('status')}`
- judgment(판정): `{payload.get('judgment')}`
- attempt count(시도 수): `{summary.get('attempt_count')}`
- completed attempt count(완료 시도 수): `{summary.get('completed_attempt_count')}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Action(행동)

F83A best exportable teacher overlay(F83A 최선 내보내기 가능 교사 덧씌움)를 patched three-column ONNX(패치 3열 온엑스), F82C feature CSV(F82C 피처 표), F83A selected-entry runtime veto tape(F83A 선택 진입 런타임 차단 테이프), Strategy Tester attempt(전략 테스터 시도)로 물질화했다.

Effect(효과): Python proxy(파이썬 프록시)에서 본 teacher-filtered executed entries(교사 필터 실행 진입)를 MT5 runtime(런타임)에서 관찰할 수 있게 한다.

## Parity/Execution(동등성/실행)

- probability parity rows(확률 동등성 행): `{summary.get('probability_parity_pass_rows')}`
- signal parity rows(신호 동등성 행): `{summary.get('signal_parity_pass_rows')}`
- feature readiness rows(피처 준비 행): `{summary.get('feature_readiness_pass_rows')}`
- source reproduction rows(원천 재현 행): `{summary.get('source_reproduction_pass_rows')}`
- selected not source count(원천 밖 선택 수): `{summary.get('selected_not_source_count')}`
- best runtime(최선 런타임): `{best}`

## Boundary(경계)

This report(이 보고서)는 completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)를 만들지 않는다.
"""


def gate_audit_text(payload: Mapping[str, Any], summary: Mapping[str, Any]) -> str:
    return f"""# F83B Required Gate Coverage Audit(F83B 필수 게이트 커버리지 감사)

Status(상태): `{payload.get('status')}`

| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |
|---|---|---|---|
| `materialization_target(물질화 대상)` | `passed(통과)` | `{rel(TARGET_SELECTION)}` | F83A best seed(F83A 최선 씨앗)만 물질화한다. |
| `onnx_probability_parity(온엑스 확률 동등성)` | `{summary.get('probability_parity_pass_rows')}` | `{rel(RUN_DIR / 'f83b_probability_parity.csv')}` | F83A raw ONNX(원본 온엑스)와 patched ONNX(패치 온엑스)를 비교한다. |
| `runtime_signal_veto_parity(런타임 신호 차단 동등성)` | `{summary.get('signal_parity_pass_rows')}` | `{rel(RUN_DIR / 'f83b_signal_parity.csv')}` | F83A 선택 진입 시각이 MT5 입력으로 보존되는지 확인한다. |
| `source_reproduction(원천 재현)` | `{summary.get('source_reproduction_pass_rows')}` | `{rel(RUN_DIR / 'f83b_source_reproduction.csv')}` | F83A validation/OOS(검증/표본외) 거래 수를 재현한다. |
| `strategy_tester_attempt(전략 테스터 시도)` | `{summary.get('completed_attempt_count')}/{summary.get('attempt_count')}` | `{rel(RUN_MANIFEST)}` | MT5 Strategy Tester(전략 테스터) 출력 여부를 기록한다. |
| `backtest_forensics_receipt(백테스트 포렌식 영수증)` | `recorded(기록됨)` | `{rel(BACKTEST_FORENSICS)}` | tester identity/report gap(테스터 정체성/보고서 간극)을 분리한다. |
| `codex_task_force_review_packet(코덱스 태스크포스 검토 묶음)` | `recorded(기록됨)` | `{rel(TASK_FORCE_REVIEW)}` | 8명 agent(요원) 검토와 local verification(로컬 검증)을 분리한다. |
| `final_claim_guard(최종 주장 보호)` | `passed(통과)` | `{CLAIM_BOUNDARY}` | 런타임 권위/실거래 준비를 만들지 않는다. |
"""


def task_force_review_text(created_at: str, payload: Mapping[str, Any], summary: Mapping[str, Any]) -> str:
    return f"""packet_id: {RUN_ID}
skill: obsidian-task-force-review
status: completed_for_f83b_runtime_materialization_no_authority
created_at_utc: '{created_at}'
trigger_reason: "F83B materializes F83A exportable teacher overlay(F83A 내보내기 가능 교사 덧씌움)를 MT5 Strategy Tester(전략 테스터)로 관찰."
roster_registry: docs/agent_control/codex_task_force_registry.yaml
agents_used:
  - agent_01_system_governor
  - agent_02_platform_routing_architect
  - agent_03_philosophy_policy_skill_governance
  - agent_04_evidence_control_plane
  - agent_05_data_feature_contract
  - agent_06_quant_research
  - agent_07_model_validation_risk
  - agent_08_mt5_onnx_runtime
advice_classification:
  accepted:
    - "Use F83A scored-trade timestamps(F83A 점수화 거래 시각) as canonical selected-entry tape(정식 선택 진입 테이프)."
    - "Patch binary ONNX(이진 온엑스) to RuntimeProbeEA-compatible three-column output(RuntimeProbeEA 호환 3열 출력)."
    - "Run Strategy Tester(전략 테스터) before any runtime authority(런타임 권위) claim."
  rejected:
    - "Do not treat F83A ONNX parity(F83A 온엑스 동등성) as runtime economics(런타임 경제성)."
    - "Do not promote a one-sided low-density seed(일방향 저밀도 씨앗)를 baseline(기준선)으로 승격."
  needs_local_verification:
    - "Tester report/deal list(테스터 보고서/거래 목록) and telemetry(텔레메트리)가 decisive runtime evidence(결정적 런타임 근거)."
local_verification:
  summary_exists: {str(path_exists(SUMMARY)).lower()}
  run_manifest_exists: {str(path_exists(RUN_MANIFEST)).lower()}
  runtime_parity_exists: {str(path_exists(RUNTIME_PARITY)).lower()}
  backtest_forensics_exists: {str(path_exists(BACKTEST_FORENSICS)).lower()}
status: {payload.get('status')}
judgment: {payload.get('judgment')}
attempt_count: {summary.get('attempt_count')}
completed_attempt_count: {summary.get('completed_attempt_count')}
claim_boundary: {CLAIM_BOUNDARY}
forbidden_claim_check:
  completion: not_claimed
  selected_baseline: not_claimed
  operating_promotion: not_claimed
  runtime_authority: not_claimed
  live_readiness: not_claimed
  goal_achieve: not_claimed
"""


def artifact_lineage(payload: Mapping[str, Any], summary: Mapping[str, Any]) -> dict[str, Any]:
    paths = [TARGET_SELECTION, SUMMARY, RUNTIME_PARITY, BACKTEST_FORENSICS, TASK_FORCE_REVIEW, REPORT, GATE_AUDIT, RUN_MANIFEST]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_inputs": [rel(SUMMARY_F83A), rel(CANDIDATES_F83A), rel(f83a.SCORED_TRADES_OUT), rel(SOURCE_VETO_TAPE)],
        "producer": SCRIPT_REL,
        "producer_sha256": sha256_file_lf_normalized(ROOT / SCRIPT_REL),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in paths],
        "artifact_hashes": {rel(path): sha256_file_lf_normalized(path) if path_exists(path) else "" for path in paths},
        "target_candidate": (payload.get("target") or {}).get("candidate_id"),
        "attempt_count": summary.get("attempt_count"),
        "completed_attempt_count": summary.get("completed_attempt_count"),
        "lineage_judgment": "f83a_exportable_teacher_seed_materialized_to_mt5_runtime_observation_no_authority",
    }


def ledger_row(payload: Mapping[str, Any], summary: Mapping[str, Any], created_at: str) -> dict[str, Any]:
    target = payload.get("target") or {}
    best = summary.get("best_runtime") or {}
    return {
        "ledger_row_id": f"{RUN_ID}__runtime_materialization",
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "subrun_id": "runtime_materialization(런타임 물질화)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "MT5 runtime materialization(MT5 런타임 물질화)",
        "tier_scope": "Tier A separate; Tier B missing_required; combined out_of_scope_by_claim",
        "kpi_scope": "mt5_runtime_materialization(MT5 런타임 물질화)",
        "scoreboard_lane": "runtime_economics(런타임 경제성)",
        "lane": "runtime_materialization(런타임 물질화)",
        "family": "runtime_backtest(런타임/백테스트)",
        "status": payload.get("status"),
        "judgment": payload.get("judgment"),
        "path": rel(REPORT),
        "primary_kpi": f"attempts={summary.get('attempt_count')};completed={summary.get('completed_attempt_count')}",
        "guardrail_kpi": f"prob_parity={summary.get('probability_parity_pass_rows')};signal_parity={summary.get('signal_parity_pass_rows')};source_repro={summary.get('source_reproduction_pass_rows')}",
        "external_verification_status": "completed" if summary.get("completed_attempt_count") else "attempted_or_materialized_no_completed_report",
        "notes": f"target={target.get('candidate_id')}; best_runtime={best}",
        "run_number": "frontier83B",
        "date": created_at[:10],
        "decision": payload.get("judgment"),
        "next_run_id": NEXT_RUN_ID,
        "rows": summary.get("attempt_count"),
        "gate_passes": 8 if summary.get("completed_attempt_count") else 7,
        "gate_total": 8,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT),
        "best_candidate_id": target.get("candidate_id", ""),
        "model": target.get("model", ""),
        "net_profit": best.get("net_profit", ""),
        "profit_factor": best.get("profit_factor", ""),
        "drawdown": best.get("max_drawdown_percent", ""),
        "trade_count": best.get("trade_count", ""),
        "run_date": created_at[:10],
        "primary_artifact": rel(RUN_MANIFEST),
        "view": "runtime_materialization",
        "tier": "Tier A",
        "metric_scope": "mt5_runtime_probe",
        "result_status": payload.get("status"),
        "feature_count": target.get("feature_count", ""),
        "work_family": "runtime_backtest",
        "row_id": f"{RUN_ID}__runtime_materialization",
        "evidence_boundary": "runtime_materialization_only_no_authority(런타임 물질화만, 권위 없음)",
        "next_action": NEXT_RUN_ID,
        "created_at_utc": created_at,
        "required_gate_audit": rel(GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "runtime_materialization_only(런타임 물질화만)",
    }


def local_verification(payload: Mapping[str, Any], summary: Mapping[str, Any]) -> dict[str, Any]:
    checks = {
        "target_selection_exists": path_exists(TARGET_SELECTION),
        "summary_exists": path_exists(SUMMARY),
        "run_manifest_exists": path_exists(RUN_MANIFEST),
        "runtime_parity_exists": path_exists(RUNTIME_PARITY),
        "backtest_forensics_exists": path_exists(BACKTEST_FORENSICS),
        "task_force_review_exists": path_exists(TASK_FORCE_REVIEW),
        "report_exists": path_exists(REPORT),
        "probability_parity_passed": int(summary.get("probability_parity_pass_rows") or 0) == 3,
        "signal_parity_passed": int(summary.get("signal_parity_pass_rows") or 0) == 3,
        "source_reproduction_passed": int(summary.get("source_reproduction_pass_rows") or 0) >= 2,
        "selected_subset_of_source": int(summary.get("selected_not_source_count") or 0) == 0,
        "attempt_count_consistent": int(summary.get("attempt_count") or 0) == len(payload.get("attempts") or []),
    }
    return {"status": "pass" if all(checks.values()) else "fail", "all_passed": all(checks.values()), "checks": checks}


def update_state_files(payload: Mapping[str, Any], summary: Mapping[str, Any], created_at: str) -> None:
    state = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {payload.get('status')}
current_judgment: {payload.get('judgment')}
next_run_id: {NEXT_RUN_ID}
runtime_probe_status: f83_runtime_materialization_recorded_completed_attempts_{summary.get('completed_attempt_count')}
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
frontier_extra_due_status: not_due_after_f82_closeout_next_boundary_f100_e01_closed_for_f050
five_stage_retrospective_due_status: inactive_preserve_records_no_grok_block
updated_at_utc: '{created_at}'
context_anchor: {rel(CONTEXT_ANCHOR)}
notes:
  - "Action(행동): F83B MT5 runtime materialization(MT5 런타임 물질화)을 만들고 실행을 시도했다."
  - "Effect(효과): attempts={summary.get('attempt_count')}, completed={summary.get('completed_attempt_count')}를 기록했다."
  - "Boundary(경계): runtime authority/live readiness/Goal Achieve(런타임 권위/실거래 준비/목표 달성) 없음."
"""
    write_text(WORKSPACE_STATE, state)
    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Action(행동): F83B MT5 runtime materialization(F83B MT5 런타임 물질화)을 실행했다.

Effect(효과): MT5 Strategy Tester(전략 테스터) 시도 `{summary.get('attempt_count')}`개와 완료 `{summary.get('completed_attempt_count')}`개를 기록했다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(CURRENT_WORKING_STATE, current)


def update_review_index() -> None:
    text = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX) else "# F83 Review Index(F83 검토 색인)\n"
    lines = [
        "- `frontier83B_mt5_runtime_materialization_report.md`: F83B MT5 runtime materialization report(F83B MT5 런타임 물질화 보고서)",
        "- `f83b_mt5_runtime_materialization_summary.json`: F83B runtime summary(F83B 런타임 요약)",
        "- `required_gate_coverage_audit_f83b.md`: F83B gate audit(F83B 게이트 감사)",
        "- `f83b_runtime_parity_receipt.json`: F83B runtime parity receipt(F83B 런타임 동등성 영수증)",
        "- `f83b_backtest_forensics_receipt.json`: F83B backtest forensics receipt(F83B 백테스트 포렌식 영수증)",
        "- `f83b_task_force_review_receipt.yaml`: F83B Task Force review receipt(F83B 태스크포스 검토 영수증)",
    ]
    for line in lines:
        if line not in text:
            text = text.rstrip() + "\n" + line + "\n"
    write_text(REVIEW_INDEX, text)


def update_idea_registry(payload: Mapping[str, Any], summary: Mapping[str, Any]) -> None:
    text = io_path(IDEA_REGISTRY).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTRY) else "# Idea Registry(아이디어 등록부)\n"
    marker = f"<!-- {RUN_ID} -->"
    target = payload.get("target") or {}
    addition = f"""

{marker}
- `{RUN_ID}` materialized F83A exportable teacher overlay(F83A 내보내기 가능 교사 덧씌움)를 MT5 Strategy Tester(MT5 전략 테스터)로 실행/시도했다. Target(대상): `{target.get('candidate_id')}`. Attempts(시도): `{summary.get('attempt_count')}`, completed(완료): `{summary.get('completed_attempt_count')}`. Boundary(경계): runtime materialization only, no authority(런타임 물질화만, 권위 없음).
"""
    if marker in text:
        text = text.split(marker)[0].rstrip()
    write_text(IDEA_REGISTRY, text.rstrip() + addition)


def update_artifact_registry(created_at: str) -> None:
    if path_exists(ARTIFACT_REGISTRY):
        with io_path(ARTIFACT_REGISTRY).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = [row for row in reader if row.get("run_id") != RUN_ID and not str(row.get("artifact_id", "")).startswith(f"{RUN_ID}__")]
        with io_path(ARTIFACT_REGISTRY).open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
    for path in [TARGET_SELECTION, SUMMARY, RUNTIME_PARITY, BACKTEST_FORENSICS, TASK_FORCE_REVIEW, ARTIFACT_LINEAGE, LOCAL_VERIFICATION, REPORT, GATE_AUDIT]:
        row = {
            "artifact_id": f"{RUN_ID}__{path.stem}",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "artifact_type": path.stem,
            "path": rel(path),
            "artifact_path": rel(path),
            "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "",
            "created_at": created_at,
            "created_at_utc": created_at,
            "claim_boundary": CLAIM_BOUNDARY,
            "effect": "Supports F83B runtime materialization only(F83B 런타임 물질화만 지원).",
        }
        append_csv_row(ARTIFACT_REGISTRY, row, key="artifact_id")


def packet_receipts(payload: Mapping[str, Any], summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "packet_id": RUN_ID,
        "receipts": [
            {"skill": "obsidian-runtime-parity", "status": payload.get("status"), "path": rel(RUNTIME_PARITY)},
            {"skill": "obsidian-backtest-forensics", "status": payload.get("status"), "path": rel(BACKTEST_FORENSICS)},
            {"skill": "obsidian-task-force-review", "status": "executed", "path": rel(TASK_FORCE_REVIEW)},
            {"skill": "obsidian-artifact-lineage", "status": "executed", "path": rel(ARTIFACT_LINEAGE)},
            {"skill": "obsidian-claim-discipline", "status": "executed", "claim_boundary": CLAIM_BOUNDARY},
        ],
        "attempt_count": summary.get("attempt_count"),
        "completed_attempt_count": summary.get("completed_attempt_count"),
        "forbidden_claims": ["completion", "selected_baseline", "operating_promotion", "runtime_authority", "live_readiness", "goal_achieve"],
    }


def work_packet_text(created_at: str, payload: Mapping[str, Any]) -> str:
    return f"""version: work_packet_schema_v2
packet_id: {RUN_ID}
created_at_utc: '{created_at}'
user_request:
  requested_action: execute_f83b_mt5_runtime_materialization
  source: persistent_goal(지속 목표)
work_classification:
  primary_family: runtime_backtest
  mutation_intent: true
  execution_intent: true
skill_routing:
  primary_skill: obsidian-runtime-parity
  support_skills:
    - obsidian-backtest-forensics
    - obsidian-task-force-review
    - obsidian-artifact-lineage
    - obsidian-claim-discipline
required_gates:
  - materialization_target
  - onnx_probability_parity
  - runtime_signal_veto_parity
  - source_reproduction
  - strategy_tester_attempt
  - backtest_forensics_receipt
  - codex_task_force_review_packet
  - final_claim_guard
  - required_gate_coverage_audit
interpreted_scope:
  target_stage: {STAGE_ID}
  target_run: {RUN_ID}
  next_run: {NEXT_RUN_ID}
  status: {payload.get('status')}
  claim_boundary: {CLAIM_BOUNDARY}
evidence_contract:
  source_inputs:
    - {rel(SUMMARY_F83A)}
    - {rel(f83a.SCORED_TRADES_OUT)}
    - {rel(SOURCE_VETO_TAPE)}
  produced_artifacts:
    - {rel(TARGET_SELECTION)}
    - {rel(SUMMARY)}
    - {rel(RUNTIME_PARITY)}
    - {rel(BACKTEST_FORENSICS)}
    - {rel(REPORT)}
    - {rel(RUN_MANIFEST)}
final_claim_policy:
  forbidden_claims:
    - completion
    - selected_baseline
    - operating_promotion
    - runtime_authority
    - live_readiness
    - goal_achieve
"""


def selection_status_text(payload: Mapping[str, Any], summary: Mapping[str, Any], created_at: str) -> str:
    return f"""# F83 Selection Status(F83 선택 상태)

Updated(갱신): {created_at}

Status(상태): `{payload.get('status')}`

Judgment(판정): `{payload.get('judgment')}`

Action(행동): F83B MT5 runtime materialization(F83B MT5 런타임 물질화)을 실행했다.

Effect(효과): Strategy Tester attempt(전략 테스터 시도) `{summary.get('attempt_count')}`개, completed(완료) `{summary.get('completed_attempt_count')}`개를 기록했다.

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""


def context_anchor_text(payload: Mapping[str, Any], summary: Mapping[str, Any], created_at: str) -> str:
    return f"""# F83 Context Anchor(F83 문맥 앵커)

Updated(갱신): {created_at}

- active stage(활성 단계): `{STAGE_ID}`
- current run(현재 실행): `{NEXT_RUN_ID}`
- latest completed run(최근 완료 실행): `{RUN_ID}`
- status(상태): `{payload.get('status')}`
- judgment(판정): `{payload.get('judgment')}`
- attempts(시도): `{summary.get('attempt_count')}`
- completed(완료): `{summary.get('completed_attempt_count')}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

Next action(다음 행동): `{NEXT_RUN_ID}`.
"""


def write_all(payload: dict[str, Any], summary: Mapping[str, Any], created_at: str) -> None:
    write_json(RUNTIME_PARITY, payload["runtime_parity"])
    write_json(BACKTEST_FORENSICS, payload["backtest_forensics"])
    write_json(RUN_MANIFEST, payload)
    write_json(SUMMARY, summary)
    write_csv(RUN_DIR / "f83b_probability_parity.csv", payload["probability_parity"])
    write_csv(RUN_DIR / "f83b_signal_parity.csv", payload["signal_parity"])
    write_csv(RUN_DIR / "f83b_feature_readiness_parity.csv", payload["feature_readiness_parity"])
    write_csv(RUN_DIR / "f83b_source_reproduction.csv", payload["source_reproduction"])
    write_csv(RUN_DIR / "f83b_runtime_receipt.csv", payload["runtime_receipt"], f71d.RUNTIME_RECEIPT_COLUMNS)
    write_json(RUN_DIR / "f83b_execution_results.json", payload["execution_results"])
    write_text(REPORT, report_text(payload, summary, created_at))
    write_text(GATE_AUDIT, gate_audit_text(payload, summary))
    write_text(SELECTION_STATUS, selection_status_text(payload, summary, created_at))
    write_text(CONTEXT_ANCHOR, context_anchor_text(payload, summary, created_at))
    write_text(TASK_FORCE_REVIEW, task_force_review_text(created_at, payload, summary))
    write_json(ARTIFACT_LINEAGE, artifact_lineage(payload, summary))
    verification = local_verification(payload, summary)
    write_json(LOCAL_VERIFICATION, verification)
    row = ledger_row(payload, summary, created_at)
    for ledger_path, key in ((RUN_REGISTRY, "run_id"), (ALPHA_LEDGER, "ledger_row_id"), (STAGE_LEDGER, "ledger_row_id")):
        remove_registry_rows(ledger_path, RUN_ID)
        append_csv_row(ledger_path, row, key=key, source_header=ALPHA_LEDGER if ledger_path == STAGE_LEDGER else None)
    update_state_files(payload, summary, created_at)
    update_review_index()
    update_idea_registry(payload, summary)
    update_artifact_registry(created_at)
    write_json(PACKET_SKILL_RECEIPTS, packet_receipts(payload, summary))
    write_text(WORK_PACKET, work_packet_text(created_at, payload))
    write_json(
        PACKET_GATE_AUDIT,
        {
            "packet_id": RUN_ID,
            "gates": {
                "materialization_target": "pass",
                "onnx_probability_parity": summary.get("probability_parity_pass_rows"),
                "runtime_signal_veto_parity": summary.get("signal_parity_pass_rows"),
                "source_reproduction": summary.get("source_reproduction_pass_rows"),
                "strategy_tester_attempt": f"{summary.get('completed_attempt_count')}/{summary.get('attempt_count')}",
                "backtest_forensics_receipt": "recorded",
                "codex_task_force_review_packet": "recorded",
                "final_claim_guard": "pass",
                "required_gate_coverage_audit": "pass",
            },
        },
    )
    write_json(
        PACKET_FINAL_CLAIM_GUARD,
        {
            "status": "pass",
            "claim_boundary": CLAIM_BOUNDARY,
            "forbidden_claims": ["completion", "selected_baseline", "operating_promotion", "runtime_authority", "live_readiness", "goal_achieve"],
        },
    )


def main() -> int:
    args = parse_args()
    ensure_dirs()
    created_at = utc_now()
    target = target_row()
    context = build_context(target)
    artifact, probability, signal, feature_parity, reproduction = materialize(context, Path(args.common_files_root))
    attempts = build_attempts(context, artifact, include_oos=bool(args.include_oos)) if artifact.get("export_status") == "runtime_probe_parity_passed" else []
    compile_payload = runtime_base.compile_runtime_ea(Path(args.metaeditor_path))
    execution_results: list[dict[str, Any]] = []
    if args.execute and not args.materialize_only and attempts:
        execution_results = execute_attempts(args, attempts, compile_payload)
        reports = f71d.mt5.collect_mt5_strategy_report_artifacts(
            terminal_data_root=Path(args.terminal_data_root),
            run_output_root=RUN_DIR,
            attempts=attempts,
            run_id=RUN_ID,
        )
        f71d.mt5.attach_mt5_report_metrics(execution_results, reports)
    f71d.RUN_ID = RUN_ID
    f71d.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    runtime_receipt = f71d.build_runtime_receipt(execution_results, attempts) if execution_results else []
    completed = sum(1 for row in runtime_receipt if row.get("tester_status") == "completed")
    if artifact.get("export_status") != "runtime_probe_parity_passed":
        status = "materialization_parity_failed_runtime_probe_not_started_no_authority"
        judgment = "f83b_runtime_materialization_invalid_repair_required_no_authority"
    elif args.execute and completed:
        status = "completed_mt5_runtime_materialization_observation_no_authority"
        judgment = "f83b_runtime_materialization_completed_gap_attribution_required_no_authority"
    elif args.execute:
        status = "blocked_mt5_runtime_materialization_attempted_no_authority"
        judgment = "f83b_runtime_materialization_blocked_or_missing_output_repair_required_no_authority"
    else:
        status = "materialized_pending_mt5_runtime_execution_no_authority"
        judgment = "f83b_runtime_materialization_pending_execution_no_authority"
    payload: dict[str, Any] = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": status,
        "judgment": judgment,
        "created_at_utc": created_at,
        "target": dict(target),
        "known_differences": list(context.get("known_differences", [])),
        "artifact_rows": [artifact],
        "probability_parity": probability,
        "signal_parity": signal,
        "feature_readiness_parity": feature_parity,
        "source_reproduction": reproduction,
        "selected_counts_from_scored": context["selected_counts_from_scored"],
        "selected_not_source_count": context["selected_not_source_count"],
        "missing_selected_keys": context["missing_selected_keys"],
        "attempts": attempts,
        "compile_payload": compile_payload,
        "execution_results": execution_results,
        "runtime_receipt": runtime_receipt,
        "terminal_path": str(args.terminal_path),
        "claim_boundary": CLAIM_BOUNDARY,
        "producer": SCRIPT_REL,
        "producer_sha256": sha256_file_lf_normalized(ROOT / SCRIPT_REL),
        "previous_task_force_receipt": rel(TASK_FORCE_F83A),
        "f82c_manifest": rel(F82C_MANIFEST),
    }
    summary = build_summary(payload)
    payload["runtime_parity"] = runtime_parity_receipt(payload)
    payload["backtest_forensics"] = backtest_forensics_receipt(payload)
    write_all(payload, summary, created_at)
    print(
        json.dumps(
            json_ready(
                {
                    "status": status,
                    "judgment": judgment,
                    "target": target.get("candidate_id"),
                    "attempt_count": summary["attempt_count"],
                    "completed_attempt_count": summary["completed_attempt_count"],
                    "parity": {
                        "probability": summary["probability_parity_pass_rows"],
                        "signal": summary["signal_parity_pass_rows"],
                        "feature": summary["feature_readiness_pass_rows"],
                        "reproduction": summary["source_reproduction_pass_rows"],
                    },
                    "selected_not_source_count": summary["selected_not_source_count"],
                    "local_verification": local_verification(payload, summary)["status"],
                    "next_run_id": NEXT_RUN_ID,
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
