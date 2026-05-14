# Stage56 Reopen Goal Progress Log(56단계 재개 목표 진행 기록)

- packet_id(묶음 ID): `stage56_reopen_goal_v1`
- stage_status(단계 상태): `active_in_progress(활성 진행 중)`
- latest_batch(최신 후보 묶음): `run50BI_stage56_extratrees_raw_density_microcooldown_v1`
- selected_research_baseline(선택 연구 기준선): `none`
- terminal_condition(종료 조건): useful BaselineAdapter(유용한 기준선 어댑터) hard condition(강한 완료 조건) not_satisfied(미충족)
- non_final_prior_packets(비최종 이전 묶음): `stage56_closeout_v1`, `stage56_reopened_closeout_v2`

Stage56(56단계)은 unfinished optimization campaign(미완 최적화 캠페인)으로 open(열림) 상태다.
Effect(효과): progress log(진행 기록)는 Stage56(56단계)을 닫지 않고 다음 hypothesis branch(가설 가지)를 정한다.

## Current Bottleneck(현재 병목)

- density(밀도): selected_research_baseline(선택 연구 기준선)은 validation/OOS(검증/표본외) 모두 5+ trades/day(일 거래 수)를 요구한다.
- Tier B OOS damage(Tier B 표본외 손상): Tier B fallback-only OOS(Tier B 대체 전용 표본외)가 음수이면 disablement(비활성화) 근거가 필요하다.
- hold compression audit(보유 압축 감사): density gain(밀도 증가)이 same-move split-trading(동일 이동 분할 거래)인지 확인해야 한다.

## Prior Batch Summary(이전 묶음 요약)

- run50B/run50C/run50D(실행50B/50C/50D)는 preserved intermediate evidence(보존 중간 근거)이며 final closeout(최종 종료)이 아니다.
- d390h10(변형)는 stronger candidate(강한 후보)일 뿐 selected_research_baseline(선택 연구 기준선)이 아니다. 효과(effect, 효과): 품질 참조는 남기지만 Stage56(56단계)을 닫지 않는다.
- d38h10(변형)는 prior candidate/reference(이전 후보/참조)일 뿐 selected_research_baseline(선택 연구 기준선)이 아니다.
- d35h07(변형)는 density frontier(밀도 경계)였지만 quality(품질)가 실패해 selected_research_baseline(선택 연구 기준선)이 아니다.
- run50E(실행50E)는 d340h06_ab_b040/d350h06_ab_b040(변형)이 validation/OOS(검증/표본외) 모두 5+ trades/day(일 거래 수)에 도달했지만 PF(수익 팩터), cost-stressed expectancy(비용 압박 기대값), same-move audit(동일 이동 감사)가 실패했다.
- run50F(실행50F)는 re-entry cooldown(재진입 쿨다운)과 stricter Tier B(더 엄격한 Tier B)를 시험했지만 OOS density(표본외 밀도), PF(수익 팩터), cost-stressed expectancy(비용 압박 기대값), Tier B fallback-only OOS(Tier B 대체 전용 표본외)가 기준을 통과하지 못했다.
- selected_research_baseline(선택 연구 기준선)은 계속 none(없음)이다. 효과(effect, 효과): 다음 hypothesis branch(가설 가지)를 이어가며 Stage56(56단계)을 open(열림)으로 유지한다.

## Attempted Variants(시도 변형)

