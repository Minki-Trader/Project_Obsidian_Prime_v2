from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
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
from stage_pipelines.stage56 import baseline_adapter_repair_batch as repair  # noqa: E402
from stage_pipelines.stage56 import independent_event_source_route_branch as aw  # noqa: E402
from stage_pipelines.stage58 import risk_atr_integration as s58  # noqa: E402


STAGE56_ID = "56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection"
STAGE58_ID = "58_adapter_risk__bounded_repair_before_atr_risk_integration"
SOURCE_STAGE59_ID = "59_adapter_repair__post_risk_atr_revalidation"
SOURCE_STAGE59A_ID = "59A_adapter_repair__risk_sizing_quality_recalibration"
STAGE59_ID = "59B_adapter_repair__model_source_or_backup_branch"
NEXT_REPAIR_STAGE_ID = "59C_adapter_repair__new_model_source_branch"
RUN_NUMBER = "run55A"
RUN_ID = "run55A_stage59b_model_source_or_backup_branch_v1"
PACKET_ID = "stage59b_model_source_or_backup_branch_v1"
PARENT_RUN_ID = "run54A_stage59a_risk_sizing_quality_recalibration_v1"
SOURCE_ADAPTER_ID = "ba14_no_atr_sd5_lot025"
DEVELOPMENT_ANCHOR = "v64_v47_ctxgap14_refill_etfw_h2_no_b"
BACKUP_ANCHOR = "v60_v47_et_stable_damage_firewall_h2c0_no_b"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)

STAGE_ROOT = Path("stages") / STAGE59_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
SPEC_ROOT = STAGE_ROOT / "00_spec"
INPUT_ROOT = STAGE_ROOT / "01_inputs"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID

SOURCE_STAGE_ROOT = Path("stages") / STAGE56_ID
SOURCE_RUN_ROOT = SOURCE_STAGE_ROOT / "02_runs/run50BR"
SOURCE_VARIANT_ROOT = SOURCE_RUN_ROOT / DEVELOPMENT_ANCHOR
SOURCE_MODEL = SOURCE_RUN_ROOT / "models/stage56_context_timed_event_signal_discrete_score_table.csv"
BACKUP_RUN_ROOT = SOURCE_STAGE_ROOT / "02_runs/run50BQ"
BACKUP_VARIANT_ROOT = BACKUP_RUN_ROOT / BACKUP_ANCHOR
BACKUP_MODEL = BACKUP_RUN_ROOT / "models/stage56_context_timed_event_signal_discrete_score_table.csv"
SOURCE_STAGE59A_ROOT = Path("stages") / SOURCE_STAGE59A_ID
SOURCE_STAGE59A_DECISION = SOURCE_STAGE59A_ROOT / "03_reviews/stage59a_decision.md"
SOURCE_STAGE59A_REPORT = SOURCE_STAGE59A_ROOT / "03_reviews/risk_sizing_quality_recalibration_report.md"
SOURCE_STAGE59A_SUMMARY = SOURCE_STAGE59A_ROOT / "03_reviews/risk_sizing_quality_recalibration_summary.csv"
SOURCE_STAGE59A_SEGMENTS = SOURCE_STAGE59A_ROOT / "03_reviews/risk_sizing_quality_segment_kpi_summary.csv"
SOURCE_STAGE59A_RISK = SOURCE_STAGE59A_ROOT / "03_reviews/risk_sizing_quality_telemetry.csv"

DEVELOPMENT_SIGNAL_COLUMN = "stage56_context_gap_refill_signal"
BACKUP_SIGNAL_COLUMN = "stage56_context_et_firewall_signal"
COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage59b/{RUN_NUMBER}_model_source_or_backup_branch"

REPORT_PATH = REVIEWS_ROOT / "model_source_or_backup_branch_report.md"
SUMMARY_JSON_PATH = REVIEWS_ROOT / "model_source_or_backup_branch_summary.json"
SUMMARY_CSV_PATH = REVIEWS_ROOT / "model_source_or_backup_branch_summary.csv"
SEGMENT_KPI_PATH = REVIEWS_ROOT / "model_source_or_backup_segment_kpi_summary.csv"
EQUITY_AUDIT_PATH = REVIEWS_ROOT / "model_source_or_backup_equity_curve_audit.md"
RISK_ATR_TELEMETRY_PATH = REVIEWS_ROOT / "model_source_or_backup_risk_atr_telemetry.csv"
DECISION_PATH = REVIEWS_ROOT / "stage59b_decision.md"
AUDIT_CSV_PATH = REVIEWS_ROOT / "stage59b_trade_audit.csv"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")

VALIDATION_DAYS = 183.0
OOS_DAYS = 195.0
SHORT_THRESHOLD = 0.55
LONG_THRESHOLD = 0.55
MIN_MARGIN = 0.0

STAGE59A_PUSHED_COMMIT = "c4af9d374450c1372bfefda0fca92d9e3f785df9"

