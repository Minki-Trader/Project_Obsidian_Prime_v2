# Stage169 Net/Density Lift With PF Preservation Report(169단계 순손익/밀도 상승과 수익요인 보존 보고)

- stage(단계): `169_adapter_research__net_density_lift_pf_preservation`
- run(실행): `run169A_stage169_net_density_lift_pf_preservation_v1`
- source_stage(원천 단계): `168_adapter_research__stage167_validation_pf_followup_review`
- source_stage168_closeout_commit(원천 168단계 종료 커밋): `9d72168e7748ba32c549cf36aebe2230ab1ca47d`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `open_stage170_net_density_followup_review_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Experiment Design(실험 설계)

- hypothesis(가설): Stage167(167단계) `short_pre_guard(숏 사전구간 보호)` 축에서 risk cap(위험 상한) 또는 long low-edge restore(롱 낮은 엣지 복원)를 쓰면 net/density(순손익/밀도)를 올리면서 PF(수익요인)를 보존할 수 있다.
- comparison_baseline(비교 기준): `s167_short_pre_guard_risk0250_h3_cd5_sht54_lng52` validation net(검증 순손익) `623.27`, OOS net(표본외 순손익) `520.84`, validation PF(검증 수익요인) `1.63`.
- control_variables(고정 변수): entry thresholds(진입 문턱값), ATR bracket(ATR 브래킷), hold bars(보유 봉), cooldown(쿨다운), short pre guard(숏 사전구간 보호).
- changed_variables(변경 변수): model risk cap(모델 위험 상한) and optional long low-edge restore(선택 롱 낮은 엣지 복원).
- success_criteria(성공 기준): net(순손익)이 Stage167 primary(167단계 주축)보다 오르고, validation/OOS PF(검증/표본외 수익요인), OOS DD(표본외 낙폭), OOS early(표본외 초반), density(밀도)가 훼손되지 않는다.

## KPI Read(KPI 판독)

| adapter(어댑터) | risk(위험) | val PF(검증 수익요인) | val net(검증 순손익) | OOS PF(표본외 수익요인) | OOS net(표본외 순손익) | OOS DD%(표본외 낙폭) | flags(플래그) |
|---|---:|---:|---:|---:|---:|---:|---|
| s169_short_pre_risk0300_h3_cd5_sht54_lng52 | 0.0300 | 1.610000 | 777.28 | 1.830000 | 667.99 | 9.56 | candidate_quality_pass_review_required |
| s169_short_pre_risk0350_h3_cd5_sht54_lng52 | 0.0350 | 1.610000 | 983.96 | 1.820000 | 835.78 | 11.03 | candidate_quality_pass_review_required |
| s169_short_pre_restore_long_risk0300_h3_cd5_sht54_lng52 | 0.0300 | 1.590000 | 950.69 | 1.580000 | 568.58 | 13.14 | oos_pf_below_34d;oos_dd_above_34d |

## Judgment(판정)

Stage169(169단계)는 net/density lift(순손익/밀도 상승)를 좁게 본다. Effect(효과): 좋은 결과가 나와도 final adapter(최종 어댑터)나 deployment(배포)가 아니며, Stage170(170단계) follow-up review(후속 검토)로 넘긴다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
