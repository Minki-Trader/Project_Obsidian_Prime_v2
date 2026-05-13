# Stage56 Reopen Goal Progress Log(56단계 재개 목표 진행 기록)

- packet_id(묶음 ID): `stage56_reopen_goal_v1`
- stage_status(단계 상태): `active_in_progress(활성 진행 중)`
- latest_batch(최신 묶음): `run50AJ_stage56_composite_route_after_qda_v1`
- selected_research_baseline(선택 연구 기준선): `none`
- terminal_condition(종료 조건): selected_research_baseline(선택 연구 기준선) found(발견)

Stage56(56단계)는 active_in_progress(활성 진행 중)이다. Effect(효과): run50B through run50AJ(실행50B부터 실행50AJ까지)는 intermediate evidence(중간 근거)이며 closeout(종료) 근거가 아니다.

## Current Bottleneck(현재 병목)

- density(밀도): nf200s25b(최신 중간 기준)는 validation(검증) 5+ trades/day(일 거래 수)를 넘겼지만 OOS(표본외)는 5에 못 미쳤다.
- route coverage(라우트 커버리지): QDA standalone(QDA 단독)이 아니라 primary-quality branch(품질 주 가지)를 유지한 composite route(합성 라우트)를 시험했다.
- same-move split(동일 이동 분할): density gain(밀도 증가)이 12-bar cooldown(12봉 쿨다운) 뒤에도 살아야 한다.

## Attempted Variants(시도 변형)

| variant(변형) | hypothesis family(가설군) | actual MT5 report paths(실제 MT5 보고서 경로) | val/day(검증 일 거래) | OOS/day(표본외 일 거래) | val PF(검증 수익 팩터) | OOS PF(표본외 수익 팩터) | val net(검증 순손익) | OOS net(표본외 순손익) | reason(이유) |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| nf200s25b_qda85_flatfill | nf200s25b_primary_qda85_secondary_flatfill | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AJ/nf200s25b_qda85_flatfill/mt5/reports/Project_Obsidian_Prime_v2_run50AJ_nf200s25b_qda85_flatfill_composite_route_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AJ/nf200s25b_qda85_flatfill/mt5/reports/Project_Obsidian_Prime_v2_run50AJ_nf200s25b_qda85_flatfill_composite_route_v1_routed_oos.htm | 5.475410 | 3.723077 | 1.16 | 1.2 | 424.33 | 362.7 | oos_density; cost_stressed_expectancy; same_move_density |
| nf200s25b_qda93_flatfill | nf200s25b_primary_qda93_secondary_flatfill | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AJ/nf200s25b_qda93_flatfill/mt5/reports/Project_Obsidian_Prime_v2_run50AJ_nf200s25b_qda93_flatfill_composite_route_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AJ/nf200s25b_qda93_flatfill/mt5/reports/Project_Obsidian_Prime_v2_run50AJ_nf200s25b_qda93_flatfill_composite_route_v1_routed_oos.htm | 5.469945 | 3.723077 | 1.18 | 1.2 | 467.14 | 362.92 | oos_density; cost_stressed_expectancy; same_move_density |
| nf200s25b_qda85_lowconf050 | nf200s25b_primary_qda85_low_confidence_handoff | stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AJ/nf200s25b_qda85_lowconf050/mt5/reports/Project_Obsidian_Prime_v2_run50AJ_nf200s25b_qda85_lowconf050_composite_route_v1_routed_validation_is.htm ; stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/02_runs/run50AJ/nf200s25b_qda85_lowconf050/mt5/reports/Project_Obsidian_Prime_v2_run50AJ_nf200s25b_qda85_lowconf050_composite_route_v1_routed_oos.htm | 4.284153 | 2.830769 | 0.98 | 1.05 | -33.64 | 75.75 | validation_density; oos_density; validation_net_positive; validation_pf; oos_pf |

## Tier B And Secondary Rule(Tier B와 보조 규칙)

- partial_context_tier_b_status(부분 문맥 Tier B 상태): `disabled(비활성화)`
- disablement_reason(비활성화 이유): Original partial-context Tier B(부분 문맥 Tier B)는 run50AH(실행50AH) fallback-only OOS(대체 전용 표본외) net(순손익)이 음수였기 때문에 disabled(비활성화)했다. Secondary coverage(보조 커버리지)는 QDA(이차 판별 분석) independent source(독립 원천)이며 simultaneous double-position(동시 이중 포지션)을 열지 않는다.
- secondary_lane(보조 레인): QDA(이차 판별 분석) source(원천)를 no-position(무포지션) 조건에서만 사용했다.

## Hold/Re-entry Audit(보유/재진입 감사)

| variant(변형) | split(분할) | MFE capture ratio(MFE 포착 비율) | winner truncation(승자 절단) | loser escape(패자 탈출) | re-entry 3/6/12(재진입 3/6/12봉) | same-move ratio(동일 이동 비율) | cost-stressed exp(비용 압박 기대값) | cooldown survives(쿨다운 생존) |
|---|---|---:|---:|---:|---|---:|---:|---:|
| nf200s25b_qda85_flatfill | validation_is | 0.606343 | 0.341053 | 0.296015 | 244/294/601 | 0.599800 | -0.076517 | False |
| nf200s25b_qda85_flatfill | oos | 0.589839 | 0.385027 | 0.377841 | 147/180/443 | 0.610193 | -0.000413 | False |
| nf200s25b_qda93_flatfill | validation_is | 0.606343 | 0.341053 | 0.294677 | 243/293/599 | 0.598402 | -0.033327 | False |
| nf200s25b_qda93_flatfill | oos | 0.589522 | 0.385027 | 0.377841 | 147/181/443 | 0.610193 | -0.000110 | False |
| nf200s25b_qda85_lowconf050 | validation_is | 0.607487 | 0.339779 | 0.296209 | 186/226/388 | 0.494898 | -0.542908 | False |
| nf200s25b_qda85_lowconf050 | oos | 0.606868 | 0.356618 | 0.339286 | 108/128/261 | 0.472826 | -0.362772 | False |

## Current Read(현재 판독)

- best_variant(최선 변형): `nf200s25b_qda93_flatfill`
- selected_research_baseline(선택 연구 기준선): `none`
- next_hypothesis_branch(다음 가설 가지): `coverage_must_come_from_new_true_trade_opportunity_not_primary_flat_or_low_confidence_qda_handoff`
