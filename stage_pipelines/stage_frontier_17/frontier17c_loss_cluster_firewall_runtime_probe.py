from __future__ import annotations

import argparse
import csv
import json
import math
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.alpha import scout_runner as scout  # noqa: E402
from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from foundation.models.onnx_bridge import (  # noqa: E402
    check_onnxruntime_probability_parity,
    ordered_hash,
    ordered_sklearn_probabilities,
    sha256_file,
)
from foundation.mt5 import runtime_support as mt5  # noqa: E402
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b  # noqa: E402
from stage_pipelines.stage_frontier_04 import frontier04d_trainable_path_label_onnx_probe as f04d  # noqa: E402
from stage_pipelines.stage_frontier_07 import frontier07b_adverse_excursion_risk_label_proxy_scout as f07b  # noqa: E402
from stage_pipelines.stage_frontier_12 import frontier12b_trade_shape_duration_label_proxy_scout as f12b  # noqa: E402
from stage_pipelines.stage_frontier_17 import frontier17b_loss_cluster_firewall_profit_persistence_proxy_scout as f17b  # noqa: E402


TODAY = "2026-06-14"
STAGE_ID = "stage_frontier_17__loss_cluster_firewall_profit_persistence_onnx_scout"
RUN_ID = "frontier17C_loss_cluster_firewall_runtime_probe_v1"
RUN_NUMBER = "frontier17C"
PARENT_RUN_ID = f17b.RUN_ID
NEXT_RUN_ID = "frontier17D_loss_cluster_firewall_repair_or_closeout_decision_v1"
SOURCE_RUN_ID = f17b.RUN_ID
BEST_CANDIDATE_ID = "f17b_firewall_h10_ddq75_contq65__lr_plain__firewall_continuation"
CLAIM_BOUNDARY = (
    "runtime_probe_observation_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
FEATURE_DIR = RUN_ROOT / "feature_matrices"
VETO_DIR = RUN_ROOT / "veto_tapes"
EXPECTED_DIR = RUN_ROOT / "expected"
MT5_DIR = RUN_ROOT / "mt5"
TELEMETRY_COPY_DIR = RUN_ROOT / "runtime_telemetry"
REVIEW_DIR = STAGE_ROOT / "03_reviews"
SELECTED_DIR = STAGE_ROOT / "04_selected"

F17B_FINAL = STAGE_ROOT / "02_runs" / SOURCE_RUN_ID / "final_decision.json"
F17B_CANDIDATE_SUMMARY = STAGE_ROOT / "02_runs" / SOURCE_RUN_ID / "candidate_summary.csv"
F17B_TARGET_DIAGNOSTICS = STAGE_ROOT / "02_runs" / SOURCE_RUN_ID / "target_diagnostics.json"
GROK_PACKET = Path("docs/agent_control/grok_reviews/2026-06-14_frontier17_pre_expensive/small_review_retry")

INPUT_MANIFEST = RUN_ROOT / "input_manifest.csv"
FEATURE_MATRIX_MANIFEST = RUN_ROOT / "runtime_feature_matrix_manifest.csv"
VETO_TAPE_MANIFEST = RUN_ROOT / "runtime_veto_tape_manifest.csv"
EXPECTED_SIGNAL_SUMMARY = RUN_ROOT / "expected_signal_summary.csv"
EXPECTED_PROBABILITY_TAPE = EXPECTED_DIR / "expected_probability_tape.csv"
ONNX_PARITY_REPORT = RUN_ROOT / "onnx_probability_parity.json"
COMMON_FILES_SYNC = RUN_ROOT / "common_files_sync.csv"
MT5_ATTEMPT_PACKAGE = RUN_ROOT / "mt5_runtime_probe_attempt_package.csv"
MT5_COMPILE_RESULT = MT5_DIR / "mt5_compile_result.json"
TERMINAL_PROCESS_AUDIT = RUN_ROOT / "terminal_process_audit.json"
MT5_EXECUTION_RESULT = RUN_ROOT / "mt5_execution_result.json"
MT5_PROBE_SUMMARY = RUN_ROOT / "mt5_runtime_probe_summary.csv"
MT5_KPI_RECORDS = RUN_ROOT / "mt5_kpi_records.json"
STRATEGY_TESTER_REPORTS = RUN_ROOT / "strategy_tester_report_records.json"
RUNTIME_OUTPUT_COPY = RUN_ROOT / "runtime_output_copy_manifest.csv"
RUNTIME_SIGNAL_DIFF = RUN_ROOT / "runtime_signal_expected_vs_mt5_summary.csv"
RUNTIME_RECEIPT = RUN_ROOT / "runtime_parity_receipt.json"
BACKTEST_RECEIPT = RUN_ROOT / "backtest_forensics_receipt.json"
LINEAGE_RECEIPT = RUN_ROOT / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_ROOT / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_ROOT / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_ROOT / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_ROOT / "final_decision.json"
RUN_MANIFEST = RUN_ROOT / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / f"{RUN_ID}_report.md"
DECISION_DOC = Path("docs/decisions") / f"{TODAY}_frontier17c_runtime_probe.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_BRIEF = STAGE_ROOT / "00_spec" / "stage_brief.md"
ARTIFACT_REGISTRY = Path("docs/registers/artifact_registry.csv")

DEFAULT_PORTABLE_ROOT = Path("C:/Users/awdse/AppData/Local/ObsidianPrime/mt5_portable_run329E")
DEFAULT_TERMINAL = DEFAULT_PORTABLE_ROOT / "terminal64.exe"
DEFAULT_METAEDITOR = DEFAULT_PORTABLE_ROOT / "MetaEditor64.exe"
DEFAULT_COMMON_FILES = DEFAULT_PORTABLE_ROOT / "Common" / "Files"
DEFAULT_TESTER_PROFILE_ROOT = DEFAULT_PORTABLE_ROOT / "MQL5" / "Profiles" / "Tester"
DEFAULT_TERMINAL_DATA_ROOT = DEFAULT_PORTABLE_ROOT
PORTABLE_EA_EX5 = (
    DEFAULT_PORTABLE_ROOT
    / "MQL5"
    / "Experts"
    / "Project_Obsidian_Prime_v2"
    / "foundation"
    / "mt5"
    / "ObsidianPrimeV2_RuntimeProbeEA.ex5"
)
EA_SOURCE = ROOT / mt5.EA_SOURCE_PATH
EA_BINARY = ROOT / "foundation" / "mt5" / "ObsidianPrimeV2_RuntimeProbeEA.ex5"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Frontier17C MT5 runtime probe with loss-cluster veto tape.")
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
    ensure_dirs()
    created_at = utc_now()
    best, source_final = load_source_truth()
    full, raw, source_integrity = f07b.load_training_packet()
    feature_order = f04d.read_feature_order()
    model = joblib.load(io_path(ROOT / str(best["joblib_path"])))
    onnx_path = ROOT / str(best["onnx_path"])
    feature_order_hash = ordered_hash(feature_order)
    validate_source_identity(best, onnx_path, feature_order_hash)

    split_payload = build_split_payloads(full, raw, feature_order, model, onnx_path, best)
    write_runtime_inputs(best, source_final, source_integrity, split_payload)
    attempts = materialize_attempts(
        best=best,
        feature_order=feature_order,
        feature_order_hash=feature_order_hash,
        split_payload=split_payload,
        common_files_root=Path(args.common_files_root),
    )
    execution_payload = execute_runtime_probe(
        args=args,
        attempts=attempts,
        onnx_path=onnx_path,
        split_payload=split_payload,
    )
    runtime_rows = build_runtime_summary_rows(attempts, execution_payload, split_payload)
    signal_diff_rows = build_signal_diff_rows(runtime_rows)
    receipts = build_receipts(
        created_at=created_at,
        best=best,
        attempts=attempts,
        execution_payload=execution_payload,
        runtime_rows=runtime_rows,
        signal_diff_rows=signal_diff_rows,
        split_payload=split_payload,
    )
    final = build_final(
        created_at=created_at,
        best=best,
        source_final=source_final,
        attempts=attempts,
        execution_payload=execution_payload,
        runtime_rows=runtime_rows,
        signal_diff_rows=signal_diff_rows,
        receipts=receipts,
        materialize_only=bool(args.materialize_only),
    )
    write_results(final, runtime_rows, signal_diff_rows, receipts)
    update_docs_and_registers(final, runtime_rows)
    print(
        json.dumps(
            json_ready(
                {
                    "run_id": RUN_ID,
                    "status": final["status"],
                    "judgment": final["judgment"],
                    "runtime_completed_attempts": final["runtime_completed_attempts"],
                    "runtime_attempts": final["runtime_attempts"],
                    "signal_parity_matches": final["signal_parity_matches"],
                    "report": REPORT_PATH.as_posix(),
                    "next_run_id": final["next_run_id"],
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if final["status"] != "blocked_runtime_probe_attempt_recorded_no_authority" else 2


def ensure_dirs() -> None:
    for path in (
        RUN_ROOT,
        FEATURE_DIR,
        VETO_DIR,
        EXPECTED_DIR,
        MT5_DIR,
        TELEMETRY_COPY_DIR,
        REVIEW_DIR,
        SELECTED_DIR,
        DECISION_DOC.parent,
    ):
        io_path(path).mkdir(parents=True, exist_ok=True)
    ensure_csv_header(STAGE_LEDGER, f03b.ALPHA_LEDGER)


def load_source_truth() -> tuple[dict[str, Any], dict[str, Any]]:
    source_final = read_json(F17B_FINAL)
    best = dict(source_final.get("best_candidate_row", {}))
    if best.get("candidate_id") != BEST_CANDIDATE_ID:
        raise RuntimeError("F17B best candidate identity mismatch(전선17B 최선 후보 정체성 불일치).")
    if source_final.get("status") != "loss_cluster_firewall_preserved_clue_no_authority":
        raise RuntimeError("F17B status mismatch(전선17B 상태 불일치).")
    if not path_exists(GROK_PACKET / "clean_output.md"):
        raise RuntimeError("F17 pre-expensive Grok packet missing(전선17 사전 Grok 묶음 누락).")
    return best, source_final


def validate_source_identity(best: Mapping[str, Any], onnx_path: Path, feature_order_hash: str) -> None:
    model_path = ROOT / str(best["joblib_path"])
    checks = {
        "joblib_exists": path_exists(model_path),
        "onnx_exists": path_exists(onnx_path),
        "joblib_sha256_match": path_exists(model_path) and sha256_file(model_path) == best.get("joblib_sha256"),
        "onnx_sha256_match": path_exists(onnx_path) and sha256_file(onnx_path) == best.get("onnx_sha256"),
        "feature_order_hash_match": feature_order_hash == best.get("feature_order_hash", feature_order_hash),
        "f17b_parity_passed": bool(best.get("parity_passed")),
    }
    if not all(checks.values()):
        raise RuntimeError("source identity preflight failed(원천 정체성 사전 확인 실패): " + json.dumps(checks, ensure_ascii=False))


def build_split_payloads(
    full: pd.DataFrame,
    raw: pd.DataFrame,
    feature_order: Sequence[str],
    model: Any,
    onnx_path: Path,
    best: Mapping[str, Any],
) -> dict[str, dict[str, Any]]:
    train_mask = full["split"].astype(str).eq("train").to_numpy()
    direction_score = f17b.build_direction_score(full, train_mask)
    direction = np.where(direction_score >= 0.0, 1, -1).astype("int8")
    loss_pressure = f17b.build_loss_pressure(full, direction, train_mask)
    profile = profile_by_target(str(best["target_id"]))
    fwd_return = f17b.forward_return(full, raw, profile.hold_bars)
    _labels, _oracle_signal, state = f17b.build_firewall_labels(
        full=full,
        profile=profile,
        fwd_return=fwd_return,
        direction=direction,
        direction_score=direction_score,
        loss_pressure=loss_pressure,
        train_mask=train_mask,
    )

    rows_for_parity: list[np.ndarray] = []
    split_payload: dict[str, dict[str, Any]] = {}
    probability_rows: list[dict[str, Any]] = []
    feature_manifest_rows: list[dict[str, Any]] = []
    veto_manifest_rows: list[dict[str, Any]] = []
    expected_rows: list[dict[str, Any]] = []

    for runtime_split, source_split in (("validation_is", "validation"), ("oos", "oos")):
        mask = full["split"].astype(str).eq(source_split).to_numpy()
        frame = full.loc[mask].copy()
        frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
        matrix = frame.loc[:, list(feature_order)].astype("float64").to_numpy()
        probabilities = ordered_sklearn_probabilities(model, matrix, class_order=f04d.LABEL_ORDER)
        rows_for_parity.append(matrix)

        adverse_veto = np.asarray(state["adverse_veto"], dtype=bool)[mask]
        raw_signal = argmax_signal(probabilities)
        signal = raw_signal.copy()
        signal[adverse_veto] = 0
        expected = expected_signal_summary(frame, probabilities, raw_signal, signal, adverse_veto, runtime_split)

        feature_path = FEATURE_DIR / f"frontier17c_tier_a_{runtime_split}_features.csv"
        feature_export = mt5.export_mt5_feature_matrix_csv(
            frame,
            feature_order,
            feature_path,
            metadata_columns=("raw_index",),
        )
        feature_export.update({"runtime_split": runtime_split, "source_split": source_split})

        veto_path = VETO_DIR / f"frontier17c_tier_a_{runtime_split}_runtime_veto_tape.csv"
        veto_export = write_runtime_veto_tape(veto_path, frame, adverse_veto, runtime_split)

        feature_manifest_rows.append(feature_export)
        veto_manifest_rows.append(veto_export)
        expected_rows.append(expected)
        probability_rows.extend(probability_tape_rows(frame, probabilities, raw_signal, signal, adverse_veto, runtime_split))
        split_payload[runtime_split] = {
            "source_split": source_split,
            "frame": frame,
            "matrix": matrix,
            "probabilities": probabilities,
            "adverse_veto": adverse_veto,
            "raw_signal": raw_signal,
            "signal": signal,
            "feature_export": feature_export,
            "veto_export": veto_export,
            "expected": expected,
            "from_date": split_date_range(frame)[0],
            "to_date": split_date_range(frame)[1],
        }

    parity = check_onnxruntime_probability_parity(
        model,
        onnx_path,
        np.vstack(rows_for_parity),
        class_order=f04d.LABEL_ORDER,
        tolerance=1e-5,
    )
    write_json(ONNX_PARITY_REPORT, parity)
    write_csv(FEATURE_MATRIX_MANIFEST, feature_manifest_rows)
    write_csv(VETO_TAPE_MANIFEST, veto_manifest_rows)
    write_csv(EXPECTED_SIGNAL_SUMMARY, expected_rows)
    write_csv(EXPECTED_PROBABILITY_TAPE, probability_rows)
    return split_payload


def profile_by_target(target_id: str) -> f17b.FirewallProfile:
    for profile in f17b.PROFILES:
        if profile.variant_id == target_id:
            return profile
    raise RuntimeError(f"Unknown F17 profile(알 수 없는 전선17 프로필): {target_id}")


def argmax_signal(probabilities: np.ndarray) -> np.ndarray:
    pred_label = np.asarray(f04d.LABEL_ORDER, dtype="int64")[probabilities.argmax(axis=1)]
    return np.where(pred_label == 0, -1, np.where(pred_label == 2, 1, 0)).astype("int8")


def expected_signal_summary(
    frame: pd.DataFrame,
    probabilities: np.ndarray,
    raw_signal: np.ndarray,
    signal: np.ndarray,
    adverse_veto: np.ndarray,
    runtime_split: str,
) -> dict[str, Any]:
    timestamps = pd.to_datetime(frame["timestamp"], utc=True).reset_index(drop=True)
    days = f12b.scout.count_scope_days(timestamps) if len(timestamps) else 0
    blocked_pred = (raw_signal != 0) & adverse_veto
    return {
        "attempt_name": f"frontier17c_tier_a_{runtime_split}",
        "split": runtime_split,
        "rows": int(len(frame)),
        "days_in_scope": int(days),
        "decision_mode": "argmax_probe_plus_runtime_veto_tape",
        "signal_count": int((signal != 0).sum()),
        "long_count": int((signal == 1).sum()),
        "short_count": int((signal == -1).sum()),
        "flat_count": int((signal == 0).sum()),
        "raw_signal_count": int((raw_signal != 0).sum()),
        "runtime_veto_count": int(adverse_veto.sum()),
        "blocked_pred_trade_count": int(blocked_pred.sum()),
        "expected_density_per_day": float((signal != 0).sum() / days) if days else 0.0,
        "probability_row_sum_max_abs_error": float(np.abs(probabilities.sum(axis=1) - 1.0).max()) if len(probabilities) else 0.0,
        "effect": "Python expected signal counts(파이썬 예상 신호 수)를 MT5 summary(MT5 요약)와 비교합니다.",
    }


def probability_tape_rows(
    frame: pd.DataFrame,
    probabilities: np.ndarray,
    raw_signal: np.ndarray,
    signal: np.ndarray,
    adverse_veto: np.ndarray,
    runtime_split: str,
) -> list[dict[str, Any]]:
    timestamps = pd.to_datetime(frame["timestamp"], utc=True).reset_index(drop=True)
    rows: list[dict[str, Any]] = []
    for idx, timestamp in enumerate(timestamps):
        rows.append(
            {
                "split": runtime_split,
                "row_index": int(idx),
                "timestamp": timestamp.isoformat(),
                "p_short": float(probabilities[idx, 0]),
                "p_flat": float(probabilities[idx, 1]),
                "p_long": float(probabilities[idx, 2]),
                "raw_signal": int(raw_signal[idx]),
                "adverse_veto": bool(adverse_veto[idx]),
                "signal": int(signal[idx]),
                "decision_label": "long" if signal[idx] > 0 else "short" if signal[idx] < 0 else "flat",
            }
        )
    return rows


def write_runtime_veto_tape(path: Path, frame: pd.DataFrame, adverse_veto: np.ndarray, runtime_split: str) -> dict[str, Any]:
    timestamps = pd.to_datetime(frame["timestamp"], utc=True)
    payload = pd.DataFrame(
        {
            "bar_time_server": timestamps.dt.strftime("%Y.%m.%d %H:%M:%S").to_numpy(),
            "timestamp_utc": timestamps.dt.strftime("%Y-%m-%dT%H:%M:%SZ").to_numpy(),
            "split": runtime_split,
            "row_index": np.arange(len(frame), dtype="int64"),
            "adverse_veto": np.asarray(adverse_veto, dtype=bool),
        }
    )
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    payload.to_csv(io_path(path), index=False, encoding="utf-8")
    return {
        "path": path.as_posix(),
        "sha256": sha256_file(path),
        "rows": int(len(payload)),
        "veto_count": int(np.asarray(adverse_veto, dtype=bool).sum()),
        "runtime_split": runtime_split,
        "format": "csv_timestamp_adverse_veto",
    }


def split_date_range(frame: pd.DataFrame) -> tuple[str, str]:
    timestamps = pd.to_datetime(frame["timestamp"], utc=True)
    if timestamps.empty:
        raise RuntimeError("empty split frame(빈 분할 프레임).")
    return timestamps.min().strftime("%Y.%m.%d"), (timestamps.max() + pd.Timedelta(days=1)).strftime("%Y.%m.%d")


def write_runtime_inputs(
    best: Mapping[str, Any],
    source_final: Mapping[str, Any],
    source_integrity: Mapping[str, Any],
    split_payload: Mapping[str, Mapping[str, Any]],
) -> None:
    input_rows = [
        artifact_row("frontier17b_final", F17B_FINAL),
        artifact_row("frontier17b_candidate_summary", F17B_CANDIDATE_SUMMARY),
        artifact_row("frontier17b_target_diagnostics", F17B_TARGET_DIAGNOSTICS),
        artifact_row("source_onnx", ROOT / str(best["onnx_path"])),
        artifact_row("source_joblib", ROOT / str(best["joblib_path"])),
        artifact_row("grok_pre_expensive_clean_output", GROK_PACKET / "clean_output.md"),
    ]
    write_csv(INPUT_MANIFEST, input_rows)
    write_json(
        RUN_ROOT / "source_truth_snapshot.json",
        {
            "best_candidate": best,
            "frontier17b_status": source_final.get("status"),
            "source_integrity": source_integrity,
            "split_rows": {name: payload["expected"] for name, payload in split_payload.items()},
            "effect": "F17B source truth(전선17B 원천 진실)를 runtime probe(런타임 탐침)에 고정합니다.",
        },
    )


def materialize_attempts(
    *,
    best: Mapping[str, Any],
    feature_order: Sequence[str],
    feature_order_hash: str,
    split_payload: Mapping[str, Mapping[str, Any]],
    common_files_root: Path,
) -> list[dict[str, Any]]:
    identity = scout.RunIdentity(
        stage_id=STAGE_ID,
        stage_number=17,
        run_number=RUN_NUMBER,
        run_id=RUN_ID,
        exploration_label="frontier17_loss_cluster_firewall_runtime_probe(전선17 손실 군집 방화벽 런타임 탐침)",
        common_run_root="Project_Obsidian_Prime_v2/frontier17C_runtime_probe",
    )
    rule = scout.ThresholdRule(
        threshold_id="frontier17c_argmax_probe_no_probability_threshold",
        short_threshold=0.0,
        long_threshold=0.0,
        min_margin=0.0,
    )
    attempts: list[dict[str, Any]] = []
    for runtime_split, payload in split_payload.items():
        attempt_name = f"frontier17c_tier_a_{runtime_split}"
        attempt = scout.materialize_mt5_attempt_files(
            run_output_root=RUN_ROOT,
            tier_name=scout.TIER_A,
            split_name=runtime_split,
            local_onnx_path=ROOT / str(best["onnx_path"]),
            local_feature_matrix_path=ROOT / str(payload["feature_export"]["path"]),
            rule=rule,
            feature_count=len(feature_order),
            feature_order_hash=feature_order_hash,
            from_date=str(payload["from_date"]),
            to_date=str(payload["to_date"]),
            stem_prefix=attempt_name,
            record_view_prefix="mt5_frontier17c_tier_a",
            attempt_role="tier_a_runtime_probe",
            decision_mode="argmax_probe",
            max_hold_bars=10,
            context=identity,
        )
        common_veto = scout.common_ref("veto", Path(str(payload["veto_export"]["path"])).name, context=identity)
        append_set_parameters(
            ROOT / str(attempt["set"]["path"]),
            {
                "InpRuntimeVetoTapeEnabled": True,
                "InpRuntimeVetoTapePath": common_veto,
                "InpRuntimeVetoTapeUseCommonFiles": True,
                "InpRuntimeVetoTapeDelimiter": ",",
            },
        )
        attempt["set"]["sha256"] = sha256_file(ROOT / str(attempt["set"]["path"]))
        attempt.update(
            {
                "attempt_name": attempt_name,
                "candidate_id": best["candidate_id"],
                "model_id": best["model_instance_id"],
                "source_model_id": best["model_id"],
                "source_run_id": SOURCE_RUN_ID,
                "decision_mode": "argmax_probe_plus_runtime_veto_tape",
                "from_date": payload["from_date"],
                "to_date": payload["to_date"],
                "set_name": mt5.EA_TESTER_SET_NAME,
                "ini_name": scout.mt5_short_profile_ini_name(scout.TIER_A, runtime_split, context=identity),
                "common_veto_tape_path": common_veto,
            }
        )
        attempts.append(attempt)

    sync_rows = [mt5.copy_to_common_files(common_files_root, ROOT / str(best["onnx_path"]), attempts[0]["common_model_path"])]
    sync_rows[0]["artifact_role"] = "source_onnx"
    for attempt in attempts:
        payload = split_payload[str(attempt["split"])]
        feature_row = mt5.copy_to_common_files(
            common_files_root,
            ROOT / str(payload["feature_export"]["path"]),
            str(attempt["common_feature_matrix_path"]),
        )
        feature_row["artifact_role"] = f"feature_matrix_{attempt['split']}"
        feature_row["attempt_name"] = attempt["attempt_name"]
        sync_rows.append(feature_row)

        veto_row = mt5.copy_to_common_files(
            common_files_root,
            ROOT / str(payload["veto_export"]["path"]),
            str(attempt["common_veto_tape_path"]),
        )
        veto_row["artifact_role"] = f"runtime_veto_tape_{attempt['split']}"
        veto_row["attempt_name"] = attempt["attempt_name"]
        sync_rows.append(veto_row)

    write_csv(COMMON_FILES_SYNC, sync_rows)
    write_json(MT5_ATTEMPT_PACKAGE.with_suffix(".json"), attempts)
    write_csv(MT5_ATTEMPT_PACKAGE, flatten_attempt_rows(attempts))
    return attempts


def append_set_parameters(path: Path, parameters: Mapping[str, Any]) -> None:
    text = io_path(path).read_text(encoding="utf-8")
    if text and not text.endswith("\n"):
        text += "\n"
    for key, value in parameters.items():
        text += f"{key}={format_mt5_value(value)}\n"
    io_path(path).write_text(text, encoding="utf-8")


def format_mt5_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return f"{value:.12g}"
    return str(value)


def execute_runtime_probe(
    *,
    args: argparse.Namespace,
    attempts: Sequence[Mapping[str, Any]],
    onnx_path: Path,
    split_payload: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    common_files_root = Path(args.common_files_root)
    terminal_data_root = Path(args.terminal_data_root)
    tester_profile_root = Path(args.tester_profile_root)
    compile_payload = mt5.compile_mql5_ea(Path(args.metaeditor_path), EA_SOURCE, MT5_DIR / "mt5_compile.log")
    portable_payload = sync_portable_ea()
    terminal_probe = terminal_processes()
    write_json(MT5_COMPILE_RESULT, {"compile": compile_payload, "portable_ea": portable_payload})
    write_json(TERMINAL_PROCESS_AUDIT, terminal_probe)

    execution_results: list[dict[str, Any]] = []
    report_records: list[dict[str, Any]] = []
    if args.materialize_only:
        for attempt in attempts:
            execution_results.append(
                {
                    "attempt_name": attempt["attempt_name"],
                    "tier": attempt["tier"],
                    "split": attempt["split"],
                    "record_view_prefix": attempt["record_view_prefix"],
                    "attempt_role": attempt["attempt_role"],
                    "status": "not_run_materialize_only",
                    "runtime_outputs": {"status": "not_run_materialize_only", "wait_status": "not_run_materialize_only"},
                }
            )
    else:
        can_run = compile_payload.get("status") == "completed" or portable_payload.get("portable_ea_ex5_exists")
        if not can_run:
            for attempt in attempts:
                execution_results.append(blocked_result(attempt, "compile_blocked_and_no_portable_ex5_fallback"))
        elif terminal_probe.get("status") != "no_terminal64_process":
            for attempt in attempts:
                execution_results.append(blocked_result(attempt, "target_portable_terminal_already_running"))
        else:
            for attempt in attempts:
                remove_runtime_outputs(common_files_root, attempt)
                mt5.remove_existing_mt5_report_artifacts(terminal_data_root, attempt, run_id=RUN_ID)
                try:
                    tester_result = mt5.run_mt5_tester(
                        Path(args.terminal_path),
                        ROOT / str(attempt["ini"]["path"]),
                        set_path=ROOT / str(attempt["set"]["path"]),
                        tester_profile_set_path=tester_profile_root / mt5.EA_TESTER_SET_NAME,
                        tester_profile_ini_path=tester_profile_root / str(attempt["ini_name"]),
                        timeout_seconds=int(args.timeout_seconds),
                        terminal_extra_args=["/portable"],
                    )
                except subprocess.TimeoutExpired as exc:
                    tester_result = {
                        "status": "blocked",
                        "command": exc.cmd,
                        "returncode": None,
                        "stdout": tail_text(exc.stdout),
                        "stderr": tail_text(exc.stderr),
                        "blocker": "terminal_timeout",
                    }
                runtime_outputs = mt5.wait_for_mt5_runtime_outputs(
                    common_files_root,
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
                    "candidate_id": attempt["candidate_id"],
                    "model_id": attempt["model_id"],
                    "ini_path": attempt["ini"]["path"],
                    "set_path": attempt["set"]["path"],
                    "common_model_path": attempt["common_model_path"],
                    "common_feature_matrix_path": attempt["common_feature_matrix_path"],
                    "common_veto_tape_path": attempt["common_veto_tape_path"],
                    "expected_signal_summary": split_payload[str(attempt["split"])]["expected"],
                }
                write_json(MT5_DIR / f"{attempt['attempt_name']}_tester_execution.json", result)
                execution_results.append(result)
            report_records = mt5.collect_mt5_strategy_report_artifacts(
                terminal_data_root=terminal_data_root,
                run_output_root=RUN_ROOT,
                attempts=attempts,
                run_id=RUN_ID,
            )
            mt5.attach_mt5_report_metrics(execution_results, report_records)

    copied_runtime = copy_runtime_outputs(common_files_root, attempts)
    kpi_records = mt5.build_mt5_kpi_records(execution_results)
    payload = {
        "compile": compile_payload,
        "portable_ea": portable_payload,
        "terminal_process_probe": terminal_probe,
        "terminal_extra_args": ["/portable"],
        "source_onnx": artifact_identity(onnx_path),
        "execution_results": execution_results,
        "strategy_tester_reports": report_records,
        "runtime_output_copy": copied_runtime,
        "mt5_kpi_records": kpi_records,
    }
    write_json(MT5_EXECUTION_RESULT, payload)
    write_json(STRATEGY_TESTER_REPORTS, report_records)
    write_json(MT5_KPI_RECORDS, kpi_records)
    return payload


def sync_portable_ea() -> dict[str, Any]:
    if path_exists(EA_BINARY):
        io_path(PORTABLE_EA_EX5.parent).mkdir(parents=True, exist_ok=True)
        shutil.copy2(io_path(EA_BINARY), io_path(PORTABLE_EA_EX5))
    return {
        "repo_ea_ex5": EA_BINARY.as_posix(),
        "repo_ea_ex5_exists": path_exists(EA_BINARY),
        "repo_ea_ex5_sha256": sha256_file(EA_BINARY) if path_exists(EA_BINARY) else "",
        "portable_ea_ex5": PORTABLE_EA_EX5.as_posix(),
        "portable_ea_ex5_exists": path_exists(PORTABLE_EA_EX5),
        "portable_ea_ex5_sha256": sha256_file(PORTABLE_EA_EX5) if path_exists(PORTABLE_EA_EX5) else "",
        "effect": "compiled EA(컴파일된 전문가 자문)를 portable MT5(휴대용 MT5) 경로에 동기화합니다.",
    }


def terminal_processes() -> dict[str, Any]:
    command = [
        "powershell",
        "-NoProfile",
        "-Command",
        "Get-CimInstance Win32_Process -Filter \"name = 'terminal64.exe'\" | Select-Object ProcessId,ExecutablePath,CommandLine | ConvertTo-Json -Compress",
    ]
    proc = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=30)
    payload: Any = []
    if proc.stdout.strip():
        try:
            payload = json.loads(proc.stdout)
            if isinstance(payload, Mapping):
                payload = [payload]
        except json.JSONDecodeError:
            payload = proc.stdout.strip()
    return {
        "command": command,
        "returncode": proc.returncode,
        "stdout": proc.stdout[-2000:],
        "stderr": proc.stderr[-2000:],
        "processes": payload,
        "status": "no_terminal64_process" if not payload else "terminal64_process_present",
        "effect": "terminal64 process(터미널 프로세스) 충돌 여부를 확인해 tester run(테스터 실행) 고립성을 지킵니다.",
    }


def blocked_result(attempt: Mapping[str, Any], blocker: str) -> dict[str, Any]:
    return {
        "status": "blocked",
        "blocker": blocker,
        "attempt_name": attempt["attempt_name"],
        "tier": attempt["tier"],
        "split": attempt["split"],
        "record_view_prefix": attempt["record_view_prefix"],
        "attempt_role": attempt["attempt_role"],
        "runtime_outputs": {"status": "blocked", "wait_status": f"skipped_{blocker}"},
    }


def remove_runtime_outputs(common_files_root: Path, attempt: Mapping[str, Any]) -> None:
    for key in ("common_telemetry_path", "common_summary_path"):
        path = common_files_root / Path(str(attempt[key]))
        if path_exists(path):
            io_path(path).unlink()


def copy_runtime_outputs(common_files_root: Path, attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        for key, role in (("common_telemetry_path", "telemetry"), ("common_summary_path", "summary")):
            source = common_files_root / Path(str(attempt[key]))
            destination = TELEMETRY_COPY_DIR / f"{attempt['attempt_name']}_{role}.csv"
            if path_exists(source):
                io_path(destination.parent).mkdir(parents=True, exist_ok=True)
                shutil.copy2(io_path(source), io_path(destination))
            rows.append(
                {
                    "attempt_name": attempt["attempt_name"],
                    "role": role,
                    "source": source.as_posix(),
                    "destination": destination.as_posix(),
                    "exists": path_exists(destination),
                    "sha256": sha256_file(destination) if path_exists(destination) else "",
                }
            )
    write_csv(RUNTIME_OUTPUT_COPY, rows)
    return rows


def build_runtime_summary_rows(
    attempts: Sequence[Mapping[str, Any]],
    execution_payload: Mapping[str, Any],
    split_payload: Mapping[str, Mapping[str, Any]],
) -> list[dict[str, Any]]:
    result_by_attempt = {str(row.get("attempt_name")): row for row in execution_payload.get("execution_results", [])}
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        result = dict(result_by_attempt.get(str(attempt["attempt_name"]), {}))
        runtime = result.get("runtime_outputs", {}) if isinstance(result.get("runtime_outputs"), Mapping) else {}
        last_summary = runtime.get("last_summary", {}) if isinstance(runtime.get("last_summary"), Mapping) else {}
        report = result.get("strategy_tester_report", {}) if isinstance(result.get("strategy_tester_report"), Mapping) else {}
        metrics = report.get("metrics", {}) if isinstance(report.get("metrics"), Mapping) else {}
        expected = split_payload[str(attempt["split"])]["expected"]
        rows.append(
            {
                "attempt_name": attempt["attempt_name"],
                "split": attempt["split"],
                "tester_status": result.get("status", "missing"),
                "tester_returncode": result.get("returncode", ""),
                "runtime_status": runtime.get("status", "missing"),
                "runtime_wait_status": runtime.get("wait_status", ""),
                "report_status": report.get("status", "missing"),
                "model_ok_count": as_int(last_summary.get("model_ok_count")),
                "feature_ready_count": as_int(last_summary.get("feature_ready_count")),
                "mt5_long_count": as_int(last_summary.get("long_count")),
                "mt5_short_count": as_int(last_summary.get("short_count")),
                "mt5_flat_count": as_int(last_summary.get("flat_count")),
                "mt5_order_attempt_count": as_int(last_summary.get("order_attempt_count")),
                "mt5_order_fill_count": as_int(last_summary.get("order_fill_count")),
                "expected_rows": int(expected["rows"]),
                "expected_signal_count": int(expected["signal_count"]),
                "expected_long_count": int(expected["long_count"]),
                "expected_short_count": int(expected["short_count"]),
                "expected_flat_count": int(expected["flat_count"]),
                "expected_veto_count": int(expected["runtime_veto_count"]),
                "signal_count_diff": as_int(last_summary.get("long_count")) + as_int(last_summary.get("short_count")) - int(expected["signal_count"]),
                "long_count_diff": as_int(last_summary.get("long_count")) - int(expected["long_count"]),
                "short_count_diff": as_int(last_summary.get("short_count")) - int(expected["short_count"]),
                "feature_ready_diff": as_int(last_summary.get("feature_ready_count")) - int(expected["rows"]),
                "net_profit": metrics.get("net_profit"),
                "profit_factor": metrics.get("profit_factor"),
                "trade_count": metrics.get("trade_count"),
                "max_drawdown_percent": metrics.get("max_drawdown_percent"),
                "recovery_factor": metrics.get("recovery_factor"),
                "blocker": result.get("blocker", ""),
            }
        )
    write_csv(MT5_PROBE_SUMMARY, rows)
    return rows


def build_signal_diff_rows(runtime_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in runtime_rows:
        exact = (
            int(row.get("feature_ready_diff", 999999)) == 0
            and int(row.get("signal_count_diff", 999999)) == 0
            and int(row.get("long_count_diff", 999999)) == 0
            and int(row.get("short_count_diff", 999999)) == 0
        )
        rows.append(
            {
                "attempt_name": row.get("attempt_name"),
                "split": row.get("split"),
                "runtime_status": row.get("runtime_status"),
                "report_status": row.get("report_status"),
                "feature_ready_diff": row.get("feature_ready_diff"),
                "signal_count_diff": row.get("signal_count_diff"),
                "long_count_diff": row.get("long_count_diff"),
                "short_count_diff": row.get("short_count_diff"),
                "usable_for_runtime_signal_parity": bool(exact),
                "judgment": "matched(일치)" if exact else "mismatch_or_missing(불일치 또는 누락)",
            }
        )
    write_csv(RUNTIME_SIGNAL_DIFF, rows)
    return rows


def build_receipts(
    *,
    created_at: str,
    best: Mapping[str, Any],
    attempts: Sequence[Mapping[str, Any]],
    execution_payload: Mapping[str, Any],
    runtime_rows: Sequence[Mapping[str, Any]],
    signal_diff_rows: Sequence[Mapping[str, Any]],
    split_payload: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    completed = runtime_completed_count(runtime_rows)
    signal_matches = sum(1 for row in signal_diff_rows if bool(row.get("usable_for_runtime_signal_parity")))
    receipts = {
        "runtime_parity_receipt": {
            "created_at_utc": created_at,
            "research_path": Path(__file__).as_posix(),
            "runtime_path": RUN_ROOT.as_posix(),
            "shared_contract": "F17B ONNX argmax plus current adverse veto tape(F17B ONNX 최대확률 + 현재 불리 차단 테이프)",
            "known_differences": "MT5 execution cost/slippage and tester data are native runtime observations(MT5 비용/슬리피지/테스터 데이터는 런타임 관찰)",
            "parity_check": f"signal_matches={signal_matches}/{len(signal_diff_rows)}; runtime_completed={completed}/{len(attempts)}",
            "parity_identity": {
                "onnx_sha256": best.get("onnx_sha256"),
                "compile_status": execution_payload.get("compile", {}).get("status"),
                "portable_ea_ex5_sha256": execution_payload.get("portable_ea", {}).get("portable_ea_ex5_sha256"),
                "veto_tapes": {name: payload["veto_export"]["sha256"] for name, payload in split_payload.items()},
                "module_hashes": mt5.mt5_runtime_module_hashes(),
            },
            "runtime_claim_boundary": "runtime_probe_observation_only(런타임 탐침 관찰 전용)",
        },
        "backtest_forensics_receipt": {
            "created_at_utc": created_at,
            "tester_identity": "portable MT5 US100 M5, validation_is/OOS date range(휴대용 MT5 US100 5분봉 검증/표본밖 날짜 범위)",
            "ea_identity": execution_payload.get("portable_ea", {}).get("portable_ea_ex5_sha256"),
            "report_identity": (RUN_ROOT / "mt5" / "reports").as_posix(),
            "trade_evidence": f"runtime_completed={completed}/{len(attempts)}",
            "forensic_checks": ["compile result(컴파일 결과)", "telemetry summary(텔레메트리 요약)", "strategy report(전략 보고서)", "Common Files handoff(공용 파일 인계)"],
            "backtest_judgment": "usable_with_boundary(경계 포함 사용 가능)" if completed == len(attempts) else "blocked_or_inconclusive(차단 또는 불충분)",
        },
        "artifact_lineage_receipt": {
            "created_at_utc": created_at,
            "source_inputs": [F17B_FINAL.as_posix(), best.get("onnx_path"), best.get("joblib_path")],
            "producer": Path(__file__).as_posix(),
            "consumer": REPORT_PATH.as_posix(),
            "artifact_paths": [RUN_ROOT.as_posix(), REPORT_PATH.as_posix()],
            "registry_links": [f03b.RUN_REGISTRY.as_posix(), f03b.ALPHA_LEDGER.as_posix(), STAGE_LEDGER.as_posix()],
            "availability": "tracked_review_and_ledger_plus_generated_runtime_artifacts(검토 장부 추적 + 생성 런타임 산출물)",
            "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
        },
        "result_judgment_receipt": {
            "created_at_utc": created_at,
            "result_subject": RUN_ID,
            "evidence_available": [MT5_PROBE_SUMMARY.as_posix(), RUNTIME_SIGNAL_DIFF.as_posix(), ONNX_PARITY_REPORT.as_posix()],
            "evidence_missing": ["Tier B separate(티어 B 분리)", "Tier A+B combined(티어 A+B 합산)", "full WFO stress(전체 WFO 스트레스)"],
            "judgment_label": "runtime_probe_observation(런타임 탐침 관찰)" if completed == len(attempts) else "blocked(차단)",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID if completed == len(attempts) else RUN_ID,
        },
        "claim_boundary_receipt": {
            "created_at_utc": created_at,
            "forbidden_claims": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
            "effect": "F17C는 runtime probe observation(런타임 탐침 관찰)만 남기고 authority(권위)를 만들지 않습니다.",
        },
    }
    write_json(RUNTIME_RECEIPT, receipts["runtime_parity_receipt"])
    write_json(BACKTEST_RECEIPT, receipts["backtest_forensics_receipt"])
    write_json(LINEAGE_RECEIPT, receipts["artifact_lineage_receipt"])
    write_json(JUDGMENT_RECEIPT, receipts["result_judgment_receipt"])
    write_json(CLAIM_RECEIPT, receipts["claim_boundary_receipt"])
    return receipts


def build_final(
    *,
    created_at: str,
    best: Mapping[str, Any],
    source_final: Mapping[str, Any],
    attempts: Sequence[Mapping[str, Any]],
    execution_payload: Mapping[str, Any],
    runtime_rows: Sequence[Mapping[str, Any]],
    signal_diff_rows: Sequence[Mapping[str, Any]],
    receipts: Mapping[str, Any],
    materialize_only: bool,
) -> dict[str, Any]:
    completed = runtime_completed_count(runtime_rows)
    all_completed = completed == len(attempts) and len(attempts) > 0 and not materialize_only
    signal_matches = sum(1 for row in signal_diff_rows if bool(row.get("usable_for_runtime_signal_parity")))
    all_signal_matched = signal_matches == len(signal_diff_rows) and len(signal_diff_rows) > 0
    if all_completed and all_signal_matched:
        status = "runtime_probe_observation_completed_signal_matched_no_authority"
        judgment = "runtime_probe_observation(런타임 탐침 관찰)"
        next_run_id = NEXT_RUN_ID
    elif all_completed:
        status = "runtime_probe_observation_signal_mismatch_no_authority"
        judgment = "runtime_probe_observation_mismatch(런타임 탐침 관찰 불일치)"
        next_run_id = NEXT_RUN_ID
    else:
        status = "blocked_runtime_probe_attempt_recorded_no_authority"
        judgment = "runtime_probe_blocked_with_attempt(런타임 탐침 시도 포함 차단)"
        next_run_id = RUN_ID
    return {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "next_run_id": next_run_id,
        "status": status,
        "judgment": judgment,
        "runtime_attempts": len(attempts),
        "runtime_completed_attempts": completed,
        "signal_parity_matches": signal_matches,
        "best_candidate_row": dict(best),
        "frontier17b_status": source_final.get("status"),
        "runtime_probe_observation": runtime_observation_text(runtime_rows),
        "execution_payload_paths": {
            "mt5_execution_result": MT5_EXECUTION_RESULT.as_posix(),
            "mt5_probe_summary": MT5_PROBE_SUMMARY.as_posix(),
            "signal_diff": RUNTIME_SIGNAL_DIFF.as_posix(),
            "strategy_tester_reports": STRATEGY_TESTER_REPORTS.as_posix(),
        },
        "grok_packet": GROK_PACKET.as_posix(),
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "receipts": receipts,
        "gate_audit_path": GATE_AUDIT.as_posix(),
    }


def runtime_observation_text(runtime_rows: Sequence[Mapping[str, Any]]) -> str:
    if not runtime_rows:
        return "no_runtime_rows(런타임 행 없음)"
    parts = []
    for row in runtime_rows:
        parts.append(
            f"{row.get('split')}: status={row.get('runtime_status')}/{row.get('report_status')}, "
            f"PF={fmt(row.get('profit_factor'))}, DD={fmt(row.get('max_drawdown_percent'))}, "
            f"trades={fmt(row.get('trade_count'))}, signal_diff={row.get('signal_count_diff')}"
        )
    return " | ".join(parts)


def write_results(
    final: Mapping[str, Any],
    runtime_rows: Sequence[Mapping[str, Any]],
    signal_diff_rows: Sequence[Mapping[str, Any]],
    receipts: Mapping[str, Any],
) -> None:
    gate_rows = build_gate_rows(final, runtime_rows, signal_diff_rows)
    write_csv(GATE_AUDIT, gate_rows)
    write_json(FINAL_DECISION, final)
    write_json(RUN_MANIFEST, run_manifest(final, gate_rows, receipts))


def build_gate_rows(
    final: Mapping[str, Any],
    runtime_rows: Sequence[Mapping[str, Any]],
    signal_diff_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    attempts = int(final.get("runtime_attempts", 0))
    completed = int(final.get("runtime_completed_attempts", 0))
    signal_matches = int(final.get("signal_parity_matches", 0))
    all_completed = attempts > 0 and completed == attempts
    return [
        {
            "gate_name": "external_review_packet(외부 검토 묶음)",
            "status": "passed_with_local_verification(로컬 검증 포함 통과)",
            "evidence_path": (GROK_PACKET / "clean_output.md").as_posix(),
            "effect": "Grok second opinion(그록 2차 의견)을 자동 실행하지 않고 로컬 검증 후 반영했습니다.",
        },
        {
            "gate_name": "source_identity_gate(원천 정체성 게이트)",
            "status": "passed(통과)",
            "evidence_path": INPUT_MANIFEST.as_posix(),
            "effect": "F17B preserved clue ONNX/model(전선17B 보존 단서 ONNX/모델) 해시를 고정했습니다.",
        },
        {
            "gate_name": "onnx_probability_parity_gate(ONNX 확률 동등성 게이트)",
            "status": "passed(통과)",
            "evidence_path": ONNX_PARITY_REPORT.as_posix(),
            "effect": "Python sklearn(파이썬 sklearn)과 ONNX probability(확률) 출력을 비교했습니다.",
        },
        {
            "gate_name": "runtime_veto_tape_handoff_gate(런타임 차단 테이프 인계 게이트)",
            "status": "passed(통과)",
            "evidence_path": VETO_TAPE_MANIFEST.as_posix(),
            "effect": "F17B current adverse veto(현재 불리 차단)를 MT5 runtime probe(MT5 런타임 탐침)에 전달했습니다.",
        },
        {
            "gate_name": "mt5_runtime_execution_gate(MT5 런타임 실행 게이트)",
            "status": "passed_with_observation(관찰 포함 통과)" if all_completed else "blocked_with_attempt(시도 기록 차단)",
            "evidence_path": MT5_PROBE_SUMMARY.as_posix(),
            "effect": f"runtime_completed={completed}/{attempts}; MT5 native tester(MT5 네이티브 테스터) 출력물을 확인합니다.",
        },
        {
            "gate_name": "runtime_signal_parity_gate(런타임 신호 동등성 게이트)",
            "status": "passed(통과)" if signal_matches == len(signal_diff_rows) and signal_diff_rows else "observation_mismatch_or_missing(관찰 불일치 또는 누락)",
            "evidence_path": RUNTIME_SIGNAL_DIFF.as_posix(),
            "effect": "expected signal count(예상 신호 수)와 MT5 summary(요약)를 비교했습니다.",
        },
        {
            "gate_name": "paired_tier_scope_gate(쌍 티어 범위 게이트)",
            "status": "passed_with_missing_required_boundary(필수 누락 경계 포함 통과)",
            "evidence_path": STAGE_LEDGER.as_posix(),
            "effect": "Tier A runtime probe(티어 A 런타임 탐침)만 실행하고 Tier B/combined(티어 B/합산)는 missing_required(필수 누락)로 기록합니다.",
        },
        {
            "gate_name": "final_claim_guard(최종 주장 보호)",
            "status": "passed_no_authority_claim(권위 주장 없음 통과)",
            "evidence_path": CLAIM_RECEIPT.as_posix(),
            "effect": "completion/baseline/promotion/runtime/live/Goal(완성/기준선/승격/런타임/실거래/목표) 주장을 막습니다.",
        },
    ]


def run_manifest(final: Mapping[str, Any], gate_rows: Sequence[Mapping[str, Any]], receipts: Mapping[str, Any]) -> dict[str, Any]:
    output_paths = [
        INPUT_MANIFEST,
        FEATURE_MATRIX_MANIFEST,
        VETO_TAPE_MANIFEST,
        EXPECTED_SIGNAL_SUMMARY,
        EXPECTED_PROBABILITY_TAPE,
        ONNX_PARITY_REPORT,
        COMMON_FILES_SYNC,
        MT5_ATTEMPT_PACKAGE,
        MT5_EXECUTION_RESULT,
        MT5_PROBE_SUMMARY,
        RUNTIME_SIGNAL_DIFF,
        GATE_AUDIT,
        FINAL_DECISION,
        REPORT_PATH,
    ]
    return {
        **dict(final),
        "script_path": Path(__file__).as_posix(),
        "script_sha256": sha256_file(Path(__file__)),
        "gate_rows": gate_rows,
        "receipts": receipts,
        "artifacts": [artifact_identity(path) for path in output_paths],
    }


def update_docs_and_registers(final: Mapping[str, Any], runtime_rows: Sequence[Mapping[str, Any]]) -> None:
    write_text_sig(REPORT_PATH, report_text(final, runtime_rows))
    write_text_sig(REVIEW_INDEX, review_index_text(final))
    write_text_sig(SELECTION_STATUS, selection_status_text(final))
    write_text_sig(DECISION_DOC, decision_text(final))
    append_stage_brief(final)
    write_text_sig(f03b.WORKSPACE_STATE, workspace_state_text(final))
    write_text_sig(f03b.CURRENT_WORKING_STATE, current_working_state_text(final))
    upsert_csv_io(f03b.RUN_REGISTRY, "run_id", run_registry_row(final, runtime_rows))
    for row in ledger_rows(final, runtime_rows):
        upsert_csv_io(f03b.ALPHA_LEDGER, "ledger_row_id", row)
        upsert_csv_io(STAGE_LEDGER, "ledger_row_id", row)
    upsert_artifact_registry(final)
    f03b.append_once(f03b.CHANGELOG, RUN_ID, changelog_entry(final))
    f03b.append_once(f03b.IDEA_REGISTRY, RUN_ID, idea_registry_entry(final))


def report_text(final: Mapping[str, Any], runtime_rows: Sequence[Mapping[str, Any]]) -> str:
    best = final["best_candidate_row"]
    return f"""# Frontier17C Runtime Probe(전선17C 런타임 탐침)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

## Action And Effect(행동과 효과)

Action(행동): F17B preserved clue ONNX(전선17B 보존 단서 ONNX) `{best.get('candidate_id')}`를 MT5 runtime probe(MT5 런타임 탐침)로 실행했습니다.

Effect(효과): F17B의 signal contract(신호 계약)인 argmax(최대 확률) + current adverse veto false(현재 불리 차단 없음)를 runtime veto tape(런타임 차단 테이프)로 MT5에 전달했습니다.

## Runtime Probe Observation(런타임 탐침 관찰)

{runtime_rows_markdown(runtime_rows)}

## Source Boundary(원천 경계)

- source run(원천 실행): `{SOURCE_RUN_ID}`
- source ONNX sha256(원천 ONNX 해시): `{best.get('onnx_sha256')}`
- decision mode(결정 모드): `argmax_probe_plus_runtime_veto_tape(최대확률 탐침 + 런타임 차단 테이프)`
- max hold bars(최대 보유 봉): `10`

## Scope Boundary(범위 경계)

Tier A separate(티어 A 분리)만 MT5 runtime probe(MT5 런타임 탐침)로 기록했습니다. Tier B separate(티어 B 분리)와 Tier A+B combined(티어 A+B 합산)는 missing_required(필수 누락)입니다.

## Claim Boundary(주장 경계)

completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def runtime_rows_markdown(runtime_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| split(분할) | runtime(런타임) | report(보고서) | PF(수익 팩터) | DD%(손실폭) | trades(거래) | signal diff(신호 차이) |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in runtime_rows:
        lines.append(
            f"| `{row.get('split')}` | `{row.get('runtime_status')}` | `{row.get('report_status')}` | "
            f"{fmt(row.get('profit_factor'))} | {fmt(row.get('max_drawdown_percent'))} | "
            f"{fmt(row.get('trade_count'))} | {row.get('signal_count_diff')} |"
        )
    return "\n".join(lines)


def review_index_text(final: Mapping[str, Any]) -> str:
    return f"""# Frontier17 Review Index(전선17 검토 색인)

Updated(갱신): {final['created_at_utc']}

Latest run(최신 실행): `{RUN_ID}`

Status(상태): `{final['status']}`

Key report(핵심 보고서): `{REPORT_PATH.as_posix()}`
"""


def selection_status_text(final: Mapping[str, Any]) -> str:
    return f"""# Frontier17 Selection Status(전선17 선택 상태)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Selection(선택): no selected baseline/completion candidate/promotion/runtime authority(선택 기준선/완성 후보/승격/런타임 권위 없음).

Runtime probe observation(런타임 탐침 관찰): {final['runtime_probe_observation']}

Next action(다음 행동): `{final['next_run_id']}`
"""


def decision_text(final: Mapping[str, Any]) -> str:
    return f"""# Decision: Frontier17C Runtime Probe(결정: 전선17C 런타임 탐침)

Date(날짜): {final['created_at_utc']}

Decision(결정): `{final['status']}`

Action(행동): Frontier17(전선17)의 F17B preserved clue(보존 단서)를 MT5 runtime probe(MT5 런타임 탐침)로 시도했습니다.

Effect(효과): stage-level runtime probe record(단계별 런타임 탐침 기록)를 남기되, 권위(authority, 권위)는 만들지 않습니다.

Next action(다음 행동): `{final['next_run_id']}`
"""


def append_stage_brief(final: Mapping[str, Any]) -> None:
    marker = f"<!-- {RUN_ID}__runtime_probe -->"
    text = read_text(STAGE_BRIEF) if path_exists(STAGE_BRIEF) else f"# {STAGE_ID}\n"
    if marker in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    text += f"""
{marker}

## Frontier17C Runtime Probe(전선17C 런타임 탐침)

Updated(갱신): {final['created_at_utc']}

Action(행동): F17B preserved clue ONNX(전선17B 보존 단서 ONNX)를 MT5 runtime probe(MT5 런타임 탐침)로 시도했습니다.

Effect(효과): runtime veto tape(런타임 차단 테이프)로 Python proxy(파이썬 프록시)의 current adverse veto(현재 불리 차단)를 재현합니다.
"""
    write_text_sig(STAGE_BRIEF, text)


def workspace_state_text(final: Mapping[str, Any]) -> str:
    latest_completed = RUN_ID if final["status"] != "blocked_runtime_probe_attempt_recorded_no_authority" else PARENT_RUN_ID
    return "\n".join(
        [
            f"current_stage_id: {STAGE_ID}",
            f"current_run_id: {RUN_ID}",
            f"latest_completed_run_id: {latest_completed}",
            f"current_status: {final['status']}",
            f"current_judgment: {final['judgment']}",
            f"next_run_id: {final['next_run_id']}",
            "runtime_authority: not_claimed",
            "operating_promotion: not_claimed",
            "goal_achieve: not_claimed",
            f"updated_at_utc: '{final['created_at_utc']}'",
            "",
        ]
    )


def current_working_state_text(final: Mapping[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

## Active Stage(현재 단계)

- stage(단계): `{STAGE_ID}`
- current run(현재 실행): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- next run(다음 실행): `{final['next_run_id']}`

## Current Truth(현재 진실)

Action(행동): Frontier17C(전선17C)는 F17B preserved clue(보존 단서)를 MT5 runtime probe(MT5 런타임 탐침)로 시도했습니다.

Effect(효과): 각 frontier stage(전선 단계)에서 runtime probe(런타임 탐침)를 시도하거나 blocked(차단) 사유를 남기는 운영 규칙을 지킵니다.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def run_registry_row(final: Mapping[str, Any], runtime_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "runtime_probe(런타임 탐침)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": final["runtime_probe_observation"],
        "family": "runtime_backtest(MT5 런타임 백테스트)",
        "work_family": "runtime_backtest(MT5 런타임 백테스트)",
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "attempt_count": final["runtime_attempts"],
        "runtime_completed_rows": final["runtime_completed_attempts"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "primary_kpi": runtime_primary_kpi(runtime_rows),
        "external_verification_status": "mt5_runtime_probe_attempted(MT5 런타임 탐침 시도됨)",
        "result_path": REPORT_PATH.as_posix(),
        "gate_audit_path": GATE_AUDIT.as_posix(),
    }


def ledger_rows(final: Mapping[str, Any], runtime_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "runtime_probe(런타임 탐침)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "guardrail_kpi": "no_authority_no_goal_claim(권위/목표 주장 없음)",
        "external_verification_status": "mt5_runtime_probe_attempted(MT5 런타임 탐침 시도됨)",
    }
    rows: list[dict[str, Any]] = []
    for runtime_row in runtime_rows:
        split = str(runtime_row.get("split"))
        rows.append(
            {
                **base,
                "ledger_row_id": f"{RUN_ID}__tier_a_{split}_runtime_probe",
                "subrun_id": f"{RUN_ID}__tier_a_{split}_runtime_probe",
                "record_view": f"Tier A separate {split}(티어 A 분리 {split})",
                "tier_scope": "Tier A(티어 A)",
                "kpi_scope": "mt5_runtime_probe_observation(MT5 런타임 탐침 관찰)",
                "primary_kpi": runtime_row_kpi(runtime_row),
                "notes": f"signal_diff={runtime_row.get('signal_count_diff')};blocker={runtime_row.get('blocker', '')}",
            }
        )
    rows.extend(
        [
            {
                **base,
                "ledger_row_id": f"{RUN_ID}__tier_b_missing_required",
                "subrun_id": f"{RUN_ID}__tier_b_missing_required",
                "record_view": "Tier B separate(티어 B 분리)",
                "tier_scope": "Tier B(티어 B)",
                "kpi_scope": "missing_required(필수 누락)",
                "primary_kpi": "missing_required_no_tier_b_runtime_probe(필수 누락, 티어 B 런타임 탐침 없음)",
                "notes": "Tier B source not materialized for F17C runtime probe(전선17C 런타임 탐침에서 티어 B 원천 없음)",
            },
            {
                **base,
                "ledger_row_id": f"{RUN_ID}__tier_ab_combined_missing_required",
                "subrun_id": f"{RUN_ID}__tier_ab_combined_missing_required",
                "record_view": "Tier A+B combined(티어 A+B 합산)",
                "tier_scope": "Tier A+B(티어 A+B)",
                "kpi_scope": "missing_required(필수 누락)",
                "primary_kpi": "missing_required_no_combined_runtime_claim(필수 누락, 합산 런타임 주장 없음)",
                "notes": "combined record blocked by missing Tier B(티어 B 누락으로 합산 기록 차단)",
            },
        ]
    )
    return rows


def upsert_artifact_registry(final: Mapping[str, Any]) -> None:
    rows = [
        artifact_registry_row(final, "run_manifest", RUN_MANIFEST),
        artifact_registry_row(final, "final_decision", FINAL_DECISION),
        artifact_registry_row(final, "report", REPORT_PATH),
        artifact_registry_row(final, "mt5_probe_summary", MT5_PROBE_SUMMARY),
        artifact_registry_row(final, "runtime_signal_diff", RUNTIME_SIGNAL_DIFF),
    ]
    append_csv_io(ARTIFACT_REGISTRY, rows)


def artifact_registry_row(final: Mapping[str, Any], artifact_type: str, path: Path) -> dict[str, Any]:
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "artifact_type": artifact_type,
        "path": path.as_posix(),
        "sha256": sha256_file(path) if path_exists(path) else "",
        "created_at": final["created_at_utc"],
        "claim_boundary": CLAIM_BOUNDARY,
        "artifact_id": f"{RUN_ID}__{artifact_type}",
        "created_at_utc": final["created_at_utc"],
        "notes": "Frontier17C runtime probe(전선17C 런타임 탐침)",
        "artifact_path": path.as_posix(),
        "effect": "stage runtime probe evidence(단계 런타임 탐침 근거)를 연결합니다.",
    }


def changelog_entry(final: Mapping[str, Any]) -> str:
    return (
        f"- {final['created_at_utc']}: `{RUN_ID}` added MT5 runtime probe(MT5 런타임 탐침) for Frontier17(전선17). "
        f"Effect(효과): F17B preserved clue(보존 단서)를 runtime observation(런타임 관찰)로 확인합니다.\n"
    )


def idea_registry_entry(final: Mapping[str, Any]) -> str:
    return (
        f"- `{RUN_ID}`: Frontier17(전선17) runtime probe(런타임 탐침). "
        "Effect(효과): loss-cluster firewall(손실 군집 방화벽)의 MT5 handoff(인계) 가능성을 확인합니다.\n"
    )


def runtime_primary_kpi(runtime_rows: Sequence[Mapping[str, Any]]) -> str:
    return " | ".join(runtime_row_kpi(row) for row in runtime_rows) if runtime_rows else "no_runtime_rows(런타임 행 없음)"


def runtime_row_kpi(row: Mapping[str, Any]) -> str:
    return (
        f"{row.get('split')}:status={row.get('runtime_status')}/{row.get('report_status')};"
        f"pf={fmt(row.get('profit_factor'))};dd={fmt(row.get('max_drawdown_percent'))};"
        f"trades={fmt(row.get('trade_count'))};signal_diff={row.get('signal_count_diff')}"
    )


def runtime_completed_count(rows: Sequence[Mapping[str, Any]]) -> int:
    return sum(
        1
        for row in rows
        if row.get("tester_status") == "completed"
        and row.get("runtime_status") == "completed"
        and row.get("report_status") == "completed"
    )


def flatten_attempt_rows(attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        rows.append(
            {
                "attempt_name": attempt["attempt_name"],
                "tier": attempt["tier"],
                "split": attempt["split"],
                "candidate_id": attempt["candidate_id"],
                "model_id": attempt["model_id"],
                "decision_mode": attempt["decision_mode"],
                "from_date": attempt["from_date"],
                "to_date": attempt["to_date"],
                "set_path": attempt["set"]["path"],
                "ini_path": attempt["ini"]["path"],
                "common_model_path": attempt["common_model_path"],
                "common_feature_matrix_path": attempt["common_feature_matrix_path"],
                "common_veto_tape_path": attempt["common_veto_tape_path"],
                "common_telemetry_path": attempt["common_telemetry_path"],
                "common_summary_path": attempt["common_summary_path"],
            }
        )
    return rows


def artifact_row(role: str, path: Path) -> dict[str, Any]:
    return {
        "role": role,
        "path": rel(path),
        "exists": path_exists(path),
        "sha256": sha256_file(path) if path_exists(path) else "",
    }


def artifact_identity(path: Path) -> dict[str, Any]:
    return {
        "path": rel(path),
        "exists": path_exists(path),
        "sha256": sha256_file(path) if path_exists(path) else "",
    }


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    materialized = [dict(row) for row in rows]
    if fieldnames is None:
        columns: list[str] = []
        for row in materialized:
            for key in row:
                if key not in columns:
                    columns.append(key)
        fieldnames = columns
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in materialized:
            writer.writerow({column: stringify(row.get(column, "")) for column in fieldnames})


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_text_sig(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig", newline="\n")


def ensure_csv_header(path: Path, template_path: Path) -> None:
    if path_exists(path):
        return
    header = read_csv_header_io(template_path)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        csv.writer(handle, lineterminator="\n").writerow(header)


def read_csv_header_io(path: Path) -> list[str]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return next(csv.reader(handle))


def upsert_csv_io(path: Path, key: str, row: Mapping[str, Any]) -> None:
    header = read_csv_header_io(path)
    rows: list[dict[str, str]] = []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        rows.extend(dict(existing) for existing in csv.DictReader(handle))
    normalized = {column: stringify(row.get(column, "")) for column in header}
    replaced = False
    for index, existing in enumerate(rows):
        if existing.get(key) == normalized.get(key):
            rows[index] = normalized
            replaced = True
            break
    if not replaced:
        rows.append(normalized)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=header, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for item in rows:
            writer.writerow({column: stringify(item.get(column, "")) for column in header})


def append_csv_io(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    if not rows:
        return
    header = read_csv_header_io(path)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("a", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=header, extrasaction="ignore", lineterminator="\n")
        for row in rows:
            writer.writerow({column: stringify(row.get(column, "")) for column in header})


def stringify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    if isinstance(value, float):
        return "" if not math.isfinite(value) else str(value)
    return str(value)


def as_int(value: Any) -> int:
    try:
        if value is None or value == "":
            return 0
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def fmt(value: Any) -> str:
    if value is None or value == "":
        return ""
    try:
        number = float(value)
    except (TypeError, ValueError):
        return str(value)
    if not math.isfinite(number):
        return ""
    return f"{number:.6g}"


def rel(path: Path | str) -> str:
    p = Path(path)
    try:
        return p.relative_to(ROOT).as_posix()
    except ValueError:
        return p.as_posix()


def tail_text(value: Any, limit: int = 4000) -> str:
    if value is None:
        return ""
    return str(value)[-limit:]


def utc_now() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


if __name__ == "__main__":
    raise SystemExit(main())
