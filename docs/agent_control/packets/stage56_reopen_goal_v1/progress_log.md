# Stage56 Reopen Goal Progress Log(56단계 재개 목표 진행 기록)

- packet_id(묶음 ID): `stage56_reopen_goal_v1`
- stage_status(단계 상태): `active_in_progress(활성 진행 중)`
- latest_batch(최신 후보 묶음): `run50AZ_stage56_cooldown12_broad_model_source_v1`
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
| et10c12_h4_s160l090_a | extratrees_leaf10_cooldown12_no_side_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AZ/et10c12_h4_s160l090_a/mt5/reports/Project_Obsidian_Prime_v2_run50AZ_et10c12_h4_s160l090_a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AZ/et10c12_h4_s160l090_a/mt5/reports/Project_Obsidian_Prime_v2_run50AZ_et10c12_h4_s160l090_a_logreg_deep_v1_routed_oos.htm | 4.071038 | 3.092308 | 0.78 | 1.11 | -395.56 | 135.34 | validation_density; oos_density; validation_net_positive; validation_pf |
| et10c12_h4_s160l090_b | extratrees_leaf10_cooldown12_tier_b_damage_audit | true | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AZ/et10c12_h4_s160l090_b/mt5/reports/Project_Obsidian_Prime_v2_run50AZ_et10c12_h4_s160l090_b_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AZ/et10c12_h4_s160l090_b/mt5/reports/Project_Obsidian_Prime_v2_run50AZ_et10c12_h4_s160l090_b_logreg_deep_v1_routed_oos.htm | 4.163934 | 3.184615 | 0.8 | 1.11 | -379.85 | 133.66 | validation_density; oos_density; validation_net_positive; validation_pf |
| nf250c12_h4_s160l090_a | logreg_nonflat250_cooldown12_no_side_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AZ/nf250c12_h4_s160l090_a/mt5/reports/Project_Obsidian_Prime_v2_run50AZ_nf250c12_h4_s160l090_a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AZ/nf250c12_h4_s160l090_a/mt5/reports/Project_Obsidian_Prime_v2_run50AZ_nf250c12_h4_s160l090_a_logreg_deep_v1_routed_oos.htm | 4.513661 | 3.035897 | 1.03 | 0.91 | 45.74 | -118.83 | validation_density; oos_density; oos_net_positive; validation_pf |
| r24balc12_h4_s140l080_a | recent2024_balanced_cooldown12_no_side_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AZ/r24balc12_h4_s140l080_a/mt5/reports/Project_Obsidian_Prime_v2_run50AZ_r24balc12_h4_s140l080_a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AZ/r24balc12_h4_s140l080_a/mt5/reports/Project_Obsidian_Prime_v2_run50AZ_r24balc12_h4_s140l080_a_logreg_deep_v1_routed_oos.htm | 3.901639 | 2.958974 | 0.77 | 0.85 | -405.47 | -223.22 | validation_density; oos_density; validation_net_positive; oos_net_positive |

## Tier Views(티어 보기)

