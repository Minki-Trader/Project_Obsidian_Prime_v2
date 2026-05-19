# Stage242 Selective Midsegment Repair Report(242단계 선택적 중간 구간 수리 보고서)

- stage(단계): `242_adapter_research__selective_midsegment_quality_repair_after_highbonus_tradeoff`
- run(실행): `run242A_stage242_selective_midsegment_quality_repair_after_highbonus_tradeoff_v1`
- source_stage(원천 단계): `241_adapter_research__stage240_highbonus_repair_followup_review`
- source_run(원천 실행): `run241A_stage241_stage240_highbonus_repair_followup_review_v1`
- source_stage241_evidence_commit(원천 241단계 근거 커밋): `d005c4f7dcb4c95c6ac4d6c774205fec8df61d95`
- source_stage241_hash_record_commit(원천 241단계 해시 기록 커밋): `978cccf09d6ddbb684edbfb52e320333093d1ff4`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `open_stage243_bounded_followup_due_to_selective_midsegment_tradeoff_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Design(경계 설계)

- hypothesis(가설): Stage240(240단계)의 전역 risk cap(위험 상한)은 순손익을 너무 깎았다. 중간 기간의 낮은 margin bucket(마진 구간) 신호만 선택적으로 막으면 DD(낙폭)와 mid PF(중간 수익요인)를 고치면서 net/OOS(순손익/표본외)를 보존할 수 있다.
- fixed variables(고정 변수): highbonus(고마진 보너스) `0.10/0.15`, ATR SL/TP(ATR 손절/익절) `2.0325/4.615`, hold(보유) `3`, cooldown(대기) `8`, Stage235 reference side filter(235단계 기준 방향 필터).
- changed variables(변경 변수): middle-window guard(중간 기간 보호문) `none/low/low_mid`, mild cap(완만한 상한) `0.0305` one variant(한 변형).
- stop condition(정지 조건): 4개 variants(변형)를 validation/OOS(검증/표본외) MT5 Strategy Tester(MetaTrader 5 전략 테스터)로 측정하면 Stage242(242단계)는 닫는다.

## KPI Read(KPI 핵심 성과 지표 판독)

| adapter(어댑터) | val net(검증 순손익) | early PF(초반 수익요인) | mid PF(중간 수익요인) | val DD%(검증 낙폭) | OOS net(표본외 순손익) | OOS PF(표본외 수익요인) | OOS DD%(표본외 낙폭) | flags(표식) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| s242_samecap_control | 967.85 | 1.562195 | 1.498473 | 13.3771 | 812.80 | 1.780000 | 9.7920 | validation_pf_below_34d;validation_net_below_34d;validation_balance_dd_above_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d |
| s242_midlow_guard | 967.85 | 1.562195 | 1.498473 | 13.3771 | 812.80 | 1.780000 | 9.7920 | validation_pf_below_34d;validation_net_below_34d;validation_balance_dd_above_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d |
| s242_midlowmid_guard | 967.85 | 1.562195 | 1.498473 | 13.3771 | 812.80 | 1.780000 | 9.7920 | validation_pf_below_34d;validation_net_below_34d;validation_balance_dd_above_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d |
| s242_midlowmid_guard_cap0305 | 976.67 | 1.595626 | 1.522877 | 12.9428 | 775.76 | 1.780000 | 9.5076 | validation_net_below_34d;validation_balance_dd_above_34d;validation_mid_pf_below_34d |

## Validity Boundary(유효성 경계)

- gate_feature_summary(보호문 피처 요약): `stage242_gate_feature_summary.csv` records `mid_window_rows`(중간 창 행 수) `0` and `selective_blocked_signal_rows`(선택 차단 신호 행 수) `0` for every variant(변형).
- cause(원인): Stage242(242단계) parser(파서)는 ISO date(ISO 날짜) 형식을 기대했지만 feature time(피처 시간)은 `YYYY.MM.DD HH:MM:SS` 형식이었다. Effect(효과): middle-window guard(중간 기간 보호문)가 실제로 작동하지 않았다.
- attribution(기여 판정): `s242_midlow_guard`와 `s242_midlowmid_guard`는 사실상 samecap control(동일 상한 대조군)과 같다. `s242_midlowmid_guard_cap0305`의 KPI(핵심 성과 지표) 개선은 active guard(작동 보호문)가 아니라 mild model-risk cap(완만한 모델 위험 상한) `0.0305`에서 온 것으로 본다.
- judgment_boundary(판정 경계): Stage242(242단계)는 failed/inactive guard measurement(실패/비활성 보호문 측정)와 near-miss mild-cap measurement(근접 실패 완만한 상한 측정)로 유효하다. selective midsegment repair(선택적 중간 구간 수리)가 성공했다는 증거로는 유효하지 않다.

## Judgment(판정)

- best_row(최선 행): `s242_midlowmid_guard_cap0305` with validation net(검증 순손익) `976.67`, validation DD(검증 낙폭) `12.9428`, mid PF(중간 수익요인) `1.522877250708345`, OOS net(표본외 순손익) `775.76`.
- quality_read(품질 판독): 34D(34D 기준) 대비 validation net(검증 순손익)은 `-10.93`, validation DD(검증 낙폭)는 `0.033664` percentage point(퍼센트포인트) 높고, mid PF(중간 수익요인)는 여전히 낮다. OOS net(표본외 순손익)은 samecap control(동일 상한 대조군) `812.80`에서 `775.76`으로 줄었다.
- decision(판정): `open_stage243_bounded_followup_due_to_selective_midsegment_tradeoff_candidate_not_final`.
- overall_goal_complete(전체 목표 완료): `false`.

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선).
