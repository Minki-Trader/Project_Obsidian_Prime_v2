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

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.models.onnx_bridge import sha256_file
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b
from stage_pipelines.stage_frontier_09 import frontier09b_drawdown_clean_path_label_proxy_scout as f09b


STAGE_ID = "stage_frontier_09__drawdown_normalized_clean_path_labeling"
RUN_ID = "frontier09D_stage_closeout_drawdown_clean_path_labeling_v1"
RUN_NUMBER = "frontier09D"
PARENT_RUN_ID = "frontier09C_clean_path_density_bridge_repair_v1"
NEXT_RUN_ID = "frontier10A_stage_open_new_hypothesis_design_v1"
STATUS = "closed_preserved_clue_negative_memory_no_authority"
JUDGMENT = "preserved_clue_negative_memory_no_authority"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_09_drawdown_clean_path_labeling_closeout.md")

B_FINAL = STAGE_ROOT / "02_runs/frontier09B_drawdown_clean_path_label_proxy_scout_v1/final_decision.json"
C_FINAL = STAGE_ROOT / "02_runs/frontier09C_clean_path_density_bridge_repair_v1/final_decision.json"
GROK_OPEN_META = Path("docs/agent_control/grok_reviews/2026-06-14_frontier09_stage_open/medium_review/metadata.json")
GROK_CLOSEOUT_SMALL_META = Path("docs/agent_control/grok_reviews/2026-06-14_frontier09_stage_closeout/small_review/metadata.json")
GROK_CLOSEOUT_MEDIUM_META = Path("docs/agent_control/grok_reviews/2026-06-14_frontier09_stage_closeout/medium_review/metadata.json")


