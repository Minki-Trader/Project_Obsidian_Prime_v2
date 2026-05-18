# Stage167 Validation PF Lift With Density Preservation Report(167단계 검증 수익요인 상승과 밀도 보존 보고)

- stage(단계): `167_adapter_research__validation_pf_lift_density_preservation`
- run(실행): `run167A_stage167_validation_pf_lift_density_preservation_v1`
- source_stage(원천 단계): `166_adapter_research__stage165_side_context_followup_review`
- source_stage166_closeout_commit(원천 166단계 종료 커밋): `905da4d9c24ee4122db3dc93727d70caab3a0b89`
- source_stage166_hash_record_commit(원천 166단계 해시 기록 커밋): `dd96a0b0153d84464300480d6d25acbfa9e4196b`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `open_stage168_validation_pf_followup_review_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Experiment Design(실험 설계)

- hypothesis(가설): Stage165(165단계) primary shortgate low-edge route(주 숏게이트 낮은 엣지 경로)에서 short-side block(숏 방향 차단)을 조금 넓히면 validation PF(검증 수익요인)를 34D 위로 올릴 수 있다.
- decision_use(판정 사용처): Stage168(168단계)에서 이 축을 계속 수리할지, 다른 bounded repair(경계 수리)로 넘길지 결정한다.
- comparison_baseline(비교 기준): `s165_shortgate_long_lowedge_risk0250_h3_cd5_sht54_lng52` with validation PF(검증 수익요인) `1.55`, OOS PF(표본외 수익요인) `1.86`, OOS net(표본외 순손익) `566.88`.
- control_variables(고정 변수): ATR bracket(ATR 브래킷), model risk cap(모델 위험 상한) 2.5%, hold bars(보유 봉) 3, cooldown(쿨다운) 5, thresholds(문턱값) short 0.54 / long 0.52.
- changed_variables(변경 변수): short-side context block rule(숏 방향 문맥 차단 규칙) only.
- success_criteria(성공 기준): validation PF(검증 수익요인) >= 34D, OOS PF(표본외 수익요인) >= 34D, OOS DD(표본외 낙폭) <= 34D, OOS early(표본외 초반) positive(양호), and density(밀도) not thin versus Stage165 primary.
- failure_criteria(실패 기준): validation PF(검증 수익요인)가 여전히 낮거나, OOS/density(표본외/밀도)가 손상된다.
- invalid_conditions(무효 조건): MT5(MetaTrader 5, 메타트레이더5) 외부 검증 실패, telemetry(기록) 누락, required ledgers(필수 장부) 누락.

## KPI Read(KPI 판독)

| adapter(어댑터) | axis(축) | val PF(검증 수익요인) | val net(검증 순손익) | val trades(검증 거래) | OOS PF(표본외 수익요인) | OOS net(표본외 순손익) | OOS DD%(표본외 낙폭) | OOS early PF(표본외 초반 수익요인) | flags(플래그) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| s167_short_pre_guard_risk0250_h3_cd5_sht54_lng52 | short_pre_guard | 1.630000 | 623.27 | 243 | 1.820000 | 520.84 | 8.10 | 1.781029 | candidate_quality_pass_review_required |
| s167_short_wide_lowedge_risk0250_h3_cd5_sht54_lng52 | short_wide_lowedge | 1.610000 | 547.06 | 224 | 1.840000 | 433.87 | 10.39 | 1.599065 | candidate_quality_pass_review_required |
| s167_short_cash45_guard_risk0250_h3_cd5_sht54_lng52 | short_cash45_guard | 1.410000 | 236.59 | 199 | 2.050000 | 404.33 | 6.41 | 1.896483 | validation_pf_below_34d;validation_net_density_thin_vs_stage165_primary |

## Judgment(판정)

Stage167(167단계)는 validation PF lift(검증 수익요인 상승)만 좁게 본 bounded experiment(경계 실험)이다. Effect(효과): 결과가 좋더라도 research package complete(연구 패키지 완료)가 아니며, Stage168(168단계) follow-up review(후속 검토)로 넘긴다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
