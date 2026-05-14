# Stage56 Reopen Goal Progress Log(56단계 재개 목표 진행 기록)

- packet_id(묶음 ID): `stage56_reopen_goal_v1`
- stage_status(단계 상태): `active_in_progress(활성 진행 중)`
- latest_batch(최신 후보 묶음): `run50BM_stage56_leaf_same_direction_density_pivot_v1`
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
- selected_research_baseline(선택 연구 기준선)은 계속 none(없음)이다. Effect(효과): 다음 hypothesis branch(가설 가지)를 이어가며 Stage56(56단계)을 open(열림)으로 유지하고, report(보고)는 terminal condition(종료 조건)이 아니다.

## Attempted Variants(시도 변형)

| variant(변형) | hypothesis family(가설군) | fallback(대체) | report paths(보고서 경로) | val/day(검증/일) | OOS/day(표본외/일) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) | reason(이유) |
|---|---|---:|---|---:|---:|---:|---:|---:|---:|---|
| et20h6sd2_s240l150_r015_a | leaf20_same_direction_density_recovery_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BM/et20h6sd2_s240l150_r015_a/mt5/reports/Project_Obsidian_Prime_v2_run50BM_et20h6sd2_s240l150_r015_a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BM/et20h6sd2_s240l150_r015_a/mt5/reports/Project_Obsidian_Prime_v2_run50BM_et20h6sd2_s240l150_r015_a_logreg_deep_v1_routed_oos.htm | 6.043716 | 4.425641 | 1.1 | 1.06 | 273.23 | 135.34 | oos_density; oos_pf; cost_stressed_expectancy; same_move_density |
| et20h6sd2_s220l130_r015_a | leaf20_threshold_expansion_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BM/et20h6sd2_s220l130_r015_a/mt5/reports/Project_Obsidian_Prime_v2_run50BM_et20h6sd2_s220l130_r015_a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BM/et20h6sd2_s220l130_r015_a/mt5/reports/Project_Obsidian_Prime_v2_run50BM_et20h6sd2_s220l130_r015_a_logreg_deep_v1_routed_oos.htm | 6.043716 | 4.425641 | 1.1 | 1.06 | 273.23 | 135.34 | oos_density; oos_pf; cost_stressed_expectancy; same_move_density |
| et20h4sd2_s220l130_r015_a | leaf20_hold4_threshold_expansion_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BM/et20h4sd2_s220l130_r015_a/mt5/reports/Project_Obsidian_Prime_v2_run50BM_et20h4sd2_s220l130_r015_a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BM/et20h4sd2_s220l130_r015_a/mt5/reports/Project_Obsidian_Prime_v2_run50BM_et20h4sd2_s220l130_r015_a_logreg_deep_v1_routed_oos.htm | 6.338798 | 4.451282 | 1.01 | 1.06 | 33.85 | 126.92 | oos_density; validation_pf; oos_pf; cost_stressed_expectancy |
| et30h6sd2_s230l140_r015_a | leaf30_middle_granularity_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BM/et30h6sd2_s230l140_r015_a/mt5/reports/Project_Obsidian_Prime_v2_run50BM_et30h6sd2_s230l140_r015_a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50BM/et30h6sd2_s230l140_r015_a/mt5/reports/Project_Obsidian_Prime_v2_run50BM_et30h6sd2_s230l140_r015_a_logreg_deep_v1_routed_oos.htm | 5.781421 | 4.158974 | 1.02 | 1.23 | 67.39 | 455.26 | oos_density; validation_pf; cost_stressed_expectancy; same_move_density |

## Tier Views(티어 보기)

