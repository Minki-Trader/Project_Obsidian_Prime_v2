from __future__ import annotations

import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, path_exists  # noqa: E402
from stage_pipelines.stage122 import v41_density_scale_repair_after_dd_guardrail as s122  # noqa: E402


s100 = s122.s100

STAGE_ID = "136_adapter_research__stage122_survivor_trade_count_concentration_repair"
RUN_NUMBER = "run136A"
RUN_ID = "run136A_stage136_stage122_survivor_trade_count_concentration_repair_v1"
PACKET_ID = "stage136_stage122_survivor_trade_count_concentration_repair_v1"
PARENT_RUN_ID = "run135A_stage135_stage122_survivor_segment_equity_audit_v1"
SOURCE_STAGE135_ID = "135_adapter_research__stage122_survivor_segment_equity_audit"
SOURCE_STAGE135_CLOSEOUT_COMMIT = "9098c8855307eb6516bed1422c3765ec263b61e0"
SOURCE_STAGE135_LATEST_COMMIT = "9098c8855307eb6516bed1422c3765ec263b61e0"
SOURCE_ADAPTER_ID = "s133_stage122_control_cd5_h3_risk035"
NEXT_STAGE_ID = "137_adapter_research__stage136_trade_count_concentration_followup_review"
NEXT_RUN_ID = "run137A_stage137_stage136_trade_count_concentration_followup_review_v1"
NEXT_PACKET_ID = "stage137_stage136_trade_count_concentration_followup_review_v1"
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
COMMON_ROOT = f"OPV2/s136a/{RUN_NUMBER}"

SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage136_trade_count_concentration_repair_summary.json"
SUMMARY_CSV_PATH = REVIEWS_ROOT / "stage136_trade_count_concentration_repair_summary.csv"
REPORT_PATH = REVIEWS_ROOT / "stage136_trade_count_concentration_repair_report.md"
SEGMENT_KPI_PATH = REVIEWS_ROOT / "stage136_segment_kpi_summary.csv"
RISK_ATR_TELEMETRY_PATH = REVIEWS_ROOT / "stage136_risk_atr_telemetry.csv"
GATE_FEATURE_SUMMARY_PATH = REVIEWS_ROOT / "stage136_gate_feature_summary.csv"
TIER_B_DIAGNOSTIC_PATH = REVIEWS_ROOT / "stage136_tier_b_diagnostic_summary.csv"
DECISION_PATH = REVIEWS_ROOT / "stage136_decision.md"
AUDIT_CSV_PATH = REVIEWS_ROOT / "stage136_trade_audit.csv"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

LEGACY_34D = {
    "profit_factor": 1.583157,
    "net_profit": 987.60,
    "max_drawdown_percent": 12.909136,
    "trade_count": 404,
}
STAGE135_SOURCE = {
    "profit_factor": 1.747830217,
    "net_profit": 1102.04,
    "max_drawdown_percent": 14.66,
    "trade_count": 179,
    "validation_profit_factor": 1.58255668,
    "validation_net_profit": 1392.66,
    "validation_trade_count": 263,
    "validation_late_net_share": 897.14 / 1392.66,
}
STAGE110_REFERENCE = {
    "oos_net": 644.76,
    "oos_pf": 1.637076853,
    "oos_dd_pct": 18.69,
    "oos_trade_count": 147,
}

