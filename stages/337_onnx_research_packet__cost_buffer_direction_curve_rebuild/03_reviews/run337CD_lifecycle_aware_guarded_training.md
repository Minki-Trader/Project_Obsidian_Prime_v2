# Stage337 run337CD Lifecycle-Aware Guarded Training(생애주기 인식 방어 학습)

## Conclusion(결론)

run337CD(337CD 실행)는 cost2-aware label(비용2 인식 라벨)로 새 ONNX scout(온엑스 스카우트)를 학습하고 proxy expected(프록시 예상)를 만들었다.

Effect(효과): forward threshold tuning(전진 임계값 조정) 없이 비용2를 라벨 경계에 반영했다. 다음은 MT5 runtime probe(MT5 런타임 탐침)로 proxy expected(프록시 예상)와 실제 telemetry(기록)를 비교하는 것이다. Forward/Goal(전진/목표)은 주장하지 않는다.

## Result(결과)

- status(상태): `completed_stage337CD_lifecycle_aware_guarded_scouts_trained_proxy_expected_materialized_no_selection`
- judgment(판정): `cost2_aware_scouts_materialized_but_proxy_cost2_guard_still_failed_requires_attribution`
- decision(결정): `stage337CD_open_run337CE_execute_lifecycle_aware_mt5_runtime_probe`
- next_action(다음 행동): `run337CE_execute_lifecycle_aware_mt5_runtime_probe_without_db_v1`
- gates(게이트): `25/25`
- trained_models(학습 모델): `6`
- onnx_parity_passed(ONNX 동등성 통과): `6/6`
- cost2_survivors(비용2 생존): `0`

## Lifecycle Proxy(생애주기 프록시)

| model(모델) | role(역할) | closed events(닫힌 이벤트) | net cost1(비용1 순수익) | PF cost1(비용1 수익 팩터) | cost2 guard(비용2 가드) |
|---|---|---:|---:|---:|---|
| `cd_bt_core56_equity_stale_stress_not_primary__extratrees_cost2_depth5_leaf180` | `stress_only_not_primary` | 15 | -0.020462660723710325 | 0.3721415742317431 | `cost2_forward_proxy_failed_guard` |
| `cd_bt_core56_equity_stale_stress_not_primary__logreg_cost2_balanced_c075` | `stress_only_not_primary` | 381 | -0.05229417668777891 | 0.8382281308398952 | `cost2_forward_proxy_failed_guard` |
| `cd_bt_macro48_macro_lag_ablation__extratrees_cost2_depth5_leaf180` | `lag_audited_materialization_allowed` | 13 | -0.016304129655185837 | 0.42657059031263855 | `cost2_forward_proxy_failed_guard` |
| `cd_bt_macro48_macro_lag_ablation__logreg_cost2_balanced_c075` | `lag_audited_materialization_allowed` | 380 | -0.04390646984708728 | 0.8668344275050219 | `cost2_forward_proxy_failed_guard` |
| `cd_bt_technical42_low_stale_control__extratrees_cost2_depth5_leaf180` | `primary_materialization_allowed` | 19 | -0.023194847879904047 | 0.38457920442336113 | `cost2_forward_proxy_failed_guard` |
| `cd_bt_technical42_low_stale_control__logreg_cost2_balanced_c075` | `primary_materialization_allowed` | 354 | -0.03584339638055599 | 0.8893396286663824 | `cost2_forward_proxy_failed_guard` |

## Versus BU(기존 BU 대비)

| CD model(CD 모델) | BU reference(BU 기준) | net delta(순수익 차이) | PF delta(PF 차이) | judgment(판정) |
|---|---|---:|---:|---|
| `cd_bt_core56_equity_stale_stress_not_primary__extratrees_cost2_depth5_leaf180` | `bt_core56_equity_stale_stress_not_primary__extratrees_depth6_leaf120` | 0.010193095318989674 | -0.015502643617256895 | `not_improved_vs_bu_proxy` |
| `cd_bt_core56_equity_stale_stress_not_primary__logreg_cost2_balanced_c075` | `bt_core56_equity_stale_stress_not_primary__logreg_balanced_c1` | 0.02854706806722109 | 0.07088407114089523 | `improved_vs_bu_proxy_diagnostic_not_selection` |
| `cd_bt_macro48_macro_lag_ablation__extratrees_cost2_depth5_leaf180` | `bt_macro48_macro_lag_ablation__extratrees_depth6_leaf120` | -0.008345315718365836 | -0.24207940090636149 | `not_improved_vs_bu_proxy` |
| `cd_bt_macro48_macro_lag_ablation__logreg_cost2_balanced_c075` | `bt_macro48_macro_lag_ablation__logreg_balanced_c1` | 0.01974710504091272 | 0.04764691494602191 | `improved_vs_bu_proxy_diagnostic_not_selection` |
| `cd_bt_technical42_low_stale_control__extratrees_cost2_depth5_leaf180` | `bt_technical42_low_stale_control__extratrees_depth6_leaf120` | 0.027333373447295955 | 0.12636373444336113 | `improved_vs_bu_proxy_diagnostic_not_selection` |
| `cd_bt_technical42_low_stale_control__logreg_cost2_balanced_c075` | `bt_technical42_low_stale_control__logreg_balanced_c1` | -0.008288852173855988 | -0.024840771557617658 | `not_improved_vs_bu_proxy` |

## Boundary(경계)

- model_training(모델 학습): `run`
- threshold_tuning(임계값 조정): `not_run`
- lot_optimization(로트 최적화): `not_run`
- candidate_selection(후보 선택): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Claim boundary(주장 경계): `research_development_only_stage337CD_lifecycle_aware_guarded_training_without_db_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve`
