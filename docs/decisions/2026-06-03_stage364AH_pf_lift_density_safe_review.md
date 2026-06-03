# run364AH PF lift density-safe review(364AH PF 상승 밀도 안전 검토)

## Current Truth(현재 진실)

- run_id(실행 ID): `run364AH_review_pf_lift_density_safe_expansion_scout_without_db_v1`
- parent_run_id(부모 실행 ID): `run364AG_train_pf_lift_density_safe_expansion_scout_without_db_v1`
- next_run_id(다음 실행 ID): `run364AI_materialize_session_side_pf_lift_density_repair_inputs_without_db_v1`
- judgment(판정): `negative_for_package_positive_for_session_side_pf_lift_density_repair_no_authority`
- package_decision(패키지 결정): `no_package_pf_below_target_and_strict_pass_zero(패키지 없음, PF 목표 미달 및 엄격 통과 0)`
- selected net/PF/trades/density/expectancy/DD/RF(선택 순수익/수익 팩터/거래수/밀도/기대값/낙폭/회복 계수): `840.055` / `1.2739357721` / `1001` / `3.006006006` / `0.8392157842` / `-142.323` / `5.9024542765`
- package_candidate_rows(패키지 후보 행): `0`
- pf_pass_density_fail_rows(PF 통과 밀도 실패 행): `3`
- next_queue_rows(다음 대기열 행): `4`
- runtime_authority(런타임 권위): `not_claimed`

## Surface Review(표면 검토)

| queue_id | review_status | combined_net_profit | combined_profit_factor | combined_trade_per_business_day | combined_max_drawdown | combined_short_count |
| --- | --- | --- | --- | --- | --- | --- |
| selected_density_safe_control | density_safe_pf_near_target_seed(밀도 안전 PF 근접 씨앗) | 840.055 | 1.2739357721 | 3.006006006 | -142.323 | 119.0 |
| pfpass_short050_restore_short0475 | pf_pass_density_fail_repair_seed(PF 통과 밀도 실패 수리 씨앗) | 794.569 | 1.3021603444 | 2.6876876877 | -120.303 | 13.0 |
| pf_pass_density_fail_control | pf_pass_density_fail_repair_seed(PF 통과 밀도 실패 수리 씨앗) | 799.943 | 1.3066323163 | 2.6726726727 | -120.303 | 8.0 |
| pfpass_short050_restore_margin008 | pf_pass_density_fail_repair_seed(PF 통과 밀도 실패 수리 씨앗) | 799.943 | 1.3066323163 | 2.6726726727 | -120.303 | 8.0 |
| selected_short0455_restore_margin010 | reject_density_floor(밀도 하한 탈락) | 799.923 | 1.2639812133 | 2.963963964 | -133.361 | 105.0 |
| selected_short0460_restore_margin010 | reject_density_floor(밀도 하한 탈락) | 774.416 | 1.2598776815 | 2.9009009009 | -133.361 | 85.0 |
| selected_short0465_restore_margin008 | reject_density_floor(밀도 하한 탈락) | 672.228 | 1.2262896407 | 2.8708708709 | -125.956 | 74.0 |
| mixed_long041_adx35_short0475 | reject_density_floor(밀도 하한 탈락) | 620.121 | 1.2122481628 | 2.8108108108 | -122.656 | 50.0 |
| selected_short0475_restore_short0475 | reject_density_floor(밀도 하한 탈락) | 628.996 | 1.216407956 | 2.7987987988 | -122.656 | 50.0 |
| pfpass_short049_restore_margin010 | reject_density_floor(밀도 하한 탈락) | 754.681 | 1.2815511632 | 2.7087087087 | -120.303 | 20.0 |

## Package Gate Audit(패키지 게이트 감사)

| gate_id | status | observed | required | effect(효과) |
| --- | --- | --- | --- | --- |
| density_floor(밀도 하한) | passed | 3.006006006 | 3.0 | 선택 후보의 최소 거래 밀도를 확인한다. |
| profit_factor_target(PF 목표) | failed | 1.2739357721 | 1.3 | PF 목표 미달이면 패키지를 열지 않는다. |
| strict_package_rows(엄격 패키지 행) | failed | 0 | 1 | PF/밀도/분할/숏 노출 동시 통과가 없으면 MT5 패키지로 올리지 않는다. |
| external_runtime_evidence(외부 런타임 근거) | out_of_scope_by_claim(주장 범위 밖) | not_run(미실행) | MT5 runtime probe(MT5 런타임 탐침) | 이번 검토는 프록시 판정까지만 닫는다. |

## Session Side Review(세션 방향 검토)

