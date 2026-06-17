from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized
from stage_pipelines.stage_frontier_71 import frontier71d_mt5_runtime_probe_economics_native_scout as f71d
from stage_pipelines.stage_frontier_74 import frontier74e_mt5_microburst_negative_control_runtime_probe as f74e
from stage_pipelines.stage_frontier_77 import frontier77d_mt5_lifecycle_negative_control_runtime_probe as runtime_base
from stage_pipelines.stage_frontier_78 import frontier78b_execution_calibrated_density_contract_pnl_proxy_scout as f78b
from stage_pipelines.stage_frontier_79 import frontier79b_runtime_native_trade_shape_label_proxy_scout as f79b
from stage_pipelines.stage_frontier_79 import frontier79d_mt5_runtime_native_negative_control_runtime_probe as f79d
from stage_pipelines.stage_frontier_80 import frontier80b_broad_extreme_multi_axis_proxy_scout as f80b
from stage_pipelines.stage_frontier_runtime_backfill.run_frontier_runtime_probe_backfill import (
    DEFAULT_COMMON_FILES,
    DEFAULT_METAEDITOR,
    DEFAULT_PORTABLE_ROOT,
    DEFAULT_TERMINAL,
    DEFAULT_TESTER_PROFILE_ROOT,
)


STAGE_ID = f80b.STAGE_ID
RUN_ID = "frontier80D_mt5_runtime_probe_quality_v1"
PARENT_RUN_ID = "frontier80C_wfo_aware_surface_selection_v1"
NEXT_RUN_ID = "frontier80E_proxy_runtime_gap_attribution_v1"
COMMON_RUN_ROOT = "Project_Obsidian_Prime_v2/frontier80D_mt5_runtime_probe_quality"
RUNTIME_CANDIDATE_PREFIX = "f80d_runtime"
ATTEMPT_PREFIX = "f80d_runtime_probe_quality"
EXPLORATION_LABEL = "frontier80D_runtime_probe_quality"
ATTEMPT_ROLE = "runtime_probe_quality"
RECORD_VIEW_PREFIX = "mt5_f80d_runtime_probe_quality"
THRESHOLD_EPSILON = 1e-7
CLAIM_BOUNDARY = (
    "runtime_probe_quality_observation_only_no_completion_no_baseline_"
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

TARGET_SELECTION = REVIEW_DIR / "f80c_runtime_materialization_target_selection.json"
REPORT = REVIEW_DIR / "frontier80D_mt5_runtime_probe_quality_report.md"
GATE_AUDIT = REVIEW_DIR / "required_gate_coverage_audit_f80d.md"
SUMMARY = REVIEW_DIR / "f80d_mt5_runtime_probe_quality_summary.json"
RUNTIME_PARITY = REVIEW_DIR / "f80d_runtime_parity_receipt.json"
BACKTEST_FORENSICS = REVIEW_DIR / "f80d_backtest_forensics_receipt.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
CONTEXT_ANCHOR = REVIEW_DIR / "context_anchor.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"

WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
SCRIPT_REL = "stage_pipelines/stage_frontier_80/frontier80d_mt5_runtime_probe_quality.py"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="F80D MT5 runtime probe quality.")
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
    return f78b.utc_now()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    rows = list(rows)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = list(columns or (rows[0].keys() if rows else ["empty"]))
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: json_ready(row.get(field, "")) for field in fieldnames})


def upsert_csv(path: Path, key: str, row: Mapping[str, Any], source_header: Path | None = None) -> None:
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
    rows = [existing for existing in rows if existing.get(key) != row.get(key)]
    rows.append({field: json_ready(row.get(field, "")) for field in fieldnames})
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


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


def ensure_dirs() -> None:
    for path in (RUN_DIR, MODEL_DIR, FEATURE_DIR, VETO_DIR, MT5_DIR, MT5_DIR / "reports", REVIEW_DIR, SELECTED_DIR):
        io_path(path).mkdir(parents=True, exist_ok=True)


def target_row() -> dict[str, Any]:
    payload = read_json(TARGET_SELECTION)
    target = dict(payload.get("runtime_materialization_target") or {})
    if not target:
        raise RuntimeError("f80c_target_missing")
    if str(target.get("export_status")) != "export_ok":
        raise RuntimeError(f"target_not_exportable:{target.get('candidate_id')}:{target.get('export_status')}")
    return target


def cleaned_full_frame(frame: Any, train_valid: np.ndarray, columns: Sequence[str]) -> Any:
    output = frame.copy()
    train = output.loc[train_valid, list(columns)].replace([np.inf, -np.inf], np.nan)
    med = train.median(numeric_only=True).fillna(0.0)
    output.loc[:, list(columns)] = output.loc[:, list(columns)].replace([np.inf, -np.inf], np.nan).fillna(med).astype(float)
    return output


