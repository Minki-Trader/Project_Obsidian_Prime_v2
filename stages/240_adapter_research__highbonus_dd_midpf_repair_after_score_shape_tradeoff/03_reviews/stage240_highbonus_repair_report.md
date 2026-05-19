# Stage240 Highbonus DD/MidPF Repair Report(240단계 고마진 낙폭/중간 수익요인 수리 보고서)

- stage(단계): `240_adapter_research__highbonus_dd_midpf_repair_after_score_shape_tradeoff`
- run(실행): `run240A_stage240_highbonus_dd_midpf_repair_after_score_shape_tradeoff_v1`
- source_stage(원천 단계): `239_adapter_research__stage238_score_shape_followup_review`
- source_run(원천 실행): `run239A_stage239_stage238_score_shape_followup_review_v1`
- source_stage239_evidence_commit(원천 239단계 근거 커밋): `36307c14a286f112dbb50d88733091a1bb169252`
- source_stage239_hash_record_commit(원천 239단계 해시 기록 커밋): `b9da2e36ade4563a0a96df4371bf27ede732c275`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `open_stage241_bounded_followup_due_to_highbonus_dd_midpf_tradeoff_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Design(경계 설계)

- hypothesis(가설): highbonus(고마진 보너스)는 좋은 net/OOS(순손익/표본외) 단서지만, risk cap(위험 상한)과 score strength(점수 강도)를 낮추면 validation DD(검증 낙폭)와 mid PF(중간 수익요인)가 나아질 수 있다.
- fixed variables(고정 변수): ATR SL/TP(ATR 손절/익절) `2.0325/4.615`, hold(보유) `3`, same-direction cooldown(동방향 대기) `8`, Stage235 reference side filter(235단계 기준 방향 필터).
- changed variables(변경 변수): model_risk_max_pct(모델 위험 최대 비율) `0.031375/0.0275/0.0250758284/0.0290`, high/vhigh bonus(고/초고 마진 보너스) `0.10/0.15` 또는 `0.075/0.1125`.
- stop condition(정지 조건): 4개 variants(변형)를 validation/OOS(검증/표본외) MT5 Strategy Tester(MetaTrader 5 전략 테스터)로 측정하면 Stage240(240단계)은 닫는다.

## KPI Read(KPI 핵심 성과 지표 판독)

| adapter(어댑터) | val net(검증 순손익) | early PF(초반 수익요인) | mid PF(중간 수익요인) | val DD%(검증 낙폭) | OOS net(표본외 순손익) | OOS PF(표본외 수익요인) | OOS DD%(표본외 낙폭) | flags(표식) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| s240_highbonus010_samecap | 967.85 | 1.562195 | 1.498473 | 13.3771 | 812.80 | 1.780000 | 9.7920 | validation_pf_below_34d;validation_net_below_34d;validation_balance_dd_above_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d |
| s240_highbonus010_cap0275 | 804.67 | 1.587249 | 1.497961 | 11.8125 | 672.18 | 1.790000 | 8.5829 | validation_pf_below_34d;validation_net_below_34d;validation_mid_pf_below_34d;oos_net_materially_below_stage171_primary |
| s240_highbonus010_cap0251 | 718.17 | 1.595879 | 1.513290 | 10.7826 | 593.41 | 1.790000 | 7.8028 | validation_net_below_34d;validation_mid_pf_below_34d;oos_net_materially_below_stage171_primary |
| s240_highbonus0075_cap0290 | 875.39 | 1.580069 | 1.523627 | 12.3042 | 704.16 | 1.770000 | 8.8714 | validation_net_below_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d;oos_net_materially_below_stage171_primary |

## Judgment(판정)

- best_row(최선 행): `s240_highbonus010_samecap` with validation net(검증 순손익) `967.85`, validation DD(검증 낙폭) `13.3771`, mid PF(중간 수익요인) `1.4984730779533884`, OOS net(표본외 순손익) `812.8`.
- decision(판정): `open_stage241_bounded_followup_due_to_highbonus_dd_midpf_tradeoff_candidate_not_final`.
- overall_goal_complete(전체 목표 완료): `false`.

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선).
