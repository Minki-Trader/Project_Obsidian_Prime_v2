# 97_adapter_research__v41_oos_early_lifecycle_repair

Stage97(97단계)는 Stage96(96단계) 판정에 따라 V41 adapter(브이41 어댑터)의 OOS early flatline risk(표본외 초반 평탄화 위험)를 lifecycle/hold/re-entry(생명주기/보유/재진입) 축으로만 좁게 수리한다.

## Bounded Question(경계 질문)

`max_hold_bars(최대 보유 봉수)` 또는 same-direction re-entry cooldown(동방향 재진입 쿨다운)을 좁게 바꾸면 Stage93 best(93단계 최선안)의 validation/OOS full split KPI(검증/표본외 전체 분할 핵심성과지표)를 보존하면서 OOS early(표본외 초반) 약점이 개선되는가?

Effect(효과): Stage97(97단계)는 entry gate(진입 게이트)를 더 조이지 않고, trade lifecycle(거래 생명주기)만 좁게 확인한다.

## Planned Variants(계획 변형)

- `h2_cd10`: max_hold_bars(최대 보유 봉수) 2, same-direction cooldown(동방향 쿨다운) 10.
- `h4_cd10`: max_hold_bars(최대 보유 봉수) 4, same-direction cooldown(동방향 쿨다운) 10.
- `h3_cd8`: max_hold_bars(최대 보유 봉수) 3, same-direction cooldown(동방향 쿨다운) 8.

## Boundary(경계)

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`
