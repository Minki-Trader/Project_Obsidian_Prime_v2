# Stage56 Reopen Goal Progress Log(56단계 재개 목표 진행 기록)

- packet_id(묶음 ID): `stage56_reopen_goal_v1`
- stage_status(단계 상태): `active_in_progress(활성 진행 중)`
- latest_batch(최신 후보 묶음): `run50AH_stage56_s25_model_axis_oos_density_v1`
- selected_research_baseline(선택 연구 기준선): `none`
- terminal_condition(종료 조건): selected_research_baseline(선택 연구 기준선) found(발견)
- non_final_prior_packets(비최종 이전 묶음): `stage56_closeout_v1`, `stage56_reopened_closeout_v2`

Stage56(56단계)은 unfinished optimization campaign(미완 최적화 캠페인)으로 open(열림) 상태다.
Effect(효과): progress log(진행 기록)는 Stage56(56단계)을 닫지 않고 다음 hypothesis branch(가설 가지)를 정한다.

## Current Bottleneck(현재 병목)

- density(밀도): selected_research_baseline(선택 연구 기준선)은 validation/OOS(검증/표본외) 모두 5+ trades/day(일 거래 수)를 요구한다. run50AH(실행50AH)는 model-axis perturbation(모델 축 교란)으로 validation density(검증 밀도)는 유지했지만 OOS density(표본외 밀도)는 최고 3.789744 trades/day(일 거래 수)에 그쳤다.
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
| c025s25a | s25_model_axis_c025_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AH/c025s25a/mt5/reports/Project_Obsidian_Prime_v2_run50AH_c025s25a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AH/c025s25a/mt5/reports/Project_Obsidian_Prime_v2_run50AH_c025s25a_logreg_deep_v1_routed_oos.htm | 5.377049 | 3.553846 | 1.18 | 1.16 | 449.96 | 294.18 | oos_density; cost_stressed_expectancy; same_move_density; tier_b_rule |
| c025s25b | s25_model_axis_c025_tier_b_comparison | true | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AH/c025s25b/mt5/reports/Project_Obsidian_Prime_v2_run50AH_c025s25b_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AH/c025s25b/mt5/reports/Project_Obsidian_Prime_v2_run50AH_c025s25b_logreg_deep_v1_routed_oos.htm | 5.431694 | 3.605128 | 1.14 | 1.24 | 364.33 | 427.07 | oos_density; cost_stressed_expectancy; same_move_density; tier_b_rule |
| c100s25a | s25_model_axis_c100_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AH/c100s25a/mt5/reports/Project_Obsidian_Prime_v2_run50AH_c100s25a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AH/c100s25a/mt5/reports/Project_Obsidian_Prime_v2_run50AH_c100s25a_logreg_deep_v1_routed_oos.htm | 5.349727 | 3.625641 | 1.16 | 1.26 | 398.56 | 468.44 | oos_density; cost_stressed_expectancy; same_move_density |
| c100s25b | s25_model_axis_c100_tier_b_comparison | true | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AH/c100s25b/mt5/reports/Project_Obsidian_Prime_v2_run50AH_c100s25b_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AH/c100s25b/mt5/reports/Project_Obsidian_Prime_v2_run50AH_c100s25b_logreg_deep_v1_routed_oos.htm | 5.393443 | 3.697436 | 1.13 | 1.31 | 334.28 | 545.59 | oos_density; cost_stressed_expectancy; same_move_density; tier_b_rule |
| nf200s25a | s25_model_axis_nonflat200_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AH/nf200s25a/mt5/reports/Project_Obsidian_Prime_v2_run50AH_nf200s25a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AH/nf200s25a/mt5/reports/Project_Obsidian_Prime_v2_run50AH_nf200s25a_logreg_deep_v1_routed_oos.htm | 5.437158 | 3.733333 | 1.23 | 1.17 | 550.2 | 310.59 | oos_density; cost_stressed_expectancy; same_move_density; tier_b_rule |
| nf200s25b | s25_model_axis_nonflat200_tier_b_comparison | true | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AH/nf200s25b/mt5/reports/Project_Obsidian_Prime_v2_run50AH_nf200s25b_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AH/nf200s25b/mt5/reports/Project_Obsidian_Prime_v2_run50AH_nf200s25b_logreg_deep_v1_routed_oos.htm | 5.513661 | 3.789744 | 1.18 | 1.24 | 459.98 | 428.88 | oos_density; cost_stressed_expectancy; same_move_density; tier_b_rule |
| r23s25a | s25_model_axis_recent2023_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AH/r23s25a/mt5/reports/Project_Obsidian_Prime_v2_run50AH_r23s25a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AH/r23s25a/mt5/reports/Project_Obsidian_Prime_v2_run50AH_r23s25a_logreg_deep_v1_routed_oos.htm | 3.814208 | 2.820513 | 1.06 | 0.98 | 122.86 | -29.41 | validation_density; oos_density; oos_net_positive; validation_pf |
| r23s25b | s25_model_axis_recent2023_tier_b_comparison | true | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AH/r23s25b/mt5/reports/Project_Obsidian_Prime_v2_run50AH_r23s25b_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AH/r23s25b/mt5/reports/Project_Obsidian_Prime_v2_run50AH_r23s25b_logreg_deep_v1_routed_oos.htm | 3.841530 | 2.958974 | 1.05 | 0.99 | 108.69 | -22.21 | validation_density; oos_density; oos_net_positive; validation_pf |

## Tier Views(티어 보기)

