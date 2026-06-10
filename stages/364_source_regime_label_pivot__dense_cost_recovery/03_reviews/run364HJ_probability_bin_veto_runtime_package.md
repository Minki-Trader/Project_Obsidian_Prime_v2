# run364HJ Probability-Bin Veto Runtime Package(확률 구간 거부 런타임 패키지)

Updated(갱신): 2026-06-08T12:29:49Z

## Current Truth(현재 진실)

- run_id(실행 ID): `run364HJ_materialize_h17_oos108_pf125_probability_bin_veto_runtime_package_without_db_v1`
- primary model(우선 모델): `gz_cost_h2_m0p32__gz_joint_frontier_blend__rf9_l20_n176`
- fallback model(대체 모델): `hb_rebalance_h2_m0p26__hb_oos_profit_density_bridge__rf9_l20_n192`
- feature contract(피처 계약): primary 60 + fallback 56(우선 60 + 대체 56)
- probability-bin veto(확률 구간 거부): `17|4|6;21|5|7`
- set/ini(설정/초기화): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HJ/mt5/sets/OPv2_run364HJ_probability_bin_veto.set` / `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HJ/mt5/inis/OPv2_run364HJ_probability_bin_veto.ini`
- compile zero errors(컴파일 오류 0): `True`
- portable EA copied(휴대용 전문가 자문 복사): `True`
- next_run_id(다음 실행 ID): `run364HK_execute_h17_oos108_pf125_probability_bin_veto_mt5_runtime_probe_without_db_v1`

## Action/Effect(행동/효과)

Action(행동): HI에서 구현한 probability-bin veto runtime support(확률 구간 거부 런타임 지원)를 GZ primary + HB fallback(GZ 우선 + HB 대체) ONNX(온엑스) 패키지, feature CSV(피처 CSV), MT5 set/ini(MT5 설정/초기화 파일), Common Files(공용 파일) handoff(인계)로 물질화했습니다.

Effect(효과): HK에서 MT5 Strategy Tester(MT5 전략 테스터)를 바로 실행하고 proxy vs MT5(프록시 대 MT5) 차이를 비교할 수 있습니다.

## Expected Proxy(예상 프록시)

- OOS net/PF/density/trades(표본외 순수익/수익 팩터/밀도/거래수): `78.188` / `1.2173488818` / `1.3740458015` / `180`
- OOS long/short(표본외 롱/숏): `42` / `138`

## Runtime Boundary(런타임 경계)

- probability-bin veto(확률 구간 거부)는 represented(표현됨)입니다.
- dual-source route(이중 원천 라우트)는 partial_represented(부분 표현)입니다. HF Python router(HF 파이썬 라우터)의 score_plus_0p02(점수 0.02 추가) switch(전환)를 EA(전문가 자문)가 완전히 재현하지 않습니다.
- expected OOS density(예상 표본외 밀도)는 3/day(일 3회) 목표보다 낮습니다. 이 실행은 runtime capability probe package(런타임 기능 탐침 패키지)이지 operating candidate(운영 후보)가 아닙니다.

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| input_lineage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HJ/input_manifest.csv | 입력 계보가 연결됐습니다. |
| feature_matrix_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HJ/feature_matrix_audit.csv | primary/fallback feature CSV(우선/대체 피처 CSV)가 작성됐습니다. |
| onnx_handoff_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HJ/mt5_onnx_contract_audit.csv | MT5-compatible ONNX handoff(MT5 호환 온엑스 인계)가 작성됐습니다. |
| probability_bin_veto_parameter_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HI/probability_bin_veto_parameter_contract.json | probability-bin veto(확률 구간 거부) 파라미터가 연결됐습니다. |
| runtime_representation_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HJ/runtime_representation_audit.csv | runtime representation(런타임 표현)을 기록했습니다. |
| compile_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HJ/mt5_compile_result.json | MetaEditor compile(메타에디터 컴파일) 오류 0개와 portable EA(휴대용 전문가 자문) 복사를 확인했습니다. |
| runtime_handoff_package_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HJ/runtime_probe_attempt_package.csv | set/ini/attempt package(설정/초기화/시도 패키지)가 작성됐습니다. |
| common_files_sync_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HJ/common_files_sync.csv | Common Files(공용 파일) 복사가 확인됐습니다. |
| proxy_mt5_comparison_contract_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HJ/proxy_mt5_comparison_contract.csv | proxy vs MT5 비교 계약(프록시 대 MT5 비교 계약)이 작성됐습니다. |
| receipt_coverage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HJ/runtime_parity_receipt.json | 필수 receipt(영수증)가 있습니다. |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HJ/required_gate_coverage_audit.csv | 필수 gate(게이트)가 종료 기록에 연결됐습니다. |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HJ/claim_boundary_receipt.json | 권위/승격/목표 주장을 하지 않았습니다. |

## Claim Boundary(주장 경계)

`runtime_probe_package_only_probability_bin_veto_dual_source_partial_route_no_mt5_execution_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`
