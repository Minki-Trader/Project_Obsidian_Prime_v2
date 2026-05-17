# Stage106 OOS Net Density/DD After Early Recovery Repair Report(106단계 표본외 순손익 밀도/손실률 초반 회복 후 수리 보고서)

- run(실행): `run106A_stage106_v41_oos_net_density_dd_after_early_recovery_repair_v1`
- source_stage(원천 단계): `105_adapter_research__v41_oos_early_segment_followup_review`
- source_stage105_closeout_commit(원천 105단계 종료 커밋): `10ea0d39ab4063ab9b192b99539183c6bb8ce385`
- source_stage105_latest_commit(원천 105단계 최신 커밋): `865027a04dba01702276876d9cec8c70c8ac5356`
- source_stage104_latest_commit(원천 104단계 최신 커밋): `61778183dc73e327b612f58b70491a2f14408de2`
- source_adapter(원천 어댑터): `s104_v41_h3_cd8_lng_early_adx19`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `continue_oos_net_density_dd_followup_review_in_stage107`
- boundary(경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Hypothesis(가설)

Stage104 balanced candidate(104단계 균형 후보)는 OOS early(표본외 초반)를 회복했지만 full OOS net(전체 표본외 순손익)이 Stage102 best(102단계 최선)보다 낮다. ADX 18.5(ADX 18.5) midpoint(중간값), max hold 4(최대 보유 4봉), cooldown 9(쿨다운 9봉) 중 하나가 early floor(초반 바닥)를 보존하면서 net density/DD(순손익 밀도/손실률)를 개선할 수 있다.

Effect(효과): Stage106(106단계)은 모델을 새로 찾지 않고, Stage104(104단계)의 회복 조건을 보존한 좁은 수리만 실행한다.

## Result Table(결과 표)

| adapter(어댑터) | OOS PF(표본외 수익 팩터) | OOS net(표본외 순손익) | OOS DD%(표본외 손실률) | early PF(초반 수익 팩터) | early net(초반 순손익) | early ok(초반 통과) |
|---|---:|---:|---:|---:|---:|---|
| s106_v41_h3_cd8_lng_early_adx185 | 1.590000 | 614.67 | 18.69 | 1.128143 | 32.51 | yes |
| s106_v41_h4_cd8_lng_early_adx19 | 1.550000 | 615.72 | 16.06 | 1.198059 | 57.13 | yes |
| s106_v41_h3_cd9_lng_early_adx19 | 1.640000 | 644.76 | 18.69 | 1.157012 | 38.84 | yes |

## Best Balanced Read(균형 최선 판독)

- best_balanced_variant(균형 최선 변형): `s106_v41_h3_cd9_lng_early_adx19`
- oos_pf(표본외 수익 팩터): `1.640000`
- oos_net(표본외 순손익): `644.76`
- oos_dd_pct(표본외 손실률): `18.69`
- early_pf(초반 수익 팩터): `1.157012`
- early_net(초반 순손익): `38.84`
- early_floor_preserved(초반 바닥 보존): `yes`

## Decision(판정)

decision(판정): `continue_oos_net_density_dd_followup_review_in_stage107`

Stage106(106단계)는 전체 목표 완료가 아니다. Effect(효과): 결과를 Stage107(107단계)에서 후속 검토하고, 34D KPI(34D 핵심 성과 지표) 격차가 남으면 다음 좁은 수리로 넘긴다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
