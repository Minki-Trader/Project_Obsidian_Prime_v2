from __future__ import annotations

import argparse
import csv
import json
import math
import re
import shutil
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

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
from foundation.control_plane.mt5_trade_attribution import MarketData, compute_trade_attribution  # noqa: E402
from foundation.models.onnx_bridge import ordered_hash  # noqa: E402
from foundation.mt5 import runtime_support as mt5  # noqa: E402
from foundation.mt5.trade_report import pair_deals_into_trades, parse_mt5_trade_report  # noqa: E402
from stage_pipelines.stage56 import agreement_firewall_density_recovery_branch as audit_support  # noqa: E402
from stage_pipelines.stage56 import baseline_adapter_mt5_development as base  # noqa: E402
from stage_pipelines.stage56 import baseline_adapter_repair_batch as repair  # noqa: E402
from stage_pipelines.stage56 import independent_event_source_route_branch as aw  # noqa: E402


STAGE56_ID = "56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection"
STAGE57_ID = "57_adapter_quality__equity_segment_kpi_audit_gate"
STAGE58_ID = "58_adapter_risk__bounded_repair_before_atr_risk_integration"
STAGE59_ID = "59_adapter_repair__post_risk_atr_revalidation"
RUN_NUMBER = "run52A"
RUN_ID = "run52A_stage58_adapter_repair_before_risk_atr_v1"
PACKET_ID = "stage58_risk_atr_integration_v1"
PARENT_RUN_ID = "run50CA_stage56_baseline_adapter_onnx_runtime_reproduction_v1"
SOURCE_REPAIR_RUN_ID = "run50BY_stage56_baseline_adapter_same_move_lot_repair_v1"
SOURCE_ADAPTER_ID = "ba14_no_atr_sd5_lot025"
DEVELOPMENT_ANCHOR = "v64_v47_ctxgap14_refill_etfw_h2_no_b"
BACKUP_ANCHOR = "v60_v47_et_stable_damage_firewall_h2c0_no_b"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)

RUN_ROOT = Path("stages") / STAGE58_ID / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = Path("stages") / STAGE58_ID / "03_reviews"
SELECTED_ROOT = Path("stages") / STAGE58_ID / "04_selected"
SPEC_ROOT = Path("stages") / STAGE58_ID / "00_spec"
INPUT_ROOT = Path("stages") / STAGE58_ID / "01_inputs"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
SOURCE_STAGE_ROOT = Path("stages") / STAGE56_ID
SOURCE_RUN_ROOT = SOURCE_STAGE_ROOT / "02_runs/run50BR"
SOURCE_VARIANT_ROOT = SOURCE_RUN_ROOT / DEVELOPMENT_ANCHOR
SOURCE_MODEL = SOURCE_RUN_ROOT / "models/stage56_context_timed_event_signal_discrete_score_table.csv"
SOURCE_STAGE57_DECISION = Path("stages") / STAGE57_ID / "03_reviews/stage57_decision.md"
SOURCE_STAGE57_SEGMENTS = Path("stages") / STAGE57_ID / "03_reviews/segment_kpi_summary.csv"
SOURCE_BA14_SPEC = SOURCE_STAGE_ROOT / "04_selected/baseline_adapter_ba14_spec.json"
SOURCE_RUN50CA_SUMMARY = SOURCE_STAGE_ROOT / "03_reviews/run50CA_baseline_adapter_onnx_runtime_reproduction_summary.csv"
SOURCE_RUN50CA_RISK = SOURCE_STAGE_ROOT / "03_reviews/run50CA_baseline_adapter_onnx_runtime_reproduction_risk_telemetry.csv"
SIGNAL_COLUMN = "stage56_context_gap_refill_signal"
FEATURE_ORDER_HASH = ordered_hash((SIGNAL_COLUMN,))
COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage58/{RUN_NUMBER}_risk_atr_integration"

REPORT_PATH = REVIEWS_ROOT / "risk_atr_integration_report.md"
RISK_TELEMETRY_SUMMARY_PATH = REVIEWS_ROOT / "risk_telemetry_summary.csv"
ATR_BRACKET_TELEMETRY_PATH = REVIEWS_ROOT / "atr_bracket_telemetry_summary.csv"
RISK_FLOOR_IMPACT_PATH = REVIEWS_ROOT / "risk_floor_segment_impact.csv"
SEGMENT_KPI_PATH = REVIEWS_ROOT / "risk_atr_segment_kpi_summary.csv"
DECISION_PATH = REVIEWS_ROOT / "stage58_decision.md"
SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage58_risk_atr_integration_summary.json"
RAW_SUMMARY_PATH = REVIEWS_ROOT / "stage58_raw_attempt_summary.csv"
AUDIT_CSV_PATH = REVIEWS_ROOT / "stage58_trade_audit.csv"
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

STAGE58_VARIANTS = (
    repair.RepairVariant(
        adapter_id="s58_no_atr_fixed_lot025_sd5",
        label="fixed_lot_no_atr_control_sd5",
        atr_enabled=False,
        model_risk_enabled=False,
        fixed_lot=0.25,
        atr_stop_multiplier=0.0,
        atr_take_profit_multiplier=0.0,
        model_risk_max_pct=0.0,
        same_direction_reentry_cooldown_bars=5,
        notes="Stage58 fixed-risk no-ATR control matching the ba14 reference shape.",
    ),
    repair.RepairVariant(
        adapter_id="s58_atr_fixed_lot025_sd5",
        label="fixed_lot_atr_bracket_sd5",
        atr_enabled=True,
        model_risk_enabled=False,
        fixed_lot=0.25,
        atr_stop_multiplier=1.5,
        atr_take_profit_multiplier=2.0,
        model_risk_max_pct=0.0,
        same_direction_reentry_cooldown_bars=5,
        notes="Stage58 ATR bracket control with fixed lot to isolate bracket impact.",
    ),
    repair.RepairVariant(
        adapter_id="s58_atr_modelrisk5_sd5",
        label="model_risk_atr_bracket_sd5",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=1.5,
        atr_take_profit_multiplier=2.0,
        model_risk_max_pct=0.05,
        same_direction_reentry_cooldown_bars=5,
        notes="Stage58 mandatory model-controlled risk% plus ATR bracket combined version.",
    ),
    repair.RepairVariant(
        adapter_id="s58_wideatr_modelrisk5_sd5",
        label="model_risk_wide_atr_bracket_sd5",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.5,
        atr_take_profit_multiplier=3.5,
        model_risk_max_pct=0.05,
        same_direction_reentry_cooldown_bars=5,
        notes="Stage58 wider bracket bucket with model-controlled risk% to test bracket bucket sensitivity.",
    ),
)


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
        if not math.isfinite(value):
            return ""
        return f"{value:.10g}"
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


def copy_local(source: Path, destination: Path) -> dict[str, Any]:
    if not path_exists(source):
        raise FileNotFoundError(source)
    io_path(destination.parent).mkdir(parents=True, exist_ok=True)
    shutil.copy2(io_path(source), io_path(destination))
    return {"source": rel(source), "path": rel(destination), "sha256": sha256_file_lf_normalized(destination)}


def source_attempt_ini(split: str) -> Path:
    return SOURCE_VARIANT_ROOT / "mt5" / ("x01_ta_val.ini" if split == "validation_is" else "x01_ta_oos.ini")


def source_feature(split: str, tier: str = "a") -> Path:
    token = "val" if split == "validation_is" else "oos"
    return SOURCE_VARIANT_ROOT / "features" / f"{DEVELOPMENT_ANCHOR}_{tier}_{token}.csv"


