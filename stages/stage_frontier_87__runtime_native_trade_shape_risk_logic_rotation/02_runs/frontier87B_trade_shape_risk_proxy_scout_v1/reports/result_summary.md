# F87B Trade Shape/Risk Proxy Scout(F87B 거래 형태/위험 프록시 탐색)

## Conclusion(결론)

F87B completed a proxy scout(F87B 프록시 탐색 완료) but did not run MT5 Strategy Tester(MT5 전략 테스터는 실행하지 않음). Runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 주장하지 않는다.

## What changed(변경 사항)

Action(행동): F86G sequence feature surface(F86G 시퀀스 피처 표면)와 F86D first-touch labels(F86D 첫 터치 라벨)를 결합해 trade-shape/risk proxy surface(거래 형태/위험 프록시 표면)를 만들었다.

Effect(효과): first-touch prediction(첫 터치 예측)을 그대로 반복하지 않고, MFE/MAE/shape score(최대 유리 이동/최대 불리 이동/형태 점수) 기반으로 후보의 위험 형태를 본다.

## What gates passed(통과한 게이트)

work_packet_schema_lint(작업 묶음 스키마 검사), skill_receipt_schema_lint(스킬 영수증 스키마 검사), frontier_extra_due_check(전선 추가 도래 점검), frontier_five_stage_direction_synthesis(전선 5단계 방향 종합), frontier_topic_rotation_check(전선 주제 회전 점검), scope_completion_gate(범위 완료 게이트), data_integrity_audit(데이터 무결성 감사), model_validation_audit(모델 검증 감사), kpi_contract_audit(KPI 계약 감사), artifact_lineage_audit(산출물 계보 감사), result_judgment_receipt(결과 판정 영수증), state_sync_audit(상태 동기화 감사), required_gate_coverage_audit(필수 게이트 커버리지 감사), final_claim_guard(최종 주장 보호)를 통과 대상으로 둔다.

## What gates were not applicable(해당 없음 게이트)

runtime_evidence_gate(런타임 근거 게이트)는 Strategy Tester runtime/economics(전략 테스터 런타임/경제성) 주장이 없으므로 해당 없음이다. codex_task_force_review_packet(코덱스 태스크포스 검토 묶음)은 Task Force reviewed/pass(태스크포스 검토됨/통과) 주장이 없으므로 해당 없음이다.

## What is still not enforced(아직 강제하지 않는 것)

MT5 Strategy Tester(MT5 전략 테스터), ONNX export(온엑스 내보내기), EA handoff(EA 인계), runtime economics(런타임 경제성)는 아직 없다. Git push(깃 원격 반영)는 validation(검증)이 아니다.

## Proxy readout(프록시 판독)

- Best model(최선 모델): `sequence_context__good_shape_logreg_l2_balanced`
- Inner top20 shape lift(내부 상위 20% 형태 점수 개선): `-0.004800918074965049`
- Inner top20 proxy trades/day(내부 상위 20% 프록시 거래/일): `0.8536585365853658`
- Locked OOS top20 shape lift(잠긴 OOS 상위 20% 형태 점수 개선): `-0.10561124310527928`
- Meaningful candidate(의미 있는 후보): `False`

## Allowed claims(허용 주장)

- `f87b_trade_shape_risk_proxy_surface_materialized`
- `f87b_leakage_and_split_audits_recorded`
- `f87b_proxy_scout_result_recorded`
- `f87b_runtime_preflight_decision_recorded`

## Forbidden claims(금지 주장)

- `completion`
- `selected_baseline`
- `operating_promotion`
- `runtime_authority`
- `live_readiness`
- `goal_achieve`
- `runtime_verified`
- `strategy_tester_runtime_economics`
- `materialization_ready`
- `ea_onnx_runtime_bundle_ready`
- `oos_selected_model`
- `task_force_reviewed`
- `reviewed_by_unspawned_agents`

## Next hardening step(다음 경화 단계)

F87C repair or rotation decision(F87C 수리 또는 회전 결정)으로 넘긴다.
