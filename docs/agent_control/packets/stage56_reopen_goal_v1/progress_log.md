# Stage56 Reopen Goal Progress Log(56단계 재개 목표 진행 기록)

- packet_id(묶음 ID): `stage56_reopen_goal_v1`
- stage_status(단계 상태): `active_in_progress(활성 진행 중)`
- latest_batch(최신 후보 묶음): `run50AR_stage56_extratrees_validation_density_repair_v1`
- selected_research_baseline(선택 연구 기준선): `none`
- terminal_condition(종료 조건): useful BaselineAdapter(유용한 기준선 어댑터) hard condition(강한 완료 조건) satisfied(충족)
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
| et40s25_c0_h8_a | cooldown_density_repair_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AR/et40s25_c0_h8_a/mt5/reports/Project_Obsidian_Prime_v2_run50AR_et40s25_c0_h8_a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AR/et40s25_c0_h8_a/mt5/reports/Project_Obsidian_Prime_v2_run50AR_et40s25_c0_h8_a_logreg_deep_v1_routed_oos.htm | 6.606557 | 4.861538 | 1.02 | 1.31 | 61.18 | 765.43 | oos_density; validation_pf; cost_stressed_expectancy; same_move_density |
| et40s25_c4_h8_a | cooldown_density_repair_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AR/et40s25_c4_h8_a/mt5/reports/Project_Obsidian_Prime_v2_run50AR_et40s25_c4_h8_a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AR/et40s25_c4_h8_a/mt5/reports/Project_Obsidian_Prime_v2_run50AR_et40s25_c4_h8_a_logreg_deep_v1_routed_oos.htm | 5.420765 | 3.923077 | 1.01 | 1.28 | 29.91 | 554.97 | oos_density; validation_pf; cost_stressed_expectancy; same_move_density |
| et40s25_c0_h6_a | hold_compression_density_repair_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AR/et40s25_c0_h6_a/mt5/reports/Project_Obsidian_Prime_v2_run50AR_et40s25_c0_h6_a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AR/et40s25_c0_h6_a/mt5/reports/Project_Obsidian_Prime_v2_run50AR_et40s25_c0_h6_a_logreg_deep_v1_routed_oos.htm | 7.404372 | 5.502564 | 1.04 | 1.25 | 147.86 | 655.4 | validation_pf; cost_stressed_expectancy; same_move_density; tier_b_rule |
| et40s25_c4_h6_a | hold_compression_density_repair_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AR/et40s25_c4_h6_a/mt5/reports/Project_Obsidian_Prime_v2_run50AR_et40s25_c4_h6_a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AR/et40s25_c4_h6_a/mt5/reports/Project_Obsidian_Prime_v2_run50AR_et40s25_c4_h6_a_logreg_deep_v1_routed_oos.htm | 5.595628 | 4.117949 | 0.91 | 1.25 | -238.57 | 481.02 | oos_density; validation_net_positive; validation_pf; cost_stressed_expectancy |
| et40adxweak_c0_h8_a | weak_trend_firewall_quality_repair_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AR/et40adxweak_c0_h8_a/mt5/reports/Project_Obsidian_Prime_v2_run50AR_et40adxweak_c0_h8_a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AR/et40adxweak_c0_h8_a/mt5/reports/Project_Obsidian_Prime_v2_run50AR_et40adxweak_c0_h8_a_logreg_deep_v1_routed_oos.htm | 4.961749 | 3.492308 | 1.0 | 1.36 | -0.32 | 646.97 | validation_density; oos_density; validation_net_positive; validation_pf |
| et40adxweak_c0_h6_a | weak_trend_firewall_quality_repair_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AR/et40adxweak_c0_h6_a/mt5/reports/Project_Obsidian_Prime_v2_run50AR_et40adxweak_c0_h6_a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AR/et40adxweak_c0_h6_a/mt5/reports/Project_Obsidian_Prime_v2_run50AR_et40adxweak_c0_h6_a_logreg_deep_v1_routed_oos.htm | 5.535519 | 4.025641 | 1.02 | 1.16 | 49.59 | 321.81 | oos_density; validation_pf; cost_stressed_expectancy; same_move_density |
| et40s25_c0_h8_b | tier_b_damage_control_comparison | true | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AR/et40s25_c0_h8_b/mt5/reports/Project_Obsidian_Prime_v2_run50AR_et40s25_c0_h8_b_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AR/et40s25_c0_h8_b/mt5/reports/Project_Obsidian_Prime_v2_run50AR_et40s25_c0_h8_b_logreg_deep_v1_routed_oos.htm | 6.644809 | 4.948718 | 1.03 | 1.31 | 94.67 | 763.47 | oos_density; validation_pf; cost_stressed_expectancy; same_move_density |

## Tier Views(티어 보기)

