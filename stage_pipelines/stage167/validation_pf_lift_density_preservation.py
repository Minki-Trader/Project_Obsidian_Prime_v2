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
from stage_pipelines.stage56 import baseline_adapter_repair_batch as repair  # noqa: E402
from stage_pipelines.stage58 import risk_atr_integration as s58  # noqa: E402
from stage_pipelines.stage161 import score_margin_or_side_filter_repair as s161  # noqa: E402

STAGE_ID = "167_adapter_research__validation_pf_lift_density_preservation"
RUN_NUMBER = "run167A"
RUN_ID = "run167A_stage167_validation_pf_lift_density_preservation_v1"
PACKET_ID = "stage167_validation_pf_lift_density_preservation_v1"
PARENT_RUN_ID = "run166A_stage166_stage165_side_context_followup_review_v1"
SOURCE_STAGE_ID = "166_adapter_research__stage165_side_context_followup_review"
SOURCE_RUN_ID = "run166A_stage166_stage165_side_context_followup_review_v1"
SOURCE_STAGE166_CLOSEOUT_COMMIT = "905da4d9c24ee4122db3dc93727d70caab3a0b89"
SOURCE_STAGE166_HASH_RECORD_COMMIT = "dd96a0b0153d84464300480d6d25acbfa9e4196b"
SOURCE_STAGE165_PRIMARY_ADAPTER = "s165_shortgate_long_lowedge_risk0250_h3_cd5_sht54_lng52"
NEXT_STAGE_ID = "168_adapter_research__stage167_validation_pf_followup_review"
NEXT_RUN_ID = "run168A_stage168_stage167_validation_pf_followup_review_v1"
NEXT_PACKET_ID = "stage168_stage167_validation_pf_followup_review_v1"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_no_legacy_inheritance"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)

LEGACY_34D = {
    "profit_factor": 1.583157,
    "net_profit": 987.60,
    "max_drawdown_percent": 12.909136,
    "trade_count": 404,
}
STAGE165_PRIMARY = {
    "adapter_id": SOURCE_STAGE165_PRIMARY_ADAPTER,
    "validation_pf": 1.55,
    "validation_net": 569.19,
    "validation_trade_count": 270.0,
    "oos_pf": 1.86,
    "oos_net": 566.88,
    "oos_dd_percent": 7.91,
    "oos_trade_count": 189.0,
    "oos_early_pf": 1.8086020364870596,
    "oos_early_net": 152.47,
}

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID
PARTIALS_ROOT = RUN_ROOT / "partials"
COMMON_ROOT = f"OPV2/s167a/{RUN_NUMBER}"

SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage167_validation_pf_lift_density_preservation_summary.json"
SUMMARY_CSV_PATH = REVIEWS_ROOT / "stage167_validation_pf_lift_density_preservation_summary.csv"
REPORT_PATH = REVIEWS_ROOT / "stage167_validation_pf_lift_density_preservation_report.md"
SEGMENT_KPI_PATH = REVIEWS_ROOT / "stage167_segment_kpi_summary.csv"
RISK_ATR_TELEMETRY_PATH = REVIEWS_ROOT / "stage167_risk_atr_telemetry.csv"
GATE_FEATURE_SUMMARY_PATH = REVIEWS_ROOT / "stage167_gate_feature_summary.csv"
PROBABILITY_BINDING_PATH = REVIEWS_ROOT / "stage167_probability_binding_summary.csv"
MODEL_SCORE_AUDIT_PATH = REVIEWS_ROOT / "stage167_model_score_audit.csv"
TIER_B_DIAGNOSTIC_PATH = REVIEWS_ROOT / "stage167_tier_b_diagnostic_summary.csv"
DECISION_PATH = REVIEWS_ROOT / "stage167_decision.md"
AUDIT_CSV_PATH = REVIEWS_ROOT / "stage167_trade_audit.csv"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage167/validation_pf_lift_density_preservation.py")
ARTIFACT_COLUMNS = (
    "artifact_id",
    "artifact_type",
    "path",
    "sha256",
    "stage_id",
    "run_id",
    "created_at_utc",
    "notes",
)

