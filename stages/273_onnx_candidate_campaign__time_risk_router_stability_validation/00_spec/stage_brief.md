# 273_onnx_candidate_campaign__time_risk_router_stability_validation

Stage273(273단계)는 q04 time-risk router(시간 위험 라우터) pressure survivor(압박 생존 분기)의 stability validation(안정성 검증) 단계다.
효과(effect, 효과): Stage272(272단계)의 좋은 MT5(`MetaTrader 5`, 메타트레이더5) 숫자를 곧바로 candidate package(후보 패키지)로 부르지 않고, 약한 월/세션/구간/곡선/거래 품질을 다시 압박한다.

## Bounded Question(경계 질문)

q04 weak-clock throttle router(4번 약한 시계 제한 라우터)가 validation/OOS(검증/표본외) 양쪽에서 balance/equity curve(잔액/평가금 곡선), drawdown(손실폭), weak slice(약한 구간), trade quality(거래 품질)를 견디는가?
효과(effect, 효과): 좋은 PF(profit factor, 수익 팩터)와 순수익만 보고 ONNX-worthy candidate(온엑스화 가치 후보)로 과장하지 않는다.

## Stability Seed(안정성 씨앗)

- `run272A_q04_weak_clock_throttle_router` `Tier A`: PF_min(최소 수익 팩터) `1.14`, net_sum(순수익 합) `421.99`, DD_max(최대 손실폭) `34.89`
- `run272A_q04_weak_clock_throttle_router` `Tier B`: PF_min(최소 수익 팩터) `1.14`, net_sum(순수익 합) `421.99`, DD_max(최대 손실폭) `34.89`

## Required Evidence(필수 근거)

- Tier A separate(Tier A 분리)
- Tier B separate(Tier B 분리)
- Tier A+B combined(Tier A+B 합산) 또는 out_of_scope_by_claim(주장 범위 밖)
- balance/equity curve(잔액/평가금 곡선) 전체와 확대 구간
- month/session/chron slice(월/세션/시간 순서 구간)
- trade count/net/PF/DD/recovery/expectancy(거래 수/순수익/수익 팩터/손실폭/회복/기대값)
- Adapter identity precheck(어댑터 정체성 사전 점검)
- no selected candidate claim(선택 후보 주장 없음)

## Exit Conditions(종료 조건)

- q04(4번 분기)가 안정성 압박을 견디면 Adapter package(어댑터 패키지) 준비 단계로 넘긴다.
- 약한 월/세션, 확대 곡선, 거래 품질에서 무너지면 failure memory(실패 기억)로 닫는다.
- selected candidate(선택 후보), ONNX readiness(온엑스 준비)는 이 단계 개방만으로 주장하지 않는다.

## Boundary(경계)

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
