# Stage120 Post-DD Density Expansion Repair Report(120단계 손실률 압축 뒤 밀도 확장 수리 보고서)

- run(실행): `run120A_stage120_v41_post_dd_density_expansion_repair_v1`
- source_stage(원천 단계): `119_adapter_research__v41_dd_compression_followup_review`
- source_stage119_closeout_commit(원천 119단계 종료 커밋): `83fb1a83b27a60a7953c88259a2655ceec772c42`
- source_stage119_latest_commit(원천 119단계 최신 커밋): `33280e4223984a5d49484a30cee574874e929b16`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `continue_post_dd_density_followup_review_in_stage121_with_density_gain`
- boundary(경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Question(경계 질문)

Stage118/119(118/119단계)에서 확인한 risk cap 0.035(위험 상한 3.5%) DD guardrail(손실률 가드레일)을 유지하면서, trade count(거래 수)를 34D target(34D 목표)에 더 가깝게 늘릴 수 있는가?

Effect(효과): Stage120(120단계)은 새 모델 hunting(모델 탐색)이 아니라 threshold/cooldown(임계값/대기시간)만 좁게 풀어 density(밀도) 회복 가능성을 측정한다.

## Result Table(결과 표)

| adapter(어댑터) | source(원천) | OOS PF(표본외 수익 팩터) | OOS net(표본외 순손익) | OOS DD%(표본외 손실률) | trades(거래 수) | trade gain(거래 증가) | early PF(초반 수익 팩터) |
|---|---|---:|---:|---:|---:|---:|---:|
| s120_v41_h3_cd9_session_margin_risk035_lng51 | s118_v41_h3_cd9_session_margin_risk035_lng52 | 1.830000 | 1195.83 | 14.39 | 174 | 0 | 1.677162 |
| s120_v41_h3_cd8_session_margin_risk035_lng52 | s118_v41_h3_cd8_session_margin_risk035_lng53 | 1.730000 | 1070.61 | 14.75 | 176 | 0 | 1.622275 |
| s120_v41_h3_cd7_session_margin_risk035_lng53 | s118_v41_h3_cd8_session_margin_risk035_lng53 | 1.740000 | 1074.35 | 14.75 | 177 | 1 | 1.622275 |
| s120_v41_h3_cd7_session_margin_risk035_lng52 | s118_v41_h3_cd8_session_margin_risk035_lng53 | 1.740000 | 1074.35 | 14.75 | 177 | 1 | 1.622275 |

## Best Read(최선 판독)

- best_variant(최선 변형): `s120_v41_h3_cd7_session_margin_risk035_lng53`
- oos_pf(표본외 수익 팩터): `1.740000`
- oos_net(표본외 순손익): `1074.35`
- oos_dd_pct(표본외 손실률): `14.75`
- trades(거래 수): `177`
- trade_gain_vs_source(원천 대비 거래 증가): `1`

## Judgment(판정)

- result_subject(판정 대상): Stage120 post-DD density expansion repair(120단계 손실률 압축 뒤 밀도 확장 수리).
- evidence_available(있는 근거): MT5 runtime reports(MT5 실행환경 보고서), summary CSV(요약 CSV), segment KPI(구간 핵심 성과 지표), risk/ATR telemetry(위험/ATR 텔레메트리).
- evidence_missing(부족 근거): Stage121(121단계) 후속 검토 전에는 equity-shape audit(자본 곡선 형태 감사)과 density durability(밀도 지속성)가 아직 부족하다.
- judgment_label(판정 라벨): `post_dd_density_expansion_measured_not_final`.
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