VARIANTS = (
    repair.RepairVariant(
        adapter_id="s167_short_pre_guard_risk0250_h3_cd5_sht54_lng52",
        label="stage167_short_pre_guard_risk0250",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0250,
        same_direction_reentry_cooldown_bars=5,
        short_threshold=0.54,
        long_threshold=0.52,
        close_on_flat_signal=False,
        reverse_on_opposite_signal=True,
        close_only_on_opposite_signal=False,
        max_hold_bars=3,
        notes="Stage167: Stage165 primary with short low-edge plus pre-window guard; long low-edge guard unchanged.",
    ),
    repair.RepairVariant(
        adapter_id="s167_short_wide_lowedge_risk0250_h3_cd5_sht54_lng52",
        label="stage167_short_wide_lowedge_risk0250",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0250,
        same_direction_reentry_cooldown_bars=5,
        short_threshold=0.54,
        long_threshold=0.52,
        close_on_flat_signal=False,
        reverse_on_opposite_signal=True,
        close_only_on_opposite_signal=False,
        max_hold_bars=3,
        notes="Stage167: wider observable low-edge short guard; long low-edge guard unchanged.",
    ),
    repair.RepairVariant(
        adapter_id="s167_short_cash45_guard_risk0250_h3_cd5_sht54_lng52",
        label="stage167_short_cash45_guard_risk0250",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0250,
        same_direction_reentry_cooldown_bars=5,
        short_threshold=0.54,
        long_threshold=0.52,
        close_on_flat_signal=False,
        reverse_on_opposite_signal=True,
        close_only_on_opposite_signal=False,
        max_hold_bars=3,
        notes="Stage167: short low-edge plus cash-open 0-45 guard; long low-edge guard unchanged.",
    ),
)

VARIANT_EXTRAS: dict[str, dict[str, Any]] = {
    "s167_short_pre_guard_risk0250_h3_cd5_sht54_lng52": {
        "logit_strength": 0.50,
        "risk_confidence_floor": 0.50,
        "risk_confidence_ceiling": 0.60,
        "block_mode": "encoded_side_context",
        "side_filter_enabled": True,
        "short_block_rule": "lowedge_or_pre",
        "long_block_rule": "lowedge_gate",
        "axis": "short_pre_guard",
    },
    "s167_short_wide_lowedge_risk0250_h3_cd5_sht54_lng52": {
        "logit_strength": 0.50,
        "risk_confidence_floor": 0.50,
        "risk_confidence_ceiling": 0.60,
        "block_mode": "encoded_side_context",
        "side_filter_enabled": True,
        "short_block_rule": "wide_lowedge",
        "long_block_rule": "lowedge_gate",
        "axis": "short_wide_lowedge",
    },
    "s167_short_cash45_guard_risk0250_h3_cd5_sht54_lng52": {
        "logit_strength": 0.50,
        "risk_confidence_floor": 0.50,
        "risk_confidence_ceiling": 0.60,
        "block_mode": "encoded_side_context",
        "side_filter_enabled": True,
        "short_block_rule": "lowedge_or_cash45",
        "long_block_rule": "lowedge_gate",
        "axis": "short_cash45_guard",
    },
}

MODEL_RISK_MIN_PCT = {variant.adapter_id: 0.005 for variant in VARIANTS}


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    candidate = Path(str(path))
    try:
        return io_path(candidate).resolve().relative_to(io_path(REPO_ROOT).resolve()).as_posix()
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


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    s161.write_csv(path, rows, columns)


def parse_float(value: Any, default: float = 0.0) -> float:
    return s161.parse_float(value, default)


def actual_row(rows: Sequence[Mapping[str, Any]], adapter_id: str, split: str) -> Mapping[str, Any]:
    for row in rows:
        if row.get("adapter_id") == adapter_id and row.get("split") == split and row.get("view") == "actual_routed_total":
            return row
    return {}


def segment_row(rows: Sequence[Mapping[str, Any]], adapter_id: str, split: str, segment: str) -> Mapping[str, Any]:
    for row in rows:
        if (
            row.get("adapter_id") == adapter_id
            and row.get("split") == split
            and row.get("view") == "actual_routed_total"
            and row.get("segment_type") == "chronological_third"
            and row.get("segment") == segment
        ):
            return row
    return {}


def minutes_for(row: Mapping[str, str]) -> float | None:
    timestamp = str(row.get("timestamp_utc", ""))
    value = s161.context_lookup().get(timestamp)
    return float(value) if value is not None else None


def margin_for(row: Mapping[str, str]) -> float:
    return parse_float(row.get("et40_decision_margin"), 1.0)


def lowedge_hit(row: Mapping[str, str], spec: Mapping[str, Any]) -> bool:
    minutes = minutes_for(row)
    session_hit = False
    if minutes is not None:
        session_hit = float(spec["session_min"]) <= minutes <= float(spec["session_max"])
    margin = margin_for(row)
    margin_hit = float(spec["margin_min"]) <= margin <= float(spec["margin_max"])
    return session_hit or margin_hit


def pre_hit(row: Mapping[str, str], spec: Mapping[str, Any]) -> bool:
    minutes = minutes_for(row)
    return minutes is not None and float(spec["pre_min"]) <= minutes <= float(spec["pre_max"])


def cash45_hit(row: Mapping[str, str], spec: Mapping[str, Any]) -> bool:
    minutes = minutes_for(row)
    return minutes is not None and float(spec["cash45_min"]) <= minutes <= float(spec["cash45_max"])


def wide_lowedge_hit(row: Mapping[str, str], spec: Mapping[str, Any]) -> bool:
    minutes = minutes_for(row)
    margin = margin_for(row)
    session_hit = minutes is not None and float(spec["wide_session_min"]) <= minutes <= float(spec["wide_session_max"])
    margin_hit = float(spec["wide_margin_min"]) <= margin <= float(spec["wide_margin_max"])
    return session_hit or margin_hit


