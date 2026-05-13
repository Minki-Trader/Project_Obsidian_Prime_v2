# Stage56 Reopen Goal Progress Log(56단계 재개 목표 진행 기록)

- packet_id(묶음 ID): `stage56_reopen_goal_v1`
- stage_status(단계 상태): `active_in_progress(활성 진행 중)`
- latest_batch(최신 후보 묶음): `run50AS_stage56_extratrees_rearm_real_density_guard_v1`
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
| et40h6_tr_a | strict_transition_gate_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AS/et40h6_tr_a/mt5/reports/Project_Obsidian_Prime_v2_run50AS_et40h6_tr_a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AS/et40h6_tr_a/mt5/reports/Project_Obsidian_Prime_v2_run50AS_et40h6_tr_a_logreg_deep_v1_routed_oos.htm | 5.338798 | 3.615385 | 1.08 | 1.44 | 196.93 | 663.37 | oos_density; validation_pf; cost_stressed_expectancy; same_move_density |
| et40h6_r015_a | confidence_rearm_guard_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AS/et40h6_r015_a/mt5/reports/Project_Obsidian_Prime_v2_run50AS_et40h6_r015_a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AS/et40h6_r015_a/mt5/reports/Project_Obsidian_Prime_v2_run50AS_et40h6_r015_a_logreg_deep_v1_routed_oos.htm | 5.978142 | 4.271795 | 1.12 | 1.34 | 317.78 | 632.5 | oos_density; cost_stressed_expectancy; same_move_density; tier_b_rule |
| et40h6_r030_a | confidence_rearm_guard_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AS/et40h6_r030_a/mt5/reports/Project_Obsidian_Prime_v2_run50AS_et40h6_r030_a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AS/et40h6_r030_a/mt5/reports/Project_Obsidian_Prime_v2_run50AS_et40h6_r030_a_logreg_deep_v1_routed_oos.htm | 5.535519 | 3.800000 | 1.14 | 1.39 | 357.69 | 633.65 | oos_density; cost_stressed_expectancy; same_move_density; tier_b_rule |
| et40h6_r050_a | confidence_rearm_guard_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AS/et40h6_r050_a/mt5/reports/Project_Obsidian_Prime_v2_run50AS_et40h6_r050_a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AS/et40h6_r050_a/mt5/reports/Project_Obsidian_Prime_v2_run50AS_et40h6_r050_a_logreg_deep_v1_routed_oos.htm | 5.382514 | 3.641026 | 1.09 | 1.43 | 216.76 | 650.43 | oos_density; validation_pf; cost_stressed_expectancy; same_move_density |
| et40h6_r030_s24l15_a | transition_guard_density_recovery_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AS/et40h6_r030_s24l15_a/mt5/reports/Project_Obsidian_Prime_v2_run50AS_et40h6_r030_s24l15_a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AS/et40h6_r030_s24l15_a/mt5/reports/Project_Obsidian_Prime_v2_run50AS_et40h6_r030_s24l15_a_logreg_deep_v1_routed_oos.htm | 5.535519 | 3.800000 | 1.14 | 1.39 | 357.69 | 633.65 | oos_density; cost_stressed_expectancy; same_move_density; tier_b_rule |
| et40h8_r030_a | hold8_transition_guard_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AS/et40h8_r030_a/mt5/reports/Project_Obsidian_Prime_v2_run50AS_et40h8_r030_a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AS/et40h8_r030_a/mt5/reports/Project_Obsidian_Prime_v2_run50AS_et40h8_r030_a_logreg_deep_v1_routed_oos.htm | 5.398907 | 3.641026 | 1.04 | 1.34 | 109.06 | 592.96 | oos_density; validation_pf; cost_stressed_expectancy; same_move_density |
| et40h6_r030_b | tier_b_damage_control_comparison | true | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AS/et40h6_r030_b/mt5/reports/Project_Obsidian_Prime_v2_run50AS_et40h6_r030_b_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AS/et40h6_r030_b/mt5/reports/Project_Obsidian_Prime_v2_run50AS_et40h6_r030_b_logreg_deep_v1_routed_oos.htm | 5.584699 | 3.892308 | 1.16 | 1.39 | 385.93 | 639.18 | oos_density; cost_stressed_expectancy; same_move_density |

## Tier Views(티어 보기)

