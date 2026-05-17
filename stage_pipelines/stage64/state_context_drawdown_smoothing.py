from __future__ import annotations

import argparse
import csv
import json
import re
import sys
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
    parse_ini,
)
from foundation.mt5 import runtime_support as mt5  # noqa: E402
from stage_pipelines.stage56 import baseline_adapter_repair_batch as repair  # noqa: E402
from stage_pipelines.stage58 import risk_atr_integration as s58  # noqa: E402
from stage_pipelines.stage59d import source_lifecycle_or_demote as engine  # noqa: E402
from stage_pipelines.stage59y import new_model_branch_from_stage59x as checkpoint  # noqa: E402


STAGE64_ID = "64_adapter_research__state_context_drawdown_smoothing"
RUN_NUMBER = "run64A"
RUN_ID = "run64A_stage64_state_context_drawdown_smoothing_v1"
PACKET_ID = "stage64_state_context_drawdown_smoothing_v1"
PARENT_RUN_ID = "run63A_stage63_risk_atr_drawdown_compression_v1"
NEXT_STAGE_ID = "65_adapter_research__state_context_branch_review"
NEXT_RUN_ID = "run65A_stage65_state_context_branch_review_v1"
NEXT_PACKET_ID = "stage65_state_context_branch_review_v1"
SOURCE_STAGE59AR_ID = "59AR_adapter_repair__new_model_branch_from_stage59aq"
SOURCE_STAGE63_COMMIT = "9ee5cdf86f8cd352f3aa01454f8e8364f44dc40d"
SOURCE_ADAPTER_ID = "s62_v41_sd8_h5"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_no_legacy_inheritance"
DEVELOPMENT_ANCHOR = "v41_v22_midcov_et40_agree_h2c0_no_b"
BACKUP_ANCHOR = "s62_v41_sd8_h5"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)

STAGE_ROOT = Path("stages") / STAGE64_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
SPEC_ROOT = STAGE_ROOT / "00_spec"
INPUT_ROOT = STAGE_ROOT / "01_inputs"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
PARTIALS_ROOT = RUN_ROOT / "partials"

SOURCE_STAGE_ROOT = Path("stages") / "56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection"
RUN50BN_ROOT = SOURCE_STAGE_ROOT / "02_runs/run50BN"
RUN50BN_MODEL = RUN50BN_ROOT / "models/stage56_context_timed_event_signal_discrete_score_table.csv"
RUN50BN_SIGNAL = "stage56_context_et_event_signal"
SOURCE_ANCHOR = "v41_v22_midcov_et40_agree_h2c0_no_b"
SOURCE_TOKEN = "x01"
COMMON_ROOT = f"OPV2/s64/{RUN_NUMBER}"
MIN_MARGIN = 0.0

SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage64_state_context_summary.json"
SUMMARY_CSV_PATH = REVIEWS_ROOT / "stage64_state_context_summary.csv"
REPORT_PATH = REVIEWS_ROOT / "stage64_state_context_report.md"
SEGMENT_KPI_PATH = REVIEWS_ROOT / "stage64_segment_kpi_summary.csv"
RISK_ATR_TELEMETRY_PATH = REVIEWS_ROOT / "stage64_risk_atr_telemetry.csv"
GATE_FEATURE_SUMMARY_PATH = REVIEWS_ROOT / "stage64_gate_feature_summary.csv"
TIER_B_DIAGNOSTIC_PATH = REVIEWS_ROOT / "stage64_tier_b_diagnostic_summary.csv"
DECISION_PATH = REVIEWS_ROOT / "stage64_decision.md"
AUDIT_CSV_PATH = REVIEWS_ROOT / "stage64_trade_audit.csv"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

LEGACY_34D_TARGETS = {
    "latest_net_profit": 987.60,
    "latest_profit_factor": 1.583157,
    "latest_max_dd_pct": 12.909136,
    "latest_trade_count": 404,
    "latest_expectancy_per_trade": 2.444554,
    "extended_net_profit": 2950.79,
    "extended_profit_factor": 1.302494,
    "extended_max_dd_pct": 18.760867,
    "extended_trade_count": 1134,
    "extended_expectancy_per_trade": 2.602108,
}
STAGE63_REFERENCE = {
    "validation_pf": 1.199478619,
    "validation_net": 587.44,
    "validation_dd_pct": 18.69,
    "oos_pf": 1.319099231,
    "oos_net": 402.65,
    "oos_dd_pct": 34.86,
}

