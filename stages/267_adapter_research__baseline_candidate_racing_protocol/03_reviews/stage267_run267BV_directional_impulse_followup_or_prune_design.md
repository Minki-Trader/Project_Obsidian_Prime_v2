# Stage267 Run267BV Directional/Impulse Follow-up or Prune Design(267단계 267BV 방향/임펄스 후속/가지치기 설계)

## Summary(요약)

- run_id(실행 ID): `run267BV_stage267_directional_impulse_followup_or_prune_design_v1`
- parent_run(상위 실행): `run267BU_stage267_pool_wide_directional_impulse_followup_balance_timeslice_trade_quality_review_v1`
- status(상태): `run267BV_directional_impulse_followup_or_prune_design_completed`
- branch_decisions(분기 판단): `4`
- materialization_queue_rows(물질화 대기열 행): `11`
- aggressive_watchlist_rows(공격형 관찰 행): `5`
- negative_register_status(부정 결과 등록 상태): `registered`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Action(행동): run267BU(267BU 실행)의 profile summary(프로필 요약), candidate review(후보 검토), failure memory(실패 기억)를 받아 다음 실험 설계로 바꿨다.
Effect(효과): directional_asymmetry(방향 비대칭)는 독립 분기로 닫고, aggressive_impulse_replacement(공격형 임펄스 대체)는 방어 필터 덧붙이기가 아니라 cross-period/DD-shape pressure(확장 기간/손실폭 형태 압박)로 넘긴다.

## Profile Read(프로필 판독)

| profile(프로필) | positive(양수) | negative/PF broken(음수/PF 붕괴) | high DD(높은 손실폭) | net mean(순수익 평균) | read(판독) |
| --- | ---: | ---: | ---: | ---: | --- |
| `aggressive_impulse_replacement` | 5 | 0 | 5 | 82.89 | `salvage_as_aggressive_clue_not_selection(공격형 단서로 회수, 선택 아님)` |
| `directional_asymmetry` | 0 | 5 | 5 | -40.14 | `prune_as_standalone_profile(독립 프로필 가지치기)` |

## Branch Decisions(분기 판단)

| decision(판단) | label(라벨) | next_use(다음 사용) |
| --- | --- | --- |
| `bv_d01_prune_directional_asymmetry_standalone` | `prune_standalone_profile(독립 프로필 가지치기)` | side-pressure diagnostic(방향 압박 진단)으로만 보존한다. |
| `bv_d02_continue_aggressive_impulse_as_pressure_branch` | `continue_as_aggressive_clue_no_selection(공격형 단서로 지속, 선택 아님)` | DD-shape pressure(손실폭 형태 압박), cross-period(확장 기간), similar replacement(유사 대체) 설계로 넘긴다. |
| `bv_d03_top_three_pressure_watch` | `materialize_top_three_pressure_queue(상위 3개 압박 큐 물질화)` | run267BW(267BW 실행)에서 2023H2/2025H1/2025H2와 DD-shape diagnostic(손실폭 형태 진단)에 태운다. |
| `bv_d04_hold_controls_for_comparison` | `hold_as_controls(대조군으로 보류)` | 필요하면 run267BW의 compact control(소형 대조군) 또는 후속 review(검토)에서 비교 기준으로 사용한다. |

## Aggressive Watchlist(공격형 관찰 목록)

| rank(순위) | candidate(후보) | net(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭) | worst(최악 구간) | next_use(다음 사용) |
| ---: | --- | ---: | ---: | ---: | ---: | --- | --- |
| 1 | `s258_stc` | 105.26 | 1.05 | 378 | 40.04 | `month/2024-07` -173.99 | run267BW(267BW 실행) cross-period/DD-shape pressure(확장 기간/손실폭 형태 압박)에 포함 |
| 2 | `s264_aih` | 93.46 | 1.05 | 353 | 36.10 | `weekday/Monday` -142.26 | run267BW(267BW 실행) cross-period/DD-shape pressure(확장 기간/손실폭 형태 압박)에 포함 |
| 3 | `s264_aia` | 92.91 | 1.05 | 354 | 35.76 | `weekday/Monday` -141.28 | run267BW(267BW 실행) cross-period/DD-shape pressure(확장 기간/손실폭 형태 압박)에 포함 |
| 4 | `s264_lc` | 71.38 | 1.04 | 350 | 36.59 | `weekday/Monday` -151.93 | 대조군(control, 대조군)으로 보류 |
| 5 | `s262_lih` | 51.42 | 1.03 | 352 | 39.01 | `weekday/Monday` -148.53 | 대조군(control, 대조군)으로 보류 |

## Next Queue(다음 대기열)

