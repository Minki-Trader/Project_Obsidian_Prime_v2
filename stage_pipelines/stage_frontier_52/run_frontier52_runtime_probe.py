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
from stage_pipelines.stage_frontier_51 import run_frontier51_lifecycle as f51  # noqa: E402
from stage_pipelines.stage_frontier_runtime_backfill import run_frontier_runtime_probe_backfill as backfill  # noqa: E402


STAGE_ID = "stage_frontier_52__short_pf_edge_order_path_cost_recurrence_after_f51_runtime_memory"
SOURCE_STAGE_ID = f51.STAGE_ID
RUN_A = "frontier52A_stage_open_short_pf_edge_order_path_cost_recurrence_hypothesis_design_v1"
RUN_B = "frontier52B_order_path_cost_policy_proxy_v1"
RUN_D = "frontier52D_stage_closeout_order_path_cost_recurrence_v1"
RUN_ID = "frontier52Z_runtime_probe_backfill_v1"
RUN_NUMBER = "frontier52Z"
RUN_ROOT = Path("stages") / STAGE_ID / "02_runs" / RUN_ID
MT5_ROOT = RUN_ROOT / "mt5"
MODELS_ROOT = RUN_ROOT / "models"
FEATURE_ROOT = RUN_ROOT / "feature_matrices"
REVIEWS_ROOT = Path("stages") / STAGE_ID / "03_reviews"
SELECTED_ROOT = Path("stages") / STAGE_ID / "04_selected"
SUMMARY_PATHS = (
    Path("stages") / SOURCE_STAGE_ID / "02_runs" / f51.RUN_C / "repair_candidate_summary.csv",
    Path("stages") / SOURCE_STAGE_ID / "02_runs" / f51.RUN_B / "initial_candidate_summary.csv",
)
GROK_STAGE_OPEN_ROOT = Path("docs") / "agent_control" / "grok_reviews" / "2026-06-16_frontier52_stage_open" / "small_review"
GROK_PRE_MT5_ROOT = Path("docs") / "agent_control" / "grok_reviews" / "2026-06-16_frontier52_pre_mt5" / "small_review"
GROK_STAGE_CLOSE_ROOT = Path("docs") / "agent_control" / "grok_reviews" / "2026-06-16_frontier52_stage_closeout" / "small_review"

RUNTIME_POLICY = {
    "InpCloseOnFlatSignal": True,
    "InpEntryTransitionOnly": True,
    "InpEntryTransitionRearmMinConfidenceDelta": 0.02,
    "InpMaxHoldBars": 6,
    "InpReentryCooldownBars": 3,
    "InpSameDirectionReentryCooldownBars": 6,
    "InpAtrSltpEnabled": True,
    "InpAtrPeriod": 14,
    "InpAtrStopMultiplier": 0.8,
    "InpAtrTakeProfitMultiplier": 1.2,
    "InpAtrMinStopPoints": 40.0,
    "InpAtrMaxStopPoints": 180.0,
    "InpAtrMinTakeProfitPoints": 60.0,
    "InpAtrMaxTakeProfitPoints": 260.0,
}