STAGE64_VARIANTS = (
    repair.RepairVariant(
        adapter_id="s64_ctx_margin08",
        label="h5_risk3_sl20_tp32_margin08_gate",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.0,
        atr_take_profit_multiplier=3.2,
        model_risk_max_pct=0.03,
        same_direction_reentry_cooldown_bars=8,
        short_threshold=0.55,
        long_threshold=0.55,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=True,
        max_hold_bars=5,
        notes=(
            "Stage64 v2-native state/context gate: block entries when ET40 margin is below 0.08 "
            "while preserving Stage63 risk3 tight bracket trade shape. "
            "Legacy 34D is a lesson-only target surface, not copied logic."
        ),
    ),
    repair.RepairVariant(
        adapter_id="s64_ctx_prob48",
        label="h5_risk3_sl20_tp32_prob48_gate",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.0,
        atr_take_profit_multiplier=3.2,
        model_risk_max_pct=0.03,
        same_direction_reentry_cooldown_bars=8,
        short_threshold=0.55,
        long_threshold=0.55,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=True,
        max_hold_bars=5,
        notes=(
            "Stage64 v2-native state/context gate: block entries when ET40 decision probability is below 0.48 "
            "while preserving Stage63 risk3 tight bracket trade shape. "
            "Legacy 34D is a lesson-only target surface, not copied logic."
        ),
    ),
    repair.RepairVariant(
        adapter_id="s64_ctx_session16",
        label="h5_risk3_sl20_tp32_session16_gate",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.0,
        atr_take_profit_multiplier=3.2,
        model_risk_max_pct=0.03,
        same_direction_reentry_cooldown_bars=8,
        short_threshold=0.55,
        long_threshold=0.55,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=True,
        max_hold_bars=5,
        notes=(
            "Stage64 v2-native state/context gate: block the 16:30-17:25 UTC entry band "
            "as a session-stability probe while preserving Stage63 risk3 tight bracket trade shape. "
            "Legacy 34D is a lesson-only target surface, not copied logic."
        ),
    ),
)

MODEL_RISK_MIN_PCT = {variant.adapter_id: 0.005 for variant in STAGE64_VARIANTS}

CONTEXT_GATE_SPECS = {
    "s64_ctx_margin08": {
        "gate_column": "stage64_gate_margin_lt_008",
        "description": "block if et40_decision_margin < 0.08 on non-flat source rows",
    },
    "s64_ctx_prob48": {
        "gate_column": "stage64_gate_probability_lt_048",
        "description": "block if et40_decision_probability < 0.48 on non-flat source rows",
    },
    "s64_ctx_session16": {
        "gate_column": "stage64_gate_utc_1630_1725",
        "description": "block if timestamp UTC is between 16:30 and 17:25 on non-flat source rows",
    },
}


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    candidate = Path(str(path))
    try:
        return io_path(candidate).resolve().relative_to(io_path(REPO_ROOT).resolve()).as_posix()
    except ValueError:
        return candidate.as_posix()


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.10g}"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return str(value)


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


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


def parse_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def parse_utc_hour_minute(value: str) -> tuple[int, int]:
    text = str(value).replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        return (-1, -1)
    return (dt.hour, dt.minute)


def gate_value(row: Mapping[str, str], variant: repair.RepairVariant) -> float:
    signal = int(round(parse_float(row.get(RUN50BN_SIGNAL), 0.0)))
    if signal == 0:
        return 0.0
    if variant.adapter_id == "s64_ctx_margin08":
        return 1.0 if parse_float(row.get("et40_decision_margin"), 1.0) < 0.08 else 0.0
    if variant.adapter_id == "s64_ctx_prob48":
        return 1.0 if parse_float(row.get("et40_decision_probability"), 1.0) < 0.48 else 0.0
    if variant.adapter_id == "s64_ctx_session16":
        hour, minute = parse_utc_hour_minute(str(row.get("timestamp_utc") or ""))
        return 1.0 if ((hour == 16 and minute >= 30) or (hour == 17 and minute <= 25)) else 0.0
    return 0.0


def write_neutral_gate_model(source: Path, destination: Path) -> None:
    rows = list(csv.reader(io_path(source).open("r", encoding="utf-8-sig", newline="")))
    rows.extend(
        [
            ["cut", "1", "0", "0.5", "", "", ""],
            ["score", "1", "0", "", "0", "0", "0"],
            ["score", "1", "1", "", "0", "0", "0"],
            ["score", "1", "2", "", "0", "0", "0"],
        ]
    )
    io_path(destination.parent).mkdir(parents=True, exist_ok=True)
    with io_path(destination).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerows(rows)


def write_gated_feature(source: Path, destination: Path, variant: repair.RepairVariant) -> dict[str, Any]:
    gate_column = str(CONTEXT_GATE_SPECS[variant.adapter_id]["gate_column"])
    io_path(destination.parent).mkdir(parents=True, exist_ok=True)
    total_rows = 0
    blocked_rows = 0
    with io_path(source).open("r", encoding="utf-8-sig", newline="") as input_handle:
        reader = csv.DictReader(input_handle)
        with io_path(destination).open("w", encoding="utf-8", newline="") as output_handle:
            writer = csv.DictWriter(
                output_handle,
                fieldnames=("bar_time_server", RUN50BN_SIGNAL, gate_column),
                lineterminator="\n",
            )
            writer.writeheader()
            for row in reader:
                gate = gate_value(row, variant)
                if gate >= 0.5:
                    blocked_rows += 1
                total_rows += 1
                writer.writerow(
                    {
                        "bar_time_server": row.get("bar_time_server") or row.get("timestamp_utc") or "",
                        RUN50BN_SIGNAL: csv_value(parse_float(row.get(RUN50BN_SIGNAL), 0.0)),
                        gate_column: csv_value(gate),
                    }
                )
    return {
        "variant_id": variant.adapter_id,
        "gate_column": gate_column,
        "source_feature": rel(source),
        "gated_feature": rel(destination),
        "total_rows": total_rows,
        "blocked_rows": blocked_rows,
        "blocked_ratio": (blocked_rows / total_rows) if total_rows else 0.0,
        "gate_description": CONTEXT_GATE_SPECS[variant.adapter_id]["description"],
    }


