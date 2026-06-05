# Stage 345(345단계)

Stage345(345단계)는 cash-open long quality/short carry runtime probe(현금장 롱 품질/숏 기여 런타임 탐침)만 다룬다.

- current_run(현재 실행): `run345B_execute_cash_open_long_quality_short_carry_decomposition_mt5_probe_without_db_v1`
- branch_run(분기 실행): `run345A_branch_stage344_to_cash_open_long_quality_short_carry_runtime_probe_without_db_v1`
- source_package(원천 패키지): `run344N_materialize_cash_open_long_quality_short_carry_decomposition_package_without_db_v1`
- retargeted_queue(재지정 대기열): `stages/345_cash_open_decomposition__long_quality_short_carry_runtime_probe/02_runs/run345A/run345B_cash_open_long_quality_short_carry_mt5_probe_queue.csv`

Effect(효과): Stage344(344단계)의 탐색 단서(clue, 단서)는 보존하고, MT5 runtime evidence(MT5 런타임 근거)는 새 단계에서 분리해 본다.

## run345B Cash-Open Runtime MT5 Probe(345B 현금장 런타임 MT5 탐침)

- run_id(실행 ID): `run345B_execute_cash_open_long_quality_short_carry_decomposition_mt5_probe_without_db_v1`
- summary(요약): `stages/345_cash_open_decomposition__long_quality_short_carry_runtime_probe/02_runs/run345B/cash_open_long_quality_short_carry_mt5_probe_summary.csv`
- diff(차이): `stages/345_cash_open_decomposition__long_quality_short_carry_runtime_probe/02_runs/run345B/proxy_mt5_runtime_difference.csv`
- effect(효과): run345C review(검토)가 MT5 KPI(MT5 핵심 성과 지표)를 기준으로 판정하게 한다.
