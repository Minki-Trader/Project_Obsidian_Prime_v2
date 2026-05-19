# Stage229 Dual-Objective Guard Blend Report(229단계 이중목표 보호 혼합 보고서)

- stage(단계): `229_adapter_research__dual_objective_guard_blend_after_selection_tradeoff`
- run(실행): `run229A_stage229_dual_objective_guard_blend_after_selection_tradeoff_v1`
- source_stage(원천 단계): `228_adapter_research__stage227_selection_structure_followup_review`
- source_run(원천 실행): `run228A_stage228_stage227_selection_structure_followup_review_v1`
- source_stage228_evidence_commit(원천 228단계 근거 커밋): `cdb3022287a76f8130a580d389f9dcce11dfef7e`
- source_stage228_hash_record_commit(원천 228단계 해시 기록 커밋): `9057f767ae2ea8b8a59fd7f7110d87ff3cf1cb68`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `open_stage230_bounded_followup_due_to_guard_blend_tradeoff_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Design(경계 설계)

- hypothesis(가설): session-only(세션 전용)의 OOS preservation(표본외 보존)을 경계로 두고, margin band(마진 구간) 폭을 조절하면 validation recovery(검증 회복)를 일부 얻을 수 있다.
- comparison_baseline(비교 기준): Stage227 session-only(세션 전용) OOS net(표본외 순손익) `719.48`, Stage227 session-and-margin(세션+마진) validation net(검증 순손익) `1046.57`.
- control_variables(고정 변수): long threshold(롱 임계값) `0.52`, short threshold(숏 임계값) `0.54`, ATR SL/TP(ATR 손절/익절) `2.0325/4.615`, model risk cap(모델 위험 상한) `0.031375`, lifecycle(생애주기) `hold=3,same_dir_cd=8,reverse=true`.
- changed_variables(변경 변수): session long block(세션 롱 차단)에 붙는 margin band(마진 구간) 폭만 `none`, `wide`, `base`, `tight`로 바꾼다.
- stop_condition(정지 조건): 4개 variants(변형)를 validation/OOS(검증/표본외) MT5 Strategy Tester(MetaTrader 5 전략 테스터)로 측정하면 Stage229(229단계)는 닫는다.

## KPI Read(KPI 핵심 성과 지표 판독)

| adapter(어댑터) | blend(혼합) | val net(검증 순손익) | early PF(초반 수익요인) | mid PF(중반 수익요인) | val DD%(검증 낙폭) | OOS net(표본외 순손익) | OOS PF(표본외 수익요인) | flags(표식) |
|---|---|---:|---:|---:|---:|---:|---:|---|
| s229_blend_session_only_ref | session_only | 952.16 | 1.563704 | 1.541194 | 12.6953 | 719.48 | 1.740000 | validation_net_below_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d |
| s229_blend_wide_margin_band | session_and_wide_margin | 1046.57 | 1.604594 | 1.481867 | 11.5520 | 637.94 | 1.640000 | validation_mid_pf_below_34d;oos_net_materially_below_stage171_primary |
| s229_blend_base_margin_band | session_and_base_margin | 1046.57 | 1.604594 | 1.481867 | 11.5520 | 625.27 | 1.620000 | validation_mid_pf_below_34d;oos_net_materially_below_stage171_primary |
| s229_blend_tight_margin_band | session_and_tight_margin | 1046.57 | 1.604594 | 1.481867 | 11.5520 | 624.78 | 1.620000 | validation_mid_pf_below_34d;oos_net_materially_below_stage171_primary |

## Judgment(판정)

- result_subject(판정 대상): Stage229 dual-objective guard blend(229단계 이중목표 보호 혼합).
- evidence_available(사용 근거): MT5 Strategy Tester(MetaTrader 5 전략 테스터) validation/OOS(검증/표본외), segment KPI(구간 핵심 성과 지표), monthly KPI(월별 핵심 성과 지표), concentration risk(집중 위험), risk/ATR telemetry(위험/ATR 기록).
- best_row(최선 행): `s229_blend_session_only_ref` with validation net(검증 순손익) `952.16`, mid PF(중반 수익요인) `1.541194`, OOS net(표본외 순손익) `719.48`.
- judgment_label(판정 라벨): `bounded_research_measurement_not_final(경계 연구 측정, 최종 아님)`.
- claim_boundary(주장 경계): research/development only(연구개발 전용).

Stage229(229단계)는 deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료)를 주장하지 않는다.
