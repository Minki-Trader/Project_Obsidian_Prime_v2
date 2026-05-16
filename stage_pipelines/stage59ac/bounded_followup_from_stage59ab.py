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
SOURCE_STAGE59AB_ID = "59AB_adapter_repair__bounded_followup_from_stage59aa"
STAGE59AC_ID = "59AC_adapter_repair__bounded_followup_from_stage59ab"
NEXT_REPAIR_STAGE_ID = "59AD_adapter_repair__bounded_followup_from_stage59ac"
RUN_NUMBER = "run59X"
RUN_ID = "run59X_stage59ac_bounded_followup_from_stage59ab_v1"
PACKET_ID = "stage59ac_bounded_followup_from_stage59ab_v1"
PARENT_RUN_ID = "run59W_stage59ab_bounded_followup_from_stage59aa_v1"
SOURCE_ADAPTER_ID = "s59ab_v64_gap14_t59_h2_entrytrans_rearm002_sd5"
DEVELOPMENT_ANCHOR = "v64_v47_ctxgap14_refill_etfw_h2_no_b"
BACKUP_ANCHOR = "v60_v47_et_stable_damage_firewall_h2c0_no_b"
SOURCE_STAGE59AB_PUSHED_COMMIT = "9ba71b24f7ec71c6e41371a1bad28761f385cbfe"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)

STAGE_ROOT = Path("stages") / STAGE59AC_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
SPEC_ROOT = STAGE_ROOT / "00_spec"
INPUT_ROOT = STAGE_ROOT / "01_inputs"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID

SOURCE_STAGE_ROOT = Path("stages") / STAGE56_ID
SOURCE_STAGE59AB_ROOT = Path("stages") / SOURCE_STAGE59AB_ID
SOURCE_STAGE59AB_DECISION = SOURCE_STAGE59AB_ROOT / "03_reviews/stage59ab_decision.md"
SOURCE_STAGE59AB_REPORT = SOURCE_STAGE59AB_ROOT / "03_reviews/bounded_followup_from_stage59aa_report.md"
SOURCE_STAGE59AB_SUMMARY = SOURCE_STAGE59AB_ROOT / "03_reviews/bounded_followup_summary.csv"
SOURCE_STAGE59AB_JSON = SOURCE_STAGE59AB_ROOT / "03_reviews/bounded_followup_summary.json"

RUN50BR_ROOT = SOURCE_STAGE_ROOT / "02_runs/run50BR"
RUN50BR_V64_ANCHOR = "v64_v47_ctxgap14_refill_etfw_h2_no_b"
RUN50BR_SIGNAL = "stage56_context_gap_refill_signal"

COMMON_ROOT = f"Project_Obsidian_Prime_v2/s59ac/{RUN_NUMBER}"

REPORT_PATH = REVIEWS_ROOT / "bounded_followup_from_stage59ab_report.md"
SUMMARY_JSON_PATH = REVIEWS_ROOT / "bounded_followup_summary.json"
SUMMARY_CSV_PATH = REVIEWS_ROOT / "bounded_followup_summary.csv"
SEGMENT_KPI_PATH = REVIEWS_ROOT / "bounded_followup_segment_kpi_summary.csv"
EQUITY_AUDIT_PATH = REVIEWS_ROOT / "bounded_followup_equity_curve_audit.md"
RISK_ATR_TELEMETRY_PATH = REVIEWS_ROOT / "bounded_followup_risk_atr_telemetry.csv"
DECISION_PATH = REVIEWS_ROOT / "stage59ac_decision.md"
AUDIT_CSV_PATH = REVIEWS_ROOT / "stage59ac_trade_audit.csv"
PARTIALS_ROOT = RUN_ROOT / "partials"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")

MIN_MARGIN = 0.0

