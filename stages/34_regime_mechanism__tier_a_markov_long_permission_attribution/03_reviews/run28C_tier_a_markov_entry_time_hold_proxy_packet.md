# RUN28C Tier A Markov Entry-Time Hold Proxy Packet(28C 실행 티어 A 마르코프 진입 시점 보유 대리 신호 묶음)

## Judgment(판정)

- run(실행): `run28C_tier_a_markov_long_permission_entry_time_hold_proxy_probe_v1`
- status(상태): `reviewed_entry_time_proxy_probe_completed`
- judgment(판정): `inconclusive_tier_a_markov_entry_time_proxy_probe_completed`
- source(원천): `run28A_tier_a_markov_long_permission_attribution_scout_v1` and `run28B_tier_a_markov_long_permission_segment_stress_probe_v1`
- boundary(경계): `stage34_entry_time_proxy_probe_only_no_baseline_no_promotion_no_runtime_authority`
- next action(다음 행동): `run28D_tier_a_markov_entry_proxy_runtime_probe_v1`

효과(effect, 효과): run28B(28B 실행)의 ex-post hold shape(사후 보유 형태) 단서를 진입 시점(entry time, 진입 시점)에 아는 session/regime(세션/국면) 조합으로 대리할 수 있는지 봤다. 새 MT5(MetaTrader 5, 메타트레이더5) 실행은 하지 않았다.

## Result(결과)

- primary candidate(1차 후보): `keep_late_or_vol_mid`
  - validation PF(검증 수익 팩터) `2.224467`, trades(거래 수) `40`
  - OOS PF(표본외 수익 팩터) `2.132004`, trades(거래 수) `26`
  - classification(분류): `entry_proxy_candidate_thin_sample`
- stable secondary(안정 보조 후보): `exclude_vol_high_or_adx_20_25`
  - validation PF(검증 수익 팩터) `2.081755`, OOS PF(표본외 수익 팩터) `1.541089`
  - classification(분류): `entry_proxy_candidate_modest`
- aggressive diagnostic(공격적 진단): `keep_vol_mid_or_late_not_adx_20_25`
  - validation PF(검증 수익 팩터) `3.828298`, OOS PF(표본외 수익 팩터) `3.534806`
  - classification(분류): `sample_thin_diagnostic_only`

## Read(판독)

`keep_late_or_vol_mid`가 가장 좋은 entry-time proxy(진입 시점 대리 신호)다. 다만 validation(검증) 40개, OOS(표본외) 26개로 sample margin(표본 여유)이 얇다.

효과(effect, 효과): 이 규칙은 바로 운영 의미(operating meaning, 운영 의미)가 아니라, run28D(28D 실행) MT5 runtime probe(MT5 런타임 탐침) 후보로만 남긴다.

## Files(파일)

- summary(요약): `docs/agent_control/packets/stage34_run28C_tier_a_markov_long_permission_entry_time_hold_proxy_probe_v1/entry_proxy_rule_summary.csv`
- split metrics(분할 지표): `docs/agent_control/packets/stage34_run28C_tier_a_markov_long_permission_entry_time_hold_proxy_probe_v1/entry_proxy_split_metrics.csv`
- label surface(라벨 표면): `docs/agent_control/packets/stage34_run28C_tier_a_markov_long_permission_entry_time_hold_proxy_probe_v1/entry_label_surface.csv`

Forbidden claims(금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위), MT5-verified runtime rule(MT5 검증 런타임 규칙).