| queue(대기열) | priority(우선순위) | workstream(작업 흐름) | candidate(후보) | period(기간) | purpose(목적) |
| --- | --- | --- | --- | --- | --- |
| `run267bw_q00_directional_asymmetry_prune_receipt` | `P0` | `prune_receipt` | `pool_wide` | `not_applicable` | 같은 독립 방향 비대칭 실행을 반복하지 않게 막는다. |
| `run267bw_q01_s258_stc_2023h2_aggressive_impulse_period_pressure` | `P0` | `aggressive_impulse_cross_period_pressure` | `s258_stc` | `2023H2` | top-three aggressive clue(상위 3개 공격형 단서)를 계속 밀지, 실패 기억으로 낮출지 결정한다. |
| `run267bw_q01_s258_stc_2025h1_aggressive_impulse_period_pressure` | `P0` | `aggressive_impulse_cross_period_pressure` | `s258_stc` | `2025H1` | top-three aggressive clue(상위 3개 공격형 단서)를 계속 밀지, 실패 기억으로 낮출지 결정한다. |
| `run267bw_q01_s258_stc_2025h2_aggressive_impulse_period_pressure` | `P0` | `aggressive_impulse_cross_period_pressure` | `s258_stc` | `2025H2` | top-three aggressive clue(상위 3개 공격형 단서)를 계속 밀지, 실패 기억으로 낮출지 결정한다. |
| `run267bw_q01_s264_aih_2023h2_aggressive_impulse_period_pressure` | `P0` | `aggressive_impulse_cross_period_pressure` | `s264_aih` | `2023H2` | top-three aggressive clue(상위 3개 공격형 단서)를 계속 밀지, 실패 기억으로 낮출지 결정한다. |
| `run267bw_q01_s264_aih_2025h1_aggressive_impulse_period_pressure` | `P0` | `aggressive_impulse_cross_period_pressure` | `s264_aih` | `2025H1` | top-three aggressive clue(상위 3개 공격형 단서)를 계속 밀지, 실패 기억으로 낮출지 결정한다. |
| `run267bw_q01_s264_aih_2025h2_aggressive_impulse_period_pressure` | `P0` | `aggressive_impulse_cross_period_pressure` | `s264_aih` | `2025H2` | top-three aggressive clue(상위 3개 공격형 단서)를 계속 밀지, 실패 기억으로 낮출지 결정한다. |
| `run267bw_q01_s264_aia_2023h2_aggressive_impulse_period_pressure` | `P0` | `aggressive_impulse_cross_period_pressure` | `s264_aia` | `2023H2` | top-three aggressive clue(상위 3개 공격형 단서)를 계속 밀지, 실패 기억으로 낮출지 결정한다. |
| `run267bw_q01_s264_aia_2025h1_aggressive_impulse_period_pressure` | `P0` | `aggressive_impulse_cross_period_pressure` | `s264_aia` | `2025H1` | top-three aggressive clue(상위 3개 공격형 단서)를 계속 밀지, 실패 기억으로 낮출지 결정한다. |
| `run267bw_q01_s264_aia_2025h2_aggressive_impulse_period_pressure` | `P0` | `aggressive_impulse_cross_period_pressure` | `s264_aia` | `2025H2` | top-three aggressive clue(상위 3개 공격형 단서)를 계속 밀지, 실패 기억으로 낮출지 결정한다. |
| `run267bw_q02_impulse_similar_replacement_design_probe` | `P1` | `similar_feature_replacement_probe` | `s258_stc,s264_aih,s264_aia` | `2024_then_extension` | feature engineering(피처 엔지니어링)을 단순 미세 튜닝이 아니라 구조 검증으로 확장한다. |

## Judgment(판정)

- directional_asymmetry(방향 비대칭)는 standalone branch(독립 분기)로 가지치기한다.
- aggressive_impulse_replacement(공격형 임펄스 대체)는 clue(단서)로만 유지하고, 선택 후보로 올리지 않는다.
- 다음은 run267BW(267BW 실행)에서 top-three aggressive watch(상위 3개 공격형 관찰 후보)를 2023H2/2025H1/2025H2와 DD-shape pressure(손실폭 형태 압박)에 태우는 것이다.
- ONNX conversion(ONNX 변환), ONNX parity(ONNX 동등성), runtime reproduction(런타임 재현)은 아직 진행하지 않는다.

## Artifacts(산출물)

- branch_decision_matrix(분기 판단 행렬): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BV/directional_impulse_followup_or_prune_design/branch_decision_matrix.csv`
- materialization_queue(물질화 대기열): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BV/directional_impulse_followup_or_prune_design/materialization_queue.csv`
- aggressive_candidate_watchlist(공격형 후보 관찰 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BV/directional_impulse_followup_or_prune_design/aggressive_candidate_watchlist.csv`
- failure_memory(실패 기억): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BV/directional_impulse_followup_or_prune_design/failure_memory.csv`
- experiment_design_receipt(실험 설계 영수증): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BV/directional_impulse_followup_or_prune_design/experiment_design_receipt.csv`
- result_judgment(결과 판정): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BV/directional_impulse_followup_or_prune_design/result_judgment.csv`
- next_action(다음 행동): `run267BW_materialize_aggressive_impulse_dd_shape_cross_period_queue`
