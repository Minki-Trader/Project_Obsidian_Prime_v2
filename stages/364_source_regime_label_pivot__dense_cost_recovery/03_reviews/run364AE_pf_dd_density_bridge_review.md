# run364AE PF/DD density bridge review(364AE PF/DD 밀도 연결 검토)

## Current truth(현재 진실)

- run_id(실행 ID): `run364AE_review_pf_dd_near_miss_density_bridge_scout_without_db_v1`
- parent_run_id(부모 실행 ID): `run364AD_train_pf_dd_near_miss_density_bridge_scout_without_db_v1`
- next_run_id(다음 실행 ID): `run364AF_materialize_pf_lift_density_safe_expansion_without_db_v1`
- judgment(판정): `negative_for_package_positive_for_pf_lift_density_safe_expansion_no_authority`
- package_decision(패키지 결정): `no_package_pf_below_target(패키지 없음, PF 목표 미달)`
- parent selected net/PF/trades/density/DD(부모 선택 순수익/수익 팩터/거래수/밀도/낙폭): `840.055` / `1.2739357721` / `1001` / `3.006006006` / `-142.323`
- package_candidate_rows(패키지 후보 행): `0`
- pf_lift_candidate_rows(PF 상승 후보 행): `3`
- runtime_authority(런타임 권위): `not_claimed`

## Surface review(표면 검토)

| queue_id | review_status | combined_net_profit | combined_profit_factor | combined_trade_per_business_day | combined_max_drawdown |
| --- | --- | --- | --- | --- | --- |
| stress3_restore_non_hour16_margin_0_1 | pf_lift_seed_density_safe(PF 상승 씨앗, 밀도 안전) | 840.055 | 1.2739357721 | 3.006006006 | -142.323 |
| stress3_restore_march_short_p0_475 | pf_lift_seed_density_safe(PF 상승 씨앗, 밀도 안전) | 834.818 | 1.2721814278 | 3.0 | -142.323 |
| stress4_short050_pf_lift | pf_pass_density_fail_seed(PF 통과, 밀도 실패 씨앗) | 799.943 | 1.3066323163 | 2.6726726727 | -120.303 |
| adx38_stress3_month_block | reject_density_floor(밀도 하한 탈락) | 848.542 | 1.2835497807 | 2.9159159159 | -128.661 |
| stress3_restore_long_p0_42_adx35_0 | reject_density_floor(밀도 하한 탈락) | 846.467 | 1.277866063 | 2.987987988 | -142.323 |
| stress3_restore_non_hour16_margin_0_14 | reject_density_floor(밀도 하한 탈락) | 844.03 | 1.2768298079 | 2.993993994 | -142.323 |
| stress3_restore_march_short_p0_49 | reject_density_floor(밀도 하한 탈락) | 841.18 | 1.2761305224 | 2.987987988 | -142.323 |
| stress_zone_3_control | reject_density_floor(밀도 하한 탈락) | 840.192 | 1.2758061959 | 2.984984985 | -142.323 |

## Package gate audit(패키지 게이트 감사)

| gate_id | status | observed | required | effect(효과) |
| --- | --- | --- | --- | --- |
| density_floor(밀도 하한) | passed | 3.006006006 | 3.0 | minimum trade density(최소 거래 밀도)를 확인한다. |
| profit_factor_target(PF 목표) | failed | 1.2739357721 | 1.3 | PF 목표 미달이면 package(패키지)를 열지 않는다. |
| strict_package_rows(엄격 패키지 행) | failed | 0 | 1 | PF/density(수익 팩터/밀도) 동시 통과 없이는 MT5 package(MT5 패키지)를 열지 않는다. |

## PF lift candidates(PF 상승 후보)

| queue_id | review_status | combined_profit_factor | combined_trade_per_business_day | combined_net_profit |
| --- | --- | --- | --- | --- |
| stress3_restore_non_hour16_margin_0_1 | pf_lift_seed_density_safe(PF 상승 씨앗, 밀도 안전) | 1.2739357721 | 3.006006006 | 840.055 |
| stress3_restore_march_short_p0_475 | pf_lift_seed_density_safe(PF 상승 씨앗, 밀도 안전) | 1.2721814278 | 3.0 | 834.818 |
| stress4_short050_pf_lift | pf_pass_density_fail_seed(PF 통과, 밀도 실패 씨앗) | 1.3066323163 | 2.6726726727 | 799.943 |

## Positive clues(긍정 단서)

