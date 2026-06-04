# run364BP short source quality repair review(364BP 숏 원천 품질 수리 검토)

## Current Truth(현재 진실)

- reviewed candidate(검토 후보): `bo00_bn_seed_h17_or_h20_margin_08_10_reference`
- reviewed KPI(검토 핵심 성과 지표): net/PF/density/short share(순수익/수익 팩터/밀도/숏비중) `1037.17` / `1.4101564709` / `3.0750750751` / `0.1201171875`
- month_bad_count(월 나쁨 수): `2`
- package decision(패키지 결정): `rejected_package_ineligible_month_stress_no_mt5(패키지 부적격 거절, 월 압박 및 MT5 없음)`
- next primary seed(다음 주 씨앗): `bo90_broad_h17_20_ps0440_margin080_control`

## Action And Effect(행동과 효과)

Action(행동): BO selected proxy(BO 선택 프록시)를 package gate(패키지 게이트), stress attribution(압박 귀속), proxy/MT5 diff(프록시/MT5 차이), next offensive seed(다음 공격 씨앗)으로 분리했다.

Effect(효과): package(패키지)는 거절하지만, `bo90` clean broad source(클린 넓은 원천), `bo91` overlap repair(겹침 수리), `bo05` high short-source PF(높은 숏 원천 PF)를 BQ scout(BQ 정찰)로 보존한다.

## Package Gate(패키지 게이트)

| gate_id | subject | status | reason | effect |
| --- | --- | --- | --- | --- |
| selected_bo_package_gate(선택 BO 패키지 게이트) | bo00_bn_seed_h17_or_h20_margin_08_10_reference | rejected_package_ineligible(패키지 부적격 거절) | month_bad_count=2; package_candidate_rows=0; new_mt5_execution=not_run | 프록시 단서를 MT5 package(MT5 패키지)로 바로 올리지 않는다. |
| bo05_high_source_pf_gate(bo05 높은 원천 PF 게이트) | bo05_h17_margin_075_105_or_h20_margin_08_10 | preserved_clue_not_package(보존 단서, 패키지 아님) | short_share=0.1111111111 < 0.12; synthetic_short_pf=2.8224308655 | 높은 숏 원천 품질을 BQ의 품질 하한 씨앗으로 쓴다. |
| bo90_broad_clean_gate(bo90 넓은 클린 게이트) | bo90_broad_h17_20_ps0440_margin080_control | preserved_clue_short_share_repair_required(보존 단서, 숏 비중 수리 필요) | net=1044.49; pf=1.4158388603; short_share=0.1102362205 < 0.12; overlap=0 | 넓은 풀에서 겹침 없는 양수 숏 원천을 다음 공격 수리로 넘긴다. |
| bo91_overlap_gate(bo91 겹침 게이트) | bo91_broad_h16_17_20_ps0445_margin080_control | rejected_overlap_but_repair_seed(겹침 거절, 수리 씨앗) | synthetic_overlap_count=8; short_share=0.1240310078 | h16 확장은 outcome(결과값)이 아니라 entry-known priority(진입기지 우선순위)로만 재시험한다. |

## Stress Failure Attribution(압박 실패 귀속)