| entry_session | side | review_status | segment_net_profit | segment_profit_factor | segment_trade_count | segment_trade_per_business_day |
| --- | --- | --- | --- | --- | --- | --- |
| us_cash_core(미국 현금장 핵심) | long | positive_pf_session_or_month(양수 PF 세션/월) | 622.482 | 1.316715265 | 715 | 2.1471471471 |
| us_cash_core(미국 현금장 핵심) | short | positive_pf_session_or_month(양수 PF 세션/월) | 102.921 | 1.3122669474 | 86 | 0.2613981763 |
| post_cash_late(현금장 후반) | long | too_sparse_watch(희소 관찰) | 80.77 | inf | 5 | 0.0246305419 |
| us_premarket_cash_open(미국 프리마켓/현금장 초반) | long | positive_but_pf_below_target(PF 목표 미만 양수) | 46.197 | 1.0737177544 | 162 | 0.4864864865 |
| us_premarket_cash_open(미국 프리마켓/현금장 초반) | short | loss_or_pf_drag(손실 또는 PF 끌림) | -12.315 | 0.9150191492 | 33 | 0.1044303797 |

## Month Side Review(월 방향 검토)

| entry_month | side | review_status | segment_net_profit | segment_profit_factor | segment_trade_count |
| --- | --- | --- | --- | --- | --- |
| 2025-04 | long | positive_pf_session_or_month(양수 PF 세션/월) | 175.964 | 1.435582488 | 87 |
| 2025-11 | long | positive_pf_session_or_month(양수 PF 세션/월) | 112.066 | 1.4471728981 | 59 |
| 2025-05 | long | positive_pf_session_or_month(양수 PF 세션/월) | 93.222 | 1.9164929805 | 59 |
| 2026-03 | long | positive_pf_session_or_month(양수 PF 세션/월) | 86.985 | 1.353705398 | 78 |
| 2025-06 | long | positive_pf_session_or_month(양수 PF 세션/월) | 85.534 | 1.7558611182 | 60 |
| 2025-10 | long | positive_pf_session_or_month(양수 PF 세션/월) | 73.454 | 1.4761978853 | 62 |
| 2026-02 | short | positive_pf_session_or_month(양수 PF 세션/월) | 60.988 | 2.8773047681 | 11 |
| 2026-01 | long | positive_pf_session_or_month(양수 PF 세션/월) | 52.2 | 1.3646015227 | 67 |

## Positive Clues(긍정 단서)

| clue_id | evidence | kpi_read | effect(효과) |
| --- | --- | --- | --- |
| density_safe_pf_near_target(밀도 안전 PF 근접) | selected_density_safe_control__ps0_45__floor0_0__hold8 | net=840.055; pf=1.2739357721; density=3.006006006; dd=-142.323 | 밀도를 깨지 않고 PF만 올리는 수리 방향을 유지한다. |
| pf_pass_density_fail_exists(PF 통과 밀도 실패 존재) | pfpass_short050_restore_short0475__ps0_5__floor0_0__hold8; pf_pass_density_fail_control__ps0_5__floor0_0__hold8 | pf=1.3021603444; density=2.6876876877; pf=1.3066323163; density=2.6726726727 | PF를 올리는 규칙은 있으나 밀도 복원 장치가 필요함을 보여준다. |
| us_cash_core_dual_side_positive(미국 현금장 핵심 양방향 양수) | long 622.482; short 102.921 | side=long; pf=1.316715265; trades=715; side=short; pf=1.3122669474; trades=86 | 세션 필터를 공격 탐색 씨앗으로 쓸 수 있다. |
| month_side_pockets_positive(월/방향 양수 포켓) | 2025-04 long; 2025-11 long | net=175.964; pf=1.435582488; trades=87; net=112.066; pf=1.4471728981; trades=59 | 월별 손실 구간을 모두 죽이지 않고 양수 포켓을 분리해 볼 수 있다. |

## Failure Memory(실패 기억)

| failure_id | evidence | kpi_read | constraint_for_next(다음 제약) |
| --- | --- | --- | --- |
| pf_below_target_blocks_package(PF 목표 미달 패키지 차단) | selected_density_safe_control__ps0_45__floor0_0__hold8 | pf=1.2739357721; target=1.3 | PF>=1.30 and density>=3/day before MT5 package(PF 1.30 이상과 일 3회 이상 밀도 전에는 MT5 패키지 금지) |
| pf_lift_breaks_density(PF 상승이 밀도 훼손) | pfpass_short050_restore_short0475; pf_pass_density_fail_control; pfpass_short050_restore_margin008 | pf=1.3021603444; density=2.6876876877; pf=1.3066323163; density=2.6726726727; pf=1.3066323163; density=2.6726726727 | PF 상승 규칙은 세션/방향 복원과 같은 작업 묶음에서 시험한다. |
| premarket_short_pf_drag(프리마켓 숏 PF 끌림) | us_premarket_cash_open(미국 프리마켓/현금장 초반) short | net=-12.315; pf=0.9150191492; trades=33 | 세션별 숏 허용 규칙을 분리하고, 손실 세션은 별도 대조군으로 둔다. |

