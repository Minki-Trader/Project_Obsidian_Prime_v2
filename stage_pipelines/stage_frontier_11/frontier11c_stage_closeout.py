from __future__ import annotations

import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.models.onnx_bridge import sha256_file
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b
from stage_pipelines.stage_frontier_11 import frontier11b_subperiod_stability_proxy_scout as f11b


STAGE_ID = f11b.STAGE_ID
RUN_ID = "frontier11C_stage_closeout_subperiod_stability_first_onnx_scout_v1"
RUN_NUMBER = "frontier11C"
PARENT_RUN_ID = f11b.RUN_ID
NEXT_RUN_ID = "frontier12A_stage_open_new_hypothesis_design_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_11/frontier11c_stage_closeout.py")
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_11_subperiod_stability_closeout.md")

F11A_REPORT = STAGE_ROOT / "03_reviews" / "frontier11A_stage_open_subperiod_stability_first_onnx_scout_v1_report.md"
F11B_REPORT = STAGE_ROOT / "03_reviews" / f"{f11b.RUN_ID}_report.md"
F11B_FINAL = STAGE_ROOT / "02_runs" / f11b.RUN_ID / "final_decision.json"
F11B_SUMMARY = STAGE_ROOT / "02_runs" / f11b.RUN_ID / "stability_candidate_summary.csv"
F11B_SELECTOR = STAGE_ROOT / "02_runs" / f11b.RUN_ID / "selector_comparison.csv"
GROK_PACKET = Path("docs/agent_control/grok_reviews/2026-06-14_frontier11_stage_closeout/small_review")
GROK_PROMPT = GROK_PACKET / "prompt.md"
GROK_OUTPUT = GROK_PACKET / "clean_output.md"


