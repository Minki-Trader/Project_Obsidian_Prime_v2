# F87C trade-shape/risk repair or rotation decision(거래 형태/위험 수리 또는 회전 결정)

## Conclusion(결론)

F87C closes the trade-shape/risk repair decision(거래 형태/위험 수리 결정): F87B proxy scout(프록시 스카우트)는 MT5 runtime materialization(런타임 물질화)로 올릴 만큼 강하지 않다.

Result(결과): `negative_trade_shape_risk_proxy_axis_no_runtime_candidate_no_runtime_evidence`.

## What Changed(변경 사항)

- Action(행동): F87B top20 proxy evidence(상위 20% 프록시 근거)를 읽고 same-axis repair(동일 축 수리)를 capped(상한 처리)했다.
- Effect(효과): 다음은 `frontier87D_stage_closeout_or_f88_rotation_handoff_v1`이며, 같은 threshold/filter/parameter(임계값/필터/파라미터) 반복으로 이어지지 않는다.

## Evidence(근거)

- Best model(최선 모델): `sequence_context__good_shape_logreg_l2_balanced`
- Inner top20 shape lift(내부 상위20 형태 상승): `-0.004800918074965049`
- Locked OOS top20 shape lift(잠금 OOS 상위20 형태 상승): `-0.10561124310527928`
- Inner trades/day proxy(내부 일 거래수 프록시): `0.8536585365853658`
- Runtime probe trigger(런타임 탐침 트리거): `False`

## What Gates Passed(통과 게이트)

work_packet_schema_lint(작업 묶음 스키마 검사), skill_receipt_schema_lint(스킬 영수증 스키마 검사), frontier_extra_due_check(전선 추가 도래 점검), frontier_five_stage_direction_synthesis(전선 5단계 방향 종합), frontier_topic_rotation_check(전선 주제 회전 점검), scope_completion_gate(범위 완료 게이트), kpi_contract_audit(KPI 계약 감사), artifact_lineage_audit(산출물 계보 감사), result_judgment_receipt(결과 판정 영수증), state_sync_audit(상태 동기화 감사), required_gate_coverage_audit(필수 게이트 커버리지 감사), final_claim_guard(최종 주장 보호)가 통과 대상이다.

## What Gates Were Not Applicable(해당 없음 게이트)

runtime_evidence_gate(런타임 근거 게이트)는 Strategy Tester runtime/economics(전략 테스터 런타임/경제성)를 주장하지 않으므로 해당 없음이다. codex_task_force_review_packet(코덱스 태스크포스 검토 묶음)은 Task Force reviewed/pass(태스크포스 검토됨/통과) 주장이 없으므로 해당 없음이다.

## What Is Still Not Enforced(아직 강제하지 않는 것)

F87C does not run MT5(메타트레이더5), does not create ONNX/EA bundle identity(온엑스/EA 번들 정체성), and does not select a baseline(기준선).

## Allowed Claims(허용 주장)

- `f87c_trade_shape_risk_decision_recorded`
- `trade_shape_risk_threshold_filter_repair_capped`
- `stage_closeout_or_f88_rotation_handoff_next_planned`
- `runtime_materialization_not_started_due_to_no_meaningful_proxy_candidate`

## Forbidden Claims(금지 주장)

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
- `task_force_reviewed`
- `reviewed_by_unspawned_agents`
- `oos_selected_model`

## Next Hardening Step(다음 경화 단계)

Open `frontier87D_stage_closeout_or_f88_rotation_handoff_v1`. Action(행동)은 F87 negative memory(부정 기억), salvage clue(회수 단서), and F88 rotation proposal(F88 회전 제안)을 닫는 것이다. Effect(효과)는 trade-shape/risk topic(거래 형태/위험 주제)을 영구 금지하지 않고, 바로 다음 인접 단계에서 같은 축으로 미는 것만 막는다.