| failure_id | failure_type | segment | net_profit | profit_factor | trade_count | repair_use |
| --- | --- | --- | --- | --- | --- | --- |
| stress_month(월)_2025-03 | combined_month_stress(합산 월 압박) | 2025-03 | -9.26 | 0.7656451654 | 14 | next run may test entry-known broad clean lift, not exact month removal(다음 실행은 정확 월 제거가 아니라 진입기지 넓은 클린 보강을 시험) |
| stress_month(월)_2025-12 | combined_month_stress(합산 월 압박) | 2025-12 | -9.76 | 0.9389408489 | 62 | next run may test entry-known broad clean lift, not exact month removal(다음 실행은 정확 월 제거가 아니라 진입기지 넓은 클린 보강을 시험) |
| short_source_entry_month(진입월)_2025-01 | synthetic_short_source_stress(합성 숏 원천 압박) | 2025-01 | 18.84 | 21.7717750827 | 3 | convert to quality constraint, not package promotion(품질 제약으로 쓰고 패키지 승격에는 쓰지 않음) |
| short_source_entry_month(진입월)_2025-03 | synthetic_short_source_stress(합성 숏 원천 압박) | 2025-03 | -12.4 | 0.5314542638 | 7 | convert to quality constraint, not package promotion(품질 제약으로 쓰고 패키지 승격에는 쓰지 않음) |
| short_source_entry_month(진입월)_2025-04 | synthetic_short_source_stress(합성 숏 원천 압박) | 2025-04 | -22.65 | 0.2061205174 | 3 | convert to quality constraint, not package promotion(품질 제약으로 쓰고 패키지 승격에는 쓰지 않음) |
| short_source_entry_month(진입월)_2025-08 | synthetic_short_source_stress(합성 숏 원천 압박) | 2025-08 | -7.67 | 0.5012360135 | 4 | convert to quality constraint, not package promotion(품질 제약으로 쓰고 패키지 승격에는 쓰지 않음) |
| short_source_entry_month(진입월)_2025-09 | synthetic_short_source_stress(합성 숏 원천 압박) | 2025-09 | 1.92 | 3.0338624339 | 2 | convert to quality constraint, not package promotion(품질 제약으로 쓰고 패키지 승격에는 쓰지 않음) |
| short_source_entry_month(진입월)_2025-12 | synthetic_short_source_stress(합성 숏 원천 압박) | 2025-12 | -10.07 | 0.452270873 | 2 | convert to quality constraint, not package promotion(품질 제약으로 쓰고 패키지 승격에는 쓰지 않음) |
| short_source_entry_month(진입월)_2026-01 | synthetic_short_source_stress(합성 숏 원천 압박) | 2026-01 | 4.47 | 1.5521927116 | 3 | convert to quality constraint, not package promotion(품질 제약으로 쓰고 패키지 승격에는 쓰지 않음) |
| short_source_entry_quarter(진입분기)_2025Q2 | synthetic_short_source_stress(합성 숏 원천 압박) | 2025Q2 | -27.58 | 0.1757322176 | 4 | convert to quality constraint, not package promotion(품질 제약으로 쓰고 패키지 승격에는 쓰지 않음) |
| short_source_entry_quarter(진입분기)_2025Q3 | synthetic_short_source_stress(합성 숏 원천 압박) | 2025Q3 | -8.6 | 0.5513716491 | 7 | convert to quality constraint, not package promotion(품질 제약으로 쓰고 패키지 승격에는 쓰지 않음) |
| short_source_entry_quarter(진입분기)_2025Q4 | synthetic_short_source_stress(합성 숏 원천 압박) | 2025Q4 | -6.49 | 0.6472667936 | 4 | convert to quality constraint, not package promotion(품질 제약으로 쓰고 패키지 승격에는 쓰지 않음) |

## Positive Clues(긍정 단서)

| clue_id | clue_type | net_profit | profit_factor | density | short_share | synthetic_short_profit_factor | usable_as |
| --- | --- | --- | --- | --- | --- | --- | --- |
| bo00_bn_seed_h17_or_h20_margin_08_10_reference | selected_proxy_clue(선택 프록시 단서) | 1037.17 | 1.4101564709 | 3.0750750751 | 0.1201171875 | 1.3816978038 | BP reviewed proxy clue(BP 검토 프록시 단서) |
| bo05_h17_margin_075_105_or_h20_margin_08_10 | high_short_source_pf_clue(높은 숏 원천 PF 단서) | 1026.66 | 1.4088361576 | 3.0540540541 | 0.1111111111 | 2.8224308655 | BQ offensive seed(BQ 공격 씨앗) |
| bo90_broad_h17_20_ps0440_margin080_control | broad_clean_source_clue(넓은 클린 원천 단서) | 1044.49 | 1.4158388603 | 3.0510510511 | 0.1102362205 | 1.7848439305 | BQ offensive seed(BQ 공격 씨앗) |
| bo91_broad_h16_17_20_ps0445_margin080_control | overlap_repair_clue(겹침 수리 단서) | 1067.36 | 1.4132149882 | 3.0990990991 | 0.1240310078 | 1.5601999121 | BQ offensive seed(BQ 공격 씨앗) |

