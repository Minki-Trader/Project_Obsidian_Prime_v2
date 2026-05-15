from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

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
    EA_TESTER_SET_NAME,
    METAEDITOR_PATH_DEFAULT,
    TERMINAL_DATA_ROOT_DEFAULT,
    TERMINAL_PATH_DEFAULT,
    TESTER_PROFILE_ROOT_DEFAULT,
    attempt_payload,
    clear_runtime_outputs,
    parse_ini,
    safe_name,
)
from foundation.mt5 import runtime_support as mt5  # noqa: E402
from stage_pipelines.stage56 import baseline_adapter_repair_batch as repair  # noqa: E402
from stage_pipelines.stage56 import independent_event_source_route_branch as aw  # noqa: E402
from stage_pipelines.stage58 import risk_atr_integration as s58  # noqa: E402
from stage_pipelines.stage59d import source_lifecycle_or_demote as engine  # noqa: E402


STAGE56_ID = "56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection"
SOURCE_STAGE59S_ID = "59S_adapter_repair__bounded_followup_from_stage59r"
SOURCE_STAGE59U_ID = "59U_adapter_repair__bounded_followup_from_stage59t"
STAGE59V_ID = "59V_adapter_repair__bounded_followup_from_stage59u"
NEXT_REPAIR_STAGE_ID = "59W_adapter_repair__bounded_followup_from_stage59v"
RUN_NUMBER = "run59Q"
RUN_ID = "run59Q_stage59v_bounded_followup_from_stage59u_v1"
PACKET_ID = "stage59v_bounded_followup_from_stage59u_v1"
PARENT_RUN_ID = "run59P_stage59u_bounded_followup_from_stage59t_v1"
SOURCE_ADAPTER_ID = "s59s_v61_long54_sl20_tp30_sd12_h5_rearm002"
DEVELOPMENT_ANCHOR = "v64_v47_ctxgap14_refill_etfw_h2_no_b"
BACKUP_ANCHOR = "v60_v47_et_stable_damage_firewall_h2c0_no_b"
SOURCE_STAGE59S_PUSHED_COMMIT = "456e723800d6ceb724958b8ded669c72ccdae5f1"
SOURCE_STAGE59U_PUSHED_COMMIT = "8d59fd46b34bde5350cd357e468a2eb9bb59e7dd"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)

STAGE_ROOT = Path("stages") / STAGE59V_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
SPEC_ROOT = STAGE_ROOT / "00_spec"
INPUT_ROOT = STAGE_ROOT / "01_inputs"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID

SOURCE_STAGE_ROOT = Path("stages") / STAGE56_ID
SOURCE_STAGE59S_ROOT = Path("stages") / SOURCE_STAGE59S_ID
SOURCE_STAGE59S_DECISION = SOURCE_STAGE59S_ROOT / "03_reviews/stage59s_decision.md"
SOURCE_STAGE59S_REPORT = SOURCE_STAGE59S_ROOT / "03_reviews/bounded_followup_from_stage59r_report.md"
SOURCE_STAGE59S_SUMMARY = SOURCE_STAGE59S_ROOT / "03_reviews/bounded_followup_summary.csv"
SOURCE_STAGE59S_JSON = SOURCE_STAGE59S_ROOT / "03_reviews/bounded_followup_summary.json"
SOURCE_STAGE59U_ROOT = Path("stages") / SOURCE_STAGE59U_ID
SOURCE_STAGE59U_DECISION = SOURCE_STAGE59U_ROOT / "03_reviews/stage59u_decision.md"
SOURCE_STAGE59U_REPORT = SOURCE_STAGE59U_ROOT / "03_reviews/bounded_followup_from_stage59t_report.md"
SOURCE_STAGE59U_SUMMARY = SOURCE_STAGE59U_ROOT / "03_reviews/bounded_followup_summary.csv"
SOURCE_STAGE59U_JSON = SOURCE_STAGE59U_ROOT / "03_reviews/bounded_followup_summary.json"

RUN50BQ_ROOT = SOURCE_STAGE_ROOT / "02_runs/run50BQ"
RUN50BQ_V61_ANCHOR = "v61_v47_et_firewall_h2_transition_no_b"
RUN50BQ_V62_ANCHOR = "v62_v47_et_firewall_h4_transition_no_b"
RUN50BQ_V63_ANCHOR = "v63_v47_et_firewall_h6_transition_no_b"
RUN50BQ_SIGNAL = "stage56_context_et_firewall_signal"

COMMON_ROOT = f"Project_Obsidian_Prime_v2/s59v/{RUN_NUMBER}"

REPORT_PATH = REVIEWS_ROOT / "bounded_followup_from_stage59u_report.md"
SUMMARY_JSON_PATH = REVIEWS_ROOT / "bounded_followup_summary.json"
SUMMARY_CSV_PATH = REVIEWS_ROOT / "bounded_followup_summary.csv"
SEGMENT_KPI_PATH = REVIEWS_ROOT / "bounded_followup_segment_kpi_summary.csv"
EQUITY_AUDIT_PATH = REVIEWS_ROOT / "bounded_followup_equity_curve_audit.md"
RISK_ATR_TELEMETRY_PATH = REVIEWS_ROOT / "bounded_followup_risk_atr_telemetry.csv"
DECISION_PATH = REVIEWS_ROOT / "stage59v_decision.md"
AUDIT_CSV_PATH = REVIEWS_ROOT / "stage59v_trade_audit.csv"
PARTIALS_ROOT = RUN_ROOT / "partials"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")

MIN_MARGIN = 0.0

STAGE59V_VARIANTS = (
    repair.RepairVariant(
        adapter_id="s59v_s59s_mr015_sl20_tp30_sd12_h5_rearm002",
        label="run50BQ_v61_transition_h2_close_only_sl20_tp30_sd12_h5_rearm002_risk1p5pct_atr",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.0,
        atr_take_profit_multiplier=3.0,
        model_risk_max_pct=0.015,
        same_direction_reentry_cooldown_bars=12,
        entry_transition_only=True,
        entry_transition_rearm_min_confidence_delta=0.02,
        short_threshold=0.52,
        long_threshold=0.54,
        close_on_flat_signal=False,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=True,
        max_hold_bars=5,
        notes="Stage59V bounded follow-up: return to Stage59S strong pre-exit-policy anchor and compress model_risk_max_pct to 1.5%.",
    ),
    repair.RepairVariant(
        adapter_id="s59v_s59s_mr020_sl20_tp30_sd12_h5_rearm002",
        label="run50BQ_v61_transition_h2_close_only_sl20_tp30_sd12_h5_rearm002_risk2pct_atr",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.0,
        atr_take_profit_multiplier=3.0,
        model_risk_max_pct=0.020,
        same_direction_reentry_cooldown_bars=12,
        entry_transition_only=True,
        entry_transition_rearm_min_confidence_delta=0.02,
        short_threshold=0.52,
        long_threshold=0.54,
        close_on_flat_signal=False,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=True,
        max_hold_bars=5,
        notes="Stage59V bounded follow-up: return to Stage59S strong pre-exit-policy anchor and compress model_risk_max_pct to 2.0%.",
    ),
    repair.RepairVariant(
        adapter_id="s59v_s59s_mr025_sl20_tp30_sd12_h5_rearm002",
        label="run50BQ_v61_transition_h2_close_only_sl20_tp30_sd12_h5_rearm002_risk2p5pct_atr",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.0,
        atr_take_profit_multiplier=3.0,
        model_risk_max_pct=0.025,
        same_direction_reentry_cooldown_bars=12,
        entry_transition_only=True,
        entry_transition_rearm_min_confidence_delta=0.02,
        short_threshold=0.52,
        long_threshold=0.54,
        close_on_flat_signal=False,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=True,
        max_hold_bars=5,
        notes="Stage59V bounded follow-up: return to Stage59S strong pre-exit-policy anchor and compress model_risk_max_pct to 2.5%.",
    ),
)

