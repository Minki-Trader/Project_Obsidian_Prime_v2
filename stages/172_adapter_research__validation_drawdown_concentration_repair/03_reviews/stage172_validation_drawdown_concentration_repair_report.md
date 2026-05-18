# Stage172 Validation Drawdown Concentration Repair Report(172단계 검증 낙폭 집중도 수정 보고서)

- stage(단계): `172_adapter_research__validation_drawdown_concentration_repair`
- run(실행): `run172A_stage172_validation_drawdown_concentration_repair_v1`
- source_stage(원천 단계): `171_adapter_research__segment_stability_equity_curve_audit`
- source_run(원천 실행): `run171A_stage171_segment_stability_equity_curve_audit_v1`
- source_adapter(원천 어댑터): `s169_short_pre_risk0350_h3_cd5_sht54_lng52`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `open_stage173_bounded_repair_followup_due_to_drawdown_net_tradeoff_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Experiment Design(실험 설계)

- hypothesis(가설): Stage171(171단계)에서 확인한 validation DD(검증 낙폭)와 late concentration(후반 집중)은 entry model(진입 모델)을 바꾸지 않고 ATR SL(ATR 손절), bounded risk cap(경계 위험 상한), context gate(문맥 제한문)만 좁게 조정하면 완화될 수 있다.
- decision_use(판정 용도): 34D KPI(34D 핵심 성과 지표) 이상으로 계속 밀 후보가 있는지, 아니면 Stage173(173단계)에서 새 bounded repair(경계 수정)를 열어야 하는지 정한다.
- comparison_baseline(비교 기준): Stage171 primary(171단계 주 후보) `s169_short_pre_risk0350_h3_cd5_sht54_lng52` validation net(검증 순손익) `983.96`, validation DD(검증 낙폭) `14.301`, OOS net(표본외 순손익) `835.78`.
- control_variables(고정 변수): model source(모델 원천), signal column(신호 열), validation/OOS split(검증/표본외 분할), Tier B disabled(티어 B 비활성), thresholds(문턱값) short 0.54 / long 0.52, hold 3 bars(3봉 보유), cooldown 5 bars(5봉 대기).
- changed_variables(변경 변수): ATR stop multiplier(ATR 손절 배수), model risk cap(모델 위험 상한), short context gate width(숏 문맥 제한 폭).
- sample_scope(표본 범위): FPMarkets US100 M5(브로커 US100 5분봉), validation(검증) 2025-01-01~2025-09-30, OOS(표본외) 2025-10-01~2026-04-13.
- success_criteria(성공 기준): validation PF/net/DD(검증 수익요인/순손익/낙폭)가 34D 이상 또는 이내이고, early/mid PF(초반/중반 수익요인), late concentration(후반 집중), OOS PF/DD/net(표본외 수익요인/낙폭/순손익)가 함께 보존된다.
- failure_criteria(실패 기준): net(순손익)만 좋아지거나, DD(낙폭)만 좋아지면서 34D net(34D 순손익)과 segment PF(구간 수익요인)를 훼손한다.
- invalid_conditions(무효 조건): MT5 Strategy Tester(메타트레이더5 전략 테스터) report(보고서), telemetry(텔레메트리), risk/ATR record(위험/ATR 기록), artifact hash(산출물 해시)가 누락된다.
- stop_conditions(정지 조건): 이 4개 bounded variants(경계 변형)를 측정하면 Stage172(172단계)는 닫고 Stage173(173단계)로 넘긴다.
- evidence_plan(근거 계획): summary CSV(요약 CSV), segment KPI(구간 핵심 성과 지표), balance curve audit(잔고 곡선 감사), monthly KPI(월별 핵심 성과 지표), concentration report(집중도 보고), risk/ATR telemetry(위험/ATR 텔레메트리), ledgers(장부), current truth(현재 진실).

## KPI Read(KPI 판독)

| adapter(어댑터) | SL(손절) | risk(위험) | val PF(검증 수익요인) | val net(검증 순손익) | val DD%(검증 낙폭) | early/mid PF(초반/중반 수익요인) | late share(후반 비중) | OOS PF(표본외 수익요인) | OOS net(표본외 순손익) | flags(표식) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| s172_short_pre_control_risk0350_h3_cd5_sht54_lng52 | 2.075 | 0.0350 | 1.610000 | 983.96 | 14.3010 | 1.481586/1.477427 | 0.5508 | 1.820000 | 835.78 | validation_net_below_34d;validation_balance_dd_above_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d;validation_late_concentration_above_50pct |
| s172_short_pre_sl195_risk0350_h3_cd5_sht54_lng52 | 1.950 | 0.0350 | 1.540000 | 877.41 | 14.6856 | 1.280539/1.450489 | 0.5979 | 1.850000 | 948.34 | validation_pf_below_34d;validation_net_below_34d;validation_balance_dd_above_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d;validation_late_concentration_above_50pct |
| s172_short_pre_sl195_risk0360_h3_cd5_sht54_lng52 | 1.950 | 0.0360 | 1.540000 | 906.13 | 14.9140 | 1.271580/1.455890 | 0.6025 | 1.860000 | 999.52 | validation_pf_below_34d;validation_net_below_34d;validation_balance_dd_above_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d;validation_late_concentration_above_50pct |
| s172_short_wide_sl195_risk0365_h3_cd5_sht54_lng52 | 1.950 | 0.0365 | 1.480000 | 760.45 | 11.7848 | 1.575421/1.288458 | 0.4723 | 1.840000 | 793.98 | validation_pf_below_34d;validation_net_below_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d;oos_balance_dd_above_34d |

## Best Read(최선 판독)

- best_adapter(최선 어댑터): `s172_short_wide_sl195_risk0365_h3_cd5_sht54_lng52`
- validation_net(검증 순손익): `760.45`
- validation_balance_dd(검증 잔고 낙폭): `11.7848`
- validation_late_share(검증 후반 비중): `0.4723`
- oos_pf(표본외 수익요인): `1.840000`
- quality_flags(품질 표식): `validation_pf_below_34d;validation_net_below_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d;oos_balance_dd_above_34d`

## Judgment(판정)

Stage172(172단계)는 deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위)를 만들지 않는다. Effect(효과): 결과가 좋아도 research/development only(연구개발 전용) 후보로만 남긴다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
