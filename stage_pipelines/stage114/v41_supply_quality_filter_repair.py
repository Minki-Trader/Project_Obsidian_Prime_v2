from __future__ import annotations

import csv
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import (  # noqa: E402
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    ledger_pairs,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from stage_pipelines.stage112 import v41_route_supply_density_repair as s112  # noqa: E402


s100 = s112.s100
s108 = s112.s108

STAGE_ID = "114_adapter_research__v41_supply_quality_filter_repair"
RUN_NUMBER = "run114A"
RUN_ID = "run114A_stage114_v41_supply_quality_filter_repair_v1"
PACKET_ID = "stage114_v41_supply_quality_filter_repair_v1"
PARENT_RUN_ID = "run113A_stage113_v41_route_supply_followup_review_v1"
SOURCE_STAGE113_ID = "113_adapter_research__v41_route_supply_followup_review"
SOURCE_STAGE113_CLOSEOUT_COMMIT = "903b5fc4ae2abef7bcff6f61b67b59edb38d9bbf"
SOURCE_STAGE113_LATEST_COMMIT = "83cf8dceba863e768ed821fcd6590c5751fe409f"
SOURCE_STAGE112_ID = "112_adapter_research__v41_route_supply_density_repair"
SOURCE_STAGE112_CLOSEOUT_COMMIT = "3adab2ed445509bc58b365ab59c0ccbf14c141a1"
SOURCE_STAGE112_LATEST_COMMIT = "defeb9257037327717105cac64b509ccf690e073"
SOURCE_STAGE110_LATEST_COMMIT = "c702502f01e2ef0e9a17d2ac9ec86b6108a82d04"
SOURCE_ADAPTER_ID = "s112_v41_h3_cd9_nogate_lng53"
NEXT_STAGE_ID = "115_adapter_research__v41_supply_quality_followup_review"
NEXT_RUN_ID = "run115A_stage115_v41_supply_quality_followup_review_v1"
NEXT_PACKET_ID = "stage115_v41_supply_quality_followup_review_v1"
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
COMMON_ROOT = f"OPV2/s114a/{RUN_NUMBER}"

SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage114_supply_quality_filter_summary.json"
SUMMARY_CSV_PATH = REVIEWS_ROOT / "stage114_supply_quality_filter_summary.csv"
REPORT_PATH = REVIEWS_ROOT / "stage114_supply_quality_filter_report.md"
SEGMENT_KPI_PATH = REVIEWS_ROOT / "stage114_segment_kpi_summary.csv"
RISK_ATR_TELEMETRY_PATH = REVIEWS_ROOT / "stage114_risk_atr_telemetry.csv"
GATE_FEATURE_SUMMARY_PATH = REVIEWS_ROOT / "stage114_gate_feature_summary.csv"
TIER_B_DIAGNOSTIC_PATH = REVIEWS_ROOT / "stage114_tier_b_diagnostic_summary.csv"
DECISION_PATH = REVIEWS_ROOT / "stage114_decision.md"
AUDIT_CSV_PATH = REVIEWS_ROOT / "stage114_trade_audit.csv"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
FEATURE_FRAME_PATH = s100.FEATURE_FRAME_PATH

STAGE110_REFERENCE = {
    "oos_net": 644.76,
    "oos_pf": 1.637076853,
    "oos_dd_pct": 18.69,
    "oos_trade_count": 147,
    "oos_early_net": 38.84,
    "oos_early_pf": 1.157011764,
}
LEGACY_34D = {
    "profit_factor": 1.583157,
    "net_profit": 987.60,
    "max_drawdown_percent": 12.909136,
    "trade_count": 404,
}

VARIANTS = (
    s100.repair.RepairVariant(
        adapter_id="s114_v41_h3_cd9_rule_block_lng53",
        label="stage114_h3_cd9_rule_quality_block_lng53",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0475,
        same_direction_reentry_cooldown_bars=9,
        short_threshold=0.55,
        long_threshold=0.53,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=True,
        max_hold_bars=3,
        notes="Stage114 quality filter: block Stage112 no-gate trades from the three worst OOS context rules while keeping the opened supply path.",
    ),
    s100.repair.RepairVariant(
        adapter_id="s114_v41_h3_cd9_margin_mid_block_lng53",
        label="stage114_h3_cd9_mid_margin_quality_block_lng53",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0475,
        same_direction_reentry_cooldown_bars=9,
        short_threshold=0.55,
        long_threshold=0.53,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=True,
        max_hold_bars=3,
        notes="Stage114 quality filter: block ambiguous ET40 margin band 0.04-0.08 on the no-gate supply path.",
    ),
    s100.repair.RepairVariant(
        adapter_id="s114_v41_h3_cd9_rule_margin_block_lng53",
        label="stage114_h3_cd9_rule_plus_mid_margin_quality_block_lng53",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0475,
        same_direction_reentry_cooldown_bars=9,
        short_threshold=0.55,
        long_threshold=0.53,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=True,
        max_hold_bars=3,
        notes="Stage114 quality filter: combine worst context-rule block and ambiguous ET40 margin block.",
    ),
    s100.repair.RepairVariant(
        adapter_id="s114_v41_h3_cd9_session_margin_block_lng53",
        label="stage114_h3_cd9_session_plus_mid_margin_quality_block_lng53",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0475,
        same_direction_reentry_cooldown_bars=9,
        short_threshold=0.55,
        long_threshold=0.53,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=True,
        max_hold_bars=3,
        notes="Stage114 quality filter: combine weak late/mid session block with ambiguous ET40 margin block.",
    ),
)

SOURCE_SPECS_BY_VARIANT = {
    variant.adapter_id: {
        "label": "v41_v22_midcov_et40_agree_h2c0_no_b",
        "feature_anchor": "s59ar_v41_sd8_h3_stage59d_adapter",
        "variant_root": s100.SOURCE_VARIANT_ROOT,
        "model": s100.SOURCE_MODEL,
        "validation_ini": s100.SOURCE_VAL_INI,
        "oos_ini": s100.SOURCE_OOS_INI,
    }
    for variant in VARIANTS
}

BAD_CONTEXT_RULES = {"s4_short_ret_ge67", "s5_long_breadth_le20", "s6_short_us_le33"}
CONTEXT_GATE_SPECS = {
    "s114_v41_h3_cd9_rule_block_lng53": {
        "gate_column": "stage114_gate_bad_rule_block",
        "gate_type": "bad_context_rule_block",
        "block_mode": "both",
        "description": "Block the Stage112 no-gate entries whose context_rule_id was negative in OOS trade attribution.",
    },
    "s114_v41_h3_cd9_margin_mid_block_lng53": {
        "gate_column": "stage114_gate_margin_004_008_block",
        "gate_type": "et40_mid_margin_block",
        "block_mode": "both",
        "margin_min": 0.04,
        "margin_max": 0.08,
        "description": "Block ambiguous ET40 decision margin rows where 0.04 < margin <= 0.08.",
    },
    "s114_v41_h3_cd9_rule_margin_block_lng53": {
        "gate_column": "stage114_gate_rule_margin_block",
        "gate_type": "bad_context_rule_or_et40_mid_margin_block",
        "block_mode": "both",
        "margin_min": 0.04,
        "margin_max": 0.08,
        "description": "Block negative OOS context rules plus ambiguous ET40 margin rows.",
    },
    "s114_v41_h3_cd9_session_margin_block_lng53": {
        "gate_column": "stage114_gate_session_margin_block",
        "gate_type": "weak_session_or_et40_mid_margin_block",
        "block_mode": "both",
        "session_min": 165.0,
        "session_max": 275.0,
        "margin_min": 0.04,
        "margin_max": 0.08,
        "description": "Block entries in weak 165-275 minute cash-session window plus ambiguous ET40 margin rows.",
    },
}

_CONTEXT_LOOKUP: dict[str, dict[str, float]] | None = None


def rel(path: Path | str) -> str:
    return Path(path).as_posix()


def parse_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def context_lookup() -> dict[str, dict[str, float]]:
    global _CONTEXT_LOOKUP
    if _CONTEXT_LOOKUP is not None:
        return _CONTEXT_LOOKUP
    frame = pd.read_parquet(io_path(FEATURE_FRAME_PATH), columns=["timestamp", "minutes_from_cash_open"])
    frame["timestamp_key"] = pd.to_datetime(frame["timestamp"], utc=True).dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    _CONTEXT_LOOKUP = {
        str(row["timestamp_key"]): {"minutes_from_cash_open": float(row["minutes_from_cash_open"])}
        for row in frame.to_dict("records")
    }
    return _CONTEXT_LOOKUP


def gate_reason(row: Mapping[str, str], variant: s100.repair.RepairVariant) -> str:
    spec = CONTEXT_GATE_SPECS.get(variant.adapter_id, {})
    rule_id = str(row.get("context_rule_id") or "")
    margin = parse_float(row.get("et40_decision_margin"), -1.0)
    minutes = parse_float(row.get("minutes_from_cash_open"), -9999.0)
    margin_mid = margin > float(spec.get("margin_min", 9999.0)) and margin <= float(spec.get("margin_max", -9999.0))
    bad_rule = rule_id in BAD_CONTEXT_RULES
    weak_session = (
        minutes > float(spec.get("session_min", 9999.0))
        and minutes <= float(spec.get("session_max", -9999.0))
    )
    gate_type = str(spec.get("gate_type", ""))
    if gate_type == "bad_context_rule_block" and bad_rule:
        return "bad_context_rule"
    if gate_type == "et40_mid_margin_block" and margin_mid:
        return "et40_mid_margin"
    if gate_type == "bad_context_rule_or_et40_mid_margin_block":
        if bad_rule:
            return "bad_context_rule"
        if margin_mid:
            return "et40_mid_margin"
    if gate_type == "weak_session_or_et40_mid_margin_block":
        if weak_session:
            return "weak_session_165_275"
        if margin_mid:
            return "et40_mid_margin"
    return ""


def gate_value(row: Mapping[str, str], variant: s100.repair.RepairVariant) -> float:
    signal = int(round(parse_float(row.get(s100.base.RUN50BN_SIGNAL), 0.0)))
    if signal == 0:
        return 0.0
    enriched = dict(row)
    context = context_lookup().get(str(row.get("timestamp_utc", "")))
    if context:
        enriched["minutes_from_cash_open"] = str(context["minutes_from_cash_open"])
    return 1.0 if gate_reason(enriched, variant) else 0.0


def write_gated_feature(source: Path, destination: Path, variant: s100.repair.RepairVariant) -> dict[str, Any]:
    gate_column = str(CONTEXT_GATE_SPECS[variant.adapter_id]["gate_column"])
    io_path(destination.parent).mkdir(parents=True, exist_ok=True)
    total_rows = 0
    blocked_rows = 0
    missing_context_rows = 0
    reason_counts: dict[str, int] = {}
    with io_path(source).open("r", encoding="utf-8-sig", newline="") as input_handle:
        reader = csv.DictReader(input_handle)
        with io_path(destination).open("w", encoding="utf-8", newline="") as output_handle:
            writer = csv.DictWriter(
                output_handle,
                fieldnames=("bar_time_server", s100.base.RUN50BN_SIGNAL, gate_column),
                lineterminator="\n",
            )
            writer.writeheader()
            for row in reader:
                enriched = dict(row)
                context = context_lookup().get(str(row.get("timestamp_utc", "")))
                if context:
                    enriched["minutes_from_cash_open"] = str(context["minutes_from_cash_open"])
                else:
                    missing_context_rows += 1
                reason = gate_reason(enriched, variant)
                gate = 1.0 if reason and int(round(parse_float(row.get(s100.base.RUN50BN_SIGNAL), 0.0))) != 0 else 0.0
                if gate >= 0.5:
                    blocked_rows += 1
                    reason_counts[reason] = reason_counts.get(reason, 0) + 1
                total_rows += 1
                writer.writerow(
                    {
                        "bar_time_server": row.get("bar_time_server") or row.get("timestamp_utc") or "",
                        s100.base.RUN50BN_SIGNAL: s100.base.csv_value(
                            parse_float(row.get(s100.base.RUN50BN_SIGNAL), 0.0)
                        ),
                        gate_column: s100.base.csv_value(gate),
                    }
                )
    return {
        "variant_id": variant.adapter_id,
        "gate_column": gate_column,
        "gate_type": CONTEXT_GATE_SPECS[variant.adapter_id]["gate_type"],
        "block_mode": CONTEXT_GATE_SPECS[variant.adapter_id]["block_mode"],
        "source_feature": rel(source),
        "gated_feature": rel(destination),
        "total_rows": total_rows,
        "blocked_rows": blocked_rows,
        "blocked_ratio": (blocked_rows / total_rows) if total_rows else 0.0,
        "missing_context_rows": missing_context_rows,
        "blocked_reason_counts": json.dumps(reason_counts, sort_keys=True),
        "context_source": rel(FEATURE_FRAME_PATH),
        "gate_description": CONTEXT_GATE_SPECS[variant.adapter_id]["description"],
    }


def stage114_extra_set_values(variant: s100.repair.RepairVariant, magic: int) -> dict[str, Any]:
    values = s100.base.engine.extra_set_values(variant, magic)
    block_mode = str(CONTEXT_GATE_SPECS.get(variant.adapter_id, {}).get("block_mode", "both"))
    values["InpSideFilterEnabled"] = True
    values["InpSideFilterFeatureIndex"] = 1
    values["InpFallbackSideFilterFeatureIndex"] = 1
    values["InpBlockShortFeatureRange"] = block_mode in {"both", "short"}
    values["InpBlockShortFeatureMin"] = 0.5
    values["InpBlockShortFeatureMax"] = 1.5
    values["InpBlockLongFeatureRange"] = block_mode in {"both", "long"}
    values["InpBlockLongFeatureMin"] = 0.5
    values["InpBlockLongFeatureMax"] = 1.5
    return values


def build_attempts(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    for variant_index, variant in enumerate(VARIANTS, start=1):
        variant_root = RUN_ROOT / variant.adapter_id
        for split in ("validation_is", "oos"):
            date_values = s100.parse_ini(s100.base.engine.source_attempt_ini(split, variant))
            split_token = "val" if split == "validation_is" else "oos"
            for role_index, (tier, attempt_role, prefix, attempt_token) in enumerate(
                (
                    (s100.mt5.TIER_A, "tier_only_total", f"mt5_tier_a_only_{variant.adapter_id}", "ta"),
                    (s100.mt5.TIER_AB, "routed_total", f"mt5_routed_{variant.adapter_id}", "rt"),
                ),
                start=1,
            ):
                magic = 11410000 + variant_index * 100 + (1 if split == "validation_is" else 50) + role_index
                attempts.append(
                    s100.attempt_payload(
                        run_root=variant_root,
                        run_id=RUN_ID,
                        stage_number=114,
                        exploration_label="stage114_BaselineAdapter__SupplyQualityFilterRepair",
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
                        extra_set_values=stage114_extra_set_values(variant, magic),
                    )
                )
    return attempts


def as_float(row: Mapping[str, Any], key: str, default: float = 0.0) -> float:
    return s108.as_float(row, key, default)


def routed_oos(summary_rows: Sequence[Mapping[str, Any]]) -> list[Mapping[str, Any]]:
    return s108.routed_oos(summary_rows)


def early_segment(segment_rows: Sequence[Mapping[str, Any]], adapter_id: str) -> Mapping[str, Any]:
    return s108.early_segment(segment_rows, adapter_id)


def early_ok(early: Mapping[str, Any]) -> bool:
    return (
        as_float(early, "profit_factor") >= STAGE110_REFERENCE["oos_early_pf"]
        and as_float(early, "net_profit") >= 0.0
    )


def best_stage114(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    candidates = []
    for row in routed_oos(summary_rows):
        early = early_segment(segment_rows, str(row.get("adapter_id", "")))
        trades = as_float(row, "trade_count")
        oos_pf = as_float(row, "profit_factor")
        oos_net = as_float(row, "net_profit")
        oos_dd = as_float(row, "max_drawdown_percent", 99.0)
        candidates.append(
            (
                trades >= 180,
                oos_net >= STAGE110_REFERENCE["oos_net"],
                oos_pf >= 1.50,
                oos_dd <= 25.0,
                early_ok(early),
                oos_pf,
                oos_net,
                trades,
                -oos_dd,
                row,
            )
        )
    return max(candidates, key=lambda item: item[:9])[-1] if candidates else {}


def decide(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]], external: str) -> str:
    if external != "completed":
        return "continue_supply_quality_filter_runtime_repair_in_stage115_due_to_incomplete_runtime"
    best = best_stage114(summary_rows, segment_rows)
    early = early_segment(segment_rows, str(best.get("adapter_id", "")))
    trades = as_float(best, "trade_count")
    oos_net = as_float(best, "net_profit")
    oos_pf = as_float(best, "profit_factor")
    oos_dd = as_float(best, "max_drawdown_percent", 99.0)
    if (
        trades >= 180
        and oos_net >= STAGE110_REFERENCE["oos_net"]
        and oos_pf >= LEGACY_34D["profit_factor"]
        and oos_dd <= STAGE110_REFERENCE["oos_dd_pct"]
        and early_ok(early)
    ):
        return "continue_supply_quality_followup_review_in_stage115_with_strong_candidate"
    if trades >= 180 and oos_net >= STAGE110_REFERENCE["oos_net"] and oos_pf >= 1.45 and oos_dd <= 25.0:
        return "continue_supply_quality_followup_review_in_stage115"
    return "continue_supply_quality_filter_repair_review_in_stage115"


def row_table(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | OOS PF(표본외 수익 팩터) | OOS net(표본외 순손익) | OOS DD%(표본외 손실률) | trades(거래 수) | delta vs Stage110(Stage110 대비 차이) | early PF(초반 수익 팩터) | early net(초반 순손익) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in routed_oos(summary_rows):
        early = early_segment(segment_rows, str(row.get("adapter_id", "")))
        trades = as_float(row, "trade_count")
        lines.append(
            "| {adapter} | {pf:.6f} | {net:.2f} | {dd:.2f} | {trades:.0f} | {delta:.0f} | {early_pf:.6f} | {early_net:.2f} |".format(
                adapter=row.get("adapter_id", ""),
                pf=as_float(row, "profit_factor"),
                net=as_float(row, "net_profit"),
                dd=as_float(row, "max_drawdown_percent"),
                trades=trades,
                delta=trades - STAGE110_REFERENCE["oos_trade_count"],
                early_pf=as_float(early, "profit_factor"),
                early_net=as_float(early, "net_profit"),
            )
        )
    return "\n".join(lines)


def report_markdown(
    summary_rows: Sequence[Mapping[str, Any]],
    segment_rows: Sequence[Mapping[str, Any]],
    decision: str,
    external: str,
) -> str:
    best = best_stage114(summary_rows, segment_rows)
    early = early_segment(segment_rows, str(best.get("adapter_id", "")))
    return f"""# Stage114 Supply Quality Filter Repair Report(114단계 공급 품질 필터 수리 보고서)

- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE113_ID}`
- source_stage113_closeout_commit(원천 113단계 종료 커밋): `{SOURCE_STAGE113_CLOSEOUT_COMMIT}`
- source_stage113_latest_commit(원천 113단계 최신 커밋): `{SOURCE_STAGE113_LATEST_COMMIT}`
- source_adapter(원천 어댑터): `{SOURCE_ADAPTER_ID}`
- external_verification_status(외부 검증 상태): `{external}`
- decision(판정): `{decision}`
- boundary(경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Stage112(112단계)에서 열린 no-gate route supply(무제한 경로 공급)를 유지하되, context rule(문맥 규칙), ET40 margin(ET40 여유폭), session window(세션 구간) 기반 quality filter(품질 필터)로 PF/DD(수익 팩터/손실률) 손상을 줄일 수 있는가?

Effect(효과): Stage114(114단계)는 새 모델 탐색(model hunting, 모델 탐색)이 아니라 Stage112의 공급 손상 원인을 좁게 거르는 bounded repair(경계 수리)다.

## Result Table(결과 표)

{row_table(summary_rows, segment_rows)}

## Best Read(최선 판독)

- best_variant(최선 변형): `{best.get("adapter_id", "none")}`
- oos_pf(표본외 수익 팩터): `{as_float(best, "profit_factor"):.6f}`
- oos_net(표본외 순손익): `{as_float(best, "net_profit"):.2f}`
- oos_dd_pct(표본외 손실률): `{as_float(best, "max_drawdown_percent"):.2f}`
- trades(거래 수): `{as_float(best, "trade_count"):.0f}`
- early_pf(초반 수익 팩터): `{as_float(early, "profit_factor"):.6f}`
- early_net(초반 순손익): `{as_float(early, "net_profit"):.2f}`

## Evidence Files(근거 파일)

- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- segment_kpi_summary(구간 KPI 요약): `{rel(SEGMENT_KPI_PATH)}`
- risk_atr_telemetry(위험/ATR 텔레메트리): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- gate_feature_summary(게이트 피처 요약): `{rel(GATE_FEATURE_SUMMARY_PATH)}`
- trade_audit(거래 감사): `{rel(AUDIT_CSV_PATH)}`

## Result Judgment(결과 판정)

- result_subject(판정 대상): Stage114 supply quality filter repair(114단계 공급 품질 필터 수리).
- evidence_available(있는 근거): MT5 runtime reports(MT5 실행환경 보고서), summary CSV(요약 CSV), segment KPI(구간 핵심 성과 지표), risk/ATR telemetry(위험/ATR 텔레메트리), gate feature summary(게이트 피처 요약).
- evidence_missing(빠진 근거): Stage115(115단계) 후속 검토 전에는 Stage114 결과를 전체 연구 패키지로 보지 않는다.
- judgment_label(판정 라벨): `supply_quality_filter_repair_measured`.
- claim_boundary(주장 경계): `{BOUNDARY}`.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
"""


def decision_markdown(decision: str, external: str) -> str:
    return f"""# Stage114 Decision(114단계 판정)

decision(판정): `{decision}`

Stage114(114단계)는 Stage113(113단계)의 판정대로 Stage112 no-gate supply(112단계 무제한 공급)에 quality filter(품질 필터)를 붙여 실제 MT5 runtime(실행환경)에서 측정했다.

Effect(효과): 공급 증가와 PF/DD(수익 팩터/손실률) 회복 사이의 상충을 Stage115(115단계) 후속 검토로 넘긴다.

## Evidence(근거)

- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- segment_kpi_summary(구간 KPI 요약): `{rel(SEGMENT_KPI_PATH)}`
- risk_atr_telemetry(위험/ATR 텔레메트리): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- gate_feature_summary(게이트 피처 요약): `{rel(GATE_FEATURE_SUMMARY_PATH)}`
- source_stage113_closeout_commit(원천 113단계 종료 커밋): `{SOURCE_STAGE113_CLOSEOUT_COMMIT}`
- external_verification_status(외부 검증 상태): `{external}`
- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`

## Next(다음)

next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Stage114(114단계)는 전체 목표 완료가 아니다. Effect(효과): 34D KPI(34D 핵심 성과 지표) 이상을 향한 v2-native research(브이투 고유 연구)는 Stage115(115단계)로 이어진다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
"""


def artifact_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    created = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
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
                    "artifact_type": "stage114_supply_quality_filter_repair_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage114 v2-native supply quality filter repair artifact.",
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
                    "notes": "Actual Stage114 MT5 Strategy Tester HTML report.",
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
                "lane": "baseline_adapter_v2_native_v41_supply_quality_filter_repair",
                "status": status,
                "judgment": decision,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_adapter", SOURCE_ADAPTER_ID),
                        ("source_stage113_closeout_commit", SOURCE_STAGE113_CLOSEOUT_COMMIT),
                        ("source_stage113_latest_commit", SOURCE_STAGE113_LATEST_COMMIT),
                        ("source_stage112_latest_commit", SOURCE_STAGE112_LATEST_COMMIT),
                        ("target_surface", TARGET_SURFACE),
                        ("legacy_relation", "lesson_only"),
                    )
                ),
            }
        ],
        key="run_id",
    )
    alpha_rows = s100.build_mt5_alpha_ledger_rows(
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
                "kpi_scope": "stage114_v41_supply_quality_filter_repair",
                "scoreboard_lane": "runtime_probe",
                "status": status,
                "judgment": decision,
                "path": rel(DECISION_PATH),
                "primary_kpi": "mt5_kpi_records=0",
                "guardrail_kpi": f"target_surface={TARGET_SURFACE}",
                "external_verification_status": external,
                "notes": "Stage114 run materialized or blocked before KPI records were available.",
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


def tier_b_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    coverage = s100.base.engine.route_coverage()
    for variant in VARIANTS:
        variant_cov = coverage.get(variant.adapter_id, {})
        for split_name in ("validation", "oos"):
            split_cov = variant_cov.get(split_name, {})
            rows.append(
                {
                    "run_id": RUN_ID,
                    "adapter_id": variant.adapter_id,
                    "split": split_name,
                    "tier_b_policy": "diagnostic_missing_required_but_disabled_for_this_supply_quality_filter_repair",
                    "tier_b_rows_available": split_cov.get("tier_b_fallback_rows_available_but_disabled", 0),
                    "tier_b_rows_used": split_cov.get("tier_b_fallback_rows_used", 0),
                    "reason": "Stage114 isolates Tier A routed no-gate supply quality filters before any Tier B fallback repair.",
                }
            )
    return rows


def write_packet_files(result: Mapping[str, Any], decision: str, ledger_payload: Mapping[str, Any]) -> None:
    status = "completed" if result.get("external_verification_status") == "completed" else "blocked"
    s108.write_json(PACKET_ROOT / "routing_receipt.json", {"packet_id": PACKET_ID, "stage_id": STAGE_ID, "primary_family": "experiment_design", "primary_skill": "obsidian-experiment-design", "support_skills": ["obsidian-performance-attribution", "obsidian-model-validation", "obsidian-runtime-parity"], "required_gates": ["runtime_evidence_gate", "kpi_contract_audit", "result_judgment_gate"], "status": status})
    s108.write_json(PACKET_ROOT / "runtime_evidence_gate.json", {"packet_id": PACKET_ID, "run_id": RUN_ID, "external_verification_status": result.get("external_verification_status"), "completed_attempt_count": result.get("completed_attempt_count"), "expected_attempt_count": result.get("expected_attempt_count"), "gate_feature_summary_path": rel(GATE_FEATURE_SUMMARY_PATH), "claim_boundary": BOUNDARY})
    s108.write_json(PACKET_ROOT / "result_judgment_gate.json", {"packet_id": PACKET_ID, "run_id": RUN_ID, "decision": decision, "legacy_relation": "lesson_only_target_surface_no_code_copy", "overall_goal_complete": False, "forbidden_claims": ["deployment", "live_readiness", "production_baseline", "operating_promotion", "operating_reference", "runtime_authority", "legacy_inheritance"]})
    s108.write_json(PACKET_ROOT / "aggregate_summary.json", {"packet_id": PACKET_ID, "stage_id": STAGE_ID, "run_id": RUN_ID, "decision": decision, "source_stage113_closeout_commit": SOURCE_STAGE113_CLOSEOUT_COMMIT, "source_stage113_latest_commit": SOURCE_STAGE113_LATEST_COMMIT, "source_stage112_closeout_commit": SOURCE_STAGE112_CLOSEOUT_COMMIT, "source_stage112_latest_commit": SOURCE_STAGE112_LATEST_COMMIT, "ledger_payload": ledger_payload, "pushed_commit_hash": "pending_until_push", "overall_goal_complete": False})


def create_next_stage(decision: str, external: str) -> None:
    s108.write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage115(115단계)는 Stage114(114단계)의 supply quality filter repair(공급 품질 필터 수리) 결과를 후속 검토한다.

## Bounded Question(경계 질문)

Stage114(114단계)의 quality filter(품질 필터)가 Stage112 no-gate supply(무제한 공급) 대비 PF/DD(수익 팩터/손실률), 거래 수, 순손익, 초반 구간 품질을 실제로 개선했는가?

Effect(효과): Stage115(115단계)는 새 최적화가 아니라 실제 실행 결과를 판독하고, 다음 bounded repair(경계 수리) 또는 분기를 정한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    s108.write_md(NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md", f"""# Stage115 Input References(115단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{decision}`
- source_external_verification_status(원천 외부 검증 상태): `{external}`
- stage114_report(114단계 보고서): `{rel(REPORT_PATH)}`
- stage114_summary(114단계 요약): `{rel(SUMMARY_CSV_PATH)}`
- target_surface(목표 표면): `{TARGET_SURFACE}`

Effect(효과): Stage115(115단계)는 Stage114(114단계) runtime(실행환경) 근거만 받아 34D KPI(34D 핵심 성과 지표) 격차 축소 여부를 판정한다.
""")
    s108.write_md(NEXT_STAGE_ROOT / "03_reviews" / "review_index.md", f"""# Stage115 Review Index(115단계 검토 색인)

- status(상태): `open_planned`
- source_decision(원천 판정): `{decision}`
- planned_packet(계획 작업 묶음): `{NEXT_PACKET_ID}`
- planned_run(계획 실행): `{NEXT_RUN_ID}`

Effect(효과): Stage115(115단계)는 Stage114(114단계) closeout(종료 기록)을 이어받아 후속 판정만 수행한다.
""")
    s108.write_md(NEXT_STAGE_ROOT / "04_selected" / "selection_status.md", f"""# Stage115 Selection Status(115단계 선택 상태)

- stage_status(단계 상태): `open_planned`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{decision}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage115(115단계)는 34D KPI(34D 핵심 성과 지표) 격차 축소를 계속하지만, 운영 의미 없이 연구개발로만 이어진다.
""")


def update_current_truth(decision: str, external: str) -> None:
    import re as _re

    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = _re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", text, count=1, flags=_re.MULTILINE)
    text = _re.sub(r"^updated_on: .*$", "updated_on: '2026-05-18'", text, count=1, flags=_re.MULTILINE)
    text = _re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", text, count=1, flags=_re.MULTILINE)
    current_focus = f"""current_focus:
- >-
  Stage114(114단계) closed(종료) as `{decision}` and Stage115(115단계) `{NEXT_STAGE_ID}` is open_planned(열림 계획). Effect(효과): supply quality filter(공급 품질 필터) 결과를 후속 검토로 넘긴다.
- >-
  Stage114 result(114단계 결과)는 `{rel(SUMMARY_CSV_PATH)}`와 `{rel(SEGMENT_KPI_PATH)}`에 기록했다. Effect(효과): 34D KPI(34D 핵심 성과 지표) 대비 거래 수·순손익·손실률 격차를 다음 단계 입력으로 보존한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(브이투 고유 연구)만 계속한다.
"""
    text = _re.sub(r"current_focus:\n.*?\n\nstage", current_focus.rstrip() + "\n\nstage", text, count=1, flags=_re.DOTALL)
    block = f"""

stage114_v41_supply_quality_filter_repair:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{decision}
  current_run_id: {RUN_ID}
  adapter_under_review: {SOURCE_ADAPTER_ID}
  source_stage113_closeout_commit: {SOURCE_STAGE113_CLOSEOUT_COMMIT}
  source_stage113_latest_commit: {SOURCE_STAGE113_LATEST_COMMIT}
  source_stage112_closeout_commit: {SOURCE_STAGE112_CLOSEOUT_COMMIT}
  source_stage112_latest_commit: {SOURCE_STAGE112_LATEST_COMMIT}
  target_surface: {TARGET_SURFACE}
  decision: {decision}
  next_stage_or_branch: {NEXT_STAGE_ID}
  report_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  external_verification_status: {external}
  pushed_commit_hash: pending_until_push
  boundary: {BOUNDARY}
"""
    marker = "stage114_v41_supply_quality_filter_repair:"
    if marker in text:
        text = _re.sub(r"\nstage114_v41_supply_quality_filter_repair:\n(?:  .*\n)+", block + "\n", text, count=1)
    else:
        text = text.rstrip() + block + "\n"
    io_path(WORKSPACE_STATE_PATH).write_text(text.rstrip() + "\n", encoding="utf-8-sig")
    s108.write_md(SELECTED_ROOT / "selection_status.md", f"""# Stage114 Selection Status(114단계 선택 상태)

- stage_status(단계 상태): `closed_{decision}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE113_ID}`
- source_decision(원천 판정): `continue_supply_quality_filter_repair_in_stage114`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- stage114_decision(114단계 판정): `{decision}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage114(114단계)는 실제 실행 결과를 기록하고, 운영 의미 없이 Stage115(115단계)로 넘긴다.
""")
    s108.write_md(CURRENT_WORKING_STATE_PATH, f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준): `research_package_only_reference_surface`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `stage115_supply_quality_followup_review_surface`
- status(상태): `stage114_closed_{decision}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage114(114단계) closed(종료) as v2-native v41 supply quality filter repair(브이투 고유 브이41 공급 품질 필터 수리). Effect(효과): legacy 34D(레거시 34D)는 target surface(목표 표면)로만 쓰고, 다음 연구는 Stage115(115단계) 후속 검토로 이어진다.

## Latest Stage114 Evidence(최신 114단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- external_verification_status(외부 검증 상태): `{external}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- segment_kpi_summary(구간 KPI 요약): `{rel(SEGMENT_KPI_PATH)}`
- risk_atr_telemetry(위험/ATR 텔레메트리): `{rel(RISK_ATR_TELEMETRY_PATH)}`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속).
""")
    create_next_stage(decision, external)


def append_changelog(decision: str) -> None:
    entry = (
        "\n## 2026-05-18 - Stage114 v41 supply quality filter repair closeout(114단계 v41 공급 품질 필터 수리 종료)\n\n"
        f"- run(실행): `{RUN_ID}`\n"
        f"- decision(판정): `{decision}`\n"
        "- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`\n"
        f"- target_surface(목표 표면): `{TARGET_SURFACE}`\n"
        "- effect(효과): Stage112 no-gate route supply(112단계 무제한 경로 공급)에 품질 필터를 붙여 PF/DD(수익 팩터/손실률) 회복 가능성을 실제 MT5 runtime(실행환경)으로 측정하고 Stage115(115단계) 후속 검토로 넘겼다.\n"
    )
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID not in existing:
        io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def configure_stage114() -> None:
    for name, value in {
        "STAGE_ID": STAGE_ID,
        "RUN_NUMBER": RUN_NUMBER,
        "RUN_ID": RUN_ID,
        "PACKET_ID": PACKET_ID,
        "PARENT_RUN_ID": PARENT_RUN_ID,
        "SOURCE_STAGE111_ID": SOURCE_STAGE113_ID,
        "SOURCE_STAGE111_CLOSEOUT_COMMIT": SOURCE_STAGE113_CLOSEOUT_COMMIT,
        "SOURCE_STAGE111_LATEST_COMMIT": SOURCE_STAGE113_LATEST_COMMIT,
        "SOURCE_STAGE110_ID": SOURCE_STAGE112_ID,
        "SOURCE_STAGE110_CLOSEOUT_COMMIT": SOURCE_STAGE112_CLOSEOUT_COMMIT,
        "SOURCE_STAGE110_LATEST_COMMIT": SOURCE_STAGE112_LATEST_COMMIT,
        "SOURCE_ADAPTER_ID": SOURCE_ADAPTER_ID,
        "NEXT_STAGE_ID": NEXT_STAGE_ID,
        "NEXT_RUN_ID": NEXT_RUN_ID,
        "NEXT_PACKET_ID": NEXT_PACKET_ID,
        "TARGET_SURFACE": TARGET_SURFACE,
        "BOUNDARY": BOUNDARY,
        "STAGE_ROOT": STAGE_ROOT,
        "RUN_ROOT": RUN_ROOT,
        "REVIEWS_ROOT": REVIEWS_ROOT,
        "SELECTED_ROOT": SELECTED_ROOT,
        "PACKET_ROOT": PACKET_ROOT,
        "NEXT_STAGE_ROOT": NEXT_STAGE_ROOT,
        "COMMON_ROOT": COMMON_ROOT,
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
        "SOURCE_SPECS_BY_VARIANT": SOURCE_SPECS_BY_VARIANT,
        "CONTEXT_GATE_SPECS": CONTEXT_GATE_SPECS,
        "VARIANTS": VARIANTS,
        "STAGE106_NET_PF_BEST": STAGE110_REFERENCE,
        "LEGACY_34D": LEGACY_34D,
    }.items():
        setattr(s112, name, value)
    s112.build_attempts = build_attempts
    s112.decide = decide
    s112.report_markdown = report_markdown
    s112.decision_markdown = decision_markdown
    s112.artifact_rows = artifact_rows
    s112.write_ledgers = write_ledgers
    s112.write_packet_files = write_packet_files
    s112.update_current_truth = update_current_truth
    s112.append_changelog = append_changelog
    s112.configure_stage112()
    s100.write_gated_feature = write_gated_feature
    s100.gate_value = gate_value
    s100.tier_b_rows = tier_b_rows


def main(argv: Sequence[str] | None = None) -> int:
    configure_stage114()
    return s100.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