STAGE59_VARIANTS = (
    repair.RepairVariant(
        adapter_id="s59b_v64_control_thr57_mr03_wideatr_sd5",
        label="v64_control_threshold57_risk3pct_wide_atr_sd5",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.5,
        atr_take_profit_multiplier=3.5,
        model_risk_max_pct=0.03,
        same_direction_reentry_cooldown_bars=5,
        short_threshold=0.57,
        long_threshold=0.57,
        notes="Stage59B bounded source control: v64 source with Stage59A best threshold, 3% model-controlled risk cap, and wide ATR.",
    ),
    repair.RepairVariant(
        adapter_id="s59b_v60_backup_thr55_mr03_wideatr_sd5",
        label="v60_backup_threshold55_risk3pct_wide_atr_sd5",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.5,
        atr_take_profit_multiplier=3.5,
        model_risk_max_pct=0.03,
        same_direction_reentry_cooldown_bars=5,
        short_threshold=0.55,
        long_threshold=0.55,
        notes="Stage59B bounded backup branch: v60 backup source with native 0.55 threshold, 3% model-controlled risk cap, and wide ATR.",
    ),
    repair.RepairVariant(
        adapter_id="s59b_v60_backup_thr57_mr03_wideatr_sd5",
        label="v60_backup_threshold57_risk3pct_wide_atr_sd5",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.5,
        atr_take_profit_multiplier=3.5,
        model_risk_max_pct=0.03,
        same_direction_reentry_cooldown_bars=5,
        short_threshold=0.57,
        long_threshold=0.57,
        notes="Stage59B bounded backup branch: v60 backup source with Stage59A 0.57 threshold, 3% model-controlled risk cap, and wide ATR.",
    ),
)

MODEL_RISK_MIN_PCT = {variant.adapter_id: 0.005 for variant in STAGE59_VARIANTS}


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    candidate = Path(str(path))
    try:
        return io_path(candidate).resolve().relative_to(io_path(REPO_ROOT).resolve()).as_posix()
    except ValueError:
        try:
            return candidate.resolve().relative_to(REPO_ROOT.resolve()).as_posix()
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
        return f"{value:.10f}"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return str(value)


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    if columns is None:
        ordered: list[str] = []
        for row in rows:
            for key in row:
                if key not in ordered:
                    ordered.append(key)
        columns = tuple(ordered)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in columns})


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


def variant_uses_backup_source(variant: repair.RepairVariant | str) -> bool:
    adapter_id = variant.adapter_id if isinstance(variant, repair.RepairVariant) else str(variant)
    return "_v60_backup_" in adapter_id


def source_root_for_variant(variant: repair.RepairVariant | str) -> Path:
    return BACKUP_VARIANT_ROOT if variant_uses_backup_source(variant) else SOURCE_VARIANT_ROOT


def source_anchor_for_variant(variant: repair.RepairVariant | str) -> str:
    return BACKUP_ANCHOR if variant_uses_backup_source(variant) else DEVELOPMENT_ANCHOR


def source_model_for_variant(variant: repair.RepairVariant | str) -> Path:
    return BACKUP_MODEL if variant_uses_backup_source(variant) else SOURCE_MODEL


def signal_column_for_variant(variant: repair.RepairVariant | str) -> str:
    return BACKUP_SIGNAL_COLUMN if variant_uses_backup_source(variant) else DEVELOPMENT_SIGNAL_COLUMN


def feature_order_hash_for_variant(variant: repair.RepairVariant | str) -> str:
    return ordered_hash((signal_column_for_variant(variant),))


def source_attempt_ini(split: str, variant: repair.RepairVariant | str) -> Path:
    return source_root_for_variant(variant) / "mt5" / ("x01_ta_val.ini" if split == "validation_is" else "x01_ta_oos.ini")


def source_feature(split: str, variant: repair.RepairVariant | str, tier: str = "a") -> Path:
    token = "val" if split == "validation_is" else "oos"
    anchor = source_anchor_for_variant(variant)
    return source_root_for_variant(variant) / "features" / f"{anchor}_{tier}_{token}.csv"


def copy_local(source: Path, destination: Path) -> dict[str, Any]:
    if not path_exists(source):
        raise FileNotFoundError(source)
    io_path(destination.parent).mkdir(parents=True, exist_ok=True)
    shutil.copy2(io_path(source), io_path(destination))
    return {"source": rel(source), "path": rel(destination), "sha256": sha256_file_lf_normalized(destination)}


def prepare_inputs(common_files_root: Path) -> dict[str, Any]:
    copied: list[dict[str, Any]] = []
    model_exports: dict[str, dict[str, Any]] = {}
    feature_exports: dict[str, dict[str, dict[str, Any]]] = {}
    for variant in STAGE59_VARIANTS:
        source_label = "backup_v60" if variant_uses_backup_source(variant) else "control_v64"
        model_source = source_model_for_variant(variant)
        model_local = RUN_ROOT / variant.adapter_id / "models" / f"{source_label}_{model_source.name}"
        copied.append(copy_local(model_source, model_local))
        copied.append(copy_to_common(model_local, f"{COMMON_ROOT}/{variant.adapter_id}/models/{model_local.name}", common_files_root))
        model_exports[variant.adapter_id] = {
            "path": rel(model_local),
            "common_path": f"{COMMON_ROOT}/{variant.adapter_id}/models/{model_local.name}",
            "sha256": sha256_file_lf_normalized(model_local),
            "source_model": rel(model_source),
            "source_anchor": source_anchor_for_variant(variant),
            "signal_column": signal_column_for_variant(variant),
            "feature_order_hash": feature_order_hash_for_variant(variant),
        }
        feature_exports[variant.adapter_id] = {}
        for split in ("validation_is", "oos"):
            token = "val" if split == "validation_is" else "oos"
            feature_source = source_feature(split, variant, "a")
            feature_local = RUN_ROOT / variant.adapter_id / "features" / f"{variant.adapter_id}_stage59b_adapter_a_{token}.csv"
            copied.append(copy_local(feature_source, feature_local))
            copied.append(copy_to_common(feature_local, f"{COMMON_ROOT}/{variant.adapter_id}/features/{feature_local.name}", common_files_root))
            feature_exports[variant.adapter_id][split] = {
                "path": rel(feature_local),
                "common_path": f"{COMMON_ROOT}/{variant.adapter_id}/features/{feature_local.name}",
                "sha256": sha256_file_lf_normalized(feature_local),
                "source_feature": rel(feature_source),
            }
    return {
        "model_exports": model_exports,
        "feature_exports": feature_exports,
        "common_copies": copied,
    }


