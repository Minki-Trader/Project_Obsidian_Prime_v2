# run337II Runtime Positive Repair Training Review(run337II 런타임 양성 수리 학습 검토)

## Summary(요약)

- run_id(실행 ID): `run337II_review_runtime_positive_low_pf_drawdown_side_balance_repair_training_without_db_v1`
- parent_run_id(부모 실행 ID): `run337IH_train_runtime_positive_low_pf_drawdown_side_balance_repair_candidates_without_db_v1`
- judgment(판정): `one_weak_proxy_positive_onnx_candidate_found_mt5_runtime_probe_required_no_selection`
- gates(게이트): `12/12`
- positive_proxy_rows(양성 프록시 행): `1`
- best_model_id(최고 프록시 모델 ID): `ih_if_ie003_pf_recovery_fwd18_xgboost`
- best_proxy_net(최고 프록시 순수익): `0.4754999014553505`
- best_profit_factor(최고 수익 팩터): `1.0164863573227334`
- best_recovery_factor(최고 회복 계수): `0.2072868161244308`
- best_side_balance_ratio(최고 방향 균형 비율): `0.7385952208544533`
- best_weakness_tags(약점 태그): `low_profit_factor_below_1_05;low_recovery_factor_below_1;side_net_negative_present;high_signal_density_above_0_80;weak_balanced_accuracy_below_0_40`

## Action(행동)

IH training(학습) 산출물 6개를 review(검토)했고, ONNX parity(온엑스 동등성) 6/6을 확인했다.
Effect(효과): weak proxy-positive(약한 프록시 양성) 1개를 selected model(선정 모델)이 아니라 MT5 runtime probe(런타임 탐침) 비교 대상으로만 분리했다.

## Finding(발견)

`ih_if_ie003_pf_recovery_fwd18_xgboost`는 proxy net(프록시 순수익)이 양수지만 PF(수익 팩터) `1.0164863573227334`와 recovery factor(회복 계수) `0.2072868161244308`가 낮다.
Effect(효과): 이 후보는 운영 후보가 아니라 proxy-vs-MT5 comparison(프록시-MT5 비교) 필요 후보로만 남긴다.

## Boundary(경계)

No candidate selection(후보 선택 없음), no MT5 execution in II(II에서 MT5 실행 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).

## Next(다음)

`run337IJ_materialize_runtime_positive_low_pf_drawdown_side_balance_repair_runtime_probe_package_without_db_v1`에서 runtime probe package(런타임 탐침 패키지)를 만든다.
Effect(효과): proxy expected value(프록시 예상값)를 MT5 runtime evidence(MT5 런타임 근거)와 비교할 수 있게 한다.