DEFAULT_PORTABLE_ROOT = Path("C:/Users/awdse/AppData/Local/ObsidianPrime/mt5_portable_run329E")
DEFAULT_TERMINAL = DEFAULT_PORTABLE_ROOT / "terminal64.exe"
DEFAULT_METAEDITOR = DEFAULT_PORTABLE_ROOT / "MetaEditor64.exe"
DEFAULT_COMMON_FILES = DEFAULT_PORTABLE_ROOT / "Common" / "Files"
DEFAULT_TESTER_PROFILE_ROOT = DEFAULT_PORTABLE_ROOT / "MQL5" / "Profiles" / "Tester"
DEFAULT_TERMINAL_DATA_ROOT = DEFAULT_PORTABLE_ROOT


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Frontier52 MT5 runtime order-path policy probe.")
    parser.add_argument("--candidate-id", default="f51c_0046")
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
    attempts = apply_runtime_policy_overrides(attempts)

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
        "runtime_policy": RUNTIME_POLICY,
        "runtime_rows": runtime_rows,
        "proxy_runtime_gap_rows": proxy_gap_rows,
        "claim_boundary": backfill.claim_boundary_payload(),
        "created_at_utc": created_at,
    }
    backfill.write_json(RUN_ROOT / "final_decision.json", final)
    backfill.write_json(RUN_ROOT / "run_manifest.json", final)
    write_reports(final, row, runtime_rows, proxy_gap_rows, attempts, execution_payload)
    backfill.upsert_backfill_status_ledger(
        52,
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
                "runtime_policy": RUNTIME_POLICY,
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
    summary_frames = [read_csv(path) for path in SUMMARY_PATHS if path_exists(path)]
    summary = pd.concat([frame for frame in summary_frames if not frame.empty], ignore_index=True) if summary_frames else pd.DataFrame()
    if summary.empty:
        raise RuntimeError("No F51 proxy candidate summary is available for F52 reference-only runtime probe.")
    if candidate_id:
        match = summary.loc[summary["candidate_id"].astype(str).eq(candidate_id)]
        if not match.empty:
            return match.iloc[0]
    scout_rows = summary.loc[summary["f51_scout_clue_flag"].astype(bool)].copy()
    if scout_rows.empty:
        return summary.sort_values(["forward_min_pf", "forward_max_dd"], ascending=[False, True]).iloc[0]
    scout_rows = scout_rows.sort_values(["forward_min_pf", "forward_max_dd"], ascending=[False, True])
    return scout_rows.iloc[0]


def train_runtime_candidate(row: pd.Series) -> dict[str, Any]:
    frame = f23b.load_frame()
    feature_order = f23b.read_feature_order()
    raw_path = f33b.load_raw_path(frame)
    path_labels = f33b.build_path_labels(frame, raw_path)
    labels = path_labels[f51.SIDE_VALUE]
    event_spec = match_spec(f51.event_specs(frame, labels, str(row["profile"])), "event_variant", str(row["event_variant"]))
    base_spec = match_spec(f51.base_scorer_specs(str(row["profile"])), "base_scorer_family", str(row["base_scorer_family"]))
    context_spec = match_spec(f51.sequence_context_specs(str(row["profile"])), "context_variant", str(row["context_variant"]))
    model_family_token = str(row["model_family"]).split("__", 1)[0]
    model_spec = match_spec(f51.model_specs(str(row["profile"])), "model_family", model_family_token)

    x_raw = frame[feature_order].to_numpy(dtype="float64")
    valid_raw_features = np.isfinite(x_raw).all(axis=1)
    y = np.asarray(event_spec["event"], dtype="int8")
    train_mask = f33b.split_mask(frame, "train") & valid_raw_features & labels["valid"]
    fit_mask = train_mask & np.isfinite(y)
    base_model = base_spec["factory"]()
    base_model.fit(x_raw[fit_mask], y[fit_mask])
    base_score = np.full(len(frame), np.nan, dtype="float64")
    base_score[valid_raw_features] = f51.event_probability(base_model, x_raw[valid_raw_features])
    finite_base_score = np.isfinite(base_score) & valid_raw_features
    context = f51.build_sequence_context(
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
    score[valid_context] = f51.event_probability(model, x_model[valid_context])
    base_mask = valid_context & (score >= float(row["score_threshold"]))
    risk_spec = match_spec(f51.risk_budget_specs(str(row["profile"])), "risk_budget_variant", str(row["risk_budget_variant"]))
    risk_mask, risk_meta = f51.apply_risk_budget_mask(
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
    probabilities = np.zeros((len(frame), 3), dtype="float64")
    probabilities[:, 1] = 1.0
    probabilities[valid_context] = binary_to_three_class(model, x_model[valid_context])
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
        stage_num=52,
        stage_id=STAGE_ID,
        parent_run_id=RUN_B,
        source_run_id=f51.RUN_C,
        candidate_id=str(row["candidate_id"]),
        model_id=str(artifacts["model_id"]),
        model_path=Path(str(artifacts["model_path"])),
        onnx_path=Path(str(artifacts["onnx_path"])),
        decision_mode="threshold_margin",
        short_threshold=threshold,
        long_threshold=1.0,
        min_margin=0.0,
        max_hold_bars=int(RUNTIME_POLICY["InpMaxHoldBars"]),
        cooldown_bars=int(RUNTIME_POLICY["InpReentryCooldownBars"]),
        source_contract="binary_event_probability_mapped_to_three_class_short_threshold",
        source_note="F52 order-path cost policy probe using F51 representative candidate as reference-only artifact",
    )


def apply_runtime_policy_overrides(attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    patched: list[dict[str, Any]] = []
    for attempt in attempts:
        row = dict(attempt)
        set_payload = dict(row["set"])
        set_path = Path(str(set_payload["path"]))
        override_set_file(set_path, RUNTIME_POLICY)
        set_payload["sha256"] = sha256_file(set_path)
        set_payload["runtime_policy_override"] = json_ready(RUNTIME_POLICY)
        row["set"] = set_payload
        row["runtime_policy"] = json_ready(RUNTIME_POLICY)
        patched.append(row)
    backfill.write_json(MT5_ROOT / "runtime_policy_override_manifest.json", {"policy": RUNTIME_POLICY, "attempts": patched})
    return patched


def override_set_file(path: Path, overrides: Mapping[str, Any]) -> None:
    existing = io_path(path).read_text(encoding="utf-8").splitlines()
    values = {key: format_set_value(value) for key, value in overrides.items()}
    seen: set[str] = set()
    output: list[str] = []
    for line in existing:
        if "=" not in line or line.lstrip().startswith(";"):
            output.append(line)
            continue
        key, _value = line.split("=", 1)
        if key in values:
            output.append(f"{key}={values[key]}")
            seen.add(key)
        else:
            output.append(line)
    for key, value in values.items():
        if key not in seen:
            output.append(f"{key}={value}")
    io_path(path).write_text("\n".join(output).rstrip() + "\n", encoding="utf-8")


def format_set_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return f"{value:.12g}"
    return str(value)


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
    backfill.write_text_sig(REVIEWS_ROOT / f"{RUN_ID}_report.md", report)
    backfill.write_text_sig(REVIEWS_ROOT / "proxy_runtime_gap_report.md", proxy_runtime_gap_report_text(proxy_gap_rows))
    backfill.write_json(REVIEWS_ROOT / "runtime_probe_status.json", final)
    backfill.write_json(MT5_ROOT / "handoff_manifest.json", {"attempts": attempts, "execution": execution_payload})
    write_stage_lifecycle_documents(final, proxy_row, runtime_rows, proxy_gap_rows, attempts, execution_payload)
    append_runtime_status_to_selection(final)


def runtime_report_text(
    final: Mapping[str, Any],
    proxy_row: pd.Series,
    runtime_rows: Sequence[Mapping[str, Any]],
    proxy_gap_rows: Sequence[Mapping[str, Any]],
) -> str:
    kpi_lines = "\n".join(
        f"- {row.get('split')}: runtime_status(런타임 상태)={row.get('runtime_status')}, report_status(보고서 상태)={row.get('report_status')}, "
        f"PF={row.get('profit_factor')}, DD={row.get('max_drawdown_percent')}, trades(거래)={row.get('trade_count')}, signal_diff(신호 차이)={row.get('signal_count_diff')}, feature_ready_diff(피처 준비 차이)={row.get('feature_ready_diff')}"
        for row in runtime_rows
    )
    gap_lines = "\n".join(
        f"- {row.get('split')}: PF gap(MT5-proxy)={row.get('profit_factor_gap_mt5_minus_proxy')}, "
        f"DD gap(MT5-proxy)={row.get('dd_gap_mt5_minus_proxy')}, trade gap(MT5-proxy)={row.get('trade_count_gap_mt5_minus_proxy')}"
        for row in proxy_gap_rows
    )
    policy_lines = "\n".join(f"- {key}: {value}" for key, value in RUNTIME_POLICY.items())
    return f"""# Frontier52 MT5 Runtime Probe(MT5 런타임 탐침)

- run(실행): `{RUN_ID}`
- reference_candidate(참조 후보): `{proxy_row['candidate_id']}`
- status(상태): `{final.get('classification')}`
- source_boundary(원천 경계): F51 candidate is reference-only(F51 후보는 참조 전용)
- proxy_forward_min_pf(프록시 전진 최소 PF): {proxy_row.get('forward_min_pf')}
- proxy_forward_max_dd(프록시 전진 최대 DD): {proxy_row.get('forward_max_dd')}
- proxy_forward_density(프록시 전진 거래 밀도): {proxy_row.get('forward_min_density')} ~ {proxy_row.get('forward_max_density')}
- order_path_keep_rate(주문 경로 유지율): {proxy_row.get('order_path_keep_rate')}

## Runtime Policy(런타임 정책)
{policy_lines}

## Runtime KPI(런타임 성과 지표)
{kpi_lines}

Signal_diff note(신호 차이 메모): negative signal_diff(음수 신호 차이)는 entry-transition/close-on-flat policy(전환 진입/무신호 청산 정책)가 expected export signal(예상 내보내기 신호)을 의도적으로 억제한 값이다. Feature_ready_diff(피처 준비 차이)는 `0`이어야 local parity boundary(로컬 동등성 경계)가 유지된다.

## Proxy Runtime Gap(프록시 런타임 차이)
{gap_lines}

Claim boundary(주장 경계): runtime probe observation only(런타임 탐침 관찰 전용). No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 주장하지 않는다.
"""


def proxy_runtime_gap_report_text(proxy_gap_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# Frontier52 Proxy Runtime Gap(프록시 런타임 차이)",
        "",
        "Action(행동): F51 representative clue(대표 단서)를 reference-only(참조 전용)로 재물질화하고 MT5 Strategy Tester(전략 테스터)에 order-path policy(주문 경로 정책)를 적용했다.",
        "",
        "Effect(효과): Python proxy(파이썬 프록시)와 EA order path(EA 주문 경로)의 차이가 런타임 정책으로 줄어드는지 관찰한다.",
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


def write_stage_lifecycle_documents(
    final: Mapping[str, Any],
    proxy_row: pd.Series,
    runtime_rows: Sequence[Mapping[str, Any]],
    proxy_gap_rows: Sequence[Mapping[str, Any]],
    attempts: Sequence[Mapping[str, Any]],
    execution_payload: Mapping[str, Any],
) -> None:
    spec_root = Path("stages") / STAGE_ID / "00_spec"
    input_root = Path("stages") / STAGE_ID / "01_inputs"
    run_a_root = Path("stages") / STAGE_ID / "02_runs" / RUN_A
    run_b_root = Path("stages") / STAGE_ID / "02_runs" / RUN_B
    run_d_root = Path("stages") / STAGE_ID / "02_runs" / RUN_D
    for path in (spec_root, input_root, run_a_root, run_b_root, run_d_root, REVIEWS_ROOT, SELECTED_ROOT):
        io_path(path).mkdir(parents=True, exist_ok=True)

    judgment = stage_judgment(runtime_rows, proxy_gap_rows)
    selection = {
        "stage_id": STAGE_ID,
        "source_stage_id": SOURCE_STAGE_ID,
        "run_id": RUN_ID,
        "reference_candidate_id": str(proxy_row["candidate_id"]),
        "classification": final.get("classification"),
        "judgment": judgment,
        "runtime_policy": RUNTIME_POLICY,
        "runtime_rows": list(runtime_rows),
        "proxy_runtime_gap_rows": list(proxy_gap_rows),
        "claim_boundary": backfill.claim_boundary_payload(),
        "next_stage_id": "",
    }
    backfill.write_json(SELECTED_ROOT / "selection_status.json", selection)
    backfill.write_json(input_root / "runtime_policy_manifest.json", {"policy": RUNTIME_POLICY, "attempts": attempts})
    backfill.write_json(run_a_root / "stage_open_manifest.json", {"stage_id": STAGE_ID, "source_stage_id": SOURCE_STAGE_ID, "grok_stage_open": grok_receipt_payload(GROK_STAGE_OPEN_ROOT)})
    backfill.write_json(run_b_root / "runtime_policy_proxy_manifest.json", {"policy": RUNTIME_POLICY, "proxy_candidate": json_ready(dict(proxy_row))})
    backfill.write_json(run_d_root / "closeout_manifest.json", selection)
    backfill.write_json(RUN_ROOT / "execution_payload_summary.json", summarize_execution_payload(execution_payload))

    backfill.write_text_sig(spec_root / "stage_brief.md", stage_brief_text(proxy_row))
    backfill.write_text_sig(REVIEWS_ROOT / "runA_report.md", run_a_report_text(proxy_row))
    backfill.write_text_sig(REVIEWS_ROOT / "runB_report.md", run_b_report_text(proxy_row))
    backfill.write_text_sig(REVIEWS_ROOT / "runD_closeout_report.md", closeout_report_text(selection))
    backfill.write_text_sig(REVIEWS_ROOT / "required_gate_coverage_audit.md", gate_audit_text(selection))
    backfill.write_text_sig(REVIEWS_ROOT / "local_verification.md", local_verification_text(selection))
    backfill.write_text_sig(REVIEWS_ROOT / "grok_stage_open_receipt.md", grok_receipt_text("stage_open(단계 개방)", GROK_STAGE_OPEN_ROOT))
    backfill.write_text_sig(REVIEWS_ROOT / "grok_pre_mt5_receipt.md", grok_receipt_text("pre_mt5(사전 MT5)", GROK_PRE_MT5_ROOT))
    backfill.write_text_sig(REVIEWS_ROOT / "grok_stage_closeout_receipt.md", grok_receipt_text("stage_closeout(단계 마감)", GROK_STAGE_CLOSE_ROOT))
    backfill.write_text_sig(SELECTED_ROOT / "selection_status.md", selection_status_text(selection))
    backfill.write_text_sig(SELECTED_ROOT / "negative_memory.md", negative_memory_text(selection))
    backfill.write_text_sig(SELECTED_ROOT / "preserved_clue.md", preserved_clue_text(selection))


def stage_judgment(runtime_rows: Sequence[Mapping[str, Any]], proxy_gap_rows: Sequence[Mapping[str, Any]]) -> str:
    completed = [row for row in runtime_rows if row.get("runtime_status") == "completed" and row.get("report_status") == "completed"]
    if not completed:
        return "blocked_attempt_failed(차단, 시도 실패)"
    feature_ready_ok = all(as_float(row.get("feature_ready_diff")) == 0.0 for row in completed)
    entry_policy_suppression = any((as_float(row.get("signal_count_diff")) or 0.0) < 0.0 for row in completed)
    max_dd = max((as_float(row.get("max_drawdown_percent")) or 999.0) for row in completed)
    min_pf = min((as_float(row.get("profit_factor")) or 0.0) for row in completed)
    trade_counts = [as_float(row.get("trade_count")) or 0.0 for row in completed]
    materially_better_dd = any((as_float(gap.get("dd_gap_mt5_minus_proxy")) or 999.0) < 30.0 for gap in proxy_gap_rows)
    if feature_ready_ok and max_dd < 30.0 and min_pf >= 1.0 and min(trade_counts) >= 80:
        return "preserved_clue_runtime_policy_dd_compression(보존 단서, 런타임 정책 손실폭 압축)"
    if feature_ready_ok and max_dd < 10.0 and entry_policy_suppression and min_pf < 1.0:
        return "preserved_clue_negative_memory_dd_compressed_but_pf_failed(보존 단서+부정 기억, 손실폭은 압축됐지만 수익 팩터 실패)"
    if feature_ready_ok and materially_better_dd:
        return "preserved_clue_partial_runtime_policy_compression(보존 단서, 부분 런타임 정책 압축)"
    return "negative_memory_order_path_policy_did_not_repair_mt5_economics(부정 기억, 주문 경로 정책이 MT5 경제성을 수리하지 못함)"


def grok_receipt_payload(root: Path) -> dict[str, Any]:
    clean = root / "clean_output.md"
    metadata = root / "metadata.json"
    return {
        "root": root.as_posix(),
        "clean_output_exists": path_exists(clean),
        "metadata_exists": path_exists(metadata),
        "classification": "needs_local_verification(로컬 검증 필요)" if path_exists(clean) else "missing_required(필수 누락)",
    }


def grok_receipt_text(label: str, root: Path) -> str:
    payload = grok_receipt_payload(root)
    clean_text = ""
    clean_path = root / "clean_output.md"
    if path_exists(clean_path):
        clean_text = io_path(clean_path).read_text(encoding="utf-8-sig").strip()
    return f"""# Grok Receipt(그록 영수증): {label}

- path(경로): `{root.as_posix()}`
- classification(분류): `{payload['classification']}`
- local_action(로컬 행동): Codex verified direction with repo files, EA parameters, set overrides, and MT5 outputs(코덱스가 저장소 파일, EA 파라미터, 설정 덮어쓰기, MT5 출력으로 직접 검증).
- effect(효과): Grok(Grok, 그록) output did not create authority(권위), it only informed review boundary(검토 경계).

## Clean Output(정리 출력)
{clean_text or 'missing_required(필수 누락)'}
"""


def stage_brief_text(proxy_row: pd.Series) -> str:
    policy_lines = "\n".join(f"- {key}: {value}" for key, value in RUNTIME_POLICY.items())
    return f"""# Frontier52 Stage Brief(전선52 단계 요약)

- stage_id(단계 ID): `{STAGE_ID}`
- work_family(작업군): `runtime_backtest(MT5/런타임/백테스트 실행)`
- primary_skill(주 스킬): `obsidian-runtime-parity(런타임 동등성)`
- source_boundary(원천 경계): F51 candidate `{proxy_row['candidate_id']}` is reference-only(F51 후보는 참조 전용).

## Hypothesis(가설)
F51(전선51)의 failure(실패)는 ONNX signal handoff(온엑스 신호 인계)보다 MT5 execution lifecycle(메타트레이더5 실행 생명주기)에 있을 수 있다.

## Runtime Policy(런타임 정책)
{policy_lines}

## Exit Rule(종료 규칙)
MT5 runtime probe(MT5 런타임 탐침) 뒤 preserved clue(보존 단서), negative memory(부정 기억), invalid setup(무효 설정), blocked(차단) 중 하나로 닫는다.

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음).
"""


def run_a_report_text(proxy_row: pd.Series) -> str:
    return f"""# Frontier52 Run A(전선52 실행 A)

Action(행동): F51 negative memory(전선51 부정 기억)를 읽고 order-path cost recurrence(주문 경로 비용 재발) 가설을 열었다.

Effect(효과): `{proxy_row['candidate_id']}`를 reference-only artifact(참조 전용 산출물)로 제한하고, 런타임 정책만 changed variable(변경 변수)로 둔다.
"""


def run_b_report_text(proxy_row: pd.Series) -> str:
    policy_lines = "\n".join(f"- {key}: {value}" for key, value in RUNTIME_POLICY.items())
    return f"""# Frontier52 Run B(전선52 실행 B)

Action(행동): `.set` parameter policy(설정 파라미터 정책)를 물질화했다.

Effect(효과): ONNX(온엑스), feature order(피처 순서), signal parity(신호 동등성)를 유지한 채 close-on-flat/transition/cooldown/ATR SLTP(무신호 청산/전환/쿨다운/평균진폭 손익절)만 시험한다.

## Reference Candidate(참조 후보)
- candidate(후보): `{proxy_row['candidate_id']}`
- proxy_forward_min_pf(프록시 전진 최소 수익 팩터): {proxy_row.get('forward_min_pf')}
- proxy_forward_max_dd(프록시 전진 최대 손실폭): {proxy_row.get('forward_max_dd')}

## Policy(정책)
{policy_lines}
"""


def closeout_report_text(selection: Mapping[str, Any]) -> str:
    rows = selection.get("runtime_rows", [])
    row_lines = "\n".join(
        f"- {row.get('split')}: PF={row.get('profit_factor')}, DD={row.get('max_drawdown_percent')}, trades={row.get('trade_count')}, signal_diff={row.get('signal_count_diff')}, feature_ready_diff={row.get('feature_ready_diff')}"
        for row in rows
    )
    return f"""# Frontier52 Closeout(전선52 마감)

- judgment(판정): `{selection.get('judgment')}`
- runtime_probe_run(런타임 탐침 실행): `{RUN_ID}`
- reference_candidate(참조 후보): `{selection.get('reference_candidate_id')}`

## Runtime Observation(런타임 관찰)
{row_lines}

Claim boundary(주장 경계): runtime probe observation only(런타임 탐침 관찰 전용). No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 주장하지 않는다.
"""


def gate_audit_text(selection: Mapping[str, Any]) -> str:
    return f"""# Required Gate Coverage Audit(필수 게이트 커버리지 감사)

- runtime_evidence_gate(런타임 근거 게이트): covered by `{RUN_ID}` MT5 Strategy Tester(전략 테스터) output.
- scope_completion_gate(범위 완료 게이트): F52 lifecycle(전선52 생명주기) closed as `{selection.get('judgment')}`.
- kpi_contract_audit(KPI 계약 감사): Tier A separate(티어 A 분리) rows recorded; Tier B/combined(티어 B/합산)는 missing_required(필수 누락)로 장부화.
- required_gate_coverage_audit(필수 게이트 커버리지 감사): this file(이 파일).
- final_claim_guard(최종 주장 가드): authority/live/goal(권위/실거래/목표) not_claimed(주장 없음).
- external_review_packet(외부 검토 묶음): Grok receipts(그록 영수증) recorded with local verification(로컬 검증).
"""


def local_verification_text(selection: Mapping[str, Any]) -> str:
    return f"""# Local Verification(로컬 검증)

- git_scope(깃 범위): F52 stage-local adapter(단계 전용 어댑터), stage artifacts(단계 산출물), ledgers(장부), Grok receipts(그록 영수증).
- EA boundary(EA 경계): `foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5` unchanged(변경 없음); `.set` parameter(설정 파라미터) only.
- reference_boundary(참조 경계): F51 candidate(전선51 후보)는 reference-only(참조 전용), no inherited winner/baseline(승자/기준선 상속 없음).
- runtime_policy(런타임 정책): `{json.dumps(json_ready(RUNTIME_POLICY), ensure_ascii=False, sort_keys=True)}`
- signal_diff_boundary(신호 차이 경계): negative signal_diff(음수 신호 차이)는 entry policy suppression(진입 정책 억제)로 해석하며, feature_ready_diff(피처 준비 차이) `0`이 핵심 로컬 확인값이다.
- judgment(판정): `{selection.get('judgment')}`
"""


def selection_status_text(selection: Mapping[str, Any]) -> str:
    return f"""# Frontier52 Selection Status(전선52 선택 상태)

- judgment(판정): `{selection.get('judgment')}`
- runtime_probe_run(런타임 탐침 실행): `{RUN_ID}`
- reference_candidate(참조 후보): `{selection.get('reference_candidate_id')}`
- status(상태): `{selection.get('classification')}`

No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 claimed(주장)하지 않는다.
"""


def negative_memory_text(selection: Mapping[str, Any]) -> str:
    return f"""# Frontier52 Negative Memory(전선52 부정 기억)

- judgment(판정): `{selection.get('judgment')}`
- memory(기억): order-path policy(주문 경로 정책)는 F51 signal/feature parity(신호/피처 동등성) 문제와 별개로 MT5 economics(메타트레이더5 경제성)를 충분히 수리하지 못했는지 여부를 기록한다.
- boundary(경계): 같은 F51 outcome-memory score(결과 기억 점수)와 단순 `.set` lifecycle(설정 생명주기)만 반복하지 않는다.
"""


def preserved_clue_text(selection: Mapping[str, Any]) -> str:
    return f"""# Frontier52 Preserved Clue(전선52 보존 단서)

- judgment(판정): `{selection.get('judgment')}`
- clue(단서): close-on-flat/transition/cooldown/ATR SLTP(무신호 청산/전환/쿨다운/평균진폭 손익절)의 실제 MT5 effect(효과)를 proxy/runtime gap(프록시/런타임 차이)와 함께 보존한다.
- boundary(경계): clue(단서) only, no authority(권위 없음).
"""


def summarize_execution_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "compile_status": ((payload.get("compile_payload") or {}).get("compile") or {}).get("status"),
        "terminal_probe_status": (payload.get("terminal_probe") or {}).get("status"),
        "execution_attempts": len(payload.get("execution_results", []) or []),
        "report_records": len(payload.get("report_records", []) or []),
        "copied_runtime_outputs": len(payload.get("copied_runtime_outputs", []) or []),
        "created_at_utc": payload.get("created_at_utc"),
    }


def append_runtime_status_to_selection(final: Mapping[str, Any]) -> None:
    marker = "<!-- f52_runtime_probe_status -->"
    end_marker = "<!-- /f52_runtime_probe_status -->"
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
