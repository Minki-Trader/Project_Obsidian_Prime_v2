from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage_frontier_77 import frontier77d_mt5_lifecycle_negative_control_runtime_probe as base


RUN_ID = "frontier77F_mt5_lifecycle_point_unit_repair_probe_v1"
PARENT_RUN_ID = "frontier77E_proxy_runtime_gap_analysis_and_repair_decision_v1"
NEXT_RUN_ID = "frontier77G_post_repair_gap_analysis_or_closeout_decision_v1"
CLAIM_BOUNDARY = (
    "repair_runtime_probe_observation_only_no_completion_no_baseline_"
    "no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve"
)


def configure_base() -> None:
    base.RUN_ID = RUN_ID
    base.PARENT_RUN_ID = PARENT_RUN_ID
    base.NEXT_RUN_ID = NEXT_RUN_ID
    base.COMMON_RUN_ROOT = "Project_Obsidian_Prime_v2/frontier77F_mt5_lifecycle_point_unit_repair_probe"
    base.RUNTIME_CANDIDATE_PREFIX = "f77f_point_unit_repair"
    base.SLTP_POINT_SCALE = 100.0
    base.TRADE_SHAPE_LABEL = "short_only_max_hold_12_fixed_tp1800_sl1200_broker_points"
    base.RUN_SHORT_LABEL = "F77F"
    base.ATTEMPT_PREFIX = "f77f_point_unit_repair"
    base.EXPLORATION_LABEL = "frontier77F_point_unit_repair_runtime_probe"
    base.ATTEMPT_ROLE = "point_unit_repair_runtime_probe"
    base.RECORD_VIEW_PREFIX = "mt5_f77f_point_unit_repair"
    base.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    base.RUN_DIR = base.STAGE_DIR / "02_runs" / RUN_ID
    base.MODEL_DIR = base.RUN_DIR / "models"
    base.FEATURE_DIR = base.RUN_DIR / "features"
    base.VETO_DIR = base.RUN_DIR / "runtime_veto_tapes"
    base.MT5_DIR = base.RUN_DIR / "mt5"
    base.REPORT_PATH = base.REVIEW_DIR / "frontier77F_mt5_lifecycle_point_unit_repair_probe_report.md"
    base.GATE_AUDIT_PATH = base.REVIEW_DIR / "required_gate_coverage_audit_f77f.md"
    base.SUMMARY_PATH = base.REVIEW_DIR / "f77f_mt5_lifecycle_point_unit_repair_probe_summary.json"
    base.RUN_MANIFEST_PATH = base.RUN_DIR / "run_manifest.json"