def gate_value(row: Mapping[str, str], variant: repair.RepairVariant) -> float:
    signal = int(round(parse_float(row.get(s161.SIGNAL_COLUMN), 0.0)))
    if signal == 0:
        return 0.0
    spec = s161.CONTEXT_GATE_SPECS[variant.adapter_id]
    extra = VARIANT_EXTRAS[variant.adapter_id]
    if signal > 0:
        if str(extra["long_block_rule"]) == "lowedge_gate" and lowedge_hit(row, spec):
            return 2.0
    if signal < 0:
        rule = str(extra["short_block_rule"])
        if rule == "lowedge_or_pre" and (lowedge_hit(row, spec) or pre_hit(row, spec)):
            return 1.0
        if rule == "wide_lowedge" and wide_lowedge_hit(row, spec):
            return 1.0
        if rule == "lowedge_or_cash45" and (lowedge_hit(row, spec) or cash45_hit(row, spec)):
            return 1.0
    return 0.0


def extra_set_values(variant: repair.RepairVariant, magic: int) -> dict[str, Any]:
    values = s161.base.engine.extra_set_values(variant, magic)
    extra = VARIANT_EXTRAS[variant.adapter_id]
    values["InpSideFilterEnabled"] = bool(extra["side_filter_enabled"])
    values["InpSideFilterFeatureIndex"] = 1
    values["InpFallbackSideFilterFeatureIndex"] = 1
    values["InpBlockShortFeatureRange"] = True
    values["InpBlockShortFeatureMin"] = 0.5
    values["InpBlockShortFeatureMax"] = 1.5
    values["InpBlockLongFeatureRange"] = True
    values["InpBlockLongFeatureMin"] = 1.5
    values["InpBlockLongFeatureMax"] = 2.5
    values["InpModelRiskConfidenceFloor"] = float(extra["risk_confidence_floor"])
    values["InpModelRiskConfidenceCeiling"] = float(extra["risk_confidence_ceiling"])
    return values