| variant(변형) | Tier A val/OOS(Tier A 검증/표본외) | Tier B fallback-only val/OOS(Tier B 대체 전용 검증/표본외) | A+B actual routed val/OOS(A+B 실제 라우팅 검증/표본외) | Tier B contribution(Tier B 기여) |
|---|---|---|---|---|
| et10c12_h4_s160l090_a | net -395.56/135.34, PF 0.78/1.11 | net -16.31/4.92, PF 0.07/1.44 | net -395.56/135.34, PF 0.78/1.11 | fallback bars None/None |
| et10c12_h4_s160l090_b | net -395.56/135.34, PF 0.78/1.11 | net -16.31/4.92, PF 0.07/1.44 | net -379.85/133.66, PF 0.8/1.11 | fallback bars None/None |
| nf250c12_h4_s160l090_a | net 45.74/-118.83, PF 1.03/0.91 | net -16.31/4.92, PF 0.07/1.44 | net 45.74/-118.83, PF 1.03/0.91 | fallback bars None/None |
| r24balc12_h4_s140l080_a | net -405.47/-223.22, PF 0.77/0.85 | net -16.31/4.92, PF 0.07/1.44 | net -405.47/-223.22, PF 0.77/0.85 | fallback bars None/None |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture ratio(MFE 포착 비율) | winner truncation(승자 절단) | loser escape(패자 탈출) | re-entry 3/6/12(재진입 3/6/12봉) | same-move ratio(동일 이동 비율) | cost-stressed exp(비용 압박 기대값) | cooldown survives(쿨다운 생존) |
|---|---|---:|---:|---:|---|---:|---:|---:|
| et10c12_h4_s160l090_a | validation_is | 0.600934 | 0.363905 | 0.275184 | 156/157/157 | 0.210738 | -1.030953 | False |
| et10c12_h4_s160l090_a | oos | 0.591983 | 0.365385 | 0.323024 | 136/139/139 | 0.230514 | -0.275556 | False |
| et10c12_h4_s160l090_b | validation_is | 0.605638 | 0.354467 | 0.267470 | 164/165/165 | 0.216535 | -0.998491 | False |
| et10c12_h4_s160l090_b | oos | 0.595894 | 0.356250 | 0.318937 | 143/146/146 | 0.235105 | -0.284767 | False |
| nf250c12_h4_s160l090_a | validation_is | 0.595652 | 0.345499 | 0.327711 | 140/147/148 | 0.179177 | -0.444625 | False |
| nf250c12_h4_s160l090_a | oos | 0.603662 | 0.340206 | 0.352159 | 69/70/70 | 0.118243 | -0.700726 | False |
| r24balc12_h4_s140l080_a | validation_is | 0.624638 | 0.308605 | 0.275862 | 155/155/155 | 0.217087 | -1.067885 | False |
| r24balc12_h4_s140l080_a | oos | 0.595075 | 0.345070 | 0.365188 | 140/141/141 | 0.244367 | -0.886863 | False |

## Current Read(현재 판독)

- best_variant(최선 변형): `nf250c12_h4_s160l090_a`
- selected_research_baseline(선택 연구 기준선): `none`
- stage56_remains_open(56단계 열림 유지): `True`
- next_hypothesis_branch(다음 가설 가지): `continue_density_repair_without_same_move_splitting_and_tier_b_damage_control`

## 2026-05-14T04:07:44Z run50BA Context-Timed Opportunity Source(문맥/시간 기회 원천)

- action(행동): slot/context rule(시간 구간/문맥 규칙)로 하루 여러 독립 신호를 만들고 actual MT5 validation/OOS(실제 MT5 검증/표본외)를 실행했다.
- effect(효과): threshold relaxation(문턱값 완화)이 아니라 opportunity source(기회 원천) 자체가 density/PF/net(밀도/수익 팩터/순손익)을 만들 수 있는지 확인했다.
- best_variant(현재 최선 변형): `v09_slot30_cycle_dense_h2c12_no_b`
- validation/OOS trades/day(검증/표본외 일 거래): `0.000000` / `0.000000`
- validation/OOS PF(검증/표본외 수익 팩터): `` / ``
- validation/OOS net(검증/표본외 순손익): `` / ``
- decision(결정): selected_research_baseline(선택 연구 기준선)=`none`; failure_reasons(실패 사유)=`validation_density;oos_density;validation_net_positive;oos_net_positive;validation_pf;oos_pf;cost_stressed_expectancy;same_move_density`.

## 2026-05-14T04:20:40Z run50BA Context-Timed Opportunity Source(문맥/시간 기회 원천)

- action(행동): slot/context rule(시간 구간/문맥 규칙)로 하루 여러 독립 신호를 만들고 actual MT5 validation/OOS(실제 MT5 검증/표본외)를 실행했다.
- effect(효과): threshold relaxation(문턱값 완화)이 아니라 opportunity source(기회 원천) 자체가 density/PF/net(밀도/수익 팩터/순손익)을 만들 수 있는지 확인했다.
- best_variant(현재 최선 변형): `v11_slot30_dense_control_h2c12_with_b`
- validation/OOS trades/day(검증/표본외 일 거래): `3.295082` / `2.200000`
- validation/OOS PF(검증/표본외 수익 팩터): `1.170000` / `1.320000`
- validation/OOS net(검증/표본외 순손익): `188.87` / `265.10`
- decision(결정): selected_research_baseline(선택 연구 기준선)=`none`; failure_reasons(실패 사유)=`validation_density;oos_density;cost_stressed_expectancy;same_move_density`.

## 2026-05-14T04:25:46Z run50BB Context-Timed No Runtime Cooldown(문맥/시간 런타임 쿨다운 없음)

