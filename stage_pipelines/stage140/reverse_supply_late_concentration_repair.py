from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

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
from stage_pipelines.stage138 import trade_supply_repair_after_stage136_no_gain as s138  # noqa: E402


s122 = s138.s122
s100 = s138.s100

STAGE_ID = "140_adapter_research__reverse_supply_late_concentration_repair"
RUN_NUMBER = "run140A"
RUN_ID = "run140A_stage140_reverse_supply_late_concentration_repair_v1"
PACKET_ID = "stage140_reverse_supply_late_concentration_repair_v1"
PARENT_RUN_ID = "run139A_stage139_stage138_trade_supply_followup_review_v1"
SOURCE_STAGE139_ID = "139_adapter_research__stage138_trade_supply_followup_review"
SOURCE_STAGE139_CLOSEOUT_COMMIT = "5ccb7ae5c36b5c83638ee6157d6caa9a49e17031"
SOURCE_STAGE139_HASH_RECORD_COMMIT = "7ddace59be1aac317467dfedc93e0e137d9f2e3c"
SOURCE_STAGE138_ID = "138_adapter_research__trade_supply_repair_after_stage136_no_gain"
SOURCE_STAGE138_CLOSEOUT_COMMIT = "9a5bedb1b1e8e20d13ef1072edeca7039dba1080"
SOURCE_ADAPTER_ID = "s138_reverse_opposite_h3_cd5_risk035"
NEXT_STAGE_ID = "141_adapter_research__stage140_reverse_supply_followup_review"
NEXT_RUN_ID = "run141A_stage141_stage140_reverse_supply_followup_review_v1"
NEXT_PACKET_ID = "stage141_stage140_reverse_supply_followup_review_v1"
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
COMMON_ROOT = f"OPV2/s140a/{RUN_NUMBER}"

SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage140_reverse_supply_repair_summary.json"
SUMMARY_CSV_PATH = REVIEWS_ROOT / "stage140_reverse_supply_repair_summary.csv"
REPORT_PATH = REVIEWS_ROOT / "stage140_reverse_supply_repair_report.md"
SEGMENT_KPI_PATH = REVIEWS_ROOT / "stage140_segment_kpi_summary.csv"
RISK_ATR_TELEMETRY_PATH = REVIEWS_ROOT / "stage140_risk_atr_telemetry.csv"
GATE_FEATURE_SUMMARY_PATH = REVIEWS_ROOT / "stage140_gate_feature_summary.csv"
TIER_B_DIAGNOSTIC_PATH = REVIEWS_ROOT / "stage140_tier_b_diagnostic_summary.csv"
DECISION_PATH = REVIEWS_ROOT / "stage140_decision.md"
AUDIT_CSV_PATH = REVIEWS_ROOT / "stage140_trade_audit.csv"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

LEGACY_34D = {
    "profit_factor": 1.583157,
    "net_profit": 987.60,
    "max_drawdown_percent": 12.909136,
    "trade_count": 404,
}
STAGE138_SOURCE = {
    "profit_factor": 1.80,
    "net_profit": 1186.30,
    "max_drawdown_percent": 14.66,
    "trade_count": 180,
    "validation_profit_factor": 1.58,
    "validation_net_profit": 1388.24,
    "validation_trade_count": 265,
    "validation_late_net_share": 922.40 / 1388.24,
}
STAGE110_REFERENCE = {
    "oos_net": 644.76,
    "oos_pf": 1.637076853,
    "oos_dd_pct": 18.69,
    "oos_trade_count": 147,
}

