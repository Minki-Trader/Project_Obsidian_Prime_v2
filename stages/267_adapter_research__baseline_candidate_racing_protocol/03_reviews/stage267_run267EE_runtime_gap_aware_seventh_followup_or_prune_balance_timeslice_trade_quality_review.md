# Stage267 Run267EE Balance/Time-Slice/Trade-Quality Review(267단계 267EE 잔액/시간구간/거래품질 검토)

- status(상태): `run267EE_runtime_gap_aware_seventh_followup_or_prune_balance_timeslice_trade_quality_review_completed`
- source_run(원천 실행): `run267ED_stage267_runtime_gap_aware_seventh_followup_or_prune_mt5_execution_v1`
- candidate_profile_rows(후보-프로필 행): `9`
- trade_records(거래 기록): `2065`
- negative_slices(음수 구간): `79`
- parser_errors(파서 오류): `0`
- next_action(다음 행동): `run267EF_design_runtime_gap_aware_eighth_followup_or_prune_from_run267EE_review`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

run267ED(267ED 실행)는 14개 시도 중 9개가 KPI(핵심 성과 지표)까지 나왔고, 검토 결과는 아직 후보 선택이 아니다.
s258_stc는 period survival gate(기간 생존 게이트) 2개는 양수지만 explosive impulse(폭발형 임펄스) 3개가 런타임 출력에서 끊겼다. s264_aih는 validation anchor(검증 앵커)는 살아났지만 2026.04 final-month probe(마지막 달 탐침)가 음수이고, explosive counter impulse(폭발형 역임펄스) 2개도 끊겼다. s264_lc/s262_lih/s264_aia의 2026.04 coverage/control(커버리지/대조)도 음수라 그 달 자체가 불리한 시장 구간일 수 있다.

## Candidate Profile(후보 프로필)

| candidate(후보) | profile(프로필) | net(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭 %) | weakest(최약점) | read(판독) |
|---|---|---:|---:|---:|---:|---|---|
| `s258_stc` | `s258_stc_2025h1_period_survival_gate` | 301.88 | 1.1820188000072356 | 357 | 14.65 | `2025-05=-1.2199999999999978` | `positive_but_not_strong_enough_no_selection(양수지만 충분히 강하지 않음, 선택 아님)` |
| `s258_stc` | `s258_stc_2025h2_period_survival_gate` | 164.54 | 1.1345930470347647 | 257 | 20.51 | `2025-12=-82.97` | `positive_but_not_strong_enough_no_selection(양수지만 충분히 강하지 않음, 선택 아님)` |
| `s264_aih` | `s264_aih_validation_anchor_integrity` | 518.62 | 1.2219388300945322 | 467 | 11.71 | `2025-09=-23.95` | `positive_but_not_strong_enough_no_selection(양수지만 충분히 강하지 않음, 선택 아님)` |
| `s264_aih` | `s264_aih_202604_counter_shock_rebuild` | -30.46 | 0.4292673786771595 | 17 | 8.58 | `2026-04=-30.46` | `final_month_break_no_selection(마지막 달 붕괴, 선택 아님)` |
| `s264_lc` | `s264_lc_202604_counter_shock_control` | -39.29 | 0.4039745145631068 | 17 | 10.36 | `2026-04=-39.29` | `final_month_break_no_selection(마지막 달 붕괴, 선택 아님)` |
| `s262_lih` | `s262_lih_validation_coverage_rejoin` | 574.21 | 1.2129085124843344 | 458 | 13.39 | `2025-09=-33.510000000000005` | `positive_but_not_strong_enough_no_selection(양수지만 충분히 강하지 않음, 선택 아님)` |
| `s262_lih` | `s262_lih_202604_coverage_rejoin` | -39.29 | 0.4039745145631068 | 17 | 10.36 | `2026-04=-39.29` | `final_month_break_no_selection(마지막 달 붕괴, 선택 아님)` |
| `s264_aia` | `s264_aia_validation_coverage_rejoin` | 574.21 | 1.2129085124843344 | 458 | 13.39 | `2025-09=-33.510000000000005` | `positive_but_not_strong_enough_no_selection(양수지만 충분히 강하지 않음, 선택 아님)` |
| `s264_aia` | `s264_aia_202604_coverage_rejoin` | -39.29 | 0.4039745145631068 | 17 | 10.36 | `2026-04=-39.29` | `final_month_break_no_selection(마지막 달 붕괴, 선택 아님)` |

