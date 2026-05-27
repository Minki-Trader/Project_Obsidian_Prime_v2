# Stage337AK Synthetic Custom Exact Timestamp Parity Repair(337AK 합성 커스텀 정확 시각 동등성 수리)

- run_id(실행 ID): `run337AK_next_rollover_or_synthetic_custom_parity_repair_v1`
- status(상태): `completed_stage337AK_synthetic_custom_exact_timestamp_proxy_parity_repaired_no_forward_decision`
- judgment(판정): `synthetic_custom_tester_cycle_exact_proxy_parity_repaired_broker_gap_remains`
- decision(결정): `stage337AK_open_run337AL_boundary_policy_or_rollover_wait_no_selection`
- next_action(다음 행동): `run337AL_exact_timestamp_policy_boundary_or_broker_rollover_wait_v1`
- seed_status(심기 상태): `completed`
- runtime completed(런타임 완료): `2/2`
- exact proxy parity(정확 프록시 동등성): `10/10`
- broker gap(브로커 공백): `tester_feature_last_gap_remains`
- shifted custom gap(이동 커스텀 공백): `tester_reached_feature_last`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Meaning(의미)

run337AK(337AK 실행)는 새 후보 개발이 아니다. MT5 cycle timestamp(MT5 사이클 시각)와 정확히 같은 feature row(피처 행)만 Python ONNX proxy(파이썬 온엑스 프록시)에 넣어, run337AC mismatch(불일치)가 continuous window overcount(연속 창 과대계산)인지 확인한다.

Effect(효과): shifted custom(이동 커스텀)이 맞아도 synthetic diagnostic(합성 진단)일 뿐이며, broker forward decision(브로커 전진 판정)이나 Goal Achieve(목표 달성)는 열지 않는다.

## API Visibility(API 가시성)

| symbol(심볼) | status(상태) | custom(커스텀) | m5 last close(M5 마지막 종가 시각) |
|---|---|---:|---:|
| `US100` | `completed` | `False` | `2026-05-27T07:55:00Z` |
| `US100.OPV337AKM` | `completed` | `True` | `2026-05-26T07:35:00Z` |

## Tester Gap(테스터 공백)

| attempt(시도) | symbol(심볼) | feature last(피처 마지막) | tester last(테스터 마지막) | gap status(공백 상태) |
|---|---|---:|---:|---|
| `u42_plain_rf_ak_broker_rollover_control` | `US100` | `2026-05-27T02:00:00Z` | `2026-05-26T23:55:00Z` | `tester_feature_last_gap_remains` |
| `u42_plain_rf_ak_shifted_custom_exact_timestamp` | `US100.OPV337AKM` | `2026-05-26T02:00:00Z` | `2026-05-26T02:00:00Z` | `tester_reached_feature_last` |

## Exact Timestamp Scope(정확 시각 범위)

| attempt(시도) | telemetry rows(기록 행) | continuous rows(연속 창 행) | exact rows(정확 행) | overcount(과대계산) |
|---|---:|---:|---:|---:|
| `u42_plain_rf_ak_broker_rollover_control` | `8081` | `8081` | `8081` | `0` |
| `u42_plain_rf_ak_shifted_custom_exact_timestamp` | `6583` | `7819` | `6583` | `1236` |

## Usability(사용 가능 범위)

| attempt(시도) | proxy matched(프록시 일치) | diagnostic usability(진단 사용성) | forward usability(전진 사용성) |
|---|---:|---|---|
| `u42_plain_rf_ak_broker_rollover_control` | `5/5` | `usable_for_runtime_signal_parity` | `blocked_until_broker_reaches_feature_last` |
| `u42_plain_rf_ak_shifted_custom_exact_timestamp` | `5/5` | `usable_for_runtime_signal_parity` | `not_forward_authority_synthetic_shift` |
