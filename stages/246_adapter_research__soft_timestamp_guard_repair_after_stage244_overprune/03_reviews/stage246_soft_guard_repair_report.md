# Stage246 Soft Timestamp Guard Repair Report(246단계 부드러운 시간 보호문 수리 보고서)

- stage(단계): `246_adapter_research__soft_timestamp_guard_repair_after_stage244_overprune`
- run(실행): `run246A_stage246_soft_timestamp_guard_repair_after_stage244_overprune_v1`
- source_stage(원천 단계): `245_adapter_research__stage244_timestamp_guard_followup_review`
- source_stage245_evidence_commit(원천 245단계 근거 커밋): `1481b1323d65bd5974aefc973bc16d9fff74519a`
- source_stage245_hash_record_commit(원천 245단계 해시 기록 커밋): `efa84d56d2c36e619b42a7f7cab09ec4c0ad35a3`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `open_stage247_bounded_followup_due_to_soft_guard_tradeoff_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Design(경계 설계)

- action(행동): hard guard(강한 차단)를 제거하고 middle window(중간 창)의 low/mid bucket(저/중간 구간)에 flat tilt(무포지션 쪽 점수 기울기)를 작게 넣었다.
- effect(효과): 신호를 강제로 없애지 않고 confidence(신뢰도)를 낮춰서 validation net(검증 순손익) 손상을 줄이면서 DD(낙폭)와 mid PF(중간 수익요인)를 다시 본다.
- fixed variables(고정 변수): ATR SL/TP(ATR 손절/익절) `2.0325/4.615`, model-controlled risk%(모델 제어 위험 비율) cap(상한) `0.0305`, hold(보유) `3`, cooldown(대기) `8`.
- stop condition(정지 조건): 5 variants(변형)를 validation/OOS(검증/표본외) MT5 Strategy Tester(MetaTrader 5 전략 테스터)로 측정하면 Stage246(246단계)는 닫는다.

## KPI Read(KPI 핵심 성과 지표 판독)

| adapter(어댑터) | val net(검증 순손익) | early PF(초반 수익요인) | mid PF(중간 수익요인) | val DD%(검증 낙폭) | OOS net(표본외 순손익) | OOS PF(표본외 수익요인) | OOS DD%(표본외 낙폭) | flags(표식) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| s246_cap0305_control | 976.67 | 1.595626 | 1.522877 | 12.9428 | 775.76 | 1.780000 | 9.5076 | validation_net_below_34d;validation_balance_dd_above_34d;validation_mid_pf_below_34d |
| s246_softlow_flat003 | 921.30 | 1.595626 | 1.499805 | 12.2261 | 772.80 | 1.790000 | 9.5137 | validation_pf_below_34d;validation_net_below_34d;validation_mid_pf_below_34d |
| s246_softlow_flat005 | 905.28 | 1.595626 | 1.502614 | 11.6296 | 767.37 | 1.790000 | 9.5307 | validation_pf_below_34d;validation_net_below_34d;validation_mid_pf_below_34d |
| s246_softlowmid_lite | 905.70 | 1.595626 | 1.489841 | 12.0496 | 773.15 | 1.790000 | 9.5594 | validation_pf_below_34d;validation_net_below_34d;validation_mid_pf_below_34d |
| s246_softlowmid_balanced | 897.16 | 1.595626 | 1.499664 | 11.6721 | 765.43 | 1.790000 | 9.5101 | validation_pf_below_34d;validation_net_below_34d;validation_mid_pf_below_34d |

## Judgment(판정)

- best_row(최선 행): `s246_cap0305_control` with validation net(검증 순손익) `976.67`, validation DD(검증 낙폭) `12.9428`, mid PF(중간 수익요인) `1.522877250708345`, OOS net(표본외 순손익) `775.76`.
- legacy_34d_target(레거시 34D 목표): net(순손익) `987.6`, PF(수익요인) `1.583157`, DD%(낙폭) `12.909136`.
- decision(판정): `open_stage247_bounded_followup_due_to_soft_guard_tradeoff_candidate_not_final`.
- overall_goal_complete(전체 목표 완료): `false`.

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준).