VARIANTS = (
    s100.repair.RepairVariant(
        adapter_id="s140_reverse_control_h3_cd5_risk035",
        label="stage140_reverse_control_h3_cd5_risk035",
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
        notes="Stage140 control: preserve Stage138 reverse-on-opposite candidate.",
    ),
    s100.repair.RepairVariant(
        adapter_id="s140_reverse_cd3_h3_risk035",
        label="stage140_reverse_cd3_h3_risk035",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0350,
        same_direction_reentry_cooldown_bars=3,
        short_threshold=0.54,
        long_threshold=0.52,
        close_on_flat_signal=False,
        reverse_on_opposite_signal=True,
        close_only_on_opposite_signal=False,
        max_hold_bars=3,
        notes="Stage140 repair: shorten same-direction cooldown under reverse supply.",
    ),
    s100.repair.RepairVariant(
        adapter_id="s140_reverse_cd3_h2_risk035",
        label="stage140_reverse_cd3_h2_risk035",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0350,
        same_direction_reentry_cooldown_bars=3,
        short_threshold=0.54,
        long_threshold=0.52,
        close_on_flat_signal=False,
        reverse_on_opposite_signal=True,
        close_only_on_opposite_signal=False,
        max_hold_bars=2,
        notes="Stage140 repair: combine reverse supply with shorter hold, excluding flat exits.",
    ),
    s100.repair.RepairVariant(
        adapter_id="s140_reverse_sht53_lng51_cd3_h3_risk035",
        label="stage140_reverse_sht53_lng51_cd3_h3_risk035",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0350,
        same_direction_reentry_cooldown_bars=3,
        short_threshold=0.53,
        long_threshold=0.51,
        close_on_flat_signal=False,
        reverse_on_opposite_signal=True,
        close_only_on_opposite_signal=False,
        max_hold_bars=3,
        notes="Stage140 repair: test threshold loosen only inside the reverse supply axis.",
    ),
)

SOURCE_BASELINE_BY_VARIANT = {variant.adapter_id: SOURCE_ADAPTER_ID for variant in VARIANTS}
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
CONTEXT_GATE_SPECS = {
    variant.adapter_id: {
        "gate_column": f"stage140_gate_session_margin_{variant.adapter_id}",
        "gate_type": "weak_session_or_et40_mid_margin_block",
        "block_mode": "both",
        "session_min": 165.0,
        "session_max": 275.0,
        "margin_min": 0.04,
        "margin_max": 0.08,
        "description": f"Stage140 selective reverse supply repair: {variant.label}.",
    }
    for variant in VARIANTS
}


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def source_baseline(row: Mapping[str, Any]) -> Mapping[str, Any]:
    return STAGE138_SOURCE if str(row.get("adapter_id", "")) in SOURCE_BASELINE_BY_VARIANT else {}


def as_float(row: Mapping[str, Any], key: str, default: float = 0.0) -> float:
    return s122.as_float(row, key, default)


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


def validation_late_share(segment_rows: Sequence[Mapping[str, Any]], adapter_id: str) -> float:
    full = next(
        (
            row
            for row in segment_rows
            if row.get("adapter_id") == adapter_id
            and row.get("split") == "validation_is"
            and row.get("view") == "actual_routed_total"
            and row.get("segment_type") == "full_split"
        ),
        {},
    )
    late = segment_row(segment_rows, adapter_id, "validation_is", "late")
    return as_float(late, "net_profit") / as_float(full, "net_profit", 1.0)


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
                magic = 14010000 + variant_index * 100 + (1 if split == "validation_is" else 50) + role_index
                attempts.append(
                    s100.attempt_payload(
                        run_root=variant_root,
                        run_id=RUN_ID,
                        stage_number=140,
                        exploration_label="stage140_BaselineAdapter__ReverseSupplyLateConcentrationRepair",
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
                        extra_set_values=s122.s120.stage120_extra_set_values(variant, magic),
                    )
                )
    return attempts


