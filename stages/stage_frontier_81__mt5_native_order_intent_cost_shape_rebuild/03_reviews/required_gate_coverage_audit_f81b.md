# F81B Required Gate Coverage Audit(F81B 필수 게이트 커버리지 감사)

Status(상태): `f81b_proxy_material_signal_mt5_materialization_required_no_authority`

| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |
|---|---|---|---|
| `data_feature_contract_preflight` | `passed(통과)` | `stages/stage_frontier_81__mt5_native_order_intent_cost_shape_rebuild/03_reviews/f81b_data_feature_contract_preflight.json` | 데이터/피처/라벨/분할 경계를 실행 산출물로 남긴다. |
| `kpi_contract_audit` | `passed_proxy_only(프록시 한정 통과)` | `stages/stage_frontier_81__mt5_native_order_intent_cost_shape_rebuild/03_reviews/f81b_order_intent_cost_shape_proxy_summary.json`, `stages/stage_frontier_81__mt5_native_order_intent_cost_shape_rebuild/03_reviews/f81b_order_intent_cost_shape_ranked_top200.csv` | DD(손실폭), PF(수익 팩터), density(밀도), lifecycle(생명주기)을 같이 기록한다. |
| `signal_count_diagnostic_boundary` | `passed(통과)` | candidate fields(후보 필드) `raw_signal_total_diagnostic_only` | 신호 수를 경제성 결론으로 쓰지 않는다. |
| `tier_record_audit` | `passed_with_missing_required_boundary(필수 누락 경계 포함 통과)` | `stages/stage_frontier_81__mt5_native_order_intent_cost_shape_rebuild/03_reviews/f81b_tier_record_audit.csv` | Tier A/B/combined(티어 A/B/합산)을 빈칸으로 두지 않는다. |
| `runtime_probe_gate` | `pending_after_proxy(프록시 이후 대기)` | next run(다음 실행) `frontier81C_mt5_runtime_materialization_v1` | MT5 runtime probe(MT5 런타임 탐침) 전에는 권위 주장을 만들지 않는다. |
| `final_claim_guard` | `passed(통과)` | `proxy_scout_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve_no_parity_only_economics` | completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)를 금지한다. |

Counts(개수): scout `1862`, material `1013`, meaningful `162`, final-like `0`.
