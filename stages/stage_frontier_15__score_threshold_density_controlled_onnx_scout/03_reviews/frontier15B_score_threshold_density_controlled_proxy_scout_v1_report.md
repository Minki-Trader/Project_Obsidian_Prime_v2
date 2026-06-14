# Frontier15B Score Threshold Density Controlled Proxy Scout(프론티어15B 점수 임계값 빈도 통제 프록시 탐색)

Updated(갱신): 2026-06-14T01:55:32Z

Status(상태): `score_threshold_no_strict_clue_no_authority`

Judgment(판정): `negative_memory_candidate(부정 기억 후보)`

Action(행동): F14(프론티어14) opportunity labels(기회 라벨)을 control(통제)로 두고, ONNX probability score threshold(온엑스 확률 점수 임계값) 9칸을 학습 전용 빈도 기준으로 평가했습니다.

Effect(효과): argmax baseline(최대확률 기준행)과 score threshold signal(점수 임계값 신호)을 나란히 기록해 density cliff(빈도 절벽)가 decision contract(결정 계약)에서 고쳐지는지 확인했습니다.

## Result Summary(결과 요약)

- candidate rows(후보 행): `81`
- primary strict rows(1순위 엄격 행): `0`
- secondary strict-like rows(보조 엄격 유사 행): `0`
- preserved clue rows(보존 단서 행): `0`
- best candidate(최고 후보): `f14b_day_q6_h8__lr_plain__utility_tilt__target5`
- best validation PF/density/DD(최고 검증 수익 팩터/빈도/손실폭): `1.00637` / `5.97814` / `17.506%`
- best OOS PF/density/DD(최고 표본밖 수익 팩터/빈도/손실폭): `1.04656` / `5.58779` / `18.8668%`
- best primary candidate(최고 1순위 후보): `f14b_cash_q10_h12__rf_bal__edge_margin__target8`
- primary validation/OOS PF-density-DD(1순위 검증/표본밖 수익 팩터-빈도-손실폭): `0.895191` / `7.11475` / `21.8306%` and `1.07124` / `6.25191` / `11.834%`

## Artifacts(산출물)

- candidate summary(후보 요약): `stages/stage_frontier_15__score_threshold_density_controlled_onnx_scout/02_runs/frontier15B_score_threshold_density_controlled_proxy_scout_v1/candidate_summary.csv`
- threshold manifest(임계값 목록): `stages/stage_frontier_15__score_threshold_density_controlled_onnx_scout/02_runs/frontier15B_score_threshold_density_controlled_proxy_scout_v1/threshold_manifest.csv`
- argmax baseline metrics(최대확률 기준 지표): `stages/stage_frontier_15__score_threshold_density_controlled_onnx_scout/02_runs/frontier15B_score_threshold_density_controlled_proxy_scout_v1/argmax_baseline_metrics.csv`
- label/model density gap(라벨/모델 빈도 격차): `stages/stage_frontier_15__score_threshold_density_controlled_onnx_scout/02_runs/frontier15B_score_threshold_density_controlled_proxy_scout_v1/label_model_density_gap.csv`
- ONNX parity(온엑스 동등성): `stages/stage_frontier_15__score_threshold_density_controlled_onnx_scout/02_runs/frontier15B_score_threshold_density_controlled_proxy_scout_v1/onnx_parity.csv`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
