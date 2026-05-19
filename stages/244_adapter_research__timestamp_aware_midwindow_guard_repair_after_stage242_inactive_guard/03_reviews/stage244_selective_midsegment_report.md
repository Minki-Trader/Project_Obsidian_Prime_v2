# Stage244 Selective Midsegment Repair Report(244단계 선택적 중간 구간 수리 보고서)

- stage(단계): `244_adapter_research__timestamp_aware_midwindow_guard_repair_after_stage242_inactive_guard`
- run(실행): `run244A_stage244_timestamp_aware_midwindow_guard_repair_after_stage242_inactive_guard_v1`
- source_stage(원천 단계): `243_adapter_research__stage242_selective_midsegment_followup_review`
- source_run(원천 실행): `run243A_stage243_stage242_selective_midsegment_followup_review_v1`
- source_stage243_evidence_commit(원천 243단계 근거 커밋): `4b7c3394df8525180d4df401973cd8c61d8262e3`
- source_stage243_hash_record_commit(원천 243단계 해시 기록 커밋): `156c5a743b379a90e79f4ec99ee97b75581f6257`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `open_stage245_bounded_followup_due_to_timestamp_guard_tradeoff_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Design(경계 설계)

- hypothesis(가설): Stage240(240단계)의 전역 risk cap(위험 상한)은 순손익을 너무 깎았다. 중간 기간의 낮은 margin bucket(마진 구간) 신호만 선택적으로 막으면 DD(낙폭)와 mid PF(중간 수익요인)를 고치면서 net/OOS(순손익/표본외)를 보존할 수 있다.
- fixed variables(고정 변수): highbonus(고마진 보너스) `0.10/0.15`, ATR SL/TP(ATR 손절/익절) `2.0325/4.615`, hold(보유) `3`, cooldown(대기) `8`, Stage235 reference side filter(235단계 기준 방향 필터).
- changed variables(변경 변수): middle-window guard(중간 기간 보호문) `none/low/low_mid`, mild cap(완만한 상한) `0.0305` one variant(한 변형).
- stop condition(정지 조건): 5개 variants(변형)를 validation/OOS(검증/표본외) MT5 Strategy Tester(MetaTrader 5 전략 테스터)로 측정하면 Stage244(244단계)는 닫는다.

## KPI Read(KPI 핵심 성과 지표 판독)

| adapter(어댑터) | val net(검증 순손익) | early PF(초반 수익요인) | mid PF(중간 수익요인) | val DD%(검증 낙폭) | OOS net(표본외 순손익) | OOS PF(표본외 수익요인) | OOS DD%(표본외 낙폭) | flags(표식) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| s244_samecap_control | 967.85 | 1.562195 | 1.498473 | 13.3771 | 812.80 | 1.780000 | 9.7920 | validation_pf_below_34d;validation_net_below_34d;validation_balance_dd_above_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d |
| s244_midlow_guard | 526.85 | 1.712131 | 1.148244 | 8.7440 | 708.12 | 1.890000 | 9.8007 | validation_pf_below_34d;validation_net_below_34d;validation_mid_pf_below_34d;validation_late_concentration_above_50pct;oos_net_materially_below_stage171_primary |
| s244_midlowmid_guard | 453.46 | 1.895803 | 1.019201 | 11.7633 | 695.64 | 1.900000 | 9.8336 | validation_pf_below_34d;validation_net_below_34d;validation_mid_pf_below_34d;validation_late_concentration_above_50pct;oos_net_materially_below_stage171_primary |
| s244_cap0305_control | 976.67 | 1.595626 | 1.522877 | 12.9428 | 775.76 | 1.780000 | 9.5076 | validation_net_below_34d;validation_balance_dd_above_34d;validation_mid_pf_below_34d |
| s244_midlowmid_guard_cap0305 | 454.48 | 1.944235 | 1.027011 | 10.3027 | 680.50 | 1.920000 | 9.4742 | validation_pf_below_34d;validation_net_below_34d;validation_mid_pf_below_34d;validation_late_concentration_above_50pct;oos_net_materially_below_stage171_primary |

## Judgment(판정)

- best_row(최선 행): `s244_cap0305_control` with validation net(검증 순손익) `976.67`, validation DD(검증 낙폭) `12.9428`, mid PF(중간 수익요인) `1.522877250708345`, OOS net(표본외 순손익) `775.76`.
- decision(판정): `open_stage245_bounded_followup_due_to_timestamp_guard_tradeoff_candidate_not_final`.
- overall_goal_complete(전체 목표 완료): `false`.

## Validity Boundary And Failure Memory(유효성 경계와 실패 기억)

- timestamp_parser_repair(시간 파서 수리): Stage244(244단계)는 `YYYY.MM.DD HH:MM:SS` 형식을 읽어 middle-window guard(중간 창 보호문)를 실제로 작동시켰다.
- activation_evidence(작동 근거): `s244_midlow_guard` blocked(차단) `73` validation(검증) signals(신호) and `40` OOS(표본외) signals(신호); `s244_midlowmid_guard` blocked(차단) `87` validation(검증) signals(신호) and `46` OOS(표본외) signals(신호).
- damage_observed(손상 관찰): active guard(작동 보호문)는 DD(낙폭)를 일부 낮췄지만 validation net(검증 순손익)과 mid PF(중간 수익요인)를 크게 훼손했다.
- cap_control_boundary(상한 대조 경계): `s244_cap0305_control` remains(남음) the best near-miss(근접 실패), but it is still below 34D(34D 기준) on validation net(검증 순손익), validation DD(검증 낙폭), and mid PF(중간 수익요인).
- claim_boundary(주장 경계): Stage244(244단계)는 research/development(연구개발) evidence(근거) only(전용)이고 final adapter(최종 어댑터), deployment(배포), live readiness(실거래 준비), runtime authority(런타임 권위), production baseline(생산 기준선)이 아니다.

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선).
