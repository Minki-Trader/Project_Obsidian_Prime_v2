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
from stage_pipelines.stage_frontier_10 import frontier10b_utility_distillation_proxy_scout as f10b
from stage_pipelines.stage_frontier_10 import frontier10c_utility_distillation_capped_repair_scout as f10c


STAGE_ID = "stage_frontier_10__split_consistent_utility_distillation"
RUN_ID = "frontier10D_stage_closeout_split_consistent_utility_distillation_v1"
RUN_NUMBER = "frontier10D"
PARENT_RUN_ID = "frontier10C_utility_distillation_capped_repair_scout_v1"
NEXT_RUN_ID = "frontier11A_stage_open_new_hypothesis_design_v1"
STATUS = "closed_preserved_clue_negative_memory_no_authority"
JUDGMENT = "preserved_clue_negative_memory_no_authority"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_10_split_consistent_utility_distillation_closeout.md")
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_10/frontier10d_stage_closeout.py")

B_FINAL = STAGE_ROOT / "02_runs/frontier10B_utility_distillation_proxy_scout_v1/final_decision.json"
C_FINAL = STAGE_ROOT / "02_runs/frontier10C_utility_distillation_capped_repair_scout_v1/repair_final_decision.json"
GROK_META = Path("docs/agent_control/grok_reviews/2026-06-14_frontier10_stage_closeout/small_review/metadata.json")
GROK_OUTPUT = Path("docs/agent_control/grok_reviews/2026-06-14_frontier10_stage_closeout/small_review/clean_output.md")
GROK_PACKET = Path("docs/agent_control/grok_reviews/2026-06-14_frontier10_stage_closeout/small_review")


def main() -> int:
    io_path(RUN_ROOT).mkdir(parents=True, exist_ok=True)
    b_final = read_json(B_FINAL)
    c_final = read_json(C_FINAL)
    grok_meta = read_json(GROK_META)
    grok_output = io_path(GROK_OUTPUT).read_text(encoding="utf-8-sig")
    final = build_final(b_final, c_final, grok_meta, grok_output)
    artifacts = write_artifacts(final)
    write_report(final, artifacts)
    write_decision(final, artifacts)
    write_manifest(final, artifacts)
    update_state_docs(final, artifacts)
    update_registries(final, artifacts)
    print(json.dumps(json_ready({
        "status": final["status"],
        "judgment": final["judgment"],
        "run_id": RUN_ID,
        "next_run_id": final["next_run_id"],
        "report": REPORT_PATH.as_posix(),
        "grok_classification": final["grok_closeout_classification"],
    }), ensure_ascii=False, indent=2))
    return 0


