# Stage267 Run267C P1 Axis Selection(267단계 267C 실행 1차 축 선택)

- action(행동): P1 soft-axis(1차 부드러운 축) 결과를 Adapter prototype(어댑터 원형), P2 replacement(2차 대체), watch(관찰), failure memory(실패 기억)로 분리했다.
- effect(효과): 가장 좋아 보이는 숫자만 고르지 않고, P0 repair retention(0차 수리 유지), trade cost(거래 비용), DD(drawdown, 손실폭), signal retention(신호 유지율)을 같이 본다.
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`

## Experiment Design Receipt(실험 설계 기록)

- hypothesis(가설): P1 soft-axis(1차 부드러운 축) 중 일부는 P0 hard block(0차 강제 차단)의 수리 단서를 더 낮은 과차단으로 유지할 수 있다.
- decision_use(결정 사용처): 다음 Adapter prototype(어댑터 원형) 또는 P2 replacement(2차 대체) 물질화 축을 고른다.
- comparison_baseline(비교 기준): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267B/historical_2024/mt5_kpi_summary.csv`와 `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267C/p0_mt5_variants/p0_mt5_full_batch_candidate_variant_summary.csv`.
- control_variables(고정 변수): Stage267(267단계) 5개 후보군, 2024 historical stress(2024 과거 압박) 기간, MT5 EA(메타트레이더5 전문가 자문), threshold(임계값), trade management(거래 관리)를 유지한다.
- changed_variables(변경 변수): 다음 작업에서 이월할 axis family(축 계열)와 adapter/replacement(어댑터/대체) 역할만 바꾼다.
- sample_scope(표본 범위): Tier A(티어 A)와 Tier A+B(티어 A+B) routed historical 2024(라우팅 과거 2024) MT5 Strategy Tester(전략 테스터) 결과.
- success_criteria(성공 기준): 수익/PF(수익 팩터)가 기준보다 좋아지고, DD(손실폭)가 줄며, 거래 수와 신호 유지율이 과도하게 무너지지 않는 축을 다음 구조 검증으로 넘긴다.
- failure_criteria(실패 기준): 기준 대비 효과가 작거나 P0 repair(0차 수리)를 거의 잃거나, 같은 cutoff(절단값) 반복만 남는 축은 실패 기억으로 닫는다.
- invalid_conditions(무효 조건): MT5 report(보고서), KPI(KPI, 핵심 성과 지표), feature manifest(피처 목록), P0/base comparison(0차/기준 비교)이 누락되면 이 선택은 무효다.
- stop_conditions(중단 조건): next run(다음 실행)이 다시 한 축 미세조정만 반복하면 P2(2차)로 넘기지 않고 실패 기억으로 닫는다.
- evidence_plan(근거 계획): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267C/p1_soft_axis_followup/p1_axis_selection_matrix.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267C/p1_soft_axis_followup/p1_adapter_p2_candidate_shortlist.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267C/p1_soft_axis_followup/p1_axis_failure_memory.csv`를 장부에 연결한다.

## Axis Decision(축 결정)

| axis(축) | decision(결정) | avg net delta(평균 순수익 차이) | avg PF delta(평균 수익 팩터 차이) | avg trade delta(평균 거래 수 차이) | avg DD% delta(평균 손실폭% 차이) | P1 vs P0 net(1차 대 0차 순수익) | signal retention(신호 유지율) | reason(이유) |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `late21` | `carry_forward_adapter_prototype_axis` | 98.6 | 0.068 | -42 | -14.15 | -34.022 | 0.898148148148 | retains_p0_repair_with_usable_trade_cost(P0 수리 효과를 유지하면서 거래 비용이 감당 가능) |
| `atrcomp` | `carry_forward_p2_replacement_axis` | 166.376 | 0.104 | -40 | -8.958 | -186.302 | 0.825925925926 | strongest_net_replacement_but_signal_retention_cost_is_high(가장 강한 순수익 대체 축이지만 신호 유지 비용이 큼) |
| `vlowadx` | `carry_forward_p2_replacement_axis` | 102.6 | 0.058 | -19.6 | -2.616 | -250.078 | 0.942592592593 | good_trade_retention_replacement_but_dd_repair_is_shallow(거래 유지가 좋은 대체 축이지만 손실폭 수리는 얕음) |
| `latevlow` | `defer_composition_watch` | 67.334 | 0.03 | -5.2 | -5.416 | -285.344 | 0.97037037037 | low_trade_cost_but_p0_repair_loss_too_large(거래 비용은 낮지만 P0 수리 효과 손실이 큼) |
| `lateadx` | `close_as_low_impact_failure_memory` | 28.794 | 0.014 | -5.2 | -1.188 | -103.828 | 0.97037037037 | low_impact_vs_base_and_p0_repair_not_retained(기준 대비 효과가 작고 P0 수리 효과도 유지하지 못함) |

## Carry Forward(다음 이월)

- Adapter prototype(어댑터 원형): `late21`.
- P2 replacement(2차 대체): `atrcomp;vlowadx`.
- watch(관찰): `latevlow`.
- failure/watch memory(실패/관찰 기억): `latevlow;lateadx`.

## Shortlist Pair Read(후보-축 짝 판독)

| candidate(후보) | axis(축) | role(역할) | pair_role(짝 역할) | net(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭%) |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: |
| `s264_aih` | `late21` | `challenger_core` | `primary_adapter_probe_pair(주 어댑터 탐침 쌍)` | 198.2 | 1.12 | 312 | 22.86 |
| `s258_stc` | `late21` | `stress_challenger` | `adapter_stress_or_anchor_pair(어댑터 압박/앵커 쌍)` | 190.46 | 1.11 | 332 | 26.42 |
| `s264_aia` | `late21` | `oos_anchor` | `adapter_stress_or_anchor_pair(어댑터 압박/앵커 쌍)` | 189.67 | 1.12 | 313 | 22.88 |
| `s264_lc` | `late21` | `defensive_control` | `adapter_control_pair(어댑터 대조 쌍)` | 173.26 | 1.11 | 309 | 22.86 |
| `s262_lih` | `late21` | `validation_heavy` | `adapter_control_pair(어댑터 대조 쌍)` | 142.76 | 1.09 | 311 | 25.89 |
| `s264_aih` | `atrcomp` | `challenger_core` | `p2_replacement_pair(2차 대체 쌍)` | 269.2 | 1.16 | 314 | 28.73 |
| `s264_aia` | `atrcomp` | `oos_anchor` | `p2_replacement_pair(2차 대체 쌍)` | 261.08 | 1.16 | 315 | 28.89 |
| `s258_stc` | `atrcomp` | `stress_challenger` | `p2_replacement_pair(2차 대체 쌍)` | 260.91 | 1.14 | 334 | 29.99 |
| `s264_lc` | `atrcomp` | `defensive_control` | `p2_replacement_pair(2차 대체 쌍)` | 240.12 | 1.15 | 311 | 28.78 |
| `s258_stc` | `vlowadx` | `stress_challenger` | `p2_replacement_pair(2차 대체 쌍)` | 203.28 | 1.1 | 357 | 39.62 |
| `s262_lih` | `atrcomp` | `validation_heavy` | `p2_replacement_pair(2차 대체 쌍)` | 201.92 | 1.12 | 313 | 30.48 |
| `s264_aih` | `vlowadx` | `challenger_core` | `p2_replacement_pair(2차 대체 쌍)` | 196.82 | 1.11 | 334 | 34.07 |
| `s264_aia` | `vlowadx` | `oos_anchor` | `p2_replacement_pair(2차 대체 쌍)` | 196.82 | 1.11 | 334 | 34.07 |
| `s264_lc` | `vlowadx` | `defensive_control` | `p2_replacement_pair(2차 대체 쌍)` | 175.16 | 1.1 | 331 | 34.39 |
| `s262_lih` | `vlowadx` | `validation_heavy` | `p2_replacement_pair(2차 대체 쌍)` | 142.27 | 1.08 | 333 | 36.43 |

## Judgment Boundary(판정 경계)

- selected_candidate(선택 후보): `none`.
- selected_research_baseline(선택 연구 기준선): `none`.
- ONNX readiness(ONNX 준비): `not_claimed`.
- result_subject(결과 대상): `run267C_p1_axis_selection`.
- evidence_available(사용 가능 근거): P1 KPI(KPI, 핵심 성과 지표), P0 comparison(0차 비교), run267B base(267B 기준값), feature manifest(피처 목록), MT5 backtest forensics(백테스트 포렌식).
- evidence_missing(빠진 근거): Adapter prototype MT5 run(어댑터 원형 MT5 실행), P2 replacement MT5 run(2차 대체 MT5 실행), zoomed equity curve(확대 평가금 곡선), full time-slice breakdown(전체 시간 구간 분해), ONNX parity(ONNX 동등성).
- judgment_label(판정 라벨): `exploratory_axis_selection(탐색 축 선택)`.
- failure_memory_rows(실패 기억 행): `2`.
- next_condition(다음 조건): `run267D_materialize_late21_adapter_prototype_and_p2_replacement_design`. Effect(효과): late21(후반 21시)은 Adapter prototype(어댑터 원형)으로, atrcomp/vlowadx(ATR 압축/낮은 변동성+ADX)는 P2 replacement(2차 대체)로 물질화해 다시 MT5(메타트레이더5) 검증한다.
