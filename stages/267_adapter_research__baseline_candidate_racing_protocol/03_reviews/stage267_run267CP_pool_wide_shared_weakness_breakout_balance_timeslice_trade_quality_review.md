# Stage267 Run267CP Shared Weakness Breakout Balance/Time-Slice/Trade-Quality Review(267단계 267CP 공유 약점 돌파 잔액/시간구간/거래품질 검토)

- action(행동): run267CO(267CO 실행)의 12개 MT5(MetaTrader 5, 메타트레이더5) report(보고서)를 trade list(거래 목록)로 다시 읽고 balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간구간 핵심 성과 지표), trade quality(거래 품질)를 계산했다.
- effect(효과): headline KPI(대표 핵심 성과 지표)가 좋아 보여도 월별/요일별/시간별/세션별/방향별/기간 구간 약점이 후보 선택을 막는지 확인한다.
- status(상태): `run267CP_pool_wide_shared_weakness_breakout_balance_timeslice_trade_quality_review_completed`
- source_run(원천 실행): `run267CO_stage267_pool_wide_shared_weakness_breakout_mt5_execution_v1`
- trade_records(거래 기록): `4700`
- curve_rows(곡선 행): `12`
- time_slice_rows(시간구간 행): `454`
- candidate_profile_rows(후보-프로필 행): `6`
- negative_slices(음수 구간): `34`
- parser_errors(파서 오류): `0`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `run267CQ_design_shared_weakness_breakout_followup_or_prune_from_run267CP_review`

## Easy Read(쉬운 해석)

이번 실행은 후보를 고르는 단계가 아니다. `s264_lc`는 상대적으로 손실폭이 편하지만 더 넓은 follow-up(후속)이 필요하고, `s264_aia`와 `s258_stc`는 수익은 보이나 DD(drawdown, 손실폭)와 약한 구간이 불편하다. `s264_aih`의 aggressive shock release(공격형 충격 해소)는 PF(profit factor, 수익 팩터)는 좋지만 거래 수와 총수익이 작아 단독 선택 근거가 아니다.

따라서 다음 run267CQ(267CQ 실행)는 숫자 1등을 고르는 것이 아니라 shared weakness breakout(공유 약점 돌파)을 후속/가지치기 설계로 바꾸어야 한다.

## Candidate Summary(후보 요약)

| candidate(후보) | profile rows(프로필 행) | constructive rows(건설 행) | risk rows(위험 행) | avg net(평균 순수익) | avg PF(평균 수익 팩터) | avg DD%(평균 손실폭 %) | avg trades(평균 거래 수) | worst month floor(최악 월 바닥) | read(판독) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `s264_lc` | 1 | 1 | 0 | 1883.88 | 1.513673 | 13.52 | 445.0 | -191.47 | narrow_or_mixed_clue_needs_more_pressure(좁거나 혼합 단서, 추가 압박 필요) |
| `s258_stc` | 1 | 0 | 1 | 1775.7 | 1.484981 | 31.52 | 438.0 | -218.65 | profitable_but_curve_risk_no_selection(수익은 있으나 곡선 위험, 선택 아님) |
| `s264_aia` | 1 | 1 | 0 | 1659.28 | 1.533047 | 28.17 | 424.0 | -165.39 | narrow_or_mixed_clue_needs_more_pressure(좁거나 혼합 단서, 추가 압박 필요) |
| `s262_lih` | 1 | 1 | 0 | 1216.12 | 1.398379 | 25.94 | 423.0 | -138.46 | narrow_or_mixed_clue_needs_more_pressure(좁거나 혼합 단서, 추가 압박 필요) |
| `s264_aih` | 2 | 2 | 0 | 924.875 | 1.562085 | 22.705 | 310.0 | -217.73 | narrow_or_mixed_clue_needs_more_pressure(좁거나 혼합 단서, 추가 압박 필요) |

## Profile Axis(프로필 축)

| profile(프로필) | rows(행) | avg net(평균 순수익) | avg PF(평균 수익 팩터) | avg DD%(평균 손실폭 %) | avg trades(평균 거래 수) | risk rows(위험 행) | best candidate(최고 후보) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `shared_weakness_state_interaction` | 5 | 1554.394 | 1.466367 | 25.216 | 426.2 | 1 | `s264_lc` |
| `aggressive_shock_release_reentry` | 1 | 612.76 | 1.722415 | 18.48 | 219.0 | 0 | `s264_aih` |

## Top Candidate-Profile Rows(상위 후보-프로필 행)