def build_final(
    b_final: dict[str, Any],
    c_final: dict[str, Any],
    grok_meta: dict[str, Any],
    grok_output: str,
) -> dict[str, Any]:
    if not grok_meta.get("success"):
        raise RuntimeError("Grok closeout review did not succeed; closeout gate is not satisfied.")
    if "accepted" not in grok_output.lower() and "수용" not in grok_output:
        raise RuntimeError("Grok closeout output does not contain accepted/수용 classification.")

    best_b = dict(b_final.get("best_candidate_row", {}))
    best_c = dict(c_final.get("best_candidate_row", {}))
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
        "frontier10b": summarize_run(b_final, best_b),
        "frontier10c": summarize_run(c_final, best_c),
        "grok_closeout_classification": "accepted(수용)",
        "grok_packet": GROK_PACKET.as_posix(),
        "grok_prompt_hash": grok_meta.get("prompt_hash"),
        "grok_duration_seconds": grok_meta.get("duration_seconds"),
        "grok_local_verification": (
            "accepted_with_minor_negative_memory_wording_refinement"
            "(소규모 부정 기억 문구 보강과 함께 수용)"
        ),
        "preserved_clues": [
            "utility_margin_target_reference_only(효용 마진 목표 참조 전용)",
            "modest_fixed_side_class_weight_reference_only(완만한 고정 방향 클래스 가중 참조 전용)",
            "split_consistent_label_construction_and_leakage_guard(분할 일관 라벨 구성과 누수 보호)",
            "onnx_argmax_only_export_parity_pattern(온엑스 최대확률 전용 내보내기 동등성 패턴)",
        ],
        "negative_memory": [
            "validation_drawdown_remained_56_to_60_percent(검증 손실폭 56~60% 잔존)",
            "strict_scout_clue_zero_after_proxy_and_capped_repair(프록시와 상한 수리 뒤 엄격 탐색 단서 0)",
            "density_pf_dd_not_simultaneously_satisfied(밀도/수익 팩터/손실폭 동시 충족 없음)",
            "side_class_weight_ladder_created_density_drawdown_tradeoff(방향 클래스 가중 사다리가 밀도/손실폭 절충 생성)",
            "best_preserved_repair_worsened_oos_dd_vs_frontier10b(최상 보존 수리도 전선10B 대비 OOS 손실폭 악화)",
            "do_not_repeat_same_side_weight_ladder_or_posthoc_bridge(같은 방향 가중 사다리나 사후 브리지 반복 금지)",
        ],
        "wfo_mt5_status": "not_run_validly_out_of_scope_no_strict_scout_clue(엄격 탐색 단서 없음으로 미실행 타당)",
        "tier_records": {
            "tier_a": "recorded(기록됨)",
            "tier_b": "missing_required(필수 누락)",
            "tier_ab": "missing_required(필수 누락)",
        },
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def summarize_run(final: dict[str, Any], best: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": final.get("run_id"),
        "status": final.get("status"),
        "judgment": final.get("judgment"),
        "strict_scout_clue_rows": final.get("strict_scout_clue_rows"),
        "preserved_clue_rows": final.get("preserved_clue_rows"),
        "model_count": final.get("model_count"),
        "best_candidate": best.get("candidate_id"),
        "best_validation_pf": best.get("validation_profit_factor"),
        "best_validation_density": best.get("validation_trades_per_day"),
        "best_validation_dd": best.get("validation_dd_risk_percent"),
        "best_oos_pf": best.get("oos_profit_factor"),
        "best_oos_density": best.get("oos_trades_per_day"),
        "best_oos_dd": best.get("oos_dd_risk_percent"),
        "best_frontier10b_improvement_count": best.get("frontier10b_best_improvement_count"),
    }


def write_artifacts(final: dict[str, Any]) -> dict[str, Path]:
    artifacts = {
        "closeout_summary": RUN_ROOT / "closeout_summary.json",
        "run_manifest": RUN_ROOT / "run_manifest.json",
    }
    write_json(artifacts["closeout_summary"], final)
    return artifacts


def write_manifest(final: dict[str, Any], artifacts: dict[str, Path]) -> None:
    manifest = {
        **final,
        "script_path": SCRIPT_PATH.as_posix(),
        "script_sha256": sha256_file(SCRIPT_PATH),
        "inputs": {
            "frontier10b_final_decision": {"path": B_FINAL.as_posix(), "sha256": sha256_file(B_FINAL)},
            "frontier10c_repair_final_decision": {"path": C_FINAL.as_posix(), "sha256": sha256_file(C_FINAL)},
            "grok_metadata": {"path": GROK_META.as_posix(), "sha256": sha256_file(GROK_META)},
            "grok_output": {"path": GROK_OUTPUT.as_posix(), "sha256": sha256_file(GROK_OUTPUT)},
        },
        "outputs": {
            "closeout_summary": {"path": artifacts["closeout_summary"].as_posix(), "sha256": sha256_file(artifacts["closeout_summary"])},
            "report": {"path": REPORT_PATH.as_posix(), "sha256": sha256_file(REPORT_PATH)},
            "decision": {"path": DECISION_PATH.as_posix(), "sha256": sha256_file(DECISION_PATH)},
        },
        "forbidden_claims": f03b.FORBIDDEN_CLAIMS,
    }
    write_json(artifacts["run_manifest"], manifest)