| clue_id | evidence | kpi_read | effect(효과) |
| --- | --- | --- | --- |
| density_safe_pf_near_target(밀도 안전 PF 목표 근접) | stress3_restore_non_hour16_margin_0_1__ps0_45__adx40_0__hold8 | net=840.055; pf=1.2739357721; density=3.006006006; dd=-142.323 | 다음 작업은 밀도 손실 없이 PF만 올리는 방향으로 좁힌다. |
| pf_pass_but_density_fail_exists(PF 통과 밀도 실패 존재) | stress3_restore_non_hour16_margin_0_1__ps0_45__adx40_0__hold8 | queue=stress3_restore_non_hour16_margin_0_1; pf=1.2739357721; density=3.006006006 | PF를 올리는 규칙은 찾았지만 density bridge(밀도 연결)가 필요함을 보여준다. |

## Failure memory(실패 기억)

| failure_id | evidence | kpi_read | constraint_for_next(다음 제약) |
| --- | --- | --- | --- |
| pf_below_target_blocks_package(PF 목표 미달로 패키지 차단) | stress3_restore_non_hour16_margin_0_1__ps0_45__adx40_0__hold8 | pf=1.2739357721; target=1.3 | do not package before PF>=1.30 and density>=3/day(PF 1.30 이상과 일 3회 이상 전 패키지 금지) |
| pf_lift_variants_reduce_density(PF 상승 변형이 밀도 감소) | stress4_short050_pf_lift | PF 1.3066 but density 2.6727(PF 1.3066이나 밀도 2.6727) | PF lift(PF 상승)는 density bridge(밀도 연결)와 함께 시험한다. |

## Next queue(다음 대기열)

| queue_id | seed_variant_id | hypothesis(가설) | required_control(필수 대조) |
| --- | --- | --- | --- |
| short_quality_plus_density_restore(숏 품질 + 밀도 복원) | stress3_restore_non_hour16_margin_0_1__ps0_45__adx40_0__hold8 | raise short quality toward PF>=1.30 while restoring only timestamp-safe high-margin trades to keep density>=3/day(숏 품질을 올려 PF 1.30에 접근하면서 시점 안전 고마진 거래만 복원해 밀도 3 이상을 유지한다) | run364AD selected, stress4_short050_pf_lift, baseline replay(364AD 선택, stress4_short050, 기준 재생) |
| margin_band_pf_lift(마진 구간 PF 상승) | stress3_restore_non_hour16_margin_0_1__ps0_45__adx40_0__hold8 | filter low-margin March restored trades and preserve the non-hour16 density bridge(저마진 3월 복원 거래를 거르고 non-hour16 밀도 연결을 보존한다) | no top_n replay(top_n 재생 금지); fixed threshold only(고정 임계값만 사용) |

## Gate audit(게이트 감사)

| gate(게이트) | status | evidence(근거) | effect(효과) |
| --- | --- | --- | --- |
| scope_completion_gate(범위 완료 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AE/final_decision.json | run364AE review(364AE 검토)를 닫는다. |
| input_parent_gate(부모 입력 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AE/input_manifest.csv | run364AD 산출물과 gate(게이트)를 확인한다. |
| surface_review_gate(표면 검토 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AE/surface_review.csv | 13개 scout row(정찰 행)를 판정한다. |
| package_boundary_gate(패키지 경계 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AE/package_gate_audit.csv | PF 목표 미달로 package(패키지)를 열지 않는다. |
| performance_attribution_gate(성과 귀속 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AE/performance_attribution_receipt.json | PF/density/DD(수익 팩터/밀도/낙폭) 변화를 귀속한다. |
| next_queue_gate(다음 대기열 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AE/run364AF_pf_lift_density_safe_queue.csv | run364AF queue(364AF 대기열)를 만든다. |
| artifact_lineage_audit(산출물 계보 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AE/artifact_lineage_receipt.json | 입력/출력 hash(해시)를 연결한다. |
| claim_boundary_audit(주장 경계 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AE/claim_boundary_receipt.json | runtime authority(런타임 권위)를 열지 않는다. |
| required_gate_coverage_audit(필수 게이트 커버리지 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AE/required_gate_coverage_audit.csv | 필수 gate(게이트)를 closeout(종료 기록)에 연결한다. |

## Claim boundary(주장 경계)

`research_development_proxy_review_only_no_new_model_training_no_new_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

Effect(효과): 이 review(검토)는 package(패키지), MT5 runtime probe(MT5 런타임 탐침), operating promotion(운영 승격)을 열지 않고, PF lift(PF 상승)와 density safety(밀도 안전)를 다음 탐색으로 넘긴다.
