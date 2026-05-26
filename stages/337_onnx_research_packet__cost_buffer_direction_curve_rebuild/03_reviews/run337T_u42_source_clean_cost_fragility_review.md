# Stage337T u42 Source-Clean Cost Fragility Review(337T u42 원천 깨끗한 비용 취약성 리뷰)

- run_id(실행 ID): `run337T_source_clean_u42_cost_fragility_or_tester_rollover_probe_v1`
- status(상태): `completed_stage337T_u42_source_clean_cost_fragility_review_no_forward_decision`
- judgment(판정): `u42_source_clean_control_runtime_parity_ok_but_cost_and_slice_fragility_not_onnx_ready`
- decision(결정): `stage337T_open_run337U_cost_buffer_rebuild_or_tester_rollover_reprobe_no_selection`
- proxy_runtime_parity(프록시 런타임 동등성): `matched`
- one_point_pf(1포인트 손익비): `1.08630090555`
- five_point_net(5포인트 순익): `-72.1175977083`
- weak_slice_count(약한 구간 수): `19`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Weak Pockets(약한 포켓)

| axis(축) | bucket(구간) | net(순익) | PF(손익비) | trades(거래수) | status(상태) |
|---|---|---:|---:|---:|---|
| `weekday` | `Monday` | `-82.18` | `0.605756776205` | `69` | `base_negative_pocket` |
| `direction` | `sell` | `-59.08` | `0.603516542514` | `31` | `base_negative_pocket` |
| `weekday` | `Tuesday` | `-35.15` | `0.816803043728` | `77` | `base_negative_pocket` |
| `adx_regime` | `adx_20_to_25` | `-34.75` | `0.842809969693` | `90` | `base_negative_pocket` |
| `open_hour_utc` | `15` | `-20.25` | `0.712112595962` | `21` | `base_negative_pocket` |
| `open_hour_utc` | `08` | `-19.7` | `0.643245201014` | `31` | `base_negative_pocket` |
| `session_utc` | `session_07_12_utc` | `-17.78` | `0.945165767155` | `183` | `base_negative_pocket` |
| `open_hour_utc` | `07` | `-14.08` | `0.704883672186` | `30` | `base_negative_pocket` |
| `open_hour_utc` | `10` | `-13.73` | `0.805165318575` | `31` | `base_negative_pocket` |
| `chron_segment` | `chron_late` | `-11.45` | `0.965924647342` | `114` | `base_negative_pocket` |

## Read(판독)

u42_plain_rf(US100 기술42 일반 RF)는 source-clean control(원천 깨끗한 대조군)로는 유용하다. 하지만 비용 1포인트에서 PF(손익비)가 1.1 아래로 내려가고, 5포인트에서는 순익이 음수로 바뀐다.
효과: 이 축은 운영 가능한 ONNX(온엑스) 준비가 아니라, 다음 cost-buffer rebuild(비용 버퍼 재구성) 또는 tester rollover reprobe(테스터 이월 재탐침)의 실패 기억으로 사용한다.
