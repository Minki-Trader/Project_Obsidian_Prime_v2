# run43B_reversal_selection_rule_mt5_linkage_v1 Packet(패킷)

- stage_id(단계 ID): `49_trade_lifecycle__compression_stress_mfe_capture_exit_timing`
- judgment(판정): `reviewed_completed_positive_runtime_linkage_probe_only`
- source candidate(원천 후보): `c08_extreme_compression_stress`
- rule(규칙): `skip_short_adx_20_25` / `skip short entries when 20 <= adx_14 <= 25`
- MT5 attempts(MT5 시도): `2`
- MT5 KPI rows(MT5 핵심 성과 지표 행): `6`
- validation original/filtered/delta(검증 원본/필터/차이): `57.7` -> `111.53` / `53.83`
- OOS original/filtered/delta(외표본 원본/필터/차이): `146.86` -> `242.28` / `95.42`
- decision reasons(결정 이유): `both_split_mt5_net_profit_delta_positive;posthoc_selection_rule_not_promotion`
- boundary(주장 경계): `runtime_linkage_probe_only_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_operating_reference`

Interpretation(해석): this is runtime_linkage_probe_only(런타임 수익 연동 탐침 전용). It tests whether the post-hoc clue(사후 단서) survives an actual MT5 rerun(실제 MT5 재실행), but it creates no baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or operating reference(운영 기준).
