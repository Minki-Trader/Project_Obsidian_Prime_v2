# Stage57 Equity Curve Audit(57단계 자금 곡선 감사)

- stage(단계): `57_adapter_quality__equity_segment_kpi_audit_gate`
- run(실행): `run51A_stage57_equity_segment_kpi_audit_v1`
- source(원천): Stage56(56단계) `run50CA_stage56_baseline_adapter_onnx_runtime_reproduction_v1`
- adapter(어댑터): `ba14_no_atr_sd5_lot025`
- boundary(경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Question(질문)

현재 Stage56(56단계) BaselineAdapter(기준선 어댑터) anchor(기준점)가 equity curve(자금 곡선)와 segment KPI(구간 핵심 성과 지표) 기준으로 ATR/risk(ATR/위험) 통합으로 바로 갈 만큼 충분한가?

## Read(판독)

Stage57(57단계)는 optimization(최적화)이나 repair(수리)를 하지 않았다. Effect(효과): 기존 run50CA(실행 run50CA) MT5 ONNX runtime(런타임) 보고서만 사용해 Stage58(58단계) 방향을 정한다.

## Validation(검증)

- net(순손익): `1009.93`
- trade_count(거래 수): `1358`
- early/mid/late net(초/중/후반 순손익): `early=276.35;mid=738.22;late=-4.64`
- negative months(음수 월): `2025-01, 2025-06, 2025-07`
- risk flags(위험 표식): `best_month_net_share, cost_stressed_expectancy, equity_drawdown_maximal_amount, largest_third_net_share, late_third_net_share, negative_month_count, negative_or_flat_segment, single_window_profit_concentration, top5_trade_share, validation_late_flatline_risk, weak_segment_pf`

Validation(검증)은 final net(최종 순손익)은 높지만 late third(후반 3분위)가 flat/negative(정체/음수)이고, top-five trade share(상위 5거래 비중)가 높다. Effect(효과): final net(최종 순손익)만으로 strong(강함)을 주장하지 않는다.

## OOS(표본외)

- net(순손익): `1048.98`
- trade_count(거래 수): `1014`
- early/mid/late net(초/중/후반 순손익): `early=9.49;mid=249.2;late=790.29`
- negative months(음수 월): `2025-10`
- risk flags(위험 표식): `largest_third_net_share, negative_month_count, oos_late_period_concentration, single_window_profit_concentration, weak_segment_pf`

OOS(표본외)는 net(순손익)이 좋지만 early third(초반 3분위)의 PF(수익 팩터)가 약하고 first month(첫 달)가 음수이며 late third(후반 3분위)에 수익이 몰린다. Effect(효과): validation/OOS consistency(검증/표본외 일관성)를 아직 research-grade(연구 등급)로 닫지 않는다.

## Decision(판정)

`proceed_to_stage58_adapter_repair_before_risk_atr`

Effect(효과): `ba14_no_atr_sd5_lot025`는 development reference(개발 참조)로 보존하지만, Stage58(58단계)는 먼저 bounded repair(경계 수리) 판단을 포함해야 한다. ATR SL/TP(ATR 손절/익절)와 model-controlled risk%(모델 제어 위험률)는 mandatory(필수)이지만, 추가 자체가 completion(완료)이 아니다.