def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    candidate = Path(str(path))
    try:
        return io_path(candidate).resolve().relative_to(io_path(REPO_ROOT).resolve()).as_posix()
    except ValueError:
        return candidate.as_posix()


def source_specs() -> dict[str, dict[str, Any]]:
    v61 = {
        "label": "run50bq_v61_transition_h2",
        "run_root": RUN50BQ_ROOT,
        "variant_root": RUN50BQ_ROOT / RUN50BQ_V61_ANCHOR,
        "anchor": RUN50BQ_V61_ANCHOR,
        "model": RUN50BQ_ROOT / "models/stage56_context_timed_event_signal_discrete_score_table.csv",
        "signal_column": RUN50BQ_SIGNAL,
        "validation_ini": RUN50BQ_ROOT / RUN50BQ_V61_ANCHOR / "mt5/x02_ta_val.ini",
        "oos_ini": RUN50BQ_ROOT / RUN50BQ_V61_ANCHOR / "mt5/x02_ta_oos.ini",
        "source_note": "Stage59V source anchor: Stage59S strong pre-exit-policy adapter on Stage56 run50BQ v61 context ExtraTrees firewall transition hold2 source",
    }
    return {variant.adapter_id: dict(v61) for variant in STAGE59V_VARIANTS}

def configure_reused_engine() -> None:
    engine.STAGE59_ID = STAGE59V_ID
    engine.NEXT_REPAIR_STAGE_ID = NEXT_REPAIR_STAGE_ID
    engine.RUN_NUMBER = RUN_NUMBER
    engine.RUN_ID = RUN_ID
    engine.PACKET_ID = PACKET_ID
    engine.PARENT_RUN_ID = PARENT_RUN_ID
    engine.SOURCE_ADAPTER_ID = SOURCE_ADAPTER_ID
    engine.DEVELOPMENT_ANCHOR = DEVELOPMENT_ANCHOR
    engine.BACKUP_ANCHOR = BACKUP_ANCHOR
    engine.BOUNDARY = BOUNDARY
    engine.STAGE_ROOT = STAGE_ROOT
    engine.RUN_ROOT = RUN_ROOT
    engine.REVIEWS_ROOT = REVIEWS_ROOT
    engine.SELECTED_ROOT = SELECTED_ROOT
    engine.SPEC_ROOT = SPEC_ROOT
    engine.INPUT_ROOT = INPUT_ROOT
    engine.PACKET_ROOT = PACKET_ROOT
    engine.COMMON_ROOT = COMMON_ROOT
    engine.REPORT_PATH = REPORT_PATH
    engine.SUMMARY_JSON_PATH = SUMMARY_JSON_PATH
    engine.SUMMARY_CSV_PATH = SUMMARY_CSV_PATH
    engine.SEGMENT_KPI_PATH = SEGMENT_KPI_PATH
    engine.EQUITY_AUDIT_PATH = EQUITY_AUDIT_PATH
    engine.RISK_ATR_TELEMETRY_PATH = RISK_ATR_TELEMETRY_PATH
    engine.DECISION_PATH = DECISION_PATH
    engine.AUDIT_CSV_PATH = AUDIT_CSV_PATH
    engine.STAGE_LEDGER_PATH = STAGE_LEDGER_PATH
    engine.RUN_REGISTRY_PATH = RUN_REGISTRY_PATH
    engine.PROJECT_LEDGER_PATH = PROJECT_LEDGER_PATH
    engine.ARTIFACT_REGISTRY_PATH = ARTIFACT_REGISTRY_PATH
    engine.WORKSPACE_STATE_PATH = WORKSPACE_STATE_PATH
    engine.CURRENT_WORKING_STATE_PATH = CURRENT_WORKING_STATE_PATH
    engine.CHANGELOG_PATH = CHANGELOG_PATH
    engine.STAGE59_VARIANTS = STAGE59V_VARIANTS
    engine.SOURCE_SPECS = source_specs()
    engine.MODEL_RISK_MIN_PCT = {variant.adapter_id: 0.005 for variant in STAGE59V_VARIANTS}

    repair.STAGE_ID = STAGE59V_ID
    repair.RUN_NUMBER = RUN_NUMBER
    repair.RUN_ID = RUN_ID
    repair.RUN_ROOT = RUN_ROOT
    repair.REPAIR_VARIANTS = STAGE59V_VARIANTS
    s58.STAGE58_ID = STAGE59V_ID
    s58.RUN_NUMBER = RUN_NUMBER
    s58.RUN_ID = RUN_ID
    s58.PACKET_ID = PACKET_ID
    s58.PARENT_RUN_ID = PARENT_RUN_ID
    s58.RUN_ROOT = RUN_ROOT
    s58.REVIEWS_ROOT = REVIEWS_ROOT
    s58.STAGE58_VARIANTS = STAGE59V_VARIANTS
    s58.COMMON_ROOT = COMMON_ROOT


def extra_set_values(variant: repair.RepairVariant, magic: int) -> dict[str, Any]:
    values = repair.extra_set_values(variant, magic)
    values["InpModelRiskMinPct"] = 0.005
    values["InpModelRiskMaxPct"] = min(float(variant.model_risk_max_pct), 0.05)
    values["InpModelRiskFallbackLot"] = variant.fixed_lot
    return values


