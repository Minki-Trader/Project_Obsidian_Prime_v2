# Frontier18B Asymmetric Exit Lifecycle Proxy Scout(전선18B 비대칭 청산 생명주기 프록시 탐색)

Updated(갱신): 2026-06-14T04:42:17Z

Status(상태): `asymmetric_exit_lifecycle_no_forward_clue_no_authority`

Judgment(판정): `negative_memory_candidate(부정 기억 후보)`

## Action And Effect(행동과 효과)

Action(행동): fixed fwd12 entry ONNX models(고정 fwd12 진입 ONNX 모델)에 3 pre-registered lifecycle profiles(사전 등록 생명주기 프로필)를 붙여 validation/OOS(검증/표본외) proxy path(프록시 경로)를 시뮬레이션했습니다.

Effect(효과): F17 loss-cluster firewall(손실 군집 방화벽)을 상속하지 않고, 이번 가설의 exit lifecycle(청산 생명주기) 축이 PF/density/DD/smoothness(PF/빈도/손실폭/매끄러움)에 주는 영향을 분리해서 봅니다.

## Result Summary(결과 요약)

- candidate rows(후보 행): `9`
- strict scout clue rows(엄격 탐색 단서 행): `0`
- seed surface rows(씨앗 표면 행): `0`
- preserved clue rows(보존 단서 행): `0`
- best candidate(최선 후보): `f18b_hold6_reverse_atr1p5_tp3p0__lr_plain__lifecycle`
- validation PF/density/DD(검증 PF/빈도/손실폭): `1.03878` / `9.42697` / `8.87262%`
- OOS PF/density/DD(표본외 PF/빈도/손실폭): `0.99953` / `10.5873` / `7.60684%`
- worst subperiod DD(최악 하위기간 손실폭): `8.87262%`
- negative subperiod fraction(부정 하위기간 비율): `0.409091`
- ONNX parity(ONNX 동등성): `True`

## Artifacts(산출물)

- candidate summary(후보 요약): `stages/stage_frontier_18__asymmetric_exit_lifecycle_profit_lock_onnx_scout/02_runs/frontier18B_asymmetric_exit_lifecycle_proxy_scout_v1/candidate_summary.csv`
- model metrics(모델 지표): `stages/stage_frontier_18__asymmetric_exit_lifecycle_profit_lock_onnx_scout/02_runs/frontier18B_asymmetric_exit_lifecycle_proxy_scout_v1/model_metrics.csv`
- subperiod metrics(하위기간 지표): `stages/stage_frontier_18__asymmetric_exit_lifecycle_profit_lock_onnx_scout/02_runs/frontier18B_asymmetric_exit_lifecycle_proxy_scout_v1/subperiod_metrics.csv`
- trade log(거래 기록): `stages/stage_frontier_18__asymmetric_exit_lifecycle_profit_lock_onnx_scout/02_runs/frontier18B_asymmetric_exit_lifecycle_proxy_scout_v1/trade_log.csv`
- ONNX parity(ONNX 동등성): `stages/stage_frontier_18__asymmetric_exit_lifecycle_profit_lock_onnx_scout/02_runs/frontier18B_asymmetric_exit_lifecycle_proxy_scout_v1/onnx_parity.csv`
- run manifest(실행 목록): `stages/stage_frontier_18__asymmetric_exit_lifecycle_profit_lock_onnx_scout/02_runs/frontier18B_asymmetric_exit_lifecycle_proxy_scout_v1/run_manifest.json`

## Boundaries(경계)

Evidence boundary(근거 경계): proxy-only(프록시 전용)이며, Python OHLC lifecycle simulation(파이썬 OHLC 생명주기 시뮬레이션)은 MT5 runtime parity(MT5 런타임 동등성)가 아닙니다.

Missing evidence(부족 근거): WFO(워크포워드 최적화), stress(스트레스), MT5 runtime probe(MT5 런타임 탐침)는 아직 실행하지 않았습니다.

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.

Next action(다음 행동): `frontier18C_asymmetric_exit_lifecycle_repair_or_closeout_decision_v1`. Effect(효과): 비싼 WFO/MT5(워크포워드/MT5) 또는 repair/closeout(수리/마감) 전 단계에서 claim boundary(주장 경계)를 유지합니다.
