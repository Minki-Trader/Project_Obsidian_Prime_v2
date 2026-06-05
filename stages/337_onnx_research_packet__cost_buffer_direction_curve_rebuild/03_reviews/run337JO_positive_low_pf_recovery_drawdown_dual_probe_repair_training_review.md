# run337JO Positive Low PF Recovery Drawdown Training Review(run337JO 양수 저PF 회복 낙폭 학습 검토)

## Summary(요약)

- run_id(실행 ID): `run337JO_review_runtime_positive_low_pf_recovery_drawdown_dual_probe_repair_training_without_db_v1`
- parent_run_id(부모 실행 ID): `run337JN_train_runtime_positive_low_pf_recovery_drawdown_dual_probe_repair_candidates_without_db_v1`
- judgment(판정): `proxy_positive_but_high_density_side_imbalance_and_weak_accuracy_mt5_runtime_probe_required_no_selection`
- gates(게이트): `14/14`
- positive_proxy_rows(프록시 양수 행): `4`
- primary_probe_model(주 탐침 모델): `jn_jl_jk004_long_quarantine_short_preserve_xgboost`
- primary_proxy_net(주 탐침 프록시 순수익): `4.816295379355324`
- primary_profit_factor(주 탐침 수익 팩터): `1.1581750411500111`
- primary_recovery_factor(주 탐침 회복 계수): `1.929306764301475`
- primary_side_balance_ratio(주 탐침 방향 균형 비율): `0.11452567283832793`
- balance_control_model(균형 대조 모델): `jn_jl_jk001_pf_recovery_profit_quality_xgboost`
- cost_control_model(비용 대조 모델): `jn_jl_jk006_cost_stress_buffer_extratrees`
- primary_weakness_tags(주 탐침 약점 태그): `extreme_signal_density_above_0_95;side_balance_ratio_below_0_50;long_net_negative;weak_balanced_accuracy_below_0_40`

## Action(행동)

JN training(JN 학습) 산출물 8개를 review(검토)하고 ONNX parity(ONNX 동등성) 8/8을 확인했다.
Effect(효과): proxy-positive(프록시 양수) 4개를 selected model(선정 모델)이 아니라 MT5 runtime probe(MT5 런타임 탐침) 비교 대상으로만 분리했다.

## Finding(발견)

Raw top(순수 1위)은 `jn_jl_jk004_long_quarantine_short_preserve_xgboost`이고, balance control(균형 대조)은 `jn_jl_jk001_pf_recovery_profit_quality_xgboost`, cost control(비용 대조)은 `jn_jl_jk006_cost_stress_buffer_extratrees`이다.
Effect(효과): high-density/short-heavy(고밀도/숏 편중) 실패 가능성을 단일 proxy net(프록시 순수익)보다 먼저 MT5에서 확인하게 한다.

## Boundary(경계)

No candidate selection(후보 선택 없음), no MT5 execution in JO(JO에서 MT5 실행 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).

## Next(다음)

`run337JP_materialize_runtime_positive_low_pf_recovery_drawdown_dual_probe_repair_runtime_probe_package_without_db_v1`에서 runtime probe package(런타임 탐침 패키지)를 만든다.
