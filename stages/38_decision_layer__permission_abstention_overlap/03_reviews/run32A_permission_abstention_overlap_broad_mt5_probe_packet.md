# Stage38 RUN32A Permission/Abstention Overlap MT5 Runtime Probe Packet(38단계 32A 실행 허용/기권 겹침 MT5 런타임 탐침 묶음)

## Judgment(판정)

- final_judgment(최종 판정): `reviewed_completed_inconclusive_runtime_probe_only`
- claim_boundary(주장 경계): `runtime_probe_only_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_operating_reference`
- MT5 attempts(MT5 시도): `34`
- MT5 KPI records(MT5 핵심 성과 지표 기록): `102`

## Broad Sweep(넓은 훑기)

| candidate_id | split | net_profit | profit_factor | trade_count | tier_a_used_count_mt5 | tier_b_fallback_used_count_mt5 | candidate_rejection_reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| c01_no_overlap_reference | validation_is | 334.73 | 1.08 | 1356 | 7327 | 1478 | oos_net_not_positive;oos_pf_below_1_05;tier_b_fallback_carrying_too_much |
| c01_no_overlap_reference | oos | -494.46 | 0.86 | 982 | 5680 | 727 | oos_net_not_positive;oos_pf_below_1_05;tier_b_fallback_carrying_too_much |
| c02_permission_only | validation_is | -37.74 | 0.99 | 1659 | 7753 | 987 | validation_net_not_positive;validation_pf_below_1_05 |
| c02_permission_only | oos | 160.98 | 1.05 | 1171 | 6091 | 685 | validation_net_not_positive;validation_pf_below_1_05 |
| c03_abstention_only | validation_is | -494.9 | 0.89 | 1513 | 8359 | 1136 | validation_net_not_positive;validation_pf_below_1_05 |
| c03_abstention_only | oos | 151.91 | 1.05 | 1153 | 6519 | 609 | validation_net_not_positive;validation_pf_below_1_05 |
| c04_permission_abstention | validation_is | -183.08 | 0.96 | 1514 | 6595 | 558 | validation_net_not_positive;validation_pf_below_1_05 |
| c04_permission_abstention | oos | 225.54 | 1.07 | 1069 | 5185 | 430 | validation_net_not_positive;validation_pf_below_1_05 |
| c05_permission_entropy | validation_is | 61.09 | 1.01 | 1413 | 5841 | 719 | validation_pf_below_1_05 |
| c05_permission_entropy | oos | 420.56 | 1.14 | 998 | 4585 | 485 | validation_pf_below_1_05 |
| c06_permission_tail | validation_is | -337.35 | 0.88 | 1059 | 4248 | 777 | validation_net_not_positive;validation_pf_below_1_05;oos_pf_below_1_05 |
| c06_permission_tail | oos | 92.1 | 1.04 | 747 | 3292 | 438 | validation_net_not_positive;validation_pf_below_1_05;oos_pf_below_1_05 |
| c07_permission_ebm | validation_is | -140.66 | 0.95 | 751 | 3587 | 440 | validation_net_not_positive;oos_net_not_positive;validation_pf_below_1_05;oos_pf_below_1_05 |
| c07_permission_ebm | oos | -3.69 | 1.0 | 544 | 2846 | 294 | validation_net_not_positive;oos_net_not_positive;validation_pf_below_1_05;oos_pf_below_1_05 |
| c08_permission_abstention_entropy | validation_is | -3.6 | 1.0 | 1291 | 5083 | 423 | validation_net_not_positive;validation_pf_below_1_05 |
| c08_permission_abstention_entropy | oos | 232.73 | 1.08 | 915 | 3984 | 298 | validation_net_not_positive;validation_pf_below_1_05 |
| c09_permission_abstention_tail | validation_is | -381.33 | 0.85 | 946 | 3464 | 434 | validation_net_not_positive;validation_pf_below_1_05 |
| c09_permission_abstention_tail | oos | 130.93 | 1.06 | 662 | 2704 | 279 | validation_net_not_positive;validation_pf_below_1_05 |
| c10_permission_abstention_ebm | validation_is | -196.71 | 0.93 | 696 | 3123 | 272 | validation_net_not_positive;oos_net_not_positive;validation_pf_below_1_05;oos_pf_below_1_05 |
| c10_permission_abstention_ebm | oos | -173.6 | 0.92 | 509 | 2502 | 182 | validation_net_not_positive;oos_net_not_positive;validation_pf_below_1_05;oos_pf_below_1_05 |
| c11_permission_entropy_tail | validation_is | -294.18 | 0.86 | 772 | 2486 | 557 | validation_net_not_positive;validation_pf_below_1_05 |
| c11_permission_entropy_tail | oos | 198.2 | 1.12 | 553 | 1908 | 290 | validation_net_not_positive;validation_pf_below_1_05 |
| c12_permission_entropy_ebm | validation_is | -0.27 | 1.0 | 669 | 2806 | 325 | validation_net_not_positive;oos_net_not_positive;validation_pf_below_1_05;oos_pf_below_1_05 |
| c12_permission_entropy_ebm | oos | -19.27 | 0.99 | 467 | 2221 | 216 | validation_net_not_positive;oos_net_not_positive;validation_pf_below_1_05;oos_pf_below_1_05 |
| c13_permission_tail_ebm | validation_is | 109.42 | 1.07 | 478 | 1890 | 346 | oos_net_not_positive;oos_pf_below_1_05 |
| c13_permission_tail_ebm | oos | -211.51 | 0.86 | 340 | 1512 | 174 | oos_net_not_positive;oos_pf_below_1_05 |
| c14_permission_abstention_entropy_tail | validation_is | -273.87 | 0.87 | 688 | 2063 | 324 | validation_net_not_positive;validation_pf_below_1_05 |
| c14_permission_abstention_entropy_tail | oos | 137.43 | 1.09 | 489 | 1611 | 180 | validation_net_not_positive;validation_pf_below_1_05 |
| c15_permission_abstention_entropy_ebm | validation_is | -84.09 | 0.97 | 611 | 2470 | 214 | validation_net_not_positive;oos_net_not_positive;validation_pf_below_1_05;oos_pf_below_1_05 |
| c15_permission_abstention_entropy_ebm | oos | -236.46 | 0.88 | 444 | 1986 | 136 | validation_net_not_positive;oos_net_not_positive;validation_pf_below_1_05;oos_pf_below_1_05 |
| c16_permission_abstention_tail_ebm | validation_is | 159.67 | 1.12 | 432 | 1614 | 218 | oos_net_not_positive;oos_pf_below_1_05 |
| c16_permission_abstention_tail_ebm | oos | -172.86 | 0.87 | 309 | 1323 | 118 | oos_net_not_positive;oos_pf_below_1_05 |
| c17_permission_abstention_entropy_tail_ebm | validation_is | 175.24 | 1.18 | 285 | 1008 | 0 | oos_net_not_positive;oos_pf_below_1_05 |
| c17_permission_abstention_entropy_tail_ebm | oos | -245.51 | 0.75 | 237 | 857 | 90 | oos_net_not_positive;oos_pf_below_1_05 |

