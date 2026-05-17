# Stage108 DD Control After Net/Early Recovery Repair Report(108단계 손실률 제어 후속 수리 보고서)

- run(실행): `run108A_stage108_v41_dd_control_after_net_early_recovery_repair_v1`
- source_stage(원천 단계): `107_adapter_research__v41_oos_net_density_dd_followup_review`
- source_stage107_closeout_commit(원천 107단계 종료 커밋): `6af2f17a497baacff8f1ad4089c97a36bad95398`
- source_stage107_latest_commit(원천 107단계 최신 커밋): `728d4cba5b3361ba5eaf49561ea8b2d2282b6343`
- source_stage106_latest_commit(원천 106단계 최신 커밋): `0e34739b13eaf7d8c7d9bfb48bf168396122d17a`
- source_adapter(원천 어댑터): `s106_v41_h3_cd9_lng_early_adx19`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `continue_dd_control_repair_review_in_stage109`
- boundary(경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Hypothesis(가설)

Stage106(106단계)의 `h3_cd9`는 OOS net/PF/early(표본외 순손익/수익 팩터/초반)를 보존했지만 DD(손실률)는 `18.69`로 남았다. `h4_cd8`는 DD(손실률)를 `16.06`까지 낮췄지만 PF/net(수익 팩터/순손익)을 훼손했다.

Effect(효과): Stage108(108단계)은 새 모델 탐색(model hunting, 모델 탐색)이 아니라 `hold 4(보유 4봉)`와 `cooldown 9/10(쿨다운 9/10봉)`만 좁게 조합한다.

## Result Table(결과 표)

| adapter(어댑터) | OOS PF(표본외 수익 팩터) | OOS net(표본외 순손익) | OOS DD%(표본외 손실률) | trades(거래 수) | early PF(초반 수익 팩터) | early net(초반 순손익) | early ok(초반 통과) |
|---|---:|---:|---:|---:|---:|---:|---|
| s108_v41_h4_cd9_lng_early_adx19 | 1.550000 | 615.72 | 16.06 | 147 | 1.198059 | 57.13 | yes |
| s108_v41_h4_cd10_lng_early_adx19 | 1.560000 | 575.36 | 16.02 | 144 | 1.127002 | 36.24 | no |
| s108_v41_h3_cd10_lng_early_adx19 | 1.640000 | 644.76 | 18.69 | 147 | 1.157012 | 38.84 | yes |

## Best Balanced Read(균형 최선 판독)

- best_balanced_variant(균형 최선 변형): `s108_v41_h3_cd10_lng_early_adx19`
- oos_pf(표본외 수익 팩터): `1.640000`
- oos_net(표본외 순손익): `644.76`
- oos_dd_pct(표본외 손실률): `18.69`
- early_pf(초반 수익 팩터): `1.157012`
- early_net(초반 순손익): `38.84`
- stage106_net_gap(106단계 순손익 최선 대비): `0.00`
- stage106_dd_gap(106단계 손실률 최선 대비): `2.63`
- early_floor_preserved(초반 바닥 보존): `yes`

## Result Judgment(결과 판정)

- result_subject(판정 대상): Stage108 DD control after net/early recovery repair(108단계 손실률 제어 후속 수리).
- evidence_available(있는 근거): MT5 runtime reports(실행환경 보고서), summary CSV(요약 CSV), segment KPI(구간 핵심 성과 지표), risk/ATR telemetry(위험/ATR 텔레메트리).
- evidence_missing(빠진 근거): 34D KPI(34D 핵심 성과 지표) 수준의 net/DD/trade density(순손익/손실률/거래 밀도) 동시 충족.
- judgment_label(판정 라벨): `exploratory_repair_continues`.
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`.
- next_condition(다음 조건): `continue_dd_control_repair_review_in_stage109`.

## Decision(판정)

decision(판정): `continue_dd_control_repair_review_in_stage109`

Stage108(108단계)는 전체 목표 완료가 아니다. Effect(효과): 결과는 Stage109(109단계)에서 후속 검토하고, 부족하면 다음 bounded repair(경계 수리)로 넘긴다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
