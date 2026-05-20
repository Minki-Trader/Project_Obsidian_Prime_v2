# Stage267 Historical 2024 Visual/Ablation Design(267단계 2024 시각/제거 설계)

- action(행동): MT5 chart PNG(MT5 차트 이미지) 10개를 hash(해시), 크기, 픽셀 범위로 sanity check(기초 점검)하고, 2024 약점에서 다음 ablation/replacement(제거/대체) 실험 설계를 만들었다.
- effect(효과): 후보를 고르지 않고, 약점이 어디서 다시 검증되어야 하는지 실행 가능한 질문으로 바꾸었다.
- visual_manifest_rows(시각 목록 행): `10`
- design_rows(설계 행): `10`
- visual_status(시각 상태): `completed_visual_artifact_sanity_not_quality_approval`
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`

## Visual Artifact Sanity(시각 산출물 기초 점검)

| candidate(후보) | role(역할) | route(경로) | net(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭%) | curve grade(곡선 등급) | chart status(차트 상태) |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| `s258_short_tight_control` | `stress_challenger` | `routed_total` | 102.89 | 1.05 | 378 | 40.43 | `D_fragile` | `nonblank_png_verified` |
| `s262_lowrank_inner_half_filter` | `validation_heavy` | `routed_total` | 44.49 | 1.02 | 352 | 40.13 | `D_fragile` | `nonblank_png_verified` |
| `s264_allow_inner_all_oos_anchor` | `oos_anchor` | `routed_total` | 87.07 | 1.05 | 354 | 36.9 | `C_watch` | `nonblank_png_verified` |
| `s264_allow_inner_high_quarter` | `core_challenger` | `routed_total` | 95.56 | 1.05 | 353 | 36.68 | `C_watch` | `nonblank_png_verified` |
| `s264_lowrank_control` | `defensive_control` | `routed_total` | 71.34 | 1.04 | 350 | 37.52 | `C_watch` | `nonblank_png_verified` |

Read(판독): chart PNG(MT5 차트 이미지)는 모두 비어 있지 않은 파일로 확인됐다. Effect(효과): 다음 rerun(재실행)에서 balance/equity curve(잔액/평가금 곡선)를 대조할 수 있는 시각 산출물 신원은 확보했다.

Boundary(경계): 이 점검은 그림 파일이 존재하고 열리는지 확인한 것이다. curve(곡선)가 예쁘거나 후보가 강하다는 판정은 아니다.

## Prioritized Design(우선 설계)

| design(설계) | type(유형) | weakness(약점) | priority(우선순위) | status(상태) |
| --- | --- | --- | --- | --- |
| `d01_vol_low_volatility_bandwidth_ablation` | `feature_category_ablation` | `volatility_regime:vol_low` | `P0` | `designed_not_executed` |
| `d02_vol_low_atr_to_historical_vol_replacement` | `similar_feature_replacement` | `volatility_regime:vol_low` | `P0` | `designed_not_executed` |
| `d03_adx_20_25_trend_strength_ablation` | `feature_category_ablation` | `adx_bucket:adx_20_25` | `P1` | `designed_not_executed` |
| `d04_adx_to_di_vortex_supertrend_replacement` | `similar_feature_replacement` | `adx_bucket:adx_20_25` | `P1` | `designed_not_executed` |
| `d05_july_2024_holdout_stress` | `period_stress_holdout` | `month:2024-07` | `P0` | `designed_not_executed` |
| `d06_monday_session_timing_ablation` | `feature_category_ablation` | `weekday:Monday` | `P1` | `designed_not_executed` |
| `d07_late_session_interaction_engineering` | `feature_engineering_design` | `session_slice:late` | `P0` | `designed_not_executed` |
| `d08_rank_gate_compressed_surface_ablation` | `compressed_gate_ablation` | `candidate_gate:rank_inner_outer_bucket` | `P0` | `designed_not_executed` |
| `d09_chron_mid_weakness_decomposition` | `time_slice_decomposition` | `chron_segment:chron_mid` | `P1` | `designed_not_executed` |
| `d10_breadth_macro_context_replacement` | `similar_feature_replacement` | `context_proxy:breadth_macro_optional` | `P2` | `designed_not_executed` |

## Judgment(판정)

- result_subject(판정 대상): Stage267 run267B 2024 visual artifact sanity(시각 산출물 기초 점검) and ablation/replacement design(제거/대체 설계).
- evidence_available(사용 가능 근거): MT5 chart PNG(MT5 차트 이미지), visual manifest(시각 목록), time-slice KPI(시간 구간 핵심 성과 지표), candidate weakness summary(후보 약점 요약), design CSV/JSON(설계 표/JSON).
- evidence_missing(부족 근거): actual ablation/replacement reruns(실제 제거/대체 재실행), Adapter validation(어댑터 검증), ONNX parity(ONNX 동등성), runtime reproduction(런타임 재현).
- judgment_label(판정 라벨): `exploratory_design_completed`.
- selected_candidate(선택 후보): `none`.
- selected_research_baseline(선택 연구 기준선): `none`.
- ONNX readiness(ONNX 준비): `not_claimed`.
- next_condition(다음 조건): `run267C_stage267_execute_prioritized_ablation_replacement_variants`.