def build_attempts(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    for variant_index, variant in enumerate(VARIANTS, start=1):
        variant_root = RUN_ROOT / variant.adapter_id
        for split in ("validation_is", "oos"):
            date_values = s161.base.parse_ini(s161.base.engine.source_attempt_ini(split, variant))
            split_token = "val" if split == "validation_is" else "oos"
            for role_index, (tier, attempt_role, prefix, attempt_token) in enumerate(
                (
                    (s161.base.mt5.TIER_A, "tier_only_total", f"mt5_tier_a_only_{variant.adapter_id}", "ta"),
                    (s161.base.mt5.TIER_AB, "routed_total", f"mt5_routed_{variant.adapter_id}", "rt"),
                ),
                start=1,
            ):
                magic = 16710000 + variant_index * 100 + (1 if split == "validation_is" else 50) + role_index
                attempts.append(
                    s161.base.attempt_payload(
                        run_root=variant_root,
                        run_id=RUN_ID,
                        stage_number=167,
                        exploration_label="stage167_BaselineAdapter__ValidationPFLiftDensityPreservation",
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


def configure_runner() -> None:
    patch_values = {
        "STAGE_ID": STAGE_ID,
        "RUN_NUMBER": RUN_NUMBER,
        "RUN_ID": RUN_ID,
        "PACKET_ID": PACKET_ID,
        "PARENT_RUN_ID": PARENT_RUN_ID,
        "NEXT_STAGE_ID": NEXT_STAGE_ID,
        "NEXT_RUN_ID": NEXT_RUN_ID,
        "NEXT_PACKET_ID": NEXT_PACKET_ID,
        "SOURCE_ADAPTER_ID": SOURCE_STAGE165_PRIMARY_ADAPTER,
        "TARGET_SURFACE": TARGET_SURFACE,
        "BOUNDARY": BOUNDARY,
        "STAGE_ROOT": STAGE_ROOT,
        "RUN_ROOT": RUN_ROOT,
        "REVIEWS_ROOT": REVIEWS_ROOT,
        "SELECTED_ROOT": SELECTED_ROOT,
        "PACKET_ROOT": PACKET_ROOT,
        "NEXT_STAGE_ROOT": NEXT_STAGE_ROOT,
        "PARTIALS_ROOT": PARTIALS_ROOT,
        "COMMON_ROOT": COMMON_ROOT,
        "SUMMARY_JSON_PATH": SUMMARY_JSON_PATH,
        "SUMMARY_CSV_PATH": SUMMARY_CSV_PATH,
        "REPORT_PATH": REPORT_PATH,
        "SEGMENT_KPI_PATH": SEGMENT_KPI_PATH,
        "RISK_ATR_TELEMETRY_PATH": RISK_ATR_TELEMETRY_PATH,
        "GATE_FEATURE_SUMMARY_PATH": GATE_FEATURE_SUMMARY_PATH,
        "PROBABILITY_BINDING_PATH": PROBABILITY_BINDING_PATH,
        "MODEL_SCORE_AUDIT_PATH": MODEL_SCORE_AUDIT_PATH,
        "TIER_B_DIAGNOSTIC_PATH": TIER_B_DIAGNOSTIC_PATH,
        "DECISION_PATH": DECISION_PATH,
        "AUDIT_CSV_PATH": AUDIT_CSV_PATH,
        "STAGE_LEDGER_PATH": STAGE_LEDGER_PATH,
        "PRODUCER_PATH": PRODUCER_PATH,
        "VARIANTS": VARIANTS,
        "VARIANT_EXTRAS": VARIANT_EXTRAS,
        "MODEL_RISK_MIN_PCT": MODEL_RISK_MIN_PCT,
        "SOURCE_SPECS_BY_VARIANT": {variant.adapter_id: dict(s161.s158.LOW_EDGE_SOURCE_SPEC) for variant in VARIANTS},
        "CONTEXT_GATE_SPECS": {
            variant.adapter_id: {
                "gate_column": f"stage167_gate_{VARIANT_EXTRAS[variant.adapter_id]['axis']}",
                "gate_type": "encoded_validation_pf_lift_side_context_block",
                "block_mode": VARIANT_EXTRAS[variant.adapter_id]["block_mode"],
                "session_min": 170.0,
                "session_max": 265.0,
                "margin_min": 0.04,
                "margin_max": 0.0775,
                "pre_min": 90.0,
                "pre_max": 170.0,
                "cash45_min": 0.0,
                "cash45_max": 45.0,
                "wide_session_min": 150.0,
                "wide_session_max": 300.0,
                "wide_margin_min": 0.035,
                "wide_margin_max": 0.085,
                "description": (
                    "Stage167 encoded side-context gate: value 1 blocks short range, "
                    "value 2 blocks long range. Long low-edge guard remains fixed."
                ),
            }
            for variant in VARIANTS
        },
    }
    for name, value in patch_values.items():
        setattr(s161, name, value)
    s161.gate_value = gate_value
    s161.extra_set_values = extra_set_values
    s161.build_attempts = build_attempts
    s161._CONTEXT_LOOKUP = None


def quality_rows(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for variant in VARIANTS:
        val = actual_row(summary_rows, variant.adapter_id, "validation_is")
        oos = actual_row(summary_rows, variant.adapter_id, "oos")
        oos_early = segment_row(segment_rows, variant.adapter_id, "oos", "early")
        oos_mid = segment_row(segment_rows, variant.adapter_id, "oos", "mid")
        oos_late = segment_row(segment_rows, variant.adapter_id, "oos", "late")
        flags: list[str] = []
        val_pf = parse_float(val.get("profit_factor"))
        oos_pf = parse_float(oos.get("profit_factor"))
        oos_dd = parse_float(oos.get("max_drawdown_percent"))
        oos_early_pf = parse_float(oos_early.get("profit_factor"))
        oos_early_net = parse_float(oos_early.get("net_profit"))
        val_net = parse_float(val.get("net_profit"))
        oos_net = parse_float(oos.get("net_profit"))
        val_trades = parse_float(val.get("trade_count"))
        oos_trades = parse_float(oos.get("trade_count"))
        if val_pf < LEGACY_34D["profit_factor"]:
            flags.append("validation_pf_below_34d")
        if oos_pf < LEGACY_34D["profit_factor"]:
            flags.append("oos_pf_below_34d")
        if oos_dd > LEGACY_34D["max_drawdown_percent"]:
            flags.append("oos_dd_above_34d")
        if oos_early_pf < 1.10 or oos_early_net <= 0:
            flags.append("oos_early_damage")
        if val_trades / STAGE165_PRIMARY["validation_trade_count"] < 0.65:
            flags.append("validation_trade_density_thin_vs_stage165_primary")
        if oos_trades / STAGE165_PRIMARY["oos_trade_count"] < 0.65:
            flags.append("oos_trade_density_thin_vs_stage165_primary")
        if val_net / STAGE165_PRIMARY["validation_net"] < 0.65:
            flags.append("validation_net_density_thin_vs_stage165_primary")
        if oos_net / STAGE165_PRIMARY["oos_net"] < 0.65:
            flags.append("oos_net_density_thin_vs_stage165_primary")
        rows.append(
            {
                "adapter_id": variant.adapter_id,
                "label": variant.label,
                "axis": VARIANT_EXTRAS[variant.adapter_id]["axis"],
                "long_block_rule": VARIANT_EXTRAS[variant.adapter_id]["long_block_rule"],
                "short_block_rule": VARIANT_EXTRAS[variant.adapter_id]["short_block_rule"],
                "validation_pf": val_pf,
                "validation_net": val_net,
                "validation_trade_count": val_trades,
                "oos_pf": oos_pf,
                "oos_net": oos_net,
                "oos_dd_percent": oos_dd,
                "oos_trade_count": oos_trades,
                "oos_early_pf": oos_early_pf,
                "oos_early_net": oos_early_net,
                "oos_mid_pf": parse_float(oos_mid.get("profit_factor")),
                "oos_late_pf": parse_float(oos_late.get("profit_factor")),
                "validation_pf_delta_vs_stage165_primary": val_pf - STAGE165_PRIMARY["validation_pf"],
                "validation_net_retention_vs_stage165_primary": val_net / STAGE165_PRIMARY["validation_net"],
                "validation_trade_retention_vs_stage165_primary": val_trades / STAGE165_PRIMARY["validation_trade_count"],
                "oos_net_retention_vs_stage165_primary": oos_net / STAGE165_PRIMARY["oos_net"],
                "oos_trade_retention_vs_stage165_primary": oos_trades / STAGE165_PRIMARY["oos_trade_count"],
                "quality_flags": ";".join(flags) if flags else "candidate_quality_pass_review_required",
                "candidate_quality_pass": not flags,
            }
        )
    return rows


def decide(rows: Sequence[Mapping[str, Any]], external: str) -> str:
    if external != "completed":
        return "continue_stage167_runtime_completion_due_to_incomplete_runtime_candidate_not_final"
    if any(row.get("candidate_quality_pass") for row in rows):
        return "open_stage168_validation_pf_followup_review_candidate_not_final"
    return "open_stage168_validation_pf_repair_followup_due_to_kpi_damage_candidate_not_final"


def kpi_table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | axis(축) | val PF(검증 수익요인) | val net(검증 순손익) | val trades(검증 거래) | OOS PF(표본외 수익요인) | OOS net(표본외 순손익) | OOS DD%(표본외 낙폭) | OOS early PF(표본외 초반 수익요인) | flags(플래그) |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {adapter_id} | {axis} | {validation_pf:.6f} | {validation_net:.2f} | {validation_trade_count:.0f} | {oos_pf:.6f} | {oos_net:.2f} | {oos_dd_percent:.2f} | {oos_early_pf:.6f} | {quality_flags} |".format(
                **row
            )
        )
    return "\n".join(lines)


def report_markdown(rows: Sequence[Mapping[str, Any]], decision: str, external: str) -> str:
    return f"""# Stage167 Validation PF Lift With Density Preservation Report(167단계 검증 수익요인 상승과 밀도 보존 보고)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_stage166_closeout_commit(원천 166단계 종료 커밋): `{SOURCE_STAGE166_CLOSEOUT_COMMIT}`
- source_stage166_hash_record_commit(원천 166단계 해시 기록 커밋): `{SOURCE_STAGE166_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{external}`
- decision(판정): `{decision}`
- boundary(주장 경계): `{BOUNDARY}`

## Experiment Design(실험 설계)

- hypothesis(가설): Stage165(165단계) primary shortgate low-edge route(주 숏게이트 낮은 엣지 경로)에서 short-side block(숏 방향 차단)을 조금 넓히면 validation PF(검증 수익요인)를 34D 위로 올릴 수 있다.
- decision_use(판정 사용처): Stage168(168단계)에서 이 축을 계속 수리할지, 다른 bounded repair(경계 수리)로 넘길지 결정한다.
- comparison_baseline(비교 기준): `{SOURCE_STAGE165_PRIMARY_ADAPTER}` with validation PF(검증 수익요인) `{STAGE165_PRIMARY["validation_pf"]}`, OOS PF(표본외 수익요인) `{STAGE165_PRIMARY["oos_pf"]}`, OOS net(표본외 순손익) `{STAGE165_PRIMARY["oos_net"]}`.
- control_variables(고정 변수): ATR bracket(ATR 브래킷), model risk cap(모델 위험 상한) 2.5%, hold bars(보유 봉) 3, cooldown(쿨다운) 5, thresholds(문턱값) short 0.54 / long 0.52.
- changed_variables(변경 변수): short-side context block rule(숏 방향 문맥 차단 규칙) only.
- success_criteria(성공 기준): validation PF(검증 수익요인) >= 34D, OOS PF(표본외 수익요인) >= 34D, OOS DD(표본외 낙폭) <= 34D, OOS early(표본외 초반) positive(양호), and density(밀도) not thin versus Stage165 primary.
- failure_criteria(실패 기준): validation PF(검증 수익요인)가 여전히 낮거나, OOS/density(표본외/밀도)가 손상된다.
- invalid_conditions(무효 조건): MT5(MetaTrader 5, 메타트레이더5) 외부 검증 실패, telemetry(기록) 누락, required ledgers(필수 장부) 누락.

## KPI Read(KPI 판독)

{kpi_table(rows)}

## Judgment(판정)

Stage167(167단계)는 validation PF lift(검증 수익요인 상승)만 좁게 본 bounded experiment(경계 실험)이다. Effect(효과): 결과가 좋더라도 research package complete(연구 패키지 완료)가 아니며, Stage168(168단계) follow-up review(후속 검토)로 넘긴다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
"""


def decision_markdown(decision: str, external: str) -> str:
    return f"""# Stage167 Decision(167단계 판정)

- decision(판정): `{decision}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage166_closeout_commit(원천 166단계 종료 커밋): `{SOURCE_STAGE166_CLOSEOUT_COMMIT}`
- external_verification_status(외부 검증 상태): `{external}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary_csv(요약 CSV): `{rel(SUMMARY_CSV_PATH)}`
- segment_kpi(구간 핵심 성과 지표): `{rel(SEGMENT_KPI_PATH)}`
- probability_binding(확률 작동): `{rel(PROBABILITY_BINDING_PATH)}`
- gate_feature_summary(게이트 피처 요약): `{rel(GATE_FEATURE_SUMMARY_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage167(167단계) closeout(종료)은 overall goal complete(전체 목표 완료)가 아니다.
"""


def artifact_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    now = utc_now()
    rows: list[dict[str, Any]] = []
    paths = [
        PRODUCER_PATH,
        REPORT_PATH,
        DECISION_PATH,
        SUMMARY_JSON_PATH,
        SUMMARY_CSV_PATH,
        SEGMENT_KPI_PATH,
        RISK_ATR_TELEMETRY_PATH,
        GATE_FEATURE_SUMMARY_PATH,
        PROBABILITY_BINDING_PATH,
        MODEL_SCORE_AUDIT_PATH,
        TIER_B_DIAGNOSTIC_PATH,
        AUDIT_CSV_PATH,
        STAGE_LEDGER_PATH,
    ]
    for path in paths:
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{Path(path).name}",
                    "artifact_type": "stage167_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": now,
                    "notes": "Stage167 validation PF lift density preservation evidence.",
                }
            )
    for execution in result.get("execution_results", []):
        outputs = execution.get("runtime_outputs", {}) if isinstance(execution.get("runtime_outputs"), Mapping) else {}
        for key in ("report_path", "telemetry_path", "orders_path"):
            raw_path = outputs.get(key)
            if raw_path and path_exists(Path(str(raw_path))):
                path = Path(str(raw_path))
                rows.append(
                    {
                        "artifact_id": f"{RUN_ID}__{execution.get('attempt_name','attempt')}__{key}",
                        "artifact_type": "mt5_runtime_output",
                        "path": rel(path),
                        "sha256": sha256_file_lf_normalized(path),
                        "stage_id": STAGE_ID,
                        "run_id": RUN_ID,
                        "created_at_utc": now,
                        "notes": "Stage167 MT5 runtime output; research only.",
                    }
                )
    return rows


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
                "lane": "baseline_adapter_stage167_validation_pf_lift_density_preservation",
                "status": status,
                "judgment": decision,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_stage166_closeout_commit", SOURCE_STAGE166_CLOSEOUT_COMMIT),
                        ("source_stage166_hash_record_commit", SOURCE_STAGE166_HASH_RECORD_COMMIT),
                        ("source_stage165_primary", SOURCE_STAGE165_PRIMARY_ADAPTER),
                        ("target_surface", TARGET_SURFACE),
                        ("legacy_relation", "lesson_only_no_inheritance"),
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
                "kpi_scope": "stage167_validation_pf_lift_density_preservation",
                "scoreboard_lane": "runtime_probe",
                "status": status,
                "judgment": decision,
                "path": rel(DECISION_PATH),
                "primary_kpi": "mt5_kpi_records=0",
                "guardrail_kpi": f"target_surface={TARGET_SURFACE}",
                "external_verification_status": external,
                "notes": "Stage167 materialized or blocked before KPI records were available.",
            }
        ]
    for row in alpha_rows:
        row["parent_run_id"] = row.get("parent_run_id") or PARENT_RUN_ID
    alpha_payload = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, list(artifacts), key="artifact_id")
    return {
        "run_registry": run_payload,
        "alpha_ledger": alpha_payload,
        "stage_ledger": stage_payload,
        "artifact_registry": artifact_payload,
    }