def build_attempts(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    for variant_index, variant in enumerate(STAGE59V_VARIANTS, start=1):
        variant_root = RUN_ROOT / variant.adapter_id
        for split in ("validation_is", "oos"):
            date_values = parse_ini(engine.source_attempt_ini(split, variant))
            split_token = "val" if split == "validation_is" else "oos"
            for role_index, (tier, attempt_role, prefix, attempt_token) in enumerate(
                (
                    (mt5.TIER_A, "tier_only_total", f"mt5_tier_a_only_{variant.adapter_id}", "ta"),
                    (mt5.TIER_AB, "routed_total", f"mt5_routed_{variant.adapter_id}", "rt"),
                ),
                start=1,
            ):
                magic = 5905900 + variant_index * 100 + (1 if split == "validation_is" else 50) + role_index
                attempts.append(
                    attempt_payload(
                        run_root=variant_root,
                        run_id=RUN_ID,
                        stage_number=59,
                        exploration_label="stage59V_BaselineAdapter__RiskCapCompressionFromStage59U",
                        attempt_name=f"{variant.adapter_id}_{attempt_token}_{split_token}",
                        tier=tier,
                        split=split,
                        model_path=str(inputs["model_exports"][variant.adapter_id]["common_path"]),
                        model_id=f"{RUN_ID}_{variant.adapter_id}_entry_adapter",
                        model_backend="ebm_table",
                        feature_path=str(inputs["feature_exports"][variant.adapter_id][split]["common_path"]),
                        feature_count=1,
                        feature_order_hash=engine.feature_order_hash_for_variant(variant),
                        short_threshold=variant.short_threshold,
                        long_threshold=variant.long_threshold,
                        min_margin=MIN_MARGIN,
                        invert_signal=False,
                        from_date=str(date_values["FromDate"]),
                        to_date=str(date_values["ToDate"]),
                        primary_active_tier="tier_a",
                        attempt_role=attempt_role,
                        record_view_prefix=prefix,
                        max_hold_bars=variant.max_hold_bars,
                        common_root=f"{COMMON_ROOT}/{variant.adapter_id}",
                        fallback_enabled=False,
                        close_on_flat_signal=variant.close_on_flat_signal,
                        reverse_on_opposite_signal=variant.reverse_on_opposite_signal,
                        close_only_on_opposite_signal=variant.close_only_on_opposite_signal,
                        extra_set_values=extra_set_values(variant, magic),
                    )
                )
    return attempts


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
    return execute_prepared_run_checkpointed(prepared, args)


def partial_path(attempt_name: str) -> Path:
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", attempt_name).strip("_")
    return PARTIALS_ROOT / f"{safe}.json"


def load_partial_results() -> dict[str, dict[str, Any]]:
    if not path_exists(PARTIALS_ROOT):
        return {}
    results: dict[str, dict[str, Any]] = {}
    for path in io_path(PARTIALS_ROOT).glob("*.json"):
        if path.name.endswith(".started.json"):
            continue
        payload = json.loads(io_path(path).read_text(encoding="utf-8-sig"))
        attempt_name = str(payload.get("attempt_name") or path.stem)
        results[attempt_name] = payload
    return results


def selected_attempts(attempts: Sequence[Mapping[str, Any]], args: argparse.Namespace) -> list[Mapping[str, Any]]:
    selected = list(attempts)
    if args.attempt_name_contains:
        selected = [attempt for attempt in selected if args.attempt_name_contains in str(attempt.get("attempt_name") or "")]
    if args.attempt_offset:
        selected = selected[int(args.attempt_offset) :]
    if args.attempt_limit is not None:
        selected = selected[: int(args.attempt_limit)]
    return selected


def execute_prepared_run_checkpointed(prepared: Mapping[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    run_root = Path(prepared["run_root"])
    attempts = list(prepared["attempts"])
    terminal_path = Path(args.terminal_path)
    metaeditor_path = Path(args.metaeditor_path)
    terminal_data_root = Path(args.terminal_data_root)
    common_files_root = Path(args.common_files_root)
    tester_profile_root = Path(args.tester_profile_root)
    compile_payload = mt5.compile_mql5_ea(metaeditor_path, mt5.EA_SOURCE_PATH, run_root / "mt5/mt5_compile.log")
    partials = load_partial_results()
    if compile_payload.get("status") == "completed":
        for attempt in selected_attempts(attempts, args):
            attempt_name = str(attempt.get("attempt_name") or "")
            if args.resume_partials and attempt_name in partials and partials[attempt_name].get("status") == "completed":
                continue
            engine.write_json(PARTIALS_ROOT / f"{attempt_name}.started.json", {"attempt_name": attempt_name, "started_at_utc": utc_now()})
            for key in ("common_telemetry_path", "common_summary_path"):
                target_parent = common_files_root / Path(str(attempt[key])).parent
                io_path(target_parent).mkdir(parents=True, exist_ok=True)
            clear_runtime_outputs(common_files_root, attempt)
            mt5.remove_existing_mt5_report_artifacts(terminal_data_root, attempt)
            try:
                result = mt5.run_mt5_tester(
                    terminal_path,
                    Path(attempt["ini"]["path"]),
                    set_path=Path(attempt["set"]["path"]),
                    tester_profile_set_path=tester_profile_root / EA_TESTER_SET_NAME,
                    tester_profile_ini_path=tester_profile_root / f"opv2_{safe_name(str(prepared['run_id']), 48)}_{attempt_name}.ini",
                    timeout_seconds=int(args.timeout_seconds),
                )
            except Exception as exc:
                result = {
                    "status": "blocked",
                    "command": [str(terminal_path), f"/config:{Path(attempt['ini']['path']).resolve()}"],
                    "returncode": None,
                    "blocker": f"{type(exc).__name__}: {exc}",
                }
            result["tier"] = attempt["tier"]
            result["split"] = attempt["split"]
            result["attempt_name"] = attempt_name
            result["attempt_role"] = attempt.get("attempt_role")
            result["record_view_prefix"] = attempt.get("record_view_prefix")
            if "routing_mode" in attempt:
                result["routing_mode"] = attempt["routing_mode"]
            result["ini_path"] = attempt["ini"]["path"]
            result["runtime_outputs"] = mt5.wait_for_mt5_runtime_outputs(
                common_files_root,
                attempt,
                timeout_seconds=int(args.runtime_output_timeout_seconds),
            )
            if result["runtime_outputs"].get("status") != "completed":
                result["status"] = "blocked"
            partials[attempt_name] = result
            engine.write_json(partial_path(attempt_name), result)

    execution_results = [partials[str(attempt.get("attempt_name") or "")] for attempt in attempts if str(attempt.get("attempt_name") or "") in partials]
    report_records = mt5.collect_mt5_strategy_report_artifacts(
        terminal_data_root=terminal_data_root,
        run_output_root=run_root,
        attempts=attempts,
    )
    mt5.attach_mt5_report_metrics(execution_results, report_records)
    kpi_records = mt5.build_mt5_kpi_records(execution_results)
    kpi_records = mt5.enrich_mt5_kpi_records_with_route_coverage(kpi_records, prepared["route_coverage"])
    completed_attempt_names = {str(item.get("attempt_name") or "") for item in execution_results if item.get("status") == "completed"}
    all_attempt_names = {str(attempt.get("attempt_name") or "") for attempt in attempts}
    completed = bool(execution_results) and completed_attempt_names == all_attempt_names and all(item.get("status") == "completed" for item in execution_results)
    report_completed = bool(kpi_records) and all(item.get("status") == "completed" for item in kpi_records)
    return {
        **dict(prepared),
        "compile": compile_payload,
        "execution_results": execution_results,
        "strategy_tester_reports": report_records,
        "mt5_kpi_records": kpi_records,
        "partial_results_path": rel(PARTIALS_ROOT),
        "completed_attempt_count": len(completed_attempt_names),
        "expected_attempt_count": len(all_attempt_names),
        "external_verification_status": "completed" if completed and report_completed else "blocked",
        "judgment": "inconclusive_stage59v_runtime_probe_completed" if completed and report_completed else "blocked_stage59v_runtime_probe",
    }


def upsert_csv_rows_retry(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], *, key: str) -> dict[str, Any]:
    last_error: OSError | None = None
    for attempt in range(3):
        try:
            return upsert_csv_rows(path, columns, rows, key=key)
        except OSError as exc:
            last_error = exc
            time.sleep(0.5 * (attempt + 1))
    assert last_error is not None
    raise last_error


def best_repaired_variant(summary_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return engine.best_repaired_variant(summary_rows)


def repair_failure_reasons(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]]) -> list[str]:
    return engine.repair_failure_reasons(summary_rows, segment_rows)


def decide_stage(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]], external: str) -> str:
    if external != "completed":
        return "continue_repair_in_new_bounded_stage"
    reasons = repair_failure_reasons(summary_rows, segment_rows)
    if not reasons:
        return "proceed_to_stage60_onnx_hardening"
    severe = {
        "mandatory_model_risk_atr_repaired_variant_missing",
        "validation_net_not_positive_after_repair",
        "oos_net_not_positive_after_repair",
    }
    if severe & set(reasons):
        return "continue_repair_in_new_bounded_stage"
    return "continue_repair_in_new_bounded_stage"


def next_stage_for_decision(decision: str) -> str:
    if decision == "proceed_to_stage60_onnx_hardening":
        return "60_adapter_onnx__hardening_runtime_reproduction"
    if decision == "demote_current_adapter_and_select_backup":
        return "59W_adapter_repair__backup_or_demote_from_stage59v"
    if decision == "open_bounded_followup":
        return "59W_adapter_repair__bounded_followup_from_stage59v"
    return NEXT_REPAIR_STAGE_ID


def next_packet_for_decision(decision: str) -> tuple[str, str]:
    next_stage = next_stage_for_decision(decision)
    if next_stage.startswith("60_"):
        return "stage60_onnx_hardening_v1", "run60A_stage60_onnx_hardening_v1"
    return "stage59w_bounded_followup_from_stage59v_v1", "run59R_stage59w_bounded_followup_from_stage59v_v1"