| variant(변형) | Tier A val/OOS(Tier A 검증/표본외) | Tier B fallback-only val/OOS(Tier B 대체 전용 검증/표본외) | A+B actual routed val/OOS(A+B 실제 라우팅 검증/표본외) | Tier B contribution(Tier B 기여) |
|---|---|---|---|---|
| et40h6_tr_a | net 196.93/663.37, PF 1.08/1.44 | net -80.99/13.5, PF 0.11/1.71 | net 196.93/663.37, PF 1.08/1.44 | fallback bars None/None |
| et40h6_r015_a | net 317.78/632.5, PF 1.12/1.34 | net -80.99/13.5, PF 0.11/1.71 | net 317.78/632.5, PF 1.12/1.34 | fallback bars None/None |
| et40h6_r030_a | net 357.69/633.65, PF 1.14/1.39 | net -80.99/13.5, PF 0.11/1.71 | net 357.69/633.65, PF 1.14/1.39 | fallback bars None/None |
| et40h6_r050_a | net 216.76/650.43, PF 1.09/1.43 | net -80.99/13.5, PF 0.11/1.71 | net 216.76/650.43, PF 1.09/1.43 | fallback bars None/None |
| et40h6_r030_s24l15_a | net 357.69/633.65, PF 1.14/1.39 | net -80.99/13.5, PF 0.11/1.71 | net 357.69/633.65, PF 1.14/1.39 | fallback bars None/None |
| et40h8_r030_a | net 109.06/592.96, PF 1.04/1.34 | net -18.86/-5.44, PF 0.36/0.86 | net 109.06/592.96, PF 1.04/1.34 | fallback bars None/None |
| et40h6_r030_b | net 357.69/633.65, PF 1.14/1.39 | net -80.99/13.5, PF 0.11/1.71 | net 385.93/639.18, PF 1.16/1.39 | fallback bars None/None |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture ratio(MFE 포착 비율) | winner truncation(승자 절단) | loser escape(패자 탈출) | re-entry 3/6/12(재진입 3/6/12봉) | same-move ratio(동일 이동 비율) | cost-stressed exp(비용 압박 기대값) | cooldown survives(쿨다운 생존) |
|---|---|---:|---:|---:|---|---:|---:|---:|
| et40h6_tr_a | validation_is | 0.598507 | 0.353881 | 0.259740 | 312/424/536 | 0.548618 | -0.298434 | False |
| et40h6_tr_a | oos | 0.618090 | 0.310651 | 0.291553 | 241/304/367 | 0.520567 | 0.440950 | False |
| et40h6_r015_a | validation_is | 0.600701 | 0.348606 | 0.251689 | 391/547/673 | 0.615174 | -0.209525 | False |
| et40h6_r015_a | oos | 0.606260 | 0.325758 | 0.313501 | 312/418/517 | 0.620648 | 0.259304 | False |
| et40h6_r030_a | validation_is | 0.600148 | 0.349558 | 0.262032 | 335/457/581 | 0.573544 | -0.146900 | False |
| et40h6_r030_a | oos | 0.615901 | 0.314448 | 0.291237 | 264/337/405 | 0.546559 | 0.355128 | False |
| et40h6_r050_a | validation_is | 0.599015 | 0.352941 | 0.259669 | 315/431/545 | 0.553299 | -0.279939 | False |
| et40h6_r050_a | oos | 0.617139 | 0.311765 | 0.289189 | 243/306/371 | 0.522535 | 0.416099 | False |
| et40h6_r030_s24l15_a | validation_is | 0.600148 | 0.349558 | 0.262032 | 335/457/581 | 0.573544 | -0.146900 | False |
| et40h6_r030_s24l15_a | oos | 0.615901 | 0.314448 | 0.291237 | 264/337/405 | 0.546559 | 0.355128 | False |
| et40h8_r030_a | validation_is | 0.603753 | 0.351852 | 0.262590 | 342/458/557 | 0.563765 | -0.389615 | False |
| et40h8_r030_a | oos | 0.588181 | 0.368263 | 0.289894 | 258/330/385 | 0.542254 | 0.335155 | False |
| et40h6_r030_b | validation_is | 0.600498 | 0.347921 | 0.265487 | 336/460/586 | 0.573386 | -0.122378 | False |
| et40h6_r030_b | oos | 0.615861 | 0.315068 | 0.286802 | 266/344/419 | 0.552042 | 0.342134 | False |

## Current Read(현재 판독)

- best_variant(최선 변형): `et40h6_r030_b`
- selected_research_baseline(선택 연구 기준선): `none`
- stage56_remains_open(56단계 열림 유지): `True`
- judgment(판정): rearm/transition guard(재허용/전환 가드)는 validation/OOS PF(검증/표본외 수익 팩터)를 `1.16` / `1.39`까지 개선했지만 OOS density(표본외 밀도) `3.892308`, same-move ratio(동일 이동 비율) `0.573386` / `0.552042`, 12-bar cooldown after density(12봉 쿨다운 후 밀도) `2.382514` / `1.743590`로 실패했다. Effect(효과): leaf40(잎 40) ExtraTrees(엑스트라트리스)의 원래 밀도는 독립 기회 원천보다 split re-entry(분할 재진입)에 더 가까웠다.
- attribution_read(기여도 판독): `et40h6_r030_b`와 closest density(밀도 최접근) `et40h6_r015_a`는 OOS(표본외) major buckets(주요 구간)가 양수이고 mid session(중간 세션)도 양수지만 약하다. Effect(효과): 다음 분기는 단순 market-state filter(시장 상태 필터)가 아니라 model granularity/source(모델 세분도/원천) 변경이다.
- next_hypothesis_branch(다음 가설 가지): `run50AT_extratrees_leaf_granularity_transition_density_source`
