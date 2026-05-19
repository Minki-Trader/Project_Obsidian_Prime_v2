# 208_adapter_research__stage206_risk_cap_interpolation_repair

Stage208(208단계)은 Stage207(207단계) 판정에서 열린 bounded repair(경계 수리) 단계다.

## Bounded Question(경계 질문)

Can intermediate model risk caps(중간 모델 위험 상한) between 2.5% and 3.25%(2.5%와 3.25% 사이) reduce validation DD(검증 낙폭) below 34D(34D) while preserving validation net(검증 순손익) above 34D(34D)?

Effect(효과): Stage206(206단계)의 risk0250 clue(2.5% 위험 단서)는 쓰되, 세션 창이나 진입 로직을 새로 만지지 않는다.

## Constraints(제약)

- start from `s206_ls_ref_r0325` long-session structure(롱 세션 구조에서 시작)
- change model_risk_max_pct only(모델 위험 상한만 변경)
- no session window widening(세션 창 확장 금지)
- no entry logic change(진입 로직 변경 금지)
- preserve validation net above 34D(검증 순손익 34D 이상 보존)
- preserve validation PF and mid PF above 34D(검증 수익요인과 중반 수익요인 34D 이상 보존)
- record OOS PF/net/DD(표본외 수익요인/순손익/낙폭 기록)
- record risk/ATR telemetry(위험/ATR 기록)
- if no interpolation works, close Stage208(208단계) with evidence and route next bounded repair(다음 경계 수리)

## Boundary(경계)

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`