def normalized_proxy_kpi(metrics: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "net_profit": metrics.get("net"),
        "gross_profit": metrics.get("gross_profit"),
        "gross_loss": metrics.get("gross_loss"),
        "profit_factor": metrics.get("pf"),
        "max_drawdown_percent": metrics.get("dd_pct"),
        "trade_count": metrics.get("trade_count"),
        "calendar_trades_day": metrics.get("calendar_trades_day"),
        "active_trades_day": metrics.get("active_trades_day"),
        "win_rate": metrics.get("win_rate"),
        "expectancy": metrics.get("expectancy"),
        "recovery_factor": metrics.get("recovery"),
        "avg_hold_bars": metrics.get("avg_hold_bars"),
        "avg_mae_contract": metrics.get("avg_mae_contract"),
        "avg_spread_cost_contract": metrics.get("avg_spread_cost_contract"),
        "max_consecutive_loss": metrics.get("max_consecutive_loss"),
        "time_under_water_trades": metrics.get("time_under_water_trades"),
    }


def build_context(target: Mapping[str, Any]) -> dict[str, Any]:
    f78b.INITIAL_BALANCE = f80b.INITIAL_BALANCE
    frame, raw, features = f78b.load_inputs()
    spec = next(item for item in f80b.runtime_specs() if item.name == str(target["label_name"]))
    outcome = f79b.compute_outcome(raw, f79b.entry_indices(frame, raw, spec.entry_mode), spec)
    label = f80b.make_label(frame, outcome, spec)
    train_valid = (frame["split"] == "train").to_numpy() & np.asarray(outcome["valid"], dtype=bool)
    feature_columns = f80b.feature_sets(features)[str(target["feature_set"])]
    if len(feature_columns) != as_int(target.get("feature_count")):
        raise RuntimeError(f"feature_count_lock_failed:{len(feature_columns)}:{target.get('feature_count')}")
    matrices = f78b.clean_matrices(frame, train_valid, feature_columns)
    model = f80b.model_builders()[str(target["model"])]()
    model.fit(matrices["train"], label[train_valid])
    train_probs = f78b.probability(model, matrices["train"])
    threshold = float(np.quantile(train_probs, as_float(target.get("prob_quantile"))))
    if abs(threshold - as_float(target.get("prob_threshold"))) > 1e-10:
        raise RuntimeError(f"prob_threshold_drift:{threshold}:{target.get('prob_threshold')}")
    clean_frame = cleaned_full_frame(frame, train_valid, feature_columns)
    binary_proba = f74e.binary_probabilities(model, clean_frame.loc[:, feature_columns])
    score = binary_proba[:, 1]
    thresholds = f78b.risk_thresholds(frame)
    selected_global = np.zeros(len(clean_frame), dtype=bool)
    raw_signal_global = np.zeros(len(clean_frame), dtype=bool)
    event_filter_global = np.zeros(len(clean_frame), dtype=bool)
    proxy_kpi_by_split: dict[str, dict[str, Any]] = {}
    reproduction_rows: list[dict[str, Any]] = []
    for split, prefix in (("validation", "val"), ("oos", "oos")):
        split_mask = clean_frame["split"].astype(str).eq(split).to_numpy(dtype=bool)
        split_df = clean_frame.loc[split_mask].reset_index(drop=True)
        split_outcome = {key: np.asarray(value)[split_mask] for key, value in outcome.items()}
        valid = np.asarray(split_outcome["valid"], dtype=bool)
        event_filter = valid & f80b.regime_mask(split_df, str(target["regime"]), spec.side, thresholds) & f80b.risk_mask(split_df, str(target["risk_filter"]), spec.side, thresholds)
        raw_signal = (score[split_mask] >= threshold) & event_filter
        selected = f78b.lifecycle_select(raw_signal, np.asarray(split_outcome["exit_offset"], dtype=int), as_int(target.get("cooldown_bars")))
        metrics = f78b.contract_kpi(split_df, selected, split_outcome)
        proxy_kpi_by_split[split] = normalized_proxy_kpi(metrics)
        selected_global[split_mask] = selected
        raw_signal_global[split_mask] = raw_signal
        event_filter_global[split_mask] = event_filter
        raw_key = f"{split}_raw_signal_count"
        lifecycle_key = f"{split}_lifecycle_trade_count"
        reproduction_rows.append(
            {
                "split": split,
                "source_trade_count": target.get(f"{prefix}_trade_count"),
                "source_raw_signal_count": target.get(raw_key),
                "source_lifecycle_trade_count": target.get(lifecycle_key),
                "reproduced_net_profit": metrics["net"],
                "reproduced_profit_factor": metrics["pf"],
                "reproduced_max_drawdown_percent": metrics["dd_pct"],
                "reproduced_trade_count": metrics["trade_count"],
                "reproduced_raw_signal_count": int(raw_signal.sum()),
                "reproduced_lifecycle_trade_count": int(selected.sum()),
                "count_diff": int(metrics["trade_count"]) - as_int(target.get(f"{prefix}_trade_count")),
                "raw_signal_count_diff": int(raw_signal.sum()) - as_int(target.get(raw_key)),
                "lifecycle_trade_count_diff": int(selected.sum()) - as_int(target.get(lifecycle_key)),
                "net_diff": float(metrics["net"]) - as_float(target.get(f"{prefix}_net")),
                "pf_diff": float(metrics["pf"]) - as_float(target.get(f"{prefix}_pf")),
                "dd_diff": float(metrics["dd_pct"]) - as_float(target.get(f"{prefix}_dd_pct")),
                "passed": bool(
                    int(metrics["trade_count"]) == as_int(target.get(f"{prefix}_trade_count"))
                    and int(raw_signal.sum()) == as_int(target.get(raw_key))
                    and int(selected.sum()) == as_int(target.get(lifecycle_key))
                    and abs(float(metrics["net"]) - as_float(target.get(f"{prefix}_net"))) <= 1e-6
                    and abs(float(metrics["pf"]) - as_float(target.get(f"{prefix}_pf"))) <= 1e-9
                ),
            }
        )
    return {
        "target": dict(target),
        "frame": clean_frame,
        "spec": spec,
        "features": list(feature_columns),
        "feature_order_hash": runtime_base.ordered_hash(feature_columns),
        "model": model,
        "binary_proba": binary_proba,
        "score": score,
        "threshold": threshold,
        "runtime_threshold": threshold - THRESHOLD_EPSILON,
        "selected": selected_global,
        "raw_signal": raw_signal_global,
        "event_filter": event_filter_global,
        "proxy_kpi_by_split": proxy_kpi_by_split,
        "reproduction_rows": reproduction_rows,
        "known_differences": [
            "Python proxy(파이썬 프록시)는 selected-entry veto tape(선택 진입 거부 테이프)로 MT5 진입 시각을 강제한다.",
            "MT5 Strategy Tester(전략 테스터)는 브로커 체결/스프레드/슬리피지 의미를 따르므로 proxy economics(프록시 경제성)와 다를 수 있다.",
            "This probe(이 탐침)는 runtime quality observation(런타임 품질 관찰)만 만들며 authority(권위)를 만들지 않는다.",
        ],
    }