## Next Queue(다음 대기열)

| queue_id | seed_variant_id | hypothesis(가설) | required_control(필수 대조) | forbidden(금지) |
| --- | --- | --- | --- | --- |
| core_session_dual_side_pf_lift(핵심 세션 양방향 PF 상승) | selected_density_safe_control__ps0_45__floor0_0__hold8 | us_cash_core long/short positive pocket(미국 현금장 핵심 롱/숏 양수 포켓)을 보존하고 premarket short drag(프리마켓 숏 끌림)을 차단하면 PF를 올리며 밀도 3/day를 지킬 수 있다. | run364AG selected control and full-session replay(364AG 선택 대조와 전체 세션 재생) | top_n, post-entry ranking, trade splitting(top_n, 진입 후 순위, 거래 쪼개기) |
| pf_pass_density_bridge_restore(PF 통과 밀도 연결 복원) | pfpass_short050_restore_short0475__ps0_5__floor0_0__hold8 | PF>=1.30 but density<3(PF 1.30 이상이나 밀도 3 미만) 씨앗에 core-session restore(핵심 세션 복원)를 붙이면 PF와 밀도를 동시에 맞출 수 있다. | pfpass_short050_restore_short0475 and pf_pass_density_fail_control(PF 통과 밀도 실패 대조) | trade count splitting(거래수 쪼개기) |
| validation_pf_repair_without_oos_overfit(검증 PF 수리와 표본외 과적합 방지) | selected_density_safe_control__ps0_45__floor0_0__hold8 | validation PF 1.2147(검증 PF 1.2147)이 약하고 OOS PF 1.3369(표본외 PF 1.3369)가 강하므로, 검증 손실 세그먼트를 줄이되 OOS 조건을 그대로 고정한다. | validation/OOS split separate records(검증/표본외 분리 기록) | using OOS to choose final operating threshold(표본외로 운영 임계값 선택) |
| premarket_short_block_control(프리마켓 숏 차단 대조) | selected_density_safe_control__ps0_45__floor0_0__hold8 | premarket short net -12.315 and PF 0.915(프리마켓 숏 순수익 -12.315, PF 0.915)를 차단하면 PF 손상을 줄일 수 있다. | same long rules, short session block only(같은 롱 규칙, 숏 세션 차단만 변경) | long-side hidden filter(롱 방향 숨은 필터) |

## Gate Audit(게이트 감사)

| gate(게이트) | status | evidence(근거) | effect(효과) |
| --- | --- | --- | --- |
| scope_completion_gate(범위 완료 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AH/final_decision.json | run364AH proxy review(364AH 프록시 검토)를 닫음 |
| input_parent_gate(부모 입력 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AH/input_manifest.csv | run364AG 산출물과 review queue(검토 대기열)를 확인함 |
| kpi_contract_audit(KPI 계약 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AH/surface_review.csv | PF/밀도/낙폭/거래수/방향 지표를 검토함 |
| row_grain_audit(행 단위 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AH/surface_review.csv | surface row(표면 행) 12개와 review queue(검토 대기열) 1개를 분리함 |
| source_authority_audit(원천 권위 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AH/data_integrity_receipt.json | 부모 run364AG(실행364AG)를 원천으로 고정함 |
| package_boundary_gate(패키지 경계 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AH/package_gate_audit.csv | PF 목표 미달과 엄격 통과 0개로 패키지를 차단함 |
| performance_attribution_gate(성과 귀속 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AH/performance_attribution_receipt.json | 세션/방향/PF-밀도 맞교환 원인을 기록함 |
| next_queue_gate(다음 대기열 게이트) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AH/run364AI_session_side_pf_lift_density_repair_queue.csv | run364AI(실행364AI) 수리 입력을 만듦 |
| artifact_lineage_audit(산출물 계보 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AH/artifact_lineage_receipt.json | 입력/출력 해시를 연결함 |
| claim_boundary_audit(주장 경계 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AH/claim_boundary_receipt.json | 런타임 권위와 운영 승격을 주장하지 않음 |
| required_gate_coverage_audit(필수 게이트 커버리지 감사) | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364AH/required_gate_coverage_audit.csv | 필수 게이트를 종료 기록에 연결함 |

## Claim Boundary(주장 경계)

`research_development_proxy_review_only_no_new_model_training_no_new_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

Effect(효과): 이 review(검토)는 package(패키지), MT5 runtime authority(MT5 런타임 권위), operating promotion(운영 승격)을 열지 않고, run364AI(실행364AI) 수리 입력만 연다.
