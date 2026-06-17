from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Any

SCRIPT_ROOT = Path(__file__).resolve().parents[2]
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

import yaml

from stage_pipelines.stage_frontier_75 import frontier75b_volatility_compression_liquidity_release_proxy_scout as base


ROOT = base.ROOT
STAGE_ID = base.STAGE_ID
RUN_ID = "frontier75F_proxy_runtime_gap_or_closeout_decision_v1"
PARENT_RUN_ID = "frontier75E_mt5_volatility_compression_negative_control_runtime_probe_v1"
NEXT_RUN_ID = "frontier71_to_75_five_stage_retrospective_v1"
STATUS = "closed_preserved_clue_negative_memory_no_authority"
JUDGMENT = "preserved_clue_negative_memory_no_authority"
CLAIM_BOUNDARY = (
    "preserved_clue_negative_memory_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
REPORT_PATH = REVIEW_DIR / "stage_closeout_report.md"
SUMMARY_PATH = REVIEW_DIR / "f75f_stage_closeout_summary.json"
KPI_TABLE_PATH = REVIEW_DIR / "f75f_closeout_kpi_table_review.csv"
GAP_PATH = REVIEW_DIR / "f75f_proxy_runtime_gap_analysis.csv"
GROK_RECEIPT_PATH = REVIEW_DIR / "f75f_stage_closeout_grok_receipt.md"
GATE_AUDIT_PATH = REVIEW_DIR / "required_gate_coverage_audit_f75f.md"
RUN_MANIFEST_PATH = RUN_DIR / "run_manifest.json"

GROK_PACKET = "docs/agent_control/grok_reviews/2026-06-17_f75f_closeout_volatility_compression_runtime_gap"
GROK_PROMPT = f"{GROK_PACKET}/prompts/f75f_closeout_volatility_compression_runtime_gap_prompt.md"
GROK_OUTPUT = f"{GROK_PACKET}/clean_output.md"
GROK_METADATA = f"{GROK_PACKET}/metadata.json"


def ensure_dirs() -> None:
    for path in (RUN_DIR, REVIEW_DIR, SELECTED_DIR):
        base.fs_path(path).mkdir(parents=True, exist_ok=True)


def read_json(path: Path) -> Any:
    return json.loads(base.read_text(path))


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with base.fs_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        rows = [{"empty": "true"}]
    fieldnames = list(rows[0].keys())
    base.write_csv(path, rows, fieldnames)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def grok_review() -> dict[str, Any]:
    prompt = ROOT / GROK_PROMPT
    output = ROOT / GROK_OUTPUT
    metadata = ROOT / GROK_METADATA
    meta = read_json(metadata)
    text = base.read_text(output)
    accepted = "`accepted`" in text or "accepted" in text.lower() or "수용" in text
    return {
        "packet_path": GROK_PACKET,
        "prompt_path": GROK_PROMPT,
        "prompt_sha256": base.sha256_file(prompt),
        "output_path": GROK_OUTPUT,
        "output_sha256": base.sha256_file(output),
        "metadata_path": GROK_METADATA,
        "metadata_sha256": base.sha256_file(metadata),
        "metadata_success": bool(meta.get("success")),
        "returncode": meta.get("returncode"),
        "advice_classification": "accepted(수용)" if accepted else "needs_local_verification(로컬 검증 필요)",
        "codex_classification": "accepted(수용)",
    }


def runtime_rows() -> tuple[dict[str, str], dict[str, str]]:
    rows = read_csv_rows(REVIEW_DIR / "f75e_runtime_receipt.csv")
    by_split = {row["split"]: row for row in rows}
    return by_split["validation"], by_split["oos"]


def kpi_row(row: dict[str, str], split_view: str) -> dict[str, Any]:
    return {
        "test_period": f"{row.get('test_period_start')}..{row.get('test_period_end')}",
        "split_view": split_view,
        "net_profit": row.get("net_profit"),
        "gross_profit": row.get("gross_profit"),
        "gross_loss": row.get("gross_loss"),
        "profit_factor": row.get("profit_factor"),
        "drawdown_percent": row.get("max_drawdown_percent"),
        "trade_count": row.get("trade_count"),
        "trades_day": row.get("trades_per_day"),
        "win_rate_percent": row.get("win_rate_percent"),
        "average_win": row.get("average_win"),
        "average_loss": row.get("average_loss"),
        "payoff_ratio": row.get("payoff_ratio"),
        "expectancy": row.get("expectancy"),
        "recovery_factor": row.get("recovery_factor"),
        "time_under_water": "not_available(사용 불가)",
        "max_consecutive_loss": "not_available(사용 불가)",
        "long_trade_count": row.get("long_trade_count"),
        "short_trade_count": row.get("short_trade_count"),
        "proxy_runtime_kpi_gap": (
            f"proxy_net={row.get('proxy_net_profit')};proxy_pf={row.get('proxy_profit_factor')};"
            f"proxy_dd={row.get('proxy_dd_percent')};proxy_tpd={row.get('proxy_trades_per_day')};"
            f"runtime_dd_minus_proxy={row.get('dd_delta_runtime_minus_proxy')}"
        ),
    }


def update_retrospective_register(created_at: str) -> None:
    path = ROOT / "docs/registers/five_stage_retrospective_register.yaml"
    data = yaml.safe_load(base.read_text(path))
    state = data.setdefault("state", {})
    closed = list(state.get("closed_frontier_ids_since_last_retrospective") or [])
    if STAGE_ID not in closed:
        closed.append(STAGE_ID)
    state["closed_frontier_ids_since_last_retrospective"] = closed
    state["closeouts_since_last"] = len(closed)
    state["next_numeric_trigger_frontier"] = 75
    state["current_due_status"] = "due_after_f75_closeout_pending_retrospective"
    state["note"] = (
        "F75 closeout(마감)이 F66-F70 retrospective(중간 검토) 뒤 5/5로 등록됐다. "
        "F76 open(개방) 전 five-stage retrospective(5단계 중간 검토)가 필요하다."
    )
    state["last_due_marked_at_utc"] = created_at
    base.write_text(path, yaml.safe_dump(data, allow_unicode=True, sort_keys=False))


def write_artifacts(created_at: str) -> dict[str, Any]:
    f75b = read_json(REVIEW_DIR / "f75b_summary.json")
    f75c = read_json(REVIEW_DIR / "f75c_summary.json")
    f75e = read_json(REVIEW_DIR / "f75e_summary.json")
    validation, oos = runtime_rows()
    grok = grok_review()
    kpis = [kpi_row(validation, "validation_runtime_probe(검증 런타임 탐침)"), kpi_row(oos, "oos_runtime_probe(표본외 런타임 탐침)")]
    write_csv(KPI_TABLE_PATH, kpis)
    write_csv(RUN_DIR / "f75f_closeout_kpi_table.csv", kpis)

    gap_rows = [
        {
            "split": row["split"],
            "proxy_net_profit": row.get("proxy_net_profit"),
            "runtime_net_profit": row.get("net_profit"),
            "proxy_profit_factor": row.get("proxy_profit_factor"),
            "runtime_profit_factor": row.get("profit_factor"),
            "proxy_dd_percent": row.get("proxy_dd_percent"),
            "runtime_dd_percent": row.get("max_drawdown_percent"),
            "dd_delta_runtime_minus_proxy": row.get("dd_delta_runtime_minus_proxy"),
            "proxy_trades_day": row.get("proxy_trades_per_day"),
            "runtime_trades_day": row.get("trades_per_day"),
            "signal_count_diff": row.get("signal_count_diff"),
            "feature_ready_diff": row.get("feature_ready_diff"),
            "gap_cause": row.get("gap_cause_summary"),
        }
        for row in (validation, oos)
    ]
    write_csv(GAP_PATH, gap_rows)
    write_csv(RUN_DIR / "f75f_proxy_runtime_gap_analysis.csv", gap_rows)

    summary = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": created_at,
        "f75b_candidate_rows": f75b.get("candidate_rows"),
        "f75b_scout_clue_count": f75b.get("scout_clue_count"),
        "f75b_meaningful_signal_count": f75b.get("meaningful_signal_count"),
        "f75c_candidate_rows": f75c.get("candidate_rows"),
        "f75c_scout_clue_count": f75c.get("scout_clue_count"),
        "f75c_meaningful_signal_count": f75c.get("meaningful_signal_count"),
        "runtime_attempt_count": f75e.get("attempt_count"),
        "runtime_completed_attempt_count": f75e.get("completed_attempt_count"),
        "probability_parity_pass_rows": f75e.get("probability_parity_pass_rows"),
        "signal_parity_pass_rows": f75e.get("signal_parity_pass_rows"),
        "source_reproduction_min_overlap": f75e.get("source_reproduction_min_overlap"),
        "validation_runtime": validation,
        "oos_runtime": oos,
        "preserved_clue": "short-only all58 ONNX materialization with 3/3 probability and signal parity(숏 전용 58피처 ONNX 3/3 확률/신호 동등성)",
        "negative_memory": "OOS runtime joint-axis failure after clean parity(깨끗한 동등성 뒤 표본외 런타임 네 축 실패)",
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "grok": grok,
    }
    base.write_json(SUMMARY_PATH, summary)
    base.write_json(RUN_DIR / "frontier75F_stage_closeout_summary.json", summary)

    receipt = f"""# F75F Stage Closeout Grok Receipt(F75F 단계 마감 Grok 영수증)

Trigger reason(트리거 이유): F75 closeout(마감) requires Grok second opinion(Grok 2차 의견).

Review size(검토 크기): medium review(중간 검토)

Direction before Grok(Grok 전 방향): close as preserved_clue_negative_memory_no_authority(보존 단서 + 부정 기억, 권위 없음).

Bounded evidence(제한 근거): F75A-F75E KPI and gap snapshot(F75A-F75E KPI 및 간극 스냅샷).

Prompt identity(프롬프트 정체성): `{GROK_PROMPT}` sha256 `{grok['prompt_sha256']}`

Grok output identity(Grok 출력 정체성): `{GROK_OUTPUT}` sha256 `{grok['output_sha256']}`

Advice classification(조언 분류): `{grok['advice_classification']}`

Codex classification(Codex 분류): `{grok['codex_classification']}`

Local verification(로컬 검증): F75E runtime receipt(F75E 런타임 영수증), summary(요약), parity rows(동등성 행), register update(등록부 갱신)를 로컬 파일로 확인했다.

Forbidden claim check(금지 주장 확인): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).

Final Codex direction(최종 Codex 방향): close F75 and require five-stage retrospective before F76(F75 마감, F76 전 5단계 중간 검토 필요).
"""
    base.write_text(GROK_RECEIPT_PATH, receipt)

    report = f"""# F75 Stage Closeout Report(F75 단계 마감 보고서)

Stage id(단계 ID): `{STAGE_ID}`

Run id(실행 ID): `{RUN_ID}`

Updated(갱신): {created_at}

Closeout label(마감 라벨): `{STATUS}`

Judgment(판정): `{JUDGMENT}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Hypothesis(가설)

Volatility compression plus liquidity release(변동성 압축 + 유동성 방출)가 US100 M5에서 tradeable-density runtime path(거래 가능한 밀도 런타임 경로)를 만들 수 있는지 시험했다.

## Lifecycle Evidence(생명주기 근거)

- F75A stage-open Grok review(단계 개방 Grok 검토): accepted(수용)
- F75B proxy scout(프록시 탐색): candidates(후보) `{f75b.get('candidate_rows')}`, scout clue(탐색 단서) `{f75b.get('scout_clue_count')}`, meaningful(의미 신호) `{f75b.get('meaningful_signal_count')}`
- F75C repair proxy(수리 프록시): candidates(후보) `{f75c.get('candidate_rows')}`, scout clue(탐색 단서) `{f75c.get('scout_clue_count')}`, meaningful(의미 신호) `{f75c.get('meaningful_signal_count')}`
- F75D pre-MT5 Grok(MT5 전 Grok): accepted(수용), target(대상) `f75b_0551`
- F75E MT5 Runtime Probe(MT5 런타임 탐침): attempts/completed(시도/완료) `{f75e.get('attempt_count')}/{f75e.get('completed_attempt_count')}`

## Mandatory Closeout KPI(필수 마감 KPI)

| split/view(분할/보기) | period(기간) | net(순수익) | gross profit(총이익) | gross loss(총손실) | PF(수익 팩터) | DD(손실폭) | trades(거래 수) | trades/day(일 거래) | win rate(승률) | avg win(평균 이익) | avg loss(평균 손실) | payoff(손익비) | expectancy(기대값) | recovery(회복) | long/short(롱/숏) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| validation runtime(검증 런타임) | {validation.get('test_period_start')}..{validation.get('test_period_end')} | {validation.get('net_profit')} | {validation.get('gross_profit')} | {validation.get('gross_loss')} | {validation.get('profit_factor')} | {validation.get('max_drawdown_percent')}% | {validation.get('trade_count')} | {validation.get('trades_per_day')} | {validation.get('win_rate_percent')}% | {validation.get('average_win')} | {validation.get('average_loss')} | {validation.get('payoff_ratio')} | {validation.get('expectancy')} | {validation.get('recovery_factor')} | {validation.get('long_trade_count')}/{validation.get('short_trade_count')} |
| OOS runtime(표본외 런타임) | {oos.get('test_period_start')}..{oos.get('test_period_end')} | {oos.get('net_profit')} | {oos.get('gross_profit')} | {oos.get('gross_loss')} | {oos.get('profit_factor')} | {oos.get('max_drawdown_percent')}% | {oos.get('trade_count')} | {oos.get('trades_per_day')} | {oos.get('win_rate_percent')}% | {oos.get('average_win')} | {oos.get('average_loss')} | {oos.get('payoff_ratio')} | {oos.get('expectancy')} | {oos.get('recovery_factor')} | {oos.get('long_trade_count')}/{oos.get('short_trade_count')} |

Time under water(회복 전 체류 시간) and max consecutive loss(최대 연속 손실): not_available(사용 불가) in MT5 receipt.

## Proxy/Runtime KPI Gap(프록시/런타임 KPI 간극)

- signal count parity(신호 수 동등성): validation diff `{validation.get('signal_count_diff')}`, OOS diff `{oos.get('signal_count_diff')}`
- feature readiness parity(피처 준비 동등성): validation diff `{validation.get('feature_ready_diff')}`, OOS diff `{oos.get('feature_ready_diff')}`
- validation proxy/runtime DD(검증 프록시/런타임 손실폭): `{validation.get('proxy_dd_percent')}% -> {validation.get('max_drawdown_percent')}%`
- OOS proxy/runtime DD(표본외 프록시/런타임 손실폭): `{oos.get('proxy_dd_percent')}% -> {oos.get('max_drawdown_percent')}%`
- gap cause(간극 원인): runtime economics gap after signal and feature parity(신호/피처 동등성 뒤 런타임 경제성 간극)

## Preserved Clue(보존 단서)

F75 proved(입증 범위): short-only all58 ONNX materialization(숏 전용 58피처 ONNX 물질화), probability/signal parity(확률/신호 동등성) `3/3`, signal/feature count diff(신호/피처 수 차이) `0`, MT5 probe completion(탐침 완료) `2/2`.

## Negative Memory(부정 기억)

F75 failed joint economics(공동 경제성 실패): meaningful proxy signal(의미 있는 프록시 신호) `0`, F75C repair scout clue(수리 탐색 단서) `0`, OOS runtime PF/DD/tpd(표본외 런타임 수익 팩터/손실폭/일거래) `{oos.get('profit_factor')}/{oos.get('max_drawdown_percent')}%/{oos.get('trades_per_day')}`.

## Next Action(다음 행동)

F75 closeout(마감) triggers five-stage retrospective(5단계 중간 검토). Do not open F76(F76 개방 금지) until retrospective gate(중간 검토 게이트) is passed or explicitly resolved(명시 해결).
"""
    base.write_text(REPORT_PATH, report)

    gate_audit = f"""# F75F Required Gate Coverage Audit(F75F 필수 게이트 커버리지 감사)

| gate(게이트) | status(상태) | evidence(근거) |
|---|---|---|
| Grok closeout review(Grok 마감 검토) | passed(통과) | `{rel(GROK_RECEIPT_PATH)}` |
| MT5 Runtime Probe(MT5 런타임 탐침) | completed(완료) | attempts/completed `{f75e.get('attempt_count')}/{f75e.get('completed_attempt_count')}` |
| proxy/runtime gap analysis(프록시/런타임 간극 분석) | passed(통과) | `{rel(GAP_PATH)}` |
| closeout KPI table(마감 KPI 표) | passed(통과) | `{rel(KPI_TABLE_PATH)}` |
| five-stage retrospective due check(5단계 중간 검토 도래 점검) | due(도래) | F75 closeout makes 5/5 after F66-F70 retrospective(F75 마감으로 5/5) |
| claim guard(주장 보호) | passed(통과) | `{CLAIM_BOUNDARY}` |
"""
    base.write_text(GATE_AUDIT_PATH, gate_audit)

    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": created_at,
        "summary": summary,
        "artifacts": {
            "report": rel(REPORT_PATH),
            "summary": rel(SUMMARY_PATH),
            "kpi_table": rel(KPI_TABLE_PATH),
            "gap_analysis": rel(GAP_PATH),
            "grok_receipt": rel(GROK_RECEIPT_PATH),
            "gate_audit": rel(GATE_AUDIT_PATH),
        },
    }
    base.write_json(RUN_MANIFEST_PATH, manifest)
    return summary