def feature_order_hash_for_variant(variant: repair.RepairVariant) -> str:
    gate_column = str(CONTEXT_GATE_SPECS[variant.adapter_id]["gate_column"])
    return engine.ordered_hash((RUN50BN_SIGNAL, gate_column))


def prepare_inputs(common_files_root: Path) -> dict[str, Any]:
    copied: list[dict[str, Any]] = []
    gate_rows: list[dict[str, Any]] = []
    model_exports: dict[str, dict[str, Any]] = {}
    feature_exports: dict[str, dict[str, dict[str, Any]]] = {}
    for variant in STAGE64_VARIANTS:
        source_label = engine.source_label_for_variant(variant)
        model_source = engine.source_model_for_variant(variant)
        gate_column = str(CONTEXT_GATE_SPECS[variant.adapter_id]["gate_column"])
        model_local = RUN_ROOT / variant.adapter_id / "models" / f"{source_label}_{model_source.stem}_{gate_column}.csv"
        write_neutral_gate_model(model_source, model_local)
        copied.append({"source": rel(model_source), "path": rel(model_local), "sha256": sha256_file_lf_normalized(model_local), "transform": "append_neutral_gate_feature"})
        copied.append(engine.copy_to_common(model_local, f"{COMMON_ROOT}/{variant.adapter_id}/models/{model_local.name}", common_files_root))
        model_exports[variant.adapter_id] = {
            "path": rel(model_local),
            "common_path": f"{COMMON_ROOT}/{variant.adapter_id}/models/{model_local.name}",
            "sha256": sha256_file_lf_normalized(model_local),
            "source_model": rel(model_source),
            "source_anchor": engine.source_anchor_for_variant(variant),
            "signal_column": RUN50BN_SIGNAL,
            "gate_column": gate_column,
            "feature_order_hash": feature_order_hash_for_variant(variant),
        }
        feature_exports[variant.adapter_id] = {}
        for split in ("validation_is", "oos"):
            token = "val" if split == "validation_is" else "oos"
            feature_source = engine.source_feature(split, variant, "a")
            feature_local = RUN_ROOT / variant.adapter_id / "features" / f"{variant.adapter_id}_stage64_state_context_a_{token}.csv"
            gate_row = write_gated_feature(feature_source, feature_local, variant)
            gate_row["split"] = split
            gate_rows.append(gate_row)
            copied.append({"source": rel(feature_source), "path": rel(feature_local), "sha256": sha256_file_lf_normalized(feature_local), "transform": "state_context_gate_feature"})
            copied.append(engine.copy_to_common(feature_local, f"{COMMON_ROOT}/{variant.adapter_id}/features/{feature_local.name}", common_files_root))
            feature_exports[variant.adapter_id][split] = {
                "path": rel(feature_local),
                "common_path": f"{COMMON_ROOT}/{variant.adapter_id}/features/{feature_local.name}",
                "sha256": sha256_file_lf_normalized(feature_local),
                "source_feature": rel(feature_source),
                "gate_column": gate_column,
            }
    return {
        "model_exports": model_exports,
        "feature_exports": feature_exports,
        "common_copies": copied,
        "gate_rows": gate_rows,
    }


def stage64_extra_set_values(variant: repair.RepairVariant, magic: int) -> dict[str, Any]:
    values = engine.extra_set_values(variant, magic)
    values["InpSideFilterEnabled"] = True
    values["InpSideFilterFeatureIndex"] = 1
    values["InpFallbackSideFilterFeatureIndex"] = 1
    values["InpBlockShortFeatureRange"] = True
    values["InpBlockShortFeatureMin"] = 0.5
    values["InpBlockShortFeatureMax"] = 1.5
    values["InpBlockLongFeatureRange"] = True
    values["InpBlockLongFeatureMin"] = 0.5
    values["InpBlockLongFeatureMax"] = 1.5
    return values


def configure_reused_engine() -> None:
    source_specs = {}
    for variant in STAGE64_VARIANTS:
        root = RUN50BN_ROOT / SOURCE_ANCHOR
        source_specs[variant.adapter_id] = {
            "label": SOURCE_ANCHOR,
            "run_root": RUN50BN_ROOT,
            "variant_root": root,
            "anchor": SOURCE_ANCHOR,
            "model": RUN50BN_MODEL,
            "signal_column": RUN50BN_SIGNAL,
            "validation_ini": root / "mt5" / f"{SOURCE_TOKEN}_ta_val.ini",
            "oos_ini": root / "mt5" / f"{SOURCE_TOKEN}_ta_oos.ini",
            "source_note": "Stage64 v2-native state/context gate from Stage63 risk/ATR compression branch",
        }

    engine.STAGE59_ID = STAGE64_ID
    engine.NEXT_REPAIR_STAGE_ID = NEXT_STAGE_ID
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
    engine.EQUITY_AUDIT_PATH = REVIEWS_ROOT / "stage64_equity_curve_audit.md"
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
    engine.STAGE59_VARIANTS = STAGE64_VARIANTS
    engine.SOURCE_SPECS = source_specs
    engine.MODEL_RISK_MIN_PCT = MODEL_RISK_MIN_PCT

    repair.STAGE_ID = STAGE64_ID
    repair.RUN_NUMBER = RUN_NUMBER
    repair.RUN_ID = RUN_ID
    repair.RUN_ROOT = RUN_ROOT
    repair.REPAIR_VARIANTS = STAGE64_VARIANTS

    s58.STAGE58_ID = STAGE64_ID
    s58.RUN_NUMBER = RUN_NUMBER
    s58.RUN_ID = RUN_ID
    s58.PACKET_ID = PACKET_ID
    s58.PARENT_RUN_ID = PARENT_RUN_ID
    s58.RUN_ROOT = RUN_ROOT
    s58.REVIEWS_ROOT = REVIEWS_ROOT
    s58.STAGE58_VARIANTS = STAGE64_VARIANTS
    s58.COMMON_ROOT = COMMON_ROOT

    checkpoint.PARTIALS_ROOT = PARTIALS_ROOT


