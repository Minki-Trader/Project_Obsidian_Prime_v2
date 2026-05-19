# Stage227 Selection Structure Repair Report(227단계 선택 구조 수리 보고서)

- stage(단계): `227_adapter_research__selection_structure_repair_after_threshold_axis_no_effect`
- run(실행): `run227A_stage227_selection_structure_repair_after_threshold_axis_no_effect_v1`
- source_stage(원천 단계): `226_adapter_research__stage225_validation_recovery_followup_review`
- source_run(원천 실행): `run226A_stage226_stage225_validation_recovery_followup_review_v1`
- source_stage226_evidence_commit(원천 226단계 근거 커밋): `a8ea88d0fcf550d2432dc4b19376551c4124b008`
- source_stage226_hash_record_commit(원천 226단계 해시 기록 커밋): `73d1ec90acda97676c3447c56210bbe4425743eb`
- source_lowedge_adapter(원천 저엣지 어댑터): `s225_val_lowedge_lng520`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `open_stage228_bounded_followup_due_to_selection_structure_tradeoff_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Design(경계 설계)

- hypothesis(가설): Stage225(225단계)에서 long threshold(롱 임계값)가 효과 없었으므로, lowedge guard(저엣지 보호)의 selection structure(선택 구조)를 바꾸면 validation(검증)을 회복할 수 있다.
- comparison_baseline(비교 기준): Stage225(225단계) lowedge OR control(저엣지 또는 대조군), validation net(검증 순손익) `833.22`, OOS net(표본외 순손익) `765.40`.
- control_variables(고정 변수): long threshold(롱 임계값) `0.52`, short threshold(숏 임계값) `0.54`, ATR SL/TP(ATR 손절/익절) `2.0325/4.615`, model risk cap(모델 위험 상한) `0.031375`, lifecycle(생애주기) `hold=3,same_dir_cd=8,reverse=true`.
- changed_variables(변경 변수): long block structure(롱 차단 구조)만 `lowedge_or`, `lowedge_session_only`, `lowedge_margin_only`, `lowedge_and`로 바꾼다.
- stop_condition(정지 조건): 4개 variants(변형)를 validation/OOS(검증/표본외) MT5 Strategy Tester(MetaTrader 5 전략 테스터)로 측정하면 Stage227(227단계)는 닫는다.

## KPI Read(KPI 핵심 성과 지표 판독)

| adapter(어댑터) | structure(구조) | val net(검증 순손익) | early PF(초반 수익요인) | mid PF(중반 수익요인) | val DD%(검증 낙폭) | OOS net(표본외 순손익) | OOS PF(표본외 수익요인) | flags(표식) |
|---|---|---:|---:|---:|---:|---:|---:|---|
| s227_sel_lowedge_or_control | lowedge_or | 833.22 | 1.446826 | 1.498516 | 13.0158 | 765.40 | 1.930000 | validation_net_below_34d;validation_balance_dd_above_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d;validation_late_concentration_above_50pct |
| s227_sel_session_only | lowedge_session_only | 952.16 | 1.563704 | 1.541194 | 12.6953 | 719.48 | 1.740000 | validation_net_below_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d |
| s227_sel_margin_only | lowedge_margin_only | 915.23 | 1.474608 | 1.459179 | 11.7416 | 678.96 | 1.780000 | validation_net_below_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d;validation_late_concentration_above_50pct;oos_net_materially_below_stage171_primary |
| s227_sel_session_and_margin | lowedge_and | 1046.57 | 1.604594 | 1.481867 | 11.5520 | 625.27 | 1.620000 | validation_mid_pf_below_34d;oos_net_materially_below_stage171_primary |

## Judgment(판정)

- result_subject(판정 대상): Stage227 selection structure repair(227단계 선택 구조 수리).
- evidence_available(사용 근거): MT5 Strategy Tester(MetaTrader 5 전략 테스터) validation/OOS(검증/표본외), segment KPI(구간 핵심 성과 지표), monthly KPI(월별 핵심 성과 지표), concentration risk(집중 위험), risk/ATR telemetry(위험/ATR 기록).
- best_row(최선 행): `s227_sel_session_only` with validation net(검증 순손익) `952.16`, mid PF(중반 수익요인) `1.541194`, OOS net(표본외 순손익) `719.48`.
- judgment_label(판정 라벨): `bounded_research_measurement_not_final(경계 연구 측정, 최종 아님)`.
- claim_boundary(주장 경계): research/development only(연구개발 전용).

Stage227(227단계)는 deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료)를 주장하지 않는다.
