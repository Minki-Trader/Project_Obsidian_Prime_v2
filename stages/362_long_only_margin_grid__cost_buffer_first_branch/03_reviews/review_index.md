# Stage362 Review Index(362단계 검토 색인)

- `run362A_branch_stage361_to_long_only_margin_grid_without_db_v1`: `stages/362_long_only_margin_grid__cost_buffer_first_branch/03_reviews/run362A_stage_branch.md`. Action(행동): Stage361B(361B 실행)의 heavy materialization(무거운 구체화)을 Stage362 margin grid(362단계 마진 격자)로 분기. Effect(효과): next_run(다음 실행)을 `run362B_materialize_q05_long_only_margin_grid_without_db_v1`로 가볍게 재지정.

- `run362B_materialize_q05_long_only_margin_grid_without_db_v1`: `stages/362_long_only_margin_grid__cost_buffer_first_branch/03_reviews/run362B_q05_long_only_margin_grid_materialization.md`. Action(행동): q05 long-only margin grid(q05 롱 단독 마진 격자) 35행을 구체화. Effect(효과): passing_cross_split_rows(교차 분할 통과 행) `0`, next_run(다음 실행) `run362C_review_q05_long_only_margin_grid_without_db_v1`.
