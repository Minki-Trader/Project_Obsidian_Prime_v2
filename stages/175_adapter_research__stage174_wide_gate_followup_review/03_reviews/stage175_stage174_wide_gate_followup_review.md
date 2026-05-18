# Stage175 Stage174 Wide Gate Follow-up Review(175단계 174단계 넓은 제한문 후속 검토)

- stage(단계): `175_adapter_research__stage174_wide_gate_followup_review`
- run(실행): `run175A_stage175_stage174_wide_gate_followup_review_v1`
- source_stage(원천 단계): `174_adapter_research__wide_gate_mid_segment_recovery_repair`
- source_run(원천 실행): `run174A_stage174_wide_gate_mid_segment_recovery_repair_v1`
- external_verification_status(외부 검증 상태): `review_only_source_stage174_mt5_reports_completed`
- decision(판정): `open_stage176_tp45_dd_midpf_repair_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Result Subject(결과 대상)

Stage174(174단계)의 wide gate(넓은 제한문), TP(익절), SL(손절), risk cap(위험 상한) 변형을 판독했다. Effect(효과): Stage176(176단계)는 가장 좋은 단서만 좁게 이어받는다.

## Evidence Available(사용 가능한 근거)

- source_report(원천 보고서): `stages/174_adapter_research__wide_gate_mid_segment_recovery_repair/03_reviews/stage174_wide_gate_mid_segment_recovery_report.md`
- quality_matrix(품질 행렬): `stages/174_adapter_research__wide_gate_mid_segment_recovery_repair/03_reviews/stage174_quality_matrix.csv`
- balance_curve_audit(잔고 곡선 감사): `stages/174_adapter_research__wide_gate_mid_segment_recovery_repair/03_reviews/stage174_balance_curve_audit.csv`
- segment_kpi(구간 핵심 성과 지표): `stages/174_adapter_research__wide_gate_mid_segment_recovery_repair/03_reviews/stage174_segment_kpi_summary.csv`
- risk_atr_telemetry(위험/ATR 기록): `stages/174_adapter_research__wide_gate_mid_segment_recovery_repair/03_reviews/stage174_risk_atr_telemetry.csv`

## KPI Read(KPI 핵심 성과 지표 판독)

| adapter(어댑터) | val PF(검증 수익요인) | val net(검증 순손익) | val DD%(검증 낙폭) | mid PF(중반 수익요인) | late share(후반 비중) | OOS PF(표본외 수익요인) | OOS net(표본외 순손익) | OOS DD%(표본외 낙폭) | lesson(교훈) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| s174_wide_sl2075_risk0365_h3_cd5_sht54_lng52 | 1.580000 | 917.21 | 13.6782 | 1.313065 | 0.4438 | 1.830000 | 712.61 | 14.1950 | Original SL 2.075(기존 손절 2.075)와 wide gate(넓은 제한문)는 Stage172 SL 1.95(172단계 손절 1.95)보다 나아졌지만 34D net/PF/DD(34D 순손익/수익요인/낙폭)에는 아직 못 미친다. |
| s174_wide_sl2075_risk0380_h3_cd5_sht54_lng52 | 1.580000 | 971.62 | 14.2379 | 1.313500 | 0.4511 | 1.820000 | 748.53 | 14.8078 | Risk 3.8 percent(위험 3.8퍼센트)는 validation PF/net(검증 수익요인/순손익)을 충분히 고치지 못했고 DD(낙폭)를 키웠다. |
| s174_wide_tp45_sl2075_risk0365_h3_cd5_sht54_lng52 | 1.620000 | 1037.74 | 13.7450 | 1.375002 | 0.4078 | 1.910000 | 823.11 | 14.2029 | TP 4.5(익절 4.5)는 validation PF/net(검증 수익요인/순손익)을 회복하고 late share(후반 비중)를 낮췄지만, DD(낙폭), mid PF(중반 수익요인), OOS DD(표본외 낙폭)는 아직 실패다. |
| s174_midwide_sl2075_risk0370_h3_cd5_sht54_lng52 | 1.640000 | 1077.31 | 15.0661 | 1.416853 | 0.5435 | 1.820000 | 789.87 | 9.1306 | Midwide gate(중간 폭 제한문)는 validation PF/net(검증 수익요인/순손익)과 OOS DD(표본외 낙폭)를 좋게 했지만, validation DD(검증 낙폭)와 late concentration(후반 집중도)를 악화했다. |

## Judgment(판정)

- judgment_label(판정 라벨): `exploratory(탐색)`
- primary_clue(주 단서): `s174_wide_tp45_sl2075_risk0365_h3_cd5_sht54_lng52`
- why(이유): TP 4.5(익절 4.5)는 validation PF/net(검증 수익요인/순손익)을 34D(34D) 위로 올리고 late share(후반 비중)를 낮췄지만, validation DD(검증 낙폭), validation mid PF(검증 중반 수익요인), OOS DD(표본외 낙폭)가 아직 실패다.
- claim_boundary(주장 경계): research/development only(연구개발 전용). Deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료)는 아니다.
- next_condition(다음 조건): Stage176(176단계)에서 TP 4.5(익절 4.5)의 net/PF(순손익/수익요인)를 보존하면서 DD(낙폭), mid PF(중반 수익요인), OOS DD(표본외 낙폭)를 좁게 수리해야 한다.

## Route Decision(경로 판정)

- next_stage(다음 단계): `176_adapter_research__tp45_dd_midpf_repair`
- next_run(다음 실행): `run176A_stage176_tp45_dd_midpf_repair_v1`
- route_matrix(경로 행렬): `stages/175_adapter_research__stage174_wide_gate_followup_review/03_reviews/stage175_route_matrix.csv`
