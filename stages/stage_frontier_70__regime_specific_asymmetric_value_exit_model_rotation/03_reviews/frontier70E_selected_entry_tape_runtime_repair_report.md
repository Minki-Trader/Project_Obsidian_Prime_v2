# F70E Selected-Entry Tape Runtime Repair(F70E 선택 진입 테이프 런타임 수리)

Updated(갱신): 2026-06-16T22:15:33Z

Action(행동): F70D와 같은 모델/피처/임계값을 유지하고 RuntimeVetoTape(런타임 차단 테이프)만 proxy selected non-overlap entries(프록시 선택 비중첩 진입)로 바꿔 MT5 Runtime Probe(MT5 런타임 탐침)를 다시 실행했다.

Effect(효과): trade_lifecycle_gap_after_signal_parity(신호 동등성 이후 거래 생명주기 간극)가 줄어드는지 관찰한다.

- status(상태): `completed_selected_entry_tape_runtime_repair_observation_no_authority`
- judgment(판정): `selected_entry_tape_runtime_repair_observation_recorded_no_authority`
- Grok advice(그록 조언): `accepted_selected_entry_repair_needs_local_verification`
- claim boundary(주장 경계): `runtime_repair_observation_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Runtime KPI(런타임 핵심 성과 지표)

| axis(축) | split(분할) | net(순수익) | PF(수익 팩터) | DD%(손실폭) | trades(거래) | trades/day(일거래) | expected selected(예상 선택) | signal diff(신호 차이) | feature diff(피처 차이) | gap cause(간극 원인) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `reference_low_dd_axis` | `validation` | `44.63` | `1.14` | `8.49` | `254` | `0.933824` | `254` | `0` | `0` | `runtime_economics_gap_after_signal_and_feature_parity` |
| `reference_low_dd_axis` | `oos` | `68` | `1.29` | `5.61` | `174` | `0.892308` | `174` | `0` | `0` | `runtime_economics_gap_after_signal_and_feature_parity` |
| `small_nn_density_axis` | `validation` | `93.06` | `1.22` | `6.93` | `311` | `1.143382` | `311` | `0` | `0` | `runtime_economics_gap_after_signal_and_feature_parity` |
| `small_nn_density_axis` | `oos` | `7.15` | `1.02` | `10.56` | `239` | `1.225641` | `239` | `0` | `0` | `runtime_economics_gap_after_signal_and_feature_parity` |

Claim boundary(주장 경계): `runtime_repair_observation_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`
