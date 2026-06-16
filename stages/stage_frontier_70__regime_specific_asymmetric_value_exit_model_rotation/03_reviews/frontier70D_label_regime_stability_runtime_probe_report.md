# F70D Label-Regime Stability MT5 Runtime Probe(F70D 라벨-장세 안정성 MT5 런타임 탐침)

Updated(갱신): 2026-06-16T22:00:26Z

## Action And Effect(행동과 효과)

Action(행동): F70C near-miss axes(F70C 근접 실패 축) 2개를 ONNX(온엑스), RuntimeVetoTape(런타임 차단 테이프), MT5 Strategy Tester(MT5 전략 테스터)로 물질화했다.

Effect(효과): proxy-only clue(프록시 전용 단서)가 runtime execution(런타임 실행)에서 신호, 피처, 거래 경제성으로 어떻게 달라지는지 관찰한다.

- status(상태): `completed_mt5_runtime_probe_observation_no_authority`
- judgment(판정): `runtime_probe_observation_recorded_no_authority`
- attempts(시도): `4`
- claim boundary(주장 경계): `runtime_probe_observation_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## ONNX And Signal Parity(ONNX와 신호 동등성)

| axis(축) | candidate(후보) | role(역할) | export(내보내기) | probability parity(확률 동등성) | signal parity(신호 동등성) |
|---|---|---|---|---|---|
| `reference_low_dd_axis` | `f70c_f9a2939acd19` | `near_miss_reference_axis_joint_soft_zero_observation_only` | `exported_onnx_parity_passed` | `True` | `True` |
| `small_nn_density_axis` | `f70c_5c8a3021f38f` | `hypothesis_carrier_small_nn_joint_soft_zero_observation_only` | `exported_onnx_parity_passed` | `True` | `True` |

## Runtime KPI(런타임 핵심 성과 지표)

| axis(축) | split(분할) | period(기간) | net(순수익) | gross profit(총이익) | gross loss(총손실) | PF(수익 팩터) | DD%(손실폭) | trades(거래) | trades/day(일거래) | signal diff(신호 차이) | feature diff(피처 차이) | gap cause(간극 원인) |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `reference_low_dd_axis` | `validation` | `2025-01-02..2025-10-01` | `105.04` | `1426.7` | `-1321.66` | `1.08` | `13.73` | `960` | `3.529412` | `0` | `0` | `trade_lifecycle_gap_after_signal_parity` |
| `reference_low_dd_axis` | `oos` | `2025-10-01..2026-04-14` | `119.38` | `1070.98` | `-951.6` | `1.13` | `10.74` | `655` | `3.358974` | `0` | `0` | `trade_lifecycle_gap_after_signal_parity` |
| `small_nn_density_axis` | `validation` | `2025-01-02..2025-10-01` | `226.24` | `1819.54` | `-1593.3` | `1.14` | `8.69` | `1093` | `4.018382` | `0` | `0` | `trade_lifecycle_gap_after_signal_parity` |
| `small_nn_density_axis` | `oos` | `2025-10-01..2026-04-14` | `92.29` | `1599.3` | `-1507.01` | `1.06` | `17.5` | `952` | `4.882051` | `0` | `0` | `trade_lifecycle_gap_after_signal_parity` |

## Runtime Parity Boundary(런타임 동등성 경계)

- research_path(연구 경로): `stage_pipelines/stage_frontier_70/frontier70d_label_regime_stability_runtime_probe.py`.
- runtime_path(런타임 경로): `foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5` and include modules(포함 모듈).
- shared_contract(공유 계약): feature order hash(피처 순서 해시), ONNX probability output(온엑스 확률 출력), edge_margin decision mode(엣지 마진 의사결정), RuntimeVetoTape selection mask(런타임 차단 테이프 선택 마스크), ATR SL/TP(평균진폭 손절/익절), max hold bars(최대 보유 봉수).
- known_differences(알려진 차이): proxy non-overlap(프록시 비중첩)은 EA max hold/cooldown(EA 최대 보유/쿨다운)과 같지 않을 수 있어 trade count gap(거래 수 간극)을 별도로 기록한다.

Claim boundary(주장 경계): `runtime_probe_observation_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`
