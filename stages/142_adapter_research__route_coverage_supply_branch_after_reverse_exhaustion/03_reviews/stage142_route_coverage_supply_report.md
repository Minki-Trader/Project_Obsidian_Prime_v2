# Stage142 Route Coverage Supply Report(142단계 경로 커버리지 공급 보고서)

- stage(단계): `142_adapter_research__route_coverage_supply_branch_after_reverse_exhaustion`
- run(실행): `run142A_stage142_route_coverage_supply_branch_after_reverse_exhaustion_v1`
- source_stage141(원천 141단계): `141_adapter_research__stage140_reverse_supply_followup_review`
- source_stage140_adapter(원천 140단계 어댑터): `s140_reverse_control_h3_cd5_risk035`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `continue_stage143_route_coverage_repair_after_damage_or_no_gain_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Question(경계 질문)

Can route coverage supply(경로 커버리지 공급) add validation/OOS trades(검증/미래구간 거래) beyond the Stage140 reverse ceiling(140단계 반전 상한) without damaging PF/net/DD(수익 팩터/순손익/손실률), segment KPI(구간 핵심 성과 지표), and risk/ATR telemetry(위험/ATR 원격측정)?

Effect(효과): reverse axis(반전 축)을 더 늘리지 않고, side gate release(방향 게이트 완화)와 no-gate pressure(무게이트 압력)가 거래 수와 품질에 주는 영향을 분리한다.

## Experiment Design(실험 설계)

- hypothesis(가설): short-only route gate(숏 전용 경로 게이트) 또는 tight no-gate(촘촘한 무게이트)가 거래 수를 늘리면서 품질 손상을 제한할 수 있다.
- comparison_baseline(비교 기준): Stage140 control(140단계 대조군) `s140_reverse_control_h3_cd5_risk035` with OOS PF(미래구간 수익 팩터) `1.80`, net(순손익) `1186.30`, DD(손실률) `14.66`, trades(거래 수) `180`.
- changed_variables(변경 변수): route gate block mode(경로 게이트 차단 방식), reverse-on-opposite(반대 신호 반전), threshold(임계값).
- control_variables(고정 변수): v41 source model(원천 모델), ATR bracket(ATR 괄호), model-risk cap(모델 위험 한도) `3.5%`, max hold(최대 보유) `3`, cooldown(대기) `5`.
- stop_condition(중단 조건): 한 stage(단계) 안에서 추가 최적화하지 않고 Stage143(143단계) 검토로 넘긴다.

## KPI Table(KPI 핵심 성과 지표 표)

| adapter(어댑터) | gate(게이트) | reverse(반전) | val PF(검증 수익 팩터) | val net(검증 순손익) | val trades(검증 거래 수) | val late share(검증 후반 비중) | OOS PF(미래구간 수익 팩터) | OOS net(미래구간 순손익) | OOS DD%(미래구간 손실률) | OOS trades(미래구간 거래 수) | gain(증가) |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| s142_control_reverse_bothgate_h3_cd5_risk035 | both | true | 1.580000 | 1388.24 | 265 | 0.664 | 1.800000 | 1186.30 | 14.66 | 180 | 0 |
| s142_route_shortgate_no_reverse_h3_cd5_risk035 | short | false | 1.560000 | 1822.98 | 319 | 0.581 | 1.510000 | 889.34 | 20.23 | 230 | 50 |
| s142_route_shortgate_reverse_h3_cd5_risk035 | short | true | 1.560000 | 1821.00 | 321 | 0.590 | 1.550000 | 963.92 | 20.23 | 231 | 51 |
| s142_route_nogate_tight_no_reverse_h3_cd5_risk035 | none | false | 1.180000 | 747.20 | 462 | 0.496 | 1.210000 | 541.54 | 34.42 | 343 | 163 |

## Best Read(최선 판독)

- best_candidate(최선 후보): `s142_control_reverse_bothgate_h3_cd5_risk035`
- oos_trade_gain_vs_stage140(140단계 대비 미래구간 거래 증가): `0`
- validation_trade_gain_vs_stage140(140단계 대비 검증 거래 증가): `0`
- oos_trade_gap_to_34d(34D 대비 미래구간 거래 수 격차): `-224`
- oos_pf_gap_to_34d(34D 대비 미래구간 수익 팩터 격차): `0.216843`
- oos_net_gap_to_34d(34D 대비 미래구간 순손익 격차): `198.70`
- oos_dd_gap_to_34d(34D 대비 미래구간 손실률 격차): `1.75`
- overall_goal_complete(전체 목표 완료): `false`

## Judgment(판정)

- result_subject(판정 대상): Stage142 route coverage supply branch(142단계 경로 커버리지 공급 분기).
- evidence_available(사용 가능 근거): MT5 runtime reports(MT5 런타임 보고서), summary CSV(요약 CSV), segment KPI(구간 핵심 성과 지표), risk/ATR telemetry(위험/ATR 원격측정), gate feature summary(게이트 피처 요약).
- evidence_missing(부족 근거): Stage143 follow-up review(143단계 후속 검토) 전까지 equity shape(자금곡선 모양), concentration(집중도), route-specific damage attribution(경로별 손상 귀속)은 최종 판정하지 않는다.
- judgment_label(판정 라벨): `route_coverage_supply_measured_not_final`.
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
