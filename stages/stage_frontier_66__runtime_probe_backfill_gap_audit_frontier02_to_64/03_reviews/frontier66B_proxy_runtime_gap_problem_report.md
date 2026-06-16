# F66B Proxy Runtime Gap Problem Report(프록시-런타임 간극 문제 보고)

Superseded note(대체 갱신 메모): F66C `frontier66C_proxy_signal_mt5_backfill_v1` later materialized(이후 물질화) F11,F15,F18-F49 proxy signal(프록시 신호) into MT5 runtime probe(런타임 탐침) handoff(인계) and executed(실행) 64/64 split runs(분할 실행). This F66B report(보고서)는 초기 problem framing(문제 프레이밍)으로 보존하며 current truth(현재 진실)는 F66C gap decomposition(간극 해체)을 우선한다.


- created_at_utc(생성 시각): `2026-06-16T02:49:06Z`
- claim boundary(주장 경계): `runtime_probe_backfill_gap_audit_observation_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Main Problems(주요 문제)

1. runtime KPI missing split(런타임 KPI 누락 분리): F15/F18/F19는 raw ONNX/joblib material(원 온엑스/잡리브 재료)이 있으나 EA-compatible candidate contract(EA 호환 후보 계약) 또는 runtime handoff candidate(런타임 인계 후보)가 없다. 나머지 누락 stage(단계)는 raw runtime material(원 런타임 재료)도 없다.
2. gap report missing(간극 보고 누락): F02-F10, F12-F14, F16-F17은 runtime KPI(런타임 KPI)가 있지만 proxy-runtime gap(프록시-런타임 간극) 보고가 stage-local(단계 로컬)로 없다.
3. runtime economics collapse(런타임 경제성 붕괴): F50~F64 중 gap report(간극 보고)가 있는 단계는 runtime PF(런타임 수익 팩터)가 대체로 낮고 DD(손실폭)가 목표축을 자주 넘는다.
4. semantics mismatch risk(의미 불일치 위험): F65에서 확인한 SL/TP unit semantics(손절/익절 단위 의미) 문제는 이전 stage(단계)의 proxy(프록시)와 MT5(메타트레이더5) 비교에도 공통 위험으로 남는다.

## Stage Gap Table(단계별 간극 표)

| stage(단계) | proxy best PF(프록시 최고 PF) | runtime best PF(런타임 최고 PF) | runtime worst DD%(런타임 최악 DD%) | signal diff(신호 차이) | SL/TP semantics risk(손절/익절 의미 위험) | problem tags(문제 태그) |
|---:|---:|---:|---:|---:|---|---|
| F02 | 1.27 | 1.21 | 46.15 | 0 | not_assessed_after_f65_clue(미평가, F65 단서 이후) | gap_report_missing(간극 보고 누락); runtime_dd_over_goal_axis(런타임 손실폭 목표축 초과) |
| F03 | 1.205 | 0.98 | 76.26 | 0 | not_assessed_after_f65_clue(미평가, F65 단서 이후) | gap_report_missing(간극 보고 누락); proxy_pf_not_transferred_to_runtime(프록시 수익 팩터 런타임 미전이); runtime_dd_over_goal_axis(런타임 손실폭 목표축 초과); runtime_pf_low(런타임 수익 팩터 낮음) |
| F04 | NA | 0.99 | 82.16 | 0 | not_applicable_proxy_metric_missing(해당 없음, 프록시 지표 누락) | gap_report_missing(간극 보고 누락); runtime_dd_over_goal_axis(런타임 손실폭 목표축 초과); runtime_pf_low(런타임 수익 팩터 낮음) |
| F05 | NA | 2.01 | 37.83 | 0 | not_applicable_proxy_metric_missing(해당 없음, 프록시 지표 누락) | gap_report_missing(간극 보고 누락); runtime_dd_over_goal_axis(런타임 손실폭 목표축 초과) |
| F06 | NA | 1.12 | 61.28 | 0 | not_applicable_proxy_metric_missing(해당 없음, 프록시 지표 누락) | gap_report_missing(간극 보고 누락); runtime_dd_over_goal_axis(런타임 손실폭 목표축 초과); runtime_pf_low(런타임 수익 팩터 낮음) |
| F07 | NA | 0.99 | 55.93 | 0 | not_applicable_proxy_metric_missing(해당 없음, 프록시 지표 누락) | gap_report_missing(간극 보고 누락); runtime_dd_over_goal_axis(런타임 손실폭 목표축 초과); runtime_pf_low(런타임 수익 팩터 낮음) |
| F08 | NA | 1.08 | 71.55 | 0 | not_applicable_proxy_metric_missing(해당 없음, 프록시 지표 누락) | gap_report_missing(간극 보고 누락); runtime_dd_over_goal_axis(런타임 손실폭 목표축 초과); runtime_pf_low(런타임 수익 팩터 낮음) |
| F09 | NA | 1.44 | 46.24 | 0 | not_applicable_proxy_metric_missing(해당 없음, 프록시 지표 누락) | gap_report_missing(간극 보고 누락); runtime_dd_over_goal_axis(런타임 손실폭 목표축 초과) |
| F10 | NA | 1.35 | 29.18 | 0 | not_applicable_proxy_metric_missing(해당 없음, 프록시 지표 누락) | gap_report_missing(간극 보고 누락); runtime_dd_over_goal_axis(런타임 손실폭 목표축 초과) |
| F12 | NA | 1.71 | 29.98 | 0 | not_applicable_proxy_metric_missing(해당 없음, 프록시 지표 누락) | gap_report_missing(간극 보고 누락); runtime_dd_over_goal_axis(런타임 손실폭 목표축 초과) |
| F13 | NA | 4.21 | 32.43 | 0 | not_applicable_proxy_metric_missing(해당 없음, 프록시 지표 누락) | gap_report_missing(간극 보고 누락); runtime_dd_over_goal_axis(런타임 손실폭 목표축 초과) |
| F14 | NA | 4.97 | 11.73 | 0 | not_applicable_proxy_metric_missing(해당 없음, 프록시 지표 누락) | gap_report_missing(간극 보고 누락); runtime_dd_over_goal_axis(런타임 손실폭 목표축 초과) |
| F16 | NA | 1.37 | NA | NA | not_applicable_proxy_metric_missing(해당 없음, 프록시 지표 누락) | gap_report_missing(간극 보고 누락) |
| F17 | NA | 1.13 | NA | NA | not_applicable_proxy_metric_missing(해당 없음, 프록시 지표 누락) | gap_report_missing(간극 보고 누락); runtime_pf_low(런타임 수익 팩터 낮음) |
| F50 | NA | 0.99 | 76.21 | 0 | not_applicable_proxy_metric_missing(해당 없음, 프록시 지표 누락) | runtime_dd_over_goal_axis(런타임 손실폭 목표축 초과); runtime_pf_low(런타임 수익 팩터 낮음) |
| F51 | NA | 0.86 | 86.37 | 0 | not_applicable_proxy_metric_missing(해당 없음, 프록시 지표 누락) | runtime_dd_over_goal_axis(런타임 손실폭 목표축 초과); runtime_pf_low(런타임 수익 팩터 낮음) |
| F52 | NA | 0.66 | 7.36 | 1269 | not_applicable_proxy_metric_missing(해당 없음, 프록시 지표 누락) | signal_count_parity_gap(신호 수 동등성 간극); runtime_pf_low(런타임 수익 팩터 낮음) |
| F53 | NA | 0.56 | 31.92 | 0 | not_applicable_proxy_metric_missing(해당 없음, 프록시 지표 누락) | runtime_dd_over_goal_axis(런타임 손실폭 목표축 초과); runtime_pf_low(런타임 수익 팩터 낮음) |
| F54 | NA | 0.61 | 63.63 | 0 | not_applicable_proxy_metric_missing(해당 없음, 프록시 지표 누락) | runtime_dd_over_goal_axis(런타임 손실폭 목표축 초과); runtime_pf_low(런타임 수익 팩터 낮음) |
| F55 | NA | 0.64 | 20.84 | 0 | not_applicable_proxy_metric_missing(해당 없음, 프록시 지표 누락) | runtime_dd_over_goal_axis(런타임 손실폭 목표축 초과); runtime_pf_low(런타임 수익 팩터 낮음) |
| F56 | NA | 0.74 | 29.91 | 0 | not_applicable_proxy_metric_missing(해당 없음, 프록시 지표 누락) | runtime_dd_over_goal_axis(런타임 손실폭 목표축 초과); runtime_pf_low(런타임 수익 팩터 낮음) |
| F57 | NA | 0.68 | 32.41 | 0 | not_applicable_proxy_metric_missing(해당 없음, 프록시 지표 누락) | runtime_dd_over_goal_axis(런타임 손실폭 목표축 초과); runtime_pf_low(런타임 수익 팩터 낮음) |
| F58 | NA | 0.68 | 34.43 | 0 | not_applicable_proxy_metric_missing(해당 없음, 프록시 지표 누락) | runtime_dd_over_goal_axis(런타임 손실폭 목표축 초과); runtime_pf_low(런타임 수익 팩터 낮음) |
| F59 | NA | 0.58 | 22.84 | 0 | not_applicable_proxy_metric_missing(해당 없음, 프록시 지표 누락) | runtime_dd_over_goal_axis(런타임 손실폭 목표축 초과); runtime_pf_low(런타임 수익 팩터 낮음) |
| F60 | NA | 0.51 | 14.89 | 1501 | not_applicable_proxy_metric_missing(해당 없음, 프록시 지표 누락) | runtime_dd_over_goal_axis(런타임 손실폭 목표축 초과); signal_count_parity_gap(신호 수 동등성 간극); runtime_pf_low(런타임 수익 팩터 낮음) |
| F61 | NA | 0.71 | 53.18 | 0 | not_applicable_proxy_metric_missing(해당 없음, 프록시 지표 누락) | runtime_dd_over_goal_axis(런타임 손실폭 목표축 초과); runtime_pf_low(런타임 수익 팩터 낮음) |
| F62 | NA | 0.61 | 22.31 | 685 | not_applicable_proxy_metric_missing(해당 없음, 프록시 지표 누락) | runtime_dd_over_goal_axis(런타임 손실폭 목표축 초과); signal_count_parity_gap(신호 수 동등성 간극); runtime_pf_low(런타임 수익 팩터 낮음) |
| F63 | NA | 0.44 | 22.56 | 670 | not_applicable_proxy_metric_missing(해당 없음, 프록시 지표 누락) | runtime_dd_over_goal_axis(런타임 손실폭 목표축 초과); signal_count_parity_gap(신호 수 동등성 간극); runtime_pf_low(런타임 수익 팩터 낮음) |
| F64 | NA | 0.7 | 28.23 | NA | not_applicable_proxy_metric_missing(해당 없음, 프록시 지표 누락) | runtime_dd_over_goal_axis(런타임 손실폭 목표축 초과); runtime_pf_low(런타임 수익 팩터 낮음) |

## Interpretation(해석)

현재 gap(간극)은 하나의 코드 오류로 단정하기 어렵다. F02-F10, F12-F14, F16-F17의 early backfill(초기 소급 실행)은 signal_count_diff(신호 수 차이)가 0인 경우가 많아 feature/signal parity(피처/신호 동등성)보다 exit/economics semantics(청산/경제성 의미) 쪽이 더 의심된다. F50 이후는 이미 gap report(간극 보고)가 있어 경제성 붕괴와 DD(손실폭) 초과가 반복된 negative memory(부정 기억) 계열이다. F11, F20~F49의 핵심 문제는 runtime probe(런타임 탐침) 실행 누락보다 runtime materialization(런타임 물질화) 자체의 부재이고, F15/F18/F19는 모델 파일은 있으나 실행 계약과 handoff candidate(인계 후보)가 닫히지 않은 문제다.
