# run286C Trade Density Curve Quality Review(286C 거래 밀도/곡선 품질 검토)

- stage_id(단계 ID): `286_onnx_candidate_campaign__trade_density_curve_quality_rebuild`
- run_id(실행 ID): `run286C_review_trade_density_curve_quality_mt5_probe_v1`
- status(상태): `completed_trade_density_curve_quality_review_no_candidate_stage287_opened`
- judgment(판정): `density_scale_found_but_curve_pockets_fail_no_candidate`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Stage287 seeds(287단계 씨앗): `2`
- next_action(다음 행동): `run287A_design_density_scale_curve_pocket_rebuild_packet`

## Review Read(검토 판독)

- `cp286A_entry_dense_direct_surface`: validation(검증) `-75.42` / `2.57` trades/day(일 거래), OOS(표본외) `420.98` / `2.76` trades/day(일 거래), curve gate(곡선 게이트) `failed`.
- `cp286B_trend_density_thr58_surface`: validation(검증) `118.89` / `3.53` trades/day(일 거래), OOS(표본외) `614.73` / `3.82` trades/day(일 거래), curve gate(곡선 게이트) `failed`.
- `cp286C_trend_density_thr52_surface`: validation(검증) `54.39` / `4.83` trades/day(일 거래), OOS(표본외) `533.58` / `5.07` trades/day(일 거래), curve gate(곡선 게이트) `failed`.
- `cp286D_trend_density_thr48_surface`: validation(검증) `202.24` / `5.83` trades/day(일 거래), OOS(표본외) `670.53` / `6.05` trades/day(일 거래), curve gate(곡선 게이트) `failed`.
- `cp286E_macro_blend_density_surface`: validation(검증) `369.73` / `5.22` trades/day(일 거래), OOS(표본외) `324.04` / `5.34` trades/day(일 거래), curve gate(곡선 게이트) `failed`.

Stage286(286단계)는 density/scale clue(밀도/규모 단서)를 찾았지만 smooth curve(매끄러운 곡선) 조건은 통과하지 못했다.
Effect(효과): cp286D/cp286E(286D/286E 후보)는 selected candidate(선택 후보)가 아니라 Stage287(287단계) curve-pocket rebuild(곡선 포켓 재구성) seed(씨앗)로만 넘긴다.

## Boundary(경계)

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`

Effect(효과): 운영 의미나 ONNX(온엑스) 진행을 주장하지 않고, 다음 단계에서 새 구조로 검증한다.
