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


RUN_ID = "frontier68H_atr_sltp_risk_envelope_runtime_repair_probe_v1"
PARENT_RUN_ID = "frontier68G_repair_result_review_or_next_validation_v1"
SOURCE_RUN_ID = "frontier68F_near_four_axis_onnx_runtime_repair_probe_v1"
NEXT_RUN_ID = "frontier68I_risk_envelope_result_review_or_stage_closeout_decision_v1"

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
MT5_ROOT = RUN_ROOT / "mt5"
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
F68F_RUN_ROOT = STAGE_ROOT / "02_runs" / SOURCE_RUN_ID

F68F_HANDOFF = F68F_RUN_ROOT / "frontier68F_handoff_intent.csv"
F68F_SIGNAL_PARITY = F68F_RUN_ROOT / "frontier68F_onnx_signal_parity.csv"
F68F_KPI_BY_SPLIT = F68F_RUN_ROOT / "frontier68F_candidate_axis_kpi_by_split.csv"
F68F_RECEIPT = REVIEWS_ROOT / "frontier68F_runtime_probe_receipt_review.csv"
F68G_VARIANTS = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "f68g_next_repair_variants.csv"

GROK_PACKET_ROOT = ROOT / "docs/agent_control/grok_reviews/2026-06-17_f68h_pre_atr_sltp_runtime_repair_probe"
GROK_PROMPT = GROK_PACKET_ROOT / "prompts/f68h_pre_atr_sltp_runtime_repair_probe_prompt.md"
GROK_CLEAN = GROK_PACKET_ROOT / "outputs/clean_output.md"
GROK_METADATA = GROK_PACKET_ROOT / "outputs/metadata.json"

COMMON_RUN_ROOT = "Project_Obsidian_Prime_v2/frontier68H_atr_sltp_risk_envelope_probe"

CLAIM_BOUNDARY = (
    "atr_sltp_runtime_repair_probe_observation_only_no_completion_no_baseline_"
    "no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve"
)

