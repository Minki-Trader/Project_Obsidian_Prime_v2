# Stage223 OOS Recovery Report(223단계 표본외 회복 보고서)

- stage(단계): `223_adapter_research__oos_recovery_after_no_long_block_validation_gain`
- run(실행): `run223A_stage223_oos_recovery_after_no_long_block_validation_gain_v1`
- source_stage(원천 단계): `222_adapter_research__stage221_entry_signal_gate_followup_review`
- source_run(원천 실행): `run222A_stage222_stage221_entry_signal_gate_followup_review_v1`
- source_stage222_evidence_commit(원천 222단계 근거 커밋): `17d3cb4ef4f45decd8efa11baddf6253336a19cb`
- source_stage222_hash_record_commit(원천 222단계 해시 기록 커밋): `17098466e85db987a1bf9cefc35a6d9ec9009d43`
- source_clue(원천 단서): `s221_gate_no_long_block`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `open_stage224_bounded_followup_due_to_oos_recovery_tradeoff_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Design(경계 설계)

- hypothesis(가설): Stage221(221단계)의 no_long_block(롱 차단 제거)이 validation gain(검증 개선)을 만들었지만 OOS net(표본외 순손익)을 손상했다면, 약한 long guard(롱 보호)를 되돌려 OOS(표본외)와 mid PF(중반 수익요인)를 회복할 수 있다.
- comparison_baseline(비교 기준): `s221_gate_no_long_block` 단서와 Stage219 control(219단계 대조군) OOS net(표본외 순손익) `719.48`.
- control_variables(고정 변수): ATR SL/TP(ATR 손절/익절) `2.0325/4.615`, model risk cap(모델 위험 상한) `0.031375`, lifecycle(생애주기) `hold=3,same_dir_cd=8,reverse=true`, thresholds(문턱값) `short=0.54,long=0.52`.
- changed_variables(변경 변수): long block rule(롱 차단 규칙)만 `none`, `session_only_p10`, `session_only_p5`, `lowedge_gate`로 비교한다.
- stop_condition(정지 조건): 4개 variants(변형)를 validation/OOS(검증/표본외) MT5 Strategy Tester(MetaTrader 5 전략 테스터)로 측정하면 Stage223(223단계)는 닫는다.

## KPI Read(KPI 핵심 성과 지표 판독)

| adapter(어댑터) | gate(게이트) | val net(검증 순손익) | early PF(초반 수익요인) | mid PF(중반 수익요인) | val DD%(검증 낙폭) | OOS net(표본외 순손익) | flags(표식) |
|---|---|---:|---:|---:|---:|---:|---|
| s223_oos_control_no_long | control_no_long(대조군 롱 차단 없음) | 1050.87 | 1.604594 | 1.484282 | 11.6030 | 626.79 | validation_mid_pf_below_34d;oos_net_materially_below_stage171_primary |
| s223_oos_tight_long_guard | tight_long_guard(좁은 롱 보호) | 952.16 | 1.563704 | 1.541194 | 12.6953 | 719.48 | validation_net_below_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d |
| s223_oos_wide_long_guard | wide_long_guard(넓은 롱 보호) | 875.89 | 1.516356 | 1.495635 | 12.2033 | 640.04 | validation_net_below_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d;oos_net_materially_below_stage171_primary |
| s223_oos_lowedge_long_guard | lowedge_long_guard(저엣지 롱 보호) | 833.22 | 1.446826 | 1.498516 | 13.0158 | 765.40 | validation_net_below_34d;validation_balance_dd_above_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d;validation_late_concentration_above_50pct |

## Judgment(판정)

- result_subject(판정 대상): Stage223 long guard OOS recovery(223단계 롱 보호 표본외 회복).
- evidence_available(사용 근거): MT5 Strategy Tester(MetaTrader 5 전략 테스터) validation/OOS(검증/표본외), segment KPI(구간 핵심 성과 지표), monthly KPI(월별 핵심 성과 지표), concentration risk(집중 위험), risk/ATR telemetry(위험/ATR 기록).
- best_row(최선 행): `s223_oos_tight_long_guard` with validation net(검증 순손익) `952.16`, mid PF(중반 수익요인) `1.541194`, OOS net(표본외 순손익) `719.48`.
- judgment_label(판정 라벨): `bounded_research_measurement_not_final(경계 연구 측정, 최종 아님)`.
- claim_boundary(주장 경계): research/development only(연구개발 전용).

Stage223(223단계)는 deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료)를 주장하지 않는다.
