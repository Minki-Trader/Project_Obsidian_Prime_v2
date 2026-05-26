# run329G Raw Forward Session Gap Overfit Review(329G 원본 전진 세션 간극/과적합 검토)

- run_id(실행 ID): `run329G_raw_forward_session_gap_and_overfit_pressure_review_v1`
- parent_run_id(부모 실행 ID): `run329F_forward_mt5_kpi_regime_cost_curve_review_v1`
- status(상태): `completed_raw_forward_session_gap_and_overfit_pressure_review_no_forward_decision`
- judgment(판정): `raw_forward_gap_keeps_forward_decision_open_no_goal_achieve`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Pressure Table(압력 표)

| artifact(산출물) | pressure(압력) | raw/session signal ratio(원본/세션 신호 비율) | exclusive signal rate(전용 원본 신호율) | MT5 PF(MT5 수익 팩터) | cost+1 PF(비용+1 수익 팩터) |
|---|---:|---:|---:|---:|---:|
| u42_bal | high:13 | 6.4033487709 | 0.4704446382 | 1.01 | 0.807904 |
| m48_bal | high:8 | 5.682038835 | 0.5220568336 | 1.5 | 1.172244 |
| m48_plain | high:8 | 5.5938864629 | 0.5694181326 | 1.98 | 1.512868 |
| u42_plain | high:8 | 5.889478556 | 0.4931124673 | 1.54 | 1.192883 |
| c56_bal | medium:4 | 1.0498812352 | 0.0747330961 | 1.15 | 0.917077 |
| c56_plain | low:2 | 1.0296610169 | 0.0498220641 | 1.87 | 1.432225 |

## Read(판독)

- high_pressure(높은 압력): `m48_bal, m48_plain, u42_bal, u42_plain`
- medium_pressure(중간 압력): `c56_bal`
- low_pressure(낮은 압력): `c56_plain`
- effect(효과): session-parity MT5(세션 동등 MT5) 양수 근거가 있어도 raw_forward(원본 전진) 공급 구조가 다르면 Forward Passed(전진 통과)로 닫지 않는다.

## Next(다음)

`run329H_cp322A_exact_handoff_repair_feasibility_or_research_artifact_closeout`