def artifact_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    created = utc_now()
    paths = [
        REPORT_PATH,
        SUMMARY_JSON_PATH,
        SUMMARY_CSV_PATH,
        SEGMENT_KPI_PATH,
        EQUITY_AUDIT_PATH,
        RISK_ATR_TELEMETRY_PATH,
        DECISION_PATH,
        AUDIT_CSV_PATH,
        STAGE_LEDGER_PATH,
        RUN_ROOT / "run_manifest.json",
        RUN_ROOT / "kpi_record.json",
    ]
    rows: list[dict[str, Any]] = []
    for path in paths:
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{re.sub(r'[^A-Za-z0-9]+', '_', rel(path)).strip('_')}",
                    "stage_id": STAGE59V_ID,
                    "run_id": RUN_ID,
                    "artifact_type": "stage59v_bounded_followup_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "created_at_utc": created,
                    "notes": "Stage59V bounded follow-up from Stage59U artifact.",
                }
            )
    for report in result.get("strategy_tester_reports", []):
        html = report.get("html_report", {}) if isinstance(report.get("html_report"), Mapping) else {}
        raw_path = report.get("path") or html.get("path")
        if not raw_path:
            continue
        report_path = Path(str(raw_path))
        if path_exists(report_path) and io_path(report_path).is_file():
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__mt5_report__{report_path.stem}",
                    "stage_id": STAGE59V_ID,
                    "run_id": RUN_ID,
                    "artifact_type": "mt5_strategy_tester_report",
                    "path": rel(report_path),
                    "sha256": sha256_file_lf_normalized(report_path),
                    "created_at_utc": created,
                    "notes": "Actual Stage59V MT5 Strategy Tester HTML report.",
                }
            )
    return rows


def write_run_identity(result: Mapping[str, Any]) -> None:
    engine.write_json(
        RUN_ROOT / "run_manifest.json",
        {
            "run_id": RUN_ID,
            "packet_id": PACKET_ID,
            "stage_id": STAGE59V_ID,
            "stage_number": 59,
            "run_number": RUN_NUMBER,
            "bounded_question": "Can bounded model-risk-cap compression on the Stage59S pre-exit-policy anchor reduce OOS drawdown and late concentration while preserving validation/OOS PF, net, cost-stressed expectancy, segment KPI, ATR/bracket telemetry, and model-controlled risk behavior without starting ONNX?",
            "source_stage59u_decision": rel(SOURCE_STAGE59U_DECISION),
            "source_stage59u_pushed_commit": SOURCE_STAGE59U_PUSHED_COMMIT,
            "source_stage59s_decision": rel(SOURCE_STAGE59S_DECISION),
            "source_stage59s_pushed_commit": SOURCE_STAGE59S_PUSHED_COMMIT,
            "variants": [
                {
                    **variant.__dict__,
                    "source_anchor": engine.source_anchor_for_variant(variant),
                    "signal_column": engine.signal_column_for_variant(variant),
                    "feature_order_hash": engine.feature_order_hash_for_variant(variant),
                }
                for variant in STAGE59V_VARIANTS
            ],
            "attempts": result.get("attempts", []),
            "common_copies": result.get("common_copies", []),
            "compile": result.get("compile", {}),
            "route_coverage": result.get("route_coverage", {}),
            "external_verification_status": result.get("external_verification_status"),
            "judgment": result.get("judgment"),
            "claim_boundary": BOUNDARY,
        },
    )
    engine.write_json(
        RUN_ROOT / "kpi_record.json",
        {
            "run_id": RUN_ID,
            "packet_id": PACKET_ID,
            "stage_id": STAGE59V_ID,
            "mt5_kpi_records": result.get("mt5_kpi_records", []),
            "strategy_tester_reports": result.get("strategy_tester_reports", []),
            "execution_results": result.get("execution_results", []),
            "external_verification_status": result.get("external_verification_status"),
            "judgment": result.get("judgment"),
            "claim_boundary": BOUNDARY,
        },
    )


def write_ledgers(
    result: Mapping[str, Any],
    summary_rows: Sequence[Mapping[str, Any]],
    segment_rows: Sequence[Mapping[str, Any]],
    decision: str,
    artifacts: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    external = str(result.get("external_verification_status") or "blocked")
    best = best_repaired_variant(summary_rows)
    val = best.get("validation") if isinstance(best.get("validation"), Mapping) else {}
    oos = best.get("oos") if isinstance(best.get("oos"), Mapping) else {}
    status = "completed" if external == "completed" else "blocked"
    run_payload = upsert_csv_rows_retry(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE59V_ID,
                "lane": "baseline_adapter_bounded_followup_from_stage59u",
                "status": status,
                "judgment": decision,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_adapter", SOURCE_ADAPTER_ID),
                        ("best_repaired_adapter", best.get("adapter_id")),
                        ("validation_net", val.get("net_profit")),
                        ("oos_net", oos.get("net_profit")),
                        ("boundary", BOUNDARY),
                    )
                ),
            }
        ],
        key="run_id",
    )
    ledger_rows = build_mt5_alpha_ledger_rows(
        run_id=RUN_ID,
        stage_id=STAGE59V_ID,
        mt5_kpi_records=result.get("mt5_kpi_records", []),
        run_output_root=RUN_ROOT,
        external_verification_status=external,
    )
    ledger_rows.append(
        {
            "ledger_row_id": f"{RUN_ID}__aggregate_bounded_followup_from_stage59u",
            "stage_id": STAGE59V_ID,
            "run_id": RUN_ID,
            "subrun_id": "aggregate_bounded_followup_from_stage59u",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "bounded_followup_from_stage59u",
            "tier_scope": "Tier A+B",
            "kpi_scope": "baseline_adapter_repair",
            "scoreboard_lane": "runtime_probe",
            "status": status,
            "judgment": decision,
            "path": rel(DECISION_PATH),
            "primary_kpi": ledger_pairs(
                (
                    ("best_repaired_adapter", best.get("adapter_id")),
                    ("validation_net", val.get("net_profit")),
                    ("oos_net", oos.get("net_profit")),
                    ("validation_pf", val.get("profit_factor")),
                    ("oos_pf", oos.get("profit_factor")),
                )
            ),
            "guardrail_kpi": ledger_pairs(
                (
                    ("failure_reasons", repair_failure_reasons(summary_rows, segment_rows)),
                    ("atr_sltp", "measured"),
                    ("model_controlled_risk_pct", "measured"),
                    ("overall_goal_complete", False),
                )
            ),
            "external_verification_status": external,
            "notes": "Stage59V bounded model-risk-cap compression follow-up from Stage59U failure memory and Stage59S source anchor evidence; not final package completion.",
        }
    )
    stage_payload = upsert_csv_rows_retry(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id")
    project_payload = upsert_csv_rows_retry(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id")
    artifact_payload = upsert_csv_rows_retry(ARTIFACT_REGISTRY_PATH, aw.ARTIFACT_COLUMNS, list(artifacts), key="artifact_id")
    return {"run_registry": run_payload, "stage_ledger": stage_payload, "project_alpha_ledger": project_payload, "artifact_registry": artifact_payload}


def report_markdown(summary_rows: Sequence[Mapping[str, Any]], decision: str, reasons: Sequence[str], external: str) -> str:
    rows = [row for row in summary_rows if row.get("view") == "actual_routed_total"]
    table = "\n".join(
        "| {adapter} | {split} | {pf} | {net} | {dd} | {cost} | {risk} | {lot} | {sl} | {tp} |".format(
            adapter=row.get("adapter_id"),
            split=row.get("split"),
            pf=aw.fmt(row.get("profit_factor")),
            net=aw.fmt(row.get("net_profit")),
            dd=aw.fmt(row.get("max_drawdown_amount")),
            cost=aw.fmt(row.get("cost_stressed_expectancy")),
            risk=aw.fmt(row.get("avg_model_risk_pct")),
            lot=aw.fmt(row.get("avg_executed_lot")),
            sl=aw.fmt(row.get("avg_open_sl_points")),
            tp=aw.fmt(row.get("avg_open_tp_points")),
        )
        for row in rows
    )
    best = best_repaired_variant(summary_rows)
    return f"""# Stage59V Risk Cap Compression From Stage59U Report(59V단계 59U단계 기반 위험 상한 압축 보고서)

- stage(단계): `{STAGE59V_ID}`
- run(실행): `{RUN_ID}`
- source_decision(원천 판정): `continue_repair_in_new_bounded_stage`
- external_verification_status(외부 검증 상태): `{external}`
- decision(판정): `{decision}`
- boundary(경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Can bounded model-risk-cap compression(경계 모델 위험 상한 압축)이 Stage59S pre-exit-policy anchor(59S단계 청산 정책 이전 기준점)의 OOS drawdown(표본외 손실폭)과 late concentration(후반 집중)을 줄이면서 validation/OOS PF(검증/표본외 수익 팩터), net(순손익), cost-stressed expectancy(비용 압박 기대값), segment KPI(구간 KPI), ATR/bracket telemetry(ATR/브래킷 텔레메트리), model-controlled risk behavior(모델 제어 위험 동작)을 보존할 수 있는가?

## Result Table(결과 표)

| adapter(어댑터) | split(구간) | PF(수익 팩터) | net(순손익) | DD(드로다운) | cost exp(비용 압박 기대값) | avg risk(평균 위험률) | lot(랏) | SL(손절) | TP(익절) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
{table}

## Read(판독)

- best_repaired_adapter(최선 수리 어댑터): `{best.get('adapter_id', 'none')}`
- failure_reasons(실패/약점 사유): `{";".join(reasons) if reasons else "none"}`
- bounded_followup_summary(경계 후속 요약): `{rel(SUMMARY_CSV_PATH)}`
- bounded_followup_segment_kpi_summary(경계 후속 구간 KPI 요약): `{rel(SEGMENT_KPI_PATH)}`
- bounded_followup_risk_atr_telemetry(경계 후속 위험/ATR 텔레메트리): `{rel(RISK_ATR_TELEMETRY_PATH)}`

Effect(효과): Stage59V(59V단계)는 Stage59U failure memory(59U단계 실패 기억)를 입력으로 보존하되, source anchor(원천 기준점), thresholds(임계값), ATR bracket(ATR 브래킷), cooldown(쿨다운), max_hold_bars(최대 보유 봉수), close-only lifecycle(청산 전용 생명주기)를 고정하고 model_risk_max_pct(모델 위험 상한)만 바꿔 final adapter completion(최종 어댑터 완료)이나 ONNX hardening(ONNX 경화)으로 자동 진행하지 않는다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
"""


def equity_audit_markdown(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]]) -> str:
    best = best_repaired_variant(summary_rows)
    best_id = best.get("adapter_id", "none")
    best_segments = [row for row in segment_rows if row.get("adapter_id") == best_id]
    flags = sorted({str(row.get("quality_flag")) for row in best_segments if row.get("quality_flag") and row.get("quality_flag") != "acceptable_measurement_only"})
    lines = "\n".join(
        f"- {row.get('split')} {row.get('segment_type')} {row.get('segment')}: net(순손익) `{aw.fmt(row.get('net_profit'))}`, PF(수익 팩터) `{aw.fmt(row.get('profit_factor'))}`, flag(표식) `{row.get('quality_flag')}`"
        for row in best_segments
        if row.get("segment_type") == "chronological_third"
    )
    return f"""# Stage59V Bounded Followup Equity Curve Audit(59V단계 경계 후속 자금 곡선 감사)

- best_repaired_adapter(최선 수리 어댑터): `{best_id}`
- audit_boundary(감사 경계): `segment/equity measurement only(구간/자금 측정 전용)`
- quality_flags(품질 표식): `{";".join(flags) if flags else "none"}`

## Chronological Thirds(시간 순서 3분할)

{lines if lines else "- segment_rows(구간 행): `missing_or_not_completed`"}

Effect(효과): final net(최종 순손익)만 보지 않고 validation/OOS(검증/표본외) 구간 흔들림, drawdown recovery(드로다운 회복), late flatline risk(후반 정체 위험)를 다음 판정에 반영한다.
"""