VARIANTS = (
    s100.repair.RepairVariant(
        adapter_id="s136_control_sht54_lng52_cd5_h3_risk035",
        label="stage136_control_sht54_lng52_cd5_h3_risk035",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0350,
        same_direction_reentry_cooldown_bars=5,
        short_threshold=0.54,
        long_threshold=0.52,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=True,
        max_hold_bars=3,
        notes="Stage136 control from Stage135 survivor candidate.",
    ),
    s100.repair.RepairVariant(
        adapter_id="s136_lng51_sht54_cd5_h3_risk035",
        label="stage136_lng51_sht54_cd5_h3_risk035",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0350,
        same_direction_reentry_cooldown_bars=5,
        short_threshold=0.54,
        long_threshold=0.51,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=True,
        max_hold_bars=3,
        notes="Stage136 bounded repair: loosen long threshold by one point.",
    ),
    s100.repair.RepairVariant(
        adapter_id="s136_sht53_lng51_cd5_h3_risk030",
        label="stage136_sht53_lng51_cd5_h3_risk030",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0300,
        same_direction_reentry_cooldown_bars=5,
        short_threshold=0.53,
        long_threshold=0.51,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=True,
        max_hold_bars=3,
        notes="Stage136 bounded repair: loosen both sides and lower risk cap.",
    ),
    s100.repair.RepairVariant(
        adapter_id="s136_sht53_lng51_cd3_h3_risk030",
        label="stage136_sht53_lng51_cd3_h3_risk030",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0300,
        same_direction_reentry_cooldown_bars=3,
        short_threshold=0.53,
        long_threshold=0.51,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=True,
        max_hold_bars=3,
        notes="Stage136 bounded repair: loosen both sides plus shorter same-direction cooldown with lower risk cap.",
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
        "gate_column": f"stage136_gate_session_margin_{variant.adapter_id}",
        "gate_type": "weak_session_or_et40_mid_margin_block",
        "block_mode": "both",
        "session_min": 165.0,
        "session_max": 275.0,
        "margin_min": 0.04,
        "margin_max": 0.08,
        "description": f"Stage136 trade-count/concentration repair: {variant.label}.",
    }
    for variant in VARIANTS
}


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def source_baseline(row: Mapping[str, Any]) -> Mapping[str, Any]:
    return STAGE135_SOURCE if str(row.get("adapter_id", "")) in SOURCE_BASELINE_BY_VARIANT else {}


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


def best_stage136(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    candidates = []
    for oos in s122.s120.routed_oos(summary_rows):
        adapter_id = str(oos.get("adapter_id", ""))
        val = split_row(summary_rows, adapter_id, "validation_is")
        late_share = validation_late_share(segment_rows, adapter_id)
        oos_trade_gain = as_float(oos, "trade_count") - STAGE135_SOURCE["trade_count"]
        val_trade_gain = as_float(val, "trade_count") - STAGE135_SOURCE["validation_trade_count"]
        safe = (
            as_float(oos, "profit_factor") >= LEGACY_34D["profit_factor"]
            and as_float(oos, "net_profit") >= LEGACY_34D["net_profit"]
            and as_float(oos, "max_drawdown_percent", 99.0) <= 16.5
            and as_float(val, "profit_factor") >= 1.55
            and as_float(val, "net_profit") >= LEGACY_34D["net_profit"]
            and as_float(val, "max_drawdown_percent", 99.0) <= 15.0
        )
        material = safe and oos_trade_gain >= 20 and late_share <= 0.60
        small = safe and (oos_trade_gain > 0 or val_trade_gain > 0 or late_share < STAGE135_SOURCE["validation_late_net_share"])
        candidates.append(
            (
                material,
                small,
                oos_trade_gain,
                val_trade_gain,
                -late_share,
                -as_float(oos, "max_drawdown_percent", 99.0),
                as_float(oos, "profit_factor"),
                as_float(oos, "net_profit"),
                oos,
            )
        )
    return max(candidates, key=lambda item: item[:8])[-1] if candidates else {}


def decide(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]], external: str) -> str:
    if external != "completed":
        return "continue_stage136_runtime_repair_due_to_incomplete_runtime"
    best = best_stage136(summary_rows, segment_rows)
    adapter_id = str(best.get("adapter_id", ""))
    val = split_row(summary_rows, adapter_id, "validation_is")
    late_share = validation_late_share(segment_rows, adapter_id)
    oos_trade_gain = as_float(best, "trade_count") - STAGE135_SOURCE["trade_count"]
    val_trade_gain = as_float(val, "trade_count") - STAGE135_SOURCE["validation_trade_count"]
    safe = (
        as_float(best, "profit_factor") >= LEGACY_34D["profit_factor"]
        and as_float(best, "net_profit") >= LEGACY_34D["net_profit"]
        and as_float(best, "max_drawdown_percent", 99.0) <= 16.5
        and as_float(val, "profit_factor") >= 1.55
        and as_float(val, "net_profit") >= LEGACY_34D["net_profit"]
        and as_float(val, "max_drawdown_percent", 99.0) <= 15.0
    )
    if safe and oos_trade_gain >= 20 and late_share <= 0.60:
        return "proceed_to_stage137_followup_review_with_material_repair_candidate_not_final"
    if safe and (oos_trade_gain > 0 or val_trade_gain > 0 or late_share < STAGE135_SOURCE["validation_late_net_share"]):
        return "proceed_to_stage137_followup_review_with_small_repair_candidate_not_final"
    return "continue_trade_count_concentration_repair_in_new_bounded_stage"