| variant(변형) | Tier A val/OOS(Tier A 검증/표본외) | Tier B fallback-only val/OOS(Tier B 대체 전용 검증/표본외) | A+B actual routed val/OOS(A+B 실제 라우팅 검증/표본외) | Tier B contribution(Tier B 기여) |
|---|---|---|---|---|
| et20h6sd2_s240l150_r015_a | net 273.23/135.34, PF 1.1/1.06 | net -16.21/13.5, PF 0.39/1.71 | net 273.23/135.34, PF 1.1/1.06 | fallback bars None/None |
| et20h6sd2_s220l130_r015_a | net 273.23/135.34, PF 1.1/1.06 | net -16.21/13.5, PF 0.39/1.71 | net 273.23/135.34, PF 1.1/1.06 | fallback bars None/None |
| et20h4sd2_s220l130_r015_a | net 33.85/126.92, PF 1.01/1.06 | net -87.87/14.18, PF 0.05/1.87 | net 33.85/126.92, PF 1.01/1.06 | fallback bars None/None |
| et30h6sd2_s230l140_r015_a | net 67.39/455.26, PF 1.02/1.23 | net -16.21/13.5, PF 0.39/1.71 | net 67.39/455.26, PF 1.02/1.23 | fallback bars None/None |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture ratio(MFE 포착 비율) | winner truncation(승자 절단) | loser escape(패자 탈출) | re-entry 3/6/12(재진입 3/6/12봉) | same-move ratio(동일 이동 비율) | cost-stressed exp(비용 압박 기대값) | cooldown survives(쿨다운 생존) |
|---|---|---:|---:|---:|---|---:|---:|---:|
| et20h6sd2_s240l150_r015_a | validation_is | 0.621620 | 0.331395 | 0.250847 | 350/522/664 | 0.600362 | -0.252957 | False |
| et20h6sd2_s240l150_r015_a | oos | 0.588554 | 0.377273 | 0.264775 | 278/420/546 | 0.632677 | -0.343175 | False |
| et20h6sd2_s220l130_r015_a | validation_is | 0.621620 | 0.331395 | 0.250847 | 350/522/664 | 0.600362 | -0.252957 | False |
| et20h6sd2_s220l130_r015_a | oos | 0.588554 | 0.377273 | 0.264775 | 278/420/546 | 0.632677 | -0.343175 | False |
| et20h4sd2_s220l130_r015_a | validation_is | 0.619299 | 0.328922 | 0.304279 | 321/524/713 | 0.614655 | -0.470819 | False |
| et20h4sd2_s220l130_r015_a | oos | 0.615476 | 0.334086 | 0.251765 | 225/369/538 | 0.619816 | -0.353779 | False |
| et30h6sd2_s230l140_r015_a | validation_is | 0.590280 | 0.385093 | 0.276522 | 307/489/611 | 0.577505 | -0.436304 | False |
| et30h6sd2_s230l140_r015_a | oos | 0.618763 | 0.317500 | 0.265207 | 254/367/490 | 0.604192 | 0.061356 | False |

## Current Read(현재 판독)

- best_variant(최선 변형): `et20h6sd2_s240l150_r015_a`
- selected_research_baseline(선택 연구 기준선): `none`
- stage56_remains_open(56단계 열림 유지): `True`
- next_hypothesis_branch(다음 가설 가지): `new_source_or_model_branch_beyond_extratrees_cooldown_polishing`

## 2026-05-14T13:01:01Z run50BN Context ExtraTrees Agreement(문맥 ExtraTrees 합의)

- action(행동): context-timed(문맥/시간) source(원천)와 run50BH ExtraTrees(엑스트라트리스)를 합의/충돌 veto(거부) 방식으로 결합해 actual MT5 validation/OOS(실제 MT5 검증/표본외)를 실행했다.
- effect(효과): low same-move(낮은 동일 이동) 구조에 OOS quality(표본외 품질)를 붙일 수 있는지 확인했다.
- best_variant(현재 최선 변형): `v47_v22_topup_plus_et40_slotfill_h2c0_no_b`
- validation/OOS trades/day(검증/표본외 일 거래): `9.748634` / `7.071795`
- validation/OOS PF(검증/표본외 수익 팩터): `1.170000` / `1.180000`
- validation/OOS net(검증/표본외 순손익): `446.11` / `380.77`
- decision(결정): selected_research_baseline(선택 연구 기준선)=`none`; failure_reasons(실패 이유)=`cost_stressed_expectancy;same_move_density`.

## 2026-05-14T13:23:09Z run50BO Context ExtraTrees Same-Direction Cooldown(문맥 ExtraTrees 동일 방향 쿨다운)

