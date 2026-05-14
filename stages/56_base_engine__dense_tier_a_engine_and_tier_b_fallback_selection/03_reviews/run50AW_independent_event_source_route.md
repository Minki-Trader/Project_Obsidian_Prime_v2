# Stage56 run50AW Independent Event Source Route(독립 이벤트 원천 라우트)

- run_id(실행 ID): `run50AW_stage56_independent_event_source_route_v1`
- packet_id(묶음 ID): `stage56_run50AW_independent_event_source_route_v1`
- selected_research_baseline(선택 연구 기준선): `none`
- external_verification_status(외부 검증 상태): `completed`
- claim_boundary(주장 경계): `research_baseline_selection_only_no_operating_claim`

Action(행동): Stage43/45/47 independent source(독립 원천)를 Stage56 actual MT5 routed path(실제 MT5 라우팅 경로)로 다시 실행했다.
Effect(효과): 이전 source clue(원천 단서)가 현재 BaselineAdapter(기준선 어댑터) 밀도 병목을 풀 수 있는지 한 계정 경로(one tester account path, 단일 테스터 계정 경로)로 판정한다.

## Best Read(최선 판독)

- best_variant(최선 변형): `s45c04_h4c6`
- validation/OOS trades/day(검증/표본외 일 거래): `5.535519` / `3.553846`
- validation/OOS PF(검증/표본외 수익 팩터): `0.980000` / `1.180000`
- validation/OOS net(검증/표본외 순손익): `-32.280000` / `246.33`
- failure_reasons(실패 사유): `oos_density;validation_net_positive;validation_pf;cost_stressed_expectancy;same_move_density`

## Variant Summary(변형 요약)

| variant | source | val day | oos day | val PF | oos PF | val net | oos net | failures |
|---|---|---:|---:|---:|---:|---:|---:|---|
| s45c04_h4c6 | s45:c04_histvol_ratio_expansion | 5.535519 | 3.553846 | 0.980000 | 1.180000 | -32.280000 | 246.33 | oos_density;validation_net_positive;validation_pf;cost_stressed_expectancy;same_move_density |
| s47c03_h4c6 | s47:c03_majority_agreement | 4.551913 | 3.179487 | 1.020000 | 1.100000 | 29.030000 | 134.19 | validation_density;oos_density;validation_pf;cost_stressed_expectancy;same_move_density |
| s43c02_h4c6 | s43:c02_top8_stability_ranked_elasticnet | 4.169399 | 3.000000 | 1.010000 | 1.060000 | 26.520000 | 80.340000 | validation_density;oos_density;validation_pf;oos_pf;cost_stressed_expectancy;same_move_density |
| s43c08_h4c6 | s43:c08_constrained_tree_stump_combo | 3.196721 | 2.200000 | 0.750000 | 1.160000 | -350.45 | 139.73 | validation_density;oos_density;validation_net_positive;validation_pf;cost_stressed_expectancy;same_move_density |
| s45c06_h4c6 | s45:c06_direction_specific_expansion_breakout | 1.000000 | 0.769231 | 0.760000 | 0.930000 | -100.03 | -23.930000 | validation_density;oos_density;validation_net_positive;oos_net_positive;validation_pf;oos_pf;cost_stressed_expectancy;same_move_density |

## Audit Summary(감사 요약)

| variant | split | MFE capture | same move | cooldown day | cost-stressed exp |
|---|---|---:|---:|---:|---:|
| s43c02_h4c6 | validation_is | 0.613397 | 0.484928 | 2.147541 | -0.465242 |
| s43c02_h4c6 | oos | 0.608852 | 0.577778 | 1.266667 | -0.362667 |
| s43c08_h4c6 | validation_is | 0.624140 | 0.553846 | 1.426230 | -1.099060 |
| s43c08_h4c6 | oos | 0.604839 | 0.585082 | 0.912821 | -0.174289 |
| s45c04_h4c6 | validation_is | 0.593277 | 0.318855 | 3.770492 | -0.531866 |
| s45c04_h4c6 | oos | 0.608904 | 0.305916 | 2.466667 | -0.144545 |
| s45c06_h4c6 | validation_is | 0.590699 | 0.065574 | 0.934426 | -1.046612 |
| s45c06_h4c6 | oos | 0.604868 | 0.060000 | 0.723077 | -0.659533 |
| s47c03_h4c6 | validation_is | 0.594470 | 0.422569 | 2.628415 | -0.465150 |
| s47c03_h4c6 | oos | 0.614875 | 0.493548 | 1.610256 | -0.283565 |

Judgment(판정): `in_progress_no_selected_research_baseline`.
Effect(효과): run50AW(실행50AW)는 progress evidence(진행 근거)이고 Stage56(56단계)은 계속 open(열림)이다.
