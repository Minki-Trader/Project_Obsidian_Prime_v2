# Frontier31B Gate Audit(전선31B 게이트 감사)

- stage_open_lock_gate(단계 개방 잠금 게이트): `stages/stage_frontier_31__exit_shape_pivot_for_density_preserved_source_scout_pf_lift_onnx_scout/02_runs/frontier31A_stage_open_exit_shape_pivot_for_density_preserved_source_scout_pf_lift_hypothesis_design_v1/return_space_exit_shape_lock.json` read(읽음)
- fixed_entry_surface_gate(고정 진입 표면 게이트): F30B source no-veto scout rows(전선30B 원천 무차단 탐색 행) `5` only(만 사용)
- train_only_selection_gate(학습 전용 선택 게이트): stop/take(손절/익절) caps(상한)는 train PnL distribution(학습 손익 분포)에서만 산출
- leakage_guard(누수 방어): validation/OOS(검증/표본외)는 read-only diagnostics(읽기 전용 진단)
- executable_boundary_gate(실행 가능성 경계 게이트): return-space clipping(수익률 공간 클리핑)은 MT5 executable representation(MT5 실행 가능 표현)이 아님
- tier_pair_gate(티어 쌍 게이트): Tier B(티어 B)는 missing_required(필수 누락), Tier A+B(티어 A+B)는 out_of_scope_by_claim(주장 범위 밖)
- runtime_probe_gate(런타임 탐침 게이트): `runtime_probe_pending_executable_exit_representation_repair_before_mt5`
- final_claim_guard(최종 주장 방어): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) all not_claimed(모두 주장 없음)
