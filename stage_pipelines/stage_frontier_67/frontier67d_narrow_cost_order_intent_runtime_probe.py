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
from typing import Any, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.control_plane.mt5_tier_balance_completion import attempt_payload
from foundation.mt5 import runtime_support as mt5
from stage_pipelines.stage_frontier_67.frontier67c_runtime_native_order_intent_economics import (
    as_float,
    as_int,
    extract_deal_metrics,
    ratio,
)
from stage_pipelines.stage_frontier_runtime_backfill.run_frontier_runtime_probe_backfill import (
    DEFAULT_COMMON_FILES,
    DEFAULT_METAEDITOR,
    DEFAULT_PORTABLE_ROOT,
    DEFAULT_TERMINAL,
    DEFAULT_TESTER_PROFILE_ROOT,
    EA_BINARY,
    PORTABLE_EA_BINARY,
)


STAGE_ID = "stage_frontier_67__count_parity_not_pnl_parity_runtime_economics_crosswalk"
RUN_ID = "frontier67D_narrow_cost_order_intent_runtime_probe_v1"
F66_STAGE_ID = "stage_frontier_66__runtime_probe_backfill_gap_audit_frontier02_to_64"
F66_RUN_ID = "frontier66C_proxy_signal_mt5_backfill_v1"

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
COMMON_RUN_ROOT = "Project_Obsidian_Prime_v2/frontier67D_narrow_cost_order_intent_runtime_probe"

F66_RUN_ROOT = ROOT / "stages" / F66_STAGE_ID / "02_runs" / F66_RUN_ID
F66_ATTEMPTS_JSON = F66_RUN_ROOT / "frontier66_proxy_signal_mt5_attempts.json"
F67A_ROWS = REVIEWS_ROOT / "frontier67A_dd_basis_crosswalk_rows_review.csv"
F67B_ROWS = REVIEWS_ROOT / "frontier67B_config_parity_rows_review.csv"
F67C_ROWS = REVIEWS_ROOT / "frontier67C_runtime_native_order_intent_rows_review.csv"
GROK_PACKET_ROOT = ROOT / "docs/agent_control/grok_reviews/2026-06-16_f67d_pre_mt5_cost_order_intent_runtime_probe"

ATTEMPT_NAME = "f67d_f31_f31b_0013_oos_order_intent"
SELECTED_STAGE_NUM = "31"
SELECTED_SPLIT = "oos"

CLAIM_BOUNDARY = (
    "runtime_probe_observation_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="F67D narrow cost/order-intent MT5 runtime probe.")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--wait-timeout-seconds", type=int, default=240)
    parser.add_argument("--terminal-path", default=str(DEFAULT_TERMINAL))
    parser.add_argument("--metaeditor-path", default=str(DEFAULT_METAEDITOR))
    parser.add_argument("--common-files-root", default=str(DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(DEFAULT_PORTABLE_ROOT))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ensure_dirs()
    created_at = utc_now()
    source_attempt = select_source_attempt()
    anchors = selected_anchor_rows()
    attempt = materialize_attempt(source_attempt, anchors, Path(args.common_files_root))
    local_verification = build_local_verification(created_at, source_attempt, attempt, anchors)
    write_json(RUN_ROOT / "frontier67D_local_verification.json", local_verification)
    write_json(RUN_ROOT / "frontier67D_mt5_attempt.json", attempt)

    execution_payload: dict[str, Any] = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "source_attempt_name": source_attempt.get("attempt_name"),
        "selected_stage_num": SELECTED_STAGE_NUM,
        "selected_split": SELECTED_SPLIT,
        "grok_packet": grok_identity(),
        "local_verification": local_verification,
        "attempts": [attempt],
        "execution_results": [],
        "strategy_tester_reports": [],
        "mt5_kpi_records": [],
        "order_intent_receipt": [],
        "gap_classification": [],
    }

    if args.materialize_only or not args.execute:
        execution_payload["status"] = "materialized_pending_mt5"
        write_outputs(execution_payload, created_at)
        print(json.dumps(json_ready({"status": execution_payload["status"], "attempt": ATTEMPT_NAME}), ensure_ascii=False, indent=2))
        return 0

    compile_payload = compile_runtime_ea(Path(args.metaeditor_path))
    execution_payload["compile_payload"] = compile_payload
    result = execute_attempt(args, attempt, compile_payload)
    report_records = mt5.collect_mt5_strategy_report_artifacts(
        terminal_data_root=Path(args.terminal_data_root),
        run_output_root=RUN_ROOT,
        attempts=[attempt],
        run_id=RUN_ID,
    )
    execution_results = [result]
    mt5.attach_mt5_report_metrics(execution_results, report_records)
    kpi_records = mt5.build_mt5_kpi_records(execution_results)
    receipt_rows = build_order_intent_receipt(execution_results[0], attempt, anchors)
    gap_rows = build_gap_classification(receipt_rows[0] if receipt_rows else {}, anchors)

    execution_payload.update(
        {
            "status": runtime_status(execution_results, report_records, receipt_rows),
            "execution_results": execution_results,
            "strategy_tester_reports": report_records,
            "mt5_kpi_records": kpi_records,
            "order_intent_receipt": receipt_rows,
            "gap_classification": gap_rows,
        }
    )
    write_outputs(execution_payload, created_at)
    print(
        json.dumps(
            json_ready(
                {
                    "status": execution_payload["status"],
                    "attempt": ATTEMPT_NAME,
                    "tester_status": result.get("status"),
                    "runtime_status": (result.get("runtime_outputs") or {}).get("status"),
                    "report_status": report_records[0].get("status") if report_records else "missing",
                    "order_intent_rows": len(receipt_rows),
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def ensure_dirs() -> None:
    for path in (
        RUN_ROOT,
        RUN_ROOT / "models",
        RUN_ROOT / "features",
        RUN_ROOT / "mt5",
        RUN_ROOT / "mt5" / "reports",
        REVIEWS_ROOT,
    ):
        io_path(path).mkdir(parents=True, exist_ok=True)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2), encoding="utf-8")


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: json_ready(row.get(key, "")) for key in columns})


