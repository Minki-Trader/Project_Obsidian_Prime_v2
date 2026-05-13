# Stage56 Reopen Goal Progress Log(56단계 재개 목표 진행 기록)

- packet_id(묶음 ID): `stage56_reopen_goal_v1`
- stage_status(단계 상태): `active_in_progress(활성 진행 중)`
- latest_batch(최신 후보 묶음): `run50AO_stage56_lgbm_fwd6_inverse_side_threshold_repair_v1`
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
| inv6_s048l045_h3_b060 | inverse_short_firewall_hold3 | true | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AO/inv6_s048l045_h3_b060/mt5/reports/Project_Obsidian_Prime_v2_run50AO_inv6_s048l045_h3_b060_lgbm_fwd6_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AO/inv6_s048l045_h3_b060/mt5/reports/Project_Obsidian_Prime_v2_run50AO_inv6_s048l045_h3_b060_lgbm_fwd6_v1_routed_oos.htm | 4.60655737704918 | 3.1487179487179486 | 1.05 | 1.12 | 107.95 | 195.67 | validation_density; oos_density; validation_pf; cost_stressed_expectancy |
| inv6_s050l045_h3_b060 | inverse_stronger_short_firewall_hold3 | true | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AO/inv6_s050l045_h3_b060/mt5/reports/Project_Obsidian_Prime_v2_run50AO_inv6_s050l045_h3_b060_lgbm_fwd6_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AO/inv6_s050l045_h3_b060/mt5/reports/Project_Obsidian_Prime_v2_run50AO_inv6_s050l045_h3_b060_lgbm_fwd6_v1_routed_oos.htm | 4.273224043715847 | 2.8974358974358974 | 1.08 | 1.11 | 164.1 | 158.45 | validation_density; oos_density; validation_pf; cost_stressed_expectancy |
| inv6_s052l045_h3_b060 | inverse_max_short_firewall_hold3 | true | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AO/inv6_s052l045_h3_b060/mt5/reports/Project_Obsidian_Prime_v2_run50AO_inv6_s052l045_h3_b060_lgbm_fwd6_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AO/inv6_s052l045_h3_b060/mt5/reports/Project_Obsidian_Prime_v2_run50AO_inv6_s052l045_h3_b060_lgbm_fwd6_v1_routed_oos.htm | 4.092896174863388 | 2.5794871794871796 | 1.02 | 1.08 | 36.18 | 103.93 | validation_density; oos_density; validation_pf; oos_pf |
| inv6_s048l043_h3_b060 | inverse_long_density_restore_hold3 | true | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AO/inv6_s048l043_h3_b060/mt5/reports/Project_Obsidian_Prime_v2_run50AO_inv6_s048l043_h3_b060_lgbm_fwd6_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AO/inv6_s048l043_h3_b060/mt5/reports/Project_Obsidian_Prime_v2_run50AO_inv6_s048l043_h3_b060_lgbm_fwd6_v1_routed_oos.htm | 5.6502732240437155 | 3.887179487179487 | 1.02 | 1.11 | 58.04 | 199.36 | oos_density; validation_pf; cost_stressed_expectancy; same_move_density |
| inv6_s050l043_h3_b060 | inverse_firewall_long_density_hold3 | true | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AO/inv6_s050l043_h3_b060/mt5/reports/Project_Obsidian_Prime_v2_run50AO_inv6_s050l043_h3_b060_lgbm_fwd6_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AO/inv6_s050l043_h3_b060/mt5/reports/Project_Obsidian_Prime_v2_run50AO_inv6_s050l043_h3_b060_lgbm_fwd6_v1_routed_oos.htm | 5.278688524590164 | 3.6769230769230767 | 1.14 | 1.1 | 318.69 | 179.25 | oos_density; cost_stressed_expectancy; same_move_density; tier_b_rule |

## Tier Views(티어 보기)