def build_attempts(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    for variant_index, variant in enumerate(STAGE64_VARIANTS, start=1):
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
                magic = 64064000 + variant_index * 100 + (1 if split == "validation_is" else 50) + role_index
                attempts.append(
                    attempt_payload(
                        run_root=variant_root,
                        run_id=RUN_ID,
                        stage_number=64,
                        exploration_label="stage64_BaselineAdapter__StateContextDrawdownSmoothing",
                        attempt_name=f"{variant.adapter_id}_{attempt_token}_{split_token}",
                        tier=tier,
                        split=split,
                        model_path=str(inputs["model_exports"][variant.adapter_id]["common_path"]),
                        model_id=f"{RUN_ID}_{variant.adapter_id}_entry_adapter",
                        model_backend="ebm_table",
                        feature_path=str(inputs["feature_exports"][variant.adapter_id][split]["common_path"]),
                        feature_count=2,
                        feature_order_hash=inputs["model_exports"][variant.adapter_id]["feature_order_hash"],
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
                        extra_set_values=stage64_extra_set_values(variant, magic),
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
    return checkpoint.execute_prepared_run_checkpointed(prepared, args)


def best_variant(summary_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return engine.best_repaired_variant(summary_rows)


def target_progress_rows(summary_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in summary_rows:
        if row.get("view") != "actual_routed_total":
            continue
        pf = s58.as_float(row.get("profit_factor"), 0.0) or 0.0
        net = s58.as_float(row.get("net_profit"), 0.0) or 0.0
        dd = s58.as_float(row.get("max_drawdown_percent"), 0.0) or 0.0
        expectancy = s58.as_float(row.get("expectancy"), 0.0) or 0.0
        rows.append(
            {
                "run_id": RUN_ID,
                "adapter_id": row.get("adapter_id"),
                "split": row.get("split"),
                "view": row.get("view"),
                "profit_factor": pf,
                "net_profit": net,
                "max_drawdown_percent": dd,
                "expectancy": expectancy,
                "pf_gap_to_34d_latest": pf - LEGACY_34D_TARGETS["latest_profit_factor"],
                "pf_gap_to_34d_extended": pf - LEGACY_34D_TARGETS["extended_profit_factor"],
                "expectancy_gap_to_34d_latest": expectancy - LEGACY_34D_TARGETS["latest_expectancy_per_trade"],
                "dd_pct_gap_to_34d_latest": dd - LEGACY_34D_TARGETS["latest_max_dd_pct"],
                "target_surface": TARGET_SURFACE,
            }
        )
    return rows


def decide(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]], external: str) -> str:
    if external != "completed":
        return "continue_stage64_due_to_incomplete_runtime"
    best = best_variant(summary_rows)
    val = best.get("validation") if isinstance(best.get("validation"), Mapping) else {}
    oos = best.get("oos") if isinstance(best.get("oos"), Mapping) else {}
    val_pf = s58.as_float(val.get("profit_factor"), 0.0) or 0.0
    oos_pf = s58.as_float(oos.get("profit_factor"), 0.0) or 0.0
    val_net = s58.as_float(val.get("net_profit"), 0.0) or 0.0
    oos_net = s58.as_float(oos.get("net_profit"), 0.0) or 0.0
    val_dd = s58.as_float(val.get("max_drawdown_percent"), 99.0) or 99.0
    oos_dd = s58.as_float(oos.get("max_drawdown_percent"), 99.0) or 99.0
    reasons = engine.repair_failure_reasons(summary_rows, segment_rows)
    val_dd_not_worse = val_dd <= STAGE63_REFERENCE["validation_dd_pct"] + 0.25
    oos_dd_improved = oos_dd < STAGE63_REFERENCE["oos_dd_pct"]
    if val_net > 0 and oos_net > 0 and val_dd_not_worse and oos_dd_improved and val_pf >= 1.20 and oos_pf >= 1.25 and not reasons:
        return "proceed_with_state_context_candidate"
    if val_net > 0 and oos_net > 0 and oos_dd_improved and (val_pf >= 1.18 or oos_pf >= 1.20):
        return "continue_state_context_branch_repair"
    return "open_new_model_branch_due_to_context_damage"


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage64 v2-native state/context drawdown smoothing batch.")
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
    parser.add_argument("--cost-stress-per-trade", type=float, default=0.3)
    return parser.parse_args(argv)


def report_markdown(
    summary_rows: Sequence[Mapping[str, Any]],
    segment_rows: Sequence[Mapping[str, Any]],
    target_rows: Sequence[Mapping[str, Any]],
    decision: str,
    external: str,
) -> str:
    lines = [
        "| adapter(어댑터) | split(분할) | PF(수익 팩터) | net(순손익) | DD%(손실률) | expectancy(기대값) | PF gap latest(최신 PF 차이) |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for row in target_rows:
        lines.append(
            "| {adapter} | {split} | {pf:.4f} | {net:.2f} | {dd:.2f} | {exp:.4f} | {gap:.4f} |".format(
                adapter=row.get("adapter_id", ""),
                split=row.get("split", ""),
                pf=float(row.get("profit_factor") or 0.0),
                net=float(row.get("net_profit") or 0.0),
                dd=float(row.get("max_drawdown_percent") or 0.0),
                exp=float(row.get("expectancy") or 0.0),
                gap=float(row.get("pf_gap_to_34d_latest") or 0.0),
            )
        )
    best = best_variant(summary_rows)
    reasons = engine.repair_failure_reasons(summary_rows, segment_rows) if external == "completed" else ["runtime_incomplete_or_blocked"]
    variants = ", ".join(variant.adapter_id for variant in STAGE64_VARIANTS)
    return f"""# Stage64 State/Context Report(64단계 상태/문맥 보고)

- run(실행): `{RUN_ID}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- source_adapter(원천 어댑터): `{SOURCE_ADAPTER_ID}`
- variants(변형): `{variants}`
- legacy_relation(레거시 관계): `lesson_only_target_surface_no_code_copy`
- external_verification_status(외부 검증 상태): `{external}`
- decision(판정): `{decision}`
- boundary(경계): `{BOUNDARY}`

## Target Read(목표 판독)

Legacy 34D(레거시 34D)는 code copy(코드 복사) 대상이 아니다. Effect(효과): Stage64(64단계)는 Stage63(63단계) risk3 tight bracket(위험 3% 타이트 브래킷)을 출발점으로 두고, state/context gate(상태/문맥 게이트)가 OOS DD(표본외 손실률)와 early/mid weakness(초기/중간 약점)를 줄이는지만 본다.

## Result Table(결과 표)

{chr(10).join(lines)}

## Read(판독)

- best_variant(최선 변형): `{best.get("adapter_id", "none")}`
- weakness_reasons(약점 이유): `{";".join(reasons) if reasons else "none"}`
- segment_kpi_summary(구간 KPI 요약): `{rel(SEGMENT_KPI_PATH)}`
- risk_atr_telemetry(위험/ATR 텔레메트리): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- gate_feature_summary(게이트 피처 요약): `{rel(GATE_FEATURE_SUMMARY_PATH)}`
- tier_b_diagnostic(Tier B 진단): `{rel(TIER_B_DIAGNOSTIC_PATH)}`

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
"""


def decision_markdown(decision: str, external: str) -> str:
    return f"""# Stage64 Decision(64단계 판정)

decision(판정): `{decision}`

Stage64(64단계)는 legacy 34D(레거시 34D)를 복사하지 않고, Stage63(63단계) 후보의 OOS DD(표본외 손실률)를 state/context gate(상태/문맥 게이트)로 낮출 수 있는지 측정했다.

Effect(효과): 이번 단계 결과는 operating claim(운영 주장)이 아니라 다음 bounded research(경계 연구) 근거만 만든다.

## Evidence(근거)

- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- segment_kpi_summary(구간 KPI 요약): `{rel(SEGMENT_KPI_PATH)}`
- risk_atr_telemetry(위험/ATR 텔레메트리): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- gate_feature_summary(게이트 피처 요약): `{rel(GATE_FEATURE_SUMMARY_PATH)}`
- tier_b_diagnostic(Tier B 진단): `{rel(TIER_B_DIAGNOSTIC_PATH)}`
- external_verification_status(외부 검증 상태): `{external}`

## Next(다음)

next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
"""


def tier_b_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    coverage = engine.route_coverage()
    for variant in STAGE64_VARIANTS:
        variant_cov = coverage.get(variant.adapter_id, {})
        for split_name in ("validation", "oos"):
            split_cov = variant_cov.get(split_name, {})
            rows.append(
                {
                    "run_id": RUN_ID,
                    "adapter_id": variant.adapter_id,
                    "split": split_name,
                    "tier_b_policy": "diagnostic_missing_required_but_disabled_for_this_state_context_gate_probe",
                    "tier_b_rows_available": split_cov.get("tier_b_fallback_rows_available_but_disabled", 0),
                    "tier_b_rows_used": split_cov.get("tier_b_fallback_rows_used", 0),
                    "reason": "Stage64 isolates state/context gating first; Tier B fallback remains diagnostic and disabled.",
                }
            )
    return rows


def artifact_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    created = utc_now()
    paths = [
        REPORT_PATH,
        SUMMARY_JSON_PATH,
        SUMMARY_CSV_PATH,
        SEGMENT_KPI_PATH,
        RISK_ATR_TELEMETRY_PATH,
        GATE_FEATURE_SUMMARY_PATH,
        TIER_B_DIAGNOSTIC_PATH,
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
                    "artifact_type": "stage64_state_context_drawdown_smoothing_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE64_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage64 v2-native state/context drawdown smoothing artifact.",
                }
            )
    for report in result.get("strategy_tester_reports", []):
        html = report.get("html_report", {}) if isinstance(report.get("html_report"), Mapping) else {}
        raw_path = report.get("path") or html.get("path")
        if raw_path and path_exists(Path(str(raw_path))):
            path = Path(str(raw_path))
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__mt5_report__{path.stem}",
                    "artifact_type": "mt5_strategy_tester_report",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE64_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Actual Stage64 MT5 Strategy Tester HTML report.",
                }
            )
    return rows


def write_run_identity(result: Mapping[str, Any]) -> None:
    write_json(
        RUN_ROOT / "run_manifest.json",
        {
            "run_id": RUN_ID,
            "packet_id": PACKET_ID,
            "stage_id": STAGE64_ID,
            "run_number": RUN_NUMBER,
            "parent_run_id": PARENT_RUN_ID,
            "source_adapter_id": SOURCE_ADAPTER_ID,
            "source_stage63_pushed_commit": SOURCE_STAGE63_COMMIT,
            "target_surface": TARGET_SURFACE,
            "legacy_relation": "lesson_only_target_surface_no_code_copy_no_promotion_inheritance",
            "variants": [variant.__dict__ for variant in STAGE64_VARIANTS],
            "attempts": result.get("attempts", []),
            "model_artifacts": result.get("model_artifacts", {}),
            "feature_exports": result.get("feature_exports", {}),
            "gate_rows": result.get("gate_rows", []),
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
            "stage_id": STAGE64_ID,
            "mt5_kpi_records": result.get("mt5_kpi_records", []),
            "strategy_tester_reports": result.get("strategy_tester_reports", []),
            "execution_results": result.get("execution_results", []),
            "gate_rows": result.get("gate_rows", []),
            "external_verification_status": result.get("external_verification_status"),
            "judgment": result.get("judgment"),
            "claim_boundary": BOUNDARY,
        },
    )


def write_ledgers(
    result: Mapping[str, Any],
    decision: str,
    artifacts: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    external = str(result.get("external_verification_status") or "blocked")
    status = "completed" if external == "completed" else "blocked"
    run_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE64_ID,
                "lane": "baseline_adapter_v2_native_state_context_drawdown_smoothing",
                "status": status,
                "judgment": decision,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_adapter", SOURCE_ADAPTER_ID),
                        ("source_stage63_commit", SOURCE_STAGE63_COMMIT),
                        ("target_surface", TARGET_SURFACE),
                        ("legacy_relation", "lesson_only"),
                    )
                ),
            }
        ],
        key="run_id",
    )
    alpha_rows = build_mt5_alpha_ledger_rows(
        run_id=RUN_ID,
        stage_id=STAGE64_ID,
        mt5_kpi_records=result.get("mt5_kpi_records", []),
        run_output_root=RUN_ROOT,
        external_verification_status=external,
    )
    if not alpha_rows:
        alpha_rows = [
            {
                "ledger_row_id": f"{RUN_ID}__materialized_or_blocked",
                "stage_id": STAGE64_ID,
                "run_id": RUN_ID,
                "subrun_id": "materialized_or_blocked",
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "materialized_or_blocked",
                "tier_scope": "Tier A+B",
                "kpi_scope": "stage64_state_context_drawdown_smoothing",
                "scoreboard_lane": "runtime_probe",
                "status": status,
                "judgment": decision,
                "path": rel(DECISION_PATH),
                "primary_kpi": "mt5_kpi_records=0",
                "guardrail_kpi": f"target_surface={TARGET_SURFACE}",
                "external_verification_status": external,
                "notes": "Stage64 run materialized or blocked before KPI records were available.",
            }
        ]
    alpha_payload = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    artifact_payload = upsert_csv_rows(
        ARTIFACT_REGISTRY_PATH,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
        list(artifacts),
        key="artifact_id",
    )
    return {"run_registry": run_payload, "alpha_ledger": alpha_payload, "stage_ledger": stage_payload, "artifact_registry": artifact_payload}


