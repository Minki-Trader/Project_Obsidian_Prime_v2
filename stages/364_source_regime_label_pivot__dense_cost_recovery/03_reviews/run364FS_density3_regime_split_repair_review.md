# run364FS Density3 Regime Split Repair Review(밀도3 국면 분할 수리 검토)

Created(생성): 2026-06-07T06:02:58Z

Action(행동): FR density3 regime split repair(FR 밀도3 국면 분할 수리)를 package decision(패키지 결정), failure memory(실패 기억), FT queue(FT 대기열)로 검토했습니다.

Effect(효과): validation profit(검증 수익) 회수 단서는 보존하고, density3(밀도3) 소실은 다음 재확장 조건으로 고정합니다.

- judgment(판정): `negative_density3_regime_split_repair_review_profit_salvage_density_lost_no_package_no_authority`
- selected model(선택 모델): `fr_sym_h2_m1p5__fr_regime_macro__rf8_l20_n160`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `188.314` / `1.1749938204` / `2.393442623`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `-6.562` / `0.9901955218` / `2.2824427481`
- OOS cost0.9(표본외 비용0.9): `-185.962`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `181.752` / `2.347133758` / `-260.448` / `0.7598371777`
- validation_positive_density3_count(검증 양수 밀도3 수): `0`
- density3_all_splits_count(전 분할 밀도3 수): `0`
- density3_all_splits_valpos_oospos_count(전 분할 양수 밀도3 수): `0`
- oos_pf125_cost09_count(표본외 PF125와 비용0.9 수): `3540`
- next_run_id(다음 실행 ID): `run364FT_train_h17_oos108_pf125_regime_profit_density_reexpand_without_db_v1`

## Surface Diagnostic(표면 진단)

| diagnostic_id | model_id | validation_net | validation_density | oos_profit_factor | oos_cost09_net | oos_density | combined_density | combined_cost09_net | combined_short_share | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| fs_selected_candidate(선택 후보) | fr_sym_h2_m1p5__fr_regime_macro__rf8_l20_n160 | 188.314 | 2.393442623 | 0.9901955218 | -185.962 | 2.2824427481 | 2.347133758 | -260.448 | 0.7598371777 | 선택 후보는 validation(검증) 수익을 크게 살렸지만 density(밀도)가 낮고 OOS(표본외)가 약한 손실입니다. |
| fs_best_oos_positive(표본외 양수 상위) | fr_asym_h2_l1p5_s2p5__fr_regime_macro__rf8_l20_n160 | 106.852 | 2.3333333333 | 1.0315018701 | -146.468 | 2.1221374046 | 2.2452229299 | -295.816 | 0.8340425532 | OOS(표본외) 양수 후보는 있지만 density3(밀도3)까지 확장되지 않았습니다. |
| fs_best_validation_positive(검증 양수 상위) | fr_sym_h2_m1p5__fr_regime_macro__rf8_l20_n160 | 188.314 | 2.393442623 | 0.9901955218 | -185.962 | 2.2824427481 | 2.347133758 | -260.448 | 0.7598371777 | 검증 양수 후보는 FR의 회수 단서입니다. |
| fs_density3_all_splits(전 분할 밀도3) |  |  |  |  |  |  |  |  |  | FR 표면에는 전 분할 density3(밀도3)가 남지 않았습니다. |
| fs_oos_pf125_cost09(표본외 PF125 비용0.9) | fr_sym_h2_m1p5__fr_regime_macro__et7_l10_n160 | 85.501 | 1.8469945355 | 1.3399474638 | 46.639 | 1.6870229008 | 1.7802547771 | -70.66 | 0.6529516995 | OOS PF125/cost0.9(표본외 수익 팩터 1.25/비용0.9)는 여전히 저밀도 탐색 단서입니다. |

## Attribution(귀속)