def best_stage140(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    candidates = []
    for oos in s122.s120.routed_oos(summary_rows):
        adapter_id = str(oos.get("adapter_id", ""))
        val = split_row(summary_rows, adapter_id, "validation_is")
        late_share = validation_late_share(segment_rows, adapter_id)
        oos_trade_gain = as_float(oos, "trade_count") - STAGE138_SOURCE["trade_count"]
        val_trade_gain = as_float(val, "trade_count") - STAGE138_SOURCE["validation_trade_count"]
        safe = (
            as_float(oos, "profit_factor") >= LEGACY_34D["profit_factor"]
            and as_float(oos, "net_profit") >= LEGACY_34D["net_profit"]
            and as_float(oos, "max_drawdown_percent", 99.0) <= 16.5
            and as_float(val, "profit_factor") >= 1.55
            and as_float(val, "net_profit") >= LEGACY_34D["net_profit"]
            and as_float(val, "max_drawdown_percent", 99.0) <= 15.0
        )
        candidates.append(
            (
                safe and oos_trade_gain >= 10 and val_trade_gain >= 0 and late_share <= STAGE138_SOURCE["validation_late_net_share"],
                safe and oos_trade_gain > 0 and late_share <= STAGE138_SOURCE["validation_late_net_share"] + 0.005,
                safe and late_share < STAGE138_SOURCE["validation_late_net_share"],
                oos_trade_gain,
                val_trade_gain,
                -late_share,
                -as_float(oos, "max_drawdown_percent", 99.0),
                as_float(oos, "profit_factor"),
                as_float(oos, "net_profit"),
                oos,
            )
        )
    return max(candidates, key=lambda item: item[:9])[-1] if candidates else {}


def decide(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]], external: str) -> str:
    if external != "completed":
        return "continue_stage141_runtime_repair_due_to_incomplete_runtime"
    best = best_stage140(summary_rows, segment_rows)
    adapter_id = str(best.get("adapter_id", ""))
    val = split_row(summary_rows, adapter_id, "validation_is")
    late_share = validation_late_share(segment_rows, adapter_id)
    oos_trade_gain = as_float(best, "trade_count") - STAGE138_SOURCE["trade_count"]
    val_trade_gain = as_float(val, "trade_count") - STAGE138_SOURCE["validation_trade_count"]
    safe = (
        as_float(best, "profit_factor") >= LEGACY_34D["profit_factor"]
        and as_float(best, "net_profit") >= LEGACY_34D["net_profit"]
        and as_float(best, "max_drawdown_percent", 99.0) <= 16.5
        and as_float(val, "profit_factor") >= 1.55
        and as_float(val, "net_profit") >= LEGACY_34D["net_profit"]
        and as_float(val, "max_drawdown_percent", 99.0) <= 15.0
    )
    if safe and oos_trade_gain >= 10 and val_trade_gain >= 0 and late_share <= STAGE138_SOURCE["validation_late_net_share"]:
        return "proceed_to_stage141_reverse_supply_followup_review_with_material_gain_candidate_not_final"
    if safe and (oos_trade_gain > 0 or late_share < STAGE138_SOURCE["validation_late_net_share"]):
        return "proceed_to_stage141_reverse_supply_followup_review_with_small_gain_or_concentration_repair_candidate_not_final"
    return "continue_stage141_reverse_supply_repair_after_damage_or_no_gain_candidate_not_final"


def row_table(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | val PF(검증 수익 팩터) | val net(검증 순손익) | val trades(검증 거래 수) | val late share(검증 후반 비중) | OOS PF(미래구간 수익 팩터) | OOS net(미래구간 순손익) | OOS DD%(미래구간 손실률) | OOS trades(미래구간 거래 수) | gain(증가) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for oos in s122.s120.routed_oos(summary_rows):
        adapter_id = str(oos.get("adapter_id", ""))
        val = split_row(summary_rows, adapter_id, "validation_is")
        lines.append(
            "| {adapter} | {val_pf:.6f} | {val_net:.2f} | {val_trades:.0f} | {late:.3f} | {oos_pf:.6f} | {oos_net:.2f} | {dd:.2f} | {trades:.0f} | {gain:.0f} |".format(
                adapter=adapter_id,
                val_pf=as_float(val, "profit_factor"),
                val_net=as_float(val, "net_profit"),
                val_trades=as_float(val, "trade_count"),
                late=validation_late_share(segment_rows, adapter_id),
                oos_pf=as_float(oos, "profit_factor"),
                oos_net=as_float(oos, "net_profit"),
                dd=as_float(oos, "max_drawdown_percent"),
                trades=as_float(oos, "trade_count"),
                gain=as_float(oos, "trade_count") - STAGE138_SOURCE["trade_count"],
            )
        )
    return "\n".join(lines)


def report_markdown(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]], decision: str, external: str) -> str:
    best = best_stage140(summary_rows, segment_rows)
    best_id = str(best.get("adapter_id", ""))
    best_val = split_row(summary_rows, best_id, "validation_is")
    return f"""# Stage140 Reverse Supply Repair Report(140단계 반전 공급 수리 보고서)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage139(원천 139단계): `{SOURCE_STAGE139_ID}`
- source_adapter(원천 어댑터): `{SOURCE_ADAPTER_ID}`
- external_verification_status(외부 검증 상태): `{external}`
- decision(판정): `{decision}`
- boundary(주장 경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Can selective reverse supply(선택적 반전 공급) add more trades than Stage138(138단계) while controlling late concentration(후반 집중)?

Effect(효과): flat exit(평탄 청산)을 제외하고 reverse(반전) 축 안에서만 거래 수와 집중도 균형을 측정한다.

## KPI Table(KPI 핵심 성과 지표 표)

{row_table(summary_rows, segment_rows)}

## Read(판독)

- best_candidate(최선 후보): `{best_id or "none"}`
- oos_trade_gain_vs_stage138_reverse(138단계 반전 대비 미래구간 거래 증가): `{as_float(best, "trade_count") - STAGE138_SOURCE["trade_count"]:.0f}`
- validation_trade_gain_vs_stage138_reverse(138단계 반전 대비 검증 거래 증가): `{as_float(best_val, "trade_count") - STAGE138_SOURCE["validation_trade_count"]:.0f}`
- validation_late_share(검증 후반 비중): `{validation_late_share(segment_rows, best_id):.3f}`
- overall_goal_complete(전체 목표 완료): `false`

Stage140(140단계)는 research/development(연구개발) 측정 단계다. Effect(효과): 결과는 Stage141(141단계) follow-up review(후속 검토)로 넘기며, 최종/운영 주장은 만들지 않는다.
"""


