# 362_long_only_margin_grid__cost_buffer_first_branch

Stage362(362단계)는 Stage361A(361A 실행)의 q05 long-only margin grid(q05 롱 단독 마진 격자)를 먼저 구체화한다.

- opened_by_run_id(개설 실행 ID): `run362A_branch_stage361_to_long_only_margin_grid_without_db_v1`
- next_run_id(다음 실행 ID): `run362B_materialize_q05_long_only_margin_grid_without_db_v1`
- source_queue(원천 대기열): `stages/361_long_only_cost_buffer__validation_oos_positive_cost_failure/02_runs/run361A/run361B_materialization_queue.csv`
- source_margin_grid(원천 마진 격자): `stages/361_long_only_cost_buffer__validation_oos_positive_cost_failure/02_runs/run361A/margin_grid_plan.csv`

Action(행동): Stage361B(361B 실행)의 무거운 materialization bundle(구체화 묶음)을 Stage362(362단계)로 나눴다.

Effect(효과): 다음 재진입은 margin grid(마진 격자) 하나만 실행하면 된다.

## run362B Materialization Closeout(362B 구체화 종료)

- report(보고서): `stages/362_long_only_margin_grid__cost_buffer_first_branch/03_reviews/run362B_q05_long_only_margin_grid_materialization.md`
- final_decision(최종 결정): `stages/362_long_only_margin_grid__cost_buffer_first_branch/02_runs/run362B/final_decision.json`
- passing_cross_split_rows(교차 분할 통과 행): `0`
- next_run_id(다음 실행 ID): `run362C_review_q05_long_only_margin_grid_without_db_v1`

Action(행동): Stage362B(362B 실행)는 margin grid(마진 격자)를 구체화했다.

Effect(효과): 다음 재진입은 Stage362C review(362C 검토)에서 no-selection judgment(선택 없음 판정)와 다음 공격 씨앗을 결정한다.
