# run347B Cash-Open Asymmetric Source Input Materialization(347B 현금장 비대칭 원천 입력 물질화)

## Result(결과)

- status(상태): `completed_stage347B_cash_open_asymmetric_source_inputs_materialized_proxy_training_ready_no_selection`
- judgment(판정): `timestamp_safe_teacher_source_inputs_materialized_for_proxy_training_tier_b_missing_no_operating_claim`
- decision(결정): `stage347B_open_run347C_train_cash_open_asymmetric_source_proxy_models`
- next_run(다음 실행): `run347C_train_cash_open_asymmetric_source_proxy_models_without_db_v1`

Action(행동): run344N runtime features(런타임 피처)와 expected tape(예상 테이프)를 결합해 asymmetric source input(비대칭 원천 입력)을 물질화했다.
Effect(효과): run347C(347C 실행)가 teacher/source labels(교사/원천 라벨)와 proxy grid(프록시 격자)로 학습/선별을 시작할 수 있다.

## Materialized Scope(물질화 범위)

- materialized_rows(물질화 행): `5827`
- first_bar_time(첫 봉 시각): `2024.07.30 18:35:00`
- last_bar_time(마지막 봉 시각): `2024.12.31 19:50:00`
- proxy_grid_rows(프록시 격자 행): `225`
- Tier B(티어 B): `missing_required(필수 누락)`

## Important Boundary(중요 경계)

The labels(라벨)은 realized PnL label(실현 손익 라벨)이 아니다. They are teacher/source labels(교사/원천 라벨) from n02 long-only and n03 short-only expected decisions(n02 롱 전용과 n03 숏 전용 예상 결정)이다.

## Artifacts(산출물)

- feature_label_table(피처/라벨 표): `stages/347_cash_open_asymmetric_source__long_short_head_design/02_runs/run347B/feature_label_source_table.csv`
- feature_schema_manifest(피처 스키마 목록): `stages/347_cash_open_asymmetric_source__long_short_head_design/02_runs/run347B/feature_schema_manifest.csv`
- label_source_manifest(라벨 원천 목록): `stages/347_cash_open_asymmetric_source__long_short_head_design/02_runs/run347B/teacher_label_manifest.csv`
- proxy_screen_grid(프록시 선별 격자): `stages/347_cash_open_asymmetric_source__long_short_head_design/02_runs/run347B/proxy_screen_grid.csv`
- handoff_index(인계 색인): `stages/347_cash_open_asymmetric_source__long_short_head_design/02_runs/run347B/handoff_index.csv`

## Claim Boundary(주장 경계)

`research_development_materialization_only_cash_open_asymmetric_source_teacher_labels_no_model_training_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`
