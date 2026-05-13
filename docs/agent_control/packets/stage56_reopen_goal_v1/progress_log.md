# Stage56 Reopen Goal Progress Log(56단계 재개 목표 진행 기록)

- packet_id(묶음 ID): `stage56_reopen_goal_v1`
- stage_status(단계 상태): `active_in_progress(활성 진행 중)`
- latest_batch(최신 후보 묶음): `run50AT_stage56_extratrees_leaf_granularity_transition_density_source_v1`
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
| et20h6_r015_a | leaf20_transition_density_source_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AT/et20h6_r015_a/mt5/reports/Project_Obsidian_Prime_v2_run50AT_et20h6_r015_a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AT/et20h6_r015_a/mt5/reports/Project_Obsidian_Prime_v2_run50AT_et20h6_r015_a_logreg_deep_v1_routed_oos.htm | 6.551913 | 4.666667 | 1.07 | 1.12 | 226.28 | 277.78 | oos_density; validation_pf; cost_stressed_expectancy; same_move_density |
| et20h6_r015_b | leaf20_transition_density_source_tier_b_comparison | true | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AT/et20h6_r015_b/mt5/reports/Project_Obsidian_Prime_v2_run50AT_et20h6_r015_b_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AT/et20h6_r015_b/mt5/reports/Project_Obsidian_Prime_v2_run50AT_et20h6_r015_b_logreg_deep_v1_routed_oos.htm | 6.584699 | 4.748718 | 1.07 | 1.14 | 220.66 | 312.02 | oos_density; validation_pf; cost_stressed_expectancy; same_move_density |
| et20h6_r030_a | leaf20_quality_guard_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AT/et20h6_r030_a/mt5/reports/Project_Obsidian_Prime_v2_run50AT_et20h6_r030_a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AT/et20h6_r030_a/mt5/reports/Project_Obsidian_Prime_v2_run50AT_et20h6_r030_a_logreg_deep_v1_routed_oos.htm | 5.945355 | 4.189744 | 1.13 | 1.11 | 351.16 | 215.59 | oos_density; cost_stressed_expectancy; same_move_density; tier_b_rule |
| et20h6_r030_b | leaf20_quality_guard_tier_b_comparison | true | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AT/et20h6_r030_b/mt5/reports/Project_Obsidian_Prime_v2_run50AT_et20h6_r030_b_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AT/et20h6_r030_b/mt5/reports/Project_Obsidian_Prime_v2_run50AT_et20h6_r030_b_logreg_deep_v1_routed_oos.htm | 5.983607 | 4.271795 | 1.13 | 1.13 | 346.02 | 249.83 | oos_density; cost_stressed_expectancy; same_move_density |
| et20h6_r030_s24l15_a | leaf20_threshold_recovery_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AT/et20h6_r030_s24l15_a/mt5/reports/Project_Obsidian_Prime_v2_run50AT_et20h6_r030_s24l15_a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AT/et20h6_r030_s24l15_a/mt5/reports/Project_Obsidian_Prime_v2_run50AT_et20h6_r030_s24l15_a_logreg_deep_v1_routed_oos.htm | 5.945355 | 4.189744 | 1.13 | 1.11 | 351.16 | 215.59 | oos_density; cost_stressed_expectancy; same_move_density; tier_b_rule |
| et30h6_r015_a | leaf30_transition_density_source_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AT/et30h6_r015_a/mt5/reports/Project_Obsidian_Prime_v2_run50AT_et30h6_r015_a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AT/et30h6_r015_a/mt5/reports/Project_Obsidian_Prime_v2_run50AT_et30h6_r015_a_logreg_deep_v1_routed_oos.htm | 6.125683 | 4.379487 | 1.06 | 1.29 | 157.82 | 604.46 | oos_density; validation_pf; cost_stressed_expectancy; same_move_density |
| et30h6_r030_a | leaf30_quality_guard_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AT/et30h6_r030_a/mt5/reports/Project_Obsidian_Prime_v2_run50AT_et30h6_r030_a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AT/et30h6_r030_a/mt5/reports/Project_Obsidian_Prime_v2_run50AT_et30h6_r030_a_logreg_deep_v1_routed_oos.htm | 5.524590 | 3.902564 | 1.13 | 1.32 | 324.6 | 576.56 | oos_density; cost_stressed_expectancy; same_move_density; tier_b_rule |
| et60h6_r015_a | leaf60_smooth_transition_source_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AT/et60h6_r015_a/mt5/reports/Project_Obsidian_Prime_v2_run50AT_et60h6_r015_a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AT/et60h6_r015_a/mt5/reports/Project_Obsidian_Prime_v2_run50AT_et60h6_r015_a_logreg_deep_v1_routed_oos.htm | 5.699454 | 4.056410 | 1.06 | 1.27 | 164.77 | 510.11 | oos_density; validation_pf; cost_stressed_expectancy; same_move_density |