| candidate(후보) | profile(프로필) | net(순수익) | PF(수익 팩터) | DD%(손실폭 %) | trades(거래 수) | weakest month(최약 월) | read(판독) |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| `s264_lc` | `shared_weakness_state_interaction` | 1883.88 | 1.513673 | 13.52 | 445 | `2024-06` -191.47 | constructive_stability_clue_no_selection(건설적 안정 단서, 선택 아님) |
| `s258_stc` | `shared_weakness_state_interaction` | 1775.7 | 1.484981 | 31.52 | 438 | `2024-07` -218.65 | profit_but_dd_or_month_hole_uncomfortable(수익은 있으나 손실폭 또는 월별 구멍 불편) |
| `s264_aia` | `shared_weakness_state_interaction` | 1659.28 | 1.533047 | 28.17 | 424 | `2024-06` -165.39 | constructive_stability_clue_no_selection(건설적 안정 단서, 선택 아님) |
| `s264_aih` | `shared_weakness_state_interaction` | 1236.99 | 1.401754 | 26.93 | 401 | `2024-12` -217.73 | mixed_constructive_needs_followup(혼합 건설적, 후속 필요) |
| `s262_lih` | `shared_weakness_state_interaction` | 1216.12 | 1.398379 | 25.94 | 423 | `2024-12` -138.46 | mixed_constructive_needs_followup(혼합 건설적, 후속 필요) |
| `s264_aih` | `aggressive_shock_release_reentry` | 612.76 | 1.722415 | 18.48 | 219 | `2024-12` -72.24 | mixed_constructive_needs_followup(혼합 건설적, 후속 필요) |

## Weak Slices(약한 구간)

| candidate(후보) | profile(프로필) | axis(축) | bucket(구간) | trades(거래 수) | net(순수익) | PF(수익 팩터) | DD%(손실폭 %) |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: |
| `s264_aih` | `shared_weakness_state_interaction` | `weekday` | `Monday` | 60 | -291.01 | 0.610762 | 72.472332 |
| `s258_stc` | `shared_weakness_state_interaction` | `month` | `2024-07` | 55 | -218.65 | 0.628532 | 58.544 |
| `s264_aih` | `shared_weakness_state_interaction` | `month` | `2024-12` | 37 | -217.73 | 0.616592 | 51.435008 |
| `s264_lc` | `shared_weakness_state_interaction` | `weekday` | `Monday` | 66 | -202.71 | 0.748742 | 71.944807 |
| `s258_stc` | `shared_weakness_state_interaction` | `weekday` | `Monday` | 67 | -197.24 | 0.758154 | 68.017734 |
| `s262_lih` | `shared_weakness_state_interaction` | `weekday` | `Monday` | 64 | -195.78 | 0.705381 | 51.942934 |
| `s264_lc` | `shared_weakness_state_interaction` | `month` | `2024-06` | 16 | -191.47 | 0.368107 | 38.818934 |
| `s264_aia` | `shared_weakness_state_interaction` | `month` | `2024-06` | 16 | -165.39 | 0.46113 | 33.647306 |
| `s258_stc` | `shared_weakness_state_interaction` | `month` | `2024-06` | 18 | -159.44 | 0.56844 | 32.452695 |
| `s264_aih` | `shared_weakness_state_interaction` | `direction` | `buy` | 210 | -156.13 | 0.906131 | 54.905252 |
| `s264_aih` | `aggressive_shock_release_reentry` | `weekday` | `Monday` | 32 | -149.75 | 0.368916 | 29.95 |
| `s264_lc` | `shared_weakness_state_interaction` | `session_report` | `session_07_12_report_time` | 3 | -149.25 | 0.0 | 29.85 |
| `s264_aih` | `shared_weakness_state_interaction` | `month` | `2024-07` | 51 | -146.33 | 0.689558 | 46.282 |
| `s258_stc` | `shared_weakness_state_interaction` | `session_report` | `session_07_12_report_time` | 3 | -142.99 | 0.0 | 28.598 |
| `s262_lih` | `shared_weakness_state_interaction` | `month` | `2024-12` | 41 | -138.46 | 0.743853 | 38.572129 |

## Performance Attribution(성과 귀속)

