# Stage56 Reopen Goal Progress Log(56단계 재개 목표 진행 기록)

- packet_id(묶음 ID): `stage56_reopen_goal_v1`
- stage_status(단계 상태): `active_in_progress(활성 진행 중)`
- latest_batch(최신 후보 묶음): `run50BH_stage56_extratrees_light_rearm_density_recovery_v1`
- selected_research_baseline(선택 연구 기준선): `none`
- terminal_condition(종료 조건): selected_research_baseline(선택 연구 기준선) found(발견)
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
| et40h6_r001_a | light_rearm_density_recovery_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BH/et40h6_r001_a/mt5/reports/Project_Obsidian_Prime_v2_run50BH_et40h6_r001_a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BH/et40h6_r001_a/mt5/reports/Project_Obsidian_Prime_v2_run50BH_et40h6_r001_a_logreg_deep_v1_routed_oos.htm | 6.846995 | 5.102564 | 1.1 | 1.26 | 313.49 | 613.58 | cost_stressed_expectancy; same_move_density; tier_b_rule |
| et40h6_r005_a | light_rearm_density_recovery_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BH/et40h6_r005_a/mt5/reports/Project_Obsidian_Prime_v2_run50BH_et40h6_r005_a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BH/et40h6_r005_a/mt5/reports/Project_Obsidian_Prime_v2_run50BH_et40h6_r005_a_logreg_deep_v1_routed_oos.htm | 6.677596 | 4.902564 | 1.1 | 1.43 | 314.45 | 911.32 | oos_density; cost_stressed_expectancy; same_move_density; tier_b_rule |
| et40h6_r010_a | light_rearm_density_recovery_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BH/et40h6_r010_a/mt5/reports/Project_Obsidian_Prime_v2_run50BH_et40h6_r010_a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BH/et40h6_r010_a/mt5/reports/Project_Obsidian_Prime_v2_run50BH_et40h6_r010_a_logreg_deep_v1_routed_oos.htm | 6.344262 | 4.620513 | 1.18 | 1.38 | 505.33 | 743.61 | oos_density; cost_stressed_expectancy; same_move_density; tier_b_rule |
| et30h6_r001_a | leaf30_light_rearm_density_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BH/et30h6_r001_a/mt5/reports/Project_Obsidian_Prime_v2_run50BH_et30h6_r001_a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BH/et30h6_r001_a/mt5/reports/Project_Obsidian_Prime_v2_run50BH_et30h6_r001_a_logreg_deep_v1_routed_oos.htm | 7.142077 | 5.200000 | 1.04 | 1.35 | 140.74 | 818.43 | validation_pf; cost_stressed_expectancy; same_move_density; tier_b_rule |
| et30h6_r005_a | leaf30_light_rearm_density_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BH/et30h6_r005_a/mt5/reports/Project_Obsidian_Prime_v2_run50BH_et30h6_r005_a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BH/et30h6_r005_a/mt5/reports/Project_Obsidian_Prime_v2_run50BH_et30h6_r005_a_logreg_deep_v1_routed_oos.htm | 6.901639 | 5.035897 | 1.0 | 1.4 | -13.81 | 886.15 | validation_net_positive; validation_pf; cost_stressed_expectancy; same_move_density |
| et30h6_r005_b | leaf30_light_rearm_tier_b_damage_check | true | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BH/et30h6_r005_b/mt5/reports/Project_Obsidian_Prime_v2_run50BH_et30h6_r005_b_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BH/et30h6_r005_b/mt5/reports/Project_Obsidian_Prime_v2_run50BH_et30h6_r005_b_logreg_deep_v1_routed_oos.htm | 6.939891 | 5.128205 | 1.0 | 1.4 | 13.11 | 890.13 | validation_pf; cost_stressed_expectancy; same_move_density |

## Tier Views(티어 보기)

