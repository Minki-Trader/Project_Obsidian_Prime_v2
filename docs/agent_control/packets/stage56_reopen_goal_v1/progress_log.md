# Stage56 Reopen Goal Progress Log(56단계 재개 목표 진행 기록)

- packet_id(묶음 ID): `stage56_reopen_goal_v1`
- stage_status(단계 상태): `active_in_progress(활성 진행 중)`
- latest_batch(최신 후보 묶음): `run50AL_stage56_entry_confidence_rearm_v1`
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
| nfal_s33l20_r020 | entry_rearm_delta020_anchor | true | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AL/nfal_s33l20_r020/mt5/reports/Project_Obsidian_Prime_v2_run50AL_nfal_s33l20_r020_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AL/nfal_s33l20_r020/mt5/reports/Project_Obsidian_Prime_v2_run50AL_nfal_s33l20_r020_logreg_deep_v1_routed_oos.htm | 7.202186 | 4.789744 | 1.13 | 1.09 | 423.32 | 213.37 | oos_density; oos_pf; cost_stressed_expectancy; same_move_density |
| nfal_s33l20_r040 | entry_rearm_delta040_anchor | true | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AL/nfal_s33l20_r040/mt5/reports/Project_Obsidian_Prime_v2_run50AL_nfal_s33l20_r040_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AL/nfal_s33l20_r040/mt5/reports/Project_Obsidian_Prime_v2_run50AL_nfal_s33l20_r040_logreg_deep_v1_routed_oos.htm | 5.530055 | 3.651282 | 1.16 | 1.18 | 373.47 | 310.99 | oos_density; cost_stressed_expectancy; same_move_density |
| nfal_s33l20_r060 | entry_rearm_delta060_anchor | true | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AL/nfal_s33l20_r060/mt5/reports/Project_Obsidian_Prime_v2_run50AL_nfal_s33l20_r060_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AL/nfal_s33l20_r060/mt5/reports/Project_Obsidian_Prime_v2_run50AL_nfal_s33l20_r060_logreg_deep_v1_routed_oos.htm | 4.857923 | 3.292308 | 1.19 | 1.25 | 383.21 | 390.95 | validation_density; oos_density; cost_stressed_expectancy; same_move_density |
| nfal_s33l20_r040l40 | entry_rearm_delta040_long_firewall | true | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AL/nfal_s33l20_r040l40/mt5/reports/Project_Obsidian_Prime_v2_run50AL_nfal_s33l20_r040l40_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AL/nfal_s33l20_r040l40/mt5/reports/Project_Obsidian_Prime_v2_run50AL_nfal_s33l20_r040l40_logreg_deep_v1_routed_oos.htm | 5.300546 | 3.574359 | 1.15 | 1.19 | 347.36 | 324.45 | oos_density; cost_stressed_expectancy; same_move_density |

## Tier Views(티어 보기)

| variant(변형) | Tier A val/OOS(Tier A 검증/표본외) | Tier B fallback-only val/OOS(Tier B 대체 전용 검증/표본외) | A+B actual routed val/OOS(A+B 실제 라우팅 검증/표본외) | Tier B contribution(Tier B 기여) |
|---|---|---|---|---|
| nfal_s33l20_r020 | net 399.0/224.32, PF 1.12/1.09 | net -82.21/5.24, PF 0.09/1.27 | net 423.32/213.37, PF 1.13/1.09 | fallback bars None/None |
| nfal_s33l20_r040 | net 367.32/311.21, PF 1.16/1.18 | net -82.21/5.24, PF 0.09/1.27 | net 373.47/310.99, PF 1.16/1.18 | fallback bars None/None |
| nfal_s33l20_r060 | net 368.93/385.36, PF 1.18/1.25 | net -82.21/5.24, PF 0.09/1.27 | net 383.21/390.95, PF 1.19/1.25 | fallback bars None/None |
| nfal_s33l20_r040l40 | net 335.88/333.32, PF 1.15/1.2 | net -65.42/6.63, PF 0.11/1.37 | net 347.36/324.45, PF 1.15/1.19 | fallback bars None/None |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture ratio(MFE 포착 비율) | winner truncation(승자 절단) | loser escape(패자 탈출) | re-entry 3/6/12(재진입 3/6/12봉) | same-move ratio(동일 이동 비율) | cost-stressed exp(비용 압박 기대값) | cooldown survives(쿨다운 생존) |
|---|---|---:|---:|---:|---|---:|---:|---:|
| nfal_s33l20_r020 | validation_is | 0.610455 | 0.329231 | 0.330838 | 543/747/932 | 0.707132 | -0.178816 | False |
| nfal_s33l20_r020 | oos | 0.597298 | 0.366197 | 0.350114 | 340/492/620 | 0.663812 | -0.271552 | False |
| nfal_s33l20_r040 | validation_is | 0.611627 | 0.330000 | 0.322266 | 314/420/529 | 0.522727 | -0.130958 | False |
| nfal_s33l20_r040 | oos | 0.590385 | 0.380697 | 0.351032 | 191/265/353 | 0.495787 | -0.063216 | False |
| nfal_s33l20_r060 | validation_is | 0.600843 | 0.353881 | 0.290466 | 264/347/423 | 0.475816 | -0.068943 | False |
| nfal_s33l20_r060 | oos | 0.601398 | 0.367647 | 0.344371 | 166/226/293 | 0.456386 | 0.108956 | False |
| nfal_s33l20_r040l40 | validation_is | 0.615695 | 0.326360 | 0.333333 | 285/395/503 | 0.518557 | -0.141897 | False |
| nfal_s33l20_r040l40 | oos | 0.600974 | 0.360434 | 0.359756 | 176/255/341 | 0.489240 | -0.034505 | False |

## Current Read(현재 판독)

- best_variant(최선 변형): `nfal_s33l20_r060`
- selected_research_baseline(선택 연구 기준선): `none`
- stage56_remains_open(56단계 열림 유지): `True`
- next_hypothesis_branch(다음 가설 가지): `separate_model_or_feature_source_after_rearm_density_realness_tradeoff`
