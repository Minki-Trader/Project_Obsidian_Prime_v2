# Stage267 run267BH Aggressive Candidate Pressure Queue(공격형 후보 압박 큐)

## Summary(요약)

- run_id(실행 ID): `run267BH_stage267_aggressive_candidate_pressure_queue_v1`
- parent_run(상위 실행): `run267BG_stage267_adjacent_period_replacement_fresh_report_mt5_execution_v1`
- status(상태): `run267BH_aggressive_candidate_pressure_queue_materialized_execution_pending`
- queue_rows(큐 행): `20`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Action(행동): 다섯 Baseline candidates(기준 후보)를 aggressive pressure(공격형 압박) 축에 다시 올렸다.
Effect(효과): defensive filter stacking(방어 필터 덧붙이기)만 반복하지 않고, 넓은 permission(허용), payoff convexity(손익 비대칭), interaction feature(상호작용 피처), overconstraint prune(과제약 가지치기)을 실제 다음 실행 큐로 만든다.

## Queue Shape(큐 구조)

| variant(변형) | rows(행 수) | intent(의도) |
| --- | ---: | --- |
| `explode_opportunity_recall` | 5 | A wider permission surface can reveal a stronger raw edge before defensive filters hide it. |
| `payoff_convexity_push` | 5 | Some candidates may need asymmetric payoff expansion rather than more entry filtering. |
| `state_acceleration_interaction` | 5 | Explosive moves may be captured by interaction features rather than single ADX/ATR replacement. |
| `anti_overconstraint_prune` | 5 | Recent branches may be overconstrained by defensive repair habits; pruning filters can expose a better candidate family. |

## Boundary(경계)

- 이 큐는 materialization priority(물질화 우선순위)일 뿐 selected candidate(선택 후보)가 아니다.
- MT5(MetaTrader 5, 메타트레이더5) tester handoff(테스터 인계)가 막히면 invalid/blocked(무효/차단)로 기록하고 성능으로 해석하지 않는다.
- true fallback(실제 대체)과 actual routed total(실제 라우팅 전체)은 route manifest(라우트 목록)가 생기기 전까지 차단 상태다.
- 다음 실행은 한 번에 미세조정하지 않고, coarse aggressive tranche(거친 공격형 묶음)부터 본다.

## Artifacts(산출물)

- queue(큐): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BH/aggressive_candidate_pressure_queue/aggressive_experiment_queue.csv`
- design receipt(설계 영수증): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BH/aggressive_candidate_pressure_queue/experiment_design_receipt.csv`
- failure memory seed(실패 기억 씨앗): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BH/aggressive_candidate_pressure_queue/failure_memory_seed.csv`
- manifest(목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BH/aggressive_candidate_pressure_queue/run_manifest.json`
- lineage(계보): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BH/aggressive_candidate_pressure_queue/lineage.json`
- next_action(다음 행동): `run267BI_repair_tester_handoff_and_execute_aggressive_pressure_queue_tranche`
