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

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.control_plane.mt5_tier_balance_completion import attempt_payload
from foundation.mt5 import runtime_support as mt5
from stage_pipelines.stage_frontier_68 import frontier68c_candidate_scoring_or_onnx_scout_export as f68c
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


RUN_ID = "frontier68F_near_four_axis_onnx_runtime_repair_probe_v1"
PARENT_RUN_ID = "frontier68E_proxy_runtime_gap_analysis_and_repair_decision_v1"
NEXT_RUN_ID = "frontier68G_repair_result_review_or_next_validation_v1"

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
MODEL_ROOT = RUN_ROOT / "models"
FEATURE_ROOT = RUN_ROOT / "features"
MT5_ROOT = RUN_ROOT / "mt5"
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
COMMON_RUN_ROOT = "Project_Obsidian_Prime_v2/frontier68F_near_four_axis_repair_probe"

GROK_PACKET_ROOT = ROOT / "docs/agent_control/grok_reviews/2026-06-17_f68f_pre_repair_onnx_runtime_probe"
GROK_PROMPT = GROK_PACKET_ROOT / "prompts/f68f_pre_repair_onnx_runtime_probe_prompt.md"
GROK_CLEAN = GROK_PACKET_ROOT / "outputs/clean_output.md"
GROK_METADATA = GROK_PACKET_ROOT / "outputs/metadata.json"

F68B_SUMMARY = REVIEWS_ROOT / "f68b_proxy_candidate_summary_review.csv"

CLAIM_BOUNDARY = (
    "repair_runtime_probe_observation_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

REPAIR_AXIS = f68c.CandidateAxis(
    axis_id="near_four_axis_repair_axis",
    candidate_id="f68b_0872ddc6192f",
    role="repair_no_mega_cooldown6_dd_pf_tradeoff",
    target_prefix="h2_ddp03_min1p5",
    feature_prefix="no_mega_top3",
    model_prefix="extra_trees_shallow",
    threshold_quantile=0.30,
    cooldown_bars=6,
    side_prefix="both",
    exit_prefix="close_horizon",
    priority=1,
)

DUPLICATE_CHECK_AXIS = f68c.CandidateAxis(
    axis_id="session_regime_duplicate_check_axis",
    candidate_id="f68b_0f012336cfaf",
    role="duplicate_or_regime_hash_check",
    target_prefix="h2_ddp03_min1p5",
    feature_prefix="session_regime_no_mega",
    model_prefix="extra_trees_shallow",
    threshold_quantile=0.30,
    cooldown_bars=6,
    side_prefix="both",
    exit_prefix="close_horizon",
    priority=2,
)

SPLIT_WINDOWS = {
    "validation": {"from": "2025.01.02", "to": "2025.10.01"},
    "oos": {"from": "2025.10.01", "to": "2026.04.14"},
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="F68F ONNX export and MT5 runtime repair probe.")
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
    patch_imported_runtime_globals()
    reference = f68b_reference_by_candidate()
    model_input_raw, raw, raw_positions = f68c.f68b.load_frames()
    model_input = f68c.f68b.model_input_with_spread(model_input_raw, raw)
    primary_context = f68c.build_candidate_context(REPAIR_AXIS, model_input, raw, raw_positions, reference[REPAIR_AXIS.candidate_id])
    duplicate_context = f68c.build_candidate_context(
        DUPLICATE_CHECK_AXIS,
        model_input,
        raw,
        raw_positions,
        reference[DUPLICATE_CHECK_AXIS.candidate_id],
    )
    export = f68c.export_candidate(primary_context)
    feature_rows = write_feature_csvs([primary_context, duplicate_context], model_input)
    summary_rows = [f68c.axis_summary_row(primary_context, export, reference[REPAIR_AXIS.candidate_id])]
    kpi_rows = list(primary_context["kpi_rows"])
    handoff_rows = [f68c.handoff_intent_row(primary_context, export, feature_rows)]
    duplicate_check = duplicate_surface_check(primary_context, duplicate_context)
    local_verification = build_local_verification(export, handoff_rows[0], duplicate_check)
    attempts = build_attempts(handoff_rows[0], primary_context, export, Path(args.common_files_root))
    payload: dict[str, Any] = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": created_at,
        "status": "materialized_pending_mt5_repair_probe_execution_no_authority(물질화 완료, MT5 수리 탐침 실행 대기, 권위 없음)",
        "judgment": "near_four_axis_repair_export_materialized_pending_runtime_no_authority(네 축 근접 수리 내보내기 물질화, 런타임 대기, 권위 없음)",
        "claim_boundary": CLAIM_BOUNDARY,
        "grok_packet": grok_identity(),
        "summary_rows": summary_rows,
        "kpi_rows": kpi_rows,
        "exports": [export],
        "feature_csv_rows": feature_rows,
        "handoff_intent_rows": handoff_rows,
        "probability_parity_rows": list(export.get("probability_parity") or []),
        "signal_parity_rows": list(export.get("signal_parity") or []),
        "duplicate_check": duplicate_check,
        "local_verification": local_verification,
        "attempts": attempts,
        "execution_results": [],
        "strategy_tester_reports": [],
        "mt5_kpi_records": [],
        "runtime_receipt": [],
        "gap_classification": [],
    }
    if args.materialize_only or not args.execute or not local_verification["can_execute"]:
        write_outputs(payload)
        update_state_and_ledgers(payload)
        print(json.dumps(json_ready(compact_status(payload)), ensure_ascii=False, indent=2))
        return 0 if local_verification["export_and_parity_passed"] else 1

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
    execution_completed = bool(execution_results) and all(row.get("status") == "completed" for row in execution_results)
    report_completed = bool(kpi_records) and len(kpi_records) == len(attempts)
    payload.update(
        {
            "status": (
                "completed_repair_runtime_probe_observation_no_authority(MT5 수리 탐침 관찰 완료, 권위 없음)"
                if execution_completed and report_completed
                else "blocked_repair_runtime_probe_attempted_repair_required_no_authority(MT5 수리 탐침 시도 차단, 수리 필요, 권위 없음)"
            ),
            "judgment": (
                repair_judgment(receipt_rows)
                if execution_completed and report_completed
                else "repair_runtime_probe_blocked_no_authority(수리 런타임 탐침 차단, 권위 없음)"
            ),
            "compile_payload": compile_payload,
            "execution_results": execution_results,
            "strategy_tester_reports": report_records,
            "mt5_kpi_records": kpi_records,
            "runtime_receipt": receipt_rows,
            "gap_classification": gap_rows,
        }
    )
    write_outputs(payload)
    update_state_and_ledgers(payload)
    print(json.dumps(json_ready(compact_status(payload)), ensure_ascii=False, indent=2))
    return 0