| variant(변형) | Tier A val/OOS(Tier A 검증/표본외) | Tier B fallback-only val/OOS(Tier B 대체 전용 검증/표본외) | A+B actual routed val/OOS(A+B 실제 라우팅 검증/표본외) | Tier B contribution(Tier B 기여) |
|---|---|---|---|---|
| et40h6_r001_a | net 313.49/613.58, PF 1.1/1.26 | net -82.3/8.19, PF 0.11/1.34 | net 313.49/613.58, PF 1.1/1.26 | fallback bars None/None |
| et40h6_r005_a | net 314.45/911.32, PF 1.1/1.43 | net -80.99/8.19, PF 0.11/1.34 | net 314.45/911.32, PF 1.1/1.43 | fallback bars None/None |
| et40h6_r010_a | net 505.33/743.61, PF 1.18/1.38 | net -80.99/8.19, PF 0.11/1.34 | net 505.33/743.61, PF 1.18/1.38 | fallback bars None/None |
| et30h6_r001_a | net 140.74/818.43, PF 1.04/1.35 | net -82.3/8.19, PF 0.11/1.34 | net 140.74/818.43, PF 1.04/1.35 | fallback bars None/None |
| et30h6_r005_a | net -13.81/886.15, PF 1.0/1.4 | net -80.99/8.19, PF 0.11/1.34 | net -13.81/886.15, PF 1.0/1.4 | fallback bars None/None |
| et30h6_r005_b | net -13.81/886.15, PF 1.0/1.4 | net -80.99/8.19, PF 0.11/1.34 | net 13.11/890.13, PF 1.0/1.4 | fallback bars None/None |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture ratio(MFE 포착 비율) | winner truncation(승자 절단) | loser escape(패자 탈출) | re-entry 3/6/12(재진입 3/6/12봉) | same-move ratio(동일 이동 비율) | cost-stressed exp(비용 압박 기대값) | cooldown survives(쿨다운 생존) |
|---|---|---:|---:|---:|---|---:|---:|---:|
| et40h6_r001_a | validation_is | 0.597153 | 0.355172 | 0.258544 | 625/761/857 | 0.683958 | -0.249808 | False |
| et40h6_r001_a | oos | 0.622472 | 0.310782 | 0.300766 | 552/650/715 | 0.718593 | 0.116663 | False |
| et40h6_r005_a | validation_is | 0.599127 | 0.352415 | 0.266968 | 562/721/822 | 0.672668 | -0.242676 | False |
| et40h6_r005_a | oos | 0.624715 | 0.306554 | 0.298137 | 474/594/673 | 0.703975 | 0.453264 | False |
| et40h6_r010_a | validation_is | 0.598202 | 0.355019 | 0.260032 | 471/633/755 | 0.650301 | -0.064746 | False |
| et40h6_r010_a | oos | 0.606429 | 0.324263 | 0.310870 | 387/513/609 | 0.675916 | 0.325316 | False |
| et30h6_r001_a | validation_is | 0.609525 | 0.352445 | 0.287115 | 681/815/898 | 0.687070 | -0.392318 | False |
| et30h6_r001_a | oos | 0.632943 | 0.298625 | 0.310891 | 531/649/735 | 0.724852 | 0.307130 | False |
| et30h6_r005_a | validation_is | 0.598487 | 0.367418 | 0.274052 | 600/758/851 | 0.673793 | -0.510934 | False |
| et30h6_r005_a | oos | 0.635997 | 0.295775 | 0.309278 | 471/609/700 | 0.712831 | 0.402393 | False |
| et30h6_r005_b | validation_is | 0.598681 | 0.368330 | 0.275762 | 597/759/854 | 0.672441 | -0.489677 | False |
| et30h6_r005_b | oos | 0.635023 | 0.299213 | 0.308943 | 471/618/714 | 0.714000 | 0.390130 | False |

## Current Read(현재 판독)

- best_variant(최선 변형): `et40h6_r001_a`
- selected_research_baseline(선택 연구 기준선): `none`
- stage56_remains_open(56단계 열림 유지): `True`
- next_hypothesis_branch(다음 가설 가지): `continue_density_repair_without_same_move_splitting_and_tier_b_damage_control`
