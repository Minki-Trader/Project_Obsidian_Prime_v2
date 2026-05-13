# Stage56 Reopen Goal Progress Log(56단계 재개 목표 진행 기록)

- packet_id(묶음 ID): `stage56_reopen_goal_v1`
- stage_status(단계 상태): `active_in_progress(활성 진행 중)`
- latest_batch(최신 후보 묶음): `run50AM_stage56_lgbm_fwd6_density_branch_v1`
- selected_research_baseline(선택 연구 기준선): `none`
- terminal_condition(종료 조건): selected_research_baseline(선택 연구 기준선) found(발견)
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
| lgbm6_s048l045_h4_b060 | short_horizon_density_asym | true | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AM/lgbm6_s048l045_h4_b060/mt5/reports/Project_Obsidian_Prime_v2_run50AM_lgbm6_s048l045_h4_b060_lgbm_fwd6_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AM/lgbm6_s048l045_h4_b060/mt5/reports/Project_Obsidian_Prime_v2_run50AM_lgbm6_s048l045_h4_b060_lgbm_fwd6_v1_routed_oos.htm | 2.2185792349726774 | 2.8205128205128207 | 0.69 | 0.77 | -496.02 | -448.65 | validation_density; oos_density; validation_net_positive; oos_net_positive |
| lgbm6_s045l045_h4_b060 | short_horizon_density_symmetric | true | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AM/lgbm6_s045l045_h4_b060/mt5/reports/Project_Obsidian_Prime_v2_run50AM_lgbm6_s045l045_h4_b060_lgbm_fwd6_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AM/lgbm6_s045l045_h4_b060/mt5/reports/Project_Obsidian_Prime_v2_run50AM_lgbm6_s045l045_h4_b060_lgbm_fwd6_v1_routed_oos.htm | 2.5737704918032787 | 3.348717948717949 | 0.7 | 0.81 | -496.35 | -412.52 | validation_density; oos_density; validation_net_positive; oos_net_positive |
| lgbm6_s050l045_h4_b060 | short_horizon_short_firewall | true | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AM/lgbm6_s050l045_h4_b060/mt5/reports/Project_Obsidian_Prime_v2_run50AM_lgbm6_s050l045_h4_b060_lgbm_fwd6_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AM/lgbm6_s050l045_h4_b060/mt5/reports/Project_Obsidian_Prime_v2_run50AM_lgbm6_s050l045_h4_b060_lgbm_fwd6_v1_routed_oos.htm | 2.442622950819672 | 2.5743589743589745 | 0.73 | 0.83 | -495.84 | -288.19 | validation_density; oos_density; validation_net_positive; oos_net_positive |
| lgbm6_s048l045_h6_b060 | short_horizon_hold6_quality | true | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AM/lgbm6_s048l045_h6_b060/mt5/reports/Project_Obsidian_Prime_v2_run50AM_lgbm6_s048l045_h6_b060_lgbm_fwd6_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AM/lgbm6_s048l045_h6_b060/mt5/reports/Project_Obsidian_Prime_v2_run50AM_lgbm6_s048l045_h6_b060_lgbm_fwd6_v1_routed_oos.htm | 3.387978142076503 | 2.3794871794871795 | 0.83 | 0.79 | -411.56 | -394.85 | validation_density; oos_density; validation_net_positive; oos_net_positive |

## Tier Views(티어 보기)

| variant(변형) | Tier A val/OOS(Tier A 검증/표본외) | Tier B fallback-only val/OOS(Tier B 대체 전용 검증/표본외) | A+B actual routed val/OOS(A+B 실제 라우팅 검증/표본외) | Tier B contribution(Tier B 기여) |
|---|---|---|---|---|
| lgbm6_s048l045_h4_b060 | net -510.95/-510.34, PF 0.71/0.74 | net 0.0/14.76, PF 0.0/0.0 | net -496.02/-448.65, PF 0.69/0.77 | fallback bars 747/1250 |
| lgbm6_s045l045_h4_b060 | net -496.63/-429.19, PF 0.7/0.81 | net -4.0/-7.25, PF 0.0/0.67 | net -496.35/-412.52, PF 0.7/0.81 | fallback bars 747/1250 |
| lgbm6_s050l045_h4_b060 | net -496.13/-350.41, PF 0.73/0.8 | net 5.27/14.76, PF 2.32/0.0 | net -495.84/-288.19, PF 0.73/0.83 | fallback bars 747/1250 |
| lgbm6_s048l045_h6_b060 | net -431.63/-447.0, PF 0.83/0.77 | net 0.0/3.51, PF 0.0/1.08 | net -411.56/-394.85, PF 0.83/0.79 | fallback bars 2647/1250 |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture ratio(MFE 포착 비율) | winner truncation(승자 절단) | loser escape(패자 탈출) | re-entry 3/6/12(재진입 3/6/12봉) | same-move ratio(동일 이동 비율) | cost-stressed exp(비용 압박 기대값) | cooldown survives(쿨다운 생존) |
|---|---|---:|---:|---:|---|---:|---:|---:|
| lgbm6_s048l045_h4_b060 | validation_is | 0.641810 | 0.277457 | 0.347639 | 213/251/280 | 0.689655 | -1.721724 | False |
| lgbm6_s048l045_h4_b060 | oos | 0.618021 | 0.328185 | 0.302405 | 242/287/324 | 0.589091 | -1.315727 | False |
| lgbm6_s045l045_h4_b060 | validation_is | 0.611140 | 0.311927 | 0.320158 | 261/303/330 | 0.700637 | -1.553822 | False |
| lgbm6_s045l045_h4_b060 | oos | 0.606861 | 0.332258 | 0.317784 | 308/355/403 | 0.617152 | -1.131730 | False |
| lgbm6_s050l045_h4_b060 | validation_is | 0.604442 | 0.320197 | 0.356557 | 241/273/304 | 0.680089 | -1.609262 | False |
| lgbm6_s050l045_h4_b060 | oos | 0.589624 | 0.356000 | 0.337302 | 210/256/287 | 0.571713 | -1.074084 | False |
| lgbm6_s048l045_h6_b060 | validation_is | 0.631646 | 0.303754 | 0.311927 | 239/291/340 | 0.548387 | -1.163806 | False |
| lgbm6_s048l045_h6_b060 | oos | 0.637338 | 0.299107 | 0.283333 | 153/189/230 | 0.495690 | -1.350970 | False |

## Current Read(현재 판독)

- best_variant(최선 변형): `lgbm6_s048l045_h6_b060`
- selected_research_baseline(선택 연구 기준선): `none`
- stage56_remains_open(56단계 열림 유지): `True`
- next_hypothesis_branch(다음 가설 가지): `continue_density_repair_without_same_move_splitting_and_tier_b_damage_control`
