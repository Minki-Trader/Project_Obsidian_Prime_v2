# Re-entry Order

이 문서는 프로젝트에 다시 들어올 때 읽는 순서(re-entry order, 재진입 순서)를 정한다.

목적은 오래된 단계 드리프트(stage drift, 단계 드리프트)를 다시 살리지 않는 것이다.

## 읽는 순서(Read Order, 읽는 순서)

1. `AGENTS.md`
2. `docs/workspace/workspace_state.yaml`
3. `docs/context/current_working_state.md`
4. 활성 단계(active stage, 활성 단계) `04_selected/selection_status.md`
5. 활성 단계(active stage, 활성 단계) `00_spec/stage_brief.md`
6. `docs/policies/stage_structure.md`
7. `docs/policies/exploration_mandate.md`
8. `docs/policies/architecture_invariants.md`
9. `docs/policies/kpi_measurement_standard.md`
10. `docs/policies/run_result_management.md`
11. `docs/policies/result_judgment_policy.md`
12. `docs/policies/agent_trigger_policy.md`
13. `docs/contracts/feature_calculation_spec_fpmarkets_v2.md`
14. `docs/contracts/python_feature_parser_spec_fpmarkets_v2.md`
15. `docs/contracts/mt5_ea_input_order_contract_fpmarkets_v2.md`

## 진실 우선순위(Truth Precedence, 진실 우선순위)

문서가 서로 다르면 다음 순서를 따른다.

1. `docs/workspace/workspace_state.yaml`
2. 활성 단계(active stage, 활성 단계) `04_selected/selection_status.md`
3. `docs/context/current_working_state.md`
4. `AGENTS.md`
5. 정책 문서(policy docs, 정책 문서)
6. 계약 문서(contract docs, 계약 문서)
7. 단계 노트(stage notes, 단계 노트)와 보고서(reports, 보고서)

## 재시작 경계(Restart Boundary, 재시작 경계)

오래된 Stage 00부터 Stage 07까지의 흐름은 현재 진실(current truth, 현재 진실)이 아니다. 과거 추적 이력(prior tracked history, 과거 추적 이력)일 뿐이다.

탐색(exploration, 탐색)을 진행할 수 있는지 판단할 때 오래된 방어 리뷰 문장(defensive review language, 방어 리뷰 문장)을 쓰지 않는다.
