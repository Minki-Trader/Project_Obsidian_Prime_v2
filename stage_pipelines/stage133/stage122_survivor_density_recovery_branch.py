from __future__ import annotations

import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage122 import v41_density_scale_repair_after_dd_guardrail as s122  # noqa: E402


s100 = s122.s100

STAGE_ID = "133_adapter_research__stage122_survivor_density_recovery_branch"
RUN_NUMBER = "run133A"
RUN_ID = "run133A_stage133_stage122_survivor_density_recovery_branch_v1"
PACKET_ID = "stage133_stage122_survivor_density_recovery_branch_v1"
PARENT_RUN_ID = "run132A_stage132_v42_density_repair_followup_v1"
SOURCE_STAGE132_ID = "132_adapter_research__v42_density_repair_followup"
SOURCE_STAGE132_CLOSEOUT_COMMIT = "cd1f54ffadea31d38299946063e74bc3d378fae6"
SOURCE_STAGE132_LATEST_COMMIT = "cd1f54ffadea31d38299946063e74bc3d378fae6"
SOURCE_STAGE122_CLOSEOUT_COMMIT = "d7d1d83862e40bc55f61473209d3a1c38b15d525"
SOURCE_STAGE122_LATEST_COMMIT = "fed35f028fac5621453df67889c4a95cbd8bd77a"
SOURCE_ADAPTER_ID = "s122_v41_h3_cd5_session_margin_risk035_sht54_lng52"
NEXT_STAGE_ID = "134_adapter_research__stage122_survivor_followup_review"
NEXT_RUN_ID = "run134A_stage134_stage122_survivor_followup_review_v1"
NEXT_PACKET_ID = "stage134_stage122_survivor_followup_review_v1"
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
COMMON_ROOT = f"OPV2/s133a/{RUN_NUMBER}"

SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage133_survivor_recovery_summary.json"
SUMMARY_CSV_PATH = REVIEWS_ROOT / "stage133_survivor_recovery_summary.csv"
REPORT_PATH = REVIEWS_ROOT / "stage133_survivor_recovery_report.md"
SEGMENT_KPI_PATH = REVIEWS_ROOT / "stage133_segment_kpi_summary.csv"
RISK_ATR_TELEMETRY_PATH = REVIEWS_ROOT / "stage133_risk_atr_telemetry.csv"
GATE_FEATURE_SUMMARY_PATH = REVIEWS_ROOT / "stage133_gate_feature_summary.csv"
TIER_B_DIAGNOSTIC_PATH = REVIEWS_ROOT / "stage133_tier_b_diagnostic_summary.csv"
DECISION_PATH = REVIEWS_ROOT / "stage133_decision.md"
AUDIT_CSV_PATH = REVIEWS_ROOT / "stage133_trade_audit.csv"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

STAGE122_SURVIVOR = {
    "adapter_id": SOURCE_ADAPTER_ID,
    "profit_factor": 1.75,
    "net_profit": 1102.04,
    "max_drawdown_percent": 14.66,
    "trade_count": 179,
}
LEGACY_34D = {
    "profit_factor": 1.583157,
    "net_profit": 987.60,
    "max_drawdown_percent": 12.909136,
    "trade_count": 404,
}
STAGE110_REFERENCE = {
    "oos_net": 644.76,
    "oos_pf": 1.637076853,
    "oos_dd_pct": 18.69,
    "oos_trade_count": 147,
}


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")

VARIANTS = (
    s100.repair.RepairVariant(
        adapter_id="s133_stage122_control_cd5_h3_risk035",
        label="stage133_stage122_control_cd5_h3_risk035",
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
        notes="Stage133 survivor recovery control: exact Stage122 best shell.",
    ),
    s100.repair.RepairVariant(
        adapter_id="s133_stage122_cd4_h3_risk035",
        label="stage133_stage122_cd4_h3_risk035",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0350,
        same_direction_reentry_cooldown_bars=4,
        short_threshold=0.54,
        long_threshold=0.52,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=True,
        max_hold_bars=3,
        notes="Stage133 survivor recovery: one-bar lower same-direction cooldown to test mild density.",
    ),
    s100.repair.RepairVariant(
        adapter_id="s133_stage122_cd5_h4_risk035",
        label="stage133_stage122_cd5_h4_risk035",
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
        max_hold_bars=4,
        notes="Stage133 survivor recovery: keep entries and allow one extra hold bar.",
    ),
    s100.repair.RepairVariant(
        adapter_id="s133_stage122_cd5_h3_risk030",
        label="stage133_stage122_cd5_h3_risk030",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.075,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.0300,
        same_direction_reentry_cooldown_bars=5,
        short_threshold=0.54,
        long_threshold=0.52,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=True,
        max_hold_bars=3,
        notes="Stage133 survivor recovery: lower risk cap to see if DD improves without losing PF.",
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
        "gate_column": f"stage133_gate_session_margin_{variant.adapter_id}",
        "gate_type": "weak_session_or_et40_mid_margin_block",
        "block_mode": "both",
        "session_min": 165.0,
        "session_max": 275.0,
        "margin_min": 0.04,
        "margin_max": 0.08,
        "description": f"Stage133 survivor recovery: {variant.label}.",
    }
    for variant in VARIANTS
}


