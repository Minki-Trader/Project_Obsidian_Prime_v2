# run347A Cash-Open Asymmetric Source Design(347A 현금장 비대칭 원천 설계)

## Result(결과)

- status(상태): `completed_stage347A_cash_open_asymmetric_source_design_ready_no_selection`
- judgment(판정): `asymmetric_long_short_source_design_ready_timestamp_safe_materialization_required_no_operating_claim`
- decision(결정): `stage347A_open_run347B_materialize_cash_open_asymmetric_source_inputs`
- next_run(다음 실행): `run347B_materialize_cash_open_asymmetric_source_inputs_without_db_v1`

Action(행동): Stage346(346단계)의 positive clue(긍정 단서)와 failure memory(실패 기억)를 asymmetric long/short source design(비대칭 롱/숏 원천 설계)으로 바꿨다.
Effect(효과): 다음 run347B(347B 실행)는 feature/label/proxy input(피처/라벨/프록시 입력)을 timestamp-safe(시점 안전)하게 물질화할 수 있다.

## Design Rows(설계 행)

- `a01_dual_logreg_side_heads(이중 로지스틱 방향 헤드)`
- `a02_tree_long_quality_short_carry(트리 롱 품질/숏 기여)`
- `a03_cash_open_regime_allocator(현금장 국면 배분기)`

## Guardrails(가드레일)

- single side-filter micro-tuning(단일 방향 필터 미세조정)을 중심 주제로 반복하지 않는다.
- proxy(프록시)는 MT5 KPI(MT5 핵심 성과 지표)를 대체하지 않는다.
- feature/label boundary(피처/라벨 경계)는 timestamp-safe(시점 안전)이어야 한다.

## Artifacts(산출물)

- design_matrix(설계 표): `stages/347_cash_open_asymmetric_source__long_short_head_design/02_runs/run347A/asymmetric_source_design_matrix.csv`
- feature_source_plan(피처 원천 계획): `stages/347_cash_open_asymmetric_source__long_short_head_design/02_runs/run347A/feature_source_plan.csv`
- label_head_plan(라벨 헤드 계획): `stages/347_cash_open_asymmetric_source__long_short_head_design/02_runs/run347A/label_head_plan.csv`
- model_family_plan(모델 계열 계획): `stages/347_cash_open_asymmetric_source__long_short_head_design/02_runs/run347A/model_family_plan.csv`
- run347B_queue(347B 대기열): `stages/347_cash_open_asymmetric_source__long_short_head_design/02_runs/run347A/run347B_materialization_queue.csv`

## Claim Boundary(주장 경계)

`research_development_design_only_cash_open_asymmetric_long_short_source_no_model_training_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`
