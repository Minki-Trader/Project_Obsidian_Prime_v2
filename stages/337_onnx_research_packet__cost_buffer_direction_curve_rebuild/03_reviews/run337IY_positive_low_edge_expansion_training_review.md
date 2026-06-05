# run337IY Positive Low-Edge Expansion Training Review(run337IY 양수 낮은 엣지 확장 학습 검토)

## Summary(요약)

- run_id(실행 ID): `run337IY_review_lifecycle_cost_positive_low_edge_cost_stress_trade_shape_expansion_training_without_db_v1`
- parent_run_id(부모 실행 ID): `run337IX_train_lifecycle_cost_positive_low_edge_cost_stress_trade_shape_expansion_candidates_without_db_v1`
- judgment(판정): `four_proxy_positive_cost_stress_onnx_candidates_found_mt5_runtime_probe_required_no_selection`
- gates(게이트): `13/13`
- positive_proxy_rows(프록시 양성 행): `4`
- best_model_id(최고 프록시 모델 ID): `ix_iv_iu001_cost_stress_fwd18_xgboost`
- best_proxy_net(최고 프록시 순수익): `4.124490419405447`
- best_profit_factor(최고 수익 팩터): `1.1338998246730707`
- best_recovery_factor(최고 회복 계수): `1.473258669269806`
- best_side_balance_ratio(최고 방향 균형 비율): `0.8863049095607235`
- best_weakness_tags(약점 태그): `high_signal_density_above_0_80;long_net_negative;weak_balanced_accuracy_below_0_40`

## Action(행동)

IX training(IX 학습) 산출물 7개를 review(검토)했고 ONNX parity(ONNX 동등성) 7/7을 확인했다.
Effect(효과): proxy-positive(프록시 양성) 4개를 selected model(선정 모델)이 아니라 MT5 runtime probe(MT5 런타임 탐침) 비교 대상으로만 분리했다.

## Finding(발견)

`ix_iv_iu001_cost_stress_fwd18_xgboost`가 proxy net(프록시 순수익) `4.124490419405447`와 PF(수익 팩터) `1.1338998246730707`를 보였다.
Effect(효과): 이 후보는 운영 후보가 아니라 proxy-vs-MT5 comparison(프록시-MT5 비교) 필요 후보로만 열린다.

## Boundary(경계)

No candidate selection(후보 선택 없음), no MT5 execution in IY(IY에서 MT5 실행 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).

## Next(다음)

`run337IZ_materialize_lifecycle_cost_positive_low_edge_cost_stress_trade_shape_expansion_runtime_probe_package_without_db_v1`에서 runtime probe package(런타임 탐침 패키지)를 만든다.
Effect(효과): proxy expected value(프록시 예상값)를 MT5 runtime evidence(MT5 런타임 근거)와 비교할 준비를 한다.