## Proxy/MT5 Diff(프록시/MT5 차이)

| comparison_id | mt5_net_profit | proxy_net_profit | net_diff_proxy_minus_mt5 | mt5_profit_factor | proxy_profit_factor | usability |
| --- | --- | --- | --- | --- | --- | --- |
| bo_proxy_vs_bk_mt5_runtime_probe(BO 프록시 대 BK MT5 런타임 탐침) | 959.64 | 1037.17 | 77.53 | 1.3820937835 | 1.4101564709 | not_usable_for_authority_package_rejected(권위에 사용 불가, 패키지 거절) |

## BQ Queue(BQ 대기열)

| queue_rank | queue_id | seed_source | action | success_criteria |
| --- | --- | --- | --- | --- |
| 1 | bq01_broad_h17_20_clean_short_share_lift | bo90_broad_h17_20_ps0440_margin080_control | expand clean broad h17/h20 source while lifting short share(겹침 없는 넓은 17/20시 원천을 숏 비중 보강으로 확장) | PF>=1.35, density>=3, short_share>=0.12, synthetic_short_pf>=1.15, overlap=0(PF 1.35 이상, 밀도 3 이상, 숏비중 0.12 이상, 합성 숏 PF 1.15 이상, 겹침 0) |
| 2 | bq02_entry_known_overlap_safe_h16_extension | bo91_broad_h16_17_20_ps0445_margin080_control | retry h16 extension with entry-known p_short/margin priority only(16시 확장을 진입기지 p_short/마진 우선순위만으로 재시험) | no outcome-priority, no overlap, no top_n, no exact month(결과값 우선순위 없음, 겹침 없음, top_n 없음, 정확 월 없음) |
| 3 | bq03_high_short_source_pf_guardrail | bo05_h17_margin_075_105_or_h20_margin_08_10 | use bo05 high synthetic PF as quality guardrail(bo05 높은 합성 PF를 품질 가드레일로 사용) | short source PF remains high while share recovers(숏 원천 PF가 높은 상태에서 숏 비중 회복) |

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| kpi_contract_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BP/positive_clue_register.csv | net/PF/expectancy/DD/recovery/trades/short share를 분리 검토했다. |
| row_grain_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BP/stress_failure_attribution.csv | 패키지 게이트, 월 압박, 숏 원천 조각을 행 단위로 분리했다. |
| source_authority_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BP/proxy_mt5_diff_review.csv | proxy expected value(프록시 예상값)가 MT5 KPI(MT5 핵심 성과 지표)를 대체하지 않게 했다. |
| package_reject_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BP/package_gate_decision.csv | BO proxy(BO 프록시)를 패키지 후보에서 제외했다. |
| stress_memory_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BP/stress_failure_attribution.csv | 월별 실패를 다음 탐색 제약으로 바꿨다. |
| next_offensive_seed_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BP/run364BQ_broad_clean_short_share_lift_queue.csv | bo90/bo91/bo05 단서를 다음 BQ 공격 탐색으로 연결했다. |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BP/required_gate_coverage_audit.csv | 필수 게이트와 closeout(종료 기록)을 연결했다. |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BP/claim_boundary_receipt.json | runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)를 차단했다. |

## Boundary(경계)

BP is review only(BP는 검토 전용). No new model training(새 모델 학습 없음), no new MT5 execution(새 MT5 실행 없음), no forward pass(전진 통과 없음), no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음), no Goal Achieve(목표 달성 없음).