| variant(변형) | Tier A val/OOS(Tier A 검증/표본외) | Tier B fallback-only val/OOS(Tier B 대체 전용 검증/표본외) | A+B actual routed val/OOS(A+B 실제 라우팅 검증/표본외) | Tier B contribution(Tier B 기여) |
|---|---|---|---|---|
| inv6_s048l045_h3_b060 | net 108.98/220.91, PF 1.05/1.14 | net 0.0/11.6, PF 0.0/2.15 | net 107.95/195.67, PF 1.05/1.12 | fallback bars 2647/1250 |
| inv6_s050l045_h3_b060 | net 189.58/286.32, PF 1.09/1.21 | net 2.52/-19.78, PF 0.0/0.52 | net 164.1/158.45, PF 1.08/1.11 | fallback bars 2647/1250 |
| inv6_s052l045_h3_b060 | net 91.31/117.18, PF 1.05/1.09 | net 0.0/14.6, PF 0.0/2.44 | net 36.18/103.93, PF 1.02/1.08 | fallback bars 2647/1250 |
| inv6_s048l043_h3_b060 | net 81.13/272.29, PF 1.03/1.16 | net -2.66/1.38, PF 0.49/1.07 | net 58.04/199.36, PF 1.02/1.11 | fallback bars 2647/1250 |
| inv6_s050l043_h3_b060 | net 289.4/265.87, PF 1.12/1.15 | net 0.0/-9.87, PF 0.0/0.69 | net 318.69/179.25, PF 1.14/1.1 | fallback bars 2647/1250 |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture ratio(MFE 포착 비율) | winner truncation(승자 절단) | loser escape(패자 탈출) | re-entry 3/6/12(재진입 3/6/12봉) | same-move ratio(동일 이동 비율) | cost-stressed exp(비용 압박 기대값) | cooldown survives(쿨다운 생존) |
|---|---|---:|---:|---:|---|---:|---:|---:|
| inv6_s048l045_h3_b060 | validation_is | 0.607787 | 0.326829 | 0.321016 | 439/517/557 | 0.660735 | -0.371945 | False |
| inv6_s048l045_h3_b060 | oos | 0.630801 | 0.305994 | 0.356902 | 304/344/388 | 0.631922 | -0.181319 | False |
| inv6_s050l045_h3_b060 | validation_is | 0.615653 | 0.328165 | 0.308861 | 401/474/516 | 0.659847 | -0.290153 | False |
| inv6_s050l045_h3_b060 | oos | 0.652341 | 0.278351 | 0.339416 | 262/314/346 | 0.612389 | -0.219558 | False |
| inv6_s052l045_h3_b060 | validation_is | 0.598491 | 0.337017 | 0.294574 | 390/448/481 | 0.642190 | -0.451696 | False |
| inv6_s052l045_h3_b060 | oos | 0.615459 | 0.340909 | 0.347280 | 234/280/315 | 0.626243 | -0.293380 | False |
| inv6_s048l043_h3_b060 | validation_is | 0.626759 | 0.304703 | 0.322936 | 561/644/716 | 0.692456 | -0.443868 | False |
| inv6_s048l043_h3_b060 | oos | 0.631872 | 0.288770 | 0.356771 | 385/440/502 | 0.662269 | -0.236992 | False |
| inv6_s050l043_h3_b060 | validation_is | 0.619253 | 0.308977 | 0.320329 | 519/604/667 | 0.690476 | -0.170093 | False |
| inv6_s050l043_h3_b060 | oos | 0.639853 | 0.287671 | 0.352273 | 380/430/488 | 0.680614 | -0.250000 | False |

## Current Read(현재 판독)

- best_variant(최선 변형): `inv6_s050l043_h3_b060`
- selected_research_baseline(선택 연구 기준선): `none`
- stage56_remains_open(56단계 열림 유지): `True`
- run50AO judgment(실행50AO 판정): `inv6_s050l043_h3_b060`은 validation(검증) density/PF/net(밀도/수익 팩터/순손익)를 통과하고 OOS PF(표본외 수익 팩터)를 `1.1004`까지 회복했지만 OOS density(표본외 밀도) `3.676923/day`, cost-stressed expectancy(비용 압박 기대값) `-0.25`, same-move ratio(동일 이동 비율) `0.680614`, Tier B fallback-only OOS(Tier B 대체 전용 표본외) `-9.87`로 hard condition(강한 완료 조건)에 부족하다.
- next_hypothesis_branch(다음 가설 가지): `run50AP_new_source_real_density_branch`
