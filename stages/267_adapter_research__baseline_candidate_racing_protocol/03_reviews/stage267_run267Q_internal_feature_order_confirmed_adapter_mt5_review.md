# Stage267 Run267Q Internal Feature Order Confirmed Adapter MT5 Review(267단계 267Q 내부 피처 순서 확인 어댑터 MT5 검토)

- action(행동): MT5 Strategy Tester(MT5 전략 테스터) reports(보고서) `8`개를 trade/curve/time-slice(거래/곡선/시간구간)로 다시 검토했다.
- effect(효과): run267Q(267Q 실행)가 단순 KPI(핵심 성과 지표) 숫자만 좋은지, 아니면 내부 feature order(피처 순서) 고정 후에도 거래 모양과 약한 구간이 설명 가능한지 확인한다.
- status(상태): `run267Q_internal_feature_order_confirmed_adapter_mt5_review_completed`
- trade_records(거래 기록): `2516`
- time_slice_rows(시간 구간 행): `328`
- candidate_test_rows(후보-시험 행): `8`
- negative_slices(음수/손실폭 구간): `80`
- source_reproduction_mismatches(원천 재현 불일치): `0`
- max_abs_net_delta_vs_run267N(run267N 대비 최대 순수익 차이): `0.0`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 해석)

좋은 소식은 run267Q(267Q 실행)가 MT5(MetaTrader 5, 메타트레이더5)에서 run267N(267N 실행) 원천 표면을 거의 그대로 재현했다는 점이다. 즉, proxy score(대체 점수)를 internal adapter feature(내부 어댑터 피처)로 이름과 순서를 고정해도 런타임이 깨지지 않았다.
하지만 이건 후보 선택이 아니다. 더 중요한 점은 `abl_volatility_bandwidth`와 `rep_volatility_atr`, 그리고 Tier A(티어 A)와 Tier A+B(티어 A+B)가 후보별로 거의 같은 KPI 모양으로 접혔다는 점이다. 효과는 새 alpha(알파)를 찾았다기보다, 강했던 단서가 구조적으로 재현 가능한지 확인했다는 쪽에 가깝다.
그래프와 약한 구간 검토 기준에서는 아직 Goal Achieve(목표 달성) 조건이 아니다. 다음은 이 내부 Adapter(어댑터)를 더 밀지, 짧게 follow-up(후속)할지, 또는 후보군 전체 racing(경주)으로 되돌릴지 결정해야 한다.

## Candidate Review(후보 검토)

| candidate(후보) | test(시험) | route(경로) | net(순수익) | PF(수익 팩터) | DD%(손실폭) | trades(거래 수) | worst month(최악 월) | reproduction(재현) | read(판독) |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- |
| `s264_aia` | `abl_volatility_bandwidth` | `routed_total` | 408.29 | 1.347088 | 15.85 | 315 | `2024-06` -32.37 | `matched` | constructive_reproduction_watch_not_selection(건설적 재현 관찰, 선택 아님) |
| `s264_aia` | `abl_volatility_bandwidth` | `tier_only_total` | 408.29 | 1.347088 | 15.85 | 315 | `2024-06` -32.37 | `matched` | constructive_reproduction_watch_not_selection(건설적 재현 관찰, 선택 아님) |
| `s264_aia` | `rep_volatility_atr` | `routed_total` | 408.29 | 1.347088 | 15.85 | 315 | `2024-06` -32.37 | `matched` | constructive_reproduction_watch_not_selection(건설적 재현 관찰, 선택 아님) |
| `s264_aia` | `rep_volatility_atr` | `tier_only_total` | 408.29 | 1.347088 | 15.85 | 315 | `2024-06` -32.37 | `matched` | constructive_reproduction_watch_not_selection(건설적 재현 관찰, 선택 아님) |
| `s264_aih` | `abl_volatility_bandwidth` | `routed_total` | 412.57 | 1.349864 | 15.9 | 314 | `2024-06` -32.73 | `matched` | constructive_reproduction_watch_not_selection(건설적 재현 관찰, 선택 아님) |
| `s264_aih` | `abl_volatility_bandwidth` | `tier_only_total` | 412.57 | 1.349864 | 15.9 | 314 | `2024-06` -32.73 | `matched` | constructive_reproduction_watch_not_selection(건설적 재현 관찰, 선택 아님) |
| `s264_aih` | `rep_volatility_atr` | `routed_total` | 412.57 | 1.349864 | 15.9 | 314 | `2024-06` -32.73 | `matched` | constructive_reproduction_watch_not_selection(건설적 재현 관찰, 선택 아님) |
| `s264_aih` | `rep_volatility_atr` | `tier_only_total` | 412.57 | 1.349864 | 15.9 | 314 | `2024-06` -32.73 | `matched` | constructive_reproduction_watch_not_selection(건설적 재현 관찰, 선택 아님) |

## Candidate Summary(후보 요약)