def decision_markdown(decision: str, external: str) -> str:
    return f"""# Stage140 Decision(140단계 판정)

decision(판정): `{decision}`

Stage140(140단계)는 reverse supply(반전 공급)와 late concentration(후반 집중)만 좁게 측정했다. Effect(효과): Stage141(141단계)에서 거래 증가가 충분했는지, 집중도 손상이 있는지 따로 판정한다.

## Evidence(근거)

- report(보고서): `{s138.rel(REPORT_PATH)}`
- summary_csv(요약 CSV): `{s138.rel(SUMMARY_CSV_PATH)}`
- segment_kpi(구간 KPI): `{s138.rel(SEGMENT_KPI_PATH)}`
- risk_atr_telemetry(위험/ATR 원격측정): `{s138.rel(RISK_ATR_TELEMETRY_PATH)}`
- gate_feature_summary(게이트 피처 요약): `{s138.rel(GATE_FEATURE_SUMMARY_PATH)}`
- source_stage139_closeout_commit(원천 139단계 종료 커밋): `{SOURCE_STAGE139_CLOSEOUT_COMMIT}`
- source_stage139_hash_record_commit(원천 139단계 해시 기록 커밋): `{SOURCE_STAGE139_HASH_RECORD_COMMIT}`
- source_stage138_closeout_commit(원천 138단계 종료 커밋): `{SOURCE_STAGE138_CLOSEOUT_COMMIT}`
- external_verification_status(외부 검증 상태): `{external}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

## Next(다음)

next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
"""


