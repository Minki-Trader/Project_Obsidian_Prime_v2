# Stage348 Selection Status(348단계 선정 상태)

- active_stage_at_handoff(인계 당시 단계): `348_cash_open_proxy_review__long_oos_gap_short_carry_triage`
- latest_completed_run(최근 완료 실행): `run348C_materialize_onnx_deployable_short_carry_probe_package_without_db_v1`
- superseded_planned_run(대체된 예정 실행): `run348D_execute_onnx_deployable_short_carry_mt5_probe_without_db_v1`
- handoff_stage(인계 단계): `349_onnx_short_carry_runtime__execute_mt5_probe`
- handoff_run(인계 실행): `run349A_branch_stage348_to_onnx_short_carry_runtime_probe_without_db_v1`
- next_runtime_run(다음 런타임 실행): `run349B_execute_onnx_deployable_short_carry_mt5_probe_without_db_v1`
- selected_model(선정 모델): `none(없음)`
- latest_package(최근 패키지): `run348C_materialize_onnx_deployable_short_carry_probe_package_without_db_v1`
- packaged_attempts(패키지 시도): `4`
- feature_order_boundary(피처 순서 경계): `53_feature_probe_only(53개 피처 탐침 전용)`
- trade_density_requirement(거래 밀도 요구): `trade_per_day_min_3_to_10_plus_no_trade_splitting`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): Stage348(348단계)은 MT5 runtime execution(MT5 런타임 실행)을 더 품지 않고 Stage349(349단계)로 넘긴다.
