# run364HO Single-Source Probability-Bin Veto Runtime Package(단일 원천 확률 구간 거부 런타임 패키지)

Updated(갱신): 2026-06-09T12:25:50Z

## Current Truth(현재 진실)

- run_id(실행 ID): `run364HO_materialize_h17_oos108_pf125_single_source_probability_bin_veto_runtime_package_without_db_v1`
- model(모델): `fj_sym_h2_m1p75__fj_behavior_density_cost__et8_l18_n160`
- feature contract(피처 계약): `60` features(피처), hash(해시) `204d912740d40322db76967362166c363a86afeb559cbeca8538cc9b9ab0d654`
- set/ini(설정/초기화): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HO/mt5/sets/OPv2_run364HO_single_source_probability_bin_veto.set` / `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HO/mt5/inis/OPv2_run364HO_single_source_probability_bin_veto.ini`
- compile zero errors(컴파일 오류 0): `True`
- portable EA copied(휴대 실행 EA 복사): `True`
- next_run_id(다음 실행 ID): `run364HP_execute_h17_oos108_pf125_single_source_probability_bin_veto_mt5_runtime_probe_without_db_v1`

## Action/Effect(행동/효과)

Action(행동): HN이 승인한 FJ single-source seed(FJ 단일 원천 씨앗)를 MT5-compatible ONNX(MT5 호환 온엑스), feature CSV(피처 CSV), probability-bin veto(확률 구간 거부) set/ini(설정/초기화 파일), Common Files(공용 파일) handoff(인계)로 materialize(물질화)했습니다.

Effect(효과): HP에서 MT5 Strategy Tester(MT5 전략 테스터)를 실행하고 proxy vs MT5(프록시 대 MT5) 차이를 기록할 수 있습니다.

## Expected Proxy(예상 프록시)

- OOS net/PF/density/trades(표본외 순수익/수익 팩터/밀도/거래수): `333.32` / `1.4709758917` / `2.5496183206` / `334`
- scaled density estimate(스케일 밀도 추정): `3.055518353`
- OOS long/short(표본외 롱/숏): `162` / `172`

## Runtime Boundary(런타임 경계)

- probability-bin veto(확률 구간 거부)는 enabled(활성)입니다.
- FJ selected proxy tape(FJ 선택 프록시 거래 목록)에서 vetoed trades(거부 거래)는 0건입니다.
- scaled density estimate(스케일 밀도 추정)는 MT5 proof(MT5 증명)가 아닙니다.
- 이 run(실행)은 runtime package(런타임 패키지)만 만들었고 MT5 execution(MT5 실행)은 아직 하지 않았습니다.

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| input_lineage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HO/input_manifest.csv | 입력 계보가 연결됐습니다. |
| feature_matrix_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HO/feature_matrix_audit.csv | single-source feature CSV(단일 원천 피처 CSV)가 작성됐습니다. |
| onnx_handoff_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HO/mt5_onnx_contract_audit.csv | MT5-compatible ONNX handoff(MT5 호환 온엑스 인계)가 작성됐습니다. |
| probability_bin_veto_parameter_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HI/probability_bin_veto_parameter_contract.json | probability-bin veto(확률 구간 거부) 파라미터가 연결됐습니다. |
| veto_applicability_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HO/probability_bin_veto_applicability_audit.csv | FJ 선택 테이프에서 veto(거부) 적용성을 기록했습니다. |
| runtime_representation_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HO/runtime_representation_audit.csv | runtime representation(런타임 표현)을 기록했습니다. |
| compile_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HO/mt5_compile_result.json | MetaEditor compile(메타에디터 컴파일) 오류 0개와 portable EA(휴대 실행 EA) 복사를 확인했습니다. |
| runtime_handoff_package_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HO/runtime_probe_attempt_package.csv | set/ini/attempt package(설정/초기화/시도 패키지)가 작성됐습니다. |
| common_files_sync_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HO/common_files_sync.csv | Common Files(공용 파일) 복사가 확인됐습니다. |
| proxy_mt5_comparison_contract_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HO/proxy_mt5_comparison_contract.csv | proxy vs MT5(프록시 대 MT5) 비교 계약이 작성됐습니다. |
| receipt_coverage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HO/runtime_parity_receipt.json | 필수 receipt(영수증)가 있습니다. |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HO/required_gate_coverage_audit.csv | 필수 gate(게이트)가 종료 기록에 연결됐습니다. |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HO/claim_boundary_receipt.json | 권위/승격/목표 주장을 하지 않았습니다. |

## Claim Boundary(주장 경계)

`runtime_probe_package_only_single_source_probability_bin_veto_no_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`
