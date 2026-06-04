# run364CB review bx03 guard stack runtime probe(364CB BX3 가드 묶음 런타임 탐침 리뷰)

## Result(결과)

Action(행동): CA runtime probe(CA 런타임 탐침) 4개와 prior BX3(이전 BX3)를 trade membership(거래 구성), swap/gross/net(스왑/총손익/순수익), source/month/session(원천/월/세션), set parameter(설정 파라미터), Common Files hash(Common Files 해시)로 review(리뷰)했다.

Effect(효과): CA01은 BX3와 거래 경로가 완전히 같고 gross profit(총손익)도 같지만, swap(스왑)이 `-10.69` 바뀌어 net(순수익)이 `-10.69` 낮아졌음을 분리했다.

- status(상태): `completed_stage364CB_ca_runtime_probe_reviewed_swap_cost_drift_open_cc_no_authority`
- judgment(판정): `runtime_probe_review_usable_with_boundary_ca01_best_positive_vs_bv_but_swap_sensitive_below_bx3_no_authority`
- best variant(최선 변형): `ca01_bx03_semantics_control`
- CA best MT5 net/PF/trades/density(최선 MT5 순수익/수익 팩터/거래수/밀도): `997.49` / `1.4` / `1008` / `3.2101910828`
- CA01 vs BX3 common trades(공통 거래): `1008`
- CA01 vs BX3 gross/swap/net delta(총손익/스왑/순수익 차이): `0.0` / `-10.69` / `-10.69`
- CA01 vs CA06 overlay delta(오버레이 차이): `41.09`

## CA Scoreboard(CA 점수판)

| variant_id | net_profit | profit_factor | trade_count | trade_density_per_feature_business_day | recovery_factor | equity_drawdown_amount | net_diff_vs_bx3 | parsed_swap |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ca01_bx03_semantics_control | 997.49 | 1.4 | 1008 | 3.2101910828 | 7.67 | 130.11 | -10.69 | -5.14 |
| ca03_december_h21_h23_long_block_stress | 997.49 | 1.4 | 1008 | 3.2101910828 | 7.67 | 130.11 | -10.69 | -5.14 |
| ca02_december_h22_only_long_block_isolation | 989.62 | 1.39 | 1012 | 3.2229299363 | 7.61 | 130.11 | -18.56 | -5.26 |
| ca06_native_short_same_calendar_control | 956.4 | 1.38 | 1002 | 3.1910828025 | 7.35 | 130.11 | -51.78 | -5.14 |

## Source Attribution(원천 귀속)

| source_bucket | trade_count | net_profit | gross_profit | swap | expectancy |
| --- | --- | --- | --- | --- | --- |
| long_threshold | 903 | 871.13 | 874.67 | -3.54 | 0.964707 |
| native_short_threshold | 66 | 57.17 | 58.77 | -1.6 | 0.866212 |
| synthetic_short_overlay | 39 | 69.19 | 69.19 | 0.0 | 1.774103 |

## Pair Deltas(쌍 차이)

| pair_id | net_delta_left_minus_right | gross_delta_common_left_minus_right | swap_delta_common_left_minus_right | left_only_count | right_only_count | interpretation |
| --- | --- | --- | --- | --- | --- | --- |
| ca01_vs_bx3_reproducibility_control | -10.69 | 0.0 | -10.69 | 0 | 0 | same_trade_path_same_gross_swap_cost_drift(거래 경로와 총손익은 같고 스왑 비용만 흔들림) |
| ca03_vs_ca01_h23_stress_increment | 0.0 | 0.0 | 0.0 | 0 | 0 | no_incremental_h23_trade_effect(h23 확장 추가 거래 효과 없음) |
| ca02_vs_ca01_h22_only_isolation | -7.87 | 0.0 | 0.0 | 4 | 0 | h21_unblocked_longs_added_and_hurt_net(h21 차단 해제 롱이 추가되어 순수익 훼손) |
| ca01_vs_ca06_synthetic_overlay_value | 41.09 | 0.0 | 0.0 | 13 | 7 | h17_synthetic_overlay_remains_positive_vs_native_short_control(17시 합성 숏 오버레이가 기본 숏 대조보다 우세) |

## Swap Reconciliation(스왑 대조)

| close_month_ca01 | trade_count | net_diff_ca01_minus_bx3 | gross_diff_ca01_minus_bx3 | swap_diff_ca01_minus_bx3 |
| --- | --- | --- | --- | --- |
| 2025-01 | 87 | -1.47 | 0.0 | -1.47 |
| 2025-02 | 74 | 0.86 | 0.0 | 0.86 |
| 2025-03 | 9 | -0.63 | 0.0 | -0.63 |
| 2025-04 | 119 | -1.26 | 0.0 | -1.26 |
| 2025-05 | 75 | -1.89 | 0.0 | -1.89 |
| 2025-06 | 68 | -1.05 | 0.0 | -1.05 |
| 2025-07 | 35 | -0.42 | 0.0 | -0.42 |
| 2025-08 | 47 | -0.42 | 0.0 | -0.42 |

## Next Queue(다음 대기열)

| queue_id | action | priority | success_condition |
| --- | --- | --- | --- |
| cc01_same_session_bx3_ca01_swap_reprobe | same-session MT5 reprobe(동일 세션 MT5 재탐침) | 1 | same trade path and swap/net delta near zero(동일 거래 경로와 스왑/순수익 차이 0 근처) |
| cc02_swap_neutral_gross_score_review | swap-neutral scoring materialization(스왑 중립 점수 구체화) | 2 | preserve gross/net/cost layers separately(총손익/순수익/비용 층 분리 보존) |
| cc03_keep_h21_h22_block_reject_h22_only_isolation | calendar guard constraint(캘린더 가드 제약) | 3 | keep BX3 21-23 semantics until stronger contrary evidence(BX3 21-23 의미를 반대 근거 전까지 유지) |
| cc04_preserve_h17_synthetic_overlay_seed | offensive source guard seed(공격적 원천 가드 씨앗) | 4 | test new source guard without removing h17 synthetic clue(17시 합성 단서를 제거하지 않고 새 원천 가드 시험) |

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| kpi_contract_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CB/kpi_contract_audit.csv | KPI(핵심 성과 지표)를 deal table(거래 표)과 대조했다. |
| row_grain_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CB/row_grain_audit.csv | closed trade(종료 거래) 행 단위를 고정했다. |
| source_authority_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CB/source_authority_audit.csv | MT5 report(보고서)와 telemetry(기록)의 권위를 분리했다. |
| runtime_parity_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CB/runtime_parity_audit.csv | CA/BX 런타임 의미와 비용 차이를 분리했다. |
| backtest_forensics_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CB/backtest_forensics_audit.csv | 테스터 정체성과 비용 드리프트를 기록했다. |
| performance_attribution_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CB/performance_attribution_receipt.json | 수익 변화의 원인을 source/month/session/cost로 나눴다. |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CB/required_gate_coverage_audit.csv | 필수 gate(게이트)를 closeout(종료 기록)에 연결했다. |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CB/claim_boundary_receipt.json | 운영 승격과 런타임 권위를 주장하지 않는다. |

## Boundary(경계)

runtime probe review(런타임 탐침 리뷰)만 주장한다. runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)이다.