def row_table(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | val PF(검증 수익 팩터) | val net(검증 순손익) | val late share(검증 후반 비중) | OOS PF(외부 표본 수익 팩터) | OOS net(외부 표본 순손익) | OOS DD%(외부 표본 손실률) | OOS trades(외부 표본 거래) | gain(증가) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for oos in s122.s120.routed_oos(summary_rows):
        adapter_id = str(oos.get("adapter_id", ""))
        val = split_row(summary_rows, adapter_id, "validation_is")
        gain = as_float(oos, "trade_count") - STAGE135_SOURCE["trade_count"]
        lines.append(
            "| {adapter} | {val_pf:.6f} | {val_net:.2f} | {late:.3f} | {oos_pf:.6f} | {oos_net:.2f} | {dd:.2f} | {trades:.0f} | {gain:.0f} |".format(
                adapter=adapter_id,
                val_pf=as_float(val, "profit_factor"),
                val_net=as_float(val, "net_profit"),
                late=validation_late_share(segment_rows, adapter_id),
                oos_pf=as_float(oos, "profit_factor"),
                oos_net=as_float(oos, "net_profit"),
                dd=as_float(oos, "max_drawdown_percent"),
                trades=as_float(oos, "trade_count"),
                gain=gain,
            )
        )
    return "\n".join(lines)


def report_markdown(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]], decision: str, external: str) -> str:
    best = best_stage136(summary_rows, segment_rows)
    return f"""# Stage136 Trade Count/Concentration Repair Report(136단계 거래 수/집중 수리 보고서)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_adapter(원천 어댑터): `{SOURCE_ADAPTER_ID}`
- external_verification_status(외부 검증 상태): `{external}`
- decision(판정): `{decision}`
- boundary(주장 경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Stage135(135단계) survivor candidate(생존 후보)의 trade count(거래 수)를 늘리거나 validation concentration(검증 집중)을 낮추면서 PF/net(수익 팩터/순손익), drawdown(손실폭), risk/ATR(위험/ATR)을 보존할 수 있는가?

Effect(효과): final net(최종 순손익)만 더 키우는 것이 아니라, 34D(레거시 기준)와의 거래 수/곡선 품질 격차를 줄이는지 본다.

## Result Table(결과 표)

{row_table(summary_rows, segment_rows)}

## Read(판독)

- best_candidate(최선 후보): `{best.get("adapter_id", "none")}`
- overall_goal_complete(전체 목표 완료): `false`
- legacy_relation(레거시 관계): `lesson_only_target_surface_no_code_copy`

Stage136(136단계)는 repair(수리) 단계이지 final package(최종 패키지) 단계가 아니다. Effect(효과): 좋은 후보를 보존하되, 약점이 남으면 Stage137(137단계) 검토나 새 bounded stage(경계 단계)로 넘긴다.
"""


