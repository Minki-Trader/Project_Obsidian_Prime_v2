# Required Gate Coverage Audit F78B(F78B 필수 게이트 커버리지 감사)

| gate(게이트) | status(상태) | evidence/effect(근거/효과) |
|---|---|---|
| data integrity(데이터 무결성) | `recorded(기록됨)` | `stages/stage_frontier_78__execution_calibrated_density_contract_pnl_rebuild/03_reviews/f78b_data_integrity_review.json` |
| model validation(모델 검증) | `recorded(기록됨)` | `stages/stage_frontier_78__execution_calibrated_density_contract_pnl_rebuild/03_reviews/f78b_model_validation_review.json` |
| proxy KPI contract(프록시 KPI 계약) | `passed(통과)` | `stages/stage_frontier_78__execution_calibrated_density_contract_pnl_rebuild/03_reviews/f78b_contract_proxy_summary.json` |
| contract P/L identity(계약 손익 정체성) | `recorded(기록됨)` | scale `0.08870965974736267` source `F77 observed gross-profit runtime/proxy scale mean(관찰 총이익 런타임/프록시 배율 평균): (0.09352576207175615 + 0.08389355742296918) / 2` |
| calendar density denominator(달력 밀도 분모) | `recorded(기록됨)` | candidate rows contain calendar_trades_day(달력 일 거래 수) and active_trades_day(활성일 거래 수) |
| Tier paired record(티어 쌍 기록) | `boundary_recorded(경계 기록)` | Tier A separate(티어 A 분리), Tier B missing_required(필수 누락), combined out_of_scope(합산 범위 밖) |
| runtime probe rule(런타임 탐침 규칙) | `required_next(다음 필수)` | meaningful/weak nonzero signal(의미/약한 비영 신호)이 있으면 pre-MT5 Grok + MT5 Runtime Probe(사전 MT5 그록 + MT5 런타임 탐침) |
| claim guard(주장 보호) | `passed(통과)` | `proxy_scout_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve` |

Open status(현재 상태): `proxy_contract_weak_nonzero_signal_negative_control_probe_required_no_authority`

Next run(다음 실행): `frontier78C_pre_mt5_grok_execution_calibrated_negative_control_runtime_probe_v1`