| variant(변형) | hypothesis family(가설군) | fallback(대체) | report paths(보고서 경로) | val/day(검증/일) | OOS/day(표본외/일) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) | reason(이유) |
|---|---|---:|---|---:|---:|---:|---:|---:|---:|---|
| et40h3c0_s240l150_r001_a | raw_density_short_hold_control_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BI/et40h3c0_s240l150_r001_a/mt5/reports/Project_Obsidian_Prime_v2_run50BI_et40h3c0_s240l150_r001_a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BI/et40h3c0_s240l150_r001_a/mt5/reports/Project_Obsidian_Prime_v2_run50BI_et40h3c0_s240l150_r001_a_logreg_deep_v1_routed_oos.htm | 8.508197 | 6.410256 | 0.97 | 1.12 | -114.55 | 284.7 | validation_net_positive; validation_pf; cost_stressed_expectancy; same_move_density |
| et40h3c3_s240l150_r001_a | raw_density_microcooldown_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BI/et40h3c3_s240l150_r001_a/mt5/reports/Project_Obsidian_Prime_v2_run50BI_et40h3c3_s240l150_r001_a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BI/et40h3c3_s240l150_r001_a/mt5/reports/Project_Obsidian_Prime_v2_run50BI_et40h3c3_s240l150_r001_a_logreg_deep_v1_routed_oos.htm | 5.846995 | 4.420513 | 0.99 | 1.14 | -25.18 | 225.85 | oos_density; validation_net_positive; validation_pf; cost_stressed_expectancy |
| et40h4c3_s240l150_r001_a | raw_density_microcooldown_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BI/et40h4c3_s240l150_r001_a/mt5/reports/Project_Obsidian_Prime_v2_run50BI_et40h4c3_s240l150_r001_a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BI/et40h4c3_s240l150_r001_a/mt5/reports/Project_Obsidian_Prime_v2_run50BI_et40h4c3_s240l150_r001_a_logreg_deep_v1_routed_oos.htm | 5.803279 | 4.333333 | 0.96 | 1.11 | -99.1 | 219.13 | oos_density; validation_net_positive; validation_pf; cost_stressed_expectancy |
| et40h4c3_s235l145_r001_a | raw_density_threshold_expansion_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BI/et40h4c3_s235l145_r001_a/mt5/reports/Project_Obsidian_Prime_v2_run50BI_et40h4c3_s235l145_r001_a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BI/et40h4c3_s235l145_r001_a/mt5/reports/Project_Obsidian_Prime_v2_run50BI_et40h4c3_s235l145_r001_a_logreg_deep_v1_routed_oos.htm | 5.803279 | 4.333333 | 0.96 | 1.11 | -99.1 | 219.13 | oos_density; validation_net_positive; validation_pf; cost_stressed_expectancy |
| et40h4c3_s230l140_r001_a | raw_density_threshold_expansion_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BI/et40h4c3_s230l140_r001_a/mt5/reports/Project_Obsidian_Prime_v2_run50BI_et40h4c3_s230l140_r001_a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BI/et40h4c3_s230l140_r001_a/mt5/reports/Project_Obsidian_Prime_v2_run50BI_et40h4c3_s230l140_r001_a_logreg_deep_v1_routed_oos.htm | 5.803279 | 4.333333 | 0.96 | 1.11 | -99.1 | 219.13 | oos_density; validation_net_positive; validation_pf; cost_stressed_expectancy |
| et40h4c3_s240l150_r005_a | raw_density_rearm_quality_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BI/et40h4c3_s240l150_r005_a/mt5/reports/Project_Obsidian_Prime_v2_run50BI_et40h4c3_s240l150_r005_a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BI/et40h4c3_s240l150_r005_a/mt5/reports/Project_Obsidian_Prime_v2_run50BI_et40h4c3_s240l150_r005_a_logreg_deep_v1_routed_oos.htm | 5.617486 | 4.123077 | 0.92 | 1.34 | -186.86 | 545.53 | oos_density; validation_net_positive; validation_pf; cost_stressed_expectancy |
| et40h4c6_s240l150_r001_a | raw_density_cooldown_stress_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BI/et40h4c6_s240l150_r001_a/mt5/reports/Project_Obsidian_Prime_v2_run50BI_et40h4c6_s240l150_r001_a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BI/et40h4c6_s240l150_r001_a/mt5/reports/Project_Obsidian_Prime_v2_run50BI_et40h4c6_s240l150_r001_a_logreg_deep_v1_routed_oos.htm | 4.579235 | 3.435897 | 1.06 | 1.27 | 119.63 | 367.74 | validation_density; oos_density; validation_pf; cost_stressed_expectancy |
| et40h4c3_s240l150_r001_b | raw_density_microcooldown_tier_b_check | true | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BI/et40h4c3_s240l150_r001_b/mt5/reports/Project_Obsidian_Prime_v2_run50BI_et40h4c3_s240l150_r001_b_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BI/et40h4c3_s240l150_r001_b/mt5/reports/Project_Obsidian_Prime_v2_run50BI_et40h4c3_s240l150_r001_b_logreg_deep_v1_routed_oos.htm | 5.841530 | 4.415385 | 0.96 | 1.14 | -98.55 | 265.08 | oos_density; validation_net_positive; validation_pf; cost_stressed_expectancy |

## Tier Views(티어 보기)