def write_packet_files(result: Mapping[str, Any], decision: str, ledger_payload: Mapping[str, Any]) -> None:
    status = "completed" if result.get("external_verification_status") == "completed" else "blocked"
    write_json(
        PACKET_ROOT / "routing_receipt.json",
        {
            "packet_id": PACKET_ID,
            "stage_id": STAGE64_ID,
            "primary_family": "experiment_design",
            "primary_skill": "obsidian-experiment-design",
            "support_skills": ["obsidian-exploration-mandate", "obsidian-performance-attribution", "obsidian-model-validation"],
            "required_gates": ["runtime_evidence_gate", "kpi_contract_audit", "result_judgment_gate"],
            "status": status,
        },
    )
    write_json(
        PACKET_ROOT / "runtime_evidence_gate.json",
        {
            "packet_id": PACKET_ID,
            "run_id": RUN_ID,
            "external_verification_status": result.get("external_verification_status"),
            "completed_attempt_count": result.get("completed_attempt_count"),
            "expected_attempt_count": result.get("expected_attempt_count"),
            "gate_feature_summary_path": rel(GATE_FEATURE_SUMMARY_PATH),
            "claim_boundary": BOUNDARY,
        },
    )
    write_json(
        PACKET_ROOT / "result_judgment_gate.json",
        {
            "packet_id": PACKET_ID,
            "run_id": RUN_ID,
            "decision": decision,
            "legacy_relation": "lesson_only_target_surface_no_code_copy",
            "forbidden_claims": [
                "deployment",
                "live_readiness",
                "production_baseline",
                "operating_promotion",
                "operating_reference",
                "runtime_authority",
                "legacy_inheritance",
            ],
        },
    )
    write_json(
        PACKET_ROOT / "aggregate_summary.json",
        {
            "packet_id": PACKET_ID,
            "stage_id": STAGE64_ID,
            "run_id": RUN_ID,
            "decision": decision,
            "gate_feature_summary_path": rel(GATE_FEATURE_SUMMARY_PATH),
            "ledger_payload": ledger_payload,
            "overall_goal_complete": False,
        },
    )