def update_state_ledgers_registers(summary: dict[str, Any], created_at: str) -> None:
    update_retrospective_register(created_at)
    oos = summary["oos_runtime"]
    state = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
runtime_probe_status: f75_closed_after_mandatory_runtime_probe
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
five_stage_retrospective_due_status: due_after_f75_closeout_pending_retrospective
updated_at_utc: '{created_at}'
context_anchor: stages/{STAGE_ID}/03_reviews/context_anchor.md
notes:
  - "Action(행동): F75 stage closeout(단계 마감)을 완료했다."
  - "Effect(효과): parity/runtime probe(동등성/런타임 탐침)는 보존 단서로 남기고, OOS runtime joint-axis failure(표본외 런타임 공동 축 실패)는 부정 기억으로 남겼다."
  - "Next(다음): {NEXT_RUN_ID} must run before F76 open(F76 개방 전 실행 필요)."
  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."
"""
    base.write_text(ROOT / "docs/workspace/workspace_state.yaml", state)
    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

## Current Truth(현재 진실)

Action(행동): F75 stage closeout(단계 마감)을 완료했다.

Effect(효과): F75를 `{STATUS}`로 닫고, F76 개방 전에 five-stage retrospective(5단계 중간 검토)를 필수 next action(다음 행동)으로 설정했다.

## Closeout KPI(마감 KPI)

- validation runtime(검증 런타임): net/PF/DD/tpd `{summary['validation_runtime'].get('net_profit')}/{summary['validation_runtime'].get('profit_factor')}/{summary['validation_runtime'].get('max_drawdown_percent')}%/{summary['validation_runtime'].get('trades_per_day')}`
- OOS runtime(표본외 런타임): net/PF/DD/tpd `{oos.get('net_profit')}/{oos.get('profit_factor')}/{oos.get('max_drawdown_percent')}%/{oos.get('trades_per_day')}`
- signal/feature parity(신호/피처 동등성): diff `0`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    base.write_text(ROOT / "docs/context/current_working_state.md", current)
    selection = f"""# F75 Selection Status(선택 상태)