| variant(변형) | Tier A val/OOS(Tier A 검증/표본외) | Tier B fallback-only val/OOS(Tier B 대체 전용 검증/표본외) | A+B actual routed val/OOS(A+B 실제 라우팅 검증/표본외) | Tier B contribution(Tier B 기여) |
|---|---|---|---|---|
| et40h3c0_s240l150_r001_a | net -114.55/284.7, PF 0.97/1.12 | net -90.93/-8.73, PF 0.02/0.76 | net -114.55/284.7, PF 0.97/1.12 | fallback bars None/None |
| et40h3c3_s240l150_r001_a | net -25.18/225.85, PF 0.99/1.14 | net -70.57/1.81, PF 0.03/1.08 | net -25.18/225.85, PF 0.99/1.14 | fallback bars None/None |
| et40h4c3_s240l150_r001_a | net -99.1/219.13, PF 0.96/1.11 | net -87.87/8.49, PF 0.05/1.39 | net -99.1/219.13, PF 0.96/1.11 | fallback bars None/None |
| et40h4c3_s235l145_r001_a | net -99.1/219.13, PF 0.96/1.11 | net -87.87/8.49, PF 0.05/1.39 | net -99.1/219.13, PF 0.96/1.11 | fallback bars None/None |
| et40h4c3_s230l140_r001_a | net -99.1/219.13, PF 0.96/1.11 | net -87.87/8.49, PF 0.05/1.39 | net -99.1/219.13, PF 0.96/1.11 | fallback bars None/None |
| et40h4c3_s240l150_r005_a | net -186.86/545.53, PF 0.92/1.34 | net -87.87/8.49, PF 0.05/1.39 | net -186.86/545.53, PF 0.92/1.34 | fallback bars None/None |
| et40h4c6_s240l150_r001_a | net 119.63/367.74, PF 1.06/1.27 | net -7.12/-10.32, PF 0.39/0.65 | net 119.63/367.74, PF 1.06/1.27 | fallback bars None/None |
| et40h4c3_s240l150_r001_b | net -99.1/219.13, PF 0.96/1.11 | net -87.87/8.49, PF 0.05/1.39 | net -98.55/265.08, PF 0.96/1.14 | fallback bars None/None |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture ratio(MFE 포착 비율) | winner truncation(승자 절단) | loser escape(패자 탈출) | re-entry 3/6/12(재진입 3/6/12봉) | same-move ratio(동일 이동 비율) | cost-stressed exp(비용 압박 기대값) | cooldown survives(쿨다운 생존) |
|---|---|---:|---:|---:|---|---:|---:|---:|
| et40h3c0_s240l150_r001_a | validation_is | 0.611801 | 0.327935 | 0.268382 | 833/1032/1138 | 0.730893 | -0.573571 | False |
| et40h3c0_s240l150_r001_a | oos | 0.609866 | 0.339683 | 0.303226 | 714/884/958 | 0.766400 | -0.272240 | False |
| et40h3c3_s240l150_r001_a | validation_is | 0.615517 | 0.322772 | 0.284956 | 94/469/632 | 0.590654 | -0.523533 | False |
| et40h3c3_s240l150_r001_a | oos | 0.606129 | 0.346512 | 0.314815 | 102/454/564 | 0.654292 | -0.237993 | False |
| et40h4c3_s240l150_r001_a | validation_is | 0.604385 | 0.336170 | 0.295608 | 175/489/634 | 0.596987 | -0.593315 | False |
| et40h4c3_s240l150_r001_a | oos | 0.604351 | 0.329356 | 0.326291 | 157/444/557 | 0.659172 | -0.240675 | False |
| et40h4c3_s235l145_r001_a | validation_is | 0.604385 | 0.336170 | 0.295608 | 175/489/634 | 0.596987 | -0.593315 | False |
| et40h4c3_s235l145_r001_a | oos | 0.604351 | 0.329356 | 0.326291 | 157/444/557 | 0.659172 | -0.240675 | False |
| et40h4c3_s230l140_r001_a | validation_is | 0.604385 | 0.336170 | 0.295608 | 175/489/634 | 0.596987 | -0.593315 | False |
| et40h4c3_s230l140_r001_a | oos | 0.604351 | 0.329356 | 0.326291 | 157/444/557 | 0.659172 | -0.240675 | False |
| et40h4c3_s240l150_r005_a | validation_is | 0.596781 | 0.347826 | 0.283451 | 173/431/588 | 0.571984 | -0.681770 | False |
| et40h4c3_s240l150_r005_a | oos | 0.610452 | 0.330120 | 0.334190 | 140/363/510 | 0.634328 | 0.178520 | False |
| et40h4c6_s240l150_r001_a | validation_is | 0.601633 | 0.339623 | 0.291221 | 129/130/425 | 0.507160 | -0.357243 | False |
| et40h4c6_s240l150_r001_a | oos | 0.596631 | 0.353982 | 0.320242 | 109/111/368 | 0.549254 | 0.048866 | False |
| et40h4c3_s240l150_r001_b | validation_is | 0.604396 | 0.334746 | 0.301508 | 176/494/640 | 0.598690 | -0.592189 | False |
| et40h4c3_s240l150_r001_b | oos | 0.608310 | 0.319444 | 0.326340 | 156/447/568 | 0.659698 | -0.192125 | False |

## Current Read(현재 판독)

- latest_best_variant(최신 최선 변형): `et40h4c6_s240l150_r001_a`
- current_frontier_candidate(현재 최전선 후보): `run50BH/et40h6_r001_a`
- selected_research_baseline(선택 연구 기준선): `none`
- stage56_remains_open(56단계 열림 유지): `True`
- next_hypothesis_branch(다음 가설 가지): `run50BJ_cooldown_aware_independent_source_branch`