def write_report(final: dict[str, Any], artifacts: dict[str, Path]) -> None:
    b = final["frontier10b"]
    c = final["frontier10c"]
    text = f"""# Frontier10D Stage Closeout Report(전선10D 단계 마감 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

## Action And Effect(행동과 효과)

Action(행동): Frontier10(전선10)의 proxy scout(프록시 탐색), capped repair(상한 수리), Grok closeout review(그록 마감 검토)를 묶어 stage closeout(단계 마감)을 기록했습니다.

Effect(효과): utility distillation(효용 증류)은 reference-only preserved clue(참조 전용 보존 단서)로 남기고, validation DD(검증 손실폭)와 density/DD tradeoff(밀도/손실폭 절충)는 negative memory(부정 기억)로 잠급니다.

## Evidence Summary(근거 요약)

- Frontier10B(전선10B): strict rows(엄격 행) `{b['strict_scout_clue_rows']}`, preserved rows(보존 행) `{b['preserved_clue_rows']}`, ONNX parity(온엑스 동등성) `33/33`, best validation PF/density/DD(검증 수익 팩터/밀도/손실폭) `{fmt(b['best_validation_pf'])}` / `{fmt(b['best_validation_density'])}` / `{fmt(b['best_validation_dd'])}%`, OOS `{fmt(b['best_oos_pf'])}` / `{fmt(b['best_oos_density'])}` / `{fmt(b['best_oos_dd'])}%`.
- Frontier10C(전선10C): strict rows(엄격 행) `{c['strict_scout_clue_rows']}`, preserved rows(보존 행) `{c['preserved_clue_rows']}`, ONNX parity(온엑스 동등성) `99/99`, best validation PF/density/DD(검증 수익 팩터/밀도/손실폭) `{fmt(c['best_validation_pf'])}` / `{fmt(c['best_validation_density'])}` / `{fmt(c['best_validation_dd'])}%`, OOS `{fmt(c['best_oos_pf'])}` / `{fmt(c['best_oos_density'])}` / `{fmt(c['best_oos_dd'])}%`.
- WFO/MT5(WFO/MT5): `{final['wfo_mt5_status']}`.

## Grok Receipt(그록 영수증)

- closeout small review(마감 소규모 검토): `{final['grok_closeout_classification']}`
- packet(묶음): `{final['grok_packet']}`
- local verification(로컬 검증): `{final['grok_local_verification']}`

Codex classification(코덱스 분류): Grok accepted(그록 수용) 뒤 로컬 final decision files(최종 판단 파일), reports(보고서), ONNX parity(온엑스 동등성), ledgers(장부)로 재확인했습니다.

## Preserved Clue(보존 단서)

- utility_margin target(효용 마진 목표)은 reference only(참조 전용)로 남깁니다.
- modest fixed side-class weighting(완만한 고정 방향 클래스 가중)은 OOS PF/density(표본밖 수익 팩터/밀도)를 일부 개선한 objective tweak(목적 조정) 단서입니다.
- split-consistent construction and leakage guard(분할 일관 구성과 누수 보호)는 재사용 가능한 audit pattern(감사 패턴)입니다.

## Negative Memory(부정 기억)

- validation DD(검증 손실폭)가 proxy scout(프록시 탐색)와 capped repair(상한 수리) 뒤에도 56~60%에 머물렀습니다.
- strict scout clue(엄격 탐색 단서)는 0입니다.
- higher side weights(더 높은 방향 가중치)는 density(밀도)를 올렸지만 DD(손실폭)를 악화했습니다.
- best preserved repair(최상 보존 수리)도 Frontier10B(전선10B) 대비 OOS DD(표본밖 손실폭)를 `{fmt(b['best_oos_dd'])}%`에서 `{fmt(c['best_oos_dd'])}%`로 악화했습니다.
- 같은 side-class-weight ladder(방향 클래스 가중 사다리), density bridge(밀도 브리지), threshold micro-search(임계값 미세 탐색)를 Frontier10(전선10) 안에서 반복하지 않습니다.

## Tier Records(티어 기록)

- Tier A separate(Tier A 분리): `{final['tier_records']['tier_a']}`
- Tier B separate(Tier B 분리): `{final['tier_records']['tier_b']}`
- Tier A+B combined(Tier A+B 합산): `{final['tier_records']['tier_ab']}`

## Claim Boundary(주장 경계)

completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.

## Artifacts(산출물)

- closeout summary(마감 요약): `{artifacts['closeout_summary'].as_posix()}`
- run manifest(실행 목록): `{artifacts['run_manifest'].as_posix()}`
- decision(결정): `{DECISION_PATH.as_posix()}`

## Next Action(다음 행동)

`{final['next_run_id']}`. Action(행동)은 새 frontier stage(전선 단계)를 새 hypothesis(가설)로 여는 것입니다. Effect(효과)는 Frontier10(전선10)의 winner/baseline(승자/기준선)을 상속하지 않고, 보존 단서와 부정 기억만 reference(참조)로 쓰는 것입니다.
"""
    write_text_sig(REPORT_PATH, text)


