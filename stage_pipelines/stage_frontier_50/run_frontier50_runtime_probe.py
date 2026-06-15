from __future__ import annotations

import argparse
import json
import math
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.alpha import scout_runner as scout  # noqa: E402
from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from foundation.models.onnx_bridge import export_sklearn_to_onnx_zipmap_disabled, ordered_hash, sha256_file  # noqa: E402
from foundation.mt5 import runtime_support as mt5  # noqa: E402
from stage_pipelines.stage_frontier_23 import frontier23b_payoff_asymmetry_pf_source_proxy_scout as f23b  # noqa: E402
from stage_pipelines.stage_frontier_33 import frontier33b_path_native_mfe_mae_exit_surface_proxy_scout as f33b  # noqa: E402
from stage_pipelines.stage_frontier_50 import run_frontier50_lifecycle as f50  # noqa: E402
from stage_pipelines.stage_frontier_runtime_backfill import run_frontier_runtime_probe_backfill as backfill  # noqa: E402


STAGE_ID = f50.STAGE_ID
RUN_ID = "frontier50Z_runtime_probe_backfill_v1"
RUN_NUMBER = "frontier50Z"
RUN_ROOT = Path("stages") / STAGE_ID / "02_runs" / RUN_ID
MT5_ROOT = RUN_ROOT / "mt5"
MODELS_ROOT = RUN_ROOT / "models"
FEATURE_ROOT = RUN_ROOT / "feature_matrices"
REVIEWS_ROOT = Path("stages") / STAGE_ID / "03_reviews"
SELECTED_ROOT = Path("stages") / STAGE_ID / "04_selected"
SUMMARY_PATH = Path("stages") / STAGE_ID / "02_runs" / f50.RUN_C / "repair_candidate_summary.csv"