- action(행동): run50BN slot-fill(슬롯 보강) source(원천)에 same-direction cooldown(동일 방향 쿨다운)을 적용해 actual MT5 validation/OOS(실제 MT5 검증/표본외)를 실행했다.
- effect(효과): headline density(겉보기 밀도)가 같은 방향 재진입인지, cooldown(쿨다운) 뒤에도 진짜 기회가 남는지 확인했다.
- best_variant(현재 최선 변형): `v50_topup_slotfill_sd2_h2c0_no_b`
- validation/OOS trades/day(검증/표본외 일 거래): `8.857923` / `6.420513`
- validation/OOS PF(검증/표본외 수익 팩터): `1.170000` / `1.190000`
- validation/OOS net(검증/표본외 순손익): `380.19` / `342.92`
- decision(결정): selected_research_baseline(선택 연구 기준선)=`none`; failure_reasons(실패 이유)=`cost_stressed_expectancy;same_move_density`.

## 2026-05-14T13:46:06Z run50BP ExtraTrees Slot Lifecycle(ExtraTrees 슬롯 생명주기)

- action(행동): run50BH ExtraTrees(엑스트라트리스)를 20/25/30-minute slot lifecycle(분 슬롯 생명주기)로 재구성해 actual MT5 validation/OOS(실제 MT5 검증/표본외)를 실행했다.
- effect(효과): same-move density(동일 이동 밀도)를 cooldown(쿨다운)이 아니라 source spacing(원천 간격)으로 줄일 수 있는지 확인했다.
- best_variant(현재 최선 변형): `v54_et40_slot20_first_h2c0_no_b`
- validation/OOS trades/day(검증/표본외 일 거래): `9.306011` / `7.205128`
- validation/OOS PF(검증/표본외 수익 팩터): `1.000000` / `1.000000`
- validation/OOS net(검증/표본외 순손익): `2.740000` / `-9.720000`
- decision(결정): selected_research_baseline(선택 연구 기준선)=`none`; failure_reasons(실패 이유)=`oos_net_positive;validation_pf;oos_pf;cost_stressed_expectancy;same_move_density`.

## 2026-05-14T13:59:42Z run50BQ Context ExtraTrees Firewall Transition(문맥 ExtraTrees 방화벽 전환)

- action(행동): run50BN v47(실행50BN v47)의 stable ET damage slots(안정 ET 손상 슬롯)를 막고 transition-only entry(전환 진입)를 실제 MT5 validation/OOS(검증/표본외)로 시험했다.
- effect(효과): quality lift(품질 상승)가 same-move split re-entry(동일 이동 분할 재진입)와 cost-stressed expectancy(비용 압박 기대값)를 동시에 고치는지 확인했다.
- best_variant(현재 최선 변형): `v60_v47_et_stable_damage_firewall_h2c0_no_b`
- validation/OOS trades/day(검증/표본외 일 거래): `0.000000` / `0.000000`
- validation/OOS PF(검증/표본외 수익 팩터): `` / ``
- validation/OOS net(검증/표본외 순손익): `` / ``
- decision(결정): selected_research_baseline(선택 연구 기준선)=`none`; failure_reasons(실패 이유)=`validation_density;oos_density;validation_net_positive;oos_net_positive;validation_pf;oos_pf;cost_stressed_expectancy;same_move_density`.

## 2026-05-14T14:12:46Z run50BQ Context ExtraTrees Firewall Transition(문맥 ExtraTrees 방화벽 전환)

- action(행동): run50BN v47(실행50BN v47)의 stable ET damage slots(안정 ET 손상 슬롯)를 막고 transition-only entry(전환 진입)를 실제 MT5 validation/OOS(검증/표본외)로 시험했다.
- effect(효과): quality lift(품질 상승)가 same-move split re-entry(동일 이동 분할 재진입)와 cost-stressed expectancy(비용 압박 기대값)를 동시에 고치는지 확인했다.
- best_variant(현재 최선 변형): `v60_v47_et_stable_damage_firewall_h2c0_no_b`
- validation/OOS trades/day(검증/표본외 일 거래): `9.617486` / `6.948718`
- validation/OOS PF(검증/표본외 수익 팩터): `1.180000` / `1.220000`
- validation/OOS net(검증/표본외 순손익): `462.21` / `436.33`
- decision(결정): selected_research_baseline(선택 연구 기준선)=`none`; failure_reasons(실패 이유)=`cost_stressed_expectancy;same_move_density`.
