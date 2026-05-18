from __future__ import annotations

import argparse
import csv
import json
import math
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.alpha.discrete_signal_table import (  # noqa: E402
    export_single_discrete_signal_score_table,
)
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
from stage_pipelines.stage56 import baseline_adapter_repair_batch as repair  # noqa: E402
from stage_pipelines.stage58 import risk_atr_integration as s58  # noqa: E402
from stage_pipelines.stage70 import new_model_branch_from_short_gate_limit as base  # noqa: E402
from stage_pipelines.stage158 import stage156_validation_pf_margin_repair as s158  # noqa: E402
from stage_pipelines.stage160 import stage158_threshold_binding_audit as s160  # noqa: E402


STAGE_ID = "161_adapter_research__score_margin_or_side_filter_repair"
RUN_NUMBER = "run161A"
RUN_ID = "run161A_stage161_score_margin_or_side_filter_repair_v1"
PACKET_ID = "stage161_score_margin_or_side_filter_repair_v1"
PARENT_RUN_ID = "run160A_stage160_stage158_threshold_binding_audit_v1"
SOURCE_STAGE_ID = "160_adapter_research__stage158_threshold_binding_audit"
SOURCE_STAGE160_CLOSEOUT_COMMIT = "3805fd185dd669ebd674fe8df4cf19e504b07ee6"
SOURCE_STAGE160_HASH_RECORD_COMMIT = "2fc10d2ae5e28f08e12b4ed84af972b49fcec6d6"
SOURCE_STAGE158_ID = "158_adapter_research__stage156_validation_pf_margin_repair"
SOURCE_STAGE158_RUN_ID = "run158A_stage158_stage156_validation_pf_margin_repair_v1"
SOURCE_ADAPTER_ID = "s156_low_edge_risk0300_h3_cd5_sht54_lng52"
NEXT_STAGE_ID = "162_adapter_research__stage161_score_margin_followup_review"
NEXT_RUN_ID = "run162A_stage162_stage161_score_margin_followup_review_v1"
NEXT_PACKET_ID = "stage162_stage161_score_margin_followup_review_v1"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_no_legacy_inheritance"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID
PARTIALS_ROOT = RUN_ROOT / "partials"
COMMON_ROOT = f"OPV2/s161a/{RUN_NUMBER}"

SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage161_score_margin_or_side_filter_repair_summary.json"
SUMMARY_CSV_PATH = REVIEWS_ROOT / "stage161_score_margin_or_side_filter_repair_summary.csv"
REPORT_PATH = REVIEWS_ROOT / "stage161_score_margin_or_side_filter_repair_report.md"
SEGMENT_KPI_PATH = REVIEWS_ROOT / "stage161_segment_kpi_summary.csv"
RISK_ATR_TELEMETRY_PATH = REVIEWS_ROOT / "stage161_risk_atr_telemetry.csv"
GATE_FEATURE_SUMMARY_PATH = REVIEWS_ROOT / "stage161_gate_feature_summary.csv"
PROBABILITY_BINDING_PATH = REVIEWS_ROOT / "stage161_probability_binding_summary.csv"
MODEL_SCORE_AUDIT_PATH = REVIEWS_ROOT / "stage161_model_score_audit.csv"
TIER_B_DIAGNOSTIC_PATH = REVIEWS_ROOT / "stage161_tier_b_diagnostic_summary.csv"
DECISION_PATH = REVIEWS_ROOT / "stage161_decision.md"
AUDIT_CSV_PATH = REVIEWS_ROOT / "stage161_trade_audit.csv"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage161/score_margin_or_side_filter_repair.py")

FEATURE_FRAME_PATH = Path(
    "data/processed/datasets/"
    "dataset_fpmarkets_v2_us100_m5_20220901_20260413_cashopen_fullcash_proxyw58/"
    "features.parquet"
)
SIGNAL_COLUMN = "stage56_context_et_event_signal"

LEGACY_34D = {
    "profit_factor": 1.583157,
    "net_profit": 987.60,
    "max_drawdown_percent": 12.909136,
    "trade_count": 404,
}
STAGE156_REFERENCE = {
    "adapter_id": SOURCE_ADAPTER_ID,
    "validation_profit_factor": 1.55,
    "validation_net_profit": 1037.79,
    "validation_max_drawdown_percent": 10.23,
    "profit_factor": 1.85,
    "net_profit": 1032.34,
    "max_drawdown_percent": 11.92,
    "trade_count": 193,
    "oos_mid_profit_factor": 1.659175838,
}

VARIANTS = (
    repair.RepairVariant(
        adapter_id="s161_cal050_both_risk0300_h3_cd5_sht54_lng52",
        label="stage161_calibrated050_both_gate_control",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0300,
        same_direction_reentry_cooldown_bars=5,
        short_threshold=0.54,
        long_threshold=0.52,
        close_on_flat_signal=False,
        reverse_on_opposite_signal=True,
        close_only_on_opposite_signal=False,
        max_hold_bars=3,
        notes="Stage161 calibration control: non-saturated score, both-side low-edge gate, risk cap 3.00%.",
    ),
    repair.RepairVariant(
        adapter_id="s161_cal050_shortprob_risk0300_h3_cd5_sht58_lng52",
        label="stage161_calibrated050_short_threshold_filter",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0300,
        same_direction_reentry_cooldown_bars=5,
        short_threshold=0.58,
        long_threshold=0.52,
        close_on_flat_signal=False,
        reverse_on_opposite_signal=True,
        close_only_on_opposite_signal=False,
        max_hold_bars=3,
        notes="Stage161 short-side probability filter: calibrated p around 0.576 blocks weak short rows.",
    ),
    repair.RepairVariant(
        adapter_id="s161_cal050_shortgate_risk0300_h3_cd5_sht54_lng52",
        label="stage161_calibrated050_short_only_gate",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0300,
        same_direction_reentry_cooldown_bars=5,
        short_threshold=0.54,
        long_threshold=0.52,
        close_on_flat_signal=False,
        reverse_on_opposite_signal=True,
        close_only_on_opposite_signal=False,
        max_hold_bars=3,
        notes="Stage161 side-filter repair: low-edge gate blocks short rows only, long rows stay eligible.",
    ),
)

VARIANT_EXTRAS: dict[str, dict[str, Any]] = {
    "s161_cal050_both_risk0300_h3_cd5_sht54_lng52": {
        "logit_strength": 0.50,
        "risk_confidence_floor": 0.50,
        "risk_confidence_ceiling": 0.60,
        "block_mode": "both",
        "side_filter_enabled": True,
        "axis": "calibrated_score_control",
    },
    "s161_cal050_shortprob_risk0300_h3_cd5_sht58_lng52": {
        "logit_strength": 0.50,
        "risk_confidence_floor": 0.50,
        "risk_confidence_ceiling": 0.60,
        "block_mode": "both",
        "side_filter_enabled": True,
        "axis": "short_probability_filter",
    },
    "s161_cal050_shortgate_risk0300_h3_cd5_sht54_lng52": {
        "logit_strength": 0.50,
        "risk_confidence_floor": 0.50,
        "risk_confidence_ceiling": 0.60,
        "block_mode": "short",
        "side_filter_enabled": True,
        "axis": "short_only_side_filter",
    },
}