def write_md(path: Path, lines: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text("\n".join(lines) + "\n", encoding="utf-8-sig")


def select_source_attempt() -> dict[str, Any]:
    attempts = read_json(F66_ATTEMPTS_JSON)
    for attempt in attempts:
        if str(attempt.get("stage_num")) == SELECTED_STAGE_NUM and str(attempt.get("split")) == SELECTED_SPLIT:
            return dict(attempt)
    raise RuntimeError("selected F31 OOS source attempt missing(선택된 F31 표본외 원천 시도 누락)")


def selected_anchor_rows() -> dict[str, dict[str, str]]:
    anchors: dict[str, dict[str, str]] = {}
    for name, path in (("f67a", F67A_ROWS), ("f67b", F67B_ROWS), ("f67c", F67C_ROWS)):
        for row in read_csv(path):
            if str(row.get("stage_num")) == SELECTED_STAGE_NUM and str(row.get("split")) == SELECTED_SPLIT:
                anchors[name] = row
                break
        if name not in anchors:
            raise RuntimeError(f"{name} anchor row missing({name} 기준 행 누락)")
    return anchors


def materialize_attempt(source_attempt: Mapping[str, Any], anchors: Mapping[str, Mapping[str, str]], common_files_root: Path) -> dict[str, Any]:
    model_payload = dict(source_attempt.get("model_payload") or {})
    feature_payload = dict(source_attempt.get("feature_payload") or {})
    model_local = copy_run_artifact(Path(str(model_payload["path"])), RUN_ROOT / "models" / Path(str(model_payload["path"])).name)
    feature_local = copy_run_artifact(Path(str(feature_payload["path"])), RUN_ROOT / "features" / Path(str(feature_payload["path"])).name)
    model_common = f"{COMMON_RUN_ROOT}/models/{model_local.name}"
    feature_common = f"{COMMON_RUN_ROOT}/features/{feature_local.name}"
    model_common_payload = mt5.copy_to_common_files(common_files_root, model_local, model_common)
    feature_common_payload = mt5.copy_to_common_files(common_files_root, feature_local, feature_common)

    extra_set_values = dict(source_attempt.get("extra_set_values") or {})
    execution_policy = dict(source_attempt.get("execution_policy") or {})
    attempt = attempt_payload(
        run_root=RUN_ROOT,
        run_id=RUN_ID,
        stage_number=67,
        exploration_label="frontier67D_narrow_cost_order_intent_runtime_probe(F67D 좁은 비용/주문 의도 런타임 탐침)",
        attempt_name=ATTEMPT_NAME,
        tier=str(source_attempt.get("tier") or mt5.TIER_A),
        split=SELECTED_SPLIT,
        model_path=model_common,
        model_id=f"F67D_{model_payload.get('physical_artifact_tag', 'F31')}_signal_table",
        model_backend=str(source_attempt.get("model_payload", {}).get("format", "") and "ebm_table"),
        feature_path=feature_common,
        feature_count=int(feature_payload.get("feature_count") or 1),
        feature_order_hash=str(feature_payload.get("feature_order_hash") or ""),
        short_threshold=0.0,
        long_threshold=0.0,
        min_margin=0.0,
        invert_signal=False,
        from_date=str((source_attempt.get("ini") or {}).get("tester", {}).get("FromDate")),
        to_date=str((source_attempt.get("ini") or {}).get("tester", {}).get("ToDate")),
        primary_active_tier=str(source_attempt.get("tier") or mt5.TIER_A),
        attempt_role="frontier67d_narrow_cost_order_intent_runtime_probe",
        record_view_prefix="mt5_f67d_f31_f31b_0013_oos",
        max_hold_bars=int(source_attempt.get("max_hold_bars") or anchors["f67b"].get("max_hold_bars") or 12),
        common_root=COMMON_RUN_ROOT,
        close_on_flat_signal=bool(execution_policy.get("close_on_flat_signal", False)),
        reverse_on_opposite_signal=bool(execution_policy.get("reverse_on_opposite_signal", False)),
        close_only_on_opposite_signal=bool(execution_policy.get("close_only_on_opposite_signal", False)),
        extra_set_values=extra_set_values,
    )
    attempt.update(
        {
            "stage_num": int(SELECTED_STAGE_NUM),
            "stage_id": source_attempt.get("stage_id"),
            "candidate_id": source_attempt.get("candidate_id"),
            "source_attempt_name": source_attempt.get("attempt_name"),
            "source_run_id": F66_RUN_ID,
            "selected_anchor": {
                "selection_reason": (
                    "dominant_trade_shape_hold12_atr_1_1_plus_meaningful_dd_gap_and_order_fill_deal_mismatch"
                ),
                "f67a": dict(anchors["f67a"]),
                "f67b": dict(anchors["f67b"]),
                "f67c": dict(anchors["f67c"]),
            },
            "model_payload": {
                **model_payload,
                "path": model_local.as_posix(),
                "common_copy": model_common_payload,
            },
            "feature_payload": {
                **feature_payload,
                "path": feature_local.as_posix(),
                "common_copy": feature_common_payload,
            },
            "expected_signal_count": as_int(source_attempt.get("expected_signal_count")),
            "expected_long_count": as_int(source_attempt.get("expected_long_count")),
            "expected_short_count": as_int(source_attempt.get("expected_short_count")),
            "expected_rows": as_int(source_attempt.get("expected_rows")),
            "cost_identity_plan": cost_identity_plan(anchors["f67b"]),
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    return attempt


def copy_run_artifact(source: Path, destination: Path) -> Path:
    if not path_exists(source):
        raise FileNotFoundError(source.as_posix())
    io_path(destination.parent).mkdir(parents=True, exist_ok=True)
    shutil.copy2(io_path(source), io_path(destination))
    return destination


def cost_identity_plan(config_row: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "config_spread_identity": config_row.get("spread_identity") or "missing",
        "config_commission_identity": config_row.get("commission_identity") or "missing",
        "config_slippage_identity": config_row.get("slippage_identity") or "missing",
        "config_swap_identity": config_row.get("swap_identity") or "missing",
        "source": "f67b_config_parity_rows_review",
        "verification_note": (
            "cost identity must be recorded from config where present, and from tester report/deal table as observation where config is missing"
        ),
    }


def grok_identity() -> dict[str, Any]:
    prompt = GROK_PACKET_ROOT / "prompts" / "prompt.md"
    clean_output = GROK_PACKET_ROOT / "outputs" / "clean_output.md"
    metadata = GROK_PACKET_ROOT / "outputs" / "metadata.json"
    return {
        "packet_root": rel(GROK_PACKET_ROOT),
        "prompt_path": rel(prompt),
        "clean_output_path": rel(clean_output),
        "metadata_path": rel(metadata),
        "prompt_exists": path_exists(prompt),
        "clean_output_exists": path_exists(clean_output),
        "metadata_exists": path_exists(metadata),
    }


def build_local_verification(
    created_at: str,
    source_attempt: Mapping[str, Any],
    attempt: Mapping[str, Any],
    anchors: Mapping[str, Mapping[str, str]],
) -> dict[str, Any]:
    f67a = anchors["f67a"]
    f67c = anchors["f67c"]
    checks = {
        "grok_pre_mt5_review_exists": path_exists(GROK_PACKET_ROOT / "outputs" / "clean_output.md"),
        "selected_source_attempt_exists": bool(source_attempt),
        "selected_row_is_f31_oos": str(f67a.get("stage_num")) == SELECTED_STAGE_NUM and str(f67a.get("split")) == SELECTED_SPLIT,
        "model_copy_exists": path_exists(ROOT / str(attempt["model_payload"]["path"])),
        "feature_copy_exists": path_exists(ROOT / str(attempt["feature_payload"]["path"])),
        "set_file_exists": path_exists(ROOT / str(attempt["set"]["path"])),
        "ini_file_exists": path_exists(ROOT / str(attempt["ini"]["path"])),
        "meaningful_dd_gap": (as_float(f67a.get("dd_delta_runtime_minus_proxy")) or 0.0) > 10.0,
        "order_fill_deal_mismatch_present": (as_int(f67c.get("deal_minus_order_fill")) or 0) > 0,
    }
    return {
        "created_at_utc": created_at,
        "selected_slice": "F31_oos",
        "advice_classification": {
            "accepted": [
                "explicit_cost_identity_block",
                "order_intent_receipt_schema",
                "accounting_parity_sheet",
                "economics_decomposition_template",
                "narrow_selection_rule_one_trade_shape",
                "frozen_comparison_anchor",
                "swap_commission_cross_check",
            ],
            "rejected": [
                "pf_dd_optimization_in_f67d",
                "full_64_row_replay_in_f67d",
                "runtime_authority_or_closeout_claim_from_f67d_alone",
            ],
            "needs_local_verification": [
                "row_selection",
                "manifest_paths",
                "actual_tester_settings",
            ],
        },
        "checks": checks,
        "passed": all(checks.values()),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def compile_runtime_ea(metaeditor_path: Path) -> dict[str, Any]:
    compile_payload = mt5.compile_mql5_ea(metaeditor_path, mt5.EA_SOURCE_PATH, RUN_ROOT / "mt5" / "mt5_compile.log")
    portable_payload = {
        "repo_ea_ex5": EA_BINARY.as_posix(),
        "portable_ea_ex5": PORTABLE_EA_BINARY.as_posix(),
        "portable_ea_ex5_exists_before": path_exists(PORTABLE_EA_BINARY),
        "copied": False,
    }
    if path_exists(EA_BINARY):
        io_path(PORTABLE_EA_BINARY.parent).mkdir(parents=True, exist_ok=True)
        shutil.copy2(io_path(EA_BINARY), io_path(PORTABLE_EA_BINARY))
        portable_payload["copied"] = True
        portable_payload["portable_ea_ex5_exists_after"] = path_exists(PORTABLE_EA_BINARY)
        portable_payload["portable_ea_sha256"] = mt5.sha256_file(PORTABLE_EA_BINARY)
    return {"compile": compile_payload, "portable_ea": portable_payload}


def execute_attempt(args: argparse.Namespace, attempt: Mapping[str, Any], compile_payload: Mapping[str, Any]) -> dict[str, Any]:
    result: dict[str, Any]
    if not can_run_terminal(compile_payload):
        result = blocked_result(attempt, "compile_failed_and_portable_ea_missing")
    else:
        clear_runtime_outputs(Path(args.common_files_root), attempt)
        mt5.remove_existing_mt5_report_artifacts(Path(args.terminal_data_root), attempt, run_id=RUN_ID)
        try:
            result = mt5.run_mt5_tester(
                Path(args.terminal_path),
                ROOT / str(attempt["ini"]["path"]),
                set_path=ROOT / str(attempt["set"]["path"]),
                tester_profile_set_path=Path(args.tester_profile_root) / mt5.EA_TESTER_SET_NAME,
                tester_profile_ini_path=Path(args.tester_profile_root) / f"opv2_{attempt['attempt_name']}.ini",
                timeout_seconds=int(args.timeout_seconds),
                terminal_extra_args=["/portable"],
            )
        except subprocess.TimeoutExpired as exc:
            result = {
                "status": "blocked",
                "command": exc.cmd,
                "returncode": None,
                "stdout": (exc.stdout or "")[-2000:],
                "stderr": (exc.stderr or "")[-2000:],
                "blocker": "terminal_timeout",
            }
        runtime_outputs = mt5.wait_for_mt5_runtime_outputs(
            Path(args.common_files_root),
            attempt,
            timeout_seconds=int(args.wait_timeout_seconds),
            poll_seconds=2.0,
        )
        if runtime_outputs.get("status") != "completed":
            result["status"] = "blocked"
            result.setdefault("blocker", "runtime_outputs_missing_or_init_failed")
        result["runtime_outputs"] = runtime_outputs
    result.update(
        {
            "attempt_name": attempt["attempt_name"],
            "tier": attempt["tier"],
            "split": attempt["split"],
            "attempt_role": attempt.get("attempt_role"),
            "record_view_prefix": attempt.get("record_view_prefix"),
            "stage_num": attempt.get("stage_num"),
            "stage_id": attempt.get("stage_id"),
            "candidate_id": attempt.get("candidate_id"),
            "expected_signal_count": attempt.get("expected_signal_count"),
            "expected_rows": attempt.get("expected_rows"),
        }
    )
    write_json(RUN_ROOT / "mt5" / f"{attempt['attempt_name']}_tester_execution.json", result)
    return result


def can_run_terminal(compile_payload: Mapping[str, Any]) -> bool:
    compile_status = (compile_payload.get("compile") or {}).get("status")
    return compile_status == "completed" or path_exists(PORTABLE_EA_BINARY)


def blocked_result(attempt: Mapping[str, Any], blocker: str) -> dict[str, Any]:
    return {
        "status": "blocked",
        "blocker": blocker,
        "attempt_name": attempt["attempt_name"],
        "tier": attempt["tier"],
        "split": attempt["split"],
        "attempt_role": attempt.get("attempt_role"),
        "record_view_prefix": attempt.get("record_view_prefix"),
        "stage_num": attempt.get("stage_num"),
        "stage_id": attempt.get("stage_id"),
        "candidate_id": attempt.get("candidate_id"),
    }


def clear_runtime_outputs(common_root: Path, attempt: Mapping[str, Any]) -> None:
    for key in ("common_telemetry_path", "common_summary_path"):
        value = str(attempt.get(key, "")).strip()
        if not value:
            continue
        path = common_root / Path(value)
        if path_exists(path):
            io_path(path).unlink()


def build_order_intent_receipt(
    result: Mapping[str, Any],
    attempt: Mapping[str, Any],
    anchors: Mapping[str, Mapping[str, str]],
) -> list[dict[str, Any]]:
    runtime = result.get("runtime_outputs", {}) if isinstance(result.get("runtime_outputs"), Mapping) else {}
    last = runtime.get("last_summary", {}) if isinstance(runtime.get("last_summary"), Mapping) else {}
    report = result.get("strategy_tester_report", {}) if isinstance(result.get("strategy_tester_report"), Mapping) else {}
    metrics = report.get("metrics", {}) if isinstance(report.get("metrics"), Mapping) else {}
    report_path = Path(str((report.get("html_report") or {}).get("path", "")))
    deal_metrics = extract_deal_metrics(ROOT / report_path) if report_path and path_exists(ROOT / report_path) else empty_deal_metrics()

    long_count = as_int(last.get("long_count")) or 0
    short_count = as_int(last.get("short_count")) or 0
    signal_count = long_count + short_count
    order_attempt_count = as_int(last.get("order_attempt_count")) or 0
    order_fill_count = as_int(last.get("order_fill_count")) or 0
    trade_count = as_int(metrics.get("trade_count")) or 0
    deal_count = as_int(metrics.get("deal_count")) or int(deal_metrics["deal_row_count"])
    winning_trade_count = as_int(metrics.get("winning_trade_count")) or 0
    losing_trade_count = as_int(metrics.get("losing_trade_count")) or 0
    gross_profit = as_float(metrics.get("gross_profit"))
    gross_loss = as_float(metrics.get("gross_loss"))
    average_win = as_float(metrics.get("average_win"))
    if average_win is None and winning_trade_count and gross_profit is not None:
        average_win = gross_profit / winning_trade_count
    average_loss = as_float(metrics.get("average_loss"))
    if average_loss is None and losing_trade_count and gross_loss is not None:
        average_loss = gross_loss / losing_trade_count
    payoff_ratio = as_float(metrics.get("payoff_ratio"))
    if payoff_ratio is None and average_win is not None and average_loss not in (None, 0):
        payoff_ratio = abs(average_win / average_loss)
    test_period = tester_period(attempt)
    trades_per_day = ratio(trade_count, test_period.get("calendar_days_exclusive"))
    proxy_dd = as_float(anchors["f67a"].get("proxy_dd"))
    runtime_dd = as_float(metrics.get("max_drawdown_percent"))
    proxy_pf = as_float((attempt.get("selected_anchor") or {}).get("f67c", {}).get("profit_factor"))
    row = {
        "run_id": RUN_ID,
        "attempt_name": attempt.get("attempt_name"),
        "stage_num": attempt.get("stage_num"),
        "stage_id": attempt.get("stage_id"),
        "candidate_id": attempt.get("candidate_id"),
        "split": attempt.get("split"),
        "test_period_start": test_period.get("start"),
        "test_period_end": test_period.get("end"),
        "calendar_days_exclusive": test_period.get("calendar_days_exclusive"),
        "tester_status": result.get("status"),
        "runtime_status": runtime.get("status", "missing"),
        "report_status": report.get("status", "missing"),
        "expected_rows": attempt.get("expected_rows"),
        "feature_ready_count": as_int(last.get("feature_ready_count")) or 0,
        "feature_ready_diff": (as_int(last.get("feature_ready_count")) or 0) - int(attempt.get("expected_rows") or 0),
        "expected_signal_count": attempt.get("expected_signal_count"),
        "signal_count": signal_count,
        "signal_count_diff": signal_count - int(attempt.get("expected_signal_count") or 0),
        "order_attempt_count": order_attempt_count,
        "order_fill_count": order_fill_count,
        "order_fill_rate": ratio(order_fill_count, order_attempt_count),
        "trade_count": trade_count,
        "trades_per_day": trades_per_day,
        "long_trade_count": metrics.get("long_trade_count"),
        "short_trade_count": metrics.get("short_trade_count"),
        "winning_trade_count": winning_trade_count,
        "losing_trade_count": losing_trade_count,
        "deal_count": deal_count,
        "deal_in_count": deal_metrics["deal_in_count"],
        "deal_out_count": deal_metrics["deal_out_count"],
        "deal_minus_order_fill": deal_count - order_fill_count,
        "deal_count_equals_2x_trade": deal_count == 2 * trade_count if trade_count else False,
        "order_fill_equals_deal_count": order_fill_count == deal_count,
        "entry_exit_balance_read": entry_exit_balance_read(deal_metrics, trade_count),
        "tester_side_exit_deal_read": "deal_minus_order_fill_positive" if deal_count > order_fill_count else "no_deal_inflation_vs_order_fill",
        "net_profit": metrics.get("net_profit"),
        "gross_profit": metrics.get("gross_profit"),
        "gross_loss": metrics.get("gross_loss"),
        "profit_factor": metrics.get("profit_factor"),
        "expectancy": metrics.get("expectancy"),
        "win_rate_percent": metrics.get("win_rate_percent"),
        "average_win": average_win,
        "average_loss": average_loss,
        "payoff_ratio": payoff_ratio,
        "recovery_factor": metrics.get("recovery_factor"),
        "max_drawdown_amount": metrics.get("max_drawdown_amount"),
        "max_drawdown_percent": runtime_dd,
        "proxy_dd": proxy_dd,
        "dd_delta_runtime_minus_proxy": (runtime_dd - proxy_dd) if runtime_dd is not None and proxy_dd is not None else None,
        "source_f67c_profit_factor": proxy_pf,
        "deal_profit_sum": deal_metrics["deal_profit_sum"],
        "deal_commission_sum": deal_metrics["deal_commission_sum"],
        "deal_swap_sum": deal_metrics["deal_swap_sum"],
        "deal_cost_sum": deal_metrics["deal_cost_sum"],
        "net_reconciliation_error": reconciliation_error(metrics.get("net_profit"), deal_metrics),
        "config_spread_identity": attempt["cost_identity_plan"]["config_spread_identity"],
        "config_commission_identity": attempt["cost_identity_plan"]["config_commission_identity"],
        "config_slippage_identity": attempt["cost_identity_plan"]["config_slippage_identity"],
        "config_swap_identity": attempt["cost_identity_plan"]["config_swap_identity"],
        "report_path": (report.get("html_report") or {}).get("path", ""),
        "telemetry_path": runtime.get("telemetry_path", ""),
        "summary_path": runtime.get("summary_path", ""),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return [row]


def empty_deal_metrics() -> dict[str, Any]:
    return {
        "deal_table_encoding": "",
        "deal_row_count": 0,
        "deal_in_count": 0,
        "deal_out_count": 0,
        "deal_commission_sum": 0.0,
        "deal_swap_sum": 0.0,
        "deal_profit_sum": 0.0,
        "deal_cost_sum": 0.0,
    }


def entry_exit_balance_read(deal_metrics: Mapping[str, Any], trade_count: int) -> str:
    if not trade_count:
        return "missing_trade_count"
    if int(deal_metrics.get("deal_in_count") or 0) == trade_count and int(deal_metrics.get("deal_out_count") or 0) == trade_count:
        return "entry_exit_deals_match_trade_count"
    return "entry_exit_deals_do_not_match_trade_count"


def reconciliation_error(net_profit: Any, deal_metrics: Mapping[str, Any]) -> float | None:
    net = as_float(net_profit)
    if net is None:
        return None
    computed = (
        float(deal_metrics.get("deal_profit_sum") or 0.0)
        + float(deal_metrics.get("deal_commission_sum") or 0.0)
        + float(deal_metrics.get("deal_swap_sum") or 0.0)
    )
    return computed - net


def tester_period(attempt: Mapping[str, Any]) -> dict[str, Any]:
    tester = ((attempt.get("ini") or {}).get("tester") or {})
    start = str(tester.get("FromDate") or "").replace(".", "-")
    end = str(tester.get("ToDate") or "").replace(".", "-")
    days = None
    if start and end:
        try:
            start_dt = datetime.strptime(start, "%Y-%m-%d")
            end_dt = datetime.strptime(end, "%Y-%m-%d")
            days = max((end_dt - start_dt).days, 1)
        except ValueError:
            days = None
    return {
        "start": start,
        "end": end,
        "calendar_days_exclusive": days,
    }


def build_gap_classification(receipt: Mapping[str, Any], anchors: Mapping[str, Mapping[str, str]]) -> list[dict[str, Any]]:
    rows = [
        {
            "layer": "count_parity",
            "metric": "signal_count",
            "proxy_value": receipt.get("expected_signal_count"),
            "runtime_value": receipt.get("signal_count"),
            "delta": receipt.get("signal_count_diff"),
            "gap_class": "count_parity_exact" if receipt.get("signal_count_diff") == 0 else "count_parity_gap",
            "evidence": "runtime_summary_vs_expected_signal_count",
        },
        {
            "layer": "feature_readiness",
            "metric": "feature_ready_count",
            "proxy_value": receipt.get("expected_rows"),
            "runtime_value": receipt.get("feature_ready_count"),
            "delta": receipt.get("feature_ready_diff"),
            "gap_class": "feature_ready_exact" if receipt.get("feature_ready_diff") == 0 else "feature_ready_gap",
            "evidence": "runtime_summary_feature_ready_count",
        },
        {
            "layer": "accounting_parity",
            "metric": "order_fill_vs_deal_count",
            "proxy_value": receipt.get("order_fill_count"),
            "runtime_value": receipt.get("deal_count"),
            "delta": receipt.get("deal_minus_order_fill"),
            "gap_class": receipt.get("tester_side_exit_deal_read"),
            "evidence": "runtime_order_fill_count_vs_strategy_report_deal_count",
        },
        {
            "layer": "economics_parity",
            "metric": "drawdown_percent",
            "proxy_value": anchors["f67a"].get("proxy_dd"),
            "runtime_value": receipt.get("max_drawdown_percent"),
            "delta": receipt.get("dd_delta_runtime_minus_proxy"),
            "gap_class": "runtime_dd_exceeds_proxy_dd" if (as_float(receipt.get("dd_delta_runtime_minus_proxy")) or 0.0) > 0 else "runtime_dd_not_above_proxy",
            "evidence": "f67a_proxy_dd_vs_f67d_strategy_report_dd",
        },
        {
            "layer": "cost_identity",
            "metric": "swap_commission",
            "proxy_value": "config_identity_missing",
            "runtime_value": f"commission={receipt.get('deal_commission_sum')};swap={receipt.get('deal_swap_sum')}",
            "delta": receipt.get("deal_cost_sum"),
            "gap_class": cost_gap_class(receipt),
            "evidence": "set_ini_identity_vs_strategy_report_deal_table",
        },
    ]
    for row in rows:
        row["run_id"] = RUN_ID
        row["attempt_name"] = receipt.get("attempt_name", ATTEMPT_NAME)
        row["claim_boundary"] = CLAIM_BOUNDARY
    return rows


def cost_gap_class(receipt: Mapping[str, Any]) -> str:
    config_missing = all(str(receipt.get(field, "missing")).startswith("missing") for field in (
        "config_spread_identity",
        "config_commission_identity",
        "config_slippage_identity",
        "config_swap_identity",
    ))
    swap = as_float(receipt.get("deal_swap_sum")) or 0.0
    commission = as_float(receipt.get("deal_commission_sum")) or 0.0
    if config_missing and abs(swap) > 1e-9:
        return "observed_swap_with_missing_config_cost_identity"
    if abs(commission) > 1e-9:
        return "observed_commission"
    return "no_observed_commission_or_swap"


def runtime_status(
    execution_results: Sequence[Mapping[str, Any]],
    report_records: Sequence[Mapping[str, Any]],
    receipt_rows: Sequence[Mapping[str, Any]],
) -> str:
    if not execution_results or execution_results[0].get("status") != "completed":
        return "blocked_runtime_probe_execution"
    if not report_records or report_records[0].get("status") != "completed":
        return "blocked_strategy_report_parse"
    if not receipt_rows:
        return "blocked_order_intent_receipt_missing"
    return "completed_runtime_probe_observation_no_authority"


def write_outputs(payload: Mapping[str, Any], created_at: str) -> None:
    write_json(RUN_ROOT / "frontier67D_runtime_probe_execution_result.json", payload)
    write_csv(
        RUN_ROOT / "frontier67D_order_intent_receipt.csv",
        payload.get("order_intent_receipt", []),
        ORDER_INTENT_COLUMNS,
    )
    write_csv(
        REVIEWS_ROOT / "frontier67D_order_intent_receipt_review.csv",
        payload.get("order_intent_receipt", []),
        ORDER_INTENT_COLUMNS,
    )
    write_csv(
        RUN_ROOT / "frontier67D_gap_classification.csv",
        payload.get("gap_classification", []),
        GAP_COLUMNS,
    )
    write_csv(
        REVIEWS_ROOT / "frontier67D_gap_classification_review.csv",
        payload.get("gap_classification", []),
        GAP_COLUMNS,
    )
    summary = build_summary(payload)
    write_json(RUN_ROOT / "frontier67D_runtime_probe_summary.json", summary)
    write_json(REVIEWS_ROOT / "frontier67D_runtime_probe_summary_review.json", summary)
    write_report(payload, summary, created_at)
    write_grok_receipt(payload, created_at)
    write_run_manifest(payload, summary, created_at)
    write_kpi_record(payload, summary, created_at)
    write_result_summary(payload, summary, created_at)


def build_summary(payload: Mapping[str, Any]) -> dict[str, Any]:
    receipt = (payload.get("order_intent_receipt") or [{}])[0] if payload.get("order_intent_receipt") else {}
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": payload.get("status"),
        "selected_slice": "F31_oos",
        "attempt_name": ATTEMPT_NAME,
        "tester_status": receipt.get("tester_status", "missing"),
        "runtime_status": receipt.get("runtime_status", "missing"),
        "report_status": receipt.get("report_status", "missing"),
        "test_period_start": receipt.get("test_period_start"),
        "test_period_end": receipt.get("test_period_end"),
        "trades_per_day": receipt.get("trades_per_day"),
        "signal_count_diff": receipt.get("signal_count_diff"),
        "feature_ready_diff": receipt.get("feature_ready_diff"),
        "deal_minus_order_fill": receipt.get("deal_minus_order_fill"),
        "deal_count_equals_2x_trade": receipt.get("deal_count_equals_2x_trade"),
        "net_profit": receipt.get("net_profit"),
        "gross_profit": receipt.get("gross_profit"),
        "gross_loss": receipt.get("gross_loss"),
        "profit_factor": receipt.get("profit_factor"),
        "trade_count": receipt.get("trade_count"),
        "win_rate_percent": receipt.get("win_rate_percent"),
        "average_win": receipt.get("average_win"),
        "average_loss": receipt.get("average_loss"),
        "payoff_ratio": receipt.get("payoff_ratio"),
        "expectancy": receipt.get("expectancy"),
        "recovery_factor": receipt.get("recovery_factor"),
        "long_trade_count": receipt.get("long_trade_count"),
        "short_trade_count": receipt.get("short_trade_count"),
        "max_drawdown_percent": receipt.get("max_drawdown_percent"),
        "proxy_dd": receipt.get("proxy_dd"),
        "dd_delta_runtime_minus_proxy": receipt.get("dd_delta_runtime_minus_proxy"),
        "deal_commission_sum": receipt.get("deal_commission_sum"),
        "deal_swap_sum": receipt.get("deal_swap_sum"),
        "cost_gap_class": cost_gap_class(receipt) if receipt else "missing_receipt",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_action": "F67D gap analysis and repair decision before F67 closeout",
    }


def write_report(payload: Mapping[str, Any], summary: Mapping[str, Any], created_at: str) -> None:
    receipt = (payload.get("order_intent_receipt") or [{}])[0] if payload.get("order_intent_receipt") else {}
    gap_rows = payload.get("gap_classification") or []
    lines = [
        "# F67D Narrow Cost/Order-Intent MT5 Runtime Probe(F67D 좁은 비용/주문 의도 MT5 런타임 탐침)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        f"Status(상태): `{summary.get('status')}`",
        "",
        "Action(행동): F31 OOS(F31 표본외) 한 조각을 F67D 전용 run root(실행 루트)에서 MT5 Strategy Tester(MT5 전략 테스터)로 재실행했습니다.",
        "",
        "Effect(효과): F66 기존 실행을 덮어쓰지 않고, cost identity(비용 정체성), order intent receipt(주문 의도 영수증), accounting gap(회계 간극)을 F67 단계 근거로 새로 남겼습니다.",
        "",
        "## Selected Slice(선택 조각)",
        "",
        "- selected_slice(선택 조각): `F31_oos`",
        f"- test_period(테스트 기간): `{receipt.get('test_period_start', '')}`..`{receipt.get('test_period_end', '')}`",
        "- selection_reason(선택 이유): dominant trade shape(주요 거래 형태) `hold12 + ATR SLTP 1/1`, meaningful DD gap(의미 있는 손실폭 간극), order-fill/deal mismatch(주문 체결/딜 불일치)",
        "- source_attempt(원천 시도): `f66_f31_f31b_0013_oos`",
        "- claim_boundary(주장 경계): runtime_probe_observation(런타임 탐침 관찰) only(만 해당)",
        "",
        "## Order Intent Receipt(주문 의도 영수증)",
        "",
        f"- expected_signal_count(예상 신호 수): `{receipt.get('expected_signal_count', '')}`",
        f"- signal_count(신호 수): `{receipt.get('signal_count', '')}`",
        f"- signal_count_diff(신호 수 차이): `{receipt.get('signal_count_diff', '')}`",
        f"- order_attempt_count(주문 시도 수): `{receipt.get('order_attempt_count', '')}`",
        f"- order_fill_count(주문 체결 수): `{receipt.get('order_fill_count', '')}`",
        f"- trade_count(거래 수): `{receipt.get('trade_count', '')}`",
        f"- trades_per_day(일 거래 수): `{receipt.get('trades_per_day', '')}`",
        f"- deal_count(딜 수): `{receipt.get('deal_count', '')}`",
        f"- deal_in_count/deal_out_count(진입/청산 딜 수): `{receipt.get('deal_in_count', '')}` / `{receipt.get('deal_out_count', '')}`",
        f"- deal_minus_order_fill(딜-주문 체결 차이): `{receipt.get('deal_minus_order_fill', '')}`",
        "",
        "## Economics(경제성)",
        "",
        f"- net_profit(순수익): `{receipt.get('net_profit', '')}`",
        f"- gross_profit/gross_loss(총이익/총손실): `{receipt.get('gross_profit', '')}` / `{receipt.get('gross_loss', '')}`",
        f"- profit_factor(수익 팩터): `{receipt.get('profit_factor', '')}`",
        f"- win_rate_percent(승률 %): `{receipt.get('win_rate_percent', '')}`",
        f"- average_win/average_loss(평균 이익/평균 손실): `{receipt.get('average_win', '')}` / `{receipt.get('average_loss', '')}`",
        f"- payoff_ratio(손익비): `{receipt.get('payoff_ratio', '')}`",
        f"- expectancy(기대값): `{receipt.get('expectancy', '')}`",
        f"- recovery_factor(회복 계수): `{receipt.get('recovery_factor', '')}`",
        f"- max_drawdown_percent(최대 손실폭 %): `{receipt.get('max_drawdown_percent', '')}`",
        f"- long/short breakdown(롱/숏 분해): `{receipt.get('long_trade_count', '')}` / `{receipt.get('short_trade_count', '')}`",
        f"- proxy_dd(프록시 손실폭): `{receipt.get('proxy_dd', '')}`",
        f"- dd_delta_runtime_minus_proxy(런타임-프록시 손실폭 차이): `{receipt.get('dd_delta_runtime_minus_proxy', '')}`",
        f"- deal_commission_sum(딜 수수료 합계): `{receipt.get('deal_commission_sum', '')}`",
        f"- deal_swap_sum(딜 스왑 합계): `{receipt.get('deal_swap_sum', '')}`",
        "",
        "## Gap Classification(간극 분류)",
        "",
        "| layer(층) | metric(지표) | gap_class(간극 분류) | delta(차이) |",
        "|---|---|---|---:|",
    ]
    for row in gap_rows:
        lines.append(f"| `{row.get('layer')}` | `{row.get('metric')}` | `{row.get('gap_class')}` | `{row.get('delta')}` |")
    lines.extend(
        [
            "",
            "Runtime claim boundary(런타임 주장 경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 주장 없음).",
        ]
    )
    write_md(REVIEWS_ROOT / "frontier67D_narrow_cost_order_intent_runtime_probe_report.md", lines)


def write_grok_receipt(payload: Mapping[str, Any], created_at: str) -> None:
    local_verification = payload.get("local_verification") or {}
    lines = [
        "# F67D Grok Pre-MT5 Receipt(F67D MT5 전 그록 영수증)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        "- trigger_reason(트리거 이유): goal rule(목표 규칙) requires Grok review(그록 검토) before MT5 Runtime Probe(MT5 런타임 탐침).",
        "- review_size(검토 크기): medium review(중간 검토).",
        "- direction_before_grok(그록 전 방향): F67D narrow MT5 Runtime Probe(F67D 좁은 MT5 런타임 탐침) with explicit cost identity(명시 비용 정체성) and order intent receipt(주문 의도 영수증).",
        f"- bounded_evidence(제한 근거): `{rel(GROK_PACKET_ROOT / 'inputs' / 'bounded_snapshot.md')}`",
        f"- prompt_identity(프롬프트 정체성): `{rel(GROK_PACKET_ROOT / 'prompts' / 'prompt.md')}`",
        f"- grok_output_identity(그록 출력 정체성): `{rel(GROK_PACKET_ROOT / 'outputs' / 'clean_output.md')}`",
        "- advice_classification(조언 분류): accepted_with_required_additions_and_local_verification(필수 추가 및 로컬 검증 조건부 수용).",
        "- accepted(수용): cost identity block(비용 정체성 블록), order intent receipt(주문 의도 영수증), accounting parity sheet(회계 동등성 표), frozen F31 OOS anchor(고정 F31 표본외 기준 행).",
        "- rejected(거절): PF/DD optimization(PF/DD 최적화), full 64-row replay(64행 전체 재실행), F67D 단독 closeout/runtime authority(마감/런타임 권위) 주장.",
        f"- local_verification(로컬 검증): `{local_verification.get('passed')}` with checks(검사) `{json.dumps(local_verification.get('checks', {}), ensure_ascii=False)}`",
        "- forbidden_claim_check(금지 주장 확인): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 주장 없음).",
        "- final_codex_direction(최종 Codex 방향): run F31 OOS narrow probe(F31 표본외 좁은 탐침) as runtime_probe_observation(런타임 탐침 관찰) only(만 해당).",
    ]
    write_md(REVIEWS_ROOT / "grok_f67d_pre_mt5_receipt.md", lines)


def write_run_manifest(payload: Mapping[str, Any], summary: Mapping[str, Any], created_at: str) -> None:
    attempt = (payload.get("attempts") or [{}])[0] if payload.get("attempts") else {}
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "status": payload.get("status"),
        "claim_boundary": CLAIM_BOUNDARY,
        "producer": "stage_pipelines/stage_frontier_67/frontier67d_narrow_cost_order_intent_runtime_probe.py",
        "hypothesis": (
            "Fresh F31 OOS MT5 runtime probe can preserve exact signal/feature counts while exposing accounting, DD, and cost gaps."
        ),
        "selected_slice": "F31_oos",
        "test_period": {
            "start": summary.get("test_period_start"),
            "end": summary.get("test_period_end"),
            "calendar_days_exclusive": ((payload.get("order_intent_receipt") or [{}])[0] or {}).get("calendar_days_exclusive"),
        },
        "source_inputs": {
            "source_attempt_name": payload.get("source_attempt_name"),
            "source_run_id": F66_RUN_ID,
            "parent_run_id": "frontier67C_runtime_native_order_intent_economics_v1",
            "grok_packet": payload.get("grok_packet"),
        },
        "execution": {
            "attempt_name": ATTEMPT_NAME,
            "tester": ((attempt.get("ini") or {}).get("tester") or {}),
            "common_telemetry_path": attempt.get("common_telemetry_path"),
            "common_summary_path": attempt.get("common_summary_path"),
            "compile_payload": payload.get("compile_payload"),
        },
        "artifacts": artifact_manifest(payload),
        "summary": summary,
        "next_action": "F67E gap analysis/repair decision before F67 closeout",
    }
    write_json(RUN_ROOT / "run_manifest.json", manifest)


def write_kpi_record(payload: Mapping[str, Any], summary: Mapping[str, Any], created_at: str) -> None:
    receipt = (payload.get("order_intent_receipt") or [{}])[0] if payload.get("order_intent_receipt") else {}
    kpi_record = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "status": payload.get("status"),
        "claim_boundary": CLAIM_BOUNDARY,
        "test_period": {
            "start": receipt.get("test_period_start"),
            "end": receipt.get("test_period_end"),
            "calendar_days_exclusive": receipt.get("calendar_days_exclusive"),
        },
        "split_view": "F31_oos_runtime_probe",
        "proxy_expectation": {
            "expected_signal_count": receipt.get("expected_signal_count"),
            "expected_rows": receipt.get("expected_rows"),
            "proxy_dd": receipt.get("proxy_dd"),
            "source_f67c_profit_factor": receipt.get("source_f67c_profit_factor"),
        },
        "proxy_kpi": {
            "proxy_dd": receipt.get("proxy_dd"),
            "source_f67c_profit_factor": receipt.get("source_f67c_profit_factor"),
        },
        "runtime_probe_kpi": {
            "net_profit": receipt.get("net_profit"),
            "gross_profit": receipt.get("gross_profit"),
            "gross_loss": receipt.get("gross_loss"),
            "profit_factor": receipt.get("profit_factor"),
            "max_drawdown_percent": receipt.get("max_drawdown_percent"),
            "max_drawdown_amount": receipt.get("max_drawdown_amount"),
            "trade_count": receipt.get("trade_count"),
            "trades_per_day": receipt.get("trades_per_day"),
            "win_rate_percent": receipt.get("win_rate_percent"),
            "average_win": receipt.get("average_win"),
            "average_loss": receipt.get("average_loss"),
            "payoff_ratio": receipt.get("payoff_ratio"),
            "expectancy": receipt.get("expectancy"),
            "recovery_factor": receipt.get("recovery_factor"),
            "long_trade_count": receipt.get("long_trade_count"),
            "short_trade_count": receipt.get("short_trade_count"),
        },
        "parity": {
            "signal_count_diff": receipt.get("signal_count_diff"),
            "feature_ready_diff": receipt.get("feature_ready_diff"),
            "order_fill_count": receipt.get("order_fill_count"),
            "deal_count": receipt.get("deal_count"),
            "deal_minus_order_fill": receipt.get("deal_minus_order_fill"),
        },
        "costs": {
            "deal_commission_sum": receipt.get("deal_commission_sum"),
            "deal_swap_sum": receipt.get("deal_swap_sum"),
            "deal_cost_sum": receipt.get("deal_cost_sum"),
            "cost_gap_class": cost_gap_class(receipt) if receipt else "missing_receipt",
        },
        "proxy_runtime_gap": {
            "dd_delta_runtime_minus_proxy": receipt.get("dd_delta_runtime_minus_proxy"),
            "gap_classification": payload.get("gap_classification", []),
            "gap_cause": (
                "count_feature_parity_exact_but_accounting_parity_deal_inflation_plus_runtime_dd_repricing_plus_missing_config_cost_identity"
            ),
        },
        "source_authority": "F67D MT5 Strategy Tester report and runtime telemetry",
        "next_action": "F67E gap analysis/repair decision before F67 closeout",
    }
    write_json(RUN_ROOT / "kpi_record.json", kpi_record)


def write_result_summary(payload: Mapping[str, Any], summary: Mapping[str, Any], created_at: str) -> None:
    receipt = (payload.get("order_intent_receipt") or [{}])[0] if payload.get("order_intent_receipt") else {}
    lines = [
        "# F67D Result Summary(F67D 결과 요약)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        "Action(행동): F31 OOS(F31 표본외) MT5 Runtime Probe(MT5 런타임 탐침)를 새 run root(실행 루트)에서 실행했다.",
        "",
        "Effect(효과): F67 closeout(마감) 전 필수 runtime probe observation(런타임 탐침 관찰)을 만들고, signal/feature parity(신호/피처 동등성)와 accounting/DD/cost gap(회계/손실폭/비용 간극)을 같은 evidence root(근거 루트)에 묶었다.",
        "",
        f"- status(상태): `{payload.get('status')}`",
        f"- test_period(테스트 기간): `{receipt.get('test_period_start')}`..`{receipt.get('test_period_end')}`",
        f"- net_profit/PF/DD(순수익/수익 팩터/손실폭): `{receipt.get('net_profit')}` / `{receipt.get('profit_factor')}` / `{receipt.get('max_drawdown_percent')}`",
        f"- trade_count/trades_per_day(거래 수/일 거래 수): `{receipt.get('trade_count')}` / `{receipt.get('trades_per_day')}`",
        f"- signal_count_diff/feature_ready_diff(신호 수 차이/피처 준비 차이): `{receipt.get('signal_count_diff')}` / `{receipt.get('feature_ready_diff')}`",
        f"- deal_minus_order_fill(딜-주문 체결 차이): `{receipt.get('deal_minus_order_fill')}`",
        f"- cost_gap_class(비용 간극 분류): `{summary.get('cost_gap_class')}`",
        "",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ]
    write_md(RUN_ROOT / "reports" / "result_summary.md", lines)


def artifact_manifest(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    paths: list[tuple[str, Path, bool]] = [
        ("execution_result", RUN_ROOT / "frontier67D_runtime_probe_execution_result.json", True),
        ("order_intent_receipt", RUN_ROOT / "frontier67D_order_intent_receipt.csv", True),
        ("gap_classification", RUN_ROOT / "frontier67D_gap_classification.csv", True),
        ("runtime_summary", RUN_ROOT / "frontier67D_runtime_probe_summary.json", True),
        ("review_report", REVIEWS_ROOT / "frontier67D_narrow_cost_order_intent_runtime_probe_report.md", True),
        ("grok_receipt", REVIEWS_ROOT / "grok_f67d_pre_mt5_receipt.md", True),
    ]
    attempt = (payload.get("attempts") or [{}])[0] if payload.get("attempts") else {}
    for key in ("set", "ini"):
        raw_path = ((attempt.get(key) or {}).get("path"))
        if raw_path:
            paths.append((f"mt5_{key}", ROOT / str(raw_path), True))
    report_path = (((payload.get("strategy_tester_reports") or [{}])[0] or {}).get("html_report") or {}).get("path")
    if report_path:
        paths.append(("strategy_tester_html_report", ROOT / str(report_path), True))
    artifacts: list[dict[str, Any]] = []
    for role, path, required in paths:
        exists = path_exists(path)
        artifacts.append(
            {
                "role": role,
                "path": rel(path),
                "required": required,
                "exists": exists,
                "sha256": mt5.sha256_file(path) if exists else "",
            }
        )
    return artifacts


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix() if path.is_absolute() else path.as_posix()


ORDER_INTENT_COLUMNS = (
    "run_id",
    "attempt_name",
    "stage_num",
    "stage_id",
    "candidate_id",
    "split",
    "test_period_start",
    "test_period_end",
    "calendar_days_exclusive",
    "tester_status",
    "runtime_status",
    "report_status",
    "expected_rows",
    "feature_ready_count",
    "feature_ready_diff",
    "expected_signal_count",
    "signal_count",
    "signal_count_diff",
    "order_attempt_count",
    "order_fill_count",
    "order_fill_rate",
    "trade_count",
    "trades_per_day",
    "long_trade_count",
    "short_trade_count",
    "winning_trade_count",
    "losing_trade_count",
    "deal_count",
    "deal_in_count",
    "deal_out_count",
    "deal_minus_order_fill",
    "deal_count_equals_2x_trade",
    "order_fill_equals_deal_count",
    "entry_exit_balance_read",
    "tester_side_exit_deal_read",
    "net_profit",
    "gross_profit",
    "gross_loss",
    "profit_factor",
    "expectancy",
    "win_rate_percent",
    "average_win",
    "average_loss",
    "payoff_ratio",
    "recovery_factor",
    "max_drawdown_amount",
    "max_drawdown_percent",
    "proxy_dd",
    "dd_delta_runtime_minus_proxy",
    "source_f67c_profit_factor",
    "deal_profit_sum",
    "deal_commission_sum",
    "deal_swap_sum",
    "deal_cost_sum",
    "net_reconciliation_error",
    "config_spread_identity",
    "config_commission_identity",
    "config_slippage_identity",
    "config_swap_identity",
    "report_path",
    "telemetry_path",
    "summary_path",
    "claim_boundary",
)

GAP_COLUMNS = (
    "run_id",
    "attempt_name",
    "layer",
    "metric",
    "proxy_value",
    "runtime_value",
    "delta",
    "gap_class",
    "evidence",
    "claim_boundary",
)


if __name__ == "__main__":
    raise SystemExit(main())
