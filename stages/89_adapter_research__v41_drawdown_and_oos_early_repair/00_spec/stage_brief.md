# 89_adapter_research__v41_drawdown_and_oos_early_repair

Stage89(89단계)는 Stage88(88단계) 판정에 따라 Stage87 best(87단계 최선안)의 DD(손실률)와 OOS early(표본외 초반) 약점을 좁게 수리하는 단계다.

## Bounded Question(경계 질문)

Can the Stage87 best adapter(87단계 최선 어댑터) lower validation DD(검증 손실률) and strengthen OOS early(표본외 초반) while preserving PF/net(수익 팩터/순손익)?

Effect(효과): Stage89(89단계)는 넓은 model search(모델 탐색)가 아니라, Stage87 best(87단계 최선안)의 약점 두 개만 겨냥한다.

## Candidate Knobs(후보 조절점)

- SL compression(손절 압축): `sl205` 또는 `sl210`
- cooldown guard(재진입 냉각 보호): `cd12` 재확인
- risk cap balance(위험 상한 균형): `risk45` 또는 `risk475`

## Boundary(경계)

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`
