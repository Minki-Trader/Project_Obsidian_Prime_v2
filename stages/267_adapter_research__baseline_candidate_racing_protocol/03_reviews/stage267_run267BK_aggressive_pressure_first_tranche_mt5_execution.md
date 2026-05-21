# Stage267 run267BK Aggressive Pressure First Tranche MT5 Execution(공격형 압박 첫 묶음 MT5 실행)

## Summary(요약)

- run_id(실행 ID): `run267BK_stage267_aggressive_pressure_first_tranche_mt5_execution_v1`
- source_run(원천 실행): `run267BJ_stage267_aggressive_pressure_first_tranche_materialization_v1`
- status(상태): `run267BK_aggressive_pressure_first_tranche_mt5_batch_completed`
- attempts_executed(실행 시도): `4`
- kpi_records(KPI 기록): `4`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Action(행동): run267BJ(267BJ 실행)의 s264_aih(핵심 도전자) 공격형 4개 attempt(시도)를 MT5(MetaTrader 5, 메타트레이더5) Strategy Tester(전략 테스터)로 실행했다.
Effect(효과): 넓은 허용/손익 비대칭/상태 강조/과제약 제거가 실제 tester output(테스터 출력)과 KPI(핵심 성과 지표)로 이어지는지 확인한다.

## KPI Snapshot(KPI 요약)

| variant(변형) | net_profit(순수익) | PF(수익 팩터) | trades(거래 수) | max_DD%(최대 손실폭 %) |
| --- | ---: | ---: | ---: | ---: |
| `explode_opportunity_recall` | 9213.54 | 1.78 | 670 | 11.45 |
| `payoff_convexity_push` | 6021.35 | 1.52 | 336 | 27.99 |
| `state_acceleration_interaction` | 2128.47 | 1.61 | 409 | 11.47 |
| `anti_overconstraint_prune` | 6887.04 | 1.81 | 495 | 16.53 |

## Boundary(경계)

- 이 실행은 research racing(연구 경주) 실행이며 candidate selection(후보 선택)이 아니다.
- balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질) 검토 전에는 좋은 후보라고 말하지 않는다.
- ONNX parity(ONNX 동등성)나 ONNX conversion(ONNX 변환)은 시작하지 않는다.

## Artifacts(산출물)

- execution_result(실행 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BK/aggressive_pressure_first_tranche_mt5_execution/execution_result.json`
- kpi_summary(KPI 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BK/aggressive_pressure_first_tranche_mt5_execution/kpi_summary.csv`
- profile_encoding_receipt(프로필 인코딩 영수증): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BK/aggressive_pressure_first_tranche_mt5_execution/profile_encoding_receipt.csv`
- forensics(포렌식): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BK/aggressive_pressure_first_tranche_mt5_execution/backtest_forensics.csv`
- next_action(다음 행동): `run267BL_review_aggressive_pressure_first_tranche_balance_timeslice_trade_quality`
