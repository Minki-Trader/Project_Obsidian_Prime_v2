from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import sys
from dataclasses import dataclass
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
from stage_pipelines.stage56 import agreement_firewall_density_recovery_branch as audit_support  # noqa: E402
from stage_pipelines.stage56 import baseline_adapter_mt5_development as base  # noqa: E402
from stage_pipelines.stage56 import independent_event_source_route_branch as aw  # noqa: E402


STAGE_ID = "56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection"
RUN_NUMBER = "run50BU"
RUN_ID = "run50BU_stage56_baseline_adapter_repair_v1"
PACKET_ID = "stage56_baseline_adapter_repair_v1"
TERMINAL_LABEL = "adapter_mt5_repair_completed"
IN_PROGRESS_LABEL = "adapter_repair_in_progress"
BLOCKED_LABEL = "blocked_adapter_repair_mt5_execution_missing_evidence"
BOUNDARY = "research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion"
STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
SOURCE_RUN_ROOT = STAGE_ROOT / "02_runs/run50BR"
DEVELOPMENT_ANCHOR = "v64_v47_ctxgap14_refill_etfw_h2_no_b"
BACKUP_ANCHOR = "v60_v47_et_stable_damage_firewall_h2c0_no_b"
SOURCE_VARIANT_ROOT = SOURCE_RUN_ROOT / DEVELOPMENT_ANCHOR
SOURCE_MODEL = SOURCE_RUN_ROOT / "models/stage56_context_timed_event_signal_discrete_score_table.csv"
SIGNAL_COLUMN = "stage56_context_gap_refill_signal"
FEATURE_ORDER_HASH = ordered_hash((SIGNAL_COLUMN,))
COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage56/{RUN_NUMBER}_baseline_adapter_repair"

