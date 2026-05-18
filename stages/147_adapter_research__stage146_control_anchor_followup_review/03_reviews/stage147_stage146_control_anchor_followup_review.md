# Stage147 Stage146 Control Anchor Follow-up Review(147단계 146단계 대조군 앵커 후속 검토)

- stage(단계): `147_adapter_research__stage146_control_anchor_followup_review`
- run(실행): `run147A_stage147_stage146_control_anchor_followup_review_v1`
- source_stage(원천 단계): `146_adapter_research__control_anchor_trade_supply_after_shortgate_no_repair`
- source_stage146_closeout_commit(원천 146단계 종료 커밋): `d17bc202a1cb49df164cd0e70a8445dd2f9694e2`
- source_stage146_hash_record_commit(원천 146단계 해시 기록 커밋): `f63827bc249653329b99494eca2b17f0926af7cd`
- external_verification_status(외부 검증 상태): `completed_existing_stage146_mt5_runtime_evidence_reviewed`
- decision(판정): `open_stage148_softsession_supply_quality_repair_after_stage146_damage_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Question(경계 질문)

Did Stage146(146단계) increase trade count(거래 수)를 without damaging PF/net/DD(수익 팩터/순손익/손실률), segment KPI(구간 핵심 성과 지표), risk/ATR telemetry(위험/ATR 기록), and concentration(집중도)?

Effect(효과): Stage146(146단계) 안에서 계속 고치지 않고, 결과 판독만 분리해 다음 수리 축을 좁게 고른다.

## KPI Read(KPI 핵심 성과 지표 판독)

| adapter(어댑터) | val PF(검증 수익 팩터) | val net(검증 순손익) | val DD%(검증 손실률) | OOS PF(표본외 수익 팩터) | OOS net(표본외 순손익) | OOS DD%(표본외 손실률) | OOS trades(표본외 거래 수) | gain(증가) | mid PF(중반 수익 팩터) | read(판독) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| s146_control_bothgate_ease_h3_cd5_sht53_lng51_risk035 | 1.580000 | 1388.24 | 11.85 | 1.800000 | 1186.30 | 14.66 | 180 | 0 | 1.985169 | quality_preserved_but_no_trade_supply_gain |
| s146_control_bothgate_hold4_h4_cd5_sht54_lng52_risk035 | 1.530000 | 1253.83 | 15.51 | 1.830000 | 1257.02 | 15.03 | 178 | -2 | 1.746135 | hold_extension_kept_oos_quality_but_cut_trades_and_damaged_validation |
| s146_control_bothgate_replay_h3_cd5_sht54_lng52_risk035 | 1.580000 | 1388.24 | 11.85 | 1.800000 | 1186.30 | 14.66 | 180 | 0 | 1.985169 | quality_preserved_but_no_trade_supply_gain |
| s146_control_bothgate_softsession_h3_cd5_sht54_lng52_risk035 | 1.430000 | 1052.35 | 13.31 | 1.610000 | 1142.79 | 9.67 | 215 | 35 | 1.408466 | trade_supply_gain_with_validation_pf_and_oos_mid_damage |

## Judgment(판정)

- answer(답): `no`
- usable_supply_seed(사용 가능한 거래 공급 씨앗): `s146_control_bothgate_softsession_h3_cd5_sht54_lng52_risk035`
- seed_oos_trades(씨앗 표본외 거래 수): `215`
- seed_oos_trade_gain_vs_control(대조군 대비 표본외 거래 증가): `35`
- seed_oos_pf(씨앗 표본외 수익 팩터): `1.610000`
- seed_validation_pf(씨앗 검증 수익 팩터): `1.430000`
- failure_read(실패 판독): softsession(소프트 세션)은 표본외 거래 수를 180에서 215로 늘렸지만 validation PF(검증 수익 팩터)가 1.43으로 손상됐고 OOS mid PF(표본외 중반 수익 팩터)가 1.408로 약하다.
- control_read(대조군 판독): replay/ease(재현/완화)는 품질은 보존했지만 표본외 거래 수가 180으로 늘지 않았다.
- hold_read(보유 판독): hold4(4봉 보유)는 표본외 PF/net(수익 팩터/순손익)은 좋지만 거래 수가 178로 줄고 validation PF/DD(검증 수익 팩터/손실률)가 손상됐다.
- decision_use(판정 용도): Stage148(148단계)은 softsession(소프트 세션) 거래 공급 증가분만 repair seed(수리 씨앗)로 쓰고, validation guard(검증 보호문)와 OOS mid filter(표본외 중반 필터)를 좁게 시험한다.
- overall_goal_complete(전체 목표 완료): `false`

## Performance Attribution(성과 귀속)

- observed_change(관찰 변화): weak-session block(약한 세션 차단)을 좁히면 거래 수는 늘지만 약한 validation/mid segment(검증/중반 구간) 거래도 같이 들어왔다.
- likely_drivers(가능 원인): session block width(세션 차단 폭), et40 mid margin block(et40 중간 마진 차단), both-side gate(양방향 게이트), unchanged threshold(유지된 임계값).
- risk_read(위험 판독): risk floor(최소 로트 위험 바닥)는 Stage146 표본외 실제 라우팅에서 0으로, 현재 실패 원인은 위험 바닥보다 진입 품질 쪽이다.
- next_probe(다음 확인): `148_adapter_research__softsession_supply_quality_repair_after_stage146_damage`.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