def write_packet_files(result: Mapping[str, Any], decision: str, ledger_payload: Mapping[str, Any], quality: Sequence[Mapping[str, Any]]) -> None:
    status = "completed" if result.get("external_verification_status") == "completed" else "blocked"
    payload = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "status": status,
        "decision": decision,
        "report_path": rel(REPORT_PATH),
        "decision_path": rel(DECISION_PATH),
        "summary_csv": rel(SUMMARY_CSV_PATH),
        "segment_kpi": rel(SEGMENT_KPI_PATH),
        "gate_feature_summary": rel(GATE_FEATURE_SUMMARY_PATH),
        "ledger_payload": ledger_payload,
        "quality_rows": list(quality),
        "claim_boundary": BOUNDARY,
        "overall_goal_complete": False,
    }
    write_json(PACKET_ROOT / "aggregate_summary.json", payload)
    write_json(PACKET_ROOT / "result_judgment_gate.json", payload)
    write_json(PACKET_ROOT / "packet_receipt.json", payload)
    write_md(
        PACKET_ROOT / "closeout_packet.md",
        f"""# Stage167 Closeout Packet(167단계 종료 작업 묶음)

- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- status(상태): `{status}`
- decision(판정): `{decision}`
- report(보고서): `{rel(REPORT_PATH)}`
- overall_goal_complete(전체 목표 완료): `false`
- boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage167(167단계) evidence(근거)를 장부와 packet(작업 묶음)에 연결해서 Stage168(168단계)이 같은 근거를 읽게 한다.
""",
    )


