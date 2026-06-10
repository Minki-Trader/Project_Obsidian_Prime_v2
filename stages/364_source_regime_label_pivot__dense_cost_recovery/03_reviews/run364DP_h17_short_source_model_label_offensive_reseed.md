# run364DP h17 short-source model/label offensive reseed(17시 숏 원천 모델/라벨 공격 재시드)

Updated(갱신): 2026-06-06T09:18:33Z

## Judgment(판정)

- run_id(실행 ID): `run364DP_train_h17_short_source_model_label_offensive_reseed_without_db_v1`
- parent_run_id(부모 실행 ID): `run364DO_review_h17_short_source_pf_balance_polish_scout_without_db_v1`
- selected_model_id(선택 모델 ID): `short_h3_m2__full58(전체_58)__et6_l80_n96(엑스트라트리6_잎80_96)`
- judgment(판정): `inconclusive_short_source_model_label_reseed_oos_clue_validation_density_fail_no_package_no_authority`
- next_run_id(다음 실행 ID): `run364DQ_review_h17_short_source_model_label_offensive_reseed_without_db_v1`
- runtime_package(런타임 패키지): `not_opened(열지 않음)`
- runtime_authority(런타임 권위): `not_claimed(주장 안 함)`

## Key Read(핵심 판독)

Action(행동): train split(학습 분할)로 short-source gate model(숏 원천 게이트 모델)을 학습하고, validation threshold(검증 임계값)와 OOS read(표본외 판독), ONNX smoke(온엑스 스모크)를 확인했습니다.

Effect(효과): parameter-only polish(파라미터 전용 다듬기) 실패 뒤에도 새 model/label/feature seed(모델/라벨/피처 씨앗)를 열었고, 검증 밀도/순수익이 약하면 package(패키지)로 넘기지 않게 했습니다.

| selected_model | validation_net | validation_pf | validation_density | oos_net | oos_pf | oos_density | strict_count |
| --- | --- | --- | --- | --- | --- | --- | --- |
| short_h3_m2__full58(전체_58)__et6_l80_n96(엑스트라트리6_잎80_96) | 77.23 | 1.0620695198 | 1.6775956284 | 218.16 | 1.2733303682 | 1.6564885496 | 0 |

## Top Surface(상위 표면)

| model_id | label_id | feature_set_id | threshold_id | max_hold_m5 | validation_net | validation_profit_factor | validation_trade_density | oos_net | oos_profit_factor | oos_trade_density | strict_cross_split_success |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| short_h3_m2__full58(전체_58)__et6_l80_n96(엑스트라트리6_잎80_96) | short_h3_m2 | full58(전체_58) | density_8_0 | 8 | 77.23 | 1.0620695198 | 1.6775956284 | 218.16 | 1.2733303682 | 1.6564885496 | failed(실패) |
| short_h12_m5__short_regime_33(숏_국면_33)__et6_l80_n96(엑스트라트리6_잎80_96) | short_h12_m5 | short_regime_33(숏_국면_33) | density_4_0 | 8 | 38.973 | 1.0530011981 | 0.9508196721 | 203.86 | 1.4979530821 | 0.9694656489 | failed(실패) |
| short_h3_m2__full58(전체_58)__et6_l80_n96(엑스트라트리6_잎80_96) | short_h3_m2 | full58(전체_58) | density_6_0 | 8 | 223.098 | 1.241044485 | 1.3333333333 | 134.681 | 1.1853448217 | 1.4045801527 | failed(실패) |
| short_h12_m5__full58(전체_58)__et6_l80_n96(엑스트라트리6_잎80_96) | short_h12_m5 | full58(전체_58) | density_4_0 | 2 | 105.299 | 1.1541922985 | 1.7431693989 | 133.201 | 1.2594209814 | 1.9389312977 | failed(실패) |
| short_h12_m5__full58(전체_58)__et6_l80_n96(엑스트라트리6_잎80_96) | short_h12_m5 | full58(전체_58) | density_4_0 | 8 | 77.466 | 1.1201334299 | 0.868852459 | 152.268 | 1.3164089286 | 0.9541984733 | failed(실패) |
| short_h3_m2__short_regime_33(숏_국면_33)__et6_l80_n96(엑스트라트리6_잎80_96) | short_h3_m2 | short_regime_33(숏_국면_33) | density_4_0 | 8 | 5.144 | 1.0066851644 | 1.0765027322 | 173.439 | 1.3187589941 | 0.9312977099 | failed(실패) |
| short_h6_m3__short_regime_33(숏_국면_33)__et6_l80_n96(엑스트라트리6_잎80_96) | short_h6_m3 | short_regime_33(숏_국면_33) | density_6_0 | 6 | -133.5 | 0.8873683855 | 1.6721311475 | 262.867 | 1.3486147158 | 1.7786259542 | failed(실패) |
| short_h6_m3__short_regime_33(숏_국면_33)__et6_l80_n96(엑스트라트리6_잎80_96) | short_h6_m3 | short_regime_33(숏_국면_33) | density_6_0 | 8 | -23.175 | 0.9786749679 | 1.4699453552 | 216.116 | 1.2935668654 | 1.5496183206 | failed(실패) |

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| scope_completion_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DP/short_source_model_trade_shape_surface.csv | DP surface(표면)와 선택 요약을 작성했습니다. |
| input_lineage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DP/input_manifest.csv | 입력 계보가 연결됐습니다. |
| data_integrity_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DP/data_integrity_audit.csv | 시점/분할/피처 검사를 통과했습니다. |
| training_split_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DP/model_scorecard.csv | train split(학습 분할)로 모델을 적합하고 validation/OOS(검증/표본외)를 분리했습니다. |
| model_artifact_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DP/model_artifact_manifest.csv | joblib/ONNX(잡립/온엑스) 산출물 목록이 있습니다. |
| onnx_smoke_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DP/onnx_smoke_report.csv | ONNX smoke(온엑스 스모크) 통과 모델이 있습니다. |
| candidate_surface_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DP/short_source_model_trade_shape_surface.csv | 후보 표면을 기록했습니다. |
| strict_contract_decision_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DP/run364DQ_review_queue.csv | 엄격 후보 수와 다음 검토를 기록했습니다. |
| no_trade_splitting_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DP/data_integrity_audit.csv | 단일 포지션 재생입니다. |
| receipt_coverage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DP/run_evidence_receipt.json | 필수 영수증이 있습니다. |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DP/required_gate_coverage_audit.csv | 필수 게이트가 종료 기록에 연결됐습니다. |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DP/claim_boundary_receipt.json | 권위/승격/목표 달성 주장을 차단했습니다. |

## Boundary(경계)

This is scout-only(스카우트 전용) with ONNX smoke(온엑스 스모크) only. MT5 execution(MT5 실행), runtime package(런타임 패키지), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 안 함)`입니다.