def decision_markdown(decision: str, reasons: Sequence[str], best: Mapping[str, Any], external: str) -> str:
    return f"""# Stage59V Decision(59V단계 판정)

decision(판정): `{decision}`

Stage59V(59V단계)는 Stage59U evidence(59U단계 근거)와 Stage59S source anchor(59S단계 원천 기준점)를 사용한 bounded risk-cap compression follow-up(경계 위험 상한 압축 후속)으로 기록한다. Effect(효과): model_risk_max_pct(모델 위험 상한) 압축의 성공/실패를 다음 bounded stage(경계 다음 단계)의 입력 근거로 넘긴다.

## Evidence(근거)

- report(보고서): `{rel(REPORT_PATH)}`
- repaired_adapter_summary(수리 어댑터 요약): `{rel(SUMMARY_CSV_PATH)}`
- repaired_segment_kpi_summary(수리 구간 KPI 요약): `{rel(SEGMENT_KPI_PATH)}`
- repaired_equity_curve_audit(수리 자금 곡선 감사): `{rel(EQUITY_AUDIT_PATH)}`
- repaired_risk_atr_telemetry(수리 위험/ATR 텔레메트리): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- external_verification_status(외부 검증 상태): `{external}`

## Reason(이유)

- best_repaired_adapter(최선 수리 어댑터): `{best.get('adapter_id', 'none')}`
- failure_reasons(실패/약점 사유): `{";".join(reasons) if reasons else "none"}`

## Next(다음)

next_stage_or_branch(다음 단계/분기): `{next_stage_for_decision(decision)}`

Stage59V closeout(59V단계 종료)는 overall goal completion(전체 목표 완료)이 아니다. Effect(효과): Stage60 ONNX hardening(60단계 ONNX 경화)은 adapter quality(어댑터 품질)가 강할 때만 열린다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
"""


def write_required_outputs(
    result: Mapping[str, Any],
    summary_rows: Sequence[Mapping[str, Any]],
    risk_rows: Sequence[Mapping[str, Any]],
    segment_rows: Sequence[Mapping[str, Any]],
    decision: str,
    ledger_payload: Mapping[str, Any],
) -> None:
    reasons = repair_failure_reasons(summary_rows, segment_rows)
    best = best_repaired_variant(summary_rows)
    external = str(result.get("external_verification_status") or "blocked")
    engine.write_csv(SUMMARY_CSV_PATH, summary_rows)
    engine.write_csv(SEGMENT_KPI_PATH, segment_rows)
    engine.write_csv(RISK_ATR_TELEMETRY_PATH, risk_rows)
    engine.write_md(REPORT_PATH, report_markdown(summary_rows, decision, reasons, external))
    engine.write_md(EQUITY_AUDIT_PATH, equity_audit_markdown(summary_rows, segment_rows))
    engine.write_md(DECISION_PATH, decision_markdown(decision, reasons, best, external))
    engine.write_json(
        SUMMARY_JSON_PATH,
        {
            "created_at_utc": utc_now(),
            "stage_id": STAGE59V_ID,
            "run_id": RUN_ID,
            "packet_id": PACKET_ID,
            "source_stage59u_decision": rel(SOURCE_STAGE59U_DECISION),
            "source_stage59u_pushed_commit": SOURCE_STAGE59U_PUSHED_COMMIT,
            "source_stage59s_decision": rel(SOURCE_STAGE59S_DECISION),
            "source_stage59s_pushed_commit": SOURCE_STAGE59S_PUSHED_COMMIT,
            "source_adapter": SOURCE_ADAPTER_ID,
            "variants": [
                {
                    **variant.__dict__,
                    "source_anchor": engine.source_anchor_for_variant(variant),
                    "signal_column": engine.signal_column_for_variant(variant),
                    "feature_order_hash": engine.feature_order_hash_for_variant(variant),
                }
                for variant in STAGE59V_VARIANTS
            ],
            "external_verification_status": external,
            "decision": decision,
            "best_repaired_variant": best,
            "failure_reasons": reasons,
            "required_outputs": {
                "bounded_followup_report": rel(REPORT_PATH),
                "bounded_followup_summary_json": rel(SUMMARY_JSON_PATH),
                "bounded_followup_summary_csv": rel(SUMMARY_CSV_PATH),
                "bounded_followup_segment_kpi_summary": rel(SEGMENT_KPI_PATH),
                "bounded_followup_equity_curve_audit": rel(EQUITY_AUDIT_PATH),
                "bounded_followup_risk_atr_telemetry": rel(RISK_ATR_TELEMETRY_PATH),
                "stage59v_decision": rel(DECISION_PATH),
            },
            "ledger_payload": ledger_payload,
            "claim_boundary": BOUNDARY,
            "overall_goal_complete": False,
        },
    )


