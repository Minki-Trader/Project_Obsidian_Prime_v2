# Stage56 Reopen Goal Progress Log(56단계 재개 목표 진행 기록)

- packet_id(묶음 ID): `stage56_reopen_goal_v1`
- stage_status(단계 상태): `active_in_progress(활성 진행 중)`
- latest_batch(최신 후보 묶음): `run50AV_stage56_cooldown12_new_source_density_survival_v1`
- selected_research_baseline(선택 연구 기준선): `none`
- terminal_condition(종료 조건): useful BaselineAdapter(유용한 기준선 어댑터) hard condition(강한 완료 조건) not_satisfied(미충족)
- non_final_prior_packets(비최종 이전 묶음): `stage56_closeout_v1`, `stage56_reopened_closeout_v2`

Stage56(56단계)은 unfinished optimization campaign(미완 최적화 캠페인)으로 open(열림) 상태다.
Effect(효과): progress log(진행 기록)는 Stage56(56단계)을 닫지 않고 다음 hypothesis branch(가설 가지)를 정한다.

## Current Bottleneck(현재 병목)

- density(밀도): selected_research_baseline(선택 연구 기준선)은 validation/OOS(검증/표본외) 모두 5+ trades/day(일 거래 수)를 요구한다.
- Tier B OOS damage(Tier B 표본외 손상): Tier B fallback-only OOS(Tier B 대체 전용 표본외)가 음수이면 disablement(비활성화) 근거가 필요하다.
- hold compression audit(보유 압축 감사): density gain(밀도 증가)이 same-move split-trading(동일 이동 분할 거래)인지 확인해야 한다.

## Run50AV Failure Read(실행50AV 실패 판독)

- action(행동): actual cooldown12(실제 12봉 쿨다운)을 MT5 execution translation(MT5 실행 변환)에 넣고 ExtraTrees/logreg source(엑스트라트리스/로지스틱 원천)를 다시 검증했다.
- effect(효과): same-move ratio(동일 이동 비율)는 `0.133221`~`0.209738`까지 줄었지만 cooldown density(쿨다운 뒤 밀도)는 최고 validation/OOS(검증/표본외) `3.655738` / `2.635897`에 그쳐 5/day(일 5회)를 통과하지 못했다.
- best_overall(전체 최선): `nf200c12_h4_s240l150_a`는 validation/OOS(검증/표본외) trades/day(일 거래 수) `4.295082` / `3.041026`, PF(수익 팩터) `1.29` / `1.01`, net(순손익) `435.08` / `7.66`이다.
- failure_axis(실패 축): validation/OOS density(검증/표본외 밀도), OOS PF(표본외 수익 팩터), OOS cost-stressed expectancy(표본외 비용 압박 기대값), cooldown survival(쿨다운 생존).
- attribution(기여도): `nf200c12_h4_s240l150_a` OOS(표본외)는 early/vol_high(초반/고변동)이 강하지만 late/vol_low(후반/저변동)가 약하다. `et40c12_h4_s220l140_b`는 OOS early/downtrend/adx_gt25(초반/하락 추세/ADX 25 초과)가 강하지만 validation mid/range/adx_20_25(검증 중간/횡보/ADX 20-25)가 손상됐다.
- decision(결정): current source/lifecycle path(현재 원천/생명주기 경로)는 reference_only/failure_memory(참조 전용/실패 기억)로 낮추고, 다음은 `run50AW_independent_event_source_route_branch`에서 독립 event source(이벤트 원천)를 라우팅 원천으로 연다.

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
| et40c12_h4_s220l140_a | extratrees_leaf40_actual_cooldown12_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AV/et40c12_h4_s220l140_a/mt5/reports/Project_Obsidian_Prime_v2_run50AV_et40c12_h4_s220l140_a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AV/et40c12_h4_s220l140_a/mt5/reports/Project_Obsidian_Prime_v2_run50AV_et40c12_h4_s220l140_a_logreg_deep_v1_routed_oos.htm | 3.464481 | 2.600000 | 0.93 | 1.37 | -113.5 | 353.84 | validation_density; oos_density; validation_net_positive; validation_pf |
| et40c12_h4_s200l120_a | extratrees_leaf40_actual_cooldown12_aggressive_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AV/et40c12_h4_s200l120_a/mt5/reports/Project_Obsidian_Prime_v2_run50AV_et40c12_h4_s200l120_a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AV/et40c12_h4_s200l120_a/mt5/reports/Project_Obsidian_Prime_v2_run50AV_et40c12_h4_s200l120_a_logreg_deep_v1_routed_oos.htm | 3.464481 | 2.600000 | 0.93 | 1.37 | -113.5 | 353.84 | validation_density; oos_density; validation_net_positive; validation_pf |
| et30c12_h4_s220l140_a | extratrees_leaf30_actual_cooldown12_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AV/et30c12_h4_s220l140_a/mt5/reports/Project_Obsidian_Prime_v2_run50AV_et30c12_h4_s220l140_a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AV/et30c12_h4_s220l140_a/mt5/reports/Project_Obsidian_Prime_v2_run50AV_et30c12_h4_s220l140_a_logreg_deep_v1_routed_oos.htm | 3.655738 | 2.553846 | 0.88 | 1.28 | -179.23 | 274.45 | validation_density; oos_density; validation_net_positive; validation_pf |
| et20c12_h4_s240l150_a | extratrees_leaf20_actual_cooldown12_quality_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AV/et20c12_h4_s240l150_a/mt5/reports/Project_Obsidian_Prime_v2_run50AV_et20c12_h4_s240l150_a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AV/et20c12_h4_s240l150_a/mt5/reports/Project_Obsidian_Prime_v2_run50AV_et20c12_h4_s240l150_a_logreg_deep_v1_routed_oos.htm | 3.590164 | 2.738462 | 0.95 | 0.99 | -82.27 | -14.4 | validation_density; oos_density; validation_net_positive; oos_net_positive |
| nf200c12_h4_s240l150_a | logreg_nonflat200_actual_cooldown12_control_aonly | false | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AV/nf200c12_h4_s240l150_a/mt5/reports/Project_Obsidian_Prime_v2_run50AV_nf200c12_h4_s240l150_a_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AV/nf200c12_h4_s240l150_a/mt5/reports/Project_Obsidian_Prime_v2_run50AV_nf200c12_h4_s240l150_a_logreg_deep_v1_routed_oos.htm | 4.295082 | 3.041026 | 1.29 | 1.01 | 435.08 | 7.66 | validation_density; oos_density; oos_pf; cost_stressed_expectancy |
| et40c12_h4_s220l140_b | extratrees_leaf40_actual_cooldown12_tier_b_comparison | true | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AV/et40c12_h4_s220l140_b/mt5/reports/Project_Obsidian_Prime_v2_run50AV_et40c12_h4_s220l140_b_logreg_deep_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AV/et40c12_h4_s220l140_b/mt5/reports/Project_Obsidian_Prime_v2_run50AV_et40c12_h4_s220l140_b_logreg_deep_v1_routed_oos.htm | 3.480874 | 2.671795 | 0.99 | 1.18 | -9.26 | 184.8 | validation_density; oos_density; validation_net_positive; validation_pf |

