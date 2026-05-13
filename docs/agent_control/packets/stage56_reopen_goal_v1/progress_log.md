# Stage56 Reopen Goal Progress Log(56단계 재개 목표 진행 기록)

- packet_id(묶음 ID): `stage56_reopen_goal_v1`
- stage_status(단계 상태): `active_in_progress(활성 진행 중)`
- latest_batch(최신 후보 묶음): `run50AN_stage56_lgbm_fwd6_inverse_signal_probe_v1`
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
| inv6_s040l040_h3_b060 | inverse_high_density_symmetric | true | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AN/inv6_s040l040_h3_b060/mt5/reports/Project_Obsidian_Prime_v2_run50AN_inv6_s040l040_h3_b060_lgbm_fwd6_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AN/inv6_s040l040_h3_b060/mt5/reports/Project_Obsidian_Prime_v2_run50AN_inv6_s040l040_h3_b060_lgbm_fwd6_v1_routed_oos.htm | 9.327868852459016 | 6.887179487179488 | 0.89 | 0.94 | -465.22 | -185.52 | validation_net_positive; oos_net_positive; validation_pf; oos_pf |
| inv6_s042l040_h3_b060 | inverse_short_firewall_density | true | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AN/inv6_s042l040_h3_b060/mt5/reports/Project_Obsidian_Prime_v2_run50AN_inv6_s042l040_h3_b060_lgbm_fwd6_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AN/inv6_s042l040_h3_b060/mt5/reports/Project_Obsidian_Prime_v2_run50AN_inv6_s042l040_h3_b060_lgbm_fwd6_v1_routed_oos.htm | 8.721311475409836 | 6.4051282051282055 | 0.98 | 0.97 | -75.85 | -89.44 | validation_net_positive; oos_net_positive; validation_pf; oos_pf |
| inv6_s045l045_h3_b060 | inverse_mid_density_symmetric | true | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AN/inv6_s045l045_h3_b060/mt5/reports/Project_Obsidian_Prime_v2_run50AN_inv6_s045l045_h3_b060_lgbm_fwd6_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AN/inv6_s045l045_h3_b060/mt5/reports/Project_Obsidian_Prime_v2_run50AN_inv6_s045l045_h3_b060_lgbm_fwd6_v1_routed_oos.htm | 5.371584699453552 | 3.6256410256410256 | 1.11 | 1.05 | 265.28 | 84.42 | oos_density; oos_pf; cost_stressed_expectancy; same_move_density |
| inv6_s048l045_h4_b060 | inverse_run50am_direct_comparison | true | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AN/inv6_s048l045_h4_b060/mt5/reports/Project_Obsidian_Prime_v2_run50AN_inv6_s048l045_h4_b060_lgbm_fwd6_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AN/inv6_s048l045_h4_b060/mt5/reports/Project_Obsidian_Prime_v2_run50AN_inv6_s048l045_h4_b060_lgbm_fwd6_v1_routed_oos.htm | 4.163934426229508 | 2.8153846153846156 | 1.11 | 1.17 | 223.57 | 258.0 | validation_density; oos_density; cost_stressed_expectancy; same_move_density |

## Tier Views(티어 보기)