def write_decision(final: dict[str, Any], artifacts: dict[str, Path]) -> None:
    text = f"""# Decision: Frontier10 Closeout(결정: 전선10 마감)

Date(날짜): {final['created_at_utc']}

Decision(결정): `{final['status']}`

Action(행동): Frontier10(전선10)을 preserved clue + negative memory + no authority(보존 단서 + 부정 기억 + 권위 없음)로 닫았습니다.

Effect(효과): 다음 frontier stage(전선 단계)는 새 hypothesis(가설)로 시작하고, Frontier10(전선10) 산출물은 reference only(참조 전용)입니다.

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
    io_path(f03b.WORKSPACE_STATE).write_text(state_text, encoding="utf-8-sig", newline="\n")
    write_text_sig(f03b.CURRENT_WORKING_STATE, current_state_text(final))
    write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_text(final))
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
        f"- {final['created_at_utc']}: `{RUN_ID}` {final['judgment']}. Effect(효과): Frontier10 closed(전선10 마감), next run(다음 실행) `{final['next_run_id']}`.\n",
    )
    f03b.append_once(
        f03b.IDEA_REGISTRY,
        RUN_ID,
        f"- `{RUN_ID}`: Frontier10 split-consistent utility distillation(전선10 분할 일관 효용 증류)은 preserved clue + negative memory(보존 단서 + 부정 기억)로 닫혔습니다. Effect(효과): utility-margin/side-weight clue(효용 마진/방향 가중 단서)는 참조 전용으로, validation DD failure(검증 손실폭 실패)와 same-family repair loop(같은 계열 수리 반복)는 부정 기억으로 남깁니다.\n",
    )
    f03b.append_once(
        f03b.NEGATIVE_RESULT_REGISTER,
        RUN_ID,
        f"- `{RUN_ID}`: validation DD(검증 손실폭)가 56~60%로 남고 best preserved repair(최상 보존 수리)도 OOS DD(표본밖 손실폭)를 악화했습니다. Effect(효과): 같은 side-class-weight ladder/density bridge/threshold micro-search(방향 클래스 가중 사다리/밀도 브리지/임계값 미세 탐색)를 Frontier10 안에서 반복하지 않습니다.\n",
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

Action(행동): Frontier10(전선10)을 stage closeout(단계 마감)으로 닫았습니다.

Effect(효과): utility distillation(효용 증류)은 reference-only preserved clue(참조 전용 보존 단서)로 남기고, validation DD(검증 손실폭)와 density/DD tradeoff(밀도/손실폭 절충)는 negative memory(부정 기억)로 남깁니다.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def selection_text(final: dict[str, Any]) -> str:
    return f"""# Frontier10 Selection Status(전선10 선택 상태)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Selection(선택): no selected baseline/completion candidate/promotion/runtime authority(선택 기준선/완성 후보/승격/런타임 권위 없음).

Preserved clue(보존 단서): utility_margin target(효용 마진 목표), modest side-class weighting(완만한 방향 클래스 가중), split-consistent audit pattern(분할 일관 감사 패턴).

Negative memory(부정 기억): validation DD 56~60%(검증 손실폭 56~60%), strict rows 0(엄격 행 0), same-family repair repetition stopped(같은 계열 수리 반복 중단).

Report(보고서): `{REPORT_PATH.as_posix()}`

