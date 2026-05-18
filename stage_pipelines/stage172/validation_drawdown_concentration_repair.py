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
from stage_pipelines.stage167 import validation_pf_lift_density_preservation as s167  # noqa: E402
from stage_pipelines.stage171 import segment_stability_equity_curve_audit as s171  # noqa: E402

STAGE_ID = "172_adapter_research__validation_drawdown_concentration_repair"
RUN_NUMBER = "run172A"
RUN_ID = "run172A_stage172_validation_drawdown_concentration_repair_v1"
PACKET_ID = "stage172_validation_drawdown_concentration_repair_v1"
PARENT_RUN_ID = "run171A_stage171_segment_stability_equity_curve_audit_v1"
SOURCE_STAGE_ID = "171_adapter_research__segment_stability_equity_curve_audit"
SOURCE_RUN_ID = "run171A_stage171_segment_stability_equity_curve_audit_v1"
SOURCE_STAGE171_CLOSEOUT_COMMIT = "9880380842d81463d7728384a0575bdd0079a252"
SOURCE_STAGE171_HASH_RECORD_COMMIT = "ec4d903d936248bbc0a66b28f10a7f14ebc976e7"
SOURCE_ADAPTER_ID = "s169_short_pre_risk0350_h3_cd5_sht54_lng52"
NEXT_STAGE_ID = "173_adapter_research__stage172_repair_followup_review"
NEXT_RUN_ID = "run173A_stage173_stage172_repair_followup_review_v1"
NEXT_PACKET_ID = "stage173_stage172_repair_followup_review_v1"
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
STAGE171_PRIMARY = {
    "adapter_id": SOURCE_ADAPTER_ID,
    "validation_pf": 1.611235,
    "validation_net": 983.96,
    "validation_balance_dd_percent": 14.301,
    "validation_late_share": 0.5508,
    "oos_pf": 1.8221,
    "oos_net": 835.78,
    "oos_balance_dd_percent": 10.0007,
    "oos_late_share": 0.5078,
}

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID
PARTIALS_ROOT = RUN_ROOT / "partials"
COMMON_ROOT = f"OPV2/s172a/{RUN_NUMBER}"

SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage172_validation_drawdown_concentration_repair_summary.json"
SUMMARY_CSV_PATH = REVIEWS_ROOT / "stage172_validation_drawdown_concentration_repair_summary.csv"
REPORT_PATH = REVIEWS_ROOT / "stage172_validation_drawdown_concentration_repair_report.md"
SEGMENT_KPI_PATH = REVIEWS_ROOT / "stage172_segment_kpi_summary.csv"
BALANCE_CURVE_AUDIT_PATH = REVIEWS_ROOT / "stage172_balance_curve_audit.csv"
MONTHLY_KPI_PATH = REVIEWS_ROOT / "stage172_monthly_kpi_summary.csv"
CONCENTRATION_PATH = REVIEWS_ROOT / "stage172_concentration_risk_summary.csv"
DRAWDOWN_PATH = REVIEWS_ROOT / "stage172_drawdown_recovery_summary.csv"
QUALITY_MATRIX_PATH = REVIEWS_ROOT / "stage172_quality_matrix.csv"
RISK_ATR_TELEMETRY_PATH = REVIEWS_ROOT / "stage172_risk_atr_telemetry.csv"
GATE_FEATURE_SUMMARY_PATH = REVIEWS_ROOT / "stage172_gate_feature_summary.csv"
PROBABILITY_BINDING_PATH = REVIEWS_ROOT / "stage172_probability_binding_summary.csv"
MODEL_SCORE_AUDIT_PATH = REVIEWS_ROOT / "stage172_model_score_audit.csv"
TIER_B_DIAGNOSTIC_PATH = REVIEWS_ROOT / "stage172_tier_b_diagnostic_summary.csv"
DECISION_PATH = REVIEWS_ROOT / "stage172_decision.md"
AUDIT_CSV_PATH = REVIEWS_ROOT / "stage172_trade_audit.csv"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage172/validation_drawdown_concentration_repair.py")
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
        adapter_id="s172_short_pre_control_risk0350_h3_cd5_sht54_lng52",
        label="stage172_short_pre_control_risk0350",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0350,
        same_direction_reentry_cooldown_bars=5,
        short_threshold=0.54,
        long_threshold=0.52,
        close_on_flat_signal=False,
        reverse_on_opposite_signal=True,
        close_only_on_opposite_signal=False,
        max_hold_bars=3,
        notes="Stage172 control: Stage169 short-pre gate, 3.5 percent model risk cap, original ATR bracket.",
    ),
    repair.RepairVariant(
        adapter_id="s172_short_pre_sl195_risk0350_h3_cd5_sht54_lng52",
        label="stage172_short_pre_sl195_risk0350",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=1.95,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0350,
        same_direction_reentry_cooldown_bars=5,
        short_threshold=0.54,
        long_threshold=0.52,
        close_on_flat_signal=False,
        reverse_on_opposite_signal=True,
        close_only_on_opposite_signal=False,
        max_hold_bars=3,
        notes="Stage172: tighten ATR stop to 1.95 while keeping Stage169 gate and 3.5 percent risk cap.",
    ),
    repair.RepairVariant(
        adapter_id="s172_short_pre_sl195_risk0360_h3_cd5_sht54_lng52",
        label="stage172_short_pre_sl195_risk0360",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=1.95,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0360,
        same_direction_reentry_cooldown_bars=5,
        short_threshold=0.54,
        long_threshold=0.52,
        close_on_flat_signal=False,
        reverse_on_opposite_signal=True,
        close_only_on_opposite_signal=False,
        max_hold_bars=3,
        notes="Stage172: tightened ATR stop plus small risk-cap recapture bounded below the 5 percent cap.",
    ),
    repair.RepairVariant(
        adapter_id="s172_short_wide_sl195_risk0365_h3_cd5_sht54_lng52",
        label="stage172_short_wide_sl195_risk0365",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=1.95,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0365,
        same_direction_reentry_cooldown_bars=5,
        short_threshold=0.54,
        long_threshold=0.52,
        close_on_flat_signal=False,
        reverse_on_opposite_signal=True,
        close_only_on_opposite_signal=False,
        max_hold_bars=3,
        notes="Stage172: wider short low-edge gate plus tightened ATR stop and bounded risk recapture.",
    ),
)