STAGE59AC_VARIANTS = (
    repair.RepairVariant(
        adapter_id="s59ac_v64_gap14_t59_h1_entrytrans_sd5",
        label="run50BR_v64_context_gap14_t59_hold1_entry_transition_risk3pct_wide_atr_sd5",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.5,
        atr_take_profit_multiplier=3.5,
        model_risk_max_pct=0.03,
        same_direction_reentry_cooldown_bars=5,
        entry_transition_only=True,
        entry_transition_rearm_min_confidence_delta=0.002,
        short_threshold=0.59,
        long_threshold=0.59,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=True,
        max_hold_bars=1,
        notes="Stage59AC bounded follow-up: reduce max hold to one bar on the Stage59AB best adapter to test whether late validation weakness is exit-timing driven.",
    ),
    repair.RepairVariant(
        adapter_id="s59ac_v64_gap14_t59_h3_entrytrans_sd5",
        label="run50BR_v64_context_gap14_t59_hold3_entry_transition_risk3pct_wide_atr_sd5",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.5,
        atr_take_profit_multiplier=3.5,
        model_risk_max_pct=0.03,
        same_direction_reentry_cooldown_bars=5,
        entry_transition_only=True,
        entry_transition_rearm_min_confidence_delta=0.002,
        short_threshold=0.59,
        long_threshold=0.59,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=True,
        max_hold_bars=3,
        notes="Stage59AC bounded follow-up: extend max hold to three bars on the Stage59AB best adapter to test whether current hold2 exits too early or too late by segment.",
    ),
    repair.RepairVariant(
        adapter_id="s59ac_v64_gap14_t59_h4_entrytrans_sd5",
        label="run50BR_v64_context_gap14_t59_hold4_entry_transition_risk3pct_wide_atr_sd5",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.5,
        atr_take_profit_multiplier=3.5,
        model_risk_max_pct=0.03,
        same_direction_reentry_cooldown_bars=5,
        entry_transition_only=True,
        entry_transition_rearm_min_confidence_delta=0.002,
        short_threshold=0.59,
        long_threshold=0.59,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=True,
        max_hold_bars=4,
        notes="Stage59AC bounded follow-up: extend max hold to four bars on the Stage59AB best adapter as a bounded lifecycle stress check, not a new model search.",
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
    return {
        "s59ac_v64_gap14_t59_h1_entrytrans_sd5": {
            "label": "run50br_v64_context_gap14_h2",
            "run_root": RUN50BR_ROOT,
            "variant_root": RUN50BR_ROOT / RUN50BR_V64_ANCHOR,
            "anchor": RUN50BR_V64_ANCHOR,
            "model": RUN50BR_ROOT / "models/stage56_context_timed_event_signal_discrete_score_table.csv",
            "signal_column": RUN50BR_SIGNAL,
            "validation_ini": RUN50BR_ROOT / RUN50BR_V64_ANCHOR / "mt5/x01_ta_val.ini",
            "oos_ini": RUN50BR_ROOT / RUN50BR_V64_ANCHOR / "mt5/x01_ta_oos.ini",
            "source_note": "Stage56 run50BR v64 context-gap14 refill ET firewall hold2 source",
        },
        "s59ac_v64_gap14_t59_h3_entrytrans_sd5": {
            "label": "run50br_v64_context_gap14_h2",
            "run_root": RUN50BR_ROOT,
            "variant_root": RUN50BR_ROOT / RUN50BR_V64_ANCHOR,
            "anchor": RUN50BR_V64_ANCHOR,
            "model": RUN50BR_ROOT / "models/stage56_context_timed_event_signal_discrete_score_table.csv",
            "signal_column": RUN50BR_SIGNAL,
            "validation_ini": RUN50BR_ROOT / RUN50BR_V64_ANCHOR / "mt5/x01_ta_val.ini",
            "oos_ini": RUN50BR_ROOT / RUN50BR_V64_ANCHOR / "mt5/x01_ta_oos.ini",
            "source_note": "Stage56 run50BR v64 context-gap14 refill ET firewall hold2 source",
        },
        "s59ac_v64_gap14_t59_h4_entrytrans_sd5": {
            "label": "run50br_v64_context_gap14_h2",
            "run_root": RUN50BR_ROOT,
            "variant_root": RUN50BR_ROOT / RUN50BR_V64_ANCHOR,
            "anchor": RUN50BR_V64_ANCHOR,
            "model": RUN50BR_ROOT / "models/stage56_context_timed_event_signal_discrete_score_table.csv",
            "signal_column": RUN50BR_SIGNAL,
            "validation_ini": RUN50BR_ROOT / RUN50BR_V64_ANCHOR / "mt5/x01_ta_val.ini",
            "oos_ini": RUN50BR_ROOT / RUN50BR_V64_ANCHOR / "mt5/x01_ta_oos.ini",
            "source_note": "Stage56 run50BR v64 context-gap14 refill ET firewall hold2 source",
        },
    }


def configure_reused_engine() -> None:
    engine.STAGE59_ID = STAGE59AC_ID
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
    engine.STAGE59_VARIANTS = STAGE59AC_VARIANTS
    engine.SOURCE_SPECS = source_specs()
    engine.MODEL_RISK_MIN_PCT = {variant.adapter_id: 0.005 for variant in STAGE59AC_VARIANTS}

    repair.STAGE_ID = STAGE59AC_ID
    repair.RUN_NUMBER = RUN_NUMBER
    repair.RUN_ID = RUN_ID
    repair.RUN_ROOT = RUN_ROOT
    repair.REPAIR_VARIANTS = STAGE59AC_VARIANTS
    s58.STAGE58_ID = STAGE59AC_ID
    s58.RUN_NUMBER = RUN_NUMBER
    s58.RUN_ID = RUN_ID
    s58.PACKET_ID = PACKET_ID
    s58.PARENT_RUN_ID = PARENT_RUN_ID
    s58.RUN_ROOT = RUN_ROOT
    s58.REVIEWS_ROOT = REVIEWS_ROOT
    s58.STAGE58_VARIANTS = STAGE59AC_VARIANTS
    s58.COMMON_ROOT = COMMON_ROOT


def extra_set_values(variant: repair.RepairVariant, magic: int) -> dict[str, Any]:
    values = repair.extra_set_values(variant, magic)
    values["InpModelRiskMinPct"] = 0.005
    values["InpModelRiskMaxPct"] = min(float(variant.model_risk_max_pct), 0.05)
    values["InpModelRiskFallbackLot"] = variant.fixed_lot
    return values


def build_attempts(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    for variant_index, variant in enumerate(STAGE59AC_VARIANTS, start=1):
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
                magic = 5906000 + variant_index * 100 + (1 if split == "validation_is" else 50) + role_index
                attempts.append(
                    attempt_payload(
                        run_root=variant_root,
                        run_id=RUN_ID,
                        stage_number=59,
                        exploration_label="stage59AC_BaselineAdapter__HoldLifecycle",
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
        "judgment": "inconclusive_stage59ac_runtime_probe_completed" if completed and report_completed else "blocked_stage59ac_runtime_probe",
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
        return "59AD_adapter_repair__backup_or_demote_from_stage59ac"
    if decision == "open_new_model_branch":
        return "59AD_adapter_repair__new_model_branch_from_stage59ac"
    return NEXT_REPAIR_STAGE_ID


def next_packet_for_decision(decision: str) -> tuple[str, str]:
    next_stage = next_stage_for_decision(decision)
    if next_stage.startswith("60_"):
        return "stage60_onnx_hardening_v1", "run60A_stage60_onnx_hardening_v1"
    return "stage59ad_bounded_followup_from_stage59ac_v1", "run59Y_stage59ad_bounded_followup_from_stage59ac_v1"


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
                    "stage_id": STAGE59AC_ID,
                    "run_id": RUN_ID,
                    "artifact_type": "stage59ac_bounded_followup_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "created_at_utc": created,
                    "notes": "Stage59AC bounded hold-lifecycle follow-up from Stage59AB artifact.",
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
                    "stage_id": STAGE59AC_ID,
                    "run_id": RUN_ID,
                    "artifact_type": "mt5_strategy_tester_report",
                    "path": rel(report_path),
                    "sha256": sha256_file_lf_normalized(report_path),
                    "created_at_utc": created,
                    "notes": "Actual Stage59AC MT5 Strategy Tester HTML report.",
                }
            )
    return rows


def write_run_identity(result: Mapping[str, Any]) -> None:
    engine.write_json(
        RUN_ROOT / "run_manifest.json",
        {
            "run_id": RUN_ID,
            "packet_id": PACKET_ID,
            "stage_id": STAGE59AC_ID,
            "stage_number": 59,
            "run_number": RUN_NUMBER,
            "bounded_question": "Can bounded max-hold changes on the Stage59AB best adapter repair validation late flatline and cost weakness without damaging OOS behavior?",
            "source_stage59ab_decision": rel(SOURCE_STAGE59AB_DECISION),
            "source_stage59ab_pushed_commit": SOURCE_STAGE59AB_PUSHED_COMMIT,
            "variants": [
                {
                    **variant.__dict__,
                    "source_anchor": engine.source_anchor_for_variant(variant),
                    "signal_column": engine.signal_column_for_variant(variant),
                    "feature_order_hash": engine.feature_order_hash_for_variant(variant),
                }
                for variant in STAGE59AC_VARIANTS
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
            "stage_id": STAGE59AC_ID,
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
                "stage_id": STAGE59AC_ID,
                "lane": "baseline_adapter_bounded_followup_from_stage59ab",
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
        stage_id=STAGE59AC_ID,
        mt5_kpi_records=result.get("mt5_kpi_records", []),
        run_output_root=RUN_ROOT,
        external_verification_status=external,
    )
    ledger_rows.append(
        {
            "ledger_row_id": f"{RUN_ID}__aggregate_bounded_followup_from_stage59ab",
            "stage_id": STAGE59AC_ID,
            "run_id": RUN_ID,
            "subrun_id": "aggregate_bounded_followup_from_stage59ab",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "bounded_followup_from_stage59ab",
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
            "notes": "Stage59AC bounded hold-lifecycle follow-up from Stage59AB evidence; not final package completion.",
        }
    )
    stage_payload = upsert_csv_rows_retry(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id")
    project_payload = upsert_csv_rows_retry(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id")
    artifact_payload = upsert_csv_rows_retry(ARTIFACT_REGISTRY_PATH, aw.ARTIFACT_COLUMNS, list(artifacts), key="artifact_id")
    return {"run_registry": run_payload, "stage_ledger": stage_payload, "project_alpha_ledger": project_payload, "artifact_registry": artifact_payload}








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
            "stage_id": STAGE59AC_ID,
            "run_id": RUN_ID,
            "packet_id": PACKET_ID,
            "source_stage59ab_decision": rel(SOURCE_STAGE59AB_DECISION),
            "source_stage59ab_pushed_commit": SOURCE_STAGE59AB_PUSHED_COMMIT,
            "source_adapter": SOURCE_ADAPTER_ID,
            "variants": [
                {
                    **variant.__dict__,
                    "source_anchor": engine.source_anchor_for_variant(variant),
                    "signal_column": engine.signal_column_for_variant(variant),
                    "feature_order_hash": engine.feature_order_hash_for_variant(variant),
                }
                for variant in STAGE59AC_VARIANTS
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
                "stage59ac_decision": rel(DECISION_PATH),
            },
            "ledger_payload": ledger_payload,
            "claim_boundary": BOUNDARY,
            "overall_goal_complete": False,
        },
    )
























def report_markdown(summary_rows: Sequence[Mapping[str, Any]], decision: str, reasons: Sequence[str], external: str) -> str:
    rows = [row for row in summary_rows if row.get("view") == "actual_routed_total"]
    table = "\n".join(
        "| {adapter} | {split} | {pf} | {net} | {dd} | {cost} | {trades} | {same_move} | {risk} |".format(
            adapter=row.get("adapter_id"),
            split=row.get("split"),
            pf=aw.fmt(row.get("profit_factor")),
            net=aw.fmt(row.get("net_profit")),
            dd=aw.fmt(row.get("max_drawdown_amount")),
            cost=aw.fmt(row.get("cost_stressed_expectancy")),
            trades=aw.fmt(row.get("trades_per_day")),
            same_move=aw.fmt(row.get("same_move_reentry_ratio")),
            risk=aw.fmt(row.get("avg_model_risk_pct")),
        )
        for row in rows
    )
    best = best_repaired_variant(summary_rows)
    return f"""# Stage59AC Bounded Follow-Up From Stage59AB Report(59AC단계 Stage59AB 기반 경계 후속 보고서)

- stage(단계): `{STAGE59AC_ID}`
- run(실행): `{RUN_ID}`
- source_decision(원천 판정): `continue_repair_in_new_bounded_stage`
- external_verification_status(외부 검증 상태): `{external}`
- decision(판정): `{decision}`
- boundary(경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Can bounded max_hold_bars(최대 보유 봉 수) changes on the Stage59AB best adapter(Stage59AB 최선 어댑터) repair validation late flatline(검증 후반 횡보) and cost-stressed expectancy(비용 압박 기대값) weakness without damaging OOS(표본외)?

## Result Table(결과 표)

| adapter(어댑터) | split(구간) | PF(수익 팩터) | net(순손익) | DD(최대 손실) | cost exp(비용 압박 기대값) | trades/day(일 거래 수) | same move(동일 이동) | avg risk(평균 위험률) |
|---|---|---:|---:|---:|---:|---:|---:|---:|
{table}

## Read(판독)

- best_repaired_adapter(최선 수리 어댑터): `{best.get('adapter_id', 'none')}`
- failure_reasons(실패/약점 이유): `{";".join(reasons) if reasons else "none"}`
- bounded_followup_summary(경계 후속 요약): `{rel(SUMMARY_CSV_PATH)}`
- bounded_followup_segment_kpi_summary(경계 후속 구간 KPI 요약): `{rel(SEGMENT_KPI_PATH)}`
- bounded_followup_risk_atr_telemetry(경계 후속 위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`

Effect(효과): Stage59AC(59AC단계)는 Stage59AB(59AB단계)의 best adapter(최선 어댑터)를 ONNX hardening(ONNX 경화)으로 넘기기 전에, max_hold_bars(최대 보유 봉 수) 차이만 작게 시험해 품질 약점이 실제로 고쳐지는지 확인한다.

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
    return f"""# Stage59AC Bounded Follow-Up Equity Curve Audit(59AC단계 경계 후속 자금 곡선 감사)

- best_repaired_adapter(최선 수리 어댑터): `{best_id}`
- audit_boundary(감사 경계): `segment/equity measurement only(구간/자금 측정 전용)`
- quality_flags(품질 표식): `{";".join(flags) if flags else "none"}`

## Chronological Thirds(시간 순서 3분할)

{lines if lines else "- segment_rows(구간 행): `missing_or_not_completed`"}

Effect(효과): max_hold_bars(최대 보유 봉 수) 차이가 final net(최종 순손익)만 올렸는지, 아니면 validation/OOS(검증/표본외) 구간 품질과 drawdown recovery(손실 회복)를 같이 개선했는지 판정 근거로 남긴다.
"""


def decision_markdown(decision: str, reasons: Sequence[str], best: Mapping[str, Any], external: str) -> str:
    return f"""# Stage59AC Decision(59AC단계 판정)

decision(판정): `{decision}`

Stage59AC(59AC단계)는 Stage59AB best adapter evidence(Stage59AB 최선 어댑터 근거)를 사용한 bounded hold-lifecycle follow-up(경계 보유 생명주기 후속)이다. Effect(효과): Stage60 ONNX(60단계 ONNX)로 넘어가기 전 validation late flatline(검증 후반 횡보)과 cost-stressed expectancy(비용 압박 기대값) 약점을 먼저 확인한다.

## Evidence(근거)

- report(보고서): `{rel(REPORT_PATH)}`
- repaired_adapter_summary(수리 어댑터 요약): `{rel(SUMMARY_CSV_PATH)}`
- repaired_segment_kpi_summary(수리 구간 KPI 요약): `{rel(SEGMENT_KPI_PATH)}`
- repaired_equity_curve_audit(수리 자금 곡선 감사): `{rel(EQUITY_AUDIT_PATH)}`
- repaired_risk_atr_telemetry(수리 위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- external_verification_status(외부 검증 상태): `{external}`

## Reason(이유)

- best_repaired_adapter(최선 수리 어댑터): `{best.get('adapter_id', 'none')}`
- failure_reasons(실패/약점 이유): `{";".join(reasons) if reasons else "none"}`

## Next(다음)

next_stage_or_branch(다음 단계/분기): `{next_stage_for_decision(decision)}`

Stage59AC closeout(59AC단계 종료)는 overall goal completion(전체 목표 완료)이 아니다. Effect(효과): strong full adapter evidence(강한 전체 어댑터 근거)가 없으면 다음 bounded stage(경계 다음 단계)로 넘긴다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
"""


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
            "hypothesis": "Bounded max_hold_bars changes on the Stage59AB best adapter may reduce validation late flatline and cost-stressed expectancy weakness while preserving OOS net, PF, ATR/bracket telemetry, and model-risk telemetry.",
            "decision_use": "Route to Stage60 only if the full post-ATR/risk adapter evidence is strong; otherwise continue bounded repair, demote, or open another branch.",
            "comparison_baseline": "Stage59AB best adapter s59ab_v64_gap14_t59_h2_entrytrans_rearm002_sd5 with validation PF 1.07, validation cost-stressed expectancy below zero, and validation late flatline risk.",
            "control_variables": ["US100", "M5", "split_v1", "run50BR v64 source", "Tier B disabled", "entry_transition_only", "entry_transition_rearm_min_confidence_delta=0.002", "short_threshold=0.59", "long_threshold=0.59", "close_only_on_opposite", "wide ATR bracket", "3% model-controlled risk cap", "ONNX deferred"],
            "changed_variables": ["max_hold_bars"],
            "sample_scope": "FPMarkets US100 M5 validation 2025-01-01 to 2025-09-30 and OOS 2025-10-01 to 2026-04-13.",
            "success_criteria": ["validation and OOS net positive", "validation and OOS PF >= 1.10", "validation and OOS cost-stressed expectancy positive", "ATR and model risk telemetry present", "no severe segment flags"],
            "failure_criteria": ["negative validation/OOS net", "PF < 1.10", "cost-stressed expectancy <= 0", "missing risk or ATR telemetry", "segment flags remain", "OOS density collapses"],
            "invalid_conditions": ["missing model table", "missing feature files", "missing MT5 report", "telemetry parse failure"],
            "stop_conditions": "three bounded Stage59AC max-hold lifecycle variants only",
            "evidence_plan": [rel(SUMMARY_CSV_PATH), rel(SEGMENT_KPI_PATH), rel(EQUITY_AUDIT_PATH), rel(RISK_ATR_TELEMETRY_PATH), rel(DECISION_PATH)],
            "status": "completed",
        },
        "runtime_evidence_gate.json": {"external_verification_status": external, "mt5_reports": result.get("strategy_tester_reports", []), "status": external},
        "kpi_contract_audit.json": {"summary_rows": len(summary_rows), "segment_rows": len(segment_rows), "risk_rows": len(risk_rows), "status": "completed"},
        "result_judgment_gate.json": {
            "result_subject": RUN_ID,
            "evidence_available": [rel(REPORT_PATH), rel(SUMMARY_CSV_PATH), rel(SEGMENT_KPI_PATH), rel(RISK_ATR_TELEMETRY_PATH)],
            "evidence_missing": [] if external == "completed" else ["completed_mt5_external_verification"],
            "external_verification_status": external,
            "judgment_label": "runtime_probe" if external == "completed" else "blocked",
            "stage_decision": decision,
            "failure_reasons": reasons,
            "best_repaired_adapter": best.get("adapter_id", "none"),
            "claim_boundary": BOUNDARY,
            "next_condition": next_stage_for_decision(decision),
            "status": "passed_with_boundary",
        },
        "artifact_lineage_audit.json": {
            "source_inputs": [
                rel(SOURCE_STAGE59AB_DECISION),
                rel(SOURCE_STAGE59AB_REPORT),
                rel(SOURCE_STAGE59AB_SUMMARY),
                rel(SOURCE_STAGE59AB_JSON),
                rel(RUN50BR_ROOT / "models/stage56_context_timed_event_signal_discrete_score_table.csv"),
                rel(RUN50BR_ROOT / RUN50BR_V64_ANCHOR),
            ],
            "producer": rel(Path("stage_pipelines/stage59ac/bounded_followup_from_stage59ab.py")),
            "consumers": [rel(REPORT_PATH), rel(DECISION_PATH), rel(SUMMARY_JSON_PATH)],
            "ledger_links": ledger_payload,
            "lineage_judgment": "connected_with_boundary",
            "status": "completed",
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
            "stage_id": STAGE59AC_ID,
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
                "stage59ac_decision": rel(DECISION_PATH),
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
        f"""# Stage59AC Brief(59AC단계 개요)

- stage_id(단계 ID): `{STAGE59AC_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE59AB_ID}`
- source_decision(원천 판정): `continue_repair_in_new_bounded_stage`
- bounded_question(경계 질문): `Can bounded max-hold changes on the Stage59AB best adapter repair validation late flatline and cost weakness without damaging OOS behavior?`
- boundary(경계): `{BOUNDARY}`

Stage59AC(59AC단계)는 Stage59AB(59AB단계)의 best adapter(최선 어댑터) `{SOURCE_ADAPTER_ID}`에서 max_hold_bars(최대 보유 봉 수) 세 변형만 측정한다. Effect(효과): Stage60 ONNX(60단계 ONNX)로 조기 이동하지 않고 검증 품질 약점을 먼저 좁게 확인한다.
""",
    )
    engine.write_md(
        INPUT_ROOT / "input_refs.md",
        f"""# Stage59AC Input References(59AC단계 입력 참조)

- stage59ab_decision(59AB단계 판정): `{rel(SOURCE_STAGE59AB_DECISION)}`
- stage59ab_report(59AB단계 보고서): `{rel(SOURCE_STAGE59AB_REPORT)}`
- stage59ab_summary(59AB단계 요약): `{rel(SOURCE_STAGE59AB_SUMMARY)}`
- stage59ab_pushed_commit(59AB단계 푸시 커밋): `{SOURCE_STAGE59AB_PUSHED_COMMIT}`
- run50br_v64_source(run50BR v64 원천): `{rel(RUN50BR_ROOT / RUN50BR_V64_ANCHOR)}`
- run50br_source_model(run50BR 원천 모델): `{rel(RUN50BR_ROOT / "models/stage56_context_timed_event_signal_discrete_score_table.csv")}`

Effect(효과): Stage59AC(59AC단계)는 Stage59AB(59AB단계) 약점과 run50BR v64(run50BR 변형64) 원천을 명시적으로 연결한다.
""",
    )
    engine.write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage59AC Selection Status(59AC단계 선택 상태)

- stage_status(단계 상태): `closed_bounded_followup_from_stage59ab`
- source_stage(원천 단계): `{SOURCE_STAGE59AB_ID}`
- source_decision(원천 판정): `continue_repair_in_new_bounded_stage`
- stage59ac_decision(59AC단계 판정): `{decision}`
- next_stage_or_branch(다음 단계/분기): `{next_stage}`
- selected_research_baseline(선택 연구 기준선): `none`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage59AC(59AC단계)는 측정 결과를 보존하지만 final package(최종 패키지)나 operating claim(운영 주장)을 만들지 않는다.
""",
    )
    engine.write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage59AC Review Index(59AC단계 검토 색인)

- bounded_followup_report(경계 후속 보고서): `{rel(REPORT_PATH)}`
- bounded_followup_summary(경계 후속 요약): `{rel(SUMMARY_CSV_PATH)}`
- bounded_followup_segment_kpi(경계 후속 구간 KPI): `{rel(SEGMENT_KPI_PATH)}`
- bounded_followup_equity_curve_audit(경계 후속 자금 곡선 감사): `{rel(EQUITY_AUDIT_PATH)}`
- bounded_followup_risk_atr_telemetry(경계 후속 위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- stage59ac_decision(59AC단계 판정): `{rel(DECISION_PATH)}`
""",
    )
    if not next_stage.startswith("60_"):
        next_root = Path("stages") / next_stage
        next_stage_label = next_stage.split("_", 1)[0]
        engine.write_md(
            next_root / "00_spec/stage_brief.md",
            f"""# {next_stage_label} Brief({next_stage_label}단계 개요)

- stage_id(단계 ID): `{next_stage}`
- source_stage(원천 단계): `{STAGE59AC_ID}`
- source_decision(원천 판정): `{decision}`
- bounded_question(경계 질문): `What bounded follow-up should repair, demote, or branch from the Stage59AC hold-lifecycle evidence without starting ONNX prematurely?`
- boundary(경계): `{BOUNDARY}`

{next_stage_label}({next_stage_label}단계)는 Stage59AC(59AC단계) 결과가 Stage60 ONNX(60단계 ONNX)에 충분하지 않을 때 이어지는 bounded follow-up(경계 후속)이다. Effect(효과): repair(수리), demotion(강등), branch(분기)를 다음 작은 질문으로 제한한다.
""",
        )
        engine.write_md(
            next_root / "01_inputs/input_refs.md",
            f"""# {next_stage_label} Input References({next_stage_label}단계 입력 참조)

- stage59ac_decision(59AC단계 판정): `{rel(DECISION_PATH)}`
- stage59ac_report(59AC단계 보고서): `{rel(REPORT_PATH)}`
- stage59ac_summary(59AC단계 요약): `{rel(SUMMARY_CSV_PATH)}`
- stage59ac_segment_kpi(59AC단계 구간 KPI): `{rel(SEGMENT_KPI_PATH)}`
- stage59ac_risk_atr_telemetry(59AC단계 위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`
""",
        )
        engine.write_md(
            next_root / "03_reviews/review_index.md",
            f"""# {next_stage_label} Review Index({next_stage_label}단계 검토 색인)

{next_stage_label}({next_stage_label}단계)는 planned(계획) 상태다. Effect(효과): Stage59AC(59AC단계) 약점을 다음 bounded repair(경계 수리) 근거로 넘긴다.
""",
        )
        engine.write_md(
            next_root / "04_selected/selection_status.md",
            f"""# {next_stage_label} Selection Status({next_stage_label}단계 선택 상태)

- stage_status(단계 상태): `active_planned_from_stage59ac`
- source_stage(원천 단계): `{STAGE59AC_ID}`
- source_decision(원천 판정): `{decision}`
- selected_research_baseline(선택 연구 기준선): `none`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): {next_stage_label}({next_stage_label}단계)는 Stage59AC(59AC단계) 이후 필요한 다음 작은 질문만 다룬다.
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
- status(상태): `stage59ac_closed_{decision}`
- claim_boundary(주장 경계): research/development only(연구/개발 전용)

Stage59AC(59AC단계) closed(종료) as bounded hold-lifecycle follow-up from Stage59AB(Stage59AB 기반 경계 보유 생명주기 후속). Effect(효과): Stage59AB(59AB단계)의 validation PF/cost weakness(검증 수익 팩터/비용 약점)를 보존하고, Stage60 ONNX(60단계 ONNX)는 품질 근거가 강할 때만 열린다.

## Latest Stage59AC Evidence(최신 59AC단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- best_repaired_adapter(최선 수리 어댑터): `{best.get('adapter_id', 'none')}`
- external_verification_status(외부 검증 상태): `{external}`
- next_stage_or_branch(다음 단계/분기): `{next_stage}`
- report(보고서): `{rel(REPORT_PATH)}`
- stage59ac_decision(59AC단계 판정): `{rel(DECISION_PATH)}`

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
        f"  Stage59AC(59AC단계) `{STAGE59AC_ID}` closed(종료) as bounded hold-lifecycle follow-up from Stage59AB(Stage59AB 기반 경계 보유 생명주기 후속); decision(판정)=`{decision}`. "
        f"Effect(효과): full BaselineAdapter repair(전체 기준선 어댑터 수리)는 계속 research/development boundary(연구/개발 경계) 안에 있으며 final(최종) 또는 operating(운영) 주장은 없다.\n"
        f"- >-\n"
        f"  Next stage_or_branch(다음 단계/분기) `{next_stage}` is active/planned(활성/계획). Effect(효과): Stage59AC(59AC단계) 결과를 다음 bounded step(경계 다음 단계)으로 넘긴다.\n"
    )
    text = re.sub(r"current_focus:\n(?:- >-\n(?:  .*\n)+)+", focus, text, count=1)
    block = f"""

stage59ac_bounded_followup_from_stage59ab:
  packet_id: {PACKET_ID}
  stage_id: {STAGE59AC_ID}
  status: closed_bounded_followup_from_stage59ab
  current_run_id: {RUN_ID}
  source_adapter: {SOURCE_ADAPTER_ID}
  source_stage59ab_pushed_commit: {SOURCE_STAGE59AB_PUSHED_COMMIT}
  best_repaired_adapter: {best.get('adapter_id', 'none')}
  decision: {decision}
  next_stage_or_branch: {next_stage}
  report_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  external_verification_status: {external}
  boundary: {BOUNDARY}
"""
    if "stage59ac_bounded_followup_from_stage59ab:" in text:
        text = re.sub(r"\nstage59ac_bounded_followup_from_stage59ab:\n(?:  .*\n)*", block, text, count=1)
    else:
        text += block
    io_path(WORKSPACE_STATE_PATH).write_text(text, encoding="utf-8-sig")


def append_changelog(decision: str) -> None:
    entry = (
        "\n## 2026-05-16 - Stage59AC bounded hold-lifecycle follow-up closeout(59AC단계 경계 보유 생명주기 후속 종료)\n\n"
        f"- run(실행): `{RUN_ID}`\n"
        f"- decision(판정): `{decision}`\n"
        "- effect(효과): Stage59AB(59AB단계) best adapter(최선 어댑터)의 validation late/cost weakness(검증 후반/비용 약점)를 max-hold lifecycle variants(최대 보유 생명주기 변형) 세 개로 측정하고 다음 bounded stage(경계 다음 단계) 조건을 남겼다.\n"
    )
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if f"- run(실행): `{RUN_ID}`" not in existing:
        io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage59AC bounded follow-up from Stage59AB.")
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
        raise FileNotFoundError("Stage59AC existing run_manifest.json or kpi_record.json is missing")
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
            "stage_id": STAGE59AC_ID,
            "stage_number": 59,
            "run_number": RUN_NUMBER,
            "run_root": RUN_ROOT,
            "packet_id": PACKET_ID,
            "attempts": attempts,
            "common_copies": inputs["common_copies"],
            "feature_exports": inputs["feature_exports"],
            "model_artifacts": inputs["model_exports"],
            "route_coverage": engine.route_coverage(),
            "model_family": "baseline_adapter_stage59ac_hold_lifecycle_ebm_table",
            "feature_set_id": "stage59ac_hold_lifecycle_signal",
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
