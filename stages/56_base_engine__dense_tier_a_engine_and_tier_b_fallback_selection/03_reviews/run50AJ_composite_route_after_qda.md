# run50AJ_stage56_composite_route_after_qda_v1(Stage56 56단계 composite route 합성 라우트)

- packet_id(묶음 ID): `stage56_run50AJ_composite_route_after_qda_v1`
- stage_status(단계 상태): `active_in_progress(활성 진행 중)`
- selected_research_baseline(선택 연구 기준선): `none`
- valid_new_actual_mt5_routed_variants(유효 신규 실제 MT5 라우팅 변형): `3` / bound(상한) `6`
- boundary(주장 경계): `research_baseline_selection_only_no_closeout_no_operating_claim`

## Design(설계)

Action(행동): QDA standalone(QDA 단독)을 반복하지 않고 nf200s25b(강한 품질 가지)를 primary(주 라우트)로 유지했다.
Effect(효과): primary(주 라우트)가 flat(관망)이거나, repair variant(수정 변형)에서는 low-confidence(저신뢰)일 때만 QDA secondary coverage(보조 커버리지)를 평가한다.

No simultaneous double-position(동시 이중 포지션 없음): secondary(보조)는 position_before(진입 전 포지션)가 none(없음)일 때만 실행된다. Effect(효과): 같은 포지션 위에 두 번째 엔진을 겹치지 않는다.

Partial-context Tier B(부분 문맥 Tier B)는 disabled(비활성화)했다. Effect(효과): run50AH(실행50AH)의 damaging fallback-only OOS(손상 대체 전용 표본외)를 composite read(합성 판독)에 섞지 않는다.

## Variant Results(변형 결과)

| variant(변형) | mode(방식) | val/day(검증 일 거래) | OOS/day(표본외 일 거래) | val PF(검증 수익 팩터) | OOS PF(표본외 수익 팩터) | val net(검증 순손익) | OOS net(표본외 순손익) | secondary bars val/OOS(보조 봉 검증/표본외) | judgment(판정) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| nf200s25b_qda85_flatfill | primary_flat_no_position_secondary_coverage | 5.475410 | 3.723077 | 1.16 | 1.2 | 424.33 | 362.7 | 192/188 | `weak_dense_engine_candidate_actual_routed_mt5` |
| nf200s25b_qda93_flatfill | primary_flat_no_position_secondary_quality_coverage | 5.469945 | 3.723077 | 1.18 | 1.2 | 467.14 | 362.92 | 192/191 | `weak_dense_engine_candidate_actual_routed_mt5` |
| nf200s25b_qda85_lowconf050 | primary_flat_or_low_confidence_no_position_secondary_coverage | 4.284153 | 2.830769 | 0.98 | 1.05 | -33.64 | 75.75 | 3990/3035 | `quality_failed_actual_routed_mt5` |

## Tier And Secondary Views(티어와 보조 보기)

| variant(변형) | Tier A only(Tier A 단독) | secondary-only(보조 단독) | actual routed(실제 라우팅) |
|---|---|---|---|
| nf200s25b_qda85_flatfill | val/OOS net 550.2/310.59, PF 1.23/1.17 | val/OOS net 100.75/198.98, PF 1.05/1.2 | val/OOS net 424.33/362.7, PF 1.16/1.2 |
| nf200s25b_qda93_flatfill | val/OOS net 550.2/310.59, PF 1.23/1.17 | val/OOS net -137.8/4.53, PF 0.89/1.01 | val/OOS net 467.14/362.92, PF 1.18/1.2 |
| nf200s25b_qda85_lowconf050 | val/OOS net 550.2/310.59, PF 1.23/1.17 | val/OOS net 100.75/198.98, PF 1.05/1.2 | val/OOS net -33.64/75.75, PF 0.98/1.05 |

## Same-Move Audit(동일 이동 감사)

| variant(변형) | split(분할) | MFE capture(MFE 포착) | re-entry 3/6/12(재진입 3/6/12봉) | same-move ratio(동일 이동 비율) | cooldown day(쿨다운 뒤 일 거래) | cost-stressed exp(비용 압박 기대값) | survives(생존) |
|---|---|---:|---|---:|---:|---:|---:|
| nf200s25b_qda85_flatfill | validation_is | 0.606343 | 244/294/601 | 0.599800 | 2.191257 | -0.076517 | False |
| nf200s25b_qda85_flatfill | oos | 0.589839 | 147/180/443 | 0.610193 | 1.451282 | -0.000413 | False |
| nf200s25b_qda93_flatfill | validation_is | 0.606343 | 243/293/599 | 0.598402 | 2.196721 | -0.033327 | False |
| nf200s25b_qda93_flatfill | oos | 0.589522 | 147/181/443 | 0.610193 | 1.451282 | -0.000110 | False |
| nf200s25b_qda85_lowconf050 | validation_is | 0.607487 | 186/226/388 | 0.494898 | 2.163934 | -0.542908 | False |
| nf200s25b_qda85_lowconf050 | oos | 0.606868 | 108/128/261 | 0.472826 | 1.492308 | -0.362772 | False |

## Read(판독)

- best_variant(최선 변형): `nf200s25b_qda93_flatfill`
- selected_research_baseline(선택 연구 기준선): `none`
- stage56_remains_open(56단계 열림 유지): `True`
- reason(이유): no composite route variant passed every selected_research_baseline gate
- next_hypothesis_branch(다음 가설 가지): `coverage_must_come_from_new_true_trade_opportunity_not_primary_flat_or_low_confidence_qda_handoff`

## Best Failed Checks(최선 변형 실패 조건)

- `oos_density`: OOS trades/day >= 5.0
- `cost_stressed_expectancy`: cost-stressed expectancy positive
- `same_move_density`: density survives cooldown and is not mainly same-move re-entry
