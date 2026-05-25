# Stage328 Frozen Signal Contract Extraction(328단계 고정 신호 계약 추출)

- stage_id(단계 ID): `328_onnx_candidate_campaign__cp322a_frozen_signal_contract_extraction`
- run_id(실행 ID): `run328A_extract_frozen_signal_contract_no_new_data_tuning_v1`
- objective(목표): `run322b_route_signal`을 새 forward(전진) 데이터 튜닝 없이 만들 수 있는지 확인한다.
- fixed_rule(고정 규칙): cp322A ONNX(온닉스), adapter(어댑터), feature order(피처 순서), D/B rule(D/B 규칙), threshold(임계값)는 변경하지 않는다.
- effect(효과): split-local rank(분할 내부 순위)를 그대로 전진에 쓰는 누수와, frozen numeric threshold(고정 숫자 임계값) 대체가 cp322A를 바꾸는 문제를 분리한다.
- next_action(다음 행동): `run328B_deep_audit_cp318_outcome_source_and_live_feature_rebuild_options`