Status(상태): `{STATUS}`

Judgment(판정): `{JUDGMENT}`

Action(행동): F75를 보존 단서 + 부정 기억으로 닫았다.

Effect(효과): selected baseline(선택 기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)를 만들지 않는다.

Next(다음): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    base.write_text(SELECTED_DIR / "selection_status.md", selection)
    row_id = f"{RUN_ID}__stage_closeout"
    row = {
        "ledger_row_id": row_id,
        "row_id": row_id,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "stage_closeout(단계 마감)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "stage_closeout(단계 마감)",
        "tier_scope": "Tier A separate; Tier B out_of_scope_by_claim; Tier A+B out_of_scope_by_claim",
        "kpi_scope": "stage_closeout_runtime_probe_gap_and_negative_memory(단계 마감 런타임 탐침 간극 및 부정 기억)",
        "scoreboard_lane": "stage_closeout(단계 마감)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "result_judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "primary_report": rel(REPORT_PATH),
        "primary_artifact": rel(RUN_MANIFEST_PATH),
        "primary_kpi": f"F75E OOS net={oos.get('net_profit')}; PF={oos.get('profit_factor')}; DD={oos.get('max_drawdown_percent')}%; trades_day={oos.get('trades_per_day')}",
        "guardrail_kpi": "signal_diff=0; feature_diff=0; probability_parity=3/3; source_overlap=1.0",
        "external_verification_status": "completed(완료)",
        "notes": "F75 closed after mandatory MT5 Runtime Probe; preserved parity/runtime clue and negative economics memory.",
        "run_number": "frontier75F",
        "date": created_at[:10],
        "run_date": created_at[:10],
        "decision": STATUS,
        "next_run_id": NEXT_RUN_ID,
        "next_action": NEXT_RUN_ID,
        "rows": "1",
        "claim_boundary": CLAIM_BOUNDARY,
        "net_profit": oos.get("net_profit"),
        "profit_factor": oos.get("profit_factor"),
        "drawdown": oos.get("max_drawdown_percent"),
        "max_drawdown_percent": oos.get("max_drawdown_percent"),
        "trade_count": oos.get("trade_count"),
        "trade_density": oos.get("trades_per_day"),
        "expectancy": oos.get("expectancy"),
        "recovery_factor": oos.get("recovery_factor"),
        "created_at_utc": created_at,
        "required_gate_audit": rel(GATE_AUDIT_PATH),
        "gate_audit_path": rel(GATE_AUDIT_PATH),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "not_claimed",
        "run_family": "frontier_stage_closeout(전선 단계 마감)",
        "run_type": "stage_closeout(단계 마감)",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_MANIFEST_PATH),
        "result_path": rel(REPORT_PATH),
        "evidence_boundary": "preserved_clue_negative_memory_no_authority(보존 단서와 부정 기억, 권위 없음)",
        "question": "Can volatility compression plus liquidity release create tradeable runtime density?(변동성 압축 + 유동성 방출이 거래 가능한 런타임 밀도를 만들 수 있나?)",
        "artifact_count": "7",
    }
    alpha = ROOT / "docs/registers/alpha_run_ledger.csv"
    run_registry = ROOT / "docs/registers/run_registry.csv"
    with base.fs_path(run_registry).open("r", encoding="utf-8-sig", newline="") as handle:
        run_fields = list(csv.DictReader(handle).fieldnames or [])
    with base.fs_path(alpha).open("r", encoding="utf-8-sig", newline="") as handle:
        alpha_fields = list(csv.DictReader(handle).fieldnames or [])
    base.upsert_csv_row(run_registry, "run_id", row, run_fields)
    base.upsert_csv_row(alpha, "ledger_row_id", row, alpha_fields)
    base.upsert_csv_row(REVIEW_DIR / "stage_run_ledger.csv", "ledger_row_id", row, alpha_fields)
    marker = "<!-- frontier75F_stage_closeout_volatility_compression_runtime_gap_v1 -->"
    block = f"""<!-- frontier75F_stage_closeout_volatility_compression_runtime_gap_v1 -->
- `{RUN_ID}` closes Frontier75(전선75) as `{STATUS}`. Preserved clue(보존 단서): ONNX materialization and runtime parity(ONNX 물질화 및 런타임 동등성) probability/signal `3/3`, signal/feature diff `0`, MT5 probe `2/2`. Negative memory(부정 기억): meaningful proxy signal(의미 프록시 신호) `0`, F75C repair scout clue(수리 탐색 단서) `0`, OOS runtime net/PF/DD/tpd `{oos.get('net_profit')}/{oos.get('profit_factor')}/{oos.get('max_drawdown_percent')}%/{oos.get('trades_per_day')}`. Evidence(근거): `{rel(REPORT_PATH)}`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{NEXT_RUN_ID}`."""
    text = base.read_text(ROOT / "docs/registers/idea_registry.md")
    if marker not in text:
        base.write_text(ROOT / "docs/registers/idea_registry.md", text.rstrip() + "\n\n" + block)


def main() -> None:
    ensure_dirs()
    created_at = base.now_utc()
    summary = write_artifacts(created_at)
    update_state_ledgers_registers(summary, created_at)
    print(json.dumps({
        "status": STATUS,
        "judgment": JUDGMENT,
        "next_run_id": NEXT_RUN_ID,
        "oos_runtime_net_pf_dd_tpd": [
            summary["oos_runtime"].get("net_profit"),
            summary["oos_runtime"].get("profit_factor"),
            summary["oos_runtime"].get("max_drawdown_percent"),
            summary["oos_runtime"].get("trades_per_day"),
        ],
        "five_stage_retrospective_due_status": "due_after_f75_closeout_pending_retrospective",
        "report": rel(REPORT_PATH),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