VARIANT_EXTRAS: dict[str, dict[str, Any]] = {
    "s172_short_pre_control_risk0350_h3_cd5_sht54_lng52": {
        "logit_strength": 0.50,
        "risk_confidence_floor": 0.50,
        "risk_confidence_ceiling": 0.60,
        "block_mode": "encoded_side_context",
        "side_filter_enabled": True,
        "short_block_rule": "lowedge_or_pre",
        "long_block_rule": "lowedge_gate",
        "axis": "short_pre_control_risk0350",
    },
    "s172_short_pre_sl195_risk0350_h3_cd5_sht54_lng52": {
        "logit_strength": 0.50,
        "risk_confidence_floor": 0.50,
        "risk_confidence_ceiling": 0.60,
        "block_mode": "encoded_side_context",
        "side_filter_enabled": True,
        "short_block_rule": "lowedge_or_pre",
        "long_block_rule": "lowedge_gate",
        "axis": "short_pre_sl195_risk0350",
    },
    "s172_short_pre_sl195_risk0360_h3_cd5_sht54_lng52": {
        "logit_strength": 0.50,
        "risk_confidence_floor": 0.50,
        "risk_confidence_ceiling": 0.60,
        "block_mode": "encoded_side_context",
        "side_filter_enabled": True,
        "short_block_rule": "lowedge_or_pre",
        "long_block_rule": "lowedge_gate",
        "axis": "short_pre_sl195_risk0360",
    },
    "s172_short_wide_sl195_risk0365_h3_cd5_sht54_lng52": {
        "logit_strength": 0.50,
        "risk_confidence_floor": 0.50,
        "risk_confidence_ceiling": 0.60,
        "block_mode": "encoded_side_context",
        "side_filter_enabled": True,
        "short_block_rule": "wide_lowedge",
        "long_block_rule": "lowedge_gate",
        "axis": "short_wide_sl195_risk0365",
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


def parse_float(value: Any, default: float = 0.0) -> float:
    return s161.parse_float(value, default)


def as_float(row: Mapping[str, Any], key: str, default: float = 0.0) -> float:
    return parse_float(row.get(key), default)


def lowedge_hit(row: Mapping[str, str], spec: Mapping[str, Any]) -> bool:
    minutes = s167.minutes_for(row)
    session_hit = minutes is not None and float(spec["session_min"]) <= minutes <= float(spec["session_max"])
    margin = s167.margin_for(row)
    margin_hit = float(spec["margin_min"]) <= margin <= float(spec["margin_max"])
    return session_hit or margin_hit


def pre_hit(row: Mapping[str, str], spec: Mapping[str, Any]) -> bool:
    minutes = s167.minutes_for(row)
    return minutes is not None and float(spec["pre_min"]) <= minutes <= float(spec["pre_max"])


def wide_lowedge_hit(row: Mapping[str, str], spec: Mapping[str, Any]) -> bool:
    minutes = s167.minutes_for(row)
    margin = s167.margin_for(row)
    session_hit = minutes is not None and float(spec["wide_session_min"]) <= minutes <= float(spec["wide_session_max"])
    margin_hit = float(spec["wide_margin_min"]) <= margin <= float(spec["wide_margin_max"])
    return session_hit or margin_hit


def gate_value(row: Mapping[str, str], variant: repair.RepairVariant) -> float:
    signal = int(round(parse_float(row.get(s161.SIGNAL_COLUMN), 0.0)))
    if signal == 0:
        return 0.0
    spec = s161.CONTEXT_GATE_SPECS[variant.adapter_id]
    extra = VARIANT_EXTRAS[variant.adapter_id]
    if signal > 0 and str(extra["long_block_rule"]) == "lowedge_gate" and lowedge_hit(row, spec):
        return 2.0
    if signal < 0:
        rule = str(extra["short_block_rule"])
        if rule == "lowedge_or_pre" and (lowedge_hit(row, spec) or pre_hit(row, spec)):
            return 1.0
        if rule == "wide_lowedge" and wide_lowedge_hit(row, spec):
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
    values["InpBlockLongFeatureRange"] = str(extra["long_block_rule"]) != "none"
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
                magic = 17210000 + variant_index * 100 + (1 if split == "validation_is" else 50) + role_index
                attempts.append(
                    s161.base.attempt_payload(
                        run_root=variant_root,
                        run_id=RUN_ID,
                        stage_number=172,
                        exploration_label="stage172_BaselineAdapter__ValidationDrawdownConcentrationRepair",
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
    context_specs = {
        variant.adapter_id: {
            "gate_column": f"stage172_gate_{VARIANT_EXTRAS[variant.adapter_id]['axis']}",
            "gate_type": "encoded_validation_dd_concentration_context_block",
            "block_mode": VARIANT_EXTRAS[variant.adapter_id]["block_mode"],
            "session_min": 170.0,
            "session_max": 265.0,
            "margin_min": 0.04,
            "margin_max": 0.0775,
            "pre_min": 90.0,
            "pre_max": 170.0,
            "wide_session_min": 150.0,
            "wide_session_max": 300.0,
            "wide_margin_min": 0.035,
            "wide_margin_max": 0.085,
            "description": "Stage172 encoded gate: value 1 blocks short, value 2 blocks long when enabled.",
        }
        for variant in VARIANTS
    }
    for name, value in {
        "STAGE_ID": STAGE_ID,
        "RUN_NUMBER": RUN_NUMBER,
        "RUN_ID": RUN_ID,
        "PACKET_ID": PACKET_ID,
        "PARENT_RUN_ID": PARENT_RUN_ID,
        "NEXT_STAGE_ID": NEXT_STAGE_ID,
        "NEXT_RUN_ID": NEXT_RUN_ID,
        "NEXT_PACKET_ID": NEXT_PACKET_ID,
        "SOURCE_ADAPTER_ID": SOURCE_ADAPTER_ID,
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
        "CONTEXT_GATE_SPECS": context_specs,
    }.items():
        setattr(s161, name, value)
    s161.gate_value = gate_value
    s161.extra_set_values = extra_set_values
    s161.build_attempts = build_attempts
    s161._CONTEXT_LOOKUP = None


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


def monthly_rows(run_id: str, adapter_id: str, split: str, closed: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    buckets: dict[str, list[float]] = {}
    for row in closed:
        month = str(row.get("time", ""))[:7]
        if month:
            buckets.setdefault(month, []).append(float(row.get("net_pnl", s171.deal_pnl(row))))
    rows = []
    for month, values in sorted(buckets.items()):
        pf = s171.profit_factor(values)
        quality = "acceptable_measurement_only"
        if sum(values) < 0:
            quality = "negative_month"
        elif isinstance(pf, float) and pf < LEGACY_34D["profit_factor"]:
            quality = "pf_below_34d"
        rows.append(
            {
                "run_id": run_id,
                "adapter_id": adapter_id,
                "split": split,
                "month": month,
                "trade_count": len(values),
                "net_profit": round(sum(values), 4),
                "profit_factor": pf,
                "winner_count": sum(1 for value in values if value > 0),
                "loser_count": sum(1 for value in values if value < 0),
                "quality_flag": quality,
            }
        )
    return rows


def balance_points(deals: Sequence[Mapping[str, Any]], closed: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    start_balance = s171.initial_balance(deals)
    points = [{"time": deals[0]["time"] if deals else "", "balance": start_balance, "profit": 0.0}]
    running_balance = start_balance
    for row in closed:
        pnl = float(row.get("net_pnl", s171.deal_pnl(row)))
        running_balance += pnl
        points.append({"time": row["time"], "balance": round(running_balance, 4), "profit": pnl})
    return points


def split_segment_flags(segment_rows: Sequence[Mapping[str, Any]], adapter_id: str, split: str) -> str:
    flags: list[str] = []
    for segment in ("early", "mid", "late"):
        row = segment_row(segment_rows, adapter_id, split, segment)
        if not row:
            continue
        pf = as_float(row, "profit_factor")
        if pf < LEGACY_34D["profit_factor"]:
            flags.append(segment)
    return ";".join(flags)


def build_curve_audit(
    summary_rows: Sequence[Mapping[str, Any]],
    segment_rows: Sequence[Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    balance_rows: list[dict[str, Any]] = []
    monthly: list[dict[str, Any]] = []
    concentration_rows: list[dict[str, Any]] = []
    drawdown_rows: list[dict[str, Any]] = []
    for variant in VARIANTS:
        for split in ("validation_is", "oos"):
            row = actual_row(summary_rows, variant.adapter_id, split)
            report_value = str(row.get("report_path") or "")
            if not report_value:
                continue
            report_path = Path(report_value)
            if not path_exists(report_path):
                report_path = io_path(REPO_ROOT / report_path)
            if not path_exists(report_path):
                balance_rows.append(
                    {
                        "run_id": RUN_ID,
                        "adapter_id": variant.adapter_id,
                        "split": split,
                        "status": "missing_report",
                        "report_path": report_value,
                    }
                )
                continue
            deals, report_metrics = s171.parse_report_deals(report_path)
            closed = s171.out_deals(deals)
            points = balance_points(deals, closed)
            start_balance = float(points[0]["balance"]) if points else 0.0
            final_balance = float(points[-1]["balance"]) if points else start_balance
            net = final_balance - start_balance
            dd = s171.drawdown_stats(points)
            conc = s171.concentration_stats(closed, net)
            late = segment_row(segment_rows, variant.adapter_id, split, "late")
            late_share = as_float(late, "net_profit") / net if abs(net) > 1e-9 else 0.0
            weak_segments = split_segment_flags(segment_rows, variant.adapter_id, split)
            flags: list[str] = []
            if split == "validation_is" and float(dd.get("max_drawdown_percent") or 0.0) > LEGACY_34D["max_drawdown_percent"]:
                flags.append("validation_dd_above_34d")
            if split == "validation_is" and weak_segments:
                flags.append("validation_segment_pf_below_34d")
            if split == "validation_is" and late_share > 0.50:
                flags.append("validation_late_concentration_above_50pct")
            if split == "oos" and as_float(row, "profit_factor") < LEGACY_34D["profit_factor"]:
                flags.append("oos_pf_below_34d")
            if split == "oos" and float(dd.get("max_drawdown_percent") or 0.0) > LEGACY_34D["max_drawdown_percent"]:
                flags.append("oos_dd_above_34d")
            if split == "oos" and late_share > 0.50:
                flags.append("oos_late_concentration_above_50pct")
            balance_rows.append(
                {
                    "run_id": RUN_ID,
                    "adapter_id": variant.adapter_id,
                    "split": split,
                    "status": "completed",
                    "report_path": rel(report_path),
                    "initial_balance": round(start_balance, 4),
                    "final_balance": round(final_balance, 4),
                    "net_profit": round(net, 4),
                    "closed_trade_count": len(closed),
                    "profit_factor": s171.profit_factor([float(row_.get("net_pnl", s171.deal_pnl(row_))) for row_ in closed]),
                    "legacy_34d_pf": LEGACY_34D["profit_factor"],
                    "legacy_34d_dd_percent": LEGACY_34D["max_drawdown_percent"],
                    "max_drawdown_amount": dd.get("max_drawdown_amount", ""),
                    "max_drawdown_percent": dd.get("max_drawdown_percent", ""),
                    "report_balance_drawdown_maximal": report_metrics.get("balance_drawdown_maximal", ""),
                    "report_equity_drawdown_maximal": report_metrics.get("equity_drawdown_maximal", ""),
                    "report_balance_drawdown_relative": report_metrics.get("balance_drawdown_relative", ""),
                    "report_equity_drawdown_relative": report_metrics.get("equity_drawdown_relative", ""),
                    "late_net_share": round(late_share, 4),
                    "weak_segments": weak_segments,
                    "split_quality_flag": ";".join(flags) if flags else "acceptable_measurement_only",
                }
            )
            concentration_rows.append({"run_id": RUN_ID, "adapter_id": variant.adapter_id, "split": split, **conc})
            drawdown_rows.append(
                {
                    "run_id": RUN_ID,
                    "adapter_id": variant.adapter_id,
                    "split": split,
                    **dd,
                    "drawdown_flag": (
                        "dd_above_34d"
                        if float(dd.get("max_drawdown_percent") or 0.0) > LEGACY_34D["max_drawdown_percent"]
                        else "dd_measurement_only"
                    ),
                }
            )
            monthly.extend(monthly_rows(RUN_ID, variant.adapter_id, split, closed))
    return balance_rows, monthly, concentration_rows, drawdown_rows


def balance_lookup(balance_rows: Sequence[Mapping[str, Any]], adapter_id: str, split: str) -> Mapping[str, Any]:
    for row in balance_rows:
        if row.get("adapter_id") == adapter_id and row.get("split") == split:
            return row
    return {}


def quality_rows(
    summary_rows: Sequence[Mapping[str, Any]],
    segment_rows: Sequence[Mapping[str, Any]],
    balance_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for variant in VARIANTS:
        val = actual_row(summary_rows, variant.adapter_id, "validation_is")
        oos = actual_row(summary_rows, variant.adapter_id, "oos")
        val_bal = balance_lookup(balance_rows, variant.adapter_id, "validation_is")
        oos_bal = balance_lookup(balance_rows, variant.adapter_id, "oos")
        val_early = segment_row(segment_rows, variant.adapter_id, "validation_is", "early")
        val_mid = segment_row(segment_rows, variant.adapter_id, "validation_is", "mid")
        val_late = segment_row(segment_rows, variant.adapter_id, "validation_is", "late")
        oos_late = segment_row(segment_rows, variant.adapter_id, "oos", "late")
        val_net = as_float(val, "net_profit")
        oos_net = as_float(oos, "net_profit")
        val_late_share = as_float(val_late, "net_profit") / val_net if abs(val_net) > 1e-9 else 0.0
        oos_late_share = as_float(oos_late, "net_profit") / oos_net if abs(oos_net) > 1e-9 else 0.0
        flags: list[str] = []
        if as_float(val, "profit_factor") < LEGACY_34D["profit_factor"]:
            flags.append("validation_pf_below_34d")
        if val_net < LEGACY_34D["net_profit"]:
            flags.append("validation_net_below_34d")
        if as_float(val_bal, "max_drawdown_percent", 99.0) > LEGACY_34D["max_drawdown_percent"]:
            flags.append("validation_balance_dd_above_34d")
        if as_float(val_early, "profit_factor") < LEGACY_34D["profit_factor"]:
            flags.append("validation_early_pf_below_34d")
        if as_float(val_mid, "profit_factor") < LEGACY_34D["profit_factor"]:
            flags.append("validation_mid_pf_below_34d")
        if val_late_share > 0.50:
            flags.append("validation_late_concentration_above_50pct")
        if as_float(oos, "profit_factor") < LEGACY_34D["profit_factor"]:
            flags.append("oos_pf_below_34d")
        if as_float(oos_bal, "max_drawdown_percent", 99.0) > LEGACY_34D["max_drawdown_percent"]:
            flags.append("oos_balance_dd_above_34d")
        if oos_net < STAGE171_PRIMARY["oos_net"] * 0.85:
            flags.append("oos_net_materially_below_stage171_primary")
        rows.append(
            {
                "adapter_id": variant.adapter_id,
                "label": variant.label,
                "axis": VARIANT_EXTRAS[variant.adapter_id]["axis"],
                "short_block_rule": VARIANT_EXTRAS[variant.adapter_id]["short_block_rule"],
                "atr_stop_multiplier": variant.atr_stop_multiplier,
                "atr_take_profit_multiplier": variant.atr_take_profit_multiplier,
                "model_risk_max_pct": variant.model_risk_max_pct,
                "validation_pf": as_float(val, "profit_factor"),
                "validation_net": val_net,
                "validation_net_gap_vs_34d": val_net - LEGACY_34D["net_profit"],
                "validation_balance_dd_percent": as_float(val_bal, "max_drawdown_percent"),
                "validation_dd_margin_vs_34d": LEGACY_34D["max_drawdown_percent"] - as_float(val_bal, "max_drawdown_percent", 99.0),
                "validation_early_pf": as_float(val_early, "profit_factor"),
                "validation_mid_pf": as_float(val_mid, "profit_factor"),
                "validation_late_pf": as_float(val_late, "profit_factor"),
                "validation_late_net_share": round(val_late_share, 4),
                "oos_pf": as_float(oos, "profit_factor"),
                "oos_net": oos_net,
                "oos_balance_dd_percent": as_float(oos_bal, "max_drawdown_percent"),
                "oos_late_net_share": round(oos_late_share, 4),
                "stage171_validation_dd_delta": as_float(val_bal, "max_drawdown_percent") - STAGE171_PRIMARY["validation_balance_dd_percent"],
                "stage171_validation_net_delta": val_net - STAGE171_PRIMARY["validation_net"],
                "stage171_oos_net_delta": oos_net - STAGE171_PRIMARY["oos_net"],
                "quality_flags": ";".join(flags) if flags else "stage172_hard_quality_pass_review_required",
                "hard_quality_pass": not flags,
            }
        )
    return rows


def decide(rows: Sequence[Mapping[str, Any]], external: str) -> str:
    if external != "completed":
        return "continue_stage172_runtime_completion_due_to_incomplete_runtime_candidate_not_final"
    if any(row.get("hard_quality_pass") for row in rows):
        return "open_stage173_repair_followup_review_candidate_not_final"
    return "open_stage173_bounded_repair_followup_due_to_drawdown_net_tradeoff_candidate_not_final"


def best_row(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    if not rows:
        return {}
    return max(
        rows,
        key=lambda row: (
            bool(row.get("hard_quality_pass")),
            as_float(row, "validation_dd_margin_vs_34d", -99.0),
            as_float(row, "validation_pf"),
            as_float(row, "validation_net"),
            as_float(row, "oos_pf"),
        ),
    )


def kpi_table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | SL(손절) | risk(위험) | val PF(검증 수익요인) | val net(검증 순손익) | val DD%(검증 낙폭) | early/mid PF(초반/중반 수익요인) | late share(후반 비중) | OOS PF(표본외 수익요인) | OOS net(표본외 순손익) | flags(표식) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {adapter_id} | {atr_stop_multiplier:.3f} | {model_risk_max_pct:.4f} | {validation_pf:.6f} | {validation_net:.2f} | {validation_balance_dd_percent:.4f} | {validation_early_pf:.6f}/{validation_mid_pf:.6f} | {validation_late_net_share:.4f} | {oos_pf:.6f} | {oos_net:.2f} | {quality_flags} |".format(
                **row
            )
        )
    return "\n".join(lines)


def report_markdown(rows: Sequence[Mapping[str, Any]], decision: str, external: str) -> str:
    best = best_row(rows)
    return f"""# Stage172 Validation Drawdown Concentration Repair Report(172단계 검증 낙폭 집중도 수정 보고서)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_adapter(원천 어댑터): `{SOURCE_ADAPTER_ID}`
- external_verification_status(외부 검증 상태): `{external}`
- decision(판정): `{decision}`
- boundary(주장 경계): `{BOUNDARY}`

## Experiment Design(실험 설계)

- hypothesis(가설): Stage171(171단계)에서 확인한 validation DD(검증 낙폭)와 late concentration(후반 집중)은 entry model(진입 모델)을 바꾸지 않고 ATR SL(ATR 손절), bounded risk cap(경계 위험 상한), context gate(문맥 제한문)만 좁게 조정하면 완화될 수 있다.
- decision_use(판정 용도): 34D KPI(34D 핵심 성과 지표) 이상으로 계속 밀 후보가 있는지, 아니면 Stage173(173단계)에서 새 bounded repair(경계 수정)를 열어야 하는지 정한다.
- comparison_baseline(비교 기준): Stage171 primary(171단계 주 후보) `{SOURCE_ADAPTER_ID}` validation net(검증 순손익) `{STAGE171_PRIMARY["validation_net"]}`, validation DD(검증 낙폭) `{STAGE171_PRIMARY["validation_balance_dd_percent"]}`, OOS net(표본외 순손익) `{STAGE171_PRIMARY["oos_net"]}`.
- control_variables(고정 변수): model source(모델 원천), signal column(신호 열), validation/OOS split(검증/표본외 분할), Tier B disabled(티어 B 비활성), thresholds(문턱값) short 0.54 / long 0.52, hold 3 bars(3봉 보유), cooldown 5 bars(5봉 대기).
- changed_variables(변경 변수): ATR stop multiplier(ATR 손절 배수), model risk cap(모델 위험 상한), short context gate width(숏 문맥 제한 폭).
- sample_scope(표본 범위): FPMarkets US100 M5(브로커 US100 5분봉), validation(검증) 2025-01-01~2025-09-30, OOS(표본외) 2025-10-01~2026-04-13.
- success_criteria(성공 기준): validation PF/net/DD(검증 수익요인/순손익/낙폭)가 34D 이상 또는 이내이고, early/mid PF(초반/중반 수익요인), late concentration(후반 집중), OOS PF/DD/net(표본외 수익요인/낙폭/순손익)가 함께 보존된다.
- failure_criteria(실패 기준): net(순손익)만 좋아지거나, DD(낙폭)만 좋아지면서 34D net(34D 순손익)과 segment PF(구간 수익요인)를 훼손한다.
- invalid_conditions(무효 조건): MT5 Strategy Tester(메타트레이더5 전략 테스터) report(보고서), telemetry(텔레메트리), risk/ATR record(위험/ATR 기록), artifact hash(산출물 해시)가 누락된다.
- stop_conditions(정지 조건): 이 4개 bounded variants(경계 변형)를 측정하면 Stage172(172단계)는 닫고 Stage173(173단계)로 넘긴다.
- evidence_plan(근거 계획): summary CSV(요약 CSV), segment KPI(구간 핵심 성과 지표), balance curve audit(잔고 곡선 감사), monthly KPI(월별 핵심 성과 지표), concentration report(집중도 보고), risk/ATR telemetry(위험/ATR 텔레메트리), ledgers(장부), current truth(현재 진실).

## KPI Read(KPI 판독)

{kpi_table(rows)}

## Best Read(최선 판독)

- best_adapter(최선 어댑터): `{best.get("adapter_id", "none")}`
- validation_net(검증 순손익): `{as_float(best, "validation_net"):.2f}`
- validation_balance_dd(검증 잔고 낙폭): `{as_float(best, "validation_balance_dd_percent"):.4f}`
- validation_late_share(검증 후반 비중): `{as_float(best, "validation_late_net_share"):.4f}`
- oos_pf(표본외 수익요인): `{as_float(best, "oos_pf"):.6f}`
- quality_flags(품질 표식): `{best.get("quality_flags", "")}`

## Judgment(판정)

Stage172(172단계)는 deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위)를 만들지 않는다. Effect(효과): 결과가 좋아도 research/development only(연구개발 전용) 후보로만 남긴다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
"""


def decision_markdown(decision: str, external: str) -> str:
    return f"""# Stage172 Decision(172단계 판정)

- decision(판정): `{decision}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_adapter(원천 어댑터): `{SOURCE_ADAPTER_ID}`
- source_stage171_closeout_commit(원천 171단계 종료 커밋): `{SOURCE_STAGE171_CLOSEOUT_COMMIT}`
- source_stage171_hash_record_commit(원천 171단계 해시 기록 커밋): `{SOURCE_STAGE171_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{external}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary_csv(요약 CSV): `{rel(SUMMARY_CSV_PATH)}`
- segment_kpi(구간 핵심 성과 지표): `{rel(SEGMENT_KPI_PATH)}`
- balance_curve_audit(잔고 곡선 감사): `{rel(BALANCE_CURVE_AUDIT_PATH)}`
- monthly_kpi(월별 핵심 성과 지표): `{rel(MONTHLY_KPI_PATH)}`
- concentration_risk(집중 위험): `{rel(CONCENTRATION_PATH)}`
- risk_atr_telemetry(위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage172(172단계) closeout(종료)는 overall goal complete(전체 목표 완료)가 아니다. Effect(효과): Stage173(173단계)에서 KPI(핵심 성과 지표) tradeoff(상충)를 다시 판독하거나 추가 bounded repair(경계 수정)를 연다.
"""


def artifact_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    now = utc_now()
    rows: list[dict[str, Any]] = []
    paths = (
        PRODUCER_PATH,
        REPORT_PATH,
        DECISION_PATH,
        SUMMARY_JSON_PATH,
        SUMMARY_CSV_PATH,
        SEGMENT_KPI_PATH,
        BALANCE_CURVE_AUDIT_PATH,
        MONTHLY_KPI_PATH,
        CONCENTRATION_PATH,
        DRAWDOWN_PATH,
        QUALITY_MATRIX_PATH,
        RISK_ATR_TELEMETRY_PATH,
        GATE_FEATURE_SUMMARY_PATH,
        PROBABILITY_BINDING_PATH,
        MODEL_SCORE_AUDIT_PATH,
        TIER_B_DIAGNOSTIC_PATH,
        AUDIT_CSV_PATH,
        STAGE_LEDGER_PATH,
    )
    for path in paths:
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{Path(path).name}",
                    "artifact_type": "stage172_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": now,
                    "notes": "Stage172 validation drawdown concentration repair evidence.",
                }
            )
    for report in result.get("reports", []):
        if not isinstance(report, Mapping):
            continue
        path = Path(str(report.get("report_path") or ""))
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__mt5_report__{path.stem}",
                    "artifact_type": "mt5_strategy_tester_report",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": now,
                    "notes": "Stage172 MT5 Strategy Tester report.",
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
                "lane": "baseline_adapter_stage172_validation_drawdown_concentration_repair",
                "status": status,
                "judgment": decision,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_stage171_closeout_commit", SOURCE_STAGE171_CLOSEOUT_COMMIT),
                        ("source_stage171_hash_record_commit", SOURCE_STAGE171_HASH_RECORD_COMMIT),
                        ("source_adapter", SOURCE_ADAPTER_ID),
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
                "kpi_scope": "stage172_validation_drawdown_concentration_repair",
                "scoreboard_lane": "runtime_probe",
                "status": status,
                "judgment": decision,
                "path": rel(DECISION_PATH),
                "primary_kpi": "mt5_kpi_records=0",
                "guardrail_kpi": f"target_surface={TARGET_SURFACE}",
                "external_verification_status": external,
                "notes": "Stage172 materialized or blocked before KPI records were available.",
            }
        ]
    for row in alpha_rows:
        row["parent_run_id"] = row.get("parent_run_id") or PARENT_RUN_ID
    return {
        "run_registry": run_payload,
        "alpha_ledger": upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id"),
        "stage_ledger": upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id"),
        "artifact_registry": upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, list(artifacts), key="artifact_id"),
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
        "balance_curve_audit": rel(BALANCE_CURVE_AUDIT_PATH),
        "monthly_kpi": rel(MONTHLY_KPI_PATH),
        "concentration_risk": rel(CONCENTRATION_PATH),
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
        f"""# Stage172 Closeout Packet(172단계 종료 작업 묶음)

- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- status(상태): `{status}`
- decision(판정): `{decision}`
- report(보고서): `{rel(REPORT_PATH)}`
- overall_goal_complete(전체 목표 완료): `false`
- boundary(주장 경계): `{BOUNDARY}`
""",
    )


def write_next_stage_seed(decision: str, external: str) -> None:
    if external != "completed":
        return
    write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage173(173단계)는 Stage172(172단계) repair(수정) 결과를 follow-up review(후속 검토)한다.

## Bounded Question(경계 질문)

Did Stage172(172단계) produce a v2-native(브이투 고유) BaselineAdapter(기준선 어댑터) candidate(후보) that truly improves validation DD(검증 낙폭), segment PF(구간 수익요인), late concentration(후반 집중), and OOS(표본외) preservation(보존) toward or beyond legacy 34D KPI(레거시 34D 핵심 성과 지표)?

Effect(효과): Stage172(172단계) 안에서 고치기를 계속하지 않고, KPI(핵심 성과 지표) 상충을 별도 단계에서 판독한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage173 Inputs(173단계 입력)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{decision}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary_csv(요약 CSV): `{rel(SUMMARY_CSV_PATH)}`
- quality_matrix(품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- balance_curve_audit(잔고 곡선 감사): `{rel(BALANCE_CURVE_AUDIT_PATH)}`
- decision_path(판정 파일): `{rel(DECISION_PATH)}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage173 Review Index(173단계 검토 색인)

- status(상태): `open_planned_from_stage172`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{decision}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage173 Selection Status(173단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage172`
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
  Stage172(172단계) closed(종료) as `{decision}` and Stage173(173단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): validation drawdown/concentration repair(검증 낙폭/집중도 수정) 결과를 별도 follow-up review(후속 검토)로 넘긴다.
- >-
  Stage172 evidence(172단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(SUMMARY_CSV_PATH)}`, `{rel(QUALITY_MATRIX_PATH)}`, `{rel(BALANCE_CURVE_AUDIT_PATH)}`, `{rel(RISK_ATR_TELEMETRY_PATH)}`에 있다. Effect(효과): net(순손익), PF(수익요인), DD(낙폭), segment(구간), concentration(집중도), ATR/risk telemetry(ATR/위험 기록)를 같이 본다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)만 계속한다.

"""
    else:
        focus = f"""current_focus:
- >-
  Stage172(172단계) runtime evidence(런타임 근거)가 incomplete(불완전)하여 `{decision}`로 기록했다. Effect(효과): 완료 주장을 낮추고 Stage172 runtime completion(런타임 완료) 조건을 보존한다.

"""
    state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, state, count=1)
    state = re.sub(r"(?ms)^stage172_validation_drawdown_concentration_repair:\r?\n.*?(?=^stage\d+_|\Z)", "", state)
    block = f"""
stage172_validation_drawdown_concentration_repair:
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
  quality_matrix_path: {rel(QUALITY_MATRIX_PATH)}
  balance_curve_audit_path: {rel(BALANCE_CURVE_AUDIT_PATH)}
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
- adapter_under_review(검토 중 어댑터): `stage172_validation_drawdown_concentration_repair_surface`
- status(상태): `stage172_{decision}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage172(172단계)는 Stage171(171단계)의 near-34D(34D 근접) 후보를 validation DD/concentration repair(검증 낙폭/집중도 수정)로 측정했다. Effect(효과): Stage173(173단계)는 결과를 final(최종)로 보지 않고 follow-up review(후속 검토)로 판독한다.

## Latest Stage172 Evidence(최신 172단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- external_verification_status(외부 검증 상태): `{external}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- quality_matrix(품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- balance_curve_audit(잔고 곡선 감사): `{rel(BALANCE_CURVE_AUDIT_PATH)}`
- risk_atr_telemetry(위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
""",
    )


def write_status_files(decision: str, external: str) -> None:
    status = f"closed_{decision}" if external == "completed" else "blocked_runtime_incomplete"
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage172 Selection Status(172단계 선택 상태)

- stage_status(단계 상태): `{status}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- external_verification_status(외부 검증 상태): `{external}`
- decision(판정): `{decision}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID if external == 'completed' else STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )
    write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage172 Review Index(172단계 검토 색인)

- status(상태): `{status}`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- quality_matrix(품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- segment_kpi(구간 핵심 성과 지표): `{rel(SEGMENT_KPI_PATH)}`
- balance_curve_audit(잔고 곡선 감사): `{rel(BALANCE_CURVE_AUDIT_PATH)}`
- risk_atr_telemetry(위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID if external == 'completed' else STAGE_ID}`
""",
    )


def append_changelog(decision: str) -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {utc_now()} Stage172 validation drawdown concentration repair closeout(172단계 검증 낙폭 집중도 수정 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{decision}`.\n"
        "- effect(효과): ATR SL(ATR 손절), risk cap(위험 상한), context gate(문맥 제한문) 변형을 MT5(MetaTrader 5, 메타트레이더5)로 측정하고 Stage173(173단계) follow-up review(후속 검토)로 넘겼다.\n"
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
        "stage_number": 172,
        "run_number": RUN_NUMBER,
        "run_root": RUN_ROOT,
        "packet_id": PACKET_ID,
        "attempts": attempts,
        "common_copies": inputs["common_copies"],
        "feature_exports": inputs["feature_exports"],
        "model_artifacts": inputs["model_exports"],
        "route_coverage": s161.base.engine.route_coverage(),
        "model_family": "baseline_adapter_stage172_v2_native_validation_drawdown_concentration_repair",
        "feature_set_id": "stage172_signal_plus_encoded_validation_dd_concentration_gate",
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
    balance_rows, monthly_rows_, concentration_rows, drawdown_rows = build_curve_audit(summary_rows, segment_rows)
    quality = quality_rows(summary_rows, segment_rows, balance_rows)
    external = str(result.get("external_verification_status") or "blocked")
    decision = decide(quality, external)

    s161.write_run_identity(result, probability_rows, model_rows)
    s161.write_csv(AUDIT_CSV_PATH, audit_rows)
    s161.write_csv(SUMMARY_CSV_PATH, summary_rows)
    s161.write_csv(SEGMENT_KPI_PATH, segment_rows)
    s161.write_csv(BALANCE_CURVE_AUDIT_PATH, balance_rows)
    s161.write_csv(MONTHLY_KPI_PATH, monthly_rows_)
    s161.write_csv(CONCENTRATION_PATH, concentration_rows)
    s161.write_csv(DRAWDOWN_PATH, drawdown_rows)
    s161.write_csv(QUALITY_MATRIX_PATH, quality)
    s161.write_csv(RISK_ATR_TELEMETRY_PATH, risk_rows)
    s161.write_csv(GATE_FEATURE_SUMMARY_PATH, inputs["gate_rows"])
    s161.write_csv(PROBABILITY_BINDING_PATH, probability_rows)
    s161.write_csv(MODEL_SCORE_AUDIT_PATH, model_rows)
    s161.write_csv(TIER_B_DIAGNOSTIC_PATH, s161.tier_b_rows())
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
            "balance_rows": balance_rows,
            "monthly_rows": monthly_rows_,
            "concentration_rows": concentration_rows,
            "drawdown_rows": drawdown_rows,
            "probability_rows": probability_rows,
            "model_rows": model_rows,
            "quality_rows": quality,
            "gate_rows": inputs["gate_rows"],
            "legacy_34d": LEGACY_34D,
            "stage171_primary": STAGE171_PRIMARY,
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
                    "quality_matrix": rel(QUALITY_MATRIX_PATH),
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