DEFAULT_PORTABLE_ROOT = Path("C:/Users/awdse/AppData/Local/ObsidianPrime/mt5_portable_run329E")
DEFAULT_TERMINAL = DEFAULT_PORTABLE_ROOT / "terminal64.exe"
DEFAULT_METAEDITOR = DEFAULT_PORTABLE_ROOT / "MetaEditor64.exe"
DEFAULT_COMMON_FILES = DEFAULT_PORTABLE_ROOT / "Common" / "Files"
DEFAULT_TESTER_PROFILE_ROOT = DEFAULT_PORTABLE_ROOT / "MQL5" / "Profiles" / "Tester"
DEFAULT_TERMINAL_DATA_ROOT = DEFAULT_PORTABLE_ROOT


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Frontier50 MT5 runtime probe.")
    parser.add_argument("--candidate-id", default="f50c_0064")
    parser.add_argument("--terminal-path", default=str(DEFAULT_TERMINAL))
    parser.add_argument("--metaeditor-path", default=str(DEFAULT_METAEDITOR))
    parser.add_argument("--common-files-root", default=str(DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(DEFAULT_TERMINAL_DATA_ROOT))
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--wait-timeout-seconds", type=int, default=240)
    parser.add_argument("--materialize-only", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    created_at = utc_now()
    mkdirs()
    row = select_candidate(args.candidate_id)
    training = train_runtime_candidate(row)
    artifacts = materialize_model_artifacts(row, training)
    split_payload = materialize_split_payload(row, training, artifacts)
    spec = candidate_spec(row, artifacts)
    attempts = backfill.materialize_attempts(spec, split_payload, training["runtime_feature_order"], artifacts["feature_order_hash"], Path(args.common_files_root))

    compile_payload = backfill.compile_runtime_ea(Path(args.metaeditor_path))
    terminal_probe = backfill.terminal_processes()
    execution_payload = execute_attempts(args, spec, attempts, compile_payload, terminal_probe, created_at)
    runtime_rows = backfill.build_runtime_summary_rows(spec, attempts, execution_payload, split_payload)
    classification = "runtime_probe_observation_no_authority"
    if not any(row.get("runtime_status") == "completed" and row.get("report_status") == "completed" for row in runtime_rows):
        classification = "blocked_attempt_failed"

    proxy_gap_rows = proxy_runtime_gap_rows(row, runtime_rows)
    backfill.write_csv(RUN_ROOT / "proxy_runtime_gap.csv", proxy_gap_rows)
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "candidate_id": str(row["candidate_id"]),
        "classification": classification,
        "runtime_probe_status": classification,
        "proxy_candidate": json_ready(dict(row)),
        "model_artifacts": artifacts,
        "runtime_rows": runtime_rows,
        "proxy_runtime_gap_rows": proxy_gap_rows,
        "claim_boundary": backfill.claim_boundary_payload(),
        "created_at_utc": created_at,
    }
    backfill.write_json(RUN_ROOT / "final_decision.json", final)
    backfill.write_json(RUN_ROOT / "run_manifest.json", final)
    write_reports(final, row, runtime_rows, proxy_gap_rows, attempts, execution_payload)
    backfill.upsert_backfill_status_ledger(
        50,
        STAGE_ID,
        created_at,
        classification,
        {
            "status": classification,
            "reason": "mandatory_stage_runtime_probe_recorded",
            "checks": {
                "candidate_id": str(row["candidate_id"]),
                "onnx_path": artifacts["onnx_path"],
                "feature_count": artifacts["feature_count"],
            },
        },
        spec,
        runtime_rows,
    )
    print(json.dumps(json_ready({"status": classification, "run_id": RUN_ID, "runtime_rows": runtime_rows}), ensure_ascii=False, indent=2))
    return 0 if classification != "blocked_attempt_failed" else 1


def mkdirs() -> None:
    for path in (RUN_ROOT, MT5_ROOT, MODELS_ROOT, FEATURE_ROOT, REVIEWS_ROOT, SELECTED_ROOT):
        io_path(path).mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig")


def select_candidate(candidate_id: str) -> pd.Series:
    summary = read_csv(SUMMARY_PATH)
    if candidate_id:
        match = summary.loc[summary["candidate_id"].astype(str).eq(candidate_id)]
        if not match.empty:
            return match.iloc[0]
    scout_rows = summary.loc[summary["f50_scout_clue_flag"].astype(bool)].copy()
    if scout_rows.empty:
        return summary.sort_values(["forward_min_pf", "forward_max_dd"], ascending=[False, True]).iloc[0]
    scout_rows = scout_rows.sort_values(["forward_min_pf", "forward_max_dd"], ascending=[False, True])
    return scout_rows.iloc[0]


def train_runtime_candidate(row: pd.Series) -> dict[str, Any]:
    frame = f23b.load_frame()
    feature_order = f23b.read_feature_order()
    raw_path = f33b.load_raw_path(frame)
    path_labels = f33b.build_path_labels(frame, raw_path)
    labels = path_labels[f50.SIDE_VALUE]
    event_spec = match_spec(f50.event_specs(frame, labels, str(row["profile"])), "event_variant", str(row["event_variant"]))
    base_spec = match_spec(f50.base_scorer_specs(str(row["profile"])), "base_scorer_family", str(row["base_scorer_family"]))
    context_spec = match_spec(f50.sequence_context_specs(str(row["profile"])), "context_variant", str(row["context_variant"]))
    model_family_token = str(row["model_family"]).split("__", 1)[0]
    model_spec = match_spec(f50.model_specs(str(row["profile"])), "model_family", model_family_token)

    x_raw = frame[feature_order].to_numpy(dtype="float64")
    valid_raw_features = np.isfinite(x_raw).all(axis=1)
    y = np.asarray(event_spec["event"], dtype="int8")
    train_mask = f33b.split_mask(frame, "train") & valid_raw_features & labels["valid"]
    fit_mask = train_mask & np.isfinite(y)
    base_model = base_spec["factory"]()
    base_model.fit(x_raw[fit_mask], y[fit_mask])
    base_score = np.full(len(frame), np.nan, dtype="float64")
    base_score[valid_raw_features] = f50.event_probability(base_model, x_raw[valid_raw_features])
    finite_base_score = np.isfinite(base_score) & valid_raw_features
    context = f50.build_sequence_context(
        frame=frame,
        base_score=base_score,
        event=y,
        event_spec=event_spec,
        train_mask=train_mask & finite_base_score,
        context_spec=context_spec,
    )
    x_context = context["matrix"]
    valid_context = context["valid_context"] & valid_raw_features
    x_model = np.column_stack([x_raw, x_context])
    fit_mask_context = fit_mask & valid_context
    model = model_spec["factory"]()
    model.fit(x_model[fit_mask_context], y[fit_mask_context])
    score = np.full(len(frame), np.nan, dtype="float64")
    score[valid_context] = f50.event_probability(model, x_model[valid_context])
    base_mask = valid_context & (score >= float(row["score_threshold"]))
    risk_spec = match_spec(f50.risk_budget_specs(str(row["profile"])), "risk_budget_variant", str(row["risk_budget_variant"]))
    risk_mask, risk_meta = f50.apply_risk_budget_mask(
        frame=frame,
        base_mask=base_mask,
        train_mask=train_mask & np.isfinite(score),
        context=context,
        risk_spec=risk_spec,
    )
    runtime_feature_order = list(feature_order) + list(context["feature_names"])
    runtime_frame = pd.concat(
        [
            frame[["timestamp", "symbol", "split"]].reset_index(drop=True),
            pd.DataFrame(x_model, columns=runtime_feature_order),
        ],
        axis=1,
    )
    runtime_frame["runtime_candidate_mask"] = risk_mask
    probabilities = binary_to_three_class(model, x_model)
    return {
        "frame": frame,
        "runtime_frame": runtime_frame,
        "runtime_feature_order": runtime_feature_order,
        "runtime_feature_matrix": x_model,
        "risk_mask": risk_mask,
        "score": score,
        "probabilities": probabilities,
        "model": model,
        "context": context,
        "risk_meta": risk_meta,
        "raw_path": raw_path,
    }


def match_spec(specs: Sequence[Mapping[str, Any]], key: str, value: str) -> Mapping[str, Any]:
    for spec in specs:
        if str(spec.get(key)) == value:
            return spec
    raise RuntimeError(f"spec not found: {key}={value}")


def binary_to_three_class(model: Any, values: np.ndarray) -> np.ndarray:
    raw = np.asarray(model.predict_proba(values), dtype="float64")
    classes = [int(item) for item in list(getattr(model, "classes_", []))]
    if not classes and hasattr(model, "steps"):
        classes = [int(item) for item in list(model.steps[-1][1].classes_)]
    class_to_index = {label: index for index, label in enumerate(classes)}
    p_event = raw[:, class_to_index[1]]
    p_flat = raw[:, class_to_index[0]]
    p_long = np.zeros(len(raw), dtype="float64")
    return np.column_stack([p_event, p_flat, p_long])


def materialize_model_artifacts(row: pd.Series, training: Mapping[str, Any]) -> dict[str, Any]:
    model_id = f"{str(row['candidate_id'])}_binary_event_to_short3"
    model_path = MODELS_ROOT / f"{model_id}.joblib"
    binary_onnx_path = MODELS_ROOT / f"{model_id}.binary.onnx"
    onnx_path = MODELS_ROOT / f"{model_id}.onnx"
    joblib.dump(training["model"], io_path(model_path))
    binary_meta = export_sklearn_to_onnx_zipmap_disabled(
        training["model"],
        binary_onnx_path,
        feature_count=len(training["runtime_feature_order"]),
        target_opset=12,
        drop_label_output=False,
    )
    patch_binary_onnx_to_three_class(binary_onnx_path, onnx_path)
    parity = onnx_three_class_parity(onnx_path, training["runtime_feature_matrix"], training["probabilities"])
    payload = {
        "model_id": model_id,
        "model_path": model_path.as_posix(),
        "model_sha256": sha256_file(model_path),
        "binary_onnx": binary_meta,
        "onnx_path": onnx_path.as_posix(),
        "onnx_sha256": sha256_file(onnx_path),
        "feature_count": len(training["runtime_feature_order"]),
        "feature_order_hash": ordered_hash(training["runtime_feature_order"]),
        "feature_order_path": (MODELS_ROOT / f"{model_id}.feature_order.txt").as_posix(),
        "onnx_parity": parity,
        "probability_mapping": "p_short=binary_event_probability,p_flat=non_event_probability,p_long=0",
    }
    io_path(Path(payload["feature_order_path"])).write_text("\n".join(training["runtime_feature_order"]) + "\n", encoding="utf-8")
    backfill.write_json(MODELS_ROOT / "model_artifact_manifest.json", payload)
    return payload


def patch_binary_onnx_to_three_class(source: Path, destination: Path) -> None:
    import onnx
    from onnx import TensorProto, helper, numpy_helper

    model = onnx.load(str(io_path(source)))
    probability_output = None
    for output in model.graph.output:
        tensor = output.type.tensor_type
        dims = [dim.dim_value if dim.dim_value else None for dim in tensor.shape.dim]
        if len(dims) == 2 and dims[-1] == 2:
            probability_output = output.name
            break
    if probability_output is None:
        probability_output = model.graph.output[-1].name
    initializers = [
        numpy_helper.from_array(np.asarray([0], dtype=np.int64), name="op_slice_start0"),
        numpy_helper.from_array(np.asarray([1], dtype=np.int64), name="op_slice_end1"),
        numpy_helper.from_array(np.asarray([1], dtype=np.int64), name="op_slice_start1"),
        numpy_helper.from_array(np.asarray([2], dtype=np.int64), name="op_slice_end2"),
        numpy_helper.from_array(np.asarray([1], dtype=np.int64), name="op_slice_axes1"),
        numpy_helper.from_array(np.asarray([1], dtype=np.int64), name="op_slice_steps1"),
        numpy_helper.from_array(np.asarray([0.0], dtype=np.float32), name="op_zero_scalar"),
    ]
    model.graph.initializer.extend(initializers)
    model.graph.node.extend(
        [
            helper.make_node("Slice", [probability_output, "op_slice_start0", "op_slice_end1", "op_slice_axes1", "op_slice_steps1"], ["op_p_flat"]),
            helper.make_node("Slice", [probability_output, "op_slice_start1", "op_slice_end2", "op_slice_axes1", "op_slice_steps1"], ["op_p_short"]),
            helper.make_node("Mul", ["op_p_short", "op_zero_scalar"], ["op_p_long"]),
            helper.make_node("Concat", ["op_p_short", "op_p_flat", "op_p_long"], ["op_probabilities_3class"], axis=1),
        ]
    )
    del model.graph.output[:]
    model.graph.output.extend([helper.make_tensor_value_info("op_probabilities_3class", TensorProto.FLOAT, [None, 3])])
    onnx.checker.check_model(model)
    io_path(destination.parent).mkdir(parents=True, exist_ok=True)
    onnx.save(model, str(io_path(destination)))


def onnx_three_class_parity(onnx_path: Path, values: np.ndarray, expected: np.ndarray) -> dict[str, Any]:
    import onnxruntime as ort

    sample = np.asarray(values[np.isfinite(values).all(axis=1)][:2048], dtype="float32")
    expected_sample = np.asarray(expected[np.isfinite(values).all(axis=1)][:2048], dtype="float64")
    session = ort.InferenceSession(str(io_path(onnx_path)), providers=["CPUExecutionProvider"])
    actual = session.run(None, {session.get_inputs()[0].name: sample})[0]
    diff = np.abs(np.asarray(actual, dtype="float64") - expected_sample)
    return {
        "passed": bool(float(diff.max()) <= 1e-5),
        "rows": int(len(sample)),
        "max_abs_diff": float(diff.max()),
        "mean_abs_diff": float(diff.mean()),
        "output_names": [output.name for output in session.get_outputs()],
    }


def materialize_split_payload(row: pd.Series, training: Mapping[str, Any], artifacts: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    rows_for_expected: list[dict[str, Any]] = []
    runtime_frame = training["runtime_frame"]
    probabilities = training["probabilities"]
    signal = signal_from_three_class(probabilities, float(row["score_threshold"]))
    candidate_mask = np.asarray(training["risk_mask"], dtype=bool)
    for runtime_split, source_split in (("validation_is", "validation"), ("oos", "oos")):
        split_all = runtime_frame["split"].astype(str).eq(source_split).to_numpy()
        export_mask = split_all & candidate_mask
        export_frame = runtime_frame.loc[export_mask].copy()
        feature_path = FEATURE_ROOT / f"{RUN_ID}_{runtime_split}_features.csv"
        feature_export = mt5.export_mt5_feature_matrix_csv(export_frame, training["runtime_feature_order"], feature_path)
        split_frame = runtime_frame.loc[split_all].copy()
        split_signal = signal[export_mask]
        expected = expected_signal_summary(split_frame, split_signal, runtime_split, export_rows=len(export_frame))
        rows_for_expected.append(expected)
        out[runtime_split] = {
            "source_split": source_split,
            "frame": export_frame,
            "feature_export": feature_export,
            "expected": expected,
            "from_date": backfill.split_date_range(split_frame)[0],
            "to_date": backfill.split_date_range(split_frame)[1],
        }
    backfill.write_csv(RUN_ROOT / "expected_signal_summary.csv", rows_for_expected)
    return out


def signal_from_three_class(probabilities: np.ndarray, threshold: float) -> np.ndarray:
    p_short = probabilities[:, 0]
    p_flat = probabilities[:, 1]
    short_ok = (p_short >= threshold) & (p_short >= p_flat)
    return np.where(short_ok, -1, 0).astype("int8")


def expected_signal_summary(frame: pd.DataFrame, signal: np.ndarray, runtime_split: str, *, export_rows: int) -> dict[str, Any]:
    timestamps = pd.to_datetime(frame["timestamp"], utc=True).reset_index(drop=True)
    days = backfill.count_scope_days(timestamps) if len(timestamps) else 0
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "split": runtime_split,
        "rows": int(export_rows),
        "full_split_rows": int(len(frame)),
        "days_in_scope": int(days),
        "decision_mode": "threshold_margin",
        "signal_count": int((signal != 0).sum()),
        "long_count": int((signal == 1).sum()),
        "short_count": int((signal == -1).sum()),
        "flat_count": int((signal == 0).sum()),
        "expected_density_per_day": float((signal != 0).sum() / days) if days else 0.0,
    }


def candidate_spec(row: pd.Series, artifacts: Mapping[str, Any]) -> backfill.CandidateSpec:
    threshold = float(row["score_threshold"])
    return backfill.CandidateSpec(
        stage_num=50,
        stage_id=STAGE_ID,
        parent_run_id=f50.RUN_D,
        source_run_id=f50.RUN_C,
        candidate_id=str(row["candidate_id"]),
        model_id=str(artifacts["model_id"]),
        model_path=Path(str(artifacts["model_path"])),
        onnx_path=Path(str(artifacts["onnx_path"])),
        decision_mode="threshold_margin",
        short_threshold=threshold,
        long_threshold=1.0,
        min_margin=0.0,
        max_hold_bars=12,
        cooldown_bars=0,
        source_contract="binary_event_probability_mapped_to_three_class_short_threshold",
        source_note="F50 mandatory MT5 runtime probe representative scout clue",
    )


def execute_attempts(
    args: argparse.Namespace,
    spec: backfill.CandidateSpec,
    attempts: Sequence[Mapping[str, Any]],
    compile_payload: Mapping[str, Any],
    terminal_probe: Mapping[str, Any],
    created_at: str,
) -> dict[str, Any]:
    backfill.write_json(spec.mt5_root / "mt5_compile_result.json", compile_payload)
    backfill.write_json(spec.run_root / "terminal_process_audit.json", terminal_probe)
    backfill.write_csv(spec.run_root / "mt5_runtime_probe_attempt_package.csv", backfill.flatten_attempt_rows(attempts))
    execution_results: list[dict[str, Any]] = []
    report_records: list[dict[str, Any]] = []
    if args.materialize_only:
        execution_results = [backfill.blocked_result(spec, attempt, "not_run_materialize_only") for attempt in attempts]
    else:
        compile_status = (compile_payload.get("compile") or {}).get("status")
        can_run = compile_status == "completed" or path_exists(backfill.PORTABLE_EA_BINARY)
        if not can_run:
            execution_results = [backfill.blocked_result(spec, attempt, "compile_blocked_and_no_portable_ex5_fallback") for attempt in attempts]
        elif terminal_probe.get("status") != "no_terminal64_process":
            execution_results = [backfill.blocked_result(spec, attempt, "target_portable_terminal_already_running") for attempt in attempts]
        else:
            for attempt in attempts:
                backfill.remove_runtime_outputs(Path(args.common_files_root), attempt)
                mt5.remove_existing_mt5_report_artifacts(Path(args.terminal_data_root), attempt, run_id=spec.run_id)
                try:
                    tester_result = mt5.run_mt5_tester(
                        Path(args.terminal_path),
                        ROOT / str(attempt["ini"]["path"]),
                        set_path=ROOT / str(attempt["set"]["path"]),
                        tester_profile_set_path=Path(args.tester_profile_root) / mt5.EA_TESTER_SET_NAME,
                        tester_profile_ini_path=Path(args.tester_profile_root) / str(attempt["ini_name"]),
                        timeout_seconds=int(args.timeout_seconds),
                        terminal_extra_args=["/portable"],
                    )
                except subprocess.TimeoutExpired as exc:
                    tester_result = {
                        "status": "blocked",
                        "command": exc.cmd,
                        "returncode": None,
                        "stdout": backfill.tail_text(exc.stdout),
                        "stderr": backfill.tail_text(exc.stderr),
                        "blocker": "terminal_timeout",
                    }
                runtime_outputs = mt5.wait_for_mt5_runtime_outputs(
                    Path(args.common_files_root),
                    attempt,
                    timeout_seconds=int(args.wait_timeout_seconds),
                    poll_seconds=2.0,
                )
                if runtime_outputs.get("status") != "completed":
                    tester_result["status"] = "blocked"
                    tester_result.setdefault("blocker", "runtime_outputs_missing_or_init_failed")
                result = {
                    **tester_result,
                    "runtime_outputs": runtime_outputs,
                    "attempt_name": attempt["attempt_name"],
                    "tier": attempt["tier"],
                    "split": attempt["split"],
                    "record_view_prefix": attempt["record_view_prefix"],
                    "attempt_role": attempt["attempt_role"],
                    "candidate_id": spec.candidate_id,
                    "model_id": spec.model_id,
                    "ini_path": attempt["ini"]["path"],
                    "set_path": attempt["set"]["path"],
                    "common_model_path": attempt["common_model_path"],
                    "common_feature_matrix_path": attempt["common_feature_matrix_path"],
                }
                backfill.write_json(spec.mt5_root / f"{attempt['attempt_name']}_tester_execution.json", result)
                execution_results.append(result)
            report_records = mt5.collect_mt5_strategy_report_artifacts(
                terminal_data_root=Path(args.terminal_data_root),
                run_output_root=spec.run_root,
                attempts=attempts,
                run_id=spec.run_id,
            )
            mt5.attach_mt5_report_metrics(execution_results, report_records)
    copied_runtime = backfill.copy_runtime_outputs(Path(args.common_files_root), spec, attempts)
    execution_payload = {
        "compile_payload": compile_payload,
        "terminal_probe": terminal_probe,
        "execution_results": execution_results,
        "report_records": report_records,
        "copied_runtime_outputs": copied_runtime,
        "created_at_utc": created_at,
    }
    backfill.write_json(spec.run_root / "mt5_execution_result.json", execution_payload)
    backfill.write_json(spec.run_root / "strategy_tester_report_records.json", report_records)
    return execution_payload


def proxy_runtime_gap_rows(proxy_row: pd.Series, runtime_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in runtime_rows:
        split = str(row.get("split", ""))
        proxy_prefix = "validation" if split == "validation_is" else "oos"
        proxy_pf = as_float(proxy_row.get(f"{proxy_prefix}_profit_factor"))
        proxy_dd = as_float(proxy_row.get(f"{proxy_prefix}_dd_risk"))
        proxy_trades = as_float(proxy_row.get(f"{proxy_prefix}_trade_count"))
        mt5_pf = as_float(row.get("profit_factor"))
        mt5_dd = as_float(row.get("max_drawdown_percent"))
        mt5_trades = as_float(row.get("trade_count"))
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "candidate_id": str(proxy_row["candidate_id"]),
                "split": split,
                "proxy_profit_factor": proxy_pf,
                "mt5_profit_factor": mt5_pf,
                "profit_factor_gap_mt5_minus_proxy": none_gap(mt5_pf, proxy_pf),
                "proxy_dd_risk": proxy_dd,
                "mt5_max_drawdown_percent": mt5_dd,
                "dd_gap_mt5_minus_proxy": none_gap(mt5_dd, proxy_dd),
                "proxy_trade_count": proxy_trades,
                "mt5_trade_count": mt5_trades,
                "trade_count_gap_mt5_minus_proxy": none_gap(mt5_trades, proxy_trades),
                "signal_count_diff": row.get("signal_count_diff"),
                "feature_ready_diff": row.get("feature_ready_diff"),
            }
        )
    return rows


