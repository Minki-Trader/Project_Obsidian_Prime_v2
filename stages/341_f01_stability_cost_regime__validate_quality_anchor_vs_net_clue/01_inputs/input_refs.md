# Stage 341 Input Refs(341단계 입력 참조)

## Source Inputs(원천 입력)

- run340H final decision(340H 최종 결정): `stages/340_runtime_lifecycle_exit__quality_balance_pressure_review/02_runs/run340H/final_decision.json`
- run340H gate audit(340H 게이트 감사): `stages/340_runtime_lifecycle_exit__quality_balance_pressure_review/02_runs/run340H/required_gate_coverage_audit.csv`
- run340H scorecard(340H 점수표): `stages/340_runtime_lifecycle_exit__quality_balance_pressure_review/02_runs/run340H/f01_close_on_flat_false_pressure_review_scorecard.csv`
- run340H KPI judgment(340H 핵심 성과 지표 판정): `stages/340_runtime_lifecycle_exit__quality_balance_pressure_review/02_runs/run340H/f01_close_on_flat_false_pressure_kpi_judgment.csv`
- run340H attribution(340H 성과 귀속): `stages/340_runtime_lifecycle_exit__quality_balance_pressure_review/02_runs/run340H/performance_attribution.csv`
- run340H failure memory(340H 실패 기억): `stages/340_runtime_lifecycle_exit__quality_balance_pressure_review/02_runs/run340H/failure_memory.csv`
- run340H seed queue(340H 씨앗 대기열): `stages/340_runtime_lifecycle_exit__quality_balance_pressure_review/02_runs/run340H/run341A_seed_queue.csv`
- run340G MT5 summary(340G MT5 요약): `stages/340_runtime_lifecycle_exit__quality_balance_pressure_review/02_runs/run340G/f01_close_on_flat_false_pressure_mt5_probe_summary.csv`

## Stage 341 Handoff Files(341단계 인계 파일)

- handoff manifest(인계 목록): `stages/341_f01_stability_cost_regime__validate_quality_anchor_vs_net_clue/02_runs/run341A/stage340_to_stage341_handoff_manifest.csv`
- source inventory(원천 목록): `stages/341_f01_stability_cost_regime__validate_quality_anchor_vs_net_clue/02_runs/run341A/stage340_source_inventory.csv`
- next queue(다음 대기열): `stages/341_f01_stability_cost_regime__validate_quality_anchor_vs_net_clue/02_runs/run341A/run341B_validation_seed_queue.csv`

Effect(효과): run341B(341B 실행)가 Stage 340(340단계) 파일을 다시 수색하지 않고 바로 validation design(검증 설계)을 시작하게 한다.
