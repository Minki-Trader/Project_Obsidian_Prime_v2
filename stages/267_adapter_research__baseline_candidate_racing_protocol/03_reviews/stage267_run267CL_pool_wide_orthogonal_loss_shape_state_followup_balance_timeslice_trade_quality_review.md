# Stage267 Run267CL Follow-up Balance/Time-Slice/Trade-Quality Review(267단계 267CL 후속 잔액/시간구간/거래품질 검토)

- status(상태): `run267CL_pool_wide_orthogonal_loss_shape_state_followup_balance_timeslice_trade_quality_review_completed`
- source_run(원천 실행): `run267CK_stage267_pool_wide_orthogonal_loss_shape_state_followup_mt5_execution_v1`
- trade_records(거래 기록): `1348`
- curve_rows(곡선 행): `4`
- time_slice_rows(시간 구간 행): `152`
- parser_errors(파서 오류): `0`
- next_action(다음 행동): `run267CM_design_pool_wide_orthogonal_loss_shape_state_followup_or_prune_from_run267CL_review`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 해석)

run267CK(267CK 실행)의 숫자는 둘 다 좋아 보였지만, run267CL(267CL 실행)은 그 숫자를 바로 고르지 않고 거래 목록과 곡선으로 다시 열어본 검토다.
효과(effect, 효과)는 `s264_lc`와 `s264_aia`가 실제로 덜 깨지는지, 특정 월/시간/방향에 손실이 몰리는지, DD(drawdown, 손실폭)가 편한지 분리해서 보는 것이다.
현재 결론은 둘 다 연구 단서로는 살아 있지만, 아직 선택 후보(selected candidate, 선택 후보)나 연구 기준 후보(selected research baseline, 선택 연구 기준 후보)는 아니다.

## Candidate Summary(후보 요약)

| candidate(후보) | profile rows(프로필 행) | strong clue rows(강한 단서 행) | risk rows(위험 행) | avg net(평균 순수익) | avg PF(평균 수익 팩터) | avg DD%(평균 손실폭 %) | avg trades(평균 거래 수) | worst month floor(최악 월 바닥) | read(판독) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `s264_lc` | 1 | 0 | 1 | 1207.3 | 1.506786 | 17.62 | 354.0 | -234.28 | profitable_but_curve_risk_watch_no_selection(수익 있으나 곡선 위험 관찰, 선택 아님) |
| `s264_aia` | 1 | 0 | 0 | 1119.33 | 1.548395 | 16.03 | 320.0 | -166.41 | broad_constructive_watch_no_selection(넓은 건설 관찰, 선택 아님) |

## Profile Axis(프로필 축)

| profile(프로필) | candidates(후보 수) | avg net(평균 순수익) | avg PF(평균 수익 팩터) | avg DD%(평균 손실폭 %) | avg trades(평균 거래 수) | worst month floor(최악 월 바닥) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `controlled impulse DD state throttle(통제형 임펄스 손실폭 상태 조절)` | 1 | 1207.3 | 1.506786 | 17.62 | 354.0 | -234.28 |
| `OOS anchor impulse pressure(표본외 앵커 임펄스 압박)` | 1 | 1119.33 | 1.548395 | 16.03 | 320.0 | -166.41 |

## Candidate-Profile Rows(후보-프로필 행)

| candidate(후보) | profile(프로필) | net(순수익) | PF(수익 팩터) | DD%(손실폭 %) | trades(거래 수) | worst month(최악 월) | weak session(약한 세션) | weak chron(약한 순서) | read(판독) |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- | --- |
| `s264_lc` | `controlled impulse DD state throttle(통제형 임펄스 손실폭 상태 조절)` | 1207.3 | 1.506786 | 17.62 | 354 | `2024-12` -234.28 | `session_07_12_report_time` -118.67 | `chron_mid` 225.71 | profit_with_uncomfortable_curve_risk(수익은 있으나 곡선 위험 불편) |
| `s264_aia` | `OOS anchor impulse pressure(표본외 앵커 임펄스 압박)` | 1119.33 | 1.548395 | 16.03 | 320 | `2024-12` -166.41 | `session_07_12_report_time` -114.42 | `chron_mid` 198.3 | constructive_followup_watch_no_selection(건설적 후속 관찰, 선택 아님) |