- observed_change(관찰 변화): shared weakness breakout(공유 약점 돌파)은 전 후보에서 PF(profit factor, 수익 팩터)와 net profit(순수익)을 만들었지만, DD(drawdown, 손실폭)와 약한 월/세션이 후보별로 다르게 남았다.
- likely_drivers(가능 원인): shared weakness state interaction(공유 약점 상태 상호작용)은 거래 수를 충분히 유지하지만, 특정 후보는 손실폭이 같이 커진다. aggressive shock release(공격형 충격 해소)는 PF는 높지만 거래 수가 줄어 안정 후보로 보기 어렵다.
- alternative_explanations(대안 설명): Tier A+B(티어 A+B)는 duplicate-boundary(중복 경계)이므로 true fallback(실제 대체) 효과로 해석하면 안 된다. 또한 2024 기간 압박만으로 전체 기간 안정성을 말할 수 없다.
- attribution_confidence(귀속 신뢰도): `medium_low(중간-낮음)`. 거래 목록과 구간 근거는 생겼지만, 후속 설계와 반복 검증 전에는 선택 근거가 아니다.

## Backtest Forensics(백테스트 포렌식)

- source_execution_result(원천 실행 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CO/pool_wide_shared_weakness_breakout_mt5_execution/execution_result.json`
- source_kpi_summary(원천 KPI 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CO/pool_wide_shared_weakness_breakout_mt5_execution/kpi_summary.csv`
- source_forensics(원천 포렌식): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CO/pool_wide_shared_weakness_breakout_mt5_execution/backtest_forensics.csv`
- source_reports(원천 보고서): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CO/pool_wide_shared_weakness_breakout_mt5_execution/mt5/reports`
- tester_identity(테스터 정체성): historical 2024(2024 과거 기간) `US100` `M5`, deposit(예치금) 500, Strategy Tester(전략 테스터) 산출물.
- cost_assumptions(비용 가정): spread/commission/slippage/swap(스프레드/수수료/슬리피지/스왑)은 Strategy Tester(전략 테스터)와 broker history(브로커 이력) 조건을 따른다. 별도 비용 우위는 주장하지 않는다.

## Artifact Lineage(산출물 계보)

- producer(생산자): `stage_pipelines/stage267/run267CP_pool_wide_shared_weakness_breakout_balance_timeslice_trade_quality_review.py`
- trade_records(거래 기록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CP/pool_wide_shared_weakness_breakout_balance_timeslice_trade_quality_review/trade_records.csv`
- time_slice_kpi(시간구간 핵심 성과 지표): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CP/pool_wide_shared_weakness_breakout_balance_timeslice_trade_quality_review/time_slice_kpi.csv`
- curve_diagnostics(곡선 진단): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CP/pool_wide_shared_weakness_breakout_balance_timeslice_trade_quality_review/curve_diagnostics.csv`
- candidate_profile_review(후보-프로필 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CP/pool_wide_shared_weakness_breakout_balance_timeslice_trade_quality_review/candidate_profile_review.csv`
- candidate_summary(후보 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CP/pool_wide_shared_weakness_breakout_balance_timeslice_trade_quality_review/candidate_balance_timeslice_summary.csv`
- profile_axis_summary(프로필 축 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CP/pool_wide_shared_weakness_breakout_balance_timeslice_trade_quality_review/profile_axis_summary.csv`
- negative_slice_summary(음수 구간 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CP/pool_wide_shared_weakness_breakout_balance_timeslice_trade_quality_review/negative_slice_summary.csv`
- performance_attribution_summary(성과 귀속 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CP/pool_wide_shared_weakness_breakout_balance_timeslice_trade_quality_review/performance_attribution_summary.csv`
- result_judgment(결과 판정): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CP/pool_wide_shared_weakness_breakout_balance_timeslice_trade_quality_review/result_judgment.csv`
- parser_checks(파서 점검): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CP/pool_wide_shared_weakness_breakout_balance_timeslice_trade_quality_review/parser_checks.csv`
- review_result(검토 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CP/pool_wide_shared_weakness_breakout_balance_timeslice_trade_quality_review/review_result.json`

## Judgment Boundary(판정 경계)

- result_subject(결과 대상): `run267CP_pool_wide_shared_weakness_breakout_balance_timeslice_trade_quality_review`.
- judgment_label(판정 라벨): `exploratory(탐색)`.
- selected_candidate(선택 후보): `none`.
- selected_research_baseline(선택 연구 기준 후보): `none`.
- ONNX readiness(ONNX 준비): `not_claimed`.
- Goal Achieve(목표 달성): `not_claimed`.
- next_action(다음 행동): `run267CQ_design_shared_weakness_breakout_followup_or_prune_from_run267CP_review`.
