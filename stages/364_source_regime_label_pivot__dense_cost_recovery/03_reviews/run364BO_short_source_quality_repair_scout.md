# run364BO short source quality repair scout(364BO 숏 원천 품질 수리 정찰)

## Current Truth(현재 진실)

- parent seed(부모 씨앗): `bn02_h17_or_h20_margin_08_10_quality_repair`
- selected candidate(선택 후보): `bo00_bn_seed_h17_or_h20_margin_08_10_reference`
- selected KPI(선택 핵심 성과 지표): net/PF/density/short share(순수익/수익 팩터/밀도/숏비중) `1037.17` / `1.4101564709` / `3.0750750751` / `0.1201171875`
- synthetic short PF(합성 숏 수익 팩터): `1.3816978038`
- stress status(압박 상태): quarter_bad_count(분기 나쁨 수) `0`, month_bad_count(월 나쁨 수) `2`
- package candidate rows(패키지 후보 행): `0`

## Action And Effect(행동과 효과)

Action(행동): BN repair seed(BN 수리 씨앗)를 entry-known hour/probability/margin(진입시점 시간/확률/마진) rule surface(규칙 표면)로 재생하고, broad pool negative control(넓은 풀 부정 대조)을 붙였다.

Effect(효과): h17/h20 margin seed(17시/20시 마진 씨앗)는 여전히 proxy(프록시)로 쓸 수 있지만, monthly stress(월별 압박)가 남아 package(패키지)는 열지 않고 BP review(BP 검토)로 넘긴다.

## Rule Surface(규칙 표면)

| candidate_id | candidate_status | net_profit | profit_factor | trade_count | trade_density_per_business_day | short_share | synthetic_short_profit_factor | month_bad_count | selection_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bo05_h17_margin_075_105_or_h20_margin_08_10 | watch_short_share_below_target(관찰, 숏 비중 목표 미달) | 1026.66 | 1.4088361576 | 1017 | 3.0540540541 | 0.1111111111 | 2.8224308655 | 1 | 192.176712228 |
| bo00_bn_seed_h17_or_h20_margin_08_10_reference | proxy_review_candidate_stress_watch_no_package(프록시 검토 후보, 스트레스 관찰, 패키지 아님) | 1037.17 | 1.4101564709 | 1024 | 3.0750750751 | 0.1201171875 | 1.3816978038 | 2 | 57.809682468 |
| bo02_h17_or_h20_margin_075_105_wide_band | proxy_review_candidate_stress_watch_no_package(프록시 검토 후보, 스트레스 관찰, 패키지 아님) | 1037.17 | 1.4101564709 | 1024 | 3.0750750751 | 0.1201171875 | 1.3816978038 | 2 | 55.809682468 |
| bo06_h17_h20_margin_08_10_plus_h18_strict | proxy_review_candidate_stress_watch_no_package(프록시 검토 후보, 스트레스 관찰, 패키지 아님) | 1035.71 | 1.4093444314 | 1025 | 3.0780780781 | 0.1209756098 | 1.3644473008 | 2 | 53.271307904 |
| bo04_h17_p445_or_h20_margin_08_10 | watch_short_share_below_target(관찰, 숏 비중 목표 미달) | 1024.82 | 1.4071317165 | 1018 | 3.0570570571 | 0.1139489194 | 1.5301159872 | 1 | 39.968377434 |
| bo07_h17_h20_margin_08_10_plus_h19_strict | proxy_review_candidate_stress_watch_no_package(프록시 검토 후보, 스트레스 관찰, 패키지 아님) | 1025.36 | 1.4024262738 | 1027 | 3.0840840841 | 0.1226874391 | 1.23929501 | 2 | 33.761867086 |
| bo03_h17_or_h20_p445_margin075 | watch_short_share_below_target(관찰, 숏 비중 목표 미달) | 1035.62 | 1.4098563272 | 1022 | 3.0690690691 | 0.1183953033 | 1.408071384 | 2 | 23.352204976 |
| bo08_h17_or_h20_p46_pressure | watch_short_share_below_target(관찰, 숏 비중 목표 미달) | 1027.4 | 1.4066043661 | 1021 | 3.0660660661 | 0.1175318315 | 1.3337853598 | 2 | 10.975529074 |
| bo01_h17_only_quality_floor | watch_short_share_below_target(관찰, 숏 비중 목표 미달) | 1019.86 | 1.4036183558 | 1019 | 3.0600600601 | 0.1157998037 | 1.2655745708 | 2 | -0.38624746 |

## Broad Pool Negative Control(넓은 풀 부정 대조)

