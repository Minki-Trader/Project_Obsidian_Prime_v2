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

SCRIPT_ROOT = Path(__file__).resolve().parents[2]
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.control_plane.mt5_tier_balance_completion import attempt_payload
from foundation.models.onnx_bridge import sha256_file
from stage_pipelines.stage_frontier_71 import frontier71d_mt5_runtime_probe_economics_native_scout as f71d
from stage_pipelines.stage_frontier_74 import frontier74e_mt5_microburst_negative_control_runtime_probe as f74e
from stage_pipelines.stage_frontier_75 import frontier75b_volatility_compression_liquidity_release_proxy_scout as base
from stage_pipelines.stage_frontier_runtime_backfill.run_frontier_runtime_probe_backfill import (
    DEFAULT_COMMON_FILES,
    DEFAULT_METAEDITOR,
    DEFAULT_PORTABLE_ROOT,
    DEFAULT_TERMINAL,
    DEFAULT_TESTER_PROFILE_ROOT,
    EA_BINARY,
    PORTABLE_EA_BINARY,
)


ROOT = base.ROOT
STAGE_ID = base.STAGE_ID
RUN_ID = "frontier75E_mt5_volatility_compression_negative_control_runtime_probe_v1"
PARENT_RUN_ID = "frontier75D_pre_mt5_grok_volatility_compression_negative_control_runtime_probe_v1"
NEXT_RUN_ID = "frontier75F_proxy_runtime_gap_or_closeout_decision_v1"
SOURCE_CANDIDATE_ID = "f75b_0551"
TARGET_CANDIDATE_ID = f"f75e_negative_control_{SOURCE_CANDIDATE_ID}"
COMMON_RUN_ROOT = "Project_Obsidian_Prime_v2/frontier75E_mt5_volatility_compression_negative_control_runtime_probe"
THRESHOLD_EPSILON = 1e-7
CLAIM_BOUNDARY = (
    "negative_control_runtime_probe_observation_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
MODEL_DIR = RUN_DIR / "models"
FEATURE_DIR = RUN_DIR / "features"
VETO_DIR = RUN_DIR / "runtime_veto_tapes"
MT5_DIR = RUN_DIR / "mt5"
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "frontier75E_mt5_negative_control_runtime_probe_report.md"
GATE_AUDIT_PATH = REVIEW_DIR / "required_gate_coverage_audit_f75e.md"
RUN_MANIFEST_PATH = RUN_DIR / "run_manifest.json"
CONTEXT_ANCHOR_PATH = f"stages/{STAGE_ID}/03_reviews/context_anchor.md"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="F75E negative-control MT5 runtime probe.")
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


def ensure_dirs() -> None:
    for path in (RUN_DIR, MODEL_DIR, FEATURE_DIR, VETO_DIR, MT5_DIR, MT5_DIR / "reports", REVIEW_DIR):
        io_path(path).mkdir(parents=True, exist_ok=True)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
    write_text(path, json.dumps(json_ready(payload), ensure_ascii=False, indent=2))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    rows = list(rows)
    if not rows:
        rows = [{"empty": "true"}]
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({name: json_ready(row.get(name, "")) for name in fieldnames})


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
        raise FileNotFoundError(path)
    rows = [existing for existing in rows if existing.get(key) != row.get(key)]
    rows.append({name: json_ready(row.get(name, "")) for name in fieldnames})
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def append_once(path: Path, marker: str, block: str) -> None:
    text = io_path(path).read_text(encoding="utf-8-sig") if path_exists(path) else ""
    if marker in text:
        return
    write_text(path, text.rstrip() + "\n\n" + block.rstrip())


def candidate_row() -> dict[str, Any]:
    path = STAGE_DIR / "02_runs" / base.RUN_ID / "f75b_candidate_results.csv"
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            if row.get("candidate_id") == SOURCE_CANDIDATE_ID:
                return row
    raise RuntimeError(f"candidate_not_found:{SOURCE_CANDIDATE_ID}")


def split_mask(frame: Any, split: str) -> np.ndarray:
    return frame["split"].astype(str).eq(split).to_numpy(dtype=bool)