| variant(변형) | Tier A val/OOS(Tier A 검증/표본외) | Tier B fallback-only val/OOS(Tier B 대체 전용 검증/표본외) | A+B actual routed val/OOS(A+B 실제 라우팅 검증/표본외) | Tier B contribution(Tier B 기여) |
|---|---|---|---|---|
| et40s25_c0_h8_a | net 61.18/765.43, PF 1.02/1.31 | net -80.17/-9.55, PF 0.12/0.78 | net 61.18/765.43, PF 1.02/1.31 | fallback bars None/None |
| et40s25_c4_h8_a | net 29.91/554.97, PF 1.01/1.28 | net -1.06/6.01, PF 0.89/1.18 | net 29.91/554.97, PF 1.01/1.28 | fallback bars None/None |
| et40s25_c0_h6_a | net 147.86/655.4, PF 1.04/1.25 | net -81.14/9.54, PF 0.12/1.41 | net 147.86/655.4, PF 1.04/1.25 | fallback bars None/None |
| et40s25_c4_h6_a | net -238.57/481.02, PF 0.91/1.25 | net 2.33/-11.35, PF 1.28/0.54 | net -238.57/481.02, PF 0.91/1.25 | fallback bars None/None |
| et40adxweak_c0_h8_a | net -0.32/646.97, PF 1.0/1.36 | net -84.92/-4.81, PF 0.04/0.83 | net -0.32/646.97, PF 1.0/1.36 | fallback bars None/None |
| et40adxweak_c0_h6_a | net 49.59/321.81, PF 1.02/1.16 | net -18.09/12.74, PF 0.34/1.67 | net 49.59/321.81, PF 1.02/1.16 | fallback bars None/None |
| et40s25_c0_h8_b | net 61.18/765.43, PF 1.02/1.31 | net -80.17/-9.55, PF 0.12/0.78 | net 94.67/763.47, PF 1.03/1.31 | fallback bars None/None |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture ratio(MFE 포착 비율) | winner truncation(승자 절단) | loser escape(패자 탈출) | re-entry 3/6/12(재진입 3/6/12봉) | same-move ratio(동일 이동 비율) | cost-stressed exp(비용 압박 기대값) | cooldown survives(쿨다운 생존) |
|---|---|---:|---:|---:|---|---:|---:|---:|
| et40s25_c0_h8_a | validation_is | 0.599932 | 0.357678 | 0.265185 | 653/759/825 | 0.682382 | -0.449396 | False |
| et40s25_c0_h8_a | oos | 0.605240 | 0.352423 | 0.297571 | 557/629/684 | 0.721519 | 0.307416 | False |
| et40s25_c4_h8_a | validation_is | 0.599044 | 0.351852 | 0.273214 | 249/528/588 | 0.592742 | -0.469849 | False |
| et40s25_c4_h8_a | oos | 0.613120 | 0.330460 | 0.328537 | 204/437/486 | 0.635294 | 0.225451 | False |
| et40s25_c0_h6_a | validation_is | 0.596523 | 0.357143 | 0.267930 | 778/882/966 | 0.712915 | -0.390878 | False |
| et40s25_c0_h6_a | oos | 0.604692 | 0.336538 | 0.294756 | 677/741/802 | 0.747437 | 0.110811 | False |
| et40s25_c4_h6_a | validation_is | 0.598616 | 0.352679 | 0.265625 | 234/539/632 | 0.617188 | -0.732979 | False |
| et40s25_c4_h6_a | oos | 0.596894 | 0.364796 | 0.296837 | 180/456/524 | 0.652553 | 0.099029 | False |
| et40adxweak_c0_h8_a | validation_is | 0.602248 | 0.346835 | 0.265107 | 457/523/563 | 0.620044 | -0.500352 | False |
| et40adxweak_c0_h8_a | oos | 0.615395 | 0.329114 | 0.304110 | 375/411/438 | 0.643172 | 0.450029 | False |
| et40adxweak_c0_h6_a | validation_is | 0.605179 | 0.341410 | 0.261181 | 550/612/660 | 0.651530 | -0.451046 | False |
| et40adxweak_c0_h6_a | oos | 0.598988 | 0.341398 | 0.297821 | 473/509/536 | 0.682803 | -0.090051 | False |
| et40s25_c0_h8_b | validation_is | 0.599499 | 0.358736 | 0.266962 | 656/761/828 | 0.680921 | -0.422146 | False |
| et40s25_c0_h8_b | oos | 0.602494 | 0.356838 | 0.293763 | 561/637/699 | 0.724352 | 0.291161 | False |

## Current Read(현재 판독)

- best_variant(최선 변형): `et40s25_c0_h6_a`
- selected_research_baseline(선택 연구 기준선): `none`
- stage56_remains_open(56단계 열림 유지): `True`
- judgment(판정): `et40s25_c0_h6_a`는 validation/OOS density(검증/표본외 밀도) `7.404372` / `5.502564`와 OOS PF(표본외 수익 팩터) `1.25`를 만들었지만 validation PF(검증 수익 팩터) `1.04`, validation cost-stressed expectancy(검증 비용 압박 기대값) `-0.390878`, same-move ratio(동일 이동 비율) `0.712915` / `0.747437`, 12-bar cooldown after density(12봉 쿨다운 후 밀도) `2.125683` / `1.389744`로 실패했다. Effect(효과): density gain(밀도 증가)은 실제 새 기회보다 split re-entry(분할 재진입)에 더 가깝다.
- next_hypothesis_branch(다음 가설 가지): `run50AS_extratrees_rearm_real_density_guard`