def as_float(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def none_gap(left: float | None, right: float | None) -> float | None:
    if left is None or right is None:
        return None
    return float(left - right)


def write_reports(
    final: Mapping[str, Any],
    proxy_row: pd.Series,
    runtime_rows: Sequence[Mapping[str, Any]],
    proxy_gap_rows: Sequence[Mapping[str, Any]],
    attempts: Sequence[Mapping[str, Any]],
    execution_payload: Mapping[str, Any],
) -> None:
    report = runtime_report_text(final, proxy_row, runtime_rows, proxy_gap_rows)
    backfill.write_text_sig(REVIEWS_ROOT / "runtime_probe_report.md", report)
    backfill.write_text_sig(REVIEWS_ROOT / "proxy_runtime_gap_report.md", proxy_runtime_gap_report_text(proxy_gap_rows))
    backfill.write_json(REVIEWS_ROOT / "runtime_probe_status.json", final)
    backfill.write_json(MT5_ROOT / "handoff_manifest.json", {"attempts": attempts, "execution": execution_payload})
    append_runtime_status_to_selection(final)


def runtime_report_text(
    final: Mapping[str, Any],
    proxy_row: pd.Series,
    runtime_rows: Sequence[Mapping[str, Any]],
    proxy_gap_rows: Sequence[Mapping[str, Any]],
) -> str:
    kpi_lines = "\n".join(
        f"- {row.get('split')}: runtime_status(런타임 상태)={row.get('runtime_status')}, report_status(보고서 상태)={row.get('report_status')}, "
        f"PF={row.get('profit_factor')}, DD={row.get('max_drawdown_percent')}, trades(거래)={row.get('trade_count')}, signal_diff(신호 차이)={row.get('signal_count_diff')}"
        for row in runtime_rows
    )
    gap_lines = "\n".join(
        f"- {row.get('split')}: PF gap(MT5-proxy)={row.get('profit_factor_gap_mt5_minus_proxy')}, "
        f"DD gap(MT5-proxy)={row.get('dd_gap_mt5_minus_proxy')}, trade gap(MT5-proxy)={row.get('trade_count_gap_mt5_minus_proxy')}"
        for row in proxy_gap_rows
    )
    return f"""# Frontier50 MT5 Runtime Probe(MT5 런타임 탐침)

- run(실행): `{RUN_ID}`
- candidate(후보): `{proxy_row['candidate_id']}`
- status(상태): `{final.get('classification')}`
- proxy_forward_min_pf(프록시 전진 최소 PF): {proxy_row.get('forward_min_pf')}
- proxy_forward_max_dd(프록시 전진 최대 DD): {proxy_row.get('forward_max_dd')}
- proxy_forward_density(프록시 전진 밀도): {proxy_row.get('forward_min_density')} ~ {proxy_row.get('forward_max_density')}

## Runtime KPI(런타임 지표)
{kpi_lines}

## Proxy Runtime Gap(프록시 런타임 차이)
{gap_lines}

Claim boundary(주장 경계): runtime_probe observation only(런타임 탐침 관찰 전용). No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 주장하지 않는다.
"""


def proxy_runtime_gap_report_text(proxy_gap_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# Frontier50 Proxy Runtime Gap(프록시 런타임 차이)",
        "",
        "Action(행동): F50 scout clue(탐색 단서)를 MT5 Strategy Tester(전략 테스터)에 넣어 proxy/runtime KPI(프록시/런타임 지표)를 비교했다.",
        "",
        "Effect(효과): Python first-hit proxy(파이썬 첫 터치 프록시)와 실제 EA order path(EA 주문 경로)의 차이를 다음 stage(단계)의 negative memory/preserved clue(부정 기억/보존 단서)로 쓴다.",
        "",
    ]
    for row in proxy_gap_rows:
        lines.append(
            f"- {row.get('split')}: PF {row.get('proxy_profit_factor')} -> {row.get('mt5_profit_factor')}; "
            f"DD {row.get('proxy_dd_risk')} -> {row.get('mt5_max_drawdown_percent')}; "
            f"trades {row.get('proxy_trade_count')} -> {row.get('mt5_trade_count')}; "
            f"signal_diff={row.get('signal_count_diff')}; feature_ready_diff={row.get('feature_ready_diff')}"
        )
    lines.append("")
    return "\n".join(lines)


def append_runtime_status_to_selection(final: Mapping[str, Any]) -> None:
    marker = "<!-- f50_runtime_probe_status -->"
    end_marker = "<!-- /f50_runtime_probe_status -->"
    text = f"""
{marker}

# Runtime Probe Status(런타임 탐침 상태)

- run(실행): `{RUN_ID}`
- status(상태): `{final.get('classification')}`
- candidate(후보): `{final.get('candidate_id')}`
- report(보고서): `stages/{STAGE_ID}/03_reviews/runtime_probe_report.md`

Claim boundary(주장 경계): observation only(관찰 전용), no runtime authority(런타임 권위 없음).
{end_marker}
"""
    for path in (SELECTED_ROOT / "selection_status.md",):
        existing = io_path(path).read_text(encoding="utf-8-sig") if path_exists(path) else ""
        if marker in existing and end_marker in existing:
            before, rest = existing.split(marker, 1)
            _old, after = rest.split(end_marker, 1)
            backfill.write_text_sig(path, before.rstrip() + "\n\n" + text.strip() + "\n" + after.lstrip())
        else:
            backfill.write_text_sig(path, existing.rstrip() + "\n\n" + text.strip() + "\n")


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