def train_context() -> dict[str, Any]:
    source = candidate_row()
    frame, feature_order, data_identity = base.load_inputs()
    features = base.feature_bundles(feature_order)[source["feature_bundle"]]
    context_masks = base.make_context_masks(frame)
    session_masks = base.make_session_masks(frame)
    horizon = int(float(source["horizon"]))
    target_mult = float(source["target_atr_mult"])
    stop_mult = float(source["stop_atr_mult"])
    future_ok = base.future_continuity_ok(frame["timestamp"], horizon)
    pnl, exit_bars = base.first_touch_outcome(
        close=frame["close"].to_numpy(dtype=float),
        high=frame["high"].to_numpy(dtype=float),
        low=frame["low"].to_numpy(dtype=float),
        spread_cost=frame["spread_points"].to_numpy(dtype=float) * base.SPREAD_POINT_VALUE,
        atr=frame["atr_14"].to_numpy(dtype=float),
        future_ok=future_ok,
        horizon=horizon,
        target_mult=target_mult,
        stop_mult=stop_mult,
        direction=str(source["direction"]),
    )
    y = (pnl > 0).astype(int)
    finite = np.isfinite(pnl) & future_ok
    gate = context_masks[source["context_gate"]] & session_masks[source["session_gate"]] & finite
    train = split_mask(frame, "train") & gate
    model = base.model_builders()[source["model_family"]]()
    model.fit(frame.loc[train, features], y[train])
    proba = f74e.binary_probabilities(model, frame.loc[:, features])
    score = proba[:, 1]
    threshold = float(source["validation_threshold"])
    raw_selected = gate & np.isfinite(score) & (score >= threshold)
    selected = np.zeros(len(frame), dtype=bool)
    for split in ("train", "validation", "oos"):
        idx = np.where(raw_selected & split_mask(frame, split))[0]
        selected[base.non_overlapping_indices(idx, horizon)] = True
    proxy_kpi_by_split: dict[str, Any] = {}
    for split in ("train", "validation", "oos"):
        idx = selected & split_mask(frame, split)
        proxy_kpi_by_split[split] = base.trade_metrics(pnl[idx], exit_bars[idx], base.split_days(frame, split))
    return {
        "source_candidate": source,
        "frame": frame,
        "features": list(features),
        "data_identity": data_identity,
        "model": model,
        "binary_proba": proba,
        "score": score,
        "threshold": threshold,
        "pnl": pnl,
        "exit_bars": exit_bars,
        "raw_selected": raw_selected,
        "selected": selected,
        "event_mask": gate,
        "proxy_kpi_by_split": proxy_kpi_by_split,
        "horizon": horizon,
        "target_atr_mult": target_mult,
        "stop_atr_mult": stop_mult,
    }


def onnx_probability(onnx_path: Path, values: np.ndarray, expected_cols: int) -> np.ndarray:
    return f74e.onnx_probability(onnx_path, values, expected_cols)


def parity_rows(context: Mapping[str, Any], raw_onnx_path: Path, patched_onnx_path: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    frame = context["frame"]
    features = context["features"]
    threshold = float(context["threshold"])
    runtime_threshold = threshold - THRESHOLD_EPSILON
    probability_rows: list[dict[str, Any]] = []
    signal_rows: list[dict[str, Any]] = []
    for split in ("train", "validation", "oos"):
        subset = frame.loc[frame["split"].astype(str).eq(split)]
        idx = subset.index.to_numpy()
        values = subset.loc[:, features].to_numpy(dtype="float64")
        binary_expected = context["binary_proba"][idx]
        patched_expected = np.column_stack([binary_expected[:, 1], binary_expected[:, 0], np.zeros(len(binary_expected))])
        sample_values = values[: min(len(values), 4096)]
        raw_actual = onnx_probability(raw_onnx_path, sample_values, 2)
        patched_actual = onnx_probability(patched_onnx_path, sample_values, 3)
        raw_diff = np.abs(raw_actual - binary_expected[: len(sample_values)])
        patched_diff = np.abs(patched_actual - patched_expected[: len(sample_values)])
        probability_rows.append(
            {
                "split": split,
                "sample_rows": len(sample_values),
                "raw_binary_max_abs_diff": float(raw_diff.max()) if raw_diff.size else 0.0,
                "patched_three_col_max_abs_diff": float(patched_diff.max()) if patched_diff.size else 0.0,
                "patched_long_col_max_abs": float(np.abs(patched_actual[:, 2]).max()) if len(patched_actual) else 0.0,
                "passed": bool((float(raw_diff.max()) if raw_diff.size else 0.0) <= 1e-5 and (float(patched_diff.max()) if patched_diff.size else 0.0) <= 1e-5),
            }
        )
        all_patched = onnx_probability(patched_onnx_path, values, 3)
        onnx_raw_signal = context["event_mask"][idx] & (all_patched[:, 0] >= runtime_threshold)
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
                "source_threshold": threshold,
                "runtime_threshold": runtime_threshold,
                "threshold_epsilon": THRESHOLD_EPSILON,
                "passed": bool(int((onnx_vetoed_signal != selected_expected).sum()) == 0),
            }
        )
    return probability_rows, signal_rows