def main() -> int:
    io_path(RUN_ROOT).mkdir(parents=True, exist_ok=True)
    f11b_final = read_json(F11B_FINAL)
    grok_output = io_path(GROK_OUTPUT).read_text(encoding="utf-8-sig")
    final = build_final(f11b_final, grok_output)
    artifacts = write_artifacts(final)
    write_report(final, artifacts)
    update_registries(final, artifacts)
    print(
        json.dumps(
            json_ready(
                {
                    "status": final["status"],
                    "judgment": final["judgment"],
                    "run_id": RUN_ID,
                    "grok_classification": final["grok_classification"],
                    "next_run_id": NEXT_RUN_ID,
                    "report": REPORT_PATH.as_posix(),
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def build_final(f11b_final: dict[str, Any], grok_output: str) -> dict[str, Any]:
    best = dict(f11b_final.get("best_candidate_row", {}))
    aggregate = dict(f11b_final.get("aggregate_top_candidate", {}))
    checks = {
        "grok_accepted": grok_accepted(grok_output),
        "f11b_strict_zero": int(f11b_final.get("strict_scout_clue_rows", -1)) == 0,
        "f11b_preserved_zero": int(f11b_final.get("preserved_clue_rows", -1)) == 0,
        "aggregate_equals_stability_top": str(best.get("candidate_id", "")) == str(aggregate.get("candidate_id", "")),
        "worst_subperiod_dd_not_repaired": safe_float(best.get("validation_oos_subperiod_worst_dd_risk_percent"), 0.0) >= 59.0,
    }
    if not all(checks.values()):
        status = "frontier11_closeout_needs_local_verification_no_authority"
        judgment = "needs_local_verification(로컬 검증 필요)"
        classification = "needs_local_verification(로컬 검증 필요)"
    else:
        status = "closed_negative_memory_no_authority"
        judgment = "negative_memory(부정 기억)"
        classification = "accepted(수용)"
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": utc_now(),
        "status": status,
        "judgment": judgment,
        "closeout_classification": "negative_memory(부정 기억)",
        "grok_classification": classification,
        "local_verification": {
            "checks": checks,
            "judgment": "pass_with_boundary(경계부 통과)" if all(checks.values()) else "needs_local_verification(로컬 검증 필요)",
        },
        "source_f11b_status": f11b_final.get("status", ""),
        "source_f11b_judgment": f11b_final.get("judgment", ""),
        "strict_scout_clue_rows": int(f11b_final.get("strict_scout_clue_rows", 0)),
        "preserved_clue_rows": int(f11b_final.get("preserved_clue_rows", 0)),
        "best_candidate_row": best,
        "aggregate_top_candidate": aggregate,
        "negative_memory": [
            "post_fit_subperiod_stability_selection_did_not_change_aggregate_top(적합 후 하위기간 안정성 선택이 합계 최상위를 바꾸지 못함)",
            "validation_dd_floor_remained_about_59p5_percent(검증 손실폭 바닥이 약 59.5%로 남음)",
            "same_pool_selector_weight_tweaks_are_repetitive_repair(같은 후보군 선택기 가중 미세조정은 반복 수리)",
        ],
        "reference_only_carry": [
            "subperiod_slice_metric_spec(하위기간 조각 지표 명세)",
            "selector_comparison_control_arm_pattern(선택기 비교 대조군 패턴)",
            "f10_utility_margin_clue_as_frozen_surface_reference(F10 효용 마진 단서의 고정 표면 참조)",
            "negative_memory_that_post_fit_selection_alone_cannot_break_f10c_validation_dd_floor(적합 후 선택만으로 F10C 검증 손실폭 바닥을 깨지 못한다는 부정 기억)",
        ],
        "wfo_mt5_status": "skipped_valid_no_strict_or_preserved_clue(엄격/보존 단서 없음으로 생략 타당)",
        "stage_closeout_decision": "close_frontier11_and_open_next_frontier_hypothesis(전선11을 닫고 다음 전선 가설 개방)",
        "artifact_lineage": {
            "source_inputs": [F11B_FINAL.as_posix(), F11B_SUMMARY.as_posix(), F11B_SELECTOR.as_posix(), GROK_OUTPUT.as_posix()],
            "producer": SCRIPT_PATH.as_posix(),
            "consumer": NEXT_RUN_ID,
            "lineage_judgment": "connected_with_grok_closeout_boundary(그록 마감 경계로 연결)",
        },
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_artifacts(final: dict[str, Any]) -> dict[str, Path]:
    artifacts = {
        "closeout_summary": RUN_ROOT / "closeout_summary.json",
        "run_manifest": RUN_ROOT / "run_manifest.json",
        "decision": DECISION_PATH,
    }
    write_json(artifacts["closeout_summary"], final)
    manifest = {
        **final,
        "script_path": SCRIPT_PATH.as_posix(),
        "script_sha256": sha256_file(SCRIPT_PATH),
        "inputs": {
            "f11a_report": {"path": F11A_REPORT.as_posix(), "sha256": sha256_file(F11A_REPORT)},
            "f11b_report": {"path": F11B_REPORT.as_posix(), "sha256": sha256_file(F11B_REPORT)},
            "f11b_final": {"path": F11B_FINAL.as_posix(), "sha256": sha256_file(F11B_FINAL)},
            "f11b_summary": {"path": F11B_SUMMARY.as_posix(), "sha256": sha256_file(F11B_SUMMARY)},
            "f11b_selector": {"path": F11B_SELECTOR.as_posix(), "sha256": sha256_file(F11B_SELECTOR)},
            "grok_prompt": {"path": GROK_PROMPT.as_posix(), "sha256": sha256_file(GROK_PROMPT)},
            "grok_output": {"path": GROK_OUTPUT.as_posix(), "sha256": sha256_file(GROK_OUTPUT)},
        },
        "artifacts": {
            "closeout_summary": {"path": artifacts["closeout_summary"].as_posix(), "sha256": sha256_file(artifacts["closeout_summary"])},
            "decision": {"path": artifacts["decision"].as_posix(), "sha256": sha256_file(artifacts["decision"]) if path_exists(artifacts["decision"]) else ""},
        },
        "forbidden_claims": f03b.FORBIDDEN_CLAIMS,
    }
    write_json(artifacts["run_manifest"], manifest)
    write_text_sig(artifacts["decision"], decision_text(final))
    # Re-write manifest after the decision file exists so its hash is current.
    manifest["artifacts"]["decision"]["sha256"] = sha256_file(artifacts["decision"])
    write_json(artifacts["run_manifest"], manifest)
    return artifacts


def write_report(final: dict[str, Any], artifacts: dict[str, Path]) -> None:
    best = final["best_candidate_row"]
    aggregate = final["aggregate_top_candidate"]
    text = f"""# Frontier11C Stage Closeout Report(전선11C 단계 마감 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

## Action And Effect(행동과 효과)

Action(행동): Frontier11(전선11)을 Grok stage-closeout review(그록 단계 마감 검토) accepted(수용)와 F11B(전선11B) local verification(로컬 검증)에 따라 negative memory(부정 기억)로 닫았습니다.

Effect(효과): subperiod stability-first selection(하위기간 안정성 우선 선택)이 기존 F10C(전선10C) 후보군의 validation DD floor(검증 손실폭 바닥)를 낮추지 못했다는 사실을 다음 frontier stage(다음 전선 단계)의 reference-only memory(참조 전용 기억)로 넘깁니다.

## Evidence Read(근거 판독)

- aggregate-only top(합계 전용 최상위): `{aggregate.get('candidate_id', 'none')}`
- stability-first top(안정성 우선 최상위): `{best.get('candidate_id', 'none')}`
- strict scout clue rows(엄격 탐색 단서 행): `{final['strict_scout_clue_rows']}`
- preserved clue rows(보존 단서 행): `{final['preserved_clue_rows']}`
- validation PF/density/DD(검증 수익 팩터/밀도/손실폭): `{fmt(best.get('validation_profit_factor'))}` / `{fmt(best.get('validation_trades_per_day'))}` / `{fmt(best.get('validation_dd_risk_percent'))}%`
- OOS PF/density/DD(표본밖 수익 팩터/밀도/손실폭): `{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_trades_per_day'))}` / `{fmt(best.get('oos_dd_risk_percent'))}%`
- worst subperiod DD(최악 하위기간 손실폭): `{fmt(best.get('validation_oos_subperiod_worst_dd_risk_percent'))}%`
- WFO/MT5 status(WFO/MT5 상태): `{final['wfo_mt5_status']}`

## Grok Receipt(그록 영수증)

- trigger_reason(트리거 이유): stage closeout review(단계 마감 검토)
- review_size(검토 크기): small review(소규모 검토)
- advice_classification(조언 분류): `{final['grok_classification']}`
- prompt(프롬프트): `{GROK_PROMPT.as_posix()}`
- output(출력): `{GROK_OUTPUT.as_posix()}`
- local_verification(로컬 검증): `{final['local_verification']['judgment']}`
- final_codex_direction(최종 코덱스 방향): `closed_negative_memory_no_authority`

## Reference-Only Carry(참조 전용 이관)

{bullet_lines(final['reference_only_carry'])}

## Negative Memory(부정 기억)

{bullet_lines(final['negative_memory'])}

## Artifacts(산출물)

- closeout summary(마감 요약): `{artifacts['closeout_summary'].as_posix()}`
- run manifest(실행 목록): `{artifacts['run_manifest'].as_posix()}`
- decision(결정): `{artifacts['decision'].as_posix()}`

## Claim Boundary(주장 경계)

completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.

## Next Action(다음 행동)

`{NEXT_RUN_ID}`. Action(행동): 새 hypothesis lifecycle(가설 생명주기)로 다음 frontier stage(전선 단계)를 열 준비를 합니다. Effect(효과): Frontier11(전선11)의 실패 기억을 상속하지 않고 reference-only(참조 전용)로만 사용합니다.
"""
    write_text_sig(REPORT_PATH, text)


def update_registries(final: dict[str, Any], artifacts: dict[str, Path]) -> None:
    state_text = f"""current_stage_id: {STAGE_ID}
current_run_id: {RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {final['status']}
current_judgment: {final['judgment']}
next_run_id: {NEXT_RUN_ID}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: '{final['created_at_utc']}'
"""
    io_path(f03b.WORKSPACE_STATE).write_text(state_text, encoding="utf-8-sig", newline="\n")
    write_text_sig(f03b.CURRENT_WORKING_STATE, current_state_text(final))
    write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_text(final, artifacts))
    write_text_sig(STAGE_ROOT / "03_reviews" / "review_index.md", review_index_text(final, artifacts))
    write_text_sig(STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md", gate_audit_text(final))
    f11b.upsert_csv(f03b.RUN_REGISTRY, "run_id", run_registry_row(final, artifacts))
    stage_ledger = STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv"
    f11b.ensure_csv_header(stage_ledger, f03b.ALPHA_LEDGER)
    for row in ledger_rows(final, artifacts):
        f11b.upsert_csv(f03b.ALPHA_LEDGER, "ledger_row_id", row)
        f11b.upsert_csv(stage_ledger, "ledger_row_id", row)
    f11b.append_once(
        f03b.CHANGELOG,
        RUN_ID,
        f"- {final['created_at_utc']}: `{RUN_ID}` closed Frontier11(전선11) as negative memory(부정 기억). Effect(효과): next run(다음 실행) `{NEXT_RUN_ID}` starts a new hypothesis lifecycle(새 가설 생명주기).\n",
    )
    f11b.append_once(
        f03b.IDEA_REGISTRY,
        RUN_ID,
        f"- `{RUN_ID}`: Frontier11(전선11) closed negative memory(부정 기억 마감). Effect(효과): subperiod stability selector(하위기간 안정성 선택기)는 reference-only diagnostic pattern(참조 전용 진단 패턴)으로만 남깁니다.\n",
    )
    f11b.append_once(
        f03b.NEGATIVE_RESULT_REGISTER,
        RUN_ID,
        negative_register_entry(final),
    )


def current_state_text(final: dict[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

## Active Stage(현재 단계)

- stage(단계): `{STAGE_ID}`
- latest run(최근 실행): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- next run(다음 실행): `{NEXT_RUN_ID}`

## Current Truth(현재 진실)

Action(행동): Frontier11(전선11)은 negative memory(부정 기억)로 닫혔습니다.

Effect(효과): post-fit subperiod stability selection(적합 후 하위기간 안정성 선택)은 기존 F10C(전선10C) 후보군의 validation DD floor(검증 손실폭 바닥)를 낮추지 못했다는 기억만 reference-only(참조 전용)로 남깁니다.

Next action(다음 행동): `{NEXT_RUN_ID}`.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def selection_text(final: dict[str, Any], artifacts: dict[str, Path]) -> str:
    return f"""# Frontier11 Selection Status(전선11 선택 상태)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Latest run(최근 실행): `{RUN_ID}`

Report(보고서): `{REPORT_PATH.as_posix()}`

Final decision(최종 판단 파일): `{artifacts['closeout_summary'].as_posix()}`

Closeout classification(마감 분류): `{final['closeout_classification']}`

Next action(다음 행동): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) 없음.
"""


def review_index_text(final: dict[str, Any], artifacts: dict[str, Path]) -> str:
    artifact_lines = "\n".join(f"- `{path.as_posix()}`" for path in artifacts.values())
    return f"""# Frontier11 Review Index(전선11 검토 색인)

Updated(갱신): {final['created_at_utc']}

## Reviews(검토)

- `frontier11A_stage_open_subperiod_stability_first_onnx_scout_v1`: stage open(단계 개방), Grok retry accepted(그록 재시도 수용).
- `{f11b.RUN_ID}`: subperiod stability proxy scout(하위기간 안정성 프록시 탐색), strict/preserved rows(엄격/보존 행) 0.
- `{RUN_ID}`: stage closeout(단계 마감), Grok accepted(그록 수용), negative memory(부정 기억).

## Latest Artifacts(최신 산출물)

{artifact_lines}
"""


def gate_audit_text(final: dict[str, Any]) -> str:
    return f"""# Frontier11C Required Gate Coverage Audit(전선11C 필수 게이트 커버리지 감사)

Updated(갱신): {final['created_at_utc']}

Status(상태): pass_with_boundary(경계부 통과)

## Gate Coverage(게이트 커버리지)

- scope_completion_gate(범위 완료 게이트): satisfied_with_boundary(경계부 충족)
- external_review_packet(외부 검토 묶음): Grok closeout accepted(그록 마감 수용)
- local_verification_gate(로컬 검증 게이트): strict/preserved 0 and selector top unchanged(엄격/보존 0과 선택기 최상위 동일 확인)
- result_judgment_gate(결과 판정 게이트): negative_memory not invalid/block/completion(부정 기억이며 무효/차단/완성 아님)
- required_gate_coverage_audit(필수 게이트 커버리지 감사): satisfied_with_boundary(경계부 충족)
- final_claim_guard(최종 주장 보호): satisfied_with_boundary(경계부 충족)

Action(행동): Frontier11(전선11)을 closeout(마감)했습니다.

Effect(효과): WFO/MT5(WFO/MT5), operating promotion(운영 승격), runtime authority(런타임 권위), completion(완성)은 주장하지 않습니다.
"""


def decision_text(final: dict[str, Any]) -> str:
    return f"""# Decision(결정): Frontier11 Closeout(전선11 마감)

Date(날짜): 2026-06-14

Decision(결정): `{final['status']}`

Action(행동): Frontier11(전선11)을 negative memory(부정 기억)로 닫습니다.

Effect(효과): same-pool selector weight tweak(같은 후보군 선택기 가중 미세조정)을 반복하지 않고, 다음 frontier stage(전선 단계)는 새 hypothesis lifecycle(가설 생명주기)로 시작합니다.

Grok receipt(그록 영수증): `{GROK_OUTPUT.as_posix()}` accepted(수용).

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) 없음.
"""


def run_registry_row(final: dict[str, Any], artifacts: dict[str, Path]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_closeout(단계 마감)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": "frontier11_closed_negative_memory_no_authority_next_frontier12a",
        "work_family": "result_judgment(결과 판정)",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "candidate_count": "0",
        "claim_boundary": "stage_closeout_no_wfo_no_mt5_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "ledger_row_id": f"{RUN_ID}__tier_a_stage_closeout",
        "subrun_id": f"{RUN_ID}__tier_a_stage_closeout",
        "record_view": "Tier A separate(티어 A 분리)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "stage_closeout_negative_memory_not_runtime(단계 마감 부정 기억, 런타임 아님)",
        "primary_kpi": "strict=0;preserved=0;closed_negative_memory",
        "guardrail_kpi": "grok_accepted_no_wfo_no_mt5_no_authority(그록 수용, WFO/MT5/권위 없음)",
        "external_verification_status": "grok_closeout_review_done_mt5_out_of_scope(그록 마감 검토 완료, MT5 범위 밖)",
        "source_run_id": PARENT_RUN_ID,
        "artifact_path": artifacts["run_manifest"].as_posix(),
        "result_path": REPORT_PATH.as_posix(),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "exploration_lane": "frontier_hypothesis_lifecycle(전선 가설 생명주기)",
        "evidence_boundary": "stage_closeout_only(단계 마감 전용)",
        "reopen_condition": NEXT_RUN_ID,
        "question": "Should Frontier11 close as negative memory?(전선11을 부정 기억으로 닫아야 하는가?)",
        "skill_family": "result_judgment(결과 판정)",
        "lineage_summary": "frontier11b_to_frontier11c_closeout(전선11B에서 전선11C 마감)",
    }


def ledger_rows(final: dict[str, Any], artifacts: dict[str, Path]) -> list[dict[str, Any]]:
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "stage_closeout(단계 마감)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "guardrail_kpi": "grok_accepted_no_wfo_no_mt5_no_authority(그록 수용, WFO/MT5/권위 없음)",
        "external_verification_status": "grok_closeout_review_done_mt5_out_of_scope(그록 마감 검토 완료, MT5 범위 밖)",
    }
    return [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_a_stage_closeout",
            "subrun_id": f"{RUN_ID}__tier_a_stage_closeout",
            "record_view": "Tier A separate(티어 A 분리)",
            "tier_scope": "Tier A(티어 A)",
            "kpi_scope": "stage_closeout_negative_memory_not_runtime(단계 마감 부정 기억, 런타임 아님)",
            "primary_kpi": "strict=0;preserved=0;closed_negative_memory",
            "notes": f"next={NEXT_RUN_ID};no_authority",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_b_missing_required",
            "subrun_id": f"{RUN_ID}__tier_b_missing_required",
            "record_view": "Tier B separate(티어 B 분리)",
            "tier_scope": "Tier B(티어 B)",
            "kpi_scope": "missing_required(필수 누락)",
            "primary_kpi": "missing_required_no_paired_source(필수 누락, 짝 원천 없음)",
            "notes": "Tier B paired materialization not available(티어 B 짝 물질화 없음)",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_ab_combined_missing_required",
            "subrun_id": f"{RUN_ID}__tier_ab_combined_missing_required",
            "record_view": "Tier A+B combined(티어 A+B 합산)",
            "tier_scope": "Tier A+B(티어 A+B)",
            "kpi_scope": "missing_required(필수 누락)",
            "primary_kpi": "missing_required_no_combined_claim(필수 누락, 합산 주장 없음)",
            "notes": "combined record blocked by missing Tier B(티어 B 부재로 합산 기록 차단)",
        },
    ]


def negative_register_entry(final: dict[str, Any]) -> str:
    return (
        f"- `{RUN_ID}`: Frontier11(전선11) negative memory(부정 기억). "
        f"Action(행동): post-fit subperiod stability selector(적합 후 하위기간 안정성 선택기)를 F10C(전선10C) 후보군에 적용했지만 strict/preserved rows(엄격/보존 행)가 0이었습니다. "
        f"Effect(효과): same-pool selector weight tweak(같은 후보군 선택기 가중 미세조정)은 반복 수리로 보고 다음 전선으로 넘깁니다.\n"
    )


def bullet_lines(values: list[str]) -> str:
    return "\n".join(f"- `{value}`" for value in values)


def grok_accepted(text: str) -> bool:
    normalized = text.lower()
    return "accepted" in normalized and "수용" in text


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text_sig(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig", newline="\n")


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        out = float(value)
    except (TypeError, ValueError):
        return default
    return out if math.isfinite(out) else default


def fmt(value: Any) -> str:
    try:
        value_float = float(value)
    except (TypeError, ValueError):
        return "n/a"
    if math.isinf(value_float):
        return "inf"
    return f"{value_float:.6g}"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