def report_text(payload: Mapping[str, Any], created_at: str) -> str:
    summary = base.build_summary(payload)
    best = summary["best_runtime"]
    lines = [
        "# Frontier77F MT5 Lifecycle Point-Unit Repair Probe(F77F MT5 생명주기 포인트 단위 수리 탐침)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        f"- status(상태): `{payload.get('status')}`",
        f"- judgment(판정): `{payload.get('judgment')}`",
        "- repair action(수리 행동): TP18/SL12 price units(가격 단위)을 TP1800/SL1200 broker points(브로커 포인트)로 변환했다.",
        f"- attempts/completed(시도/완료): `{summary['attempt_count']}/{summary['completed_attempt_count']}`",
        f"- probability/signal/feature/reproduction parity pass(확률/신호/피처/재현 동등성 통과): `{summary['probability_parity_pass_rows']}/{summary['signal_parity_pass_rows']}/{summary['feature_readiness_pass_rows']}/{summary['source_reproduction_pass_rows']}`",
        f"- best runtime net/PF/DD/tpd(최선 런타임 순수익/수익 팩터/손실폭/일거래): `{best.get('net_profit', '')}/{best.get('profit_factor', '')}/{best.get('max_drawdown_percent', '')}/{best.get('trades_per_day', '')}`",
        f"- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Runtime KPI(런타임 핵심 성과 지표)",
        "",
        "| split(분할) | period(기간) | net(순수익) | gross profit(총이익) | gross loss(총손실) | PF(수익 팩터) | DD%(손실폭) | trades(거래) | trades/day(일거래) | win%(승률) | avg win(평균 이익) | avg loss(평균 손실) | payoff(손익비) | expectancy(기대값) | recovery(회복) | signal diff(신호 차이) | feature diff(피처 차이) | gap cause(간극 원인) |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in payload.get("runtime_receipt", []):
        period = f"{row.get('test_period_start', '')}..{row.get('test_period_end', '')}"
        lines.append(
            "| `{split}` | `{period}` | `{net}` | `{gp}` | `{gl}` | `{pf}` | `{dd}` | `{trades}` | `{tpd}` | `{win}` | `{avgw}` | `{avgl}` | `{payoff}` | `{exp}` | `{rec}` | `{sig}` | `{feat}` | `{gap}` |".format(
                split=row.get("split"),
                period=period,
                net=row.get("net_profit", ""),
                gp=row.get("gross_profit", ""),
                gl=row.get("gross_loss", ""),
                pf=row.get("profit_factor", ""),
                dd=row.get("max_drawdown_percent", ""),
                trades=row.get("trade_count", ""),
                tpd=row.get("trades_per_day", ""),
                win=row.get("win_rate_percent", ""),
                avgw=row.get("average_win", ""),
                avgl=row.get("average_loss", ""),
                payoff=row.get("payoff_ratio", ""),
                exp=row.get("expectancy", ""),
                rec=row.get("recovery_factor", ""),
                sig=row.get("signal_count_diff", ""),
                feat=row.get("feature_ready_diff", ""),
                gap=row.get("gap_cause_summary", ""),
            )
        )
    lines.extend(
        [
            "",
            "## Repair Boundary(수리 경계)",
            "",
            "Action(행동): F77D의 order fill gap(주문 체결 간극)을 수리하기 위해 SL/TP point scale(SL/TP 포인트 배율)만 바꿨다.",
            "",
            "Effect(효과): 결과가 좋아도 completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 만들지 않고, F77G gap analysis(간극 분석)로 보낸다.",
            "",
            "## Next Action(다음 행동)",
            "",
            f"`{NEXT_RUN_ID}`.",
        ]
    )
    return "\n".join(lines)


def gate_audit_text(payload: Mapping[str, Any], created_at: str) -> str:
    summary = base.build_summary(payload)
    return f"""# Required Gate Coverage Audit F77F(F77F 필수 게이트 커버리지 감사)

Updated(갱신): {created_at}

| gate(게이트) | status(상태) | evidence/effect(근거/효과) |
|---|---|---|
| F77E Grok repair review(F77E Grok 수리 검토) | `passed(통과)` | `stages/{base.STAGE_ID}/03_reviews/grok_f77e_gap_analysis_repair_decision_receipt.md` |
| changed variable lock(변경 변수 고정) | `passed(통과)` | only SL/TP point scale 1 -> 100(SL/TP 포인트 배율만 1 -> 100) |
| source reproduction(원천 재현) | `{summary['source_reproduction_pass_rows']}/2` | validation/OOS proxy KPI reproduction(검증/표본외 프록시 KPI 재현) |
| probability parity(확률 동등성) | `{summary['probability_parity_pass_rows']}/3` | ONNX short schema(온엑스 숏 스키마) |
| signal count parity(신호 수 동등성) | `{summary['signal_parity_pass_rows']}/3` | selected-entry veto tape(선택 진입 거부 테이프) |
| feature readiness parity(피처 준비 동등성) | `{summary['feature_readiness_pass_rows']}/1` | 11 feature CSV(11개 피처 CSV) |
| MT5 runtime repair probe(MT5 런타임 수리 탐침) | `{summary['completed_attempt_count']}/{summary['attempt_count']}` | Strategy Tester attempts(전략 테스터 시도) |
| final claim guard(최종 주장 보호) | `passed(통과)` | `{CLAIM_BOUNDARY}` |
"""


def update_ledgers(payload: Mapping[str, Any], created_at: str) -> None:
    summary = base.build_summary(payload)
    best = summary["best_runtime"]
    row_id = f"{RUN_ID}__runtime_repair_probe"
    row = {
        "ledger_row_id": row_id,
        "stage_id": base.STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "runtime_repair_probe(런타임 수리 탐침)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Tier A MT5 Runtime Repair Probe(Tier A MT5 런타임 수리 탐침)",
        "tier_scope": "Tier A separate; Tier B missing_required; combined out_of_scope",
        "kpi_scope": "runtime_repair_probe_kpi(런타임 수리 탐침 KPI)",
        "scoreboard_lane": "runtime_repair_probe(런타임 수리 탐침)",
        "status": payload.get("status"),
        "judgment": payload.get("judgment"),
        "path": base.rel(base.REPORT_PATH),
        "primary_kpi": f"net={best.get('net_profit', '')};pf={best.get('profit_factor', '')};dd={best.get('max_drawdown_percent', '')};tpd={best.get('trades_per_day', '')}",
        "guardrail_kpi": f"signal_diff={best.get('signal_count_diff', '')};feature_diff={best.get('feature_ready_diff', '')};point_scale=100",
        "external_verification_status": "completed(완료)" if summary["completed_attempt_count"] else "blocked_or_materialized_pending(차단 또는 물질화 대기)",
        "notes": f"F77F point-unit repair probe; attempts={summary['attempt_count']};completed={summary['completed_attempt_count']}",
        "lane": "mt5_runtime_repair_probe(MT5 런타임 수리 탐침)",
        "family": "runtime_backtest(런타임 백테스트)",
        "primary_report": base.rel(base.REPORT_PATH),
        "run_number": "frontier77F",
        "date": created_at[:10],
        "decision": payload.get("judgment"),
        "next_run_id": NEXT_RUN_ID,
        "rows": str(summary["attempt_count"]),
        "gate_passes": str(summary["probability_parity_pass_rows"] + summary["signal_parity_pass_rows"] + summary["feature_readiness_pass_rows"] + summary["source_reproduction_pass_rows"] + summary["completed_attempt_count"]),
        "gate_total": "11",
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": base.rel(base.REPORT_PATH),
        "run_date": created_at[:10],
        "primary_artifact": base.rel(base.RUN_MANIFEST_PATH),
        "result_status": payload.get("status"),
        "view": "MT5 Runtime Repair Probe(MT5 런타임 수리 탐침)",
        "tier": "Tier A separate; Tier B missing_required; combined out_of_scope",
        "metric_scope": "runtime_repair_probe_kpi",
        "result_judgment": payload.get("judgment"),
        "final_decision_path": base.rel(base.SELECTED_DIR / "selection_status.md"),
        "gate_audit_path": base.rel(base.GATE_AUDIT_PATH),
        "created_at": created_at,
        "work_family": "runtime_backtest(런타임 백테스트)",
        "row_id": row_id,
        "evidence_boundary": "runtime_repair_probe_observation_no_authority(런타임 수리 탐침 관찰, 권위 없음)",
        "next_action": NEXT_RUN_ID,
        "created_at_utc": created_at,
        "required_gate_audit": base.rel(base.GATE_AUDIT_PATH),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "runtime_backtest",
        "run_type": "mt5_lifecycle_point_unit_repair_probe",
        "input_run_id": PARENT_RUN_ID,
        "output_path": base.rel(base.RUN_MANIFEST_PATH),
        "result_path": base.rel(base.REPORT_PATH),
        "goal_achieve": "not_claimed",
        "net_profit": best.get("net_profit", ""),
        "profit_factor": best.get("profit_factor", ""),
        "drawdown": best.get("max_drawdown_percent", ""),
        "trade_count": best.get("trade_count", ""),
        "trade_density": best.get("trades_per_day", ""),
        "expectancy": best.get("expectancy", ""),
        "recovery_factor": best.get("recovery_factor", ""),
    }
    base.upsert_csv(ROOT / "docs/registers/run_registry.csv", "run_id", row)
    base.upsert_csv(ROOT / "docs/registers/alpha_run_ledger.csv", "ledger_row_id", row)
    base.upsert_csv(base.REVIEW_DIR / "stage_run_ledger.csv", "ledger_row_id", row, source_header=ROOT / "docs/registers/alpha_run_ledger.csv")


def update_state(payload: Mapping[str, Any], created_at: str) -> None:
    summary = base.build_summary(payload)
    best = summary["best_runtime"]
    status = payload.get("status")
    judgment = payload.get("judgment")
    state = f"""current_stage_id: {base.STAGE_ID}
active_stage: {base.STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {status}
current_judgment: {judgment}
next_run_id: {NEXT_RUN_ID}
runtime_probe_status: f77_point_unit_repair_probe_attempted
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
five_stage_retrospective_due_status: not_due_after_f76_closeout_1_of_5
updated_at_utc: '{created_at}'
context_anchor: {base.CONTEXT_ANCHOR_PATH}
notes:
  - "Action(행동): F77F point-unit repair MT5 probe(포인트 단위 수리 MT5 탐침)를 실행/시도했다."
  - "Effect(효과): F77D Invalid stops(잘못된 손절·익절) 간극을 TP1800/SL1200 broker points(브로커 포인트)로 수리했는지 확인했다."
  - "Best runtime(최선 런타임): net/PF/DD/tpd {best.get('net_profit', '')}/{best.get('profit_factor', '')}/{best.get('max_drawdown_percent', '')}/{best.get('trades_per_day', '')}."
  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."
"""
    base.write_text(ROOT / "docs/workspace/workspace_state.yaml", state)
    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{base.STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

## Current Truth(현재 진실)

Action(행동): F77F point-unit repair MT5 probe(포인트 단위 수리 MT5 탐침)를 실행/시도했다.

Effect(효과): F77D의 Invalid stops(잘못된 손절·익절) 문제를 수리한 뒤 runtime economics(런타임 경제성)를 다시 관찰했다.

## Runtime Result(런타임 결과)

- attempts/completed(시도/완료): `{summary['attempt_count']}/{summary['completed_attempt_count']}`
- best runtime net/PF/DD/tpd(최선 런타임 순수익/수익 팩터/손실폭/일거래): `{best.get('net_profit', '')}/{best.get('profit_factor', '')}/{best.get('max_drawdown_percent', '')}/{best.get('trades_per_day', '')}`

## Open Work(열린 작업)

- next run(다음 실행): `{NEXT_RUN_ID}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    base.write_text(ROOT / "docs/context/current_working_state.md", current)
    selection = f"""# F77 Selection Status(F77 선택 상태)

Updated(갱신): {created_at}

Status(상태): `{status}`

Judgment(판정): `{judgment}`

Action(행동): F77F point-unit repair MT5 probe(포인트 단위 수리 MT5 탐침)를 실행/시도했다.

Effect(효과): 다음 실행은 F77G post-repair gap analysis(수리 후 간극 분석) 또는 closeout decision(마감 결정)이다.

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    base.write_text(base.SELECTED_DIR / "selection_status.md", selection)
    marker = "<!-- frontier77F_mt5_lifecycle_point_unit_repair_probe_v1 -->"
    idea_path = ROOT / "docs/registers/idea_registry.md"
    idea_text = base.io_path(idea_path).read_text(encoding="utf-8-sig")
    if marker not in idea_text:
        block = f"""

{marker}
- `{RUN_ID}` executed/attempted(실행/시도) point-unit repair MT5 probe(포인트 단위 수리 MT5 탐침). Best runtime net/PF/DD/tpd(최선 런타임 순수익/수익 팩터/손실폭/일거래): `{best.get('net_profit', '')}/{best.get('profit_factor', '')}/{best.get('max_drawdown_percent', '')}/{best.get('trades_per_day', '')}`. Boundary(경계): no authority(권위 없음). Next(다음): `{NEXT_RUN_ID}`.
"""
        base.write_text(idea_path, idea_text.rstrip() + block)


def report_text(payload: Mapping[str, Any], created_at: str) -> str:
    summary = base.build_summary(payload)
    best = summary["best_runtime"]
    lines = [
        "# Frontier77F MT5 Lifecycle Point-Unit Repair Probe(F77F MT5 생명주기 포인트 단위 수리 탐침)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        f"- status(상태): `{payload.get('status')}`",
        f"- judgment(판정): `{payload.get('judgment')}`",
        "- repair action(수리 행동): TP18/SL12 price units(가격 단위)을 TP1800/SL1200 broker points(브로커 포인트)로 변환했다.",
        f"- attempts/completed(시도/완료): `{summary['attempt_count']}/{summary['completed_attempt_count']}`",
        f"- probability/signal/feature/reproduction parity pass(확률/신호/피처/재현 동등성 통과): `{summary['probability_parity_pass_rows']}/{summary['signal_parity_pass_rows']}/{summary['feature_readiness_pass_rows']}/{summary['source_reproduction_pass_rows']}`",
        f"- best runtime net/PF/DD/tpd(최선 런타임 순수익/수익 팩터/손실폭/일 거래 수): `{best.get('net_profit', '')}/{best.get('profit_factor', '')}/{best.get('max_drawdown_percent', '')}/{best.get('trades_per_day', '')}`",
        f"- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Runtime KPI(런타임 핵심 성과 지표)",
        "",
        "| split(분할) | period(기간) | net(순수익) | gross profit(총이익) | gross loss(총손실) | PF(수익 팩터) | DD%(손실폭) | trades(거래 수) | trades/day(일 거래 수) | win%(승률) | avg win(평균 이익) | avg loss(평균 손실) | payoff(손익비) | expectancy(기대값) | recovery(회복 계수) | signal diff(신호 차이) | feature diff(피처 차이) | gap cause(간극 원인) |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in payload.get("runtime_receipt", []):
        period = f"{row.get('test_period_start', '')}..{row.get('test_period_end', '')}"
        lines.append(
            "| `{split}` | `{period}` | `{net}` | `{gp}` | `{gl}` | `{pf}` | `{dd}` | `{trades}` | `{tpd}` | `{win}` | `{avgw}` | `{avgl}` | `{payoff}` | `{exp}` | `{rec}` | `{sig}` | `{feat}` | `{gap}` |".format(
                split=row.get("split"),
                period=period,
                net=row.get("net_profit", ""),
                gp=row.get("gross_profit", ""),
                gl=row.get("gross_loss", ""),
                pf=row.get("profit_factor", ""),
                dd=row.get("max_drawdown_percent", ""),
                trades=row.get("trade_count", ""),
                tpd=row.get("trades_per_day", ""),
                win=row.get("win_rate_percent", ""),
                avgw=row.get("average_win", ""),
                avgl=row.get("average_loss", ""),
                payoff=row.get("payoff_ratio", ""),
                exp=row.get("expectancy", ""),
                rec=row.get("recovery_factor", ""),
                sig=row.get("signal_count_diff", ""),
                feat=row.get("feature_ready_diff", ""),
                gap=row.get("gap_cause_summary", ""),
            )
        )
    lines.extend(
        [
            "",
            "## Repair Boundary(수리 경계)",
            "",
            "Action(행동): F77D order fill gap(주문 체결 간극)을 수리하기 위해 SL/TP point scale(SL/TP 포인트 배율)만 1에서 100으로 바꿨다.",
            "",
            "Effect(효과): 결과가 좋아도 completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 만들지 않고, F77G gap analysis(간극 분석)로 보낸다.",
            "",
            "## Next Action(다음 행동)",
            "",
            f"`{NEXT_RUN_ID}`.",
        ]
    )
    return "\n".join(lines)


def gate_audit_text(payload: Mapping[str, Any], created_at: str) -> str:
    summary = base.build_summary(payload)
    return f"""# Required Gate Coverage Audit F77F(F77F 필수 게이트 커버리지 감사)

Updated(갱신): {created_at}

| gate(게이트) | status(상태) | evidence/effect(근거/효과) |
|---|---|---|
| F77E Grok repair review(F77E Grok 수리 검토) | `passed(통과)` | `stages/{base.STAGE_ID}/03_reviews/grok_f77e_gap_analysis_repair_decision_receipt.md` |
| changed variable lock(변경 변수 고정) | `passed(통과)` | only SL/TP point scale 1 -> 100(SL/TP 포인트 배율만 1 -> 100) |
| source reproduction(원천 재현) | `{summary['source_reproduction_pass_rows']}/2` | validation/OOS proxy KPI reproduction(검증/표본외 프록시 핵심 성과 지표 재현) |
| probability parity(확률 동등성) | `{summary['probability_parity_pass_rows']}/3` | ONNX short schema(ONNX 숏 스키마) |
| signal count parity(신호 수 동등성) | `{summary['signal_parity_pass_rows']}/3` | selected-entry veto tape(선택 진입 거부 테이프) |
| feature readiness parity(피처 준비 동등성) | `{summary['feature_readiness_pass_rows']}/1` | 11 feature CSV(11개 피처 CSV) |
| MT5 runtime repair probe(MT5 런타임 수리 탐침) | `{summary['completed_attempt_count']}/{summary['attempt_count']}` | Strategy Tester attempts(전략 테스터 시도) |
| final claim guard(최종 주장 보호) | `passed(통과)` | `{CLAIM_BOUNDARY}` |
"""


def update_ledgers(payload: Mapping[str, Any], created_at: str) -> None:
    summary = base.build_summary(payload)
    best = summary["best_runtime"]
    row_id = f"{RUN_ID}__runtime_repair_probe"
    row = {
        "ledger_row_id": row_id,
        "stage_id": base.STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "runtime_repair_probe(런타임 수리 탐침)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Tier A MT5 Runtime Repair Probe(Tier A MT5 런타임 수리 탐침)",
        "tier_scope": "Tier A separate(Tier A 분리); Tier B missing_required(Tier B 필수 누락); combined out_of_scope(합산 범위 밖)",
        "kpi_scope": "runtime_repair_probe_kpi(런타임 수리 탐침 핵심 성과 지표)",
        "scoreboard_lane": "runtime_repair_probe(런타임 수리 탐침)",
        "status": payload.get("status"),
        "judgment": payload.get("judgment"),
        "path": base.rel(base.REPORT_PATH),
        "primary_kpi": f"net={best.get('net_profit', '')};pf={best.get('profit_factor', '')};dd={best.get('max_drawdown_percent', '')};tpd={best.get('trades_per_day', '')}",
        "guardrail_kpi": f"signal_diff={best.get('signal_count_diff', '')};feature_diff={best.get('feature_ready_diff', '')};point_scale=100",
        "external_verification_status": "completed(완료)" if summary["completed_attempt_count"] else "blocked_or_materialized_pending(차단 또는 물질화 대기)",
        "notes": f"F77F point-unit repair probe(포인트 단위 수리 탐침); attempts={summary['attempt_count']};completed={summary['completed_attempt_count']}",
        "lane": "mt5_runtime_repair_probe(MT5 런타임 수리 탐침)",
        "family": "runtime_backtest(런타임 백테스트)",
        "primary_report": base.rel(base.REPORT_PATH),
        "run_number": "frontier77F",
        "date": created_at[:10],
        "decision": payload.get("judgment"),
        "next_run_id": NEXT_RUN_ID,
        "rows": str(summary["attempt_count"]),
        "gate_passes": str(summary["probability_parity_pass_rows"] + summary["signal_parity_pass_rows"] + summary["feature_readiness_pass_rows"] + summary["source_reproduction_pass_rows"] + summary["completed_attempt_count"]),
        "gate_total": "11",
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": base.rel(base.REPORT_PATH),
        "run_date": created_at[:10],
        "primary_artifact": base.rel(base.RUN_MANIFEST_PATH),
        "result_status": payload.get("status"),
        "view": "MT5 Runtime Repair Probe(MT5 런타임 수리 탐침)",
        "tier": "Tier A separate(Tier A 분리); Tier B missing_required(Tier B 필수 누락); combined out_of_scope(합산 범위 밖)",
        "metric_scope": "runtime_repair_probe_kpi",
        "result_judgment": payload.get("judgment"),
        "final_decision_path": base.rel(base.SELECTED_DIR / "selection_status.md"),
        "gate_audit_path": base.rel(base.GATE_AUDIT_PATH),
        "created_at": created_at,
        "work_family": "runtime_backtest(런타임 백테스트)",
        "row_id": row_id,
        "evidence_boundary": "runtime_repair_probe_observation_no_authority(런타임 수리 탐침 관찰, 권위 없음)",
        "next_action": NEXT_RUN_ID,
        "created_at_utc": created_at,
        "required_gate_audit": base.rel(base.GATE_AUDIT_PATH),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "runtime_backtest",
        "run_type": "mt5_lifecycle_point_unit_repair_probe",
        "input_run_id": PARENT_RUN_ID,
        "output_path": base.rel(base.RUN_MANIFEST_PATH),
        "result_path": base.rel(base.REPORT_PATH),
        "goal_achieve": "not_claimed",
        "net_profit": best.get("net_profit", ""),
        "profit_factor": best.get("profit_factor", ""),
        "drawdown": best.get("max_drawdown_percent", ""),
        "trade_count": best.get("trade_count", ""),
        "trade_density": best.get("trades_per_day", ""),
        "expectancy": best.get("expectancy", ""),
        "recovery_factor": best.get("recovery_factor", ""),
    }
    base.upsert_csv(ROOT / "docs/registers/run_registry.csv", "run_id", row)
    base.upsert_csv(ROOT / "docs/registers/alpha_run_ledger.csv", "ledger_row_id", row)
    base.upsert_csv(base.REVIEW_DIR / "stage_run_ledger.csv", "ledger_row_id", row, source_header=ROOT / "docs/registers/alpha_run_ledger.csv")


def update_state(payload: Mapping[str, Any], created_at: str) -> None:
    summary = base.build_summary(payload)
    best = summary["best_runtime"]
    status = payload.get("status")
    judgment = payload.get("judgment")
    state = f"""current_stage_id: {base.STAGE_ID}
active_stage: {base.STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {status}
current_judgment: {judgment}
next_run_id: {NEXT_RUN_ID}
runtime_probe_status: f77_point_unit_repair_probe_attempted
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
five_stage_retrospective_due_status: not_due_after_f76_closeout_1_of_5
updated_at_utc: '{created_at}'
context_anchor: {base.CONTEXT_ANCHOR_PATH}
notes:
  - "Action(행동): F77F point-unit repair MT5 probe(포인트 단위 수리 MT5 탐침)를 실행 또는 시도했다."
  - "Effect(효과): F77D Invalid stops(잘못된 손절·익절) 간극이 TP1800/SL1200 broker points(브로커 포인트)로 수리되는지 확인했다."
  - "Best runtime(최선 런타임): net/PF/DD/tpd {best.get('net_profit', '')}/{best.get('profit_factor', '')}/{best.get('max_drawdown_percent', '')}/{best.get('trades_per_day', '')}."
  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."
"""
    base.write_text(ROOT / "docs/workspace/workspace_state.yaml", state)
    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{base.STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

## Current Truth(현재 진실)

Action(행동): F77F point-unit repair MT5 probe(포인트 단위 수리 MT5 탐침)를 실행 또는 시도했다.

Effect(효과): F77D의 Invalid stops(잘못된 손절·익절) 문제를 수리한 뒤 runtime economics(런타임 경제성)를 다시 관찰했다.

## Runtime Result(런타임 결과)

- attempts/completed(시도/완료): `{summary['attempt_count']}/{summary['completed_attempt_count']}`
- best runtime net/PF/DD/tpd(최선 런타임 순수익/수익 팩터/손실폭/일 거래 수): `{best.get('net_profit', '')}/{best.get('profit_factor', '')}/{best.get('max_drawdown_percent', '')}/{best.get('trades_per_day', '')}`

## Open Work(열린 작업)

- next run(다음 실행): `{NEXT_RUN_ID}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    base.write_text(ROOT / "docs/context/current_working_state.md", current)
    selection = f"""# F77 Selection Status(F77 선택 상태)

Updated(갱신): {created_at}

Status(상태): `{status}`

Judgment(판정): `{judgment}`

Action(행동): F77F point-unit repair MT5 probe(포인트 단위 수리 MT5 탐침)를 실행 또는 시도했다.

Effect(효과): 다음 실행은 F77G post-repair gap analysis(수리 후 간극 분석) 또는 closeout decision(마감 결정)이다.

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    base.write_text(base.SELECTED_DIR / "selection_status.md", selection)
    marker = "<!-- frontier77F_mt5_lifecycle_point_unit_repair_probe_v1 -->"
    idea_path = ROOT / "docs/registers/idea_registry.md"
    idea_text = base.io_path(idea_path).read_text(encoding="utf-8-sig")
    if marker not in idea_text:
        block = f"""

{marker}
- `{RUN_ID}` executed/attempted(실행/시도) point-unit repair MT5 probe(포인트 단위 수리 MT5 탐침). Best runtime net/PF/DD/tpd(최선 런타임 순수익/수익 팩터/손실폭/일 거래 수): `{best.get('net_profit', '')}/{best.get('profit_factor', '')}/{best.get('max_drawdown_percent', '')}/{best.get('trades_per_day', '')}`. Boundary(경계): no authority(권위 없음). Next(다음): `{NEXT_RUN_ID}`.
"""
        base.write_text(idea_path, idea_text.rstrip() + block)


def parse_args() -> argparse.Namespace:
    parser = base.parse_args()
    return parser


def main() -> int:
    configure_base()
    args = parse_args()
    base.ensure_dirs()
    created_at = base.now_utc()
    target = base.target_row()
    context = base.build_context(target)
    artifact, probability, signal, feature_parity = base.materialize(context, Path(args.common_files_root))
    attempts = base.build_attempts(context, artifact) if artifact.get("export_status") == "negative_control_parity_passed" else []
    compile_payload = base.compile_runtime_ea(Path(args.metaeditor_path))
    execution_results: list[dict[str, Any]] = []
    if args.execute and not args.materialize_only and attempts:
        execution_results = base.execute_attempts(args, attempts, compile_payload)
        reports = base.f71d.mt5.collect_mt5_strategy_report_artifacts(
            terminal_data_root=Path(args.terminal_data_root),
            run_output_root=base.RUN_DIR,
            attempts=attempts,
            run_id=RUN_ID,
        )
        base.f71d.mt5.attach_mt5_report_metrics(execution_results, reports)
    base.f71d.RUN_ID = RUN_ID
    base.f71d.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    runtime_receipt = base.f71d.build_runtime_receipt(execution_results, attempts) if execution_results else []
    completed = sum(1 for row in runtime_receipt if row.get("tester_status") == "completed")
    if artifact.get("export_status") != "negative_control_parity_passed":
        status = "repair_materialization_parity_failed_runtime_probe_not_started_no_authority"
        judgment = "repair_materialization_invalid_repair_required_no_authority"
    elif args.execute and completed:
        status = "completed_mt5_lifecycle_point_unit_repair_probe_observation_no_authority"
        judgment = "point_unit_repair_probe_completed_gap_analysis_required_no_authority"
    elif args.execute:
        status = "blocked_mt5_lifecycle_point_unit_repair_probe_attempted_no_authority"
        judgment = "point_unit_repair_probe_blocked_or_missing_output_no_authority"
    else:
        status = "materialized_pending_mt5_point_unit_repair_probe_execution_no_authority"
        judgment = "point_unit_repair_probe_materialized_pending_execution_no_authority"
    payload = {
        "run_id": RUN_ID,
        "stage_id": base.STAGE_ID,
        "status": status,
        "judgment": judgment,
        "created_at_utc": created_at,
        "artifact_rows": [artifact],
        "probability_parity": probability,
        "signal_parity": signal,
        "feature_readiness_parity": feature_parity,
        "source_reproduction": context["reproduction_rows"],
        "attempts": attempts,
        "compile_payload": compile_payload,
        "execution_results": execution_results,
        "runtime_receipt": runtime_receipt,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    base.write_json(base.RUN_MANIFEST_PATH, payload)
    summary = base.build_summary(payload)
    base.write_json(base.SUMMARY_PATH, summary)
    base.write_csv(base.RUN_DIR / "f77f_probability_parity.csv", probability)
    base.write_csv(base.RUN_DIR / "f77f_signal_parity.csv", signal)
    base.write_csv(base.RUN_DIR / "f77f_feature_readiness_parity.csv", feature_parity)
    base.write_csv(base.RUN_DIR / "f77f_source_reproduction.csv", context["reproduction_rows"])
    base.write_csv(base.RUN_DIR / "f77f_runtime_receipt.csv", runtime_receipt, base.f71d.RUNTIME_RECEIPT_COLUMNS)
    base.write_json(base.RUN_DIR / "f77f_execution_results.json", execution_results)
    base.write_text(base.REPORT_PATH, report_text(payload, created_at))
    base.write_text(base.GATE_AUDIT_PATH, gate_audit_text(payload, created_at))
    update_ledgers(payload, created_at)
    update_state(payload, created_at)
    print(
        json.dumps(
            {
                "status": status,
                "judgment": judgment,
                "attempt_count": summary["attempt_count"],
                "completed_attempt_count": summary["completed_attempt_count"],
                "best_runtime": summary["best_runtime"],
                "report": base.rel(base.REPORT_PATH),
                "next_run_id": NEXT_RUN_ID,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