def reproduction_rows(context: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = []
    source = context["source_candidate"]
    for split in ("validation", "oos"):
        proxy = context["proxy_kpi_by_split"][split]
        source_count = int(float(source.get(f"{split}_trade_count", 0) or 0))
        reproduced_count = int((context["selected"] & split_mask(context["frame"], split)).sum())
        count_ratio = float(min(source_count, reproduced_count) / max(source_count, reproduced_count, 1))
        rows.append(
            {
                "split": split,
                "source_selected_count": source_count,
                "reproduced_selected_count": reproduced_count,
                "overlap_ratio_vs_source": count_ratio,
                "count_diff": reproduced_count - source_count,
                "source_net_profit": source.get(f"{split}_net_profit"),
                "source_profit_factor": source.get(f"{split}_profit_factor"),
                "source_max_drawdown_percent": source.get(f"{split}_max_drawdown_percent"),
                "source_trades_day": source.get(f"{split}_trades_day"),
                "reproduced_net_profit": proxy.get("net_profit"),
                "reproduced_profit_factor": proxy.get("profit_factor"),
                "reproduced_max_drawdown_percent": proxy.get("max_drawdown_percent"),
                "reproduced_trades_day": proxy.get("trades_day"),
            }
        )
    return rows


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
    patch_meta = f74e.patch_binary_onnx_to_short_three_columns(raw_onnx_path, patched_onnx_path)
    feature_meta = f71d.mt5.export_mt5_feature_matrix_csv(context["frame"], context["features"], feature_csv_path, metadata_columns=("split",))
    veto_meta = f71d.selected_entry_tape(context["frame"], context["selected"], context["event_mask"], veto_path)
    probability, signal = parity_rows(context, raw_onnx_path, patched_onnx_path)
    reproduction = reproduction_rows(context)
    probability_ok = all(row.get("passed") for row in probability)
    signal_ok = all(row.get("passed") for row in signal)
    overlap_ok = all(float(row.get("overlap_ratio_vs_source", 0.0)) >= 0.98 for row in reproduction)
    artifact = {
        "candidate_id": TARGET_CANDIDATE_ID,
        "source_candidate_id": SOURCE_CANDIDATE_ID,
        "materialization_mode": "short_binary_onnx_three_column_negative_control",
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
        "source_reproduction_overlap_passed": overlap_ok,
        "threshold": float(context["threshold"]),
        "short_threshold": float(context["threshold"]) - THRESHOLD_EPSILON,
        "long_threshold": 1.1,
        "threshold_epsilon": THRESHOLD_EPSILON,
        "decision_mode": "threshold_margin",
    }
    if probability_ok and signal_ok and overlap_ok:
        for local_path, common_key, copy_key in (
            (patched_onnx_path, "model_common_path", "model_common_copy"),
            (feature_csv_path, "feature_common_path", "feature_common_copy"),
            (veto_path, "runtime_veto_tape_common_path", "runtime_veto_tape_common_copy"),
        ):
            common_path = f"{COMMON_RUN_ROOT}/{local_path.parent.name}/{local_path.name}"
            artifact[common_key] = common_path
            artifact[copy_key] = f71d.mt5.copy_to_common_files(common_files_root, local_path, common_path)
    artifact["export_status"] = "negative_control_parity_passed" if probability_ok and signal_ok and overlap_ok else "negative_control_parity_failed"
    return artifact, probability, signal, reproduction


def build_attempts(context: Mapping[str, Any], artifact: Mapping[str, Any]) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    for split in ("validation", "oos"):
        from_date, to_date = f71d.split_dates(context["frame"], split)
        mask = split_mask(context["frame"], split)
        expected = int((context["selected"] & mask).sum())
        attempt_name = f"f75e_negative_control_{split}"
        extra = {
            "InpSameDirectionReentryCooldownBars": int(context["horizon"]),
            "InpReentryCooldownBars": 0,
            "InpAtrSltpEnabled": True,
            "InpAtrStopMultiplier": float(context["stop_atr_mult"]),
            "InpAtrTakeProfitMultiplier": float(context["target_atr_mult"]),
            "InpAtrMinStopPoints": 1.0,
            "InpAtrMinTakeProfitPoints": 1.0,
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
            stage_number=75,
            exploration_label="frontier75E_negative_control_runtime_probe",
            attempt_name=attempt_name,
            tier=f71d.mt5.TIER_A,
            split=split,
            model_path=str(artifact["model_common_path"]),
            model_id=f"F75E_{artifact['candidate_id']}",
            model_backend="onnx",
            feature_path=str(artifact["feature_common_path"]),
            feature_count=len(context["features"]),
            feature_order_hash=str(artifact.get("feature_order_sha256")),
            short_threshold=float(context["threshold"]) - THRESHOLD_EPSILON,
            long_threshold=1.1,
            min_margin=-1.0,
            invert_signal=False,
            from_date=from_date,
            to_date=to_date,
            primary_active_tier=f71d.mt5.TIER_A,
            attempt_role="negative_control_runtime_probe",
            record_view_prefix="mt5_f75e_negative_control",
            max_hold_bars=int(context["horizon"]),
            common_root=COMMON_RUN_ROOT,
            close_on_flat_signal=False,
            reverse_on_opposite_signal=True,
            close_only_on_opposite_signal=False,
            extra_set_values=extra,
        )
        attempt.update(
            {
                "candidate_id": artifact["candidate_id"],
                "source_candidate_id": SOURCE_CANDIDATE_ID,
                "expected_rows": int(mask.sum()),
                "expected_signal_count": expected,
                "expected_selected_trade_count": expected,
                "proxy_kpi": context["proxy_kpi_by_split"].get(split, {}),
                "runtime_threshold": float(context["threshold"]) - THRESHOLD_EPSILON,
                "threshold_epsilon": THRESHOLD_EPSILON,
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


def can_run_terminal(payload: Mapping[str, Any]) -> bool:
    return ((payload.get("compile") or {}).get("status") == "completed") or path_exists(PORTABLE_EA_BINARY)


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
    return next((row for row in receipts if row.get("split") == "oos"), receipts[0] if receipts else {})


def build_summary(payload: Mapping[str, Any]) -> dict[str, Any]:
    receipts = list(payload.get("runtime_receipt", []))
    completed = sum(1 for row in receipts if row.get("tester_status") == "completed")
    best = best_receipt(receipts)
    probability = list(payload.get("probability_parity", []))
    signal = list(payload.get("signal_parity", []))
    reproduction = list(payload.get("source_reproduction", []))
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
        "source_reproduction_min_overlap": min((float(row.get("overlap_ratio_vs_source", 0.0)) for row in reproduction), default=0.0),
        "best_runtime": best,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def report_lines(payload: Mapping[str, Any], created_at: str) -> list[str]:
    summary = build_summary(payload)
    best = summary["best_runtime"]
    return [
        "# Frontier75E MT5 Negative-Control Runtime Probe Report(F75E MT5 부정 대조 런타임 탐침 보고서)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        f"- status(상태): `{payload.get('status')}`",
        f"- judgment(판정): `{payload.get('judgment')}`",
        f"- candidate(후보): `{TARGET_CANDIDATE_ID}` from `{SOURCE_CANDIDATE_ID}`",
        f"- attempts/completed(시도/완료): `{summary['attempt_count']}/{summary['completed_attempt_count']}`",
        f"- probability/signal parity pass(확률/신호 동등성 통과): `{summary['probability_parity_pass_rows']}/{summary['signal_parity_pass_rows']}`",
        f"- source reproduction min overlap(원천 재현 최소 중복): `{summary['source_reproduction_min_overlap']}`",
        f"- best runtime net/PF/DD/tpd(최선 런타임 순수익/수익 팩터/손실폭/일거래): `{best.get('net_profit', '')}/{best.get('profit_factor', '')}/{best.get('max_drawdown_percent', '')}/{best.get('trades_per_day', '')}`",
        f"- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Purpose(목적)",
        "",
        "Action(행동): F75B의 약한 scout clue(탐색 단서)를 MT5 Runtime Probe(MT5 런타임 탐침)로 물질화했다.",
        "",
        "Effect(효과): positive result(긍정 결과)가 아니라 proxy/runtime gap(프록시/런타임 간극)을 관찰한다.",
    ]


def gate_audit_lines(payload: Mapping[str, Any], created_at: str) -> list[str]:
    summary = build_summary(payload)
    return [
        "# F75E Required Gate Coverage Audit(F75E 필수 게이트 커버리지 감사)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        "| gate(게이트) | status(상태) | evidence/effect(근거/효과) |",
        "|---|---|---|",
        f"| ONNX/materialization parity(ONNX/물질화 동등성) | `{'pass(통과)' if summary['probability_parity_pass_rows'] == 3 and summary['signal_parity_pass_rows'] == 3 else 'fail_or_blocked(실패 또는 차단)'}` | probability/signal rows(확률/신호 행) `{summary['probability_parity_pass_rows']}/{summary['signal_parity_pass_rows']}` |",
        f"| MT5 runtime probe(MT5 런타임 탐침) | `{'completed(완료)' if summary['completed_attempt_count'] else 'blocked_or_materialized_pending(차단 또는 물질화 후 대기)'}` | attempts/completed(시도/완료) `{summary['attempt_count']}/{summary['completed_attempt_count']}` |",
        "| negative-control boundary(부정 대조 경계) | `pass(통과)` | success criterion(성공 기준)은 gap observation(간극 관찰)이다. |",
        "| final claim guard(최종 주장 보호) | `pass(통과)` | no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). |",
    ]


def update_ledgers(payload: Mapping[str, Any], created_at: str) -> None:
    summary = build_summary(payload)
    best = summary["best_runtime"]
    row = {
        "ledger_row_id": f"{RUN_ID}__runtime_probe",
        "row_id": f"{RUN_ID}__runtime_probe",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "negative_control_runtime_probe(부정 대조 런타임 탐침)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "MT5 negative-control runtime probe(MT5 부정 대조 런타임 탐침)",
        "tier_scope": "Tier A separate; Tier B missing_required; Tier A+B out_of_scope_by_claim",
        "kpi_scope": "runtime_probe_kpi(런타임 탐침 KPI)",
        "scoreboard_lane": "runtime_probe(런타임 탐침)",
        "status": payload.get("status"),
        "result_status": payload.get("status"),
        "judgment": payload.get("judgment"),
        "result_judgment": payload.get("judgment"),
        "path": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "primary_report": rel(REPORT_PATH),
        "primary_artifact": rel(RUN_MANIFEST_PATH),
        "output_path": rel(RUN_MANIFEST_PATH),
        "result_path": rel(REPORT_PATH),
        "primary_kpi": f"attempts={summary['attempt_count']};completed={summary['completed_attempt_count']}",
        "guardrail_kpi": f"prob_parity={summary['probability_parity_pass_rows']};signal_parity={summary['signal_parity_pass_rows']}",
        "external_verification_status": "completed(완료)" if summary["completed_attempt_count"] else "blocked_or_materialized_pending(차단 또는 물질화 후 대기)",
        "notes": "F75E negative-control MT5 Runtime Probe; no authority(F75E 부정 대조 MT5 런타임 탐침, 권위 없음).",
        "run_number": "frontier75E",
        "date": created_at[:10],
        "run_date": created_at[:10],
        "decision": payload.get("judgment"),
        "next_run_id": NEXT_RUN_ID,
        "next_action": NEXT_RUN_ID,
        "rows": summary["attempt_count"],
        "claim_boundary": CLAIM_BOUNDARY,
        "attempt_rows": summary["attempt_count"],
        "runtime_completed_rows": summary["completed_attempt_count"],
        "probability_parity_pass_rows": summary["probability_parity_pass_rows"],
        "net_profit": best.get("net_profit", ""),
        "profit_factor": best.get("profit_factor", ""),
        "drawdown": best.get("max_drawdown_percent", ""),
        "max_drawdown_percent": best.get("max_drawdown_percent", ""),
        "trade_count": best.get("trade_count", ""),
        "trade_density": best.get("trades_per_day", ""),
        "expectancy": best.get("expectancy", ""),
        "recovery_factor": best.get("recovery_factor", ""),
        "created_at_utc": created_at,
        "required_gate_audit": rel(GATE_AUDIT_PATH),
        "gate_audit_path": rel(GATE_AUDIT_PATH),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "not_claimed",
        "run_family": "runtime_backtest(MT5 런타임/백테스트)",
        "run_type": "negative_control_runtime_probe(부정 대조 런타임 탐침)",
        "input_run_id": PARENT_RUN_ID,
        "question": "How does F75B weak scout materialize in MT5 runtime?(F75B 약한 탐색 단서는 MT5 런타임에서 어떻게 물질화되는가?)",
        "evidence_boundary": "runtime_probe_observation_no_authority(런타임 탐침 관찰, 권위 없음)",
    }
    alpha = ROOT / "docs/registers/alpha_run_ledger.csv"
    run_registry = ROOT / "docs/registers/run_registry.csv"
    upsert_csv(alpha, "ledger_row_id", row)
    upsert_csv(run_registry, "run_id", row)
    upsert_csv(REVIEW_DIR / "stage_run_ledger.csv", "ledger_row_id", row, source_header=alpha)


def update_registers_and_state(payload: Mapping[str, Any], created_at: str) -> None:
    summary = build_summary(payload)
    best = summary["best_runtime"]
    marker = "<!-- frontier75E_mt5_negative_control_runtime_probe_v1 -->"
    block = f"""<!-- frontier75E_mt5_negative_control_runtime_probe_v1 -->
- `{RUN_ID}` executed/attempted(실행/시도) F75 negative-control MT5 Runtime Probe(F75 부정 대조 MT5 런타임 탐침). Result(결과): `{payload.get('judgment')}`. Attempts(시도) `{summary['attempt_count']}`, completed(완료) `{summary['completed_attempt_count']}`. Best runtime(최선 런타임) net/PF/DD/trades_day(순수익/수익 팩터/손실폭/일거래): `{best.get('net_profit', '')}/{best.get('profit_factor', '')}/{best.get('max_drawdown_percent', '')}/{best.get('trades_per_day', '')}`. Evidence(근거): `{rel(REPORT_PATH)}`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{NEXT_RUN_ID}`."""
    append_once(ROOT / "docs/registers/idea_registry.md", marker, block)

    state = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {payload.get('status')}
current_judgment: {payload.get('judgment')}
next_run_id: {NEXT_RUN_ID}
runtime_probe_status: f75_negative_control_runtime_probe_attempted
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
five_stage_retrospective_due_status: not_due_after_f74_closeout_f75_closeout_will_trigger
updated_at_utc: '{created_at}'
context_anchor: {CONTEXT_ANCHOR_PATH}
notes:
  - "Action(행동): F75E negative-control MT5 Runtime Probe(부정 대조 MT5 런타임 탐침)를 실행/시도했다."
  - "Effect(효과): runtime receipt rows(런타임 영수증 행) {len(payload.get('runtime_receipt', []))}개를 만들고 다음 행동을 {NEXT_RUN_ID}로 설정했다."
  - "Best runtime(최선 런타임): net/PF/DD/tpd {best.get('net_profit', '')}/{best.get('profit_factor', '')}/{best.get('max_drawdown_percent', '')}/{best.get('trades_per_day', '')}."
  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."
"""
    write_text(ROOT / "docs/workspace/workspace_state.yaml", state)
    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Context anchor(맥락 고정점): `{CONTEXT_ANCHOR_PATH}`

## Current Truth(현재 진실)

Action(행동): F75E negative-control MT5 Runtime Probe(부정 대조 MT5 런타임 탐침)를 실행/시도했다.

Effect(효과): F75B weak scout clue(약한 탐색 단서)를 MT5 runtime evidence(런타임 근거)로 물질화했다.

## Runtime Result(런타임 결과)

- attempts/completed(시도/완료): `{summary['attempt_count']}/{summary['completed_attempt_count']}`
- probability/signal parity(확률/신호 동등성): `{summary['probability_parity_pass_rows']}/{summary['signal_parity_pass_rows']}`
- best runtime net/PF/DD/tpd(최선 런타임 순수익/수익 팩터/손실폭/일거래): `{best.get('net_profit', '')}/{best.get('profit_factor', '')}/{best.get('max_drawdown_percent', '')}/{best.get('trades_per_day', '')}`

## Open Work(열린 작업)

Next run(다음 실행): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(ROOT / "docs/context/current_working_state.md", current)


def main() -> int:
    args = parse_args()
    ensure_dirs()
    created_at = base.now_utc()
    context = train_context()
    artifact, probability, signal, reproduction = materialize(context, Path(args.common_files_root))
    attempts = build_attempts(context, artifact) if artifact.get("export_status") == "negative_control_parity_passed" else []
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
    runtime_receipt = f71d.build_runtime_receipt(execution_results, attempts) if execution_results else []
    completed = sum(1 for row in runtime_receipt if row.get("tester_status") == "completed")
    if args.execute and completed:
        status = "completed_negative_control_runtime_probe_observation_no_authority"
        judgment = "negative_control_runtime_probe_completed_gap_analysis_required_no_authority"
    elif args.execute:
        status = "blocked_negative_control_runtime_probe_attempted_no_authority"
        judgment = "negative_control_runtime_probe_blocked_no_authority"
    else:
        status = "materialized_pending_negative_control_runtime_probe_no_authority"
        judgment = "negative_control_runtime_probe_materialized_pending_execution_no_authority"
    payload = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": status,
        "judgment": judgment,
        "created_at_utc": created_at,
        "artifact_rows": [artifact],
        "probability_parity": probability,
        "signal_parity": signal,
        "source_reproduction": reproduction,
        "attempts": attempts,
        "compile_payload": compile_payload,
        "execution_results": execution_results,
        "runtime_receipt": runtime_receipt,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(RUN_MANIFEST_PATH, payload)
    write_json(RUN_DIR / "f75e_summary.json", build_summary(payload))
    write_csv(RUN_DIR / "f75e_probability_parity.csv", probability)
    write_csv(RUN_DIR / "f75e_signal_parity.csv", signal)
    write_csv(RUN_DIR / "f75e_source_reproduction.csv", reproduction)
    write_csv(RUN_DIR / "f75e_runtime_receipt.csv", runtime_receipt)
    write_json(RUN_DIR / "f75e_execution_results.json", execution_results)
    write_json(REVIEW_DIR / "f75e_summary.json", build_summary(payload))
    write_csv(REVIEW_DIR / "f75e_runtime_receipt.csv", runtime_receipt)
    write_csv(REVIEW_DIR / "f75e_probability_parity.csv", probability)
    write_csv(REVIEW_DIR / "f75e_signal_parity.csv", signal)
    write_text(REPORT_PATH, "\n".join(report_lines(payload, created_at)))
    write_text(GATE_AUDIT_PATH, "\n".join(gate_audit_lines(payload, created_at)))
    update_ledgers(payload, created_at)
    update_registers_and_state(payload, created_at)
    print(json.dumps(json_ready(build_summary(payload)), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
