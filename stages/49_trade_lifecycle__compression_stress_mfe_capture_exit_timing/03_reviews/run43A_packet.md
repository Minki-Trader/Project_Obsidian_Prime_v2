# run43A_compression_stress_mfe_capture_exit_timing_scout_v1 Packet(패킷)

- stage_id(단계 ID): `49_trade_lifecycle__compression_stress_mfe_capture_exit_timing`
- judgment(판정): `reviewed_completed_inconclusive_counterfactual_exit_timing_scout_only`
- source(원천): `c08_extreme_compression_stress` from Stage48(48단계) run42B
- diagnostic rows(진단 행): `735`
- validation loss with positive MFE(검증 양의 MFE 보유 손실): `257` / `271` share `0.948339`
- OOS loss with positive MFE(외표본 양의 MFE 보유 손실): `169` / `178` share `0.949438`
- best validation fixed target(검증 최선 고정 목표): `14.0` delta `55.34`
- best OOS fixed target(외표본 최선 고정 목표): `16.0` delta `-2.06`
- best common fixed target(공통 최선 고정 목표): `16.0` validation delta `38.84` OOS delta `-2.06`
- decision reasons(결정 이유): `no_common_fixed_take_profit_target_improves_both_splits;validation_improvement_not_oos_confirmed;loss_rescue_diagnostic_large_but_not_executable_without_selection_rule`
- boundary(주장 경계): `counterfactual_exit_timing_scout_only_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_operating_reference`

Interpretation(해석): positive MFE(양의 최대 유리 변동)는 대부분 손실 거래에 있었지만, unconditional fixed take-profit(무조건 고정 익절)은 both splits(양쪽 분할)를 동시에 개선하지 못했다. This is an exit-timing clue(청산 타이밍 단서), not a promotion(승격) or runtime authority(런타임 권위).