def update_current_truth(decision: str, external: str) -> None:
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^updated_on: .*$", "updated_on: '2026-05-17'", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", text, count=1, flags=re.MULTILINE)
    current_focus = f"""current_focus:
- >-
  Stage64(64단계) closed(종료) as `{decision}` and Stage65(65단계) `{NEXT_STAGE_ID}` is open_planned(열림 계획). Effect(효과): state/context gate(상태/문맥 게이트) 실험 근거를 보존하고, 다음 연구 질문으로만 넘긴다.
- >-
  Stage64 result(64단계 결과): validation(검증), OOS(표본외), PF(수익 팩터), net(순손익), DD(손실률), gate feature(게이트 피처)는 `{rel(SUMMARY_CSV_PATH)}`와 `{rel(GATE_FEATURE_SUMMARY_PATH)}`에 기록됐다. Effect(효과): 34D target surface(34D 목표 표면) 대비 남은 KPI(핵심 성과 지표) 차이를 다음 단계 입력으로 보존한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): 목표는 높게 유지하지만 v2-native research(브이투 고유 연구)만 계속한다.
"""
    text = re.sub(r"current_focus:\n(?:- >-\n(?:  .*\n)+)+", current_focus, text, count=1, flags=re.MULTILINE)
    block = f"""

stage64_state_context_drawdown_smoothing:
  packet_id: {PACKET_ID}
  stage_id: {STAGE64_ID}
  status: closed_{decision}
  current_run_id: {RUN_ID}
  adapter_under_review: {SOURCE_ADAPTER_ID}
  source_stage63_pushed_commit: {SOURCE_STAGE63_COMMIT}
  target_surface: {TARGET_SURFACE}
  decision: {decision}
  next_stage_or_branch: {NEXT_STAGE_ID}
  report_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  external_verification_status: {external}
  boundary: {BOUNDARY}
"""
    if "stage64_state_context_drawdown_smoothing:" not in text:
        text = text.rstrip() + block
    io_path(WORKSPACE_STATE_PATH).write_text(text + ("\n" if not text.endswith("\n") else ""), encoding="utf-8")
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage64 Selection Status(64단계 선택 상태)