## Weak Slices(약한 구간)

| candidate(후보) | profile(프로필) | axis(축) | bucket(구간) | trades(거래 수) | net(순수익) | PF(수익 팩터) | DD%(손실폭 %) |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: |
| `s264_aia` | `OOS anchor impulse pressure(표본외 앵커 임펄스 압박)` | `weekday` | `Monday` | 47 | -303.41 | 0.460336 | 60.969266 |
| `s264_lc` | `controlled impulse DD state throttle(통제형 임펄스 손실폭 상태 조절)` | `weekday` | `Monday` | 49 | -241.79 | 0.594659 | 51.631912 |
| `s264_lc` | `controlled impulse DD state throttle(통제형 임펄스 손실폭 상태 조절)` | `month` | `2024-12` | 30 | -234.28 | 0.562159 | 54.464 |
| `s264_aia` | `OOS anchor impulse pressure(표본외 앵커 임펄스 압박)` | `month` | `2024-12` | 25 | -166.41 | 0.591461 | 43.222 |
| `s264_lc` | `controlled impulse DD state throttle(통제형 임펄스 손실폭 상태 조절)` | `session_report` | `session_07_12_report_time` | 3 | -118.67 | 0.0 | 23.734 |
| `s264_aia` | `OOS anchor impulse pressure(표본외 앵커 임펄스 압박)` | `session_report` | `session_07_12_report_time` | 3 | -114.42 | 0.0 | 22.884 |
| `s264_lc` | `controlled impulse DD state throttle(통제형 임펄스 손실폭 상태 조절)` | `month` | `2024-06` | 12 | -71.81 | 0.621973 | 14.456098 |
| `s264_lc` | `controlled impulse DD state throttle(통제형 임펄스 손실폭 상태 조절)` | `month` | `2024-07` | 46 | -61.39 | 0.780051 | 20.488 |
| `s264_aia` | `OOS anchor impulse pressure(표본외 앵커 임펄스 압박)` | `month` | `2024-06` | 10 | -53.39 | 0.65141 | 11.97 |
| `s264_aia` | `OOS anchor impulse pressure(표본외 앵커 임펄스 압박)` | `month` | `2024-07` | 41 | -45.14 | 0.820095 | 18.644 |
| `s264_lc` | `controlled impulse DD state throttle(통제형 임펄스 손실폭 상태 조절)` | `direction` | `buy` | 174 | -5.11 | 0.995745 | 33.423309 |

## Performance Attribution(성과 귀속)

- observed_change(관찰 변화): run267CK(267CK 실행)의 두 follow-up(후속) 후보는 2024 구간에서 순수익과 PF(수익 팩터)를 모두 양수로 유지했다.
- comparison_baseline(비교 기준): Stage267(267단계)의 2024 baseline(2024 기준), run267CG(267CG 실행), run267CH(267CH 실행)의 약한 구간 검토다.
- likely_drivers(가능 원인): `s264_lc`는 controlled impulse DD state throttle(통제형 임펄스 손실폭 상태 조절)로 거래 공급을 유지했고, `s264_aia`는 OOS anchor impulse pressure(표본외 앵커 임펄스 압박)로 PF(수익 팩터)를 조금 더 높였다.
- segment_checks(구간 점검): month(월), weekday(요일), close_hour_report(청산 시간), session_report(세션), direction(방향), chron_segment(시간 순서 구간)를 분리했다.
- attribution_confidence(귀속 신뢰도): `medium(중간)`. trade list(거래 목록)는 있지만, 아직 다음 설계에서 보류된 후보와 실패 기억을 함께 비교해야 한다.

