# run364DN h17 short-source PF/net polish scout(17시 숏 원천 PF/순수익 다듬기 스카우트)

Updated(갱신): 2026-06-06T08:48:46Z

## Judgment(판정)

- run_id(실행 ID): `run364DN_train_h17_short_source_pf_balance_polish_scout_without_db_v1`
- parent_run_id(부모 실행 ID): `run364DM_review_h17_short_source_profit_recovery_mt5_runtime_probe_without_db_v1`
- selected_variant_id(선택 변형 ID): `dn04_risk_mult125_all_h17_20`
- judgment(판정): `proxy_pf_balance_polish_scout_no_calibrated_db_exceed_candidate_review_required_no_authority`
- next_run_id(다음 실행 ID): `run364DO_review_h17_short_source_pf_balance_polish_scout_without_db_v1`
- runtime_authority(런타임 권위): `not_claimed(주장 안 함)`

## Key Read(핵심 판독)

Action(행동): DL proxy/MT5 gap(DL 프록시/MT5 차이)을 보수 보정으로 적용해 source filter(원천 필터)와 risk-scale overlay(위험비율 오버레이)를 비교했습니다.

Effect(효과): net-only pass(순수익만 통과)와 PF pass(PF 통과)를 분리해, PF 상승 없는 밀도/위험 증가를 다음 패키지로 넘기지 않게 했습니다.

| selected_variant_id | calibrated_net | calibrated_pf | calibrated_net_delta_vs_db | calibrated_pf_delta_vs_db | estimated_shorts | calibrated_precheck | net_pass_pf_fail |
| --- | --- | --- | --- | --- | --- | --- | --- |
| dn04_risk_mult125_all_h17_20 | 1031.3784 | 1.3987327524 | 12.5984 | -0.0112672476 | 149.0 | failed_calibrated_precheck(보정 사전검사 실패) | net_pass_pf_fail(PF 부족 순수익 통과) |

## Top Surface(상위 표면)

| variant_id | runtime_calibrated_net_profit | runtime_calibrated_profit_factor | calibrated_net_delta_vs_db | calibrated_pf_delta_vs_db | estimated_mt5_short_trade_count | calibrated_precheck_status | net_pass_pf_fail_status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| dn04_risk_mult125_all_h17_20 | 1031.3784 | 1.3987327524 | 12.5984 | -0.0112672476 | 149.0 | failed_calibrated_precheck(보정 사전검사 실패) | net_pass_pf_fail(PF 부족 순수익 통과) |
| dn03_risk_mult120_all_h17_20 | 1026.9556 | 1.3991512694 | 8.1756 | -0.0108487306 | 149.0 | failed_calibrated_precheck(보정 사전검사 실패) | net_pass_pf_fail(PF 부족 순수익 통과) |
| dn05_core_risk_h17_18_20_min060 | 1023.5013 | 1.4012267323 | 4.7213 | -0.0087732677 | 149.0 | failed_calibrated_precheck(보정 사전검사 실패) | net_pass_pf_fail(PF 부족 순수익 통과) |
| dn06_core_risk_h17_18_20_min070 | 1022.21 | 1.4015270018 | 3.43 | -0.0084729982 | 149.0 | failed_calibrated_precheck(보정 사전검사 실패) | net_pass_pf_fail(PF 부족 순수익 통과) |
| dn02_risk_mult115_all_h17_20 | 1022.5328 | 1.3995736671 | 3.7528 | -0.0104263329 | 149.0 | failed_calibrated_precheck(보정 사전검사 실패) | net_pass_pf_fail(PF 부족 순수익 통과) |
| dn07_core_risk_h17_18_20_mult115 | 1020.7382 | 1.4003583101 | 1.9582 | -0.0096416899 | 149.0 | failed_calibrated_precheck(보정 사전검사 실패) | net_pass_pf_fail(PF 부족 순수익 통과) |
| dn08_risk_h17_20_mult115 | 1019.094 | 1.4015129246 | 0.314 | -0.0084870754 | 149.0 | failed_calibrated_precheck(보정 사전검사 실패) | net_pass_pf_fail(PF 부족 순수익 통과) |
| dn01_dl_anchor_no19_m050_r110 | 1018.11 | 1.4 | -0.67 | -0.01 | 149.0 | failed_calibrated_precheck(보정 사전검사 실패) |  |

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| scope_completion_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DN/dn_short_source_pf_balance_polish_surface.csv | all DN variants scored(모든 DN 변형 점수화) |
| input_lineage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DN/input_manifest.csv | inputs linked(입력 연결) |
| data_integrity_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DN/data_integrity_audit.csv | timestamp/no-overlap checks passed(시점/무겹침 검사 통과) |
| candidate_surface_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DN/dn_short_source_pf_balance_polish_surface.csv | selected variant changes source or risk params(선택 변형이 원천 또는 위험 파라미터 변경) |
| runtime_representability_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DN/runtime_representation_audit.csv | selected variant is parameter-ready(선택 변형이 파라미터 준비됨) |
| kpi_contract_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DN/package_precheck.csv | selected row has review-worthy calibrated signal(선택 행이 검토할 보정 신호 보유) |
| calibrated_proxy_boundary_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DN/proxy_mt5_calibration.csv | DL proxy/MT5 gap used as boundary(DL 프록시/MT5 차이를 경계로 사용) |
| no_trade_splitting_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DN/data_integrity_audit.csv | single-position replay used(단일 포지션 재생 사용) |
| receipt_coverage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DN/run_evidence_receipt.json | required receipts exist(필수 영수증 존재) |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DN/required_gate_coverage_audit.csv | required gates connected to closeout(필수 게이트 종료 기록 연결) |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DN/claim_boundary_receipt.json | no authority/promotion/goal claim(권위/승격/목표 주장 없음) |

## Boundary(경계)

This is proxy scout only(프록시 스카우트 전용)입니다. MT5 execution(MT5 실행), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 안 함)`입니다.
