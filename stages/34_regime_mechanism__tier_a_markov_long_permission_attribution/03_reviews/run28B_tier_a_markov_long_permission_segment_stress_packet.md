# RUN28B Tier A Markov Segment Stress Packet(28B 실행 티어 A 마르코프 구간 압박 묶음)

## Judgment(판정)

- run(실행): `run28B_tier_a_markov_long_permission_segment_stress_probe_v1`
- status(상태): `reviewed_segment_stress_probe_completed`
- judgment(판정): `inconclusive_tier_a_markov_segment_stress_probe_completed`
- source(원천): `run28A_tier_a_markov_long_permission_attribution_scout_v1` and `run22B_markov_regression_state_runtime_probe_v1`
- boundary(경계): `stage34_segment_stress_probe_only_no_baseline_no_promotion_no_runtime_authority`
- next action(다음 행동): `run28C_tier_a_markov_long_permission_entry_time_hold_proxy_probe_v1`

효과(effect, 효과): run28A(28A 실행)에서 보인 Tier A Markov long permission(티어 A 마르코프 롱 허용)을 새 MT5(MetaTrader 5, 메타트레이더5) 실행 없이 구간별 stress(압박)로 찔렀다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.

## Result(결과)

- `exclude_short_hold_0_12`: validation PF(검증 수익 팩터) `1.844226`, OOS PF(표본외 수익 팩터) `1.491944`. 짧은 보유를 빼면 양쪽이 같이 좋아진다.
- `keep_hold_gt_96_only`: validation PF(검증 수익 팩터) `2.779691`, OOS PF(표본외 수익 팩터) `1.496619`. 긴 보유가 수익을 많이 들고 있다.
- `exclude_mid_session`: OOS net(표본외 순손익)은 `124.61`로 좋아지지만 validation net(검증 순손익)은 `90.07`로 줄어든다. 그래서 직접 규칙으로는 불안정하다.

## Read(판독)

가장 센 단서는 hold shape(보유 형태)다. 다만 hold bucket(보유 버킷)은 거래가 끝난 뒤에야 아는 ex-post(사후) 정보라서, 그대로 runtime rule(런타임 규칙)이 될 수 없다.

효과(effect, 효과): 다음 run28C(28C 실행)는 entry time(진입 시점)에 짧은 보유 실패를 미리 알아볼 proxy(대리 신호)를 찾는 쪽이 맞다.

## Files(파일)

- summary(요약): `docs/agent_control/packets/stage34_run28B_tier_a_markov_long_permission_segment_stress_probe_v1/segment_stress_summary.csv`
- split metrics(분할 지표): `docs/agent_control/packets/stage34_run28B_tier_a_markov_long_permission_segment_stress_probe_v1/segment_stress_split_metrics.csv`
- removed impact(제거 영향): `docs/agent_control/packets/stage34_run28B_tier_a_markov_long_permission_segment_stress_probe_v1/rule_removed_slice_impact.csv`

Forbidden claims(금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).