def write_next_stage_seed(decision: str, external: str) -> None:
    if external != "completed":
        return
    write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage168(168단계)는 Stage167(167단계) validation PF lift(검증 수익요인 상승) 결과를 review-only(검토 전용)로 판독한다.

## Bounded Question(경계 질문)

Did Stage167(167단계) produce a v2-native repair(v2 고유 수리) that lifts validation PF(검증 수익요인) above 34D while preserving OOS and density(표본외와 밀도)?

Effect(효과): Stage167(167단계) 안에서 계속 고치지 않고, 성공/실패를 분리해서 다음 경계를 정한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage168 Inputs(168단계 입력)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{decision}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary_csv(요약 CSV): `{rel(SUMMARY_CSV_PATH)}`
- segment_kpi(구간 핵심 성과 지표): `{rel(SEGMENT_KPI_PATH)}`
- gate_feature_summary(게이트 피처 요약): `{rel(GATE_FEATURE_SUMMARY_PATH)}`
- decision_path(판정 파일): `{rel(DECISION_PATH)}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage168 Review Index(168단계 검토 색인)

- status(상태): `open_planned_from_stage167`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{decision}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage168 Selection Status(168단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage167`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{decision}`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )


def update_current_truth(decision: str, external: str) -> None:
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    if external == "completed":
        state = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", state, count=1, flags=re.MULTILINE)
        state = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", state, count=1, flags=re.MULTILINE)
        focus = f"""current_focus:
- >-
  Stage167(167단계) closed(종료) as `{decision}` and Stage168(168단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): validation PF lift(검증 수익요인 상승) 결과를 후속 검토로 넘긴다.
- >-
  Stage167 evidence(167단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(SUMMARY_CSV_PATH)}`, `{rel(SEGMENT_KPI_PATH)}`, `{rel(GATE_FEATURE_SUMMARY_PATH)}`에 있다. Effect(효과): short-side block(숏 방향 차단), validation/OOS KPI(검증/표본외 핵심 성과 지표), density(밀도), DD(낙폭)를 같이 판독한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)만 계속한다.

