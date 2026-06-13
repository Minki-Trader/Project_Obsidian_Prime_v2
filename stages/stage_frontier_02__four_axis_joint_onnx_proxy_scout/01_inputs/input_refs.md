# Input References(입력 참조)

This file(이 파일)은 Frontier 02(전선 02)가 쓰는 bounded reference(제한 참조)를 고정한다.

## Governance Inputs(운영 입력)

- `docs/policies/frontier_governance.md`: frontier stage(전선 단계) open/close(개방/마감) 규칙.
- `docs/policies/exploration_mandate.md`: exploration(탐색)은 운영 게이트가 아니라 claim boundary(주장 경계)로 다룬다.
- `docs/policies/stage_structure.md`: stage folder(단계 폴더)와 run numbering(실행 번호) 규칙.
- `docs/policies/agent_trigger_policy.md`: skill routing(스킬 라우팅)과 Grok overlay(그록 오버레이) 규칙.

## Contract Inputs(계약 입력)

- `docs/contracts/time_axis_policy_fpmarkets_v2.md`: timestamp(타임스탬프)를 broker-clock alignment key(브로커 시계 정렬 키)로 다룬다.
- `docs/contracts/feature_calculation_spec_fpmarkets_v2.md`: closed-bar only(확정봉 전용) feature meaning(피처 의미).
- `docs/contracts/python_feature_parser_spec_fpmarkets_v2.md`: parser output order(파서 출력 순서), leakage guard(누수 방지), NaN policy(결측 정책).
- `docs/contracts/training_label_split_contract_fpmarkets_v2.md`: fwd12 label(12봉 전방 라벨)과 train/validation/OOS(학습/검증/표본외) 분할.
- `docs/contracts/model_input_feature_set_contract_fpmarkets_v2.md`: selected 58 feature set(선택 58개 피처 세트)와 feature order hash(피처 순서 해시).
- `docs/contracts/mt5_ea_input_order_contract_fpmarkets_v2.md`: ONNX input order(ONNX 입력 순서), shape(형태), skip policy(스킵 정책).

## Archive Inputs(보관소 입력)

- `stages/stage_frontier_01__archive_synthesis_and_new_axis_lock/01_inputs/stage12_364_campaign_map.md`
- `stages/stage_frontier_01__archive_synthesis_and_new_axis_lock/01_inputs/do_not_repeat_list.md`
- `stages/stage_frontier_01__archive_synthesis_and_new_axis_lock/01_inputs/reusable_artifact_index.md`
- `stages/stage_frontier_01__archive_synthesis_and_new_axis_lock/04_selected/next_frontier_proposal.md`
- `docs/registers/idea_registry.md`
- `docs/registers/negative_result_register.md`

## Current Use Boundary(현재 사용 경계)

These inputs(이 입력들)는 design and scout planning(설계와 탐색 계획)에만 쓴다.

Effect(효과): Frontier 02(전선 02)는 past clue(과거 단서)를 참고하지만, 과거 candidate(후보)나 runtime authority(런타임 권위)를 가져오지 않는다.
