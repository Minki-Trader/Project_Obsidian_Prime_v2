# Stage180 TP45 Context Lifecycle DD Repair Report(180단계 익절 4.5 문맥/생활주기 낙폭 수정 보고서)

- stage(단계): `180_adapter_research__tp45_context_lifecycle_dd_repair`
- run(실행): `run180A_stage180_tp45_context_lifecycle_dd_repair_v1`
- source_stage(원천 단계): `179_adapter_research__stage178_risk_compression_followup_review`
- source_run(원천 실행): `run179A_stage179_stage178_risk_compression_followup_review_v1`
- source_adapter(원천 어댑터): `s178_tp45_control_risk0365_c060_h3_cd5_sht54_lng52`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `open_stage181_bounded_followup_due_to_context_lifecycle_tradeoff_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Experiment Design(실험 설계)

- hypothesis(가설): Stage178(178단계)의 risk cap compression(위험 상한 압축)은 DD(낙폭)를 낮추지만 net(순손익)을 깨뜨렸다. 그러므로 Stage180(180단계)는 risk cap(위험 상한)을 유지하고 context/lifecycle(문맥/생활주기)만 좁게 수정한다.
- action(행동): source model(원천 모델), TP45(익절 4.5), SL2.075(손절 2.075), ATR bracket(ATR 브래킷), model risk cap(모델 위험 상한) `0.0365`, threshold(문턱값) short `0.54` / long `0.52`를 고정했다.
- effect(효과): KPI(핵심 성과 지표) 변화가 exposure scale(노출 규모) 축소가 아니라 entry context/lifecycle(진입 문맥/생활주기) 수정 때문인지 판독할 수 있다.
- changed_variables(변경 변수): same-direction cooldown(동방향 대기) `5/8`, max hold bars(최대 보유 봉) `3/2`, wide vs midwide low-edge context gate(넓은/중간넓은 저가장자리 문맥 제한문).
- success_criteria(성공 기준): validation PF/net(검증 수익요인/순손익)이 legacy 34D(레거시 34D) 이상이고 validation DD/OOS DD(검증 낙폭/표본외 낙폭)와 validation mid PF(검증 중반 수익요인)가 같이 개선되어야 한다.
- stop_condition(정지 조건): 네 개 bounded variants(경계 변형)를 MT5 Strategy Tester(메타트레이더5 전략 테스터)로 측정하면 Stage180(180단계)을 닫고 Stage181(181단계) follow-up review(후속 검토)로 넘긴다.

## KPI Read(KPI 핵심 성과 지표 판독)

| adapter(어댑터) | axis(축) | hold(보유) | cooldown(대기) | val PF(검증 수익요인) | val net(검증 순손익) | val DD%(검증 낙폭) | mid PF(중반 수익요인) | OOS PF(표본외 수익요인) | OOS net(표본외 순손익) | OOS DD%(표본외 낙폭) | flags(표식) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| s180_tp45_control_risk0365_h3_cd5_ctxwide_sht54_lng52 | tp45_control_ctxwide | 3 | 5 | 1.620000 | 1037.74 | 13.7450 | 1.375002 | 1.910000 | 823.11 | 14.2029 | validation_balance_dd_above_34d;validation_mid_pf_below_34d;oos_balance_dd_above_34d |
| s180_tp45_cd8_risk0365_h3_cd8_ctxwide_sht54_lng52 | tp45_cd8_ctxwide | 3 | 8 | 1.640000 | 1085.62 | 13.7243 | 1.365049 | 1.890000 | 800.74 | 14.2401 | validation_balance_dd_above_34d;validation_mid_pf_below_34d;oos_balance_dd_above_34d |
| s180_tp45_hold2_risk0365_h2_cd5_ctxwide_sht54_lng52 | tp45_hold2_ctxwide | 2 | 5 | 1.590000 | 446.88 | 8.9028 | 1.133111 | 1.630000 | 294.31 | 10.3819 | validation_net_below_34d;validation_mid_pf_below_34d;validation_late_concentration_above_50pct;oos_net_materially_below_stage171_primary |
| s180_tp45_midwide_risk0365_h3_cd5_ctxmid_sht54_lng52 | tp45_midwide_ctx | 3 | 5 | 1.680000 | 1223.67 | 14.8516 | 1.487087 | 1.910000 | 914.52 | 8.8227 | validation_balance_dd_above_34d;validation_mid_pf_below_34d |

## Best Read(최선 판독)

- best_adapter(최선 어댑터): `s180_tp45_cd8_risk0365_h3_cd8_ctxwide_sht54_lng52`
- validation_net(검증 순손익): `1085.62`
- validation_balance_dd(검증 잔고 낙폭): `13.7243`
- validation_mid_pf(검증 중반 수익요인): `1.365049`
- oos_balance_dd(표본외 잔고 낙폭): `14.2401`
- quality_flags(품질 표식): `validation_balance_dd_above_34d;validation_mid_pf_below_34d;oos_balance_dd_above_34d`

## Judgment(판정)

Stage180(180단계)는 research/development only(연구개발 전용)이다. Effect(효과): 결과가 좋아도 deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료)를 만들지 않는다.
