# 362_long_only_margin_grid__cost_buffer_first_branch

Stage362(362단계)는 Stage361A(361A 실행)의 q05 long-only margin grid(q05 롱 단독 마진 격자)를 먼저 구체화한다.

- opened_by_run_id(개설 실행 ID): `run362A_branch_stage361_to_long_only_margin_grid_without_db_v1`
- next_run_id(다음 실행 ID): `run362B_materialize_q05_long_only_margin_grid_without_db_v1`
- source_queue(원천 대기열): `stages/361_long_only_cost_buffer__validation_oos_positive_cost_failure/02_runs/run361A/run361B_materialization_queue.csv`
- source_margin_grid(원천 마진 격자): `stages/361_long_only_cost_buffer__validation_oos_positive_cost_failure/02_runs/run361A/margin_grid_plan.csv`

Action(행동): Stage361B(361B 실행)의 무거운 materialization bundle(구체화 묶음)을 Stage362(362단계)로 나눴다.

Effect(효과): 다음 재진입은 margin grid(마진 격자) 하나만 실행하면 된다.
