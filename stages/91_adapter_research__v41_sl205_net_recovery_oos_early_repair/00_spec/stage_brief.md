# 91_adapter_research__v41_sl205_net_recovery_oos_early_repair

Stage91(91단계)는 Stage90(90단계) 판정에 따라 SL2.05(손절 2.05)의 DD(손실률) 개선을 보존하면서 validation net/PF(검증 순손익/수익 팩터)와 OOS early(표본외 초반)를 회복하는 좁은 수리 단계다.

## Bounded Question(경계 질문)

Can SL2.05 DD compression(손절 2.05 손실률 압축) recover validation net/PF(검증 순손익/수익 팩터) and strengthen OOS early(표본외 초반) without losing OOS net(표본외 순손익)?

Effect(효과): Stage91(91단계)는 Stage89(89단계)의 좋은 단서인 DD(손실률) 압축을 버리지 않고, 손상된 validation net/PF(검증 순손익/수익 팩터)만 좁게 수리한다.

## Candidate Knobs(후보 조절점)

- TP recovery(익절 회복): `sl205_tp40_cd10`
- risk balance(위험 균형): `risk45_sl205_tp38_cd10`
- middle stop(중간 손절): `sl210_tp38_cd10`

## Boundary(경계)

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`
