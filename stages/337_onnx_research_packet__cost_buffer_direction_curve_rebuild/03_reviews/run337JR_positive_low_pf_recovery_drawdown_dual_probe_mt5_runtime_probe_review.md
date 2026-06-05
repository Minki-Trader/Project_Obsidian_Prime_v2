# run337JR MT5 Runtime Probe Review(run337JR MT5 런타임 탐침 검토)

## Summary(요약)

- run_id(실행 ID): `run337JR_review_runtime_positive_low_pf_recovery_drawdown_dual_probe_repair_mt5_runtime_probe_or_repair_without_db_v1`
- parent_run_id(부모 실행 ID): `run337JQ_execute_runtime_positive_low_pf_recovery_drawdown_dual_probe_repair_mt5_runtime_probe_without_db_v1`
- status(상태): `completed_stage337JR_positive_low_pf_recovery_drawdown_dual_probe_mt5_runtime_probe_review_negative_repair_design_required`
- judgment(판정): `valid_negative_mt5_runtime_probe_proxy_signal_parity_but_trade_lifecycle_unprofitable_no_selection`
- gates(게이트): `8/8`
- attempts(시도): `3`
- parity_ok(동등성 정상): `True`
- mismatch_rows(불일치 행): `0`
- best_model_id(가장 덜 나쁜 모델 ID): `jn_jl_jk006_cost_stress_buffer_extratrees`
- best_mt5_net_profit(가장 덜 나쁜 MT5 순수익): `-191.49`
- best_mt5_profit_factor(가장 덜 나쁜 MT5 수익 팩터): `0.92`
- best_mt5_recovery_factor(가장 덜 나쁜 MT5 회복 계수): `-0.58`
- best_mt5_drawdown(가장 덜 나쁜 MT5 낙폭): `330.36`

## Judgment(판정)

JQ의 3개 ONNX(온엑스) 후보는 모두 runtime parity(런타임 동등성)가 맞았지만 MT5 KPI(MT5 핵심 성과 지표)가 모두 음수다.
Effect(효과): 이 결과는 invalid(무효)가 아니라 valid negative(유효한 부정)이고, 후보 선택이 아니라 trade lifecycle repair(거래 생명주기 수리)로 넘긴다.

## Evidence(근거)

- scorecard(점수표): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337JR/jr_mt5_runtime_probe_review_scorecard.csv`
- attribution(귀속): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337JR/jr_proxy_mt5_attribution.csv`
- failure_memory(실패 기억): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337JR/jr_failure_memory_and_repair_constraints.csv`
- next_queue(다음 대기열): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337JR/run337JS_design_queue.csv`

## Boundary(경계)

Candidate selection(후보 선택), Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)는 없다.