def write_packet_files(
    result: Mapping[str, Any],
    summary_rows: Sequence[Mapping[str, Any]],
    segment_rows: Sequence[Mapping[str, Any]],
    risk_rows: Sequence[Mapping[str, Any]],
    decision: str,
    ledger_payload: Mapping[str, Any],
) -> None:
    external = str(result.get("external_verification_status") or "blocked")
    reasons = repair_failure_reasons(summary_rows, segment_rows)
    best = best_repaired_variant(summary_rows)
    files = {
        "routing_receipt.json": {
            "packet_id": PACKET_ID,
            "primary_family": "adapter_development",
            "primary_skill": "obsidian-model-validation",
            "support_skills": ["obsidian-experiment-design", "obsidian-runtime-parity", "obsidian-backtest-forensics", "obsidian-result-judgment"],
            "required_gates": [
                "experiment_design_receipt",
                "runtime_evidence_gate",
                "kpi_contract_audit",
                "result_judgment_gate",
                "artifact_lineage_audit",
                "final_claim_guard",
            ],
            "status": "completed",
        },
        "experiment_design_receipt.json": {
            "hypothesis": "A bounded model-risk-cap compression on the Stage59S pre-exit-policy anchor may reduce OOS drawdown and late concentration while preserving validation/OOS PF, net, cost-stressed expectancy, segment KPI, ATR/bracket telemetry, and model-controlled risk behavior.",
            "decision_use": "Route to Stage60 only if the full post-ATR/risk adapter evidence is strong; otherwise continue bounded repair, demote, or open another branch.",
            "comparison_baseline": "Stage59S best candidate s59s_v61_long54_sl20_tp30_sd12_h5_rearm002, with Stage59U flat_reverse weakness preserved as failure memory.",
            "control_variables": ["US100", "M5", "split_v1", "Tier B disabled", "run50BQ v61 source anchor", "short threshold 0.52", "long threshold 0.54", "same-direction cooldown 12", "ATR SL 2.0", "ATR TP 3.0", "max hold 5", "close-only-on-opposite lifecycle", "entry transition rearm 0.02", "ONNX deferred"],
            "changed_variables": ["model_risk_max_pct"],
            "sample_scope": "FPMarkets US100 M5 validation 2025-01-01 to 2025-09-30 and OOS 2025-10-01 to 2026-04-13.",
            "success_criteria": ["validation and OOS net positive", "validation and OOS PF >= 1.10", "validation and OOS cost-stressed expectancy positive", "ATR and model risk telemetry present", "no severe segment flags"],
            "failure_criteria": ["negative validation/OOS net", "PF < 1.10", "cost-stressed expectancy <= 0", "missing risk or ATR telemetry", "segment flags remain"],
            "invalid_conditions": ["missing model table", "missing feature files", "missing MT5 report", "telemetry parse failure"],
            "stop_conditions": "three bounded Stage59V model-risk-cap compression variants only",
            "evidence_plan": [rel(SUMMARY_CSV_PATH), rel(SEGMENT_KPI_PATH), rel(EQUITY_AUDIT_PATH), rel(RISK_ATR_TELEMETRY_PATH), rel(DECISION_PATH)],
            "status": "completed",
        },
        "runtime_evidence_gate.json": {"external_verification_status": external, "mt5_reports": result.get("strategy_tester_reports", []), "status": external},
        "kpi_contract_audit.json": {"summary_rows": len(summary_rows), "segment_rows": len(segment_rows), "risk_rows": len(risk_rows), "status": "completed"},
        "result_judgment_gate.json": {
            "result_subject": RUN_ID,
            "evidence_available": [rel(REPORT_PATH), rel(SUMMARY_CSV_PATH), rel(SEGMENT_KPI_PATH), rel(RISK_ATR_TELEMETRY_PATH)],
            "evidence_missing": [] if external == "completed" else ["completed_mt5_external_verification"],
            "judgment_label": decision,
            "failure_reasons": reasons,
            "best_repaired_adapter": best.get("adapter_id", "none"),
            "claim_boundary": BOUNDARY,
            "next_condition": next_stage_for_decision(decision),
            "status": "passed_with_boundary",
        },
        "artifact_lineage_audit.json": {
            "source_inputs": [
                rel(SOURCE_STAGE59U_DECISION),
                rel(SOURCE_STAGE59U_REPORT),
                rel(SOURCE_STAGE59U_SUMMARY),
                rel(SOURCE_STAGE59U_JSON),
                rel(SOURCE_STAGE59S_DECISION),
                rel(SOURCE_STAGE59S_REPORT),
                rel(SOURCE_STAGE59S_SUMMARY),
                rel(SOURCE_STAGE59S_JSON),
            ],
            "consumers": [rel(REPORT_PATH), rel(DECISION_PATH), rel(SUMMARY_JSON_PATH)],
            "ledger_links": ledger_payload,
        },
        "final_claim_guard.json": {
            "overall_goal_complete": False,
            "deployment_claim": False,
            "live_readiness_claim": False,
            "runtime_authority_claim": False,
            "production_baseline_claim": False,
            "operating_reference_claim": False,
            "operating_promotion_claim": False,
            "status": "passed",
        },
        "required_gate_coverage_audit.json": {
            "required_gates": [
                "experiment_design_receipt",
                "runtime_evidence_gate",
                "kpi_contract_audit",
                "result_judgment_gate",
                "artifact_lineage_audit",
                "final_claim_guard",
            ],
            "covered_by": [
                "experiment_design_receipt.json",
                "runtime_evidence_gate.json",
                "kpi_contract_audit.json",
                "result_judgment_gate.json",
                "artifact_lineage_audit.json",
                "final_claim_guard.json",
            ],
            "status": "completed",
        },
        "aggregate_summary.json": {
            "packet_id": PACKET_ID,
            "stage_id": STAGE59V_ID,
            "run_id": RUN_ID,
            "decision": decision,
            "external_verification_status": external,
            "required_outputs": {
                "bounded_followup_report": rel(REPORT_PATH),
                "bounded_followup_summary_json": rel(SUMMARY_JSON_PATH),
                "bounded_followup_summary_csv": rel(SUMMARY_CSV_PATH),
                "bounded_followup_segment_kpi_summary": rel(SEGMENT_KPI_PATH),
                "bounded_followup_equity_curve_audit": rel(EQUITY_AUDIT_PATH),
                "bounded_followup_risk_atr_telemetry": rel(RISK_ATR_TELEMETRY_PATH),
                "stage59v_decision": rel(DECISION_PATH),
            },
            "claim_boundary": BOUNDARY,
            "overall_goal_complete": False,
        },
    }
    for name, payload in files.items():
        engine.write_json(PACKET_ROOT / name, payload)


