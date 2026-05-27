# Stage337AC Next-Day Rollover or Custom Symbol Seed Repair(337AC 다음날 이월 또는 커스텀 심볼 심기 수리)

- run_id(실행 ID): `run337AC_next_day_broker_rollover_or_custom_symbol_seed_repair_v1`
- status(상태): `completed_stage337AC_shifted_custom_seed_repair_confirms_current_day_tester_policy_no_forward_decision`
- judgment(판정): `shifted_custom_symbol_reaches_feature_last_while_broker_current_day_gap_remains`
- decision(결정): `stage337AC_open_run337AD_completed_day_forward_slice_or_next_day_rollover_confirm_no_selection`
- next_action(다음 행동): `run337AD_completed_day_forward_slice_or_next_day_rollover_confirm_v1`
- next_day_rollover_status(다음날 이월 상태): `not_yet_due_same_utc_date`
- shifted_custom_symbol(이동 커스텀 심볼): `US100.OPV337ACM`
- shift_minutes(이동 분): `-1440`
- MT5 runtime completed(MT5 런타임 완료): `2/2`
- broker control gap(브로커 대조 공백): `tester_feature_last_gap_remains`
- shifted custom gap(이동 커스텀 공백): `tester_reached_feature_last`
- timestamp-aligned proxy parity(시점 맞춤 프록시 동등성): `5/10`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Meaning(의미)

run337AC(337AC 실행)는 새 후보 개발이 아니다. broker control(브로커 대조군)은 원래 시간축을 유지하고, shifted custom mirror(이동 커스텀 미러)는 같은 봉과 같은 feature value(피처 값)를 1440분 과거로 옮긴다.

Effect(효과): 이동 미러가 feature_last(피처 마지막 시점)에 도달하면, custom symbol seed(커스텀 심볼 심기)와 feature handoff(피처 인계)는 과거 완성일에서는 작동한다는 뜻이다. 그 경우 현재 공백은 ONNX parity(온엑스 동등성)보다 Strategy Tester current-day policy(전략 테스터 현재일 정책) 쪽으로 좁혀진다.

## API Visibility(API 가시성)

| symbol(심볼) | status(상태) | custom(커스텀) | m5 last close(M5 마지막 종가 시점) |
|---|---|---:|---:|
| `US100` | `completed` | `False` | `2026-05-27T05:40:00Z` |
| `US100.OPV337ACM` | `completed` | `True` | `2026-05-26T05:40:00Z` |

## Tester Boundary(테스터 경계)

| attempt(시도) | symbol(심볼) | requested to(요청 종료) | log test to(로그 종료) | last observed(마지막 관측) | gap status(공백 상태) |
|---|---|---:|---:|---:|---|
| `u42_plain_rf_ac_broker_rollover_control` | `US100` | `2026.05.30` | `2026.05.27 00:00` | `2026-05-26T23:55:00Z` | `tester_feature_last_gap_remains` |
| `u42_plain_rf_ac_shifted_custom_mirror` | `US100.OPV337ACM` | `2026.05.28` | `2026.05.27 00:00` | `2026-05-26T02:00:00Z` | `tester_reached_feature_last` |

## Proxy vs MT5(프록시 대 MT5)

proxy expected(프록시 예상값)는 timestamp-aligned(시점 맞춤) runtime signal parity(런타임 신호 동등성)에만 쓴다. shifted mirror(이동 미러)는 synthetic diagnostic(합성 진단)이므로 Forward decision(전진 판정)이나 KPI authority(KPI 권위)가 아니다.

| attempt(시도) | matched(일치) | diagnostic usability(진단 활용성) | forward usability(전진 활용성) |
|---|---:|---|---|
| `u42_plain_rf_ac_broker_rollover_control` | `5/5` | `usable_for_signal_parity_until_tester_cutoff_not_forward_decision` | `not_usable_as_forward_decision` |
| `u42_plain_rf_ac_shifted_custom_mirror` | `0/5` | `usable_for_boundary_visibility_only_not_signal_parity` | `not_usable_as_forward_decision` |