- action(행동): runtime re-entry cooldown(런타임 재진입 쿨다운)을 0으로 낮추고 audit cooldown(감사 쿨다운)을 별도 기록했다.
- effect(효과): actual density(실제 밀도)가 execution setting(실행 설정) 때문에 눌렸는지 확인했다.
- best_variant(현재 최선 변형): `v13_slot30_dense_control_h2c0_with_b`
- validation/OOS trades/day(검증/표본외 일 거래): `0.000000` / `0.000000`
- validation/OOS PF(검증/표본외 수익 팩터): `` / ``
- validation/OOS net(검증/표본외 순손익): `` / ``
- decision(결정): selected_research_baseline(선택 연구 기준선)=`none`; failure_reasons(실패 사유)=`validation_density;oos_density;validation_net_positive;oos_net_positive;validation_pf;oos_pf;cost_stressed_expectancy;same_move_density`.

## 2026-05-14T04:40:52Z run50BB Context-Timed No Runtime Cooldown(문맥/시간 런타임 쿨다운 없음)

- action(행동): runtime re-entry cooldown(런타임 재진입 쿨다운)을 0으로 낮추고 audit cooldown(감사 쿨다운)을 별도 기록했다.
- effect(효과): actual density(실제 밀도)가 execution setting(실행 설정) 때문에 눌렸는지 확인했다.
- best_variant(현재 최선 변형): `v13_slot30_dense_control_h2c0_with_b`
- validation/OOS trades/day(검증/표본외 일 거래): `7.704918` / `5.194872`
- validation/OOS PF(검증/표본외 수익 팩터): `1.080000` / `1.040000`
- validation/OOS net(검증/표본외 순손익): `211.37` / `82.250000`
- decision(결정): selected_research_baseline(선택 연구 기준선)=`none`; failure_reasons(실패 사유)=`validation_pf;oos_pf;cost_stressed_expectancy;same_move_density`.

## 2026-05-14T04:49:36Z run50BC Context-Timed Alternating Slot(문맥/시간 교대 슬롯)

- action(행동): 40/45-minute alternating slot(40/45분 교대 슬롯) 원천을 actual MT5 validation/OOS(실제 MT5 검증/표본외)로 실행했다.
- effect(효과): raw density(원 거래 밀도)와 same-move density(동일 이동 밀도)를 동시에 볼 수 있게 했다.
- best_variant(현재 최선 변형): `v17_slot40_even_short_odd_long_context_h2c0_no_b`
- validation/OOS trades/day(검증/표본외 일 거래): `0.000000` / `0.000000`
- validation/OOS PF(검증/표본외 수익 팩터): `` / ``
- validation/OOS net(검증/표본외 순손익): `` / ``
- decision(결정): selected_research_baseline(선택 연구 기준선)=`none`; failure_reasons(실패 사유)=`validation_density;oos_density;validation_net_positive;oos_net_positive;validation_pf;oos_pf;cost_stressed_expectancy;same_move_density`.

## 2026-05-14T05:07:53Z run50BC Context-Timed Alternating Slot(문맥/시간 교대 슬롯)

- action(행동): 40/45-minute alternating slot(40/45분 교대 슬롯) 원천을 actual MT5 validation/OOS(실제 MT5 검증/표본외)로 실행했다.
- effect(효과): raw density(원 거래 밀도)와 same-move density(동일 이동 밀도)를 동시에 볼 수 있게 했다.
- best_variant(현재 최선 변형): `v19_slot40_even_short_odd_long_always_h2c0_no_b`
- validation/OOS trades/day(검증/표본외 일 거래): `8.240437` / `5.656410`
- validation/OOS PF(검증/표본외 수익 팩터): `0.960000` / `0.920000`
- validation/OOS net(검증/표본외 순손익): `-92.750000` / `-142.02`
- decision(결정): selected_research_baseline(선택 연구 기준선)=`none`; failure_reasons(실패 사유)=`validation_net_positive;oos_net_positive;validation_pf;oos_pf;cost_stressed_expectancy`.

## 2026-05-14T05:28:22Z run50BD Context-Timed Quality-Gated Slot(문맥/시간 품질 필터 슬롯)

