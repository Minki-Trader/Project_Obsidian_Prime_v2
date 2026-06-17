from __future__ import annotations

import argparse
import csv
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import numpy as np
import onnx
import pandas as pd
from onnx import TensorProto, helper, numpy_helper

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.control_plane.mt5_tier_balance_completion import attempt_payload
from foundation.models.onnx_bridge import ordered_hash, sha256_file
from stage_pipelines.stage_frontier_71 import frontier71d_mt5_runtime_probe_economics_native_scout as f71d
from stage_pipelines.stage_frontier_74 import frontier74e_mt5_microburst_negative_control_runtime_probe as f74e
from stage_pipelines.stage_frontier_76 import frontier76b_axis_ablation_proxy_scout as f76b
from stage_pipelines.stage_frontier_runtime_backfill.run_frontier_runtime_probe_backfill import (
    DEFAULT_COMMON_FILES,
    DEFAULT_METAEDITOR,
    DEFAULT_PORTABLE_ROOT,
    DEFAULT_TERMINAL,
    DEFAULT_TESTER_PROFILE_ROOT,
    EA_BINARY,
    PORTABLE_EA_BINARY,
)


STAGE_ID = f76b.STAGE_ID
RUN_ID = "frontier76D_mt5_axis_ablation_runtime_probe_v1"
PARENT_RUN_ID = "frontier76C_pre_mt5_grok_axis_ablation_runtime_probe_v1"
NEXT_RUN_ID = "frontier76E_proxy_runtime_gap_analysis_and_repair_decision_v1"
SOURCE_CANDIDATE_ID = "f76b_06637"
TARGET_CANDIDATE_ID = f"f76d_runtime_{SOURCE_CANDIDATE_ID}"
COMMON_RUN_ROOT = "Project_Obsidian_Prime_v2/frontier76D_mt5_axis_ablation_runtime_probe"
THRESHOLD_EPSILON = 1e-7
CLAIM_BOUNDARY = (
    "runtime_probe_observation_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
MODEL_DIR = RUN_DIR / "models"
FEATURE_DIR = RUN_DIR / "features"
VETO_DIR = RUN_DIR / "runtime_veto_tapes"
MT5_DIR = RUN_DIR / "mt5"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
SUMMARY_PATH = REVIEW_DIR / "f76b_summary.json"
REPORT_PATH = REVIEW_DIR / "frontier76D_mt5_axis_ablation_runtime_probe_report.md"
GATE_AUDIT_PATH = REVIEW_DIR / "required_gate_coverage_audit_f76d.md"
RUN_MANIFEST_PATH = RUN_DIR / "run_manifest.json"
CONTEXT_ANCHOR_PATH = f"stages/{STAGE_ID}/03_reviews/context_anchor.md"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="F76D MT5 axis-ablation runtime probe.")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=600)
    parser.add_argument("--wait-timeout-seconds", type=int, default=300)
    parser.add_argument("--terminal-path", default=str(DEFAULT_TERMINAL))
    parser.add_argument("--metaeditor-path", default=str(DEFAULT_METAEDITOR))
    parser.add_argument("--common-files-root", default=str(DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(DEFAULT_PORTABLE_ROOT))
    return parser.parse_args()


def now_utc() -> str:
    return f76b.utc_now()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_text(path: Path, text: str, *, encoding: str = "utf-8-sig") -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding=encoding)


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    rows = list(rows)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = list(columns or (rows[0].keys() if rows else ["empty"]))
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({name: json_ready(row.get(name, "")) for name in fieldnames})


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def upsert_csv(path: Path, key: str, row: Mapping[str, Any]) -> None:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = [existing for existing in reader if existing.get(key) != row.get(key)]
    rows.append({name: json_ready(row.get(name, "")) for name in fieldnames})
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def ensure_dirs() -> None:
    for path in (RUN_DIR, MODEL_DIR, FEATURE_DIR, VETO_DIR, MT5_DIR, MT5_DIR / "reports", REVIEW_DIR):
        io_path(path).mkdir(parents=True, exist_ok=True)


def load_summary() -> Mapping[str, Any]:
    summary = read_json(SUMMARY_PATH)
    best = summary["best_candidate"]
    if best["candidate_id"] != SOURCE_CANDIDATE_ID:
        raise RuntimeError(f"candidate_lock_failed:{best['candidate_id']}")
    return summary


def cleaned_full_frame(frame: pd.DataFrame, features: Sequence[str]) -> pd.DataFrame:
    out = frame.copy()
    train = out.loc[out["split"].astype(str).eq("train"), list(features)].replace([np.inf, -np.inf], np.nan)
    med = train.median(numeric_only=True).fillna(0.0)
    out.loc[:, list(features)] = out.loc[:, list(features)].replace([np.inf, -np.inf], np.nan).fillna(med).astype(float)
    return out


def split_selected_mask(frame: pd.DataFrame, selected: np.ndarray, split: str) -> np.ndarray:
    return selected[frame["split"].astype(str).eq(split).to_numpy(dtype=bool)]


