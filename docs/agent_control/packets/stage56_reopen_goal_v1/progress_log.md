# Stage56 Reopen Goal Progress Log(56단계 재개 목표 진행 기록)

- packet_id(묶음 ID): `stage56_reopen_goal_v1`
- stage_status(단계 상태): `active_in_progress(활성 진행 중)`
- latest_batch(최신 묶음): `run50AI_stage56_route_coverage_micro_batch_v1`
- selected_research_baseline(선택 연구 기준선): `none`
- terminal_condition(종료 조건): selected_research_baseline(선택 연구 기준선) found(발견)
- non_final_prior_packets(비최종 이전 묶음): `stage56_closeout_v1`, `stage56_reopened_closeout_v2`

Stage56(56단계)는 active_in_progress(활성 진행 중)이다. Effect(효과): run50B through run50AI(실행50B부터 실행50AI까지)는 intermediate evidence(중간 근거)이며 closeout(종료) 근거가 아니다.

## Current Bottleneck(현재 병목)

- density(밀도): nf200s25b(최신 중간 기준)는 validation(검증) 5+ trades/day(일 거래 수)를 넘겼지만 OOS(표본외)는 5에 못 미쳤다.
- Tier B(티어 B): fallback-only OOS(대체 전용 표본외)가 damaging(손상)해서 이번 run50AI(실행50AI)는 disabled(비활성화)했다.
- same-move split(동일 이동 분할): density gain(밀도 증가)이 12-bar cooldown(12봉 쿨다운) 뒤에도 살아야 한다.

## Attempted Variants(시도 변형)

| variant(변형) | hypothesis family(가설군) | actual MT5 report paths(실제 MT5 보고서 경로) | val/day(검증 일 거래) | OOS/day(표본외 일 거래) | val PF(검증 수익 팩터) | OOS PF(표본외 수익 팩터) | val net(검증 순손익) | OOS net(표본외 순손익) | reason(이유) |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| qda_q85_aonly_bdisabled | independent_qda_coverage_source_tier_b_disabled | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AI/qda_q85_aonly_bdisabled/mt5/reports/Project_Obsidian_Prime_v2_run50AI_qda_q85_aonly_bdisabled_route_coverage_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AI/qda_q85_aonly_bdisabled/mt5/reports/Project_Obsidian_Prime_v2_run50AI_qda_q85_aonly_bdisabled_route_coverage_v1_routed_oos.htm | 3.453552 | 1.830769 | 1.05 | 1.2 | 131.93 | 263.17 | validation_density; oos_density; validation_pf; cost_stressed_expectancy |
| qda_q93_quality_bdisabled | independent_qda_quality_source_tier_b_disabled | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AI/qda_q93_quality_bdisabled/mt5/reports/Project_Obsidian_Prime_v2_run50AI_qda_q93_quality_bdisabled_route_coverage_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AI/qda_q93_quality_bdisabled/mt5/reports/Project_Obsidian_Prime_v2_run50AI_qda_q93_quality_bdisabled_route_coverage_v1_routed_oos.htm | 1.956284 | 0.974359 | 1.14 | 1.07 | 220.32 | 65.09 | validation_density; oos_density; oos_pf; cost_stressed_expectancy |
| qda_q85_guard12_bdisabled | independent_qda_coverage_source_same_move_guard | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AI/qda_q85_guard12_bdisabled/mt5/reports/Project_Obsidian_Prime_v2_run50AI_qda_q85_guard12_bdisabled_route_coverage_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AI/qda_q85_guard12_bdisabled/mt5/reports/Project_Obsidian_Prime_v2_run50AI_qda_q85_guard12_bdisabled_route_coverage_v1_routed_oos.htm | 2.846995 | 1.466667 | 1.13 | 1.16 | 251.77 | 167.69 | validation_density; oos_density; cost_stressed_expectancy; same_move_density |

## Tier B Rule(Tier B 규칙)

- tier_b_status(Tier B 상태): `disabled(비활성화)`
- disablement_reason(비활성화 이유): Tier B disabled because run50AH nf200s25b fallback-only OOS was negative and prior A-only/A+B reads did not justify carrying damaging fallback risk into this route coverage micro-batch.
- effect(효과): 이번 route coverage(라우팅 커버리지) 판독은 Tier B fallback damage(Tier B 대체 손상)를 섞지 않는다.

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture ratio(MFE 포착 비율) | winner truncation(승자 절단) | loser escape(패자 탈출) | re-entry 3/6/12(재진입 3/6/12봉) | same-move ratio(동일 이동 비율) | cost-stressed exp(비용 압박 기대값) | cooldown survives(쿨다운 생존) |
|---|---|---:|---:|---:|---|---:|---:|---:|
| qda_q85_aonly_bdisabled | validation_is | 0.570264 | 0.370242 | 0.274052 | 226/290/325 | 0.514241 | -0.291250 | False |
| qda_q85_aonly_bdisabled | oos | 0.622654 | 0.306358 | 0.304348 | 90/120/137 | 0.383754 | 0.237171 | False |
| qda_q93_quality_bdisabled | validation_is | 0.541996 | 0.400000 | 0.229508 | 76/105/125 | 0.349162 | 0.115419 | False |
| qda_q93_quality_bdisabled | oos | 0.629748 | 0.311111 | 0.280000 | 17/25/31 | 0.163158 | -0.157421 | False |
| qda_q85_guard12_bdisabled | validation_is | 0.570301 | 0.352459 | 0.252708 | 152/188/213 | 0.408829 | -0.016756 | False |
| qda_q85_guard12_bdisabled | oos | 0.590939 | 0.342657 | 0.314685 | 49/69/75 | 0.262238 | 0.086329 | False |

## Current Read(현재 판독)

- best_variant(최선 변형): `qda_q85_guard12_bdisabled`
- selected_research_baseline(선택 연구 기준선): `none`
- next_hypothesis_branch(다음 가설 가지): `independent_signal_source_or_route_coverage_axis_needs_stronger_oos_density_source_after_qda_micro_batch`
