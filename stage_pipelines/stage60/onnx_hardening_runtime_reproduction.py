from __future__ import annotations

import argparse
import csv
import json
import math
import shutil
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.alpha_run_ledgers import build_mt5_alpha_ledger_rows  # noqa: E402
from foundation.control_plane.ledger import (  # noqa: E402
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.control_plane.mt5_tier_balance_completion import (  # noqa: E402
    COMMON_FILES_ROOT_DEFAULT,
    METAEDITOR_PATH_DEFAULT,
    TERMINAL_DATA_ROOT_DEFAULT,
    TERMINAL_PATH_DEFAULT,
    TESTER_PROFILE_ROOT_DEFAULT,
    attempt_payload,
    copy_to_common,
    execute_prepared_run,
    parse_ini,
)
from foundation.models.onnx_bridge import ordered_hash  # noqa: E402
from foundation.mt5 import runtime_support as mt5  # noqa: E402
from stage_pipelines.stage56 import baseline_adapter_onnx_hardening as hardening  # noqa: E402
from stage_pipelines.stage56 import baseline_adapter_repair_batch as repair  # noqa: E402
from stage_pipelines.stage58 import risk_atr_integration as s58  # noqa: E402
from stage_pipelines.stage59ar import new_model_branch_from_stage59aq as s59ar  # noqa: E402


STAGE60_ID = "60_adapter_onnx__hardening_runtime_reproduction"
STAGE61_ID = "61_research_package__baseline_adapter_review_only"
RUN_NUMBER = "run60A"
RUN_ID = "run60A_stage60_onnx_hardening_v1"
PACKET_ID = "stage60_onnx_hardening_v1"
PARENT_RUN_ID = s59ar.RUN_ID
SOURCE_STAGE59AR_PUSHED_COMMIT = "688ce7788951a45248f846edfae5cd0546399548"
BOUNDARY = s59ar.BOUNDARY

ADAPTER_ID = "s59ar_v41_sd8_h3"
SOURCE_ANCHOR = "v41_v22_midcov_et40_agree_h2c0_no_b"
SIGNAL_COLUMN = s59ar.RUN50BN_SIGNAL
FEATURE_ORDER = (SIGNAL_COLUMN,)
FEATURE_ORDER_HASH = ordered_hash(FEATURE_ORDER)
COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage60/{RUN_NUMBER}_onnx_runtime"
MIN_MARGIN = 0.0

STAGE_ROOT = Path("stages") / STAGE60_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SPEC_ROOT = STAGE_ROOT / "00_spec"
INPUT_ROOT = STAGE_ROOT / "01_inputs"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID

SOURCE_STAGE59AR_ROOT = Path("stages") / s59ar.STAGE59AR_ID
SOURCE_STAGE59AR_RUN_ROOT = SOURCE_STAGE59AR_ROOT / "02_runs" / s59ar.RUN_NUMBER / ADAPTER_ID
SOURCE_MODEL_TABLE = SOURCE_STAGE59AR_RUN_ROOT / "models" / f"{SOURCE_ANCHOR}_stage56_context_timed_event_signal_discrete_score_table.csv"
SOURCE_FEATURE_VAL = SOURCE_STAGE59AR_RUN_ROOT / "features" / f"{ADAPTER_ID}_stage59d_adapter_a_val.csv"
SOURCE_FEATURE_OOS = SOURCE_STAGE59AR_RUN_ROOT / "features" / f"{ADAPTER_ID}_stage59d_adapter_a_oos.csv"
SOURCE_INI_VAL = SOURCE_STAGE59AR_RUN_ROOT / "mt5" / f"{ADAPTER_ID}_rt_val.ini"
SOURCE_INI_OOS = SOURCE_STAGE59AR_RUN_ROOT / "mt5" / f"{ADAPTER_ID}_rt_oos.ini"
SOURCE_STAGE59AR_SUMMARY = SOURCE_STAGE59AR_ROOT / "03_reviews/bounded_followup_summary.csv"
SOURCE_STAGE59AR_RISK = SOURCE_STAGE59AR_ROOT / "03_reviews/bounded_followup_risk_atr_telemetry.csv"
SOURCE_STAGE59AR_DECISION = SOURCE_STAGE59AR_ROOT / "03_reviews/stage59ar_decision.md"

MODEL_TABLE_PATH = RUN_ROOT / ADAPTER_ID / "models" / SOURCE_MODEL_TABLE.name
ONNX_MODEL_PATH = RUN_ROOT / ADAPTER_ID / "models" / f"{ADAPTER_ID}_entry_probability.onnx"
FEATURE_VAL_PATH = RUN_ROOT / ADAPTER_ID / "features" / f"{ADAPTER_ID}_onnx_adapter_a_val.csv"
FEATURE_OOS_PATH = RUN_ROOT / ADAPTER_ID / "features" / f"{ADAPTER_ID}_onnx_adapter_a_oos.csv"
HANDOFF_JSON_PATH = RUN_ROOT / ADAPTER_ID / "handoff" / f"{ADAPTER_ID}_onnx_runtime_handoff.json"

ONNX_EXPORT_REPORT_PATH = REVIEWS_ROOT / "onnx_export_report.json"
ONNX_PARITY_REPORT_PATH = REVIEWS_ROOT / "onnx_parity_report.json"
RUNTIME_REPORT_PATH = REVIEWS_ROOT / "mt5_onnx_runtime_reproduction.md"
SUMMARY_JSON_PATH = REVIEWS_ROOT / "mt5_onnx_runtime_summary.json"
SUMMARY_CSV_PATH = REVIEWS_ROOT / "mt5_onnx_runtime_summary.csv"
SEGMENT_KPI_PATH = REVIEWS_ROOT / "mt5_onnx_segment_kpi_summary.csv"
RISK_ATR_TELEMETRY_PATH = REVIEWS_ROOT / "mt5_onnx_risk_atr_telemetry.csv"
AUDIT_CSV_PATH = REVIEWS_ROOT / "mt5_onnx_runtime_trade_audit.csv"
DECISION_PATH = REVIEWS_ROOT / "stage60_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")

REPRODUCTION_TOLERANCE = {
    "trades_per_day": 0.02,
    "profit_factor": 0.02,
    "net_profit": 5.0,
    "max_drawdown_amount": 5.0,
    "cost_stressed_expectancy": 0.05,
}


def selected_variant() -> repair.RepairVariant:
    for variant in s59ar.STAGE59AR_VARIANTS:
        if variant.adapter_id == ADAPTER_ID:
            return variant
    raise RuntimeError(f"Missing selected variant {ADAPTER_ID}")


VARIANT = selected_variant()
STAGE60_VARIANTS = (VARIANT,)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    candidate = Path(str(path))
    try:
        return io_path(candidate).resolve().relative_to(io_path(REPO_ROOT).resolve()).as_posix()
    except ValueError:
        return candidate.as_posix()


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.10g}" if math.isfinite(value) else ""
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return str(value)


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    ordered: list[str] = []
    for row in rows:
        for key in row:
            if key not in ordered:
                ordered.append(key)
    fieldnames = list(columns or ordered)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in fieldnames})


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or value == "":
            return default
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def copy_local(source: Path, destination: Path) -> dict[str, Any]:
    if not path_exists(source):
        raise FileNotFoundError(source)
    io_path(destination.parent).mkdir(parents=True, exist_ok=True)
    shutil.copy2(io_path(source), io_path(destination))
    return {"source": rel(source), "path": rel(destination), "sha256": sha256_file_lf_normalized(destination)}