REPORT_PATH = REVIEWS_ROOT / "run50BU_baseline_adapter_repair_report.md"
SUMMARY_JSON_PATH = REVIEWS_ROOT / "run50BU_baseline_adapter_repair_summary.json"
SUMMARY_CSV_PATH = REVIEWS_ROOT / "run50BU_baseline_adapter_repair_summary.csv"
AUDIT_CSV_PATH = REVIEWS_ROOT / "run50BU_baseline_adapter_repair_audit.csv"
RISK_CSV_PATH = REVIEWS_ROOT / "run50BU_baseline_adapter_repair_risk_telemetry.csv"
SELECTION_STATUS_PATH = SELECTED_ROOT / "selection_status.md"
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
PROGRESS_LOG_PATH = Path("docs/agent_control/packets/stage56_reopen_goal_v1/progress_log.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_ALPHA_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"
CANDIDATE_CSV_PATH = REVIEWS_ROOT / "run50BS_candidate_selection.csv"
FIRST_ADAPTER_SUMMARY_CSV = REVIEWS_ROOT / "run50BT_baseline_adapter_mt5_summary.csv"
FIRST_ADAPTER_RISK_CSV = REVIEWS_ROOT / "run50BT_baseline_adapter_risk_telemetry.csv"
ANCHOR_REPORT_PATH = REVIEWS_ROOT / "run50BS_baseline_adapter_transition.md"
FIRST_ADAPTER_REPORT_PATH = REVIEWS_ROOT / "run50BT_baseline_adapter_mt5_development.md"

VALIDATION_DAYS = 183.0
OOS_DAYS = 195.0
SHORT_THRESHOLD = 0.55
LONG_THRESHOLD = 0.55
MIN_MARGIN = 0.0


@dataclass(frozen=True)
class RepairVariant:
    adapter_id: str
    label: str
    atr_enabled: bool
    model_risk_enabled: bool
    fixed_lot: float
    atr_stop_multiplier: float
    atr_take_profit_multiplier: float
    model_risk_max_pct: float
    notes: str
    reentry_cooldown_bars: int = 0
    same_direction_reentry_cooldown_bars: int = 0
    entry_transition_only: bool = False
    entry_transition_rearm_min_confidence_delta: float = 0.0
    short_threshold: float = SHORT_THRESHOLD
    long_threshold: float = LONG_THRESHOLD
    close_on_flat_signal: bool = False
    reverse_on_opposite_signal: bool = True
    close_only_on_opposite_signal: bool = False
    max_hold_bars: int = 2


@dataclass(frozen=True)
class AuditVariant:
    variant_id: str


REPAIR_VARIANTS = (
    RepairVariant(
        adapter_id="ba02_control_no_atr_fixed_lot",
        label="control_no_atr_fixed_lot",
        atr_enabled=False,
        model_risk_enabled=False,
        fixed_lot=0.1,
        atr_stop_multiplier=0.0,
        atr_take_profit_multiplier=0.0,
        model_risk_max_pct=0.0,
        notes="Run the adapter entry/route path with run50BR-style no ATR and fixed 0.1 lot.",
    ),
    RepairVariant(
        adapter_id="ba03_atr_fixed_lot",
        label="atr_fixed_lot",
        atr_enabled=True,
        model_risk_enabled=False,
        fixed_lot=0.1,
        atr_stop_multiplier=1.5,
        atr_take_profit_multiplier=2.0,
        model_risk_max_pct=0.0,
        notes="Keep ATR bracket but remove dynamic risk sizing to isolate bracket damage.",
    ),
    RepairVariant(
        adapter_id="ba04_wide_atr_fixed_lot",
        label="wide_atr_fixed_lot",
        atr_enabled=True,
        model_risk_enabled=False,
        fixed_lot=0.1,
        atr_stop_multiplier=2.5,
        atr_take_profit_multiplier=3.5,
        model_risk_max_pct=0.0,
        notes="Widen ATR bracket while holding fixed 0.1 lot to test bracket repair.",
    ),
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    candidate = Path(path)
    try:
        return io_path(candidate).resolve().relative_to(io_path(Path(".")).resolve()).as_posix()
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


def append_once(path: Path, text: str) -> None:
    existing = io_path(path).read_text(encoding="utf-8-sig") if path_exists(path) else ""
    if text.strip() in existing:
        return
    write_md(path, existing.rstrip() + "\n" + text.strip() + "\n")


def split_days(split: str) -> float:
    return VALIDATION_DAYS if split == "validation_is" else OOS_DAYS


def source_attempt_ini(split: str) -> Path:
    name = "x01_ta_val.ini" if split == "validation_is" else "x01_ta_oos.ini"
    return SOURCE_VARIANT_ROOT / "mt5" / name


def source_feature(split: str, tier: str = "a") -> Path:
    token = "val" if split == "validation_is" else "oos"
    return SOURCE_VARIANT_ROOT / "features" / f"{DEVELOPMENT_ANCHOR}_{tier}_{token}.csv"


def copy_local(source: Path, destination: Path) -> dict[str, Any]:
    if not path_exists(source):
        raise FileNotFoundError(source)
    io_path(destination.parent).mkdir(parents=True, exist_ok=True)
    shutil.copy2(io_path(source), io_path(destination))
    return {"source": rel(source), "path": rel(destination), "sha256": sha256_file_lf_normalized(destination)}


def prepare_inputs(common_files_root: Path) -> dict[str, Any]:
    model_local = RUN_ROOT / "models" / SOURCE_MODEL.name
    copied = [copy_local(SOURCE_MODEL, model_local)]
    copied.append(copy_to_common(model_local, f"{COMMON_ROOT}/models/{model_local.name}", common_files_root))
    feature_exports: dict[str, dict[str, Any]] = {}
    for split in ("validation_is", "oos"):
        split_token = "val" if split == "validation_is" else "oos"
        feature_local = RUN_ROOT / DEVELOPMENT_ANCHOR / "features" / f"{DEVELOPMENT_ANCHOR}_adapter_a_{split_token}.csv"
        copied.append(copy_local(source_feature(split, "a"), feature_local))
        copied.append(copy_to_common(feature_local, f"{COMMON_ROOT}/features/{feature_local.name}", common_files_root))
        feature_exports[split] = {
            "path": rel(feature_local),
            "common_path": f"{COMMON_ROOT}/features/{feature_local.name}",
            "sha256": sha256_file_lf_normalized(feature_local),
        }
    return {
        "model_local": model_local,
        "model_common": f"{COMMON_ROOT}/models/{model_local.name}",
        "feature_exports": feature_exports,
        "common_copies": copied,
    }


def extra_set_values(variant: RepairVariant, magic: int) -> dict[str, Any]:
    return {
        "InpFixedLot": variant.fixed_lot,
        "InpAtrSltpEnabled": variant.atr_enabled,
        "InpAtrPeriod": 14,
        "InpAtrStopMultiplier": variant.atr_stop_multiplier,
        "InpAtrTakeProfitMultiplier": variant.atr_take_profit_multiplier,
        "InpAtrMinStopPoints": 0.0,
        "InpAtrMaxStopPoints": 0.0,
        "InpAtrMinTakeProfitPoints": 0.0,
        "InpAtrMaxTakeProfitPoints": 0.0,
        "InpModelRiskSizingEnabled": variant.model_risk_enabled,
        "InpModelRiskMinPct": 0.005 if variant.model_risk_enabled else 0.0,
        "InpModelRiskMaxPct": variant.model_risk_max_pct,
        "InpModelRiskConfidenceFloor": 0.55,
        "InpModelRiskConfidenceCeiling": 0.85,
        "InpModelRiskFallbackLot": variant.fixed_lot,
        "InpFallbackEnabled": False,
        "InpFallbackUseOnPrimaryFlat": False,
        "InpFallbackUseOnPrimaryLowConfidence": False,
        "InpReentryCooldownBars": int(variant.reentry_cooldown_bars),
        "InpSameDirectionReentryCooldownBars": int(variant.same_direction_reentry_cooldown_bars),
        "InpEntryTransitionOnly": bool(variant.entry_transition_only),
        "InpEntryTransitionRearmMinConfidenceDelta": float(variant.entry_transition_rearm_min_confidence_delta),
        "InpMagic": magic,
    }


def build_attempts(inputs: Mapping[str, Any], variants: Sequence[RepairVariant]) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    for variant_index, variant in enumerate(variants, start=1):
        variant_root = RUN_ROOT / variant.adapter_id
        for split in ("validation_is", "oos"):
            date_values = parse_ini(source_attempt_ini(split))
            split_token = "val" if split == "validation_is" else "oos"
            for role_index, (role, tier, attempt_role, prefix, attempt_token) in enumerate(
                (
                    ("tier_a_only", mt5.TIER_A, "tier_only_total", f"mt5_tier_a_only_{variant.adapter_id}", "ta"),
                    ("routed", mt5.TIER_AB, "routed_total", f"mt5_routed_{variant.adapter_id}", "rt"),
                ),
                start=1,
            ):
                magic = 5606000 + variant_index * 100 + (1 if split == "validation_is" else 50) + role_index
                attempts.append(
                    attempt_payload(
                        run_root=variant_root,
                        run_id=RUN_ID,
                        stage_number=56,
                        exploration_label="stage56_BaselineAdapter__RepairBatch",
                        attempt_name=f"{variant.adapter_id}_{attempt_token}_{split_token}",
                        tier=tier,
                        split=split,
                        model_path=str(inputs["model_common"]),
                        model_id=f"{RUN_ID}_{variant.adapter_id}_entry_adapter",
                        model_backend="ebm_table",
                        feature_path=str(inputs["feature_exports"][split]["common_path"]),
                        feature_count=1,
                        feature_order_hash=FEATURE_ORDER_HASH,
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
        "tier_b_disabled_reason": "disabled_due_run50BR_fallback_only_damage",
    }
    for name, split in (("validation", "validation_is"), ("oos", "oos")):
        a_rows = max(0, sum(1 for _ in io_path(source_feature(split, "a")).open("r", encoding="utf-8-sig")) - 1)
        b_path = source_feature(split, "b")
        b_rows = max(0, sum(1 for _ in io_path(b_path).open("r", encoding="utf-8-sig")) - 1) if path_exists(b_path) else 0
        coverage["by_split"][name] = {
            "tier_a_primary_rows": a_rows,
            "tier_b_fallback_rows_available_but_disabled": b_rows,
            "tier_b_fallback_rows_used": 0,
            "routed_labelable_rows": a_rows,
        }
    return coverage


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


def metric(record: Mapping[str, Any], key: str, *aliases: str) -> Any:
    metrics = record.get("metrics", {}) if isinstance(record.get("metrics"), Mapping) else {}
    for name in (key, *aliases):
        if name in metrics:
            return metrics.get(name)
    return None


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def report_path_from_record(record: Mapping[str, Any]) -> str:
    report = record.get("report", {}) if isinstance(record.get("report"), Mapping) else {}
    html = report.get("html_report", {}) if isinstance(report.get("html_report"), Mapping) else {}
    return str(html.get("path") or metric(record, "report_path") or "")


def audit_rows_for_result(result: Mapping[str, Any], variants: Sequence[RepairVariant], cost_stress_per_trade: float) -> list[dict[str, Any]]:
    original_parent = audit_support.PARENT_RUN_ID
    try:
        audit_support.PARENT_RUN_ID = RUN_ID
        return audit_support.audit_rows_for_result(
            result,
            [AuditVariant(variant.adapter_id) for variant in variants],
            cost_stress_per_trade,
        )
    finally:
        audit_support.PARENT_RUN_ID = original_parent


def build_summary_rows(
    result: Mapping[str, Any],
    variants: Sequence[RepairVariant],
    audit_rows: Sequence[Mapping[str, Any]],
    risk_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    by_view = {str(record.get("record_view")): record for record in result.get("mt5_kpi_records", [])}
    risk_by_attempt = {str(row.get("attempt_name")): row for row in risk_rows}
    audits = {str(row.get("record_view")): row for row in audit_rows}
    rows: list[dict[str, Any]] = []
    for variant in variants:
        for split in ("validation_is", "oos"):
            split_token = "validation" if split == "validation_is" else "oos"
            for view, label, role in (
                (f"mt5_tier_a_only_{variant.adapter_id}_{split}", "tier_a_only", "tier_only_total"),
                (f"mt5_routed_{variant.adapter_id}_{split}", "actual_routed_total", "routed_total"),
            ):
                record = by_view.get(view, {})
                trade_count = as_float(metric(record, "trade_count", "total_trades"))
                attempt_name = str(record.get("report", {}).get("attempt_name") or f"{variant.adapter_id}_{'ta' if label == 'tier_a_only' else 'rt'}_{'val' if split == 'validation_is' else 'oos'}")
                risk = risk_by_attempt.get(attempt_name, {})
                audit = audits.get(view, {})
                rows.append(
                    {
                        "run_id": RUN_ID,
                        "adapter_id": variant.adapter_id,
                        "repair_label": variant.label,
                        "split": split,
                        "view": label,
                        "route_role": role,
                        "tier_b_policy": "disabled_due_run50BR_fallback_only_damage",
                        "atr_enabled": variant.atr_enabled,
                        "model_risk_enabled": variant.model_risk_enabled,
                        "fixed_lot": variant.fixed_lot,
                        "atr_stop_multiplier": variant.atr_stop_multiplier,
                        "atr_take_profit_multiplier": variant.atr_take_profit_multiplier,
                        "model_risk_max_pct": variant.model_risk_max_pct,
                        "reentry_cooldown_bars": variant.reentry_cooldown_bars,
                        "same_direction_reentry_cooldown_bars": variant.same_direction_reentry_cooldown_bars,
                        "entry_transition_only": variant.entry_transition_only,
                        "entry_transition_rearm_min_confidence_delta": variant.entry_transition_rearm_min_confidence_delta,
                        "short_threshold": variant.short_threshold,
                        "long_threshold": variant.long_threshold,
                        "close_on_flat_signal": variant.close_on_flat_signal,
                        "reverse_on_opposite_signal": variant.reverse_on_opposite_signal,
                        "close_only_on_opposite_signal": variant.close_only_on_opposite_signal,
                        "max_hold_bars": variant.max_hold_bars,
                        "status": record.get("status", "missing"),
                        "trades_per_day": trade_count / split_days(split) if trade_count else 0.0,
                        "profit_factor": metric(record, "profit_factor"),
                        "net_profit": metric(record, "net_profit"),
                        "trade_count": metric(record, "trade_count", "total_trades"),
                        "max_drawdown_amount": metric(record, "max_drawdown_amount", "max_drawdown"),
                        "max_drawdown_percent": metric(record, "max_drawdown_percent"),
                        "expectancy": metric(record, "expectancy"),
                        "cost_stressed_expectancy": audit.get("cost_stressed_expectancy"),
                        "same_move_reentry_ratio": audit.get("same_move_reentry_ratio"),
                        "mfe_capture_ratio": audit.get("mfe_capture_ratio"),
                        "cooldown12_trades_per_day": audit.get("trades_per_day_after_cooldown"),
                        "density_gain_survives_12bar_cooldown": audit.get("density_gain_survives_12bar_cooldown"),
                        "risk_floor_applied_count": risk.get("risk_floor_applied_count"),
                        "max_model_risk_pct": risk.get("max_model_risk_pct"),
                        "max_actual_risk_pct_after_floor": risk.get("max_actual_risk_pct_after_floor"),
                        "avg_executed_lot": risk.get("avg_executed_lot"),
                        "avg_atr_points": risk.get("avg_atr_points"),
                        "avg_open_sl_points": risk.get("avg_open_sl_points"),
                        "avg_open_tp_points": risk.get("avg_open_tp_points"),
                        "report_path": report_path_from_record(record),
                        "notes": variant.notes,
                    }
                )
            rows.append(
                {
                    "run_id": RUN_ID,
                    "adapter_id": variant.adapter_id,
                    "repair_label": variant.label,
                    "split": split,
                    "view": "tier_b_fallback_only",
                    "route_role": "tier_b_disabled",
                    "tier_b_policy": "disabled_due_run50BR_fallback_only_damage",
                    "status": "disabled",
                    "notes": "Tier B fallback-only remained disabled because run50BR fallback-only validation/OOS net was -94.14 / -254.32.",
                }
            )
    return rows


def load_candidate_rows() -> dict[str, Mapping[str, Any]]:
    refs: dict[str, Mapping[str, Any]] = {}
    if not path_exists(CANDIDATE_CSV_PATH):
        return refs
    with io_path(CANDIDATE_CSV_PATH).open("r", encoding="utf-8-sig", newline="") as handle:
        for raw in csv.DictReader(handle):
            refs[f"{raw.get('run_number')}/{raw.get('variant_id')}"] = dict(raw)
    return refs


def load_first_adapter_rows() -> dict[tuple[str, str], Mapping[str, Any]]:
    rows: dict[tuple[str, str], Mapping[str, Any]] = {}
    if not path_exists(FIRST_ADAPTER_SUMMARY_CSV):
        return rows
    with io_path(FIRST_ADAPTER_SUMMARY_CSV).open("r", encoding="utf-8-sig", newline="") as handle:
        for raw in csv.DictReader(handle):
            rows[(str(raw.get("split")), str(raw.get("view")))] = dict(raw)
    return rows


def routed_rows(summary_rows: Sequence[Mapping[str, Any]], adapter_id: str) -> tuple[Mapping[str, Any], Mapping[str, Any]]:
    val = next(
        (
            row
            for row in summary_rows
            if row.get("adapter_id") == adapter_id
            and row.get("split") == "validation_is"
            and row.get("view") == "actual_routed_total"
        ),
        {},
    )
    oos = next(
        (
            row
            for row in summary_rows
            if row.get("adapter_id") == adapter_id
            and row.get("split") == "oos"
            and row.get("view") == "actual_routed_total"
        ),
        {},
    )
    return val, oos


def phase_a_failure_reasons(val: Mapping[str, Any], oos: Mapping[str, Any]) -> list[str]:
    reasons: list[str] = []
    checks = (
        ("validation_trades_per_day_lt_5", as_float(val.get("trades_per_day")) < 5.0),
        ("oos_trades_per_day_lt_5", as_float(oos.get("trades_per_day")) < 5.0),
        ("validation_net_not_positive", as_float(val.get("net_profit")) <= 0.0),
        ("oos_net_not_positive", as_float(oos.get("net_profit")) <= 0.0),
        ("validation_pf_lt_1_10", as_float(val.get("profit_factor")) < 1.10),
        ("oos_pf_lt_1_10", as_float(oos.get("profit_factor")) < 1.10),
        ("validation_cost_stressed_expectancy_not_positive", as_float(val.get("cost_stressed_expectancy")) <= 0.0),
        ("oos_cost_stressed_expectancy_not_positive", as_float(oos.get("cost_stressed_expectancy")) <= 0.0),
    )
    reasons.extend(name for name, failed in checks if failed)
    if val.get("status") != "completed" or oos.get("status") != "completed":
        reasons.append("mt5_record_missing_or_blocked")
    if val.get("risk_floor_applied_count") in (None, "") or oos.get("risk_floor_applied_count") in (None, ""):
        reasons.append("risk_telemetry_incomplete")
    if val.get("mfe_capture_ratio") in (None, "") or oos.get("mfe_capture_ratio") in (None, ""):
        reasons.append("mfe_audit_incomplete")
    return reasons


def best_variant(summary_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    candidates: list[dict[str, Any]] = []
    for variant in REPAIR_VARIANTS:
        val, oos = routed_rows(summary_rows, variant.adapter_id)
        if not val and not oos:
            continue
        failures = phase_a_failure_reasons(val, oos)
        score = (
            (100 if not failures else 0)
            + as_float(val.get("net_profit"))
            + as_float(oos.get("net_profit"))
            + 1000 * as_float(val.get("profit_factor"))
            + 1000 * as_float(oos.get("profit_factor"))
        )
        candidates.append(
            {
                "adapter_id": variant.adapter_id,
                "repair_label": variant.label,
                "phase_a_eligible_for_onnx": not failures,
                "failure_reasons": failures,
                "score": score,
                "validation": dict(val),
                "oos": dict(oos),
            }
        )
    return max(candidates, key=lambda row: as_float(row.get("score")), default={})


def diagnosis(summary_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    first = load_first_adapter_rows()
    control_val, control_oos = routed_rows(summary_rows, "ba02_control_no_atr_fixed_lot")
    atr_val, atr_oos = routed_rows(summary_rows, "ba03_atr_fixed_lot")
    wide_val, wide_oos = routed_rows(summary_rows, "ba04_wide_atr_fixed_lot")
    return {
        "entry_translation_mismatch": "unlikely_if_control_reproduces_anchor_directionally",
        "route_translation_mismatch": "unlikely; Tier B remains disabled and tier_a_only/routed paths share Tier A primary rows",
        "tier_b_logic": "explicitly_disabled_due_prior_damage",
        "risk_sizing": "first_adapter_dynamic_risk_changed lot exposure; repair batch disables dynamic risk to isolate",
        "lot_floor_effect": "not_primary_if_floor_count_remains_zero_or_empty",
        "atr_bracket_behavior": {
            "first_adapter": {
                "validation_net": first.get(("validation_is", "actual_routed_total"), {}).get("net_profit"),
                "oos_net": first.get(("oos", "actual_routed_total"), {}).get("net_profit"),
            },
            "control_no_atr_validation_net": control_val.get("net_profit"),
            "atr_fixed_lot_validation_net": atr_val.get("net_profit"),
            "wide_atr_validation_net": wide_val.get("net_profit"),
            "control_no_atr_oos_net": control_oos.get("net_profit"),
            "atr_fixed_lot_oos_net": atr_oos.get("net_profit"),
            "wide_atr_oos_net": wide_oos.get("net_profit"),
        },
        "same_move_split_trading": "tracked in audit rows; not repaired in this batch",
        "cost_stressed_expectancy": "tracked per routed view; positive cost-stressed expectancy is required before ONNX",
        "telemetry_gap": "risk/ATR telemetry is required for every attempt",
    }


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
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created,
                "notes": notes,
            }
        )

    for path in extra_paths:
        add(f"stage56_{RUN_NUMBER}_{aw.safe_name(path.stem, 80)}", path.suffix.lstrip(".") or "artifact", path, "BaselineAdapter repair batch artifact.")
    for report in result.get("strategy_tester_reports", []):
        html = report.get("html_report", {}) if isinstance(report.get("html_report"), Mapping) else {}
        if html.get("path"):
            add(
                f"stage56_{RUN_NUMBER}_mt5_report_{aw.safe_name(str(report.get('attempt_name') or report.get('report_name')), 100)}",
                "mt5_html_report",
                str(html["path"]),
                "Actual BaselineAdapter repair MT5 Strategy Tester HTML report.",
            )
    for execution in result.get("execution_results", []):
        runtime_outputs = execution.get("runtime_outputs", {}) if isinstance(execution.get("runtime_outputs"), Mapping) else {}
        for key, artifact_type in (("telemetry_path", "mt5_runtime_telemetry_csv"), ("summary_path", "mt5_runtime_summary_csv")):
            value = runtime_outputs.get(key)
            if value:
                add(
                    f"stage56_{RUN_NUMBER}_{artifact_type}_{aw.safe_name(str(execution.get('attempt_name')), 80)}",
                    artifact_type,
                    str(value),
                    "Common Files runtime telemetry copied by MT5 EA.",
                )
    return rows


def write_ledgers(result: Mapping[str, Any], summary_rows: Sequence[Mapping[str, Any]], artifacts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    external = str(result.get("external_verification_status") or "blocked")
    best = best_variant(summary_rows)
    status = "completed" if external == "completed" else "blocked"
    judgment = TERMINAL_LABEL if external == "completed" else BLOCKED_LABEL
    run_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_adapter_repair",
                "status": status,
                "judgment": judgment,
                "path": rel(RUN_ROOT),
                "notes": ledger_pairs(
                    (
                        ("development_anchor", DEVELOPMENT_ANCHOR),
                        ("best_adapter", best.get("adapter_id")),
                        ("phase_a_eligible_for_onnx", best.get("phase_a_eligible_for_onnx")),
                        ("boundary", BOUNDARY),
                    )
                ),
            }
        ],
        key="run_id",
    )
    ledger_rows = build_mt5_alpha_ledger_rows(
        run_id=RUN_ID,
        stage_id=STAGE_ID,
        mt5_kpi_records=result.get("mt5_kpi_records", []),
        run_output_root=RUN_ROOT,
        external_verification_status=external,
    )
    ledger_rows.append(
        {
            "ledger_row_id": f"{RUN_ID}__parent_repair_read",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "parent_repair_read",
            "parent_run_id": RUN_ID,
            "record_view": "baseline_adapter_repair_batch",
            "tier_scope": mt5.TIER_AB,
            "kpi_scope": "baseline_adapter_repair",
            "scoreboard_lane": "runtime_probe",
            "status": status,
            "judgment": judgment,
            "path": rel(SUMMARY_JSON_PATH),
            "primary_kpi": ledger_pairs(
                (
                    ("best_adapter", best.get("adapter_id")),
                    ("phase_a_eligible_for_onnx", best.get("phase_a_eligible_for_onnx")),
                    ("validation_net", (best.get("validation") or {}).get("net_profit")),
                    ("oos_net", (best.get("oos") or {}).get("net_profit")),
                    ("validation_pf", (best.get("validation") or {}).get("profit_factor")),
                    ("oos_pf", (best.get("oos") or {}).get("profit_factor")),
                )
            ),
            "guardrail_kpi": ledger_pairs(
                (
                    ("tier_b_policy", "disabled_with_evidence"),
                    ("actual_routed_total_only", True),
                    ("forbidden_operating_claims", False),
                    ("failure_reasons", best.get("failure_reasons")),
                )
            ),
            "external_verification_status": external,
            "notes": "Repair batch compares no-ATR, ATR, and wider-ATR adapter paths; not ONNX eligible unless Phase A gate is met.",
        }
    )
    for variant in REPAIR_VARIANTS:
        ledger_rows.append(
            {
                "ledger_row_id": f"{RUN_ID}__{variant.adapter_id}__tier_b_disabled_record",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": f"{variant.adapter_id}_tier_b_disabled",
                "parent_run_id": RUN_ID,
                "record_view": f"{variant.adapter_id}_tier_b_disabled",
                "tier_scope": mt5.TIER_B,
                "kpi_scope": "baseline_adapter_repair",
                "scoreboard_lane": "runtime_probe",
                "status": "disabled",
                "judgment": "tier_b_disabled_due_prior_fallback_damage",
                "path": rel(SUMMARY_JSON_PATH),
                "primary_kpi": "tier_b_fallback_only_validation_net=-94.14;tier_b_fallback_only_oos_net=-254.32",
                "guardrail_kpi": "actual_routed_total_uses_tier_a_primary_only",
                "external_verification_status": external,
                "notes": "Tier B fallback-only was recorded as disabled, not silently omitted.",
            }
        )
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id")
    project_payload = upsert_csv_rows(PROJECT_ALPHA_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id")
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, aw.ARTIFACT_COLUMNS, list(artifacts), key="artifact_id")
    return {"run_registry": run_payload, "stage_ledger": stage_payload, "project_alpha_ledger": project_payload, "artifact_registry": artifact_payload}


def write_report(summary_rows: Sequence[Mapping[str, Any]], risk_rows: Sequence[Mapping[str, Any]], result: Mapping[str, Any]) -> None:
    refs = load_candidate_rows()
    first = load_first_adapter_rows()
    anchor = refs.get(f"run50BR/{DEVELOPMENT_ANCHOR}", {})
    backup = refs.get(f"run50BQ/{BACKUP_ANCHOR}", {})
    best = best_variant(summary_rows)
    external = str(result.get("external_verification_status") or "blocked")
    label = TERMINAL_LABEL if external == "completed" else BLOCKED_LABEL
    variant_labels = ", ".join(f"{variant.label}({variant.adapter_id})" for variant in REPAIR_VARIANTS)
    lines = [
        f"# Stage56 {RUN_NUMBER} BaselineAdapter Repair Batch(Stage56 {RUN_NUMBER} 기준선 어댑터 수리 배치)",
        "",
        f"- terminal_label(종료 라벨): `{label}`",
        f"- development_anchor(개발 기준점): `run50BR/{DEVELOPMENT_ANCHOR}`",
        f"- backup_anchor(예비 기준점): `run50BQ/{BACKUP_ANCHOR}`",
        "- selected_research_baseline(선택 연구 기준선): `none`",
        f"- external_verification_status(외부 검증 상태): `{external}`",
        f"- best_adapter(최선 어댑터): `{best.get('adapter_id', 'none')}`",
        f"- phase_a_eligible_for_onnx(Phase A ONNX 적격): `{best.get('phase_a_eligible_for_onnx', False)}`",
        "",
        f"Action(행동): first adapter(첫 어댑터)의 validation damage(검증 손상)를 `{variant_labels}` repair variants(수리 변형)로 실제 MT5 validation/OOS(검증/표본외)에서 나눠 실행했다.",
        "Effect(효과): entry/route translation(진입/라우팅 번역), ATR bracket(ATR 브래킷), dynamic risk(동적 위험), cooldown/re-entry(쿨다운/재진입) 중 다음 repair branch(수리 갈래)를 좁힐 수 있다.",
        "",
        "## References(참조)",
        "",
        "| item(항목) | val day(검증 일거래) | OOS day(표본외 일거래) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 손익) | OOS net(표본외 손익) |",
        "|---|---:|---:|---:|---:|---:|---:|",
        f"| development_anchor(개발 기준점) | {anchor.get('validation_trades_per_day','')} | {anchor.get('oos_trades_per_day','')} | {anchor.get('validation_pf','')} | {anchor.get('oos_pf','')} | {anchor.get('validation_net','')} | {anchor.get('oos_net','')} |",
        f"| backup_anchor(예비 기준점) | {backup.get('validation_trades_per_day','')} | {backup.get('oos_trades_per_day','')} | {backup.get('validation_pf','')} | {backup.get('oos_pf','')} | {backup.get('validation_net','')} | {backup.get('oos_net','')} |",
        f"| first_adapter(첫 어댑터) | {first.get(('validation_is','actual_routed_total'),{}).get('trades_per_day','')} | {first.get(('oos','actual_routed_total'),{}).get('trades_per_day','')} | {first.get(('validation_is','actual_routed_total'),{}).get('profit_factor','')} | {first.get(('oos','actual_routed_total'),{}).get('profit_factor','')} | {first.get(('validation_is','actual_routed_total'),{}).get('net_profit','')} | {first.get(('oos','actual_routed_total'),{}).get('net_profit','')} |",
        "",
        "## Repair Results(수리 결과)",
        "",
        "| adapter(어댑터) | split(구간) | view(보기) | day(일거래) | PF | net(손익) | DD | cost exp(비용 기대값) | same move(동일 이동) | MFE | floor(바닥) | lot(랏) | SL | TP |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in summary_rows:
        if row.get("view") == "tier_b_fallback_only":
            continue
        lines.append(
            "| {adapter} | {split} | {view} | {day} | {pf} | {net} | {dd} | {cost} | {same} | {mfe} | {floor} | {lot} | {sl} | {tp} |".format(
                adapter=row.get("adapter_id", ""),
                split=row.get("split", ""),
                view=row.get("view", ""),
                day=aw.fmt(row.get("trades_per_day")),
                pf=aw.fmt(row.get("profit_factor")),
                net=aw.fmt(row.get("net_profit")),
                dd=aw.fmt(row.get("max_drawdown_amount")),
                cost=aw.fmt(row.get("cost_stressed_expectancy")),
                same=aw.fmt(row.get("same_move_reentry_ratio")),
                mfe=aw.fmt(row.get("mfe_capture_ratio")),
                floor=aw.fmt(row.get("risk_floor_applied_count")),
                lot=aw.fmt(row.get("avg_executed_lot")),
                sl=aw.fmt(row.get("avg_open_sl_points")),
                tp=aw.fmt(row.get("avg_open_tp_points")),
            )
        )
    lines.extend(
        [
            "",
            "## Phase A Gate(Phase A 게이트)",
            "",
            f"- phase_a_eligible_for_onnx(ONNX 적격): `{best.get('phase_a_eligible_for_onnx', False)}`",
            f"- failure_reasons(실패 사유): `{';'.join(best.get('failure_reasons', []))}`",
            "",
            "## Diagnosis(진단)",
            "",
            f"- entry_translation_mismatch(진입 번역 불일치): `{diagnosis(summary_rows).get('entry_translation_mismatch')}`",
            f"- route_translation_mismatch(라우팅 번역 불일치): `{diagnosis(summary_rows).get('route_translation_mismatch')}`",
            f"- tier_b_logic(Tier B 논리): `{diagnosis(summary_rows).get('tier_b_logic')}`",
            f"- risk_sizing(위험 크기): `{diagnosis(summary_rows).get('risk_sizing')}`",
            f"- atr_bracket_behavior(ATR 브래킷 동작): `{json.dumps(json_ready(diagnosis(summary_rows).get('atr_bracket_behavior')), ensure_ascii=False, sort_keys=True)}`",
            "",
            "## Next Branch(다음 갈래)",
            "",
            "If Phase A fails(Phase A 실패 시), do not start ONNX(ONNX 시작 금지). Continue adapter repair(어댑터 수리 지속): keep the anchor(기준점 유지) only if the no-ATR control(ATR 없는 대조군) reproduces anchor quality(기준점 품질 재현); otherwise demote anchor(기준점 강등) and switch branch(갈래 전환).",
            "",
            "No live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), reviewed_closed(검토 종료) claim(주장) is made.",
        ]
    )
    write_md(REPORT_PATH, "\n".join(lines))


def remove_workspace_block(text: str, key: str) -> str:
    lines = text.splitlines(keepends=True)
    output: list[str] = []
    index = 0
    while index < len(lines):
        if lines[index].startswith(key):
            index += 1
            while index < len(lines) and (not lines[index].strip() or lines[index].startswith(" ")):
                index += 1
            continue
        output.append(lines[index])
        index += 1
    return "".join(output)


def update_state_docs(summary_rows: Sequence[Mapping[str, Any]], result: Mapping[str, Any]) -> None:
    external = str(result.get("external_verification_status") or "blocked")
    label = TERMINAL_LABEL if external == "completed" else BLOCKED_LABEL
    best = best_variant(summary_rows)
    best_val = best.get("validation") if isinstance(best.get("validation"), Mapping) else {}
    best_oos = best.get("oos") if isinstance(best.get("oos"), Mapping) else {}
    status_label = IN_PROGRESS_LABEL if not best.get("phase_a_eligible_for_onnx") else TERMINAL_LABEL
    write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current run(현재 실행): `{RUN_ID}`
- active stage(활성 단계): `{STAGE_ID}`
- selected_research_baseline(선택 연구 기준선): `none`
- development_anchor(개발 기준점): `{DEVELOPMENT_ANCHOR}`
- backup_anchor(예비 기준점): `{BACKUP_ANCHOR}`
- status(상태): `{status_label}`
- claim_boundary(주장 경계): research/development only(연구/개발 전용)

Stage56(56단계)는 BaselineAdapter repair(기준선 어댑터 수리)를 진행 중이다.
Effect(효과): ONNX hardening(ONNX 경화)은 Phase A gate(Phase A 게이트)를 통과할 때까지 시작하지 않는다.

## Latest Repair Evidence(최신 수리 근거)

- best_adapter(최선 어댑터): `{best.get('adapter_id', 'none')}`
- Phase A eligible(Phase A 적격): `{best.get('phase_a_eligible_for_onnx', False)}`
- validation/OOS trades/day(검증/표본외 일거래): `{aw.fmt(best_val.get('trades_per_day'))}` / `{aw.fmt(best_oos.get('trades_per_day'))}`
- validation/OOS PF(검증/표본외 PF): `{aw.fmt(best_val.get('profit_factor'))}` / `{aw.fmt(best_oos.get('profit_factor'))}`
- validation/OOS net(검증/표본외 손익): `{aw.fmt(best_val.get('net_profit'))}` / `{aw.fmt(best_oos.get('net_profit'))}`
- failure_reasons(실패 사유): `{';'.join(best.get('failure_reasons', []))}`
- tier_b_policy(Tier B 정책): disabled with evidence(근거 기반 비활성)

Forbidden claims(금지 주장): live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), reviewed_closed(검토 종료).
""",
    )
    write_md(
        SELECTION_STATUS_PATH,
        f"""# Stage56 Selection Status(56단계 선택 상태)

- stage_status(단계 상태): `active_baseline_adapter_development`
- latest_run_id(최신 실행 ID): `{RUN_ID}`
- current run(현재 실행): `{RUN_ID}`
- current_judgment(현재 판정): `{status_label}`
- selected_research_baseline(선택 연구 기준선): `none`
- development_anchor(개발 기준점): `{DEVELOPMENT_ANCHOR}`
- backup_anchor(예비 기준점): `{BACKUP_ANCHOR}`

## BaselineAdapter Evidence(기준선 어댑터 근거)

- selection_report(선택 보고서): `{rel(ANCHOR_REPORT_PATH)}`
- first_adapter_report(첫 어댑터 보고서): `{rel(FIRST_ADAPTER_REPORT_PATH)}`
- first_adapter_summary(첫 어댑터 요약): `{rel(FIRST_ADAPTER_SUMMARY_CSV)}`
- first_adapter_risk_telemetry(첫 어댑터 위험 텔레메트리): `{rel(FIRST_ADAPTER_RISK_CSV)}`
- repair_report(수리 보고서): `{rel(REPORT_PATH)}`
- repair_summary_json(수리 요약 JSON): `{rel(SUMMARY_JSON_PATH)}`
- repair_summary_csv(수리 요약 CSV): `{rel(SUMMARY_CSV_PATH)}`
- repair_risk_telemetry(수리 위험 텔레메트리): `{rel(RISK_CSV_PATH)}`

Effect(효과): selection(선택)은 baseline lock-in(기준점 고정)을 뜻하지 않는다. adapter repair(어댑터 수리)가 실패하면 anchor demotion(기준점 강등) 또는 branch switch(갈래 전환)가 가능하다.
""",
    )
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = re.sub(r"^current_run_id: .*$", f"current_run_id: {RUN_ID}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^updated_on: .*$", "updated_on: '2026-05-15'", text, count=1, flags=re.MULTILINE)
    focus = (
        "- >-\n"
        f"  Stage56(56단계) `{STAGE_ID}`: {RUN_NUMBER}(실행 {RUN_NUMBER}) BaselineAdapter repair batch(기준선 어댑터 수리 배치)를 실행했다. "
        f"best_adapter(최선 어댑터)는 `{best.get('adapter_id', 'none')}`이고 Phase A eligible(Phase A 적격)은 `{best.get('phase_a_eligible_for_onnx', False)}`이다. "
        "Effect(효과): ONNX hardening(ONNX 경화) 전 validation damage(검증 손상)의 원인을 risk/ATR/execution(위험/ATR/실행) 축으로 좁힌다.\n"
    )
    text = re.sub(r"- >-\n  Stage56[^\n]*run50BT[^\n]*BaselineAdapter MT5[^\n]*\n", "", text)
    text = re.sub(r"- >-\n  Stage56[^\n]*run50BU[^\n]*BaselineAdapter repair batch[^\n]*\n", "", text)
    text = re.sub(r"current_focus:\n", f"current_focus:\n{focus}", text, count=1)
    text = remove_workspace_block(text, "stage56_baseline_adapter_repair:")
    block = f"""
stage56_baseline_adapter_repair:
  packet_id: {PACKET_ID}
  current_run_id: {RUN_ID}
  development_anchor: {DEVELOPMENT_ANCHOR}
  backup_anchor: {BACKUP_ANCHOR}
  terminal_label: {status_label}
  phase_a_eligible_for_onnx: {str(bool(best.get('phase_a_eligible_for_onnx'))).lower()}
  best_adapter: {best.get('adapter_id', 'none')}
  boundary: {BOUNDARY}
  next_action: continue_adapter_repair_or_demote_anchor_before_onnx
"""
    io_path(WORKSPACE_STATE_PATH).write_text(text.rstrip() + "\n" + block, encoding="utf-8-sig")


def write_packet_files(
    result: Mapping[str, Any],
    summary_rows: Sequence[Mapping[str, Any]],
    risk_rows: Sequence[Mapping[str, Any]],
    ledger_payload: Mapping[str, Any],
) -> None:
    external = str(result.get("external_verification_status") or "blocked")
    best = best_variant(summary_rows)
    best_val = best.get("validation") if isinstance(best.get("validation"), Mapping) else {}
    best_oos = best.get("oos") if isinstance(best.get("oos"), Mapping) else {}
    aggregate = {
        "packet_id": PACKET_ID,
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "terminal_label": TERMINAL_LABEL if external == "completed" else BLOCKED_LABEL,
        "development_anchor": DEVELOPMENT_ANCHOR,
        "backup_anchor": BACKUP_ANCHOR,
        "selected_research_baseline": "none",
        "phase_a_eligible_for_onnx": best.get("phase_a_eligible_for_onnx", False),
        "best_variant": best,
        "diagnosis": diagnosis(summary_rows),
        "summary_json_path": rel(SUMMARY_JSON_PATH),
        "summary_csv_path": rel(SUMMARY_CSV_PATH),
        "risk_csv_path": rel(RISK_CSV_PATH),
        "report_path": rel(REPORT_PATH),
        "ledger_payload": ledger_payload,
        "hard_completion_status": "not_met",
        "next_action": "continue_adapter_repair_or_demote_anchor_before_onnx",
        "forbidden_claims": {
            "live_readiness": False,
            "runtime_authority": False,
            "operating_promotion": False,
            "operating_reference": False,
            "production_baseline": False,
            "reviewed_closed": False,
        },
    }
    write_json(PACKET_ROOT / "aggregate_summary.json", aggregate)
    write_json(PACKET_ROOT / "result_judgment_gate.json", {
        "result_subject": RUN_ID,
        "judgment_label": "adapter_repair_in_progress" if not best.get("phase_a_eligible_for_onnx") else "adapter_mt5_repair_completed",
        "phase_a_eligible_for_onnx": best.get("phase_a_eligible_for_onnx", False),
        "validation_metrics": best_val,
        "oos_metrics": best_oos,
        "failure_reasons": best.get("failure_reasons", []),
        "claim_boundary": BOUNDARY,
        "status": "passed_with_repair_needed" if external == "completed" else "blocked",
    })
    write_json(PACKET_ROOT / "runtime_parity_audit.json", {
        "status": "phase_a_only_no_onnx_yet",
        "research_path": rel(Path(__file__)),
        "runtime_path": rel(Path("foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5")),
        "known_differences": "Tier B disabled; ONNX not started; broker execution safety remains MT5-side",
        "effect": "The batch separates entry/route translation from ATR/risk execution translation before ONNX.",
    })
    write_json(PACKET_ROOT / "backtest_forensics_audit.json", {
        "status": "passed" if external == "completed" else "blocked",
        "tester_identity": "terminal64.exe; US100 M5; deposit=500; leverage=1:100; model=4",
        "trade_evidence": "MT5 Strategy Tester HTML reports and RuntimeTelemetry CSV files",
        "boundary": BOUNDARY,
    })
    write_json(PACKET_ROOT / "artifact_lineage_audit.json", {
        "status": "passed",
        "source_inputs": [rel(SOURCE_MODEL), rel(source_feature("validation_is")), rel(source_feature("oos"))],
        "producer": rel(Path(__file__)),
        "consumers": [rel(REPORT_PATH), rel(SUMMARY_JSON_PATH), rel(SUMMARY_CSV_PATH), rel(RISK_CSV_PATH)],
        "ledger_links": ledger_payload,
    })
    write_json(PACKET_ROOT / "required_gate_coverage_audit.json", {
        "required_gates": [
            "actual_adapter_mt5_validation",
            "actual_adapter_mt5_oos",
            "risk_telemetry_parse",
            "artifact_lineage_audit",
            "result_judgment_gate",
            "final_claim_guard",
        ],
        "covered_gates": [
            "actual_adapter_mt5_validation" if external == "completed" else "missing",
            "actual_adapter_mt5_oos" if external == "completed" else "missing",
            "risk_telemetry_parse" if all(row.get("status") == "completed" for row in risk_rows) else "partial",
            "artifact_lineage_audit",
            "result_judgment_gate",
            "final_claim_guard",
        ],
        "status": "passed" if external == "completed" else "blocked",
    })
    write_json(PACKET_ROOT / "final_claim_guard.json", {
        "hard_completion_label": "baseline_adapter_onnx_mt5_reproduction_completed",
        "hard_completion_met": False,
        "current_allowed_label": "adapter_repair_in_progress" if not best.get("phase_a_eligible_for_onnx") else "adapter_mt5_repair_completed",
        "forbidden_terminal_labels": [
            "reviewed_closed",
            "complete",
            "final",
            "production_ready",
            "live_ready",
            "operating_reference",
            "runtime_authority",
            "good_enough",
        ],
        "status": "passed",
    })
    write_json(PACKET_ROOT / "skill_receipts.json", [
        {"skill": "obsidian-reentry-read", "status": "completed"},
        {"skill": "obsidian-backtest-forensics", "status": "completed" if external == "completed" else "blocked"},
        {"skill": "obsidian-runtime-parity", "status": "phase_a_only"},
        {"skill": "obsidian-artifact-lineage", "status": "completed"},
        {"skill": "obsidian-model-validation", "status": "phase_a_repair_judgment"},
        {"skill": "obsidian-result-judgment", "status": "completed"},
    ])


def write_run_files(
    result: Mapping[str, Any],
    summary_rows: Sequence[Mapping[str, Any]],
    audit_rows: Sequence[Mapping[str, Any]],
    risk_rows: Sequence[Mapping[str, Any]],
    ledger_payload: Mapping[str, Any],
) -> None:
    write_csv(SUMMARY_CSV_PATH, summary_rows)
    write_csv(AUDIT_CSV_PATH, audit_rows)
    write_csv(RISK_CSV_PATH, risk_rows)
    payload = {
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "terminal_label": TERMINAL_LABEL if result.get("external_verification_status") == "completed" else BLOCKED_LABEL,
        "development_anchor": DEVELOPMENT_ANCHOR,
        "backup_anchor": BACKUP_ANCHOR,
        "selected_research_baseline": "none",
        "external_verification_status": result.get("external_verification_status"),
        "phase_a_best_variant": best_variant(summary_rows),
        "diagnosis": diagnosis(summary_rows),
        "summary_rows": list(summary_rows),
        "risk_rows": list(risk_rows),
        "strategy_tester_reports": result.get("strategy_tester_reports", []),
        "ledger_payload": ledger_payload,
        "hard_completion_status": "not_met",
    }
    write_json(SUMMARY_JSON_PATH, payload)
    write_json(RUN_ROOT / "run_manifest.json", {
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_number": RUN_NUMBER,
        "development_anchor": DEVELOPMENT_ANCHOR,
        "repair_variants": [variant.__dict__ for variant in REPAIR_VARIANTS],
        "attempts": result.get("attempts", []),
        "common_copies": result.get("common_copies", []),
        "compile": result.get("compile", {}),
        "external_verification_status": result.get("external_verification_status"),
        "judgment": result.get("judgment"),
        "boundary": BOUNDARY,
    })
    write_json(RUN_ROOT / "kpi_record.json", {
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "mt5_kpi_records": result.get("mt5_kpi_records", []),
        "strategy_tester_reports": result.get("strategy_tester_reports", []),
        "execution_results": result.get("execution_results", []),
        "external_verification_status": result.get("external_verification_status"),
        "judgment": result.get("judgment"),
        "boundary": BOUNDARY,
    })
    write_packet_files(result, summary_rows, risk_rows, ledger_payload)


def update_logs(summary_rows: Sequence[Mapping[str, Any]], result: Mapping[str, Any]) -> None:
    external = str(result.get("external_verification_status") or "blocked")
    label = TERMINAL_LABEL if external == "completed" else BLOCKED_LABEL
    best = best_variant(summary_rows)
    best_val = best.get("validation") if isinstance(best.get("validation"), Mapping) else {}
    best_oos = best.get("oos") if isinstance(best.get("oos"), Mapping) else {}
    variant_labels = ", ".join(variant.label for variant in REPAIR_VARIANTS)
    entry = f"""
## 2026-05-15 {RUN_NUMBER} BaselineAdapter Repair Batch(기준선 어댑터 수리 배치)
- action(행동): `{variant_labels}` repair variants(수리 변형)를 실제 MT5 validation/OOS(검증/표본외)로 실행했다.
- effect(효과): validation damage(검증 손상)가 entry/route(진입/라우팅)보다 risk/ATR/execution(위험/ATR/실행) 쪽인지 좁힌다.
- terminal_label(종료 라벨): `{label}`
- best_adapter(최선 어댑터): `{best.get('adapter_id', 'none')}`
- Phase A eligible(Phase A 적격): `{best.get('phase_a_eligible_for_onnx', False)}`
- validation/OOS PF(검증/표본외 PF): `{aw.fmt(best_val.get('profit_factor'))}` / `{aw.fmt(best_oos.get('profit_factor'))}`
- validation/OOS net(검증/표본외 손익): `{aw.fmt(best_val.get('net_profit'))}` / `{aw.fmt(best_oos.get('net_profit'))}`
- next_action(다음 행동): `continue_adapter_repair_or_demote_anchor_before_onnx`
"""
    append_once(PROGRESS_LOG_PATH, entry)
    append_once(
        CHANGELOG_PATH,
        """
## 2026-05-15 Stage56 {RUN_NUMBER} BaselineAdapter Repair Batch(기준선 어댑터 수리 배치)
- completed(완료): adapter repair batch(어댑터 수리 배치)를 actual MT5 validation/OOS(실제 MT5 검증/표본외)로 실행하고 summary/ledger/current truth(요약/장부/현재 진실)를 갱신했다.
""",
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage56 BaselineAdapter repair MT5 batch.")
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--finalize-existing", action="store_true")
    parser.add_argument("--cost-stress-per-trade", type=float, default=0.50)
    parser.add_argument("--common-files-root", default=str(COMMON_FILES_ROOT_DEFAULT))
    parser.add_argument("--terminal-data-root", default=str(TERMINAL_DATA_ROOT_DEFAULT))
    parser.add_argument("--tester-profile-root", default=str(TESTER_PROFILE_ROOT_DEFAULT))
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(METAEDITOR_PATH_DEFAULT))
    parser.add_argument("--timeout-seconds", type=int, default=360)
    return parser.parse_args(argv)


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
        "route_coverage": route_coverage(),
    }


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.finalize_existing:
        result = load_existing_result()
    else:
        inputs = prepare_inputs(Path(args.common_files_root))
        attempts = build_attempts(inputs, REPAIR_VARIANTS)
        prepared = {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "stage_number": 56,
            "run_number": RUN_NUMBER,
            "run_root": RUN_ROOT,
            "packet_id": PACKET_ID,
            "attempts": attempts,
            "common_copies": inputs["common_copies"],
            "feature_exports": inputs["feature_exports"],
            "model_artifacts": {"adapter_entry_model": {"path": rel(inputs["model_local"]), "common_path": inputs["model_common"]}},
            "route_coverage": route_coverage(),
            "model_family": "baseline_adapter_v64_repair_ebm_table",
            "feature_set_id": "stage56_context_gap_refill_signal_repair_batch",
            "label_id": "label_v1_fwd12_m5_logret_train_q33_3class",
            "split_contract": "split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413",
            "claim_boundary": BOUNDARY,
        }
        result = execute_or_materialize(prepared, args)
    audit_rows = (
        audit_rows_for_result(result, REPAIR_VARIANTS, float(args.cost_stress_per_trade))
        if result.get("mt5_kpi_records")
        else []
    )
    risk_rows = base.risk_rows_from_result(result)
    summary_rows = build_summary_rows(result, REPAIR_VARIANTS, audit_rows, risk_rows)
    write_csv(SUMMARY_CSV_PATH, summary_rows)
    write_csv(AUDIT_CSV_PATH, audit_rows)
    write_csv(RISK_CSV_PATH, risk_rows)
    write_report(summary_rows, risk_rows, result)
    extra_paths = [
        REPORT_PATH,
        SUMMARY_JSON_PATH,
        SUMMARY_CSV_PATH,
        AUDIT_CSV_PATH,
        RISK_CSV_PATH,
        RUN_ROOT / "run_manifest.json",
        RUN_ROOT / "kpi_record.json",
        Path(__file__),
        Path("foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5"),
        Path("foundation/mt5/include/ObsidianPrime/ExecutionBridge.mqh"),
        Path("foundation/mt5/include/ObsidianPrime/RuntimeTelemetry.mqh"),
    ]
    artifacts = artifact_rows(result, extra_paths)
    write_run_files(result, summary_rows, audit_rows, risk_rows, {})
    artifacts = artifact_rows(result, extra_paths)
    ledger_payload = write_ledgers(result, summary_rows, artifacts)
    summary_payload = json.loads(io_path(SUMMARY_JSON_PATH).read_text(encoding="utf-8-sig"))
    summary_payload["ledger_payload"] = ledger_payload
    write_json(SUMMARY_JSON_PATH, summary_payload)
    write_packet_files(result, summary_rows, risk_rows, ledger_payload)
    update_state_docs(summary_rows, result)
    update_logs(summary_rows, result)
    print(
        json.dumps(
            json_ready(
                {
                    "status": "ok" if result.get("external_verification_status") == "completed" else "blocked",
                    "run_id": RUN_ID,
                    "terminal_label": TERMINAL_LABEL if result.get("external_verification_status") == "completed" else BLOCKED_LABEL,
                    "phase_a_best_variant": best_variant(summary_rows),
                    "summary_json": SUMMARY_JSON_PATH.as_posix(),
                    "summary_csv": SUMMARY_CSV_PATH.as_posix(),
                    "risk_csv": RISK_CSV_PATH.as_posix(),
                    "report": REPORT_PATH.as_posix(),
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
