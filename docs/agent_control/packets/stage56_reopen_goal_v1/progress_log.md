# Stage56 Reopen Goal Progress Log(56단계 재개 목표 진행 기록)

- packet_id(묶음 ID): `stage56_reopen_goal_v1`
- stage_status(단계 상태): `active_in_progress(활성 진행 중)`
- latest_batch(최신 후보 묶음): `run50AQ_stage56_extratrees_model_axis_density_v1`
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
| et20s25a | extratrees_leaf20_s25_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AQ/et20s25a/mt5/reports/Project_Obsidian_Prime_v2_run50AQ_et20s25a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AQ/et20s25a/mt5/reports/Project_Obsidian_Prime_v2_run50AQ_et20s25a_logreg_deep_v1_routed_oos.htm | 4.852459 | 3.646154 | 0.98 | 1.13 | -60.48 | 237.74 | validation_density; oos_density; validation_net_positive; validation_pf |
| et20s25b | extratrees_leaf20_s25_tier_b | true | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AQ/et20s25b/mt5/reports/Project_Obsidian_Prime_v2_run50AQ_et20s25b_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AQ/et20s25b/mt5/reports/Project_Obsidian_Prime_v2_run50AQ_et20s25b_logreg_deep_v1_routed_oos.htm | 4.923497 | 3.682051 | 0.98 | 1.12 | -42.29 | 224.69 | validation_density; oos_density; validation_net_positive; validation_pf |
| et40s25a | extratrees_leaf40_s25_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AQ/et40s25a/mt5/reports/Project_Obsidian_Prime_v2_run50AQ_et40s25a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AQ/et40s25a/mt5/reports/Project_Obsidian_Prime_v2_run50AQ_et40s25a_logreg_deep_v1_routed_oos.htm | 4.540984 | 3.276923 | 1.0 | 1.29 | -6.12 | 473.93 | validation_density; oos_density; validation_net_positive; validation_pf |
| et40s25b | extratrees_leaf40_s25_tier_b | true | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AQ/et40s25b/mt5/reports/Project_Obsidian_Prime_v2_run50AQ_et40s25b_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AQ/et40s25b/mt5/reports/Project_Obsidian_Prime_v2_run50AQ_et40s25b_logreg_deep_v1_routed_oos.htm | 4.568306 | 3.389744 | 1.0 | 1.34 | 0.05 | 540.59 | validation_density; oos_density; validation_pf; cost_stressed_expectancy |
| et20s30a | extratrees_leaf20_stricter_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AQ/et20s30a/mt5/reports/Project_Obsidian_Prime_v2_run50AQ_et20s30a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AQ/et20s30a/mt5/reports/Project_Obsidian_Prime_v2_run50AQ_et20s30a_logreg_deep_v1_routed_oos.htm | 4.852459 | 3.646154 | 0.98 | 1.13 | -60.48 | 237.74 | validation_density; oos_density; validation_net_positive; validation_pf |

## Tier Views(티어 보기)

| variant(변형) | Tier A val/OOS(Tier A 검증/표본외) | Tier B fallback-only val/OOS(Tier B 대체 전용 검증/표본외) | A+B actual routed val/OOS(A+B 실제 라우팅 검증/표본외) | Tier B contribution(Tier B 기여) |
|---|---|---|---|---|
| et20s25a | net -60.48/237.74, PF 0.98/1.13 | net -83.77/-10.59, PF 0.04/0.68 | net -60.48/237.74, PF 0.98/1.13 | fallback bars None/None |
| et20s25b | net -60.48/237.74, PF 0.98/1.13 | net -83.77/-10.59, PF 0.04/0.68 | net -42.29/224.69, PF 0.98/1.12 | fallback bars None/None |
| et40s25a | net -6.12/473.93, PF 1.0/1.29 | net -83.77/-10.59, PF 0.04/0.68 | net -6.12/473.93, PF 1.0/1.29 | fallback bars None/None |
| et40s25b | net -6.12/473.93, PF 1.0/1.29 | net -83.77/-10.59, PF 0.04/0.68 | net 0.05/540.59, PF 1.0/1.34 | fallback bars None/None |
| et20s30a | net -60.48/237.74, PF 0.98/1.13 | net -83.77/-10.59, PF 0.04/0.68 | net -60.48/237.74, PF 0.98/1.13 | fallback bars None/None |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture ratio(MFE 포착 비율) | winner truncation(승자 절단) | loser escape(패자 탈출) | re-entry 3/6/12(재진입 3/6/12봉) | same-move ratio(동일 이동 비율) | cost-stressed exp(비용 압박 기대값) | cooldown survives(쿨다운 생존) |
|---|---|---:|---:|---:|---|---:|---:|---:|
| et20s25a | validation_is | 0.598463 | 0.354331 | 0.268245 | 248/320/478 | 0.538288 | -0.568108 | False |
| et20s25a | oos | 0.586190 | 0.371105 | 0.287709 | 219/259/420 | 0.590717 | -0.165626 | False |
| et20s25b | validation_is | 0.599714 | 0.355670 | 0.265107 | 252/322/482 | 0.534961 | -0.546937 | False |
| et20s25b | oos | 0.585521 | 0.361111 | 0.282123 | 213/253/421 | 0.586351 | -0.187061 | False |
| et40s25a | validation_is | 0.592287 | 0.380165 | 0.269231 | 207/265/441 | 0.530686 | -0.507365 | False |
| et40s25a | oos | 0.608452 | 0.342105 | 0.334328 | 170/205/361 | 0.564945 | 0.241674 | False |
| et40s25b | validation_is | 0.588039 | 0.385675 | 0.272727 | 204/260/441 | 0.527512 | -0.499940 | False |
| et40s25b | oos | 0.604362 | 0.343750 | 0.331378 | 178/210/378 | 0.571861 | 0.317837 | False |
| et20s30a | validation_is | 0.598463 | 0.354331 | 0.268245 | 248/320/478 | 0.538288 | -0.568108 | False |
| et20s30a | oos | 0.586190 | 0.371105 | 0.287709 | 219/259/420 | 0.590717 | -0.165626 | False |

## Current Read(현재 판독)

- best_variant(최선 변형): `et40s25b`
- selected_research_baseline(선택 연구 기준선): `none`
- stage56_remains_open(56단계 열림 유지): `True`
- judgment(판정): `et40s25b`는 OOS quality source(표본외 품질 원천) 단서지만 validation density/PF(검증 밀도/수익 팩터), OOS density(표본외 밀도), validation cost(검증 비용), same-move survival(동일 이동 생존), Tier B damage(Tier B 손상)를 통과하지 못했다. Effect(효과): selected_research_baseline(선택 연구 기준선)을 만들지 않고 다음 repair branch(수정 분기)를 연다.
- attribution_read(기여도 판독): `et40s25b` validation(검증)은 mid session(중간 세션) `-76.27`, ADX<20(ADX 20 미만) `-121.75`, vol_low(낮은 변동성) `-95.63`이 약했고, OOS(표본외)는 mid session(중간 세션) `-18.07`만 음수였다. Effect(효과): run50AR(실행50AR)는 ExtraTrees leaf40(엑스트라트리스 잎 40)에서 cooldown(쿨다운) 완화와 ADX weak-trend firewall(ADX 약추세 방화벽)을 실제 MT5(메타트레이더5)로 시험한다.
- next_hypothesis_branch(다음 가설 가지): `run50AR_extratrees_validation_density_repair`
