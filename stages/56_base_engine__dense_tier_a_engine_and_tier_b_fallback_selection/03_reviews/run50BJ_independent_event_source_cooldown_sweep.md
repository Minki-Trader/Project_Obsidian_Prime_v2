# Stage56 run50BJ Independent Event Source Cooldown Sweep(독립 이벤트 원천 쿨다운 탐색)

- run_id(실행 ID): `run50BJ_stage56_independent_event_source_cooldown_sweep_v1`
- packet_id(묶음 ID): `stage56_run50BJ_independent_event_source_cooldown_sweep_v1`
- selected_research_baseline(선택 연구 기준선): `none`
- external_verification_status(외부 검증 상태): `completed`
- claim_boundary(주장 경계): `research_baseline_selection_only_no_operating_claim`

Action(행동): Stage43/45/47 independent source(독립 원천)를 Stage56 actual MT5 routed path(실제 MT5 라우팅 경로)로 다시 실행했다.
Effect(효과): 이전 source clue(원천 단서)가 현재 BaselineAdapter(기준선 어댑터) 밀도 병목을 풀 수 있는지 한 계정 경로(one tester account path, 단일 테스터 계정 경로)로 판정한다.

## Best Read(최선 판독)

- best_variant(최선 변형): `s43c02_h4c0`
- validation/OOS trades/day(검증/표본외 일 거래): `7.393443` / `5.600000`
- validation/OOS PF(검증/표본외 수익 팩터): `1.120000` / `1.060000`
- validation/OOS net(검증/표본외 순손익): `363.02` / `156.49`
- failure_reasons(실패 사유): `oos_pf;cost_stressed_expectancy;same_move_density`

## Variant Summary(변형 요약)

| variant | source | val day | oos day | val PF | oos PF | val net | oos net | failures |
|---|---|---:|---:|---:|---:|---:|---:|---|
| s43c02_h4c0 | s43:c02_top8_stability_ranked_elasticnet | 7.393443 | 5.600000 | 1.120000 | 1.060000 | 363.02 | 156.49 | oos_pf;cost_stressed_expectancy;same_move_density |
| s47c03_h4c0 | s47:c03_majority_agreement | 7.797814 | 5.487179 | 1.020000 | 1.120000 | 74.880000 | 273.11 | validation_pf;cost_stressed_expectancy;same_move_density |
| s45c04_h4c0 | s45:c04_histvol_ratio_expansion | 7.349727 | 4.512821 | 1.010000 | 1.060000 | 33.620000 | 110.00 | oos_density;validation_pf;oos_pf;cost_stressed_expectancy;same_move_density |
| s47c03_h4c2 | s47:c03_majority_agreement | 6.306011 | 4.379487 | 0.890000 | 1.020000 | -270.58 | 33.220000 | oos_density;validation_net_positive;validation_pf;oos_pf;cost_stressed_expectancy;same_move_density |
| s45c04_h4c2 | s45:c04_histvol_ratio_expansion | 6.754098 | 4.143590 | 0.910000 | 1.030000 | -225.98 | 59.700000 | oos_density;validation_net_positive;validation_pf;oos_pf;cost_stressed_expectancy;same_move_density |
| s45c04_h4c4 | s45:c04_histvol_ratio_expansion | 6.103825 | 3.820513 | 0.930000 | 1.080000 | -157.70 | 120.93 | oos_density;validation_net_positive;validation_pf;oos_pf;cost_stressed_expectancy;same_move_density |

## Audit Summary(감사 요약)

| variant | split | MFE capture | same move | cooldown day | cost-stressed exp |
|---|---|---:|---:|---:|---:|
| s45c04_h4c0 | validation_is | 0.585859 | 0.464684 | 3.934426 | -0.475004 |
| s45c04_h4c0 | oos | 0.604767 | 0.427273 | 2.584615 | -0.375000 |
| s45c04_h4c2 | validation_is | 0.588126 | 0.424757 | 3.885246 | -0.682832 |
| s45c04_h4c2 | oos | 0.608092 | 0.386139 | 2.543590 | -0.426114 |
| s45c04_h4c4 | validation_is | 0.596655 | 0.367950 | 3.857923 | -0.641182 |
| s45c04_h4c4 | oos | 0.617574 | 0.347651 | 2.492308 | -0.337678 |
| s47c03_h4c0 | validation_is | 0.593685 | 0.659425 | 2.655738 | -0.447526 |
| s47c03_h4c0 | oos | 0.609900 | 0.706542 | 1.610256 | -0.244757 |
| s47c03_h4c2 | validation_is | 0.592969 | 0.590121 | 2.584699 | -0.734471 |
| s47c03_h4c2 | oos | 0.604884 | 0.628806 | 1.625641 | -0.461101 |
| s43c02_h4c0 | validation_is | 0.595908 | 0.740576 | 1.918033 | -0.231693 |
| s43c02_h4c0 | oos | 0.605994 | 0.780220 | 1.230769 | -0.356694 |

Judgment(판정): `in_progress_no_selected_research_baseline`.
Effect(효과): run50BJ(실행50BJ)는 progress evidence(진행 근거)이고 Stage56(56단계)은 계속 open(열림)이다.