| variant(변형) | Tier A val/OOS(Tier A 검증/표본외) | Tier B fallback-only val/OOS(Tier B 대체 전용 검증/표본외) | A+B actual routed val/OOS(A+B 실제 라우팅 검증/표본외) | Tier B contribution(Tier B 기여) |
|---|---|---|---|---|
| c025s25a | net 449.96/294.18, PF 1.18/1.16 | net -83.93/-10.43, PF 0.04/0.69 | net 449.96/294.18, PF 1.18/1.16 | fallback bars None/None |
| c025s25b | net 449.96/294.18, PF 1.18/1.16 | net -83.93/-10.43, PF 0.04/0.69 | net 364.33/427.07, PF 1.14/1.24 | fallback bars None/None |
| c100s25a | net 398.56/468.44, PF 1.16/1.26 | net -83.93/-10.43, PF 0.04/0.69 | net 398.56/468.44, PF 1.16/1.26 | fallback bars None/None |
| c100s25b | net 398.56/468.44, PF 1.16/1.26 | net -83.93/-10.43, PF 0.04/0.69 | net 334.28/545.59, PF 1.13/1.31 | fallback bars None/None |
| nf200s25a | net 550.2/310.59, PF 1.23/1.17 | net -83.93/-10.43, PF 0.04/0.69 | net 550.2/310.59, PF 1.23/1.17 | fallback bars None/None |
| nf200s25b | net 550.2/310.59, PF 1.23/1.17 | net -83.93/-10.43, PF 0.04/0.69 | net 459.98/428.88, PF 1.18/1.24 | fallback bars None/None |
| r23s25a | net 122.86/-29.41, PF 1.06/0.98 | net -83.93/-10.43, PF 0.04/0.69 | net 122.86/-29.41, PF 1.06/0.98 | fallback bars None/None |
| r23s25b | net 122.86/-29.41, PF 1.06/0.98 | net -83.93/-10.43, PF 0.04/0.69 | net 108.69/-22.21, PF 1.05/0.99 | fallback bars None/None |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture ratio(MFE 포착 비율) | winner truncation(승자 절단) | loser escape(패자 탈출) | re-entry 3/6/12(재진입 3/6/12봉) | same-move ratio(동일 이동 비율) | cost-stressed exp(비용 압박 기대값) | cooldown survives(쿨다운 생존) |
|---|---|---:|---:|---:|---|---:|---:|---:|
| c025s25a | validation_is | 0.601619 | 0.349036 | 0.290135 | 233/280/586 | 0.595528 | -0.042724 | False |
| c025s25a | oos | 0.582234 | 0.378151 | 0.354167 | 130/153/409 | 0.590188 | -0.075498 | False |
| c025s25b | validation_is | 0.601900 | 0.347548 | 0.289524 | 233/281/593 | 0.596579 | -0.133471 | False |
| c025s25b | oos | 0.581566 | 0.379781 | 0.347181 | 129/152/414 | 0.588905 | 0.107496 | False |
| c100s25a | validation_is | 0.605445 | 0.347548 | 0.278431 | 230/276/582 | 0.594484 | -0.092891 | False |
| c100s25a | oos | 0.587306 | 0.389333 | 0.343373 | 142/166/419 | 0.592645 | 0.162574 | False |
| c100s25b | validation_is | 0.607057 | 0.340426 | 0.278530 | 230/275/587 | 0.594732 | -0.161317 | False |
| c100s25b | oos | 0.580989 | 0.391753 | 0.333333 | 144/168/432 | 0.599168 | 0.256713 | False |
| nf200s25a | validation_is | 0.606140 | 0.341053 | 0.294231 | 241/290/593 | 0.595980 | 0.052965 | False |
| nf200s25a | oos | 0.587402 | 0.386059 | 0.380282 | 151/183/444 | 0.609890 | -0.073365 | False |
| nf200s25b | validation_is | 0.606710 | 0.341004 | 0.291902 | 243/293/604 | 0.598612 | -0.044123 | False |
| nf200s25b | oos | 0.581881 | 0.392765 | 0.375000 | 151/183/450 | 0.608931 | 0.080352 | False |
| r23s25a | validation_is | 0.641396 | 0.307229 | 0.333333 | 144/182/355 | 0.508596 | -0.323983 | False |
| r23s25a | oos | 0.585318 | 0.395604 | 0.285199 | 136/154/278 | 0.505455 | -0.553473 | False |
| r23s25b | validation_is | 0.643724 | 0.303303 | 0.332432 | 143/180/355 | 0.504979 | -0.345391 | False |
| r23s25b | oos | 0.591250 | 0.383275 | 0.272414 | 149/168/300 | 0.519931 | -0.538492 | False |

## Current Read(현재 판독)

- best_variant(최선 변형): `nf200s25b`
- selected_research_baseline(선택 연구 기준선): `none`
- stage56_remains_open(56단계 열림 유지): `True`
- attribution_report(귀속 보고서): `stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/03_reviews/run50AH_nf200s25b_market_weather_attribution.md`
- attribution_read(귀속 판독): validation/OOS(검증/표본외)는 모든 주요 session/volatility/trend/ADX bucket(세션/변동성/추세/평균 방향 지수 구간)이 양수였지만 mid session(중반 세션)과 ADX20-25(평균 방향 지수 20-25)가 약했다. 효과(effect, 효과): 단순 model-axis(모델 축)보다 independent signal source(독립 신호 원천)나 route coverage axis(라우팅 커버리지 축)가 필요하다.
- next_hypothesis_branch(다음 가설 가지): `independent_signal_source_or_route_coverage_axis_after_s25_model_axis_density_stall`