## Backtest Forensics(백테스트 포렌식)

- source_execution_result(원천 실행 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CK/pool_wide_orthogonal_loss_shape_state_followup_mt5_execution/execution_result.json`
- source_kpi_summary(원천 KPI 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CK/pool_wide_orthogonal_loss_shape_state_followup_mt5_execution/kpi_summary.csv`
- source_forensics(원천 포렌식): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CK/pool_wide_orthogonal_loss_shape_state_followup_mt5_execution/backtest_forensics.csv`
- source_report(원천 보고서): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267CK_pool_wide_orthogonal_loss_shape_state_followup_mt5_execution.md`
- source_reports(원천 보고서 폴더): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CK/pool_wide_orthogonal_loss_shape_state_followup_mt5_execution/mt5/reports`
- tester_identity(테스터 정체성): historical 2024(2024 과거 구간), `US100`, `M5`, deposit(예치금) `500`, Strategy Tester(전략 테스터) 산출물.
- trade_evidence(거래 근거): MT5 report(보고서)의 deal list(체결 목록)를 trade list(거래 목록)로 다시 짝지어 확인했다.
- cost_assumptions(비용 가정): spread/commission/slippage/swap(스프레드/수수료/슬리피지/스왑)는 Strategy Tester(전략 테스터)와 broker history(브로커 이력) 조건에 따른다. 별도 비용 우위는 주장하지 않는다.

## Artifact Lineage(산출물 계보)

- producer(생산자): `stage_pipelines/stage267/run267CL_pool_wide_orthogonal_loss_shape_state_followup_balance_timeslice_trade_quality_review.py`
- trade_records(거래 기록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CL/pool_wide_orthogonal_loss_shape_state_followup_balance_timeslice_trade_quality_review/trade_records.csv`
- time_slice_kpi(시간 구간 KPI): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CL/pool_wide_orthogonal_loss_shape_state_followup_balance_timeslice_trade_quality_review/time_slice_kpi.csv`
- curve_diagnostics(곡선 진단): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CL/pool_wide_orthogonal_loss_shape_state_followup_balance_timeslice_trade_quality_review/curve_diagnostics.csv`
- candidate_profile_review(후보-프로필 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CL/pool_wide_orthogonal_loss_shape_state_followup_balance_timeslice_trade_quality_review/candidate_profile_review.csv`
- candidate_summary(후보 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CL/pool_wide_orthogonal_loss_shape_state_followup_balance_timeslice_trade_quality_review/candidate_balance_timeslice_summary.csv`
- profile_axis_summary(프로필 축 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CL/pool_wide_orthogonal_loss_shape_state_followup_balance_timeslice_trade_quality_review/profile_axis_summary.csv`
- negative_slice_summary(음수 구간 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CL/pool_wide_orthogonal_loss_shape_state_followup_balance_timeslice_trade_quality_review/negative_slice_summary.csv`
- parser_checks(파서 점검): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CL/pool_wide_orthogonal_loss_shape_state_followup_balance_timeslice_trade_quality_review/parser_checks.csv`
- review_result(검토 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CL/pool_wide_orthogonal_loss_shape_state_followup_balance_timeslice_trade_quality_review/review_result.json`

## Judgment Boundary(판정 경계)

- result_subject(결과 대상): `run267CL_pool_wide_orthogonal_loss_shape_state_followup_balance_timeslice_trade_quality_review`.
- judgment_label(판정 라벨): `diagnostic_review_completed_no_candidate_selection`.
- selected_candidate(선택 후보): `none`.
- selected_research_baseline(선택 연구 기준 후보): `none`.
- ONNX readiness(ONNX 준비): `not_claimed`.
- Goal Achieve(목표 달성): `not_claimed`.
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`.
- next_action(다음 행동): `run267CM_design_pool_wide_orthogonal_loss_shape_state_followup_or_prune_from_run267CL_review`.
