# RUN28A Tier A Markov Long Permission Attribution Packet(28A 실행 티어 A 마르코프 롱 허용 귀속 묶음)

## Judgment(판정)

- run(실행): `run28A_tier_a_markov_long_permission_attribution_scout_v1`
- status(상태): `reviewed_attribution_scout_completed`
- judgment(판정): `inconclusive_tier_a_markov_long_permission_attribution_scout_completed`
- source run(원천 실행): `run22B_markov_regression_state_runtime_probe_v1`
- boundary(경계): `stage34_structural_attribution_only_no_baseline_no_promotion_no_runtime_authority`
- next action(다음 행동): `run28B_tier_a_markov_long_permission_segment_stress_probe_v1`

효과(effect, 효과): run22B(22B 실행)의 기존 MT5(메타트레이더5) 근거와 feature(피처)만 재사용해, Tier A Markov long permission(티어 A 마르코프 롱 허용)의 profit factor(수익 팩터)가 어디서 왔는지 나눈다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Observed Change(관찰 변화)

- validation(검증): Tier A(티어 A) PF(수익 팩터) `1.771465`, net(순손익) `208.01`, trades(거래 수) `77` vs Tier B(티어 B) PF(수익 팩터) `0.864054`.
- OOS(표본외): Tier A(티어 A) PF(수익 팩터) `1.224214`, net(순손익) `62.65`, trades(거래 수) `51` vs Tier B(티어 B) PF(수익 팩터) `0.989701`.

## Attribution Read(귀속 판독)

- state/confidence/entropy(상태/신뢰/엔트로피): Tier A(티어 A) 체결 거래는 모두 high-positive state(고양수 상태), confidence >= 0.97(신뢰 0.97 이상), entropy_inv >= 0.80(엔트로피 역수 0.80 이상)에 있었다.
- validation time(검증 시간): mid(중반) net(순손익) `117.94`, late(후반) net(순손익) `62.26`.
- OOS time(표본외 시간): late(후반) net(순손익) `98.08`, mid(중반) net(순손익) `-61.96`.
- hold shape(보유 형태): hold_gt_96(96봉 초과 보유)는 validation(검증) `255.35`, OOS(표본외) `89.59` 순손익을 냈다.

효과(effect, 효과): “마르코프라서 좋다”가 아니라, high-confidence long gate(고신뢰 롱 게이트) 안에서 time segment(시간 구간)와 hold shape(보유 형태)가 수익을 갈랐다고 읽는다.

## Files(파일)

- summary(요약): `docs/agent_control/packets/stage34_run28A_tier_a_markov_long_permission_attribution_scout_v1/aggregate_summary.json`
- segment attribution(구간 귀속): `docs/agent_control/packets/stage34_run28A_tier_a_markov_long_permission_attribution_scout_v1/tier_a_segment_attribution.csv`
- tier comparison(티어 비교): `docs/agent_control/packets/stage34_run28A_tier_a_markov_long_permission_attribution_scout_v1/tier_comparison_summary.csv`

Forbidden claims(금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).
