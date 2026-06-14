# Frontier16B Edge Quality Risk Veto Proxy Scout(프론티어16B 엣지 품질 위험 배제 프록시 탐색)

Updated(갱신): 2026-06-14T02:25:50Z

Status(상태): `edge_quality_risk_veto_no_strict_clue_no_authority`

Judgment(판정): `negative_memory_candidate(부정 기억 후보)`

## Action And Effect(행동과 효과)

Action(행동): 3개 risk-quality label variants(위험 품질 라벨 변형)를 학습하고 `edge_margin__target8` 단일 decision cell(결정 칸)로 평가했습니다.

Effect(효과): F15(프론티어15)의 density transfer(빈도 전이)를 calibration clue(보정 단서)로만 쓰며, PF/DD/smoothness(수익 팩터/손실폭/매끄러움)가 함께 좋아지는지 확인했습니다.

## Result Summary(결과 요약)

- candidate rows(후보 행): `9`
- strict rows(엄격 행): `0`
- preserved clue rows(보존 단서 행): `0`
- best candidate(최고 후보): `f16b_edge_h8_t0p30_cap0p45_early0p25__rf_bal__edge_margin__target8`
- validation PF/density/DD(검증 수익 팩터/빈도/손실폭): `1.06795` / `5.65574` / `12.9599%`
- OOS PF/density/DD(표본밖 수익 팩터/빈도/손실폭): `0.942216` / `5.45802` / `12.8032%`
- worst subperiod DD(최악 하위기간 손실폭): `11.3056%`

## Artifacts(산출물)

- candidate summary(후보 요약): `stages/stage_frontier_16__edge_quality_risk_veto_density_transfer_onnx_scout/02_runs/frontier16B_edge_quality_risk_veto_proxy_scout_v1/candidate_summary.csv`
- threshold manifest(임계값 목록): `stages/stage_frontier_16__edge_quality_risk_veto_density_transfer_onnx_scout/02_runs/frontier16B_edge_quality_risk_veto_proxy_scout_v1/threshold_manifest.csv`
- density transfer audit(빈도 전이 감사): `stages/stage_frontier_16__edge_quality_risk_veto_density_transfer_onnx_scout/02_runs/frontier16B_edge_quality_risk_veto_proxy_scout_v1/density_transfer_audit.csv`
- argmax baseline metrics(최대확률 기준선 지표): `stages/stage_frontier_16__edge_quality_risk_veto_density_transfer_onnx_scout/02_runs/frontier16B_edge_quality_risk_veto_proxy_scout_v1/argmax_baseline_metrics.csv`
- ONNX parity(온엑스 동등성): `stages/stage_frontier_16__edge_quality_risk_veto_density_transfer_onnx_scout/02_runs/frontier16B_edge_quality_risk_veto_proxy_scout_v1/onnx_parity.csv`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
