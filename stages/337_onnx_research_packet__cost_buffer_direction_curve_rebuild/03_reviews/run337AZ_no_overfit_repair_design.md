# Stage337 run337AZ No-Overfit Repair Design(337단계 337AZ 무과적합 수리 설계)

## Purpose(목적)

run337AZ(337AZ 실행)는 run337AY(337AY 실행)의 shifted custom exact timestamp(이동 커스텀 정확 시각) 귀속 결과를 새 후보(candidate, 후보)나 새 임계값(threshold, 임계값)으로 바꾸지 않는다.

Effect(효과): 비용 버퍼(cost buffer, 비용 버퍼), 방향 균형(direction balance, 방향 균형), 거래 밀도(trade density, 거래 밀도), 곡선 포켓(curve pocket, 곡선 포켓), proxy-MT5 boundary(프록시-MT5 경계)를 다음 materialization(물질화)에서 검증할 수 있는 사전 선언 계약으로 바꾼다.

## Result(결과)

- status(상태): `completed_stage337AZ_no_overfit_repair_design_materialized_no_training_no_selection`
- judgment(판정): `shifted_attribution_converted_to_predeclared_no_overfit_repair_design`
- design_rows(설계 행): `5`
- fragility_delta_rows(취약성 차이 행): `7`
- falsification_gate_rows(반증 게이트 행): `6`
- queue_rows(대기열 행): `2`
- gates(게이트): `9/9`

## Plain Meaning(쉬운 의미)

지금은 모델이 좋아졌다는 뜻이 아니다. run337AY(337AY 실행)에서 보인 약점을 보고, 다음 실험이 어디를 고쳐야 하고 무엇을 절대 하면 안 되는지 고정한 상태다.

Effect(효과): 다음 run337BA(337BA 실행)는 이 설계를 실제 입력 산출물로 만들 수 있지만, 아직 Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 말할 수 없다.

## Key Design Decisions(핵심 설계 결정)

- defensive cost margin objective(방어 비용 마진 목적): 작은 비용 압박에서 무너지는 후보를 먼저 반증한다.
- direction balance surface(방향 균형 표면): 숏 거래를 억지로 만들지 않고 방향별 근거 부족을 드러낸다.
- aggressive density preservation(공격적 거래 밀도 보존): 방어 수리가 거래 수를 죽여서 좋아 보이는 것을 막는다.
- curve pocket state veto(곡선 포켓 상태 거부): 날짜나 거래 번호를 외우지 않고 진입 전 상태로 포켓을 설명할 수 있는지 본다.
- proxy-MT5 dual read(프록시-MT5 이중 판독): proxy(프록시)는 신호 점검만, KPI(핵심 성과 지표)는 MT5(MetaTrader 5, 메타트레이더5)에서만 본다.

## Outputs(산출물)

- `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337AZ/shifted_fragility_delta_matrix.csv`
- `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337AZ/no_overfit_repair_design_matrix.csv`
- `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337AZ/repair_falsification_protocol.csv`
- `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337AZ/proxy_mt5_runtime_use_policy.csv`
- `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337AZ/data_feature_boundary_contract.csv`
- `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337AZ/run337BA_materialization_queue.csv`
- `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337AZ/repair_defensive_aggressive_balance_matrix.csv`
- `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337AZ/required_gate_coverage_audit.csv`

## Decision(결정)

- decision(결정): `stage337AZ_open_run337BA_materialize_no_overfit_repair_inputs_without_db_no_selection`
- next_action(다음 행동): `run337BA_materialize_no_overfit_repair_inputs_from_shifted_attribution_without_db_v1`
- claim_boundary(주장 경계): `research_development_only_stage337AZ_no_overfit_repair_design_from_shifted_attribution_without_db_no_model_training_no_threshold_retuning_no_db_rule_rewrite_no_lot_optimization_no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve`