| candidate(후보) | rows(행) | constructive(건설적) | unique shapes(고유 모양) | best net(최고 순수익) | worst DD%(최악 손실폭) | all reproduced(모두 재현) | read(판독) |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| `s264_aia` | 4 | 4 | 1 | 408.29 | 15.85 | `True` | runtime_reproduced_but_variants_collapsed(런타임 재현됨, 변형 차이는 접힘) |
| `s264_aih` | 4 | 4 | 1 | 412.57 | 15.9 | `True` | runtime_reproduced_but_variants_collapsed(런타임 재현됨, 변형 차이는 접힘) |

## Weak Slices(약한 구간)

| candidate(후보) | test(시험) | axis(축) | bucket(구간) | trades(거래 수) | net(순수익) | PF(수익 팩터) | DD%(손실폭) |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: |
| `s264_aih` | `abl_volatility_bandwidth` | `weekday` | `Monday` | 54 | -96.81 | 0.644551 | 22.346402 |
| `s264_aih` | `abl_volatility_bandwidth` | `weekday` | `Monday` | 54 | -96.81 | 0.644551 | 22.346402 |
| `s264_aih` | `rep_volatility_atr` | `weekday` | `Monday` | 54 | -96.81 | 0.644551 | 22.346402 |
| `s264_aih` | `rep_volatility_atr` | `weekday` | `Monday` | 54 | -96.81 | 0.644551 | 22.346402 |
| `s264_aia` | `abl_volatility_bandwidth` | `weekday` | `Monday` | 54 | -95.7 | 0.646315 | 22.052605 |
| `s264_aia` | `abl_volatility_bandwidth` | `weekday` | `Monday` | 54 | -95.7 | 0.646315 | 22.052605 |
| `s264_aia` | `rep_volatility_atr` | `weekday` | `Monday` | 54 | -95.7 | 0.646315 | 22.052605 |
| `s264_aia` | `rep_volatility_atr` | `weekday` | `Monday` | 54 | -95.7 | 0.646315 | 22.052605 |
| `s264_aih` | `abl_volatility_bandwidth` | `session_report` | `session_07_12_report_time` | 6 | -91.41 | 0.0 | 18.282 |
| `s264_aih` | `abl_volatility_bandwidth` | `session_report` | `session_07_12_report_time` | 6 | -91.41 | 0.0 | 18.282 |
| `s264_aih` | `rep_volatility_atr` | `session_report` | `session_07_12_report_time` | 6 | -91.41 | 0.0 | 18.282 |
| `s264_aih` | `rep_volatility_atr` | `session_report` | `session_07_12_report_time` | 6 | -91.41 | 0.0 | 18.282 |
| `s264_aia` | `abl_volatility_bandwidth` | `session_report` | `session_07_12_report_time` | 6 | -90.49 | 0.0 | 18.098 |
| `s264_aia` | `abl_volatility_bandwidth` | `session_report` | `session_07_12_report_time` | 6 | -90.49 | 0.0 | 18.098 |
| `s264_aia` | `rep_volatility_atr` | `session_report` | `session_07_12_report_time` | 6 | -90.49 | 0.0 | 18.098 |
| `s264_aia` | `rep_volatility_atr` | `session_report` | `session_07_12_report_time` | 6 | -90.49 | 0.0 | 18.098 |

## Runtime/Forensic Boundary(런타임/포렌식 경계)

- execution_result(실행 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267Q/internal_feature_order_confirmed_adapter_materialization/execution_result.json`
- source_kpi(원천 KPI): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267N/p0_ablation_replacement_materialization/kpi_summary.csv`
- source_reproduction_audit(원천 재현 감사): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267Q/internal_feature_order_confirmed_adapter_review/source_reproduction_audit.csv`
- trade_records(거래 기록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267Q/internal_feature_order_confirmed_adapter_review/trade_records.csv`
- time_slice_kpi(시간 구간 KPI): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267Q/internal_feature_order_confirmed_adapter_review/time_slice_kpi.csv`
- curve_diagnostics(곡선 진단): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267Q/internal_feature_order_confirmed_adapter_review/curve_diagnostics.csv`
- tester_identity(테스터 정체성): historical 2024(2024 과거 기간) `US100` `M5`, deposit(예치금) 500, Strategy Tester(전략 테스터) 산출물.
- runtime_claim_boundary(런타임 주장 경계): `runtime_probe` only, no runtime authority(런타임 권위 아님).
- result_judgment(결과 판정): diagnostic_review_completed_no_candidate_selection(진단 검토 완료, 후보 선택 없음).

## Judgment Boundary(판정 경계)

- selected_candidate(선택 후보): `none`.
- ONNX readiness(ONNX 준비): `not_claimed`.
- Goal Achieve(목표 달성): `not_claimed`.
- next_action(다음 행동): `run267R_design_internal_adapter_stability_followup_or_prune`.
