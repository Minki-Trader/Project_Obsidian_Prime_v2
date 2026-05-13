# Stage56 Reopen Goal Progress Log(56단계 재개 목표 진행 기록)

- packet_id(묶음 ID): `stage56_reopen_goal_v1`
- stage_status(단계 상태): `active_in_progress(활성 진행 중)`
- latest_batch(최신 후보 묶음): `run50AP_stage56_lgbm_fwd3_new_source_real_density_v1`
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
| raw3_s045l045_h3_b060 | fwd3_raw_direction_control | true | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AP/raw3_s045l045_h3_b060/mt5/reports/Project_Obsidian_Prime_v2_run50AP_raw3_s045l045_h3_b060_lgbm_fwd3_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AP/raw3_s045l045_h3_b060/mt5/reports/Project_Obsidian_Prime_v2_run50AP_raw3_s045l045_h3_b060_lgbm_fwd3_v1_routed_oos.htm | 5.136612021857924 | 3.246153846153846 | 1.05 | 1.01 | 125.28 | 17.24 | oos_density; validation_pf; oos_pf; cost_stressed_expectancy |
| inv3_s045l045_h3_b060 | fwd3_inverse_symmetric | true | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AP/inv3_s045l045_h3_b060/mt5/reports/Project_Obsidian_Prime_v2_run50AP_inv3_s045l045_h3_b060_lgbm_fwd3_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AP/inv3_s045l045_h3_b060/mt5/reports/Project_Obsidian_Prime_v2_run50AP_inv3_s045l045_h3_b060_lgbm_fwd3_v1_routed_oos.htm | 5.081967213114754 | 3.230769230769231 | 0.93 | 1.06 | -194.7 | 104.69 | oos_density; validation_net_positive; validation_pf; oos_pf |
| inv3_s050l043_h3_b060 | fwd3_inverse_side_threshold | true | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AP/inv3_s050l043_h3_b060/mt5/reports/Project_Obsidian_Prime_v2_run50AP_inv3_s050l043_h3_b060_lgbm_fwd3_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AP/inv3_s050l043_h3_b060/mt5/reports/Project_Obsidian_Prime_v2_run50AP_inv3_s050l043_h3_b060_lgbm_fwd3_v1_routed_oos.htm | 4.3497267759562845 | 3.2051282051282053 | 0.81 | 0.85 | -494.22 | -260.5 | validation_density; oos_density; validation_net_positive; oos_net_positive |
| inv3_s048l040_h2_b060 | fwd3_inverse_long_density_hold2 | true | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AP/inv3_s048l040_h2_b060/mt5/reports/Project_Obsidian_Prime_v2_run50AP_inv3_s048l040_h2_b060_lgbm_fwd3_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AP/inv3_s048l040_h2_b060/mt5/reports/Project_Obsidian_Prime_v2_run50AP_inv3_s048l040_h2_b060_lgbm_fwd3_v1_routed_oos.htm | 8.109289617486338 | 5.410256410256411 | 0.87 | 1.0 | -431.85 | -2.0 | validation_net_positive; oos_net_positive; validation_pf; oos_pf |
| inv3_s050l040_h2_b060 | fwd3_inverse_firewall_long_density_hold2 | true | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AP/inv3_s050l040_h2_b060/mt5/reports/Project_Obsidian_Prime_v2_run50AP_inv3_s050l040_h2_b060_lgbm_fwd3_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AP/inv3_s050l040_h2_b060/mt5/reports/Project_Obsidian_Prime_v2_run50AP_inv3_s050l040_h2_b060_lgbm_fwd3_v1_routed_oos.htm | 7.551912568306011 | 5.17948717948718 | 0.88 | 0.98 | -362.27 | -44.36 | validation_net_positive; oos_net_positive; validation_pf; oos_pf |

## Tier Views(티어 보기)

