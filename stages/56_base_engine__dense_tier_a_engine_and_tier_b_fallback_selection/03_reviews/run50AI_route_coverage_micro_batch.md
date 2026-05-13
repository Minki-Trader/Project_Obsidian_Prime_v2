# run50AI_stage56_route_coverage_micro_batch_v1(Stage56 56단계 route coverage 라우팅 커버리지 micro-batch 마이크로 배치)

- packet_id(묶음 ID): `stage56_run50AI_route_coverage_micro_batch_v1`
- stage_status(단계 상태): `active_in_progress(활성 진행 중)`
- selected_research_baseline(선택 연구 기준선): `none`
- valid_new_actual_mt5_routed_variants(유효 신규 실제 MT5 라우팅 변형): `3` / hard limit(상한) `6`
- boundary(주장 경계): `research_baseline_selection_only_no_closeout_no_operating_claim`

## Design(설계)

Action(행동): run50AH(실행50AH)의 nf200s25b(최신 중간 기준)가 OOS density(표본외 밀도)에서 멈춘 뒤, Stage16 QDA(16단계 이차 판별 분석) reviewed runtime probe(검토된 런타임 탐침) 신호를 Stage56(56단계) 실제 MT5(메타트레이더5) 단일 tester path(테스터 경로)로 다시 실행했다.
Effect(효과): threshold relaxation(임계값 완화)이나 hold-only tweak(보유 전용 미세 조정) 반복이 아니라 independent signal source(독립 신호 원천)가 OOS coverage(표본외 커버리지)를 실제로 열 수 있는지 확인한다.

Tier B(티어 B)는 run50AH(실행50AH)에서 fallback-only OOS(대체 전용 표본외)가 net(순손익) 음수였으므로 disabled(비활성화)했다. Effect(효과): fallback damage(대체 손상)를 새 coverage(커버리지) 판독에 섞지 않는다.

## Variant Results(변형 결과)

| variant(변형) | source(원천) | guard(가드) | val/day(검증 일 거래) | OOS/day(표본외 일 거래) | val PF(검증 수익 팩터) | OOS PF(표본외 수익 팩터) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| qda_q85_aonly_bdisabled | run09O_qda_reg015_q85_coverage_followup_v1 | 0 | 3.453552 | 1.830769 | 1.05 | 1.2 | 131.93 | 263.17 | `density_failed_actual_routed_mt5` |
| qda_q93_quality_bdisabled | run09P_qda_reg015_q93_coverage_followup_v1 | 0 | 1.956284 | 0.974359 | 1.14 | 1.07 | 220.32 | 65.09 | `density_failed_actual_routed_mt5` |
| qda_q85_guard12_bdisabled | run09O_qda_reg015_q85_coverage_followup_v1 | 12 | 2.846995 | 1.466667 | 1.13 | 1.16 | 251.77 | 167.69 | `density_failed_actual_routed_mt5` |

## Tier Views(티어 보기)

| variant(변형) | Tier A only(Tier A 단독) | Tier B fallback-only(Tier B 대체 전용) | A+B actual routed(A+B 실제 라우팅) |
|---|---|---|---|
| qda_q85_aonly_bdisabled | val/OOS net 131.93/263.17, PF 1.05/1.2 | disabled(비활성화): Tier B disabled because run50AH nf200s25b fallback-only OOS was negative and prior A-only/A+B reads did not justify carrying damaging fallback risk into this route coverage micro-batch. | val/OOS net 131.93/263.17, PF 1.05/1.2 |
| qda_q93_quality_bdisabled | val/OOS net 220.32/65.09, PF 1.14/1.07 | disabled(비활성화): Tier B disabled because run50AH nf200s25b fallback-only OOS was negative and prior A-only/A+B reads did not justify carrying damaging fallback risk into this route coverage micro-batch. | val/OOS net 220.32/65.09, PF 1.14/1.07 |
| qda_q85_guard12_bdisabled | val/OOS net 251.77/167.69, PF 1.13/1.16 | disabled(비활성화): Tier B disabled because run50AH nf200s25b fallback-only OOS was negative and prior A-only/A+B reads did not justify carrying damaging fallback risk into this route coverage micro-batch. | val/OOS net 251.77/167.69, PF 1.13/1.16 |

## Same-Move Audit(동일 이동 감사)

| variant(변형) | split(분할) | MFE capture(MFE 포착) | winner truncation(승자 절단) | loser escape(패자 탈출) | re-entry 3/6/12(재진입 3/6/12봉) | same-move ratio(동일 이동 비율) | cooldown day(쿨다운 뒤 일 거래) | cost-stressed exp(비용 압박 기대값) | survives(생존) |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|
| qda_q85_aonly_bdisabled | validation_is | 0.570264 | 0.370242 | 0.274052 | 226/290/325 | 0.514241 | 1.677596 | -0.291250 | False |
| qda_q85_aonly_bdisabled | oos | 0.622654 | 0.306358 | 0.304348 | 90/120/137 | 0.383754 | 1.128205 | 0.237171 | False |
| qda_q93_quality_bdisabled | validation_is | 0.541996 | 0.400000 | 0.229508 | 76/105/125 | 0.349162 | 1.273224 | 0.115419 | False |
| qda_q93_quality_bdisabled | oos | 0.629748 | 0.311111 | 0.280000 | 17/25/31 | 0.163158 | 0.815385 | -0.157421 | False |
| qda_q85_guard12_bdisabled | validation_is | 0.570301 | 0.352459 | 0.252708 | 152/188/213 | 0.408829 | 1.683060 | -0.016756 | False |
| qda_q85_guard12_bdisabled | oos | 0.590939 | 0.342657 | 0.314685 | 49/69/75 | 0.262238 | 1.082051 | 0.086329 | False |

## Read(판독)

- best_variant(최선 변형): `qda_q85_guard12_bdisabled`
- selected_research_baseline(선택 연구 기준선): `none`
- stage56_remains_open(56단계 열림 유지): `True`
- reason(이유): no variant passed every selected_research_baseline gate in the bounded run50AI micro-batch
- next_hypothesis_branch(다음 가설 가지): `independent_signal_source_or_route_coverage_axis_needs_stronger_oos_density_source_after_qda_micro_batch`

## Best Failed Checks(최선 변형 실패 조건)

- `validation_density`: validation trades/day >= 5.0
- `oos_density`: OOS trades/day >= 5.0
- `cost_stressed_expectancy`: cost-stressed expectancy positive
- `same_move_density`: density survives cooldown and is not mainly same-move re-entry