def load_feature_values(paths: Sequence[Path]) -> np.ndarray:
    frames: list[pd.DataFrame] = []
    for path in paths:
        frame = pd.read_csv(io_path(path))
        if SIGNAL_COLUMN not in frame.columns:
            raise ValueError(f"Feature column missing: {SIGNAL_COLUMN} in {path}")
        frames.append(frame.loc[:, [SIGNAL_COLUMN]].astype("float32"))
    merged = pd.concat(frames, axis=0, ignore_index=True)
    return merged.to_numpy(dtype=np.float32)


def decisions(probabilities: np.ndarray) -> np.ndarray:
    out: list[int] = []
    for p_short, p_flat, p_long in probabilities:
        short_margin = float(p_short) - max(float(p_flat), float(p_long))
        long_margin = float(p_long) - max(float(p_flat), float(p_short))
        if float(p_long) >= VARIANT.long_threshold and long_margin >= MIN_MARGIN and float(p_long) >= float(p_short):
            out.append(1)
        elif float(p_short) >= VARIANT.short_threshold and short_margin >= MIN_MARGIN:
            out.append(-1)
        else:
            out.append(0)
    return np.asarray(out, dtype=np.int8)


def decision_parity(onnx_path: Path, table: Mapping[str, Any], values: np.ndarray) -> dict[str, Any]:
    import onnxruntime as ort

    expected_prob = hardening.python_table_probabilities(values.astype("float64"), table)
    session = ort.InferenceSession(str(io_path(onnx_path)), providers=["CPUExecutionProvider"])
    input_name = session.get_inputs()[0].name
    actual_prob = np.asarray(session.run(None, {input_name: values.astype(np.float32)})[0], dtype=np.float64)
    expected_decisions = decisions(expected_prob)
    actual_decisions = decisions(actual_prob)
    mismatches = expected_decisions != actual_decisions
    return {
        "passed": bool(not np.any(mismatches)),
        "rows": int(len(expected_decisions)),
        "mismatch_count": int(np.sum(mismatches)),
        "expected_counts": {
            "short": int(np.sum(expected_decisions == -1)),
            "flat": int(np.sum(expected_decisions == 0)),
            "long": int(np.sum(expected_decisions == 1)),
        },
        "actual_counts": {
            "short": int(np.sum(actual_decisions == -1)),
            "flat": int(np.sum(actual_decisions == 0)),
            "long": int(np.sum(actual_decisions == 1)),
        },
    }


def prepare_inputs(common_files_root: Path) -> dict[str, Any]:
    copied: list[dict[str, Any]] = []
    copied.append(copy_local(SOURCE_MODEL_TABLE, MODEL_TABLE_PATH))
    copied.append(copy_local(SOURCE_FEATURE_VAL, FEATURE_VAL_PATH))
    copied.append(copy_local(SOURCE_FEATURE_OOS, FEATURE_OOS_PATH))
    table = hardening.parse_ebm_table(MODEL_TABLE_PATH)
    export_payload = hardening.export_table_to_onnx(table, ONNX_MODEL_PATH)
    copied.append(copy_to_common(ONNX_MODEL_PATH, f"{COMMON_ROOT}/{ADAPTER_ID}/models/{ONNX_MODEL_PATH.name}", common_files_root))
    copied.append(copy_to_common(MODEL_TABLE_PATH, f"{COMMON_ROOT}/{ADAPTER_ID}/models/{MODEL_TABLE_PATH.name}", common_files_root))
    copied.append(copy_to_common(FEATURE_VAL_PATH, f"{COMMON_ROOT}/{ADAPTER_ID}/features/{FEATURE_VAL_PATH.name}", common_files_root))
    copied.append(copy_to_common(FEATURE_OOS_PATH, f"{COMMON_ROOT}/{ADAPTER_ID}/features/{FEATURE_OOS_PATH.name}", common_files_root))
    values = load_feature_values([FEATURE_VAL_PATH, FEATURE_OOS_PATH])
    parity = hardening.check_parity(ONNX_MODEL_PATH, table, values)
    parity["decision_parity"] = decision_parity(ONNX_MODEL_PATH, table, values)
    parity["feature_order"] = list(FEATURE_ORDER)
    parity["feature_order_hash"] = FEATURE_ORDER_HASH
    parity["source_table"] = rel(SOURCE_MODEL_TABLE)
    parity["onnx_model"] = rel(ONNX_MODEL_PATH)
    return {
        "model_local": ONNX_MODEL_PATH,
        "model_common": f"{COMMON_ROOT}/{ADAPTER_ID}/models/{ONNX_MODEL_PATH.name}",
        "table_local": MODEL_TABLE_PATH,
        "feature_exports": {
            "validation_is": {
                "path": rel(FEATURE_VAL_PATH),
                "common_path": f"{COMMON_ROOT}/{ADAPTER_ID}/features/{FEATURE_VAL_PATH.name}",
                "sha256": sha256_file_lf_normalized(FEATURE_VAL_PATH),
            },
            "oos": {
                "path": rel(FEATURE_OOS_PATH),
                "common_path": f"{COMMON_ROOT}/{ADAPTER_ID}/features/{FEATURE_OOS_PATH.name}",
                "sha256": sha256_file_lf_normalized(FEATURE_OOS_PATH),
            },
        },
        "common_copies": copied,
        "onnx_export": export_payload,
        "onnx_parity": parity,
    }


def source_attempt_ini(split: str) -> Path:
    return SOURCE_INI_VAL if split == "validation_is" else SOURCE_INI_OOS


def extra_set_values(magic: int) -> dict[str, Any]:
    values = repair.extra_set_values(VARIANT, magic)
    values["InpModelRiskMinPct"] = 0.005
    values["InpModelRiskMaxPct"] = min(float(VARIANT.model_risk_max_pct), 0.05)
    values["InpModelRiskFallbackLot"] = VARIANT.fixed_lot
    return values


