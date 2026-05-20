# Stage267 Initial Racing Gap Report(267단계 초기 경주 공백 보고)

- run(실행): `run267A_stage267_baseline_candidate_racing_protocol_v1`
- status(상태): `initial_evidence_synthesis_completed_no_candidate_selection`
- evidence_boundary(근거 경계): existing Stage258/262/264/265 evidence synthesis only(기존 258/262/264/265단계 근거 합성 전용)
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`

## What Was Done(수행 내용)

Action(행동): Stage258/262/264/265(258/262/264/265단계)의 KPI CSV(핵심 성과 지표 CSV), quality matrix(품질 행렬), monthly KPI(월별 핵심 성과 지표), segment KPI(구간 핵심 성과 지표)를 다섯 Baseline candidate(기준 후보)에 맞춰 다시 묶었다.

Effect(효과): 후보를 하나 고르지 않고, 다음 R&D racing(연구개발 경주)이 어디를 먼저 때려야 하는지 보이는 scoreboard(점수판)와 weakness matrix(약점 행렬)를 만들었다.

## Candidate Read(후보 판독)

- `s262_lowrank_inner_half_filter`: validation-heavy(검증 중심) 후보답게 validation PF(검증 수익 팩터) `1.62`, validation net(검증 순수익) `1336.78`, segment issue(구간 약점) `0`으로 가장 편하다. 다만 OOS net(표본외 순수익) `745.71`이라 OOS expansion(표본외 확장)은 약하다.
- `s264_lowrank_control`: defensive control(방어 기준)로 유지할 만하다. validation PF(검증 수익 팩터) `1.61`, OOS PF(표본외 수익 팩터) `1.70`이지만 OOS net(표본외 순수익)은 `775.97`로 challenger(도전자)보다 낮다.
- `s264_allow_inner_high_quarter`: challenger(도전자) 역할은 유지한다. OOS PF(표본외 수익 팩터) `1.74`, OOS net(표본외 순수익) `857.67`은 좋지만 OOS final month(표본외 마지막 달) `2026.04`가 `-41.14`다.
- `s264_allow_inner_all_oos_anchor`: OOS anchor(표본외 앵커)로는 가치가 있지만 hard_quality_pass(강 품질 통과)가 `False(거짓)`이고 validation late PF(검증 후반 수익 팩터) `1.484572479`가 약하다.
- `s258_short_tight_control`: stress challenger(압박 도전자)로만 둔다. OOS net(표본외 순수익) `950.22`는 가장 크지만 validation PF(검증 수익 팩터) `1.48`, OOS DD(drawdown, 손실폭) `11.8815%`, segment issue(구간 약점) `4`가 불편하다.

## Evidence Gaps(근거 공백)

- extended period test(확장 기간 시험): 2024년 같은 과거 기간은 아직 이 후보군 기준으로 재시험하지 않았다.
- feature/category ablation(피처/범주 제거): 후보군 기준의 새 제거 실험은 아직 없다.
- similar feature replacement(유사 피처 대체): ADX(ADX) 같은 의미 축 대체 실험은 아직 없다.
- balance/equity curve(잔액/평가금 곡선): MT5 report(보고서) 이미지는 존재하지만 이 pass(회차)에서 확대 시각 판독은 완료하지 않았다.
- Tier B(티어 B): 이전 근거는 `disabled_due_run50BR_fallback_only_damage` 상태가 많다. missing_required(필수 누락)로 추적한다.

## Next Run Plan(다음 실행 계획)

Next run(다음 실행): `run267B_stage267_extended_period_ablation_probe_v1`

Required first moves(필수 첫 행동):

- 2024 period manifest(2024년 기간 목록)을 만들고, 후보별 extended period test(확장 기간 시험) 가능 여부를 확인한다.
- feature/category ablation map(피처/범주 제거 지도)을 만든다.
- similar replacement map(유사 대체 지도)을 만든다.
- existing MT5 equity graph(기존 MT5 평가금 그래프)를 full/zoom(전체/확대)로 판독할 기준을 만든다.
- Any candidate repair(후보 수리)는 two-stage limit(두 단계 제한)을 걸고, 단일 월이나 단일 threshold(임계값) 미세조정 루프를 금지한다.

## Judgment(판정)

Judgment(판정): `incomplete_but_progressed`

Effect(효과): Stage267(267단계)는 이제 active_planned(활성 계획)에서 initial evidence synthesis completed(초기 근거 합성 완료)로 전진했지만, selected candidate(선택 후보), selected baseline(선택 기준선), ONNX readiness(ONNX 준비), runtime authority(런타임 권위)는 모두 `not_claimed(주장 안 함)`이다.