| attribution_id | observed | driver | severity | effect |
| --- | --- | --- | --- | --- |
| fs01_profit_salvage_density_lost | selected_validation_net=188.314; selected_oos_net=-6.562; selected_density=2.393442623/2.2824427481/2.347133758 | regime split(국면 분할)이 손익 단서는 살렸지만 거래 밀도는 3/day(일 3회)에서 멀어졌습니다. | salvage_with_failure(회수와 실패) | FT는 이 수익 단서를 보존하면서 density(밀도)를 재확장합니다. |
| fs02_density3_disappeared | density3_all_splits_count=0; validation_positive_density3_count=0 | FR filters(FR 필터)가 너무 좁아져 high-density rows(고밀도 행)가 사라졌습니다. | high(높음) | 다음 run(실행)은 국면 필터를 유지하되 broad re-expand(넓은 재확장)를 시도합니다. |
| fs03_cost_scout_low_density | oos_pf125_cost09_count=3540; oos_pf125_cost09_density3_count=0 | OOS PF125/cost0.9(표본외 수익 팩터 1.25/비용0.9)는 계속 저밀도 단서입니다. | medium(중간) | 비용 단서는 scout clue(탐색 단서)로만 유지하고 package(패키지)는 열지 않습니다. |
| fs04_onnx_smoke_not_authority | onnx_smoke_pass_rows=36; new_mt5_execution=not_run | ONNX smoke(온엑스 스모크)는 변환 일치만 확인했고 MT5(메타트레이더5) 실행 근거는 아닙니다. | guardrail(가드레일) | runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)를 차단합니다. |

## Package Decision(패키지 결정)

| decision | reason | runtime_package | new_mt5_execution | effect |
| --- | --- | --- | --- | --- |
| rejected(거절) | density3_all_splits_count=0; selected_oos_net_negative; strict_candidate_count=0 | not_opened | not_run | 수익 단서가 있어도 trade density(거래 밀도)가 낮은 후보를 MT5(메타트레이더5) 운영 후보로 올리지 않습니다. |

## Failure Memory(실패 기억)

| memory_id | failed_boundary | why_failed | salvage_value | reopen_condition |
| --- | --- | --- | --- | --- |
| fs01_regime_profit_salvage_density_lost | profit salvage with density3(수익 회수와 밀도3 동시 충족) | selected_validation_net=188.314; selected_oos_net=-6.562; density3_all_splits_count=0; selected_density=2.393442623/2.2824427481/2.347133758 | selected_combined_net=181.752; selected_oos_pf=0.9901955218; max_oos_pf=2.0980072565; oos_pf125_cost09_count=3540 | profit salvage remains while combined/validation/OOS density re-expand toward 3/day(수익 단서 보존 상태에서 합산/검증/표본외 밀도가 3/day로 재확장될 때) |

## Next Queue(다음 대기열)

| queue_id | hypothesis | required_preserve | required_repair | effect |
| --- | --- | --- | --- | --- |
| ft01_regime_profit_density_reexpand | FR의 validation profit(검증 수익) 단서를 유지하면서 hour/filter breadth(시간/필터 폭)를 넓히면 density(밀도)를 3/day(일 3회) 쪽으로 재확장할 수 있습니다. | validation_net>0, combined_net>0, OOS near breakeven or better(검증/합산 순수익 양수와 표본외 손익 개선) | validation_density>=3, oos_density>=3, combined_density>=3, density3_all_splits_valpos_oospos_count>0(전 분할 밀도3과 양수 수익 회복) | FT는 수익 단서를 버리지 않고 거래수 바닥을 다시 넓힙니다. |

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| input_lineage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FS/input_manifest.csv | FR 입력 계보가 FS 검토에 연결됐습니다. |
| parent_gate_inheritance_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FR/required_gate_coverage_audit.csv | FR gate(게이트) 통과 상태를 상속했습니다. |
| kpi_contract_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FS/fs_review_summary.csv | KPI(핵심 성과 지표)와 package decision(패키지 결정)을 분리했습니다. |
| surface_overlap_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FS/fs_surface_diagnostic.csv | 수익 회수와 밀도 손실을 함께 기록했습니다. |
| failure_attribution_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FS/fs_failure_attribution.csv | 실패 원인을 수익 회수, 밀도 손실, 비용 단서, 권위 경계로 나눴습니다. |
| package_decision_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FS/package_decision.csv | runtime package(런타임 패키지) 거절 근거를 기록했습니다. |
| failure_memory_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FS/fs_failure_memory.csv | 다음 run(실행)이 반복하지 말아야 할 실패 기억을 기록했습니다. |
| next_queue_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FS/fs_ft_queue.csv | FT regime profit density reexpand(FT 국면 수익 밀도 재확장) 대기열을 만들었습니다. |
| receipt_coverage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FS/result_judgment_receipt.json | 필수 receipt(영수증)가 있습니다. |
| paired_tier_record_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv | Tier A/Tier B/Tier A+B 행을 장부에 남겼습니다. |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FS/required_gate_coverage_audit.csv | 필수 gate(게이트)가 종료 기록에 연결됐습니다. |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FS/claim_boundary_receipt.json | 권위/승격/실거래/목표 달성 주장을 차단했습니다. |

Runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