def write_stage141_seed() -> None:
    s122.s108.write_md(
        NEXT_STAGE_ROOT / "00_spec/stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage141(141단계)는 Stage140(140단계) reverse supply repair(반전 공급 수리)를 follow-up review(후속 검토)로 판정한다.

## Bounded Question(경계 질문)

Did Stage140(140단계) improve trade count(거래 수), late concentration(후반 집중), and validation/OOS KPI(검증/미래구간 핵심 성과 지표) enough to continue, or should the next bounded stage pivot?

Effect(효과): Stage140(140단계) 안에서 계속 고치지 않고, 다음 수리 축을 하나만 고른다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    s122.s108.write_md(
        NEXT_STAGE_ROOT / "01_inputs/input_refs.md",
        f"""# Stage141 Input References(141단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- stage140_decision(140단계 판정): `{s138.rel(DECISION_PATH)}`
- stage140_report(140단계 보고서): `{s138.rel(REPORT_PATH)}`
- stage140_summary(140단계 요약): `{s138.rel(SUMMARY_CSV_PATH)}`
- stage140_segment_kpi(140단계 구간 KPI): `{s138.rel(SEGMENT_KPI_PATH)}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
""",
    )
    s122.s108.write_md(
        NEXT_STAGE_ROOT / "03_reviews/review_index.md",
        f"""# Stage141 Review Index(141단계 검토 색인)

- status(상태): `open_planned`
- source_stage(원천 단계): `{STAGE_ID}`
- planned_packet(계획 작업 묶음): `{NEXT_PACKET_ID}`
- planned_run(계획 실행): `{NEXT_RUN_ID}`

Effect(효과): Stage141(141단계)는 새 실험이 아니라 Stage140(140단계) 증거 판독으로 시작한다.
""",
    )
    s122.s108.write_md(
        NEXT_STAGE_ROOT / "04_selected/selection_status.md",
        f"""# Stage141 Selection Status(141단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage140`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- selected_research_baseline(선택 연구 기준): `none`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )


def update_current_truth(decision: str, external: str) -> None:
    s122.s108.write_md(
        s138.CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준): `none`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `stage140_reverse_supply_repair_candidate`
- status(상태): `stage140_closed_{decision}_stage141_open_planned`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage140(140단계)는 reverse supply(반전 공급)와 late concentration(후반 집중)만 측정했다. Effect(효과): 결과가 좋아도 final package(최종 패키지)나 operating claim(운영 주장)이 아니라 Stage141(141단계) 검토로 넘긴다.

## Latest Stage140 Evidence(최신 140단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- external_verification_status(외부 검증 상태): `{external}`
- report(보고서): `{s138.rel(REPORT_PATH)}`
- summary(요약): `{s138.rel(SUMMARY_CSV_PATH)}`
- segment_kpi(구간 KPI): `{s138.rel(SEGMENT_KPI_PATH)}`
- risk_atr_telemetry(위험/ATR 원격측정): `{s138.rel(RISK_ATR_TELEMETRY_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
""",
    )
    state = io_path(s138.WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = __import__("re").sub(r"^current_run_id:.*$", f"current_run_id: {NEXT_RUN_ID}", state, count=1, flags=__import__("re").MULTILINE)
    state = __import__("re").sub(r"^active_stage:.*$", f"active_stage: {NEXT_STAGE_ID}", state, count=1, flags=__import__("re").MULTILINE)
    focus = f"""current_focus:
- >-
  Stage140(140단계) closed(종료) as `{decision}` and Stage141(141단계) `{NEXT_STAGE_ID}` is open_planned(열린 계획). Effect(효과): reverse supply(반전 공급) 수리 결과를 보존하고 후속 검토로 넘긴다.
- >-
  Stage140 evidence(140단계 근거)는 `{s138.rel(REPORT_PATH)}`, `{s138.rel(SUMMARY_CSV_PATH)}`, `{s138.rel(SEGMENT_KPI_PATH)}`에 있다. Effect(효과): trade count(거래 수)와 late concentration(후반 집중) 변화를 따로 판정한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)만 계속한다.

"""
    re_mod = __import__("re")
    state = re_mod.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, state, count=1)
    block = f"""
stage140_reverse_supply_late_concentration_repair:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{decision}
  current_run_id: {RUN_ID}
  source_stage139_closeout_commit: {SOURCE_STAGE139_CLOSEOUT_COMMIT}
  source_stage139_hash_record_commit: {SOURCE_STAGE139_HASH_RECORD_COMMIT}
  source_stage138_closeout_commit: {SOURCE_STAGE138_CLOSEOUT_COMMIT}
  source_adapter: {SOURCE_ADAPTER_ID}
  target_surface: {TARGET_SURFACE}
  decision: {decision}
  next_stage_or_branch: {NEXT_STAGE_ID}
  report_path: {s138.rel(REPORT_PATH)}
  decision_path: {s138.rel(DECISION_PATH)}
  packet_summary_path: {s138.rel(PACKET_ROOT / "aggregate_summary.json")}
  external_verification_status: {external}
  pushed_commit_hash: pending_until_push
  boundary: {BOUNDARY}

stage141_stage140_reverse_supply_followup_review:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: open_planned_from_stage140
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_decision: {decision}
  next_action: run141A_stage141_stage140_reverse_supply_followup_review_v1
  boundary: {BOUNDARY}
"""
    state = re_mod.sub(r"(?ms)\nstage140_reverse_supply_late_concentration_repair:.*?(?=\nstage\d+_|$)", "\n", state)
    state = re_mod.sub(r"(?ms)\nstage141_stage140_reverse_supply_followup_review:.*?(?=\nstage\d+_|$)", "\n", state)
    io_path(s138.WORKSPACE_STATE_PATH).write_text(state.rstrip() + "\n" + block, encoding="utf-8-sig")

    s122.s108.write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage140 Selection Status(140단계 선택 상태)

- stage_status(단계 상태): `closed_{decision}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE139_ID}`
- source_adapter(원천 어댑터): `{SOURCE_ADAPTER_ID}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- stage140_decision(140단계 판정): `{decision}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage140(140단계)는 닫고, 전체 목표 완료나 운영 주장은 만들지 않는다.
""",
    )
    s122.s108.write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage140 Review Index(140단계 검토 색인)

- status(상태): `closed_{decision}`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- report(보고서): `{s138.rel(REPORT_PATH)}`
- summary(요약): `{s138.rel(SUMMARY_CSV_PATH)}`
- segment_kpi(구간 KPI): `{s138.rel(SEGMENT_KPI_PATH)}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Effect(효과): Stage140(140단계) 산출물 위치를 한 곳에서 재진입할 수 있게 한다.
""",
    )
    write_stage141_seed()


