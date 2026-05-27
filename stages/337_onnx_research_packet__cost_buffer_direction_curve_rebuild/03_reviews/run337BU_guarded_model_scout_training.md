# Stage337 run337BU Guarded Model Scout Training(방어 모델 스카우트 학습)

## Conclusion(결론)

run337BU(337BU 실행)는 run337BT(337BT 실행)의 guarded scout inputs(방어 스카우트 입력)를 실제 trained model scouts(학습된 모델 스카우트)와 ONNX(온엑스) 산출물로 바꿨다.

Effect(효과): technical-only(기술 전용), macro-lag(거시 지연), equity-stale(주식 낡음) 분기마다 logreg(로지스틱 회귀)와 ExtraTrees(엑스트라트리)를 학습했고, forward(전진) 구간은 diagnostic holdout(진단 홀드아웃)으로만 채점했다. MT5 runtime comparison(MT5 런타임 비교)은 다음 run337BV(337BV 실행) 필수 조건이다.

## Result(결과)

- status(상태): `completed_stage337BU_guarded_model_scouts_trained_proxy_expected_materialized_mt5_probe_queued_no_selection`
- judgment(판정): `python_and_onnx_scout_models_materialized_proxy_forward_diagnostics_ready_mt5_runtime_comparison_missing`
- decision(결정): `stage337BU_open_run337BV_model_scout_mt5_runtime_probe`
- next_action(다음 행동): `run337BV_execute_model_scout_mt5_runtime_probe_without_db_v1`
- gates(게이트): `11/11`
- trained_models(학습 모델): `6`
- onnx_parity_passed(온엑스 동등성 통과): `6/6`
- proxy_expected_rows(프록시 예상 행): `47320`

## Forward Diagnostic(전진 진단)

Primary fixed rule(주 고정 규칙): `fixed_short040_long040_margin002`. 이 표는 selection(선택)이 아니라 다음 MT5 probe(탐침) 우선순위와 위험 감지를 위한 진단이다.

| model(모델) | branch(분기) | trades(거래) | net log return(순 로그수익) | PF(수익 팩터) | DD(손실폭) |
|---|---|---:|---:|---:|---:|
| `logreg_balanced_c1` | `bt_technical42_low_stale_control` | 3325 | 0.031785 | 1.0126 | -0.282288 |
| `extratrees_depth6_leaf120` | `bt_technical42_low_stale_control` | 82 | -0.145597 | 0.2794 | -0.140529 |
| `logreg_balanced_c1` | `bt_macro48_macro_lag_ablation` | 3356 | 0.101175 | 1.0405 | -0.275308 |
| `extratrees_depth6_leaf120` | `bt_macro48_macro_lag_ablation` | 47 | -0.071829 | 0.3596 | -0.072044 |
| `logreg_balanced_c1` | `bt_core56_equity_stale_stress_not_primary` | 3144 | 0.002411 | 1.0010 | -0.284670 |
| `extratrees_depth6_leaf120` | `bt_core56_equity_stale_stress_not_primary` | 62 | -0.101149 | 0.3368 | -0.105610 |

## Boundary(경계)

- forward_selection(전진 선택): `not_run`
- threshold_tuning(임계값 조정): `not_run`
- candidate_selection(후보 선택): `not_run`
- MT5 runtime comparison(MT5 런타임 비교): `queued_not_completed`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Claim boundary(주장 경계): `research_development_only_stage337BU_guarded_model_scout_training_without_db_no_forward_selection_no_threshold_tuning_no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve`
