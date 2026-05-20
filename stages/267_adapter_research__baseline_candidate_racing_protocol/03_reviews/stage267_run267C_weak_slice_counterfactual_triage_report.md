# Stage267 Run267C Weak-Slice Counterfactual Triage(267단계 267C 약점 구간 반사실 선별)

- action(행동): run267B(267B 실행) 2024 routed trade records(라우팅 거래 기록)에서 약한 구간을 제거하는 counterfactual(반사실) KPI(핵심 성과 지표)를 계산했다.
- effect(효과): 단순히 약한 월/세션을 지우면 좋아 보이는지, 아니면 trade count collapse(거래 수 붕괴)로 착시가 생기는지 분리했다.
- counterfactual_rows(반사실 행): `35`
- intersection_rows(교차 구간 행): `30`
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`

## Candidate Triage(후보 선별)

| candidate(후보) | role(역할) | baseline net(기준 순수익) | baseline PF(기준 수익 팩터) | baseline DD%(기준 손실폭%) | best counterfactual(최선 반사실) | net delta(순수익 변화) | retention(유지율) | read(판독) |
| --- | --- | ---: | ---: | ---: | --- | ---: | ---: | --- |
| `s262_lowrank_inner_half_filter` | `validation_heavy` | 44.49 | 1.024065 | 39.081551 | `cf_remove_vol_low_or_late` | 352.79 | 0.607955 | `broad_fragility_or_overprune` |
| `s264_allow_inner_all_oos_anchor` | `oos_anchor` | 87.07 | 1.046009 | 35.503222 | `cf_remove_vol_low_or_late` | 335.08 | 0.610169 | `broad_fragility_or_overprune` |
| `s264_lowrank_control` | `defensive_control` | 71.34 | 1.038612 | 36.172154 | `cf_remove_all_common_weak_axes` | 332.79 | 0.451429 | `broad_fragility_or_overprune` |
| `s264_allow_inner_high_quarter` | `core_challenger` | 95.56 | 1.050106 | 35.284867 | `cf_remove_vol_low_or_late` | 332.63 | 0.611898 | `broad_fragility_or_overprune` |
| `s258_short_tight_control` | `stress_challenger` | 102.89 | 1.046751 | 39.85108 | `cf_remove_vol_low_or_july` | 314.04 | 0.637566 | `broad_fragility_or_overprune` |

## Top Counterfactual Deltas(상위 반사실 변화)

| candidate(후보) | intervention(개입) | kept trades(유지 거래) | net delta(순수익 변화) | DD delta(손실폭 변화) | read(판독) |
| --- | --- | ---: | ---: | ---: | --- |
| `s262_lih` | `cf_remove_vol_low_or_late` | 214 | 352.79 | -28.126784 | `overpruned_not_candidate_solution` |
| `s262_lih` | `cf_remove_all_common_weak_axes` | 158 | 352.63 | -30.919587 | `overpruned_not_candidate_solution` |
| `s264_aia` | `cf_remove_vol_low_or_late` | 216 | 335.08 | -24.356973 | `overpruned_not_candidate_solution` |
| `s264_aia` | `cf_remove_all_common_weak_axes` | 160 | 333.69 | -27.10739 | `overpruned_not_candidate_solution` |
| `s264_lc` | `cf_remove_all_common_weak_axes` | 158 | 332.79 | -28.010191 | `overpruned_not_candidate_solution` |
| `s264_lc` | `cf_remove_vol_low_or_late` | 214 | 332.68 | -25.217388 | `overpruned_not_candidate_solution` |
| `s264_aih` | `cf_remove_vol_low_or_late` | 216 | 332.63 | -24.036483 | `overpruned_not_candidate_solution` |
| `s264_aih` | `cf_remove_all_common_weak_axes` | 160 | 331.83 | -26.834858 | `overpruned_not_candidate_solution` |
| `s258_stc` | `cf_remove_vol_low_or_july` | 241 | 314.04 | -19.0404 | `overpruned_not_candidate_solution` |
| `s258_stc` | `cf_remove_vol_low_or_late` | 225 | 312.3 | -28.652421 | `overpruned_not_candidate_solution` |

## Boundary(경계)

- 이 결과는 closed trade counterfactual(청산 거래 반사실)이다. Effect(효과): 실제 feature ablation(피처 제거), similar replacement(유사 대체), MT5 rerun(MT5 재실행)을 대체하지 않는다.
- naive filter(단순 필터)가 좋아 보여도 바로 후보 선택(selected candidate, 선택 후보)이나 ONNX readiness(ONNX 준비)로 이어지지 않는다.

## Judgment(판정)

- result_subject(판정 대상): Stage267 run267C weak-slice counterfactual triage(약점 구간 반사실 선별).
- evidence_available(사용 가능 근거): run267B trade records(거래 기록), counterfactual KPI(반사실 핵심 성과 지표), intersection KPI(교차 구간 핵심 성과 지표), candidate summary(후보 요약).
- evidence_missing(부족 근거): actual MT5 ablation/replacement reruns(실제 MT5 제거/대체 재실행), full feature ablation(전체 피처 제거), similar feature replacement(유사 피처 대체), Adapter validation(어댑터 검증), ONNX parity(ONNX 동등성).
- judgment_label(판정 라벨): `exploratory_counterfactual_only`.
- selected_candidate(선택 후보): `none`.
- ONNX readiness(ONNX 준비): `not_claimed`.
- next_condition(다음 조건): `run267C_materialize_p0_mt5_variants_from_counterfactual_triage`.
