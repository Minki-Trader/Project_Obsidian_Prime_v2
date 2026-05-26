# Stage337R Boundary Forward Attribution Stress Review(337R 경계 전진 귀속 압박 리뷰)

- run_id(실행 ID): `run337R_fresh_boundary_repaired_forward_attribution_and_asof_policy_review_v1`
- status(상태): `completed_stage337R_boundary_attribution_stress_forward_blocked_no_goal_achieve`
- judgment(판정): `forward_blocked_by_tester_current_day_gap_and_asof_source_policy_after_attribution_review`
- decision(결정): `stage337R_open_run337S_tester_visible_source_policy_repair_or_next_data_boundary_probe_no_selection`
- best_runtime_probe(최선 런타임 탐침): `m48_plain_rf` net(순익) `267.39`, PF(손익비) `1.4000807972`
- tester_gap_attempts(테스터 공백 시도): `5`
- asof_forward_blocks(시점 기준 전진 차단): `14`
- low_cost_break_rows(낮은 비용 압박 붕괴 행): `8`
- parser_errors(파서 오류): `0`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `current_run_boundary`
- runtime authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Runtime Curve(런타임 곡선)

| attempt(시도) | feature(피처) | net(순익) | PF(손익비) | trades(거래수) | DD(손실폭) | worst pocket(최악 포켓) | read(판독) |
|---|---|---:|---:|---:|---:|---|---|
| `m48_plain_rf` | `macro48_no_equity_breadth_or_top3` | `267.39` | `1.4000807972` | `344` | `88.09` | `chron_segment:chron_early` | `blocked_for_forward_decision_even_if_runtime_probe_positive` |
| `c56_plain_rf` | `core56_no_top3_weight_features` | `146.56` | `1.66776016038` | `84` | `42.92` | `chron_segment:chron_late` | `blocked_for_forward_decision_even_if_runtime_probe_positive` |
| `u42_plain_rf` | `us100_technical42_no_external` | `99.9` | `1.1343066871` | `344` | `95.53` | `chron_segment:chron_late` | `blocked_for_forward_decision_even_if_runtime_probe_positive` |
| `m48_bal_rf` | `macro48_no_equity_breadth_or_top3` | `-17.63` | `0.979500476733` | `351` | `110.72` | `month:2026-04` | `blocked_for_forward_decision_even_if_runtime_probe_positive` |
| `c56_bal_rf` | `core56_no_top3_weight_features` | `-49` | `0.867781975175` | `80` | `125.17` | `chron_segment:chron_early` | `blocked_for_forward_decision_even_if_runtime_probe_positive` |

## Boundary(경계)

run337R(337R 실행)는 새 후보 개발이 아니라 run337Q(337Q 실행)의 실제 Strategy Tester(전략 테스터) 산출물을 거래 목록 단위로 분해한 리뷰다. ONNX(온엑스), feature order(피처 순서), threshold(임계값), risk/lot(위험/랏)은 수정하지 않았다.

효과: 일부 runtime probe(런타임 탐침) 지표는 양수지만, tester current-day gap(테스터 현재일 공백)과 as-of source policy(시점 기준 원천 정책) 때문에 Forward Passed/Failed(전진 통과/실패)는 닫지 않는다.