| candidate_id | candidate_status | net_profit | profit_factor | trade_density_per_business_day | short_share | synthetic_short_profit_factor | selection_score |
| --- | --- | --- | --- | --- | --- | --- | --- |
| bo90_broad_h17_20_ps0440_margin080_control | watch_short_share_below_target(관찰, 숏 비중 목표 미달) | 1044.49 | 1.4158388603 | 3.0510510511 | 0.1102362205 | 1.7848439305 | 72.746266514 |
| bo92_broad_h17_18_20_ps0445_margin085_control | watch_short_share_below_target(관찰, 숏 비중 목표 미달) | 1009.2 | 1.3991918067 | 3.048048048 | 0.1083743842 | 1.6561249444 | 40.513518534 |
| bo91_broad_h16_17_20_ps0445_margin080_control | rejected_synthetic_overlap(거절, 합성 거래 겹침) | 1067.36 | 1.4132149882 | 3.0990990991 | 0.1240310078 | 1.5601999121 | -10.791990956 |

## Stress Slices(압박 조각)

| axis | segment_id | net_profit | profit_factor | trade_count | short_share | segment_status |
| --- | --- | --- | --- | --- | --- | --- |
| quarter(분기) | 2025Q1 | 161.91 | 1.3653943366 | 177 | 0.2033898305 | positive(양수) |
| quarter(분기) | 2025Q2 | 307.37 | 1.4041045463 | 263 | 0.0874524715 | positive(양수) |
| quarter(분기) | 2025Q3 | 56.93 | 1.2087385049 | 134 | 0.0746268657 | positive(양수) |
| quarter(분기) | 2025Q4 | 276.45 | 1.4978703479 | 223 | 0.1121076233 | positive(양수) |
| quarter(분기) | 2026Q1 | 211.22 | 1.5325903326 | 181 | 0.1602209945 | positive(양수) |
| quarter(분기) | 2026Q2 | 23.29 | 1.2319721116 | 46 | 0.0 | positive(양수) |
| month(월) | 2025-01 | 76.45 | 1.3382189642 | 89 | 0.1011235955 | positive(양수) |
| month(월) | 2025-02 | 94.73 | 1.5334572281 | 74 | 0.1756756757 | positive(양수) |
| month(월) | 2025-03 | -9.26 | 0.7656451654 | 14 | 1.0 | stress_watch(압박 관찰) |
| month(월) | 2025-04 | 205.24 | 1.4179957109 | 121 | 0.1404958678 | positive(양수) |
| month(월) | 2025-05 | 43.41 | 1.2756472538 | 75 | 0.0666666667 | positive(양수) |
| month(월) | 2025-06 | 58.72 | 1.5236778739 | 67 | 0.0149253731 | positive(양수) |
| month(월) | 2025-07 | 9.23 | 1.1305626653 | 35 | 0.0571428571 | positive(양수) |
| month(월) | 2025-08 | 10.8 | 1.1045971224 | 46 | 0.1086956522 | positive(양수) |

## Short Source Segments(숏 원천 조각)

| axis | segment_id | synthetic_short_trade_count | synthetic_short_net_profit | synthetic_short_profit_factor | segment_status |
| --- | --- | --- | --- | --- | --- |
| entry_hour(진입시) | 17 | 36 | 29.38 | 1.2655745708 | positive_clue(긍정 단서) |
| entry_hour(진입시) | 20 | 6 | 14.61 | 4.1559395248 | positive_clue(긍정 단서) |
| entry_month(진입월) | 2025-01 | 3 | 18.84 | 21.7717750827 | watch_or_negative(관찰 또는 음수) |
| entry_month(진입월) | 2025-02 | 4 | 33.3 | 999.0 | positive_clue(긍정 단서) |
| entry_month(진입월) | 2025-03 | 7 | -12.4 | 0.5314542638 | watch_or_negative(관찰 또는 음수) |
| entry_month(진입월) | 2025-04 | 3 | -22.65 | 0.2061205174 | watch_or_negative(관찰 또는 음수) |
| entry_month(진입월) | 2025-05 | 1 | -4.93 | 0.0 | watch_or_negative(관찰 또는 음수) |
| entry_month(진입월) | 2025-07 | 1 | -2.86 | 0.0 | watch_or_negative(관찰 또는 음수) |
| entry_month(진입월) | 2025-08 | 4 | -7.67 | 0.5012360135 | watch_or_negative(관찰 또는 음수) |
| entry_month(진입월) | 2025-09 | 2 | 1.92 | 3.0338624339 | watch_or_negative(관찰 또는 음수) |
| entry_month(진입월) | 2025-10 | 1 | 3.48 | 999.0 | watch_or_negative(관찰 또는 음수) |
| entry_month(진입월) | 2025-11 | 1 | 0.1 | 999.0 | watch_or_negative(관찰 또는 음수) |
| entry_month(진입월) | 2025-12 | 2 | -10.07 | 0.452270873 | watch_or_negative(관찰 또는 음수) |
| entry_month(진입월) | 2026-01 | 3 | 4.47 | 1.5521927116 | watch_or_negative(관찰 또는 음수) |