Next action(다음 행동): `{final['next_run_id']}`
"""


def review_index_text(final: dict[str, Any], artifacts: dict[str, Path]) -> str:
    return f"""# Frontier10 Review Index(전선10 검토 색인)

Updated(갱신): {final['created_at_utc']}

## Reviews(검토)

- `frontier10A_stage_open_split_consistent_utility_distillation_v1`: stage open(단계 개방), Grok accepted(그록 수용), Stage295 boundary locally verified(295단계 경계 로컬 검증).
- `frontier10B_utility_distillation_proxy_scout_v1`: utility distillation proxy scout(효용 증류 프록시 탐색), train-only leakage guard(학습 전용 누수 방지), ONNX parity(온엑스 동등성), paired controls(짝 대조군).
- `frontier10C_utility_distillation_capped_repair_scout_v1`: capped side-class-weight repair scout(상한 방향 클래스 가중 수리 탐색), ONNX parity(온엑스 동등성), no post-hoc bridge(사후 브리지 없음).
- `{RUN_ID}`: stage closeout(단계 마감), Grok small review accepted(그록 소규모 검토 수용), preserved clue + negative memory(보존 단서 + 부정 기억).

## Latest Artifacts(최신 산출물)

- `{REPORT_PATH.as_posix()}`
- `{artifacts['closeout_summary'].as_posix()}`
- `{artifacts['run_manifest'].as_posix()}`
- `{DECISION_PATH.as_posix()}`
"""


def gate_audit_text(final: dict[str, Any]) -> str:
    return f"""# Frontier10D Required Gate Coverage Audit(전선10D 필수 게이트 커버리지 감사)

Updated(갱신): {final['created_at_utc']}

Status(상태): pass_with_boundary(경계부 통과)

## Gate Coverage(게이트 커버리지)

- scope_completion_gate(범위 완료 게이트): satisfied_with_boundary(경계부 충족)
- kpi_contract_audit(KPI 계약 감사): satisfied_with_boundary(경계부 충족)
- skill_receipt_lint(스킬 영수증 검사): satisfied_with_boundary(경계부 충족)
- Grok closeout review(그록 마감 검토): accepted_with_small_review(소규모 검토 수용)
- local_verification(로컬 검증): final decisions, reports, ONNX parity, ledgers checked(최종 판단/보고서/온엑스 동등성/장부 확인)
- required_gate_coverage_audit(필수 게이트 커버리지 감사): satisfied_with_boundary(경계부 충족)
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
        "primary_kpi": "strict=0;preserved=14_after_repair;validation_dd_still_56_to_60;closed_no_authority",
        "guardrail_kpi": "no_wfo_no_mt5_no_authority(WFO/MT5/권위 없음)",
        "external_verification_status": final["wfo_mt5_status"],
        "source_run_id": PARENT_RUN_ID,
        "artifact_path": artifacts["run_manifest"].as_posix(),
        "result_path": REPORT_PATH.as_posix(),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "exploration_lane": "frontier_hypothesis_lifecycle(전선 가설 생명주기)",
        "evidence_boundary": "stage_closeout_reference_only(단계 마감 참조 전용)",
        "reopen_condition": final["next_run_id"],
        "question": "Did split-consistent utility distillation solve the fixed ONNX trade/no-trade surface?(분할 일관 효용 증류가 고정 온엑스 거래/무거래 표면을 해결했는가?)",
        "skill_family": "result_judgment(결과 판정)",
        "lineage_summary": "frontier10a_to_frontier10d_closeout(전선10A부터 전선10D 마감)",
        "final_decision_path": artifacts["closeout_summary"].as_posix(),
        "gate_audit_path": (STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md").as_posix(),
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
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
    }
    return [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_a_stage_closeout",
            "subrun_id": f"{RUN_ID}__tier_a_stage_closeout",
            "record_view": "Tier A separate(티어 A 분리)",
            "tier_scope": "Tier A(티어 A)",
            "kpi_scope": "stage_closeout_not_runtime(단계 마감, 런타임 아님)",
            "primary_kpi": "strict=0;preserved=14_after_repair;validation_dd_still_56_to_60;closed_no_authority",
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
    return f10c.fmt(value)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