- action(행동): train/validation(학습/검증) 2-bar proxy(2봉 대리 지표)로 quality-gated alternating slot(품질 필터 교대 슬롯)을 만들고 actual MT5 validation/OOS(실제 MT5 검증/표본외)를 실행했다.
- effect(효과): run50BC(실행50BC)의 density(밀도) 성과가 단순 분할이 아니라 품질 있는 opportunity source(기회 원천)로 변하는지 확인했다.
- best_variant(현재 최선 변형): `v21_w40_esol_highcov_lr2_h2c0_no_b`
- validation/OOS trades/day(검증/표본외 일 거래 수): `0.000000` / `0.000000`
- validation/OOS PF(검증/표본외 수익 팩터): `` / ``
- validation/OOS net(검증/표본외 순손익): `` / ``
- decision(결정): selected_research_baseline(선택 연구 기준선)=`none`; failure_reasons(실패 사유)=`validation_density;oos_density;validation_net_positive;oos_net_positive;validation_pf;oos_pf;cost_stressed_expectancy;same_move_density`.

## 2026-05-14T05:51:14Z run50BD Context-Timed Quality-Gated Slot(문맥/시간 품질 필터 슬롯)

- action(행동): train/validation(학습/검증) 2-bar proxy(2봉 대리 지표)로 quality-gated alternating slot(품질 필터 교대 슬롯)을 만들고 actual MT5 validation/OOS(실제 MT5 검증/표본외)를 실행했다.
- effect(효과): run50BC(실행50BC)의 density(밀도) 성과가 단순 분할이 아니라 품질 있는 opportunity source(기회 원천)로 변하는지 확인했다.
- best_variant(현재 최선 변형): `v25_w40_esol_highcov_lr2_h2c0_with_b`
- validation/OOS trades/day(검증/표본외 일 거래 수): `8.923497` / `5.784615`
- validation/OOS PF(검증/표본외 수익 팩터): `1.140000` / `0.970000`
- validation/OOS net(검증/표본외 순손익): `276.21` / `-43.280000`
- decision(결정): selected_research_baseline(선택 연구 기준선)=`none`; failure_reasons(실패 사유)=`oos_net_positive;oos_pf;cost_stressed_expectancy;same_move_density`.

## 2026-05-14T05:59:19Z run50BE V22 Density Top-Up(밀도 보강)

- action(행동): run50BD(실행50BD) v22를 기준으로 slot relaxation(슬롯 완화)과 Tier B fallback(Tier B 대체)을 actual MT5 validation/OOS(실제 MT5 검증/표본외)에서 비교했다.
- effect(효과): OOS-positive under-dense(표본외 양수이나 밀도 부족) 후보가 5/day(일 5회) 밀도까지 확장 가능한지 확인했다.
- best_variant(현재 최선 변형): `v26_v22_slot8_relax_h2c0_no_b`
- validation/OOS trades/day(검증/표본외 일 거래 수): `0.000000` / `0.000000`
- validation/OOS PF(검증/표본외 수익 팩터): `` / ``
- validation/OOS net(검증/표본외 순손익): `` / ``
- decision(결정): selected_research_baseline(선택 연구 기준선)=`none`; failure_reasons(실패 사유)=`validation_density;oos_density;validation_net_positive;oos_net_positive;validation_pf;oos_pf;cost_stressed_expectancy;same_move_density`.

## 2026-05-14T06:17:27Z run50BE V22 Density Top-Up(밀도 보강)

- action(행동): run50BD(실행50BD) v22를 기준으로 slot relaxation(슬롯 완화)과 Tier B fallback(Tier B 대체)을 actual MT5 validation/OOS(실제 MT5 검증/표본외)에서 비교했다.
- effect(효과): OOS-positive under-dense(표본외 양수이나 밀도 부족) 후보가 5/day(일 5회) 밀도까지 확장 가능한지 확인했다.
- best_variant(현재 최선 변형): `v30_v22_midcov_h2c0_with_b`
- validation/OOS trades/day(검증/표본외 일 거래 수): `8.349727` / `5.323077`
- validation/OOS PF(검증/표본외 수익 팩터): `1.140000` / `1.050000`
- validation/OOS net(검증/표본외 순손익): `271.43` / `78.850000`
- decision(결정): selected_research_baseline(선택 연구 기준선)=`none`; failure_reasons(실패 사유)=`oos_pf;cost_stressed_expectancy;same_move_density`.

## 2026-05-14T06:23:44Z run50BF Context-Timed Lifecycle Probe(생명주기 탐침)