def side_patched_expected(binary_expected: np.ndarray, side: str) -> np.ndarray:
    flat = binary_expected[:, 0]
    event = binary_expected[:, 1]
    zero = np.zeros(len(binary_expected))
    if side == "long":
        return np.column_stack([zero, flat, event])
    return np.column_stack([event, flat, zero])


def parity_rows(context: Mapping[str, Any], raw_onnx_path: Path, patched_onnx_path: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    frame = context["frame"]
    features = context["features"]
    target = context["target"]
    side = str(target["side"])
    positive_col = 2 if side == "long" else 0
    zero_col = 0 if side == "long" else 2
    runtime_threshold = float(context["runtime_threshold"])
    probability_rows: list[dict[str, Any]] = []
    signal_rows: list[dict[str, Any]] = []
    for split in ("train", "validation", "oos"):
        subset = frame.loc[frame["split"].astype(str).eq(split)]
        idx = subset.index.to_numpy()
        values = subset.loc[:, features].to_numpy(dtype="float64")
        binary_expected = context["binary_proba"][idx]
        patched_expected = side_patched_expected(binary_expected, side)
        sample_values = values[: min(len(values), 4096)]
        raw_actual = f74e.onnx_probability(raw_onnx_path, sample_values, 2)
        patched_actual = f74e.onnx_probability(patched_onnx_path, sample_values, 3)
        raw_diff = np.abs(raw_actual - binary_expected[: len(sample_values)])
        patched_diff = np.abs(patched_actual - patched_expected[: len(sample_values)])
        probability_rows.append(
            {
                "split": split,
                "sample_rows": len(sample_values),
                "raw_binary_max_abs_diff": float(raw_diff.max()) if raw_diff.size else 0.0,
                "patched_three_col_max_abs_diff": float(patched_diff.max()) if patched_diff.size else 0.0,
                "patched_zero_col_max_abs": float(np.abs(patched_actual[:, zero_col]).max()) if len(patched_actual) else 0.0,
                "positive_side": side,
                "passed": bool((float(raw_diff.max()) if raw_diff.size else 0.0) <= 1e-5 and (float(patched_diff.max()) if patched_diff.size else 0.0) <= 1e-5),
            }
        )
        all_patched = f74e.onnx_probability(patched_onnx_path, values, 3)
        onnx_raw_signal = context["event_filter"][idx] & (all_patched[:, positive_col] >= runtime_threshold)
        onnx_vetoed_signal = onnx_raw_signal & context["selected"][idx]
        selected_expected = context["selected"][idx]
        signal_rows.append(
            {
                "split": split,
                "rows": len(subset),
                "expected_selected_count": int(selected_expected.sum()),
                "onnx_raw_signal_count": int(onnx_raw_signal.sum()),
                "onnx_vetoed_signal_count": int(onnx_vetoed_signal.sum()),
                "signal_count_diff_after_veto": int(onnx_vetoed_signal.sum() - selected_expected.sum()),
                "signal_mismatch_count_after_veto": int((onnx_vetoed_signal != selected_expected).sum()),
                "runtime_threshold": runtime_threshold,
                "threshold_epsilon": THRESHOLD_EPSILON,
                "positive_side": side,
                "passed": bool(int((onnx_vetoed_signal != selected_expected).sum()) == 0),
            }
        )
    return probability_rows, signal_rows


def materialize(context: Mapping[str, Any], common_files_root: Path) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    target = context["target"]
    candidate_id = f"{RUNTIME_CANDIDATE_PREFIX}_{target['candidate_id']}"
    model_path = MODEL_DIR / f"{candidate_id}.joblib"
    raw_onnx_path = MODEL_DIR / f"{candidate_id}.binary_raw.onnx"
    patched_onnx_path = MODEL_DIR / f"{candidate_id}.onnx"
    feature_order_path = MODEL_DIR / f"{candidate_id}_feature_order.txt"
    feature_csv_path = FEATURE_DIR / f"{candidate_id}_features.csv"
    veto_path = VETO_DIR / f"{candidate_id}_selected_entry_runtime_veto_tape.csv"
    joblib.dump(context["model"], io_path(model_path))
    io_path(feature_order_path).write_text("\n".join(context["features"]) + "\n", encoding="utf-8")
    raw_export = f74e.export_binary_sklearn_to_onnx(context["model"], raw_onnx_path, len(context["features"]))
    patch_meta = f79d.patch_binary_onnx_to_side_three_columns(raw_onnx_path, patched_onnx_path, str(target["side"]))
    feature_meta = f71d.mt5.export_mt5_feature_matrix_csv(context["frame"], context["features"], feature_csv_path, metadata_columns=("split",))
    veto_meta = f71d.selected_entry_tape(context["frame"], context["selected"], context["event_filter"], veto_path)
    probability, signal = parity_rows(context, raw_onnx_path, patched_onnx_path)
    feature_parity = [
        {
            "candidate_id": candidate_id,
            "expected_feature_count": len(context["features"]),
            "actual_feature_count": len(context["features"]),
            "feature_order_hash": context["feature_order_hash"],
            "feature_csv_feature_count": feature_meta.get("feature_count"),
            "feature_csv_rows": feature_meta.get("rows"),
            "feature_readiness_parity": bool(feature_meta.get("feature_count") == len(context["features"])),
        }
    ]
    probability_ok = all(row.get("passed") for row in probability)
    signal_ok = all(row.get("passed") for row in signal)
    feature_ok = bool(feature_parity[0]["feature_readiness_parity"])
    reproduction_ok = all(row.get("passed") for row in context["reproduction_rows"])
    side = str(target["side"])
    short_threshold = 1.1 if side == "long" else float(context["runtime_threshold"])
    long_threshold = float(context["runtime_threshold"]) if side == "long" else 1.1
    artifact = {
        "candidate_id": candidate_id,
        "source_candidate_id": target.get("candidate_id"),
        "materialization_mode": f"{side}_binary_onnx_three_column_runtime_probe_quality",
        "model_path": rel(model_path),
        "model_sha256": f74e.sha256_file(model_path),
        "raw_binary_onnx_path": rel(raw_onnx_path),
        "raw_binary_onnx_sha256": f74e.sha256_file(raw_onnx_path),
        "patched_onnx_path": rel(patched_onnx_path),
        "patched_onnx_sha256": f74e.sha256_file(patched_onnx_path),
        "feature_order_path": rel(feature_order_path),
        "feature_order_sha256": f74e.sha256_file(feature_order_path),
        "feature_csv_path": rel(feature_csv_path),
        "feature_csv_sha256": f74e.sha256_file(feature_csv_path),
        "runtime_veto_tape_path": rel(veto_path),
        "runtime_veto_tape_sha256": f74e.sha256_file(veto_path),
        "raw_binary_export": raw_export,
        "patch_meta": patch_meta,
        "feature_csv": feature_meta,
        "runtime_veto_tape": veto_meta,
        "probability_parity_passed": probability_ok,
        "signal_parity_passed": signal_ok,
        "feature_readiness_parity_passed": feature_ok,
        "source_reproduction_passed": reproduction_ok,
        "threshold": context["threshold"],
        "runtime_threshold": context["runtime_threshold"],
        "threshold_epsilon": THRESHOLD_EPSILON,
        "short_threshold": short_threshold,
        "long_threshold": long_threshold,
        "min_margin": -1.0,
        "decision_mode": "threshold_margin",
        "trade_shape": f"{side}_same_bar_open_hold{target.get('hold_bars')}_tp{target.get('tp_broker_points')}_sl{target.get('sl_broker_points')}",
        "tp_price_units": target.get("tp_price_units"),
        "sl_price_units": target.get("sl_price_units"),
        "tp_broker_points": target.get("tp_broker_points"),
        "sl_broker_points": target.get("sl_broker_points"),
        "runtime_claim_ceiling": "runtime_probe_quality_observation_only",
    }
    if probability_ok and signal_ok and feature_ok and reproduction_ok:
        for local_path, common_key, copy_key in (
            (patched_onnx_path, "model_common_path", "model_common_copy"),
            (feature_csv_path, "feature_common_path", "feature_common_copy"),
            (veto_path, "runtime_veto_tape_common_path", "runtime_veto_tape_common_copy"),
        ):
            common_path = f"{COMMON_RUN_ROOT}/{local_path.parent.name}/{local_path.name}"
            artifact[common_key] = common_path
            artifact[copy_key] = f71d.mt5.copy_to_common_files(common_files_root, local_path, common_path)
    artifact["export_status"] = "runtime_probe_parity_passed" if probability_ok and signal_ok and feature_ok and reproduction_ok else "runtime_probe_parity_failed"
    return artifact, probability, signal, feature_parity


def build_attempts(context: Mapping[str, Any], artifact: Mapping[str, Any], *, include_oos: bool) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    target = context["target"]
    spec = context["spec"]
    splits = ("validation", "oos") if include_oos else ("validation",)
    side = str(target["side"])
    short_threshold = 1.1 if side == "long" else float(context["runtime_threshold"])
    long_threshold = float(context["runtime_threshold"]) if side == "long" else 1.1
    for split in splits:
        from_date, to_date = f71d.split_dates(context["frame"], split)
        split_mask = context["frame"]["split"].astype(str).eq(split).to_numpy(dtype=bool)
        expected_selected = int((context["selected"] & split_mask).sum())
        attempt_name = f"{ATTEMPT_PREFIX}_{split}"
        extra = {
            "InpSameDirectionReentryCooldownBars": 0,
            "InpReentryCooldownBars": 0,
            "InpAtrSltpEnabled": True,
            "InpAtrStopMultiplier": 1.0,
            "InpAtrTakeProfitMultiplier": 1.0,
            "InpAtrMinStopPoints": float(target.get("sl_broker_points", spec.sl_price_units * f80b.SLTP_POINT_SCALE)),
            "InpAtrMaxStopPoints": float(target.get("sl_broker_points", spec.sl_price_units * f80b.SLTP_POINT_SCALE)),
            "InpAtrMinTakeProfitPoints": float(target.get("tp_broker_points", spec.tp_price_units * f80b.SLTP_POINT_SCALE)),
            "InpAtrMaxTakeProfitPoints": float(target.get("tp_broker_points", spec.tp_price_units * f80b.SLTP_POINT_SCALE)),
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
            stage_number=80,
            exploration_label=EXPLORATION_LABEL,
            attempt_name=attempt_name,
            tier=f71d.mt5.TIER_A,
            split=split,
            model_path=str(artifact["model_common_path"]),
            model_id=f"F80D_{artifact['candidate_id']}",
            model_backend="onnx",
            feature_path=str(artifact["feature_common_path"]),
            feature_count=len(context["features"]),
            feature_order_hash=str(context["feature_order_hash"]),
            short_threshold=short_threshold,
            long_threshold=long_threshold,
            min_margin=-1.0,
            invert_signal=False,
            from_date=from_date,
            to_date=to_date,
            primary_active_tier=f71d.mt5.TIER_A,
            attempt_role=ATTEMPT_ROLE,
            record_view_prefix=RECORD_VIEW_PREFIX,
            max_hold_bars=int(spec.hold_bars),
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
                "axis_id": f"{side}_h{target.get('hold_bars')}_tp{target.get('tp_price_units')}_sl{target.get('sl_price_units')}_{target.get('feature_set')}_{target.get('model')}_{target.get('regime')}_{target.get('risk_filter')}_q{target.get('prob_quantile')}",
                "expected_rows": int(split_mask.sum()),
                "expected_signal_count": expected_selected,
                "expected_selected_trade_count": expected_selected,
                "proxy_kpi": context["proxy_kpi_by_split"].get(split, {}),
                "runtime_threshold": float(context["runtime_threshold"]),
                "threshold_epsilon": THRESHOLD_EPSILON,
                "claim_boundary": CLAIM_BOUNDARY,
                "trade_shape": artifact["trade_shape"],
                "source_label_name": target.get("label_name"),
                "feature_set": target.get("feature_set"),
                "model_family": target.get("model"),
                "surface_family": target.get("surface_family"),
                "regime": target.get("regime"),
                "risk_filter": target.get("risk_filter"),
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
    best = {}
    if completed:
        best = max(completed, key=lambda row: as_float(row.get("net_profit")))
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": payload.get("status"),
        "judgment": payload.get("judgment"),
        "target_candidate_id": (payload.get("target") or {}).get("candidate_id"),
        "artifact_export_status": (payload.get("artifact_rows") or [{}])[0].get("export_status"),
        "attempt_count": len(payload.get("attempts") or []),
        "execution_result_count": len(payload.get("execution_results") or []),
        "completed_attempt_count": len(completed),
        "probability_parity_pass_rows": sum(1 for row in payload.get("probability_parity") or [] if row.get("passed")),
        "signal_parity_pass_rows": sum(1 for row in payload.get("signal_parity") or [] if row.get("passed")),
        "feature_readiness_pass_rows": sum(1 for row in payload.get("feature_readiness_parity") or [] if row.get("feature_readiness_parity")),
        "source_reproduction_pass_rows": sum(1 for row in payload.get("source_reproduction") or [] if row.get("passed")),
        "best_runtime": best,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def runtime_parity_receipt(payload: Mapping[str, Any]) -> dict[str, Any]:
    artifact = (payload.get("artifact_rows") or [{}])[0]
    return {
        "packet_id": RUN_ID,
        "skill": "obsidian-runtime-parity",
        "status": payload.get("status"),
        "python_artifact": artifact.get("model_path"),
        "runtime_artifact": artifact.get("patched_onnx_path"),
        "compared_surface": "Python probability, ONNX probability, selected-entry veto signal(파이썬 확률/ONNX 확률/선택 진입 거부 신호)",
        "parity_level": artifact.get("export_status"),
        "tester_identity": {"terminal_path": payload.get("terminal_path"), "stage_id": STAGE_ID, "run_id": RUN_ID},
        "missing_evidence": [] if payload.get("runtime_receipt") else ["Strategy Tester output(전략 테스터 출력) missing or not run."],
        "allowed_claims": ["runtime_probe_quality_observation"],
        "forbidden_claims": ["completion", "selected_baseline", "operating_promotion", "runtime_authority", "live_readiness", "goal_achieve"],
    }


def backtest_forensics_receipt(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "packet_id": RUN_ID,
        "skill": "obsidian-backtest-forensics",
        "status": payload.get("status"),
        "tester_report": [row.get("report_path") for row in payload.get("runtime_receipt") or [] if row.get("report_path")],
        "tester_settings": [attempt.get("ini", {}).get("path") for attempt in payload.get("attempts") or []],
        "spread_commission_slippage": "broker tester environment(브로커 테스터 환경); exact report fields required for economics claim(경제성 주장에는 보고서 필드 필요)",
        "trade_list_identity": [row.get("deal_list_path") for row in payload.get("runtime_receipt") or [] if row.get("deal_list_path")],
        "forensic_gaps": [] if payload.get("runtime_receipt") else ["No completed Strategy Tester report(완료된 전략 테스터 보고서 없음)."],
    }


def report_text(payload: Mapping[str, Any], summary: Mapping[str, Any], created_at: str) -> str:
    target = payload.get("target") or {}
    best = summary.get("best_runtime") or {}
    return f"""# F80D MT5 Runtime Probe Quality Report(F80D MT5 런타임 탐침 품질 보고서)

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

F80C(전선80C)의 materialization target(물질화 대상)을 ONNX(온엑스), feature CSV(피처 CSV), selected-entry veto tape(선택 진입 거부 테이프), Strategy Tester attempt(전략 테스터 시도)로 물질화하고 실행을 시도했다.

Effect(효과): Python proxy(파이썬 프록시)와 MT5 runtime(런타임)을 같은 후보 표면으로 연결했지만, 결과는 runtime probe quality observation(런타임 탐침 품질 관찰)만 만든다.

## Parity/Execution(동등성/실행)

- probability parity rows(확률 동등성 행): `{summary.get('probability_parity_pass_rows')}`
- signal parity rows(신호 동등성 행): `{summary.get('signal_parity_pass_rows')}`
- feature readiness rows(피처 준비 행): `{summary.get('feature_readiness_pass_rows')}`
- source reproduction rows(원천 재현 행): `{summary.get('source_reproduction_pass_rows')}`
- best runtime(최선 런타임): `{best}`

## Boundary(경계)

This report(이 보고서)는 completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)를 만들지 않는다.
"""


def gate_audit_text(payload: Mapping[str, Any], summary: Mapping[str, Any]) -> str:
    return f"""# F80D Required Gate Coverage Audit(F80D 필수 게이트 커버리지 감사)

Status(상태): `{payload.get('status')}`

| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |
|---|---|---|---|
| `materialization_target` | `passed(통과)` | `{rel(TARGET_SELECTION)}` | F80C(전선80C) 대상만 물질화한다. |
| `onnx_probability_parity` | `{summary.get('probability_parity_pass_rows')}` | `{rel(RUN_DIR / 'f80d_probability_parity.csv')}` | Python/ONNX(파이썬/온엑스) 확률 차이를 확인한다. |
| `runtime_signal_veto_parity` | `{summary.get('signal_parity_pass_rows')}` | `{rel(RUN_DIR / 'f80d_signal_parity.csv')}` | 선택 진입 시각이 런타임 입력으로 보존되는지 확인한다. |
| `strategy_tester_attempt` | `{summary.get('completed_attempt_count')}/{summary.get('attempt_count')}` | `{rel(RUN_MANIFEST)}` | MT5 Strategy Tester(전략 테스터) 출력 여부를 기록한다. |
| `final_claim_guard` | `passed(통과)` | `{CLAIM_BOUNDARY}` | 런타임 권위/실거래 준비를 만들지 않는다. |
"""


def ledger_row(payload: Mapping[str, Any], summary: Mapping[str, Any], created_at: str) -> dict[str, Any]:
    target = payload.get("target") or {}
    best = summary.get("best_runtime") or {}
    return {
        "ledger_row_id": f"{RUN_ID}__runtime_probe_quality",
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "subrun_id": "runtime_probe_quality(런타임 탐침 품질)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "MT5 runtime probe quality(MT5 런타임 탐침 품질)",
        "tier_scope": "Tier A separate; Tier B missing_required; combined out_of_scope_by_claim",
        "kpi_scope": "mt5_runtime_probe_quality(MT5 런타임 탐침 품질)",
        "scoreboard_lane": "runtime_economics(런타임 경제성)",
        "lane": "runtime_probe_quality(런타임 탐침 품질)",
        "family": "runtime_backtest(런타임/백테스트)",
        "status": payload.get("status"),
        "judgment": payload.get("judgment"),
        "path": rel(REPORT),
        "primary_kpi": f"attempts={summary.get('attempt_count')};completed={summary.get('completed_attempt_count')}",
        "guardrail_kpi": f"prob_parity={summary.get('probability_parity_pass_rows')};signal_parity={summary.get('signal_parity_pass_rows')}",
        "external_verification_status": "completed" if summary.get("completed_attempt_count") else "attempted_or_materialized_no_completed_report",
        "notes": f"target={target.get('candidate_id')}; best_runtime={best}",
        "run_number": "frontier80D",
        "date": created_at[:10],
        "decision": payload.get("judgment"),
        "next_run_id": NEXT_RUN_ID,
        "rows": summary.get("attempt_count"),
        "gate_passes": 5 if summary.get("completed_attempt_count") else 4,
        "gate_total": 5,
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
        "view": "runtime_probe_quality",
        "tier": "Tier A",
        "metric_scope": "mt5_runtime_probe",
        "result_status": payload.get("status"),
        "feature_count": target.get("feature_count", ""),
        "work_family": "runtime_backtest",
        "row_id": f"{RUN_ID}__runtime_probe_quality",
        "evidence_boundary": "runtime_probe_quality_only_no_authority(런타임 탐침 품질만, 권위 없음)",
        "next_action": NEXT_RUN_ID,
        "created_at_utc": created_at,
        "required_gate_audit": rel(GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "runtime_probe_quality_only(런타임 탐침 품질만)",
    }


def update_state_files(payload: Mapping[str, Any], summary: Mapping[str, Any], created_at: str) -> None:
    state = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {payload.get('status')}
current_judgment: {payload.get('judgment')}
next_run_id: {NEXT_RUN_ID}
runtime_probe_status: f80_runtime_probe_quality_recorded_completed_attempts_{summary.get('completed_attempt_count')}
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
five_stage_retrospective_due_status: inactive_preserve_records_pending_codex_task_force_replacement
updated_at_utc: '{created_at}'
context_anchor: {rel(CONTEXT_ANCHOR)}
notes:
  - "Action(행동): F80D MT5 runtime probe quality(MT5 런타임 탐침 품질)를 물질화하고 실행을 시도했다."
  - "Effect(효과): attempts={summary.get('attempt_count')}, completed={summary.get('completed_attempt_count')}를 기록했다."
  - "Boundary(경계): runtime authority/live readiness/Goal Achieve(런타임 권위/실거래 준비/목표 달성) 없음."
"""
    write_text(WORKSPACE_STATE, state)
    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Action(행동): F80D MT5 runtime probe quality(F80D MT5 런타임 탐침 품질)를 실행했다.

Effect(효과): MT5 Strategy Tester(전략 테스터) 시도 `{summary.get('attempt_count')}`개와 완료 `{summary.get('completed_attempt_count')}`개를 기록했다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(CURRENT_WORKING_STATE, current)


def update_review_index() -> None:
    text = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX) else "# F80 Review Index(F80 검토 색인)\n"
    for line in [
        "- `frontier80D_mt5_runtime_probe_quality_report.md`: F80D MT5 runtime probe quality report(F80D MT5 런타임 탐침 품질 보고서)",
        "- `f80d_mt5_runtime_probe_quality_summary.json`: F80D runtime summary(F80D 런타임 요약)",
        "- `required_gate_coverage_audit_f80d.md`: F80D gate audit(F80D 게이트 감사)",
        "- `f80d_runtime_parity_receipt.json`: F80D runtime parity receipt(F80D 런타임 동등성 영수증)",
        "- `f80d_backtest_forensics_receipt.json`: F80D backtest forensics receipt(F80D 백테스트 포렌식 영수증)",
    ]:
        if line not in text:
            text = text.rstrip() + "\n" + line + "\n"
    write_text(REVIEW_INDEX, text)


def update_idea_registry(payload: Mapping[str, Any], summary: Mapping[str, Any]) -> None:
    text = io_path(IDEA_REGISTRY).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTRY) else "# Idea Registry(아이디어 등록부)\n"
    if RUN_ID in text:
        return
    target = payload.get("target") or {}
    addition = f"""

- `{RUN_ID}` attempted F80 MT5 runtime probe quality(F80 MT5 런타임 탐침 품질). Target(대상): `{target.get('candidate_id')}`. Attempts(시도): `{summary.get('attempt_count')}`, completed(완료): `{summary.get('completed_attempt_count')}`. Boundary(경계): runtime probe quality only, no authority(런타임 탐침 품질만, 권위 없음).
"""
    write_text(IDEA_REGISTRY, text.rstrip() + addition)


def main() -> int:
    args = parse_args()
    ensure_dirs()
    created_at = utc_now()
    target = target_row()
    context = build_context(target)
    artifact, probability, signal, feature_parity = materialize(context, Path(args.common_files_root))
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
        judgment = "runtime_materialization_invalid_repair_required_no_authority"
    elif args.execute and completed:
        status = "completed_mt5_runtime_probe_quality_observation_no_authority"
        judgment = "runtime_probe_quality_completed_gap_attribution_required_no_authority"
    elif args.execute:
        status = "blocked_mt5_runtime_probe_attempted_no_authority"
        judgment = "runtime_probe_blocked_or_missing_output_repair_required_no_authority"
    else:
        status = "materialized_pending_mt5_runtime_probe_execution_no_authority"
        judgment = "runtime_probe_materialized_pending_execution_no_authority"
    payload = {
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
        "source_reproduction": context["reproduction_rows"],
        "attempts": attempts,
        "compile_payload": compile_payload,
        "execution_results": execution_results,
        "runtime_receipt": runtime_receipt,
        "terminal_path": str(args.terminal_path),
        "claim_boundary": CLAIM_BOUNDARY,
        "producer": SCRIPT_REL,
        "producer_sha256": sha256_file_lf_normalized(ROOT / SCRIPT_REL),
    }
    summary = build_summary(payload)
    runtime_parity = runtime_parity_receipt(payload)
    backtest_forensics = backtest_forensics_receipt(payload)
    payload["runtime_parity"] = runtime_parity
    payload["backtest_forensics"] = backtest_forensics
    write_json(RUNTIME_PARITY, runtime_parity)
    write_json(BACKTEST_FORENSICS, backtest_forensics)
    write_json(RUN_MANIFEST, payload)
    write_json(SUMMARY, summary)
    write_csv(RUN_DIR / "f80d_probability_parity.csv", probability)
    write_csv(RUN_DIR / "f80d_signal_parity.csv", signal)
    write_csv(RUN_DIR / "f80d_feature_readiness_parity.csv", feature_parity)
    write_csv(RUN_DIR / "f80d_source_reproduction.csv", context["reproduction_rows"])
    write_csv(RUN_DIR / "f80d_runtime_receipt.csv", runtime_receipt, f71d.RUNTIME_RECEIPT_COLUMNS)
    write_json(RUN_DIR / "f80d_execution_results.json", execution_results)
    write_text(REPORT, report_text(payload, summary, created_at))
    write_text(GATE_AUDIT, gate_audit_text(payload, summary))
    write_text(SELECTION_STATUS, selection_status_text(payload, summary, created_at))
    write_text(CONTEXT_ANCHOR, context_anchor_text(payload, summary, created_at))
    row = ledger_row(payload, summary, created_at)
    upsert_csv(RUN_REGISTRY, "run_id", row)
    upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
    upsert_csv(STAGE_LEDGER, "ledger_row_id", row, source_header=ALPHA_LEDGER)
    update_state_files(payload, summary, created_at)
    update_review_index()
    update_idea_registry(payload, summary)
    print(json.dumps(json_ready({"status": status, "judgment": judgment, "attempt_count": summary["attempt_count"], "completed_attempt_count": summary["completed_attempt_count"], "parity": {"probability": summary["probability_parity_pass_rows"], "signal": summary["signal_parity_pass_rows"], "feature": summary["feature_readiness_pass_rows"], "reproduction": summary["source_reproduction_pass_rows"]}, "next_run_id": NEXT_RUN_ID}), ensure_ascii=False, indent=2))
    return 0


def selection_status_text(payload: Mapping[str, Any], summary: Mapping[str, Any], created_at: str) -> str:
    return f"""# F80 Selection Status(F80 선택 상태)

Updated(갱신): {created_at}

Status(상태): `{payload.get('status')}`

Judgment(판정): `{payload.get('judgment')}`

Action(행동): F80D MT5 runtime probe quality(F80D MT5 런타임 탐침 품질)를 실행했다.

Effect(효과): Strategy Tester attempt(전략 테스터 시도) `{summary.get('attempt_count')}`개, completed(완료) `{summary.get('completed_attempt_count')}`개를 기록했다.

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""


def context_anchor_text(payload: Mapping[str, Any], summary: Mapping[str, Any], created_at: str) -> str:
    return f"""# F80 Context Anchor(F80 문맥 앵커)

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


if __name__ == "__main__":
    raise SystemExit(main())
