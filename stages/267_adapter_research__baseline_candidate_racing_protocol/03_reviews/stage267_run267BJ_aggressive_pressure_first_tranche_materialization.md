# Stage267 run267BJ Aggressive Pressure First Tranche Materialization(공격형 압박 첫 묶음 물질화)

## Summary(요약)

- run_id(실행 ID): `run267BJ_stage267_aggressive_pressure_first_tranche_materialization_v1`
- parent_run(상위 실행): `run267BH_stage267_aggressive_candidate_pressure_queue_v1`
- handoff_repair(인계 수리): `run267BI_stage267_tester_profile_nobom_handoff_repair_v1`
- status(상태): `run267BJ_aggressive_pressure_first_tranche_materialized_execution_pending`
- tranche_rows(묶음 행): `4`
- attempts(시도): `4`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Action(행동): run267BH(267BH 실행)의 s264_aih(핵심 도전자) 공격형 queue(대기열) 4개를 MT5(MetaTrader 5, 메타트레이더5) feature/model/set/ini(피처/모델/설정/초기화) 입력으로 만들었다.
Effect(효과): baseline candidate(기준 후보)를 고르는 일을 방어 필터 누적만으로 끌지 않고, 넓은 허용/손익 비대칭/상태 강조/과제약 제거를 바로 실행 가능한 형태로 바꾼다.

## Tranche(묶음)

| variant(변형) | source(원천) | materialization(물질화) |
| --- | --- | --- |
| `explode_opportunity_recall` | `abl_volatility_bandwidth` | `copy_source_score_table` / `loosen_thresholds_disable_side_and_block_filters` |
| `payoff_convexity_push` | `rep_volatility_atr` | `copy_source_score_table` / `expand_atr_payoff_shape_keep_entry_surface` |
| `state_acceleration_interaction` | `abl_trend_strength_direction` | `scale_trend_return_state_scores_as_interaction_proxy` / `slightly_widen_thresholds_keep_state_surface` |
| `anti_overconstraint_prune` | `rep_trend_strength_adx` | `copy_source_score_table` / `remove_side_and_block_guard_family_keep_risk_shape` |

## Boundary(경계)

- 이 실행은 materialization(물질화)이며 candidate selection(후보 선택)이 아니다.
- Tier B(티어 B)와 actual routed total(실제 라우팅 전체)은 true fallback manifest(진짜 대체 목록)가 생기기 전까지 차단한다.
- ONNX parity(ONNX 동등성)나 ONNX conversion(ONNX 변환)은 시작하지 않는다.

## Artifacts(산출물)

- tranche_queue(묶음 큐): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BJ/aggressive_pressure_first_tranche_materialization/first_tranche_queue.csv`
- variant_manifest(변형 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BJ/aggressive_pressure_first_tranche_materialization/variant_manifest.csv`
- attempt_manifest(시도 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BJ/aggressive_pressure_first_tranche_materialization/attempt_manifest.csv`
- runtime_contract(런타임 계약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BJ/aggressive_pressure_first_tranche_materialization/runtime_contract.csv`
- model_mutation_audit(모델 변경 감사): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BJ/aggressive_pressure_first_tranche_materialization/model_mutation_audit.csv`
- next_action(다음 행동): `run267BK_execute_aggressive_pressure_first_tranche_with_nobom_profiles`
