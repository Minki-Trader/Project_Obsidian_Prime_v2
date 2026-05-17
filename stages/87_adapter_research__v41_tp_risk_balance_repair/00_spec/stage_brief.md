# 87_adapter_research__v41_tp_risk_balance_repair

Stage87(87단계)는 Stage86(86단계) 판정에 따라 risk cap(위험 상한)과 TP trim(익절 축소)을 결합해 validation DD(검증 손실률)와 net/PF(순손익/수익 팩터)의 균형을 좁게 수리한다.

## Bounded Question(경계 질문)

risk cap + TP trim combined(위험 상한 + 익절 축소 결합)이 Stage83 CD10(83단계 CD10)의 OOS(표본외) 강점을 크게 훼손하지 않고 validation DD(검증 손실률)를 낮출 수 있는가?

Effect(효과): Stage87(87단계)는 새 모델 탐색이 아니라 Stage85(85단계)에서 분리된 두 단서의 조합만 시험한다.

## Planned Variants(계획 변형)

- `s87_v41_h3_risk475_gate08_sl225_tp38_cd10`
- `s87_v41_h3_risk45_gate08_sl225_tp38_cd10`
- `s87_v41_h3_risk475_gate08_sl215_tp38_cd10`

## Boundary(경계)

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`
