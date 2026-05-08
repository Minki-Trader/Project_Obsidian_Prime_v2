# RUN28D Tier A Markov Frequency Floor Packet(28D 실행 티어 A 마르코프 거래 수 하한 묶음)
## Judgment(판정)
- run(실행): `run28D_tier_a_markov_entry_proxy_frequency_floor_probe_v1`
- status(상태): `reviewed_frequency_floor_probe_completed(검토된 거래 수 하한 탐침 완료)`
- judgment(판정): `inconclusive_tier_a_markov_entry_proxy_frequency_floor_probe_completed`
- source(원천): `run28C_tier_a_markov_long_permission_entry_time_hold_proxy_probe_v1`
- boundary(경계): `stage34_frequency_floor_probe_only_no_baseline_no_promotion_no_runtime_authority`
- next action(다음 행동): `run28E_tier_a_markov_broader_entry_proxy_probe_v1`
효과(effect, 효과): run28C(28C 실행)의 높은 PF(수익 팩터)를 바로 seed(씨앗)로 올리지 않고, 기간 대비 거래 수와 월별 집중도부터 확인했다. 이번 실행은 MT5(`MetaTrader 5`, 메타트레이더5) 새 실행이 아니다.
## Result(결과)
- preserved reference seed(보존 기준 씨앗): `baseline_all_trades` validation trades(검증 거래 수) `77`, OOS trades(표본외 거래 수) `51`, validation/OOS PF(검증/표본외 수익 팩터) `1.771465` / `1.224214`
- run28C primary(28C 1차 후보): `keep_late_or_vol_mid` validation trades(검증 거래 수) `40`, OOS trades(표본외 거래 수) `26`, validation/OOS PF(검증/표본외 수익 팩터) `2.224467` / `2.132004`
- primary decision(1차 후보 결정): `downgrade_to_thin_modifier_clue`
- broader secondary(더 넓은 보조 후보): `exclude_vol_high_or_adx_20_25` validation trades(검증 거래 수) `59`, OOS trades(표본외 거래 수) `32`, validation/OOS PF(검증/표본외 수익 팩터) `2.081755` / `1.541089`
- secondary decision(보조 후보 결정): `broader_secondary_probe_candidate`
## Read(해석)
`keep_late_or_vol_mid`는 PF(수익 팩터)는 좋지만 validation(검증) 40건, OOS(표본외) 26건이라 frequency floor(거래 수 하한)를 통과하지 못했다.
효과(effect, 효과): 이 후보는 thin modifier clue(얇은 수정 단서)로 보존하고, main seed(메인 씨앗)나 MT5 verified runtime rule(MT5 검증 런타임 규칙)로 올리지 않는다.
`exclude_vol_high_or_adx_20_25`는 PF(수익 팩터)는 낮지만 validation(검증) 59건, OOS(표본외) 32건으로 거래 수 하한을 통과했다.
효과(effect, 효과): 다음 실험은 이 넓은 보조 후보를 더 찔러보는 쪽이 맞다. 아직 baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.
## Files(파일)
- summary(요약): `docs/agent_control/packets/stage34_run28D_tier_a_markov_entry_proxy_frequency_floor_probe_v1/frequency_floor_rule_summary.csv`
- split metrics(분할 지표): `docs/agent_control/packets/stage34_run28D_tier_a_markov_entry_proxy_frequency_floor_probe_v1/frequency_floor_split_metrics.csv`
- monthly concentration(월별 집중도): `docs/agent_control/packets/stage34_run28D_tier_a_markov_entry_proxy_frequency_floor_probe_v1/frequency_floor_monthly_concentration.csv`
