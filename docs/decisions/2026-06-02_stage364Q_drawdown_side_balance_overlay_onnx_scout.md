# Stage364Q drawdown side-balance overlay ONNX scout(364Q단계 낙폭 방향 균형 오버레이 온엑스 탐색)

## Current truth(현재 진실)

- run_id(실행 ID): `run364Q_train_drawdown_side_balance_overlay_onnx_scout_without_db_v1`
- parent_run_id(부모 실행 ID): `run364P_materialize_drawdown_side_balance_offensive_inputs_without_db_v1`
- next_run_id(다음 실행 ID): `run364R_package_drawdown_side_balance_overlay_runtime_probe_without_db_v1`
- judgment(판정): `exploratory_mixed_proxy_no_mt5_execution_no_authority`
- claim_boundary(주장 경계): `research_development_overlay_onnx_training_and_proxy_scout_only_no_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`
- MT5 execution(MT5 실행): `not_run`
- runtime authority(런타임 권위): `not_claimed`

## Action/Effect(행동/효과)

Action(행동): run364P(364P 실행)의 risk overlay training table(위험 오버레이 학습 표), calendar hold labels(달력 보유 라벨), short probability tape(숏 확률 기록)를 사용해 ONNX(온엑스) risk overlay model(위험 오버레이 모델)과 proxy surface(프록시 표면)를 만들었다.

Effect(효과): run364O(364O 실행)의 positive MT5 clue(긍정 MT5 단서)를 drawdown/hold/side-balance(낙폭/보유/방향 균형) 수리 후보로 바꾸고, 다음 `run364R`에서 runtime probe package(런타임 탐침 패키지)로 넘길 후보를 좁혔다.

## Summary(요약)

- parent_oos_net(부모 표본외 순수익): `412.24`
- parent_oos_profit_factor(부모 표본외 수익 팩터): `1.3137839957`
- best_overlay_variant(최선 오버레이 변형): `risk_rf3_l30_n96__drop_top_40pct_risk`
- best_overlay_oos_net(최선 오버레이 표본외 순수익): `203.18`
- best_overlay_oos_profit_factor(최선 오버레이 표본외 수익 팩터): `1.2536579276`
- best_hold_variant(최선 보유 상한 변형): `hold_cap_96_m5_proxy`
- best_hold_oos_net(최선 보유 상한 표본외 순수익): `287.81`
- best_short_variant(최선 숏 변형): `short_q95_maxhold_12`
- best_short_oos_net(최선 숏 표본외 순수익): `212.955`
- ONNX smoke(온엑스 연기 검사): `2/2`

## Top risk overlay(상위 위험 오버레이)

| variant_id | model_id | drop_rate | validation_net | oos_net | oos_profit_factor | oos_max_drawdown | oos_trade_density |
| --- | --- | --- | --- | --- | --- | --- | --- |
| risk_rf3_l30_n96__drop_top_40pct_risk | risk_rf3_l30_n96 | 0.4 | 574.84 | 203.18 | 1.2536579276 | -87.44 | 2.4621848739 |
| risk_rf3_l30_n96__drop_top_30pct_risk | risk_rf3_l30_n96 | 0.3 | 526.47 | 272.09 | 1.2948398422 | -103.1 | 2.8925619835 |
| risk_rf3_l30_n96__drop_top_05pct_risk | risk_rf3_l30_n96 | 0.05 | 496.49 | 380.71 | 1.2993874004 | -96.28 | 3.488372093 |
| risk_rf3_l30_n96__drop_top_20pct_risk | risk_rf3_l30_n96 | 0.2 | 476.57 | 240.06 | 1.22931214 | -102.2 | 3.162601626 |
| risk_rf3_l30_n96__drop_top_10pct_risk | risk_rf3_l30_n96 | 0.1 | 457.46 | 319.43 | 1.2623374917 | -96.28 | 3.359375 |
| risk_rf3_l30_n96__drop_top_15pct_risk | risk_rf3_l30_n96 | 0.15 | 433.18 | 217.59 | 1.1877523902 | -129.93 | 3.2698412698 |

## Top hold cap proxy(상위 보유 상한 프록시)