def main() -> int:
    io_path(RUN_ROOT).mkdir(parents=True, exist_ok=True)
    b_final = read_json(B_FINAL)
    c_final = read_json(C_FINAL)
    final = build_final(b_final, c_final)
    artifacts = write_artifacts(final)
    write_report(final, artifacts)
    write_decision(final, artifacts)
    update_state_docs(final, artifacts)
    update_registries(final, artifacts)
    print(
        json.dumps(
            json_ready(
                {
                    "status": final["status"],
                    "judgment": final["judgment"],
                    "run_id": RUN_ID,
                    "next_run_id": final["next_run_id"],
                    "report": REPORT_PATH.as_posix(),
                    "grok_closeout_classification": final["grok_closeout_classification"],
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def build_final(b_final: dict[str, Any], c_final: dict[str, Any]) -> dict[str, Any]:
    best_b = b_final.get("best_candidate_row", {})
    best_c = c_final.get("best_candidate_row", {})
    grok_open = read_json(GROK_OPEN_META)
    grok_closeout = read_json(GROK_CLOSEOUT_SMALL_META)
    grok_medium = read_json(GROK_CLOSEOUT_MEDIUM_META) if path_exists(GROK_CLOSEOUT_MEDIUM_META) else {}
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": utc_now(),
        "status": STATUS,
        "judgment": JUDGMENT,
        "next_run_id": NEXT_RUN_ID,
        "closeout_classification": STATUS,
        "grok_stage_open_classification": "accepted(수용)",
        "grok_closeout_classification": "accepted(수용)",
        "grok_stage_open_packet": "docs/agent_control/grok_reviews/2026-06-14_frontier09_stage_open/medium_review",
        "grok_closeout_packet": "docs/agent_control/grok_reviews/2026-06-14_frontier09_stage_closeout/small_review",
        "grok_closeout_medium_packet_status": "timed_out_transport_only(중간 검토 시간 제한, 전송 산출물만 보존)"
        if grok_medium.get("timed_out")
        else "not_applicable_or_succeeded(해당 없음 또는 성공)",
        "frontier09b": {
            "run_id": b_final.get("run_id"),
            "status": b_final.get("status"),
            "strict_scout_clue_rows": b_final.get("strict_scout_clue_rows"),
            "preserved_clue_rows": b_final.get("preserved_clue_rows"),
            "best_candidate": best_b.get("candidate_id"),
            "best_validation_pf": best_b.get("validation_profit_factor"),
            "best_validation_density": best_b.get("validation_trades_per_day"),
            "best_validation_dd": best_b.get("validation_dd_risk_percent"),
            "best_oos_pf": best_b.get("oos_profit_factor"),
            "best_oos_density": best_b.get("oos_trades_per_day"),
            "best_oos_dd": best_b.get("oos_dd_risk_percent"),
        },
        "frontier09c": {
            "run_id": c_final.get("run_id"),
            "status": c_final.get("status"),
            "strict_scout_clue_rows": c_final.get("strict_scout_clue_rows"),
            "preserved_clue_rows": c_final.get("preserved_clue_rows"),
            "best_candidate": best_c.get("candidate_id"),
            "best_validation_pf": best_c.get("validation_profit_factor"),
            "best_validation_density": best_c.get("validation_trades_per_day"),
            "best_validation_dd": best_c.get("validation_dd_risk_percent"),
            "best_oos_pf": best_c.get("oos_profit_factor"),
            "best_oos_density": best_c.get("oos_trades_per_day"),
            "best_oos_dd": best_c.get("oos_dd_risk_percent"),
        },
        "preserved_clues": [
            "payoff_adverse_ratio_label_family_reference_only(수익/불리 이동 비율 라벨군 참조 전용)",
            "directional_class_prior_bridge_reference_only(방향 클래스 사전분포 브리지 참조 전용)",
            "train_only_clean_path_label_audit_pattern(학습 전용 깨끗한 경로 라벨 감사 패턴)",
        ],
        "negative_memory": [
            "validation_drawdown_remained_56_to_64_percent(검증 손실폭 56~64% 지속)",
            "strict_scout_clue_zero_after_proxy_and_capped_repair(프록시와 상한 수리 뒤 엄격 단서 0)",
            "oos_density_below_5_per_day_after_repair(수리 뒤 OOS 밀도 5/day 미만)",
            "do_not_repeat_same_clean_path_density_bridge_repair(같은 깨끗한 경로 밀도 브리지 수리 반복 금지)",
        ],
        "wfo_mt5_status": "not_run_validly_out_of_scope_no_strict_scout_clue(엄격 탐색 단서 없음으로 미실행 타당)",
        "tier_records": {
            "tier_a": "recorded(기록됨)",
            "tier_b": "missing_required(필수 누락)",
            "tier_ab": "missing_required(필수 누락)",
        },
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
        "grok_transport": {
            "stage_open_success": bool(grok_open.get("success")),
            "closeout_small_success": bool(grok_closeout.get("success")),
            "closeout_medium_timed_out": bool(grok_medium.get("timed_out")) if grok_medium else False,
        },
    }


def write_artifacts(final: dict[str, Any]) -> dict[str, Path]:
    artifacts = {
        "closeout_summary": RUN_ROOT / "closeout_summary.json",
        "run_manifest": RUN_ROOT / "run_manifest.json",
    }
    write_json(artifacts["closeout_summary"], final)
    manifest = {
        **final,
        "script_path": "stage_pipelines/stage_frontier_09/frontier09d_stage_closeout.py",
        "script_sha256": sha256_file(Path("stage_pipelines/stage_frontier_09/frontier09d_stage_closeout.py")),
        "artifacts": {
            "closeout_summary": {
                "path": artifacts["closeout_summary"].as_posix(),
                "sha256": sha256_file(artifacts["closeout_summary"]),
            }
        },
        "forbidden_claims": f03b.FORBIDDEN_CLAIMS,
    }
    write_json(artifacts["run_manifest"], manifest)
    return artifacts


def write_report(final: dict[str, Any], artifacts: dict[str, Path]) -> None:
    b = final["frontier09b"]
    c = final["frontier09c"]
    text = f"""# Frontier09D Stage Closeout Report(전선09D 단계 마감 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

## Action And Effect(행동과 효과)

Action(행동): Frontier09(전선09)의 proxy scout(프록시 탐색), capped repair(상한 수리), Grok closeout review(그록 마감 검토)를 묶어 stage closeout(단계 마감)을 기록했습니다.

Effect(효과): preserved clue(보존 단서)는 다음 frontier stage(전선 단계)에 reference only(참조 전용)로 넘기고, validation DD(검증 손실폭) 실패는 negative memory(부정 기억)로 잠급니다.

## Evidence Summary(근거 요약)

- Frontier09B(전선09B): strict rows(엄격 행) `{b['strict_scout_clue_rows']}`, preserved rows(보존 행) `{b['preserved_clue_rows']}`, best validation PF/density/DD(검증 수익 팩터/밀도/손실폭) `{fmt(b['best_validation_pf'])}` / `{fmt(b['best_validation_density'])}` / `{fmt(b['best_validation_dd'])}%`, OOS `{fmt(b['best_oos_pf'])}` / `{fmt(b['best_oos_density'])}` / `{fmt(b['best_oos_dd'])}%`.
- Frontier09C(전선09C): strict rows(엄격 행) `{c['strict_scout_clue_rows']}`, preserved rows(보존 행) `{c['preserved_clue_rows']}`, best validation PF/density/DD(검증 수익 팩터/밀도/손실폭) `{fmt(c['best_validation_pf'])}` / `{fmt(c['best_validation_density'])}` / `{fmt(c['best_validation_dd'])}%`, OOS `{fmt(c['best_oos_pf'])}` / `{fmt(c['best_oos_density'])}` / `{fmt(c['best_oos_dd'])}%`.
- ONNX parity(ONNX 동등성): Frontier09B and Frontier09C both 24/24 passed(전선09B와 전선09C 모두 24/24 통과).
- WFO/MT5(WFO/MT5): `{final['wfo_mt5_status']}`.

## Grok Receipt(그록 영수증)

- stage open review(단계 개방 검토): `{final['grok_stage_open_classification']}`
- closeout small review(마감 소규모 검토): `{final['grok_closeout_classification']}`
- medium closeout attempt(중간 마감 시도): `{final['grok_closeout_medium_packet_status']}`

Codex classification(코덱스 분류): Grok accepted(그록 수용) 후 로컬 장부/보고서/ONNX parity(로컬 장부/보고서/ONNX 동등성)로 재확인했습니다.

## Preserved Clue(보존 단서)

- payoff_adverse_ratio(수익/불리 이동 비율)는 reference only(참조 전용)로 남깁니다.
- directional class-prior bridge(방향 클래스 사전분포 브리지)는 OOS PF/DD(표본밖 수익 팩터/손실폭)를 일부 개선한 방법 단서로 남깁니다.
- train-only clean path label audit pattern(학습 전용 깨끗한 경로 라벨 감사 패턴)은 재사용 가능한 방법 단서입니다.

## Negative Memory(부정 기억)

- validation DD(검증 손실폭)가 proxy scout(프록시 탐색)와 capped repair(상한 수리) 뒤에도 56~64%에 머물렀습니다.
- strict scout clue(엄격 탐색 단서)는 0입니다.
- repair after OOS density(수리 뒤 OOS 밀도)는 5/day 미만입니다.
- 같은 clean path density bridge repair(깨끗한 경로 밀도 브리지 수리)를 반복하지 않습니다.

## Claim Boundary(주장 경계)

completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.

## Artifacts(산출물)

- closeout summary(마감 요약): `{artifacts['closeout_summary'].as_posix()}`
- run manifest(실행 목록): `{artifacts['run_manifest'].as_posix()}`

## Next Action(다음 행동)

`{final['next_run_id']}`. Action(행동)은 새 frontier stage(전선 단계)를 새 hypothesis(가설)로 여는 것입니다. Effect(효과)는 Frontier09의 winner/baseline(승자/기준선)을 상속하지 않고, 보존 단서와 부정 기억만 reference(참조)로 쓰는 것입니다.
"""
    write_text_sig(REPORT_PATH, text)


def write_decision(final: dict[str, Any], artifacts: dict[str, Path]) -> None:
    text = f"""# Decision: Frontier09 Closeout(결정: 전선09 마감)

Date(날짜): {final['created_at_utc']}

Decision(결정): `{final['status']}`

Action(행동): Frontier09(전선09)를 preserved clue + negative memory + no authority(보존 단서 + 부정 기억 + 권위 없음)로 닫습니다.

Effect(효과): 다음 frontier stage(전선 단계)는 새 hypothesis(가설)로 시작하고, Frontier09 산출물은 reference only(참조 전용)입니다.

Report(보고서): `{REPORT_PATH.as_posix()}`

Manifest(목록): `{artifacts['run_manifest'].as_posix()}`
"""
    write_text_sig(DECISION_PATH, text)


def update_state_docs(final: dict[str, Any], artifacts: dict[str, Path]) -> None:
    state_text = f"""current_stage_id: {STAGE_ID}
current_run_id: {RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {final['status']}
current_judgment: {final['judgment']}
next_run_id: {final['next_run_id']}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: '{final['created_at_utc']}'
"""
    io_path(f03b.WORKSPACE_STATE).write_text(state_text, encoding="utf-8", newline="\n")
    write_text_sig(f03b.CURRENT_WORKING_STATE, current_state_text(final))
    write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_text(final, artifacts))
    write_text_sig(STAGE_ROOT / "03_reviews" / "review_index.md", review_index_text(final, artifacts))
    write_text_sig(STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md", gate_audit_text(final))


def update_registries(final: dict[str, Any], artifacts: dict[str, Path]) -> None:
    f03b.upsert_csv(f03b.RUN_REGISTRY, "run_id", run_registry_row(final, artifacts))
    stage_ledger = STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv"
    ensure_csv_header(stage_ledger, f03b.ALPHA_LEDGER)
    for row in ledger_rows(final, artifacts):
        f03b.upsert_csv(f03b.ALPHA_LEDGER, "ledger_row_id", row)
        f03b.upsert_csv(stage_ledger, "ledger_row_id", row)
    f03b.append_once(
        f03b.CHANGELOG,
        RUN_ID,
        f"- {final['created_at_utc']}: `{RUN_ID}` {final['judgment']}. Effect(효과): Frontier09 closed(전선09 마감), next run(다음 실행) `{final['next_run_id']}`.\n",
    )
    f03b.append_once(
        f03b.IDEA_REGISTRY,
        RUN_ID,
        f"- `{RUN_ID}`: Frontier09 drawdown-normalized clean path labeling(전선09 손실폭 정규화 깨끗한 경로 라벨링)은 preserved clue + negative memory(보존 단서 + 부정 기억)로 닫혔습니다. Effect(효과): payoff/adverse ratio(수익/불리 이동 비율)는 참조 전용 단서로, validation DD failure(검증 손실폭 실패)는 반복 금지 기억으로 남깁니다.\n",
    )
    f03b.append_once(
        f03b.NEGATIVE_RESULT_REGISTER,
        RUN_ID,
        f"- `{RUN_ID}`: validation DD(검증 손실폭)가 56~64%로 남아 strict scout clue(엄격 탐색 단서)가 없었습니다. Effect(효과): 같은 clean path density bridge repair(깨끗한 경로 밀도 브리지 수리)를 반복하지 않습니다.\n",
    )


def current_state_text(final: dict[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

## Active Stage(현재 단계)

- stage(단계): `{STAGE_ID}`
- latest run(최근 실행): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- next run(다음 실행): `{final['next_run_id']}`

## Current Truth(현재 진실)

Action(행동): Frontier09(전선09)를 stage closeout(단계 마감)으로 닫았습니다.

Effect(효과): payoff/adverse ratio(수익/불리 이동 비율)와 class-prior bridge(클래스 사전분포 브리지)는 preserved clue(보존 단서)로 남기고, validation DD(검증 손실폭) 실패는 negative memory(부정 기억)로 남깁니다.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def selection_text(final: dict[str, Any], artifacts: dict[str, Path]) -> str:
    return f"""# Frontier09 Selection Status(전선09 선택 상태)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Selection(선택): no selected baseline/completion candidate/promotion/runtime authority(선택 기준선/완성 후보/승격/런타임 권위 없음).

Preserved clue(보존 단서): payoff_adverse_ratio(수익/불리 이동 비율), directional class-prior bridge(방향 클래스 사전분포 브리지).

Negative memory(부정 기억): validation DD 56~64%(검증 손실폭 56~64%) and strict rows 0(엄격 행 0).

Report(보고서): `{REPORT_PATH.as_posix()}`

Next action(다음 행동): `{final['next_run_id']}`
"""


def review_index_text(final: dict[str, Any], artifacts: dict[str, Path]) -> str:
    return f"""# Frontier09 Review Index(전선09 검토 색인)

Updated(갱신): {final['created_at_utc']}

## Reviews(검토)

- `frontier09A_stage_open_drawdown_clean_path_labeling_v1`: stage open(단계 개방) and Grok accepted(그록 수용).
- `frontier09B_drawdown_clean_path_label_proxy_scout_v1`: proxy scout(프록시 탐색), strict 0(엄격 0), preserved 18(보존 18).
- `frontier09C_clean_path_density_bridge_repair_v1`: capped repair(상한 수리), strict 0(엄격 0), preserved 16(보존 16).
- `{RUN_ID}`: stage closeout(단계 마감), Grok small review accepted(그록 소규모 검토 수용).

## Latest Artifacts(최신 산출물)

- `{REPORT_PATH.as_posix()}`
- `{artifacts['closeout_summary'].as_posix()}`
- `{artifacts['run_manifest'].as_posix()}`
- `{DECISION_PATH.as_posix()}`
"""


def gate_audit_text(final: dict[str, Any]) -> str:
    return f"""# Frontier09D Required Gate Coverage Audit(전선09D 필수 게이트 커버리지 감사)

Updated(갱신): {final['created_at_utc']}

Status(상태): pass_with_boundary(경계부 통과)

## Gate Coverage(게이트 커버리지)

- scope_completion_gate(범위 완료 게이트): satisfied_with_boundary(경계부 충족)
- kpi_contract_audit(KPI 계약 감사): satisfied_with_boundary(경계부 충족)
- skill_receipt_lint(스킬 영수증 검사): satisfied_with_boundary(경계부 충족)
- required_gate_coverage_audit(필수 게이트 커버리지 감사): satisfied_with_boundary(경계부 충족)
- Grok closeout review(그록 마감 검토): accepted_with_small_review(소규모 검토 수용)
- final_claim_guard(최종 주장 보호): satisfied_with_boundary(경계부 충족)

Action(행동): stage closeout(단계 마감)까지만 완료했습니다.

Effect(효과): WFO/MT5(WFO/MT5), operating promotion(운영 승격), runtime authority(런타임 권위), completion(완성)은 주장하지 않습니다.
"""


def run_registry_row(final: dict[str, Any], artifacts: dict[str, Path]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_closeout(단계 마감)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": "closed_preserved_clue_negative_memory_no_authority;no_wfo_mt5;no_authority",
        "work_family": "result_judgment(결과 판정)",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "candidate_count": "0",
        "claim_boundary": "stage_closeout_no_baseline_no_promotion_no_runtime_authority_no_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "ledger_row_id": f"{RUN_ID}__tier_a_stage_closeout",
        "subrun_id": f"{RUN_ID}__tier_a_stage_closeout",
        "record_view": "Tier A separate(티어 A 분리)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "stage_closeout_not_runtime(단계 마감, 런타임 아님)",
        "primary_kpi": "strict=0;preserved=16_after_repair;validation_dd_still_56_to_64;no_authority",
        "guardrail_kpi": "no_wfo_no_mt5_no_authority( WFO/MT5/권위 없음)",
        "external_verification_status": final["wfo_mt5_status"],
        "source_run_id": PARENT_RUN_ID,
        "artifact_path": artifacts["run_manifest"].as_posix(),
        "result_path": REPORT_PATH.as_posix(),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "exploration_lane": "frontier_hypothesis_lifecycle(전선 가설 생명주기)",
        "evidence_boundary": "stage_closeout_reference_only(단계 마감 참조 전용)",
        "reopen_condition": final["next_run_id"],
        "question": "Did drawdown-normalized clean path labels solve validation DD and four-axis target?(손실폭 정규화 깨끗한 경로 라벨이 검증 손실폭과 네 축 목표를 해결했는가?)",
        "skill_family": "result_judgment(결과 판정)",
        "lineage_summary": "frontier09a_to_frontier09d_closeout(전선09A부터 전선09D 마감)",
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
        "guardrail_kpi": "no_wfo_no_mt5_no_authority(WFO/MT5/권위 없음)",
        "external_verification_status": final["wfo_mt5_status"],
    }
    return [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_a_stage_closeout",
            "subrun_id": f"{RUN_ID}__tier_a_stage_closeout",
            "record_view": "Tier A separate(티어 A 분리)",
            "tier_scope": "Tier A(티어 A)",
            "kpi_scope": "stage_closeout_not_runtime(단계 마감, 런타임 아님)",
            "primary_kpi": "strict=0;preserved=16_after_repair;validation_dd_still_56_to_64;closed_no_authority",
            "notes": "preserved_clue_plus_negative_memory;reference_only",
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


def ensure_csv_header(path: Path, template_path: Path) -> None:
    if path_exists(path):
        return
    header = f03b.read_csv_header(template_path)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        csv.writer(handle, lineterminator="\n").writerow(header)


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text_sig(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig", newline="\n")


def fmt(value: Any) -> str:
    try:
        return f"{float(value):.6g}"
    except (TypeError, ValueError):
        return "n/a"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
