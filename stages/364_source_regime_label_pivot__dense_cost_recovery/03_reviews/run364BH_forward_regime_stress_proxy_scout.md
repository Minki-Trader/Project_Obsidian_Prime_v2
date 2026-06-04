# run364BH forward/regime stress proxy scout(364BH 전진/국면 압박 프록시 탐색)

## Scope(범위)

Action(행동): BG queue(BG 대기열)와 BF/BE MT5 closed trade + telemetry(MT5 종료 거래 + 원격측정)를 사용해 policy replay proxy scout(정책 재생 프록시 탐색)를 실행했다.

Effect(효과): Stage364(364단계)를 분기하지 않고, 작은 runtime-probe-prep candidate(런타임 탐침 준비 후보)와 density-breaking repair(밀도 붕괴 수리)를 분리했다.

## Selected(선택)

- selected_variant(선택 변형): `bh02_long_h19_margin_opp_0020`
- selected net/PF/trades/density/DD/recovery(선택 순수익/수익 팩터/거래수/밀도/낙폭/회복): `938.59` / `1.3732279833` / `1003` / `3.012012012` / `86.04` / `10.9087633659`
- selected long/short/share(선택 롱/숏/비중): `904` / `99` / `0.9012961117`
- baseline net/PF/trades/density(기준 순수익/수익 팩터/거래수/밀도): `900.36` / `1.3509614448` / `1016` / `3.0510510511`

## Top Surface(상위 표면)

| variant_id | candidate_status | net_profit | profit_factor | trade_count | trade_density_per_business_day | max_closed_drawdown_amount | long_share | removed_trade_count | forward_fail_count | selection_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bh02_long_h19_margin_opp_0020 | proxy_review_candidate_density_preserved(프록시 검토 후보, 밀도 보존) | 938.59 | 1.3732279833 | 1003 | 3.012012012 | 86.04 | 0.9012961117 | 13 | 0 | 0.765454216 |
| bh03_long_h19_margin_max_0015 | proxy_review_candidate_density_preserved(프록시 검토 후보, 밀도 보존) | 925.38 | 1.367389233 | 1001 | 3.006006006 | 86.04 | 0.9010989011 | 15 | 0 | -4.055032048 |
| bh01_long_h19_margin_opp_0015 | proxy_review_candidate_density_preserved(프록시 검토 후보, 밀도 보존) | 908.16 | 1.3568100204 | 1006 | 3.021021021 | 96.43 | 0.9015904573 | 10 | 0 | -5.073770554 |
| bh04_long_h18_margin_opp_0005 | proxy_review_candidate_density_preserved(프록시 검토 후보, 밀도 보존) | 905.96 | 1.3560687644 | 1010 | 3.033033033 | 100.45 | 0.901980198 | 6 | 0 | -12.817987158 |
| bh05_long_h16_margin_opp_0020 | proxy_review_candidate_density_preserved(프록시 검토 후보, 밀도 보존) | 900.55 | 1.3570309991 | 1003 | 3.012012012 | 90.64 | 0.9012961117 | 13 | 0 | -18.786183888 |
| bh10_h19_margin_plus_short_2025_01_h17 | watch_long_skew_worse_than_parent(관찰, 부모보다 롱 편향 악화) | 970.94 | 1.3911232497 | 1000 | 3.003003003 | 86.04 | 0.904 | 16 | 0 | -23.193832662 |
| bh00_current_runtime_policy_reference | watch_no_strict_improvement(관찰, 엄격 개선 아님) | 900.36 | 1.3509614448 | 1016 | 3.0510510511 | 99.96 | 0.9025590551 | 0 | 0 | -34.944323837 |
| bh09_short_negative_exact_slice_guard | rejected_density_breaks_3_per_day(거절, 밀도 3/day 붕괴) | 1018.22 | 1.419959003 | 996 | 2.990990991 | 85.87 | 0.9206827309 | 20 | 0 | -1028.030220724 |

## Rejected Density Repairs(거절된 밀도 수리)

| variant_id | net_profit | profit_factor | trade_count | trade_density_per_business_day | candidate_status |
| --- | --- | --- | --- | --- | --- |
| bh09_short_negative_exact_slice_guard | 1018.22 | 1.419959003 | 996 | 2.990990991 | rejected_density_breaks_3_per_day(거절, 밀도 3/day 붕괴) |
| bh06_negative_month_exact_firewall | 934.43 | 1.4098700775 | 906 | 2.7207207207 | rejected_density_breaks_3_per_day(거절, 밀도 3/day 붕괴) |
| bh07_weak_month_exact_firewall | 907.0 | 1.432861179 | 824 | 2.4744744745 | rejected_density_breaks_3_per_day(거절, 밀도 3/day 붕괴) |
| bh08_hour18_19_long_hard_firewall | 949.4 | 1.534740684 | 691 | 2.0750750751 | rejected_density_breaks_3_per_day(거절, 밀도 3/day 붕괴) |

