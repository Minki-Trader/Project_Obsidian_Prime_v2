# Stage327 cp322A Overfit/Forward/Parity Probe(327단계 cp322A 과적합/전진/동등성 탐침)

- stage_id(단계 ID): `327_onnx_candidate_campaign__cp322a_overfit_forward_parity_robustness`
- run_id(실행 ID): `run327A_audit_cp322a_overfit_forward_parity_v1`
- objective(목표): 기존 cp322A ONNX(온닉스)가 앞으로도 쓸 수 있는 구조인지 본다.
- fixed_rule(고정 규칙): ONNX(온닉스), adapter(어댑터), feature order(피처 순서), threshold(임계값), D/B surface(D/B 표면), lot/risk logic(랏/위험 로직)은 수정하지 않는다.
- design_effect(설계 효과): 수익 KPI(핵심 지표)를 더 맞추지 않고, signal handoff(신호 인계), overfit(과적합), runtime parity(런타임 동등성)의 막힌 지점을 분리한다.
- stop_condition(중지 조건): forward signal handoff(전진 신호 인계)가 leakage-safe(누수 방지)로 재현되지 않으면 Goal Achieve(목표 달성)는 없다.
- next_action(다음 행동): `run328A_design_frozen_signal_contract_extraction_without_new_data_tuning`