def write_stage_docs(decision: str) -> None:
    next_stage = next_stage_for_decision(decision)
    engine.write_md(
        SPEC_ROOT / "stage_brief.md",
        f"""# Stage59V Brief(59V단계 개요)

- stage_id(단계 ID): `{STAGE59V_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE59U_ID}`
- source_decision(원천 판정): `continue_repair_in_new_bounded_stage`
- bounded_question(경계 질문): `Can bounded model-risk-cap compression on the Stage59S pre-exit-policy anchor reduce OOS drawdown and late concentration while preserving validation/OOS PF, net, cost-stressed expectancy, segment KPI, ATR/bracket telemetry, and model-controlled risk behavior without starting ONNX?`
- boundary(경계): `{BOUNDARY}`

Stage59V(59V단계)는 Stage59U(59U단계) failure memory(실패 기억)를 보존하고, Stage59S(59S단계) best adapter(최선 어댑터)의 source anchor(원천 기준점), thresholds(임계값), ATR bracket(ATR 브래킷), cooldown(쿨다운), max_hold_bars(최대 보유 봉수), close-only lifecycle(청산 전용 생명주기)를 유지하며 model_risk_max_pct(모델 위험 상한) 세 변형만 측정한다. Effect(효과): Stage60 ONNX(60단계 ONNX)나 deployment(배포)로 이어가지 않고 위험 상한 압축이 OOS drawdown(표본외 손실폭)과 구간 약점을 줄이는지만 본다.
""",
    )
    engine.write_md(
        INPUT_ROOT / "input_refs.md",
        f"""# Stage59V Input References(59V단계 입력 참조)

- stage59u_decision(59U단계 판정): `{rel(SOURCE_STAGE59U_DECISION)}`
- stage59u_report(59U단계 보고서): `{rel(SOURCE_STAGE59U_REPORT)}`
- stage59u_summary(59U단계 요약): `{rel(SOURCE_STAGE59U_SUMMARY)}`
- stage59u_pushed_commit(59U단계 푸시 커밋): `{SOURCE_STAGE59U_PUSHED_COMMIT}`
- stage59s_decision(59S단계 판정): `{rel(SOURCE_STAGE59S_DECISION)}`
- stage59s_report(59S단계 보고서): `{rel(SOURCE_STAGE59S_REPORT)}`
- stage59s_summary(59S단계 요약): `{rel(SOURCE_STAGE59S_SUMMARY)}`
- stage59s_pushed_commit(59S단계 푸시 커밋): `{SOURCE_STAGE59S_PUSHED_COMMIT}`
- run50bq_source_model(run50BQ 원천 모델): `{rel(RUN50BQ_ROOT / "models/stage56_context_timed_event_signal_discrete_score_table.csv")}`
- run50bq_v61_source(run50BQ v61 원천): `{rel(RUN50BQ_ROOT / RUN50BQ_V61_ANCHOR)}`
- stage59v_changed_variable(59V단계 변경 변수): `model_risk_max_pct_only`

Effect(효과): Stage59V(59V단계)는 Stage59U(59U단계) 실패 기억과 Stage59S(59S단계) 강한 기준점, run50BQ(run50BQ) v61 원천을 고정한 model_risk_max_pct(모델 위험 상한) 변형을 명시적으로 연결한다.
""",
    )
    engine.write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage59V Selection Status(59V단계 선택 상태)

- stage_status(단계 상태): `closed_bounded_followup_from_stage59u`
- source_stage(원천 단계): `{SOURCE_STAGE59U_ID}`
- source_decision(원천 판정): `continue_repair_in_new_bounded_stage`
- stage59v_decision(59V단계 판정): `{decision}`
- next_stage_or_branch(다음 단계/분기): `{next_stage}`
- selected_research_baseline(선택 연구 기준선): `none`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage59V(59V단계)는 측정 결과를 보존하지만 final package(최종 패키지)나 operating claim(운영 주장)을 만들지 않는다.
""",
    )
    engine.write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage59V Review Index(59V단계 검토 색인)

- bounded_followup_report(경계 후속 보고서): `{rel(REPORT_PATH)}`
- bounded_followup_summary(경계 후속 요약): `{rel(SUMMARY_CSV_PATH)}`
- bounded_followup_segment_kpi(경계 후속 구간 KPI): `{rel(SEGMENT_KPI_PATH)}`
- bounded_followup_equity_curve_audit(경계 후속 자금 곡선 감사): `{rel(EQUITY_AUDIT_PATH)}`
- bounded_followup_risk_atr_telemetry(경계 후속 위험/ATR 텔레메트리): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- stage59v_decision(59V단계 판정): `{rel(DECISION_PATH)}`
""",
    )
    if not next_stage.startswith("60_"):
        next_root = Path("stages") / next_stage
        engine.write_md(
            next_root / "00_spec/stage_brief.md",
            f"""# Stage59W Brief(59W단계 개요)

- stage_id(단계 ID): `{next_stage}`
- source_stage(원천 단계): `{STAGE59V_ID}`
- source_decision(원천 판정): `{decision}`
- bounded_question(경계 질문): `What bounded follow-up should repair, demote, or branch from the Stage59V evidence without starting ONNX prematurely?`
- boundary(경계): `{BOUNDARY}`

Stage59W(59W단계)는 Stage59V(59V단계) 결과가 Stage60 ONNX(60단계 ONNX)에 충분하지 않을 때 이어지는 bounded follow-up(경계 후속)이다. Effect(효과): repair(수리), demotion(강등), branch(분기)를 다음 작은 질문으로 제한한다.
""",
        )
        engine.write_md(
            next_root / "01_inputs/input_refs.md",
            f"""# Stage59W Input References(59W단계 입력 참조)

- stage59v_decision(59V단계 판정): `{rel(DECISION_PATH)}`
- stage59v_report(59V단계 보고서): `{rel(REPORT_PATH)}`
- stage59v_summary(59V단계 요약): `{rel(SUMMARY_CSV_PATH)}`
- stage59v_segment_kpi(59V단계 구간 KPI): `{rel(SEGMENT_KPI_PATH)}`
- stage59v_risk_atr_telemetry(59V단계 위험/ATR 텔레메트리): `{rel(RISK_ATR_TELEMETRY_PATH)}`
""",
        )
        engine.write_md(
            next_root / "03_reviews/review_index.md",
            """# Stage59W Review Index(59W단계 검토 색인)

Stage59W(59W단계)는 planned(계획) 상태다. Effect(효과): Stage59V(59V단계) 약점을 다음 bounded repair(경계 수리) 근거로 넘긴다.
""",
        )
        engine.write_md(
            next_root / "04_selected/selection_status.md",
            f"""# Stage59W Selection Status(59W단계 선택 상태)

- stage_status(단계 상태): `active_planned_from_stage59v`
- source_stage(원천 단계): `{STAGE59V_ID}`
- source_decision(원천 판정): `{decision}`
- selected_research_baseline(선택 연구 기준선): `none`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage59W(59W단계)는 Stage59V(59V단계) 이후 필요한 다음 작은 질문만 다룬다.
""",
        )