def source_baseline(row: Mapping[str, Any]) -> Mapping[str, Any]:
    return STAGE122_SURVIVOR if str(row.get("adapter_id", "")) in SOURCE_BASELINE_BY_VARIANT else {}


def best_stage133(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    candidates = []
    for row in s122.s120.routed_oos(summary_rows):
        early = s122.s120.early_segment(segment_rows, str(row.get("adapter_id", "")))
        pf = s122.as_float(row, "profit_factor")
        net = s122.as_float(row, "net_profit")
        dd = s122.as_float(row, "max_drawdown_percent", 99.0)
        trades = s122.as_float(row, "trade_count")
        source_trades = float(STAGE122_SURVIVOR["trade_count"])
        candidates.append(
            (
                pf >= LEGACY_34D["profit_factor"] and net >= LEGACY_34D["net_profit"] and dd <= STAGE110_REFERENCE["oos_dd_pct"],
                trades - source_trades,
                pf,
                net,
                -dd,
                s122.as_float(early, "profit_factor"),
                row,
            )
        )
    return max(candidates, key=lambda item: item[:6])[-1] if candidates else {}


def decide(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]], external: str) -> str:
    if external != "completed":
        return "continue_stage122_survivor_runtime_repair_in_stage134_due_to_incomplete_runtime"
    best = best_stage133(summary_rows, segment_rows)
    pf_ok = s122.as_float(best, "profit_factor") >= LEGACY_34D["profit_factor"]
    net_ok = s122.as_float(best, "net_profit") >= LEGACY_34D["net_profit"]
    dd_ok = s122.as_float(best, "max_drawdown_percent", 99.0) <= STAGE110_REFERENCE["oos_dd_pct"]
    trade_gain = s122.as_float(best, "trade_count") - float(STAGE122_SURVIVOR["trade_count"])
    if pf_ok and net_ok and dd_ok and trade_gain > 0:
        return "proceed_to_stage134_survivor_confirmation_with_density_gain"
    if pf_ok and net_ok and dd_ok:
        return "proceed_to_stage134_survivor_confirmation_control_survived"
    return "continue_stage122_survivor_repair_in_stage134_due_to_damage"


def row_table(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | OOS PF(미래구간 수익 팩터) | OOS net(미래구간 순손익) | OOS DD%(미래구간 드로다운) | trades(거래 수) | gain(증가) | early PF(초반 수익 팩터) |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in s122.s120.routed_oos(summary_rows):
        adapter_id = str(row.get("adapter_id", ""))
        early = s122.s120.early_segment(segment_rows, adapter_id)
        gain = s122.as_float(row, "trade_count") - float(STAGE122_SURVIVOR["trade_count"])
        lines.append(
            "| {adapter} | {pf:.2f} | {net:.2f} | {dd:.2f} | {trades:.0f} | {gain:.0f} | {early_pf:.2f} |".format(
                adapter=adapter_id,
                pf=s122.as_float(row, "profit_factor"),
                net=s122.as_float(row, "net_profit"),
                dd=s122.as_float(row, "max_drawdown_percent"),
                trades=s122.as_float(row, "trade_count"),
                gain=gain,
                early_pf=s122.as_float(early, "profit_factor"),
            )
        )
    return "\n".join(lines)


def report_markdown(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]], decision: str, external: str) -> str:
    best = best_stage133(summary_rows, segment_rows)
    return f"""# Stage133 Stage122 Survivor Recovery Report(133단계 Stage122 생존 후보 복구 보고서)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_adapter(원천 어댑터): `{SOURCE_ADAPTER_ID}`
- external_verification_status(외부 검증 상태): `{external}`
- decision(판정): `{decision}`
- boundary(주장 경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Can the Stage122 survivor(Stage122 생존 후보)의 strong PF/net(강한 수익 팩터/순손익)을 보존하면서 trade count(거래 수)를 조금 늘리거나 drawdown(드로다운)을 낮출 수 있는가?

## KPI Table(KPI 표)

{row_table(summary_rows, segment_rows)}

## Read(판독)

- best_candidate(최선 후보): `{best.get("adapter_id", "none")}`
- legacy_34d_relation(레거시 34D 관계): lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)
- overall_goal_complete(전체 목표 완료): `false`

Effect(효과): Stage133(133단계)은 약한 v42를 버리고 강한 v2-native survivor(브이투 고유 생존 후보)를 다시 측정한다. 이 결과는 연구개발 근거이며 deployment(배포)나 live readiness(실거래 준비)가 아니다.
"""


