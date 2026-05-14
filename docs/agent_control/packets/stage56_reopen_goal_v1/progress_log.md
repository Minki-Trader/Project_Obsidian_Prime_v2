# Stage56 Reopen Goal Progress Log(56단계 재개 목표 진행 기록)

- packet_id(묶음 ID): `stage56_reopen_goal_v1`
- stage_status(단계 상태): `active_in_progress(활성 진행 중)`
- latest_batch(최신 후보 묶음): `run50BK_stage56_s43c02_tierb_quality_firewall_v1`
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

- latest_best_variant(최신 최선 변형): `s43c02_h4c0_no_b`
- partial_quality_clue(부분 품질 단서): `s43c02_h4c0_with_b_blvl`
- current_frontier_candidate(현재 최전선 후보): `run50BH/et40h6_r001_a`
- selected_research_baseline(선택 연구 기준선): `none`
- stage56_remains_open(56단계 열림 유지): `True`
- next_hypothesis_branch(다음 가설 가지): `run50BL_real_density_source_pivot_branch`

## 2026-05-14T09:01:33Z run50BJ Independent Event Source Cooldown Sweep(독립 이벤트 원천 쿨다운 탐색)

- action(행동): Stage43/45/47 independent event source(독립 이벤트 원천)를 Stage56(56단계) actual MT5 validation/OOS(실제 MT5 검증/표본외)로 cooldown sweep(쿨다운 탐색)까지 다시 실행했다.
- effect(효과): independent opportunity density(독립 기회 밀도)가 실제 routed account path(라우팅 계정 경로)에서 살아남는지 확인하고, Tier B fallback-only(Tier B 대체 전용) 손상을 분리했다.
- best_variant(현재 최선 변형): `s43c02_h4c0`
- validation/OOS trades/day(검증/표본외 일 거래): `7.393443` / `5.600000`
- validation/OOS PF(검증/표본외 수익 팩터): `1.120000` / `1.060000`
- validation/OOS net(검증/표본외 순손익): `363.02` / `156.49`
- decision(결정): selected_research_baseline(선택 연구 기준선)=`none`; failure_reasons(실패 사유)=`oos_pf;cost_stressed_expectancy;same_move_density`.
- Tier B read(Tier B 판독): `s43c02_h4c0` Tier B fallback-only OOS(Tier B 대체 전용 표본외)는 net(순손익) `-20.27`, PF(수익 팩터) `0.97`로 hidden OOS damage(숨은 표본외 손상)를 만들었다.
- same-move clue(동일 이동 단서): `s45c04_h4c4` OOS same-move ratio(표본외 동일 이동 비율)는 `0.347651`까지 내려갔지만 OOS density/PF(표본외 밀도/수익 팩터)와 validation quality(검증 품질)가 실패했다.
- next(다음): `run50BK_s43c02_tier_b_disable_and_cooldown_quality_firewall_branch`.

## 2026-05-14T09:47:01Z run50BK S43 Tier B Quality Firewall(S43 티어 B 품질 방화벽)

- action(행동): run50BJ(실행50BJ) attribution(귀속 분석)의 buy low-vol late(매수 저변동성 후반) OOS damage(표본외 손상)를 막고 Tier B(티어 B) disablement(비활성화)를 실제 MT5 validation/OOS(검증/표본외)로 시험했다.
- effect(효과): s43c02(43단계 c02) source(원천)를 계속 polish(다듬기)할 가치가 있는지, 또는 real density source pivot(실제 밀도 원천 전환)이 더 높은 가치인지 판정했다.
- best_variant(현재 최선 변형): `s43c02_h4c0_no_b`
- validation/OOS trades/day(검증/표본외 일 거래): `6.693989` / `5.082051`
- validation/OOS PF(검증/표본외 수익 팩터): `1.110000` / `1.070000`
- validation/OOS net(검증/표본외 순손익): `317.36` / `156.81`
- Tier B disablement read(Tier B 비활성화 판독): best route(최선 라우트)는 Tier B disabled(티어 B 비활성)이고, Tier B fallback-only OOS(Tier B 대체 전용 표본외)는 net(순손익) `-20.270000`, PF(수익 팩터) `0.970000`다.
- partial_quality_clue(부분 품질 단서): `s43c02_h4c0_with_b_blvl` A+B actual routed OOS(A+B 실제 라우팅 표본외)는 PF(수익 팩터) `1.100000`, net(순손익) `233.41`지만 Tier B fallback-only OOS(Tier B 대체 전용 표본외) PF(수익 팩터) `0.850000`와 same-move ratio(동일 이동 비율) `0.762146`가 실패한다.
- decision(결정): selected_research_baseline(선택 연구 기준선)=`none`; current_frontier_candidate(현재 최전선 후보)=`run50BH/et40h6_r001_a`; failure_reasons(실패 사유)=`oos_pf;cost_stressed_expectancy;same_move_density`.
- next(다음): `run50BL_real_density_source_pivot_branch`.

## 2026-05-14T10:24:50Z run50BH Account Cost Forensics(계좌 비용 포렌식)

- action(행동): 현재 MT5 account(계좌)와 US100 symbol(심볼), 2026년 US100 deal history(체결 이력), run50BH(실행50BH) MT5 reports(보고서), raw M5 spread_points(원천 5분봉 스프레드 포인트)를 확인했다.
- effect(효과): run50BH(실행50BH)의 cost-stressed expectancy(비용 압박 기대값) 실패가 commission(거래수수료) 때문인지, spread/slippage(스프레드/미끄러짐) 때문인지 분리했다.
- commission read(수수료 판독): live account history(실계좌 이력) US100 185 deals(체결)와 run50BH reports(보고서) 6개 모두 commission(수수료) 합계 `0.0`, nonzero commission(비영 수수료) `0`이다.
- swap read(스왑 판독): live account history(실계좌 이력) swap(스왑) 합계 `-0.75`, run50BH routed validation/OOS(라우팅 검증/표본외) swap(스왑) `+3.08` / `+2.82`로 작지만 존재한다.
- spread read(스프레드 판독): current live recent M5(현재 실계좌 최근 5분봉) 5000 rows(행)는 median/max `60/60` points(포인트); run50BH raw validation/OOS(원천 검증/표본외)는 median `140/60`, max `150/140` points(포인트)다.
- slippage boundary(미끄러짐 경계): live history order request price(실계좌 주문 요청가)가 market order(시장가 주문)에서 `0.0`으로 저장되어 request-vs-fill slippage(요청가 대비 체결가 미끄러짐)는 inconclusive(불충분)이다. MT5 tester(테스터)는 fill rate(체결률) `1.0`, reject(거절) `0`이고 deal price residual(체결가 잔차)은 대부분 bid/ask quote(매수/매도 호가) 수준이다.
- decision(결정): commission issue(수수료 문제)는 이 계좌 기준 largely resolved(대체로 해소)지만 selected_research_baseline(선택 연구 기준선)은 `none` 유지다. Effect(효과): same-move density(동일 이동 밀도)와 Tier B rule(Tier B 규칙)은 여전히 별도 병목이다.