- action(행동): run50BE(실행50BE) v30의 source/routing(원천/라우팅)을 유지하고 max hold/re-entry cooldown(최대 보유/재진입 쿨다운)을 바꿔 actual MT5 validation/OOS(실제 MT5 검증/표본외)를 실행했다.
- effect(효과): same-move/cost stress(동일 이동/비용 압박)가 lifecycle(생명주기) 문제인지 확인했다.
- best_variant(현재 최선 변형): `v31_v22_midcov_h1c0_with_b`
- validation/OOS trades/day(검증/표본외 일 거래 수): `0.000000` / `0.000000`
- validation/OOS PF(검증/표본외 수익 팩터): `` / ``
- validation/OOS net(검증/표본외 순손익): `` / ``
- decision(결정): selected_research_baseline(선택 연구 기준선)=`none`; failure_reasons(실패 사유)=`validation_density;oos_density;validation_net_positive;oos_net_positive;validation_pf;oos_pf;cost_stressed_expectancy;same_move_density`.

## 2026-05-14T06:41:00Z run50BF Context-Timed Lifecycle Probe(생명주기 탐침)

- action(행동): run50BE(실행50BE) v30의 source/routing(원천/라우팅)을 유지하고 max hold/re-entry cooldown(최대 보유/재진입 쿨다운)을 바꿔 actual MT5 validation/OOS(실제 MT5 검증/표본외)를 실행했다.
- effect(효과): same-move/cost stress(동일 이동/비용 압박)가 lifecycle(생명주기) 문제인지 확인했다.
- best_variant(현재 최선 변형): `v31_v22_midcov_h1c0_with_b`
- validation/OOS trades/day(검증/표본외 일 거래 수): `8.628415` / `5.538462`
- validation/OOS PF(검증/표본외 수익 팩터): `1.050000` / `0.960000`
- validation/OOS net(검증/표본외 순손익): `67.720000` / `-38.620000`
- decision(결정): selected_research_baseline(선택 연구 기준선)=`none`; failure_reasons(실패 사유)=`oos_net_positive;validation_pf;oos_pf;cost_stressed_expectancy;same_move_density`.

## 2026-05-14T06:52:04Z run50BG Context-Timed Hold3 Top-Up(문맥/시간 3봉 보유 보강)

- action(행동): hold3(3봉 보유) control(대조군)과 slot top-up(슬롯 보강)을 actual MT5 validation/OOS(실제 MT5 검증/표본외)에서 비교했다.
- effect(효과): Tier B(티어B)를 끈 상태에서 실제 밀도(real density, 실제 밀도)와 품질(quality, 품질)이 동시에 회복되는지 확인했다.
- best_variant(현재 최선 변형): `v36_v22_midcov_h3c0_no_b_control`
- validation/OOS trades/day(검증/표본외 일 거래 수): `0.000000` / `0.000000`
- validation/OOS PF(검증/표본외 수익 팩터): `` / ``
- validation/OOS net(검증/표본외 순손익): `` / ``
- decision(결정): selected_research_baseline(선택 연구 기준선)=`none`; failure_reasons(실패 사유)=`validation_density;oos_density;validation_net_positive;oos_net_positive;validation_pf;oos_pf;cost_stressed_expectancy;same_move_density`.

## 2026-05-14T07:08:36Z run50BG Context-Timed Hold3 Top-Up(문맥/시간 3봉 보유 보강)

- action(행동): hold3(3봉 보유) control(대조군)과 slot top-up(슬롯 보강)을 actual MT5 validation/OOS(실제 MT5 검증/표본외)에서 비교했다.
- effect(효과): Tier B(티어B)를 끈 상태에서 실제 밀도(real density, 실제 밀도)와 품질(quality, 품질)이 동시에 회복되는지 확인했다.
- best_variant(현재 최선 변형): `v40_v22_slot3_5_8_relax_h3c0_no_b`
- validation/OOS trades/day(검증/표본외 일 거래 수): `6.688525` / `4.666667`
- validation/OOS PF(검증/표본외 수익 팩터): `1.150000` / `0.950000`
- validation/OOS net(검증/표본외 순손익): `409.35` / `-108.13`
- decision(결정): selected_research_baseline(선택 연구 기준선)=`none`; failure_reasons(실패 사유)=`oos_density;oos_net_positive;oos_pf;cost_stressed_expectancy;same_move_density`.