## Tier Views(티어 보기)

| variant(변형) | Tier A val/OOS(Tier A 검증/표본외) | Tier B fallback-only val/OOS(Tier B 대체 전용 검증/표본외) | A+B actual routed val/OOS(A+B 실제 라우팅 검증/표본외) | Tier B contribution(Tier B 기여) |
|---|---|---|---|---|
| et40c12_h4_s220l140_a | net -113.5/353.84, PF 0.93/1.37 | net -7.61/4.92, PF 0.13/1.44 | net -113.5/353.84, PF 0.93/1.37 | fallback bars None/None |
| et40c12_h4_s200l120_a | net -113.5/353.84, PF 0.93/1.37 | net -7.61/4.92, PF 0.13/1.44 | net -113.5/353.84, PF 0.93/1.37 | fallback bars None/None |
| et30c12_h4_s220l140_a | net -179.23/274.45, PF 0.88/1.28 | net -7.61/4.92, PF 0.13/1.44 | net -179.23/274.45, PF 0.88/1.28 | fallback bars None/None |
| et20c12_h4_s240l150_a | net -82.27/-14.4, PF 0.95/0.99 | net -7.61/4.92, PF 0.13/1.44 | net -82.27/-14.4, PF 0.95/0.99 | fallback bars None/None |
| nf200c12_h4_s240l150_a | net 435.08/7.66, PF 1.29/1.01 | net -7.61/4.92, PF 0.13/1.44 | net 435.08/7.66, PF 1.29/1.01 | fallback bars None/None |
| et40c12_h4_s220l140_b | net -113.5/353.84, PF 0.93/1.37 | net -7.61/4.92, PF 0.13/1.44 | net -9.26/184.8, PF 0.99/1.18 | fallback bars None/None |

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture ratio(MFE 포착 비율) | winner truncation(승자 절단) | loser escape(패자 탈출) | re-entry 3/6/12(재진입 3/6/12봉) | same-move ratio(동일 이동 비율) | cost-stressed exp(비용 압박 기대값) | cooldown survives(쿨다운 생존) |
|---|---|---:|---:|---:|---|---:|---:|---:|
| et40c12_h4_s220l140_a | validation_is | 0.610498 | 0.338346 | 0.296196 | 93/94/94 | 0.148265 | -0.679022 | False |
| et40c12_h4_s220l140_a | oos | 0.608833 | 0.350746 | 0.317992 | 93/95/95 | 0.187377 | 0.197909 | False |
| et40c12_h4_s200l120_a | validation_is | 0.610498 | 0.338346 | 0.296196 | 93/94/94 | 0.148265 | -0.679022 | False |
| et40c12_h4_s200l120_a | oos | 0.608833 | 0.350746 | 0.317992 | 93/95/95 | 0.187377 | 0.197909 | False |
| et30c12_h4_s220l140_a | validation_is | 0.579434 | 0.389439 | 0.297814 | 121/124/124 | 0.185351 | -0.767907 | False |
| et30c12_h4_s220l140_a | oos | 0.596177 | 0.382979 | 0.324074 | 91/92/92 | 0.184739 | 0.051104 | False |
| et20c12_h4_s240l150_a | validation_is | 0.618508 | 0.305195 | 0.257880 | 100/101/101 | 0.153729 | -0.625221 | False |
| et20c12_h4_s240l150_a | oos | 0.597969 | 0.349315 | 0.268595 | 110/112/112 | 0.209738 | -0.526966 | False |
| nf200c12_h4_s240l150_a | validation_is | 0.613343 | 0.329975 | 0.331620 | 112/116/117 | 0.148855 | 0.053537 | False |
| nf200c12_h4_s240l150_a | oos | 0.615093 | 0.324042 | 0.320261 | 78/79/79 | 0.133221 | -0.487083 | False |
| et40c12_h4_s220l140_b | validation_is | 0.626123 | 0.308550 | 0.304348 | 90/91/91 | 0.142857 | -0.514537 | False |
| et40c12_h4_s220l140_b | oos | 0.596430 | 0.360595 | 0.309524 | 91/93/93 | 0.178503 | -0.145298 | False |