def normalized_proxy_kpi(metrics: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "net_profit": metrics.get("net"),
        "gross_profit": metrics.get("gross_profit"),
        "gross_loss": metrics.get("gross_loss"),
        "profit_factor": metrics.get("pf"),
        "max_drawdown_percent": metrics.get("dd_pct"),
        "trade_count": metrics.get("trade_count"),
        "trades_day": metrics.get("trades_day"),
        "win_rate": metrics.get("win_rate"),
        "average_win": metrics.get("avg_win"),
        "average_loss": metrics.get("avg_loss"),
        "payoff_ratio": metrics.get("payoff"),
        "expectancy": metrics.get("expectancy"),
        "recovery_factor": metrics.get("recovery"),
    }


def build_context(summary: Mapping[str, Any]) -> dict[str, Any]:
    best = summary["best_candidate"]
    if best["feature_set"] != "mega_cap_removed" or best["target"] != "long_fwd12_q60" or best["model"] != "extra_trees_d7_l60":
        raise RuntimeError("candidate_axis_lock_failed")
    frame = pd.read_parquet(io_path(f76b.DATASET_PATH)).copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True, errors="coerce")
    features = f76b.feature_sets(f76b.feature_order())[best["feature_set"]]
    if len(features) != int(best["feature_count"]):
        raise RuntimeError(f"feature_count_lock_failed:{len(features)}")
    train_mask = frame["split"].astype(str).eq("train")
    train_threshold = float(frame.loc[train_mask, "future_log_return_12"].astype(float).quantile(0.60))
    if abs(train_threshold - float(best["target_threshold"])) > 1e-12:
        raise RuntimeError(f"target_threshold_drift:{train_threshold}:{best['target_threshold']}")
    clean_frame = cleaned_full_frame(frame, features)
    matrices = f76b.clean_matrices(frame, train_mask, features)
    y_train = f76b.make_target(frame.loc[train_mask, "future_log_return_12"], f76b.TargetSpec(best["target"], "long", train_threshold, ">"))
    model = f76b.model_builders()["extra_trees_d7_l60"]()
    model.fit(matrices["train"], y_train)
    proba = f74e.binary_probabilities(model, clean_frame.loc[:, features])
    score = proba[:, 1]
    threshold = float(best["prob_threshold"])
    thresholds = f76b.risk_thresholds(frame.loc[train_mask])
    event_mask = (
        f76b.session_mask(clean_frame, "cash_open")
        & f76b.risk_mask(clean_frame, "trend_aligned", "long", thresholds)
        & np.isfinite(score)
    )
    selected = event_mask & (score >= threshold)
    selected = f76b.apply_cooldown(selected, int(best["cooldown_bars"]))
    proxy_by_split: dict[str, dict[str, Any]] = {}
    reproduction_rows: list[dict[str, Any]] = []
    for split, prefix in (("validation", "val"), ("oos", "oos")):
        split_frame = clean_frame.loc[clean_frame["split"].astype(str).eq(split)].reset_index(drop=True)
        split_mask = split_selected_mask(clean_frame, selected, split)
        metrics = f76b.kpi(split_frame, split_mask, "long")
        proxy_by_split[split] = normalized_proxy_kpi(metrics)
        reproduction_rows.append(
            {
                "split": split,
                "source_candidate_id": SOURCE_CANDIDATE_ID,
                "source_net_profit": best[f"{prefix}_net"],
                "source_profit_factor": best[f"{prefix}_pf"],
                "source_max_drawdown_percent": best[f"{prefix}_dd_pct"],
                "source_trades_day": best[f"{prefix}_trades_day"],
                "source_trade_count": best[f"{prefix}_trade_count"],
                "reproduced_net_profit": metrics["net"],
                "reproduced_profit_factor": metrics["pf"],
                "reproduced_max_drawdown_percent": metrics["dd_pct"],
                "reproduced_trades_day": metrics["trades_day"],
                "reproduced_trade_count": metrics["trade_count"],
                "count_diff": int(metrics["trade_count"]) - int(best[f"{prefix}_trade_count"]),
                "net_diff": float(metrics["net"]) - float(best[f"{prefix}_net"]),
                "pf_diff": float(metrics["pf"]) - float(best[f"{prefix}_pf"]),
                "dd_diff": float(metrics["dd_pct"]) - float(best[f"{prefix}_dd_pct"]),
                "passed": bool(
                    int(metrics["trade_count"]) == int(best[f"{prefix}_trade_count"])
                    and abs(float(metrics["net"]) - float(best[f"{prefix}_net"])) <= 1e-6
                    and abs(float(metrics["pf"]) - float(best[f"{prefix}_pf"])) <= 1e-9
                ),
            }
        )
    return {
        "frame": clean_frame,
        "features": list(features),
        "feature_order_hash": ordered_hash(features),
        "model": model,
        "binary_proba": proba,
        "score": score,
        "event_mask": event_mask,
        "selected": selected,
        "proxy_kpi_by_split": proxy_by_split,
        "reproduction_rows": reproduction_rows,
        "target_threshold": train_threshold,
        "prob_threshold": threshold,
        "runtime_threshold": threshold - THRESHOLD_EPSILON,
        "threshold_epsilon": THRESHOLD_EPSILON,
        "summary_best": best,
    }


