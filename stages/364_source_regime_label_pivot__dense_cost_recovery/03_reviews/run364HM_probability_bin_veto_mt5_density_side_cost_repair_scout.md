# run364HM Probability-Bin Veto MT5 Density/Side/Cost Repair Scout(확률 구간 거부 MT5 밀도/방향/비용 수리 탐색)

Updated(갱신): 2026-06-09T11:54:24Z

## Result(결과)

Action(행동): Stage364 prior surfaces(Stage364 이전 표면)를 모두 스캔하고, HL MT5 density lift ratio(HL MT5 밀도 상승 비율) `1.3251833741`를 보수적 estimate(추정)로 적용했습니다.

Effect(효과): direct strict pass(직접 엄격 통과)는 `0`개로 없지만, runtime-scaled repair seed(런타임 스케일 수리 씨앗)는 `1`개 확인했습니다.

- selected source(선택 원천): `run364FJ`
- selected model(선택 모델): `fj_sym_h2_m1p75__fj_behavior_density_cost__et8_l18_n160`
- OOS net/PF/density/cost0.6(표본외 순수익/수익 팩터/밀도/비용0.6): `333.32` / `1.4709758917` / `2.5496183206` / `233.12`
- combined net/trades/density/cost0.9/short share(합산 순수익/거래수/밀도/비용0.9/숏 비중): `449.501` / `724.0` / `2.3057324841` / `15.101` / `0.5483425414`
- runtime density estimate(런타임 밀도 추정): `3.055518353`
- selected ONNX(선택 ONNX, 온엑스): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FJ/onnx/fj_sym_h2_m1p75_fj_behavior_density_cost_et8_l18_n160.onnx`

Judgment(판정): `positive_proxy_scaled_density_side_cost_repair_seed_review_required_no_new_mt5_no_authority`.

## Failure Attribution(실패 귀속)

| check | threshold | pass_count | fail_count | effect |
| --- | --- | --- | --- | --- |
| direct_density_pass(직접 밀도 통과) | combined and OOS density >= 3/day(합산 및 표본외 밀도 일 3회 이상) | 3322 | 148965 | 병목을 다음 review(검토)와 package(패키지) 조건으로 분리합니다. |
| scaled_density_pass(스케일 밀도 통과) | combined density * HL ratio >= 3/day(HL 비율 적용 밀도 일 3회 이상) | 10697 | 141590 | 병목을 다음 review(검토)와 package(패키지) 조건으로 분리합니다. |
| profit_pass(수익 통과) | validation/OOS/combined net > 0(검증/표본외/합산 순수익 양수) | 43125 | 109162 | 병목을 다음 review(검토)와 package(패키지) 조건으로 분리합니다. |
| pf_pass(PF 통과) | OOS PF >=1.25 and min split PF >=1.05(표본외 수익 팩터 1.25 이상 및 분할 최소 1.05 이상) | 13864 | 138423 | 병목을 다음 review(검토)와 package(패키지) 조건으로 분리합니다. |
| cost_pass(비용 통과) | OOS cost0.6 >0 and combined cost0.9 >=0(표본외 비용0.6 양수 및 합산 비용0.9 0 이상) | 15846 | 136441 | 병목을 다음 review(검토)와 package(패키지) 조건으로 분리합니다. |
| side_caution_pass(방향 주의 통과) | short share <=0.70(숏 비중 0.70 이하) | 27182 | 125105 | 병목을 다음 review(검토)와 package(패키지) 조건으로 분리합니다. |
| side_target_pass(방향 목표 통과) | short share <=0.65(숏 비중 0.65 이하) | 14577 | 137710 | 병목을 다음 review(검토)와 package(패키지) 조건으로 분리합니다. |
| direct_strict_pass(직접 엄격 통과) | direct density + profit + PF + cost + side(직접 밀도와 수익/PF/비용/방향 동시 통과) | 0 | 152287 | 병목을 다음 review(검토)와 package(패키지) 조건으로 분리합니다. |
| runtime_scaled_repair_pass(런타임 스케일 수리 통과) | HL density ratio seed + profit/PF/cost/side(HL 밀도 비율 씨앗과 수익/PF/비용/방향 동시 통과) | 1 | 152286 | 병목을 다음 review(검토)와 package(패키지) 조건으로 분리합니다. |

## Route Parity Decision(라우트 동등성 결정)

| route_question | decision | evidence | effect |
| --- | --- | --- | --- |
| HJ/HK dual-source route(HJ/HK 이중 원천 라우트) | partial_parity_not_reused_as_authority(부분 동등성을 권위로 재사용 안 함) | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HL/runtime_route_mix_review.csv | fallback-after-flat(플랫 이후 대체)와 Python score switch(Python 점수 전환)의 차이를 다음 패키지에서 숨기지 않습니다. |
| HM selected seed(HM 선택 씨앗) | single_source_fj_model_preferred_for_next_package_review(단일 FJ 모델을 다음 패키지 검토에 우선) | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FJ/onnx/fj_sym_h2_m1p75_fj_behavior_density_cost_et8_l18_n160.onnx | dual-source fallback(이중 원천 대체) 복잡도를 줄이고, probability-bin veto(확률 구간 거부)는 단일 모델 확률 구간에서 다시 검토합니다. |
| HN next decision(HN 다음 결정) | review_package_or_reseed_boundary(패키지 또는 재시드 경계 검토) | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HM/selected_hm_seed.json | scaled density estimate(스케일 밀도 추정)가 너무 약하면 직접 3/day source(직접 일 3회 원천) 재학습으로 전환합니다. |

## Next Queue(다음 대기열)

| queue_item | seed | target | avoid | effect |
| --- | --- | --- | --- | --- |
| HN_review_selected_scaled_seed(HN 선택 스케일 씨앗 검토) | fj_sym_h2_m1p75__fj_behavior_density_cost__et8_l18_n160 | validate package readiness(패키지 준비성 검토): ONNX(온엑스), feature order(피처 순서), no-trade-splitting(거래 쪼개기 금지) | do not call scaled density MT5 proof(스케일 밀도를 MT5 증명으로 부르지 않음) | FJ seed(FJ 씨앗)를 패키지로 열 수 있는지 좁게 판정합니다. |
| single_source_probability_bin_veto_package_candidate(단일 원천 확률 구간 거부 패키지 후보) | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FJ/onnx/fj_sym_h2_m1p75_fj_behavior_density_cost_et8_l18_n160.onnx | if HN passes, materialize MT5 runtime package(HN 통과 시 MT5 런타임 패키지 물질화) | do not reuse GZ+HB fallback partial parity(GZ+HB 대체 부분 동등성 재사용 금지) | route parity(라우트 동등성)를 더 단순하게 닫을 수 있습니다. |
| direct_density_cost_side_reseed_fallback(직접 밀도/비용/방향 재시드 대체) | direct_proxy_density>=3/day required(직접 프록시 밀도 일 3회 이상 필요) | if HN rejects scaled seed, train new direct-density source(HN이 스케일 씨앗을 거부하면 직접 고밀도 원천 재학습) | repeat micro threshold search(미세 임계값 반복) | scaled clue(스케일 단서)가 약할 때 다음 공격 탐색이 바로 이어집니다. |

## Boundary(경계)

This is not a new MT5 execution(새 MT5 실행 아님), not a runtime package(런타임 패키지 아님), and not runtime authority(런타임 권위 아님). HL ratio(HL 비율)는 candidate screening(후보 선별)에만 씁니다.

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| parent_hl_lineage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HL/final_decision.json | HL 입력 계보를 확인했습니다. |
| surface_inventory_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HM/hm_prior_surface_inventory.csv | 이전 표면을 스캔했습니다. |
| direct_strict_absence_recorded_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HM/hm_failure_attribution.csv | 직접 엄격 통과 0개를 누락 없이 기록했습니다. |
| runtime_scaled_seed_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HM/hm_runtime_scaled_repair_candidates.csv | HL 비율 적용 수리 씨앗을 확인했습니다. |
| selected_seed_artifact_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HM/selected_hm_seed.json | 선택 씨앗의 ONNX(온엑스)와 smoke(스모크)를 확인했습니다. |
| no_trade_splitting_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HM/selected_hm_seed_trade_tape.csv | 거래 쪼개기 금지 경계를 확인했습니다. |
| data_integrity_boundary_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HM/data_integrity_receipt.json | 데이터 경계를 기록했습니다. |
| route_parity_decision_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HM/hm_route_parity_decision.csv | 라우트 동등성 결정을 기록했습니다. |
| paired_tier_record_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv | Tier A/Tier B/Tier A+B 기록 경계를 남깁니다. |
| artifact_lineage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HM/artifact_lineage_receipt.json | 산출물 계보를 연결했습니다. |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HM/required_gate_coverage_audit.csv | 필수 게이트를 감사했습니다. |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HM/claim_boundary_receipt.json | 운영 권위 주장을 막았습니다. |
