# Stage364P drawdown side-balance offensive inputs(364P단계 낙폭 방향 균형 공격 입력)

## Current truth(현재 진실)

- run_id(실행 ID): `run364P_materialize_drawdown_side_balance_offensive_inputs_without_db_v1`
- parent_run_id(부모 실행 ID): `run364O_review_density_lift_trade_shape_onnx_mt5_runtime_probe_without_db_v1`
- next_run_id(다음 실행 ID): `run364Q_train_drawdown_side_balance_overlay_onnx_scout_without_db_v1`
- judgment(판정): `offensive_inputs_ready_for_risk_overlay_and_side_balance_scout_no_kpi_claim_no_authority`
- claim_boundary(주장 경계): `research_development_input_materialization_only_no_new_model_training_no_new_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

## Materialized artifacts(구체화 산출물)

- trade lifecycle joined(거래 생명주기 결합): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364P/trade_lifecycle_joined.csv`
- risk overlay training table(위험 오버레이 학습 표): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364P/risk_overlay_training_table.csv`
- calendar hold tail labels(달력 보유 꼬리 라벨): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364P/calendar_hold_tail_labels.csv`
- drawdown tail entry labels(낙폭 꼬리 진입 라벨): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364P/drawdown_tail_entry_labels.csv`
- short-side probability scout(숏 방향 확률 탐색): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364P/short_side_probability_scout.csv`
- session/regime slices(세션/국면 구간): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364P/session_regime_slice_inputs.csv`
- run364Q queue(364Q 실행 대기열): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364P/run364Q_training_queue.csv`

## Readout(판독)

- actual/expected trades(실제/예상 거래): `1047/1047`
- feature rows(피처 행): `17428`
- feature count(피처 수): `58`
- risk overlay rows(위험 오버레이 행): `1047`
- avoid candidate rate(회피 후보 비율): `0.488061`
- tail loss >= 10 rate(10 이상 꼬리 손실 비율): `0.08978`
- hold tail > 96 M5 rate(96개 M5봉 초과 보유 꼬리 비율): `0.079274`
- short scout rows(숏 탐색 행): `3486`

## Data integrity(데이터 무결성)

feature(피처)는 expected entry bar(예상 진입 봉)의 닫힌 봉 값만 쓴다. label(라벨)은 이후 MT5 close(청산) 결과에서 온다. 효과(effect, 효과)는 training(학습)에서 post-trade label(거래 후 라벨)을 feature(피처)로 섞는 미래참조(look-ahead, 미래참조)를 막는 것이다.

## Next action(다음 행동)

`run364Q_train_drawdown_side_balance_overlay_onnx_scout_without_db_v1`에서 risk overlay classifier(위험 오버레이 분류기), calendar hold cap proxy(달력 보유 상한 프록시), short-side router scout(숏 방향 라우터 탐색)를 학습/탐색한다.

Goal Achieve(목표 달성), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비)는 모두 `not_claimed`다.