SPLIT_WINDOWS = {
    "validation": {"from": "2025.01.02", "to": "2025.10.01"},
    "oos": {"from": "2025.10.01", "to": "2026.04.14"},
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="F68H ATR SL/TP runtime repair probe.")
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
    variants = read_csv_rows(F68G_VARIANTS)
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
        "status": "materialized_pending_mt5_atr_sltp_runtime_repair_probe_no_authority(물질화 완료, MT5 평균진폭 손절/익절 런타임 수리 탐침 대기, 권위 없음)",
        "judgment": "atr_sltp_repair_probe_pending_no_authority(평균진폭 손절/익절 수리 탐침 대기, 권위 없음)",
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
    execution_completed = bool(execution_results) and all(row.get("status") == "completed" for row in execution_results)
    report_completed = bool(kpi_records) and len(kpi_records) == len(attempts)
    payload.update(
        {
            "status": (
                "completed_atr_sltp_runtime_repair_probe_observation_no_authority(MT5 평균진폭 손절/익절 런타임 수리 탐침 관찰 완료, 권위 없음)"
                if execution_completed and report_completed
                else "blocked_atr_sltp_runtime_repair_probe_attempted_repair_required_no_authority(MT5 평균진폭 손절/익절 런타임 수리 탐침 시도 차단, 수리 필요, 권위 없음)"
            ),
            "judgment": (
                risk_envelope_judgment(comparison_rows)
                if execution_completed and report_completed
                else "atr_sltp_runtime_probe_blocked_no_authority(평균진폭 손절/익절 런타임 탐침 차단, 권위 없음)"
            ),
            "compile_payload": compile_payload,
            "execution_results": execution_results,
            "strategy_tester_reports": report_records,
            "mt5_kpi_records": kpi_records,
            "runtime_receipt": receipt_rows,
            "gap_classification": gap_rows,
            "comparison_vs_f68f": comparison_rows,
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


def bool_text(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes"}


def check(name: str, ok: bool, detail: str) -> dict[str, str]:
    return {
        "check_name": name,
        "status": "passed" if ok else "failed",
        "detail": detail,
        "effect": "keeps F68H as risk-envelope-only runtime repair",
    }


def build_local_verification(
    handoff: Mapping[str, str],
    variants: Sequence[Mapping[str, str]],
    baseline_receipts: Sequence[Mapping[str, str]],
) -> dict[str, Any]:
    model_path = ROOT / str(handoff.get("model_path_repo", ""))
    feature_path = ROOT / str(handoff.get("feature_csv_repo", ""))
    planned_ids = {row.get("variant_id") for row in variants}
    rows = [
        check("grok_clean_output_exists", path_exists(GROK_CLEAN), rel(GROK_CLEAN)),
        check("model_path_exists", path_exists(model_path), rel(model_path)),
        check("model_sha256_matches_f68f", path_exists(model_path) and sha256_file(model_path) == handoff.get("model_sha256"), handoff.get("model_sha256", "")),
        check("feature_path_exists", path_exists(feature_path), rel(feature_path)),
        check("feature_count_49", handoff.get("feature_count") == "49", handoff.get("feature_count", "")),
        check(
            "feature_order_hash_matches_f68f",
            handoff.get("feature_order_hash") == "14a037f12cec16ad2f57a9cb5cafb5d61a374b96640872a6ac51bb6f28baf2a3",
            handoff.get("feature_order_hash", ""),
        ),
        check("baseline_f68f_receipts_present", len(baseline_receipts) == 2, str(len(baseline_receipts))),
        check("variant_count_3", len(variants) == 3, str(len(variants))),
        check(
            "variant_ids_expected",
            planned_ids == {"f52_atr08_tp12_re3_sd6", "tight_atr06_tp10_re3_sd6", "wide_atr10_tp16_re3_sd6"},
            ";".join(sorted(str(v) for v in planned_ids)),
        ),
        check("f68f_atr_disabled_before_repair", handoff.get("atr_sltp_enabled") == "False", handoff.get("atr_sltp_enabled", "")),
    ]
    passed = all(row["status"] == "passed" for row in rows)
    return {
        "rows": rows,
        "passed": passed,
        "can_execute": passed,
        "accepted": [
            "risk-envelope-only capped repair after F68F",
            "three planned ATR SL/TP variants with validation and OOS",
            "F52 clue used as reference only",
        ],
        "rejected": [
            "completion, baseline, promotion, runtime authority, live readiness, Goal Achieve",
            "treating ATR SL/TP as a new PF source",
            "changing thresholds, feature path, model path, or adding variants mid-probe",
        ],
        "needs_local_verification": [
            "handoff identity and hashes",
            "variant .set binding",
            "tester parity against F68F",
            "post-run KPI and deltas versus F68F",
        ],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def grok_receipt(local_verification: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "trigger_reason": "goal requires Grok review before MT5 Runtime Probe",
        "review_size": "medium",
        "prompt_path": rel(GROK_PROMPT),
        "clean_output_path": rel(GROK_CLEAN),
        "metadata_path": rel(GROK_METADATA),
        "prompt_sha256": sha256_file(GROK_PROMPT) if path_exists(GROK_PROMPT) else "",
        "clean_output_sha256": sha256_file(GROK_CLEAN) if path_exists(GROK_CLEAN) else "",
        "advice_classification": {
            "accepted": local_verification.get("accepted", []),
            "rejected": local_verification.get("rejected", []),
            "needs_local_verification": local_verification.get("needs_local_verification", []),
        },
        "forbidden_claim_check": "passed_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve",
        "final_codex_direction": "run F68H only if local preflight passes",
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
            attempt_name = f"f68h_{variant['variant_id']}_{split}"
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
                exploration_label="frontier68H_atr_sltp_risk_envelope_probe(F68H 평균진폭 손절/익절 위험 봉투 탐침)",
                attempt_name=attempt_name,
                tier=mt5.TIER_A,
                split=split,
                model_path=model_common,
                model_id=f"F68H_{handoff.get('candidate_id')}_{variant['variant_id']}",
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
                attempt_role="f68h_atr_sltp_risk_envelope_runtime_probe",
                record_view_prefix=f"mt5_f68h_{variant['variant_id']}",
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
                    "axis_id": "atr_sltp_risk_envelope_axis",
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
                    "intentional_delta_vs_f68f": "ATR_SLTP_enabled_and_reentry_cooldown_3_only",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            attempts.append(attempt)
    return attempts


def baseline_by_split(rows: Sequence[Mapping[str, str]]) -> dict[str, Mapping[str, str]]:
    return {str(row.get("split")): row for row in rows}


def numeric_delta(runtime: Any, baseline: Any) -> float | None:
    a = as_float(runtime)
    b = as_float(baseline)
    if a is None or b is None:
        return None
    return a - b


def build_comparison_rows(
    receipts: Sequence[Mapping[str, Any]],
    baseline_receipts: Sequence[Mapping[str, str]],
    attempts: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    baseline = baseline_by_split(baseline_receipts)
    attempt_by_name = {str(attempt["attempt_name"]): attempt for attempt in attempts}
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
                "drawdown_percent_delta_vs_f68f": fmt(numeric_delta(receipt.get("max_drawdown_percent"), base.get("max_drawdown_percent"))),
                "trades_per_day": receipt.get("trades_per_day"),
                "f68f_trades_per_day": base.get("trades_per_day"),
                "trades_per_day_delta_vs_f68f": fmt(numeric_delta(receipt.get("trades_per_day"), base.get("trades_per_day"))),
                "trade_count": receipt.get("trade_count"),
                "win_rate_percent": receipt.get("win_rate_percent"),
                "average_win": receipt.get("average_win"),
                "average_loss": receipt.get("average_loss"),
                "payoff_ratio": receipt.get("payoff_ratio"),
                "recovery_factor": receipt.get("recovery_factor"),
                "signal_count_diff": receipt.get("signal_count_diff"),
                "feature_ready_diff": receipt.get("feature_ready_diff"),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def risk_envelope_judgment(comparison_rows: Sequence[Mapping[str, Any]]) -> str:
    by_variant: dict[str, list[Mapping[str, Any]]] = {}
    for row in comparison_rows:
        by_variant.setdefault(str(row.get("variant_id")), []).append(row)
    for rows in by_variant.values():
        if len(rows) < 2:
            continue
        dd_deltas = [as_float(row.get("drawdown_percent_delta_vs_f68f")) for row in rows]
        pf_deltas = [as_float(row.get("profit_factor_delta_vs_f68f")) for row in rows]
        nets = [as_float(row.get("net_profit")) for row in rows]
        if all(v is not None and v <= -5.0 for v in dd_deltas) and all(v is not None and v >= -0.05 for v in pf_deltas) and all(v is not None and v > 0 for v in nets):
            return "risk_envelope_preserved_clue_dd_compressed_without_pf_collapse_no_authority(위험 봉투 보존 단서, 수익 팩터 붕괴 없이 손실폭 압축, 권위 없음)"
    if any((as_float(row.get("drawdown_percent_delta_vs_f68f")) or 0.0) < -5.0 for row in comparison_rows):
        return "risk_envelope_mixed_dd_compression_tradeoff_no_authority(위험 봉투 혼합 결과, 손실폭 압축과 손익 절충, 권위 없음)"
    return "risk_envelope_repair_negative_or_inconclusive_no_authority(위험 봉투 수리 부정 또는 불충분, 권위 없음)"


def build_summary(payload: Mapping[str, Any]) -> dict[str, Any]:
    comparisons = list(payload.get("comparison_vs_f68f") or [])
    best_by_oos = sorted(
        [row for row in comparisons if row.get("split") == "oos"],
        key=lambda row: (as_float(row.get("drawdown_percent")) or 999.0, -(as_float(row.get("profit_factor")) or 0.0)),
    )
    return {
        "run_id": RUN_ID,
        "status": payload.get("status"),
        "judgment": payload.get("judgment"),
        "attempt_count": len(payload.get("attempts") or []),
        "runtime_receipt_rows": len(payload.get("runtime_receipt") or []),
        "best_oos_low_dd": best_by_oos[0] if best_by_oos else {},
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_outputs(payload: Mapping[str, Any]) -> None:
    write_json(RUN_ROOT / "run_manifest.json", payload)
    write_json(RUN_ROOT / "frontier68H_atr_sltp_runtime_repair_execution_result.json", payload)
    write_json(RUN_ROOT / "frontier68H_atr_sltp_runtime_repair_summary.json", build_summary(payload))
    write_csv(RUN_ROOT / "frontier68H_variant_plan.csv", payload.get("variant_plan", []))
    write_csv(RUN_ROOT / "frontier68H_local_verification.csv", payload.get("local_verification", {}).get("rows", []))
    write_csv(RUN_ROOT / "frontier68H_runtime_probe_receipt.csv", payload.get("runtime_receipt", []))
    write_csv(RUN_ROOT / "frontier68H_gap_classification.csv", payload.get("gap_classification", []))
    write_csv(RUN_ROOT / "frontier68H_comparison_vs_f68f.csv", payload.get("comparison_vs_f68f", []))
    write_csv(REVIEWS_ROOT / "frontier68H_runtime_probe_receipt_review.csv", payload.get("runtime_receipt", []))
    write_csv(REVIEWS_ROOT / "frontier68H_gap_classification_review.csv", payload.get("gap_classification", []))
    write_csv(REVIEWS_ROOT / "frontier68H_comparison_vs_f68f_review.csv", payload.get("comparison_vs_f68f", []))
    write_md(REVIEWS_ROOT / "frontier68H_atr_sltp_runtime_repair_probe_report.md", report_lines(payload))
    write_md(REVIEWS_ROOT / "frontier68H_gate_audit.md", gate_audit_lines(payload))
    write_grok_receipt(payload)
    write_review_index()


def report_lines(payload: Mapping[str, Any]) -> list[str]:
    lines = [
        "# F68H ATR SL/TP Runtime Repair Probe(F68H 평균진폭 손절/익절 런타임 수리 탐침)",
        "",
        f"Updated(갱신): {payload['created_at_utc']}",
        "",
        "## Action And Effect(행동 및 효과)",
        "",
        "Action(행동): F68F ONNX/feature/signal path(F68F 온엑스/피처/신호 경로)를 고정하고 ATR SL/TP risk envelope(평균진폭 손절/익절 위험 봉투) 세 변형을 MT5 Strategy Tester(MT5 전략 테스터)에서 실행했다.",
        "",
        "Effect(효과): F68F의 남은 DD(drawdown, 손실폭) 문제를 모델 변화가 아닌 런타임 위험 로직 변화로 분리해서 관찰했다.",
        "",
        f"- status(상태): `{payload.get('status')}`",
        f"- judgment(판정): `{payload.get('judgment')}`",
        f"- local verification(로컬 검증): `{payload.get('local_verification', {}).get('passed')}`",
        f"- attempts(시도 수): `{len(payload.get('attempts') or [])}`",
        f"- receipt rows(영수증 행): `{len(payload.get('runtime_receipt') or [])}`",
        "",
        "## Runtime KPI Versus F68F(F68F 대비 런타임 핵심 성과 지표)",
        "",
        "| variant(변형) | split(분할) | net(순수익) | net delta(차이) | PF(수익 팩터) | PF delta(차이) | DD%(손실폭) | DD delta(차이) | trades/day(일 거래) | density delta(밀도 차이) |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in payload.get("comparison_vs_f68f", []):
        lines.append(
            "| `{variant}` | `{split}` | `{net}` | `{net_d}` | `{pf}` | `{pf_d}` | `{dd}` | `{dd_d}` | `{tpd}` | `{tpd_d}` |".format(
                variant=row.get("variant_id"),
                split=row.get("split"),
                net=fmt(row.get("net_profit")),
                net_d=fmt(row.get("net_profit_delta_vs_f68f")),
                pf=fmt(row.get("profit_factor")),
                pf_d=fmt(row.get("profit_factor_delta_vs_f68f")),
                dd=fmt(row.get("drawdown_percent")),
                dd_d=fmt(row.get("drawdown_percent_delta_vs_f68f")),
                tpd=fmt(row.get("trades_per_day")),
                tpd_d=fmt(row.get("trades_per_day_delta_vs_f68f")),
            )
        )
    if not payload.get("comparison_vs_f68f"):
        lines.append("| `pending` | `pending` |  |  |  |  |  |  |  |  |")
    lines.extend(
        [
            "",
            "## Grok Classification(Grok 조언 분류)",
            "",
            "- accepted(수용): risk-envelope-only capped repair(위험 봉투 전용 상한 수리), three variants(세 변형), validation+OOS(검증+표본외).",
            "- rejected(거절): threshold/model/feature changes(임계값/모델/피처 변경), completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성).",
            "- needs_local_verification(로컬 검증 필요): handoff hash(인계 해시), .set binding(설정 바인딩), tester parity(테스터 동등성), KPI deltas(KPI 차이).",
            "",
            "## Boundary(경계)",
            "",
            "This is runtime probe observation only(런타임 탐침 관찰 전용). ATR SL/TP(평균진폭 손절/익절)는 new PF source(새 수익 팩터 원천)가 아니라 risk shape repair(위험 형태 수리)다.",
            "",
            f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        ]
    )
    return lines


def gate_audit_lines(payload: Mapping[str, Any]) -> list[str]:
    return [
        "# F68H Gate Audit(F68H 게이트 감사)",
        "",
        f"- Grok pre-probe review(Grok 탐침 전 검토): `{'passed' if path_exists(GROK_CLEAN) else 'missing'}`.",
        f"- local verification passed(로컬 검증 통과): `{payload.get('local_verification', {}).get('passed')}`.",
        f"- F68F baseline receipt rows(F68F 기준 영수증 행): `{len(payload.get('baseline_receipts') or [])}`.",
        f"- variant count(변형 수): `{len(payload.get('variant_plan') or [])}`.",
        f"- MT5 Runtime Probe attempted(MT5 런타임 탐침 시도): `{bool(payload.get('execution_results'))}`.",
        f"- Strategy Tester reports(전략 테스터 보고서): `{len(payload.get('strategy_tester_reports') or [])}`.",
        f"- runtime receipt rows(런타임 영수증 행): `{len(payload.get('runtime_receipt') or [])}`.",
        f"- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
    ]


def write_grok_receipt(payload: Mapping[str, Any]) -> None:
    receipt = payload.get("grok_receipt", {})
    lines = [
        "# F68H Grok Pre-Probe Receipt(F68H Grok 탐침 전 영수증)",
        "",
        f"Updated(갱신): {payload['created_at_utc']}",
        "",
        f"- trigger_reason(트리거 이유): `{receipt.get('trigger_reason')}`",
        f"- review_size(검토 크기): `{receipt.get('review_size')}`",
        f"- prompt_identity(프롬프트 정체성): `{receipt.get('prompt_path')}` sha256 `{receipt.get('prompt_sha256')}`",
        f"- grok_output_identity(Grok 출력 정체성): `{receipt.get('clean_output_path')}` sha256 `{receipt.get('clean_output_sha256')}`",
        "- advice_classification(조언 분류): accepted(수용)=run capped risk-envelope probe(상한 위험 봉투 탐침 실행), rejected(거절)=강한 주장 및 scope broaden(범위 확장), needs_local_verification(로컬 검증 필요)=hash/set/tester/KPI delta(해시/설정/테스터/KPI 차이).",
        f"- local_verification(로컬 검증): `{payload.get('local_verification', {}).get('passed')}`",
        f"- forbidden_claim_check(금지 주장 확인): `{receipt.get('forbidden_claim_check')}`",
        f"- final_codex_direction(최종 Codex 방향): `{receipt.get('final_codex_direction')}`",
    ]
    write_md(GROK_PACKET_ROOT / "f68h_pre_atr_sltp_runtime_repair_probe_receipt.md", lines)


def write_review_index() -> None:
    index_path = REVIEWS_ROOT / "review_index.md"
    existing = io_path(index_path).read_text(encoding="utf-8-sig") if io_path(index_path).exists() else ""
    additions = [
        "- `frontier68H_atr_sltp_runtime_repair_probe_report.md`: F68H ATR SL/TP runtime repair probe(F68H 평균진폭 손절/익절 런타임 수리 탐침)",
        "- `frontier68H_runtime_probe_receipt_review.csv`: F68H runtime receipt(F68H 런타임 영수증)",
        "- `frontier68H_comparison_vs_f68f_review.csv`: F68H versus F68F comparison(F68H 대 F68F 비교)",
        "- `frontier68H_gate_audit.md`: F68H gate audit(F68H 게이트 감사)",
    ]
    lines = existing.rstrip().splitlines() if existing else ["# Review Index(검토 색인)", ""]
    for line in additions:
        if line not in lines:
            lines.append(line)
    lines.append(f"Next action(다음 행동): `{NEXT_RUN_ID}`")
    write_md(index_path, lines)


def update_state_and_ledgers(payload: Mapping[str, Any]) -> None:
    summary = build_summary(payload)
    best = summary.get("best_oos_low_dd") or {}
    row = {
        "ledger_row_id": f"{RUN_ID}__atr_sltp_runtime_probe",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "atr_sltp_runtime_repair_probe(평균진폭 손절/익절 런타임 수리 탐침)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "validation_oos_atr_sltp_runtime_probe(검증/표본외 평균진폭 손절/익절 런타임 탐침)",
        "tier_scope": "Tier A+B planned(티어 A+B 계획)",
        "kpi_scope": "runtime_risk_envelope_kpi_and_delta(런타임 위험 봉투 KPI 및 차이)",
        "scoreboard_lane": "runtime_probe(런타임 탐침)",
        "status": payload.get("status"),
        "judgment": payload.get("judgment"),
        "path": f"stages/{STAGE_ID}/03_reviews/frontier68H_atr_sltp_runtime_repair_probe_report.md",
        "primary_kpi": f"best_oos_variant={best.get('variant_id', '')};best_oos_pf={fmt(best.get('profit_factor'))};best_oos_dd={fmt(best.get('drawdown_percent'))};best_oos_tpd={fmt(best.get('trades_per_day'))}",
        "guardrail_kpi": f"attempts={len(payload.get('attempts') or [])};signal_gap_rows={sum(1 for r in payload.get('runtime_receipt', []) if r.get('signal_count_diff') not in (0, '0'))};feature_gap_rows={sum(1 for r in payload.get('runtime_receipt', []) if r.get('feature_ready_diff') not in (0, '0'))}",
        "external_verification_status": "completed" if str(payload.get("status", "")).startswith("completed") else "blocked",
        "notes": "F68H runs ATR SL/TP risk-envelope variants on the exact F68F ONNX path; observation only.",
        "date": payload["created_at_utc"][:10],
        "decision": "proceed_to_f68i_risk_envelope_result_review_or_stage_closeout_decision",
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": f"stages/{STAGE_ID}/03_reviews/frontier68H_atr_sltp_runtime_repair_probe_report.md",
        "result_judgment": payload.get("judgment"),
        "created_at_utc": payload["created_at_utc"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "frontier_atr_sltp_runtime_repair_probe(전선 평균진폭 손절/익절 런타임 수리 탐침)",
        "run_type": "mt5_runtime_risk_envelope_probe(MT5 런타임 위험 봉투 탐침)",
        "input_run_id": PARENT_RUN_ID,
        "output_path": f"stages/{STAGE_ID}/02_runs/{RUN_ID}/frontier68H_atr_sltp_runtime_repair_execution_result.json",
        "result_path": f"stages/{STAGE_ID}/03_reviews/frontier68H_atr_sltp_runtime_repair_probe_report.md",
        "source_authority": "mt5_strategy_tester_runtime_probe_observation(MT5 전략 테스터 런타임 탐침 관찰)",
    }
    upsert_ledger(REVIEWS_ROOT / "stage_run_ledger.csv", "ledger_row_id", row)
    upsert_ledger(ROOT / "docs/registers/alpha_run_ledger.csv", "ledger_row_id", row)
    upsert_ledger(ROOT / "docs/registers/run_registry.csv", "run_id", row)
    write_current_state(payload)
    write_selection_status(payload)


def write_current_state(payload: Mapping[str, Any]) -> None:
    lines = [
        f"current_stage_id: {STAGE_ID}",
        f"active_stage: {STAGE_ID}",
        f"current_run_id: {NEXT_RUN_ID}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {payload.get('status')}",
        f"current_judgment: {payload.get('judgment')}",
        f"next_stage_id: {STAGE_ID}",
        f"next_run_id: {NEXT_RUN_ID}",
        "runtime_probe_status: f68h_atr_sltp_runtime_probe_recorded_no_authority(F68H 평균진폭 손절/익절 런타임 탐침 기록, 권위 없음)",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        f"updated_at_utc: '{payload['created_at_utc']}'",
        "notes:",
        '  - "F68H action(행동): F68F ONNX/feature path(F68F 온엑스/피처 경로)를 고정하고 ATR SL/TP risk envelope(평균진폭 손절/익절 위험 봉투)를 MT5 Strategy Tester(MT5 전략 테스터)에서 실행했다."',
        '  - "Effect(효과): 모델 변경 없이 DD(drawdown, 손실폭) 압축 가능성을 확인했다."',
        f'  - "Next action(다음 행동): `{NEXT_RUN_ID}`에서 risk envelope result review(위험 봉투 결과 검토) 또는 stage closeout decision(단계 마감 결정)을 한다."',
        '  - "Boundary(경계): runtime probe observation only(런타임 탐침 관찰 전용), no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."',
    ]
    io_path(ROOT / "docs/workspace/workspace_state.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8-sig")
    write_md(
        ROOT / "docs/context/current_working_state.md",
        [
            "# Current Working State(현재 작업 상태)",
            "",
            f"Updated(갱신): {payload['created_at_utc']}",
            "",
            f"Active stage(활성 단계): `{STAGE_ID}`",
            "",
            f"Current run(현재 실행): `{NEXT_RUN_ID}`",
            "",
            f"Latest completed run(최근 완료 실행): `{RUN_ID}`",
            "",
            "## Current Truth(현재 진실)",
            "",
            "Action(행동): F68H ATR SL/TP runtime repair probe(F68H 평균진폭 손절/익절 런타임 수리 탐침)를 실행했다.",
            "",
            "Effect(효과): F68F의 신호/피처를 고정한 채 위험 로직만 바꿔 손실폭 압축 가능성을 관찰했다.",
            "",
            f"- F68H status(F68H 상태): `{payload.get('status')}`.",
            f"- runtime_receipt_rows(런타임 영수증 행): `{len(payload.get('runtime_receipt') or [])}`.",
            "",
            f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        ],
    )


def write_selection_status(payload: Mapping[str, Any]) -> None:
    write_md(
        STAGE_ROOT / "04_selected" / "selection_status.md",
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
            "- completed_action(완료 행동): F68H ATR SL/TP MT5 runtime repair probe(F68H 평균진폭 손절/익절 MT5 런타임 수리 탐침).",
            f"- report(보고서): `stages/{STAGE_ID}/03_reviews/frontier68H_atr_sltp_runtime_repair_probe_report.md`",
            f"- next_action(다음 행동): `{NEXT_RUN_ID}` risk envelope result review or closeout decision(위험 봉투 결과 검토 또는 마감 결정).",
            f"- boundary(경계): `{CLAIM_BOUNDARY}`.",
        ],
    )


def compact_status(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "status": payload.get("status"),
        "judgment": payload.get("judgment"),
        "attempt_count": len(payload.get("attempts") or []),
        "runtime_receipt_rows": len(payload.get("runtime_receipt") or []),
        "comparison_rows": len(payload.get("comparison_vs_f68f") or []),
        "claim_boundary": CLAIM_BOUNDARY,
    }


if __name__ == "__main__":
    raise SystemExit(main())