| variant_id | cap_m5 | forced_exit_count | validation_net | oos_net | oos_profit_factor | oos_max_drawdown | oos_trade_density |
| --- | --- | --- | --- | --- | --- | --- | --- |
| hold_cap_96_m5_proxy | 96 | 83 | 431.35 | 287.81 | 1.2183901156 | -91.825 | 3.5968992248 |
| hold_cap_24_m5_proxy | 24 | 85 | 356.22 | 227.16 | 1.176900044 | -112.92 | 3.5968992248 |
| hold_cap_48_m5_proxy | 48 | 83 | 331.973 | 294.439 | 1.2264958942 | -110.68 | 3.5968992248 |
| hold_cap_12_m5_proxy | 12 | 124 | 285.703 | 178.857 | 1.1422344689 | -143.373 | 3.5968992248 |
| hold_cap_8_m5_proxy | 8 | 358 | 254.119 | 149.268 | 1.1216364548 | -136.886 | 3.5968992248 |

## Top short router proxy(상위 숏 라우터 프록시)

| variant_id | short_quantile | max_hold_m5 | validation_net | oos_net | oos_profit_factor | oos_trade_density |
| --- | --- | --- | --- | --- | --- | --- |
| short_q95_maxhold_12 | 0.95 | 12 | 89.069 | 212.955 | 1.5636816987 | 1.74 |
| short_q90_maxhold_12 | 0.9 | 12 | 58.283 | 164.226 | 1.2531823935 | 1.9868421053 |
| short_q95_maxhold_8 | 0.95 | 8 | -55.94 | 156.051 | 1.3636959004 | 2.0784313725 |
| short_q90_maxhold_24 | 0.9 | 24 | 40.556 | 132.781 | 1.2135951535 | 1.5333333333 |
| short_q90_maxhold_8 | 0.9 | 8 | -110.204 | 118.304 | 1.1882640509 | 2.3026315789 |
| short_q95_maxhold_24 | 0.95 | 24 | 163.867 | 111.371 | 1.2723746542 | 1.4285714286 |

## Evidence(근거)

- model_scorecard(모델 점수표): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364Q/risk_overlay_model_scorecard.csv`
- onnx_smoke_report(온엑스 연기 검사 보고서): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364Q/onnx_smoke_report.csv`
- overlay_policy_surface(오버레이 정책 표면): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364Q/overlay_policy_surface.csv`
- hold_cap_proxy_surface(보유 상한 프록시 표면): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364Q/hold_cap_proxy_surface.csv`
- short_router_proxy_surface(숏 라우터 프록시 표면): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364Q/short_router_proxy_surface.csv`
- selected_overlay_summary(선택 오버레이 요약): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364Q/selected_overlay_summary.json`
- gate_audit(게이트 감사): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364Q/required_gate_coverage_audit.csv`

## Gates(게이트)

| gate(게이트) | status | evidence(근거) | effect(효과) |
| --- | --- | --- | --- |
| scope_completion_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364Q/final_decision.json | run364Q scope(범위)를 proxy ONNX scout(프록시 온엑스 탐색)로 닫는다. |
| kpi_contract_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364Q/final_decision.json | MT5 KPI(MT5 핵심 성과 지표) 대신 proxy KPI(프록시 핵심 성과 지표)로 낮춰 적는다. |
| skill_receipt_lint | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364Q/work_packet.json | required skill receipt(필수 스킬 영수증)를 남긴다. |
| data_integrity_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364Q/data_integrity_receipt.json | entry feature(진입 피처)와 post-trade label(거래 후 라벨) 경계를 확인한다. |
| model_validation_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364Q/model_validation_receipt.json | validation train(검증 학습)과 oos readout(표본외 판독)을 분리한다. |
| artifact_lineage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364Q/artifact_lineage_receipt.json | input/model/onnx/report(입력/모델/온엑스/보고서) 계보를 연결한다. |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364Q/required_gate_coverage_audit.csv | experiment_execution(실험 실행) 필수 gate(게이트)를 closeout(종료 기록)에 연결한다. |

## Boundary(경계)

proxy(프록시)는 MT5 KPI(MT5 핵심 성과 지표)를 대체하지 않는다. hold cap(보유 상한)은 미래 cap open(상한 시점 시가)을 backtest label(백테스트 라벨)로 쓴 proxy(프록시)라 runtime evidence(런타임 근거)가 필요하다. Goal Achieve(목표 달성), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비)는 모두 `not_claimed`다.
