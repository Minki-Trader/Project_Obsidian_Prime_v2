# run329F Forward MT5 KPI Regime Cost Curve Review(329F 전진 MT5 핵심 지표/국면/비용/곡선 검토)

- run_id(실행 ID): `run329F_forward_mt5_kpi_regime_cost_curve_review_v1`
- parent_run_id(부모 실행 ID): `run329E_session_parity_forward_signal_payload_and_mt5_runtime_probe_v1`
- status(상태): `completed_forward_mt5_kpi_regime_cost_curve_review_no_final_forward_decision`
- judgment(판정): `forward_mt5_review_completed_research_only_no_goal_achieve`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## MT5 KPI(핵심 성과 지표)

| attempt(시도) | net(순손익) | PF(수익 팩터) | trades/day(일별 거래) | DD%(드로다운 퍼센트) | recovery(회복계수) |
|---|---:|---:|---:|---:|---:|
| m48_plain | 173.42 | 1.98 | 2.37931 | 10.27 | 2.33 |
| c56_plain | 165.66 | 1.87 | 2.413793 | 10.82 | 2.09 |
| u42_plain | 120.78 | 1.54 | 2.482759 | 13.85 | 1.25 |
| m48_bal | 116.19 | 1.5 | 2.448276 | 9.7 | 2.28 |
| c56_bal | 43.24 | 1.15 | 2.413793 | 16.79 | 0.52 |
| u42_bal | 3.99 | 1.01 | 2.413793 | 12.65 | 0.06 |

## Read(판독)

- watchlist_not_selection(선택 아닌 관찰 목록): `c56_plain_sp, m48_bal_sp, m48_plain_sp, u42_plain_sp`
- fragility_flags(취약성 표시): `c56_bal_sp, u42_bal_sp`
- D/B attribution(D/B 귀속): `out_of_scope_by_claim`
- effect(효과): session-parity MT5 evidence(세션 동등 MT5 근거)는 생겼지만, raw-forward gap(원본 전진 간극), D/B source handoff(D/B 원천 인계), longer horizon(더 긴 기간)이 남아 Forward Passed(전진 통과)를 닫지 않는다.

## Next(다음)

`run329G_raw_forward_session_gap_and_overfit_pressure_review`