## Selected Forward Blocks(선택 전진 유사 블록)

| segment_id | trade_count | trade_density_per_business_day | net_profit | profit_factor | long_share |
| --- | --- | --- | --- | --- | --- |
| 2025Q1 | 167 | 2.6935483871 | 132.45 | 1.3112150191 | 0.8323353293 |
| 2025Q2 | 263 | 4.0461538462 | 309.21 | 1.4097721942 | 0.9201520913 |
| 2025Q3 | 129 | 1.9545454545 | 50.0 | 1.1892648951 | 0.9612403101 |
| 2025Q4 | 223 | 3.4307692308 | 238.98 | 1.4152346533 | 0.8923766816 |
| 2026Q1 | 175 | 3.0701754386 | 184.66 | 1.468086185 | 0.88 |
| 2026Q2 | 46 | 5.1111111111 | 23.29 | 1.2319721116 | 1.0 |

## Weak Month Check(약한 월 확인)

| segment_id | trade_count | net_profit | profit_factor | trade_density_per_business_day | long_share |
| --- | --- | --- | --- | --- | --- |
| 2025-08 | 46 | 6.31 | 1.0610015468 | 2.1904761905 | 0.9347826087 |
| 2025-12 | 62 | -30.17 | 0.8245318134 | 2.8181818182 | 0.9193548387 |
| 2026-01 | 81 | 37.82 | 1.2172689148 | 3.8571428571 | 0.9382716049 |

## Short Balance(숏 균형)

| audit_id | current_short_share | minimum_added_shorts_needed_if_no_long_removal | long_removals_needed_if_no_new_shorts | density_if_no_new_shorts_and_target_share | judgment |
| --- | --- | --- | --- | --- | --- |
| current_short_balance_gap(현재 숏 균형 간극) | 0.0974409449 | 27 | 191 | 2.4774774775 | new_short_source_required_for_balance_without_density_collapse(밀도 붕괴 없이 균형을 맞추려면 새 숏 원천 필요) |
| selected_short_balance_gap(선택 후보 숏 균형 간극) |  |  |  |  | selected_candidate_does_not_repair_short_balance(선택 후보는 숏 균형을 수리하지 않음) |

## BI Queue(BI 대기열)

| queue_rank | queue_id | selected_variant_id | policy_family | review_question |
| --- | --- | --- | --- | --- |
| 1 | bi01_review_micro_h19_margin_candidate | bh02_long_h19_margin_opp_0020 | hour19_closed_bar_margin_guard(19시 닫힌 봉 margin 가드) | Can hour19 closed-bar margin guard survive review and package prep without hiding forward stress?(19시 닫힌 봉 margin 가드가 전진 압박을 숨기지 않고 검토/패키지 준비를 버티는가?) |
| 2 | bi02_reject_density_breaking_repairs |  | density_breaking_hard_filters(밀도 붕괴 강한 필터) | Should hard month/hour firewalls be closed as density-breaking under this run?(강한 월/시간 방화벽을 이번 실행에서 밀도 붕괴로 닫을 것인가?) |
| 3 | bi03_open_short_source_not_exact_slice_delete |  | short_source_exploration_needed(숏 원천 탐색 필요) | Can a new short source add at least 28 short trades without trade splitting?(새 숏 원천이 거래 쪼개기 없이 최소 28개 숏을 추가할 수 있는가?) |

## Gates(게이트)

| gate | status | effect |
| --- | --- | --- |
| scope_completion_gate | passed | BH proxy scout(BH 프록시 탐색) 산출물이 생성됐다. |
| kpi_contract_audit | passed | net/PF/density/DD/side metrics(순수익/PF/밀도/DD/방향 지표)를 기록했다. |
| skill_receipt_lint | passed | 필수 receipt(영수증)를 만들었다. |
| data_integrity_audit | passed | closed trade(종료 거래)와 telemetry probability(원격측정 확률)가 1:1 결합됐다. |
| proxy_replay_gate | passed | BG queue(BG 대기열)를 여러 후보 proxy replay(프록시 재생)로 평가했다. |
| density_survival_gate | passed | 선택 후보가 3/day 밀도 하한을 유지했다. |
| short_balance_boundary_gate | passed | 숏 균형 미해결을 별도 audit(감사)로 남겼다. |
| runtime_claim_boundary_gate | passed | 새 MT5 실행, forward pass(전진 통과), runtime authority(런타임 권위)를 주장하지 않는다. |
| artifact_lineage_audit | passed | 입력/출력 산출물 계보를 연결했다. |
| required_gate_coverage_audit | passed | 필수 gate(게이트)를 closeout(종료 기록)에 연결했다. |

## Claim Boundary(주장 경계)

Effect(효과): 이 run(실행)은 proxy scout(프록시 탐색)이다. 새 MT5 execution(새 MT5 실행), forward pass(전진 통과), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 주장하지 않는다.