def patch_binary_onnx_to_long_three_columns(binary_path: Path, patched_path: Path) -> dict[str, Any]:
    model = onnx.load(str(io_path(binary_path)))
    prob_name = f74e.find_binary_probability_output(model)
    axes = numpy_helper.from_array(np.asarray([1], dtype=np.int64), name="slice_axes_col")
    steps = numpy_helper.from_array(np.asarray([1], dtype=np.int64), name="slice_steps_col")
    start0 = numpy_helper.from_array(np.asarray([0], dtype=np.int64), name="slice_start_col0")
    end1 = numpy_helper.from_array(np.asarray([1], dtype=np.int64), name="slice_end_col1")
    start1 = numpy_helper.from_array(np.asarray([1], dtype=np.int64), name="slice_start_col1")
    end2 = numpy_helper.from_array(np.asarray([2], dtype=np.int64), name="slice_end_col2")
    zero_scalar = numpy_helper.from_array(np.asarray([0.0], dtype=np.float32), name="zero_scalar")
    model.graph.initializer.extend([axes, steps, start0, end1, start1, end2, zero_scalar])
    model.graph.node.extend(
        [
            helper.make_node("Slice", [prob_name, "slice_start_col0", "slice_end_col1", "slice_axes_col", "slice_steps_col"], ["flat_col"], name="SliceFlatProbability"),
            helper.make_node("Slice", [prob_name, "slice_start_col1", "slice_end_col2", "slice_axes_col", "slice_steps_col"], ["long_col"], name="SliceLongProbability"),
            helper.make_node("Mul", ["flat_col", "zero_scalar"], ["short_zero_col"], name="BuildZeroShortProbability"),
            helper.make_node("Concat", ["short_zero_col", "flat_col", "long_col"], ["probabilities_3"], name="BuildThreeColumnProbability", axis=1),
        ]
    )
    del model.graph.output[:]
    model.graph.output.extend([helper.make_tensor_value_info("probabilities_3", TensorProto.FLOAT, [None, 3])])
    onnx.checker.check_model(model)
    io_path(patched_path.parent).mkdir(parents=True, exist_ok=True)
    onnx.save(model, str(io_path(patched_path)))
    return {
        "binary_probability_output": prob_name,
        "patched_probability_output": "probabilities_3",
        "path": rel(patched_path),
        "sha256": sha256_file(patched_path),
        "schema": "[p_short=0,p_flat,p_long]",
    }


def parity_rows(context: Mapping[str, Any], raw_onnx_path: Path, patched_onnx_path: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    frame = context["frame"]
    features = context["features"]
    probability_rows: list[dict[str, Any]] = []
    signal_rows: list[dict[str, Any]] = []
    runtime_threshold = float(context["runtime_threshold"])
    for split in ("train", "validation", "oos"):
        subset = frame.loc[frame["split"].astype(str).eq(split)]
        idx = subset.index.to_numpy()
        values = subset.loc[:, features].to_numpy(dtype="float64")
        binary_expected = context["binary_proba"][idx]
        patched_expected = np.column_stack([np.zeros(len(binary_expected)), binary_expected[:, 0], binary_expected[:, 1]])
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
                "patched_short_col_max_abs": float(np.abs(patched_actual[:, 0]).max()) if len(patched_actual) else 0.0,
                "passed": bool((float(raw_diff.max()) if raw_diff.size else 0.0) <= 1e-5 and (float(patched_diff.max()) if patched_diff.size else 0.0) <= 1e-5),
            }
        )
        all_patched = f74e.onnx_probability(patched_onnx_path, values, 3)
        onnx_raw_signal = context["event_mask"][idx] & (all_patched[:, 2] >= runtime_threshold)
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
                "passed": bool(int((onnx_vetoed_signal != selected_expected).sum()) == 0),
            }
        )
    return probability_rows, signal_rows


