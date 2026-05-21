# Stage267 Run267BX Aggressive Impulse Cross-Period MT5 Execution(267단계 267BX 공격형 임펄스 확장 기간 MT5 실행)

## Summary(요약)

- run_id(실행 ID): `run267BX_stage267_aggressive_impulse_dd_shape_cross_period_mt5_execution_v1`
- source_run(원천 실행): `run267BW_stage267_aggressive_impulse_dd_shape_cross_period_materialization_v1`
- status(상태): `run267BX_aggressive_impulse_dd_shape_cross_period_mt5_batch_completed`
- attempts_executed(실행 시도): `9`
- kpi_records(KPI 기록): `9`
- blocked_or_gap_attempts(차단 또는 공백 시도): `0`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Action(행동): run267BW(267BW 실행)의 상위 3개 관찰 후보 x 3개 기간, 총 9개 attempt(시도)를 MT5(MetaTrader 5, 메타트레이더5) Strategy Tester(전략 테스터)로 실행했다.
Effect(효과): aggressive impulse replacement(공격형 임펄스 대체)가 2023H2, 2025H1, 2025H2 기간 압박에서 실제 tester output(테스터 출력), runtime output(런타임 출력), KPI(핵심 성과 지표)로 이어지는지 확인한다.

## KPI Snapshot(KPI 요약)

| candidate(후보) | period(기간) | profile(프로필) | net_profit(순수익) | PF(수익 팩터) | trades(거래 수) | max_DD%(최대 손실폭 %) |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| `s258_stc` | `2023H2` | `aggressive_impulse_replacement` | 749.49 | 1.91 | 178 | 10.63 |
| `s258_stc` | `2025H1` | `aggressive_impulse_replacement` | 630.58 | 1.47 | 226 | 11.68 |
| `s258_stc` | `2025H2` | `aggressive_impulse_replacement` | 572.02 | 1.69 | 167 | 15.96 |
| `s264_aih` | `2023H2` | `aggressive_impulse_replacement` | 539.33 | 1.79 | 164 | 9.6 |
| `s264_aih` | `2025H1` | `aggressive_impulse_replacement` | 796.33 | 1.61 | 215 | 11.74 |
| `s264_aih` | `2025H2` | `aggressive_impulse_replacement` | 476.4 | 1.67 | 152 | 12.19 |
| `s264_aia` | `2023H2` | `aggressive_impulse_replacement` | 560.16 | 1.81 | 165 | 9.74 |
| `s264_aia` | `2025H1` | `aggressive_impulse_replacement` | 766.11 | 1.58 | 216 | 11.74 |
| `s264_aia` | `2025H2` | `aggressive_impulse_replacement` | 451.56 | 1.63 | 154 | 15.84 |

## Blocked / Gap Attempts(차단/공백 시도)

| attempt(시도) | candidate(후보) | period(기간) | tester(테스터) | runtime(런타임) | report(보고서) | note(메모) |
| --- | --- | --- | --- | --- | --- | --- |
| `none` |  |  |  |  |  |  |

## Evidence(근거)

- source attempt manifest(원천 시도 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BW/aggressive_impulse_dd_shape_cross_period_materialization/attempt_manifest.csv`
- execution result(실행 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BX/aggressive_impulse_dd_shape_cross_period_mt5_execution/execution_result.json`
- KPI records(KPI 기록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BX/aggressive_impulse_dd_shape_cross_period_mt5_execution/kpi_records.json`
- KPI summary(KPI 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BX/aggressive_impulse_dd_shape_cross_period_mt5_execution/kpi_summary.csv`
- backtest forensics(백테스트 포렌식): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BX/aggressive_impulse_dd_shape_cross_period_mt5_execution/backtest_forensics.csv`
- profile encoding receipt(프로필 인코딩 영수증): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BX/aggressive_impulse_dd_shape_cross_period_mt5_execution/profile_encoding_receipt.csv`
- runtime parity receipt(런타임 동등성 영수증): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BX/aggressive_impulse_dd_shape_cross_period_mt5_execution/runtime_parity_receipt.csv`
- lineage(계보): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BX/aggressive_impulse_dd_shape_cross_period_mt5_execution/lineage.json`

## Judgment Boundary(판정 경계)

- next_action(다음 행동): `run267BY_review_aggressive_impulse_dd_shape_cross_period_balance_timeslice_trade_quality`
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`
- 이 실행은 연구개발 경주(R&D racing, 연구개발 경주) 근거다.
- selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.
