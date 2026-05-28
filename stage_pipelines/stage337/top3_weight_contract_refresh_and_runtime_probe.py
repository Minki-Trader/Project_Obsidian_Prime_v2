from __future__ import annotations

import argparse
import csv
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, path_exists  # noqa: E402
from foundation.features.top3_price_proxy_weights import (  # noqa: E402
    PriceProxyWeightSpec,
    compute_monthly_price_proxy_weights,
    load_common_close_frame,
)
from foundation.mt5 import runtime_support as mt5  # noqa: E402
from foundation.mt5.runtime_artifacts import sha256_file  # noqa: E402
from stage_pipelines.stage329 import materialize_forward_feature_frames as stage329b  # noqa: E402
from stage_pipelines.stage337 import build_live_computable_feature_frame_preflight_without_db as bp  # noqa: E402
from stage_pipelines.stage337 import implement_asof_feature_join_and_runtime_parity_package_without_db as bq  # noqa: E402
from stage_pipelines.stage337 import materialize_common_files_and_run_argmax_parity_probe as el  # noqa: E402
from stage_pipelines.stage337 import refresh_survivor_feature_handoff_and_surface_reprobe as eo  # noqa: E402


RUN_NUMBER = "run337EP"
RUN_ID = "run337EP_refreshed_forward_surface_runtime_probe_or_failure_memory_without_db_v1"
PARENT_RUN_ID = eo.RUN_ID
NEXT_RUN_ID = "run337EQ_forward_kpi_attribution_cost_stress_curve_pocket_without_db_v1"
STATUS = "completed_stage337EP_top3_weight_contract_repaired_runtime_probe_executed_no_forward_decision"
JUDGMENT = "top3_2026_05_weight_contract_resolved_feature_gap_and_mt5_argmax_runtime_parity_passed_but_forward_kpi_not_claimed"
DECISION = "stage337EP_open_run337EQ_forward_kpi_attribution_cost_stress_curve_pocket"
CLAIM_BOUNDARY = (
    "research_development_only_stage337EP_top3_weight_contract_refresh_surface_runtime_probe_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_ID = el.STAGE_ID
STAGE_DIR = el.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RAW_ROOT = STAGE_DIR / "02_runs" / "run337EO" / "raw_refresh_probe"
RAW_LATEST = STAGE_DIR / "02_runs" / "run337EO" / "raw_refresh_latest.json"
WEIGHT_CONTRACT = RUN_DIR / "top3_monthly_price_proxy_weights_fpmarkets_v2_plus_2026_05.csv"
WEIGHT_AUDIT = RUN_DIR / "top3_weight_contract_refresh_audit.csv"
FEATURE_FRAME_DIR = RUN_DIR / "feature_frames"
FEATURE_ORDER_DIR = RUN_DIR / "feature_orders"
FEATURE_SUMMARY_DIR = RUN_DIR / "feature_summaries"
FEATURE_SET_SUMMARY = RUN_DIR / "feature_set_materialization_summary.csv"
MISSING_FEATURE_COUNTS = RUN_DIR / "missing_feature_counts.csv"
INVALID_ROW_SAMPLES = RUN_DIR / "invalid_row_samples.csv"
ASOF_SOURCE_LAG_SUMMARY = RUN_DIR / "asof_source_lag_summary.csv"
SURFACE_REPROBE = RUN_DIR / "survivor_forward_surface_reprobe.csv"
SURFACE_CHUNKS = RUN_DIR / "survivor_forward_surface_chunks.csv"
FEATURE_REFRESH_AUDIT = RUN_DIR / "survivor_feature_refresh_audit.csv"
ONNX_PARITY_CHECK = RUN_DIR / "onnx_refresh_parity_check.csv"
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"
FEATURE_DIR = RUN_DIR / "feature_matrices"
MODEL_DIR = RUN_DIR / "models"
EXPECTED_DIR = RUN_DIR / "expected_probability_tapes"
TELEMETRY_DIR = RUN_DIR / "runtime_telemetry"
ATTEMPT_PACKAGE = RUN_DIR / "top3_runtime_probe_attempt_package.csv"
COMMON_SYNC = RUN_DIR / "common_files_sync.csv"
EXPECTED_INDEX = RUN_DIR / "expected_probability_tape_index.csv"
EXECUTION_RESULT = RUN_DIR / "mt5_execution_result.json"
EXECUTION_SUMMARY = RUN_DIR / "top3_runtime_probe_execution_summary.csv"
RUNTIME_DIFF = RUN_DIR / "runtime_probability_decision_diff.csv"
FINAL_DECISION = RUN_DIR / "mt5_runtime_probe_final.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stage337EP top3 contract refresh and MT5 runtime probe.")
    parser.add_argument("--terminal-path", default=str(el.DEFAULT_TERMINAL))
    parser.add_argument("--common-files-root", default=str(el.DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(el.DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--from-date", default="2026.05.27")
    parser.add_argument("--to-date", default="2026.05.28")
    parser.add_argument("--attempt-limit", type=int, default=7)
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("--wait-timeout-seconds", type=int, default=90)
    parser.add_argument("--materialize-only", action="store_true")
    return parser.parse_args()


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return f"{value:.12g}"
    return str(value)


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fields = list(columns or (rows[0].keys() if rows else ["empty"]))
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: csv_value(row.get(field, "")) for field in fields})
    return path


def write_json(path: Path, payload: Any) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
    return path


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def bool_text(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def copy_common(common_files: Path, local_path: Path, common_path: str) -> dict[str, Any]:
    target = common_files / Path(common_path)
    io_path(target.parent).mkdir(parents=True, exist_ok=True)
    if path_exists(target):
        io_path(target).unlink()
    shutil.copy2(io_path(local_path), io_path(target))
    return {
        "source_path": rel(local_path),
        "target_path": target.as_posix(),
        "exists": path_exists(target),
        "sha256": sha256_file(target) if path_exists(target) else "",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def materialize_top3_weight_contract() -> tuple[pd.DataFrame, dict[str, Any]]:
    base = pd.read_csv(io_path(ROOT / "foundation" / "config" / "top3_monthly_price_proxy_weights_fpmarkets_v2.csv"))
    common = load_common_close_frame(io_path(RAW_ROOT))
    may = compute_monthly_price_proxy_weights(common, PriceProxyWeightSpec(start_month="2026-05", end_month="2026-05"))
    source_ts = pd.Timestamp(may.loc[0, "source_timestamp"])
    no_lookahead = source_ts < pd.Timestamp("2026-05-01T00:00:00Z")
    extended = pd.concat([base.loc[base["month"].astype(str) != "2026-05"], may], ignore_index=True)
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    extended.to_csv(io_path(WEIGHT_CONTRACT), index=False)
    audit = {
        "month": "2026-05",
        "source_timestamp": may.loc[0, "source_timestamp"],
        "source_rule": may.loc[0, "source_rule"],
        "bootstrap_month": bool(may.loc[0, "bootstrap_month"]),
        "weight_sum": float(may.loc[0, "weight_sum"]),
        "no_lookahead_passed": no_lookahead,
        "contract_path": rel(WEIGHT_CONTRACT),
        "contract_sha256": sha256_file(WEIGHT_CONTRACT),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(WEIGHT_AUDIT, [audit])
    return extended, audit


def configure_feature_materializer() -> None:
    bq.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    bq.ASOF_AUDIT_ROWS.clear()
    bq.ASOF_READY_INDEX.clear()
    stage329b.RUN_ID = RUN_ID
    stage329b.RUN_NUMBER = RUN_NUMBER
    stage329b.PARENT_RUN_ID = PARENT_RUN_ID
    stage329b.NEXT_ACTION = NEXT_RUN_ID
    stage329b.STATUS = STATUS
    stage329b.JUDGMENT = JUDGMENT
    stage329b.DECISION = DECISION
    stage329b.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    stage329b.STAGE_ID = STAGE_ID
    stage329b.STAGE_DIR = STAGE_DIR
    stage329b.RUN_DIR = RUN_DIR
    stage329b.FEATURE_FRAME_DIR = FEATURE_FRAME_DIR
    stage329b.FEATURE_ORDER_DIR = FEATURE_ORDER_DIR
    stage329b.FEATURE_SUMMARY_DIR = FEATURE_SUMMARY_DIR
    stage329b.FORWARD_RAW_ROOT = RAW_ROOT
    stage329b.FORWARD_RAW_SUMMARY = RAW_LATEST
    stage329b.FORWARD_REQUESTED_TO_UTC = pd.Timestamp("2026-05-28T06:00:00Z")
    stage329b.COMPUTE_END_UTC = pd.Timestamp("2026-05-28T06:00:00Z")
    stage329b.WEIGHTS_PATH = io_path(WEIGHT_CONTRACT)
    stage329b.COMBINED_RAW_CACHE.clear()
    stage329b.COMBINED_IDENTITY_CACHE.clear()
    stage329b.load_raw_part = bp.load_raw_part_longpath
    stage329b.required_alignment_mask = bq.required_alignment_mask_asof
    stage329b.fp.attach_external_series = bq.attach_external_series_asof
    stage329b.FEATURE_SETS = {
        "macro_equity_lag_safe_rescue": {
            "features": list(stage329b.fp.FEATURE_ORDER),
            "required_symbols": sorted(eo.REQUIRED_RAW_SYMBOLS),
            "role": "exact_survivor_macro58_top3_2026_05_contract_refresh",
        },
        "technical_session_vol_lag_safe": {
            "features": list(eo.TECHNICAL_FEATURES),
            "required_symbols": ["US100"],
            "role": "exact_survivor_technical42_refresh_control",
        },
    }


def materialize_feature_sets() -> tuple[list[dict[str, Any]], list[Path]]:
    configure_feature_materializer()
    for directory in [RUN_DIR, FEATURE_FRAME_DIR, FEATURE_ORDER_DIR, FEATURE_SUMMARY_DIR]:
        io_path(directory).mkdir(parents=True, exist_ok=True)
    summaries, missing, invalid, artifacts, _counts = stage329b.build_feature_frames()
    clean = [dict(row, join_policy="backward_asof_no_lookahead", claim_boundary=CLAIM_BOUNDARY) for row in summaries]
    write_csv(
        FEATURE_SET_SUMMARY,
        clean,
        [
            "feature_set_id",
            "role",
            "join_policy",
            "feature_count",
            "feature_order_sha256",
            "scope_rows",
            "valid_rows",
            "invalid_rows",
            "alignment_missing_rows",
            "finite_missing_rows",
            "first_valid_timestamp",
            "last_valid_timestamp",
            "status",
            "parquet_path",
            "parquet_sha256",
            "feature_order_path",
            "feature_order_sha256_file",
            "claim_boundary",
        ],
    )
    write_csv(MISSING_FEATURE_COUNTS, [dict(row, claim_boundary=CLAIM_BOUNDARY) for row in missing], ["feature_set_id", "feature", "missing_or_nonfinite_rows", "claim_boundary"])
    write_csv(INVALID_ROW_SAMPLES, [dict(row, claim_boundary=CLAIM_BOUNDARY) for row in invalid], ["feature_set_id", "timestamp", "alignment_ready", "finite_ready", "claim_boundary"])
    write_csv(
        ASOF_SOURCE_LAG_SUMMARY,
        bq.ASOF_AUDIT_ROWS,
        [
            "contract_symbol",
            "source_group",
            "feature_role",
            "target_rows",
            "ready_rows",
            "missing_rows",
            "max_lag_minutes",
            "p95_lag_minutes",
            "last_source_timestamp",
            "last_target_timestamp_with_source",
            "tolerance_hours",
            "lookahead_violations",
            "claim_boundary",
        ],
    )
    return clean, artifacts


def score_survivors() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    eo.FEATURE_FRAME_DIR = FEATURE_FRAME_DIR
    eo.FEATURE_ORDER_DIR = FEATURE_ORDER_DIR
    eo.FEATURE_SUMMARY_DIR = FEATURE_SUMMARY_DIR
    eo.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    refresh, surface, chunks, parity = eo.score_survivors(7)
    write_csv(FEATURE_REFRESH_AUDIT, refresh)
    write_csv(SURFACE_REPROBE, surface)
    write_csv(SURFACE_CHUNKS, chunks)
    write_csv(ONNX_PARITY_CHECK, parity)
    return refresh, surface, chunks, parity


def compare_runtime(attempt: Mapping[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    telemetry_path = TELEMETRY_DIR / Path(str(attempt["common_telemetry_path"])).name
    summary_path = TELEMETRY_DIR / Path(str(attempt["common_summary_path"])).name
    if not path_exists(telemetry_path):
        return {
            "attempt_name": attempt["attempt_name"],
            "probe_id": attempt["probe_id"],
            "model_id": attempt["model_id"],
            "runtime_status": "blocked_telemetry_missing",
            "matched_rows": 0,
            "probability_mismatch_rows": 0,
            "decision_mismatch_rows": 0,
            "comparison_status": "blocked_telemetry_missing",
            "claim_boundary": CLAIM_BOUNDARY,
        }, []
    telemetry = pd.read_csv(io_path(telemetry_path))
    cycles = telemetry.loc[telemetry["record_type"].astype(str).eq("cycle")].copy()
    ready = cycles.loc[cycles["feature_ready"].map(bool_text) & cycles["model_ok"].map(bool_text)].copy()
    expected = pd.read_csv(io_path(ROOT / str(attempt["expected_probability_tape_path"]))).set_index("bar_time")
    rows: list[dict[str, Any]] = []
    matched = expected_missing = probability_mismatch = decision_mismatch = 0
    max_abs = 0.0
    for row in ready.to_dict("records"):
        bar_time = str(row.get("bar_time", ""))
        if bar_time not in expected.index:
            expected_missing += 1
            continue
        exp = expected.loc[bar_time]
        if isinstance(exp, pd.DataFrame):
            exp = exp.iloc[0]
        abs_diff = max(abs(float(row.get(f"p_{label}", 0.0)) - float(exp[f"p_{label}"])) for label in ["short", "flat", "long"])
        max_abs = max(max_abs, abs_diff)
        runtime_decision = str(row.get("decision", "")).lower()
        expected_decision = str(exp["decision"]).lower()
        matched += 1
        if abs_diff > 1e-5:
            probability_mismatch += 1
        if runtime_decision != expected_decision:
            decision_mismatch += 1
        if abs_diff > 1e-5 or runtime_decision != expected_decision:
            rows.append(
                {
                    "attempt_name": attempt["attempt_name"],
                    "bar_time": bar_time,
                    "expected_decision": expected_decision,
                    "runtime_decision": runtime_decision,
                    "max_abs_probability_diff": abs_diff,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    out = {
        "attempt_name": attempt["attempt_name"],
        "probe_id": attempt["probe_id"],
        "model_id": attempt["model_id"],
        "runtime_status": "completed",
        "telemetry_cycle_rows": int(len(cycles)),
        "ready_model_rows": int(len(ready)),
        "matched_rows": matched,
        "expected_missing_rows": expected_missing,
        "probability_mismatch_rows": probability_mismatch,
        "decision_mismatch_rows": decision_mismatch,
        "max_abs_probability_diff": max_abs,
        "first_ready_bar_time": str(ready["bar_time"].iloc[0]) if len(ready) else "",
        "last_ready_bar_time": str(ready["bar_time"].iloc[-1]) if len(ready) else "",
        "comparison_status": "matched" if matched > 0 and expected_missing == 0 and probability_mismatch == 0 and decision_mismatch == 0 else "mismatch_or_blocked",
        "common_telemetry_path": attempt["common_telemetry_path"],
        "local_telemetry_path": rel(telemetry_path),
        "local_summary_path": rel(summary_path) if path_exists(summary_path) else "",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    if path_exists(summary_path):
        summary = pd.read_csv(io_path(summary_path))
        if len(summary):
            last = summary.iloc[-1].to_dict()
            for key in ["feature_ready_count", "model_ok_count", "long_count", "short_count", "flat_count", "order_attempt_count", "order_fill_count"]:
                out[key] = last.get(key, "")
    return out, rows


def runtime_probe(args: argparse.Namespace) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    common_files = Path(args.common_files_root)
    tester_profile = Path(args.tester_profile_root)
    common_root = "Project_Obsidian_Prime_v2/stage337/run337EP_top3_runtime_probe"
    attempts: list[dict[str, Any]] = []
    sync_rows: list[dict[str, Any]] = []
    expected_rows: list[dict[str, Any]] = []
    for directory in [MT5_DIR, SET_DIR, INI_DIR, FEATURE_DIR, MODEL_DIR, EXPECTED_DIR, TELEMETRY_DIR]:
        io_path(directory).mkdir(parents=True, exist_ok=True)
    for base in el.selected_attempts(args.attempt_limit):
        feature_order = eo.load_feature_order(str(base["feature_set_id"]))
        frame = pd.read_parquet(io_path(FEATURE_FRAME_DIR / f"{base['feature_set_id']}.parquet"))
        frame = el.date_filter(frame, args.from_date, args.to_date)
        local_features = FEATURE_DIR / f"{base['attempt_name']}_features.csv"
        local_model = MODEL_DIR / f"{base['attempt_name']}.onnx"
        expected_tape = EXPECTED_DIR / f"{base['attempt_name']}_expected_probability_tape.csv"
        mt5.export_mt5_feature_matrix_csv(frame, feature_order, local_features, timestamp_column="timestamp", metadata_columns=("split",))
        shutil.copy2(io_path(Path(base["onnx_path"])), io_path(local_model))
        expected_rows.append(el.write_expected_probability_tape(base, frame, feature_order, expected_tape))
        common_feature_path = f"{common_root}/features/{local_features.name}"
        common_model_path = f"{common_root}/models/{local_model.name}"
        common_telemetry_path = f"{common_root}/telemetry/{base['attempt_name']}_telemetry.csv"
        common_summary_path = f"{common_root}/telemetry/{base['attempt_name']}_summary.csv"
        for old_path in [common_telemetry_path, common_summary_path]:
            target = common_files / Path(old_path)
            if path_exists(target):
                io_path(target).unlink()
        sync_rows.append({"sync_id": f"{base['attempt_name']}::features", **copy_common(common_files, local_features, common_feature_path)})
        sync_rows.append({"sync_id": f"{base['attempt_name']}::model", **copy_common(common_files, local_model, common_model_path)})
        set_name = f"opv2_{RUN_NUMBER}_{base['probe_id']}.set"
        ini_name = f"opv2_{RUN_NUMBER}_{base['probe_id']}.ini"
        set_path = SET_DIR / f"{base['attempt_name']}.set"
        ini_path = INI_DIR / f"{base['attempt_name']}.ini"
        params = {
            "InpRunId": f"{RUN_ID}_{base['attempt_name']}",
            "InpExplorationLabel": "stage337_Top3RefreshedRuntimeProbe",
            "InpTierLabel": "Tier A",
            "InpPrimaryActiveTier": "tier_a",
            "InpSplitLabel": "top3_refreshed_forward_probe",
            "InpMainSymbol": "US100",
            "InpTimeframe": 5,
            "InpEnforceM5": True,
            "InpFeatureCsvPath": common_feature_path,
            "InpFeatureCount": int(base["feature_count"]),
            "InpFeatureCsvUseCommonFiles": True,
            "InpFeatureRequireTimestampMatch": True,
            "InpFeatureAllowLatestFallback": False,
            "InpFeatureStrictHeader": True,
            "InpFeatureCsvDelimiter": ",",
            "InpCsvTimestampIsBarClose": True,
            "InpModelPath": common_model_path,
            "InpModelId": base["model_id"],
            "InpModelBackend": "onnx",
            "InpModelUseCommonFiles": True,
            "InpModelUseCpuOnly": True,
            "InpModelNoConversion": False,
            "InpSetOutputShape": True,
            "InpFeatureOrderHash": base["feature_order_hash"],
            "InpFallbackEnabled": False,
            "InpShortThreshold": 0.55,
            "InpLongThreshold": 0.55,
            "InpMinMargin": 0.05,
            "InpDecisionMode": "argmax_probe",
            "InpInvertSignal": False,
            "InpSideFilterEnabled": False,
            "InpAllowTrading": False,
            "InpFixedLot": 0.10,
            "InpMagic": 3371300 + int(base["proxy_rank"]),
            "InpCloseOnFlatSignal": False,
            "InpReverseOnOppositeSignal": True,
            "InpMaxHoldBars": 12,
            "InpMaxConcurrentPositions": 1,
            "InpAtrSltpEnabled": False,
            "InpModelRiskSizingEnabled": False,
            "InpTelemetryEnabled": True,
            "InpTelemetryUseCommonFiles": True,
            "InpTelemetryCsvPath": common_telemetry_path,
            "InpSummaryCsvPath": common_summary_path,
        }
        mt5.materialize_tester_set_file(params, set_path, generated_by="stage337EP_top3_runtime_probe")
        mt5.materialize_tester_ini_file(
            mt5.TesterMaterializationConfig(
                expert=mt5.EA_EXPERT_PATH,
                symbol="US100",
                period="M5",
                model=4,
                deposit=500.0,
                leverage="1:100",
                shutdown_terminal=1,
                from_date=args.from_date,
                to_date=args.to_date,
                report=f"Project_Obsidian_Prime_v2_{RUN_NUMBER}_{base['attempt_name']}",
            ),
            ini_path,
            set_file_path=Path(set_name),
        )
        attempts.append(
            {
                **base,
                "expected_probability_tape_path": rel(expected_tape),
                "common_telemetry_path": common_telemetry_path,
                "common_summary_path": common_summary_path,
                "set_path": rel(set_path),
                "ini_path": rel(ini_path),
                "set_name": set_name,
                "ini_name": ini_name,
                "from_date": args.from_date,
                "to_date": args.to_date,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(ATTEMPT_PACKAGE, attempts)
    write_csv(COMMON_SYNC, sync_rows)
    write_csv(EXPECTED_INDEX, expected_rows)

    execution: list[dict[str, Any]] = []
    summaries: list[dict[str, Any]] = []
    diffs: list[dict[str, Any]] = []
    for attempt in attempts:
        if args.materialize_only:
            summary = {
                "attempt_name": attempt["attempt_name"],
                "probe_id": attempt["probe_id"],
                "model_id": attempt["model_id"],
                "runtime_status": "not_run",
                "comparison_status": "materialize_only",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        else:
            try:
                result = mt5.run_mt5_tester(
                    Path(args.terminal_path),
                    ROOT / str(attempt["ini_path"]),
                    set_path=ROOT / str(attempt["set_path"]),
                    tester_profile_set_path=tester_profile / str(attempt["set_name"]),
                    tester_profile_ini_path=tester_profile / str(attempt["ini_name"]),
                    timeout_seconds=args.timeout_seconds,
                )
            except subprocess.TimeoutExpired as exc:
                result = {"status": "blocked", "returncode": None, "blocker": "terminal_timeout", "stdout": str(exc.stdout)[-1000:], "stderr": str(exc.stderr)[-1000:]}
            wait = mt5.wait_for_mt5_runtime_outputs(common_files, attempt, timeout_seconds=args.wait_timeout_seconds, poll_seconds=2.0)
            telemetry_common = common_files / Path(str(attempt["common_telemetry_path"]))
            summary_common = common_files / Path(str(attempt["common_summary_path"]))
            if path_exists(telemetry_common):
                shutil.copy2(io_path(telemetry_common), io_path(TELEMETRY_DIR / telemetry_common.name))
            if path_exists(summary_common):
                shutil.copy2(io_path(summary_common), io_path(TELEMETRY_DIR / summary_common.name))
            summary, new_diffs = compare_runtime(attempt)
            summary["tester_status"] = result.get("status", "")
            summary["returncode"] = result.get("returncode", "")
            summary["blocker"] = result.get("blocker", "")
            execution.append({"attempt_name": attempt["attempt_name"], "tester": result, "runtime_wait": wait})
            diffs.extend(new_diffs)
        summaries.append(summary)
    write_json(EXECUTION_RESULT, execution)
    write_csv(EXECUTION_SUMMARY, summaries)
    write_csv(RUNTIME_DIFF, diffs, ["attempt_name", "bar_time", "expected_decision", "runtime_decision", "max_abs_probability_diff", "claim_boundary"])
    return attempts, summaries


def main() -> int:
    args = parse_args()
    materialize_top3_weight_contract()
    feature_summaries, feature_artifacts = materialize_feature_sets()
    _refresh, surface, _chunks, parity = score_survivors()
    attempts, runtime_rows = runtime_probe(args)
    final = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "feature_sets": len(feature_summaries),
        "surface_rows": len(surface),
        "surface_nonflat_rows": sum(int(row.get("decision_nonflat_total", 0) or 0) for row in surface),
        "onnx_parity_failed_rows": sum(1 for row in parity if row.get("parity_status") != "passed"),
        "attempt_rows": len(attempts),
        "matched_rows": sum(int(row.get("matched_rows", 0) or 0) for row in runtime_rows),
        "probability_mismatch_rows": sum(int(row.get("probability_mismatch_rows", 0) or 0) for row in runtime_rows),
        "decision_mismatch_rows": sum(int(row.get("decision_mismatch_rows", 0) or 0) for row in runtime_rows),
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(FINAL_DECISION, final)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "inputs": [rel(RAW_ROOT), rel(eo.FINAL_DECISION)],
            "outputs": [
                rel(path)
                for path in [
                    WEIGHT_CONTRACT,
                    WEIGHT_AUDIT,
                    FEATURE_SET_SUMMARY,
                    SURFACE_REPROBE,
                    ONNX_PARITY_CHECK,
                    EXECUTION_SUMMARY,
                    RUNTIME_DIFF,
                    FINAL_DECISION,
                    RUN_MANIFEST,
                    *feature_artifacts,
                ]
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    print(json.dumps(final, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