| variant(변형) | Tier A val/OOS(Tier A 검증/표본외) | Tier B fallback-only val/OOS(Tier B 대체 전용 검증/표본외) | A+B actual routed val/OOS(A+B 실제 라우팅 검증/표본외) | Tier B contribution(Tier B 기여) |
|---|---|---|---|---|
| raw3_s045l045_h3_b060 | net 33.17/3.49, PF 1.01/1.0 | net 0.0/19.87, PF 0.0/0.0 | net 125.28/17.24, PF 1.05/1.01 | fallback bars 2779/1360 |
| inv3_s045l045_h3_b060 | net -126.82/144.8, PF 0.95/1.09 | net 0.0/0.0, PF 0.0/0.0 | net -194.7/104.69, PF 0.93/1.06 | fallback bars 2779/1360 |
| inv3_s050l043_h3_b060 | net -420.34/-183.79, PF 0.84/0.89 | net 0.0/0.0, PF 0.0/0.0 | net -494.22/-260.5, PF 0.81/0.85 | fallback bars 1884/1360 |
| inv3_s048l040_h2_b060 | net -360.08/-45.53, PF 0.89/0.98 | net 0.0/-21.34, PF 0.0/0.0 | net -431.85/-2.0, PF 0.87/1.0 | fallback bars 2779/1360 |
| inv3_s050l040_h2_b060 | net -289.09/-82.19, PF 0.91/0.96 | net 0.0/0.0, PF 0.0/0.0 | net -362.27/-44.36, PF 0.88/0.98 | fallback bars 2779/1360 |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture ratio(MFE 포착 비율) | winner truncation(승자 절단) | loser escape(패자 탈출) | re-entry 3/6/12(재진입 3/6/12봉) | same-move ratio(동일 이동 비율) | cost-stressed exp(비용 압박 기대값) | cooldown survives(쿨다운 생존) |
|---|---|---:|---:|---:|---|---:|---:|---:|
| raw3_s045l045_h3_b060 | validation_is | 0.625673 | 0.318471 | 0.283582 | 425/529/614 | 0.653191 | -0.366723 | False |
| raw3_s045l045_h3_b060 | oos | 0.617100 | 0.330275 | 0.277778 | 264/327/377 | 0.595577 | -0.472765 | False |
| inv3_s045l045_h3_b060 | validation_is | 0.630935 | 0.302376 | 0.316916 | 431/535/610 | 0.655914 | -0.709355 | False |
| inv3_s045l045_h3_b060 | oos | 0.651278 | 0.283333 | 0.339394 | 247/318/357 | 0.566667 | -0.333825 | False |
| inv3_s050l043_h3_b060 | validation_is | 0.608903 | 0.339726 | 0.299304 | 395/482/542 | 0.680905 | -1.120879 | False |
| inv3_s050l043_h3_b060 | oos | 0.634965 | 0.304348 | 0.312883 | 310/360/408 | 0.652800 | -0.916800 | False |
| inv3_s048l040_h2_b060 | validation_is | 0.584728 | 0.360335 | 0.264323 | 888/1024/1139 | 0.767520 | -0.791004 | False |
| inv3_s048l040_h2_b060 | oos | 0.604371 | 0.330769 | 0.295327 | 637/724/801 | 0.759242 | -0.501896 | False |
| inv3_s050l040_h2_b060 | validation_is | 0.583537 | 0.362687 | 0.286517 | 836/965/1053 | 0.761939 | -0.762135 | False |
| inv3_s050l040_h2_b060 | oos | 0.621157 | 0.310976 | 0.303089 | 604/702/773 | 0.765347 | -0.543921 | False |

## Current Read(현재 판독)

- best_variant(최선 변형): `raw3_s045l045_h3_b060`
- selected_research_baseline(선택 연구 기준선): `none`
- stage56_remains_open(56단계 열림 유지): `True`
- run50AP judgment(실행50AP 판정): fwd3(3봉) source branch(원천 분기)는 failure_memory(실패 기억)로 보존한다. Effect(효과): raw3(원방향 3봉)는 validation density(검증 밀도)는 통과했지만 validation/OOS PF(검증/표본외 수익 팩터)가 `1.05` / `1.01`에 그쳤고, inverse hold2(반전 보유2)는 OOS density(표본외 밀도) 5+/day를 만들었지만 validation/OOS net/PF(검증/표본외 순손익/수익 팩터)가 실패해 real density(실제 밀도) 원천이 되지 못했다.
- next_hypothesis_branch(다음 가설 가지): `run50AQ_model_family_diversity_branch`
