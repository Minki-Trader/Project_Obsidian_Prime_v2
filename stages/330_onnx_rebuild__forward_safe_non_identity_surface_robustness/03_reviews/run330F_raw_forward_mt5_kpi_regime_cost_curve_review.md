# run330F Raw Forward MT5 KPI Regime Cost Curve Review(330F 원본 전진 MT5 핵심 지표/국면/비용/곡선 검토)

- run_id(실행 ID): `run330F_raw_forward_mt5_kpi_regime_cost_curve_review_v1`
- parent_run_id(부모 실행 ID): `run330E_mt5_runtime_probe_or_block_v1`
- status(상태): `completed_raw_forward_mt5_kpi_regime_cost_curve_review_no_final_forward_decision`
- judgment(판정): `raw_forward_mt5_review_completed_research_only_no_goal_achieve`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## MT5 KPI(핵심 성과 지표)

| attempt(시도) | net(순손익) | PF(수익 팩터) | trades/day(일 거래) | DD%(드로다운 퍼센트) | recovery(회복 계수) |
|---|---:|---:|---:|---:|---:|
| m48_plain | 269.88 | 1.49 | 9.275862 | 14.1 | 3.46 |
| c56_plain | 147.06 | 1.67 | 2.655172 | 10.08 | 2.09 |
| u42_plain | 119.91 | 1.17 | 9.588235 | 17.37 | 1.06 |
| m48_bal | 57.84 | 1.08 | 9.551724 | 28.11 | 0.4 |
| u42_bal | 8.66 | 1.01 | 9.5 | 30.87 | 0.05 |
| c56_bal | 1.45 | 1.0 | 2.586207 | 22.55 | 0.01 |

## Read(판독)

- watchlist_not_selection(선택 아닌 관찰 목록): `c56_plain_rf, m48_plain_rf`
- fragility_flags(취약성 표시): `c56_bal_rf, m48_bal_rf, u42_bal_rf, u42_plain_rf`
- D/B attribution(D/B 귀속): `out_of_scope_by_claim`
- effect(효과): raw-forward MT5 evidence(원본 전진 MT5 근거)는 생겼지만 cost fragility(비용 취약성), curve pocket(곡선 포켓), D/B source handoff(D/B 원천 인계)가 남아 Forward Passed(전진 통과)를 닫지 않는다.

## Next(다음)

`run330G_raw_forward_failure_fragility_memory_and_overfit_followup`
