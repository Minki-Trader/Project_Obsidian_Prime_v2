# 95_adapter_research__v41_oos_early_entry_gate_repair

Stage95(95단계)는 Stage94(94단계) 판정에 따라 Stage93 best(93단계 최선안) `s93_v41_h3_risk475_gate08_sl2075_tp40_cd10`의 OOS early flatline risk(표본외 초반 평탄화 위험)를 entry gate/confidence threshold(진입 게이트/신뢰도 문턱)로 좁게 수리한다.

## Bounded Question(경계 질문)

Can entry gate/confidence threshold(진입 게이트/신뢰도 문턱) repair OOS early flatline risk(표본외 초반 평탄화 위험) while preserving validation/OOS net/PF/DD(검증/표본외 순손익/수익 팩터/손실률)?

## Candidate Knobs(후보 조절점)

- short gate 0.09(숏 게이트 0.09): `sl2075_tp40_gate09`
- short gate 0.10(숏 게이트 0.10): `sl2075_tp40_gate10`
- threshold 0.56(문턱 0.56): `sl2075_tp40_thr056`

## Boundary(경계)

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`
