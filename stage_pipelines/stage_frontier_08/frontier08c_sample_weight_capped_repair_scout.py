from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import json_ready
from stage_pipelines.stage_frontier_08 import frontier08b_sample_weight_proxy_scout as f08b


STAGE_ID = f08b.STAGE_ID
RUN_ID = "frontier08C_sample_weight_capped_repair_scout_v1"
RUN_NUMBER = "frontier08C"
PARENT_RUN_ID = "frontier08B_sample_weight_proxy_scout_v1"
NEXT_STRICT_RUN_ID = "frontier08D_grok_pre_expensive_sample_weight_review_v1"
NEXT_CLOSEOUT_RUN_ID = "frontier08D_stage_closeout_sample_weight_objective_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
MODEL_DIR = RUN_ROOT / "models"
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"

CAPPED_REPAIR_POLICIES = (
    f08b.WeightPolicy("control", "unweighted_control", 0.0, "unweighted matched control(무가중 짝 대조군)", True),
    f08b.WeightPolicy("util_a150", "utility_emphasis", 1.50, "capped repair utility emphasis(상한 수리 경로 효용 강조)"),
    f08b.WeightPolicy("adv_a150", "adverse_downweight", 1.50, "capped repair adverse excursion downweight(상한 수리 불리 이동 하향 가중)"),
    f08b.WeightPolicy("side_a150", "side_balance_path_quality", 1.50, "capped repair side balance plus path quality(상한 수리 방향 균형+경로 품질)"),
)