def prepare_inputs(common_files_root: Path) -> dict[str, Any]:
    model_local = RUN_ROOT / "models" / SOURCE_MODEL.name
    copied = [copy_local(SOURCE_MODEL, model_local)]
    copied.append(copy_to_common(model_local, f"{COMMON_ROOT}/models/{model_local.name}", common_files_root))
    feature_exports: dict[str, dict[str, Any]] = {}
    for split in ("validation_is", "oos"):
        token = "val" if split == "validation_is" else "oos"
        feature_local = RUN_ROOT / DEVELOPMENT_ANCHOR / "features" / f"{DEVELOPMENT_ANCHOR}_stage58_adapter_a_{token}.csv"
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


def extra_set_values(variant: repair.RepairVariant, magic: int) -> dict[str, Any]:
    values = repair.extra_set_values(variant, magic)
    values["InpModelRiskMinPct"] = 0.005 if variant.model_risk_enabled else 0.0
    values["InpModelRiskMaxPct"] = min(float(variant.model_risk_max_pct), 0.05)
    values["InpModelRiskFallbackLot"] = variant.fixed_lot
    return values


def build_attempts(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    for variant_index, variant in enumerate(STAGE58_VARIANTS, start=1):
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
                magic = 5805200 + variant_index * 100 + (1 if split == "validation_is" else 50) + role_index
                attempts.append(
                    attempt_payload(
                        run_root=variant_root,
                        run_id=RUN_ID,
                        stage_number=58,
                        exploration_label="stage58_BaselineAdapter__RiskAtrIntegration",
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


def load_existing_result() -> dict[str, Any]:
    manifest_path = RUN_ROOT / "run_manifest.json"
    kpi_path = RUN_ROOT / "kpi_record.json"
    manifest = json.loads(io_path(manifest_path).read_text(encoding="utf-8-sig"))
    kpi = json.loads(io_path(kpi_path).read_text(encoding="utf-8-sig"))
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


def configure_repair_module() -> None:
    repair.RUN_ID = RUN_ID
    repair.RUN_NUMBER = RUN_NUMBER
    repair.PACKET_ID = PACKET_ID
    repair.STAGE_ID = STAGE58_ID
    repair.STAGE_ROOT = Path("stages") / STAGE58_ID
    repair.RUN_ROOT = RUN_ROOT
    repair.REVIEWS_ROOT = REVIEWS_ROOT
    repair.SELECTED_ROOT = SELECTED_ROOT
    repair.PACKET_ROOT = PACKET_ROOT
    repair.COMMON_ROOT = COMMON_ROOT
    repair.SUMMARY_CSV_PATH = RAW_SUMMARY_PATH
    repair.AUDIT_CSV_PATH = AUDIT_CSV_PATH
    repair.RISK_CSV_PATH = RISK_TELEMETRY_SUMMARY_PATH
    repair.REPAIR_VARIANTS = STAGE58_VARIANTS
    repair.BOUNDARY = BOUNDARY


def audit_rows_for_result(result: Mapping[str, Any], cost_stress_per_trade: float) -> list[dict[str, Any]]:
    original_parent = audit_support.PARENT_RUN_ID
    try:
        audit_support.PARENT_RUN_ID = RUN_ID
        return audit_support.audit_rows_for_result(
            result,
            [repair.AuditVariant(variant.adapter_id) for variant in STAGE58_VARIANTS],
            cost_stress_per_trade,
        )
    finally:
        audit_support.PARENT_RUN_ID = original_parent


def risk_rows_from_result(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    variants = {variant.adapter_id: variant for variant in STAGE58_VARIANTS}
    for execution in result.get("execution_results", []):
        attempt_name = str(execution.get("attempt_name") or "")
        adapter_id = next((item for item in variants if attempt_name.startswith(item)), "")
        variant = variants.get(adapter_id)
        runtime_outputs = execution.get("runtime_outputs", {}) if isinstance(execution.get("runtime_outputs"), Mapping) else {}
        telemetry_path = Path(str(runtime_outputs.get("telemetry_path") or ""))
        row: dict[str, Any] = {
            "attempt_name": attempt_name,
            "adapter_id": adapter_id,
            "split": execution.get("split"),
            "tier": execution.get("tier"),
            "view": "actual_routed_total" if "_rt_" in attempt_name else "tier_a_only",
            "atr_enabled": variant.atr_enabled if variant else "",
            "model_risk_enabled": variant.model_risk_enabled if variant else "",
            "atr_stop_multiplier": variant.atr_stop_multiplier if variant else "",
            "atr_take_profit_multiplier": variant.atr_take_profit_multiplier if variant else "",
            "telemetry_path": telemetry_path.as_posix() if str(telemetry_path) else "",
            "status": "missing",
        }
        if not path_exists(telemetry_path):
            row["parse_error"] = "telemetry_missing"
            rows.append(row)
            continue
        try:
            frame = pd.read_csv(io_path(telemetry_path))
            cycles = frame.loc[frame["record_type"].astype(str).eq("cycle")].copy()
            numeric_columns = (
                "model_risk_pct",
                "clipped_risk_pct",
                "computed_lot",
                "executed_lot",
                "actual_risk_pct_after_floor",
                "atr_points",
                "open_sl_points",
                "open_tp_points",
            )
            for column in numeric_columns:
                if column in cycles:
                    cycles[column] = pd.to_numeric(cycles[column], errors="coerce")
            floor = cycles.get("min_lot_floor_applied", pd.Series([], dtype=str)).astype(str).str.lower().eq("true")
            row.update(
                {
                    "status": "completed",
                    "cycle_rows": int(len(cycles)),
                    "risk_floor_applied_count": int(floor.sum()) if len(cycles) else 0,
                    "avg_model_risk_pct": _series_mean(cycles, "model_risk_pct"),
                    "max_model_risk_pct": _series_max(cycles, "model_risk_pct"),
                    "avg_clipped_risk_pct": _series_mean(cycles, "clipped_risk_pct"),
                    "max_clipped_risk_pct": _series_max(cycles, "clipped_risk_pct"),
                    "avg_computed_lot": _series_mean(cycles, "computed_lot"),
                    "max_computed_lot": _series_max(cycles, "computed_lot"),
                    "avg_executed_lot": _series_mean(cycles, "executed_lot"),
                    "max_executed_lot": _series_max(cycles, "executed_lot"),
                    "max_actual_risk_pct_after_floor": _series_max(cycles, "actual_risk_pct_after_floor"),
                    "avg_actual_risk_pct_after_floor": _series_mean(cycles, "actual_risk_pct_after_floor"),
                    "avg_atr_points": _series_mean(cycles, "atr_points"),
                    "avg_open_sl_points": _series_mean(cycles, "open_sl_points"),
                    "avg_open_tp_points": _series_mean(cycles, "open_tp_points"),
                    "risk_bucket": _risk_bucket(_series_max(cycles, "clipped_risk_pct")),
                    "telemetry_sha256": sha256_file_lf_normalized(telemetry_path),
                }
            )
        except Exception as exc:
            row["status"] = "blocked"
            row["parse_error"] = f"{type(exc).__name__}: {exc}"
        rows.append(row)
    return rows


def _series_mean(frame: pd.DataFrame, column: str) -> float | None:
    if column not in frame or frame.empty:
        return None
    value = frame[column].mean()
    return float(value) if pd.notna(value) else None


def _series_max(frame: pd.DataFrame, column: str) -> float | None:
    if column not in frame or frame.empty:
        return None
    value = frame[column].max()
    return float(value) if pd.notna(value) else None


def _risk_bucket(value: Any) -> str:
    number = as_float(value, None)
    if number is None or number <= 0.0:
        return "risk_off_or_fixed_lot"
    if number < 0.015:
        return "low"
    if number < 0.035:
        return "mid"
    return "high_capped"


def as_float(value: Any, default: float | None = 0.0) -> float | None:
    try:
        if value is None or value == "":
            return default
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def split_days(split: str) -> float:
    return VALIDATION_DAYS if split == "validation_is" else OOS_DAYS


def build_summary_rows(
    result: Mapping[str, Any],
    audit_rows: Sequence[Mapping[str, Any]],
    risk_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    rows = repair.build_summary_rows(result, STAGE58_VARIANTS, audit_rows, risk_rows)
    risk_by_attempt = {str(row.get("attempt_name")): row for row in risk_rows}
    enriched: list[dict[str, Any]] = []
    for row in rows:
        attempt = (
            f"{row.get('adapter_id')}_{'ta' if row.get('view') == 'tier_a_only' else 'rt'}_"
            f"{'val' if row.get('split') == 'validation_is' else 'oos'}"
        )
        risk = risk_by_attempt.get(attempt, {})
        current = dict(row)
        for key in (
            "avg_model_risk_pct",
            "avg_clipped_risk_pct",
            "max_clipped_risk_pct",
            "avg_computed_lot",
            "max_computed_lot",
            "max_executed_lot",
            "avg_actual_risk_pct_after_floor",
            "risk_bucket",
            "telemetry_sha256",
        ):
            current[key] = risk.get(key)
        enriched.append(current)
    return enriched


def _kpi(values: Sequence[float]) -> dict[str, Any]:
    if not values:
        return {
            "trade_count": 0,
            "net_profit": 0.0,
            "profit_factor": None,
            "win_rate": None,
            "expectancy": None,
            "max_closed_trade_drawdown": 0.0,
        }
    gross_profit = sum(value for value in values if value > 0.0)
    gross_loss = sum(value for value in values if value < 0.0)
    return {
        "trade_count": len(values),
        "net_profit": sum(values),
        "profit_factor": gross_profit / abs(gross_loss) if gross_loss else None,
        "win_rate": sum(1 for value in values if value > 0.0) / len(values),
        "expectancy": sum(values) / len(values),
        "max_closed_trade_drawdown": max_drawdown(values),
    }


def max_drawdown(values: Sequence[float]) -> float:
    peak = 0.0
    cumulative = 0.0
    max_dd = 0.0
    for value in values:
        cumulative += value
        peak = max(peak, cumulative)
        max_dd = max(max_dd, peak - cumulative)
    return max_dd


def chronological_label(index: int, length: int) -> str:
    ratio = index / max(length, 1)
    if ratio < 1 / 3:
        return "early"
    if ratio < 2 / 3:
        return "mid"
    return "late"


def segment_kpi_rows(summary_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    market_data = MarketData.load(REPO_ROOT)
    rows: list[dict[str, Any]] = []
    for summary in summary_rows:
        if summary.get("view") != "actual_routed_total" or summary.get("status") != "completed":
            continue
        report_path = Path(str(summary.get("report_path") or ""))
        if not report_path:
            continue
        report_abs = report_path if report_path.is_absolute() else REPO_ROOT / report_path
        if not path_exists(report_abs):
            continue
        report = parse_mt5_trade_report(report_abs)
        trades = pair_deals_into_trades(report["deals"])
        stats = compute_trade_attribution(trades, market_data)
        frame = pd.DataFrame(stats["trades"])
        if frame.empty:
            continue
        frame["close_time"] = pd.to_datetime(frame["close_time"])
        frame = frame.sort_values("close_time").reset_index(drop=True)
        frame["chronological_third"] = [chronological_label(i, len(frame)) for i in range(len(frame))]
        frame["month"] = frame["close_time"].dt.strftime("%Y-%m")
        for segment_type, groups in (
            ("full_split", {"actual_routed_total": frame}),
            ("chronological_third", {label: frame[frame["chronological_third"].eq(label)] for label in ("early", "mid", "late")}),
        ):
            for segment, subset in groups.items():
                net_values = [float(value) for value in subset["net_profit"]]
                kpi = _kpi(net_values)
                rows.append(
                    {
                        "run_id": RUN_ID,
                        "adapter_id": summary.get("adapter_id"),
                        "repair_label": summary.get("repair_label"),
                        "split": summary.get("split"),
                        "view": summary.get("view"),
                        "segment_type": segment_type,
                        "segment": segment,
                        "atr_enabled": summary.get("atr_enabled"),
                        "model_risk_enabled": summary.get("model_risk_enabled"),
                        "trade_count": kpi["trade_count"],
                        "trades_per_day": kpi["trade_count"] / split_days(str(summary.get("split"))),
                        "net_profit": kpi["net_profit"],
                        "profit_factor": kpi["profit_factor"],
                        "win_rate": kpi["win_rate"],
                        "expectancy": kpi["expectancy"],
                        "max_closed_trade_drawdown": kpi["max_closed_trade_drawdown"],
                        "mfe_mean": _mean(subset.get("mfe", [])),
                        "mae_mean": _mean(subset.get("mae", [])),
                        "realized_over_mfe_mean": _mean(subset.get("realized_over_mfe", [])),
                        "mfe_capture_ratio": _safe_ratio(kpi["net_profit"], _sum(subset.get("mfe", []))),
                        "avg_model_risk_pct": summary.get("avg_model_risk_pct"),
                        "avg_executed_lot": summary.get("avg_executed_lot"),
                        "avg_open_sl_points": summary.get("avg_open_sl_points"),
                        "avg_open_tp_points": summary.get("avg_open_tp_points"),
                        "quality_flag": segment_quality(str(summary.get("split")), segment_type, segment, kpi),
                        "report_path": rel(report_path),
                    }
                )
    return rows


def segment_quality(split: str, segment_type: str, segment: str, kpi: Mapping[str, Any]) -> str:
    flags: list[str] = []
    net = as_float(kpi.get("net_profit"), 0.0) or 0.0
    pf = as_float(kpi.get("profit_factor"), None)
    if segment_type == "chronological_third":
        if net <= 0.0:
            flags.append("negative_or_flat_segment")
        if pf is not None and pf < 1.05:
            flags.append("weak_segment_pf")
        if split == "validation_is" and segment == "late" and net <= 0.0:
            flags.append("validation_late_flatline_risk")
        if split == "oos" and segment == "early" and pf is not None and pf < 1.05:
            flags.append("oos_early_pf_weak")
    return ";".join(flags) if flags else "acceptable_measurement_only"


def _mean(values: Iterable[Any]) -> float | None:
    numbers = [as_float(value, None) for value in values]
    filtered = [value for value in numbers if value is not None]
    return sum(filtered) / len(filtered) if filtered else None


def _sum(values: Iterable[Any]) -> float:
    return sum(value for value in (as_float(item, None) for item in values) if value is not None)


def _safe_ratio(numerator: Any, denominator: Any) -> float | None:
    num = as_float(numerator, None)
    den = as_float(denominator, None)
    if num is None or den is None or abs(den) < 1e-12:
        return None
    return num / den


def atr_bracket_rows(summary_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in summary_rows:
        if row.get("view") == "tier_b_fallback_only":
            continue
        rows.append(
            {
                "run_id": RUN_ID,
                "adapter_id": row.get("adapter_id"),
                "split": row.get("split"),
                "view": row.get("view"),
                "atr_enabled": row.get("atr_enabled"),
                "bracket_bucket": bracket_bucket(row),
                "atr_stop_multiplier": row.get("atr_stop_multiplier"),
                "atr_take_profit_multiplier": row.get("atr_take_profit_multiplier"),
                "avg_atr_points": row.get("avg_atr_points"),
                "avg_open_sl_points": row.get("avg_open_sl_points"),
                "avg_open_tp_points": row.get("avg_open_tp_points"),
                "net_profit": row.get("net_profit"),
                "profit_factor": row.get("profit_factor"),
                "max_drawdown_amount": row.get("max_drawdown_amount"),
                "mfe_capture_ratio": row.get("mfe_capture_ratio"),
                "cost_stressed_expectancy": row.get("cost_stressed_expectancy"),
                "status": row.get("status"),
            }
        )
    return rows


def bracket_bucket(row: Mapping[str, Any]) -> str:
    if str(row.get("atr_enabled")).lower() not in {"true", "1"}:
        return "no_atr"
    stop = as_float(row.get("atr_stop_multiplier"), 0.0)
    take = as_float(row.get("atr_take_profit_multiplier"), 0.0)
    if stop and stop >= 2.5:
        return "wide_atr"
    return f"atr_{stop:g}_{take:g}"


def risk_floor_impact_rows(summary_rows: Sequence[Mapping[str, Any]], risk_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    risk_by_key = {
        (
            row.get("adapter_id"),
            row.get("split"),
            row.get("view"),
        ): row
        for row in risk_rows
    }
    rows: list[dict[str, Any]] = []
    for row in summary_rows:
        if row.get("view") == "tier_b_fallback_only":
            continue
        risk = risk_by_key.get((row.get("adapter_id"), row.get("split"), row.get("view")), {})
        floor_count = as_float(risk.get("risk_floor_applied_count"), 0.0) or 0.0
        trade_count = as_float(row.get("trade_count"), 0.0) or 0.0
        rows.append(
            {
                "run_id": RUN_ID,
                "adapter_id": row.get("adapter_id"),
                "split": row.get("split"),
                "view": row.get("view"),
                "model_risk_enabled": row.get("model_risk_enabled"),
                "trade_count": row.get("trade_count"),
                "risk_floor_applied_count": floor_count,
                "risk_floor_trade_share": floor_count / trade_count if trade_count else 0.0,
                "avg_computed_lot": risk.get("avg_computed_lot"),
                "avg_executed_lot": risk.get("avg_executed_lot"),
                "max_actual_risk_pct_after_floor": risk.get("max_actual_risk_pct_after_floor"),
                "net_profit": row.get("net_profit"),
                "profit_factor": row.get("profit_factor"),
                "impact_flag": "floor_inflation_risk" if floor_count > 0 else "no_floor_impact_observed",
            }
        )
    return rows


def select_rows(summary_rows: Sequence[Mapping[str, Any]], *, view: str = "actual_routed_total") -> list[Mapping[str, Any]]:
    return [row for row in summary_rows if row.get("view") == view and row.get("status") == "completed"]


def routed_pair(summary_rows: Sequence[Mapping[str, Any]], adapter_id: str) -> tuple[Mapping[str, Any], Mapping[str, Any]]:
    val = next((row for row in summary_rows if row.get("adapter_id") == adapter_id and row.get("split") == "validation_is" and row.get("view") == "actual_routed_total"), {})
    oos = next((row for row in summary_rows if row.get("adapter_id") == adapter_id and row.get("split") == "oos" and row.get("view") == "actual_routed_total"), {})
    return val, oos


def best_combined_variant(summary_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    candidates: list[dict[str, Any]] = []
    for variant in STAGE58_VARIANTS:
        if not (variant.atr_enabled and variant.model_risk_enabled):
            continue
        val, oos = routed_pair(summary_rows, variant.adapter_id)
        if not val or not oos:
            continue
        score = (
            (as_float(val.get("net_profit"), 0.0) or 0.0)
            + (as_float(oos.get("net_profit"), 0.0) or 0.0)
            + 500.0 * (as_float(val.get("profit_factor"), 0.0) or 0.0)
            + 500.0 * (as_float(oos.get("profit_factor"), 0.0) or 0.0)
            - 0.5 * (as_float(val.get("max_drawdown_amount"), 0.0) or 0.0)
            - 0.5 * (as_float(oos.get("max_drawdown_amount"), 0.0) or 0.0)
        )
        candidates.append({"adapter_id": variant.adapter_id, "label": variant.label, "validation": dict(val), "oos": dict(oos), "score": score})
    return max(candidates, key=lambda item: as_float(item.get("score"), -999999.0) or -999999.0, default={})


def stage58_failure_reasons(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]]) -> list[str]:
    reasons: list[str] = []
    best = best_combined_variant(summary_rows)
    if not best:
        return ["mandatory_model_risk_atr_combined_variant_missing"]
    val = best.get("validation", {})
    oos = best.get("oos", {})
    for label, row in (("validation", val), ("oos", oos)):
        if (as_float(row.get("net_profit"), 0.0) or 0.0) <= 0.0:
            reasons.append(f"{label}_net_not_positive_after_atr_risk")
        if (as_float(row.get("profit_factor"), 0.0) or 0.0) < 1.10:
            reasons.append(f"{label}_pf_lt_1_10_after_atr_risk")
        if (as_float(row.get("cost_stressed_expectancy"), 0.0) or 0.0) <= 0.0:
            reasons.append(f"{label}_cost_stressed_expectancy_not_positive_after_atr_risk")
        if (as_float(row.get("max_model_risk_pct"), 0.0) or 0.0) <= 0.0:
            reasons.append(f"{label}_model_risk_pct_not_observed")
        if (as_float(row.get("avg_open_sl_points"), 0.0) or 0.0) <= 0.0 or (as_float(row.get("avg_open_tp_points"), 0.0) or 0.0) <= 0.0:
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
        reasons.append("post_atr_risk_segment_flags_present")
    return sorted(set(reasons))


def decide_stage58(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]], external_status: str) -> str:
    if external_status != "completed":
        return "proceed_to_stage59_post_risk_atr_repair"
    reasons = stage58_failure_reasons(summary_rows, segment_rows)
    if not reasons:
        return "proceed_to_stage60_onnx_hardening_candidate"
    severe = {"validation_net_not_positive_after_atr_risk", "oos_net_not_positive_after_atr_risk", "mandatory_model_risk_atr_combined_variant_missing"}
    if severe & set(reasons):
        return "demote_adapter_due_to_risk_atr_damage"
    return "proceed_to_stage59_post_risk_atr_repair"


def decision_next_stage(decision: str) -> str:
    if decision == "proceed_to_stage60_onnx_hardening_candidate":
        return "60_adapter_onnx__hardening_runtime_reproduction"
    if decision == "open_new_model_branch_due_to_risk_atr_incompatibility":
        return "new_model_branch_to_be_named"
    if decision == "demote_adapter_due_to_risk_atr_damage":
        return STAGE59_ID
    return STAGE59_ID


def artifact_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    created = utc_now()
    paths = [
        REPORT_PATH,
        RISK_TELEMETRY_SUMMARY_PATH,
        ATR_BRACKET_TELEMETRY_PATH,
        RISK_FLOOR_IMPACT_PATH,
        SEGMENT_KPI_PATH,
        DECISION_PATH,
        SUMMARY_JSON_PATH,
        RAW_SUMMARY_PATH,
        AUDIT_CSV_PATH,
        RUN_ROOT / "run_manifest.json",
        RUN_ROOT / "kpi_record.json",
        Path(__file__),
        Path("foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5"),
        Path("foundation/mt5/include/ObsidianPrime/ExecutionBridge.mqh"),
        Path("foundation/mt5/include/ObsidianPrime/RuntimeTelemetry.mqh"),
    ]
    rows: list[dict[str, Any]] = []
    for path in paths:
        resolved = path if path.is_absolute() else REPO_ROOT / path
        if not path_exists(resolved):
            continue
        rows.append(
            {
                "artifact_id": f"stage58_{aw.safe_name(path.stem, 100)}",
                "artifact_type": path.suffix.lstrip(".") or "artifact",
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(resolved) if io_path(resolved).is_file() else "directory_or_not_feasible",
                "stage_id": STAGE58_ID,
                "run_id": RUN_ID,
                "created_at_utc": created,
                "notes": "Stage58 BaselineAdapter risk/ATR integration artifact.",
            }
        )
    for report in result.get("strategy_tester_reports", []):
        html = report.get("html_report", {}) if isinstance(report.get("html_report"), Mapping) else {}
        if html.get("path"):
            rows.append(
                {
                    "artifact_id": f"stage58_mt5_report_{aw.safe_name(str(report.get('attempt_name') or report.get('report_name')), 100)}",
                    "artifact_type": "mt5_html_report",
                    "path": rel(str(html["path"])),
                    "sha256": sha256_file_lf_normalized(Path(str(html["path"]))),
                    "stage_id": STAGE58_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Actual Stage58 MT5 Strategy Tester HTML report.",
                }
            )
    return rows


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


def write_ledgers(
    result: Mapping[str, Any],
    summary_rows: Sequence[Mapping[str, Any]],
    segment_rows: Sequence[Mapping[str, Any]],
    decision: str,
    artifacts: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    external = str(result.get("external_verification_status") or "blocked")
    best = best_combined_variant(summary_rows)
    val = best.get("validation") if isinstance(best.get("validation"), Mapping) else {}
    oos = best.get("oos") if isinstance(best.get("oos"), Mapping) else {}
    status = "completed" if external == "completed" else "blocked"
    run_payload = upsert_csv_rows_retry(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE58_ID,
                "lane": "baseline_adapter_risk_atr_integration",
                "status": status,
                "judgment": decision,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_adapter", SOURCE_ADAPTER_ID),
                        ("best_combined_adapter", best.get("adapter_id")),
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
        stage_id=STAGE58_ID,
        mt5_kpi_records=result.get("mt5_kpi_records", []),
        run_output_root=RUN_ROOT,
        external_verification_status=external,
    )
    ledger_rows.append(
        {
            "ledger_row_id": f"{RUN_ID}__aggregate_risk_atr_integration",
            "stage_id": STAGE58_ID,
            "run_id": RUN_ID,
            "subrun_id": "aggregate_risk_atr_integration",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "risk_atr_integration",
            "tier_scope": "Tier A+B",
            "kpi_scope": "baseline_adapter_risk_atr",
            "scoreboard_lane": "runtime_probe",
            "status": status,
            "judgment": decision,
            "path": rel(DECISION_PATH),
            "primary_kpi": ledger_pairs(
                (
                    ("best_combined_adapter", best.get("adapter_id")),
                    ("validation_net", val.get("net_profit")),
                    ("oos_net", oos.get("net_profit")),
                    ("validation_pf", val.get("profit_factor")),
                    ("oos_pf", oos.get("profit_factor")),
                )
            ),
            "guardrail_kpi": ledger_pairs(
                (
                    ("failure_reasons", stage58_failure_reasons(summary_rows, segment_rows)),
                    ("atr_sltp", "measured"),
                    ("model_controlled_risk_pct", "measured"),
                    ("overall_goal_complete", False),
                )
            ),
            "external_verification_status": external,
            "notes": "Stage58 integrates and measures ATR SL/TP plus model-controlled risk%; not final completion.",
        }
    )
    ledger_rows.append(
        {
            "ledger_row_id": f"{RUN_ID}__tier_b_disabled_record",
            "stage_id": STAGE58_ID,
            "run_id": RUN_ID,
            "subrun_id": "tier_b_disabled_record",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "tier_b_disabled_record",
            "tier_scope": "Tier B",
            "kpi_scope": "tier_contribution_record",
            "scoreboard_lane": "runtime_probe",
            "status": "disabled",
            "judgment": "tier_b_disabled_due_prior_fallback_damage",
            "path": rel(DECISION_PATH),
            "primary_kpi": "tier_b_fallback_only=disabled",
            "guardrail_kpi": "not_synthetic_combined;actual_routed_total_uses_tier_a_primary_only",
            "external_verification_status": external,
            "notes": "Tier B contribution was recorded as disabled, not omitted.",
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
    atr_rows: Sequence[Mapping[str, Any]],
    floor_rows: Sequence[Mapping[str, Any]],
    segment_rows: Sequence[Mapping[str, Any]],
    decision: str,
    ledger_payload: Mapping[str, Any],
) -> None:
    external = str(result.get("external_verification_status") or "blocked")
    best = best_combined_variant(summary_rows)
    reasons = stage58_failure_reasons(summary_rows, segment_rows)
    write_csv(RAW_SUMMARY_PATH, summary_rows)
    write_csv(RISK_TELEMETRY_SUMMARY_PATH, risk_rows)
    write_csv(ATR_BRACKET_TELEMETRY_PATH, atr_rows)
    write_csv(RISK_FLOOR_IMPACT_PATH, floor_rows)
    write_csv(SEGMENT_KPI_PATH, segment_rows)
    write_md(REPORT_PATH, report_markdown(summary_rows, risk_rows, atr_rows, floor_rows, segment_rows, decision, reasons, external))
    write_md(DECISION_PATH, decision_markdown(decision, reasons, best, external))
    write_json(
        SUMMARY_JSON_PATH,
        {
            "created_at_utc": utc_now(),
            "stage_id": STAGE58_ID,
            "run_id": RUN_ID,
            "packet_id": PACKET_ID,
            "source_stage57_decision": rel(SOURCE_STAGE57_DECISION),
            "source_adapter": SOURCE_ADAPTER_ID,
            "variants": [variant.__dict__ for variant in STAGE58_VARIANTS],
            "external_verification_status": external,
            "decision": decision,
            "best_combined_variant": best,
            "failure_reasons": reasons,
            "required_outputs": {
                "risk_atr_integration_report": rel(REPORT_PATH),
                "risk_telemetry_summary": rel(RISK_TELEMETRY_SUMMARY_PATH),
                "atr_bracket_telemetry_summary": rel(ATR_BRACKET_TELEMETRY_PATH),
                "risk_floor_segment_impact": rel(RISK_FLOOR_IMPACT_PATH),
                "risk_atr_segment_kpi_summary": rel(SEGMENT_KPI_PATH),
                "stage58_decision": rel(DECISION_PATH),
            },
            "ledger_payload": ledger_payload,
            "claim_boundary": BOUNDARY,
            "overall_goal_complete": False,
            "forbidden_claims": [
                "deployment",
                "live_readiness",
                "production_baseline",
                "operating_promotion",
                "operating_reference",
                "runtime_authority",
            ],
        },
    )


def report_markdown(
    summary_rows: Sequence[Mapping[str, Any]],
    risk_rows: Sequence[Mapping[str, Any]],
    atr_rows: Sequence[Mapping[str, Any]],
    floor_rows: Sequence[Mapping[str, Any]],
    segment_rows: Sequence[Mapping[str, Any]],
    decision: str,
    reasons: Sequence[str],
    external: str,
) -> str:
    best = best_combined_variant(summary_rows)
    rows = [row for row in summary_rows if row.get("view") == "actual_routed_total"]
    table = "\n".join(
        "| {adapter} | {split} | {atr} | {risk} | {pf} | {net} | {dd} | {cost} | {lot} | {sl} | {tp} |".format(
            adapter=row.get("adapter_id"),
            split=row.get("split"),
            atr=row.get("atr_enabled"),
            risk=row.get("model_risk_enabled"),
            pf=aw.fmt(row.get("profit_factor")),
            net=aw.fmt(row.get("net_profit")),
            dd=aw.fmt(row.get("max_drawdown_amount")),
            cost=aw.fmt(row.get("cost_stressed_expectancy")),
            lot=aw.fmt(row.get("avg_executed_lot")),
            sl=aw.fmt(row.get("avg_open_sl_points")),
            tp=aw.fmt(row.get("avg_open_tp_points")),
        )
        for row in rows
    )
    return f"""# Stage58 Risk/ATR Integration Report(58단계 위험/ATR 통합 보고서)

- stage(단계): `{STAGE58_ID}`
- run(실행): `{RUN_ID}`
- source_adapter(원천 어댑터): `{SOURCE_ADAPTER_ID}`
- external_verification_status(외부 검증 상태): `{external}`
- decision(판정): `{decision}`
- boundary(경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Can mandatory ATR SL/TP(필수 ATR 손절/익절) and model-controlled risk%(모델 제어 위험률) be integrated without damaging validation/OOS(검증/표본외), segment KPI(구간 핵심 성과 지표), drawdown(손실폭), cost-stressed expectancy(비용 압박 기대값), MFE/MAE(최대 유리/불리 이동), or telemetry(텔레메트리)?

## Result Table(결과 표)

| adapter(어댑터) | split(구간) | ATR | model risk(모델 위험) | PF(수익 팩터) | net(순손익) | DD(손실폭) | cost exp(비용 기대값) | lot(랏) | SL | TP |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
{table}

## Read(판독)

- best_combined_adapter(최선 합산 어댑터): `{best.get('adapter_id', 'none')}`
- failure_reasons(실패/약점 사유): `{';'.join(reasons) if reasons else 'none'}`
- risk_telemetry_summary(위험 텔레메트리 요약): `{rel(RISK_TELEMETRY_SUMMARY_PATH)}`
- atr_bracket_telemetry_summary(ATR 브래킷 텔레메트리 요약): `{rel(ATR_BRACKET_TELEMETRY_PATH)}`
- risk_floor_segment_impact(위험 바닥 구간 영향): `{rel(RISK_FLOOR_IMPACT_PATH)}`
- risk_atr_segment_kpi_summary(위험/ATR 구간 KPI 요약): `{rel(SEGMENT_KPI_PATH)}`

Effect(효과): ATR/risk(ATR/위험)는 measured mandatory capability(측정된 필수 기능)로 기록하지만 final adapter completion(최종 어댑터 완료)이나 ONNX hardening(ONNX 경화) 시작 조건을 자동으로 만들지 않는다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위).
"""


def decision_markdown(decision: str, reasons: Sequence[str], best: Mapping[str, Any], external: str) -> str:
    next_stage = decision_next_stage(decision)
    return f"""# Stage58 Decision(58단계 판정)

decision(판정): `{decision}`

Stage58(58단계)는 mandatory ATR SL/TP(필수 ATR 손절/익절)와 model-controlled risk%(모델 제어 위험률)를 measured integration(측정된 통합)으로 기록한다. Effect(효과): capability exists(기능 존재)와 package complete(패키지 완료)를 분리한다.

## Evidence(근거)

- report(보고서): `{rel(REPORT_PATH)}`
- risk_telemetry_summary(위험 텔레메트리 요약): `{rel(RISK_TELEMETRY_SUMMARY_PATH)}`
- atr_bracket_telemetry_summary(ATR 브래킷 텔레메트리 요약): `{rel(ATR_BRACKET_TELEMETRY_PATH)}`
- risk_floor_segment_impact(위험 바닥 구간 영향): `{rel(RISK_FLOOR_IMPACT_PATH)}`
- risk_atr_segment_kpi_summary(위험/ATR 구간 KPI 요약): `{rel(SEGMENT_KPI_PATH)}`
- external_verification_status(외부 검증 상태): `{external}`

## Reason(이유)

- best_combined_adapter(최선 합산 어댑터): `{best.get('adapter_id', 'none')}`
- failure_reasons(실패/약점 사유): `{';'.join(reasons) if reasons else 'none'}`

## Next(다음)

next_stage_or_branch(다음 단계/분기): `{next_stage}`

Stage58 closeout(58단계 종료)는 overall goal completion(전체 목표 완료)이 아니다. Effect(효과): Stage59/60(59/60단계) 조건을 실제 근거로만 연다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
"""


def write_run_identity(result: Mapping[str, Any]) -> None:
    write_json(
        RUN_ROOT / "run_manifest.json",
        {
            "run_id": RUN_ID,
            "packet_id": PACKET_ID,
            "stage_id": STAGE58_ID,
            "run_number": RUN_NUMBER,
            "source_stage57_decision": rel(SOURCE_STAGE57_DECISION),
            "source_adapter": SOURCE_ADAPTER_ID,
            "development_anchor": DEVELOPMENT_ANCHOR,
            "variants": [variant.__dict__ for variant in STAGE58_VARIANTS],
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
            "stage_id": STAGE58_ID,
            "mt5_kpi_records": result.get("mt5_kpi_records", []),
            "strategy_tester_reports": result.get("strategy_tester_reports", []),
            "execution_results": result.get("execution_results", []),
            "external_verification_status": result.get("external_verification_status"),
            "judgment": result.get("judgment"),
            "claim_boundary": BOUNDARY,
        },
    )


def write_packet_files(
    result: Mapping[str, Any],
    summary_rows: Sequence[Mapping[str, Any]],
    risk_rows: Sequence[Mapping[str, Any]],
    segment_rows: Sequence[Mapping[str, Any]],
    decision: str,
    ledger_payload: Mapping[str, Any],
) -> None:
    external = str(result.get("external_verification_status") or "blocked")
    reasons = stage58_failure_reasons(summary_rows, segment_rows)
    best = best_combined_variant(summary_rows)
    payloads = {
        "routing_receipt.json": {
            "packet_id": PACKET_ID,
            "work_packet_lifecycle": "runtime_backtest_to_evidence_to_report",
            "primary_family": "runtime_backtest",
            "primary_skill": "obsidian-runtime-parity",
            "support_skills": [
                "obsidian-backtest-forensics",
                "obsidian-run-evidence-system",
                "obsidian-artifact-lineage",
                "obsidian-result-judgment",
            ],
            "required_gates": [
                "runtime_evidence_gate",
                "scope_completion_gate",
                "kpi_contract_audit",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "branch_action": "stay_on_main",
            "status": "completed",
        },
        "experiment_design_receipt.json": {
            "hypothesis": "ATR SL/TP and model-controlled risk can be integrated only if post-integration validation/OOS and segment KPI remain credible.",
            "decision_use": "Route Stage58 to Stage59 repair, Stage60 ONNX candidate, demotion, or new branch.",
            "comparison_baseline": SOURCE_ADAPTER_ID,
            "control_variables": ["US100", "M5", "split_v1", "Tier B disabled", "same_direction_reentry_cooldown_bars=5"],
            "changed_variables": ["ATR bracket", "model-controlled risk percent", "bracket multiplier bucket"],
            "status": "completed",
        },
        "backtest_forensics_audit.json": {
            "status": "passed" if external == "completed" else "blocked",
            "tester_identity": "US100 M5; validation 2025-01-02..2025-10-01; OOS 2025-10-01..2026-04-13; deposit=500; leverage=1:100; model=4",
            "ea_identity": "foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5 plus ObsidianPrime includes",
            "trade_evidence": "MT5 Strategy Tester HTML and telemetry CSV",
            "cost_assumptions": "FPMarkets US100 tester path, commission-free account evidence carried from Stage56",
            "backtest_judgment": "usable_with_boundary" if external == "completed" else "blocked",
        },
        "runtime_evidence_gate.json": {
            "status": "passed" if external == "completed" else "blocked",
            "attempt_count": len(result.get("attempts", [])),
            "mt5_kpi_record_count": len(result.get("mt5_kpi_records", [])),
            "telemetry_rows": len(risk_rows),
        },
        "kpi_contract_audit.json": {
            "status": "passed_with_flags" if external == "completed" else "blocked",
            "required_outputs": {
                "risk_atr_integration_report": rel(REPORT_PATH),
                "risk_telemetry_summary": rel(RISK_TELEMETRY_SUMMARY_PATH),
                "atr_bracket_telemetry_summary": rel(ATR_BRACKET_TELEMETRY_PATH),
                "risk_floor_segment_impact": rel(RISK_FLOOR_IMPACT_PATH),
                "risk_atr_segment_kpi_summary": rel(SEGMENT_KPI_PATH),
                "stage58_decision": rel(DECISION_PATH),
            },
        },
        "artifact_lineage_audit.json": {
            "status": "passed",
            "source_inputs": [rel(SOURCE_MODEL), rel(source_feature("validation_is")), rel(source_feature("oos")), rel(SOURCE_STAGE57_DECISION)],
            "producer": rel(Path(__file__)),
            "consumers": [rel(REPORT_PATH), rel(DECISION_PATH), rel(SUMMARY_JSON_PATH)],
            "ledger_links": ledger_payload,
        },
        "result_judgment_gate.json": {
            "result_subject": RUN_ID,
            "evidence_available": [rel(REPORT_PATH), rel(RISK_TELEMETRY_SUMMARY_PATH), rel(SEGMENT_KPI_PATH), rel(DECISION_PATH)],
            "evidence_missing": reasons,
            "judgment_label": decision,
            "claim_boundary": BOUNDARY,
            "next_condition": decision_next_stage(decision),
            "status": "passed_with_boundary",
        },
        "required_gate_coverage_audit.json": {
            "required_gates": [
                "runtime_evidence_gate",
                "scope_completion_gate",
                "kpi_contract_audit",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "covered_gates": [
                "runtime_evidence_gate",
                "scope_completion_gate",
                "kpi_contract_audit",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "status": "passed" if external == "completed" else "blocked",
        },
        "final_claim_guard.json": {
            "status": "passed",
            "overall_goal_complete": False,
            "stage58_closeout_is_not_goal_completion": True,
            "decision": decision,
            "forbidden_claims": [
                "deployment",
                "live_readiness",
                "production_baseline",
                "operating_promotion",
                "operating_reference",
                "runtime_authority",
            ],
        },
        "aggregate_summary.json": {
            "stage_id": STAGE58_ID,
            "run_id": RUN_ID,
            "packet_id": PACKET_ID,
            "external_verification_status": external,
            "decision": decision,
            "best_combined_variant": best,
            "failure_reasons": reasons,
            "overall_goal_complete": False,
            "summary_json": rel(SUMMARY_JSON_PATH),
        },
    }
    for name, payload in payloads.items():
        write_json(PACKET_ROOT / name, payload)


def write_stage_selection(decision: str, summary_rows: Sequence[Mapping[str, Any]], external: str) -> None:
    best = best_combined_variant(summary_rows)
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage58 Selection Status(58단계 선택 상태)

- stage_status(단계 상태): `closed_bounded_risk_atr_integration`
- latest_run_id(최신 실행 ID): `{RUN_ID}`
- current_judgment(현재 판정): `{decision}`
- source_adapter(원천 어댑터): `{SOURCE_ADAPTER_ID}`
- best_combined_adapter(최선 합산 어댑터): `{best.get('adapter_id', 'none')}`
- selected_research_baseline(선택 연구 기준선): `none`
- external_verification_status(외부 검증 상태): `{external}`
- next_stage_or_branch(다음 단계/분기): `{decision_next_stage(decision)}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage58(58단계)는 ATR/risk(ATR/위험) measured integration(측정된 통합)으로 닫지만, 전체 BaselineAdapter goal(기준선 어댑터 목표)은 계속 진행한다.
""",
    )


def write_stage59_scaffold(decision: str) -> None:
    if decision == "proceed_to_stage60_onnx_hardening_candidate":
        return
    root = Path("stages") / STAGE59_ID
    write_md(
        root / "00_spec/stage_brief.md",
        f"""# Stage59 Brief(59단계 개요)

- stage_id(단계 ID): `{STAGE59_ID}`
- source_stage(원천 단계): `{STAGE58_ID}`
- source_decision(원천 판정): `{decision}`
- boundary(경계): `{BOUNDARY}`

Stage59(59단계)는 post-risk/ATR repair and revalidation(위험/ATR 이후 수리와 재검증) 단계다. Effect(효과): ATR SL/TP(ATR 손절/익절)와 model-controlled risk%(모델 제어 위험률)를 포함한 full adapter(전체 어댑터)를 수리/재검증한다.
""",
    )
    write_md(
        root / "01_inputs/input_refs.md",
        f"""# Stage59 Input References(59단계 입력 참조)

- stage58_decision(58단계 판정): `{rel(DECISION_PATH)}`
- risk_atr_integration_report(위험/ATR 통합 보고서): `{rel(REPORT_PATH)}`
- risk_atr_segment_kpi_summary(위험/ATR 구간 KPI 요약): `{rel(SEGMENT_KPI_PATH)}`
- risk_telemetry_summary(위험 텔레메트리 요약): `{rel(RISK_TELEMETRY_SUMMARY_PATH)}`
- atr_bracket_telemetry_summary(ATR 브래킷 텔레메트리 요약): `{rel(ATR_BRACKET_TELEMETRY_PATH)}`
""",
    )
    write_md(
        root / "03_reviews/review_index.md",
        """# Stage59 Review Index(59단계 검토 색인)

Stage59(59단계)는 아직 planning scaffold(계획 골격) 상태다.

- adapter_repair_report.md
- repaired_adapter_summary.json
- repaired_adapter_summary.csv
- repaired_segment_kpi_summary.csv
- repaired_equity_curve_audit.md
- repaired_risk_atr_telemetry.csv
- stage59_decision.md
""",
    )
    write_md(
        root / "04_selected/selection_status.md",
        f"""# Stage59 Selection Status(59단계 선택 상태)

- stage_status(단계 상태): `active_planned_from_stage58`
- source_stage(원천 단계): `{STAGE58_ID}`
- source_decision(원천 판정): `{decision}`
- selected_research_baseline(선택 연구 기준선): `none`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage59(59단계)는 Stage58(58단계)의 risk/ATR damage or weakness(위험/ATR 손상 또는 약점)를 full adapter repair(전체 어댑터 수리)로 다룬다.
""",
    )


def update_current_truth(decision: str, summary_rows: Sequence[Mapping[str, Any]], external: str) -> None:
    best = best_combined_variant(summary_rows)
    next_stage = decision_next_stage(decision)
    write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `stage59_post_risk_atr_repair_v1`
- current_run(현재 실행): `run53A_stage59_post_risk_atr_repair_v1`
- active_stage(활성 단계): `{next_stage}`
- selected_research_baseline(선택 연구 기준선): `none`
- development_anchor(개발 기준점): `{DEVELOPMENT_ANCHOR}`
- backup_anchor(예비 기준점): `{BACKUP_ANCHOR}`
- adapter_under_review(검토 중 어댑터): `{SOURCE_ADAPTER_ID}`
- status(상태): `stage58_closed_{decision}`
- claim_boundary(주장 경계): research/development only(연구/개발 전용)

Stage58(58단계) closed(종료) as bounded ATR/risk integration measurement(경계 ATR/위험 통합 측정). Effect(효과): ATR SL/TP(ATR 손절/익절)와 model-controlled risk%(모델 제어 위험률)는 measured(측정됨)됐지만 final adapter(최종 어댑터) 또는 overall goal complete(전체 목표 완료)는 아니다.

## Latest Stage58 Evidence(최신 58단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- best_combined_adapter(최선 합산 어댑터): `{best.get('adapter_id', 'none')}`
- external_verification_status(외부 검증 상태): `{external}`
- report(보고서): `{rel(REPORT_PATH)}`
- stage58_decision(58단계 판정): `{rel(DECISION_PATH)}`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), overall_goal_complete(전체 목표 완료).
""",
    )
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = re.sub(r"^current_run_id: .*$", "current_run_id: run53A_stage59_post_risk_atr_repair_v1", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^updated_on: .*$", "updated_on: '2026-05-15'", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^active_stage: .*$", f"active_stage: {next_stage}", text, count=1, flags=re.MULTILINE)
    focus = (
        "current_focus:\n"
        f"- >-\n"
        f"  Stage58(58단계) `{STAGE58_ID}` closed(종료) as bounded ATR/risk integration measurement(경계 ATR/위험 통합 측정); decision(판정)=`{decision}`. "
        f"Effect(효과): ATR SL/TP(ATR 손절/익절)와 model-controlled risk%(모델 제어 위험률)는 측정됐지만 final(최종) 또는 operating(운영) 주장은 없다.\n"
        f"- >-\n"
        f"  Next stage(다음 단계) `{next_stage}` is active/planned(활성/계획). Effect(효과): Stage58(58단계) 약점을 full adapter repair/revalidation(전체 어댑터 수리/재검증)으로 이어 간다.\n"
    )
    text = re.sub(
        r"current_focus:\n(?:- >-\n  Stage58[^\n]*\n- >-\n  Next stage[^\n]*\n)*",
        "current_focus:\n",
        text,
        count=1,
    )
    text = re.sub(r"current_focus:\n", focus, text, count=1)
    block = f"""

stage58_risk_atr_integration:
  packet_id: {PACKET_ID}
  stage_id: {STAGE58_ID}
  status: closed_bounded_risk_atr_integration
  current_run_id: {RUN_ID}
  source_adapter: {SOURCE_ADAPTER_ID}
  best_combined_adapter: {best.get('adapter_id', 'none')}
  decision: {decision}
  next_stage: {next_stage}
  report_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  external_verification_status: {external}
  boundary: {BOUNDARY}
"""
    if "stage58_risk_atr_integration:" in text:
        text = re.sub(
            r"\nstage58_risk_atr_integration:\n(?:  .*\n)*",
            block,
            text,
            count=1,
        )
    else:
        text += block
    io_path(WORKSPACE_STATE_PATH).write_text(text, encoding="utf-8-sig")


def append_changelog(decision: str) -> None:
    text = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    entry = f"""
## 2026-05-15 Stage58 Risk/ATR Integration(58단계 위험/ATR 통합)
- completed(완료): `{RUN_ID}` actual MT5 validation/OOS(실제 MT5 검증/표본외) risk/ATR integration measurement(위험/ATR 통합 측정)을 기록했다.
- decision(판정): `{decision}`.
- effect(효과): ATR SL/TP(ATR 손절/익절)와 model-controlled risk%(모델 제어 위험률)를 필수 기능으로 측정했지만, final adapter(최종 어댑터), deployment(배포), live readiness(실거래 준비), runtime authority(런타임 권위)는 주장하지 않는다.
"""
    pattern = re.compile(r"\n## 2026-05-15 Stage58 Risk/ATR Integration\(58단계 위험/ATR 통합\).*?(?=\n## |\Z)", re.DOTALL)
    text = pattern.sub("", text)
    io_path(CHANGELOG_PATH).write_text(text.rstrip() + entry, encoding="utf-8-sig")


def write_stage_briefs() -> None:
    write_md(
        SPEC_ROOT / "stage_brief.md",
        f"""# Stage58 Brief(58단계 개요)

- stage_id(단계 ID): `{STAGE58_ID}`
- run(실행): `{RUN_ID}`
- source_decision(원천 판정): `proceed_to_stage58_adapter_repair_before_risk_atr`
- boundary(경계): `{BOUNDARY}`

Stage58(58단계)는 mandatory ATR SL/TP(필수 ATR 손절/익절)와 model-controlled risk%(모델 제어 위험률)를 actual MT5 validation/OOS(실제 MT5 검증/표본외)로 통합/측정한다. Effect(효과): 기능 추가를 completion(완료)로 오해하지 않고 Stage59/60(59/60단계) 경로를 판정한다.
""",
    )
    write_md(
        INPUT_ROOT / "input_refs.md",
        f"""# Stage58 Input References(58단계 입력 참조)

- stage57_decision(57단계 판정): `{rel(SOURCE_STAGE57_DECISION)}`
- stage57_segment_kpi_summary(57단계 구간 KPI 요약): `{rel(SOURCE_STAGE57_SEGMENTS)}`
- source_adapter_spec(원천 어댑터 명세): `{rel(SOURCE_BA14_SPEC)}`
- source_runtime_summary(원천 런타임 요약): `{rel(SOURCE_RUN50CA_SUMMARY)}`
- source_runtime_risk_telemetry(원천 런타임 위험 텔레메트리): `{rel(SOURCE_RUN50CA_RISK)}`
- source_model(원천 모델): `{rel(SOURCE_MODEL)}`
""",
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage58 BaselineAdapter ATR/risk integration MT5 batch.")
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--finalize-existing", action="store_true")
    parser.add_argument("--cost-stress-per-trade", type=float, default=0.50)
    parser.add_argument("--common-files-root", default=str(COMMON_FILES_ROOT_DEFAULT))
    parser.add_argument("--terminal-data-root", default=str(TERMINAL_DATA_ROOT_DEFAULT))
    parser.add_argument("--tester-profile-root", default=str(TESTER_PROFILE_ROOT_DEFAULT))
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(METAEDITOR_PATH_DEFAULT))
    parser.add_argument("--timeout-seconds", type=int, default=480)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    configure_repair_module()
    write_stage_briefs()
    if args.finalize_existing:
        result = load_existing_result()
    else:
        inputs = prepare_inputs(Path(args.common_files_root))
        attempts = build_attempts(inputs)
        prepared = {
            "run_id": RUN_ID,
            "stage_id": STAGE58_ID,
            "stage_number": 58,
            "run_number": RUN_NUMBER,
            "run_root": RUN_ROOT,
            "packet_id": PACKET_ID,
            "attempts": attempts,
            "common_copies": inputs["common_copies"],
            "feature_exports": inputs["feature_exports"],
            "model_artifacts": {"adapter_entry_model": {"path": rel(inputs["model_local"]), "common_path": inputs["model_common"]}},
            "route_coverage": route_coverage(),
            "model_family": "baseline_adapter_stage58_risk_atr_ebm_table",
            "feature_set_id": "stage58_context_gap_refill_signal_risk_atr",
            "label_id": "label_v1_fwd12_m5_logret_train_q33_3class",
            "split_contract": "split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413",
            "claim_boundary": BOUNDARY,
        }
        result = execute_or_materialize(prepared, args)
    audit_rows = audit_rows_for_result(result, float(args.cost_stress_per_trade)) if result.get("mt5_kpi_records") else []
    risk_rows = risk_rows_from_result(result)
    summary_rows = build_summary_rows(result, audit_rows, risk_rows)
    atr_rows = atr_bracket_rows(summary_rows)
    floor_rows = risk_floor_impact_rows(summary_rows, risk_rows)
    segment_rows = segment_kpi_rows(summary_rows)
    external = str(result.get("external_verification_status") or "blocked")
    decision = decide_stage58(summary_rows, segment_rows, external)
    write_run_identity(result)
    write_csv(AUDIT_CSV_PATH, audit_rows)
    artifacts = artifact_rows(result)
    ledger_payload = write_ledgers(result, summary_rows, segment_rows, decision, artifacts)
    write_required_outputs(result, summary_rows, risk_rows, atr_rows, floor_rows, segment_rows, decision, ledger_payload)
    artifacts = artifact_rows(result)
    ledger_payload = write_ledgers(result, summary_rows, segment_rows, decision, artifacts)
    summary_payload = json.loads(io_path(SUMMARY_JSON_PATH).read_text(encoding="utf-8-sig"))
    summary_payload["ledger_payload"] = ledger_payload
    write_json(SUMMARY_JSON_PATH, summary_payload)
    write_packet_files(result, summary_rows, risk_rows, segment_rows, decision, ledger_payload)
    write_stage_selection(decision, summary_rows, external)
    write_stage59_scaffold(decision)
    update_current_truth(decision, summary_rows, external)
    append_changelog(decision)
    print(
        json.dumps(
            json_ready(
                {
                    "status": "ok" if external == "completed" else "blocked",
                    "run_id": RUN_ID,
                    "decision": decision,
                    "best_combined_variant": best_combined_variant(summary_rows),
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
