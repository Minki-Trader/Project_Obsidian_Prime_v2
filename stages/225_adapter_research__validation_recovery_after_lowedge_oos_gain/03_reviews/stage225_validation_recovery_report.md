# Stage225 Validation Recovery Report(225단계 검증 회복 보고서)

- stage(단계): `225_adapter_research__validation_recovery_after_lowedge_oos_gain`
- run(실행): `run225A_stage225_validation_recovery_after_lowedge_oos_gain_v1`
- source_stage(원천 단계): `224_adapter_research__stage223_oos_recovery_followup_review`
- source_run(원천 실행): `run224A_stage224_stage223_oos_recovery_followup_review_v1`
- source_stage224_evidence_commit(원천 224단계 근거 커밋): `98093eae8fd0d033bff8560b3aa8a8304c491885`
- source_stage224_hash_record_commit(원천 224단계 해시 기록 커밋): `6abc125d59657ed6b192d63f1773a7dba6cb952c`
- source_oos_gain(원천 표본외 개선): `s223_oos_lowedge_long_guard`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `open_stage226_bounded_followup_due_to_validation_recovery_tradeoff_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Design(경계 설계)

- hypothesis(가설): lowedge long guard(저엣지 롱 보호)의 OOS gain(표본외 개선)을 유지하면서 long threshold(롱 문턱값)을 낮추면 validation trade supply(검증 거래 공급)가 회복될 수 있다.
- comparison_baseline(비교 기준): Stage223(223단계) `s223_oos_lowedge_long_guard`, OOS net(표본외 순손익) `765.4`, validation net(검증 순손익) `833.22`.
- control_variables(고정 변수): ATR SL/TP(ATR 손절/익절) `2.0325/4.615`, model risk cap(모델 위험 상한) `0.031375`, lifecycle(생애주기) `hold=3,same_dir_cd=8,reverse=true`, short threshold(숏 문턱값) `0.54`, lowedge long guard(저엣지 롱 보호).
- changed_variables(변경 변수): long threshold(롱 문턱값)만 `0.520`, `0.515`, `0.510`, `0.505`로 낮춘다.
- stop_condition(정지 조건): 4개 variants(변형)를 validation/OOS(검증/표본외) MT5 Strategy Tester(MetaTrader 5 전략 테스터)로 측정하면 Stage225(225단계)는 닫는다.

## KPI Read(KPI 핵심 성과 지표 판독)

| adapter(어댑터) | long threshold(롱 문턱값) | val net(검증 순손익) | early PF(초반 수익요인) | mid PF(중반 수익요인) | val DD%(검증 낙폭) | OOS net(표본외 순손익) | flags(표식) |
|---|---:|---:|---:|---:|---:|---:|---|
| s225_val_lowedge_lng520 | 0.52 | 833.22 | 1.446826 | 1.498516 | 13.0158 | 765.40 | validation_net_below_34d;validation_balance_dd_above_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d;validation_late_concentration_above_50pct |
| s225_val_lowedge_lng515 | 0.515 | 833.22 | 1.446826 | 1.498516 | 13.0158 | 765.40 | validation_net_below_34d;validation_balance_dd_above_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d;validation_late_concentration_above_50pct |
| s225_val_lowedge_lng510 | 0.51 | 833.22 | 1.446826 | 1.498516 | 13.0158 | 765.40 | validation_net_below_34d;validation_balance_dd_above_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d;validation_late_concentration_above_50pct |
| s225_val_lowedge_lng505 | 0.505 | 833.22 | 1.446826 | 1.498516 | 13.0158 | 765.40 | validation_net_below_34d;validation_balance_dd_above_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d;validation_late_concentration_above_50pct |

## Judgment(판정)

- result_subject(판정 대상): Stage225 long-threshold validation recovery(225단계 롱 문턱값 검증 회복).
- evidence_available(사용 근거): MT5 Strategy Tester(MetaTrader 5 전략 테스터) validation/OOS(검증/표본외), segment KPI(구간 핵심 성과 지표), monthly KPI(월별 핵심 성과 지표), concentration risk(집중 위험), risk/ATR telemetry(위험/ATR 기록).
- best_row(최선 행): `s225_val_lowedge_lng520` with validation net(검증 순손익) `833.22`, mid PF(중반 수익요인) `1.498516`, OOS net(표본외 순손익) `765.40`.
- judgment_label(판정 라벨): `bounded_research_measurement_not_final(경계 연구 측정, 최종 아님)`.
- claim_boundary(주장 경계): research/development only(연구개발 전용).

Stage225(225단계)는 deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료)를 주장하지 않는다.
