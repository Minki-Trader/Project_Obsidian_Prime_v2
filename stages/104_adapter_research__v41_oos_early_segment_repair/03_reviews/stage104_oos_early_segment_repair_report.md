# Stage104 OOS Early Segment Repair Report(104단계 표본외 초반 구간 수리 보고서)

- run(실행): `run104A_stage104_v41_oos_early_segment_repair_v1`
- source_stage(원천 단계): `103_adapter_research__v41_oos_net_density_followup_review`
- source_stage103_closeout_commit(원천 103단계 종료 커밋): `d769c8b22ce389d4261edaf30e0c2c729971874e`
- source_stage103_latest_commit(원천 103단계 최신 커밋): `1f456de5dddadea119c5cb78c2b5d020f403c78d`
- source_stage102_latest_commit(원천 102단계 최신 커밋): `5ca329c468db459a8f68b9c28dd0897dfbf79623`
- source_adapter(원천 어댑터): `s102_v41_h3_cd8_lng_early_adx18`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `continue_oos_early_segment_repair_review_in_stage105`
- boundary(경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Hypothesis(가설)

Stage102 best(102단계 최선)의 full OOS(전체 표본외) 개선은 ADX<18(ADX 18 미만) 완화로 생겼지만, OOS early(표본외 초반)는 악화됐다. ADX<19(ADX 19 미만) 중간값 또는 ADX<20 + cooldown7(ADX 20 미만 + 쿨다운 7) control(대조군)이 초반을 회복하면서 전체 OOS(표본외)를 보존할 수 있다.

Effect(효과): Stage104(104단계)는 새 모델을 찾지 않고, 초반 구간 제한문만 좁게 조정한다.

## Result Table(결과 표)

| adapter(어댑터) | OOS PF(표본외 수익 팩터) | OOS net(표본외 순손익) | OOS DD%(표본외 손실률) | early PF(초반 수익 팩터) | early net(초반 순손익) |
|---|---:|---:|---:|---:|---:|
| s104_v41_h3_cd7_lng_early_adx20 | 1.590000 | 607.95 | 18.69 | 1.128143 | 32.51 |
| s104_v41_h3_cd8_lng_early_adx19 | 1.590000 | 614.67 | 18.69 | 1.128143 | 32.51 |
| s104_v41_h3_cd7_lng_early_adx19 | 1.600000 | 617.74 | 18.69 | 1.029162 | 8.11 |

## Best Balanced Read(균형 최선 판독)

- best_balanced_variant(균형 최선 변형): `s104_v41_h3_cd8_lng_early_adx19`
- oos_pf(표본외 수익 팩터): `1.590000`
- oos_net(표본외 순손익): `614.67`
- oos_dd_pct(표본외 손실률): `18.69`
- early_pf(초반 수익 팩터): `1.128143`
- early_net(초반 순손익): `32.51`
- early_mfe_capture(초반 MFE 포착률): `0.060749`

## Decision(판정)

decision(판정): `continue_oos_early_segment_repair_review_in_stage105`

Stage104(104단계)는 전체 목표 완료가 아니다. Effect(효과): 결과를 Stage105(105단계)에서 후속 검토하고, 34D KPI(34D 핵심 성과 지표) 격차가 남으면 다음 좁은 수리로 넘긴다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
