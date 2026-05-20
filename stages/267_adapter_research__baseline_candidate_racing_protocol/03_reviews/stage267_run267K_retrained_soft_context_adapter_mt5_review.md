# Stage267 Run267K Retrained Soft-Context Adapter MT5 Review(267단계 267K 재학습 부드러운 문맥 어댑터 MT5 검토)

- action(행동): run267K(267K 실행)의 MT5(MetaTrader 5, 메타트레이더5) report(보고서)에서 trade list(거래 목록)를 다시 파싱해 curve diagnostics(곡선 진단), time-slice KPI(시간 구간 핵심 성과 지표), negative slice(음수 구간)를 만들었다.
- effect(효과): net profit(순수익)만 보지 않고 월/요일/시간/세션/순서 구간에서 덜 깨지는지 확인한다.
- status(상태): `run267K_retrained_soft_context_adapter_mt5_review_completed`
- trade_records(거래 기록): `1140`
- time_slice_rows(시간 구간 행): `144`
- parser_errors(파서 오류): `0`
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`

## Easy Read(쉬운 해석)

두 후보 모두 run267B(267B 실행)의 2024년 원형 후보보다 순수익과 PF(profit factor, 수익 팩터)는 크게 좋아졌고 DD(drawdown, 손실폭)는 낮아졌다.
하지만 DD(drawdown, 손실폭)가 아직 22~24%대라 Goal Achieve(목표 달성)의 예쁜 곡선 기준에는 못 미친다. 즉, 다음 후보로 더 파볼 가치는 있지만 선택 후보는 아니다.
또한 routed total(라우팅 합산)은 fallback(대체 사용)이 0이라 Tier B(티어 B)가 실제로 메운 근거가 아니다. 이번에는 Tier A(티어 A) 재학습 표면의 2024 진단으로 읽어야 한다.
선택 후보(selected candidate, 선택 후보)는 없다. ONNX readiness(ONNX 준비)도 주장하지 않는다.

## Candidate Review(후보 검토)

| candidate(후보) | net(순수익) | base net(기준 순수익) | delta(차이) | PF(수익 팩터) | DD%(손실폭) | trades(거래 수) | weakest month(가장 약한 월) | read(판독) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| `s264_lc` | 779.14 | 71.34 | 707.8 | 1.358718 | 24.29 | 285 | `2024-12` -276.73 | improved_but_dd_pf_not_enough(개선됐지만 손실폭/수익 팩터 불충분) |
| `s264_aih` | 677.92 | 95.56 | 582.36 | 1.355457 | 22.92 | 285 | `2024-12` -237.96 | improved_but_dd_pf_not_enough(개선됐지만 손실폭/수익 팩터 불충분) |

## Weak Slices(약한 구간)

| candidate(후보) | axis(축) | bucket(구간) | trades(거래 수) | net(순수익) | PF(수익 팩터) | DD%(손실폭) |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| `s264_lc` | `weekday` | `Monday` | 43 | -294.12 | 0.45012 | 59.161327 |
| `s264_lc` | `month` | `2024-12` | 28 | -276.73 | 0.423022 | 58.452 |
| `s264_aih` | `weekday` | `Monday` | 43 | -262.28 | 0.445919 | 52.845496 |
| `s264_aih` | `month` | `2024-12` | 28 | -237.96 | 0.422048 | 50.648 |
| `s264_lc` | `session_report` | `session_07_12_report_time` | 3 | -100.33 | 0.0 | 20.066 |
| `s264_aih` | `session_report` | `session_07_12_report_time` | 3 | -88.3 | 0.0 | 17.66 |
| `s264_lc` | `month` | `2024-08` | 46 | -85.16 | 0.735503 | 20.871133 |
| `s264_aih` | `month` | `2024-08` | 46 | -71.41 | 0.747445 | 17.06677 |
| `s264_lc` | `month` | `2024-06` | 10 | -69.98 | 0.622607 | 15.265325 |
| `s264_aih` | `month` | `2024-06` | 10 | -60.08 | 0.63526 | 13.39646 |

## Performance Attribution(성과 귀인)

- attribution(귀인): 개선은 `stage267_adx_atr_soft_score`와 기존 rank/gate(순위/문) 표면을 supervised EBM retrain(지도학습 EBM 재학습)으로 다시 묶은 효과다.
- effect(효과): 이 결과만으로 Adapter(어댑터) 구조가 안정적이라고 말할 수 없고, 다음에는 약한 월/요일/시간 구간을 줄이면서도 PF(profit factor, 수익 팩터)와 거래 수가 유지되는지 봐야 한다.
- weakness(약점): 약한 월과 세션이 아직 남아 있고, DD(drawdown, 손실폭)가 Goal Achieve(목표 달성) 조건의 곡선 기준에 못 미친다.
- stop rule(중단 규칙): 다음 follow-up(후속)에서도 DD(drawdown, 손실폭)와 약한 월이 충분히 줄지 않으면 이 retrain branch(재학습 분기)는 짧게 닫고 전체 후보군 경주로 되돌린다.

## Backtest Forensics(백테스트 포렌식)

- execution_result(실행 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267K/retrained_soft_context_adapter_materialization/execution_result.json`
- base_kpi(기준 핵심 성과 지표): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267B/historical_2024/mt5_kpi_summary.csv`
- base_curve(기준 곡선): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267B/historical_2024/balance_curve_diagnostics.csv`
- source_reports(원천 보고서): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267K/retrained_soft_context_adapter_materialization/mt5/reports`
- tester_scope(테스터 범위): historical 2024(2024 과거 기간) `US100` `M5`, deposit(예치금) 500, Strategy Tester(전략 테스터) 산출물.
- evidence_boundary(근거 경계): reviewed diagnostic evidence(검토된 진단 근거)이며 candidate selection(후보 선택), ONNX parity(ONNX 동등성), runtime reproduction(런타임 재현) 근거가 아니다.

## Artifact Lineage(산출물 계보)

- producer(생산자): `stage_pipelines/stage267/run267K_retrained_soft_context_adapter_review.py`
- trade_records(거래 기록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267K/retrained_soft_context_adapter_materialization/trade_records.csv`
- time_slice_kpi(시간 구간 핵심 성과 지표): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267K/retrained_soft_context_adapter_materialization/time_slice_kpi.csv`
- curve_diagnostics(곡선 진단): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267K/retrained_soft_context_adapter_materialization/curve_diagnostics.csv`
- candidate_review(후보 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267K/retrained_soft_context_adapter_materialization/candidate_retrained_soft_context_review.csv`
- negative_slice_summary(음수 구간 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267K/retrained_soft_context_adapter_materialization/negative_slice_summary.csv`
- review_result(검토 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267K/retrained_soft_context_adapter_materialization/review_result.json`

## Judgment Boundary(판정 경계)

- result_subject(결과 대상): `run267K_retrained_soft_context_adapter_mt5_review`.
- judgment_label(판정 라벨): `diagnostic_review_completed_no_candidate_selection`.
- selected_candidate(선택 후보): `none`.
- ONNX readiness(ONNX 준비): `not_claimed`.
- Goal Achieve(목표 달성): `not_claimed`.
- next_action(다음 행동): `run267L_design_retrained_soft_context_adapter_followup_or_prune`.