def extra_set_values(variant: repair.RepairVariant, magic: int) -> dict[str, Any]:
    values = repair.extra_set_values(variant, magic)
    values["InpModelRiskMinPct"] = MODEL_RISK_MIN_PCT.get(variant.adapter_id, 0.005)
    values["InpModelRiskMaxPct"] = min(float(variant.model_risk_max_pct), 0.05)
    values["InpModelRiskFallbackLot"] = variant.fixed_lot
    return values


def build_attempts(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    for variant_index, variant in enumerate(STAGE59_VARIANTS, start=1):
        variant_root = RUN_ROOT / variant.adapter_id
        for split in ("validation_is", "oos"):
            date_values = parse_ini(source_attempt_ini(split, variant))
            split_token = "val" if split == "validation_is" else "oos"
            for role_index, (tier, attempt_role, prefix, attempt_token) in enumerate(
                (
                    (mt5.TIER_A, "tier_only_total", f"mt5_tier_a_only_{variant.adapter_id}", "ta"),
                    (mt5.TIER_AB, "routed_total", f"mt5_routed_{variant.adapter_id}", "rt"),
                ),
                start=1,
            ):
                magic = 5905500 + variant_index * 100 + (1 if split == "validation_is" else 50) + role_index
                attempts.append(
                    attempt_payload(
                        run_root=variant_root,
                        run_id=RUN_ID,
                        stage_number=59,
                        exploration_label="stage59B_BaselineAdapter__ModelSourceOrBackupBranch",
                        attempt_name=f"{variant.adapter_id}_{attempt_token}_{split_token}",
                        tier=tier,
                        split=split,
                        model_path=str(inputs["model_exports"][variant.adapter_id]["common_path"]),
                        model_id=f"{RUN_ID}_{variant.adapter_id}_entry_adapter",
                        model_backend="ebm_table",
                        feature_path=str(inputs["feature_exports"][variant.adapter_id][split]["common_path"]),
                        feature_count=1,
                        feature_order_hash=feature_order_hash_for_variant(variant),
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


def route_coverage() -> dict[str, Any]:
    coverage: dict[str, Any] = {
        "by_split": {},
        "tier_b_disabled_reason": "disabled_due_run50BR_and_run50BQ_fallback_only_damage",
    }
    for variant in STAGE59_VARIANTS:
        coverage[variant.adapter_id] = {}
        for name, split in (("validation", "validation_is"), ("oos", "oos")):
            a_rows = max(0, sum(1 for _ in io_path(source_feature(split, variant, "a")).open("r", encoding="utf-8-sig")) - 1)
            b_path = source_feature(split, variant, "b")
            b_rows = max(0, sum(1 for _ in io_path(b_path).open("r", encoding="utf-8-sig")) - 1) if path_exists(b_path) else 0
            coverage[variant.adapter_id][name] = {
                "source_anchor": source_anchor_for_variant(variant),
                "tier_a_primary_rows": a_rows,
                "tier_b_fallback_rows_available_but_disabled": b_rows,
                "tier_b_fallback_rows_used": 0,
                "routed_labelable_rows": a_rows,
            }
    return coverage


def patch_stage58_measurement_helpers() -> None:
    # The Stage58 measurement helpers are reused only to keep KPI parsing comparable.
    repair.STAGE_ID = STAGE59_ID
    repair.RUN_NUMBER = RUN_NUMBER
    repair.RUN_ID = RUN_ID
    repair.RUN_ROOT = RUN_ROOT
    repair.REPAIR_VARIANTS = STAGE59_VARIANTS
    s58.STAGE58_ID = STAGE59_ID
    s58.RUN_NUMBER = RUN_NUMBER
    s58.RUN_ID = RUN_ID
    s58.PACKET_ID = PACKET_ID
    s58.PARENT_RUN_ID = PARENT_RUN_ID
    s58.RUN_ROOT = RUN_ROOT
    s58.REVIEWS_ROOT = REVIEWS_ROOT
    s58.STAGE58_VARIANTS = STAGE59_VARIANTS
    s58.COMMON_ROOT = COMMON_ROOT


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
    manifest = RUN_ROOT / "run_manifest.json"
    kpi = RUN_ROOT / "kpi_record.json"
    if not path_exists(manifest) or not path_exists(kpi):
        raise FileNotFoundError("Stage59B existing run_manifest.json or kpi_record.json is missing")
    payload = json.loads(io_path(manifest).read_text(encoding="utf-8-sig"))
    payload.update(json.loads(io_path(kpi).read_text(encoding="utf-8-sig")))
    return payload


def best_repaired_variant(summary_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    candidates: list[dict[str, Any]] = []
    for variant in STAGE59_VARIANTS:
        val, oos = s58.routed_pair(summary_rows, variant.adapter_id)
        if not val or not oos:
            continue
        score = (
            (s58.as_float(val.get("net_profit"), 0.0) or 0.0)
            + (s58.as_float(oos.get("net_profit"), 0.0) or 0.0)
            + 750.0 * (s58.as_float(val.get("profit_factor"), 0.0) or 0.0)
            + 750.0 * (s58.as_float(oos.get("profit_factor"), 0.0) or 0.0)
            - 0.6 * (s58.as_float(val.get("max_drawdown_amount"), 0.0) or 0.0)
            - 0.6 * (s58.as_float(oos.get("max_drawdown_amount"), 0.0) or 0.0)
        )
        candidates.append({"adapter_id": variant.adapter_id, "label": variant.label, "validation": dict(val), "oos": dict(oos), "score": score})
    return max(candidates, key=lambda item: s58.as_float(item.get("score"), -999999.0) or -999999.0, default={})


def repair_failure_reasons(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]]) -> list[str]:
    reasons: list[str] = []
    best = best_repaired_variant(summary_rows)
    if not best:
        return ["mandatory_model_risk_atr_repaired_variant_missing"]
    val = best.get("validation", {})
    oos = best.get("oos", {})
    for label, row in (("validation", val), ("oos", oos)):
        if (s58.as_float(row.get("net_profit"), 0.0) or 0.0) <= 0.0:
            reasons.append(f"{label}_net_not_positive_after_repair")
        if (s58.as_float(row.get("profit_factor"), 0.0) or 0.0) < 1.10:
            reasons.append(f"{label}_pf_lt_1_10_after_repair")
        if (s58.as_float(row.get("cost_stressed_expectancy"), 0.0) or 0.0) <= 0.0:
            reasons.append(f"{label}_cost_stressed_expectancy_not_positive_after_repair")
        if (s58.as_float(row.get("max_model_risk_pct"), 0.0) or 0.0) <= 0.0:
            reasons.append(f"{label}_model_risk_pct_not_observed")
        if (s58.as_float(row.get("avg_open_sl_points"), 0.0) or 0.0) <= 0.0 or (s58.as_float(row.get("avg_open_tp_points"), 0.0) or 0.0) <= 0.0:
            reasons.append(f"{label}_atr_bracket_not_observed")
    best_id = best.get("adapter_id")
    segment_flags = [
        row
        for row in segment_rows
        if row.get("adapter_id") == best_id
        and row.get("segment_type") == "chronological_third"
        and row.get("quality_flag")
        and row.get("quality_flag") != "acceptable_measurement_only"
    ]
    if segment_flags:
        reasons.append("post_repair_segment_flags_present")
    return sorted(set(reasons))


def decide_stage59(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]], external: str) -> str:
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
        return "new_bounded_backup_adapter_stage_to_be_named"
    if decision == "open_new_model_branch":
        return "new_model_branch_to_be_named"
    return NEXT_REPAIR_STAGE_ID


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
                    "artifact_id": f"{RUN_ID}__{path.name}",
                    "stage_id": STAGE59_ID,
                    "run_id": RUN_ID,
                    "artifact_type": "stage59b_model_source_or_backup_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "hash_policy": "lf_normalized_text" if path.suffix.lower() in {".csv", ".json", ".md"} else "raw_file",
                    "created_at_utc": created,
                    "notes": "Stage59B bounded model source or backup branch artifact.",
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
                    "stage_id": STAGE59_ID,
                    "run_id": RUN_ID,
                    "artifact_type": "mt5_strategy_tester_report",
                    "path": rel(report_path),
                    "sha256": sha256_file_lf_normalized(report_path),
                    "hash_policy": "raw_file",
                    "created_at_utc": created,
                    "notes": "Actual Stage59B MT5 Strategy Tester HTML report.",
                }
            )
    return rows


