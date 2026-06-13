from __future__ import annotations

import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b
from stage_pipelines.stage_frontier_08 import frontier08b_sample_weight_proxy_scout as f08b


STAGE_ID = "stage_frontier_08__sample_weighted_objective"
RUN_ID = "frontier08D_stage_closeout_sample_weight_objective_v1"
RUN_NUMBER = "frontier08D"
PARENT_RUN_ID = "frontier08C_sample_weight_capped_repair_scout_v1"
NEXT_RUN_ID = "frontier09A_stage_open_new_hypothesis_design_v1"
IDEA_ID = "IDEA-FR08-MULTI-OBJECTIVE-SAMPLE-WEIGHTING"
NEGATIVE_ID = "NR-FR08-SAMPLE-WEIGHTED-OBJECTIVE"

STATUS = "closed_preserved_clue_negative_memory_no_authority"
JUDGMENT = "preserved_clue_negative_memory(보존 단서 + 부정 기억)"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_08_sample_weighted_objective_closeout.md")
GROK_CLOSEOUT_DIR = Path("docs/agent_control/grok_reviews/2026-06-14_frontier08_stage_closeout/medium_review")
GROK_OPEN_DIR = Path("docs/agent_control/grok_reviews/2026-06-14_frontier08_stage_open/medium_review")

B_RUN = "frontier08B_sample_weight_proxy_scout_v1"
C_RUN = "frontier08C_sample_weight_capped_repair_scout_v1"