| variant(변형) | Tier A val/OOS(Tier A 검증/표본외) | Tier B fallback-only val/OOS(Tier B 대체 전용 검증/표본외) | A+B actual routed val/OOS(A+B 실제 라우팅 검증/표본외) | Tier B contribution(Tier B 기여) |
|---|---|---|---|---|
| inv6_s040l040_h3_b060 | net -432.68/-144.84, PF 0.9/0.95 | net 0.0/11.6, PF 0.0/2.15 | net -465.22/-185.52, PF 0.89/0.94 | fallback bars 2647/1250 |
| inv6_s042l040_h3_b060 | net -86.0/46.07, PF 0.98/1.02 | net -26.41/-6.36, PF 0.0/0.8 | net -75.85/-89.44, PF 0.98/0.97 | fallback bars 2647/1250 |
| inv6_s045l045_h3_b060 | net 243.16/128.22, PF 1.1/1.07 | net -5.18/6.86, PF 0.0/1.46 | net 265.28/84.42, PF 1.11/1.05 | fallback bars 2647/1250 |
| inv6_s048l045_h4_b060 | net 218.7/352.49, PF 1.1/1.23 | net 3.76/-15.0, PF 0.0/0.0 | net 223.57/258.0, PF 1.11/1.17 | fallback bars 2647/1250 |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture ratio(MFE 포착 비율) | winner truncation(승자 절단) | loser escape(패자 탈출) | re-entry 3/6/12(재진입 3/6/12봉) | same-move ratio(동일 이동 비율) | cost-stressed exp(비용 압박 기대값) | cooldown survives(쿨다운 생존) |
|---|---|---:|---:|---:|---|---:|---:|---:|
| inv6_s040l040_h3_b060 | validation_is | 0.624182 | 0.310479 | 0.290150 | 1037/1199/1299 | 0.760984 | -0.772537 | False |
| inv6_s040l040_h3_b060 | oos | 0.610422 | 0.332822 | 0.316932 | 814/926/1023 | 0.761727 | -0.638138 | False |
| inv6_s042l040_h3_b060 | validation_is | 0.612737 | 0.315589 | 0.301115 | 963/1098/1180 | 0.739348 | -0.547525 | False |
| inv6_s042l040_h3_b060 | oos | 0.603185 | 0.319422 | 0.327476 | 743/860/946 | 0.757406 | -0.571609 | False |
| inv6_s045l045_h3_b060 | validation_is | 0.622104 | 0.303030 | 0.311475 | 512/593/643 | 0.654120 | -0.230132 | False |
| inv6_s045l045_h3_b060 | oos | 0.596407 | 0.356742 | 0.350427 | 357/402/461 | 0.652051 | -0.380594 | False |
| inv6_s048l045_h4_b060 | validation_is | 0.596348 | 0.349462 | 0.317949 | 354/406/464 | 0.608924 | -0.206601 | False |
| inv6_s048l045_h4_b060 | oos | 0.631508 | 0.335689 | 0.349624 | 236/283/329 | 0.599271 | -0.030055 | False |

## Current Read(현재 판독)

- best_variant(최선 변형): `inv6_s045l045_h3_b060`
- selected_research_baseline(선택 연구 기준선): `none`
- stage56_remains_open(56단계 열림 유지): `True`
- next_hypothesis_branch(다음 가설 가지): `continue_density_repair_without_same_move_splitting_and_tier_b_damage_control`

## run50AN Attribution Checkpoint(run50AN 귀인 점검)

- action(행동): `inv6_s042l040_h3_b060`, `inv6_s045l045_h3_b060`, `inv6_s048l045_h4_b060`의 routed MT5(라우팅 MT5) trade list(거래 목록)를 market-weather attribution(시장 상태 귀인)으로 분해했다.
- effect(효과): 0.45 hold3(0.45 보유3)은 validation density(검증 밀도)는 맞지만 OOS sell(표본외 매도)이 손상되고, 0.48/0.45 hold4(0.48/0.45 보유4)는 OOS PF(표본외 수익 팩터)는 좋아지지만 density(밀도)가 부족하다는 병목을 분리했다.
- read(판독): OOS(표본외)에서 buy(매수)는 0.45와 0.48 모두 양수지만 sell(매도)은 threshold/hold(문턱값/보유 기간)에 민감하다; 0.48 hold4(0.48 보유4)는 sell downtrend(매도 하락 추세) 손상을 크게 줄였지만 trade/day(일 거래 수)가 5.0에 못 미친다.
- next branch(다음 분기): `run50AO_inverse_lgbm_side_threshold_hold3_repair`는 short threshold(매도 문턱값)를 0.48~0.52로 올리고 long threshold(매수 문턱값)를 0.43~0.45 범위에서 유지하며 hold3(보유3)을 시험한다.
- boundary(주장 경계): attribution_only(귀인 전용)이며 selected_research_baseline(선택 연구 기준선), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격)을 주장하지 않는다.