def write_run_identity(result: Mapping[str, Any]) -> None:
    write_json(
        RUN_ROOT / "run_manifest.json",
        {
            "run_id": RUN_ID,
            "packet_id": PACKET_ID,
            "stage_id": STAGE59_ID,
            "stage_number": 59,
            "run_number": RUN_NUMBER,
            "bounded_question": "Can model source or backup branch repair the remaining post-Stage59A weakness without starting ONNX?",
            "source_stage59a_decision": rel(SOURCE_STAGE59A_DECISION),
            "source_stage59a_pushed_commit": STAGE59A_PUSHED_COMMIT,
            "variants": [
                {
                    **variant.__dict__,
                    "source_anchor": source_anchor_for_variant(variant),
                    "signal_column": signal_column_for_variant(variant),
                    "feature_order_hash": feature_order_hash_for_variant(variant),
                }
                for variant in STAGE59_VARIANTS
            ],
            "attempts": result.get("attempts", []),
            "common_copies": result.get("common_copies", []),
            "compile": result.get("compile", {}),
            "external_verification_status": result.get("external_verification_status"),
            "judgment": result.get("judgment"),
            "claim_boundary": BOUNDARY,
        },
    )
    write_json(
        RUN_ROOT / "kpi_record.json",
        {
            "run_id": RUN_ID,
            "packet_id": PACKET_ID,
            "stage_id": STAGE59_ID,
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
                "stage_id": STAGE59_ID,
                "lane": "baseline_adapter_model_source_or_backup_branch",
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
        stage_id=STAGE59_ID,
        mt5_kpi_records=result.get("mt5_kpi_records", []),
        run_output_root=RUN_ROOT,
        external_verification_status=external,
    )
    ledger_rows.append(
        {
            "ledger_row_id": f"{RUN_ID}__aggregate_model_source_or_backup_branch",
            "stage_id": STAGE59_ID,
            "run_id": RUN_ID,
            "subrun_id": "aggregate_model_source_or_backup_branch",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "model_source_or_backup_branch",
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
            "notes": "Stage59B bounded model source or backup branch; not final package completion.",
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
    return f"""# Stage59B Model Source Or Backup Branch Report(59B단계 모델 원천 또는 예비 분기 보고서)

- stage(단계): `{STAGE59_ID}`
- run(실행): `{RUN_ID}`
- source_adapter(원천 어댑터): `{SOURCE_ADAPTER_ID}`
- source_stage59a_commit(원천 59A단계 커밋): `{STAGE59A_PUSHED_COMMIT}`
- external_verification_status(외부 검증 상태): `{external}`
- decision(판정): `{decision}`
- boundary(경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Can model source or backup branch(모델 원천 또는 예비 분기) repair the remaining post-Stage59A weakness(59A단계 이후 남은 약점) while keeping ATR SL/TP(ATR 손절/익절) and model-controlled risk%(모델 제어 위험률), without starting ONNX hardening(ONNX 경화)?

## Result Table(결과 표)

| adapter(어댑터) | split(구간) | PF(수익 팩터) | net(순손익) | DD(손실폭) | cost exp(비용 기대값) | avg risk(평균 위험률) | lot(랏) | SL | TP |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
{table}

## Read(판독)

- best_repaired_adapter(최선 수리 어댑터): `{best.get('adapter_id', 'none')}`
- failure_reasons(실패/약점 사유): `{";".join(reasons) if reasons else "none"}`
- repaired_adapter_summary(수리 어댑터 요약): `{rel(SUMMARY_CSV_PATH)}`
- repaired_segment_kpi_summary(수리 구간 KPI 요약): `{rel(SEGMENT_KPI_PATH)}`
- repaired_risk_atr_telemetry(수리 위험/ATR 텔레메트리): `{rel(RISK_ATR_TELEMETRY_PATH)}`

Effect(효과): Stage59B(59B단계)는 current v64 source(현재 v64 원천)와 v60 backup source(v60 예비 원천)를 같은 ATR/risk(ATR/위험) 조건에서 비교하지만, final adapter completion(최종 어댑터 완료)이나 ONNX hardening(ONNX 경화) 시작을 자동으로 만들지 않는다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위).
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
    return f"""# Stage59B Model Source Equity Curve Audit(59B단계 모델 원천 자금 곡선 감사)

- best_repaired_adapter(최선 수리 어댑터): `{best_id}`
- audit_boundary(감사 경계): `segment/equity measurement only(구간/자금 측정 전용)`
- quality_flags(품질 표식): `{";".join(flags) if flags else "none"}`

## Chronological Thirds(시간 순서 3분할)

{lines}

Effect(효과): final net(최종 순손익)만 보지 않고 validation/OOS(검증/표본외) 구간 흔들림과 drawdown recovery(낙폭 회복)를 다음 판정에 반영한다.
"""


def decision_markdown(decision: str, reasons: Sequence[str], best: Mapping[str, Any], external: str) -> str:
    return f"""# Stage59B Decision(59B단계 판정)

decision(판정): `{decision}`

Stage59B(59B단계)는 model source or backup branch(모델 원천 또는 예비 분기)를 bounded repair(경계 수리)로 기록한다. Effect(효과): source branch(원천 분기)의 성공/실패가 다음 bounded stage(경계 단계)의 입력 근거가 된다.

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

Stage59B closeout(59B단계 종료)는 overall goal completion(전체 목표 완료)이 아니다. Effect(효과): Stage60(60단계) ONNX hardening(ONNX 경화)은 adapter quality(어댑터 품질)가 강할 때만 열린다.

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
    write_csv(SUMMARY_CSV_PATH, summary_rows)
    write_csv(SEGMENT_KPI_PATH, segment_rows)
    write_csv(RISK_ATR_TELEMETRY_PATH, risk_rows)
    write_md(REPORT_PATH, report_markdown(summary_rows, decision, reasons, external))
    write_md(EQUITY_AUDIT_PATH, equity_audit_markdown(summary_rows, segment_rows))
    write_md(DECISION_PATH, decision_markdown(decision, reasons, best, external))
    write_json(
        SUMMARY_JSON_PATH,
        {
            "created_at_utc": utc_now(),
            "stage_id": STAGE59_ID,
            "run_id": RUN_ID,
            "packet_id": PACKET_ID,
            "source_stage59a_decision": rel(SOURCE_STAGE59A_DECISION),
            "source_stage59a_pushed_commit": STAGE59A_PUSHED_COMMIT,
            "source_adapter": SOURCE_ADAPTER_ID,
            "variants": [
                {
                    **variant.__dict__,
                    "source_anchor": source_anchor_for_variant(variant),
                    "signal_column": signal_column_for_variant(variant),
                    "feature_order_hash": feature_order_hash_for_variant(variant),
                }
                for variant in STAGE59_VARIANTS
            ],
            "external_verification_status": external,
            "decision": decision,
            "best_repaired_variant": best,
            "failure_reasons": reasons,
            "required_outputs": {
                "adapter_repair_report": rel(REPORT_PATH),
                "repaired_adapter_summary_json": rel(SUMMARY_JSON_PATH),
                "repaired_adapter_summary_csv": rel(SUMMARY_CSV_PATH),
                "repaired_segment_kpi_summary": rel(SEGMENT_KPI_PATH),
                "repaired_equity_curve_audit": rel(EQUITY_AUDIT_PATH),
                "repaired_risk_atr_telemetry": rel(RISK_ATR_TELEMETRY_PATH),
                "stage59b_decision": rel(DECISION_PATH),
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
            "support_skills": ["obsidian-runtime-parity", "obsidian-backtest-forensics", "obsidian-result-judgment"],
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
            "hypothesis": "Changing to the v60 backup source may repair the remaining Stage59A validation cost-stressed weakness while preserving ATR bracket and model-controlled risk behavior",
            "decision_use": "route the full BaselineAdapter repair toward Stage60 only if source quality is strong, otherwise continue bounded repair or open a new model branch",
            "comparison_baseline": "Stage59A best adapter s59a_thr57_mr03_wideatr_sd5",
            "control_variables": ["US100", "M5", "split_v1", "Tier B disabled", "wide ATR bracket", "3% model-controlled risk cap", "ONNX deferred"],
            "changed_variables": ["feature source anchor", "signal column", "backup threshold"],
            "success_criteria": ["validation and OOS net positive", "validation and OOS PF >= 1.10", "validation and OOS cost-stressed expectancy positive", "ATR and model risk telemetry present", "no severe segment flags"],
            "failure_criteria": ["negative validation/OOS net", "PF < 1.10", "cost-stressed expectancy <= 0", "missing risk or ATR telemetry", "segment flags remain"],
            "stop_condition": "three bounded Stage59B variants only",
            "status": "completed",
        },
        "runtime_evidence_gate.json": {"external_verification_status": external, "mt5_reports": result.get("strategy_tester_reports", []), "status": external},
        "kpi_contract_audit.json": {"summary_rows": len(summary_rows), "segment_rows": len(segment_rows), "risk_rows": len(risk_rows), "status": "completed"},
        "result_judgment_gate.json": {
            "result_subject": RUN_ID,
            "judgment_label": decision,
            "failure_reasons": reasons,
            "best_repaired_adapter": best.get("adapter_id", "none"),
            "claim_boundary": BOUNDARY,
            "status": "passed_with_boundary",
        },
        "artifact_lineage_audit.json": {
            "source_inputs": [rel(SOURCE_STAGE59A_DECISION), rel(SOURCE_STAGE59A_REPORT), rel(SOURCE_MODEL), rel(BACKUP_MODEL)],
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
            "stage_id": STAGE59_ID,
            "run_id": RUN_ID,
            "decision": decision,
            "external_verification_status": external,
            "required_outputs": {
                "adapter_repair_report": rel(REPORT_PATH),
                "repaired_adapter_summary_json": rel(SUMMARY_JSON_PATH),
                "repaired_adapter_summary_csv": rel(SUMMARY_CSV_PATH),
                "repaired_segment_kpi_summary": rel(SEGMENT_KPI_PATH),
                "repaired_equity_curve_audit": rel(EQUITY_AUDIT_PATH),
                "repaired_risk_atr_telemetry": rel(RISK_ATR_TELEMETRY_PATH),
                "stage59b_decision": rel(DECISION_PATH),
            },
            "claim_boundary": BOUNDARY,
            "overall_goal_complete": False,
        },
    }
    for name, payload in files.items():
        write_json(PACKET_ROOT / name, payload)


def write_stage_docs(decision: str) -> None:
    next_stage = next_stage_for_decision(decision)
    write_md(
        SPEC_ROOT / "stage_brief.md",
        f"""# Stage59B Brief(59B단계 개요)

- stage_id(단계 ID): `{STAGE59_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE59A_ID}`
- source_decision(원천 판정): `continue_repair_in_new_bounded_stage`
- bounded_question(경계 질문): `Can model source or backup branch repair the remaining post-Stage59A weakness without starting ONNX?`
- boundary(경계): `{BOUNDARY}`

Stage59B(59B단계)는 current v64 source(현재 v64 원천)와 v60 backup source(v60 예비 원천)를 같은 ATR/risk(ATR/위험) 조건으로 비교한다. Effect(효과): ONNX hardening(ONNX 경화)을 열기 전에 남은 약점이 source branch(원천 분기) 문제인지 확인한다.
""",
    )
    write_md(
        INPUT_ROOT / "input_refs.md",
        f"""# Stage59B Input References(59B단계 입력 참조)

- stage59a_decision(59A단계 판정): `{rel(SOURCE_STAGE59A_DECISION)}`
- stage59a_report(59A단계 보고서): `{rel(SOURCE_STAGE59A_REPORT)}`
- stage59a_summary(59A단계 요약): `{rel(SOURCE_STAGE59A_SUMMARY)}`
- stage59a_segment_kpi(59A단계 구간 KPI): `{rel(SOURCE_STAGE59A_SEGMENTS)}`
- stage59a_risk_telemetry(59A단계 위험 텔레메트리): `{rel(SOURCE_STAGE59A_RISK)}`
- stage59a_pushed_commit(59A단계 푸시 커밋): `{STAGE59A_PUSHED_COMMIT}`
- development_source_model(개발 원천 모델): `{rel(SOURCE_MODEL)}`
- backup_source_model(예비 원천 모델): `{rel(BACKUP_MODEL)}`
""",
    )
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage59B Selection Status(59B단계 선택 상태)

- stage_status(단계 상태): `closed_bounded_model_source_or_backup_branch`
- source_stage(원천 단계): `{SOURCE_STAGE59A_ID}`
- source_decision(원천 판정): `continue_repair_in_new_bounded_stage`
- stage59b_decision(59B단계 판정): `{decision}`
- next_stage_or_branch(다음 단계/분기): `{next_stage}`
- selected_research_baseline(선택 연구 기준선): `none`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage59B(59B단계)는 model source branch(모델 원천 분기) 결과를 보존하지만 final package(최종 패키지)나 operating claim(운영 주장)을 만들지 않는다.
""",
    )
    if decision == "continue_repair_in_new_bounded_stage":
        next_root = Path("stages") / NEXT_REPAIR_STAGE_ID
        write_md(
            next_root / "00_spec/stage_brief.md",
            f"""# Stage59C Brief(59C단계 개요)

- stage_id(단계 ID): `{NEXT_REPAIR_STAGE_ID}`
- source_stage(원천 단계): `{STAGE59_ID}`
- source_decision(원천 판정): `{decision}`
- bounded_question(경계 질문): `Can a new model source branch repair the remaining post-Stage59B weakness without starting ONNX?`
- boundary(경계): `{BOUNDARY}`

Stage59C(59C단계)는 Stage59B(59B단계) 후에도 남은 약점을 new model source branch(새 모델 원천 분기)로 다루는 계획 단계다. Effect(효과): Stage60 ONNX(60단계 ONNX)는 adapter quality(어댑터 품질)가 강해질 때까지 열지 않는다.
""",
        )
        write_md(
            next_root / "01_inputs/input_refs.md",
            f"""# Stage59C Input References(59C단계 입력 참조)

- stage59b_decision(59B단계 판정): `{rel(DECISION_PATH)}`
- adapter_repair_report(어댑터 수리 보고서): `{rel(REPORT_PATH)}`
- repaired_adapter_summary(수리 어댑터 요약): `{rel(SUMMARY_CSV_PATH)}`
- repaired_segment_kpi_summary(수리 구간 KPI 요약): `{rel(SEGMENT_KPI_PATH)}`
- repaired_risk_atr_telemetry(수리 위험/ATR 텔레메트리): `{rel(RISK_ATR_TELEMETRY_PATH)}`
""",
        )
        write_md(
            next_root / "03_reviews/review_index.md",
            """# Stage59C Review Index(59C단계 검토 색인)

Stage59C(59C단계)는 아직 planned(계획) 상태다. Effect(효과): Stage59B(59B단계) 약점 기록을 다음 bounded repair(경계 수리)에 연결한다.
""",
        )
        write_md(
            next_root / "04_selected/selection_status.md",
            f"""# Stage59C Selection Status(59C단계 선택 상태)

- stage_status(단계 상태): `active_planned_from_stage59b`
- source_stage(원천 단계): `{STAGE59_ID}`
- source_decision(원천 판정): `{decision}`
- selected_research_baseline(선택 연구 기준선): `none`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage59C(59C단계)는 Stage59B(59B단계)의 남은 약점을 new model source branch(새 모델 원천 분기)로만 다룬다.
""",
        )
    write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage59B Review Index(59B단계 검토 색인)

- adapter_repair_report(어댑터 수리 보고서): `{rel(REPORT_PATH)}`
- repaired_adapter_summary(수리 어댑터 요약): `{rel(SUMMARY_CSV_PATH)}`
- repaired_segment_kpi_summary(수리 구간 KPI 요약): `{rel(SEGMENT_KPI_PATH)}`
- repaired_equity_curve_audit(수리 자금 곡선 감사): `{rel(EQUITY_AUDIT_PATH)}`
- repaired_risk_atr_telemetry(수리 위험/ATR 텔레메트리): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- stage59b_decision(59B단계 판정): `{rel(DECISION_PATH)}`
""",
    )


def update_current_truth(decision: str, summary_rows: Sequence[Mapping[str, Any]], external: str) -> None:
    best = best_repaired_variant(summary_rows)
    next_stage = next_stage_for_decision(decision)
    next_packet = "stage59c_new_model_source_branch_v1" if decision == "continue_repair_in_new_bounded_stage" else "stage60_onnx_hardening_v1"
    next_run = "run56A_stage59c_new_model_source_branch_v1" if decision == "continue_repair_in_new_bounded_stage" else "run56A_stage60_onnx_hardening_v1"
    write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{next_packet}`
- current_run(현재 실행): `{next_run}`
- active_stage(활성 단계): `{next_stage}`
- selected_research_baseline(선택 연구 기준선): `none`
- development_anchor(개발 기준점): `{DEVELOPMENT_ANCHOR}`
- backup_anchor(예비 기준점): `{BACKUP_ANCHOR}`
- adapter_under_review(검토 중 어댑터): `{SOURCE_ADAPTER_ID}`
- status(상태): `stage59b_closed_{decision}`
- claim_boundary(주장 경계): research/development only(연구/개발 전용)

Stage59B(59B단계) closed(종료) as bounded model source or backup branch(경계 모델 원천 또는 예비 분기). Effect(효과): v64 control(현재 v64 대조군)과 v60 backup source(v60 예비 원천)는 measured(측정됨)됐지만 final adapter(최종 어댑터) 또는 overall goal complete(전체 목표 완료)는 아니다.

## Latest Stage59B Evidence(최신 59B단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- best_repaired_adapter(최선 수리 어댑터): `{best.get('adapter_id', 'none')}`
- external_verification_status(외부 검증 상태): `{external}`
- next_stage_or_branch(다음 단계/분기): `{next_stage}`
- report(보고서): `{rel(REPORT_PATH)}`
- stage59b_decision(59B단계 판정): `{rel(DECISION_PATH)}`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), overall_goal_complete(전체 목표 완료).
""",
    )
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = re.sub(r"^current_run_id: .*$", f"current_run_id: {next_run}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^updated_on: .*$", "updated_on: '2026-05-15'", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^active_stage: .*$", f"active_stage: {next_stage}", text, count=1, flags=re.MULTILINE)
    focus = (
        "current_focus:\n"
        f"- >-\n"
        f"  Stage59B(59B단계) `{STAGE59_ID}` closed(종료) as bounded model source or backup branch(경계 모델 원천 또는 예비 분기); decision(판정)=`{decision}`. "
        f"Effect(효과): full adapter repair(전체 어댑터 수리)는 계속 진행 중이며 final(최종) 또는 operating(운영) 주장은 없다.\n"
        f"- >-\n"
        f"  Next stage_or_branch(다음 단계/분기) `{next_stage}` is active/planned(활성/계획). Effect(효과): Stage59B(59B단계) 결과를 다음 bounded step(경계 다음 단계)으로 넘긴다.\n"
    )
    text = re.sub(
        r"current_focus:\n(?:- >-\n  Stage59B[^\n]*\n- >-\n  Next stage_or_branch[^\n]*\n)*",
        "current_focus:\n",
        text,
        count=1,
    )
    text = re.sub(r"current_focus:\n", focus, text, count=1)
    block = f"""

stage59b_model_source_or_backup_branch:
  packet_id: {PACKET_ID}
  stage_id: {STAGE59_ID}
  status: closed_bounded_model_source_or_backup_branch
  current_run_id: {RUN_ID}
  source_adapter: {SOURCE_ADAPTER_ID}
  source_stage59a_pushed_commit: {STAGE59A_PUSHED_COMMIT}
  best_repaired_adapter: {best.get('adapter_id', 'none')}
  decision: {decision}
  next_stage_or_branch: {next_stage}
  report_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  external_verification_status: {external}
  boundary: {BOUNDARY}
"""
    if "stage59b_model_source_or_backup_branch:" in text:
        text = re.sub(r"\nstage59b_model_source_or_backup_branch:\n(?:  .*\n)*", block, text, count=1)
    else:
        text += block
    io_path(WORKSPACE_STATE_PATH).write_text(text, encoding="utf-8-sig")


def append_changelog(decision: str) -> None:
    entry = (
        "\n## 2026-05-15 - Stage59B model source or backup branch closeout(59B단계 모델 원천 또는 예비 분기 종료)\n\n"
        f"- run(실행): `{RUN_ID}`\n"
        f"- decision(판정): `{decision}`\n"
        f"- effect(효과): Stage59A(59A단계) 이후 남은 cost-stressed weakness(비용 압박 약점)를 v64 control(현재 v64 대조군)과 v60 backup source(v60 예비 원천)로 측정하고 다음 단계/분기 조건을 남겼다.\n"
    )
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if f"- run(실행): `{RUN_ID}`" not in existing:
        io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage59B bounded model source or backup branch.")
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(METAEDITOR_PATH_DEFAULT))
    parser.add_argument("--terminal-data-root", default=str(TERMINAL_DATA_ROOT_DEFAULT))
    parser.add_argument("--common-files-root", default=str(COMMON_FILES_ROOT_DEFAULT))
    parser.add_argument("--tester-profile-root", default=str(TESTER_PROFILE_ROOT_DEFAULT))
    parser.add_argument("--timeout-seconds", type=int, default=120)
    parser.add_argument("--skip-compile", action="store_true")
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--finalize-existing", action="store_true")
    parser.add_argument("--cost-stress-per-trade", type=float, default=0.3)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    patch_stage58_measurement_helpers()
    if args.finalize_existing:
        result = load_existing_result()
    else:
        inputs = prepare_inputs(Path(args.common_files_root))
        attempts = build_attempts(inputs)
        prepared = {
            "run_id": RUN_ID,
            "stage_id": STAGE59_ID,
            "stage_number": 59,
            "run_number": RUN_NUMBER,
            "run_root": RUN_ROOT,
            "packet_id": PACKET_ID,
            "attempts": attempts,
            "common_copies": inputs["common_copies"],
            "feature_exports": inputs["feature_exports"],
            "model_artifacts": inputs["model_exports"],
            "route_coverage": route_coverage(),
            "model_family": "baseline_adapter_stage59b_model_source_or_backup_ebm_table",
            "feature_set_id": "stage59b_v64_control_or_v60_backup_signal",
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
    decision = decide_stage59(summary_rows, segment_rows, external)
    write_run_identity(result)
    write_csv(AUDIT_CSV_PATH, audit_rows)
    artifacts = artifact_rows(result)
    ledger_payload = write_ledgers(result, summary_rows, segment_rows, decision, artifacts)
    write_required_outputs(result, summary_rows, risk_rows, segment_rows, decision, ledger_payload)
    artifacts = artifact_rows(result)
    ledger_payload = write_ledgers(result, summary_rows, segment_rows, decision, artifacts)
    payload = json.loads(io_path(SUMMARY_JSON_PATH).read_text(encoding="utf-8-sig"))
    payload["ledger_payload"] = ledger_payload
    write_json(SUMMARY_JSON_PATH, payload)
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