def materialize(context: Mapping[str, Any], common_files_root: Path) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    model_path = MODEL_DIR / f"{TARGET_CANDIDATE_ID}.joblib"
    raw_onnx_path = MODEL_DIR / f"{TARGET_CANDIDATE_ID}.binary_raw.onnx"
    patched_onnx_path = MODEL_DIR / f"{TARGET_CANDIDATE_ID}.onnx"
    feature_order_path = MODEL_DIR / f"{TARGET_CANDIDATE_ID}_feature_order.txt"
    feature_csv_path = FEATURE_DIR / f"{TARGET_CANDIDATE_ID}_features.csv"
    veto_path = VETO_DIR / f"{TARGET_CANDIDATE_ID}_selected_entry_runtime_veto_tape.csv"
    joblib.dump(context["model"], io_path(model_path))
    io_path(feature_order_path).write_text("\n".join(context["features"]) + "\n", encoding="utf-8")
    raw_export = f74e.export_binary_sklearn_to_onnx(context["model"], raw_onnx_path, len(context["features"]))
    patch_meta = patch_binary_onnx_to_long_three_columns(raw_onnx_path, patched_onnx_path)
    feature_meta = f71d.mt5.export_mt5_feature_matrix_csv(context["frame"], context["features"], feature_csv_path, metadata_columns=("split",))
    veto_meta = f71d.selected_entry_tape(context["frame"], context["selected"], context["event_mask"], veto_path)
    probability, signal = parity_rows(context, raw_onnx_path, patched_onnx_path)
    feature_parity = [
        {
            "candidate_id": TARGET_CANDIDATE_ID,
            "expected_feature_count": 48,
            "actual_feature_count": len(context["features"]),
            "feature_order_hash": context["feature_order_hash"],
            "feature_csv_feature_count": feature_meta.get("feature_count"),
            "feature_csv_rows": feature_meta.get("rows"),
            "feature_readiness_parity": bool(len(context["features"]) == 48 and feature_meta.get("feature_count") == 48),
        }
    ]
    probability_ok = all(row.get("passed") for row in probability)
    signal_ok = all(row.get("passed") for row in signal)
    feature_ok = bool(feature_parity[0]["feature_readiness_parity"])
    reproduction_ok = all(row.get("passed") for row in context["reproduction_rows"])
    artifact = {
        "candidate_id": TARGET_CANDIDATE_ID,
        "source_candidate_id": SOURCE_CANDIDATE_ID,
        "materialization_mode": "long_binary_onnx_three_column_selected_entry_runtime_probe",
        "model_path": rel(model_path),
        "model_sha256": sha256_file(model_path),
        "raw_binary_onnx_path": rel(raw_onnx_path),
        "raw_binary_onnx_sha256": sha256_file(raw_onnx_path),
        "patched_onnx_path": rel(patched_onnx_path),
        "patched_onnx_sha256": sha256_file(patched_onnx_path),
        "feature_order_path": rel(feature_order_path),
        "feature_order_sha256": sha256_file(feature_order_path),
        "feature_csv_path": rel(feature_csv_path),
        "feature_csv_sha256": sha256_file(feature_csv_path),
        "runtime_veto_tape_path": rel(veto_path),
        "runtime_veto_tape_sha256": sha256_file(veto_path),
        "raw_binary_export": raw_export,
        "patch_meta": patch_meta,
        "feature_csv": feature_meta,
        "runtime_veto_tape": veto_meta,
        "probability_parity_passed": probability_ok,
        "signal_parity_passed": signal_ok,
        "feature_readiness_parity_passed": feature_ok,
        "source_reproduction_passed": reproduction_ok,
        "target_threshold": context["target_threshold"],
        "prob_threshold": context["prob_threshold"],
        "runtime_threshold": context["runtime_threshold"],
        "threshold_epsilon": THRESHOLD_EPSILON,
        "long_threshold": context["runtime_threshold"],
        "short_threshold": 1.1,
        "min_margin": -1.0,
        "decision_mode": "threshold_margin",
        "trade_shape": "long_only_max_hold_12_no_atr_sltp",
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


def build_attempts(context: Mapping[str, Any], artifact: Mapping[str, Any]) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    for split in ("validation", "oos"):
        from_date, to_date = f71d.split_dates(context["frame"], split)
        split_mask = context["frame"]["split"].astype(str).eq(split).to_numpy(dtype=bool)
        expected = int((context["selected"] & split_mask).sum())
        attempt_name = f"f76d_axis_ablation_{split}"
        extra = {
            "InpSameDirectionReentryCooldownBars": 0,
            "InpReentryCooldownBars": 0,
            "InpAtrSltpEnabled": False,
            "InpAtrStopMultiplier": 0.0,
            "InpAtrTakeProfitMultiplier": 0.0,
            "InpAtrMinStopPoints": 0.0,
            "InpAtrMinTakeProfitPoints": 0.0,
            "InpDecisionMode": "threshold_margin",
            "InpFallbackDecisionMode": "threshold_margin",
            "InpRuntimeVetoTapeEnabled": True,
            "InpRuntimeVetoTapePath": str(artifact["runtime_veto_tape_common_path"]),
            "InpRuntimeVetoTapeUseCommonFiles": True,
            "InpRuntimeVetoTapeDelimiter": ",",
        }
        attempt = attempt_payload(
            run_root=RUN_DIR,
            run_id=RUN_ID,
            stage_number=76,
            exploration_label="frontier76D_axis_ablation_runtime_probe",
            attempt_name=attempt_name,
            tier=f71d.mt5.TIER_A,
            split=split,
            model_path=str(artifact["model_common_path"]),
            model_id=f"F76D_{TARGET_CANDIDATE_ID}",
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
            attempt_role="axis_ablation_meaningful_signal_runtime_probe",
            record_view_prefix="mt5_f76d_axis_ablation",
            max_hold_bars=12,
            common_root=COMMON_RUN_ROOT,
            close_on_flat_signal=False,
            reverse_on_opposite_signal=True,
            close_only_on_opposite_signal=False,
            extra_set_values=extra,
        )
        attempt.update(
            {
                "candidate_id": TARGET_CANDIDATE_ID,
                "source_candidate_id": SOURCE_CANDIDATE_ID,
                "axis_id": "f76d_mega_cap_removed_long_q60_cash_open_trend_aligned",
                "axis_role": "axis_ablation_meaningful_signal_runtime_probe",
                "expected_rows": int(split_mask.sum()),
                "expected_signal_count": expected,
                "expected_selected_trade_count": expected,
                "proxy_kpi": context["proxy_kpi_by_split"].get(split, {}),
                "label_id": "long_fwd12_q60",
                "feature_set_id": "mega_cap_removed",
                "model_id": "extra_trees_d7_l60",
                "selection_id": "cash_open_trend_aligned_q80",
                "mask_name": "selected_entry_veto_tape",
                "threshold": float(context["runtime_threshold"]),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        attempts.append(attempt)
    return attempts


def compile_runtime_ea(metaeditor_path: Path) -> dict[str, Any]:
    compile_payload = f71d.mt5.compile_mql5_ea(metaeditor_path, f71d.mt5.EA_SOURCE_PATH, MT5_DIR / "mt5_compile.log")
    portable_payload = {
        "repo_ea_ex5": rel(EA_BINARY),
        "portable_ea_ex5": PORTABLE_EA_BINARY.as_posix(),
        "portable_ea_ex5_exists_before": path_exists(PORTABLE_EA_BINARY),
        "copied": False,
    }
    if path_exists(EA_BINARY):
        io_path(PORTABLE_EA_BINARY.parent).mkdir(parents=True, exist_ok=True)
        shutil.copy2(io_path(EA_BINARY), io_path(PORTABLE_EA_BINARY))
        portable_payload.update(
            {
                "copied": True,
                "portable_ea_ex5_exists_after": path_exists(PORTABLE_EA_BINARY),
                "portable_ea_sha256": f71d.mt5.sha256_file(PORTABLE_EA_BINARY),
            }
        )
    return {"compile": compile_payload, "portable_ea": portable_payload}


def can_run_terminal(compile_payload: Mapping[str, Any]) -> bool:
    return ((compile_payload.get("compile") or {}).get("status") == "completed") or path_exists(PORTABLE_EA_BINARY)


def execute_attempts(args: argparse.Namespace, attempts: Sequence[Mapping[str, Any]], compile_payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for attempt in attempts:
        if not can_run_terminal(compile_payload):
            result = {"status": "blocked", "blocker": "compile_failed_and_portable_ea_missing"}
        else:
            f71d.clear_runtime_outputs(Path(args.common_files_root), attempt)
            f71d.mt5.remove_existing_mt5_report_artifacts(Path(args.terminal_data_root), attempt, run_id=RUN_ID)
            try:
                result = f71d.mt5.run_mt5_tester(
                    Path(args.terminal_path),
                    ROOT / str(attempt["ini"]["path"]),
                    set_path=ROOT / str(attempt["set"]["path"]),
                    tester_profile_set_path=Path(args.tester_profile_root) / f71d.mt5.EA_TESTER_SET_NAME,
                    tester_profile_ini_path=Path(args.tester_profile_root) / f"opv2_{attempt['attempt_name']}.ini",
                    timeout_seconds=int(args.timeout_seconds),
                    terminal_extra_args=["/portable"],
                )
            except subprocess.TimeoutExpired as exc:
                result = {
                    "status": "blocked",
                    "command": exc.cmd,
                    "stdout": (exc.stdout or "")[-2000:],
                    "stderr": (exc.stderr or "")[-2000:],
                    "blocker": "terminal_timeout",
                }
            runtime_outputs = f71d.mt5.wait_for_mt5_runtime_outputs(Path(args.common_files_root), attempt, timeout_seconds=int(args.wait_timeout_seconds), poll_seconds=2.0)
            if runtime_outputs.get("status") != "completed":
                result["status"] = "blocked"
                result.setdefault("blocker", "runtime_outputs_missing_or_init_failed")
            result["runtime_outputs"] = runtime_outputs
        result.update(
            {
                "attempt_name": attempt["attempt_name"],
                "tier": attempt["tier"],
                "split": attempt["split"],
                "candidate_id": attempt.get("candidate_id"),
                "source_candidate_id": attempt.get("source_candidate_id"),
                "expected_rows": attempt.get("expected_rows"),
                "expected_signal_count": attempt.get("expected_signal_count"),
                "expected_selected_trade_count": attempt.get("expected_selected_trade_count"),
                "ini_path": attempt.get("ini", {}).get("path"),
                "set_path": attempt.get("set", {}).get("path"),
            }
        )
        results.append(result)
    return results


def best_receipt(receipts: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    completed = [row for row in receipts if row.get("tester_status") == "completed"]
    rows = completed or list(receipts)
    return next((row for row in rows if row.get("split") == "oos"), rows[0] if rows else {})


def build_summary(payload: Mapping[str, Any]) -> dict[str, Any]:
    receipts = list(payload.get("runtime_receipt", []))
    probability = list(payload.get("probability_parity", []))
    signal = list(payload.get("signal_parity", []))
    feature = list(payload.get("feature_readiness_parity", []))
    reproduction = list(payload.get("source_reproduction", []))
    completed = sum(1 for row in receipts if row.get("tester_status") == "completed")
    best = best_receipt(receipts)
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": payload.get("status"),
        "judgment": payload.get("judgment"),
        "candidate_id": TARGET_CANDIDATE_ID,
        "source_candidate_id": SOURCE_CANDIDATE_ID,
        "attempt_count": len(payload.get("attempts", [])),
        "completed_attempt_count": completed,
        "probability_parity_pass_rows": sum(1 for row in probability if row.get("passed")),
        "signal_parity_pass_rows": sum(1 for row in signal if row.get("passed")),
        "feature_readiness_pass_rows": sum(1 for row in feature if row.get("feature_readiness_parity")),
        "source_reproduction_pass_rows": sum(1 for row in reproduction if row.get("passed")),
        "best_runtime": best,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def report_text(payload: Mapping[str, Any], created_at: str) -> str:
    summary = build_summary(payload)
    best = summary["best_runtime"]
    lines = [
        "# Frontier76D MT5 Axis Ablation Runtime Probe Report(F76D MT5 축 제거 런타임 탐침 보고서)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        f"- status(상태): `{payload.get('status')}`",
        f"- judgment(판정): `{payload.get('judgment')}`",
        f"- candidate(후보): `{TARGET_CANDIDATE_ID}` from `{SOURCE_CANDIDATE_ID}`",
        f"- attempts/completed(시도/완료): `{summary['attempt_count']}/{summary['completed_attempt_count']}`",
        f"- probability/signal/feature/reproduction parity pass(확률/신호/피처/재현 동등성 통과): `{summary['probability_parity_pass_rows']}/{summary['signal_parity_pass_rows']}/{summary['feature_readiness_pass_rows']}/{summary['source_reproduction_pass_rows']}`",
        f"- best runtime net/PF/DD/tpd(최선 런타임 순수익/수익 팩터/손실폭/일거래): `{best.get('net_profit', '')}/{best.get('profit_factor', '')}/{best.get('max_drawdown_percent', '')}/{best.get('trades_per_day', '')}`",
        f"- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Runtime KPI(런타임 핵심 성과 지표)",
        "",
        "| split(분할) | period(기간) | net(순수익) | gross profit(총이익) | gross loss(총손실) | PF(수익 팩터) | DD%(손실폭) | trades(거래) | trades/day(일거래) | win%(승률) | avg win(평균 이익) | avg loss(평균 손실) | payoff(손익비) | expectancy(기대값) | recovery(회복) | signal diff(신호 차이) | feature diff(피처 차이) | gap cause(간극 원인) |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in payload.get("runtime_receipt", []):
        period = f"{row.get('test_period_start', '')}..{row.get('test_period_end', '')}"
        lines.append(
            "| `{split}` | `{period}` | `{net}` | `{gp}` | `{gl}` | `{pf}` | `{dd}` | `{trades}` | `{tpd}` | `{win}` | `{avgw}` | `{avgl}` | `{payoff}` | `{exp}` | `{rec}` | `{sig}` | `{feat}` | `{gap}` |".format(
                split=row.get("split"),
                period=period,
                net=row.get("net_profit", ""),
                gp=row.get("gross_profit", ""),
                gl=row.get("gross_loss", ""),
                pf=row.get("profit_factor", ""),
                dd=row.get("max_drawdown_percent", ""),
                trades=row.get("trade_count", ""),
                tpd=row.get("trades_per_day", ""),
                win=row.get("win_rate_percent", ""),
                avgw=row.get("average_win", ""),
                avgl=row.get("average_loss", ""),
                payoff=row.get("payoff_ratio", ""),
                exp=row.get("expectancy", ""),
                rec=row.get("recovery_factor", ""),
                sig=row.get("signal_count_diff", ""),
                feat=row.get("feature_ready_diff", ""),
                gap=row.get("gap_cause_summary", ""),
            )
        )
    lines.extend(
        [
            "",
            "## Proxy/Runtime Gap Boundary(프록시/런타임 간극 경계)",
            "",
            "Action(행동): F76B proxy meaningful signal(프록시 의미 신호)을 MT5 Strategy Tester(전략 테스터)로 관찰했다.",
            "",
            "Effect(효과): 이 보고서는 runtime probe observation(런타임 탐침 관찰)만 만들며 runtime authority(런타임 권위)나 completion(완성)을 만들지 않는다.",
            "",
            "## Next Action(다음 행동)",
            "",
            f"`{NEXT_RUN_ID}`.",
        ]
    )
    return "\n".join(lines)


def gate_audit_text(payload: Mapping[str, Any], created_at: str) -> str:
    summary = build_summary(payload)
    return f"""# Required Gate Coverage Audit F76D(F76D 필수 게이트 커버리지 감사)

Updated(갱신): {created_at}

| gate(게이트) | status(상태) | evidence/effect(근거/효과) |
|---|---|---|
| candidate_lock(후보 고정) | `passed(통과)` | `{SOURCE_CANDIDATE_ID}` |
| probability_parity(확률 동등성) | `{summary['probability_parity_pass_rows']}/3` | ONNX long schema(ONNX 롱 스키마) |
| signal_count_parity(신호 수 동등성) | `{summary['signal_parity_pass_rows']}/3` | selected-entry veto tape(선택 진입 거부 테이프) |
| feature_readiness_parity(피처 준비 동등성) | `{summary['feature_readiness_pass_rows']}/1` | 48 feature CSV(48개 피처 CSV) |
| source_reproduction(프록시 재현) | `{summary['source_reproduction_pass_rows']}/2` | validation/OOS proxy KPI reproduction(검증/표본외 프록시 KPI 재현) |
| MT5 runtime probe(MT5 런타임 탐침) | `{summary['completed_attempt_count']}/{summary['attempt_count']}` | Strategy Tester attempts(전략 테스터 시도) |
| final_claim_guard(최종 주장 보호) | `passed(통과)` | `{CLAIM_BOUNDARY}` |
"""


def update_ledgers(payload: Mapping[str, Any], created_at: str) -> None:
    summary = build_summary(payload)
    best = summary["best_runtime"]
    row_id = f"{RUN_ID}__runtime_probe"
    row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "mt5_runtime_probe(MT5 런타임 탐침)",
        "status": payload.get("status"),
        "judgment": payload.get("judgment"),
        "path": rel(REPORT_PATH),
        "notes": f"attempts={summary['attempt_count']};completed={summary['completed_attempt_count']};candidate={TARGET_CANDIDATE_ID}",
        "family": "runtime_backtest(런타임/백테스트)",
        "primary_report": rel(REPORT_PATH),
        "run_number": "frontier76D",
        "date": created_at[:10],
        "decision": payload.get("judgment"),
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rows": str(summary["attempt_count"]),
        "gate_passes": str(summary["probability_parity_pass_rows"] + summary["signal_parity_pass_rows"] + summary["feature_readiness_pass_rows"] + summary["source_reproduction_pass_rows"] + summary["completed_attempt_count"]),
        "gate_total": "11",
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "run_date": created_at[:10],
        "primary_artifact": rel(RUN_MANIFEST_PATH),
        "result_status": payload.get("status"),
        "view": "MT5 Runtime Probe(MT5 런타임 탐침)",
        "tier": "Tier A separate; Tier B missing_required; combined out_of_scope",
        "metric_scope": "runtime_probe_kpi(런타임 탐침 KPI)",
        "scoreboard_lane": "runtime_probe(런타임 탐침)",
        "external_verification_status": "completed(완료)" if summary["completed_attempt_count"] else "blocked_or_materialized_pending(차단 또는 물질화 대기)",
        "result_judgment": payload.get("judgment"),
        "final_decision_path": rel(SELECTED_DIR / "selection_status.md"),
        "gate_audit_path": rel(GATE_AUDIT_PATH),
        "created_at": created_at,
        "ledger_row_id": row_id,
        "subrun_id": "runtime_probe(런타임 탐침)",
        "record_view": "Tier A MT5 Runtime Probe(Tier A MT5 런타임 탐침)",
        "tier_scope": "Tier A separate; Tier B missing_required; combined out_of_scope",
        "kpi_scope": "runtime_probe_kpi(런타임 탐침 KPI)",
        "primary_kpi": f"net={best.get('net_profit', '')};pf={best.get('profit_factor', '')};dd={best.get('max_drawdown_percent', '')};tpd={best.get('trades_per_day', '')}",
        "guardrail_kpi": f"signal_diff={best.get('signal_count_diff', '')};feature_diff={best.get('feature_ready_diff', '')}",
        "work_family": "runtime_backtest(런타임/백테스트)",
        "row_id": row_id,
        "evidence_boundary": "runtime_probe_observation_no_authority(런타임 탐침 관찰, 권위 없음)",
        "next_action": NEXT_RUN_ID,
        "question": "Does F76B axis-ablation meaningful proxy survive MT5 runtime?(F76B 축 제거 의미 프록시가 MT5 런타임에서 살아남나?)",
        "artifact_count": "10",
        "created_at_utc": created_at,
        "required_gate_audit": rel(GATE_AUDIT_PATH),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "runtime_backtest(런타임/백테스트)",
        "run_type": "mt5_axis_ablation_runtime_probe(MT5 축 제거 런타임 탐침)",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_MANIFEST_PATH),
        "result_path": rel(REPORT_PATH),
        "goal_achieve": "not_claimed",
        "source_authority": "runtime_probe_observation_only(런타임 탐침 관찰 전용)",
        "net_profit": best.get("net_profit", ""),
        "profit_factor": best.get("profit_factor", ""),
        "drawdown": best.get("max_drawdown_percent", ""),
        "trade_count": best.get("trade_count", ""),
        "trade_density": best.get("trades_per_day", ""),
        "expectancy": best.get("expectancy", ""),
        "recovery_factor": best.get("recovery_factor", ""),
        "runtime_completed_rows": summary["completed_attempt_count"],
        "probability_parity_pass_rows": summary["probability_parity_pass_rows"],
    }
    upsert_csv(ROOT / "docs/registers/run_registry.csv", "run_id", row)
    upsert_csv(ROOT / "docs/registers/alpha_run_ledger.csv", "ledger_row_id", row)
    upsert_csv(REVIEW_DIR / "stage_run_ledger.csv", "ledger_row_id", row)


def update_registers_and_state(payload: Mapping[str, Any], created_at: str) -> None:
    summary = build_summary(payload)
    best = summary["best_runtime"]
    marker = "<!-- frontier76D_mt5_axis_ablation_runtime_probe_v1 -->"
    idea_path = ROOT / "docs/registers/idea_registry.md"
    text = io_path(idea_path).read_text(encoding="utf-8-sig")
    if marker not in text:
        addition = f"""

{marker}
- `{RUN_ID}` executed/attempted F76 MT5 Runtime Probe(F76 MT5 런타임 탐침). Candidate(후보): `{TARGET_CANDIDATE_ID}`. Attempts/completed(시도/완료): `{summary['attempt_count']}/{summary['completed_attempt_count']}`. Best runtime net/PF/DD/tpd(최선 런타임 순수익/수익 팩터/손실폭/일거래): `{best.get('net_profit', '')}/{best.get('profit_factor', '')}/{best.get('max_drawdown_percent', '')}/{best.get('trades_per_day', '')}`. Evidence(근거): `{rel(REPORT_PATH)}`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{NEXT_RUN_ID}`.
"""
        write_text(idea_path, text.rstrip() + addition)
    state = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {payload.get('status')}
current_judgment: {payload.get('judgment')}
next_run_id: {NEXT_RUN_ID}
runtime_probe_status: f76_mandatory_runtime_probe_attempted
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
five_stage_retrospective_due_status: not_due_after_frontier71_to_75_retrospective_completed
updated_at_utc: '{created_at}'
context_anchor: {CONTEXT_ANCHOR_PATH}
notes:
  - "Action(행동): F76D MT5 Runtime Probe(MT5 런타임 탐침)를 실행/시도했다."
  - "Effect(효과): proxy/runtime gap(프록시/런타임 간극) 분석을 다음 실행으로 넘긴다."
  - "Best runtime(최선 런타임): net/PF/DD/tpd {best.get('net_profit', '')}/{best.get('profit_factor', '')}/{best.get('max_drawdown_percent', '')}/{best.get('trades_per_day', '')}."
  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."
"""
    write_text(ROOT / "docs/workspace/workspace_state.yaml", state)
    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

## Current Truth(현재 진실)

Action(행동): F76D MT5 Runtime Probe(MT5 런타임 탐침)를 실행/시도했다.

Effect(효과): F76B proxy(프록시) 의미 신호를 MT5 Strategy Tester(전략 테스터)로 물질화했고, 다음은 proxy/runtime gap analysis(프록시/런타임 간극 분석)다.

## Runtime Result(런타임 결과)

- attempts/completed(시도/완료): `{summary['attempt_count']}/{summary['completed_attempt_count']}`
- probability/signal/feature/reproduction parity(확률/신호/피처/재현 동등성): `{summary['probability_parity_pass_rows']}/{summary['signal_parity_pass_rows']}/{summary['feature_readiness_pass_rows']}/{summary['source_reproduction_pass_rows']}`
- best runtime net/PF/DD/tpd(최선 런타임 순수익/수익 팩터/손실폭/일거래): `{best.get('net_profit', '')}/{best.get('profit_factor', '')}/{best.get('max_drawdown_percent', '')}/{best.get('trades_per_day', '')}`

## Open Work(열린 작업)

- next run(다음 실행): `{NEXT_RUN_ID}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(ROOT / "docs/context/current_working_state.md", current)
    selection = f"""# F76 Selection Status(F76 선택 상태)

Status(상태): `{payload.get('status')}`

Judgment(판정): `{payload.get('judgment')}`

Action(행동): F76D MT5 Runtime Probe(MT5 런타임 탐침)를 실행/시도했다.

Effect(효과): 다음 실행은 F76E proxy/runtime gap analysis(프록시/런타임 간극 분석)와 repair decision(수리 결정)이다.

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(SELECTED_DIR / "selection_status.md", selection)


def main() -> int:
    args = parse_args()
    ensure_dirs()
    created_at = now_utc()
    summary = load_summary()
    context = build_context(summary)
    artifact, probability, signal, feature_parity = materialize(context, Path(args.common_files_root))
    attempts = build_attempts(context, artifact) if artifact.get("export_status") == "runtime_probe_parity_passed" else []
    compile_payload = compile_runtime_ea(Path(args.metaeditor_path))
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
    if args.execute and completed:
        status = "completed_mt5_runtime_probe_observation_no_authority"
        judgment = "runtime_probe_completed_gap_analysis_required_no_authority"
    elif args.execute:
        status = "blocked_mt5_runtime_probe_attempted_no_authority"
        judgment = "runtime_probe_blocked_or_missing_output_repair_required_no_authority"
    else:
        status = "materialized_pending_mt5_runtime_probe_execution_no_authority"
        judgment = "runtime_probe_materialized_pending_execution_no_authority"
    payload = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": status,
        "judgment": judgment,
        "created_at_utc": created_at,
        "artifact_rows": [artifact],
        "probability_parity": probability,
        "signal_parity": signal,
        "feature_readiness_parity": feature_parity,
        "source_reproduction": context["reproduction_rows"],
        "attempts": attempts,
        "compile_payload": compile_payload,
        "execution_results": execution_results,
        "runtime_receipt": runtime_receipt,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(RUN_MANIFEST_PATH, payload)
    write_json(RUN_DIR / "f76d_summary.json", build_summary(payload))
    write_csv(RUN_DIR / "f76d_probability_parity.csv", probability)
    write_csv(RUN_DIR / "f76d_signal_parity.csv", signal)
    write_csv(RUN_DIR / "f76d_feature_readiness_parity.csv", feature_parity)
    write_csv(RUN_DIR / "f76d_source_reproduction.csv", context["reproduction_rows"])
    write_csv(RUN_DIR / "f76d_runtime_receipt.csv", runtime_receipt, f71d.RUNTIME_RECEIPT_COLUMNS)
    write_json(RUN_DIR / "f76d_execution_results.json", execution_results)
    write_json(REVIEW_DIR / "f76d_summary.json", build_summary(payload))
    write_csv(REVIEW_DIR / "f76d_probability_parity.csv", probability)
    write_csv(REVIEW_DIR / "f76d_signal_parity.csv", signal)
    write_csv(REVIEW_DIR / "f76d_feature_readiness_parity.csv", feature_parity)
    write_csv(REVIEW_DIR / "f76d_source_reproduction.csv", context["reproduction_rows"])
    write_csv(REVIEW_DIR / "f76d_runtime_receipt.csv", runtime_receipt, f71d.RUNTIME_RECEIPT_COLUMNS)
    write_text(REPORT_PATH, report_text(payload, created_at))
    write_text(GATE_AUDIT_PATH, gate_audit_text(payload, created_at))
    update_ledgers(payload, created_at)
    update_registers_and_state(payload, created_at)
    print(json.dumps(json_ready(build_summary(payload)), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
