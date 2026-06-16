from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.control_plane.mt5_tier_balance_completion import attempt_payload
from foundation.mt5 import runtime_support as mt5
from stage_pipelines.stage_frontier_68 import frontier68d_mt5_runtime_probe_candidate_axis_materialization as f68d
from stage_pipelines.stage_frontier_68.frontier68a_bridge_feasibility_and_label_design import (
    STAGE_ID,
    rel,
    sha256_file,
    upsert_ledger,
    write_csv,
    write_json,
    write_md,
)
from stage_pipelines.stage_frontier_runtime_backfill.run_frontier_runtime_probe_backfill import (
    DEFAULT_COMMON_FILES,
    DEFAULT_METAEDITOR,
    DEFAULT_PORTABLE_ROOT,
    DEFAULT_TERMINAL,
    DEFAULT_TESTER_PROFILE_ROOT,
)


RUN_ID = "frontier68J_unit_corrected_atr_runtime_repair_probe_v1"
PARENT_RUN_ID = "frontier68I_risk_envelope_result_review_or_stage_closeout_decision_v1"
SOURCE_RUN_ID = "frontier68F_near_four_axis_onnx_runtime_repair_probe_v1"
NEXT_RUN_ID = "frontier68K_unit_corrected_atr_result_review_or_stage_closeout_decision_v1"

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
MT5_ROOT = RUN_ROOT / "mt5"
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
F68F_RUN_ROOT = STAGE_ROOT / "02_runs" / SOURCE_RUN_ID
F68I_RUN_ROOT = STAGE_ROOT / "02_runs" / PARENT_RUN_ID

F68F_HANDOFF = F68F_RUN_ROOT / "frontier68F_handoff_intent.csv"
F68F_SIGNAL_PARITY = F68F_RUN_ROOT / "frontier68F_onnx_signal_parity.csv"
F68F_KPI_BY_SPLIT = F68F_RUN_ROOT / "frontier68F_candidate_axis_kpi_by_split.csv"
F68F_RECEIPT = REVIEWS_ROOT / "frontier68F_runtime_probe_receipt_review.csv"
F68I_VARIANTS = F68I_RUN_ROOT / "f68i_next_unit_corrected_atr_variants.csv"

GROK_PACKET_ROOT = ROOT / "docs/agent_control/grok_reviews/2026-06-17_f68j_pre_unit_corrected_atr_runtime_probe"
GROK_PROMPT = GROK_PACKET_ROOT / "prompts/f68j_pre_unit_corrected_atr_runtime_probe_prompt.md"
GROK_CLEAN = GROK_PACKET_ROOT / "outputs/clean_output.md"
GROK_METADATA = GROK_PACKET_ROOT / "outputs/metadata.json"

COMMON_RUN_ROOT = "Project_Obsidian_Prime_v2/frontier68J_unit_corrected_atr_probe"

CLAIM_BOUNDARY = (
    "unit_corrected_atr_runtime_repair_probe_observation_only_no_completion_no_baseline_"
    "no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve"
)