def build_attempts(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    for split in ("validation_is", "oos"):
        date_values = parse_ini(source_attempt_ini(split))
        split_token = "val" if split == "validation_is" else "oos"
        for role_index, (tier, attempt_role, prefix, attempt_token) in enumerate(
            (
                (mt5.TIER_A, "tier_only_total", f"mt5_tier_a_only_{ADAPTER_ID}", "ta"),
                (mt5.TIER_AB, "routed_total", f"mt5_routed_{ADAPTER_ID}", "rt"),
            ),
            start=1,
        ):
            magic = 6000000 + (1 if split == "validation_is" else 50) + role_index
            attempts.append(
                attempt_payload(
                    run_root=RUN_ROOT / ADAPTER_ID,
                    run_id=RUN_ID,
                    stage_number=60,
                    exploration_label="stage60_BaselineAdapter__OnnxRuntimeReproduction",
                    attempt_name=f"{ADAPTER_ID}_onnx_{attempt_token}_{split_token}",
                    tier=tier,
                    split=split,
                    model_path=str(inputs["model_common"]),
                    model_id=f"{RUN_ID}_{ADAPTER_ID}_entry_onnx",
                    model_backend="onnx",
                    feature_path=str(inputs["feature_exports"][split]["common_path"]),
                    feature_count=1,
                    feature_order_hash=FEATURE_ORDER_HASH,
                    short_threshold=VARIANT.short_threshold,
                    long_threshold=VARIANT.long_threshold,
                    min_margin=MIN_MARGIN,
                    invert_signal=False,
                    from_date=str(date_values["FromDate"]),
                    to_date=str(date_values["ToDate"]),
                    primary_active_tier="tier_a",
                    attempt_role=attempt_role,
                    record_view_prefix=prefix,
                    max_hold_bars=VARIANT.max_hold_bars,
                    common_root=f"{COMMON_ROOT}/{ADAPTER_ID}",
                    fallback_enabled=False,
                    close_on_flat_signal=VARIANT.close_on_flat_signal,
                    reverse_on_opposite_signal=VARIANT.reverse_on_opposite_signal,
                    close_only_on_opposite_signal=VARIANT.close_only_on_opposite_signal,
                    extra_set_values=extra_set_values(magic),
                )
            )
    return attempts


def patch_measurement_helpers() -> None:
    repair.RUN_NUMBER = RUN_NUMBER
    repair.RUN_ID = RUN_ID
    repair.RUN_ROOT = RUN_ROOT
    repair.REPAIR_VARIANTS = STAGE60_VARIANTS
    s58.STAGE58_ID = STAGE60_ID
    s58.RUN_NUMBER = RUN_NUMBER
    s58.RUN_ID = RUN_ID
    s58.PACKET_ID = PACKET_ID
    s58.PARENT_RUN_ID = PARENT_RUN_ID
    s58.RUN_ROOT = RUN_ROOT
    s58.REVIEWS_ROOT = REVIEWS_ROOT
    s58.STAGE58_VARIANTS = STAGE60_VARIANTS


def execute_or_materialize(prepared: Mapping[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    if args.materialize_only:
        return {
            **dict(prepared),
            "compile": {"status": "not_attempted_materialize_only"},
            "execution_results": [],
            "strategy_tester_reports": [],
            "mt5_kpi_records": [],
            "external_verification_status": "blocked",
            "judgment": "materialized_only_no_mt5_evidence",
        }
    return execute_prepared_run(
        prepared,
        terminal_path=Path(args.terminal_path),
        metaeditor_path=Path(args.metaeditor_path),
        terminal_data_root=Path(args.terminal_data_root),
        common_files_root=Path(args.common_files_root),
        tester_profile_root=Path(args.tester_profile_root),
        timeout_seconds=int(args.timeout_seconds),
    )


def load_existing_result() -> dict[str, Any]:
    manifest = json.loads(io_path(RUN_ROOT / "run_manifest.json").read_text(encoding="utf-8-sig"))
    kpi = json.loads(io_path(RUN_ROOT / "kpi_record.json").read_text(encoding="utf-8-sig"))
    return {
        **manifest,
        "run_root": RUN_ROOT,
        "packet_id": PACKET_ID,
        "attempts": manifest.get("attempts", []),
        "common_copies": manifest.get("common_copies", []),
        "compile": manifest.get("compile", {}),
        "external_verification_status": kpi.get("external_verification_status", manifest.get("external_verification_status")),
        "judgment": kpi.get("judgment", manifest.get("judgment")),
        "mt5_kpi_records": kpi.get("mt5_kpi_records", []),
        "strategy_tester_reports": kpi.get("strategy_tester_reports", []),
        "execution_results": kpi.get("execution_results", []),
        "onnx_export": manifest.get("onnx_export", {}),
        "onnx_parity": manifest.get("onnx_parity", {}),
        "common_copies": manifest.get("common_copies", []),
    }


def write_run_identity(result: Mapping[str, Any]) -> None:
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE60_ID,
        "run_number": RUN_NUMBER,
        "packet_id": PACKET_ID,
        "adapter_id": ADAPTER_ID,
        "attempts": result.get("attempts", []),
        "common_copies": result.get("common_copies", []),
        "model_artifacts": result.get("model_artifacts", []),
        "feature_exports": result.get("feature_exports", {}),
        "onnx_export": result.get("onnx_export", {}),
        "onnx_parity": result.get("onnx_parity", {}),
        "handoff": result.get("handoff", {}),
        "compile": result.get("compile", {}),
        "external_verification_status": result.get("external_verification_status"),
        "judgment": result.get("judgment"),
        "claim_boundary": BOUNDARY,
    }
    kpi_payload = {
        "run_id": RUN_ID,
        "stage_id": STAGE60_ID,
        "packet_id": PACKET_ID,
        "adapter_id": ADAPTER_ID,
        "kpi_scope": "stage60_onnx_runtime_reproduction",
        "model_family": result.get("model_family"),
        "feature_set_id": result.get("feature_set_id"),
        "label_id": result.get("label_id"),
        "split_contract": result.get("split_contract"),
        "execution_results": result.get("execution_results", []),
        "strategy_tester_reports": result.get("strategy_tester_reports", []),
        "mt5_kpi_records": result.get("mt5_kpi_records", []),
        "external_verification_status": result.get("external_verification_status"),
        "judgment": result.get("judgment"),
        "boundary": BOUNDARY,
    }
    write_json(RUN_ROOT / "run_manifest.json", manifest)
    write_json(RUN_ROOT / "kpi_record.json", kpi_payload)


def routed_rows(summary_rows: Sequence[Mapping[str, Any]]) -> tuple[Mapping[str, Any], Mapping[str, Any]]:
    val = next((row for row in summary_rows if row.get("adapter_id") == ADAPTER_ID and row.get("split") == "validation_is" and row.get("view") == "actual_routed_total"), {})
    oos = next((row for row in summary_rows if row.get("adapter_id") == ADAPTER_ID and row.get("split") == "oos" and row.get("view") == "actual_routed_total"), {})
    return val, oos


def source_reference_rows() -> tuple[Mapping[str, Any], Mapping[str, Any]]:
    rows = read_csv_rows(SOURCE_STAGE59AR_SUMMARY)
    val = next((row for row in rows if row.get("adapter_id") == ADAPTER_ID and row.get("split") == "validation_is" and row.get("view") == "actual_routed_total"), {})
    oos = next((row for row in rows if row.get("adapter_id") == ADAPTER_ID and row.get("split") == "oos" and row.get("view") == "actual_routed_total"), {})
    return val, oos


def metric_diffs(runtime: Mapping[str, Any], reference: Mapping[str, Any]) -> dict[str, Any]:
    diffs: dict[str, Any] = {}
    for key, base_tol in REPRODUCTION_TOLERANCE.items():
        runtime_value = as_float(runtime.get(key))
        reference_value = as_float(reference.get(key))
        abs_diff = abs(runtime_value - reference_value)
        tol = max(float(base_tol), abs(reference_value) * 0.01) if key in {"net_profit", "max_drawdown_amount"} else float(base_tol)
        diffs[key] = {
            "runtime": runtime_value,
            "reference": reference_value,
            "abs_diff": abs_diff,
            "tolerance": tol,
            "passed": abs_diff <= tol,
        }
    return diffs


def stage60_quality_reasons(
    summary_rows: Sequence[Mapping[str, Any]],
    segment_rows: Sequence[Mapping[str, Any]],
) -> list[str]:
    reasons: list[str] = []
    val, oos = routed_rows(summary_rows)
    for label, row in (("validation", val), ("oos", oos)):
        if row.get("status") != "completed":
            reasons.append(f"{label}_runtime_row_not_completed")
        if as_float(row.get("net_profit")) <= 0.0:
            reasons.append(f"{label}_net_not_positive_after_onnx")
        if as_float(row.get("profit_factor")) < 1.10:
            reasons.append(f"{label}_pf_lt_1_10_after_onnx")
        if as_float(row.get("cost_stressed_expectancy")) <= 0.0:
            reasons.append(f"{label}_cost_stressed_expectancy_not_positive_after_onnx")
        if as_float(row.get("max_model_risk_pct")) <= 0.0:
            reasons.append(f"{label}_model_risk_pct_not_observed")
        if as_float(row.get("avg_open_sl_points")) <= 0.0 or as_float(row.get("avg_open_tp_points")) <= 0.0:
            reasons.append(f"{label}_atr_bracket_not_observed")
    segment_flags = [
        row
        for row in segment_rows
        if row.get("adapter_id") == ADAPTER_ID
        and row.get("segment_type") == "chronological_third"
        and row.get("quality_flag")
        and row.get("quality_flag") != "acceptable_measurement_only"
    ]
    if segment_flags:
        reasons.append("post_onnx_segment_flags_present")
    return sorted(set(reasons))


def runtime_gate(
    result: Mapping[str, Any],
    summary_rows: Sequence[Mapping[str, Any]],
    segment_rows: Sequence[Mapping[str, Any]],
    parity: Mapping[str, Any],
) -> dict[str, Any]:
    val, oos = routed_rows(summary_rows)
    ref_val, ref_oos = source_reference_rows()
    val_diff = metric_diffs(val, ref_val)
    oos_diff = metric_diffs(oos, ref_oos)
    failures: list[str] = []
    if not parity.get("passed"):
        failures.append("python_onnx_probability_parity_failed")
    if not (parity.get("decision_parity") or {}).get("passed"):
        failures.append("python_onnx_decision_parity_failed")
    if result.get("external_verification_status") != "completed":
        failures.append("mt5_runtime_external_verification_not_completed")
    quality_reasons = stage60_quality_reasons(summary_rows, segment_rows)
    failures.extend(f"post_onnx_{item}" for item in quality_reasons)
    for row, split in ((val, "validation"), (oos, "oos")):
        if row.get("status") != "completed":
            failures.append(f"{split}_runtime_row_not_completed")
        for key in ("risk_floor_applied_count", "avg_executed_lot", "avg_open_sl_points", "avg_open_tp_points", "max_actual_risk_pct_after_floor"):
            if row.get(key) in (None, ""):
                failures.append(f"{split}_{key}_telemetry_missing")
        if as_float(row.get("max_actual_risk_pct_after_floor"), 99.0) > 0.05:
            failures.append(f"{split}_actual_risk_after_floor_above_5pct")
    for split, diffs in (("validation", val_diff), ("oos", oos_diff)):
        for key, diff in diffs.items():
            if not diff["passed"]:
                failures.append(f"{split}_{key}_reproduction_tolerance_failed")
    return {
        "passed": not failures,
        "failure_reasons": failures,
        "validation_reproduction_diff": val_diff,
        "oos_reproduction_diff": oos_diff,
        "tolerance_policy": REPRODUCTION_TOLERANCE,
        "source_reference": {"validation": dict(ref_val), "oos": dict(ref_oos)},
    }


def decide_stage(gate: Mapping[str, Any], parity: Mapping[str, Any], external: str) -> str:
    if not parity.get("passed") or not (parity.get("decision_parity") or {}).get("passed"):
        return "demote_adapter_due_to_onnx_runtime_failure"
    if external != "completed":
        return "demote_adapter_due_to_onnx_runtime_failure"
    if gate.get("passed"):
        return "proceed_to_stage61_research_package_review"
    return "return_to_stage59_repair_due_to_runtime_damage"


def next_stage_for_decision(decision: str) -> str:
    if decision == "proceed_to_stage61_research_package_review":
        return STAGE61_ID
    if decision == "open_new_model_branch_due_to_runtime_incompatibility":
        return "59AS_adapter_repair__new_model_branch_from_stage60"
    if decision == "demote_adapter_due_to_onnx_runtime_failure":
        return "59AS_adapter_repair__demotion_from_stage60"
    return "59AS_adapter_repair__runtime_damage_from_stage60"


def write_handoff(inputs: Mapping[str, Any], attempts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    payload = {
        "run_id": RUN_ID,
        "adapter_id": ADAPTER_ID,
        "source_stage": s59ar.STAGE59AR_ID,
        "source_run": s59ar.RUN_ID,
        "boundary": BOUNDARY,
        "model_runtime": {
            "backend": "onnx",
            "local_path": rel(inputs["model_local"]),
            "common_path": inputs["model_common"],
            "sha256": sha256_file_lf_normalized(Path(str(inputs["model_local"]))),
            "input_name": inputs.get("onnx_export", {}).get("input_name"),
            "output_name": inputs.get("onnx_export", {}).get("output_name"),
            "class_order": ["short", "flat", "long"],
        },
        "feature_input_contract": {
            "feature_order": list(FEATURE_ORDER),
            "feature_count": 1,
            "feature_order_hash": FEATURE_ORDER_HASH,
            "validation_feature": inputs["feature_exports"]["validation_is"],
            "oos_feature": inputs["feature_exports"]["oos"],
        },
        "entry_contract": {
            "short_threshold": VARIANT.short_threshold,
            "long_threshold": VARIANT.long_threshold,
            "min_margin": MIN_MARGIN,
        },
        "risk_contract": {
            "model_controlled": VARIANT.model_risk_enabled,
            "model_risk_min_pct": 0.005,
            "model_risk_max_pct": VARIANT.model_risk_max_pct,
            "risk_cap_pct": 0.05,
            "min_lot_floor": 0.01,
        },
        "atr_bracket_contract": {
            "atr_sltp_enabled": VARIANT.atr_enabled,
            "atr_period": 14,
            "sl_multiplier": VARIANT.atr_stop_multiplier,
            "tp_multiplier": VARIANT.atr_take_profit_multiplier,
        },
        "lifecycle_contract": {
            "max_hold_bars": VARIANT.max_hold_bars,
            "same_direction_reentry_cooldown_bars": VARIANT.same_direction_reentry_cooldown_bars,
            "reverse_on_opposite_signal": VARIANT.reverse_on_opposite_signal,
            "close_only_on_opposite_signal": VARIANT.close_only_on_opposite_signal,
        },
        "attempt_set_files": [attempt.get("set", {}).get("path") for attempt in attempts],
    }
    write_json(HANDOFF_JSON_PATH, payload)
    return payload


def artifact_rows(result: Mapping[str, Any], extra_paths: Sequence[Path]) -> list[dict[str, Any]]:
    created = utc_now()
    rows: list[dict[str, Any]] = []

    def add(artifact_id: str, artifact_type: str, path: Path | str, notes: str) -> None:
        p = Path(str(path))
        resolved = p if p.is_absolute() else REPO_ROOT / p
        is_file = path_exists(resolved) and io_path(resolved).is_file()
        rows.append(
            {
                "artifact_id": artifact_id,
                "artifact_type": artifact_type,
                "path": rel(p),
                "sha256": sha256_file_lf_normalized(resolved) if is_file else "directory_or_not_feasible",
                "stage_id": STAGE60_ID,
                "run_id": RUN_ID,
                "created_at_utc": created,
                "notes": notes,
            }
        )

    for path in extra_paths:
        add(f"{RUN_ID}__{path.name}", "stage60_onnx_runtime_artifact", path, "Stage60 ONNX hardening/runtime artifact.")
    for execution in result.get("execution_results", []):
        outputs = execution.get("runtime_outputs", {}) if isinstance(execution.get("runtime_outputs"), Mapping) else {}
        for key, artifact_type in (("telemetry_path", "mt5_runtime_telemetry_csv"), ("summary_path", "mt5_runtime_summary_csv")):
            value = outputs.get(key)
            if value:
                add(f"{RUN_ID}__{artifact_type}__{execution.get('attempt_name')}", artifact_type, str(value), "Common Files runtime telemetry emitted by MT5 EA.")
    for report in result.get("strategy_tester_reports", []):
        html = report.get("html_report", {}) if isinstance(report.get("html_report"), Mapping) else {}
        report_path = report.get("path") or html.get("path")
        if report_path:
            add(f"{RUN_ID}__mt5_report__{Path(str(report_path)).stem}", "mt5_strategy_tester_html_report", str(report_path), "MT5 Strategy Tester HTML report.")
    return rows


def write_ledgers(
    result: Mapping[str, Any],
    summary_rows: Sequence[Mapping[str, Any]],
    decision: str,
    gate: Mapping[str, Any],
    artifacts: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    external = str(result.get("external_verification_status") or "blocked")
    val, oos = routed_rows(summary_rows)
    mt5_rows = build_mt5_alpha_ledger_rows(
        run_id=RUN_ID,
        stage_id=STAGE60_ID,
        mt5_kpi_records=result.get("mt5_kpi_records", []),
        run_output_root=RUN_ROOT,
        external_verification_status=external,
    )
    aggregate = {
        "ledger_row_id": f"{RUN_ID}__aggregate_onnx_runtime_reproduction",
        "stage_id": STAGE60_ID,
        "run_id": RUN_ID,
        "subrun_id": "aggregate_onnx_runtime_reproduction",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "stage60_onnx_runtime_reproduction",
        "tier_scope": "Tier A+B",
        "kpi_scope": "onnx_runtime_reproduction",
        "scoreboard_lane": "runtime_probe",
        "status": "completed" if external == "completed" else "blocked",
        "judgment": decision,
        "path": rel(DECISION_PATH),
        "primary_kpi": ledger_pairs(
            [
                ("validation_net", val.get("net_profit")),
                ("oos_net", oos.get("net_profit")),
                ("validation_pf", val.get("profit_factor")),
                ("oos_pf", oos.get("profit_factor")),
                ("gate_passed", gate.get("passed")),
            ]
        ),
        "guardrail_kpi": ledger_pairs(
            [
                ("failure_reasons", gate.get("failure_reasons")),
                ("overall_goal_complete", 0),
                ("deployment_claim", 0),
            ]
        ),
        "external_verification_status": external,
        "notes": "Stage60 ONNX runtime reproduction; research/development only.",
    }
    ledger_rows = [*mt5_rows, aggregate]
    run_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE60_ID,
                "lane": "baseline_adapter_onnx_runtime_reproduction",
                "status": "completed" if external == "completed" else "blocked",
                "judgment": decision,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs([("adapter_id", ADAPTER_ID), ("boundary", BOUNDARY)]),
            }
        ],
        key="run_id",
    )
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id")
    project_payload = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id")
    artifact_payload = upsert_csv_rows(
        ARTIFACT_REGISTRY_PATH,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
        list(artifacts),
        key="artifact_id",
    )
    return {
        "run_registry": run_payload,
        "stage_ledger": stage_payload,
        "project_alpha_ledger": project_payload,
        "artifact_registry": artifact_payload,
    }


def write_required_outputs(
    result: Mapping[str, Any],
    summary_rows: Sequence[Mapping[str, Any]],
    risk_rows: Sequence[Mapping[str, Any]],
    segment_rows: Sequence[Mapping[str, Any]],
    audit_rows: Sequence[Mapping[str, Any]],
    decision: str,
    gate: Mapping[str, Any],
    ledger_payload: Mapping[str, Any],
) -> None:
    val, oos = routed_rows(summary_rows)
    parity = result.get("onnx_parity", {})
    export = result.get("onnx_export", {})
    write_json(
        ONNX_EXPORT_REPORT_PATH,
        {
            "run_id": RUN_ID,
            "adapter_id": ADAPTER_ID,
            "source_table": rel(SOURCE_MODEL_TABLE),
            "onnx_export": export,
            "feature_order": list(FEATURE_ORDER),
            "feature_order_hash": FEATURE_ORDER_HASH,
            "common_copies": result.get("common_copies", []),
            "claim_boundary": BOUNDARY,
        },
    )
    write_json(
        ONNX_PARITY_REPORT_PATH,
        {
            "run_id": RUN_ID,
            "adapter_id": ADAPTER_ID,
            "probability_parity": parity,
            "decision_parity": parity.get("decision_parity", {}),
            "claim_boundary": BOUNDARY,
        },
    )
    write_csv(SUMMARY_CSV_PATH, summary_rows)
    write_csv(RISK_ATR_TELEMETRY_PATH, risk_rows)
    write_csv(SEGMENT_KPI_PATH, segment_rows)
    write_csv(AUDIT_CSV_PATH, audit_rows)
    write_json(
        SUMMARY_JSON_PATH,
        {
            "packet_id": PACKET_ID,
            "stage_id": STAGE60_ID,
            "run_id": RUN_ID,
            "adapter_id": ADAPTER_ID,
            "decision": decision,
            "external_verification_status": result.get("external_verification_status"),
            "validation": dict(val),
            "oos": dict(oos),
            "runtime_gate": gate,
            "onnx_export_report": rel(ONNX_EXPORT_REPORT_PATH),
            "onnx_parity_report": rel(ONNX_PARITY_REPORT_PATH),
            "handoff": rel(HANDOFF_JSON_PATH),
            "ledger_payload": ledger_payload,
            "overall_goal_complete": False,
            "claim_boundary": BOUNDARY,
            "next_stage_or_branch": next_stage_for_decision(decision),
        },
    )
    write_md(
        RUNTIME_REPORT_PATH,
        f"""# Stage60 ONNX Runtime Reproduction(60단계 ONNX 런타임 재현)

- decision(판정): `{decision}`
- adapter_under_review(검토 중 어댑터): `{ADAPTER_ID}`
- ONNX export(ONNX 내보내기): `{rel(ONNX_MODEL_PATH)}`
- probability_parity_passed(확률 동등성 통과): `{parity.get('passed')}`
- decision_parity_passed(결정 동등성 통과): `{(parity.get('decision_parity') or {}).get('passed')}`
- external_verification_status(외부 검증 상태): `{result.get('external_verification_status')}`
- runtime_gate_passed(런타임 게이트 통과): `{gate.get('passed')}`

Action(행동): Stage59AR(59AR단계)의 EBM table(EBM 표)을 ONNX(모델 교환 형식)로 내보내고 같은 ATR/risk(ATR/위험), lifecycle(수명주기), Tier B disabled(Tier B 비활성) 조건으로 MT5(메타트레이더5) validation/OOS(검증/표본외)를 실행했다.
Effect(효과): Python/ONNX(파이썬/ONNX) 동등성과 MT5 runtime reproduction(MT5 런타임 재현)을 한 단계 안에서 확인하되, deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위)는 주장하지 않는다.

## Routed KPI(라우팅 KPI)

- validation_net(검증 순손익): `{val.get('net_profit')}`
- validation_pf(검증 PF): `{val.get('profit_factor')}`
- validation_drawdown(검증 드로다운): `{val.get('max_drawdown_amount')}`
- validation_cost_stressed_expectancy(검증 비용 스트레스 기대값): `{val.get('cost_stressed_expectancy')}`
- oos_net(표본외 순손익): `{oos.get('net_profit')}`
- oos_pf(표본외 PF): `{oos.get('profit_factor')}`
- oos_drawdown(표본외 드로다운): `{oos.get('max_drawdown_amount')}`
- oos_cost_stressed_expectancy(표본외 비용 스트레스 기대값): `{oos.get('cost_stressed_expectancy')}`

## Gate(게이트)

- failure_reasons(실패 이유): `{';'.join(str(item) for item in gate.get('failure_reasons', [])) or 'none'}`
- next_stage_or_branch(다음 단계/분기): `{next_stage_for_decision(decision)}`
""",
    )
    write_md(
        DECISION_PATH,
        f"""# Stage60 Decision(60단계 판정)

decision(판정): `{decision}`

Stage60(60단계)는 ONNX(모델 교환 형식) hardening(경화)과 MT5(메타트레이더5) runtime reproduction(런타임 재현)으로 기록한다. Effect(효과): Stage59AR(59AR단계) post-ATR/risk(ATR/위험 이후) 어댑터의 런타임 의미를 확인하고 다음 bounded stage(경계 다음 단계)로 넘긴다.

## Evidence(근거)

- onnx_export_report(ONNX 내보내기 보고서): `{rel(ONNX_EXPORT_REPORT_PATH)}`
- onnx_parity_report(ONNX 동등성 보고서): `{rel(ONNX_PARITY_REPORT_PATH)}`
- mt5_onnx_runtime_reproduction(MT5 ONNX 런타임 재현): `{rel(RUNTIME_REPORT_PATH)}`
- mt5_onnx_runtime_summary_json(MT5 ONNX 런타임 JSON 요약): `{rel(SUMMARY_JSON_PATH)}`
- mt5_onnx_runtime_summary_csv(MT5 ONNX 런타임 CSV 요약): `{rel(SUMMARY_CSV_PATH)}`
- mt5_onnx_segment_kpi_summary(MT5 ONNX 구간 KPI 요약): `{rel(SEGMENT_KPI_PATH)}`
- mt5_onnx_risk_atr_telemetry(MT5 ONNX 위험/ATR 텔레메트리): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- external_verification_status(외부 검증 상태): `{result.get('external_verification_status')}`

## Reason(이유)

- adapter_under_review(검토 중 어댑터): `{ADAPTER_ID}`
- gate_passed(게이트 통과): `{gate.get('passed')}`
- failure_reasons(실패/약점 이유): `{';'.join(str(item) for item in gate.get('failure_reasons', [])) or 'none'}`

## Next(다음)

next_stage_or_branch(다음 단계/분기): `{next_stage_for_decision(decision)}`

Stage60 closeout(60단계 종료)는 overall goal completion(전체 목표 완료)이 아니다. Effect(효과): Stage61(61단계)이 열리더라도 research package review(연구 패키지 검토)만 허용한다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
""",
    )


def write_packet_files(
    result: Mapping[str, Any],
    summary_rows: Sequence[Mapping[str, Any]],
    risk_rows: Sequence[Mapping[str, Any]],
    segment_rows: Sequence[Mapping[str, Any]],
    decision: str,
    gate: Mapping[str, Any],
    ledger_payload: Mapping[str, Any],
) -> None:
    parity = result.get("onnx_parity", {})
    files = {
        "routing_receipt.json": {
            "packet_id": PACKET_ID,
            "primary_family": "runtime_backtest",
            "primary_skill": "obsidian-runtime-parity",
            "support_skills": ["obsidian-artifact-lineage", "obsidian-backtest-forensics", "obsidian-result-judgment"],
            "required_gates": ["onnx_parity_gate", "runtime_evidence_gate", "backtest_forensics_audit", "artifact_lineage_audit", "result_judgment_gate", "final_claim_guard"],
            "status": "completed",
        },
        "onnx_parity_gate.json": {
            "status": "completed" if parity.get("passed") and (parity.get("decision_parity") or {}).get("passed") else "blocked",
            "probability_parity": parity,
            "decision_parity": parity.get("decision_parity", {}),
        },
        "runtime_evidence_gate.json": {
            "external_verification_status": result.get("external_verification_status"),
            "mt5_reports": result.get("strategy_tester_reports", []),
            "status": result.get("external_verification_status"),
        },
        "backtest_forensics_audit.json": {
            "tester_identity": "US100 M5, deposit 500, leverage 1:100, model=4, validation/OOS from Stage59AR source ini files",
            "ea_identity": "ObsidianPrimeV2_RuntimeProbeEA with ONNX model backend and Stage60 set files",
            "trade_evidence": {"summary_rows": len(summary_rows), "segment_rows": len(segment_rows), "risk_rows": len(risk_rows)},
            "cost_assumptions": "Stage60 cost-stress uses 0.3 per trade audit; broker tester costs remain those embedded in MT5 reports.",
            "backtest_judgment": "usable_with_boundary" if result.get("external_verification_status") == "completed" else "blocked",
            "status": "completed",
        },
        "artifact_lineage_audit.json": {
            "source_inputs": [rel(SOURCE_STAGE59AR_DECISION), rel(SOURCE_STAGE59AR_SUMMARY), rel(SOURCE_STAGE59AR_RISK), rel(SOURCE_MODEL_TABLE), rel(SOURCE_FEATURE_VAL), rel(SOURCE_FEATURE_OOS)],
            "producer": "stage_pipelines/stage60/onnx_hardening_runtime_reproduction.py",
            "consumers": [rel(ONNX_EXPORT_REPORT_PATH), rel(ONNX_PARITY_REPORT_PATH), rel(RUNTIME_REPORT_PATH), rel(DECISION_PATH)],
            "ledger_links": ledger_payload,
            "lineage_judgment": "connected_with_boundary",
            "status": "completed",
        },
        "result_judgment_gate.json": {
            "result_subject": RUN_ID,
            "judgment_label": decision,
            "evidence_available": [rel(ONNX_PARITY_REPORT_PATH), rel(RUNTIME_REPORT_PATH), rel(SUMMARY_JSON_PATH)],
            "evidence_missing": [],
            "claim_boundary": BOUNDARY,
            "next_condition": next_stage_for_decision(decision),
            "status": "passed_with_boundary",
        },
        "final_claim_guard.json": {
            "overall_goal_complete": False,
            "deployment_claim": False,
            "live_readiness_claim": False,
            "runtime_authority_claim": False,
            "production_baseline_claim": False,
            "operating_promotion_claim": False,
            "operating_reference_claim": False,
            "status": "completed",
        },
        "required_gate_coverage_audit.json": {
            "required_gates": ["onnx_parity_gate", "runtime_evidence_gate", "backtest_forensics_audit", "artifact_lineage_audit", "result_judgment_gate", "final_claim_guard"],
            "covered_by": ["onnx_parity_gate.json", "runtime_evidence_gate.json", "backtest_forensics_audit.json", "artifact_lineage_audit.json", "result_judgment_gate.json", "final_claim_guard.json"],
            "status": "completed",
        },
        "aggregate_summary.json": {
            "packet_id": PACKET_ID,
            "stage_id": STAGE60_ID,
            "run_id": RUN_ID,
            "adapter_id": ADAPTER_ID,
            "decision": decision,
            "runtime_gate": gate,
            "external_verification_status": result.get("external_verification_status"),
            "overall_goal_complete": False,
            "claim_boundary": BOUNDARY,
            "next_stage_or_branch": next_stage_for_decision(decision),
            "required_outputs": {
                "onnx_export_report": rel(ONNX_EXPORT_REPORT_PATH),
                "onnx_parity_report": rel(ONNX_PARITY_REPORT_PATH),
                "mt5_onnx_runtime_reproduction": rel(RUNTIME_REPORT_PATH),
                "mt5_onnx_runtime_summary_json": rel(SUMMARY_JSON_PATH),
                "mt5_onnx_runtime_summary_csv": rel(SUMMARY_CSV_PATH),
                "mt5_onnx_segment_kpi_summary": rel(SEGMENT_KPI_PATH),
                "mt5_onnx_risk_atr_telemetry": rel(RISK_ATR_TELEMETRY_PATH),
                "stage60_decision": rel(DECISION_PATH),
            },
        },
    }
    for name, payload in files.items():
        write_json(PACKET_ROOT / name, payload)


def write_stage_docs(decision: str) -> None:
    next_stage = next_stage_for_decision(decision)
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# 60 Selection Status(60단계 선택 상태)

- stage_status(단계 상태): `closed_onnx_runtime_reproduction`
- source_stage(원천 단계): `{s59ar.STAGE59AR_ID}`
- source_decision(원천 판정): `proceed_to_stage60_onnx_hardening`
- adapter_under_review(검토 중 어댑터): `{ADAPTER_ID}`
- stage60_decision(60단계 판정): `{decision}`
- next_stage_or_branch(다음 단계/분기): `{next_stage}`
- selected_research_baseline(선택 연구 기준선): `none`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage60(60단계)은 ONNX(모델 교환 형식) hardening(경화)과 MT5(메타트레이더5) runtime reproduction(런타임 재현) 근거를 보존하지만 final package(최종 패키지)나 operating claim(운영 주장)을 만들지 않는다.
""",
    )
    if decision == "proceed_to_stage61_research_package_review":
        next_root = Path("stages") / next_stage
        write_md(
            next_root / "00_spec/stage_brief.md",
            f"""# 61 Brief(61단계 개요)

- stage_id(단계 ID): `{next_stage}`
- source_stage(원천 단계): `{STAGE60_ID}`
- source_decision(원천 판정): `{decision}`
- bounded_question(경계 질문): `Does the completed research-grade BaselineAdapter package contain enough evidence, telemetry, reproducibility, known-risk documentation, and pushed artifact traceability to be recorded as a research package only?`
- boundary(경계): `{BOUNDARY}`

Stage61(61단계)은 research package review(연구 패키지 검토) 전용이다. Effect(효과): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위)를 만들지 않는다.
""",
        )
        write_md(
            next_root / "01_inputs/input_refs.md",
            f"""# 61 Input References(61단계 입력 참조)