## Tier Views(티어 보기)

| variant(변형) | Tier A val/OOS(Tier A 검증/표본외) | Tier B fallback-only val/OOS(Tier B 대체 전용 검증/표본외) | A+B actual routed val/OOS(A+B 실제 라우팅 검증/표본외) | Tier B contribution(Tier B 기여) |
|---|---|---|---|---|
| et20h6_r015_a | net 226.28/277.78, PF 1.07/1.12 | net -80.99/13.5, PF 0.11/1.71 | net 226.28/277.78, PF 1.07/1.12 | fallback bars None/None |
| et20h6_r015_b | net 226.28/277.78, PF 1.07/1.12 | net -80.99/13.5, PF 0.11/1.71 | net 220.66/312.02, PF 1.07/1.14 | fallback bars None/None |
| et20h6_r030_a | net 351.16/215.59, PF 1.13/1.11 | net -80.99/13.5, PF 0.11/1.71 | net 351.16/215.59, PF 1.13/1.11 | fallback bars None/None |
| et20h6_r030_b | net 351.16/215.59, PF 1.13/1.11 | net -80.99/13.5, PF 0.11/1.71 | net 346.02/249.83, PF 1.13/1.13 | fallback bars None/None |
| et20h6_r030_s24l15_a | net 351.16/215.59, PF 1.13/1.11 | net -80.99/13.5, PF 0.11/1.71 | net 351.16/215.59, PF 1.13/1.11 | fallback bars None/None |
| et30h6_r015_a | net 157.82/604.46, PF 1.06/1.29 | net -80.99/13.5, PF 0.11/1.71 | net 157.82/604.46, PF 1.06/1.29 | fallback bars None/None |
| et30h6_r030_a | net 324.6/576.56, PF 1.13/1.32 | net -80.99/13.5, PF 0.11/1.71 | net 324.6/576.56, PF 1.13/1.32 | fallback bars None/None |
| et60h6_r015_a | net 164.77/510.11, PF 1.06/1.27 | net -80.99/13.5, PF 0.11/1.71 | net 164.77/510.11, PF 1.06/1.27 | fallback bars None/None |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture ratio(MFE 포착 비율) | winner truncation(승자 절단) | loser escape(패자 탈출) | re-entry 3/6/12(재진입 3/6/12봉) | same-move ratio(동일 이동 비율) | cost-stressed exp(비용 압박 기대값) | cooldown survives(쿨다운 생존) |
|---|---|---:|---:|---:|---|---:|---:|---:|
| et20h6_r015_a | validation_is | 0.615666 | 0.337545 | 0.257364 | 494/651/778 | 0.648874 | -0.311276 | False |
| et20h6_r015_a | oos | 0.597806 | 0.358811 | 0.273349 | 355/485/601 | 0.660440 | -0.194747 | False |
| et20h6_r015_b | validation_is | 0.617206 | 0.332734 | 0.260401 | 491/652/779 | 0.646473 | -0.316880 | False |
| et20h6_r015_b | oos | 0.596445 | 0.358178 | 0.268623 | 356/495/613 | 0.661987 | -0.163045 | False |
| et20h6_r030_a | validation_is | 0.610043 | 0.344423 | 0.259965 | 394/520/635 | 0.583640 | -0.177243 | False |
| et20h6_r030_a | oos | 0.591648 | 0.360775 | 0.277228 | 282/386/484 | 0.592411 | -0.236120 | False |
| et20h6_r030_b | validation_is | 0.611638 | 0.339181 | 0.264605 | 392/522/637 | 0.581735 | -0.184000 | False |
| et20h6_r030_b | oos | 0.590275 | 0.360000 | 0.272059 | 283/395/497 | 0.596639 | -0.200084 | False |
| et20h6_r030_s24l15_a | validation_is | 0.610043 | 0.344423 | 0.259965 | 394/520/635 | 0.583640 | -0.177243 | False |
| et20h6_r030_s24l15_a | oos | 0.591648 | 0.360775 | 0.277228 | 282/386/484 | 0.592411 | -0.236120 | False |
| et30h6_r015_a | validation_is | 0.588299 | 0.382239 | 0.285240 | 411/574/683 | 0.609277 | -0.359215 | False |
| et30h6_r015_a | oos | 0.624243 | 0.303738 | 0.267606 | 324/430/545 | 0.638173 | 0.207799 | False |
| et30h6_r030_a | validation_is | 0.596116 | 0.372591 | 0.283088 | 330/450/547 | 0.541048 | -0.178932 | False |
| et30h6_r030_a | oos | 0.629239 | 0.295515 | 0.261780 | 268/337/430 | 0.565046 | 0.257635 | False |
| et60h6_r015_a | validation_is | 0.606725 | 0.341991 | 0.254733 | 368/497/623 | 0.597315 | -0.342023 | False |
| et60h6_r015_a | oos | 0.595485 | 0.350254 | 0.277078 | 293/393/486 | 0.614412 | 0.144893 | False |