def decision_markdown(decision: str, external: str) -> str:
    return f"""# Stage136 Decision(136단계 판정)

decision(판정): `{decision}`

Stage136(136단계)는 trade count/concentration(거래 수/집중)만 좁게 수리했다. Effect(효과): Stage135(135단계)의 강한 PF/net(수익 팩터/순손익)을 보호하면서 거래 수와 집중 약점을 따로 검토한다.

## Evidence(근거)

- report(보고서): `{s122.rel(REPORT_PATH)}`
- summary_csv(요약 CSV): `{s122.rel(SUMMARY_CSV_PATH)}`
- segment_kpi(구간 KPI): `{s122.rel(SEGMENT_KPI_PATH)}`
- risk_atr_telemetry(위험/ATR 원격측정): `{s122.rel(RISK_ATR_TELEMETRY_PATH)}`
- external_verification_status(외부 검증 상태): `{external}`

## Next(다음)

next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
"""


def update_current_truth(decision: str, external: str) -> None:
    s122.s108.write_md(
        s122.CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준): `none`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `stage136_trade_count_concentration_repair_candidate`
- status(상태): `stage136_closed_{decision}_stage137_open_planned`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage136(136단계)는 Stage135(135단계)의 trade count/concentration(거래 수/집중) 약점을 좁게 수리했다. Effect(효과): 결과가 좋든 나쁘든 다음 Stage137(137단계) 검토로 분리해 과대 수리를 막는다.

## Latest Stage136 Evidence(최신 136단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- external_verification_status(외부 검증 상태): `{external}`
- report(보고서): `{s122.rel(REPORT_PATH)}`
- summary(요약): `{s122.rel(SUMMARY_CSV_PATH)}`
- segment_kpi(구간 KPI): `{s122.rel(SEGMENT_KPI_PATH)}`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
""",
    )
    state = io_path(s122.WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = re.sub(r"^current_run_id:.*$", f"current_run_id: {NEXT_RUN_ID}", state, count=1, flags=re.MULTILINE)
    state = re.sub(r"^active_stage:.*$", f"active_stage: {NEXT_STAGE_ID}", state, count=1, flags=re.MULTILINE)
    focus = f"""current_focus:
- >-
  Stage136(136단계) closed(종료) as `{decision}` and Stage137(137단계) `{NEXT_STAGE_ID}` is active_planned(활성 계획). Effect(효과): trade count/concentration(거래 수/집중) 수리 결과를 후속 검토로 넘긴다.
- >-
  Stage136 evidence(136단계 근거)는 `{s122.rel(REPORT_PATH)}`, `{s122.rel(SUMMARY_CSV_PATH)}`, `{s122.rel(SEGMENT_KPI_PATH)}`에 있다. Effect(효과): repair(수리)가 KPI(핵심 성과 지표)를 살렸는지 분리해서 본다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(브이투 고유 연구)만 계속한다.

"""
    state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, state, count=1) if re.search(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", state) else state.rstrip() + "\n" + focus
    block = f"""
stage136_stage122_survivor_trade_count_concentration_repair:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_bounded_repair
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE135_ID}
  decision: {decision}
  report_path: {s122.rel(REPORT_PATH)}
  decision_path: {s122.rel(DECISION_PATH)}
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}

stage137_stage136_trade_count_concentration_followup_review:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: active_planned_from_stage136
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_decision: {decision}
  next_action: run_stage137_followup_review
  boundary: {BOUNDARY}
