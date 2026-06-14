# Frontier28B Gate Audit(전선28B 게이트 감사)

- scope_completion_gate(범위 완료 게이트): stability gap artifacts(안정성 격차 산출물) created(생성) `stages/stage_frontier_28__train_only_stability_gap_penalty_for_pf_dd_balance_onnx_scout/02_runs/frontier28B_train_only_stability_gap_penalty_proxy_scout_v1/final_summary.json`
- kpi_contract_audit(KPI 계약 감사): split metrics/chunk metrics/summary(분할 지표/조각 지표/요약) created(생성)
- leakage_guard(누수 방지): selection boundary(선택 경계)는 train-only chunk rank(학습 전용 조각 순위), validation/OOS(검증/표본외)는 read-only(읽기 전용)
- required_gate_coverage_audit(필수 게이트 커버리지 감사): stage ledger/run registry rows(단계 장부/실행 등록부 행) written(기록)
- tier_pair_record_gate(티어 쌍 기록 게이트): Tier A/Tier B/Tier A+B rows(티어 A/B/A+B 행) written(기록)
- runtime_probe_gate(런타임 탐침 게이트): `out_of_scope_by_claim_no_handoff_candidate(인계 후보 없어 주장 범위 밖)`
- final_claim_guard(최종 주장 방어): runtime authority/operating promotion/Goal Achieve(런타임 권위/운영 승격/목표 달성) not_claimed(주장 없음)