"""
    else:
        focus = f"""current_focus:
- >-
  Stage167(167단계) runtime(런타임) evidence(근거)가 incomplete(불완전) 상태로 `{decision}`을 기록했다. Effect(효과): 완료 주장을 낮추고 같은 경계 안에서 실행 복구가 필요함을 보존한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 deployment(배포)나 live readiness(실거래 준비)는 금지다.

"""
    state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, state, count=1)
    state = re.sub(r"(?ms)^stage167_validation_pf_lift_density_preservation:\r?\n.*?(?=^stage\d+_|\Z)", "", state)
    block = f"""
stage167_validation_pf_lift_density_preservation:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{decision if external == "completed" else "blocked_runtime_incomplete"}
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE_ID}
  source_run: {SOURCE_RUN_ID}
  decision: {decision}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  summary_path: {rel(SUMMARY_CSV_PATH)}
  segment_kpi_path: {rel(SEGMENT_KPI_PATH)}
  external_verification_status: {external}
  pushed_commit_hash: pending_until_push
  next_action: {NEXT_RUN_ID if external == "completed" else RUN_ID}
  boundary: {BOUNDARY}
"""
    io_path(WORKSPACE_STATE_PATH).write_text(state.rstrip() + "\n" + block, encoding="utf-8-sig")
    active_stage = NEXT_STAGE_ID if external == "completed" else STAGE_ID
    active_run = NEXT_RUN_ID if external == "completed" else RUN_ID
    write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID if external == "completed" else PACKET_ID}`
- current_run(현재 실행): `{active_run}`
- active_stage(활성 단계): `{active_stage}`
- selected_research_baseline(선택 연구 기준선): `none`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `stage167_validation_pf_lift_density_preservation_surface`
- status(상태): `stage167_{decision}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage167(167단계)는 validation PF lift with density preservation(검증 수익요인 상승과 밀도 보존)을 MT5(MetaTrader 5, 메타트레이더5)로 측정했다. Effect(효과): 34D KPI(34D 핵심 성과 지표)를 lesson-only target(교훈 전용 목표)로 쓰되, v2-native research(v2 고유 연구) 경계를 유지한다.

## Latest Stage167 Evidence(최신 167단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- external_verification_status(외부 검증 상태): `{external}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- segment_kpi(구간 핵심 성과 지표): `{rel(SEGMENT_KPI_PATH)}`
- gate_feature_summary(게이트 피처 요약): `{rel(GATE_FEATURE_SUMMARY_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
""",
    )


