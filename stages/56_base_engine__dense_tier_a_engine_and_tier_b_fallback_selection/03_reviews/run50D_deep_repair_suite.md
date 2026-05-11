# Run50D Deep Repair Suite(50D 조밀 보정 묶음)

- stage_id(단계 ID): `56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection`
- parent_run_id(상위 실행 ID): `run50D_stage56_deep_repair_suite_v1`
- mt5_attempted(MT5 시도): `True`
- final_read(최종 판독): `stronger_baseline_candidate_only`
- best_variant(최선 변형): `d390h10` / `weak_dense_engine_candidate_actual_routed_mt5`
- boundary(주장 경계): `research_baseline_selection_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Design(설계)

- action(행동): d38h10 주변 threshold(임계값), hold(보유), margin(마진), long/short balance(롱/숏 균형), Tier B fallback subtype(Tier B 대체 하위유형), session slice(세션 절편)를 실제 MT5(메타트레이더5)로 다시 실행했다.
- effect(효과): previous closeout(이전 종료) `baseline_candidate_only(기준선 후보 전용)`을 보존하면서, 같은 Stage56 target contract(목표 계약)에 더 강한 증거를 붙인다.
- acceptance(수용): selected_research_baseline(선택 연구 기준선)은 actual routed MT5(실제 라우팅 MT5) validation/OOS(검증/표본외) 모두 양수, PF(수익 팩터) >= 1.05, preferred density(선호 밀도) 5~10 trades/day(거래/일)에 근접 또는 충족해야 한다.
- comparison(비교): d38h10 reference(참조)는 routed validation(라우팅 검증) 4.464481/day PF 1.07, routed OOS(라우팅 표본외) 3.446154/day PF 1.13, total net(총 순손익) 492.48이다.

## Results(결과)

| variant(변형) | group(묶음) | routed validation/day(라우팅 검증/일) | routed OOS/day(라우팅 표본외/일) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |
|---|---|---:|---:|---:|---:|---:|---:|---|
| d370h10 | dense | 4.907104 | 3.671795 | 1.05 | 1.05 | 153.4 | 136.97 | `weak_dense_engine_candidate_actual_routed_mt5` |
| d375h10 | dense | 4.650273 | 3.579487 | 1.08 | 1.03 | 231.28 | 84.8 | `quality_or_density_inconclusive_actual_routed_mt5` |
| d375h11 | dense | 4.431694 | 3.425641 | 1.04 | 1.06 | 121.7 | 150.83 | `quality_or_density_inconclusive_actual_routed_mt5` |
| d380h09 | dense | 4.688525 | 3.620513 | 1.04 | 1.04 | 113.83 | 89.14 | `quality_or_density_inconclusive_actual_routed_mt5` |
| d385h10 | dense | 4.256831 | 3.194872 | 1.1 | 1.13 | 279.68 | 296.49 | `weak_dense_engine_candidate_actual_routed_mt5` |
| d385h11 | dense | 4.071038 | 3.102564 | 1.05 | 1.12 | 135.73 | 274.45 | `weak_dense_engine_candidate_actual_routed_mt5` |
| d390h10 | dense | 4.087432 | 3.046154 | 1.13 | 1.12 | 341.54 | 273.2 | `weak_dense_engine_candidate_actual_routed_mt5` |
| d38long37short39h10 | balance | 4.491803 | 3.343590 | 1.08 | 1.07 | 232.03 | 161.84 | `weak_dense_engine_candidate_actual_routed_mt5` |
| d38short37long39h10 | balance | 4.415301 | 3.302564 | 1.11 | 1.09 | 311.11 | 207.48 | `weak_dense_engine_candidate_actual_routed_mt5` |
| d38m005h10 | balance | 4.382514 | 3.353846 | 1.06 | 1.11 | 159.35 | 262.72 | `weak_dense_engine_candidate_actual_routed_mt5` |
| d38h10_b040 | fallback | 4.382514 | 3.338462 | 1.06 | 1.09 | 174.37 | 225.05 | `weak_dense_engine_candidate_actual_routed_mt5` |
| d38h10_b042 | fallback | 4.322404 | 3.292308 | 1.07 | 1.1 | 196.94 | 232.42 | `weak_dense_engine_candidate_actual_routed_mt5` |
| d38h10_bmacro | fallback | 4.224044 | 3.189744 | 1.09 | 1.11 | 252.96 | 262.66 | `weak_dense_engine_candidate_actual_routed_mt5` |
| d38h10_bmixed | fallback | 4.240437 | 3.251282 | 1.08 | 1.08 | 226.87 | 197.19 | `weak_dense_engine_candidate_actual_routed_mt5` |
| d38h10_bcoremixed | fallback | 4.262295 | 3.251282 | 1.08 | 1.08 | 222.21 | 194.66 | `weak_dense_engine_candidate_actual_routed_mt5` |
| d38h10_early | session | 2.278689 | 1.758974 | 1.07 | 0.91 | 162.97 | -188.87 | `quality_failed_actual_routed_mt5` |
| d38h10_mid | session | 1.245902 | 1.076923 | 0.99 | 0.97 | -17.34 | -27.97 | `quality_failed_actual_routed_mt5` |
| d38h10_late | session | 1.010929 | 0.717949 | 1.02 | 0.9 | 25.88 | -89.3 | `quality_failed_actual_routed_mt5` |

## Final Read(최종 판독)

- judgment(판정): `stronger_baseline_candidate_only`
- reason(이유): stronger quality/net candidate(품질/순손익 강화 후보)이지만 selected baseline preferred density target(선택 기준선 선호 밀도 목표) 미달
- effect(효과): 이 판독은 research baseline selection(연구 기준선 선택) 안에서만 유효하고, live readiness(실거래 준비)나 runtime authority(런타임 권위)를 만들지 않는다.
