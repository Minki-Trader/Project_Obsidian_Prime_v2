# Required Gate Coverage Audit F76D(F76D 필수 게이트 커버리지 감사)

Updated(갱신): 2026-06-17T06:07:32Z

| gate(게이트) | status(상태) | evidence/effect(근거/효과) |
|---|---|---|
| candidate_lock(후보 고정) | `passed(통과)` | `f76b_06637` |
| probability_parity(확률 동등성) | `3/3` | ONNX long schema(ONNX 롱 스키마) |
| signal_count_parity(신호 수 동등성) | `3/3` | selected-entry veto tape(선택 진입 거부 테이프) |
| feature_readiness_parity(피처 준비 동등성) | `1/1` | 48 feature CSV(48개 피처 CSV) |
| source_reproduction(프록시 재현) | `2/2` | validation/OOS proxy KPI reproduction(검증/표본외 프록시 KPI 재현) |
| MT5 runtime probe(MT5 런타임 탐침) | `2/2` | Strategy Tester attempts(전략 테스터 시도) |
| final_claim_guard(최종 주장 보호) | `passed(통과)` | `runtime_probe_observation_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve` |