def append_changelog(decision: str) -> None:
    existing = io_path(s138.CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(s138.CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {utc_now()} Stage140 reverse supply repair closeout(140단계 반전 공급 수리 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{decision}`.\n"
        "- effect(효과): flat exit(평탄 청산)을 제외하고 reverse supply(반전 공급) 축만 측정한 뒤 Stage141(141단계) 검토로 넘겼다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(s138.CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


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
                    "artifact_id": f"{RUN_ID}__{Path(path).name}",
                    "artifact_type": "stage140_reverse_supply_repair_evidence",
                    "path": s138.rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage140 v2-native reverse supply and late concentration repair artifact.",
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
                    "path": s138.rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Actual Stage140 MT5 Strategy Tester HTML report.",
                }
            )
    return rows


def write_ledgers(result: Mapping[str, Any], decision: str, artifacts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    external = str(result.get("external_verification_status") or "blocked")
    status = "completed" if external == "completed" else "blocked"
    run_payload = upsert_csv_rows(
        s138.RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_adapter_stage140_reverse_supply_late_concentration_repair",
                "status": status,
                "judgment": decision,
                "path": s138.rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_stage139_closeout_commit", SOURCE_STAGE139_CLOSEOUT_COMMIT),
                        ("source_stage139_hash_record_commit", SOURCE_STAGE139_HASH_RECORD_COMMIT),
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
    alpha_rows = s100.build_mt5_alpha_ledger_rows(
        run_id=RUN_ID,
        stage_id=STAGE_ID,
        mt5_kpi_records=result.get("mt5_kpi_records", []),
        run_output_root=RUN_ROOT,
        external_verification_status=external,
    )
    alpha_payload = upsert_csv_rows(s138.PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    artifact_payload = upsert_csv_rows(
        s138.ARTIFACT_REGISTRY_PATH,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
        list(artifacts),
        key="artifact_id",
    )
    return {"run_registry": run_payload, "alpha_ledger": alpha_payload, "stage_ledger": stage_payload, "artifact_registry": artifact_payload}


def configure_stage140() -> None:
    for name, value in {
        "STAGE_ID": STAGE_ID,
        "RUN_NUMBER": RUN_NUMBER,
        "RUN_ID": RUN_ID,
        "PACKET_ID": PACKET_ID,
        "PARENT_RUN_ID": PARENT_RUN_ID,
        "SOURCE_STAGE137_ID": SOURCE_STAGE139_ID,
        "SOURCE_STAGE137_CLOSEOUT_COMMIT": SOURCE_STAGE139_CLOSEOUT_COMMIT,
        "SOURCE_STAGE137_LATEST_COMMIT": SOURCE_STAGE139_HASH_RECORD_COMMIT,
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
        "STAGE136_SOURCE": STAGE138_SOURCE,
        "STAGE110_REFERENCE": STAGE110_REFERENCE,
        "LEGACY_34D": LEGACY_34D,
        "VARIANTS": VARIANTS,
        "SOURCE_BASELINE_BY_VARIANT": SOURCE_BASELINE_BY_VARIANT,
        "SOURCE_SPECS_BY_VARIANT": SOURCE_SPECS_BY_VARIANT,
        "CONTEXT_GATE_SPECS": CONTEXT_GATE_SPECS,
    }.items():
        setattr(s138, name, value)
    s138.source_baseline = source_baseline
    s138.best_stage138 = best_stage140
    s138.decide = decide
    s138.row_table = row_table
    s138.report_markdown = report_markdown
    s138.decision_markdown = decision_markdown
    s138.update_current_truth = update_current_truth
    s138.append_changelog = append_changelog
    s138.build_attempts = build_attempts
    s138.artifact_rows = artifact_rows
    s138.write_ledgers = write_ledgers
    s138.configure_stage138()
    s122.s120.build_attempts = build_attempts
    s122.s120.artifact_rows = artifact_rows
    s122.s120.write_ledgers = write_ledgers


def main(argv: Sequence[str] | None = None) -> int:
    configure_stage140()
    code = s122.s120.main(argv)
    write_stage141_seed()
    return code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