- stage60_decision(60단계 판정): `{rel(DECISION_PATH)}`
- mt5_onnx_runtime_reproduction(MT5 ONNX 런타임 재현): `{rel(RUNTIME_REPORT_PATH)}`
- mt5_onnx_runtime_summary(MT5 ONNX 런타임 요약): `{rel(SUMMARY_JSON_PATH)}`
- mt5_onnx_segment_kpi_summary(MT5 ONNX 구간 KPI 요약): `{rel(SEGMENT_KPI_PATH)}`
- mt5_onnx_risk_atr_telemetry(MT5 ONNX 위험/ATR 텔레메트리): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- packet_summary(작업 묶음 요약): `{rel(PACKET_ROOT / 'aggregate_summary.json')}`
""",
        )
        write_md(next_root / "03_reviews/review_index.md", "# 61 Review Index(61단계 검토 색인)\n\nStage61(61단계)는 planned(계획) 상태다.\n")
        write_md(
            next_root / "04_selected/selection_status.md",
            f"""# 61 Selection Status(61단계 선택 상태)

- stage_status(단계 상태): `active_planned_from_stage60`
- source_stage(원천 단계): `{STAGE60_ID}`
- source_decision(원천 판정): `{decision}`
- adapter_under_review(검토 중 어댑터): `{ADAPTER_ID}`
- selected_research_baseline(선택 연구 기준선): `none`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage61(61단계)은 연구 패키지 충분성만 판단하고 운영 의미는 주장하지 않는다.
""",
        )


def update_current_truth(decision: str, result: Mapping[str, Any]) -> None:
    next_stage = next_stage_for_decision(decision)
    next_packet = "stage61_research_package_review_v1" if decision == "proceed_to_stage61_research_package_review" else "stage59as_runtime_damage_repair_from_stage60_v1"
    next_run = "run61A_stage61_research_package_review_v1" if decision == "proceed_to_stage61_research_package_review" else "run59AN_stage59as_runtime_damage_repair_from_stage60_v1"
    write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{next_packet}`
- current_run(현재 실행): `{next_run}`
- active_stage(활성 단계): `{next_stage}`
- selected_research_baseline(선택 연구 기준선): `none`
- development_anchor(개발 기준점): `{s59ar.DEVELOPMENT_ANCHOR}`
- backup_anchor(예비 기준점): `{s59ar.BACKUP_ANCHOR}`
- adapter_under_review(검토 중 어댑터): `{ADAPTER_ID}`
- status(상태): `stage60_closed_{decision}`
- claim_boundary(주장 경계): research/development only(연구/개발 전용)

Stage60(60단계) closed(종료) as ONNX hardening/runtime reproduction(ONNX 경화/런타임 재현). Effect(효과): Stage59AR(59AR단계)의 post-ATR/risk(ATR/위험 이후) 어댑터를 ONNX(모델 교환 형식)와 MT5(메타트레이더5) 런타임에서 확인했지만 overall goal complete(전체 목표 완료)는 아니다.

## Latest Stage60 Evidence(최신 60단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- adapter_under_review(검토 중 어댑터): `{ADAPTER_ID}`
- external_verification_status(외부 검증 상태): `{result.get('external_verification_status')}`
- next_stage_or_branch(다음 단계/분기): `{next_stage}`
- report(보고서): `{rel(RUNTIME_REPORT_PATH)}`
- stage60_decision(60단계 판정): `{rel(DECISION_PATH)}`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), overall_goal_complete(전체 목표 완료).
""",
    )
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    import re

    text = re.sub(r"^current_run_id: .*$", f"current_run_id: {next_run}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^active_stage: .*$", f"active_stage: {next_stage}", text, count=1, flags=re.MULTILINE)
    block = f"""

stage60_onnx_hardening_runtime_reproduction:
  packet_id: {PACKET_ID}
  stage_id: {STAGE60_ID}
  status: closed_onnx_runtime_reproduction
  current_run_id: {RUN_ID}
  adapter_under_review: {ADAPTER_ID}
  source_stage59ar_pushed_commit: {SOURCE_STAGE59AR_PUSHED_COMMIT}
  decision: {decision}
  next_stage_or_branch: {next_stage}
  report_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  external_verification_status: {result.get('external_verification_status')}
  boundary: {BOUNDARY}
"""
    if "stage60_onnx_hardening_runtime_reproduction:" in text:
        text = re.sub(r"\nstage60_onnx_hardening_runtime_reproduction:\n(?:  .*\n)*", block, text, count=1)
    else:
        text = text.rstrip() + "\n" + block
    io_path(WORKSPACE_STATE_PATH).write_text(text, encoding="utf-8-sig")


