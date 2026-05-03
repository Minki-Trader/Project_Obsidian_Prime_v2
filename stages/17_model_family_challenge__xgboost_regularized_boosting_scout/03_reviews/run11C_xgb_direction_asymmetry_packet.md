# Stage17 RUN11C XGBoost Direction Asymmetry Probe(17단계 실행11C XGBoost 방향 비대칭 탐침)

- run(실행): `run11C_xgb_q80_direction_asymmetry_probe_v1`
- threshold quantile(임계값 분위수): `q0.80`
- judgment(판정): `inconclusive_xgboost_direction_asymmetry_runtime_probe_completed`
- characteristic strength(특성 강도): `direction_asymmetry_visible`
- recommendation(권고): `keep_stage17_open_for_trade_shape_or_regime_attribution`
- MT5 KPI records(MT5 핵심성과지표 기록): `20`
- normalized KPI records(정규화 핵심성과지표 기록): `20`
- trade attribution records(거래 귀속 기록): `4`

| side(방향) | validation trades/net/PF(검증 거래/순수익/수익 팩터) | OOS trades/net/PF(표본외 거래/순수익/수익 팩터) |
|---|---:|---:|
| long-only(롱 전용) | `224 / -24.28 / 0.98` | `191 / -8.44 / 0.99` |
| short-only(숏 전용) | `73 / -253.76 / 0.6` | `73 / 66.91 / 1.22` |

- new characteristic visible(새 특성 보임): `True`
- trade count contrast(거래 수 대비): `0.47950089126559714`
- profit factor contrast(수익 팩터 대비): `0.07500000000000007`

효과(effect, 효과): run11B(실행11B)의 거래빈도 확대가 어느 방향에서 생기는지 분리한다. edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.