## Attribution(성과 귀속)

- `s258_stc`: s258_stc는 2023H2는 강하지만 2025H1/H2에서 PF(수익 팩터)와 DD(손실폭)가 불편해 stress challenger(압박 도전자) 위험이 계속 남는다. Next(다음): eighth follow-up(8차 후속)에서는 DD shape(손실폭 형태)와 adverse state(불리 상태)를 합치기보다 약한 기간별 생존 조건을 먼저 판정한다.
- `s264_aih`: s264_aih는 validation anchor(검증 앵커)는 회복됐지만 2026.04 counter shock(역충격)에서 음수라 final-month hole(마지막 달 구멍)이 남는다. Next(다음): validation repair(검증 수리)와 final-month shock(마지막 달 충격)을 분리해 repair cap(수리 제한) 안에서 살릴지 버릴지 결정한다.
- `s264_lc`: s264_lc control(대조)은 같은 2026.04에서 음수라 s264_aih 약점이 후보 단독 문제가 아니라 시장 구간 문제일 수 있음을 보여준다. Next(다음): control(대조)은 selection(선택)용이 아니라 해석 기준으로만 유지한다.
- `s262_lih`: s262_lih는 validation coverage rejoin(검증 커버리지 재합류)에서는 양수지만 2026.04 coverage rejoin(커버리지 재합류)에서 음수라 validation-heavy(검증 중심) 역할은 유지하되 최종월 약점이 남는다. Next(다음): validation strength(검증 강점)과 final-month fragility(마지막 달 취약성)를 분리해 대조 후보로 유지할지 판단한다.
- `s264_aia`: s264_aia는 validation coverage rejoin(검증 커버리지 재합류)에서는 s262_lih와 같은 양수 형태지만 2026.04 coverage rejoin(커버리지 재합류)에서 음수라 OOS anchor(표본외 앵커) 역할을 바로 회복했다고 볼 수 없다. Next(다음): OOS anchor(표본외 앵커) 역할은 final-month hole(마지막 달 구멍)과 validation damage(검증 손상)를 같이 본 뒤 유지 여부를 정한다.

## Boundary(경계)

- 이 검토는 exploratory review(탐색 검토)이며 후보 선택, 연구 기준선 선택, ONNX(ONNX 준비), Goal Achieve(목표 달성)를 주장하지 않는다.
- 다음 run267EF(267EF 실행)는 같은 repair(수리)를 오래 끌지 말고 s258_stc explosive runtime gap(폭발형 런타임 공백), s264_aih final-month hole(마지막 달 구멍), q06 explosive counter impulse(폭발형 역임펄스)를 분명히 나눠야 한다.

## Artifacts(산출물)

- trade_records(거래 기록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EE/runtime_gap_aware_seventh_followup_or_prune_balance_timeslice_trade_quality_review/trade_records.csv`
- time_slice_kpi(시간구간 KPI): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EE/runtime_gap_aware_seventh_followup_or_prune_balance_timeslice_trade_quality_review/time_slice_kpi.csv`
- curve_diagnostics(곡선 진단): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EE/runtime_gap_aware_seventh_followup_or_prune_balance_timeslice_trade_quality_review/curve_diagnostics.csv`
- candidate_profile_review(후보 프로필 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EE/runtime_gap_aware_seventh_followup_or_prune_balance_timeslice_trade_quality_review/candidate_profile_review.csv`
- negative_slice_summary(음수 구간 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EE/runtime_gap_aware_seventh_followup_or_prune_balance_timeslice_trade_quality_review/negative_slice_summary.csv`
- result_judgment(결과 판정): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267EE/runtime_gap_aware_seventh_followup_or_prune_balance_timeslice_trade_quality_review/result_judgment.csv`