SPLIT_WINDOWS = {
    "validation": {"from": "2025.01.02", "to": "2025.10.01"},
    "oos": {"from": "2025.10.01", "to": "2026.04.14"},
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="F68J unit-corrected ATR runtime repair probe.")
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
    created_at = utc_now()
    ensure_dirs()
    patch_runtime_globals()

    handoff = first_row(F68F_HANDOFF)
    variants = read_csv_rows(F68I_VARIANTS)
    signal_by_split = {row["split"]: row for row in read_csv_rows(F68F_SIGNAL_PARITY)}
    proxy_by_split = {row["split"]: row for row in read_csv_rows(F68F_KPI_BY_SPLIT)}
    baseline_receipts = read_csv_rows(F68F_RECEIPT)
    local_verification = build_local_verification(handoff, variants, baseline_receipts)
    attempts = build_attempts(args, handoff, variants, signal_by_split, proxy_by_split) if local_verification["can_execute"] else []

    payload: dict[str, Any] = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": created_at,
        "status": "materialized_pending_mt5_unit_corrected_atr_runtime_repair_probe_no_authority",
        "judgment": "unit_corrected_atr_repair_probe_pending_no_authority",
        "claim_boundary": CLAIM_BOUNDARY,
        "grok_receipt": grok_receipt(local_verification),
        "handoff": handoff,
        "variant_plan": variants,
        "baseline_receipts": baseline_receipts,
        "local_verification": local_verification,
        "attempts": attempts,
        "compile_payload": {},
        "execution_results": [],
        "strategy_tester_reports": [],
        "mt5_kpi_records": [],
        "runtime_receipt": [],
        "gap_classification": [],
        "comparison_vs_f68f": [],
        "effective_sltp": [],
        "signature_collapse": [],
    }

    if args.materialize_only or not args.execute or not local_verification["can_execute"]:
        write_outputs(payload)
        update_state_and_ledgers(payload)
        print(json.dumps(json_ready(compact_status(payload)), ensure_ascii=False, indent=2, sort_keys=True))
        return 0 if local_verification["passed"] else 1

    compile_payload = f68d.compile_runtime_ea(Path(args.metaeditor_path))
    execution_results = f68d.execute_attempts(args, attempts, compile_payload)
    report_records = mt5.collect_mt5_strategy_report_artifacts(
        terminal_data_root=Path(args.terminal_data_root),
        run_output_root=RUN_ROOT,
        attempts=attempts,
        run_id=RUN_ID,
    )
    mt5.attach_mt5_report_metrics(execution_results, report_records)
    kpi_records = mt5.build_mt5_kpi_records(execution_results)
    receipt_rows = f68d.build_runtime_receipt(execution_results, attempts)
    gap_rows = [row for receipt in receipt_rows for row in f68d.build_gap_classification(receipt)]
    comparison_rows = build_comparison_rows(receipt_rows, baseline_receipts, attempts)
    effective_rows = build_effective_sltp_rows(execution_results, attempts)
    signature_rows = build_signature_rows(effective_rows, comparison_rows)
    execution_completed = bool(execution_results) and all(row.get("status") == "completed" for row in execution_results)
    report_completed = bool(kpi_records) and len(kpi_records) == len(attempts)
    payload.update(
        {
            "status": (
                "completed_unit_corrected_atr_runtime_repair_probe_observation_no_authority"
                if execution_completed and report_completed
                else "blocked_unit_corrected_atr_runtime_repair_probe_attempted_repair_required_no_authority"
            ),
            "judgment": (
                unit_corrected_atr_judgment(comparison_rows, signature_rows)
                if execution_completed and report_completed
                else "unit_corrected_atr_runtime_probe_blocked_no_authority"
            ),
            "compile_payload": compile_payload,
            "execution_results": execution_results,
            "strategy_tester_reports": report_records,
            "mt5_kpi_records": kpi_records,
            "runtime_receipt": receipt_rows,
            "gap_classification": gap_rows,
            "comparison_vs_f68f": comparison_rows,
            "effective_sltp": effective_rows,
            "signature_collapse": signature_rows,
        }
    )
    write_outputs(payload)
    update_state_and_ledgers(payload)
    print(json.dumps(json_ready(compact_status(payload)), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def ensure_dirs() -> None:
    for path in (RUN_ROOT, MT5_ROOT, MT5_ROOT / "reports", REVIEWS_ROOT):
        io_path(path).mkdir(parents=True, exist_ok=True)


def patch_runtime_globals() -> None:
    f68d.RUN_ID = RUN_ID
    f68d.RUN_ROOT = RUN_ROOT
    f68d.MT5_ROOT = MT5_ROOT
    f68d.CLAIM_BOUNDARY = CLAIM_BOUNDARY


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def first_row(path: Path) -> dict[str, str]:
    rows = read_csv_rows(path)
    return rows[0] if rows else {}


def as_float(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def as_int(value: Any) -> int | None:
    number = as_float(value)
    return int(number) if number is not None else None


def fmt(value: Any) -> str:
    number = as_float(value)
    if number is None:
        return "" if value in (None, "") else str(value)
    if abs(number - round(number)) < 1e-9:
        return str(int(round(number)))
    return f"{number:.6f}".rstrip("0").rstrip(".")


def check(name: str, ok: bool, detail: str, effect: str) -> dict[str, str]:
    return {
        "check_name": name,
        "status": "passed" if ok else "failed",
        "detail": detail,
        "effect": effect,
    }


def caps_are_zero(variants: Sequence[Mapping[str, str]]) -> bool:
    cap_keys = [
        "atr_min_stop_points",
        "atr_max_stop_points",
        "atr_min_take_profit_points",
        "atr_max_take_profit_points",
    ]
    return bool(variants) and all((as_float(row.get(key)) or 0.0) == 0.0 for row in variants for key in cap_keys)


def multipliers_are_distinct(variants: Sequence[Mapping[str, str]]) -> bool:
    pairs = {
        (fmt(row.get("atr_stop_multiplier")), fmt(row.get("atr_take_profit_multiplier")))
        for row in variants
    }
    return len(pairs) == len(variants) and len(pairs) >= 3


def build_local_verification(
    handoff: Mapping[str, str],
    variants: Sequence[Mapping[str, str]],
    baseline_receipts: Sequence[Mapping[str, str]],
) -> dict[str, Any]:
    model_path = ROOT / str(handoff.get("model_path_repo", ""))
    feature_path = ROOT / str(handoff.get("feature_csv_repo", ""))
    rows = [
        check("grok_prompt_exists", path_exists(GROK_PROMPT), rel(GROK_PROMPT), "keeps required pre-probe review trace"),
        check("grok_clean_output_exists", path_exists(GROK_CLEAN), rel(GROK_CLEAN), "keeps Grok advice available before MT5"),
        check("grok_metadata_exists", path_exists(GROK_METADATA), rel(GROK_METADATA), "keeps wrapper transport identity available"),
        check("handoff_present", bool(handoff), rel(F68F_HANDOFF), "keeps F68F ONNX lineage fixed"),
        check("model_exists", path_exists(model_path), rel(model_path), "proves ONNX artifact is locally available"),
        check("feature_csv_exists", path_exists(feature_path), rel(feature_path), "proves feature handoff is locally available"),
        check("variant_rows_three", len(variants) == 3, str(len(variants)), "keeps F68J capped repair bounded"),
        check("variant_caps_all_zero", caps_are_zero(variants), "all min/max cap fields must be 0", "prevents F68H 180/260 cap collapse repetition"),
        check("variant_multipliers_distinct", multipliers_are_distinct(variants), "three multiplier pairs required", "proves variants can differentiate before runtime"),
        check("baseline_f68f_receipts_present", len(baseline_receipts) == 2, str(len(baseline_receipts)), "anchors KPI comparison to F68F, not F68H"),
    ]
    accepted = [
        "F68J is a reasonable unit-corrected ATR repair probe after F68H/F68I.",
        "Telemetry differentiation must be judged before KPI interpretation.",
    ]
    rejected = [
        "No completion, baseline, promotion, runtime authority, live readiness, or Goal Achieve claim.",
        "Do not re-run F68H/F52-style capped ATR grids under the F68J label.",
        "Do not judge success from PF/net alone if effective SL/TP signatures collapse.",
    ]
    needs_local_verification = [
        "caps zero in .set and run manifest",
        "same F68F ONNX/feature/signal path",
        "all variants execute validation and OOS",
        "signal and feature parity remain exact",
        "effective SL/TP telemetry differs by variant",
        "KPI direction compared to F68F",
    ]
    passed = all(row["status"] == "passed" for row in rows)
    return {
        "passed": passed,
        "can_execute": passed,
        "rows": rows,
        "accepted": accepted,
        "rejected": rejected,
        "needs_local_verification": needs_local_verification,
    }


def grok_receipt(local_verification: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "trigger_reason": "major_validation_pre_mt5_runtime_probe_required_by_goal",
        "review_size": "medium",
        "direction_before_grok": "run F68J unit-corrected ATR runtime repair probe only if capped SL/TP collapse is avoided",
        "bounded_evidence": [
            "F68F baseline runtime KPIs",
            "F68H capped ATR collapse and negative KPIs",
            "F68I next unit-corrected ATR variants",
        ],
        "prompt_path": rel(GROK_PROMPT),
        "prompt_sha256": sha256_file(GROK_PROMPT) if path_exists(GROK_PROMPT) else "",
        "clean_output_path": rel(GROK_CLEAN),
        "clean_output_sha256": sha256_file(GROK_CLEAN) if path_exists(GROK_CLEAN) else "",
        "advice_classification": {
            "accepted": local_verification.get("accepted", []),
            "rejected": local_verification.get("rejected", []),
            "needs_local_verification": local_verification.get("needs_local_verification", []),
        },
        "local_verification": local_verification.get("rows", []),
        "forbidden_claim_check": "passed_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve",
        "final_codex_direction": "run F68J only after caps-zero and lineage preflight pass",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_attempts(
    args: argparse.Namespace,
    handoff: Mapping[str, str],
    variants: Sequence[Mapping[str, str]],
    signal_by_split: Mapping[str, Mapping[str, str]],
    proxy_by_split: Mapping[str, Mapping[str, str]],
) -> list[dict[str, Any]]:
    model_local = ROOT / str(handoff["model_path_repo"])
    feature_local = ROOT / str(handoff["feature_csv_repo"])
    model_common = f"{COMMON_RUN_ROOT}/models/{model_local.name}"
    feature_common = f"{COMMON_RUN_ROOT}/features/{feature_local.name}"
    model_common_payload = mt5.copy_to_common_files(Path(args.common_files_root), model_local, model_common)
    feature_common_payload = mt5.copy_to_common_files(Path(args.common_files_root), feature_local, feature_common)
    attempts: list[dict[str, Any]] = []
    for variant in variants:
        for split, window in SPLIT_WINDOWS.items():
            attempt_name = f"f68j_{variant['variant_id']}_{split}"
            signal = signal_by_split.get(split, {})
            proxy = proxy_by_split.get(split, {})
            extra_set_values = {
                "InpReentryCooldownBars": as_int(variant.get("reentry_cooldown_bars")) or 0,
                "InpSameDirectionReentryCooldownBars": as_int(variant.get("same_direction_reentry_cooldown_bars")) or 0,
                "InpAtrSltpEnabled": True,
                "InpAtrPeriod": as_int(variant.get("atr_period")) or 14,
                "InpAtrStopMultiplier": as_float(variant.get("atr_stop_multiplier")) or 0.0,
                "InpAtrTakeProfitMultiplier": as_float(variant.get("atr_take_profit_multiplier")) or 0.0,
                "InpAtrMinStopPoints": as_float(variant.get("atr_min_stop_points")) or 0.0,
                "InpAtrMaxStopPoints": as_float(variant.get("atr_max_stop_points")) or 0.0,
                "InpAtrMinTakeProfitPoints": as_float(variant.get("atr_min_take_profit_points")) or 0.0,
                "InpAtrMaxTakeProfitPoints": as_float(variant.get("atr_max_take_profit_points")) or 0.0,
                "InpDecisionMode": str(handoff.get("decision_mode") or "threshold_margin"),
                "InpFallbackDecisionMode": str(handoff.get("decision_mode") or "threshold_margin"),
            }
            attempt = attempt_payload(
                run_root=RUN_ROOT,
                run_id=RUN_ID,
                stage_number=68,
                exploration_label="frontier68J_unit_corrected_atr_runtime_probe",
                attempt_name=attempt_name,
                tier=mt5.TIER_A,
                split=split,
                model_path=model_common,
                model_id=f"F68J_{handoff.get('candidate_id')}_{variant['variant_id']}",
                model_backend="onnx",
                feature_path=feature_common,
                feature_count=as_int(handoff.get("feature_count")) or 0,
                feature_order_hash=str(handoff.get("feature_order_hash") or ""),
                short_threshold=as_float(handoff.get("short_threshold")) or 0.0,
                long_threshold=as_float(handoff.get("long_threshold")) or 0.0,
                min_margin=as_float(handoff.get("min_margin")) or 0.0,
                invert_signal=False,
                from_date=window["from"],
                to_date=window["to"],
                primary_active_tier=mt5.TIER_A,
                attempt_role="f68j_unit_corrected_atr_runtime_probe",
                record_view_prefix=f"mt5_f68j_{variant['variant_id']}",
                max_hold_bars=as_int(handoff.get("max_hold_bars")) or 2,
                common_root=COMMON_RUN_ROOT,
                close_on_flat_signal=True,
                reverse_on_opposite_signal=True,
                close_only_on_opposite_signal=False,
                extra_set_values=extra_set_values,
            )
            attempt.update(
                {
                    "candidate_id": handoff.get("candidate_id"),
                    "axis_id": "unit_corrected_atr_axis",
                    "variant_id": variant.get("variant_id"),
                    "variant_role": variant.get("role"),
                    "expected_rows": as_int(signal.get("rows")) or 0,
                    "expected_signal_count": as_int(signal.get("onnx_signal_count")) or 0,
                    "expected_sklearn_signal_count": as_int(signal.get("sklearn_signal_count")) or 0,
                    "proxy_kpi": proxy,
                    "model_common_copy": model_common_payload,
                    "feature_common_copy": feature_common_payload,
                    "model_sha256_actual": sha256_file(model_local),
                    "feature_sha256_actual": sha256_file(feature_local),
                    "expected_stop_multiplier": as_float(variant.get("atr_stop_multiplier")) or 0.0,
                    "expected_take_profit_multiplier": as_float(variant.get("atr_take_profit_multiplier")) or 0.0,
                    "intentional_delta_vs_f68f": "ATR_SLTP_uncapped_unit_corrected_reentry0_same_direction6_only",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            attempts.append(attempt)
    return attempts


def baseline_by_split(rows: Sequence[Mapping[str, str]]) -> dict[str, Mapping[str, str]]:
    return {str(row.get("split")): row for row in rows}


def numeric_delta(runtime: Any, baseline: Any) -> float | None:
    left = as_float(runtime)
    right = as_float(baseline)
    return None if left is None or right is None else left - right


def build_comparison_rows(
    receipts: Sequence[Mapping[str, Any]],
    baseline_receipts: Sequence[Mapping[str, str]],
    attempts: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    baseline = baseline_by_split(baseline_receipts)
    attempt_by_name = {str(row.get("attempt_name")): row for row in attempts}
    rows: list[dict[str, Any]] = []
    for receipt in receipts:
        attempt = attempt_by_name.get(str(receipt.get("attempt_name")), {})
        base = baseline.get(str(receipt.get("split")), {})
        rows.append(
            {
                "variant_id": attempt.get("variant_id"),
                "variant_role": attempt.get("variant_role"),
                "split": receipt.get("split"),
                "period": f"{receipt.get('test_period_start')}..{receipt.get('test_period_end')}",
                "net_profit": receipt.get("net_profit"),
                "f68f_net_profit": base.get("net_profit"),
                "net_profit_delta_vs_f68f": fmt(numeric_delta(receipt.get("net_profit"), base.get("net_profit"))),
                "profit_factor": receipt.get("profit_factor"),
                "f68f_profit_factor": base.get("profit_factor"),
                "profit_factor_delta_vs_f68f": fmt(numeric_delta(receipt.get("profit_factor"), base.get("profit_factor"))),
                "drawdown_percent": receipt.get("max_drawdown_percent"),
                "f68f_drawdown_percent": base.get("max_drawdown_percent"),
                "drawdown_percent_delta_vs_f68f": fmt(
                    numeric_delta(receipt.get("max_drawdown_percent"), base.get("max_drawdown_percent"))
                ),
                "trades_per_day": receipt.get("trades_per_day"),
                "f68f_trades_per_day": base.get("trades_per_day"),
                "trades_per_day_delta_vs_f68f": fmt(numeric_delta(receipt.get("trades_per_day"), base.get("trades_per_day"))),
                "trade_count": receipt.get("trade_count"),
                "win_rate_percent": receipt.get("win_rate_percent"),
                "average_win": receipt.get("average_win"),
                "average_loss": receipt.get("average_loss"),
                "payoff_ratio": receipt.get("payoff_ratio"),
                "expectancy": receipt.get("expectancy"),
                "recovery_factor": receipt.get("recovery_factor"),
                "signal_count_diff": receipt.get("signal_count_diff"),
                "feature_ready_diff": receipt.get("feature_ready_diff"),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def mean(values: Sequence[float]) -> float | str:
    return sum(values) / len(values) if values else ""


def telemetry_order_sltp_summary(
    path: Path,
    expected_stop_multiplier: float,
    expected_take_profit_multiplier: float,
) -> dict[str, Any]:
    atr_values: list[float] = []
    sl_values: list[float] = []
    tp_values: list[float] = []
    sl_ratios: list[float] = []
    tp_ratios: list[float] = []
    with io_path(path).open("r", encoding="utf-8", errors="replace", newline="") as handle:
        for row in csv.DictReader(handle):
            if str(row.get("order_attempted")).strip().lower() not in {"true", "1"}:
                continue
            atr = as_float(row.get("atr_points"))
            sl = as_float(row.get("open_sl_points"))
            tp = as_float(row.get("open_tp_points"))
            if atr is None or sl is None or tp is None:
                continue
            atr_values.append(atr)
            sl_values.append(sl)
            tp_values.append(tp)
            if atr > 0:
                sl_ratios.append(sl / atr)
                tp_ratios.append(tp / atr)
    sl_unique = sorted(set(sl_values))
    tp_unique = sorted(set(tp_values))
    return {
        "order_rows": len(sl_values),
        "atr_min": min(atr_values) if atr_values else "",
        "atr_max": max(atr_values) if atr_values else "",
        "open_sl_min": min(sl_values) if sl_values else "",
        "open_sl_max": max(sl_values) if sl_values else "",
        "open_tp_min": min(tp_values) if tp_values else "",
        "open_tp_max": max(tp_values) if tp_values else "",
        "open_sl_unique_count": len(sl_unique),
        "open_tp_unique_count": len(tp_unique),
        "open_sl_unique_values": ";".join(fmt(v) for v in sl_unique[:8]),
        "open_tp_unique_values": ";".join(fmt(v) for v in tp_unique[:8]),
        "sl_over_atr_min": min(sl_ratios) if sl_ratios else "",
        "sl_over_atr_max": max(sl_ratios) if sl_ratios else "",
        "sl_over_atr_mean": mean(sl_ratios),
        "tp_over_atr_min": min(tp_ratios) if tp_ratios else "",
        "tp_over_atr_max": max(tp_ratios) if tp_ratios else "",
        "tp_over_atr_mean": mean(tp_ratios),
        "expected_stop_multiplier": expected_stop_multiplier,
        "expected_take_profit_multiplier": expected_take_profit_multiplier,
        "stop_multiplier_error_mean": numeric_delta(mean(sl_ratios), expected_stop_multiplier),
        "take_profit_multiplier_error_mean": numeric_delta(mean(tp_ratios), expected_take_profit_multiplier),
    }


def build_effective_sltp_rows(
    execution_results: Sequence[Mapping[str, Any]],
    attempts: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    attempt_by_name = {str(row.get("attempt_name")): row for row in attempts}
    rows: list[dict[str, Any]] = []
    for result in execution_results:
        runtime = result.get("runtime_outputs", {}) if isinstance(result.get("runtime_outputs"), Mapping) else {}
        telemetry_path = runtime.get("telemetry_path")
        attempt_name = str(result.get("attempt_name") or "")
        attempt = attempt_by_name.get(attempt_name, {})
        if not telemetry_path:
            continue
        summary = telemetry_order_sltp_summary(
            Path(str(telemetry_path)),
            as_float(attempt.get("expected_stop_multiplier")) or 0.0,
            as_float(attempt.get("expected_take_profit_multiplier")) or 0.0,
        )
        variant_id = str(attempt.get("variant_id") or attempt_name.replace("f68j_", "").replace("_validation", "").replace("_oos", ""))
        rows.append(
            {
                "attempt_name": attempt_name,
                "variant_id": variant_id,
                "split": result.get("split"),
                **summary,
                "matches_f68h_cap_signature": summary.get("open_sl_unique_values") == "180"
                and summary.get("open_tp_unique_values") == "260",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_signature_rows(
    effective_rows: Sequence[Mapping[str, Any]],
    comparison_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    by_split_effective: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for row in effective_rows:
        by_split_effective[str(row.get("split"))].append(row)
    by_split_kpi: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for row in comparison_rows:
        by_split_kpi[str(row.get("split"))].append(row)
    rows: list[dict[str, Any]] = []
    for split in sorted(set(by_split_effective) | set(by_split_kpi)):
        effective_signatures = {
            (
                fmt(row.get("open_sl_min")),
                fmt(row.get("open_sl_max")),
                fmt(row.get("open_tp_min")),
                fmt(row.get("open_tp_max")),
                fmt(row.get("sl_over_atr_mean")),
                fmt(row.get("tp_over_atr_mean")),
            )
            for row in by_split_effective.get(split, [])
        }
        kpi_signatures = {
            (
                fmt(row.get("profit_factor")),
                fmt(row.get("drawdown_percent")),
                fmt(row.get("trades_per_day")),
                fmt(row.get("net_profit")),
            )
            for row in by_split_kpi.get(split, [])
        }
        variant_count = len({str(row.get("variant_id")) for row in by_split_effective.get(split, [])})
        rows.append(
            {
                "split": split,
                "variant_count": variant_count,
                "effective_signature_count": len(effective_signatures),
                "kpi_signature_count": len(kpi_signatures),
                "effective_collapsed_all_variants": variant_count >= 3 and len(effective_signatures) == 1,
                "kpi_collapsed_all_variants": variant_count >= 3 and len(kpi_signatures) == 1,
                "matches_f68h_cap_signature_rows": sum(
                    1 for row in by_split_effective.get(split, []) if str(row.get("matches_f68h_cap_signature")) == "True"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def unit_corrected_atr_judgment(
    comparison_rows: Sequence[Mapping[str, Any]],
    signature_rows: Sequence[Mapping[str, Any]],
) -> str:
    if any(str(row.get("effective_collapsed_all_variants")) == "True" for row in signature_rows):
        return "invalid_variant_differentiation_unit_corrected_atr_signature_collapse_no_authority"
    oos_rows = [row for row in comparison_rows if row.get("split") == "oos"]
    if not oos_rows:
        return "inconclusive_unit_corrected_atr_no_oos_rows_no_authority"
    best_dd_row = min(oos_rows, key=lambda row: as_float(row.get("drawdown_percent")) or float("inf"))
    dd_delta = as_float(best_dd_row.get("drawdown_percent_delta_vs_f68f"))
    pf_delta = as_float(best_dd_row.get("profit_factor_delta_vs_f68f"))
    tpd = as_float(best_dd_row.get("trades_per_day"))
    if dd_delta is not None and dd_delta < 0 and (pf_delta or 0.0) > -0.25 and tpd is not None and tpd <= 10.0:
        return "preserved_clue_unit_corrected_atr_dd_direction_improved_no_authority"
    return "negative_or_inconclusive_unit_corrected_atr_runtime_repair_observation_no_authority"


def build_summary(payload: Mapping[str, Any]) -> dict[str, Any]:
    comparison_rows = payload.get("comparison_vs_f68f") or []
    oos_rows = [row for row in comparison_rows if row.get("split") == "oos"]
    best_oos_low_dd = min(oos_rows, key=lambda row: as_float(row.get("drawdown_percent")) or float("inf")) if oos_rows else {}
    return {
        "run_id": RUN_ID,
        "status": payload.get("status"),
        "judgment": payload.get("judgment"),
        "attempt_count": len(payload.get("attempts") or []),
        "runtime_receipt_rows": len(payload.get("runtime_receipt") or []),
        "effective_sltp_rows": len(payload.get("effective_sltp") or []),
        "signature_collapse_rows": payload.get("signature_collapse") or [],
        "best_oos_low_dd": best_oos_low_dd,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_outputs(payload: Mapping[str, Any]) -> None:
    write_json(RUN_ROOT / "run_manifest.json", payload)
    write_json(RUN_ROOT / "frontier68J_unit_corrected_atr_runtime_repair_execution_result.json", payload)
    write_json(RUN_ROOT / "frontier68J_unit_corrected_atr_runtime_repair_summary.json", build_summary(payload))
    write_csv(RUN_ROOT / "frontier68J_variant_plan.csv", payload.get("variant_plan", []))
    write_csv(RUN_ROOT / "frontier68J_local_verification.csv", payload.get("local_verification", {}).get("rows", []))
    write_csv(RUN_ROOT / "frontier68J_runtime_probe_receipt.csv", payload.get("runtime_receipt", []))
    write_csv(RUN_ROOT / "frontier68J_gap_classification.csv", payload.get("gap_classification", []))
    write_csv(RUN_ROOT / "frontier68J_comparison_vs_f68f.csv", payload.get("comparison_vs_f68f", []))
    write_csv(RUN_ROOT / "frontier68J_effective_atr_sltp_summary.csv", payload.get("effective_sltp", []))
    write_csv(RUN_ROOT / "frontier68J_signature_collapse.csv", payload.get("signature_collapse", []))
    write_csv(REVIEWS_ROOT / "frontier68J_runtime_probe_receipt_review.csv", payload.get("runtime_receipt", []))
    write_csv(REVIEWS_ROOT / "frontier68J_gap_classification_review.csv", payload.get("gap_classification", []))
    write_csv(REVIEWS_ROOT / "frontier68J_comparison_vs_f68f_review.csv", payload.get("comparison_vs_f68f", []))
    write_csv(REVIEWS_ROOT / "frontier68J_effective_atr_sltp_summary_review.csv", payload.get("effective_sltp", []))
    write_csv(REVIEWS_ROOT / "frontier68J_signature_collapse_review.csv", payload.get("signature_collapse", []))
    write_md(REVIEWS_ROOT / "frontier68J_unit_corrected_atr_runtime_repair_probe_report.md", report_lines(payload))
    write_md(REVIEWS_ROOT / "frontier68J_gate_audit.md", gate_audit_lines(payload))
    write_grok_receipt(payload)
    write_review_index()


def report_lines(payload: Mapping[str, Any]) -> list[str]:
    summary = build_summary(payload)
    lines = [
        "# F68J Unit-Corrected ATR Runtime Repair Probe(F68J 단위 보정 평균진폭 런타임 수리 탐침)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- parent_run_id(상위 실행 ID): `{PARENT_RUN_ID}`",
        f"- source_run_id(원천 실행 ID): `{SOURCE_RUN_ID}`",
        f"- status(상태): `{payload.get('status')}`",
        f"- judgment(판정): `{payload.get('judgment')}`",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "Action(행동): F68F ONNX/feature/signal path(F68F 온엑스/피처/신호 경로)를 고정하고 uncapped unit-corrected ATR SL/TP(무상한 단위 보정 평균진폭 손절/익절) 세 변형을 MT5 Strategy Tester(MT5 전략 테스터)에서 실행했다.",
        "",
        "Effect(효과): F68H의 180/260 cap collapse(상한 붕괴)를 반복하는지 먼저 확인하고, 그 다음 F68F 대비 DD/PF/trades/day(손실폭/수익 팩터/일 거래 수) 방향을 본다.",
        "",
        "## Local Verification(로컬 검증)",
        "",
        "| check(검사) | status(상태) | detail(상세) | effect(효과) |",
        "|---|---:|---|---|",
    ]
    for row in payload.get("local_verification", {}).get("rows", []):
        lines.append(f"| {row.get('check_name')} | {row.get('status')} | {row.get('detail')} | {row.get('effect')} |")
    lines.extend(
        [
            "",
            "## Runtime KPI(런타임 핵심 성과 지표)",
            "",
            "| variant(변형) | split(분할) | period(기간) | net(순수익) | PF(수익 팩터) | DD%(손실폭) | trades/day(일 거래 수) | trades(거래) | signal diff(신호 차이) | feature diff(피처 차이) |",
            "|---|---|---|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for row in payload.get("comparison_vs_f68f", []):
        lines.append(
            "| {variant} | {split} | {period} | {net} | {pf} | {dd} | {tpd} | {trades} | {sig} | {feat} |".format(
                variant=row.get("variant_id"),
                split=row.get("split"),
                period=row.get("period"),
                net=fmt(row.get("net_profit")),
                pf=fmt(row.get("profit_factor")),
                dd=fmt(row.get("drawdown_percent")),
                tpd=fmt(row.get("trades_per_day")),
                trades=fmt(row.get("trade_count")),
                sig=fmt(row.get("signal_count_diff")),
                feat=fmt(row.get("feature_ready_diff")),
            )
        )
    lines.extend(
        [
            "",
            "## Effective SL/TP(실효 손절/익절)",
            "",
            "| variant(변형) | split(분할) | ATR min/max(평균진폭 최소/최대) | SL min/max(손절 최소/최대) | TP min/max(익절 최소/최대) | SL/ATR mean(손절/평균진폭 평균) | TP/ATR mean(익절/평균진폭 평균) | F68H cap match(F68H 상한 일치) |",
            "|---|---|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for row in payload.get("effective_sltp", []):
        lines.append(
            "| {variant} | {split} | {atr_min}/{atr_max} | {sl_min}/{sl_max} | {tp_min}/{tp_max} | {sl_ratio} | {tp_ratio} | {cap_match} |".format(
                variant=row.get("variant_id"),
                split=row.get("split"),
                atr_min=fmt(row.get("atr_min")),
                atr_max=fmt(row.get("atr_max")),
                sl_min=fmt(row.get("open_sl_min")),
                sl_max=fmt(row.get("open_sl_max")),
                tp_min=fmt(row.get("open_tp_min")),
                tp_max=fmt(row.get("open_tp_max")),
                sl_ratio=fmt(row.get("sl_over_atr_mean")),
                tp_ratio=fmt(row.get("tp_over_atr_mean")),
                cap_match=row.get("matches_f68h_cap_signature"),
            )
        )
    lines.extend(
        [
            "",
            "## Signature Check(서명 점검)",
            "",
            "| split(분할) | variants(변형 수) | effective signatures(실효 서명 수) | KPI signatures(KPI 서명 수) | effective collapsed(실효 붕괴) | KPI collapsed(KPI 붕괴) |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )
    for row in payload.get("signature_collapse", []):
        lines.append(
            f"| {row.get('split')} | {row.get('variant_count')} | {row.get('effective_signature_count')} | {row.get('kpi_signature_count')} | {row.get('effective_collapsed_all_variants')} | {row.get('kpi_collapsed_all_variants')} |"
        )
    best = summary.get("best_oos_low_dd") or {}
    lines.extend(
        [
            "",
            "## Comparison Boundary(비교 경계)",
            "",
            f"- F68F OOS reference(F68F 표본외 기준): PF `1.18`, DD `19.57%`, trades/day `4.779487`.",
            f"- F68J best OOS low-DD row(F68J 표본외 최저 손실폭 행): variant `{best.get('variant_id', '')}`, PF `{fmt(best.get('profit_factor'))}`, DD `{fmt(best.get('drawdown_percent'))}`, trades/day `{fmt(best.get('trades_per_day'))}`.",
            "- This is runtime probe observation only(런타임 탐침 관찰 전용).",
            f"- next_action(다음 행동): `{NEXT_RUN_ID}` result review or closeout decision(결과 검토 또는 마감 결정).",
        ]
    )
    return lines


def gate_audit_lines(payload: Mapping[str, Any]) -> list[str]:
    return [
        "# F68J Gate Audit(F68J 게이트 감사)",
        "",
        f"- Grok pre-probe review(그록 탐침 전 검토): `{rel(GROK_CLEAN)}`.",
        f"- local verification rows(로컬 검증 행): `{len(payload.get('local_verification', {}).get('rows', []))}`.",
        f"- attempts materialized(시도 물질화): `{len(payload.get('attempts') or [])}`.",
        f"- runtime receipt rows(런타임 영수증 행): `{len(payload.get('runtime_receipt') or [])}`.",
        f"- effective SL/TP rows(실효 손절/익절 행): `{len(payload.get('effective_sltp') or [])}`.",
        f"- signature rows(서명 행): `{len(payload.get('signature_collapse') or [])}`.",
        f"- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
        "- forbidden claims(금지 주장): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성).",
    ]


def write_grok_receipt(payload: Mapping[str, Any]) -> None:
    receipt = payload.get("grok_receipt", {})
    lines = [
        "# F68J Grok Pre-Probe Receipt(F68J 그록 탐침 전 영수증)",
        "",
        f"- trigger_reason(트리거 이유): `{receipt.get('trigger_reason')}`",
        f"- review_size(검토 크기): `{receipt.get('review_size')}`",
        f"- prompt_identity(프롬프트 정체성): `{receipt.get('prompt_path')}` sha256 `{receipt.get('prompt_sha256')}`",
        f"- grok_output_identity(Grok 출력 정체성): `{receipt.get('clean_output_path')}` sha256 `{receipt.get('clean_output_sha256')}`",
        "- advice_classification(조언 분류): accepted(수용)=run F68J as unit-corrected ATR probe(F68J 단위 보정 평균진폭 탐침 실행), rejected(거절)=strong claims/capped retune/scope expansion(강한 주장/상한 재조정/범위 확장), needs_local_verification(로컬 검증 필요)=caps zero, lineage, tester parity, telemetry differentiation, KPI vs F68F(상한 0/계보/테스터 동등성/기록 구분/KPI 비교).",
        f"- local_verification(로컬 검증): `passed={payload.get('local_verification', {}).get('passed')}`.",
        f"- forbidden_claim_check(금지 주장 확인): `{receipt.get('forbidden_claim_check')}`",
        f"- final_codex_direction(최종 Codex 방향): `{receipt.get('final_codex_direction')}`",
    ]
    write_md(GROK_PACKET_ROOT / "f68j_pre_unit_corrected_atr_runtime_probe_receipt.md", lines)


def write_review_index() -> None:
    path = REVIEWS_ROOT / "review_index.md"
    block = [
        "",
        "## F68J Unit-Corrected ATR Runtime Repair Probe(F68J 단위 보정 평균진폭 런타임 수리 탐침)",
        "",
        "- `frontier68J_unit_corrected_atr_runtime_repair_probe_report.md`: F68J unit-corrected ATR runtime repair probe(F68J 단위 보정 평균진폭 런타임 수리 탐침)",
        "- `frontier68J_runtime_probe_receipt_review.csv`: F68J runtime receipt(F68J 런타임 영수증)",
        "- `frontier68J_effective_atr_sltp_summary_review.csv`: F68J effective ATR SL/TP summary(F68J 실효 평균진폭 손절/익절 요약)",
        "- `frontier68J_signature_collapse_review.csv`: F68J signature collapse check(F68J 서명 붕괴 점검)",
        f"Next action(다음 행동): `{NEXT_RUN_ID}`",
    ]
    text = io_path(path).read_text(encoding="utf-8-sig") if path_exists(path) else "# Review Index(검토 색인)\n"
    marker = "## F68J Unit-Corrected ATR Runtime Repair Probe"
    if marker not in text:
        text = text.rstrip() + "\n" + "\n".join(block).rstrip() + "\n"
        io_path(path).write_text(text, encoding="utf-8-sig")


def update_state_and_ledgers(payload: Mapping[str, Any]) -> None:
    summary = build_summary(payload)
    best = summary.get("best_oos_low_dd") or {}
    runtime_rows = payload.get("runtime_receipt") or []
    signal_gap_rows = sum(1 for row in runtime_rows if str(row.get("signal_count_diff")) not in {"0", "0.0", ""})
    feature_gap_rows = sum(1 for row in runtime_rows if str(row.get("feature_ready_diff")) not in {"0", "0.0", ""})
    collapsed_rows = sum(
        1 for row in payload.get("signature_collapse", []) if str(row.get("effective_collapsed_all_variants")) == "True"
    )
    row = {
        "ledger_row_id": f"{RUN_ID}__unit_corrected_atr_runtime_probe",
        "row_id": f"{RUN_ID}__unit_corrected_atr_runtime_probe",
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "subrun_id": "unit_corrected_atr_runtime_probe",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "validation_oos_unit_corrected_atr_runtime_probe(검증/표본외 단위 보정 평균진폭 런타임 탐침)",
        "tier_scope": "Tier A+B planned(티어 A+B 계획)",
        "kpi_scope": "runtime_risk_envelope_kpi_and_effective_sltp(런타임 위험 봉투 KPI 및 실효 손절익절)",
        "scoreboard_lane": "runtime_probe(런타임 탐침)",
        "status": payload.get("status"),
        "judgment": payload.get("judgment"),
        "path": f"stages/{STAGE_ID}/03_reviews/frontier68J_unit_corrected_atr_runtime_repair_probe_report.md",
        "primary_kpi": (
            f"best_oos_variant={best.get('variant_id', '')};"
            f"oos_pf={fmt(best.get('profit_factor'))};"
            f"oos_dd={fmt(best.get('drawdown_percent'))};"
            f"oos_tpd={fmt(best.get('trades_per_day'))}"
        ),
        "guardrail_kpi": (
            f"attempts={len(payload.get('attempts') or [])};"
            f"signal_gap_rows={signal_gap_rows};"
            f"feature_gap_rows={feature_gap_rows};"
            f"effective_signature_collapse_rows={collapsed_rows}"
        ),
        "external_verification_status": "completed" if runtime_rows else "out_of_scope_by_claim",
        "notes": "F68J tests uncapped unit-corrected ATR semantics on the exact F68F ONNX path; observation only.",
        "run_number": "frontier68J",
        "date": str(payload.get("created_at_utc", ""))[:10],
        "decision": "proceed_to_f68k_result_review_or_stage_closeout_decision",
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": f"stages/{STAGE_ID}/03_reviews/frontier68J_unit_corrected_atr_runtime_repair_probe_report.md",
        "gate_audit_path": f"stages/{STAGE_ID}/03_reviews/frontier68J_gate_audit.md",
        "created_at": payload.get("created_at_utc"),
        "attempt_count": len(payload.get("attempts") or []),
        "runtime_attempt_rows": len(runtime_rows),
        "work_family": "runtime_backtest(런타임/백테스트)",
        "run_type": "mt5_runtime_unit_corrected_atr_probe(MT5 런타임 단위 보정 평균진폭 탐침)",
        "input_run_id": PARENT_RUN_ID,
        "output_path": f"stages/{STAGE_ID}/02_runs/{RUN_ID}/frontier68J_unit_corrected_atr_runtime_repair_execution_result.json",
        "result_path": f"stages/{STAGE_ID}/03_reviews/frontier68J_unit_corrected_atr_runtime_repair_probe_report.md",
        "net_profit": best.get("net_profit", ""),
        "profit_factor": best.get("profit_factor", ""),
        "drawdown": best.get("drawdown_percent", ""),
        "recovery_factor": best.get("recovery_factor", ""),
        "trade_count": best.get("trade_count", ""),
        "result_status": payload.get("judgment"),
        "long_trade_count": "",
        "short_trade_count": "",
        "evidence_boundary": "runtime_probe_observation_only(런타임 탐침 관찰 전용)",
        "next_action": NEXT_RUN_ID,
        "question": "Does unit-corrected uncapped ATR avoid F68H signature collapse while improving risk versus F68F?",
        "source_authority": "mt5_strategy_tester_runtime_probe_observation(MT5 전략 테스터 런타임 탐침 관찰)",
        "trade_density_per_feature_day": best.get("trades_per_day", ""),
        "max_drawdown_amount": "",
    }
    upsert_ledger(ROOT / "docs/registers/run_registry.csv", "run_id", row)
    upsert_ledger(ROOT / "docs/registers/alpha_run_ledger.csv", "ledger_row_id", row)
    upsert_ledger(REVIEWS_ROOT / "stage_run_ledger.csv", "ledger_row_id", row, source_header=ROOT / "docs/registers/alpha_run_ledger.csv")
    write_current_state(payload)
    write_selection_status(payload)


def write_current_state(payload: Mapping[str, Any]) -> None:
    created_at = payload.get("created_at_utc")
    lines = [
        f"current_stage_id: {STAGE_ID}",
        f"active_stage: {STAGE_ID}",
        f"current_run_id: {NEXT_RUN_ID}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {payload.get('status')}",
        f"current_judgment: {payload.get('judgment')}",
        f"next_stage_id: {STAGE_ID}",
        f"next_run_id: {NEXT_RUN_ID}",
        "runtime_probe_status: f68j_completed_or_attempted_unit_corrected_atr_probe_next_review_required(F68J 단위 보정 평균진폭 탐침 완료 또는 시도, 다음 검토 필요)",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        f"updated_at_utc: '{created_at}'",
        "notes:",
        '  - "F68J action(행동): F68F ONNX/feature path(F68F 온엑스/피처 경로)를 고정하고 unit-corrected ATR SL/TP(단위 보정 평균진폭 손절/익절)를 MT5 Strategy Tester(MT5 전략 테스터)에서 실행 또는 물질화했다."',
        '  - "Effect(효과): F68H의 180/260 cap collapse(상한 붕괴)가 반복되는지 telemetry(기록)로 먼저 확인하게 했다."',
        f'  - "Next action(다음 행동): `{NEXT_RUN_ID}`에서 F68J result review(결과 검토) 또는 stage closeout decision(단계 마감 결정)을 한다."',
        '  - "Continuity anchor(연속성 고정점): F68J는 immediate repair probe(즉시 수리 탐침)이며, broader exploration(더 넓은 탐색)은 feature set(피처 묶음), label/target(라벨/목표), model family(모델 계열), trade shape(거래 형태), risk logic(위험 로직), regime/session split(장세/세션 분할)을 계속 회전한다."',
        '  - "Boundary(경계): runtime probe observation only(런타임 탐침 관찰 전용), no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."',
    ]
    io_path(ROOT / "docs/workspace/workspace_state.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8-sig")
    write_md(
        ROOT / "docs/context/current_working_state.md",
        [
            "# Current Working State(현재 작업 상태)",
            "",
            f"Updated(갱신): {created_at}",
            "",
            f"Active stage(활성 단계): `{STAGE_ID}`",
            "",
            f"Current run(현재 실행): `{NEXT_RUN_ID}`",
            "",
            f"Latest completed run(최근 완료 실행): `{RUN_ID}`",
            "",
            "## Current Truth(현재 진실)",
            "",
            "Action(행동): F68J unit-corrected ATR runtime repair probe(F68J 단위 보정 평균진폭 런타임 수리 탐침)를 실행 또는 물질화했다.",
            "",
            "Effect(효과): F68H capped ATR signature collapse(F68H 상한 평균진폭 서명 붕괴)를 반복하는지와 F68F 대비 DD/PF/trades/day(손실폭/수익 팩터/일 거래 수) 방향을 기록했다.",
            "",
            f"- F68J status(F68J 상태): `{payload.get('status')}`.",
            f"- F68J judgment(F68J 판정): `{payload.get('judgment')}`.",
            f"- next_run(다음 실행): `{NEXT_RUN_ID}`.",
            "",
            f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
            "",
            "## Continuity Anchor(연속성 고정점)",
            "",
            "Action(행동): goal resume(목표 재개)나 context compaction(맥락 압축) 뒤에도 F68J/F68K를 risk repair probe/review(위험 수리 탐침/검토)로 이어가되, F68 고착으로 해석하지 않는다.",
            "",
            "Effect(효과): feature set(피처 묶음), label/target(라벨/목표), model family(모델 계열), trade shape(거래 형태), risk logic(위험 로직), regime/session split(장세/세션 분할)을 계속 바꿔가며 새 가설을 열 수 있게 한다.",
        ],
    )


def write_selection_status(payload: Mapping[str, Any]) -> None:
    write_md(
        STAGE_ROOT / "04_selected/selection_status.md",
        [
            "# F68 Selection Status(F68 선택 상태)",
            "",
            f"- stage(단계): `{STAGE_ID}`",
            f"- current_run(현재 실행): `{NEXT_RUN_ID}`",
            f"- latest_completed_run(최근 완료 실행): `{RUN_ID}`",
            f"- status(상태): `{payload.get('status')}`",
            "- selected_baseline(선택 기준선): `not_claimed(주장 없음)`",
            "- runtime_authority(런타임 권위): `not_claimed(주장 없음)`",
            "- operating_promotion(운영 승격): `not_claimed(주장 없음)`",
            "- live_readiness(실거래 준비): `not_claimed(주장 없음)`",
            "- Goal Achieve(목표 달성): `not_claimed(주장 없음)`",
            "- completed_action(완료 행동): F68J unit-corrected ATR MT5 runtime repair probe(F68J 단위 보정 평균진폭 MT5 런타임 수리 탐침).",
            f"- report(보고서): `stages/{STAGE_ID}/03_reviews/frontier68J_unit_corrected_atr_runtime_repair_probe_report.md`",
            f"- next_action(다음 행동): `{NEXT_RUN_ID}` result review or closeout decision(결과 검토 또는 마감 결정).",
            "- continuity_anchor(연속성 고정점): F68J/F68K는 immediate repair probe/review(즉시 수리 탐침/검토)이며, broader exploration(더 넓은 탐색)은 feature set(피처 묶음), label/target(라벨/목표), model family(모델 계열), trade shape(거래 형태), risk logic(위험 로직), regime/session split(장세/세션 분할)을 계속 회전한다.",
            f"- boundary(경계): `{CLAIM_BOUNDARY}`.",
        ],
    )


def compact_status(payload: Mapping[str, Any]) -> dict[str, Any]:
    summary = build_summary(payload)
    return {
        "run_id": RUN_ID,
        "status": payload.get("status"),
        "judgment": payload.get("judgment"),
        "attempt_count": len(payload.get("attempts") or []),
        "runtime_receipt_rows": len(payload.get("runtime_receipt") or []),
        "effective_sltp_rows": len(payload.get("effective_sltp") or []),
        "signature_collapse_rows": summary.get("signature_collapse_rows"),
        "best_oos_low_dd": summary.get("best_oos_low_dd"),
        "next_run_id": NEXT_RUN_ID,
    }


if __name__ == "__main__":
    raise SystemExit(main())
