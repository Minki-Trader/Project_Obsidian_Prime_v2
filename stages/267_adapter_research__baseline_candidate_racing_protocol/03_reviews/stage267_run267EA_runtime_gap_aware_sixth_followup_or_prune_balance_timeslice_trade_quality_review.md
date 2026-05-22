# Stage267 Run267EA Balance/Time-Slice/Trade-Quality Review(267단계 267EA 잔액/시간구간/거래품질 검토)

- status(상태): `run267EA_runtime_gap_aware_sixth_followup_or_prune_balance_timeslice_trade_quality_review_completed`
- source_run(원천 실행): `run267DZ_stage267_runtime_gap_aware_sixth_followup_or_prune_mt5_execution_v1`
- candidate_profile_rows(후보-프로필 행): `9`
- trade_records(거래 기록): `2258`
- negative_slices(음수 구간): `71`
- parser_errors(파서 오류): `0`
- next_action(다음 행동): `run267EB_design_runtime_gap_aware_seventh_followup_or_prune_from_run267EA_review`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

run267DZ(267DZ 실행)는 9개 모두 KPI(핵심 성과 지표)까지 나왔지만, 검토 결과는 아직 후보 선택이 아니다.
s258_stc는 2023H2에서 강하지만 2025H1/H2로 갈수록 PF(수익 팩터)와 DD(손실폭)가 약해진다. s264_aih는 validation anchor(검증 앵커)는 살아났지만 2026.04 final-month probe(마지막 달 탐침)가 음수다. s264_lc control(대조)도 같은 달 음수라 그 달 자체가 불리한 시장 구간일 수 있다.

## Candidate Profile(후보 프로필)

| candidate(후보) | profile(프로필) | net(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭 %) | weakest(최약점) | read(판독) |
|---|---|---:|---:|---:|---:|---|---|
| `s258_stc` | `s258_stc_structural_dd_shape_2023h2` | 975.93 | 1.6821393872886508 | 265 | 11.52 | `2023-07=38.16` | `constructive_watch_but_not_baseline_selection(건설적 관찰이나 기준 후보 선택 아님)` |
| `s258_stc` | `s258_stc_structural_dd_shape_2025h1` | 298.75 | 1.1694573959999546 | 357 | 15.78 | `2025-05=-5.460000000000009` | `positive_but_not_strong_enough_no_selection(양수지만 충분히 강하지 않음, 선택 아님)` |
| `s258_stc` | `s258_stc_structural_dd_shape_2025h2` | 131.32 | 1.1016644731748857 | 259 | 21.81 | `2025-12=-98.4` | `positive_but_not_strong_enough_no_selection(양수지만 충분히 강하지 않음, 선택 아님)` |
| `s258_stc` | `s258_stc_adverse_slice_state_2023h2` | 1182.0 | 1.7422478429599488 | 265 | 13.45 | `2023-07=-25.78` | `constructive_watch_but_not_baseline_selection(건설적 관찰이나 기준 후보 선택 아님)` |
| `s258_stc` | `s258_stc_adverse_slice_state_2025h1` | 283.01 | 1.1494884295818169 | 355 | 23.71 | `2025-05=-90.91` | `profitable_but_curve_risk_no_selection(수익은 있으나 곡선 위험, 선택 아님)` |
| `s258_stc` | `s258_stc_adverse_slice_state_2025h2` | 234.98 | 1.1470545900582636 | 256 | 22.57 | `2025-12=-117.03999999999999` | `profitable_but_curve_risk_no_selection(수익은 있으나 곡선 위험, 선택 아님)` |
| `s264_aih` | `s264_aih_validation_anchor_repair` | 574.25 | 1.2299354539047984 | 467 | 12.01 | `2025-09=-30.25` | `positive_but_not_strong_enough_no_selection(양수지만 충분히 강하지 않음, 선택 아님)` |
| `s264_aih` | `s264_aih_202604_counter_shock_probe` | -33.79 | 0.41650837506475563 | 17 | 9.12 | `2026-04=-33.79` | `final_month_break_no_selection(마지막 달 붕괴, 선택 아님)` |
| `s264_lc` | `s264_lc_202604_same_month_control` | -39.29 | 0.4039745145631068 | 17 | 10.36 | `2026-04=-39.29` | `final_month_break_no_selection(마지막 달 붕괴, 선택 아님)` |

## Attribution(성과 귀속)

- `s258_stc`: s258_stc는 2023H2는 강하지만 2025H1/H2에서 PF(수익 팩터)와 DD(손실폭)가 불편해 stress challenger(압박 도전자) 위험이 계속 남는다. Next(다음): seventh follow-up(7차 후속)에서는 DD shape(손실폭 형태)와 adverse state(불리 상태)를 합치기보다 약한 기간별 생존 조건을 먼저 판정한다.
- `s264_aih`: s264_aih는 validation anchor(검증 앵커)는 회복됐지만 2026.04 counter shock(역충격)에서 음수라 final-month hole(마지막 달 구멍)이 남는다. Next(다음): validation repair(검증 수리)와 final-month shock(마지막 달 충격)을 분리해 repair cap(수리 제한) 안에서 살릴지 버릴지 결정한다.
- `s264_lc`: s264_lc control(대조)은 같은 2026.04에서 음수라 s264_aih 약점이 후보 단독 문제가 아니라 시장 구간 문제일 수 있음을 보여준다. Next(다음): control(대조)은 selection(선택)용이 아니라 해석 기준으로만 유지한다.

## Boundary(경계)

- 이 검토는 exploratory review(탐색 검토)이며 후보 선택, 연구 기준선 선택, ONNX(ONNX 준비), Goal Achieve(목표 달성)를 주장하지 않는다.
- 다음 run267EB(267EB 실행)는 같은 repair(수리)를 오래 끌지 말고 s258_stc DD shape(손실폭 형태), s264_aih final-month hole(마지막 달 구멍), q06 filter-stack prune(필터 누적 가지치기)을 분명히 나눠야 한다.

## Artifacts(산출물)

- trade_records(거래 기록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EA/runtime_gap_aware_sixth_followup_or_prune_balance_timeslice_trade_quality_review/trade_records.csv`
- time_slice_kpi(시간구간 KPI): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EA/runtime_gap_aware_sixth_followup_or_prune_balance_timeslice_trade_quality_review/time_slice_kpi.csv`
- curve_diagnostics(곡선 진단): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EA/runtime_gap_aware_sixth_followup_or_prune_balance_timeslice_trade_quality_review/curve_diagnostics.csv`
- candidate_profile_review(후보 프로필 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EA/runtime_gap_aware_sixth_followup_or_prune_balance_timeslice_trade_quality_review/candidate_profile_review.csv`
- negative_slice_summary(음수 구간 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EA/runtime_gap_aware_sixth_followup_or_prune_balance_timeslice_trade_quality_review/negative_slice_summary.csv`
- result_judgment(결과 판정): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EA/runtime_gap_aware_sixth_followup_or_prune_balance_timeslice_trade_quality_review/result_judgment.csv`
