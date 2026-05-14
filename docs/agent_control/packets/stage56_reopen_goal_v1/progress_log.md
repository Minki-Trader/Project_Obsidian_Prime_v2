# Stage56 Reopen Goal Progress Log(56단계 재개 목표 진행 기록)

- packet_id(묶음 ID): `stage56_reopen_goal_v1`
- stage_status(단계 상태): `active_in_progress(활성 진행 중)`
- latest_batch(최신 후보 묶음): `run50BL_stage56_same_direction_cooldown_real_density_repair_v1`
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
| et40h3sd2_s240l150_r001_a | same_direction_cooldown_short_hold_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BL/et40h3sd2_s240l150_r001_a/mt5/reports/Project_Obsidian_Prime_v2_run50BL_et40h3sd2_s240l150_r001_a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BL/et40h3sd2_s240l150_r001_a/mt5/reports/Project_Obsidian_Prime_v2_run50BL_et40h3sd2_s240l150_r001_a_logreg_deep_v1_routed_oos.htm | 7.081967 | 5.307692 | 0.92 | 1.07 | -226.7 | 146.42 | validation_net_positive; validation_pf; oos_pf; cost_stressed_expectancy |
| et40h3sd3_s240l150_r001_a | same_direction_cooldown_short_hold_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BL/et40h3sd3_s240l150_r001_a/mt5/reports/Project_Obsidian_Prime_v2_run50BL_et40h3sd3_s240l150_r001_a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BL/et40h3sd3_s240l150_r001_a/mt5/reports/Project_Obsidian_Prime_v2_run50BL_et40h3sd3_s240l150_r001_a_logreg_deep_v1_routed_oos.htm | 6.633880 | 4.953846 | 0.97 | 1.08 | -74.06 | 149.01 | oos_density; validation_net_positive; validation_pf; oos_pf |
| et40h3sd4_s240l150_r001_a | same_direction_cooldown_short_hold_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BL/et40h3sd4_s240l150_r001_a/mt5/reports/Project_Obsidian_Prime_v2_run50BL_et40h3sd4_s240l150_r001_a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BL/et40h3sd4_s240l150_r001_a/mt5/reports/Project_Obsidian_Prime_v2_run50BL_et40h3sd4_s240l150_r001_a_logreg_deep_v1_routed_oos.htm | 6.289617 | 4.625641 | 0.89 | 1.1 | -279.01 | 181.38 | oos_density; validation_net_positive; validation_pf; cost_stressed_expectancy |
| et40h3sd3_s250l160_r001_a | same_direction_cooldown_threshold_pressure_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BL/et40h3sd3_s250l160_r001_a/mt5/reports/Project_Obsidian_Prime_v2_run50BL_et40h3sd3_s250l160_r001_a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BL/et40h3sd3_s250l160_r001_a/mt5/reports/Project_Obsidian_Prime_v2_run50BL_et40h3sd3_s250l160_r001_a_logreg_deep_v1_routed_oos.htm | 6.633880 | 4.953846 | 0.97 | 1.08 | -74.06 | 149.01 | oos_density; validation_net_positive; validation_pf; oos_pf |
| et40h4sd3_s250l160_r001_a | same_direction_cooldown_hold_balance_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BL/et40h4sd3_s250l160_r001_a/mt5/reports/Project_Obsidian_Prime_v2_run50BL_et40h4sd3_s250l160_r001_a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BL/et40h4sd3_s250l160_r001_a/mt5/reports/Project_Obsidian_Prime_v2_run50BL_et40h4sd3_s250l160_r001_a_logreg_deep_v1_routed_oos.htm | 6.333333 | 4.707692 | 1.0 | 1.21 | -3.73 | 412.04 | oos_density; validation_net_positive; validation_pf; cost_stressed_expectancy |
| et40h6sd3_s260l170_r001_a | same_direction_cooldown_anchor_stress_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BL/et40h6sd3_s260l170_r001_a/mt5/reports/Project_Obsidian_Prime_v2_run50BL_et40h6sd3_s260l170_r001_a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BL/et40h6sd3_s260l170_r001_a/mt5/reports/Project_Obsidian_Prime_v2_run50BL_et40h6sd3_s260l170_r001_a_logreg_deep_v1_routed_oos.htm | 5.994536 | 4.405128 | 1.02 | 1.24 | 65.68 | 503.79 | oos_density; validation_pf; cost_stressed_expectancy; same_move_density |

## Tier Views(티어 보기)

