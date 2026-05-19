# Stage260 Tight Plus High Edge PF/OOS Recovery Repair(260단계 타이트+하이엣지 PF/표본외 회복 수리)

- stage(단계): `260_adapter_research__tight_plus_highedge_pf_oos_recovery_repair`
- run(실행): `run260A_stage260_tight_plus_highedge_pf_oos_recovery_repair_v1`
- source_stage(원천 단계): `259_adapter_research__stage258_short_tight_margin_pf_followup_review`
- source_run(원천 실행): `run259A_stage259_stage258_short_tight_margin_pf_followup_review_v1`
- source_stage258_evidence_commit(원천 258단계 근거 커밋): `5dbd67b79c824e3d7049b6f482b8c83b0eda92db`
- source_stage258_hash_record_commit(원천 258단계 해시 기록 커밋): `7f916e6bae523c45f269eb48c91f6c17e61a55e3`
- source_stage259_evidence_commit(원천 259단계 근거 커밋): `8d3f6644fa08bb344e7763d9d8e211f045c61f78`
- source_stage259_hash_record_commit(원천 259단계 해시 기록 커밋): `28cfb566f3ae6633ec04237a307754666f6cde38`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `open_stage261_bounded_followup_due_to_stage260_pf_oos_tradeoff_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Question(경계 질문)

Can rank-conditioned source gate repair(순위 조건 소스 차단문 수리) preserve `s258_tight_plus_highedge` validation net/DD(검증 순수익/손실폭) while improving PF/mid PF(수익 팩터/중간 수익 팩터) and OOS net/PF(표본외 순수익/수익 팩터)?

## Design(설계)

- fixed(고정): score table(점수 표면), thresholds(임계값) `0.54/0.52`, lifecycle(생명주기) hold 3/cooldown 8(3봉 보유/8봉 대기), ATR SL/TP(ATR 손절/익절) `2.0325/4.615`, model-controlled risk%(모델 제어 위험비율) cap(상한) `0.0305`.
- changed(변경): only rank-conditioned low-edge/high-edge short supply(순위 조건 낮은/높은 마진 가장자리 숏 공급).
- not done(하지 않음): ONNX hardening(ONNX 경화), live readiness(실거래 준비), deployment(배포), operating promotion(운영 승격).

## KPI Matrix(KPI 핵심 성과 지표 행렬)

| adapter(어댑터) | val PF(검증 수익 팩터) | val net(검증 순수익) | DD%(손실폭) | mid PF(중간 수익 팩터) | OOS PF(표본외 수익 팩터) | OOS net(표본외 순수익) | pass(통과) |
|---|---:|---:|---:|---:|---:|---:|---|
| s260_highedge_control | 1.56 | 1204.24 | 9.0307 | 1.5342048177397174 | 1.7 | 828.96 | False |
| s260_lowrank_lowedge_filter | 1.61 | 1291.28 | 9.0536 | 1.6003645706247935 | 1.7 | 775.97 | True |
| s260_midlow_lowedge_filter | 1.59 | 972.15 | 12.9281 | 1.5166508780878818 | 1.78 | 776.02 | False |
| s260_vhigh_highedge_relax | 1.56 | 1204.24 | 9.0307 | 1.5342048177397174 | 1.7 | 828.96 | False |
| s260_lowrank_filter_vhigh_relax | 1.61 | 1291.28 | 9.0536 | 1.6003645706247935 | 1.7 | 775.97 | True |

## Easy Read(쉬운 해석)

- control(대조군): `s260_highedge_control` validation PF(검증 수익 팩터) `1.56`, validation net(검증 순수익) `1204.24`, OOS net(표본외 순수익) `828.96`.
- best_read(최선 해석): `s260_lowrank_lowedge_filter` validation PF(검증 수익 팩터) `1.61`, validation net(검증 순수익) `1291.28`, OOS net(표본외 순수익) `775.97`.
- final claim(최종 주장)은 금지다. Stage261(261단계)에서 이 결과를 review-only(검토 전용)로 판정해야 한다.