## Proxy/MT5 Diff Plan(프록시/MT5 차이 계획)

| comparison_id | mt5_net_profit | proxy_net_profit | net_diff_proxy_minus_mt5 | mt5_profit_factor | proxy_profit_factor | usability |
| --- | --- | --- | --- | --- | --- | --- |
| bo_proxy_vs_bk_mt5_runtime_probe(BO 프록시 대 BK MT5 런타임 탐침) | 959.64 | 1037.17 | 77.53 | 1.3820937835 | 1.4101564709 | scout_only_requires_BP_review_then_MT5_reprobe(정찰 전용, BP 검토 뒤 MT5 재탐침 필요) |

## Guardrails(가드레일)

| audit_id | status | evidence | effect |
| --- | --- | --- | --- |
| no_exact_month_rule(정확 월 규칙 없음) | passed | candidate definitions use hour/probability/margin only(후보 정의는 시간/확률/마진만 사용) | future losing month shortcut(미래 손실 월 지름길)을 차단한다. |
| no_top_n_rule(top_n 규칙 없음) | passed | all masks are threshold or band rules(모든 마스크는 임계값 또는 밴드 규칙) | 거래 수를 쪼개서 성과를 꾸미지 않는다. |
| synthetic_overlap_audit(합성 겹침 감사) | passed | synthetic_overlap_count=0 | one-position proxy(단일 포지션 프록시) 의미를 유지한다. |
| same_tape_overfit_boundary(동일 테이프 과적합 경계) | passed_with_watch(관찰 포함 통과) | month_bad_count=2; broad_clean_hard_pass_count=0 | BO 결과를 패키지 후보가 아니라 BP 검토 대상으로 낮춰 둔다. |
| external_verification_boundary(외부 검증 경계) | out_of_scope_by_claim(주장 범위 밖) | no new MT5 execution in BO(BO 새 MT5 실행 없음) | runtime authority(런타임 권위)를 만들지 않는다. |

## BP Queue(BP 대기열)

| queue_rank | queue_id | action | success_criteria |
| --- | --- | --- | --- |
| 1 | bp01_review_bo_candidate_stress_and_package_gate | review BO selected candidate stress and package gate(BO 선택 후보 압박과 패키지 게이트 검토) | separate proxy clue from package eligibility(프록시 단서와 패키지 적격성 분리) |
| 2 | bp02_proxy_mt5_diff_reprobe_plan | prepare proxy/MT5 diff and narrow reprobe plan(프록시/MT5 차이와 좁은 재탐침 계획 준비) | explicit diff, attribution, usability before any package(패키지 전 차이/귀속/활용성 명시) |
| 3 | bp03_open_next_offensive_seed_if_package_gate_fails | if stress gate fails, preserve clue and open next offensive seed(압박 게이트 실패 시 단서 보존 후 다음 공격 씨앗 열기) | failure memory becomes constraint, not blocker loop(실패 기억을 제약으로 바꾸고 반복 차단으로 만들지 않음) |

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| scope_completion_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BO/quality_rule_surface.csv | BO 후보 표면과 선택 후보를 모두 남겼다. |
| kpi_contract_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BO/selected_quality_candidate.json | net/PF/expectancy/DD/recovery/trades/short share를 같이 점검했다. |
| data_integrity_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BO/overfit_guardrail_audit.csv | timestamp-safe entry-known rule(시점 안전 진입기지 규칙)과 no top_n(상위 N개 없음)을 확인했다. |
| model_validation_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BO/model_validation_receipt.json | 새 learned model(학습 모델)이나 ONNX(온엑스) 권위를 만들지 않고 rule surface(규칙 표면)로 제한했다. |
| proxy_mt5_comparison_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BO/proxy_mt5_diff_plan.csv | proxy expected value(프록시 예상값)를 MT5 runtime probe(MT5 런타임 탐침)와 분리 비교했다. |
| skill_receipt_lint | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BO | 실험/데이터/모델/계보/판정 영수증을 남겼다. |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BO/run364BP_review_queue.csv | 다음 BP 검토 대기열과 필수 게이트를 연결했다. |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364BO/claim_boundary_receipt.json | runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)를 차단했다. |

## Boundary(경계)

BO is proxy scout only(BO는 프록시 정찰 전용). No new MT5 execution(새 MT5 실행 없음), no forward pass(전진 통과 없음), no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음), no Goal Achieve(목표 달성 없음).