def write_status_files(decision: str, external: str) -> None:
    status = f"closed_{decision}" if external == "completed" else "blocked_runtime_incomplete"
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage167 Selection Status(167단계 선택 상태)

- stage_status(단계 상태): `{status}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- external_verification_status(외부 검증 상태): `{external}`
- decision(판정): `{decision}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID if external == "completed" else STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage167(167단계)는 이 질문만 닫고, 전체 목표 완료를 주장하지 않는다.
""",
    )
    write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage167 Review Index(167단계 검토 색인)

- status(상태): `{status}`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- segment_kpi(구간 핵심 성과 지표): `{rel(SEGMENT_KPI_PATH)}`
- risk_atr_telemetry(위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- gate_feature_summary(게이트 피처 요약): `{rel(GATE_FEATURE_SUMMARY_PATH)}`
- probability_binding(확률 작동): `{rel(PROBABILITY_BINDING_PATH)}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID if external == "completed" else STAGE_ID}`
""",
    )


def append_changelog(decision: str) -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {utc_now()} Stage167 validation PF lift density preservation closeout(167단계 검증 수익요인 상승과 밀도 보존 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{decision}`.\n"
        "- effect(효과): short-side context block(숏 방향 문맥 차단) 변형을 MT5(MetaTrader 5, 메타트레이더5)로 측정해 Stage168(168단계) 후속 판독으로 넘겼다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    return s161.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    configure_runner()
    s161.configure_base()
    args = parse_args(argv or sys.argv[1:])
    inputs = s161.prepare_inputs(Path(args.common_files_root))
    attempts = build_attempts(inputs)
    prepared = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "stage_number": 167,
        "run_number": RUN_NUMBER,
        "run_root": RUN_ROOT,
        "packet_id": PACKET_ID,
        "attempts": attempts,
        "common_copies": inputs["common_copies"],
        "feature_exports": inputs["feature_exports"],
        "model_artifacts": inputs["model_exports"],
        "route_coverage": s161.base.engine.route_coverage(),
        "model_family": "baseline_adapter_stage167_v2_native_validation_pf_lift_density_preservation",
        "feature_set_id": "stage167_signal_plus_encoded_validation_pf_lift_gate",
        "label_id": "label_v1_fwd12_m5_logret_train_q33_3class",
        "split_contract": "split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413",
        "claim_boundary": BOUNDARY,
        "target_surface": TARGET_SURFACE,
        "gate_rows": inputs["gate_rows"],
    }
    result = s161.base.execute_or_materialize(prepared, args)
    audit_rows = s58.audit_rows_for_result(result, float(args.cost_stress_per_trade)) if result.get("mt5_kpi_records") else []
    risk_rows = s58.risk_rows_from_result(result)
    summary_rows = s58.build_summary_rows(result, audit_rows, risk_rows)
    segment_rows = s58.segment_kpi_rows(summary_rows)
    probability_rows = s161.probability_binding_rows(result)
    model_rows = s161.model_score_rows(inputs)
    quality = quality_rows(summary_rows, segment_rows)
    external = str(result.get("external_verification_status") or "blocked")
    decision = decide(quality, external)

    s161.write_run_identity(result, probability_rows, model_rows)
    write_csv(AUDIT_CSV_PATH, audit_rows)
    write_csv(SUMMARY_CSV_PATH, summary_rows)
    write_csv(SEGMENT_KPI_PATH, segment_rows)
    write_csv(RISK_ATR_TELEMETRY_PATH, risk_rows)
    write_csv(GATE_FEATURE_SUMMARY_PATH, inputs["gate_rows"])
    write_csv(PROBABILITY_BINDING_PATH, probability_rows)
    write_csv(MODEL_SCORE_AUDIT_PATH, model_rows)
    write_csv(TIER_B_DIAGNOSTIC_PATH, s161.tier_b_rows())
    write_md(REPORT_PATH, report_markdown(quality, decision, external))
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
            "quality_rows": quality,
            "gate_rows": inputs["gate_rows"],
            "legacy_34d": LEGACY_34D,
            "stage165_primary": STAGE165_PRIMARY,
            "claim_boundary": BOUNDARY,
            "overall_goal_complete": False,
        },
    )
    artifacts = artifact_rows(result)
    ledger_payload = write_ledgers(result, decision, artifacts)
    write_packet_files(result, decision, ledger_payload, quality)
    if not args.materialize_only:
        write_next_stage_seed(decision, external)
        update_current_truth(decision, external)
        write_status_files(decision, external)
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
                    "overall_goal_complete": False,
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
