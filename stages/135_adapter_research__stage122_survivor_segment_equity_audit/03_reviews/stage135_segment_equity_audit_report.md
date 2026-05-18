# Stage135 Segment/Equity Audit Report(135단계 구간/자금곡선 감사 보고서)

- stage(단계): `135_adapter_research__stage122_survivor_segment_equity_audit`
- run(실행): `run135A_stage135_stage122_survivor_segment_equity_audit_v1`
- adapter(어댑터): `s133_stage122_control_cd5_h3_risk035`
- decision(판정): `continue_stage136_trade_count_concentration_repair_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Easy Read(쉬운 판독)

현재 후보는 강하다. validation/OOS(검증/외부 표본) 순손익(net P/L, 순손익)은 34D(레거시 기준)를 넘고, ATR bracket(ATR 괄호)과 model risk%(모델 위험 비율)도 이미 측정되어 있다.

하지만 아직 final package(최종 패키지)가 아니다. validation PF(검증 수익 팩터)는 34D 정확값보다 아주 조금 낮고, validation late third(검증 후반 3분위)가 순손익을 많이 들고 있으며, OOS drawdown(외부 표본 손실폭)은 34D보다 크고, trade count(거래 수)는 34D보다 많이 낮다.

Effect(효과): 이 후보를 버리지는 않지만, Stage136(136단계)에서 거래 수와 손익 집중을 작게 수리한다.

## KPI vs 34D(KPI와 34D 비교)

| split(분할) | PF(수익 팩터) | net(순손익) | DD%(손실률) | trades(거래) | main flags(주요 표시) |
|---|---:|---:|---:|---:|---|
| validation(검증) | 1.580000 | 1392.66 | 11.85 | 263 | largest_third_net_share, negative_month_count, pf_below_34d_exact, segment_quality_early, segment_quality_late, segment_quality_mid, trade_count_below_34d, trade_count_gap_to_34d |
| OOS(외부 표본) | 1.750000 | 1102.04 | 14.66 | 179 | drawdown_pct_above_34d, negative_month_count, top5_trade_share, trade_count_below_34d, trade_count_gap_to_34d |

## Evidence(근거)

- segment_stability(구간 안정성): `stages/135_adapter_research__stage122_survivor_segment_equity_audit/03_reviews/stage135_segment_stability_summary.csv`
- monthly_kpi(월별 핵심 성과 지표): `stages/135_adapter_research__stage122_survivor_segment_equity_audit/03_reviews/stage135_monthly_kpi_summary.csv`
- session_regime_kpi(세션/국면 핵심 성과 지표): `stages/135_adapter_research__stage122_survivor_segment_equity_audit/03_reviews/stage135_session_regime_kpi_summary.csv`
- long_short_kpi(롱/숏 핵심 성과 지표): `stages/135_adapter_research__stage122_survivor_segment_equity_audit/03_reviews/stage135_long_short_kpi_summary.csv`
- equity_curve_shape(자금곡선 모양): `stages/135_adapter_research__stage122_survivor_segment_equity_audit/03_reviews/stage135_equity_curve_shape_audit.md`
- risk_atr_behavior(위험/ATR 행동): `stages/135_adapter_research__stage122_survivor_segment_equity_audit/03_reviews/stage135_risk_atr_behavior_audit.csv`

## Boundary(경계)

deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료)는 주장하지 않는다.