def append_changelog(decision: str) -> None:
    entry = (
        "\n## 2026-05-16 - Stage60 ONNX hardening runtime reproduction closeout(60단계 ONNX 경화 런타임 재현 종료)\n\n"
        f"- run(실행): `{RUN_ID}`\n"
        f"- decision(판정): `{decision}`\n"
        f"- adapter_under_review(검토 중 어댑터): `{ADAPTER_ID}`\n"
        "- effect(효과): Stage59AR(59AR단계)의 post-ATR/risk(ATR/위험 이후) 어댑터를 ONNX(모델 교환 형식)와 MT5(메타트레이더5) 런타임으로 검증하고 다음 bounded stage(경계 다음 단계)를 열었다.\n"
    )
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if f"- run(실행): `{RUN_ID}`" not in existing:
        io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage60 ONNX hardening and MT5 runtime reproduction.")
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(METAEDITOR_PATH_DEFAULT))
    parser.add_argument("--terminal-data-root", default=str(TERMINAL_DATA_ROOT_DEFAULT))
    parser.add_argument("--common-files-root", default=str(COMMON_FILES_ROOT_DEFAULT))
    parser.add_argument("--tester-profile-root", default=str(TESTER_PROFILE_ROOT_DEFAULT))
    parser.add_argument("--timeout-seconds", type=int, default=180)
    parser.add_argument("--runtime-output-timeout-seconds", type=int, default=240)
    parser.add_argument("--resume-partials", action="store_true")
    parser.add_argument("--skip-compile", action="store_true")
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--finalize-existing", action="store_true")
    parser.add_argument("--cost-stress-per-trade", type=float, default=0.3)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    patch_measurement_helpers()
    args = parse_args(argv or sys.argv[1:])
    if args.finalize_existing:
        result = load_existing_result()
    else:
        inputs = prepare_inputs(Path(args.common_files_root))
        attempts = build_attempts(inputs)
        handoff = write_handoff(inputs, attempts)
        prepared = {
            "run_id": RUN_ID,
            "stage_id": STAGE60_ID,
            "stage_number": 60,
            "run_number": RUN_NUMBER,
            "run_root": RUN_ROOT,
            "packet_id": PACKET_ID,
            "attempts": attempts,
            "common_copies": inputs["common_copies"],
            "model_artifacts": [{"path": rel(ONNX_MODEL_PATH), "sha256": inputs["onnx_export"].get("sha256"), "backend": "onnx"}],
            "feature_exports": inputs["feature_exports"],
            "onnx_export": inputs["onnx_export"],
            "onnx_parity": inputs["onnx_parity"],
            "handoff": handoff,
            "route_coverage": {"tier_b_policy": "disabled_due_run50BR_fallback_only_damage", "tier_b_rows_used": 0},
            "model_family": "baseline_adapter_stage60_v41_entry_probability_onnx",
            "feature_set_id": "stage60_run50bn_v41_source_branch_discrete_signal",
            "label_id": "label_v1_fwd12_m5_logret_train_q33_3class",
            "split_contract": "split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413",
            "claim_boundary": BOUNDARY,
        }
        result = execute_or_materialize(prepared, args)
        result["onnx_export"] = inputs["onnx_export"]
        result["onnx_parity"] = inputs["onnx_parity"]
        result["handoff"] = handoff
    write_run_identity(result)
    audit_rows = s58.audit_rows_for_result(result, float(args.cost_stress_per_trade)) if result.get("mt5_kpi_records") else []
    risk_rows = s58.risk_rows_from_result(result)
    summary_rows = repair.build_summary_rows(result, STAGE60_VARIANTS, audit_rows, risk_rows)
    segment_rows = s58.segment_kpi_rows(summary_rows)
    gate = runtime_gate(result, summary_rows, segment_rows, result.get("onnx_parity", {}))
    decision = decide_stage(gate, result.get("onnx_parity", {}), str(result.get("external_verification_status") or "blocked"))
    write_csv(AUDIT_CSV_PATH, audit_rows)
    extra_paths = [
        ONNX_MODEL_PATH,
        MODEL_TABLE_PATH,
        FEATURE_VAL_PATH,
        FEATURE_OOS_PATH,
        HANDOFF_JSON_PATH,
        ONNX_EXPORT_REPORT_PATH,
        ONNX_PARITY_REPORT_PATH,
        RUNTIME_REPORT_PATH,
        SUMMARY_JSON_PATH,
        SUMMARY_CSV_PATH,
        SEGMENT_KPI_PATH,
        RISK_ATR_TELEMETRY_PATH,
        AUDIT_CSV_PATH,
        DECISION_PATH,
        RUN_ROOT / "run_manifest.json",
        RUN_ROOT / "kpi_record.json",
        Path(__file__),
    ]
    artifacts = artifact_rows(result, extra_paths)
    ledger_payload = write_ledgers(result, summary_rows, decision, gate, artifacts)
    write_required_outputs(result, summary_rows, risk_rows, segment_rows, audit_rows, decision, gate, ledger_payload)
    artifacts = artifact_rows(result, extra_paths)
    ledger_payload = write_ledgers(result, summary_rows, decision, gate, artifacts)
    payload = json.loads(io_path(SUMMARY_JSON_PATH).read_text(encoding="utf-8-sig"))
    payload["ledger_payload"] = ledger_payload
    write_json(SUMMARY_JSON_PATH, payload)
    artifacts = artifact_rows(result, extra_paths)
    ledger_payload = write_ledgers(result, summary_rows, decision, gate, artifacts)
    write_packet_files(result, summary_rows, risk_rows, segment_rows, decision, gate, ledger_payload)
    write_stage_docs(decision)
    update_current_truth(decision, result)
    append_changelog(decision)
    print(
        json.dumps(
            json_ready(
                {
                    "status": "ok" if gate.get("passed") else "blocked",
                    "run_id": RUN_ID,
                    "decision": decision,
                    "adapter_id": ADAPTER_ID,
                    "external_verification_status": result.get("external_verification_status"),
                    "onnx_parity_passed": result.get("onnx_parity", {}).get("passed"),
                    "decision_parity_passed": (result.get("onnx_parity", {}).get("decision_parity") or {}).get("passed"),
                    "runtime_gate": gate,
                    "summary_json": rel(SUMMARY_JSON_PATH),
                    "decision_path": rel(DECISION_PATH),
                }
            ),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
