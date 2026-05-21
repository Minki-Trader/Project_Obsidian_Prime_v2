# Stage267 run267BN Aggressive Second Tranche Cross-period Materialization(267단계 267BN 공격형 2차 묶음 확장 기간 물질화)

## Summary(요약)

- run_id(실행 ID): `run267BN_stage267_aggressive_second_tranche_cross_period_materialization_v1`
- parent_run(상위 실행): `run267BM_stage267_aggressive_pressure_second_tranche_or_cross_period_validation_design_v1`
- source_first_tranche(첫 공격형 묶음 원천): `run267BJ_stage267_aggressive_pressure_first_tranche_materialization_v1`
- status(상태): `run267BN_aggressive_second_tranche_cross_period_materialized_execution_pending`
- queue_rows(큐 행): `6`
- materialized_attempts(물질화 시도): `4`
- blocked_or_audit_rows(차단/감사 행): `2`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준선): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Action(행동): run267BM(267BM 실행)의 direct/control MT5 attempt ready(직접/대조 MT5 시도 준비) 행 4개를 feature/model/set/ini(피처/모델/설정/초기화) 입력으로 만들었다.
Effect(효과): run267BO(267BO 실행)에서 anti_overconstraint_prune(과제약 제거)과 state_acceleration_interaction(상태 가속 상호작용)이 2024년 밖에서도 덜 깨지는지 실행할 수 있다.

이번 실행은 성과 판정이 아니다.
Effect(효과): baseline candidate(기준 후보)를 바로 고르지 않고, 기간을 바꾸면 무너지는지 볼 준비만 끝냈다.

## Queue Decision(큐 판단)

| queue(큐) | variant(변형) | period(기간) | decision(판단) |
| --- | --- | --- | --- |
| `run267BM_01_s264_aih_anti_overconstraint_2023h2` | `anti_overconstraint_prune` | `2023H2` | `materialized_execution_pending` |
| `run267BM_02_s264_aih_anti_overconstraint_2025h1` | `anti_overconstraint_prune` | `2025H1` | `materialized_execution_pending` |
| `run267BM_03_s264_aih_anti_overconstraint_2025h2` | `anti_overconstraint_prune` | `2025H2` | `materialized_execution_pending` |
| `run267BM_04_s264_aih_anti_overconstraint_similar_replacement` | `anti_overconstraint_prune` | `2024` | `blocked_source_surface_needed_before_mt5` |
| `run267BM_05_s264_aih_state_acceleration_cross_period_control` | `state_acceleration_interaction` | `2025H1` | `materialized_execution_pending` |
| `run267BM_06_s264_aih_explode_opportunity_hole_audit` | `explode_opportunity_recall` | `2024` | `audit_only_not_materialized` |

## Period Availability(기간 가용성)

| period(기간) | role(역할) | rows(행) | first(첫 시각) | last(마지막 시각) | status(상태) |
| --- | --- | ---: | --- | --- | --- |
| `adjacent_2023_h2_train_pre_2024` | `pre_2024_train_context` | 6090 | `2023-07-05T16:40:00Z` | `2023-12-29T22:00:00Z` | `usable` |
| `adjacent_2025_h1_validation_post_2024` | `post_2024_validation_context` | 6867 | `2025-01-02T16:35:00Z` | `2025-06-30T22:00:00Z` | `usable` |
| `adjacent_2025_h2_oos_followthrough` | `oos_followthrough_context` | 6486 | `2025-07-01T16:35:00Z` | `2025-12-31T22:00:00Z` | `usable` |

## Attempt Inputs(시도 입력)

| attempt(시도) | variant(변형) | period(기간) | rows(행) | feature hash(피처 해시) | status(상태) |
| --- | --- | --- | ---: | --- | --- |
| `run267bn_01_s264_aih_anti_overconstraint_prune_2023h2` | `anti_overconstraint_prune` | `2023H2` | 6090 | `129ce96a0e184682383602f54ff8edc3acd50fa26339a71c61328c13214c27cd` | `materialized_execution_pending` |
| `run267bn_02_s264_aih_anti_overconstraint_prune_2025h1` | `anti_overconstraint_prune` | `2025H1` | 6867 | `129ce96a0e184682383602f54ff8edc3acd50fa26339a71c61328c13214c27cd` | `materialized_execution_pending` |
| `run267bn_03_s264_aih_anti_overconstraint_prune_2025h2` | `anti_overconstraint_prune` | `2025H2` | 6486 | `129ce96a0e184682383602f54ff8edc3acd50fa26339a71c61328c13214c27cd` | `materialized_execution_pending` |
| `run267bn_04_s264_aih_state_acceleration_interaction_2025h1` | `state_acceleration_interaction` | `2025H1` | 6867 | `c1ec777e6efa210b0f3af76692e8315f614b74cdf17912ecfa9103e30c54ea28` | `materialized_execution_pending` |

## Boundary(경계)

- MT5 execution(MT5 실행): `not_executed`, 다음 run267BO(267BO 실행)에서 확인한다.
- similar replacement(유사 대체): `blocked_source_surface_needed_before_mt5`, 원천 feature surface(피처 표면)가 먼저 필요하다.
- explode opportunity(기회 확장): `audit_only_not_materialized`, deep hole(깊은 구멍) 감사 전 추가 실행하지 않는다.
- Tier B fallback(Tier B 대체): `blocked`, true fallback manifest(진짜 대체 목록)가 아직 없다.
- Adapter(어댑터): 보류. cross-period MT5 KPI(확장 기간 MT5 핵심 성과 지표), trade list(거래 목록), balance/equity curve(잔액/평가금 곡선)를 본 뒤 판단한다.
- ONNX parity(ONNX 동등성): 금지. Goal gate(목표 게이트) 전에는 검토하지 않는다.
- next_action(다음 행동): `run267BO_execute_aggressive_second_tranche_cross_period_mt5`.

## Artifact Lineage(산출물 계보)

- source queue(원천 큐): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BM/aggressive_pressure_second_tranche_or_cross_period_validation_design/second_tranche_queue.csv`
- source first tranche attempt manifest(첫 묶음 시도 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BJ/aggressive_pressure_first_tranche_materialization/attempt_manifest.csv`
- feature manifest(피처 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BN/aggressive_second_tranche_cross_period_materialization/feature_frame_manifest.csv`
- attempt manifest(시도 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BN/aggressive_second_tranche_cross_period_materialization/attempt_manifest.csv`
- runtime contract(런타임 계약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BN/aggressive_second_tranche_cross_period_materialization/runtime_contract.csv`