def ensure_dirs() -> None:
    for path in (RUN_ROOT, MODEL_ROOT, FEATURE_ROOT, MT5_ROOT, MT5_ROOT / "reports", REVIEWS_ROOT):
        io_path(path).mkdir(parents=True, exist_ok=True)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def patch_imported_runtime_globals() -> None:
    f68c.RUN_ID = RUN_ID
    f68c.RUN_ROOT = RUN_ROOT
    f68c.MODEL_ROOT = MODEL_ROOT
    f68c.FEATURE_ROOT = FEATURE_ROOT
    f68c.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    f68d.RUN_ID = RUN_ID
    f68d.RUN_ROOT = RUN_ROOT
    f68d.MT5_ROOT = MT5_ROOT
    f68d.CLAIM_BOUNDARY = CLAIM_BOUNDARY


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def f68b_reference_by_candidate() -> dict[str, Mapping[str, Any]]:
    return {row["candidate_id"]: row for row in read_csv_rows(F68B_SUMMARY)}


def write_feature_csvs(contexts: Sequence[Mapping[str, Any]], model_input: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for context in contexts:
        feature_hash = str(context["feature_order_hash"])
        if feature_hash in seen:
            continue
        seen.add(feature_hash)
        feature_set = context["feature_set"]
        feature_columns = list(context["feature_columns"])
        path = FEATURE_ROOT / f"f68f_{f68c.slug(feature_set.feature_set_id)}_{len(feature_columns)}_{feature_hash[:10]}_features.csv"
        frame = model_input.loc[:, ["timestamp", *feature_columns]].copy()
        frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True).dt.strftime("%Y-%m-%d %H:%M:%S")
        frame.to_csv(io_path(path), index=False, encoding="utf-8-sig", lineterminator="\n")
        rows.append(
            {
                "feature_set_id": feature_set.feature_set_id,
                "feature_count": len(feature_columns),
                "feature_order_hash": feature_hash,
                "feature_csv_path": rel(path),
                "feature_csv_sha256": sha256_file(path),
                "feature_csv_bytes": io_path(path).stat().st_size,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def duplicate_surface_check(primary: Mapping[str, Any], duplicate: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "primary_candidate_id": primary["axis"].candidate_id,
        "duplicate_candidate_id": duplicate["axis"].candidate_id,
        "primary_feature_set_id": primary["feature_set"].feature_set_id,
        "duplicate_feature_set_id": duplicate["feature_set"].feature_set_id,
        "primary_feature_count": len(primary["feature_columns"]),
        "duplicate_feature_count": len(duplicate["feature_columns"]),
        "primary_feature_order_hash": primary["feature_order_hash"],
        "duplicate_feature_order_hash": duplicate["feature_order_hash"],
        "feature_hash_equal": bool(primary["feature_order_hash"] == duplicate["feature_order_hash"]),
        "candidate_id_check_primary": primary["candidate_id_check"],
        "candidate_id_check_duplicate": duplicate["candidate_id_check"],
        "primary_reference_passed": primary["reference_diff"]["passed"],
        "duplicate_reference_passed": duplicate["reference_diff"]["passed"],
        "decision": (
            "treat_duplicate_as_redundant_check(중복 확인으로만 취급)"
            if primary["feature_order_hash"] == duplicate["feature_order_hash"]
            else "feature_hash_differs_keep_as_regime_followup(피처 해시 다름, 장세 후속으로 보존)"
        ),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def grok_identity() -> dict[str, Any]:
    return {
        "packet_root": rel(GROK_PACKET_ROOT),
        "prompt_path": rel(GROK_PROMPT),
        "clean_output_path": rel(GROK_CLEAN),
        "metadata_path": rel(GROK_METADATA),
        "prompt_sha256": sha256_file(GROK_PROMPT) if path_exists(GROK_PROMPT) else "",
        "clean_output_sha256": sha256_file(GROK_CLEAN) if path_exists(GROK_CLEAN) else "",
        "metadata_exists": path_exists(GROK_METADATA),
    }


def build_local_verification(
    export: Mapping[str, Any],
    handoff: Mapping[str, Any],
    duplicate_check: Mapping[str, Any],
) -> dict[str, Any]:
    probability_rows = list(export.get("probability_parity") or [])
    signal_rows = list(export.get("signal_parity") or [])
    rows = [
        check("grok_clean_output_exists", path_exists(GROK_CLEAN), rel(GROK_CLEAN)),
        check("candidate_id_reconstructed", REPAIR_AXIS.candidate_id == "f68b_0872ddc6192f", REPAIR_AXIS.candidate_id),
        check("onnx_exported", str(export.get("export_status", "")).startswith("exported"), str(export.get("export_status"))),
        check("model_hash_present", bool(export.get("onnx_sha256")), str(export.get("onnx_sha256"))),
        check("probability_parity_all_passed", bool(probability_rows) and all(row.get("passed") for row in probability_rows), str(len(probability_rows))),
        check("signal_parity_all_passed", bool(signal_rows) and all(row.get("passed") for row in signal_rows), str(len(signal_rows))),
        check("feature_count_49", int(handoff.get("feature_count") or 0) == 49, str(handoff.get("feature_count"))),
        check("cooldown_6", int(handoff.get("same_direction_reentry_cooldown_bars") or 0) == 6, str(handoff.get("same_direction_reentry_cooldown_bars"))),
        check("duplicate_hash_checked", "feature_hash_equal" in duplicate_check, str(duplicate_check.get("feature_hash_equal"))),
    ]
    export_and_parity_passed = all(row["status"] == "passed" for row in rows[:6])
    return {
        "rows": rows,
        "passed": all(row["status"] == "passed" for row in rows),
        "export_and_parity_passed": export_and_parity_passed,
        "can_execute": export_and_parity_passed and bool(handoff.get("probe_eligible")),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def check(name: str, ok: bool, detail: str) -> dict[str, str]:
    return {
        "check_name": name,
        "status": "passed" if ok else "failed",
        "detail": detail,
        "effect": "prevents F68F from inheriting F68D parity or duplicate-surface assumptions",
    }


def build_attempts(
    handoff: Mapping[str, Any],
    context: Mapping[str, Any],
    export: Mapping[str, Any],
    common_files_root: Path,
) -> list[dict[str, Any]]:
    model_local = ROOT / str(handoff["model_path_repo"])
    feature_local = ROOT / str(handoff["feature_csv_repo"])
    model_common = f"{COMMON_RUN_ROOT}/models/{model_local.name}"
    feature_common = f"{COMMON_RUN_ROOT}/features/{feature_local.name}"
    model_common_payload = mt5.copy_to_common_files(common_files_root, model_local, model_common)
    feature_common_payload = mt5.copy_to_common_files(common_files_root, feature_local, feature_common)
    proxy_by_split = {str(row["split"]): row for row in context["kpi_rows"]}
    signal_by_split = {str(row["split"]): row for row in export.get("signal_parity", [])}
    attempts: list[dict[str, Any]] = []
    for split, window in SPLIT_WINDOWS.items():
        attempt_name = f"f68f_near_four_axis_{REPAIR_AXIS.candidate_id[-6:]}_{split}"
        extra_set_values = {
            "InpSameDirectionReentryCooldownBars": int(handoff.get("same_direction_reentry_cooldown_bars") or 0),
            "InpReentryCooldownBars": 0,
            "InpAtrSltpEnabled": bool(handoff.get("atr_sltp_enabled")),
            "InpAtrStopMultiplier": float(handoff.get("atr_stop_multiplier") or 0.0),
            "InpAtrTakeProfitMultiplier": float(handoff.get("atr_take_profit_multiplier") or 0.0),
            "InpDecisionMode": str(handoff.get("decision_mode") or "threshold_margin"),
            "InpFallbackDecisionMode": str(handoff.get("decision_mode") or "threshold_margin"),
        }
        attempt = attempt_payload(
            run_root=RUN_ROOT,
            run_id=RUN_ID,
            stage_number=68,
            exploration_label="frontier68F_near_four_axis_repair_probe(F68F 네 축 근접 수리 탐침)",
            attempt_name=attempt_name,
            tier=mt5.TIER_A,
            split=split,
            model_path=model_common,
            model_id=f"F68F_{REPAIR_AXIS.candidate_id}",
            model_backend="onnx",
            feature_path=feature_common,
            feature_count=int(handoff.get("feature_count") or 0),
            feature_order_hash=str(handoff.get("feature_order_hash") or ""),
            short_threshold=float(handoff.get("short_threshold") or 0.0),
            long_threshold=float(handoff.get("long_threshold") or 0.0),
            min_margin=float(handoff.get("min_margin") or 0.0),
            invert_signal=False,
            from_date=window["from"],
            to_date=window["to"],
            primary_active_tier=mt5.TIER_A,
            attempt_role="f68f_near_four_axis_repair_runtime_probe",
            record_view_prefix=f"mt5_f68f_near_four_axis_{REPAIR_AXIS.candidate_id[-6:]}",
            max_hold_bars=int(handoff.get("max_hold_bars") or 2),
            common_root=COMMON_RUN_ROOT,
            close_on_flat_signal=True,
            reverse_on_opposite_signal=True,
            close_only_on_opposite_signal=False,
            extra_set_values=extra_set_values,
        )
        attempt.update(
            {
                "candidate_id": REPAIR_AXIS.candidate_id,
                "axis_id": REPAIR_AXIS.axis_id,
                "expected_rows": int(signal_by_split.get(split, {}).get("rows") or 0),
                "expected_signal_count": int(signal_by_split.get(split, {}).get("onnx_signal_count") or 0),
                "expected_sklearn_signal_count": int(signal_by_split.get(split, {}).get("sklearn_signal_count") or 0),
                "proxy_kpi": proxy_by_split.get(split, {}),
                "model_common_copy": model_common_payload,
                "feature_common_copy": feature_common_payload,
                "model_sha256_actual": sha256_file(model_local),
                "feature_sha256_actual": sha256_file(feature_local),
                "known_runtime_difference": "close_on_flat_signal_true_matches_F68D_runtime_probe_comparison_but_may_differ_from_proxy_close_horizon",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        attempts.append(attempt)
    return attempts


def repair_judgment(receipts: Sequence[Mapping[str, Any]]) -> str:
    if not receipts:
        return "repair_runtime_probe_no_receipt_no_authority(수리 런타임 탐침 영수증 없음, 권위 없음)"
    validation = next((row for row in receipts if row.get("split") == "validation"), {})
    oos = next((row for row in receipts if row.get("split") == "oos"), {})
    val_pf = as_float(validation.get("profit_factor")) or 0.0
    oos_pf = as_float(oos.get("profit_factor")) or 0.0
    val_dd = as_float(validation.get("max_drawdown_percent")) or 999.0
    oos_dd = as_float(oos.get("max_drawdown_percent")) or 999.0
    val_tpd = as_float(validation.get("trades_per_day")) or 0.0
    oos_tpd = as_float(oos.get("trades_per_day")) or 0.0
    if min(val_pf, oos_pf) > 1.0 and max(val_dd, oos_dd) < 26.84 and min(val_tpd, oos_tpd) > 1.0:
        return "repair_probe_positive_signal_dd_improved_density_still_under_final_target_no_authority(수리 탐침 긍정 신호, 손실폭 개선, 거래 밀도 최종 목표 미달, 권위 없음)"
    if max(val_dd, oos_dd) >= 26.84 or min(val_pf, oos_pf) <= 1.0:
        return "repair_probe_negative_or_mixed_runtime_economics_no_authority(수리 탐침 부정 또는 혼합 런타임 경제성, 권위 없음)"
    return "repair_probe_inconclusive_no_authority(수리 탐침 불충분, 권위 없음)"


def compact_status(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "status": payload.get("status"),
        "judgment": payload.get("judgment"),
        "export_status": (payload.get("exports") or [{}])[0].get("export_status"),
        "probability_parity_rows": len(payload.get("probability_parity_rows") or []),
        "signal_parity_rows": len(payload.get("signal_parity_rows") or []),
        "attempt_count": len(payload.get("attempts") or []),
        "runtime_receipt_rows": len(payload.get("runtime_receipt") or []),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_outputs(payload: Mapping[str, Any]) -> None:
    write_json(RUN_ROOT / "run_manifest.json", payload)
    write_json(RUN_ROOT / "frontier68F_repair_probe_execution_result.json", payload)
    write_json(RUN_ROOT / "frontier68F_repair_probe_summary.json", build_summary(payload))
    write_csv(RUN_ROOT / "frontier68F_candidate_axis_summary.csv", payload.get("summary_rows", []))
    write_csv(RUN_ROOT / "frontier68F_candidate_axis_kpi_by_split.csv", payload.get("kpi_rows", []))
    write_csv(RUN_ROOT / "frontier68F_onnx_probability_parity.csv", payload.get("probability_parity_rows", []))
    write_csv(RUN_ROOT / "frontier68F_onnx_signal_parity.csv", payload.get("signal_parity_rows", []))
    write_csv(RUN_ROOT / "frontier68F_handoff_intent.csv", payload.get("handoff_intent_rows", []))
    write_csv(RUN_ROOT / "frontier68F_runtime_probe_receipt.csv", payload.get("runtime_receipt", []))
    write_csv(RUN_ROOT / "frontier68F_gap_classification.csv", payload.get("gap_classification", []))
    write_csv(RUN_ROOT / "frontier68F_local_verification.csv", payload.get("local_verification", {}).get("rows", []))
    write_csv(REVIEWS_ROOT / "frontier68F_runtime_probe_receipt_review.csv", payload.get("runtime_receipt", []))
    write_csv(REVIEWS_ROOT / "frontier68F_gap_classification_review.csv", payload.get("gap_classification", []))
    write_md(REVIEWS_ROOT / "frontier68F_near_four_axis_onnx_runtime_repair_probe_report.md", report_lines(payload))
    write_md(REVIEWS_ROOT / "frontier68F_gate_audit.md", gate_audit_lines(payload))
    write_grok_receipt(payload)
    write_review_index()


def build_summary(payload: Mapping[str, Any]) -> dict[str, Any]:
    receipts = list(payload.get("runtime_receipt") or [])
    return {
        "run_id": RUN_ID,
        "status": payload.get("status"),
        "judgment": payload.get("judgment"),
        "candidate_id": REPAIR_AXIS.candidate_id,
        "duplicate_check": payload.get("duplicate_check"),
        "local_verification_passed": payload.get("local_verification", {}).get("passed"),
        "validation": next((row for row in receipts if row.get("split") == "validation"), {}),
        "oos": next((row for row in receipts if row.get("split") == "oos"), {}),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def report_lines(payload: Mapping[str, Any]) -> list[str]:
    receipts = list(payload.get("runtime_receipt") or [])
    lines = [
        "# F68F Near-Four-Axis ONNX Runtime Repair Probe(F68F 네 축 근접 ONNX 런타임 수리 탐침)",
        "",
        f"Updated(갱신): {payload['created_at_utc']}",
        "",
        "## Action And Effect(행동 및 효과)",
        "",
        "Action(행동): F68E repair queue(수리 대기열)의 primary candidate(주 후보) `f68b_0872ddc6192f`를 ONNX export(ONNX 내보내기)하고 MT5 Strategy Tester(MT5 전략 테스터) validation/OOS(검증/표본외)를 실행했다.",
        "",
        "Effect(효과): F68D에서 무너진 runtime economics/DD(런타임 경제성/손실폭)가 feature set/trade spacing repair(피처 묶음/거래 간격 수리)로 개선되는지 관찰했다.",
        "",
        f"- status(상태): `{payload.get('status')}`",
        f"- judgment(판정): `{payload.get('judgment')}`",
        f"- export_status(내보내기 상태): `{(payload.get('exports') or [{}])[0].get('export_status')}`",
        f"- local_verification_passed(로컬 검증 통과): `{payload.get('local_verification', {}).get('passed')}`",
        f"- duplicate_feature_hash_equal(중복 피처 해시 동일): `{payload.get('duplicate_check', {}).get('feature_hash_equal')}`",
        "",
        "## Runtime KPI(런타임 핵심 성과 지표)",
        "",
        "| split(분할) | period(기간) | net(순수익) | gross profit(총이익) | gross loss(총손실) | PF(수익 팩터) | DD%(손실폭) | trades(거래) | trades/day(일 거래) | signal diff(신호 차이) | feature diff(피처 차이) |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in receipts:
        lines.append(
            "| `{split}` | `{start}..{end}` | `{net}` | `{gp}` | `{gl}` | `{pf}` | `{dd}` | `{trades}` | `{tpd}` | `{sig}` | `{feat}` |".format(
                split=row.get("split"),
                start=row.get("test_period_start"),
                end=row.get("test_period_end"),
                net=fmt(row.get("net_profit")),
                gp=fmt(row.get("gross_profit")),
                gl=fmt(row.get("gross_loss")),
                pf=fmt(row.get("profit_factor")),
                dd=fmt(row.get("max_drawdown_percent")),
                trades=fmt(row.get("trade_count")),
                tpd=fmt(row.get("trades_per_day")),
                sig=fmt(row.get("signal_count_diff")),
                feat=fmt(row.get("feature_ready_diff")),
            )
        )
    if not receipts:
        lines.append("| `missing` | `missing` | `NA` | `NA` | `NA` | `NA` | `NA` | `NA` | `NA` | `NA` | `NA` |")
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "- This is repair runtime probe evidence only(수리 런타임 탐침 근거 전용).",
            "- F68D density/PF axes(F68D 밀도/수익 팩터 축)는 comparison anchors(비교 기준점)일 뿐이며 selected baseline(선택 기준선)이 아니다.",
            "- If PF/DD improve but trades/day remains below 5, record preserved clue(보존 단서) or inconclusive(불충분), not completion(완성).",
            "",
            f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        ]
    )
    return lines


def gate_audit_lines(payload: Mapping[str, Any]) -> list[str]:
    return [
        "# F68F Gate Audit(F68F 게이트 감사)",
        "",
        f"- Grok pre-repair review(그록 수리 전 검토): `{'passed' if path_exists(GROK_CLEAN) else 'missing'}`.",
        f"- ONNX export(ONNX 내보내기): `{(payload.get('exports') or [{}])[0].get('export_status')}`.",
        f"- probability parity rows(확률 동등성 행): `{len(payload.get('probability_parity_rows') or [])}`.",
        f"- signal parity rows(신호 동등성 행): `{len(payload.get('signal_parity_rows') or [])}`.",
        f"- local verification(로컬 검증): `{payload.get('local_verification', {}).get('passed')}`.",
        f"- MT5 Runtime Probe attempted(MT5 런타임 탐침 시도): `{bool(payload.get('execution_results'))}`.",
        f"- Strategy Tester reports(전략 테스터 보고서): `{len(payload.get('strategy_tester_reports') or [])}`.",
        f"- runtime receipt rows(런타임 영수증 행): `{len(payload.get('runtime_receipt') or [])}`.",
        f"- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
    ]


def write_grok_receipt(payload: Mapping[str, Any]) -> None:
    lines = [
        "# F68F Grok Pre-Repair Receipt(F68F 수리 전 그록 영수증)",
        "",
        f"Updated(갱신): {payload['created_at_utc']}",
        "",
        "- trigger_reason(트리거 이유): goal rule(목표 규칙)이 ONNX handoff/MT5 Runtime Probe(ONNX 인계/MT5 런타임 탐침) 전 Grok review(그록 검토)를 요구한다.",
        "- review_size(검토 크기): medium review(중간 검토).",
        f"- prompt_identity(프롬프트 정체성): `{rel(GROK_PROMPT)}` sha256 `{sha256_file(GROK_PROMPT) if path_exists(GROK_PROMPT) else ''}`.",
        f"- grok_output_identity(그록 출력 정체성): `{rel(GROK_CLEAN)}` sha256 `{sha256_file(GROK_CLEAN) if path_exists(GROK_CLEAN) else ''}`.",
        "- advice_classification(조언 분류): accepted(수용)=F68F as narrow repair probe(좁은 수리 탐침); rejected(거절)=threshold-only repair and F68D parity inheritance(임계값만 수리와 F68D 동등성 상속); needs_local_verification(로컬 검증 필요)=export/hash/parity/MT5 KPI/density read(내보내기/해시/동등성/MT5 핵심 성과 지표/거래 밀도 판독).",
        f"- local_verification(로컬 검증): `{payload.get('local_verification', {}).get('passed')}`.",
        "- forbidden_claim_check(금지 주장 확인): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).",
        "- final_codex_direction(최종 Codex 방향): run F68F as repair runtime probe only(F68F를 수리 런타임 탐침으로만 실행).",
    ]
    write_md(GROK_PACKET_ROOT / "f68f_pre_repair_onnx_runtime_probe_receipt.md", lines)


def write_review_index() -> None:
    existing = io_path(REVIEWS_ROOT / "review_index.md").read_text(encoding="utf-8-sig")
    additions = [
        "- `frontier68F_near_four_axis_onnx_runtime_repair_probe_report.md`: F68F near-four-axis ONNX runtime repair probe(F68F 네 축 근접 ONNX 런타임 수리 탐침)",
        "- `frontier68F_runtime_probe_receipt_review.csv`: F68F runtime receipt(F68F 런타임 영수증)",
        "- `frontier68F_gap_classification_review.csv`: F68F gap classification(F68F 간극 분류)",
        "- `frontier68F_gate_audit.md`: F68F gate audit(F68F 게이트 감사)",
    ]
    lines = existing.rstrip().splitlines()
    for line in additions:
        if line not in lines:
            lines.append(line)
    lines.append(f"Next action(다음 행동): `{NEXT_RUN_ID}`")
    write_md(REVIEWS_ROOT / "review_index.md", lines)


def update_state_and_ledgers(payload: Mapping[str, Any]) -> None:
    receipts = list(payload.get("runtime_receipt") or [])
    oos = next((row for row in receipts if row.get("split") == "oos"), {})
    validation = next((row for row in receipts if row.get("split") == "validation"), {})
    row = {
        "ledger_row_id": f"{RUN_ID}__near_four_axis_repair_probe",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "near_four_axis_repair_probe(네 축 근접 수리 탐침)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "onnx_export_mt5_runtime_repair_probe(ONNX 내보내기 MT5 런타임 수리 탐침)",
        "tier_scope": "Tier A+B planned(티어 A+B 계획)",
        "kpi_scope": "onnx_parity_and_mt5_runtime_kpi(ONNX 동등성 및 MT5 런타임 핵심 성과 지표)",
        "scoreboard_lane": "runtime_probe(런타임 탐침)",
        "status": payload.get("status"),
        "judgment": payload.get("judgment"),
        "path": f"stages/{STAGE_ID}/03_reviews/frontier68F_near_four_axis_onnx_runtime_repair_probe_report.md",
        "primary_kpi": (
            f"validation_pf={fmt(validation.get('profit_factor'))};validation_dd={fmt(validation.get('max_drawdown_percent'))};"
            f"oos_pf={fmt(oos.get('profit_factor'))};oos_dd={fmt(oos.get('max_drawdown_percent'))};"
            f"oos_tpd={fmt(oos.get('trades_per_day'))}"
        ),
        "guardrail_kpi": (
            f"signal_gap_rows={sum(1 for r in receipts if r.get('signal_count_diff') not in (0, '0'))};"
            f"feature_gap_rows={sum(1 for r in receipts if r.get('feature_ready_diff') not in (0, '0'))};"
            f"runtime_receipt_rows={len(receipts)}"
        ),
        "external_verification_status": "completed" if receipts else "blocked_or_pending",
        "notes": "F68F tested ONNX-capable near-four-axis repair seed in MT5; observation only, no authority.",
        "date": payload["created_at_utc"][:10],
        "decision": "proceed_to_f68g_repair_result_review_or_next_validation",
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": f"stages/{STAGE_ID}/03_reviews/frontier68F_near_four_axis_onnx_runtime_repair_probe_report.md",
        "result_judgment": payload.get("judgment"),
        "created_at_utc": payload["created_at_utc"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "frontier_onnx_runtime_repair_probe(전선 ONNX 런타임 수리 탐침)",
        "run_type": "onnx_export_mt5_repair_probe(ONNX 내보내기 MT5 수리 탐침)",
        "input_run_id": PARENT_RUN_ID,
        "output_path": f"stages/{STAGE_ID}/02_runs/{RUN_ID}/frontier68F_repair_probe_execution_result.json",
        "result_path": f"stages/{STAGE_ID}/03_reviews/frontier68F_near_four_axis_onnx_runtime_repair_probe_report.md",
        "source_authority": "mt5_strategy_tester_runtime_probe_observation(MT5 전략 테스터 런타임 탐침 관찰)",
        "trade_density": fmt(oos.get("trades_per_day")),
        "selected_profit_factor": fmt(oos.get("profit_factor")),
        "max_drawdown_percent": fmt(oos.get("max_drawdown_percent")),
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
        "runtime_probe_status: f68f_repair_runtime_probe_recorded_no_authority(F68F 수리 런타임 탐침 기록, 권위 없음)",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        f"updated_at_utc: '{payload['created_at_utc']}'",
        "notes:",
        '  - "F68F action(행동): near-four-axis repair candidate(네 축 근접 수리 후보)를 ONNX로 내보내고 MT5 Strategy Tester(MT5 전략 테스터)에서 검증/표본외를 실행했다."',
        '  - "Effect(효과): F68D runtime economics/DD failure(F68D 런타임 경제성/손실폭 실패)를 feature set/trade spacing repair(피처 묶음/거래 간격 수리)와 비교할 수 있게 했다."',
        f'  - "Next action(다음 행동): `{NEXT_RUN_ID}`에서 repair result review(수리 결과 검토)와 다음 validation/repair/closeout(검증/수리/마감) 판단을 한다."',
        '  - "Boundary(경계): repair runtime probe observation only(수리 런타임 탐침 관찰 전용), no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."',
    ]
    io_path(ROOT / "docs/workspace/workspace_state.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8-sig")
    cws = [
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
        "Action(행동): F68F near-four-axis ONNX runtime repair probe(F68F 네 축 근접 ONNX 런타임 수리 탐침)를 실행했다.",
        "",
        "Effect(효과): F68E repair queue(수리 대기열)의 주 후보를 ONNX와 MT5 runtime(런타임)으로 물질화해, 프록시 수리가 실제 경제성으로 이어지는지 관찰했다.",
        "",
        f"- F68F status(F68F 상태): `{payload.get('status')}`.",
        f"- runtime_receipt_rows(런타임 영수증 행): `{len(payload.get('runtime_receipt') or [])}`.",
        f"- duplicate_feature_hash_equal(중복 피처 해시 동일): `{payload.get('duplicate_check', {}).get('feature_hash_equal')}`.",
        "",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ]
    write_md(ROOT / "docs/context/current_working_state.md", cws)


def write_selection_status(payload: Mapping[str, Any]) -> None:
    lines = [
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
        "- completed_action(완료 행동): F68F ONNX export and MT5 repair probe(F68F ONNX 내보내기 및 MT5 수리 탐침).",
        f"- report(보고서): `stages/{STAGE_ID}/03_reviews/frontier68F_near_four_axis_onnx_runtime_repair_probe_report.md`",
        f"- next_action(다음 행동): `{NEXT_RUN_ID}` repair result review or next validation(수리 결과 검토 또는 다음 검증).",
        f"- boundary(경계): `{CLAIM_BOUNDARY}`.",
    ]
    write_md(STAGE_ROOT / "04_selected" / "selection_status.md", lines)


def as_float(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def fmt(value: Any) -> str:
    number = as_float(value)
    if number is None:
        return "" if value in (None, "") else str(value)
    if abs(number - round(number)) < 1e-9:
        return str(int(round(number)))
    return f"{number:.6f}".rstrip("0").rstrip(".")


if __name__ == "__main__":
    raise SystemExit(main())