def decision_markdown(decision: str, external: str) -> str:
    return f"""# Stage133 Decision(133단계 판정)

decision(판정): `{decision}`

Stage133(133단계)는 Stage122 survivor(Stage122 생존 후보)를 bounded recovery branch(경계 복구 분기)로 다시 측정했다. Effect(효과): 34D KPI(34D 핵심 성과 지표)에 가까운 강한 v2-native 후보가 유지되는지 확인하고 Stage134(134단계) 검토로 넘긴다.

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
    text = f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준): `none`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `stage134_followup_from_stage133_survivor`
- status(상태): `stage133_closed_{decision}_stage134_open_planned`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage133(133단계)는 Stage122 survivor(Stage122 생존 후보)를 bounded recovery branch(경계 복구 분기)로 다시 측정했다. Effect(효과): 강한 v2-native survivor(브이투 고유 생존 후보)가 유지되는지 Stage134(134단계)에서 검토한다.

## Latest Stage133 Evidence(최신 133단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- external_verification_status(외부 검증 상태): `{external}`
- report(보고서): `{s122.rel(REPORT_PATH)}`
- summary(요약): `{s122.rel(SUMMARY_CSV_PATH)}`
- decision_path(판정 경로): `{s122.rel(DECISION_PATH)}`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
"""
    s122.s108.write_md(s122.CURRENT_WORKING_STATE_PATH, text)
    state = s122.io_path(s122.WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = s122.re.sub(r"^current_run_id:.*$", f"current_run_id: {NEXT_RUN_ID}", state, count=1, flags=s122.re.MULTILINE)
    state = s122.re.sub(r"^active_stage:.*$", f"active_stage: {NEXT_STAGE_ID}", state, count=1, flags=s122.re.MULTILINE)
    focus = f"""current_focus:
- >-
  Stage133(133단계) closed(종료) as `{decision}` and Stage134(134단계) `{NEXT_STAGE_ID}` is active_planned(활성 계획). Effect(효과): Stage122 survivor recovery(Stage122 생존 후보 복구) 결과를 검토 단계로 넘긴다.
- >-
  Stage133 evidence(133단계 근거)는 `{s122.rel(REPORT_PATH)}`, `{s122.rel(SUMMARY_CSV_PATH)}`, `{s122.rel(SEGMENT_KPI_PATH)}`에 있다. Effect(효과): KPI(핵심 성과 지표), segment(구간), risk/ATR telemetry(위험/ATR 원격측정)를 함께 추적한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(브이투 고유 연구)만 계속한다.

"""
    state = s122.re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, state, count=1) if s122.re.search(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", state) else state.rstrip() + "\n" + focus
    block = f"""
stage133_stage122_survivor_density_recovery_branch:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_bounded_survivor_recovery
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE132_ID}
  decision: {decision}
  report_path: {s122.rel(REPORT_PATH)}
  decision_path: {s122.rel(DECISION_PATH)}
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}

stage134_stage122_survivor_followup_review:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: active_planned_from_stage133
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_decision: {decision}
  next_action: run_stage134_survivor_followup_review
  boundary: {BOUNDARY}
"""
    state = s122.re.sub(r"(?ms)\nstage133_stage122_survivor_density_recovery_branch:.*?(?=\nstage\d+_|$)", "\n", state)
    state = s122.re.sub(r"(?ms)\nstage134_stage122_survivor_followup_review:.*?(?=\nstage\d+_|$)", "\n", state)
    s122.io_path(s122.WORKSPACE_STATE_PATH).write_text(state.rstrip() + "\n" + block, encoding="utf-8-sig")


def append_changelog(decision: str) -> None:
    existing = s122.io_path(s122.CHANGELOG_PATH).read_text(encoding="utf-8-sig") if s122.path_exists(s122.CHANGELOG_PATH) else ""
    entry = (
        f"\n## {utc_now()} Stage133 survivor recovery closeout(133단계 생존 후보 복구 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{decision}`.\n"
        f"- effect(효과): Stage122 survivor(Stage122 생존 후보)를 다시 측정하고 Stage134(134단계) 검토로 넘겼다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    s122.io_path(s122.CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def write_stage134_seed() -> None:
    s122.s108.write_md(
        NEXT_STAGE_ROOT / "00_spec/stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage134(134단계)는 Stage133(133단계) survivor recovery(생존 후보 복구) 결과를 review-only(검토 전용)로 판정한다.

## Bounded Question(경계 질문)

Stage133(133단계) 결과가 34D KPI(34D 핵심 성과 지표) 접근 후보로 보존할 만큼 강한가, 아니면 다음 bounded repair(경계 수리)가 필요한가?

Effect(효과): Stage133(133단계)에서 바로 전체 목표 완료를 주장하지 않는다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    s122.s108.write_md(
        NEXT_STAGE_ROOT / "01_inputs/input_refs.md",
        f"""# Stage134 Input References(134단계 입력 참조)

- stage133_decision(133단계 판정): `{s122.rel(DECISION_PATH)}`
- stage133_report(133단계 보고서): `{s122.rel(REPORT_PATH)}`
- stage133_summary(133단계 요약): `{s122.rel(SUMMARY_CSV_PATH)}`
- stage133_segment_kpi(133단계 구간 KPI): `{s122.rel(SEGMENT_KPI_PATH)}`
- stage133_risk_atr_telemetry(133단계 위험/ATR 원격측정): `{s122.rel(RISK_ATR_TELEMETRY_PATH)}`
""",
    )
    s122.s108.write_md(
        NEXT_STAGE_ROOT / "03_reviews/review_index.md",
        """# Stage134 Review Index(134단계 검토 색인)

Stage134(134단계)는 planned(계획) 상태다. Effect(효과): Stage133(133단계) 결과를 다음 review-only(검토 전용) 판정으로 연결한다.
""",
    )
    s122.s108.write_md(
        NEXT_STAGE_ROOT / "04_selected/selection_status.md",
        f"""# Stage134 Selection Status(134단계 선택 상태)

- stage_status(단계 상태): `active_planned_from_stage133`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- selected_research_baseline(선택 연구 기준): `none`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )


def configure_stage133() -> None:
    replacements = {
        "STAGE_ID": STAGE_ID,
        "RUN_NUMBER": RUN_NUMBER,
        "RUN_ID": RUN_ID,
        "PACKET_ID": PACKET_ID,
        "PARENT_RUN_ID": PARENT_RUN_ID,
        "SOURCE_STAGE121_ID": SOURCE_STAGE132_ID,
        "SOURCE_STAGE121_CLOSEOUT_COMMIT": SOURCE_STAGE132_CLOSEOUT_COMMIT,
        "SOURCE_STAGE121_LATEST_COMMIT": SOURCE_STAGE132_LATEST_COMMIT,
        "SOURCE_STAGE120_CLOSEOUT_COMMIT": SOURCE_STAGE122_CLOSEOUT_COMMIT,
        "SOURCE_STAGE120_LATEST_COMMIT": SOURCE_STAGE122_LATEST_COMMIT,
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
        "STAGE120_GUARDRAILS": {SOURCE_ADAPTER_ID: STAGE122_SURVIVOR},
        "STAGE110_REFERENCE": STAGE110_REFERENCE,
        "LEGACY_34D": LEGACY_34D,
    }
    for name, value in replacements.items():
        setattr(s122, name, value)
    s122.source_baseline = source_baseline
    s122.best_stage122 = best_stage133
    s122.decide = decide
    s122.row_table = row_table
    s122.report_markdown = report_markdown
    s122.decision_markdown = decision_markdown
    s122.update_current_truth = update_current_truth
    s122.append_changelog = append_changelog
    s122.configure_stage122()


def main(argv: Sequence[str] | None = None) -> int:
    configure_stage133()
    code = s122.s120.main(argv)
    write_stage134_seed()
    return code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
