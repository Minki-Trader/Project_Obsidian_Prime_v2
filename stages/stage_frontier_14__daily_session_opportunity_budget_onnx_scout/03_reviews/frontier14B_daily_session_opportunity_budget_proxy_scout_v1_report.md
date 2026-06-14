# Frontier14B Daily/Session Opportunity Budget Proxy Scout(프론티어14B 일별/세션별 기회 예산 프록시 탐색)

Updated(갱신): 2026-06-14T01:16:44Z

Status(상태): `opportunity_budget_preserved_clue_no_authority`

Judgment(판정): `preserved_clue_candidate(보존 단서 후보)`

Action(행동): pre-registered quota labels(사전 등록 할당 라벨) 3개와 fixed argmax ONNX models(고정 최대확률 온엑스 모델)를 학습/평가했습니다.

Effect(효과): label-side opportunity density(라벨 쪽 기회 빈도)와 model argmax density(모델 최대확률 빈도)를 분리해서 upstream frequency label(상류 빈도 라벨)이 모델로 전달되는지 측정했습니다.

## Result Summary(결과 요약)

- candidate rows(후보 행): `9`
- strict scout clue rows(엄격 탐색 단서 행): `0`
- preserved clue rows(보존 단서 행): `2`
- best candidate(최고 후보): `f14b_cash_q8_h8__lr_plain`
- validation PF/density/DD(검증 수익 팩터/빈도/손실폭): `0.709064` / `0.0983607` / `6.75478%`
- OOS PF/density/DD(표본밖 수익 팩터/빈도/손실폭): `3.35673` / `0.0687023` / `0.388877%`
- worst subperiod DD(최악 하위기간 손실폭): `6.72419%`

## Artifacts(산출물)

- candidate summary(후보 요약): `stages/stage_frontier_14__daily_session_opportunity_budget_onnx_scout/02_runs/frontier14B_daily_session_opportunity_budget_proxy_scout_v1/candidate_summary.csv`
- label/model density gap(라벨/모델 빈도 격차): `stages/stage_frontier_14__daily_session_opportunity_budget_onnx_scout/02_runs/frontier14B_daily_session_opportunity_budget_proxy_scout_v1/label_model_density_gap.csv`
- ONNX parity(온엑스 동등성): `stages/stage_frontier_14__daily_session_opportunity_budget_onnx_scout/02_runs/frontier14B_daily_session_opportunity_budget_proxy_scout_v1/onnx_parity.csv`
- run manifest(실행 목록): `stages/stage_frontier_14__daily_session_opportunity_budget_onnx_scout/02_runs/frontier14B_daily_session_opportunity_budget_proxy_scout_v1/run_manifest.json`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
