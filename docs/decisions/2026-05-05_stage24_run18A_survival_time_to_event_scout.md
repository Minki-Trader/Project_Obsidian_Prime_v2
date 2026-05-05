# 2026-05-05 Stage24 RUN18A Survival Time-To-Event Decision(24단계 실행18A 생존 시간-사건 결정)

## Decision(결정)

`run18A_survival_time_to_event_hold_shape_scout_v1`를 `inconclusive_survival_time_to_event_hold_shape_scout_completed`로 기록한다.

효과(effect, 효과): Survival model(생존 모델)의 time-to-event(사건까지 시간)와 censoring(검열) 구조를 hold/exit clue(보유/청산 단서)로 보존한다. edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.

## Selected Read(선택 판독)

- selected variant(선택 변형): `v04_weibull_aft_core24_abs_move_3x`
- validation c-index(검증 일치 지수): `0.73631244882561`
- OOS c-index(표본외 일치 지수): `0.6856377470736932`
- next action(다음 행동): `run18B_survival_time_to_event_runtime_probe_v1`