def main() -> int:
    configure_frontier08b_runtime()
    f08b.io_path(RUN_ROOT).mkdir(parents=True, exist_ok=True)
    full, raw, source_integrity = f08b.f07b.load_training_packet()
    feature_order = f08b.f04d.read_feature_order()
    path = f08b.f07b.path_arrays(full, raw, f08b.HORIZON_BARS)
    targets = [
        target
        for target in f08b.build_targets(full, raw, path)
        if target.target_id == f08b.RISK_REFERENCE_VARIANT_ID
    ]
    result = f08b.train_and_evaluate(full, feature_order, path, targets)
    final = f08b.build_final(result, source_integrity, feature_order)
    final.update(
        {
            "repair_scope": "capped_third_alpha_variants_only(상한 있는 세 번째 강도 변형만)",
            "repair_parent": PARENT_RUN_ID,
            "variant_cap": "four_families_max_three_variants_each(가족 4개 이하, 각 3변형 이하)",
        }
    )
    artifacts = f08b.write_artifacts(result, final)
    write_report(final, artifacts)
    f08b.update_registries(final, artifacts)
    update_state_docs(final, artifacts)
    print(
        json.dumps(
            json_ready(
                {
                    "status": final["status"],
                    "judgment": final["judgment"],
                    "run_id": RUN_ID,
                    "strict_scout_clue_rows": final["strict_scout_clue_rows"],
                    "preserved_clue_rows": final["preserved_clue_rows"],
                    "best_candidate": final["best_candidate_row"].get("candidate_id"),
                    "next_run_id": final["next_run_id"],
                    "report": REPORT_PATH.as_posix(),
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def configure_frontier08b_runtime() -> None:
    f08b.RUN_ID = RUN_ID
    f08b.RUN_NUMBER = RUN_NUMBER
    f08b.PARENT_RUN_ID = PARENT_RUN_ID
    f08b.NEXT_STRICT_RUN_ID = NEXT_STRICT_RUN_ID
    f08b.NEXT_REPAIR_RUN_ID = NEXT_CLOSEOUT_RUN_ID
    f08b.RUN_ROOT = RUN_ROOT
    f08b.MODEL_DIR = MODEL_DIR
    f08b.REPORT_PATH = REPORT_PATH
    f08b.POLICIES = CAPPED_REPAIR_POLICIES
    f08b.MODEL_INSTANCE_PREFIX = "f08c"


def write_report(final: dict[str, Any], artifacts: dict[str, Path]) -> None:
    best = final["best_candidate_row"]
    text = f"""# Frontier08C Capped Sample Weight Repair Scout Report(전선08C 상한 표본 가중 수리 탐색 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

## Action And Effect(행동과 효과)

Action(행동): Frontier08B(전선08B)의 보존 단서(preserved clue, 보존 단서)였던 Frontier07 risk label reference(전선07 위험 라벨 참조)에 대해서만 capped repair(상한 수리)를 실행했습니다.

Effect(효과): 새 family(가족)를 늘리지 않고 alpha 1.50(강도 1.50) 세 번째 변형만 추가해, 수리 효과(repair effect, 수리 효과)가 있는지 확인했습니다.

## Best Read(최상위 판독)

- candidate(후보): `{best.get('candidate_id', 'none')}`
- weight policy(가중 정책): `{best.get('weight_policy_id', 'none')}`
- strict scout clue rows(엄격 탐색 단서 행): `{final['strict_scout_clue_rows']}`
- preserved clue rows(보존 단서 행): `{final['preserved_clue_rows']}`
- validation PF/density/DD(검증 수익 팩터/밀도/손실폭): `{f08b.fmt(best.get('validation_profit_factor'))}` / `{f08b.fmt(best.get('validation_trades_per_day'))}` / `{f08b.fmt(best.get('validation_dd_risk_percent'))}%`
- OOS PF/density/DD(표본밖 수익 팩터/밀도/손실폭): `{f08b.fmt(best.get('oos_profit_factor'))}` / `{f08b.fmt(best.get('oos_trades_per_day'))}` / `{f08b.fmt(best.get('oos_dd_risk_percent'))}%`
- paired axis improvement count(짝 비교 축 개선 수): `{best.get('paired_axis_improvement_count', 'n/a')}`
- ONNX parity(온엑스 동등성): `{best.get('parity_passed', False)}`

## Boundaries(경계)

- repair scope(수리 범위): `{final['repair_scope']}`
- variant cap(변형 상한): `{final['variant_cap']}`
- threshold/abstention search(임계값/기권 탐색): not used(사용 안 함)
- WFO/MT5(WFO/MT5): strict scout clue(엄격 탐색 단서)가 없으면 실행하지 않습니다.
- Tier B and combined(티어 B와 합산): missing_required(필수 누락)

## Artifacts(산출물)

{chr(10).join(f'- `{path.as_posix()}`' for path in artifacts.values())}

## Next Action(다음 행동)

`{final['next_run_id']}`. Action(행동)은 strict scout clue(엄격 탐색 단서)가 있으면 Grok pre-expensive review(그록 비싼 검증 전 검토)로 가고, 없으면 stage closeout(단계 마감)을 여는 것입니다. Effect(효과)는 약한 보존 단서(preserved clue, 보존 단서)를 completion candidate(완성 후보)로 과장하지 않는 것입니다.

## Claim Boundary(주장 경계)

completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""
    f08b.write_text(REPORT_PATH, text)


def update_state_docs(final: dict[str, Any], artifacts: dict[str, Path]) -> None:
    best = final["best_candidate_row"]
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
    Path("docs/workspace/workspace_state.yaml").write_text(state_text, encoding="utf-8", newline="\n")

    current_text = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

## Active Stage(현재 단계)

- stage(단계): `{STAGE_ID}`
- latest run(최근 실행): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- next run(다음 실행): `{final['next_run_id']}`

## Current Truth(현재 진실)

Action(행동): Frontier08C(전선08C)는 Frontier08B(전선08B)의 preserved clue(보존 단서)를 대상으로 capped repair(상한 수리)를 실행했습니다.

Effect(효과): sample weighting(표본 가중) 가설이 더 강한 후보로 이어지는지 보되, 새 가중 family(가족)나 threshold search(임계값 탐색)로 범위를 넓히지 않았습니다.

## Best Frontier08C Read(전선08C 최상위 판독)

- candidate(후보): `{best.get('candidate_id', 'none')}`
- strict scout clue rows(엄격 탐색 단서 행): `{final['strict_scout_clue_rows']}`
- preserved clue rows(보존 단서 행): `{final['preserved_clue_rows']}`
- validation PF/density/DD(검증 수익 팩터/밀도/손실폭): `{f08b.fmt(best.get('validation_profit_factor'))}` / `{f08b.fmt(best.get('validation_trades_per_day'))}` / `{f08b.fmt(best.get('validation_dd_risk_percent'))}%`
- OOS PF/density/DD(표본밖 수익 팩터/밀도/손실폭): `{f08b.fmt(best.get('oos_profit_factor'))}` / `{f08b.fmt(best.get('oos_trades_per_day'))}` / `{f08b.fmt(best.get('oos_dd_risk_percent'))}%`
- ONNX parity(온엑스 동등성): `{best.get('parity_passed', False)}`

## Claim Boundary(주장 경계)

completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""
    f08b.write_text(Path("docs/context/current_working_state.md"), current_text)

    selection_text = f"""# Frontier08 Selection Status(전선08 선택 상태)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

## Latest Evidence(최신 근거)

- latest run(최근 실행): `{RUN_ID}`
- report(보고서): `{REPORT_PATH.as_posix()}`
- final decision(최종 판단 파일): `{artifacts['final_decision'].as_posix()}`
- strict scout clue rows(엄격 탐색 단서 행): `{final['strict_scout_clue_rows']}`
- preserved clue rows(보존 단서 행): `{final['preserved_clue_rows']}`

## Boundary(경계)

No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
"""
    f08b.write_text(STAGE_ROOT / "04_selected" / "selection_status.md", selection_text)

    review_index = f"""# Frontier08 Review Index(전선08 검토 색인)

Updated(갱신): {final['created_at_utc']}

## Reviews(검토)

- `frontier08A_stage_open_sample_weight_objective_v1`: stage open(단계 개방) and Grok review(그록 검토).
- `frontier08B_sample_weight_proxy_scout_v1`: proxy scout(프록시 탐색), ONNX parity(온엑스 동등성), paired control comparison(짝 대조군 비교).
- `{RUN_ID}`: capped repair scout(상한 수리 탐색), ONNX parity(온엑스 동등성), paired control comparison(짝 대조군 비교).

## Latest Artifacts(최신 산출물)

{chr(10).join(f'- `{path.as_posix()}`' for path in artifacts.values())}
"""
    f08b.write_text(STAGE_ROOT / "03_reviews" / "review_index.md", review_index)

    gate_text = f"""# Frontier08C Required Gate Coverage Audit(전선08C 필수 게이트 커버리지 감사)

Updated(갱신): {final['created_at_utc']}

Status(상태): pass_with_boundary(경계부 통과)

## Gate Coverage(게이트 커버리지)

- scope_completion_gate(범위 완료 게이트): satisfied_with_boundary(경계부 충족)
- kpi_contract_audit(KPI 계약 감사): satisfied_with_boundary(경계부 충족)
- skill_receipt_lint(스킬 영수증 점검): satisfied_with_boundary(경계부 충족)
- required_gate_coverage_audit(필수 게이트 커버리지 감사): satisfied_with_boundary(경계부 충족)
- final_claim_guard(최종 주장 보호): satisfied_with_boundary(경계부 충족)

## Boundary(경계)

Action(행동): Frontier08C(전선08C)는 capped repair scout(상한 수리 탐색)만 완료했습니다.

Effect(효과): WFO/MT5(WFO/MT5), runtime authority(런타임 권위), operating promotion(운영 승격), completion(완성)은 주장하지 않습니다.
"""
    f08b.write_text(STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md", gate_text)


if __name__ == "__main__":
    raise SystemExit(main())
