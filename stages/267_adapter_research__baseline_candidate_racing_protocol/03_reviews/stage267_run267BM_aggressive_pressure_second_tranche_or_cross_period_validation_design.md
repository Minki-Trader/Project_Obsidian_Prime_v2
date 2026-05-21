# Stage267 run267BM Aggressive Pressure Second Tranche / Cross-Period Validation Design(267단계 267BM 공격형 압박 2차 묶음 / 확장 기간 검증 설계)

- action(행동): run267BL(267BL 실행)의 first tranche review(첫 묶음 검토)를 바탕으로 `6`개 second tranche queue(2차 묶음 큐)를 만들었다.
- effect(효과): anti_overconstraint_prune(과제약 제거)을 바로 고르지 않고 2023H2/2025H1/2025H2, similar replacement(유사 대체), interaction control(상호작용 대조)로 다시 부순다.
- status(상태): `run267BM_aggressive_pressure_second_tranche_or_cross_period_validation_design_completed`
- judgment(판정): `experiment_design_completed_no_candidate_selection`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준선): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

`anti_overconstraint_prune`은 지금 가장 볼 만하다. 하지만 이건 2024 한 구간에서 나온 관찰이다.
Effect(효과): 바로 선택하지 않고 기간을 바꿔도 덜 깨지는지 확인한다. 깨지면 실패 기억으로 남기고, 버티면 다음 Adapter(어댑터) 설계 가치가 생긴다.

## Variant Decisions(변형 판단)

| priority(우선순위) | variant(변형) | net(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭) | worst slice(최악 구간) | decision(판단) |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| `P0` | `anti_overconstraint_prune` | 6887.04 | 1.81 | 495 | 16.53 | `session_report/session_07_12_report_time` -266.96 | `p0_cross_period_validate_no_selection(P0 확장 기간 검증, 선택 아님)` |
| `P1` | `state_acceleration_interaction` | 2128.47 | 1.61 | 409 | 11.47 | `weekday/Monday` -214.38 | `p1_interaction_replacement_watch_no_selection(P1 상호작용 대체 관찰, 선택 아님)` |
| `P2` | `explode_opportunity_recall` | 9213.54 | 1.78 | 670 | 11.45 | `session_report/session_07_12_report_time` -327.45 | `p2_salvage_only_due_deep_slice_hole(P2 회수 전용, 깊은 구간 구멍 때문)` |
| `P3` | `payoff_convexity_push` | 6021.35 | 1.52 | 336 | 27.99 | `weekday/Monday` -755.76 | `p3_prune_for_now_due_dd_and_month_hole(P3 일단 가지치기, 손실폭과 월 구멍 때문)` |

## Second Tranche Queue(2차 묶음 큐)

| queue(큐) | priority(우선순위) | lane(경로) | period(기간) | source(원천) | purpose(목적) |
| --- | --- | --- | --- | --- | --- |
| `run267BM_01_s264_aih_anti_overconstraint_2023h2` | `P0` | `cross_period_validation(확장 기간 검증)` | `2023H2` | `anti_overconstraint_prune` | decide whether the P0 aggressive branch deserves broader materialization(P0 공격형 분기가 더 넓은 물질화 가치가 있는지 결정) |
| `run267BM_02_s264_aih_anti_overconstraint_2025h1` | `P0` | `cross_period_validation(확장 기간 검증)` | `2025H1` | `anti_overconstraint_prune` | test OOS carry-forward value without claiming readiness(준비 주장 없이 OOS 이월 가치 검정) |
| `run267BM_03_s264_aih_anti_overconstraint_2025h2` | `P0` | `cross_period_validation(확장 기간 검증)` | `2025H2` | `anti_overconstraint_prune` | test late-OOS fragility before adapter work(어댑터 작업 전 후반 OOS 취약성 검정) |
| `run267BM_04_s264_aih_anti_overconstraint_similar_replacement` | `P1` | `similar_feature_replacement(유사 피처 대체)` | `2024` | `anti_overconstraint_prune` | decide whether Adapter feature structure is worth designing(어댑터 피처 구조 설계 가치 판단) |
| `run267BM_05_s264_aih_state_acceleration_cross_period_control` | `P1` | `interaction_control_cross_period(상호작용 대조 확장 기간)` | `2025H1` | `state_acceleration_interaction` | control against P0 so the next step does not overfit one aggressive branch(P0 대조로 한 공격형 분기에 과적합하지 않게 함) |
| `run267BM_06_s264_aih_explode_opportunity_hole_audit` | `P2` | `weak_slice_hole_audit(약한 구간 구멍 감사)` | `2024` | `explode_opportunity_recall` | decide whether to salvage or prune explode_opportunity_recall(기회 회수 확장을 회수할지 가지칠지 결정) |

## Cross-Period Plan(확장 기간 계획)

| plan(계획) | period(기간) | success floor(성공 바닥) | failure floor(실패 바닥) |
| --- | --- | --- | --- |
| `cross_2023h2` | `2023H2` | PF>=1.45;DD<=20%;month_net_min>-350;trade_count>=250 | PF<1.20 or DD>25 or month/session deep loss(PF 1.20 미만 또는 DD 25 초과 또는 월/세션 깊은 손실) |
| `cross_2025h1` | `2025H1` | PF>=1.35;DD<=22%;trade_count>=160 | PF<1.10 or DD>27 or low-trade lucky spike(PF 1.10 미만 또는 DD 27 초과 또는 적은 거래 운) |
| `cross_2025h2` | `2025H2` | PF>=1.30;DD<=22%;trade_count>=100 | late segment net negative with deep slice(후반 순수익 음수와 깊은 구간 손실) |

## Boundary(경계)

- result_subject(결과 대상): `run267BM_aggressive_pressure_second_tranche_or_cross_period_validation_design`.
- evidence_available(사용 가능 근거): run267BL(267BL 실행) variant review(변형 검토), negative slice(음수 구간), curve diagnostics(곡선 진단), profile/runtime receipts(프로필/런타임 영수증).
- evidence_missing(빠진 근거): cross-period MT5 execution(확장 기간 MT5 실행), similar replacement execution(유사 대체 실행), Adapter structure(어댑터 구조), ONNX parity(ONNX 동등성).
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`.
- next_action(다음 행동): `run267BN_materialize_aggressive_second_tranche_cross_period_validation`.

## Artifacts(산출물)

- second_tranche_queue(2차 묶음 큐): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BM/aggressive_pressure_second_tranche_or_cross_period_validation_design/second_tranche_queue.csv`
- cross_period_plan(확장 기간 계획): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BM/aggressive_pressure_second_tranche_or_cross_period_validation_design/cross_period_validation_plan.csv`
- variant_decision_matrix(변형 판단 행렬): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BM/aggressive_pressure_second_tranche_or_cross_period_validation_design/variant_decision_matrix.csv`
- failure_memory(실패 기억): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BM/aggressive_pressure_second_tranche_or_cross_period_validation_design/failure_memory.csv`
- performance_attribution(성과 귀속): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BM/aggressive_pressure_second_tranche_or_cross_period_validation_design/performance_attribution.csv`
- lineage(계보): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BM/aggressive_pressure_second_tranche_or_cross_period_validation_design/lineage.json`
