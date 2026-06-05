# run337JK Positive Low PF Recovery Drawdown Dual Probe Repair Design(run337JK 양수 저PF 회복 낙폭 이중 탐침 수리 설계)

## Summary(요약)

- run_id(실행 ID): `run337JK_design_runtime_positive_low_pf_recovery_drawdown_dual_probe_repair_without_db_v1`
- parent_run_id(부모 실행 ID): `run337JJ_review_runtime_negative_collapse_cost_stress_trade_shape_repair_mt5_runtime_probe_or_repair_without_db_v1`
- judgment(판정): `runtime_positive_low_pf_recovery_drawdown_dual_probe_repair_design_opened_no_selection`
- gates(게이트): `11/11`
- design_rows(설계 행): `8`
- positive_clue_model(긍정 단서 모델): `jf_jd_jc001_runtime_pnl_fwd18_xgboost`
- positive_net_profit(긍정 순수익): `202.81`
- positive_profit_factor(긍정 수익 팩터): `1.1`
- positive_recovery_factor(긍정 회복 계수): `0.82`
- positive_drawdown(긍정 낙폭): `246.52`
- negative_control_model(부정 대조 모델): `jf_jd_jc007_session_regime_fwd18_xgboost`
- negative_control_net_profit(부정 대조 순수익): `-203.52`

## Action(행동)

JJ runtime probe(JJ 런타임 탐침)의 +202.81 net profit(순수익) 단서를 `run337JL` materialization(입력 물질화) 설계로 바꿨다.
Effect(효과): raw PnL(원시 손익) 우위는 살리고, 낮은 PF/recovery/drawdown(수익 팩터/회복/낙폭)은 다음 입력에서 직접 수리하게 한다.

## Boundary(경계)

No training(학습 없음), no MT5 execution(MT5 실행 없음), no candidate selection(후보 선정 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