## Micro Search Gate(미세 탐색 게이트)

- status(상태): `failed`
- best_candidate(최선 후보): `None`

## Validation Commands(검증 명령)

| command | result | failures_or_blockers |
| --- | --- | --- |
| python -m py_compile stage_pipelines\stage38\permission_abstention_overlap.py foundation\pipelines\run_stage38_permission_abstention_overlap.py tests\test_stage38_permission_abstention_overlap.py | passed | none |
| $env:PYTHONPATH=(Get-Location).Path; pytest tests\test_stage38_permission_abstention_overlap.py tests\test_mt5_runtime_artifacts.py tests\test_mt5_kpi_recorder.py tests\test_control_plane_alpha_run_ledgers.py -q | 25 passed in 2.14s | none |
| $env:PYTHONPATH=(Get-Location).Path; python -m foundation.pipelines.run_stage38_permission_abstention_overlap --materialize-only | preflight generated common table, candidate grid, handoff files, and intentionally returned blocked_runtime_probe_missing_mt5_execution because MT5 execution was skipped | not a completion claim; followed by actual MT5 run |
| $env:PYTHONPATH=(Get-Location).Path; python -m foundation.pipelines.run_stage38_permission_abstention_overlap --timeout-seconds 900 | exit 0; 34 MT5 Strategy Tester reports imported; 102 MT5 KPI records written; judgment reviewed_completed_inconclusive_runtime_probe_only | none |

## Boundary(경계)

Stage38 run32A remains runtime_probe_only: no baseline, no promotion, no runtime authority, no live readiness, and no operating reference.
