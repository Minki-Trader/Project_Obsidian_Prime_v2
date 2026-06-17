# Required Gate Coverage Audit F78D(F78D 필수 게이트 커버리지 감사)

Updated(갱신): 2026-06-17T09:14:57Z

| gate(게이트) | status(상태) | evidence/effect(근거/효과) |
|---|---|---|
| F78C Grok accepted with conditions(F78C Grok 조건부 수용) | `passed(통과)` | `stages/stage_frontier_78__execution_calibrated_density_contract_pnl_rebuild/03_reviews/grok_pre_mt5_execution_calibrated_negative_control_runtime_probe_receipt.md` |
| target lock(대상 고정) | `passed(통과)` | `f78b_02234`, `logistic_l2_balanced` |
| source reproduction(원천 재현) | `2/2` | validation/OOS proxy KPI reproduction(검증/표본외 프록시 KPI 재현) |
| probability parity(확률 동등성) | `3/3` | ONNX short schema(ONNX 숏 스키마) |
| signal count parity(신호 수 동등성) | `3/3` | selected-entry veto tape(선택 진입 거부 테이프) |
| feature readiness parity(피처 준비 동등성) | `1/1` | 33 feature CSV(33개 피처 CSV) |
| MT5 runtime probe(MT5 런타임 탐침) | `1/1` | Strategy Tester attempts(전략 테스터 시도) |
| runtime parity receipt(런타임 동등성 영수증) | `recorded(기록됨)` | `stages/stage_frontier_78__execution_calibrated_density_contract_pnl_rebuild/03_reviews/f78d_runtime_parity_receipt.json` |
| backtest forensics receipt(백테스트 포렌식 영수증) | `recorded(기록됨)` | `stages/stage_frontier_78__execution_calibrated_density_contract_pnl_rebuild/03_reviews/f78d_backtest_forensics_receipt.json` |
| final claim guard(최종 주장 보호) | `passed(통과)` | `negative_control_runtime_probe_observation_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve` |