"""
    state = re.sub(r"(?ms)\nstage136_stage122_survivor_trade_count_concentration_repair:.*?(?=\nstage\d+_|$)", "\n", state)
    state = re.sub(r"(?ms)\nstage137_stage136_trade_count_concentration_followup_review:.*?(?=\nstage\d+_|$)", "\n", state)
    io_path(s122.WORKSPACE_STATE_PATH).write_text(state.rstrip() + "\n" + block, encoding="utf-8-sig")


def append_changelog(decision: str) -> None:
    existing = io_path(s122.CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(s122.CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {utc_now()} Stage136 trade count/concentration repair closeout(136단계 거래 수/집중 수리 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{decision}`.\n"
        "- effect(효과): Stage135 survivor candidate(135단계 생존 후보)의 거래 수/집중 수리 결과를 Stage137(137단계) 검토로 넘겼다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(s122.CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def write_stage137_seed() -> None:
    s122.s108.write_md(
        NEXT_STAGE_ROOT / "00_spec/stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage137(137단계)는 Stage136(136단계) trade count/concentration repair(거래 수/집중 수리)를 review-only(검토 전용)로 판정한다.

## Bounded Question(경계 질문)

Did Stage136(136단계) create a safer candidate, or should the repair continue in a new bounded stage(경계 단계)?

Effect(효과): Stage136(136단계) 안에서 끝없이 고치지 않고, 결과를 따로 판정한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    s122.s108.write_md(
        NEXT_STAGE_ROOT / "01_inputs/input_refs.md",
        f"""# Stage137 Input References(137단계 입력 참조)

- stage136_decision(136단계 판정): `{s122.rel(DECISION_PATH)}`
- stage136_report(136단계 보고서): `{s122.rel(REPORT_PATH)}`
- stage136_summary(136단계 요약): `{s122.rel(SUMMARY_CSV_PATH)}`
- stage136_segment_kpi(136단계 구간 KPI): `{s122.rel(SEGMENT_KPI_PATH)}`
- stage136_risk_atr_telemetry(136단계 위험/ATR 원격측정): `{s122.rel(RISK_ATR_TELEMETRY_PATH)}`
""",
    )
    s122.s108.write_md(
        NEXT_STAGE_ROOT / "03_reviews/review_index.md",
        """# Stage137 Review Index(137단계 검토 색인)

Stage137(137단계)는 planned(계획) 상태다. Effect(효과): Stage136(136단계) 수리 결과를 따로 판정한다.
""",
    )
    s122.s108.write_md(
        NEXT_STAGE_ROOT / "04_selected/selection_status.md",
        f"""# Stage137 Selection Status(137단계 선택 상태)

- stage_status(단계 상태): `active_planned_from_stage136`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `continue_trade_count_concentration_repair_in_new_bounded_stage`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- selected_research_baseline(선택 연구 기준): `none`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )


def configure_stage136() -> None:
    replacements = {
        "STAGE_ID": STAGE_ID,
        "RUN_NUMBER": RUN_NUMBER,
        "RUN_ID": RUN_ID,
        "PACKET_ID": PACKET_ID,
        "PARENT_RUN_ID": PARENT_RUN_ID,
        "SOURCE_STAGE121_ID": SOURCE_STAGE135_ID,
        "SOURCE_STAGE121_CLOSEOUT_COMMIT": SOURCE_STAGE135_CLOSEOUT_COMMIT,
        "SOURCE_STAGE121_LATEST_COMMIT": SOURCE_STAGE135_LATEST_COMMIT,
        "SOURCE_STAGE120_CLOSEOUT_COMMIT": SOURCE_STAGE135_CLOSEOUT_COMMIT,
        "SOURCE_STAGE120_LATEST_COMMIT": SOURCE_STAGE135_LATEST_COMMIT,
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
        "SOURCE_BASELINE_BY_VARIANT": SOURCE_BASELINE_BY_VARIANT,
        "STAGE120_GUARDRAILS": {SOURCE_ADAPTER_ID: STAGE135_SOURCE},
        "STAGE110_REFERENCE": STAGE110_REFERENCE,
        "LEGACY_34D": LEGACY_34D,
    }
    for name, value in replacements.items():
        setattr(s122, name, value)
    s122.source_baseline = source_baseline
    s122.best_stage122 = best_stage136
    s122.decide = decide
    s122.row_table = row_table
    s122.report_markdown = report_markdown
    s122.decision_markdown = decision_markdown
    s122.update_current_truth = update_current_truth
    s122.append_changelog = append_changelog
    s122.configure_stage122()


def main(argv: Sequence[str] | None = None) -> int:
    configure_stage136()
    code = s122.s120.main(argv)
    write_stage137_seed()
    return code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