## Current Read(현재 판독)

- best_variant(최선 변형): `et20h6_r030_b`
- selected_research_baseline(선택 연구 기준선): `none`
- stage56_remains_open(56단계 열림 유지): `True`
- judgment(판정): leaf20/leaf30/leaf60(잎 20/30/60) ExtraTrees(엑스트라트리스)는 run50AS(실행50AS)보다 OOS density(표본외 밀도)를 일부 회복했지만 최선 `et20h6_r030_b`도 OOS density(표본외 밀도) `4.271795`, cost-stressed expectancy(비용 압박 기대값) `-0.184000` / `-0.200084`, same-move ratio(동일 이동 비율) `0.581735` / `0.596639`로 실패했다. Effect(효과): ExtraTrees(엑스트라트리스) 계열의 transition-gated density(전환 게이트 밀도)는 아직 충분한 실제 기회 원천이 아니다.
- closest_density_variant(밀도 최접근 변형): `et20h6_r015_b`는 validation/OOS(검증/표본외) trades/day(일 거래 수) `6.584699` / `4.748718`까지 갔지만 OOS density(표본외 밀도), cost stress(비용 압박), same-move/cooldown survival(동일 이동/쿨다운 생존)이 모두 부족하다.
- attribution_read(기여도 판독): `et20h6_r030_b`는 OOS(표본외) adx_gt25(ADX 25 초과) `-95.21`과 vol_high(고변동) `-15.91`이 약하고, `et20h6_r015_b`는 OOS late session(후반 세션) `-79.22`와 vol_high(고변동) `-14.53`이 약하다. Effect(효과): 단순 필터는 밀도를 더 깎을 위험이 있어 QDA composite route(QDA 합성 라우트) 쪽으로 새 source(원천)를 연다.
- next_hypothesis_branch(다음 가설 가지): `run50AU_composite_qda_route_density_repair`