## Current Read(현재 판독)

- best_variant(최선 변형): `nf200c12_h4_s240l150_a`
- selected_research_baseline(선택 연구 기준선): `none`
- stage56_remains_open(56단계 열림 유지): `True`
- next_hypothesis_branch(다음 가설 가지): `continue_density_repair_without_same_move_splitting_and_tier_b_damage_control`

## 2026-05-14T01:48:19Z run50AW Independent Event Source Route(독립 이벤트 원천 라우트)

- action(행동): Stage43/45/47 independent event source(독립 이벤트 원천)를 Stage56(56단계) actual MT5 validation/OOS(실제 MT5 검증/표본외)로 다시 실행했다.
- effect(효과): run50AV(실행50AV)에서 드러난 independent opportunity density(독립 기회 밀도) 병목을 새 source branch(원천 분기)로 압박했다.
- correction(정정): validation day denominator(검증 일수 분모)를 Stage56 audit(감사) 기준과 같은 183일로 맞췄다. Effect(효과): summary(요약)와 audit(감사)의 trades/day(일 거래 수)가 같은 기준으로 읽힌다.
- best_variant(현재 최선 변형): `s45c04_h4c6`
- validation/OOS trades/day(검증/표본외 일 거래): `5.535519` / `3.553846`
- validation/OOS PF(검증/표본외 수익 팩터): `0.980000` / `1.180000`
- validation/OOS net(검증/표본외 순손익): `-32.280000` / `246.33`
- decision(결정): selected_research_baseline(선택 연구 기준선)=`none`; failure_reasons(실패 사유)=`oos_density;validation_net_positive;validation_pf;cost_stressed_expectancy;same_move_density`.

## 2026-05-14T02:53:05Z run50AX Source Composite Density Quality(원천 합성 밀도 품질)

- action(행동): run50AW(실행50AW)의 Stage47/Stage45 source(원천)를 composite signal(합성 신호)로 묶어 actual MT5 validation/OOS(실제 MT5 검증/표본외)를 실행했다.
- effect(효과): OOS density(표본외 밀도), PF(수익 팩터), same-move density(동일 이동 밀도)가 source union/filter(원천 합산/필터)에서 살아나는지 기록했다.
- correction(정정): MT5 report name(보고서 이름)을 short token(짧은 토큰)으로 줄이고 artifact hash(산출물 해시)를 실제 파일 기준으로 다시 기록했다. Effect(효과): tester report(테스터 보고서) 수집과 hash check(해시 검사)가 같은 경로를 가리킨다.
- best_variant(현재 최선 변형): `v02_s45_primary_s47_flatfill_h4c6`
- validation/OOS trades/day(검증/표본외 일 거래): `7.770492` / `5.046154`
- validation/OOS PF(검증/표본외 수익 팩터): `1.010000` / `1.020000`
- validation/OOS net(검증/표본외 순손익): `34.380000` / `34.010000`
- decision(결정): selected_research_baseline(선택 연구 기준선)=`none`; failure_reasons(실패 사유)=`validation_pf;oos_pf;cost_stressed_expectancy;same_move_density`.