- stage_status(단계 상태): `closed_{decision}`
- source_stage(원천 단계): `63_adapter_research__v2_native_34d_target_followup`
- source_decision(원천 판정): `open_state_context_model_branch`
- current_run(현재 실행): `{RUN_ID}`
- adapter_under_review(검토 중 어댑터): `{SOURCE_ADAPTER_ID}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- stage64_decision(64단계 판정): `{decision}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage64(64단계)는 34D KPI target(34D 핵심 성과 지표 목표)을 향한 state/context gate(상태/문맥 게이트) batch(묶음)를 닫고, 운영 의미 없이 다음 경계 연구로 넘긴다.
""",
    )
    write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준): `research_package_only_reference_surface`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `{SOURCE_ADAPTER_ID}`
- status(상태): `stage64_closed_{decision}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage64(64단계) closed(종료) as v2-native state/context drawdown smoothing batch(브이투 고유 상태/문맥 손실률 완화 묶음). Effect(효과): legacy 34D(레거시 34D)는 target surface(목표 표면)로만 쓰였고, 다음 연구는 Stage65(65단계)로 이어진다.

## Latest Stage64 Evidence(최신 64단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- external_verification_status(외부 검증 상태): `{external}`
- report(보고서): `{rel(REPORT_PATH)}`
- stage64_decision(64단계 판정): `{rel(DECISION_PATH)}`
- gate_feature_summary(게이트 피처 요약): `{rel(GATE_FEATURE_SUMMARY_PATH)}`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속).
""",
    )
    create_next_stage(decision, external)


def create_next_stage(decision: str, external: str) -> None:
    write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage65(65단계)는 Stage64(64단계)의 state/context gate(상태/문맥 게이트) 결과를 받아, 34D KPI(34D 핵심 성과 지표)에 가까워질 수 있는 다음 bounded repair(경계 수정) 질문을 고르는 follow-up(후속) 단계다.

## Bounded Question(경계 질문)

Can the Stage64 state/context branch(64단계 상태/문맥 분기) produce a stronger v2-native adapter(브이투 고유 어댑터), or should the work move to a new model branch(새 모델 분기)?

Effect(효과): Stage65(65단계)는 Stage64(64단계) 결과를 무한 조정하지 않고, 다음 후보군을 하나의 측정 질문으로 좁힌다.

## Boundary(경계)

`{BOUNDARY}`

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage65 Input References(65단계 입력 참조)

