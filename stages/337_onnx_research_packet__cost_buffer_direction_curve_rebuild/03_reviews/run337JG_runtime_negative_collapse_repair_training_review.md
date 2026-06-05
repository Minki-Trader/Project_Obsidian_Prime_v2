# run337JG Runtime Negative Collapse Repair Training Review(run337JG 런타임 음수 붕괴 수리 학습 검토)

## Summary(요약)

- run_id(실행 ID): `run337JG_review_runtime_negative_collapse_cost_stress_trade_shape_repair_training_without_db_v1`
- parent_run_id(부모 실행 ID): `run337JF_train_runtime_negative_collapse_cost_stress_trade_shape_repair_candidates_without_db_v1`
- judgment(판정): `proxy_positive_but_high_density_and_weak_accuracy_runtime_probe_required_no_selection`
- gates(게이트): `14/14`
- positive_proxy_rows(프록시 양수 행): `4`
- primary_probe_model(주 탐침 모델): `jf_jd_jc007_session_regime_fwd18_xgboost`
- primary_proxy_net(주 탐침 프록시 순수익): `4.3647865214470585`
- primary_profit_factor(주 탐침 수익 팩터): `1.1562565473613626`
- primary_signal_density(주 탐침 신호 밀도): `0.8755350111282315`
- raw_top_model(순수 1위 모델): `jf_jd_jc001_runtime_pnl_fwd18_xgboost`
- raw_top_proxy_net(순수 1위 프록시 순수익): `4.852932238507492`
- primary_weakness_tags(주 탐침 약점 태그): `high_signal_density_above_0_80;long_net_negative;weak_balanced_accuracy_below_0_40`

## Action(행동)

JF training(JF 학습) 산출물 8개를 review(검토)하고 ONNX parity(ONNX 동등성) 8/8을 확인했다.
Effect(효과): proxy-positive(프록시 양수) 4개를 selected model(선정 모델)이 아니라 MT5 runtime probe(MT5 런타임 탐침) 비교 대상으로만 분리했다.

## Finding(발견)

Risk-adjusted probe(위험 보정 탐침)는 `jf_jd_jc007_session_regime_fwd18_xgboost`이고 raw proxy top(순수 프록시 1위)은 `jf_jd_jc001_runtime_pnl_fwd18_xgboost`이다.
Effect(효과): JB high-density collapse(JB 고밀도 붕괴) 실패 기억을 반영해 단일 proxy net(프록시 순수익)만 쫓지 않는다.

## Boundary(경계)

No candidate selection(후보 선택 없음), no MT5 execution in JG(JG에서 MT5 실행 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).

## Next(다음)

`run337JH_materialize_runtime_negative_collapse_cost_stress_trade_shape_repair_runtime_probe_package_without_db_v1`에서 runtime probe package(런타임 탐침 패키지)를 만든다.
