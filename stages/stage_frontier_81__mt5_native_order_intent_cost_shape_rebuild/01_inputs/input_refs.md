# F81 Input References(F81 입력 참조)

Updated(갱신): 2026-06-18T03:00:35Z

## Source Inputs(원천 입력)

- Current state(현재 상태): `docs/workspace/workspace_state.yaml`
- Current narrative(현재 설명): `docs/context/current_working_state.md`
- F80 closeout(전선80 마감): `stages/stage_frontier_80__multi_axis_surface_rotation_for_runtime_economics/03_reviews/stage_closeout_report.md`
- F80 context anchor(F80 문맥 앵커): `stages/stage_frontier_80__multi_axis_surface_rotation_for_runtime_economics/03_reviews/context_anchor.md`
- E01 closeout(추가01 마감): `stages/stage_frontier_extra_E01__f001_f050_hypothesis_mixing_runtime_learning/03_reviews/stage_closeout_report.md`
- E01 selection status(추가01 선택 상태): `stages/stage_frontier_extra_E01__f001_f050_hypothesis_mixing_runtime_learning/04_selected/selection_status.md`
- Frontier extra stage register(전선 추가 단계 등록부): `docs/registers/frontier_extra_stage_register.yaml`
- Run registry(실행 등록부): `docs/registers/run_registry.csv`
- Alpha run ledger(알파 실행 장부): `docs/registers/alpha_run_ledger.csv`

## Contract Inputs(계약 입력)

- Frontier governance(전선 운영): `docs/policies/frontier_governance.md`
- Exploration mandate(탐색 명령): `docs/policies/exploration_mandate.md`
- KPI measurement standard(KPI 측정 기준): `docs/policies/kpi_measurement_standard.md`
- Run result management(실행 결과 관리): `docs/policies/run_result_management.md`
- Result judgment policy(결과 판정 정책): `docs/policies/result_judgment_policy.md`
- MT5 EA input order contract(MT5 EA 입력 순서 계약): `docs/contracts/mt5_ea_input_order_contract_fpmarkets_v2.md`
- Training label split contract(학습 라벨 분할 계약): `docs/contracts/training_label_split_contract_fpmarkets_v2.md`

## Opening Boundary(개방 경계)

Action(행동): F81(전선81)은 F80/E01(전선80/추가01)의 negative runtime learning(부정 런타임 학습)을 reference(참조)로 쓰되, winner/baseline/promotion/runtime authority(승자/기준선/승격/런타임 권위)를 상속하지 않는다.

Effect(효과): F81(전선81)의 첫 proxy(프록시)는 order intent/cost/exit shape(주문 의도/비용/청산 형태) axis(축)를 새로 설계해야 하며, 같은 threshold/filter/parameter(임계값/필터/파라미터) 반복만으로 closeout(마감)을 주장하지 않는다.
