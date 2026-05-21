# Stage267 Run267CH Orthogonal Loss-Shape/State Balance Review(267단계 267CH 직교 손실 형태/상태 잔액 검토)

- action(행동): run267CG(267CG 실행)의 20개 MT5(MetaTrader 5, 메타트레이더5) report(보고서)를 trade list(거래 목록)로 다시 파싱하고, balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간구간 핵심 성과 지표), trade quality(거래 품질)를 만들었다.
- effect(효과): headline KPI(대표 핵심 성과 지표)만 보지 않고 후보별 약한 월, 요일, 시간, 세션, 방향, 기간 구간을 분리해 다음 follow-up/prune(후속/가지치기) 판단에 쓸 수 있다.
- status(상태): `run267CH_pool_wide_orthogonal_loss_shape_state_balance_timeslice_trade_quality_review_completed`
- source_run(원천 실행): `run267CG_stage267_pool_wide_orthogonal_loss_shape_state_mt5_execution_v1`
- trade_records(거래 기록): `6078`
- curve_rows(곡선 행): `20`
- time_slice_rows(시간구간 행): `744`
- parser_errors(파서 오류): `0`
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`

## Easy Read(쉬운 해석)

run267CG(267CG 실행)는 숫자를 만들었고, run267CH(267CH 실행)는 그 숫자가 덜 깨지는지 봤다. loss shape proxy(손실 형태 대체)는 상대적으로 얌전하지만 수익 확장이 작고, similar replacement impulse(유사 대체 임펄스)는 수익을 키우는 대신 DD(drawdown, 손실폭)와 약한 구간 부담이 같이 커진다.

그래서 아직 selected candidate(선택 후보)는 없다. 다음 run267CI(267CI 실행)에서는 넓게 산 후보를 바로 고르지 말고, 수익을 키운 축과 손실폭을 키운 축을 분리해 follow-up/prune(후속/가지치기)해야 한다.

## Candidate Summary(후보 요약)

| candidate(후보) | strong clues(강한 단서) | risk rows(위험 행) | avg net(평균 순수익) | avg PF(평균 수익 팩터) | avg DD%(평균 손실폭) | avg trades(평균 거래 수) | worst month floor(최악 월 바닥) | read(판독) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `s264_lc` | 0 | 0 | 1133.6 | 1.709598 | 14.61 | 307.0 | -170.6 | broad_constructive_watch_no_selection(넓은 건설 관찰, 선택 아님) |
| `s258_stc` | 0 | 1 | 1119.755 | 1.569481 | 22.955 | 329.0 | -173.27 | risk_first_watch_or_prune(위험 우선 관찰 또는 가지치기) |
| `s264_aia` | 0 | 0 | 986.925 | 1.650856 | 21.685 | 295.0 | -136.74 | broad_constructive_watch_no_selection(넓은 건설 관찰, 선택 아님) |
| `s264_aih` | 0 | 0 | 930.68 | 1.706968 | 19.785 | 281.5 | -154.08 | broad_constructive_watch_no_selection(넓은 건설 관찰, 선택 아님) |
| `s262_lih` | 0 | 0 | 900.53 | 1.588567 | 18.91 | 307.0 | -152.26 | broad_constructive_watch_no_selection(넓은 건설 관찰, 선택 아님) |

## Profile Axis(프로필 축)

| profile(프로필) | candidates(후보 수) | avg net(평균 순수익) | avg PF(평균 수익 팩터) | avg DD%(평균 손실폭) | avg trades(평균 거래 수) | worst month floor(최악 월 바닥) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `similar replacement impulse(유사 대체 임펄스)` | 5 | 1348.304 | 1.467955 | 26.22 | 396.0 | -173.27 |
| `loss shape proxy(손실 형태 대체)` | 5 | 680.292 | 1.822233 | 12.958 | 211.8 | -99.07 |

## Top Candidate-Profile Rows(상위 후보-프로필 행)

| candidate(후보) | profile(프로필) | net(순수익) | PF(수익 팩터) | DD%(손실폭) | trades(거래 수) | worst month(최악 월) | read(판독) |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| `s264_lc` | `similar replacement impulse(유사 대체 임펄스)` | 1568.81 | 1.496729 | 17.43 | 408 | `2024-12` -170.6 | constructive_wide_watch_no_selection(넓은 관찰 가치, 선택 아님) |
| `s258_stc` | `similar replacement impulse(유사 대체 임펄스)` | 1414.48 | 1.435996 | 31.65 | 419 | `2024-07` -173.27 | profit_with_uncomfortable_dd_or_weak_month(수익은 있으나 손실폭 또는 약한 월 불편) |
| `s264_aia` | `similar replacement impulse(유사 대체 임펄스)` | 1408.59 | 1.500549 | 28.37 | 396 | `2024-07` -136.74 | constructive_wide_watch_no_selection(넓은 관찰 가치, 선택 아님) |
| `s262_lih` | `similar replacement impulse(유사 대체 임펄스)` | 1183.13 | 1.469658 | 28.76 | 388 | `2024-07` -152.26 | constructive_wide_watch_no_selection(넓은 관찰 가치, 선택 아님) |
| `s264_aih` | `similar replacement impulse(유사 대체 임펄스)` | 1166.51 | 1.436843 | 24.89 | 369 | `2024-12` -154.08 | constructive_wide_watch_no_selection(넓은 관찰 가치, 선택 아님) |
| `s258_stc` | `loss shape proxy(손실 형태 대체)` | 825.03 | 1.702967 | 14.26 | 239 | `2024-12` -99.07 | constructive_wide_watch_no_selection(넓은 관찰 가치, 선택 아님) |
| `s264_lc` | `loss shape proxy(손실 형태 대체)` | 698.39 | 1.922466 | 11.79 | 206 | `2024-12` -48.36 | constructive_wide_watch_no_selection(넓은 관찰 가치, 선택 아님) |
| `s264_aih` | `loss shape proxy(손실 형태 대체)` | 694.85 | 1.977093 | 14.68 | 194 | `2024-04` -54.05 | constructive_wide_watch_no_selection(넓은 관찰 가치, 선택 아님) |
| `s262_lih` | `loss shape proxy(손실 형태 대체)` | 617.93 | 1.707475 | 9.06 | 226 | `2024-12` -57.91 | constructive_wide_watch_no_selection(넓은 관찰 가치, 선택 아님) |
| `s264_aia` | `loss shape proxy(손실 형태 대체)` | 565.26 | 1.801162 | 15.0 | 194 | `2024-04` -41.61 | constructive_wide_watch_no_selection(넓은 관찰 가치, 선택 아님) |

## Weak Slices(약한 구간)

| candidate(후보) | profile(프로필) | axis(축) | bucket(구간) | trades(거래 수) | net(순수익) | PF(수익 팩터) | DD%(손실폭) |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: |
| `s258_stc` | `similar replacement impulse(유사 대체 임펄스)` | `weekday` | `Monday` | 64 | -313.09 | 0.605362 | 72.487097 |
| `s264_aih` | `similar replacement impulse(유사 대체 임펄스)` | `weekday` | `Monday` | 54 | -256.75 | 0.614252 | 62.608093 |
| `s264_lc` | `similar replacement impulse(유사 대체 임펄스)` | `weekday` | `Monday` | 61 | -256.56 | 0.655897 | 70.887953 |
| `s264_aia` | `similar replacement impulse(유사 대체 임펄스)` | `weekday` | `Monday` | 59 | -215.73 | 0.672894 | 65.835827 |
| `s258_stc` | `loss shape proxy(손실 형태 대체)` | `weekday` | `Monday` | 37 | -185.98 | 0.445911 | 37.196 |
| `s262_lih` | `similar replacement impulse(유사 대체 임펄스)` | `weekday` | `Monday` | 58 | -180.03 | 0.695576 | 56.205741 |
| `s258_stc` | `similar replacement impulse(유사 대체 임펄스)` | `month` | `2024-07` | 55 | -173.27 | 0.669805 | 53.714 |
| `s264_lc` | `similar replacement impulse(유사 대체 임펄스)` | `month` | `2024-12` | 37 | -170.6 | 0.722538 | 60.726 |
| `s264_aih` | `similar replacement impulse(유사 대체 임펄스)` | `month` | `2024-12` | 32 | -154.08 | 0.680776 | 43.450092 |
| `s262_lih` | `similar replacement impulse(유사 대체 임펄스)` | `month` | `2024-07` | 51 | -152.26 | 0.616705 | 44.692 |
| `s258_stc` | `similar replacement impulse(유사 대체 임펄스)` | `month` | `2024-06` | 17 | -146.22 | 0.523791 | 29.692561 |
| `s264_aia` | `loss shape proxy(손실 형태 대체)` | `weekday` | `Monday` | 29 | -141.03 | 0.310232 | 28.206 |
| `s264_aih` | `similar replacement impulse(유사 대체 임펄스)` | `month` | `2024-07` | 47 | -138.9 | 0.643334 | 34.28 |
| `s264_lc` | `similar replacement impulse(유사 대체 임펄스)` | `session_report` | `session_07_12_report_time` | 3 | -138.5 | 0.0 | 27.7 |
| `s264_aia` | `similar replacement impulse(유사 대체 임펄스)` | `month` | `2024-07` | 51 | -136.74 | 0.673776 | 43.778 |

## Performance Attribution(성과 귀속)

- observed_change(관찰 변화): similar replacement impulse(유사 대체 임펄스)는 대부분 후보에서 net profit(순수익)과 trade count(거래 수)를 늘렸지만 DD(drawdown, 손실폭)도 같이 커졌다.
- likely_drivers(가능 원인): trend strength proxy(추세 강도 대체)와 impulse(임펄스) 축이 진입 공급을 늘리면서 수익 기회와 손실 노출을 동시에 키운 것으로 보인다.
- alternative_explanations(대체 설명): Tier A+B(티어 A+B)는 실제 fallback(대체) 합산이 아니라 duplicate boundary(중복 경계)이므로, 넓은 라우팅 안정성으로 해석하면 안 된다.
- attribution_confidence(귀속 신뢰도): `medium(중간)`. MT5 trade list(거래 목록) 근거는 생겼지만, 아직 후속 설계와 추가 기간 압박이 필요하다.

## Backtest Forensics(백테스트 포렌식)

- source_execution_result(원천 실행 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CG/pool_wide_orthogonal_loss_shape_state_mt5_execution/execution_result.json`
- source_kpi_summary(원천 KPI 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CG/pool_wide_orthogonal_loss_shape_state_mt5_execution/kpi_summary.csv`
- source_forensics(원천 포렌식): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CG/pool_wide_orthogonal_loss_shape_state_mt5_execution/backtest_forensics.csv`
- source_reports(원천 보고서): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CG/pool_wide_orthogonal_loss_shape_state_mt5_execution/mt5/reports`
- tester_scope(테스터 범위): historical 2024(2024 과거 기간) `US100` `M5`, deposit(예치금) 500, Strategy Tester(전략 테스터) 산출물.
- cost_assumptions(비용 가정): spread/commission/slippage/swap(스프레드/수수료/슬리피지/스왑)은 Strategy Tester(전략 테스터)와 broker history(브로커 이력) 조건을 따른다. 별도 비용 우위는 주장하지 않는다.

## Artifact Lineage(산출물 계보)

- producer(생산자): `stage_pipelines/stage267/run267CH_pool_wide_orthogonal_loss_shape_state_balance_timeslice_trade_quality_review.py`
- trade_records(거래 기록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CH/pool_wide_orthogonal_loss_shape_state_balance_timeslice_trade_quality_review/trade_records.csv`
- time_slice_kpi(시간구간 KPI): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CH/pool_wide_orthogonal_loss_shape_state_balance_timeslice_trade_quality_review/time_slice_kpi.csv`
- curve_diagnostics(곡선 진단): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CH/pool_wide_orthogonal_loss_shape_state_balance_timeslice_trade_quality_review/curve_diagnostics.csv`
- candidate_profile_review(후보-프로필 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CH/pool_wide_orthogonal_loss_shape_state_balance_timeslice_trade_quality_review/candidate_profile_review.csv`
- candidate_summary(후보 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CH/pool_wide_orthogonal_loss_shape_state_balance_timeslice_trade_quality_review/candidate_balance_timeslice_summary.csv`
- profile_axis_summary(프로필 축 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CH/pool_wide_orthogonal_loss_shape_state_balance_timeslice_trade_quality_review/profile_axis_summary.csv`
- negative_slice_summary(음수 구간 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CH/pool_wide_orthogonal_loss_shape_state_balance_timeslice_trade_quality_review/negative_slice_summary.csv`
- parser_checks(파서 점검): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CH/pool_wide_orthogonal_loss_shape_state_balance_timeslice_trade_quality_review/parser_checks.csv`
- review_result(검토 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CH/pool_wide_orthogonal_loss_shape_state_balance_timeslice_trade_quality_review/review_result.json`

## Judgment Boundary(판정 경계)

- result_subject(결과 대상): `run267CH_pool_wide_orthogonal_loss_shape_state_balance_timeslice_trade_quality_review`.
- judgment_label(판정 라벨): `diagnostic_review_completed_no_candidate_selection`.
- selected_candidate(선택 후보): `none`.
- selected_research_baseline(선택 연구 기준 후보): `none`.
- ONNX readiness(ONNX 준비): `not_claimed`.
- Goal Achieve(목표 달성): `not_claimed`.
- next_action(다음 행동): `run267CI_design_pool_wide_orthogonal_loss_shape_state_followup_or_prune`.