- source_stage(원천 단계): `{STAGE64_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{decision}`
- source_external_verification_status(원천 외부 검증 상태): `{external}`
- stage64_report(64단계 보고서): `{rel(REPORT_PATH)}`
- stage64_decision(64단계 판정): `{rel(DECISION_PATH)}`
- gate_feature_summary(게이트 피처 요약): `{rel(GATE_FEATURE_SUMMARY_PATH)}`
- target_surface(목표 표면): `{TARGET_SURFACE}`

Effect(효과): 다음 단계는 34D KPI(34D 핵심 성과 지표)를 참고하되, v2 고유 근거만 입력으로 쓴다.
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage65 Review Index(65단계 검토 색인)

- status(상태): `open_planned`
- source_decision(원천 판정): `{decision}`
- planned_packet(계획 작업 묶음): `{NEXT_PACKET_ID}`
- planned_run(계획 실행): `{NEXT_RUN_ID}`

Effect(효과): Stage65(65단계)는 Stage64(64단계) closeout(종료 기록)을 이어받아 다음 bounded batch(경계 묶음 실행)만 검토한다.
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage65 Selection Status(65단계 선택 상태)

- stage_status(단계 상태): `open_planned`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE64_ID}`
- source_decision(원천 판정): `{decision}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage65(65단계)는 34D KPI(34D 핵심 성과 지표) 격차 축소를 계속하지만, 운영 의미 없이 연구개발로만 이어진다.
""",
    )


def append_changelog(decision: str) -> None:
    entry = (
        "\n## 2026-05-17 - Stage64 state/context drawdown smoothing closeout(64단계 상태/문맥 손실률 완화 종료)\n\n"
        f"- run(실행): `{RUN_ID}`\n"
        f"- decision(판정): `{decision}`\n"
        f"- target_surface(목표 표면): `{TARGET_SURFACE}`\n"
        "- effect(효과): Stage63(63단계) risk/ATR(위험/ATR) 후보를 복사 개발이 아니라 v2-native(브이투 고유) state/context gate(상태/문맥 게이트) 후보로 압박했다.\n"
    )
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID not in existing:
        io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def main(argv: Sequence[str] | None = None) -> int:
    configure_reused_engine()
    args = parse_args(argv or sys.argv[1:])
    inputs = prepare_inputs(Path(args.common_files_root))
    attempts = build_attempts(inputs)
    prepared = {
        "run_id": RUN_ID,
        "stage_id": STAGE64_ID,
        "stage_number": 64,
        "run_number": RUN_NUMBER,
        "run_root": RUN_ROOT,
        "packet_id": PACKET_ID,
        "attempts": attempts,
        "common_copies": inputs["common_copies"],
        "feature_exports": inputs["feature_exports"],
        "model_artifacts": inputs["model_exports"],
        "route_coverage": engine.route_coverage(),
        "model_family": "baseline_adapter_stage64_v2_native_state_context_gate_ebm_table",
        "feature_set_id": "stage64_run50bn_v41_state_context_gate_signal",
        "label_id": "label_v1_fwd12_m5_logret_train_q33_3class",
        "split_contract": "split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413",
        "claim_boundary": BOUNDARY,
        "target_surface": TARGET_SURFACE,
        "gate_rows": inputs["gate_rows"],
    }
    result = execute_or_materialize(prepared, args)
    audit_rows = s58.audit_rows_for_result(result, float(args.cost_stress_per_trade)) if result.get("mt5_kpi_records") else []
    risk_rows = s58.risk_rows_from_result(result)
    summary_rows = s58.build_summary_rows(result, audit_rows, risk_rows)
    segment_rows = s58.segment_kpi_rows(summary_rows)
    target_rows = target_progress_rows(summary_rows)
    external = str(result.get("external_verification_status") or "blocked")
    decision = decide(summary_rows, segment_rows, external)
    write_run_identity(result)
    write_csv(AUDIT_CSV_PATH, audit_rows)
    write_csv(SUMMARY_CSV_PATH, summary_rows)
    write_csv(SEGMENT_KPI_PATH, segment_rows)
    write_csv(RISK_ATR_TELEMETRY_PATH, risk_rows)
    write_csv(GATE_FEATURE_SUMMARY_PATH, inputs["gate_rows"])
    write_csv(TIER_B_DIAGNOSTIC_PATH, tier_b_rows())
    write_md(REPORT_PATH, report_markdown(summary_rows, segment_rows, target_rows, decision, external))
    write_md(DECISION_PATH, decision_markdown(decision, external))
    write_json(
        SUMMARY_JSON_PATH,
        {
            "run_id": RUN_ID,
            "decision": decision,
            "external_verification_status": external,
            "summary_rows": summary_rows,
            "segment_rows": segment_rows,
            "target_progress_rows": target_rows,
            "gate_rows": inputs["gate_rows"],
            "legacy_34d_targets": LEGACY_34D_TARGETS,
            "claim_boundary": BOUNDARY,
        },
    )
    artifacts = artifact_rows(result)
    ledger_payload = write_ledgers(result, decision, artifacts)
    write_packet_files(result, decision, ledger_payload)
    if not args.materialize_only:
        update_current_truth(decision, external)
        append_changelog(decision)
    print(
        json.dumps(
            json_ready(
                {
                    "status": "ok" if external == "completed" else "blocked",
                    "run_id": RUN_ID,
                    "decision": decision,
                    "external_verification_status": external,
                    "summary_csv": rel(SUMMARY_CSV_PATH),
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