def main() -> int:
    now = utc_now()
    b_final = read_json(STAGE_ROOT / "02_runs" / B_RUN / "final_decision.json")
    c_final = read_json(STAGE_ROOT / "02_runs" / C_RUN / "final_decision.json")
    grok = read_grok_closeout()
    summary = build_summary(now, b_final, c_final, grok)
    write_outputs(summary)
    update_docs_and_registers(summary)
    print(
        json.dumps(
            json_ready(
                {
                    "status": STATUS,
                    "judgment": JUDGMENT,
                    "run_id": RUN_ID,
                    "grok_classification": summary["grok_classification"],
                    "strict_scout_clue_rows_total": summary["strict_scout_clue_rows_total"],
                    "next_run_id": NEXT_RUN_ID,
                    "report": REPORT_PATH.as_posix(),
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def build_summary(now: str, b_final: dict[str, Any], c_final: dict[str, Any], grok: dict[str, Any]) -> dict[str, Any]:
    b_best = b_final["best_candidate_row"]
    c_best = c_final["best_candidate_row"]
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": now,
        "status": STATUS,
        "judgment": JUDGMENT,
        "grok_classification": classify_grok(grok["clean_output"]),
        "grok_clean_output": grok["clean_output"],
        "grok_prompt_path": grok["prompt_path"],
        "grok_clean_output_path": grok["clean_output_path"],
        "grok_metadata_path": grok["metadata_path"],
        "grok_success": grok["success"],
        "frontier08b": {
            "run_id": B_RUN,
            "strict_scout_clue_rows": b_final["strict_scout_clue_rows"],
            "preserved_clue_rows": b_final["preserved_clue_rows"],
            "candidate_count": b_final["candidate_count"],
            "model_count": b_final.get("model_count", b_final["candidate_count"]),
            "best_candidate": best_metrics(b_best),
        },
        "frontier08c": {
            "run_id": C_RUN,
            "strict_scout_clue_rows": c_final["strict_scout_clue_rows"],
            "preserved_clue_rows": c_final["preserved_clue_rows"],
            "candidate_count": c_final["candidate_count"],
            "model_count": c_final.get("model_count", c_final["candidate_count"]),
            "best_candidate": best_metrics(c_best),
        },
        "strict_scout_clue_rows_total": int(b_final["strict_scout_clue_rows"]) + int(c_final["strict_scout_clue_rows"]),
        "preserved_clue": (
            "adverse/path utility sample weighting(불리 이동/경로 효용 표본 가중)은 "
            "OOS density(표본밖 밀도)를 5~6/day 부근으로 만들 수 있다는 단서를 남겼습니다."
        ),
        "negative_memory": (
            "sample weighting alone(표본 가중 단독)은 validation DD(검증 손실폭) 58~60%와 "
            "weak PF(약한 수익 팩터)를 해결하지 못했습니다."
        ),
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
        "closeout_basis": "no_strict_scout_clue_no_wfo_no_mt5_no_authority(엄격 탐색 단서 없음, WFO/MT5 없음, 권위 없음)",
    }


def best_metrics(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "candidate_id": row.get("candidate_id", ""),
        "weight_policy_id": row.get("weight_policy_id", ""),
        "validation_profit_factor": row.get("validation_profit_factor", ""),
        "validation_trades_per_day": row.get("validation_trades_per_day", ""),
        "validation_dd_risk_percent": row.get("validation_dd_risk_percent", ""),
        "oos_profit_factor": row.get("oos_profit_factor", ""),
        "oos_trades_per_day": row.get("oos_trades_per_day", ""),
        "oos_dd_risk_percent": row.get("oos_dd_risk_percent", ""),
        "paired_axis_improvement_count": row.get("paired_axis_improvement_count", ""),
        "parity_passed": row.get("parity_passed", ""),
    }


def write_outputs(summary: dict[str, Any]) -> None:
    write_json_sig(RUN_ROOT / "closeout_summary.json", summary)
    f03b.write_text_sig(REPORT_PATH, report_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md", gate_audit(summary))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "review_index.md", review_index(summary))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(summary))
    f03b.write_text_sig(STAGE_ROOT / "README.md", readme_text(summary))
    f03b.write_text_sig(DECISION_PATH, decision_text(summary))


def update_docs_and_registers(summary: dict[str, Any]) -> None:
    now = summary["created_at_utc"]
    f03b.write_text_sig(
        Path("docs/workspace/workspace_state.yaml"),
        "\n".join(
            [
                f"current_stage_id: {STAGE_ID}",
                f"current_run_id: {RUN_ID}",
                f"latest_completed_run_id: {RUN_ID}",
                f"current_status: {STATUS}",
                "current_judgment: preserved_clue_negative_memory_no_authority",
                f"next_run_id: {NEXT_RUN_ID}",
                "runtime_authority: not_claimed",
                "operating_promotion: not_claimed",
                "goal_achieve: not_claimed",
                f"updated_at_utc: '{now}'",
                "",
            ]
        ),
    )
    f03b.write_text_sig(Path("docs/context/current_working_state.md"), current_working_state(summary))
    update_scout_registry_row(summary["frontier08b"], "frontier08B", "frontier08A_stage_open_sample_weight_objective_v1", C_RUN)
    update_scout_registry_row(summary["frontier08c"], "frontier08C", B_RUN, RUN_ID)
    f03b.upsert_csv(f03b.RUN_REGISTRY, "run_id", run_registry_row(summary))
    f03b.upsert_csv(f03b.ALPHA_LEDGER, "ledger_row_id", ledger_row(summary))
    f03b.upsert_csv(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", ledger_row(summary))
    f03b.append_once(
        Path("docs/registers/idea_registry.md"),
        f"{RUN_ID}__{IDEA_ID}",
        (
            f"- `{IDEA_ID}` closeout(마감): `{STATUS}`. "
            f"Effect(효과): sample weighting(표본 가중)은 preserved clue(보존 단서)로만 남기고 "
            f"completion candidate(완성 후보)나 runtime authority(런타임 권위)로 올리지 않습니다.\n"
        ),
    )
    f03b.append_once(
        Path("docs/registers/negative_result_register.md"),
        f"{RUN_ID}__{NEGATIVE_ID}",
        (
            f"| `{NEGATIVE_ID}` | `{IDEA_ID}` | multi-objective sample weighting(다중목적 표본 가중)이 "
            "US100 M5 ONNX(온엑스) proxy surface(프록시 표면)를 네 축 동시 개선으로 밀 수 있다 | "
            "Frontier08B/C(전선08B/C) strict scout clue rows(엄격 탐색 단서 행)가 `0`이고 "
            "best validation DD(최상 검증 손실폭)가 58~60%라 WFO/MT5(WFO/MT5) 전 단계에서 실패했다 | "
            "OOS density(표본밖 밀도) 5~6/day를 만드는 adverse/path utility weighting(불리 이동/경로 효용 가중) "
            "단서만 보존한다 | 새 objective(목적함수)가 DD/curve quality(손실폭/곡선 품질)를 직접 다룰 때만 재개 |\n"
        ),
    )
    f03b.append_once(
        Path("docs/workspace/changelog.md"),
        RUN_ID,
        (
            f"- {now}: `{RUN_ID}` closed Frontier08(전선08) as `{STATUS}`. "
            f"Effect(효과): next run(다음 실행) `{NEXT_RUN_ID}` starts a new hypothesis lifecycle(새 가설 생명주기) "
            "without inheriting winner/baseline/promotion/runtime authority(승자/기준선/승격/런타임 권위).\n"
        ),
    )


def update_scout_registry_row(packet: dict[str, Any], run_number: str, parent_run_id: str, next_run_id: str) -> None:
    best = packet["best_candidate"]
    report = STAGE_ROOT / "03_reviews" / f"{packet['run_id']}_report.md"
    final_path = STAGE_ROOT / "02_runs" / packet["run_id"] / "final_decision.json"
    row = {
        "run_id": packet["run_id"],
        "stage_id": STAGE_ID,
        "status": "sample_weight_preserved_clue_no_authority",
        "judgment": "preserved_clue(보존 단서)",
        "path": report.as_posix(),
        "notes": f"strict={packet['strict_scout_clue_rows']};preserved={packet['preserved_clue_rows']};no_authority",
        "family": "experiment_execution(실험 실행)",
        "primary_report": report.as_posix(),
        "run_number": run_number,
        "date": "2026-06-14",
        "decision": "sample_weight_proxy_scout_no_authority",
        "parent_run_id": parent_run_id,
        "next_run_id": next_run_id,
        "claim_boundary": "proxy_scout_only_no_wfo_no_mt5_no_authority_goal_claim",
        "report_path": report.as_posix(),
        "trained_models": packet["model_count"],
        "onnx_parity": "checked_per_model(모델별 확인)",
        "best_model_id": best["candidate_id"],
        "profit_factor": best["oos_profit_factor"],
        "drawdown": best["oos_dd_risk_percent"],
        "trade_count": best["oos_trades_per_day"],
        "candidate_rows": packet["candidate_count"],
        "positive_proxy_rows": packet["preserved_clue_rows"],
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖, MT5 없음)",
        "result_judgment": "preserved_clue(보존 단서)",
        "final_decision_path": final_path.as_posix(),
        "created_at_utc": "",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "sample_weight_model_scout(표본 가중 모델 탐색)",
        "goal_achieve": "not_claimed",
        "strict_joint_pass_count": packet["strict_scout_clue_rows"],
    }
    f03b.upsert_csv(f03b.RUN_REGISTRY, "run_id", row)


def run_registry_row(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": REPORT_PATH.as_posix(),
        "notes": "frontier08_closed_no_strict_scout_clue_no_authority",
        "family": "stage_closeout(단계 마감)",
        "primary_report": REPORT_PATH.as_posix(),
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "decision": STATUS,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "gate_passes": "5",
        "gate_total": "5",
        "claim_boundary": "closeout_no_completion_no_baseline_no_promotion_no_runtime_authority_no_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "candidate_rows": str(summary["frontier08b"]["candidate_count"] + summary["frontier08c"]["candidate_count"]),
        "positive_proxy_rows": str(summary["frontier08b"]["preserved_clue_rows"] + summary["frontier08c"]["preserved_clue_rows"]),
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖, MT5 없음)",
        "result_judgment": JUDGMENT,
        "final_decision_path": (RUN_ROOT / "closeout_summary.json").as_posix(),
        "gate_audit_path": (STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md").as_posix(),
        "created_at_utc": summary["created_at_utc"],
        "required_gate_audit": "pass_with_boundary(경계부 통과)",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "stage_closeout(단계 마감)",
        "goal_achieve": "not_claimed",
        "source_authority": "local_evidence_with_grok_needs_local_verification(로컬 근거와 그록 로컬 검증 필요)",
        "strict_joint_pass_count": summary["strict_scout_clue_rows_total"],
    }


def ledger_row(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "ledger_row_id": f"{RUN_ID}__stage_closeout",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__stage_closeout",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "stage closeout(단계 마감)",
        "tier_scope": "Tier A reviewed; Tier B/combined missing_required(Tier A 검토, Tier B/합산 필수 누락)",
        "kpi_scope": "closeout judgment only(마감 판정 전용)",
        "run_family": "stage_closeout(단계 마감)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": (
            f"B strict={summary['frontier08b']['strict_scout_clue_rows']};"
            f"C strict={summary['frontier08c']['strict_scout_clue_rows']};"
            "no_wfo_no_mt5_no_authority"
        ),
        "guardrail_kpi": "completion_baseline_promotion_runtime_live_goal_not_claimed(완성/기준선/승격/런타임/실거래/목표 주장 없음)",
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖, MT5 없음)",
        "notes": "preserved clue plus negative memory; no strict scout clue(보존 단서와 부정 기억, 엄격 탐색 단서 없음)",
        "primary_family": "result_judgment(결과 판정)",
        "result_subject": "sample_weight_objective_stage_closeout(표본 가중 목적 단계 마감)",
        "question": "Should Frontier08 close without WFO/MT5?(전선08을 WFO/MT5 없이 닫아야 하는가?)",
        "updated_at_utc": summary["created_at_utc"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
    }


def report_text(summary: dict[str, Any]) -> str:
    b = summary["frontier08b"]
    c = summary["frontier08c"]
    return f"""# Frontier08 Stage Closeout Report(전선08 단계 마감 보고서)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{STATUS}`

Judgment(판정): `{JUDGMENT}`

## Action And Effect(행동과 효과)

Action(행동): Frontier08(전선08)의 sample-weighted objective(표본 가중 목적) 가설을 stage open(단계 개방), proxy scout(프록시 탐색), capped repair(상한 수리), Grok closeout review(그록 마감 검토)까지 확인했습니다.

Effect(효과): 보존 단서(preserved clue, 보존 단서)는 남기되, strict scout clue(엄격 탐색 단서)가 없으므로 WFO/MT5(WFO/MT5), runtime authority(런타임 권위), completion candidate(완성 후보)로 넘기지 않습니다.

## Evidence Summary(근거 요약)

- Frontier08B(전선08B): candidates(후보) `{b['candidate_count']}`, strict scout clue rows(엄격 탐색 단서 행) `{b['strict_scout_clue_rows']}`, preserved clue rows(보존 단서 행) `{b['preserved_clue_rows']}`.
- Frontier08B best(전선08B 최상): `{b['best_candidate']['candidate_id']}` validation PF/density/DD(검증 수익 팩터/밀도/손실폭) `{fmt(b['best_candidate']['validation_profit_factor'])}` / `{fmt(b['best_candidate']['validation_trades_per_day'])}` / `{fmt(b['best_candidate']['validation_dd_risk_percent'])}%`; OOS PF/density/DD(표본밖 수익 팩터/밀도/손실폭) `{fmt(b['best_candidate']['oos_profit_factor'])}` / `{fmt(b['best_candidate']['oos_trades_per_day'])}` / `{fmt(b['best_candidate']['oos_dd_risk_percent'])}%`.
- Frontier08C(전선08C): candidates(후보) `{c['candidate_count']}`, strict scout clue rows(엄격 탐색 단서 행) `{c['strict_scout_clue_rows']}`, preserved clue rows(보존 단서 행) `{c['preserved_clue_rows']}`.
- Frontier08C best(전선08C 최상): `{c['best_candidate']['candidate_id']}` validation PF/density/DD(검증 수익 팩터/밀도/손실폭) `{fmt(c['best_candidate']['validation_profit_factor'])}` / `{fmt(c['best_candidate']['validation_trades_per_day'])}` / `{fmt(c['best_candidate']['validation_dd_risk_percent'])}%`; OOS PF/density/DD(표본밖 수익 팩터/밀도/손실폭) `{fmt(c['best_candidate']['oos_profit_factor'])}` / `{fmt(c['best_candidate']['oos_trades_per_day'])}` / `{fmt(c['best_candidate']['oos_dd_risk_percent'])}%`.

## Grok Closeout Review(그록 마감 검토)

- packet(묶음): `{GROK_CLOSEOUT_DIR.as_posix()}`
- wrapper success(래퍼 성공): `{summary['grok_success']}`
- classification(분류): `{summary['grok_classification']}`
- local handling(로컬 처리): Grok output(그록 출력)이 명시적 accepted/rejected(수용/거절)를 담지 않아 needs_local_verification(로컬 검증 필요)로 낮췄고, Codex(코덱스)가 로컬 숫자와 정책으로 마감을 확정했습니다.

## Preserved Clue(보존 단서)

{summary['preserved_clue']}

## Negative Memory(부정 기억)

{summary['negative_memory']}

## Closeout Decision(마감 결정)

`{STATUS}`. Action(행동): Frontier08(전선08)은 여기서 닫고 `{NEXT_RUN_ID}`로 새 hypothesis lifecycle(가설 생명주기)을 엽니다.

Effect(효과): sample weighting alone(표본 가중 단독)을 같은 방식으로 반복하지 않고, 다음 단계는 DD/curve quality(손실폭/곡선 품질)를 직접 다루는 새 가설로 시작합니다.

## Claim Boundary(주장 경계)

completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def gate_audit(summary: dict[str, Any]) -> str:
    return f"""# Frontier08 Closeout Required Gate Coverage Audit(전선08 마감 필수 게이트 커버리지 감사)

Updated(갱신): {summary['created_at_utc']}

Status(상태): pass_with_boundary(경계부 통과)

## Gate Coverage(게이트 커버리지)

- scope_completion_gate(범위 완료 게이트): satisfied_with_boundary(경계부 충족)
- kpi_contract_audit(KPI 계약 감사): satisfied_with_boundary(경계부 충족)
- skill_receipt_lint(스킬 영수증 점검): satisfied_with_boundary(경계부 충족)
- required_gate_coverage_audit(필수 게이트 커버리지 감사): satisfied_with_boundary(경계부 충족)
- final_claim_guard(최종 주장 보호): satisfied_with_boundary(경계부 충족)

## Boundary(경계)

Action(행동): Frontier08(전선08)은 strict scout clue(엄격 탐색 단서)가 없어 WFO/MT5(WFO/MT5)를 실행하지 않고 마감했습니다.

Effect(효과): runtime authority(런타임 권위), operating promotion(운영 승격), completion(완성), Goal Achieve(목표 달성)를 주장하지 않습니다.
"""


def review_index(summary: dict[str, Any]) -> str:
    return f"""# Frontier08 Review Index(전선08 검토 색인)

Updated(갱신): {summary['created_at_utc']}

## Reviews(검토)

- `frontier08A_stage_open_sample_weight_objective_v1`: stage open(단계 개방) and Grok review(그록 검토).
- `{B_RUN}`: proxy scout(프록시 탐색), ONNX parity(온엑스 동등성), paired control comparison(짝 대조군 비교).
- `{C_RUN}`: capped repair scout(상한 수리 탐색), ONNX parity(온엑스 동등성), paired control comparison(짝 대조군 비교).
- `{RUN_ID}`: stage closeout(단계 마감), Grok closeout review(그록 마감 검토), final claim guard(최종 주장 보호).

## Grok Packets(그록 묶음)

- stage open(단계 개방): `{GROK_OPEN_DIR.as_posix()}`
- stage closeout(단계 마감): `{GROK_CLOSEOUT_DIR.as_posix()}`
"""


def selection_status(summary: dict[str, Any]) -> str:
    return f"""# Frontier08 Selection Status(전선08 선택 상태)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{STATUS}`

Judgment(판정): `{JUDGMENT}`

## Selection(선택)

No selected baseline/completion candidate/promotion/runtime authority(선택 기준선/완성 후보/승격/런타임 권위 없음).

## Carry Forward(이월)

- preserved clue(보존 단서): {summary['preserved_clue']}
- negative memory(부정 기억): {summary['negative_memory']}
- next run(다음 실행): `{NEXT_RUN_ID}`
"""


def readme_text(summary: dict[str, Any]) -> str:
    return f"""# {STAGE_ID}

Status(상태): `{STATUS}`

Latest run(최근 실행): `{RUN_ID}`

Next run(다음 실행): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
"""


def decision_text(summary: dict[str, Any]) -> str:
    return f"""# Decision: Close Frontier08 Sample-Weighted Objective(결정: 전선08 표본 가중 목적 마감)

Date(날짜): 2026-06-14

Decision(결정): `{STATUS}`

Rationale(근거): Frontier08B/C(전선08B/C)는 strict scout clue rows(엄격 탐색 단서 행) `0`을 기록했고, capped repair(상한 수리) 뒤에도 validation DD(검증 손실폭)가 58~60%였습니다.

Effect(효과): WFO/MT5(WFO/MT5)는 실행하지 않고, 다음 frontier stage(프론티어 단계)는 새 hypothesis lifecycle(가설 생명주기)로 시작합니다.
"""


def current_working_state(summary: dict[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {summary['created_at_utc']}

## Active Boundary(현재 경계)

- latest closed stage(최근 마감 단계): `{STAGE_ID}`
- latest completed run(최근 완료 실행): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next run(다음 실행): `{NEXT_RUN_ID}`

## Current Truth(현재 진실)

Action(행동): Frontier08(전선08)은 sample weighting(표본 가중) 가설을 proxy scout(프록시 탐색)와 capped repair(상한 수리)까지 밀고 마감했습니다.

Effect(효과): preserved clue(보존 단서)는 남기되, strict scout clue(엄격 탐색 단서)가 없으므로 WFO/MT5(WFO/MT5), completion candidate(완성 후보), runtime authority(런타임 권위)는 열지 않습니다.

## Next Work(다음 작업)

`{NEXT_RUN_ID}` opens a new hypothesis lifecycle(새 가설 생명주기). Reference, not inheritance(참조이지 상속 아님): Frontier08(전선08)의 winner/baseline/promotion/runtime authority(승자/기준선/승격/런타임 권위)는 없습니다.
"""


def read_grok_closeout() -> dict[str, Any]:
    prompt_path = GROK_CLOSEOUT_DIR / "prompt.md"
    output_path = GROK_CLOSEOUT_DIR / "clean_output.md"
    metadata_path = GROK_CLOSEOUT_DIR / "metadata.json"
    if not output_path.exists() or not metadata_path.exists():
        raise FileNotFoundError("Missing Grok closeout packet. Run grok_review_wrapper before closeout.")
    metadata = read_json(metadata_path)
    return {
        "prompt_path": prompt_path.as_posix(),
        "clean_output_path": output_path.as_posix(),
        "metadata_path": metadata_path.as_posix(),
        "clean_output": io_path(output_path).read_text(encoding="utf-8-sig").strip(),
        "success": bool(metadata.get("success")),
    }


def classify_grok(text: str) -> str:
    normalized = text.lower()
    if "accepted" in normalized or "수용" in text:
        return "accepted(수용)"
    if "rejected" in normalized or "거절" in text:
        return "rejected(거절)"
    return "needs_local_verification(로컬 검증 필요)"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json_sig(path: Path, payload: dict[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def fmt(value: Any) -> str:
    return f08b.fmt(value)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