| variant(변형) | Tier A val/OOS(Tier A 검증/표본외) | Tier B fallback-only val/OOS(Tier B 대체 전용 검증/표본외) | A+B actual routed val/OOS(A+B 실제 라우팅 검증/표본외) | Tier B contribution(Tier B 기여) |
|---|---|---|---|---|
| et40h3sd2_s240l150_r001_a | net -226.7/146.42, PF 0.92/1.07 | net -73.21/1.81, PF 0.02/1.08 | net -226.7/146.42, PF 0.92/1.07 | fallback bars None/None |
| et40h3sd3_s240l150_r001_a | net -74.06/149.01, PF 0.97/1.08 | net -73.21/1.81, PF 0.02/1.08 | net -74.06/149.01, PF 0.97/1.08 | fallback bars None/None |
| et40h3sd4_s240l150_r001_a | net -279.01/181.38, PF 0.89/1.1 | net -88.64/1.81, PF 0.02/1.08 | net -279.01/181.38, PF 0.89/1.1 | fallback bars None/None |
| et40h3sd3_s250l160_r001_a | net -74.06/149.01, PF 0.97/1.08 | net -73.21/1.81, PF 0.02/1.08 | net -74.06/149.01, PF 0.97/1.08 | fallback bars None/None |
| et40h4sd3_s250l160_r001_a | net -3.73/412.04, PF 1.0/1.21 | net -87.87/8.87, PF 0.05/1.41 | net -3.73/412.04, PF 1.0/1.21 | fallback bars None/None |
| et40h6sd3_s260l170_r001_a | net 65.68/503.79, PF 1.02/1.24 | net -16.21/8.19, PF 0.39/1.34 | net 65.68/503.79, PF 1.02/1.24 | fallback bars None/None |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture ratio(MFE 포착 비율) | winner truncation(승자 절단) | loser escape(패자 탈출) | re-entry 3/6/12(재진입 3/6/12봉) | same-move ratio(동일 이동 비율) | cost-stressed exp(비용 압박 기대값) | cooldown survives(쿨다운 생존) |
|---|---|---:|---:|---:|---|---:|---:|---:|
| et40h3sd2_s240l150_r001_a | validation_is | 0.612617 | 0.332787 | 0.269679 | 382/728/871 | 0.672068 | -0.674923 | False |
| et40h3sd2_s240l150_r001_a | oos | 0.627348 | 0.311377 | 0.303371 | 322/635/732 | 0.707246 | -0.358531 | False |
| et40h3sd3_s240l150_r001_a | validation_is | 0.618915 | 0.319930 | 0.271028 | 182/610/781 | 0.643328 | -0.561005 | False |
| et40h3sd3_s240l150_r001_a | oos | 0.612449 | 0.336957 | 0.314229 | 160/543/662 | 0.685300 | -0.345745 | False |
| et40h3sd4_s240l150_r001_a | validation_is | 0.611338 | 0.330189 | 0.272142 | 174/503/706 | 0.613380 | -0.742407 | False |
| et40h3sd4_s240l150_r001_a | oos | 0.610130 | 0.335616 | 0.280172 | 145/422/592 | 0.656319 | -0.298914 | False |
| et40h3sd3_s250l160_r001_a | validation_is | 0.618915 | 0.319930 | 0.271028 | 182/610/781 | 0.643328 | -0.561005 | False |
| et40h3sd3_s250l160_r001_a | oos | 0.612449 | 0.336957 | 0.314229 | 160/543/662 | 0.685300 | -0.345745 | False |
| et40h4sd3_s250l160_r001_a | validation_is | 0.608930 | 0.326296 | 0.313480 | 228/574/725 | 0.625539 | -0.503218 | False |
| et40h4sd3_s250l160_r001_a | oos | 0.607062 | 0.341518 | 0.297872 | 187/491/618 | 0.673203 | -0.051155 | False |
| et40h6sd3_s260l170_r001_a | validation_is | 0.597859 | 0.354970 | 0.256623 | 265/554/692 | 0.630811 | -0.440128 | False |
| et40h6sd3_s260l170_r001_a | oos | 0.603358 | 0.346062 | 0.288636 | 211/469/573 | 0.667055 | 0.086484 | False |

## Current Read(현재 판독)

- best_variant(최선 변형): `et40h6sd3_s260l170_r001_a`
- selected_research_baseline(선택 연구 기준선): `none`
- stage56_remains_open(56단계 열림 유지): `True`
- next_hypothesis_branch(다음 가설 가지): `continue_density_repair_without_same_move_splitting_and_tier_b_damage_control`
