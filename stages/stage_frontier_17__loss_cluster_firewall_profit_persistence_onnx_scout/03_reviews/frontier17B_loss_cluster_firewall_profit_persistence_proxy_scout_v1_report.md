# Frontier17B Loss Cluster Firewall Profit Persistence Proxy Scout(전선17B 손실 군집 방화벽 수익 지속성 프록시 탐색)

Updated(갱신): 2026-06-14T03:44:41Z

Status(상태): `loss_cluster_firewall_preserved_clue_no_authority`

Judgment(판정): `preserved_clue_candidate(보존 단서 후보)`

## Action And Effect(행동과 효과)

Action(행동): 3개 fixed firewall profiles(고정 방화벽 프로필)에 train-only loss-pressure score(학습 전용 손실 압력 점수)와 continuation quality label(지속 품질 라벨)을 적용해 ONNX proxy scout(ONNX 프록시 탐색)를 실행했습니다.

Effect(효과): F15/F16(전선15/16)의 score threshold/edge_margin(점수 임계값/엣지 마진)을 반복하지 않고, 현재 adverse veto(불리 배제)와 모델 continuation prediction(지속 예측)이 동시에 맞는지 확인했습니다.

## Result Summary(결과 요약)

- candidate rows(후보 행): `9`
- strict scout clue rows(엄격 탐색 단서 행): `0`
- seed surface rows(씨앗 표면 행): `0`
- preserved clue rows(보존 단서 행): `3`
- best candidate(최선 후보): `f17b_firewall_h10_ddq75_contq65__lr_plain__firewall_continuation`
- validation PF/density/DD(검증 수익 팩터/빈도/손실폭): `1.30338` / `3.97268` / `13.4384%`
- OOS PF/density/DD(표본밖 수익 팩터/빈도/손실폭): `1.13674` / `5.0916` / `12.7647%`
- worst subperiod DD(최악 하위기간 손실폭): `12.7647%`
- negative subperiod fraction(부정 하위기간 비율): `0.454545`
- ONNX parity(ONNX 동등성): `True`

## Artifacts(산출물)

- candidate summary(후보 요약): `stages/stage_frontier_17__loss_cluster_firewall_profit_persistence_onnx_scout/02_runs/frontier17B_loss_cluster_firewall_profit_persistence_proxy_scout_v1/candidate_summary.csv`
- firewall transfer audit(방화벽 전이 감사): `stages/stage_frontier_17__loss_cluster_firewall_profit_persistence_onnx_scout/02_runs/frontier17B_loss_cluster_firewall_profit_persistence_proxy_scout_v1/firewall_transfer_audit.csv`
- model metrics(모델 지표): `stages/stage_frontier_17__loss_cluster_firewall_profit_persistence_onnx_scout/02_runs/frontier17B_loss_cluster_firewall_profit_persistence_proxy_scout_v1/model_metrics.csv`
- subperiod metrics(하위기간 지표): `stages/stage_frontier_17__loss_cluster_firewall_profit_persistence_onnx_scout/02_runs/frontier17B_loss_cluster_firewall_profit_persistence_proxy_scout_v1/subperiod_metrics.csv`
- ONNX parity(ONNX 동등성): `stages/stage_frontier_17__loss_cluster_firewall_profit_persistence_onnx_scout/02_runs/frontier17B_loss_cluster_firewall_profit_persistence_proxy_scout_v1/onnx_parity.csv`
- run manifest(실행 목록): `stages/stage_frontier_17__loss_cluster_firewall_profit_persistence_onnx_scout/02_runs/frontier17B_loss_cluster_firewall_profit_persistence_proxy_scout_v1/run_manifest.json`

## Boundaries(경계)

Evidence boundary(근거 경계): proxy-only(프록시 전용), P2 model-input parity(모델 입력 동등성)와 ONNX parity(ONNX 동등성)까지만 확인했습니다.

Missing evidence(부족 근거): WFO(워크포워드 최적화), stress(스트레스), MT5 runtime probe(MT5 런타임 탐침)는 아직 실행하지 않았습니다.

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.

Next action(다음 행동): `frontier17C_grok_pre_expensive_loss_cluster_firewall_review_v1`. Effect(효과): expensive WFO/MT5(비싼 WFO/MT5) 또는 closeout(마감)으로 가기 전에 Grok second opinion(그록 2차 의견)과 local verification(로컬 검증)을 거칩니다.
