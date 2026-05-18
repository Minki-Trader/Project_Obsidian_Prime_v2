# Stage196 Bctl DD Compression Mid PF Guard Report(196단계 bctl 낙폭 압축 중반 수익요인 방어 보고서)

- stage(단계): `196_adapter_research__bctl_dd_compression_midpf_guard`
- run(실행): `run196A_stage196_bctl_dd_compression_midpf_guard_v1`
- source_stage(원천 단계): `195_adapter_research__stage194_late_midpf_followup_review`
- source_run(원천 실행): `run195A_stage195_stage194_late_midpf_followup_review_v1`
- source_adapter(원천 어댑터): `s194_bctl_tp475_r0330`
- source_stage195_evidence_commit(원천 195단계 근거 커밋): `49d737c7496df93f9afac7846638ee5dc4a8dc77`
- source_stage195_hash_record_commit(원천 195단계 해시 기록 커밋): `94fb19d520bcabf8ac00bb1154ad12cc903f3689`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `open_stage197_bounded_followup_due_to_bctl_dd_midpf_tradeoff_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Design(경계 설계)

- bounded_question(경계 질문): Stage194(194단계)의 `s194_bctl_tp475_r0330` 순손익/PF/OOS/후반 비중 장점을 보존하면서 validation DD(검증 낙폭)를 34D(34D) 아래로 압축하고 mid PF(중반 수익요인)를 방어할 수 있는가?
- action(행동): bctl context gate(문맥 재균형 게이트)는 유지하고 risk cap(위험 상한) `0.0330`, `0.0325`, `0.0320`과 same-direction cooldown(동방향 재진입 대기) `8` 보조만 시험했다.
- effect(효과): risk-only increase(위험만 상향) 없이 Stage194(194단계)의 가장 좋은 단서에서 DD/mid PF(낙폭/중반 수익요인) 상충만 좁게 분리한다.
- stop_condition(정지 조건): 네 개 bounded variants(경계 변형)를 MT5 Strategy Tester(메타트레이더5 전략 테스터)로 validation/OOS(검증/표본외) 측정하면 Stage196(196단계)를 닫고 Stage197(197단계) review(검토)로 넘긴다.

## KPI Read(KPI 핵심 성과 지표 판독)

| adapter(어댑터) | axis(축) | risk cap(위험 상한) | hold/cd(보유/대기) | val PF(검증 수익요인) | val net(검증 순손익) | val DD%(검증 낙폭) | mid PF(중반 수익요인) | late share(후반 비중) | OOS PF(표본외 수익요인) | flags(표식) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| s196_bctl_ref_r0330 | bctl_ref_r0330 | 0.0330 | 3/5 | 1.730000 | 1161.27 | 13.4559 | 1.525141 | 0.4887 | 1.950000 | validation_balance_dd_above_34d;validation_mid_pf_below_34d |
| s196_bctl_r0325 | bctl_r0325 | 0.0325 | 3/5 | 1.720000 | 1106.65 | 13.4119 | 1.523109 | 0.4888 | 1.950000 | validation_balance_dd_above_34d;validation_mid_pf_below_34d |
| s196_bctl_r0320 | bctl_r0320 | 0.0320 | 3/5 | 1.720000 | 1075.56 | 13.1897 | 1.510656 | 0.4869 | 1.940000 | validation_balance_dd_above_34d;validation_mid_pf_below_34d |
| s196_bctl_cd8_r0325 | bctl_cd8_r0325 | 0.0325 | 3/8 | 1.740000 | 1124.48 | 13.2744 | 1.537676 | 0.4981 | 1.930000 | validation_balance_dd_above_34d;validation_mid_pf_below_34d |

## Attribution(성과 귀속)

- observed_change(관측 변화): best adapter(최선 어댑터) `s196_bctl_cd8_r0325`는 validation net(검증 순손익) `1124.48`, validation DD(검증 낙폭) `13.2744`, mid PF(중반 수익요인) `1.537676`, late share(후반 비중) `0.4981`를 기록했다.
- comparison_baseline(비교 기준): Stage196 reference(196단계 참조) `s196_bctl_ref_r0330`는 validation net(검증 순손익) `1161.27`, validation DD(검증 낙폭) `13.4559`, mid PF(중반 수익요인) `1.525141`, late share(후반 비중) `0.4887`다.
- likely_drivers(가능 원인): bctl context rebalance(문맥 재균형)를 고정한 상태에서 risk cap compression(위험 상한 압축)과 cooldown widening(대기 확대)이 net/DD/PF(순손익/낙폭/수익요인)를 어떻게 움직였는지 quality matrix(품질 행렬)와 segment KPI(구간 핵심 성과 지표)로 본다.
- segment_checks(구간 확인): validation/OOS(검증/표본외), chronological thirds(시간 3분할), balance drawdown(잔고 낙폭), monthly KPI(월별 핵심 성과 지표), concentration(집중도), risk/ATR telemetry(위험/ATR 기록)를 기록했다.
- trade_shape(거래 모양): trade count(거래 수), PF(수익요인), expectancy(기대값), MFE/MAE(최대유리/최대불리), lot/risk telemetry(랏/위험 기록)는 CSV 산출물에 남겼다.
- alternative_explanations(대체 설명): 한두 구간의 시장 체제 차이, late-period profit cluster(후반 수익 군집), threshold non-binding(문턱값 비구속) 잔재가 KPI(핵심 성과 지표)를 설명할 수 있다.
- attribution_confidence(귀속 신뢰도): `medium_until_stage197_review`다. Effect(효과): 이번 단계는 실행 측정이고, Stage197(197단계)가 판독만 분리해서 과장 판단을 막는다.
- next_probe(다음 탐침): Stage197(197단계)에서 DD(낙폭), mid PF(중반 수익요인), late share(후반 비중), OOS(표본외) 손상을 함께 판정한다.

## Judgment(판정)

Stage196(196단계)는 research/development only(연구개발 전용)다. Effect(효과): 결과가 좋아도 deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료)를 만들지 않는다.