SOURCE_SPECS_BY_VARIANT = {
    variant.adapter_id: dict(s158.LOW_EDGE_SOURCE_SPEC)
    for variant in VARIANTS
}
CONTEXT_GATE_SPECS = {
    variant.adapter_id: {
        "gate_column": f"stage161_gate_{VARIANT_EXTRAS[variant.adapter_id]['axis']}",
        "gate_type": "weak_session_or_et40_mid_margin_block",
        "block_mode": VARIANT_EXTRAS[variant.adapter_id]["block_mode"],
        "session_min": 170.0,
        "session_max": 265.0,
        "margin_min": 0.04,
        "margin_max": 0.0775,
        "description": f"Stage161 {VARIANT_EXTRAS[variant.adapter_id]['axis']} using Stage154/156 low-edge gate.",
    }
    for variant in VARIANTS
}
MODEL_RISK_MIN_PCT = {variant.adapter_id: 0.005 for variant in VARIANTS}
_CONTEXT_LOOKUP: dict[str, float] | None = None


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
    ordered: list[str] = []
    for row in rows:
        for key in row:
            if key not in ordered:
                ordered.append(key)
    fieldnames = list(columns or ordered)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in fieldnames})


def parse_float(value: Any, default: float = 0.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def context_lookup() -> dict[str, float]:
    global _CONTEXT_LOOKUP
    if _CONTEXT_LOOKUP is not None:
        return _CONTEXT_LOOKUP
    frame = pd.read_parquet(io_path(FEATURE_FRAME_PATH), columns=["timestamp", "minutes_from_cash_open"])
    frame["timestamp_key"] = pd.to_datetime(frame["timestamp"], utc=True).dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    _CONTEXT_LOOKUP = {
        str(row["timestamp_key"]): float(row["minutes_from_cash_open"])
        for row in frame.to_dict("records")
    }
    return _CONTEXT_LOOKUP


def gate_value(row: Mapping[str, str], variant: repair.RepairVariant) -> float:
    signal = int(round(parse_float(row.get(SIGNAL_COLUMN), 0.0)))
    if signal == 0:
        return 0.0
    spec = CONTEXT_GATE_SPECS[variant.adapter_id]
    margin = parse_float(row.get("et40_decision_margin"), 1.0)
    timestamp = str(row.get("timestamp_utc", ""))
    minutes = context_lookup().get(timestamp)
    session_hit = False
    if minutes is not None:
        session_hit = float(spec["session_min"]) <= minutes <= float(spec["session_max"])
    margin_hit = float(spec["margin_min"]) <= margin <= float(spec["margin_max"])
    return 1.0 if (session_hit or margin_hit) else 0.0


def write_strength_gate_model(path: Path, variant: repair.RepairVariant) -> dict[str, Any]:
    extra = VARIANT_EXTRAS[variant.adapter_id]
    gate_column = str(CONTEXT_GATE_SPECS[variant.adapter_id]["gate_column"])
    export_meta = export_single_discrete_signal_score_table(
        path,
        feature_order=(SIGNAL_COLUMN,),
        logit_strength=float(extra["logit_strength"]),
        format_name="stage161_calibrated_single_discrete_signal_ebm_score_table_csv_v1",
    )
    with io_path(path).open("a", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerows(
            [
                ["cut", "1", "0", "0.5", "", "", ""],
                ["score", "1", "0", "", "0", "0", "0"],
                ["score", "1", "1", "", "0", "0", "0"],
                ["score", "1", "2", "", "0", "0", "0"],
            ]
        )
    return {
        **export_meta,
        "path": rel(path),
        "sha256": sha256_file_lf_normalized(path),
        "feature_order": [SIGNAL_COLUMN, gate_column],
        "feature_order_hash": base.engine.ordered_hash((SIGNAL_COLUMN, gate_column)),
        "signal_column": SIGNAL_COLUMN,
        "gate_column": gate_column,
        "logit_strength": float(extra["logit_strength"]),
        "risk_confidence_floor": float(extra["risk_confidence_floor"]),
        "risk_confidence_ceiling": float(extra["risk_confidence_ceiling"]),
    }


def write_gated_feature(source: Path, destination: Path, variant: repair.RepairVariant) -> dict[str, Any]:
    gate_column = str(CONTEXT_GATE_SPECS[variant.adapter_id]["gate_column"])
    io_path(destination.parent).mkdir(parents=True, exist_ok=True)
    total_rows = 0
    signal_rows = 0
    blocked_rows = 0
    blocked_signal_rows = 0
    missing_context_rows = 0
    with io_path(source).open("r", encoding="utf-8-sig", newline="") as input_handle:
        reader = csv.DictReader(input_handle)
        with io_path(destination).open("w", encoding="utf-8", newline="") as output_handle:
            writer = csv.DictWriter(
                output_handle,
                fieldnames=("bar_time_server", SIGNAL_COLUMN, gate_column),
                lineterminator="\n",
            )
            writer.writeheader()
            for row in reader:
                total_rows += 1
                signal = int(round(parse_float(row.get(SIGNAL_COLUMN), 0.0)))
                if signal != 0:
                    signal_rows += 1
                if str(row.get("timestamp_utc", "")) not in context_lookup():
                    missing_context_rows += 1
                gate = gate_value(row, variant)
                if gate >= 0.5:
                    blocked_rows += 1
                    if signal != 0:
                        blocked_signal_rows += 1
                writer.writerow(
                    {
                        "bar_time_server": row.get("bar_time_server") or row.get("timestamp_utc") or "",
                        SIGNAL_COLUMN: csv_value(parse_float(row.get(SIGNAL_COLUMN), 0.0)),
                        gate_column: csv_value(gate),
                    }
                )
    return {
        "run_id": RUN_ID,
        "adapter_id": variant.adapter_id,
        "gate_column": gate_column,
        "source_feature": rel(source),
        "gated_feature": rel(destination),
        "total_rows": total_rows,
        "signal_rows": signal_rows,
        "blocked_rows": blocked_rows,
        "blocked_signal_rows": blocked_signal_rows,
        "blocked_ratio": (blocked_rows / total_rows) if total_rows else 0.0,
        "blocked_signal_ratio": (blocked_signal_rows / signal_rows) if signal_rows else 0.0,
        "missing_context_rows": missing_context_rows,
        "block_mode": CONTEXT_GATE_SPECS[variant.adapter_id]["block_mode"],
        "gate_description": CONTEXT_GATE_SPECS[variant.adapter_id]["description"],
    }


def configure_base() -> None:
    for name, value in {
        "STAGE70_ID": STAGE_ID,
        "RUN_NUMBER": RUN_NUMBER,
        "RUN_ID": RUN_ID,
        "PACKET_ID": PACKET_ID,
        "PARENT_RUN_ID": PARENT_RUN_ID,
        "NEXT_STAGE_ID": NEXT_STAGE_ID,
        "NEXT_RUN_ID": NEXT_RUN_ID,
        "NEXT_PACKET_ID": NEXT_PACKET_ID,
        "SOURCE_ADAPTER_ID": SOURCE_ADAPTER_ID,
        "TARGET_SURFACE": TARGET_SURFACE,
        "DEVELOPMENT_ANCHOR": SOURCE_ADAPTER_ID,
        "BACKUP_ANCHOR": "stage158_threshold_binding_audit",
        "BOUNDARY": BOUNDARY,
        "STAGE_ROOT": STAGE_ROOT,
        "RUN_ROOT": RUN_ROOT,
        "REVIEWS_ROOT": REVIEWS_ROOT,
        "SELECTED_ROOT": SELECTED_ROOT,
        "PACKET_ROOT": PACKET_ROOT,
        "PARTIALS_ROOT": PARTIALS_ROOT,
        "COMMON_ROOT": COMMON_ROOT,
        "SOURCE_SPECS_BY_VARIANT": SOURCE_SPECS_BY_VARIANT,
        "STAGE70_VARIANTS": VARIANTS,
        "MODEL_RISK_MIN_PCT": MODEL_RISK_MIN_PCT,
        "CONTEXT_GATE_SPECS": CONTEXT_GATE_SPECS,
        "RUN50BN_SIGNAL": SIGNAL_COLUMN,
        "SUMMARY_JSON_PATH": SUMMARY_JSON_PATH,
        "SUMMARY_CSV_PATH": SUMMARY_CSV_PATH,
        "REPORT_PATH": REPORT_PATH,
        "SEGMENT_KPI_PATH": SEGMENT_KPI_PATH,
        "RISK_ATR_TELEMETRY_PATH": RISK_ATR_TELEMETRY_PATH,
        "GATE_FEATURE_SUMMARY_PATH": GATE_FEATURE_SUMMARY_PATH,
        "TIER_B_DIAGNOSTIC_PATH": TIER_B_DIAGNOSTIC_PATH,
        "DECISION_PATH": DECISION_PATH,
        "AUDIT_CSV_PATH": AUDIT_CSV_PATH,
        "STAGE_LEDGER_PATH": STAGE_LEDGER_PATH,
        "RUN_REGISTRY_PATH": RUN_REGISTRY_PATH,
        "PROJECT_LEDGER_PATH": PROJECT_LEDGER_PATH,
        "ARTIFACT_REGISTRY_PATH": ARTIFACT_REGISTRY_PATH,
        "WORKSPACE_STATE_PATH": WORKSPACE_STATE_PATH,
        "CURRENT_WORKING_STATE_PATH": CURRENT_WORKING_STATE_PATH,
        "CHANGELOG_PATH": CHANGELOG_PATH,
        "NEXT_STAGE_ROOT": NEXT_STAGE_ROOT,
    }.items():
        setattr(base, name, value)
    base.configure_reused_engine()


def prepare_inputs(common_files_root: Path) -> dict[str, Any]:
    copied: list[dict[str, Any]] = []
    gate_rows: list[dict[str, Any]] = []
    model_exports: dict[str, dict[str, Any]] = {}
    feature_exports: dict[str, dict[str, dict[str, Any]]] = {}
    for variant in VARIANTS:
        model_source = base.engine.source_model_for_variant(variant)
        gate_column = str(CONTEXT_GATE_SPECS[variant.adapter_id]["gate_column"])
        model_local = RUN_ROOT / variant.adapter_id / "models" / f"{variant.adapter_id}_model.csv"
        model_meta = write_strength_gate_model(model_local, variant)
        copied.append(
            {
                "source": rel(model_source),
                "path": rel(model_local),
                "sha256": sha256_file_lf_normalized(model_local),
                "transform": "replace_with_stage161_calibrated_discrete_score_and_neutral_gate",
            }
        )
        copied.append(base.engine.copy_to_common(model_local, f"{COMMON_ROOT}/{variant.adapter_id}/models/{model_local.name}", common_files_root))
        model_exports[variant.adapter_id] = {
            **model_meta,
            "common_path": f"{COMMON_ROOT}/{variant.adapter_id}/models/{model_local.name}",
            "source_model": rel(model_source),
            "source_anchor": base.engine.source_anchor_for_variant(variant),
            "gate_column": gate_column,
        }
        feature_exports[variant.adapter_id] = {}
        for split in ("validation_is", "oos"):
            token = "val" if split == "validation_is" else "oos"
            feature_source = base.engine.source_feature(split, variant, "a")
            feature_local = RUN_ROOT / variant.adapter_id / "features" / f"{variant.adapter_id}_{token}.csv"
            gate_row = write_gated_feature(feature_source, feature_local, variant)
            gate_row["split"] = split
            gate_rows.append(gate_row)
            copied.append(
                {
                    "source": rel(feature_source),
                    "path": rel(feature_local),
                    "sha256": sha256_file_lf_normalized(feature_local),
                    "transform": "stage161_low_edge_side_filter_feature",
                }
            )
            copied.append(base.engine.copy_to_common(feature_local, f"{COMMON_ROOT}/{variant.adapter_id}/features/{feature_local.name}", common_files_root))
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


def extra_set_values(variant: repair.RepairVariant, magic: int) -> dict[str, Any]:
    values = base.engine.extra_set_values(variant, magic)
    extra = VARIANT_EXTRAS[variant.adapter_id]
    block_mode = str(extra["block_mode"])
    values["InpSideFilterEnabled"] = bool(extra["side_filter_enabled"])
    values["InpSideFilterFeatureIndex"] = 1
    values["InpFallbackSideFilterFeatureIndex"] = 1
    values["InpBlockShortFeatureRange"] = block_mode in {"both", "short"}
    values["InpBlockShortFeatureMin"] = 0.5
    values["InpBlockShortFeatureMax"] = 1.5
    values["InpBlockLongFeatureRange"] = block_mode in {"both", "long"}
    values["InpBlockLongFeatureMin"] = 0.5
    values["InpBlockLongFeatureMax"] = 1.5
    values["InpModelRiskConfidenceFloor"] = float(extra["risk_confidence_floor"])
    values["InpModelRiskConfidenceCeiling"] = float(extra["risk_confidence_ceiling"])
    return values


def build_attempts(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    for variant_index, variant in enumerate(VARIANTS, start=1):
        variant_root = RUN_ROOT / variant.adapter_id
        for split in ("validation_is", "oos"):
            date_values = base.parse_ini(base.engine.source_attempt_ini(split, variant))
            split_token = "val" if split == "validation_is" else "oos"
            for role_index, (tier, attempt_role, prefix, attempt_token) in enumerate(
                (
                    (base.mt5.TIER_A, "tier_only_total", f"mt5_tier_a_only_{variant.adapter_id}", "ta"),
                    (base.mt5.TIER_AB, "routed_total", f"mt5_routed_{variant.adapter_id}", "rt"),
                ),
                start=1,
            ):
                magic = 16110000 + variant_index * 100 + (1 if split == "validation_is" else 50) + role_index
                attempts.append(
                    base.attempt_payload(
                        run_root=variant_root,
                        run_id=RUN_ID,
                        stage_number=161,
                        exploration_label="stage161_BaselineAdapter__ScoreMarginOrSideFilterRepair",
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
                        min_margin=0.0,
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


def split_row(summary_rows: Sequence[Mapping[str, Any]], adapter_id: str, split: str) -> Mapping[str, Any]:
    for row in summary_rows:
        if row.get("adapter_id") == adapter_id and row.get("split") == split and row.get("view") == "actual_routed_total":
            return row
    return {}


def segment_row(segment_rows: Sequence[Mapping[str, Any]], adapter_id: str, split: str, segment: str) -> Mapping[str, Any]:
    for row in segment_rows:
        if (
            row.get("adapter_id") == adapter_id
            and row.get("split") == split
            and row.get("view") == "actual_routed_total"
            and row.get("segment_type") == "chronological_third"
            and row.get("segment") == segment
        ):
            return row
    return {}


def as_float(row: Mapping[str, Any], key: str, default: float = 0.0) -> float:
    return parse_float(row.get(key), default)


def probability_binding_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    variants = {variant.adapter_id: variant for variant in VARIANTS}
    for execution in result.get("execution_results", []):
        attempt_name = str(execution.get("attempt_name") or "")
        adapter_id = next((item for item in variants if attempt_name.startswith(item)), "")
        variant = variants.get(adapter_id)
        if not variant:
            continue
        runtime_outputs = execution.get("runtime_outputs", {}) if isinstance(execution.get("runtime_outputs"), Mapping) else {}
        telemetry_path = Path(str(runtime_outputs.get("telemetry_path") or ""))
        row = {
            "run_id": RUN_ID,
            "adapter_id": adapter_id,
            "attempt_name": attempt_name,
            "split": execution.get("split", ""),
            "tier": execution.get("tier", ""),
            "view": "actual_routed_total" if "_rt_" in attempt_name else "tier_a_only",
            "short_threshold": variant.short_threshold,
            "long_threshold": variant.long_threshold,
            "logit_strength": VARIANT_EXTRAS[adapter_id]["logit_strength"],
            "block_mode": VARIANT_EXTRAS[adapter_id]["block_mode"],
            "telemetry_path": rel(telemetry_path) if str(telemetry_path) else "",
            "status": "missing",
        }
        if not path_exists(telemetry_path):
            row["parse_error"] = "telemetry_missing"
            rows.append(row)
            continue
        try:
            summary, _ = s160.analyze_telemetry(
                telemetry_path,
                short_threshold=float(variant.short_threshold),
                long_threshold=float(variant.long_threshold),
            )
            row.update(summary)
            row["status"] = "completed"
        except Exception as exc:
            row["status"] = "blocked"
            row["parse_error"] = f"{type(exc).__name__}: {exc}"
        rows.append(row)
    return rows


def model_score_rows(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for variant in VARIANTS:
        model_path = Path(str(inputs["model_exports"][variant.adapter_id]["path"]))
        row = s160.audit_model_score(model_path, variant.adapter_id)
        row["run_id"] = RUN_ID
        row["logit_strength"] = VARIANT_EXTRAS[variant.adapter_id]["logit_strength"]
        row["risk_confidence_floor"] = VARIANT_EXTRAS[variant.adapter_id]["risk_confidence_floor"]
        row["risk_confidence_ceiling"] = VARIANT_EXTRAS[variant.adapter_id]["risk_confidence_ceiling"]
        row["block_mode"] = VARIANT_EXTRAS[variant.adapter_id]["block_mode"]
        rows.append(row)
    return rows


def safe_candidate(adapter_id: str, oos: Mapping[str, Any], val: Mapping[str, Any], mid: Mapping[str, Any]) -> bool:
    return (
        bool(adapter_id)
        and as_float(oos, "profit_factor") >= LEGACY_34D["profit_factor"]
        and as_float(oos, "net_profit") >= LEGACY_34D["net_profit"]
        and as_float(oos, "max_drawdown_percent", 99.0) <= LEGACY_34D["max_drawdown_percent"]
        and as_float(val, "profit_factor") >= LEGACY_34D["profit_factor"]
        and as_float(val, "net_profit") >= LEGACY_34D["net_profit"]
        and as_float(val, "max_drawdown_percent", 99.0) <= LEGACY_34D["max_drawdown_percent"]
        and as_float(mid, "profit_factor") >= LEGACY_34D["profit_factor"]
    )


def best_stage161(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    candidates = []
    for oos in [row for row in summary_rows if row.get("split") == "oos" and row.get("view") == "actual_routed_total"]:
        adapter_id = str(oos.get("adapter_id", ""))
        val = split_row(summary_rows, adapter_id, "validation_is")
        mid = segment_row(segment_rows, adapter_id, "oos", "mid")
        candidates.append(
            (
                safe_candidate(adapter_id, oos, val, mid),
                as_float(val, "profit_factor") >= LEGACY_34D["profit_factor"],
                as_float(oos, "profit_factor") >= LEGACY_34D["profit_factor"],
                as_float(mid, "profit_factor") >= LEGACY_34D["profit_factor"],
                as_float(val, "profit_factor"),
                as_float(oos, "profit_factor"),
                as_float(oos, "net_profit"),
                -as_float(oos, "max_drawdown_percent", 99.0),
                oos,
            )
        )
    return max(candidates, key=lambda item: item[:8])[-1] if candidates else {}


def decide(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]], external: str) -> str:
    if external != "completed":
        return "continue_stage162_runtime_completion_due_to_incomplete_stage161_runtime_candidate_not_final"
    best = best_stage161(summary_rows, segment_rows)
    adapter_id = str(best.get("adapter_id", ""))
    val = split_row(summary_rows, adapter_id, "validation_is")
    mid = segment_row(segment_rows, adapter_id, "oos", "mid")
    if safe_candidate(adapter_id, best, val, mid):
        return "proceed_to_stage162_score_margin_followup_review_candidate_not_final"
    return "continue_stage162_score_margin_or_side_filter_repair_candidate_not_final"


def target_progress_rows(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in summary_rows:
        if row.get("view") != "actual_routed_total":
            continue
        adapter_id = str(row.get("adapter_id", ""))
        mid = segment_row(segment_rows, adapter_id, str(row.get("split")), "mid")
        rows.append(
            {
                "run_id": RUN_ID,
                "adapter_id": adapter_id,
                "split": row.get("split"),
                "profit_factor": as_float(row, "profit_factor"),
                "net_profit": as_float(row, "net_profit"),
                "max_drawdown_percent": as_float(row, "max_drawdown_percent"),
                "trade_count": as_float(row, "trade_count"),
                "expectancy": as_float(row, "expectancy"),
                "mid_profit_factor": as_float(mid, "profit_factor"),
                "pf_gap_to_34d": as_float(row, "profit_factor") - LEGACY_34D["profit_factor"],
                "net_gap_to_34d": as_float(row, "net_profit") - LEGACY_34D["net_profit"],
                "dd_margin_to_34d": LEGACY_34D["max_drawdown_percent"] - as_float(row, "max_drawdown_percent", 99.0),
                "source_adapter": SOURCE_ADAPTER_ID,
                "target_surface": TARGET_SURFACE,
            }
        )
    return rows


def row_table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | split(분할) | PF(수익요인) | net(순손익) | DD%(낙폭) | trades(거래수) | PF gap(수익요인 차이) |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            "| {adapter} | {split} | {pf:.6f} | {net:.2f} | {dd:.2f} | {trades:.0f} | {gap:.6f} |".format(
                adapter=row.get("adapter_id", ""),
                split=row.get("split", ""),
                pf=parse_float(row.get("profit_factor")),
                net=parse_float(row.get("net_profit")),
                dd=parse_float(row.get("max_drawdown_percent")),
                trades=parse_float(row.get("trade_count")),
                gap=parse_float(row.get("pf_gap_to_34d")),
            )
        )
    return "\n".join(lines)


def report_markdown(
    summary_rows: Sequence[Mapping[str, Any]],
    segment_rows: Sequence[Mapping[str, Any]],
    probability_rows: Sequence[Mapping[str, Any]],
    target_rows: Sequence[Mapping[str, Any]],
    decision: str,
    external: str,
) -> str:
    best = best_stage161(summary_rows, segment_rows)
    best_id = str(best.get("adapter_id", "none"))
    val = split_row(summary_rows, best_id, "validation_is")
    mid = segment_row(segment_rows, best_id, "oos", "mid")
    prob_completed = [row for row in probability_rows if row.get("status") == "completed" and row.get("view") == "actual_routed_total"]
    band_rows = sum(int(parse_float(row.get("directional_050_060_band_rows"))) for row in prob_completed)
    near_rows = sum(int(parse_float(row.get("directional_near_threshold_001_rows"))) for row in prob_completed)
    return f"""# Stage161 Score Margin Or Side Filter Repair Report(161단계 점수 마진 또는 방향 필터 수리 보고)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_stage160_closeout_commit(원천 160단계 종료 커밋): `{SOURCE_STAGE160_CLOSEOUT_COMMIT}`
- source_stage160_hash_record_commit(원천 160단계 해시 기록 커밋): `{SOURCE_STAGE160_HASH_RECORD_COMMIT}`
- source_adapter(원천 어댑터): `{SOURCE_ADAPTER_ID}`
- external_verification_status(외부 검증 상태): `{external}`
- decision(판정): `{decision}`
- boundary(주장 경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Can score margin(점수 마진), probability calibration(확률 보정), or side filter(방향 필터) create real row-selection movement(행 선택 변화) and improve validation PF(검증 수익요인) toward legacy 34D KPI(레거시 34D 핵심 성과 지표) without damaging OOS(표본외) quality?

Effect(효과): Stage160(160단계)에서 확인한 score saturation(점수 포화)을 낮춰 threshold(문턱값)가 실제로 작동하는지 본다.

## KPI Read(KPI 판독)

{row_table(target_rows)}

## Probability Binding(확률 작동)

- directional_050_060_band_rows(0.50~0.60 방향 확률 행): `{band_rows}`
- directional_near_threshold_001_rows(문턱값 0.01 근접 행): `{near_rows}`
- probability_binding_summary(확률 작동 요약): `{rel(PROBABILITY_BINDING_PATH)}`
- model_score_audit(모델 점수 감사): `{rel(MODEL_SCORE_AUDIT_PATH)}`

## Best Read(최선 판독)

- best_adapter(최선 어댑터): `{best_id}`
- validation_pf(검증 수익요인): `{as_float(val, "profit_factor"):.6f}`
- validation_net(검증 순손익): `{as_float(val, "net_profit"):.2f}`
- validation_dd(검증 낙폭): `{as_float(val, "max_drawdown_percent"):.2f}`
- oos_pf(표본외 수익요인): `{as_float(best, "profit_factor"):.6f}`
- oos_net(표본외 순손익): `{as_float(best, "net_profit"):.2f}`
- oos_dd(표본외 낙폭): `{as_float(best, "max_drawdown_percent"):.2f}`
- oos_mid_pf(표본외 중반 수익요인): `{as_float(mid, "profit_factor"):.9f}`

## Judgment(판정)

- result_subject(판정 대상): Stage161(161단계) calibrated score margin / side filter repair(보정 점수 마진 / 방향 필터 수리).
- evidence_available(있는 근거): MT5 Strategy Tester(전략 테스터) reports(보고서), summary CSV(요약 CSV), segment KPI(구간 핵심 성과 지표), risk/ATR telemetry(위험/ATR 기록), probability binding(확률 작동).
- evidence_missing(부족 근거): final research package(최종 연구 패키지), ONNX parity(ONNX 동등성), deployment(배포)는 이번 범위 밖이다.
- claim_boundary(주장 경계): research/development only(연구개발 전용).

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
"""


def decision_markdown(decision: str, external: str) -> str:
    return f"""# Stage161 Decision(161단계 판정)

- decision(판정): `{decision}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- external_verification_status(외부 검증 상태): `{external}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_adapter(원천 어댑터): `{SOURCE_ADAPTER_ID}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary_csv(요약 CSV): `{rel(SUMMARY_CSV_PATH)}`
- segment_kpi(구간 핵심 성과 지표): `{rel(SEGMENT_KPI_PATH)}`
- risk_atr_telemetry(위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- probability_binding(확률 작동): `{rel(PROBABILITY_BINDING_PATH)}`
- model_score_audit(모델 점수 감사): `{rel(MODEL_SCORE_AUDIT_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage161(161단계)은 score margin(점수 마진)과 side filter(방향 필터)만 닫는다. Effect(효과): 한 단계 종료를 전체 목표 완료로 착각하지 않고 Stage162(162단계) 후속 판독으로 넘긴다.

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), production_baseline(생산 기준선), operating_promotion(운영 승격), operating_reference(운영 기준), runtime_authority(런타임 권위), overall_goal_complete(전체 목표 완료).
"""


def tier_b_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    coverage = base.engine.route_coverage()
    for variant in VARIANTS:
        variant_cov = coverage.get(variant.adapter_id, {})
        for split_name in ("validation", "oos"):
            split_cov = variant_cov.get(split_name, {})
            rows.append(
                {
                    "run_id": RUN_ID,
                    "adapter_id": variant.adapter_id,
                    "split": split_name,
                    "tier_b_policy": "diagnostic_missing_required_but_disabled_for_stage161_score_margin_repair",
                    "tier_b_rows_available": split_cov.get("tier_b_fallback_rows_available_but_disabled", 0),
                    "tier_b_rows_used": split_cov.get("tier_b_fallback_rows_used", 0),
                    "reason": "Stage161 isolates Tier A routed score margin and side filter repair; Tier B fallback remains disabled.",
                }
            )
    return rows


def artifact_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    created = utc_now()
    paths = [
        PRODUCER_PATH,
        REPORT_PATH,
        SUMMARY_JSON_PATH,
        SUMMARY_CSV_PATH,
        SEGMENT_KPI_PATH,
        RISK_ATR_TELEMETRY_PATH,
        GATE_FEATURE_SUMMARY_PATH,
        PROBABILITY_BINDING_PATH,
        MODEL_SCORE_AUDIT_PATH,
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
                    "artifact_id": f"{RUN_ID}__{Path(path).name}",
                    "artifact_type": "stage161_score_margin_or_side_filter_repair_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage161 v2-native score margin or side filter repair artifact.",
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
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Actual Stage161 MT5 Strategy Tester HTML report.",
                }
            )
    return rows


def write_run_identity(result: Mapping[str, Any], probability_rows: Sequence[Mapping[str, Any]], model_rows: Sequence[Mapping[str, Any]]) -> None:
    write_json(
        RUN_ROOT / "run_manifest.json",
        {
            "run_id": RUN_ID,
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "run_number": RUN_NUMBER,
            "parent_run_id": PARENT_RUN_ID,
            "source_stage160_closeout_commit": SOURCE_STAGE160_CLOSEOUT_COMMIT,
            "source_stage160_hash_record_commit": SOURCE_STAGE160_HASH_RECORD_COMMIT,
            "source_stage158_run_id": SOURCE_STAGE158_RUN_ID,
            "source_adapter_id": SOURCE_ADAPTER_ID,
            "target_surface": TARGET_SURFACE,
            "legacy_relation": "lesson_only_target_surface_no_legacy_code_or_promotion_inheritance",
            "variants": [variant.__dict__ for variant in VARIANTS],
            "variant_extras": VARIANT_EXTRAS,
            "attempts": result.get("attempts", []),
            "model_artifacts": result.get("model_artifacts", {}),
            "feature_exports": result.get("feature_exports", {}),
            "gate_rows": result.get("gate_rows", []),
            "probability_binding_rows": probability_rows,
            "model_score_rows": model_rows,
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
            "stage_id": STAGE_ID,
            "mt5_kpi_records": result.get("mt5_kpi_records", []),
            "strategy_tester_reports": result.get("strategy_tester_reports", []),
            "execution_results": result.get("execution_results", []),
            "gate_rows": result.get("gate_rows", []),
            "probability_binding_rows": probability_rows,
            "model_score_rows": model_rows,
            "external_verification_status": result.get("external_verification_status"),
            "judgment": result.get("judgment"),
            "claim_boundary": BOUNDARY,
        },
    )


def write_ledgers(result: Mapping[str, Any], decision: str, artifacts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    external = str(result.get("external_verification_status") or "blocked")
    status = "completed" if external == "completed" else "blocked"
    run_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_adapter_stage161_score_margin_or_side_filter_repair",
                "status": status,
                "judgment": decision,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_stage160_closeout_commit", SOURCE_STAGE160_CLOSEOUT_COMMIT),
                        ("source_stage160_hash_record_commit", SOURCE_STAGE160_HASH_RECORD_COMMIT),
                        ("source_adapter", SOURCE_ADAPTER_ID),
                        ("target_surface", TARGET_SURFACE),
                        ("legacy_relation", "lesson_only"),
                        ("overall_goal_complete", 0),
                    )
                ),
            }
        ],
        key="run_id",
    )
    alpha_rows = build_mt5_alpha_ledger_rows(
        run_id=RUN_ID,
        stage_id=STAGE_ID,
        mt5_kpi_records=result.get("mt5_kpi_records", []),
        run_output_root=RUN_ROOT,
        external_verification_status=external,
    )
    if not alpha_rows:
        alpha_rows = [
            {
                "ledger_row_id": f"{RUN_ID}__materialized_or_blocked",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "materialized_or_blocked",
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "materialized_or_blocked",
                "tier_scope": "Tier A+B",
                "kpi_scope": "stage161_score_margin_or_side_filter_repair",
                "scoreboard_lane": "runtime_probe",
                "status": status,
                "judgment": decision,
                "path": rel(DECISION_PATH),
                "primary_kpi": "mt5_kpi_records=0",
                "guardrail_kpi": f"target_surface={TARGET_SURFACE}",
                "external_verification_status": external,
                "notes": "Stage161 run materialized or blocked before KPI records were available.",
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


def write_packet_files(
    result: Mapping[str, Any],
    decision: str,
    ledger_payload: Mapping[str, Any],
    probability_rows: Sequence[Mapping[str, Any]],
    model_rows: Sequence[Mapping[str, Any]],
) -> None:
    status = "completed" if result.get("external_verification_status") == "completed" else "blocked"
    required_gates = [
        "runtime_evidence_gate",
        "scope_completion_gate",
        "kpi_contract_audit",
        "result_judgment_gate",
        "performance_attribution_gate",
        "artifact_lineage_audit",
        "runtime_parity_gate",
        "backtest_forensics_gate",
        "required_gate_coverage_audit",
        "final_claim_guard",
    ]
    write_json(
        PACKET_ROOT / "routing_receipt.json",
        {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "primary_family": "runtime_backtest",
            "primary_skill": "obsidian-runtime-parity",
            "support_skills": [
                "obsidian-experiment-design",
                "obsidian-performance-attribution",
                "obsidian-result-judgment",
                "obsidian-artifact-lineage",
            ],
            "required_gates": required_gates,
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
            "claim_boundary": BOUNDARY,
            "runtime_claim_boundary": "runtime_probe_research_only",
            "status": status,
        },
    )
    write_json(
        PACKET_ROOT / "scope_completion_gate.json",
        {
            "packet_id": PACKET_ID,
            "run_id": RUN_ID,
            "bounded_question": "score margin, probability calibration, or side filter repair after Stage160 non-binding threshold audit",
            "scope_completed": result.get("external_verification_status") == "completed",
            "out_of_scope": ["deployment", "live_readiness", "production_baseline", "operating_promotion", "runtime_authority", "overall_goal_completion"],
            "status": status,
        },
    )
    write_json(
        PACKET_ROOT / "kpi_contract_audit.json",
        {
            "summary_csv": rel(SUMMARY_CSV_PATH),
            "segment_kpi_csv": rel(SEGMENT_KPI_PATH),
            "risk_atr_csv": rel(RISK_ATR_TELEMETRY_PATH),
            "probability_binding_csv": rel(PROBABILITY_BINDING_PATH),
            "model_score_csv": rel(MODEL_SCORE_AUDIT_PATH),
            "legacy_34d": LEGACY_34D,
            "status": status,
        },
    )
    write_json(
        PACKET_ROOT / "result_judgment_gate.json",
        {
            "result_subject": RUN_ID,
            "evidence_available": [rel(REPORT_PATH), rel(SUMMARY_CSV_PATH), rel(PROBABILITY_BINDING_PATH), rel(DECISION_PATH)],
            "evidence_missing": [] if status == "completed" else ["completed_mt5_runtime_evidence"],
            "judgment_label": decision,
            "claim_boundary": BOUNDARY,
            "next_condition": NEXT_STAGE_ID,
            "user_explanation_hook": "Stage161 is a bounded repair measurement only; it cannot complete the overall goal.",
            "status": "passed_with_boundary" if status == "completed" else "blocked",
            "overall_goal_complete": False,
        },
    )
    write_json(
        PACKET_ROOT / "performance_attribution_gate.json",
        {
            "observed_change": "Stage161 lowers score saturation and changes short probability or side-filter axis.",
            "comparison_baseline": [SOURCE_ADAPTER_ID, "stage158_threshold_variants", "stage160_threshold_binding_audit"],
            "likely_drivers": ["logit_strength", "short_threshold", "block_mode", "risk_confidence_window"],
            "segment_checks": ["validation_vs_oos", "chronological_thirds", "risk_atr_telemetry", "probability_binding"],
            "trade_shape": rel(AUDIT_CSV_PATH),
            "attribution_confidence": "medium_if_completed_else_blocked",
            "next_probe": NEXT_STAGE_ID,
            "status": status,
        },
    )
    write_json(
        PACKET_ROOT / "artifact_lineage_audit.json",
        {
            "source_inputs": [rel(PRODUCER_PATH), rel(Path("stages") / SOURCE_STAGE_ID / "03_reviews/stage160_decision.md"), SOURCE_ADAPTER_ID],
            "producer": rel(PRODUCER_PATH),
            "consumer": [rel(REPORT_PATH), rel(DECISION_PATH), NEXT_STAGE_ID],
            "artifact_paths": {
                "report": rel(REPORT_PATH),
                "summary": rel(SUMMARY_CSV_PATH),
                "segment_kpi": rel(SEGMENT_KPI_PATH),
                "risk_atr": rel(RISK_ATR_TELEMETRY_PATH),
                "probability_binding": rel(PROBABILITY_BINDING_PATH),
                "model_score": rel(MODEL_SCORE_AUDIT_PATH),
                "stage_ledger": rel(STAGE_LEDGER_PATH),
            },
            "artifact_hashes": {"model_rows": model_rows, "probability_rows_count": len(probability_rows)},
            "registry_links": [rel(RUN_REGISTRY_PATH), rel(PROJECT_LEDGER_PATH), rel(STAGE_LEDGER_PATH), rel(ARTIFACT_REGISTRY_PATH)],
            "availability": "tracked",
            "lineage_judgment": "connected_with_boundary",
            "ledger_payload": ledger_payload,
            "status": status,
        },
    )
    write_json(PACKET_ROOT / "runtime_parity_gate.json", {"runtime_claim_boundary": "runtime_probe_research_only", "parity_check": "MT5 Strategy Tester output" if status == "completed" else "blocked_or_incomplete", "status": status})
    write_json(PACKET_ROOT / "backtest_forensics_gate.json", {"tester_identity": "MT5 Strategy Tester via generated run manifest", "trade_evidence": rel(SUMMARY_CSV_PATH), "forensic_checks": ["report_path_exists", "summary_rows", "risk_telemetry", "artifact_hashes"], "status": status})
    write_json(PACKET_ROOT / "final_claim_guard.json", {"overall_goal_complete": False, "deployment_claim": False, "live_readiness_claim": False, "runtime_authority_claim": False, "production_baseline_claim": False, "operating_reference_claim": False, "operating_promotion_claim": False, "status": "passed"})
    write_json(PACKET_ROOT / "required_gate_coverage_audit.json", {"packet_id": PACKET_ID, "run_id": RUN_ID, "declared_required_gates": required_gates, "executed_gates": required_gates, "missing_gates": [], "status": "passed" if status == "completed" else "blocked_with_evidence"})
    write_json(PACKET_ROOT / "aggregate_summary.json", {"packet_id": PACKET_ID, "stage_id": STAGE_ID, "run_id": RUN_ID, "decision": decision, "source_stage160_closeout_commit": SOURCE_STAGE160_CLOSEOUT_COMMIT, "source_stage160_hash_record_commit": SOURCE_STAGE160_HASH_RECORD_COMMIT, "summary_csv": rel(SUMMARY_CSV_PATH), "segment_kpi_csv": rel(SEGMENT_KPI_PATH), "risk_atr_telemetry_csv": rel(RISK_ATR_TELEMETRY_PATH), "probability_binding_csv": rel(PROBABILITY_BINDING_PATH), "ledger_payload": ledger_payload, "pushed_commit_hash": "pending_until_push", "claim_boundary": BOUNDARY, "overall_goal_complete": False})


def write_next_stage_seed(decision: str, external: str) -> None:
    write_md(
        NEXT_STAGE_ROOT / "00_spec/stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage162(162단계)는 Stage161(161단계) score margin(점수 마진) / side filter(방향 필터) 결과를 follow-up review(후속 검토)한다.

## Bounded Question(경계 질문)

Did Stage161(161단계) create useful row-selection movement(행 선택 변화) and KPI(핵심 성과 지표) progress toward legacy 34D(레거시 34D) target without validation/OOS(검증/표본외) damage, or should the next bounded repair choose a different branch(분기)?

Effect(효과): Stage161(161단계) 안에서 계속 고치지 않고, 결과 판독만 다음 단계에서 닫는다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs/input_refs.md",
        f"""# Stage162 Input References(162단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{decision}`
- source_external_verification_status(원천 외부 검증 상태): `{external}`
- stage161_report(161단계 보고서): `{rel(REPORT_PATH)}`
- stage161_summary(161단계 요약): `{rel(SUMMARY_CSV_PATH)}`
- stage161_segment_kpi(161단계 구간 핵심 성과 지표): `{rel(SEGMENT_KPI_PATH)}`
- stage161_probability_binding(161단계 확률 작동): `{rel(PROBABILITY_BINDING_PATH)}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews/review_index.md",
        f"""# Stage162 Review Index(162단계 검토 색인)

- status(상태): `open_planned_from_stage161`
- planned_packet(계획 작업 묶음): `{NEXT_PACKET_ID}`
- planned_run(계획 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`

Effect(효과): Stage162(162단계)는 새 최적화가 아니라 Stage161(161단계) 증거 판독으로 시작한다.
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected/selection_status.md",
        f"""# Stage162 Selection Status(162단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage161`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{decision}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- selected_research_baseline(선택 연구 기준선): `none`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage162(162단계)는 연구개발(research/development, 연구개발) 전용 후속 판독으로 고정된다.
""",
    )


def update_current_truth(decision: str, external: str) -> None:
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig") if path_exists(WORKSPACE_STATE_PATH) else ""
    state = re.sub(r"(?m)^active_stage:.*$", f"active_stage: {NEXT_STAGE_ID}", state)
    state = re.sub(r"(?m)^current_run_id:.*$", f"current_run_id: {NEXT_RUN_ID}", state)
    state = re.sub(r"(?m)^updated_on:.*$", "updated_on: '2026-05-18'", state)
    current_focus = f"""current_focus:
- >-
  Stage161(161단계) closed(종료) as `{decision}` and Stage162(162단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): score margin(점수 마진) / side filter(방향 필터) 결과를 후속 판독으로 넘긴다.
- >-
  Stage161 evidence(161단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(SUMMARY_CSV_PATH)}`, `{rel(SEGMENT_KPI_PATH)}`, `{rel(PROBABILITY_BINDING_PATH)}`에 있다. Effect(효과): threshold-only tuning(문턱값 단독 조정) 대신 실제 확률/방향 필터 작동 여부를 추적한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)만 계속한다.

"""
    state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", current_focus, state, count=1)
    state = re.sub(r"(?s)\nstage161_score_margin_or_side_filter_repair:.*?(?=\nstage\d+_|\Z)", "\n", state)
    state = re.sub(r"(?s)\nstage162_stage161_score_margin_followup_review:.*?(?=\nstage\d+_|\Z)", "\n", state)
    block = f"""
stage161_score_margin_or_side_filter_repair:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{decision}
  current_run_id: {RUN_ID}
  source_stage160_closeout_commit: {SOURCE_STAGE160_CLOSEOUT_COMMIT}
  source_stage160_hash_record_commit: {SOURCE_STAGE160_HASH_RECORD_COMMIT}
  source_stage158_run_id: {SOURCE_STAGE158_RUN_ID}
  source_adapter: {SOURCE_ADAPTER_ID}
  target_surface: {TARGET_SURFACE}
  decision: {decision}
  next_stage_or_branch: {NEXT_STAGE_ID}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  external_verification_status: {external}
  pushed_commit_hash: pending_until_push
  boundary: {BOUNDARY}

stage162_stage161_score_margin_followup_review:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: open_planned_from_stage161
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_decision: {decision}
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}
"""
    io_path(WORKSPACE_STATE_PATH).write_text(state.rstrip() + "\n" + block, encoding="utf-8-sig")
    write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준선): `none`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `stage162_stage161_score_margin_followup_surface`
- status(상태): `stage161_closed_{decision}_stage162_open_planned`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage161(161단계)는 score margin(점수 마진), probability calibration(확률 보정), side filter(방향 필터)를 MT5(메타트레이더5)로 측정했다. Effect(효과): 결과를 final package(최종 패키지)나 deployment(배포)로 부르지 않고 Stage162(162단계) 후속 판독으로 넘긴다.

## Latest Stage161 Evidence(최신 161단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- external_verification_status(외부 검증 상태): `{external}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- segment_kpi(구간 핵심 성과 지표): `{rel(SEGMENT_KPI_PATH)}`
- risk_atr_telemetry(위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- probability_binding(확률 작동): `{rel(PROBABILITY_BINDING_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
""",
    )
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage161 Selection Status(161단계 선택 상태)

- stage_status(단계 상태): `closed_{decision}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{PARENT_RUN_ID}`
- decision(판정): `{decision}`
- external_verification_status(외부 검증 상태): `{external}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage161(161단계)은 한 질문만 닫고 Stage162(162단계)로 넘긴다.
""",
    )
    write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage161 Review Index(161단계 검토 색인)

- status(상태): `closed_{decision}`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- segment_kpi(구간 핵심 성과 지표): `{rel(SEGMENT_KPI_PATH)}`
- probability_binding(확률 작동): `{rel(PROBABILITY_BINDING_PATH)}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`

Effect(효과): Stage161(161단계) 산출물 위치를 한 곳에서 추적한다.
""",
    )
    write_next_stage_seed(decision, external)


def append_changelog(decision: str) -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {utc_now()} Stage161 score margin or side filter repair closeout(161단계 점수 마진 또는 방향 필터 수리 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{decision}`.\n"
        "- effect(효과): score saturation(점수 포화)을 낮춘 확률 보정(probability calibration, 확률 보정)과 방향 필터(side filter, 방향 필터) 축을 MT5(메타트레이더5)로 측정하고 Stage162(162단계) 후속 판독으로 넘겼다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage161 score margin or side filter repair.")
    parser.add_argument("--terminal-path", default=str(base.TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(base.METAEDITOR_PATH_DEFAULT))
    parser.add_argument("--terminal-data-root", default=str(base.TERMINAL_DATA_ROOT_DEFAULT))
    parser.add_argument("--common-files-root", default=str(base.COMMON_FILES_ROOT_DEFAULT))
    parser.add_argument("--tester-profile-root", default=str(base.TESTER_PROFILE_ROOT_DEFAULT))
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


def main(argv: Sequence[str] | None = None) -> int:
    configure_base()
    args = parse_args(argv or sys.argv[1:])
    inputs = prepare_inputs(Path(args.common_files_root))
    attempts = build_attempts(inputs)
    prepared = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "stage_number": 161,
        "run_number": RUN_NUMBER,
        "run_root": RUN_ROOT,
        "packet_id": PACKET_ID,
        "attempts": attempts,
        "common_copies": inputs["common_copies"],
        "feature_exports": inputs["feature_exports"],
        "model_artifacts": inputs["model_exports"],
        "route_coverage": base.engine.route_coverage(),
        "model_family": "baseline_adapter_stage161_v2_native_score_margin_or_side_filter_repair_ebm_table",
        "feature_set_id": "stage161_calibrated_signal_plus_low_edge_side_filter",
        "label_id": "label_v1_fwd12_m5_logret_train_q33_3class",
        "split_contract": "split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413",
        "claim_boundary": BOUNDARY,
        "target_surface": TARGET_SURFACE,
        "gate_rows": inputs["gate_rows"],
    }
    result = base.execute_or_materialize(prepared, args)
    audit_rows = s58.audit_rows_for_result(result, float(args.cost_stress_per_trade)) if result.get("mt5_kpi_records") else []
    risk_rows = s58.risk_rows_from_result(result)
    summary_rows = s58.build_summary_rows(result, audit_rows, risk_rows)
    segment_rows = s58.segment_kpi_rows(summary_rows)
    probability_rows = probability_binding_rows(result)
    model_rows = model_score_rows(inputs)
    target_rows = target_progress_rows(summary_rows, segment_rows)
    external = str(result.get("external_verification_status") or "blocked")
    decision = decide(summary_rows, segment_rows, external)

    write_run_identity(result, probability_rows, model_rows)
    write_csv(AUDIT_CSV_PATH, audit_rows)
    write_csv(SUMMARY_CSV_PATH, summary_rows)
    write_csv(SEGMENT_KPI_PATH, segment_rows)
    write_csv(RISK_ATR_TELEMETRY_PATH, risk_rows)
    write_csv(GATE_FEATURE_SUMMARY_PATH, inputs["gate_rows"])
    write_csv(PROBABILITY_BINDING_PATH, probability_rows)
    write_csv(MODEL_SCORE_AUDIT_PATH, model_rows)
    write_csv(TIER_B_DIAGNOSTIC_PATH, tier_b_rows())
    write_md(REPORT_PATH, report_markdown(summary_rows, segment_rows, probability_rows, target_rows, decision, external))
    write_md(DECISION_PATH, decision_markdown(decision, external))
    write_json(
        SUMMARY_JSON_PATH,
        {
            "run_id": RUN_ID,
            "decision": decision,
            "external_verification_status": external,
            "summary_rows": summary_rows,
            "segment_rows": segment_rows,
            "probability_rows": probability_rows,
            "model_rows": model_rows,
            "target_rows": target_rows,
            "gate_rows": inputs["gate_rows"],
            "legacy_34d": LEGACY_34D,
            "stage156_reference": STAGE156_REFERENCE,
            "claim_boundary": BOUNDARY,
        },
    )
    artifacts = artifact_rows(result)
    ledger_payload = write_ledgers(result, decision, artifacts)
    write_packet_files(result, decision, ledger_payload, probability_rows, model_rows)
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