def update_current_truth(decision: str, summary_rows: Sequence[Mapping[str, Any]], external: str) -> None:
    best = best_repaired_variant(summary_rows)
    next_stage = next_stage_for_decision(decision)
    next_packet, next_run = next_packet_for_decision(decision)
    engine.write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{next_packet}`
- current_run(현재 실행): `{next_run}`
- active_stage(활성 단계): `{next_stage}`
- selected_research_baseline(선택 연구 기준선): `none`
- development_anchor(개발 기준점): `{DEVELOPMENT_ANCHOR}`
- backup_anchor(예비 기준점): `{BACKUP_ANCHOR}`
- adapter_under_review(검토 중 어댑터): `{best.get('adapter_id', SOURCE_ADAPTER_ID)}`
- status(상태): `stage59v_closed_{decision}`
- claim_boundary(주장 경계): research/development only(연구/개발 전용)

Stage59V(59V단계) closed(종료) as bounded risk-cap compression follow-up from Stage59U(59U단계 기반 경계 위험 상한 압축 후속). Effect(효과): Stage59U(59U단계) flat_reverse weakness(평탄 반전 약점)는 보존하고, Stage59S(59S단계) strong anchor(강한 기준점)의 risk cap(위험 상한) 압축 결과를 다음 판단에 넘긴다.

## Latest Stage59V Evidence(최신 59V단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- best_repaired_adapter(최선 수리 어댑터): `{best.get('adapter_id', 'none')}`
- external_verification_status(외부 검증 상태): `{external}`
- next_stage_or_branch(다음 단계/분기): `{next_stage}`
- report(보고서): `{rel(REPORT_PATH)}`
- stage59v_decision(59V단계 판정): `{rel(DECISION_PATH)}`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), overall_goal_complete(전체 목표 완료).
""",
    )
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = re.sub(r"^current_run_id: .*$", f"current_run_id: {next_run}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^updated_on: .*$", "updated_on: '2026-05-16'", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^active_stage: .*$", f"active_stage: {next_stage}", text, count=1, flags=re.MULTILINE)
    focus = (
        "current_focus:\n"
        f"- >-\n"
        f"  Stage59V(59V단계) `{STAGE59V_ID}` closed(종료) as bounded risk-cap compression follow-up from Stage59U(59U단계 기반 경계 위험 상한 압축 후속); decision(판정)=`{decision}`. "
        f"Effect(효과): full BaselineAdapter repair(전체 기준선 어댑터 수리)는 계속 research/development boundary(연구/개발 경계) 안에 있으며 final(최종) 또는 operating(운영) 주장은 없다.\n"
        f"- >-\n"
        f"  Next stage_or_branch(다음 단계/분기) `{next_stage}` is active/planned(활성/계획). Effect(효과): Stage59V(59V단계) 결과를 다음 bounded step(경계 다음 단계)으로 넘긴다.\n"
    )
    text = re.sub(
        r"current_focus:\n(?:- >-\n  Stage59V[^\n]*\n- >-\n  Next stage_or_branch[^\n]*\n)+",
        "current_focus:\n",
        text,
        count=1,
    )
    text = re.sub(r"current_focus:\n", focus, text, count=1)
    block = f"""

stage59v_bounded_followup_from_stage59u:
  packet_id: {PACKET_ID}
  stage_id: {STAGE59V_ID}
  status: closed_bounded_followup_from_stage59u
  current_run_id: {RUN_ID}
  source_adapter: {SOURCE_ADAPTER_ID}
  source_stage59s_pushed_commit: {SOURCE_STAGE59S_PUSHED_COMMIT}
  source_stage59u_pushed_commit: {SOURCE_STAGE59U_PUSHED_COMMIT}
  best_repaired_adapter: {best.get('adapter_id', 'none')}
  decision: {decision}
  next_stage_or_branch: {next_stage}
  report_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  external_verification_status: {external}
  boundary: {BOUNDARY}
"""
    if "stage59v_bounded_followup_from_stage59u:" in text:
        text = re.sub(r"\nstage59v_bounded_followup_from_stage59u:\n(?:  .*\n)*", block, text, count=1)
    else:
        text += block
    io_path(WORKSPACE_STATE_PATH).write_text(text, encoding="utf-8-sig")


def append_changelog(decision: str) -> None:
    entry = (
        "\n## 2026-05-16 - Stage59V bounded risk-cap compression follow-up from Stage59U closeout(59V단계 59U단계 기반 경계 위험 상한 압축 후속 종료)\n\n"
        f"- run(실행): `{RUN_ID}`\n"
        f"- decision(판정): `{decision}`\n"
        "- effect(효과): Stage59U(59U단계) evidence(근거)와 Stage59S(59S단계) source anchor(원천 기준점)를 model-risk-cap variants(모델 위험 상한 변형) 세 개로 측정하고 다음 bounded stage(경계 다음 단계) 조건을 남겼다.\n"
    )
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if f"- run(실행): `{RUN_ID}`" not in existing:
        io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage59V bounded follow-up from Stage59U.")
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(METAEDITOR_PATH_DEFAULT))
    parser.add_argument("--terminal-data-root", default=str(TERMINAL_DATA_ROOT_DEFAULT))
    parser.add_argument("--common-files-root", default=str(COMMON_FILES_ROOT_DEFAULT))
    parser.add_argument("--tester-profile-root", default=str(TESTER_PROFILE_ROOT_DEFAULT))
    parser.add_argument("--timeout-seconds", type=int, default=120)
    parser.add_argument("--runtime-output-timeout-seconds", type=int, default=180)
    parser.add_argument("--attempt-name-contains", default="")
    parser.add_argument("--attempt-offset", type=int, default=0)
    parser.add_argument("--attempt-limit", type=int)
    parser.add_argument("--resume-partials", action="store_true")
    parser.add_argument("--skip-compile", action="store_true")
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--finalize-existing", action="store_true")
    parser.add_argument("--cost-stress-per-trade", type=float, default=0.3)
    return parser.parse_args(argv)


def load_existing_result() -> dict[str, Any]:
    manifest = RUN_ROOT / "run_manifest.json"
    kpi = RUN_ROOT / "kpi_record.json"
    if not path_exists(manifest) or not path_exists(kpi):
        raise FileNotFoundError("Stage59V existing run_manifest.json or kpi_record.json is missing")
    payload = json.loads(io_path(manifest).read_text(encoding="utf-8-sig"))
    payload.update(json.loads(io_path(kpi).read_text(encoding="utf-8-sig")))
    return payload


def main(argv: Sequence[str] | None = None) -> int:
    configure_reused_engine()
    args = parse_args(argv or sys.argv[1:])
    if args.finalize_existing:
        result = load_existing_result()
    else:
        inputs = engine.prepare_inputs(Path(args.common_files_root))
        attempts = build_attempts(inputs)
        prepared = {
            "run_id": RUN_ID,
            "stage_id": STAGE59V_ID,
            "stage_number": 59,
            "run_number": RUN_NUMBER,
            "run_root": RUN_ROOT,
            "packet_id": PACKET_ID,
            "attempts": attempts,
            "common_copies": inputs["common_copies"],
            "feature_exports": inputs["feature_exports"],
            "model_artifacts": inputs["model_exports"],
            "route_coverage": engine.route_coverage(),
            "model_family": "baseline_adapter_stage59v_risk_cap_compression_ebm_table",
            "feature_set_id": "stage59v_run50bq_v61_risk_cap_compression_signal",
            "label_id": "label_v1_fwd12_m5_logret_train_q33_3class",
            "split_contract": "split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413",
            "claim_boundary": BOUNDARY,
        }
        result = execute_or_materialize(prepared, args)
    audit_rows = s58.audit_rows_for_result(result, float(args.cost_stress_per_trade)) if result.get("mt5_kpi_records") else []
    risk_rows = s58.risk_rows_from_result(result)
    summary_rows = s58.build_summary_rows(result, audit_rows, risk_rows)
    segment_rows = s58.segment_kpi_rows(summary_rows)
    external = str(result.get("external_verification_status") or "blocked")
    decision = decide_stage(summary_rows, segment_rows, external)
    write_run_identity(result)
    engine.write_csv(AUDIT_CSV_PATH, audit_rows)
    artifacts = artifact_rows(result)
    ledger_payload = write_ledgers(result, summary_rows, segment_rows, decision, artifacts)
    write_required_outputs(result, summary_rows, risk_rows, segment_rows, decision, ledger_payload)
    artifacts = artifact_rows(result)
    ledger_payload = write_ledgers(result, summary_rows, segment_rows, decision, artifacts)
    payload = json.loads(io_path(SUMMARY_JSON_PATH).read_text(encoding="utf-8-sig"))
    payload["ledger_payload"] = ledger_payload
    engine.write_json(SUMMARY_JSON_PATH, payload)
    write_packet_files(result, summary_rows, segment_rows, risk_rows, decision, ledger_payload)
    write_stage_docs(decision)
    update_current_truth(decision, summary_rows, external)
    append_changelog(decision)
    print(
        json.dumps(
            json_ready(
                {
                    "status": "ok" if external == "completed" else "blocked",
                    "run_id": RUN_ID,
                    "decision": decision,
                    "best_repaired_variant": best_repaired_variant(summary_rows),
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
    raise SystemExit(main(sys.argv[1:]))
