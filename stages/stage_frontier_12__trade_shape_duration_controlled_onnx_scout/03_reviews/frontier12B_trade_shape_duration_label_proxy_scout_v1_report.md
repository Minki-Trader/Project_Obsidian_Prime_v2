# Frontier12B Trade Shape Duration Label Proxy Scout(프론티어12B 거래 형상 보유 기간 라벨 프록시 탐색)

Updated(갱신): 2026-06-14T00:24:46Z

Status(상태): `trade_shape_duration_no_strict_clue_no_authority`

Judgment(판정): `negative_memory_candidate(부정 기억 후보)`

## Action And Effect(행동과 효과)

Action(행동): train-only scale(학습 전용 척도)로 3개 trade-shape label variants(거래 형상 라벨 변형)를 만들고, fixed argmax ONNX models(고정 최대확률 온엑스 모델)을 학습했습니다.

Effect(효과): label source(라벨 원천)를 바꿨을 때 validation/OOS DD(검증/표본밖 손실폭), density(빈도), PF(수익 팩터), smoothness(매끄러움)가 동시에 가까워지는지 봅니다.

## Result Summary(결과 요약)

- candidate rows(후보 행): `9`
- strict scout clue rows(엄격 탐색 단서 행): `0`
- preserved clue rows(보존 단서 행): `0`
- best candidate(최고 후보): `f12b_fast_shape_h6_e2_t0p72_cap0p42_ecap0p24_rec0p08__lr_plain`
- validation PF/density/DD(검증 수익 팩터/빈도/손실폭): `0.964967` / `2.21311` / `30.4882%`
- OOS PF/density/DD(표본밖 수익 팩터/빈도/손실폭): `1.88145` / `0.641221` / `3.03685%`
- worst subperiod DD(최악 하위기간 손실폭): `30.4882%`

## Artifacts(산출물)

- candidate summary(후보 요약): `stages/stage_frontier_12__trade_shape_duration_controlled_onnx_scout/02_runs/frontier12B_trade_shape_duration_label_proxy_scout_v1/candidate_summary.csv`
- model metrics(모델 지표): `stages/stage_frontier_12__trade_shape_duration_controlled_onnx_scout/02_runs/frontier12B_trade_shape_duration_label_proxy_scout_v1/model_metrics.csv`
- subperiod metrics(하위기간 지표): `stages/stage_frontier_12__trade_shape_duration_controlled_onnx_scout/02_runs/frontier12B_trade_shape_duration_label_proxy_scout_v1/subperiod_metrics.csv`
- ONNX parity(온엑스 동등성): `stages/stage_frontier_12__trade_shape_duration_controlled_onnx_scout/02_runs/frontier12B_trade_shape_duration_label_proxy_scout_v1/onnx_parity.csv`
- run manifest(실행 목록): `stages/stage_frontier_12__trade_shape_duration_controlled_onnx_scout/02_runs/frontier12B_trade_shape_duration_label_proxy_scout_v1/run_manifest.json`

## Claim Boundary(주장 경계)

completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다. WFO/MT5(WFO/MT5)는 strict scout clue(엄격 탐색 단서)와 Grok pre-expensive review(그록 비싼 검증 전 검토) 전에는 실행하지 않습니다.

## Next Action(다음 행동)

`frontier12C_trade_shape_duration_repair_or_closeout_decision_v1`. Action(행동): strict clue(엄격 단서)가 있으면 Grok pre-expensive review(그록 비싼 검증 전 검토)로 가고, 없으면 repair/closeout decision(수리/마감 결정)으로 갑니다. Effect(효과): proxy scout(프록시 탐색)를 completion candidate(완성 후보)로 과장하지 않습니다.
